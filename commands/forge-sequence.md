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

**Use AskUserQuestion for every missing piece of information — never silently apply defaults for choices the user should make.**

#### 1a — Scene description
If no scene description was passed, use AskUserQuestion to ask for it before doing anything else.

#### 1b — Generation mode
Always use AskUserQuestion to ask the user which mode they want:

> "How would you like to generate the media?
>
> **A — Manual (free):** I'll write the three prompts (start image, end image, video motion). You paste them into any free tool you choose and drop the output files into `output/`. Free options:
> - Images: Ideogram, Adobe Firefly, Leonardo AI, or DALL-E 3 via ChatGPT (all have free tiers)
> - Video: RunwayML Gen-3, Kling AI, Pika, or Luma Dream Machine (all have free tiers)
>
> **B — Provider (automated):** I'll call a connected API to generate everything automatically. Requires API keys and may incur cost."

Wait for the user's answer before proceeding. Set `generation_mode` to `manual` or `provider` based on their choice.

#### 1c — Silent defaults (no need to ask)
Apply these without prompting unless the project structure makes them clearly wrong:

- project root: current working directory
- fps: 30
- duration: 4 seconds
- canvas id: `image-sequence`
- frames destination: `public/images/sequenceforge`
- target hint: `hero`

If the frames destination is clearly unsuitable for this project, use AskUserQuestion to confirm the preferred path.

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

Branch on the `generation_mode` chosen in Step 1b.

#### Manual path
Show the user the three prompts clearly (start image, end image, video motion). Then tell them:

> "Paste each prompt into your chosen tool, save the outputs, and drop them here:
> - `output/frame-first.png` — your start image
> - `output/frame-last.png` — your end image
> - `output/video.mp4` — your motion video
>
> Let me know when all three files are in place and I'll continue."

Wait — do not proceed until the user confirms the files exist.

#### Provider path
Invoke `sequenceforge-generate` to call the connected API and produce all three files automatically. Report the result before continuing.

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
