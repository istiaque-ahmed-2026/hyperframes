#!/usr/bin/env python3
"""Local MP4 title cards and captioned trims for ChatGPT's FFmpeg workflow."""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

LOCAL_INPUT = ["-protocol_whitelist", "file,pipe", "-format_whitelist", "mov,matroska,webm,avi,mpeg,mpegts,flv,ogg"]

BUNDLED_FONT = Path(__file__).resolve().parents[1] / "starter/assets/NotoSansBengali-Bold.ttf"


def probe(path):
    cmd = ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", *LOCAL_INPUT, str(path)]
    return json.loads(subprocess.check_output(cmd))


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("expected a finite positive number")
    return number


def ass_text(text):
    # Keep authored lines plain. ASS override blocks and escapes change appearance.
    if any(c in text for c in "{}\\\n\r"):
        raise ValueError("use one line of plain text without braces or backslashes")
    return text


def card_script(args, folder):
    if "," in args.font:
        raise ValueError("font family must not contain a comma")
    w, h = (720, 1280) if args.portrait else (1280, 720)
    end = round(args.duration * 100)
    end_time = f"{end // 360000}:{end // 6000 % 60:02}:{end // 100 % 60:02}.{end % 100:02}"
    styles = []
    lines = []
    for name, size, color, y, text in [
        ("Series", 22, "&H0086C4FF", .16, args.label),
        ("Title", 74, "&H00EBF4FF", .40, args.title),
        ("Subtitle", 34, "&H00D3DCD6", .58, args.subtitle),
    ]:
        styles.append(f"Style: {name},{ass_text(args.font)},{size},{color},&H00000000,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1")
        x, baseline = int(w*.10), int(h*y)
        motion = r"{\move(%d,%d,%d,%d,0,450)\fad(180,0)}" % (x, baseline+14, x, baseline)
        lines.append(f"Dialogue: 0,0:00:00.00,{end_time},{name},,0,0,0,,{motion}{ass_text(text)}")
    header = f"[Script Info]\nScriptType: v4.00+\nPlayResX: {w}\nPlayResY: {h}\nWrapStyle: 2\n"
    style_format = "Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding"
    events = "Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"
    (folder / "card.ass").write_text(header + "\n[V4+ Styles]\nFormat: " + style_format + "\n" + "\n".join(styles) + "\n[Events]\nFormat: " + events + "\n" + "\n".join(lines), encoding="utf-8")
    return ["-f", "lavfi", "-i", f"color=c=0x101C27:s={w}x{h}:r=30",
            "-t", str(args.duration), "-vf",
            "drawbox=x=iw*.1:y=ih*.78:w=iw*.8:h=2:color=0x788487:t=fill,ass=card.ass:fontsdir=fonts"]


def cut_args(args, folder):
    source = args.source.resolve(strict=True)
    meta = probe(source)
    if not any(s["codec_type"] == "video" and not s.get("disposition", {}).get("attached_pic") for s in meta["streams"]):
        raise ValueError("source has no video stream")
    video = next(
        stream for stream in meta["streams"]
        if stream["codec_type"] == "video" and not stream.get("disposition", {}).get("attached_pic")
    )
    if video.get("color_transfer") in {"smpte2084", "arib-std-b67"} or video.get("color_primaries") == "bt2020":
        raise ValueError("HDR/wide-gamut footage needs the HyperFrames color-managed workflow")
    length = float(video.get("duration", meta["format"]["duration"]))
    if not (0 <= args.start < args.end <= length + .001):
        raise ValueError(f"choose a range within 0–{length:g} seconds")
    cmd = ["-ss", str(args.start), *LOCAL_INPUT, "-i", str(source), "-t", str(args.end-args.start),
           "-map", "0:V:0", "-map", "0:a:0?"]
    filters = ["pad=ceil(iw/2)*2:ceil(ih/2)*2"]
    if args.srt:
        shutil.copyfile(args.srt, folder / "captions.srt")
        filters.append("subtitles=captions.srt:fontsdir=fonts")
    return cmd + ["-vf", ",".join(filters), "-c:a", "aac", "-b:a", "192k"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_subparsers(dest="mode", required=True)
    card = mode.add_parser("card", help="create an animated editorial title card")
    card.add_argument("--title", required=True)
    card.add_argument("--subtitle", default="")
    card.add_argument("--label", default="MOTION STUDIES  /  01")
    card.add_argument("--font", default="Noto Sans Bengali")
    card.add_argument("--duration", type=positive, default=4)
    card.add_argument("--portrait", action="store_true")
    cut = mode.add_parser("cut", help="trim SDR footage, optionally burning UTF-8 SRT cues")
    cut.add_argument("source", type=Path)
    cut.add_argument("--start", type=float, default=0)
    cut.add_argument("--end", type=positive, required=True)
    cut.add_argument("--srt", type=Path, help="cue times relative to the edited clip")
    for sub in (card, cut):
        sub.add_argument("--font-file", type=Path, default=BUNDLED_FONT, help="local font (defaults to bundled Noto Sans Bengali)")
        sub.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.absolute()
    if out.suffix.lower() != ".mp4" or out.exists():
        parser.error("choose a fresh .mp4 output path")
    try:
        with tempfile.TemporaryDirectory(dir=out.parent) as temp:
            folder = Path(temp)
            (folder / "fonts").mkdir()
            if args.font_file:
                shutil.copyfile(args.font_file, folder / "fonts" / args.font_file.name)
            inputs = card_script(args, folder) if args.mode == "card" else cut_args(args, folder)
            rendered = folder / "render.mp4"
            subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", *inputs,
                            "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-movflags", "+faststart", str(rendered)], cwd=folder, check=True)
            info = probe(rendered)
            if not any(s["codec_type"] == "video" for s in info["streams"]):
                raise ValueError("render contains no video")
            os.link(rendered, out)  # Atomic publish, including concurrent callers.
            print(json.dumps({"file": str(out), "duration": info["format"]["duration"]}))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Video job failed: {error}\n")


if __name__ == "__main__":
    main()
