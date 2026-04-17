---
description: Generate media, inspect a GSAP project, and integrate a scroll image sequence into the target section.
---

# /forge-sequence

Generate prompts, produce or receive media, extract frames, inspect a GSAP project, and integrate a canvas image sequence in the project’s existing style.

## Usage

```
/forge-sequence "<scene description>" --project-root <path> --target "<page or section hint>" --dest <path> [--mode manual|provider] [--fps <number>] [--duration <seconds>] [--canvas-id <id>]
```

## Examples

```
/forge-sequence "premium watch reveal from silhouette to dial detail" --project-root ../storefront --target "home hero" --dest ../storefront/public/images/watch-sequence
/forge-sequence "camera dives through cloud layers into a shoe close-up" --project-root ../landing --target "product feature section" --dest ../landing/static/frames/feature --mode provider
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

Before prompt generation, if `docs/design/project-setup.yaml` is missing or incomplete, use the `AskUserQuestion` tool to ask all setup questions in a single call and save the answers. On resume runs where all eight fields are already present, skip the questions.

Wait for user approval before generating media.

---

### Step 2 — Choose media path

If the user supplied `--mode provider`, invoke `sequenceforge-generate`.

Otherwise use the manual path:
- show the user the three prompts
- tell them where to save the outputs:
  - `output/frame-first.png`
  - `output/frame-last.png`
  - `output/video.mp4`
- wait for the files to exist before proceeding

---

### Step 3 — Extract frames

Invoke `sequenceforge-extract` with the exact `--dest` path from the command.

---

### Step 4 — Inspect the target project

Invoke `sequenceforge-inspect` with:
- the project root
- the target hint
- the extracted frames destination

This should run:

```bash
python scripts/inspect_project.py \
  --project-root <project-root> \
  --target-hint "<target>" \
  --frames-dest <dest>
```

If multiple plausible targets are tied, stop and ask the user which file/section to use.

---

### Step 5 — Apply the integration

Invoke `sequenceforge-integrate`.

This should first build the blueprint:

```bash
python scripts/plan_integration.py \
  --prompt "<scene description>" \
  --project-root <project-root> \
  --target-hint "<target>" \
  --frames-dest <dest> \
  --generation-mode <manual|provider> \
  --fps <fps> \
  --duration <duration> \
  --canvas-id <canvas-id>
```

Then apply it directly to the target project:

```bash
python scripts/apply_integration.py \
  --prompt "<scene description>" \
  --project-root <project-root> \
  --target-hint "<target>" \
  --frames-dest <dest> \
  --generation-mode <manual|provider> \
  --fps <fps> \
  --duration <duration> \
  --canvas-id <canvas-id>
```

This must update the target project directly:
- insert the canvas in the chosen section
- apply the matching style strategy
- add the image-sequence helper if missing
- extend the project’s existing GSAP organization rather than replacing it

---

### Step 6 — Final report

Report:
- where the frames were written
- which project files were updated
- which file contains the GSAP sequence integration
- any assumptions that were applied automatically
