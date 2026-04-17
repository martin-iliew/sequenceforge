---
description: Generate the prompt pack and extract a numbered PNG frame sequence from a scene description.
---

# /forge-frames

Generate the two image prompts, the video prompt, and a scroll-ready PNG frame sequence. This is the media-only workflow; use `/forge-sequence` when you also want the target project inspected and updated.

## Usage

```
/forge-frames "<scene description>" [--dest <path>] [--mode manual|provider] [--fps <number>]
```

## Examples

```
/forge-frames "a cinematic descent from mountain peak to forest floor"
/forge-frames "premium watch product reveal, dark editorial studio" --dest public/images/hero-frames
/forge-frames "sunrise over a calm ocean, camera slowly pulling back" --fps 24 --mode provider
```

## Instructions for Claude

When this command is invoked:

### Step 1 — Write the prompts

Invoke the `sequenceforge-spec` skill with the user’s scene description.

This must produce:
- a start-image prompt
- an end-image prompt
- a video-motion prompt
- `output/frame-spec.yaml`

Before prompt generation, if `docs/design/project-setup.yaml` is missing or incomplete, use the `AskUserQuestion` tool to ask the full setup questionnaire in one call and save the answers there. If all eight fields already exist, skip that question step.

Wait for the user to approve the prompt set before proceeding.

---

### Step 2 — Generate or receive the media

If the user chose `--mode provider`, invoke `sequenceforge-generate`.

Otherwise use the manual path:
- show the user the start-image, end-image, and video prompts
- tell them to save the exported files to:
  - `output/frame-first.png`
  - `output/frame-last.png`
  - `output/video.mp4`
- wait for the user to confirm the files are ready

---

### Step 3 — Extract frames

Invoke `sequenceforge-extract` with the provided `--dest` path.

Default destination: `public/images/frames`

---

### Step 4 — Final report

Report:
- the destination folder
- frame count
- first and last frame filenames
- the public URL pattern that can be used by a GSAP image sequence
