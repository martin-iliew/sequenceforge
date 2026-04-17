---
name: sequenceforge-generate
description: "SequenceForge Phase 2 — Provider Generator. Use after frame-spec.yaml has been written and approved, and the user has chosen the provider workflow. Validates provider environment requirements, shows an approval gate, then runs scripts/generate.py to call the configured provider backend. Current built-in provider: Google Imagen 4 + Veo 3.1."
---

# Phase 02 — Generate (Provider Workflow)

Your job is to validate the provider environment, show the user what is about to run, get confirmation, and execute `scripts/generate.py`.

---

## Step 1 — Gate check

Verify `output/frame-spec.yaml` exists and all three `assembled_prompt` fields are present and non-empty. If not, stop and tell the user to run Phase 01 first.

---

## Step 2 — Environment check

For the built-in Google provider, check these environment variables. If any are missing, stop and show the setup instructions:

```
Required:
  GOOGLE_CLOUD_PROJECT           — your GCP project ID
  GOOGLE_APPLICATION_CREDENTIALS — path to service-account.json

Optional:
  GOOGLE_CLOUD_LOCATION          — region (defaults to us-central1)

Setup (one-time):
  1. Create a GCP project at console.cloud.google.com
  2. Enable Vertex AI: gcloud services enable aiplatform.googleapis.com
  3. Create a service account with roles/aiplatform.user
  4. Download the JSON key
  5. export GOOGLE_CLOUD_PROJECT="your-project-id"
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

Install Python package if not already done:
  pip install google-genai pyyaml
```

---

## Step 3 — Approval gate

Read the spec and show this summary before running anything:

```
READY TO GENERATE

[1/3] Imagen 4 — Frame 01 (<role from spec>)
  Model:  <imagen_model>
  Prompt: <first_frame.assembled_prompt>

[2/3] Imagen 4 — Frame 02 (<role from spec>)
  Model:  <imagen_model>
  Prompt: <last_frame.assembled_prompt>

[3/3] Provider video generation — Video (<duration_seconds>s, <aspect_ratio>)
  Model:  <veo_model>
  Prompt: <transition.assembled_prompt>

Outputs: output/frame-first.png, output/frame-last.png, output/video.mp4
Estimated time: 3–5 minutes (Veo runs async)

Proceed? (y/n)
```

Do not run the script until the user confirms.

---

## Step 4 — Run generate.py

```bash
python scripts/generate.py \
  --spec output/frame-spec.yaml \
  --output-dir output
```

Keep the user informed during the Veo polling stage — it can take 3–5 minutes and shows `...` dots while waiting. Let them know it's working normally.

**To test the pipeline without spending credits**, use `--mock`:

```bash
python scripts/generate.py --spec output/frame-spec.yaml --output-dir output --mock
```

Mock mode generates gradient placeholder images and a real ffmpeg crossfade video. The full pipeline (spec → generate → extract) works exactly the same at $0 cost.

---

## Step 5 — Validate outputs

After the script exits successfully, verify:

- `output/frame-first.png` exists and size > 0
- `output/frame-last.png` exists and size > 0
- `output/video.mp4` exists and size > 0

If any file is missing or empty, report the error clearly and do not proceed to Phase 03.

---

## Error handling

| Error | Action |
|-------|--------|
| Imagen safety block | Script reports the error. Ask the user if they want to adjust the prompt (return to Phase 01). |
| Veo timeout | `output/pending-operation.txt` contains the operation ID for manual retrieval from GCP. |
| API quota exceeded | Show the error. Suggest waiting or switching to the manual Flow workflow. |
| Missing package | Run `pip install google-genai pyyaml` |

---

## On success

```
Generation complete.
  output/frame-first.png  — <file size>
  output/frame-last.png   — <file size>
  output/video.mp4        — <file size>

Ready for frame extraction.
```
