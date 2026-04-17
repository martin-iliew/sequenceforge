# Imagen 4 Prompt Guide

Best practices for generating still keyframes with Google Imagen 4.

---

## Model Variants

| Model | Use when |
|-------|----------|
| `imagen-4.0-generate-001` | Default — balanced quality and speed |
| `imagen-4.0-ultra-generate-001` | Maximum quality — slower, higher cost |
| `imagen-4.0-fast-generate-001` | Fast iteration — lower quality |

---

## Writing Style: Creative Brief, Not Template

Write prompts as a **professional brief to a photographer** — not a comma-separated list of modifiers. The assembled prompt should read as coherent direction: what the shot is, how it is lit, what the camera does, and what the viewer should feel.

Target **80–120 words** per assembled_prompt.

### What this means in practice

**Comma-list (weak):**
```
luxury watch, dark background, editorial, 85mm, f/2.8, cool lighting, brushed steel,
ultra-realistic, 8K
```

**Professional brief (strong):**
```
A photo of a luxury mechanical wristwatch presented in a restrained three-quarter silhouette
on a dark matte editorial surface, product centered slightly right of frame. Shot on a DSLR
with an 85mm lens at f/2.8, eye-level axis, medium shot. A single narrow strip of cool-neutral
studio light from camera-right traces the case edge and bracelet links — the only visible
reflection in an otherwise dark frame. Fine brushed and polished steel texture on the lit
edges. Dark luxury editorial photography, anticipatory mood. Ultra-realistic, 8K HDR, deep blacks.
```

---

## Prompt Structure

Anchor Imagen in photorealistic mode by opening with `"A photo of..."`.

```
"A photo of [subject in its physical state in this shot],
[composition — where it sits in frame, negative space].
Shot on a DSLR with a [lens] at [aperture], [camera angle and shot type].
[Named light source] [direction and character — what it traces, reveals, or withholds].
[What is deliberately NOT visible or in shadow — establishes the withheld detail].
[Micro-texture sentence — what renders at close range].
[Style reference and mood]. [Quality boosters]."
```

---

## Frame Continuity Rules

When writing a two-frame sequence:

**Frame 01** establishes the environment once. Include:
- The surface, background quality, ambient character
- What the lighting source is and where it sits
- What is deliberately in shadow or not yet visible

**Frame 02** references Frame 01 instead of re-describing it. Open with:
- `"A photo of the same [subject]..."`
- `"same dark editorial studio as Frame 01"`
- `"same camera axis, camera moved forward only"`
- State what is NOW visible that was hidden

This anchors the AI in the same environment and prevents it from re-imagining the scene.

---

## Camera — Always Lens + Aperture + Shot Type

| Lens | f-stop | Use for |
|------|--------|---------|
| `16mm, f/8` | wide, sharp front-to-back | landscapes, architecture, scale |
| `35mm, f/5.6` | natural perspective | environmental portraits |
| `50mm, f/2.8` | intimate, mild background blur | editorial, lifestyle |
| `85mm, f/2.8` | portrait compression, subject isolation | product, face |
| `85mm, f/1.4` | creamy bokeh, shallow DOF | luxury product, fashion |
| `macro, f/4` | extreme close-up | texture, detail |

**Shot types:** `medium shot` · `medium close-up` · `close-up` · `wide establishing shot` · `low-angle` · `bird's-eye view`

---

## Lighting — Name the Source, Describe Its Behaviour

Generic lighting descriptions produce generic results. Name the source and describe what it does physically.

| Weak | Strong |
|------|--------|
| "good lighting" | "single narrow cool-neutral key light from camera-right tracing the case edge" |
| "dramatic" | "high-contrast side lighting leaving the far side of the subject in deep shadow" |
| "natural light" | "soft daylight from a side window, gradual natural falloff, no fill" |
| "backlit" | "hard rim light from directly behind, silhouetting the subject against a dark background" |

Always specify:
- **Direction** — camera-right, overhead, from below, 45° left
- **Character** — narrow strip, broad wash, diffused, specular
- **What it reveals** — traces the edge, illuminates the face, catches the crystal

---

## Subject Specificity

Replace generic nouns with physical descriptions.

| Generic | Specific |
|---------|----------|
| watch | luxury mechanical wristwatch with brushed case and domed crystal dial |
| bottle | dark green glass bottle with embossed label and foil neck wrap |
| tree | centuries-old Douglas fir with deeply furrowed grey bark |
| rock | black volcanic basalt with orange lichen patches |
| metal | brushed titanium with microscopic surface scratches |

---

## Micro-Texture Sentence

Add one sentence describing what the model should render at close range:

- "Fine brushed and polished steel texture visible only on the lit edges."
- "Individual fern fronds sharp with creamy bokeh on background trees."
- "Visible weave of the cotton fabric, fine skin pores."
- "Microscopic mineral striations in the volcanic rock surface."

---

## Constraints

- Avoid: text, UI chrome, readable labels, watermarks, floating objects, abstract CGI
- Avoid: explicit requests for named people
- Max prompt length: **480 tokens**
- Seed: use a consistent value (e.g. 42) across first + last frames for style coherence
- `A photo of...` opener keeps the model in photorealistic mode — always include it

---

## Quality Boosters (max 3)

Pick 2–3 that suit the image. More than 3 dilutes each other.

`ultra-realistic` · `8K HDR` · `sharp detail` · `deep blacks` · `shallow DOF` · `volumetric light` · `cinematic` · `award-winning photography`

---

## Strong Prompt Examples

### Product — dark studio (Frame 01)
```
A photo of a luxury mechanical wristwatch presented in a restrained three-quarter silhouette
on a dark matte editorial surface, product centered slightly right of frame with generous
negative space on the left. Shot on a DSLR with an 85mm lens at f/2.8, eye-level axis,
medium shot. A single narrow strip of cool-neutral studio light from camera-right traces the
case edge, polished crown, and interlocking bracelet links — the only visible reflection in
an otherwise fully dark frame. The dial is completely in shadow. Fine brushed and polished
steel texture visible only on the lit edges. Dark luxury editorial photography, silent and
anticipatory mood. Ultra-realistic, 8K HDR, deep blacks.
```

### Product — dark studio (Frame 02, same environment)
```
A photo of the same luxury mechanical wristwatch now facing directly forward in a medium
close-up, the dial architecture fully legible — face, applied hour markers, polished hands,
and domed crystal with a precise soft glass reflection. Shot on a DSLR with an 85mm lens
at f/2.8, same eye-level axis as Frame 01, camera moved forward only with no rotation. Same
dark editorial studio environment and cool-neutral lighting: the same directional key light
now revealing a precise specular highlight on the polished bezel and a controlled reflection
across the crystal. Dark background unchanged and minimal. Ultra-realistic, 8K HDR, sharp dial detail.
```

### Landscape — mountain (Frame 01)
```
A photo of a snow-capped mountain peak with jagged volcanic ridgeline rising above a sea of
low cloud, shot on a DSLR with a 16mm lens at f/8, slight low-angle perspective emphasizing
scale. Low sun from camera-left casts long amber shadows across the ridgeline with volumetric
atmospheric haze diffusing light into the cold blue sky. The forest below is entirely in
shadow — not yet visible. Fine frost textures and dark mineral striations visible on the
lit rock face. Photorealistic cinematic, National Geographic aesthetic, vast and solitary mood.
Ultra-realistic, 8K HDR, sharp foreground detail.
```

---

## Aspect Ratio Guide

| Ratio | Use when |
|-------|----------|
| `16:9` | Scroll sequences, landscape, hero backgrounds |
| `9:16` | Vertical/mobile scroll sequences |
| `1:1` | Square thumbnails |
| `3:4` / `4:3` | Portrait/landscape editorial |
