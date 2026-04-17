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

**IMPORTANT:** Both Python scripts live in the plugin, not in the user’s project. The skill system provides the plugin’s base directory at the top of this skill’s output as `Base directory for this skill: <path>`. Always use that path — never look for the scripts in the project root.

```bash
python "<plugin_base_dir>/scripts/plan_integration.py" \
  --prompt "<prompt>" \
  --project-root "<project_root>" \
  --target-hint "<target_hint>" \
  --frames-dest "<frames_dest>" \
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

**The blueprint is a reference only.** Do not paste its `canvas_markup` or `animation_code` verbatim — use them to understand intent, then write correct framework-idiomatic code yourself (see Step 2).

## Step 2 — Apply changes in the project’s pattern

**Do not run `apply_integration.py`.** It appends code outside components and produces incorrect output. Instead, use the blueprint from Step 1 as a reference and apply the integration manually with the Edit/Write tools, following the rules below.

**Canvas rules — always:**
- The canvas must fill the section completely: `position: absolute; inset: 0; width: 100%; height: 100%`
- For Tailwind projects use: `absolute inset-0 w-full h-full pointer-events-none`
- The wrapping section must have `position: relative` (or `relative` in Tailwind) and a defined height (`h-screen` or explicit px)
- Do NOT use `fixed`, `left-1/2`, `top-1/2`, `-translate-x-1/2`, or `max-w`/`max-h` constraints — these break the full-section fill

**Framework-specific integration rules:**

- **React / Next.js App Router**: add `"use client"` at the top; use `useEffect` to register `ScrollTrigger` and initialize the sequence; wrap in `gsap.context()` and return `ctx.revert()` for cleanup; import `gsap` and `ScrollTrigger` from the `gsap` package
- **Vue / Nuxt**: use `onMounted` / `onUnmounted`; register plugins inside the hook
- **Vanilla / Svelte**: use the appropriate lifecycle equivalent

**Frame URL correction for Next.js:** Files in `public/` are served at the URL root. Strip the `public/` prefix from `frames_url_base` when building frame URLs (e.g. `public/images/sequenceforge` → `/images/sequenceforge`).

**GSAP package check:** Before writing any GSAP code, verify that `gsap` appears in the project’s `package.json` dependencies. If not, install it (`pnpm add gsap` / `npm install gsap`) and report this in Step 4.

Use the blueprint to determine:
- if the animation host strategy is `module`, extend the existing animation module
- if the animation host strategy is `inline`, add the sequence inside the component
- if the style strategy is `tailwind`, use Tailwind utilities on the canvas
- if the style strategy is `scoped`, add canvas rules inside the component’s scoped style block
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
