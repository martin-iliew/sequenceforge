---
name: sequenceforge-integrate
description: "SequenceForge Phase 5 — Framework-aware Integrator. Use after project inspection is complete and the target section is known. Generates a framework-aware canvas, styling, helper, and GSAP ScrollTrigger blueprint, then applies it in the target project following the project’s existing GSAP and styling conventions."
---

# Phase 05 — Integrate

Your job is to convert the inspected project structure into a concrete GSAP image-sequence integration and apply it in the user’s project.

## Inputs

- `prompt`
- `project_root`
- `target_hint`
- `frames_dest`
- `generation_mode`
- optional `fps`, `duration`, `canvas_id`

## Step 1 — Generate the blueprint

```bash
python scripts/plan_integration.py \
  --prompt "<prompt>" \
  --project-root <project_root> \
  --target-hint "<target_hint>" \
  --frames-dest <frames_dest> \
  --generation-mode <generation_mode> \
  --fps <fps> \
  --duration <duration> \
  --canvas-id <canvas_id>
```

Read the generated JSON and identify:
- target file
- animation file
- style file or style strategy
- canvas markup
- helper code
- GSAP animation code
- notes about inline vs module integration

## Step 2 — Apply changes in the project’s pattern

Run:

```bash
python scripts/apply_integration.py \
  --prompt "<prompt>" \
  --project-root <project_root> \
  --target-hint "<target_hint>" \
  --frames-dest <frames_dest> \
  --generation-mode <generation_mode> \
  --fps <fps> \
  --duration <duration> \
  --canvas-id <canvas_id>
```

Use the blueprint as the implementation source of truth:
- if the animation host strategy is `module`, extend the existing animation module
- if the animation host strategy is `inline`, add the sequence to the existing local GSAP block
- if the style strategy is `tailwind`, prefer utility classes on the canvas
- if the style strategy is `scoped`, add the canvas rules inside the component’s scoped style block
- otherwise add CSS where the project already keeps equivalent component/page styles
- if `docs/design/project-setup.yaml` exists, use it to preserve the requested motion appetite, intensity, motion bans, and performance/accessibility constraints

## Step 3 — Preserve project conventions

Do not rewrite the project’s animation architecture.

Match the local project’s:
- GSAP import and plugin-registration pattern
- lifecycle hook or mounting pattern
- asset URL convention
- file organization

## Step 4 — Report

At the end, report:
- files changed
- canvas location
- frame URL base path used
- any assumptions or fallbacks used
