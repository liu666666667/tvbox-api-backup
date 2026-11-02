import json
from pathlib import Path

TVBOX_DIR = Path("tvbox")
count = 0
for f in TVBOX_DIR.glob("*.json"):
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        continue
    if isinstance(data, dict) and "livebak" in data:
        del data["livebak"]
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[ok] removed lives: {f.name}")
        count += 1
print(f"done, {count} files changed")
