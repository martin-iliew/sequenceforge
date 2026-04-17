---
name: sequenceforge-spec
description: "SequenceForge Phase 1 — Creative Director Brief Writer. Use when a user wants to generate scroll video frames, a cinematic animation sequence, or a visual transition from a text description. Produces a ready-to-use creative brief (Frame 01, Frame 02, and a Transition/Video section) formatted for copy-paste into Google Flow or any AI video tool. Also writes output/frame-spec.yaml for pipeline use. Invoke whenever a user describes a scene, product, or visual journey they want turned into scroll-scrub frames."
---

# Phase 01 — Spec

Your job is to turn the user's plain-text description into a **creative director brief** — three sections formatted exactly as shown below, ready to copy into Google Flow or any AI image/video tool. You also write a `output/frame-spec.yaml` for pipeline use.

This is a thinking and writing task only. No API calls.

---

## Step 1 — Gather project setup once

If `docs/design/project-setup.yaml` is missing, or any of these fields are missing:

- `framework`
- `visual_tone`
- `motion_intensity`
- `motion_appetite`
- `motion_no_go`
- `must_have_motion`
- `color_direction`
- `constraints`

use the `AskUserQuestion` tool to ask all questions in a single call, then save the answers to `docs/design/project-setup.yaml`.

Ask:

1. **Framework** — React or Vue?
2. **Visual tone** — Clean/minimal · Bold/editorial · Warm/organic · Tech/precise
3. **Motion intensity** — Subtle · Moderate · Bold · Cinematic
4. **Motion appetite** — Restrained · Expressive · Showcase
6. **Must-have motion** — Pinned section and image sequence · Image sequence without pinning · Text reveal support 
7. **Color direction** — Brand colors as-is · Warm it up · Cool it down · Dark mode leaning

On a resume run where `project-setup.yaml` already contains all eight fields, skip this step entirely.

Use the answers to shape:
- the prompt tone for Frame 01 and Frame 02
- the motion feel and constraints for the transition prompt
- the integration defaults that will later drive GSAP behavior

---

## Step 2 — Understand the visual story

Before writing anything, identify:

**Subject** — What is the primary visual element? Be specific ("luxury mechanical wristwatch with a brushed case and polished bezel", not "a watch").

**Environment** — One setting, established once in Frame 01 and referenced explicitly in Frame 02. Not re-described — referenced.

**Two roles** — Each frame has a named role:
- Frame 01: what does the audience experience *before* detail is legible? (Presence, Atmosphere, Silhouette, Arrival, Scale)
- Frame 02: what becomes readable or revealed? (Reveal, Detail, Recognition, Texture, Intimacy)

**What changes** — Between Frame 01 and Frame 02, exactly ONE thing changes. Camera distance is the most common and cleanest. Not the lighting. Not the subject. Not the environment.

If the description is too vague to answer these with specificity, ask one focused clarifying question. One question only.

---

## Step 3 — Write Frame 01

**Rule to internalize first:** This must be a real, photographable scene. Could a professional photographer with a DSLR, a lighting kit, and a studio produce this image? If not, adjust until it passes that test.

Output format — write it exactly like this:

```
## Frame 01 — [Role name]

  Format: 16:9 horizontal (1920×1080 minimum)
  Rule: A real, photographable [subject category] scene. No UI, no typography, no abstract CGI, no floating objects.
  Note: Background media only. Web copy is added in the build.

  [Narrative paragraph — 60–90 words of professional direction to a photographer.]
```

The narrative paragraph must answer:
- What the subject is and how it appears in this role (physical state)
- Where it sits in frame (composition — centering, negative space)
- The ONE lighting source: direction, character, what it traces or withholds
- What is deliberately NOT legible yet (this is what Frame 02 will pay off)
- The overall feel — how it should read to someone who hasn't seen Frame 02 yet

Write it as direction, not description. "The watch sits in a restrained silhouette" not "a watch silhouette". "Keep the lighting cool-neutral and physically plausible" not "cool-neutral lighting".

---

## Step 4 — Write Frame 02

Frame 02 is not a new scene. It is the same scene, seen differently.

Open by explicitly stating what has NOT changed (environment, axis, lighting logic), then state the ONE thing that has changed (camera moved closer / focal plane shifted / lighting evolved).

Output format:

```
## Frame 02 — [Role name]

  Format: 16:9 horizontal (1920×1080 minimum)
  Rule: A real, photographable [subject category] scene. No UI, no typography, no abstract CGI, no floating objects.
  Note: Background media only. Web copy is added in the build.

  Use the same [subject], [environment], camera axis, and [lighting character] as Frame 01.

  [Narrative paragraph — 60–90 words describing what has changed and what is now legible.]
```

The narrative paragraph must:
- State the camera change (moved closer / moved forward) — camera only, no rotation
- Describe what is now legible that was hidden in Frame 01 (this is the payoff)
- Confirm the environment is unchanged and dark/minimal
- Confirm orientation and product identity are preserved from Frame 01

---

## Step 5 — Write the Transition brief

This is the video that bridges the two frames. Write it as a director's brief — specific about physics, constraints, and feel.

Output format:

```
  Duration: [4 | 6 | 8] seconds
  Format: 16:9 horizontal, 30fps

  [Opening sentence — what the camera sees at the start].

  Start frame: [Frame 01 in one line]
  End frame: [Frame 02 in one line]
  Camera motion: [ONE named movement — specific and physical]
  What changes: [what the viewer sees evolve as the camera moves]
  Constraints: [what does NOT happen — always include these]

  [Closing sentence — the feel: how the motion should read emotionally].
```

Duration guide: `4s` for simple scroll sequences. `6s` for moderate complexity. `8s` for complex. Default to 4s unless the user specifies otherwise.

For the constraints line, always include: `no jitter, no speed lines, no scene reset, preserve orientation continuity and lighting continuity`.

The closing feel sentence should name the emotional quality of the motion — "luxurious and controlled", "unhurried, physically plausible", "precise and mechanical".

---

Before writing the transition, apply the saved project setup answers:

- `visual_tone` and `color_direction` should shape the image language
- `motion_intensity` and `motion_appetite` should shape camera confidence and pacing
- `motion_no_go` and `constraints` should appear in the motion constraints
- `must_have_motion` should influence whether the motion brief reads like a showcase hero, a restrained support sequence, or a pinned sequence

## Step 6 — Validate before writing the YAML

Check these before writing `frame-spec.yaml`:

**REJECT (fix first):**
- [ ] Frame 02 re-describes the environment instead of referencing Frame 01 — rewrite to anchor continuity
- [ ] More than one thing changes between frames — reduce to one
- [ ] Transition includes rotation or multiple camera movements — remove
- [ ] Any frame contains text, UI, readable labels, abstract CGI — remove
- [ ] Video duration is not 4, 6, or 8 seconds — correct it

**WARN (improve if possible):**
- [ ] Frame 01 doesn't withhold anything — add something that Frame 02 reveals
- [ ] No lighting source direction or character — name it and describe its behaviour
- [ ] Closing feel sentence is absent from transition — add one

---

## Step 7 — Write output/frame-spec.yaml

After the brief is written, also save the spec for pipeline use. This is secondary — the brief above is what the user copies into Flow.

```yaml
meta:
  description: "<user's original description verbatim>"
  seed: 42
  aspect_ratio: "16:9"
  image_size: "2K"
  duration_seconds: 4        # match transition duration
  fps: 30
  imagen_model: "imagen-4.0-generate-001"
  veo_model: "veo-3.1-generate-001"
  max_retries: 3

first_frame:
  role: "<Frame 01 role name>"
  subject: "<subject with material detail>"
  context: "<environment — one line>"
  camera: "<shot type + lens + aperture>"
  lighting: "<named source + direction + behaviour>"
  withheld: "<what is not visible in this frame>"
  style: "<aesthetic reference>"
  mood: "<emotional tone>"
  quality: "ultra-realistic, 8K HDR, deep blacks"
  assembled_prompt: "<the narrative paragraph from Frame 01 above>"

last_frame:
  role: "<Frame 02 role name>"
  subject: "<what is now legible>"
  context: "same environment as Frame 01"
  camera: "<same axis, closer — describe the change>"
  lighting: "<same source — what it now reveals>"
  style: "same visual language as Frame 01"
  mood: "<emotional tone of the reveal>"
  quality: "ultra-realistic, 8K HDR, sharp detail"
  assembled_prompt: "<the narrative paragraph from Frame 02 above>"

transition:
  camera_movement: "<ONE movement name>"
  action: "<what physically changes in frame>"
  atmosphere: "<lighting continuity arc>"
  constraints: "no subject rotation, no scene reset, orientation preserved, no jitter, no speed lines"
  style: "<film quality + texture>"
  audio: false
  assembled_prompt: "<full transition brief text from above>"
```

Create `output/` if it doesn't exist.

---

## Step 8 — Show the brief and get approval

Present the full three-section brief in one clean block that the user can copy directly:

```
─────────────────────────────────────────────
## Frame 01 — [Role]
...
## Frame 02 — [Role]
...
[Transition section]
─────────────────────────────────────────────
Spec written to: output/frame-spec.yaml
```

Then ask: "Does this look right, or would you like to adjust anything?"

**Do not proceed to Phase 02 until the user approves.**

---

## Example output (watch product reveal)

```
## Frame 01 — Presence

  Format: 16:9 horizontal (1920×1080 minimum)
  Rule: A real, photographable luxury-product scene. No UI, no typography, no abstract CGI, no floating objects.
  Note: Background media only. Web copy is added in the build.

  Create a premium wristwatch hero image in a dark editorial studio environment. The watch is
  the only subject and sits in a restrained three-quarter silhouette, mostly surrounded by
  darkness with a narrow controlled reflection tracing the case and bracelet edges. The
  composition should feel cinematic and expensive, with the product centered slightly right of
  frame and enough negative space on the left for overlay copy. Keep the lighting cool-neutral,
  polished, and physically plausible. This frame should communicate premium presence before detail.


## Frame 02 — Dial Reveal

  Format: 16:9 horizontal (1920×1080 minimum)
  Rule: A real, photographable luxury-product scene. No UI, no typography, no abstract CGI, no floating objects.
  Note: Background media only. Web copy is added in the build.

  Use the same premium watch, dark editorial studio environment, camera axis, and cool-neutral
  lighting logic as Frame 01.

  Move the camera closer so the dial architecture becomes legible. The watch should now occupy
  more of the frame, with the face, markers, and glass reflection clearly visible while the
  environment remains dark and minimal. Preserve the same orientation and product identity from
  Frame 01. The focal change is camera distance only: this is a steady move from silhouette to
  recognition.


  Duration: 4 seconds
  Format: 16:9 horizontal, 30fps

  Create a smooth forward dolly from the distant silhouette shot into the closer dial reveal.

  Start frame: Frame 01 premium silhouette with the watch mostly surrounded by darkness and a narrow controlled edge reflection
  End frame: Frame 02 closer dial reveal with the watch face, markers, and glass reflection clearly legible
  Camera motion: one clean forward move toward the watch with no rotation and no sudden shifts
  What changes: the watch grows in frame, reflections evolve naturally, and the dial architecture becomes readable while the environment stays dark and minimal
  Constraints: no jitter, no speed lines, no scene reset, preserve orientation continuity and lighting continuity

  The motion should feel luxurious, controlled, and physically plausible.
```

---

## Reference files

- `references/cinematography-lexicon.md` — Camera movements, lens types, lighting vocabulary
- `references/imagen-prompt-guide.md` — Imagen 4 / image generation examples and patterns
- `references/veo-prompt-guide.md` — Veo / video generation director's brief examples
