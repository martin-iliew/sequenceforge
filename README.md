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

### 2. Run the single command

Installed plugin commands are namespaced. SequenceForge now has one public command:

```text
/sequenceforge:forge-squance
```

You can also start it with a scene description:

```text
/sequenceforge:forge-squance "premium watch reveal from silhouette to dial detail"
```

### 3. Answer the questions

The command starts the whole workflow and asks for any missing details itself.

You do not need to remember flags for project root, target section, output path, or setup prompts.

By default the command will:

- use the current project as the project root
- use manual media mode unless you ask for provider mode
- write frames to `public/images/sequenceforge`
- inspect the project and ask you to choose a target section if the match is ambiguous

## What The Command Does

`/sequenceforge:forge-squance` runs the full SequenceForge flow:

1. Phase 01: writes the prompt set
2. Phase 02: asks for or generates the media
3. Phase 03: extracts the PNG frame sequence
4. Phase 04: inspects the target project
5. Phase 05: plans the integration
6. Phase 06: applies the integration and reports the changed files

## Command Reference

### `/sequenceforge:forge-squance`

```text
/sequenceforge:forge-squance
/sequenceforge:forge-squance "<scene description>"
```

Examples:

```text
/sequenceforge:forge-squance
/sequenceforge:forge-squance "camera dives through cloud layers into a shoe close-up"
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

Test the marketplace from a local checkout:

```bash
claude plugin marketplace add ./ --scope local
claude plugin install sequenceforge@sequenceforge-market --scope local
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
