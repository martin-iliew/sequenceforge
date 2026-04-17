---
name: sequenceforge-inspect
description: "SequenceForge Phase 4 — Project Inspector. Use after frames are available and the user has supplied a project root plus target hint. Detects the project framework, GSAP setup, style strategy, target section candidates, and whether the project organizes animations inline or in separate files."
---

# Phase 04 — Inspect Project

Your job is to inspect the target app before any integration edits are made.

## Inputs

- `project_root`
- `target_hint`
- `frames_dest`

## Step 1 — Run the inspector

```bash
python scripts/inspect_project.py \
  --project-root <project_root> \
  --target-hint "<target_hint>" \
  --frames-dest <frames_dest>
```

## Step 2 — Read the report

Capture and summarize:
- detected framework
- style strategy
- GSAP registration or primary animation file
- animation pattern: `inline` or `module`
- top target candidates
- any ambiguity notes

## Step 3 — Ambiguity gate

If the top two candidates are tied or the notes say the target is ambiguous:
- stop
- show the best candidates to the user
- ask which file/section should receive the sequence

Do not proceed to integration while placement is ambiguous.

## Step 4 — Pass forward

Once the target is clear, pass the confirmed target details to `sequenceforge-integrate`.
