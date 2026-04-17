---
description: Start the full SequenceForge workflow and ask for any missing details step by step.
---

# /forge-sequence

Start the full SequenceForge workflow from Phase 01 through Phase 06.

The user should be able to run this command with no flags. If details are missing, ask for them as part of the workflow.

## Usage

```text
/forge-sequence
/forge-sequence "<scene description>"
```

## Examples

```text
/forge-sequence
/forge-sequence "premium watch reveal from silhouette to dial detail"
```

## Instructions for Claude

When this command is invoked:

### Step 1 — Collect the minimum input

If the user passed text after the command, treat it as the initial scene description.

If no scene description was passed, ask for it first.

Do not require the user to provide script-style flags up front.

Use these defaults unless the user asks for something else or the project structure makes them clearly wrong:

- project root: current working directory
- generation mode: manual
- fps: 30
- duration: 4 seconds
- canvas id: `image-sequence`
- frames destination: `public/images/sequenceforge`
- target hint: `hero`

If the target project structure makes the default frames destination clearly unsuitable, ask the user for the preferred destination path.

### Step 2 — Write the prompts

Invoke the `sequenceforge-spec` skill with the scene description.

This must produce:

- a start-image prompt
- an end-image prompt
- a video-motion prompt
- `output/frame-spec.yaml`

Before prompt generation, if `docs/design/project-setup.yaml` is missing or incomplete, use the setup questions already defined by the skill and save the answers there.

Wait for user approval before generating or requesting media.

### Step 3 — Generate or receive media

If the user explicitly asks for provider mode, invoke `sequenceforge-generate`.

Otherwise use the manual path:

- show the user the three prompts
- tell them to save the outputs to:
  - `output/frame-first.png`
  - `output/frame-last.png`
  - `output/video.mp4`
- wait for the files to exist before proceeding

### Step 4 — Extract the frame sequence

Invoke `sequenceforge-extract` with the chosen frames destination.

### Step 5 — Inspect the target project

Invoke `sequenceforge-inspect` with:

- the project root
- the target hint
- the extracted frames destination

This should run:

```bash
python scripts/inspect_project.py \
  --project-root <project-root> \
  --target-hint "<target-hint>" \
  --frames-dest <frames-dest>
```

If multiple plausible targets are tied, stop and ask the user which file or section to use.

### Step 6 — Apply the integration

Invoke `sequenceforge-integrate`.

This should first build the blueprint:

```bash
python scripts/plan_integration.py \
  --prompt "<scene description>" \
  --project-root <project-root> \
  --target-hint "<target-hint>" \
  --frames-dest <frames-dest> \
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
  --target-hint "<target-hint>" \
  --frames-dest <frames-dest> \
  --generation-mode <manual|provider> \
  --fps <fps> \
  --duration <duration> \
  --canvas-id <canvas-id>
```

This must update the target project directly:

- insert the canvas in the chosen section
- apply the matching style strategy
- add the image-sequence helper if missing
- extend the project's existing GSAP organization rather than replacing it

### Step 7 — Final report

Report:

- where the frames were written
- which project files were updated
- which file contains the GSAP sequence integration
- any defaults or assumptions that were applied automatically
