# SequenceForge

SequenceForge is a Claude Code plugin for building scroll-driven GSAP image sequences from a plain-language scene description.

It writes the prompts, gets or generates the media, extracts PNG frames, inspects your project, and applies the image-sequence integration.

## Start Here

Install the marketplace:

```bash
claude plugin marketplace add martin-iliew/sequenceforge
```

Install the plugin:

```bash
claude plugin install sequenceforge@sequenceforge-market
```

Open Claude Code inside your project:

```bash
cd /path/to/your-project
claude
```

Run the command:

```text
/sequenceforge:forge-squance
```

Or start with a scene description:

```text
/sequenceforge:forge-squance "premium watch reveal from silhouette to dial detail"
```

Then just answer the questions. You do not need to remember flags.

## Prerequisites

- Claude Code `2.1+`
- Python `3.10+`
- `ffmpeg` available on your `PATH`
- `PyYAML` installed: `pip install pyyaml`
- Optional for provider mode: `pip install google-genai`
- Optional for provider mode: `GOOGLE_CLOUD_PROJECT` and `GOOGLE_APPLICATION_CREDENTIALS` configured

If the command does not appear immediately, run:

```text
/reload-plugins
```

## What You Get

By default `/sequenceforge:forge-squance` will:

- use the current project as the project root
- use manual media mode unless you ask for provider mode
- write frames to `public/images/sequenceforge`
- inspect the project and ask you to choose a target section if the match is ambiguous

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

The command runs the full 01→06 workflow:

1. write the prompt set
2. get or generate the media
3. extract the PNG sequence
4. inspect the target project
5. plan the integration
6. apply the integration and report the changed files

Files written during the workflow:

- `output/frame-spec.yaml`
- `output/frame-first.png`
- `output/frame-last.png`
- `output/video.mp4`
- `<dest>/frame_000001.png`
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

Local test:

```bash
claude plugin validate .
claude plugin marketplace add ./ --scope local
claude plugin install sequenceforge@sequenceforge-market --scope local
```
