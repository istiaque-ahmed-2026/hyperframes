"""Exercise the installed plugin helper against actual video and audio."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/framecut-studio/skills/hyperframes"
HELPER = [sys.executable, str(SKILL / "scripts/chat-video.py")]


def run(*args):
    return subprocess.run(args, check=True, capture_output=True).stdout


def streams(path):
    data = run("ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path)
    return json.loads(data)


with tempfile.TemporaryDirectory() as directory:
    d = Path(directory)
    intro, source, cut = [d / name for name in ("intro.mp4", "source.mp4", "cut.mp4")]
    run(*HELPER, "card", "--portrait", "--duration", "1", "--title", "আলো",
        "--font-file", SKILL / "starter/assets/NotoSansBengali-Bold.ttf", "--out", intro)
    video = streams(intro)["streams"][0]
    assert (video["width"], video["height"], video["nb_frames"]) == (720,1280,"30")
    run("ffmpeg", "-v", "error", "-i", intro, "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", source)
    cues = d / "cues.srt"
    cues.write_text("1\n00:00:00,000 --> 00:00:00,500\nআলো\n", encoding="utf-8")
    args = [*HELPER, "cut", source, "--start", "0.2", "--end", "0.8", "--srt", cues, "--out", cut]
    run(*args)
    info = streams(cut)
    assert [s["codec_name"] for s in info["streams"]] == ["h264", "aac"]
    assert abs(float(info["format"]["duration"]) - .6) < .05
    run("ffmpeg", "-v", "error", "-xerror", "-i", cut, "-f", "null", "-")
    first = cut.read_bytes()
    assert subprocess.run(args, capture_output=True).returncode != 0 and cut.read_bytes() == first
    bad = d / "bad.mp4"
    assert subprocess.run([*HELPER,"cut",source,"--end","9","--out",bad],capture_output=True).returncode != 0
    assert not bad.exists()
print("Portrait render, captioned trim, audio, decode, overwrite and range checks passed.")
