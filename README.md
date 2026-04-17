# SequenceForge

SequenceForge is a Claude Code plugin for building scroll-driven GSAP image sequences from a plain-language scene description.

It can:

- write the prompt set for a start frame, end frame, and transition video
- support a manual workflow or Google provider generation
- extract numbered PNG frames with `ffmpeg`
- inspect an existing GSAP project
- patch a target section with a canvas-based image-sequence integration

## What You Install

This repo is both:

- the plugin source
- a Claude Code marketplace that makes the plugin installable from GitHub

Users do not need to clone this repo to use the plugin. Claude Code installs it into the local plugin cache.

## Prerequisites

- Claude Code `2.1+`
- Python `3.10+`
- `ffmpeg` available on your `PATH`
- `PyYAML` installed: `pip install pyyaml`
- Optional for provider mode: `pip install google-genai`
- Optional for provider mode: `GOOGLE_CLOUD_PROJECT` and `GOOGLE_APPLICATION_CREDENTIALS` configured

## Install

Add the marketplace from GitHub:

```bash
claude plugin marketplace add martin-iliew/sequenceforge
```

Install the plugin:

```bash
claude plugin install sequenceforge@sequenceforge-market
```

Reload plugins in Claude Code if the commands do not appear immediately:

```text
/reload-plugins
```

## Quick Start

### 1. Open the project you want to work on

Start Claude Code inside the target site or app:

```bash
cd /path/to/your-project
claude
```

### 2. Choose the workflow

Use `forge-frames` if you only want prompt writing plus frame extraction.

Use `forge-sequence` if you also want SequenceForge to inspect the current project and update it with an image-sequence integration.

Installed plugin commands are namespaced, so run them as:

- `/sequenceforge:forge-frames`
- `/sequenceforge:forge-sequence`

## Workflow A: Media Only

Generate the prompt pack and a scroll-ready frame sequence:

```text
/sequenceforge:forge-frames "premium watch reveal from silhouette to dial detail" --dest public/images/watch-frames --mode manual
```

What happens:

1. SequenceForge writes the creative brief and saves `output/frame-spec.yaml`.
2. In `--mode manual`, Claude shows you the prompts and waits for you to save:
   - `output/frame-first.png`
   - `output/frame-last.png`
   - `output/video.mp4`
3. SequenceForge extracts numbered PNGs into your `--dest` folder.

Use provider mode if you want the Google provider workflow:

```text
/sequenceforge:forge-frames "sunrise over a calm ocean, camera slowly pulling back" --dest public/images/ocean-frames --mode provider --fps 24
```

## Workflow B: Full Project Integration

Run the full pipeline against the project Claude is currently open in:

```text
/sequenceforge:forge-sequence "camera dives through cloud layers into a shoe close-up" --project-root . --target "home hero" --dest public/images/feature-frames --mode manual
```

What happens:

1. SequenceForge writes and reviews the prompt set.
2. It waits for your manual media files, or generates them in provider mode.
3. It extracts PNG frames to the destination folder.
4. It inspects the target project to find the best integration point.
5. It builds and applies the image-sequence integration directly in the target project.
6. It reports which files changed and where the GSAP sequence was inserted.

Use `--project-root .` when Claude is already open in the target project.

## Command Reference

### `/sequenceforge:forge-frames`

```text
/sequenceforge:forge-frames "<scene description>" [--dest <path>] [--mode manual|provider] [--fps <number>]
```

Examples:

```text
/sequenceforge:forge-frames "a cinematic descent from mountain peak to forest floor"
/sequenceforge:forge-frames "premium watch product reveal, dark editorial studio" --dest public/images/hero-frames
/sequenceforge:forge-frames "sunrise over a calm ocean, camera slowly pulling back" --fps 24 --mode provider
```

### `/sequenceforge:forge-sequence`

```text
/sequenceforge:forge-sequence "<scene description>" --project-root <path> --target "<page or section hint>" --dest <path> [--mode manual|provider] [--fps <number>] [--duration <seconds>] [--canvas-id <id>]
```

Examples:

```text
/sequenceforge:forge-sequence "premium watch reveal from silhouette to dial detail" --project-root . --target "home hero" --dest public/images/watch-sequence
/sequenceforge:forge-sequence "camera dives through cloud layers into a shoe close-up" --project-root . --target "product feature section" --dest public/images/feature --mode provider
```

## Files SequenceForge Writes

Prompt and media staging:

- `output/frame-spec.yaml`
- `output/frame-first.png`
- `output/frame-last.png`
- `output/video.mp4`

Frame extraction output:

- `<dest>/frame_000001.png`
- `<dest>/frame_000002.png`
- `...`

Project setup memory:

- `docs/design/project-setup.yaml`

## Provider Mode Notes

Provider mode uses the Google provider in [`scripts/providers/google.py`](scripts/providers/google.py).

Required setup:

```bash
pip install google-genai
```

Environment:

```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

On Windows PowerShell:

```powershell
$env:GOOGLE_CLOUD_PROJECT="your-project-id"
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\\path\\to\\service-account.json"
```

## Troubleshooting

- `claude plugin validate .` reports marketplace or plugin issues: run it from the repo root before publishing updates.
- The plugin installs but commands do not show up: run `/reload-plugins` or restart Claude Code.
- `ffmpeg not found`: install `ffmpeg` and make sure the binary is on `PATH`.
- Provider mode fails immediately: install `google-genai` and confirm the Google environment variables are set.
- Installed plugin cannot find files outside the plugin directory: this is expected. Claude Code copies marketplace plugins into its local cache.

## Publishing This Repo

Validate before publishing:

```bash
claude plugin validate .
```

Create the GitHub repo and push:

```bash
git init
git branch -M main
git add .
git commit -m "feat: publish sequenceforge plugin"
gh repo create martin-iliew/sequenceforge --public --source=. --remote=origin --push
```

After the repo is live, users install it with:

```bash
claude plugin marketplace add martin-iliew/sequenceforge
claude plugin install sequenceforge@sequenceforge-market
```
