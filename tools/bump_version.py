import json
import os
import re
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "src", "djs_pyqt6.py")
STATE = os.path.join(ROOT, "tools", "version_state.json")


def suffix_for(count):
    index = count - 1
    letters = ""
    while index > 0:
        index, rem = divmod(index - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def main():
    if len(sys.argv) != 2:
        print("usage: python bump_version.py <external_version>")
        return 2
    version = sys.argv[1].strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        print("external version must use MAJOR.MINOR.PATCH")
        return 2
    today = datetime.now().strftime("%Y%m%d")
    state = {}
    if os.path.exists(STATE):
        with open(STATE, "r", encoding="utf-8") as handle:
            state = json.load(handle)
    count = int(state.get("count") or 0) + 1 if state.get("date") == today else 1
    internal = today + suffix_for(count)
    with open(SOURCE, "r", encoding="utf-8") as handle:
        source = handle.read()
    source, n1 = re.subn(r'(self\.current_version\s*=\s*)"[^"]*"',
                         lambda m: m.group(1) + '"%s"' % version, source, count=1)
    source, n2 = re.subn(r'(self\.build_version\s*=\s*)(?:"[^"]*"|\d+)',
                         lambda m: m.group(1) + '"%s"' % internal, source, count=1)
    if n1 != 1 or n2 != 1:
        print("version constants not found or ambiguous")
        return 1
    if os.path.exists(STATE):
        if os.path.getmtime(SOURCE) - os.path.getmtime(STATE) > 60:
            print("提醒: djs_pyqt6.py 在最近一次版本写入后被修改过，本次为补号")
    with open(SOURCE, "w", encoding="utf-8") as handle:
        handle.write(source)
    with open(STATE, "w", encoding="utf-8") as handle:
        json.dump({"date": today, "count": count, "external": version, "internal": internal},
                  handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print("external=%s internal=%s count=%d" % (version, internal, count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
