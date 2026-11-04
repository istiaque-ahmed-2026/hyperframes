# HyperFrames rendering contract

Use an existing approved HyperFrames installation. Run in the user's writable project, with the installed skill treated as read-only. A renderer may need Node, Chrome, FFmpeg and local animation libraries. Check their availability through the host's normal tools. Let the host handle any authorized setup.

## Structure and timing

Use index.html as the root composition, compositions/ for scenes and assets/ for local media and fonts. Set the root's data-composition-id, data-duration, data-width, data-height and data-fps. Mount scenes with data-composition-src.

Give timed elements class="clip", data-start and data-duration in seconds. A clip appears over [start, start + duration). Keep its final visible state just before its end. Use z-index for paint order and data-track-index for editor lanes.

Register one paused GSAP timeline per composition on window.__timelines after building its tweens. Use the installed approved local GSAP library when needed. For supported CSS-only compositions, data-no-timeline permits the renderer to use finite CSS animation without waiting for a GSAP timeline.

Make each frame a function of timeline time. Avoid runtime network requests, wall-clock time, timers, unseeded randomness and infinite animation. Never manually play or seek media; the renderer owns playback.

Animate a child of a clip rather than its visibility or display. Keep GSAP-transformed elements free of conflicting CSS transforms. Prefer transforms over layout properties.

Place scene markup, styles and scripts inside a template and use #root for its scoped root. Use relative assets/ paths from compositions. The bundled starter demonstrates this structure.

## Media and editing

Give every audio element an id. Keep intentional video audio with data-has-audio="true" and explicitly mute video used only as picture. Use separate audio elements for music, narration and replacement sound.

Use @font-face with local font files. Keep the Bengali font license when distributing a project containing it. Avoid character animation that separates Bengali conjuncts. Keep source footage intact and make revised exports.

A simple trim through the local helper retains the first video and first available audio stream. Use a suitable approved multitrack renderer when more streams must survive. Use explicit color management for HDR.

## Commands

Check the installed CLI's help. For a compatible HyperFrames installation, the normal order is:

    hyperframes lint /project
    hyperframes check /project --json
    hyperframes render /project --strict --no-best-effort -o /project/render.mp4

Review the reported findings and actual rendered frames. A successful process exit alone does not prove the intended visual result.
