import json
import pathlib
import urllib.request

SRC = "https://raw.githubusercontent.com/liu666666667/awesome-zhuiju-free/main/resources/resources.json"
MY_FILE = pathlib.Path("api_list.json")
WANTED = {"tvbox_config"}

def norm(u: str) -> str:
    return (u or "").strip().rstrip("/")

def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

up = fetch_json(SRC)
items = up.get("resources", up) if isinstance(up, dict) else up

data = json.loads(MY_FILE.read_text(encoding="utf-8"))
api_list = data.setdefault("API_LIST", [])
mirrors = data.setdefault("API_MIRRORS", {})

seen = set()
for pair in api_list:
    if isinstance(pair, list) and len(pair) >= 2:
        seen.add(norm(pair[1]))
for name, urls in mirrors.items():
    if isinstance(urls, list):
        for u in urls:
            seen.add(norm(u))

list_names = {
    pair[0]: i
    for i, pair in enumerate(api_list)
    if isinstance(pair, list) and pair
}

added_list = added_mirror = 0
for it in items:
    if it.get("category") not in WANTED:
        continue

    # 只排除明确不可用的，caution 放行
    verify = (it.get("verification") or {}).get("status")
    if verify in ("removed", "temporarily_unavailable"):
        continue

    url = (it.get("link_url") or it.get("url") or "").strip()
    if not url:
        continue
    key = norm(url)
    if key in seen:
        continue

    name = it.get("name") or it.get("title") or "未命名"
    seen.add(key)

    if name in mirrors and isinstance(mirrors[name], list):
        mirrors[name].append(url)
        added_mirror += 1
    elif name in list_names:
        mirrors.setdefault(name, []).append(url)
        added_mirror += 1
    else:
        api_list.append([name, url])
        list_names[name] = len(api_list) - 1
        added_list += 1

MY_FILE.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"新增 API_LIST: {added_list} 条，新增 API_MIRRORS 镜像: {added_mirror} 条")
print(f"当前 API_LIST: {len(api_list)} 条，API_MIRRORS: {len(mirrors)} 个名字")
