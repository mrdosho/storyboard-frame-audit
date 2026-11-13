"""Check a storyboard folder for missing A/B frames."""
import argparse
import csv
import re
import sys
from pathlib import Path

FRAME = re.compile(r"S([0-9]+)_([AB])\.(png|jpe?g|webp)", re.IGNORECASE)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--scenes", type=int, required=True,
                        help="Number of scenes, numbered from 1")
    args = parser.parse_args()
    if not args.folder.is_dir() or args.scenes < 1:
        parser.error("provide an existing folder and a positive scene count")

    frames = {}
    for path in sorted(args.folder.iterdir()):
        match = FRAME.fullmatch(path.name)
        if match and path.is_file():
            key = int(match[1]), match[2].upper()
            frames.setdefault(key, []).append(path)

    report = csv.writer(sys.stdout, lineterminator="\n")
    report.writerow(("scene", "frame", "status", "file"))
    problems = False
    for scene in range(1, args.scenes + 1):
        for frame in ("A", "B"):
            paths = frames.get((scene, frame), [])
            if not paths:
                report.writerow((scene, frame, "missing", ""))
                problems = True
            for path in paths:
                status = "duplicate" if len(paths) > 1 else "ok"
                if path.stat().st_size == 0:
                    status = "empty" if status == "ok" else "duplicate-empty"
                report.writerow((scene, frame, status, path.name))
                problems |= status != "ok"
    for (scene, frame), paths in sorted(frames.items()):
        if scene < 1 or scene > args.scenes:
            for path in paths:
                report.writerow((scene, frame, "unexpected", path.name))
            problems = True
    return int(problems)


if __name__ == "__main__":
    sys.exit(main())
