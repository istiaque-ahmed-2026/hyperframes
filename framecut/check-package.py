"""Verify a portable Framecut bundle against the recorded upstream inventory."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/framecut-studio"
inventory = json.loads((ROOT / "framecut/upstream-inventory.json").read_text())
manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
runtime = json.loads((PLUGIN / "runtime.json").read_text())
market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())

assert manifest["name"] == "framecut-studio"
assert runtime["upstreamCommit"] == inventory["commit"]
assert runtime["hyperframes"] == inventory["version"]
assert market["plugins"][0]["source"]["path"] == "./plugins/framecut-studio"
assert (PLUGIN / "LICENSE").is_file()
assert (PLUGIN / "NOTICE").is_file()
skills = sorted(path.parent.name for path in (PLUGIN / "skills").glob("*/SKILL.md"))
assert skills == inventory["skills"], skills

for relative, expected in inventory["files"].items():
    file = PLUGIN / relative
    assert file.is_file(), f"Missing upstream file: {relative}"
    if relative not in inventory["adapted"]:
        actual = hashlib.sha256(file.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        assert actual == expected, f"Unexpected upstream modification: {relative}"

for relative in [
    "skills/hyperframes/references/chatgpt-production.md",
    "skills/hyperframes/scripts/chat-video.py",
    "skills/hyperframes/starter/index.html",
    "skills/hyperframes/starter/compositions/card.html",
    "skills/hyperframes/starter/assets/NotoSansBengali-Bold.ttf",
    "skills/hyperframes/starter/assets/FONT-LICENSE.txt",
]:
    assert (PLUGIN / relative).is_file(), relative

print(f"Verified {len(skills)} skills and {len(inventory['files'])} upstream files, runtime pin and added assets.")
