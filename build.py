"""Build the standalone, offline-capable learning page."""
import json
import base64
from pathlib import Path

root = Path(__file__).resolve().parent
poems = json.loads((root / "poems.json").read_text())
assert len(poems) == 100 and sorted(p["id"] for p in poems) == list(range(1, 101))
for poem in poems:
    assert len(poem["jp"]) == len(poem["kana"]) == 5, poem["id"]
    assert poem["meaning"] and 1 <= len(poem["kimariji"]) <= 6, poem["id"]
sources = json.loads((root / "sources.json").read_text())
template = (root / "index.html.in").read_text()
def payload(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
html = template.replace("__POEMS_JSON__", payload(poems)).replace("__SOURCES_JSON__", payload(sources))
font = base64.b64encode((root / "shippori-mincho-subset.ttf").read_bytes()).decode()
html = html.replace("__FONT_BASE64__", font)
(root / "index.html").write_text(html)
print(f"Built {root / 'index.html'} ({len(html.encode()) // 1024} KiB)")
