---
name: sequenceforge-extract
description: "SequenceForge Phase 3 — Frame Extractor. Use after output/video.mp4 exists — whether it came from a provider pipeline or was exported manually. Validates the video file, runs scripts/extract_frames.py (ffmpeg) to extract lossless PNG frames, and saves them to the exact destination directory requested by the user."
---

# Phase 03 — Extract

Your job is to validate the video, run `scripts/extract_frames.py`, and confirm the frames landed where they should.

---

## Step 1 — Gate check

Verify `output/video.mp4` exists and is non-empty. If not:

- If the user chose the **manual path**: tell them to export the video from Flow and save it to `output/video.mp4`, then come back
- If the user chose the **API path**: tell them to run Phase 02 first

---

## Step 2 — Confirm destination

Default destination is `public/images/frames` unless the user passed `--dest`.

If the destination already contains `frame_*.png` files, warn:

```
Warning: <dest> already contains <N> frame files. These will be overwritten. Continue? (y/n)
```

---

## Step 3 — Check ffmpeg

Run `ffmpeg -version` to confirm it's available. If not:

```
ffmpeg is not installed or not on PATH.

Install:
  macOS:   brew install ffmpeg
  Ubuntu:  sudo apt install ffmpeg
  Windows: download from ffmpeg.org, add to PATH
```

---

## Step 4 — Run extract_frames.py

```bash
python scripts/extract_frames.py \
  --input output/video.mp4 \
  --dest <destination> \
  [--fps <fps>]
```

Include `--fps` only if the user specified it. Omitting it extracts at the video's native frame rate.

Frames are saved as lossless PNG (`-compression_level 0`) — no compression artifacts, no flicker between consecutive frames in the scroll sequence.

---

## Step 5 — Report

```
Extraction complete.
  <N> frames -> <destination>/
  First: frame_000001.png
  Last:  frame_<NNNNNN>.png

To use in website-builder:
  /images/frames/frame_000001.png … frame_<NNNNNN>.png
```

---

## Error handling

| Error | Action |
|-------|--------|
| ffmpeg not found | Show install instructions |
| Video file corrupt or 0 bytes | If manual path: re-export from Flow. If API path: re-run Phase 02. |
| No frames extracted | Show ffmpeg stderr for diagnosis |
| Destination write error | Check directory permissions |
