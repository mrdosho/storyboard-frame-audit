# Storyboard Frame Audit

Audit the A/B frames of a storyboard before packaging its images. Requires Python 3.8+ and no third-party dependencies.

```sh
python audit.py path/to/frames --scenes 21 > audit.csv
```

Name frames like `S01_A.png` and `S01_B.jpg`. The scanner supports PNG, JPEG, and WebP, is case-insensitive, and scans the immediate folder. It reports missing, duplicate, empty, and out-of-range frames. It checks names and file size. Image decoding and visual inspection are separate checks.

Exit codes: 0 when the frame list passes, 1 for frame problems, 2 for invalid arguments.

MIT licensed.
