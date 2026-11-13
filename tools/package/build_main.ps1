$ErrorActionPreference = "Stop"
$Package = $PSScriptRoot
$Root = Split-Path -Parent (Split-Path -Parent $Package)
$Dist = Join-Path $Root "dist"
$Work = Join-Path $Root "build"
$Source = Join-Path $Root "src\djs_pyqt6.py"
$Icon = Join-Path $Root "data\djstp.ico"
$Iscc = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if (!(Test-Path $Source)) { throw "source not found: $Source" }
if (!(Test-Path $Icon)) { throw "icon not found: $Icon" }
if (!(Test-Path $Iscc)) { throw "Inno Setup not found: $Iscc" }

$text = Get-Content $Source -Raw
$match = [regex]::Match($text, 'self\.current_version = "([^"]+)"')
if (!$match.Success) { throw "version not found in $Source" }
$Version = $match.Groups[1].Value

if (Test-Path $Dist) { Remove-Item $Dist -Recurse -Force }
if (Test-Path $Work) { Remove-Item $Work -Recurse -Force }
New-Item -ItemType Directory -Force -Path $Dist, $Work | Out-Null

$parts = $Version.Split('.')
while ($parts.Count -lt 4) { $parts += "0" }
$v4 = ($parts[0..3] -join ", ")
$VersionFile = Join-Path $Work "version_info.txt"
$vi = @"
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=($v4),
    prodvers=($v4),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '080404B0',
        [StringStruct('CompanyName', 'GuZhi'),
         StringStruct('FileDescription', '倒计时·DJS'),
         StringStruct('FileVersion', '$Version'),
         StringStruct('InternalName', 'DJS'),
         StringStruct('LegalCopyright', 'Copyright (C) 2026 GuZhi'),
         StringStruct('OriginalFilename', 'DJS.exe'),
         StringStruct('ProductName', '倒计时·DJS'),
         StringStruct('ProductVersion', '$Version')])
    ]),
    VarFileInfo([VarStruct('Translation', [2052, 1200])])
  ]
)
"@
[IO.File]::WriteAllText($VersionFile, $vi, (New-Object Text.UTF8Encoding($false)))

python -m PyInstaller --noconfirm --clean --windowed --onefile --noupx --name DJS --icon $Icon --version-file $VersionFile --collect-all qtawesome --distpath $Dist --workpath $Work --specpath $Work $Source
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed" }

$Stage = Join-Path $Dist "DJS"
New-Item -ItemType Directory -Force -Path $Stage | Out-Null
Copy-Item (Join-Path $Dist "DJS.exe") $Stage -Force
Copy-Item (Join-Path $Root "data") $Stage -Recurse -Force
Copy-Item (Join-Path $Root "LICENSE") $Stage -Force

$CertThumb = $env:DJS_SIGN_CERT
function Sign-Exe($path) {
    if (!$CertThumb) { return }
    $cert = Get-Item "Cert:\CurrentUser\My\$CertThumb" -ErrorAction Stop
    try {
        $result = Set-AuthenticodeSignature -FilePath $path -Certificate $cert -HashAlgorithm SHA256 -TimestampServer "http://timestamp.digicert.com" -ErrorAction Stop
    } catch {
        $result = Set-AuthenticodeSignature -FilePath $path -Certificate $cert -HashAlgorithm SHA256 -ErrorAction Stop
    }
    Write-Host "Signed $path : $($result.Status)"
}

Sign-Exe (Join-Path $Stage "DJS.exe")

& $Iscc "/DMyAppVersion=$Version" (Join-Path $Package "DJS.iss")
if ($LASTEXITCODE -ne 0) { throw "Inno Setup failed" }

$Installer = Join-Path $Dist "installer\DJS_Setup_$Version.exe"
$Portable = Join-Path $Dist "installer\DJS_Portable_$Version.zip"
Sign-Exe $Installer
Compress-Archive -Path (Join-Path $Dist "DJS\*") -DestinationPath $Portable -Force

$hashFile = Join-Path $Dist "installer\SHA256SUMS.txt"
$lines = @()
foreach ($file in @($Installer, $Portable)) {
    $hash = (Get-FileHash $file -Algorithm SHA256).Hash.ToLower()
    $lines += "$hash  $(Split-Path -Leaf $file)"
}
$lines | Set-Content -Path $hashFile -Encoding ASCII

Write-Host "Installer: $Installer"
Write-Host "Portable:  $Portable"
Write-Host "Checksums: $hashFile"
