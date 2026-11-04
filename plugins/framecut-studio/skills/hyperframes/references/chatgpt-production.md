# Video production in ChatGPT

A request to inspect a repository calls for a review. For an install request use the host's plugin installation surface and verify availability. For video jobs use the following sequence.

1. Extract the deliverable, audience, language, channel, length, exact copy, brand assets and last approved changes from the conversation. Ask about missing inputs only if they materially affect the cut. A finished-file request includes rendering and verification.
2. Inventory attached files. Probe footage for duration, rotation, dimensions, streams and color transfer. Map edit timestamps to the original source. Keep originals intact and choose a fresh export path. For an existing HyperFrames project inspect the timeline and patch the affected scene.
3. For multiscene animation or compositing, use the bundled release-pinned launcher and linked specialist skills. Check Node 22+, npm, FFmpeg, ffprobe and whether a browser can launch. Work in a writable project. Copy starter/ for a small Bengali motion example. When the user cannot reach a local preview server, deliver rendered frames or a review clip.
4. If only Python and FFmpeg with libass and libx264 work, use the helper below for SDR title cards and trims. For a more complex brief without a browser, deliver the editable project with assets, exact render command and observed blocker. Distinguish a preview, an editable project and an exported MP4. Generated footage, avatars, synthetic voice and transcription depend on the available provider or supplied assets. Confirm paid usage or external transfer of uploaded footage when required.
5. For a multiscene piece, make a timecoded shot plan. Tie each cut to a change of idea or action. Keep a readable final hold. For Bengali use a local font, preserve supplied copy and avoid splitting conjuncts during animation. Check glyphs on a phone-sized frame. Derive captions from verified dialogue or supplied cues. Preserve speech and ambience unless an audio change is requested.
6. Run lint and browser checks for HTML, then render. Probe the exported file for dimensions, duration, frame rate and expected audio. Decode end-to-end with FFmpeg. Inspect opening, middle, caption, transition and final-hold frames. Listen to speech against the music. Fix clipping, black frames, timing errors and missing glyphs. Deliver the MP4 and any requested editable source. Identify checks that could not run.

## Local helper

Resolve scripts/chat-video.py and starter/assets/ relative to this skill. The commands assume that directory as the working directory and existing output folders.

    python3 scripts/chat-video.py card --title "দৃশ্যপট" --subtitle "রেখা থেকে গতি" --duration 4 --font-file starter/assets/NotoSansBengali-Bold.ttf --out /path/to/intro.mp4
    python3 scripts/chat-video.py cut /path/to/source.mp4 --start 2 --end 8 --srt /path/to/cues.srt --font-file starter/assets/NotoSansBengali-Bold.ttf --out /path/to/cut.mp4

Use short single-line card copy. Add --portrait for 720×1280. Landscape uses 1280×720. For longer copy use a wrapping HTML composition. The helper loads the bundled Noto Sans Bengali font by default. Cut times are seconds. SRT times start at zero on the resulting cut. Cut keeps the first video and first available audio, encoding H.264/AAC. The helper rejects HDR and BT.2020 footage. Use the HyperFrames color-managed path for those inputs and an explicit multitrack workflow when more tracks must survive. Choose a fresh .mp4 path on a filesystem with hard links.

## Revisions

For “change the first title only,” identify its file, ID and time span, change its text, then review the title and the cut immediately after it. For a trim of a rendered upload, confirm the timestamp reference only if the original and latest cut differ ambiguously. Report the applied source range and duration in the user's language.
