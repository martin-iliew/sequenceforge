# Cinematography Lexicon

Reference vocabulary for building Imagen 4 and Veo 3.1 prompts.
Adapted from [kdowswell/veo-tools](https://github.com/kdowswell/veo-tools).

---

## Camera Movements (Veo — choose ONE per prompt)

| Movement | Effect | Use when |
|----------|--------|----------|
| `dolly forward` | Physical approach toward subject | Building intimacy, drawing viewer in |
| `dolly back` | Physical retreat from subject | Revealing context, creating distance |
| `tracking left` / `tracking right` | Lateral movement parallel to action | Progressive revelation of a space |
| `crane up` | Vertical ascent | Revealing scale, establishing shot |
| `crane down` | Vertical descent | Landing on a subject, grounding |
| `orbit` / `arc shot` | Circular rotation around subject | 360° product showcase, examination |
| `half orbit` | 180° perspective shift | Dramatic reveal from the other side |
| `static` / `locked camera` | No movement | Pure observation, ambient motion only |
| `rack focus` | Focus plane shifts between subjects | Drawing attention from BG to FG or reverse |
| `push in` | Slow, intentional zoom-like move | Building tension, narrowing focus |
| `pull out` | Slow retreat revealing context | Revealing twist, expanding world |

**Never stack movements.** "Dolly while panning" produces unpredictable results.

---

## Lens Types (Imagen — shapes composition and feel)

| Lens | Effect | Use when |
|------|--------|----------|
| `wide angle 16mm` | Expanded space, slight edge distortion | Vast environments, architectural scale |
| `normal 35mm` | Natural perspective, closest to human eye | Grounded, documentary feel |
| `portrait 85mm` | Compressed planes, subject isolation | Intimate close portraits |
| `telephoto 200mm` | Heavy compression, narrow FOV | Compressed backgrounds, distant subjects |
| `macro lens` | Extreme close-up detail | Materials, textures, tiny objects |
| `fisheye` | Extreme distortion, full hemisphere | Abstract, surreal, ultrawide |

---

## Shot Sizes (Imagen — subject framing)

| Size | Description |
|------|-------------|
| `extreme wide shot` | Environment dominates, subject is tiny |
| `wide establishing shot` | Full subject in context |
| `medium shot` | Subject from waist up |
| `close-up` | Face or key detail fills frame |
| `extreme close-up` | Single feature dominates (eye, hand, texture) |
| `low-angle shot` | Camera below subject — makes subject powerful |
| `high-angle shot` | Camera above — makes subject small or surveyed |
| `bird's-eye view` | Directly overhead |
| `ground level` | Camera at floor — intimate, immersive |

---

## Lighting

### Direction
| Term | Effect |
|------|--------|
| `front light` | Flat, even — minimal shadows |
| `side light (45°)` | Texture and dimension |
| `backlight / rim light` | Silhouette, separation from background |
| `top light` | Drama, mystery |
| `under light` | Unnatural, unsettling |

### Quality
| Term | Effect |
|------|--------|
| `hard light` | Sharp shadow edges, defined shapes |
| `soft / diffused light` | Gentle gradients, no harsh shadows |
| `volumetric light` | God rays, visible light shafts through atmosphere |
| `bokeh` | Beautiful out-of-focus blur circles in background |
| `specular highlight` | Bright points on reflective surfaces |

### Time of Day (temporal anchors)
| Term | Character |
|------|-----------|
| `golden hour` | Warm orange/amber, long shadows |
| `blue hour` | Cool deep blue, twilight atmosphere |
| `magic hour` | Transitional — mixed warm/cool |
| `high noon` | Harsh overhead, minimal shadow |
| `overcast` | Soft directionless light, muted colors |
| `3AM sodium glow` | Urban night, yellow-orange cast |
| `pre-dawn` | Very cool, still, almost monochrome |

---

## Atmospheric Elements

**Particles & Haze:** dust motes · morning mist · sea fog · smoke wisps · snow · light rain · condensation

**Light Phenomena:** god rays (crepuscular rays) · lens flare · caustics (refracted light patterns) · bokeh circles · volumetric haze

---

## Color & Grade

### Temperature
| Term | Character |
|------|-----------|
| Warm (2000–4000K) | Orange, amber, cozy, cinematic |
| Neutral (5000–6000K) | Balanced daylight, natural |
| Cool (7000K+) | Blue, clinical, cold |

### Tonal Contrasts
- `high contrast` — deep blacks, bright whites, punchy
- `low contrast` — lifted blacks, muted highlights, film-like
- `desaturated` — reduced colour intensity, muted palette
- `split toning` — warm highlights + cool shadows (or reverse)

### Common Cinematic Palettes
- `amber/teal` — filmic warmth vs cool shadow (Blade Runner 2049)
- `blue/grey` — cold procedural (Fincher)
- `green/gold` — organic warmth (Malick)
- `monochromatic` — single hue variations

---

## Film References (Style Anchors)

Use sparingly — one per prompt max. These communicate aesthetic direction efficiently.

| Reference | Aesthetic |
|-----------|-----------|
| `Blade Runner 2049` | Vast, lonely, amber/teal, neon rain |
| `Terrence Malick` | Natural light, handheld, impressionistic, organic |
| `David Fincher` | Precise, clinical, desaturated, controlled |
| `Wes Anderson` | Symmetrical, pastel, flat composition |
| `Roger Deakins` | Clean, luminous, understated |
| `Emmanuel Lubezki` | Long takes, natural light, handheld fluidity |
| `Denis Villeneuve` | Monumental, slow, geometric |
| `National Geographic` | Photorealistic, documentary, natural |

---

## Anti-Patterns

**NEVER include in prompts:**
- Text, UI chrome, labels, overlays, readable elements — Veo/Imagen cannot render text reliably
- Multiple camera movements: "dolly while panning and zooming"
- Conflicting descriptors: "dynamic but subtle", "bright but dark", "gritty but clean"
- Generic nouns without material specificity: "a tree", "some water", "metal"
- Overcomplicated multi-subject scenes: focus on one subject, one action

**Prompt assembly order:**
```
[camera/lens] + [subject + material detail] + [action/state] + [context/setting] + [lighting] + [style + film ref] + [mood] + [quality boosters]
```
