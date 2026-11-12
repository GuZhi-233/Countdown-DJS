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

python -m PyInstaller --noconfirm --clean --windowed --onedir --contents-directory . --name DJS --icon $Icon --collect-all qtawesome --add-data "$Root\data;data" --distpath $Dist --workpath $Work --specpath $Work $Source
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed" }

& $Iscc "/DMyAppVersion=$Version" (Join-Path $Package "DJS.iss")
if ($LASTEXITCODE -ne 0) { throw "Inno Setup failed" }

$Installer = Join-Path $Dist "installer\DJS_Setup_$Version.exe"
$Portable = Join-Path $Dist "installer\DJS_Portable_$Version.zip"
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
