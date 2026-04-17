# Veo 3.1 Prompt Guide

Best practices for generating cinematic video transitions with Google Veo 3.1.

---

## Model Variants

| Model | Use when |
|-------|----------|
| `veo-3.1-generate-001` | Default — higher quality |
| `veo-3.1-fast-generate-001` | Faster iteration — lower quality |

---

## First/Last Frame API

Veo 3.1 natively supports generating a video that bridges two images:

```python
operation = client.models.generate_videos(
    model="veo-3.1-generate-001",
    prompt=transition_prompt,
    image=first_frame_image,          # types.Image object
    config=types.GenerateVideosConfig(
        last_frame=last_frame_image,  # types.Image object
        duration_seconds=4,           # 4 | 6 | 8
        aspect_ratio="16:9",
    ),
)
```

The model generates a smooth, continuous video from the first image to the last. The prompt describes the **motion and atmosphere of the transition** — not the start/end (those are the images).

---

## Writing Style: Director's Brief

Write the transition prompt as a **director's brief to a cinematographer** — not a description of the result. The model behaves like a professional: the more physically specific your direction, the more precisely it executes.

Target **100–130 words** in clear sentences.

**Brief-style (strong):**
```
Camera begins in a medium shot with the watch in restrained three-quarter silhouette, only
the case and bracelet edges lit. The camera moves steadily forward on a fixed axis — one
clean, continuous dolly with no rotation and no sudden shifts. As the camera closes in,
the watch grows in frame, the bracelet detail becomes legible, the bezel specular sharpens,
and a precise reflection appears across the domed crystal. The shot ends in a medium close-up
with the dial fully readable. Lighting is physically continuous — the same cool-neutral key
light evolves naturally as camera distance changes. No subject rotation. No scene reset.
Orientation preserved. Style: dark luxury product film, controlled and unhurried, micro-texture
visible on polished and brushed steel, no jitter. Audio off.
```

**Description-style (weak):**
```
The camera slowly moves toward the watch and the scene transitions smoothly. The lighting
changes and the details become visible. Cinematic and luxurious feeling.
```

---

## Prompt Structure

```
[Camera starting position and what it sees].
[The ONE camera movement — named and described physically].
[What changes in frame as camera moves — subject grows, detail emerges, reflections evolve].
[Where the shot lands — end state].
[Lighting continuity — same source, evolving naturally with distance or time].
[Explicit constraints — what does NOT happen].
Style: [film quality, texture, motion character].
Audio off.
```

---

## Duration Strategy

| Duration | Use when |
|----------|----------|
| `4s` | Simple transitions, scroll sequences — shorter = smoother |
| `6s` | Moderate complexity, environmental progressions |
| `8s` | Complex multi-stage transitions, maximum content |

**API constraint:** only 4, 6, or 8 seconds are supported. Other values will fail.

---

## Camera Movement — Choose Exactly ONE

Stacking movements (e.g. "dolly while panning") produces unpredictable results. Choose one and name it precisely.

| Movement | Physical description | Use for |
|----------|---------------------|---------|
| `slow forward dolly on fixed axis` | Camera physically approaches subject | Intimacy build, product reveal |
| `slow dolly back` | Camera retreats, context revealed | Context, scale reveal |
| `crane down` | Vertical descent | Scale to intimacy |
| `crane up` | Vertical ascent | Intimacy to scale |
| `tracking left` / `tracking right` | Lateral movement | Space revelation |
| `static locked camera` | No movement — environment/subject changes | Ambient motion, time passage |
| `orbit` | Circular movement around subject | Product all-sides reveal |
| `rack focus` | Focus plane shifts | Foreground to background reveal |

---

## Explicit Constraints (include in every brief)

For product and scroll sequences, always state what does NOT happen. This prevents the model from adding motion it thinks is cinematic.

**Standard constraint block:**
```
No subject rotation. No scene reset. Orientation preserved throughout. No speed lines.
No abstract motion blur. No CGI effects. No jitter.
```

**Lighting continuity:**
```
Lighting is physically continuous — the same [source] evolves naturally as [camera moves /
time passes]. No sudden lighting changes.
```

---

## Atmosphere Arc

The most effective transitions have a clear physical arc from start to end. State it as a change in what the viewer *experiences*, not an emotion:

- `dark with only edge reflections → dial and detail fully legible`
- `cold open sky with long shadows → warm enclosed canopy light`
- `harsh midday overhead → soft blue-hour ambient glow`
- `distant silhouette → medium close-up with texture visible`

---

## Strong Prompt Examples

### Product forward dolly (luxury watch)
```
Camera begins in a medium shot with a luxury mechanical wristwatch presented in restrained
three-quarter silhouette, mostly surrounded by darkness with only the case and bracelet
edges lit by a narrow cool-neutral strip of light. The camera moves steadily forward on a
fixed axis toward the watch — one clean, continuous dolly with no rotation and no sudden
shifts. As the camera closes in, the watch grows in frame, the bracelet and case detail
become legible, the bezel specular sharpens, and a precise reflection appears across the
domed crystal dial. The shot ends in a medium close-up with the dial architecture fully
readable. Lighting is physically continuous — the same cool-neutral key light from camera-right
evolves naturally as camera distance changes. No subject rotation. No scene reset. Orientation
preserved. Style: dark luxury product film, controlled and unhurried, micro-texture visible on
polished and brushed steel, no jitter, no speed lines. Audio off.
```

### Descent from mountain to forest floor
```
Crane shot beginning high above a snow-capped mountain peak, slowly descending through thin
atmospheric haze and wispy cloud layers. The camera pushes downward through parting clouds,
revealing dense old-growth forest canopy below, continuing to descend through the canopy with
branches sweeping past. The shot completes with the camera resting at ground level on the
ancient forest floor, moss and ferns filling the frame. Movement is smooth, continuous, no
cuts. Atmosphere transitions from cold open golden-hour sky with long amber shadows to warm,
humid, enclosed green light. No camera rotation. Style: photorealistic, cinematic, fine
surface texture on rock and bark, subtle motion blur on passing clouds. Audio off.
```

### Static locked camera — rainy city night to dawn
```
Static locked camera at eye level, medium shot. A neon-lit rainy street corner holds frame
as rain gradually softens and sodium streetlights slowly dim. Pre-dawn cool blue ambient light
pushes in from above, replacing the orange glow. Wet cobblestones shift from warm orange
reflections to cool grey-blue. No camera movement. Atmosphere transitions from saturated urban
night to quiet desaturated pre-dawn. No sudden light changes — the shift is continuous and
physically plausible. Style: photorealistic, fine texture on wet pavement, subtle natural
grain, no artifical sharpening. Audio off.
```

---

## Anti-Patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Multiple camera movements | Unpredictable, incoherent motion |
| Text, UI, labels in prompt | Veo cannot render readable text reliably |
| `dynamic but subtle` | Conflicting direction → generic output |
| "with a cut to" | Veo generates one continuous clip, no cuts |
| Duration not 4/6/8 | API will reject the request |
| Describing the start/end state | Those are the images — describe the MOTION between them |
| Prompt under 80 words | Too little direction → generic result |
| `audio: true` for scroll | Audio-synced video breaks silent scroll scrubbing |

---

## Scroll Sequence Notes

Veo 3.1 audio should always be **disabled** for scroll sequences. Scroll-scrubbed videos are silent — the audio track is never played and wastes bandwidth.

The website-builder's GSAP scroll runtime expects a continuous video that maps cleanly to scroll position. A 4-second video at 30fps gives 120 frames, which is a comfortable range for a typical scroll section.
