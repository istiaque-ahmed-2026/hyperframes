"""Build reviewable plugin and standalone skill archives from committed source."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = "plugins/framecut-studio/"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    changed = git("status", "--porcelain", "--", PLUGIN, "framecut/skill/")
    if changed:
        parser.error("commit the plugin and standalone skill before packaging")
    outputs = []
    for name, prefix in [("framecut-studio-plugin.zip", "framecut-studio/"),
                         ("framecut-video-skill.zip", "framecut-video/")]:
        target = args.out_dir / name
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
            source = "framecut/skill/" if name == "framecut-video-skill.zip" else PLUGIN
            paths = git("ls-tree", "-r", "--name-only", "HEAD", source).decode().splitlines()
            for path in paths:
                relative = path.removeprefix(source)
                if ".." in PurePosixPath(relative).parts or PurePosixPath(relative).is_absolute():
                    raise ValueError(f"unsafe archive path: {relative}")
                mode = git("ls-tree", "HEAD", path).decode().split()[0]
                if mode != "100644":
                    raise ValueError(f"unexpected file mode {mode}: {path}")
                archive.writestr(prefix + relative, git("show", "HEAD:" + path))
        with zipfile.ZipFile(target) as archive:
            assert archive.testzip() is None
        outputs.append({"file": name, "bytes": target.stat().st_size,
                        "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
    result = {"commit": git("rev-parse", "HEAD").decode().strip(), "archives": outputs}
    (args.out_dir / "checksums.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
