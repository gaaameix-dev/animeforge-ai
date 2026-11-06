# Code-Rendered Anime — making it look real

Use this when the film is **drawn in code**: HTML + CSS + SVG, Canvas 2D, WebGL, or a
timeline engine that animates those layers frame by frame. The point is not "looks like
code". The point is a frame that survives a squint, a pause, and a full-screen look.

Two rules sit above everything else:

1. **One light rig for the whole film.** Key direction, colour temperature and contrast
   ratio are set once, written down, and never broken shot to shot. Inconsistent lighting
   is the single loudest tell of generated art.
2. **Silhouette first.** If the character reads as a shape in solid black, the drawing is
   finished enough to shade. If it does not, no amount of gradient will save it.

---

## 1. Build the character before you style it

Work in this order, and do not skip to colour:

| Pass | What you draw | Code shape |
| --- | --- | --- |
| 1. Landmarks | Head circle, brow line, eye line, nose base, chin, shoulder line, hip line | `<g id="rig">` with named `<circle>`/`<line>` guides, hidden in output |
| 2. Construction | Ribcage oval, pelvis wedge, limb tubes, hand and foot blocks | `<path>` per volume, no detail |
| 3. Silhouette | The body as one filled shape, in black | one merged `<path>` or a `<mask>` |
| 4. Clumps | Hair as 5–9 big clumps, clothing as folds, not lines | `<path>` per clump, each a closed shape |
| 5. Features | Eyes, brows, mouth, nose shadow, ear | small `<g>`, each on its own layer |
| 6. Line | Weight-varied, colour-tinted outline | `<path>` with `stroke-width` per edge |
| 7. Paint | Flat base, then shadow, then light | `<g>` per tone, `mix-blend-mode` |

Proportions that read as anime: 6.5–7.5 heads tall for adults, 5.5–6 for teens, 4 for
children. Eye line sits at roughly the middle of the head — not higher. Eyes are wide,
iris large, sclera small; the gap between the eyes is one eye wide.

**Asymmetry is realism.** Mirror nothing exactly: shift one eyebrow 1–2px, tilt the mouth,
make one iris catchlight bigger. Perfect symmetry reads as a doll.

---

## 2. The shading model

Aim for **two-tone cel plus a soft terminator**, then add light on top. Flat anime is not
flat: it is base, one shadow tone, and a rim.

Layer order, back to front:

1. **Base colour** — the local colour in neutral light.
2. **Ambient occlusion** — multiply, soft, in creases: under the chin, hairline, under
   the jaw, where cloth meets skin, inside the elbow, under the nose.
3. **Core shadow** — multiply, the shadow tone, hard edge on the light side of it.
4. **Terminator softness** — a 2–6px blur or a gradient only where the form turns slowly.
5. **Reflected light** — screen, low opacity, on the shadow side facing the floor.
6. **Rim / edge light** — screen or `lighter`, 1–3px along the lit silhouette.
7. **Specular** — screen, small and shaped: hair band, lip, eye, metal.
8. **Colour bounce** — overlay, the shadow side picks up the environment's hue.

Colour rules that stop it looking plastic:

- Shadows are **cooler and more saturated**, never grey. Skin shadow `#c98b86`–`#b56f70`,
  not `#a0a0a0`.
- Skin is not one hex. Base, a warmer mid, a cooler shadow, and a red flush on ears,
  knuckles, nose and knees.
- Use **subsurface hints**: a warm, low-opacity glow 2–4px inside the lit edge of ears,
  fingers and nose.
- Keep the palette small: 8–12 hexes for the film, written on the sheet, and nothing else.

```css
:root{
  --skin:#f0c2ae; --skin-mid:#e0a795; --skin-shadow:#c98b86; --skin-flush:#e08a86;
  --line:#3a2230;            /* never #000 */
  --rim:#ffe6c9;             /* key rim, warm */
  --fill:#8fa6d8;            /* cool fill from the sky */
}
.shadow{ mix-blend-mode:multiply; }
.rim   { mix-blend-mode:screen; }
.bounce{ mix-blend-mode:overlay; opacity:.18; }
```

**The layering rule that bites everyone.** A shade pass must reuse the *exact* `d` string of the
shape it shades. Retype it — even by 4px — and a sliver of unshaded base colour survives along the
edge. It reads as a rim light that nobody asked for, and it survives every other fix you try.

---

## 3. Face and eyes — where realism is won or lost

- **Sclera is never white.** `#f6f3ee` with a soft shadow under the upper lid.
- **Iris**: radial gradient, darker limbal ring, a bright lower crescent from bounce
  light, one crisp catchlight, one faint secondary.
- **Upper lash line** is a filled shape with thickness, heavier at the outer corner, and
  it overlaps the iris slightly. That overlap is what makes eyes look wet and alive.
- **Nose**: no outline. A shadow shape on one side plus a tiny specular dot.
- **Mouth**: line thickness varies; the lower lip gets a specular streak and a shadow
  under it. Teeth are `#efe7df`, never white.
- **Blush** is a soft multiply ellipse at low opacity, offset, not centred.
- Cheeks, chin and forehead each need one shadow shape or the face reads as a mask.

---

## 4. Hair and cloth

Hair is **clumps, then strands**:

1. Silhouette clumps (5–9), each a closed shape with a pointed tip.
2. A darker inner shadow at the roots and where clumps overlap.
3. The **specular band** — a broken ring of highlight, never a solid stripe.
4. 6–12 backlit strands, 1px, `screen`, only on the rim side.
5. Flyaway strands: 2–3, thin, low opacity. This one detail adds more life than any blur.

Cloth: folds are triangles hanging off anchor points (shoulder, elbow, knee, waist), each
with a lit face and a shadow face. Heavier fabric = fewer, wider folds. Silk = many thin
folds plus a long specular streak.

---

## 5. Light rig for the whole film

Write this down once, in the brief:

```
key:      warm 3200–4300K, 35° above, 30–45° camera-left
fill:     cool 6500–8000K, low, camera-right, 15–25% of key
rim:      strongest edge, behind, 1–3px, warm on skin, cool on metal
practical: any lamp, screen or moon in frame — it must match the key's logic
contrast: 4:1 for night, 2:1 for day interior
```

Then in code, every character and prop uses the same key vector. If a shot changes the
key side, that is a deliberate cut, and you say so.

**Atmosphere sells scale**: one haze layer per depth plane, 6–18% opacity, tinted to the
key. Bloom on the brightest 5% only. Grain at 2–4% over everything.

---

## 6. Camera and motion

- Use real lens numbers: 24mm for wide establishing, 35mm street, 50mm medium, 85mm
  close-up. Perspective, not zoom, does the work.
- Depth of field: blur far and near layers by real amounts (2–8px at 1080p for f/2), keep
  the eyes razor sharp. Never blur the whole frame.
- **Acting on twos** (12 drawings a second) for character motion; **rain, sparks, cloth
  flutter and blades on ones** (24). Mixing these two rates is what makes code animation
  feel hand-drawn.
- Motion blur: 180° shutter — blur length equals half the frame's travel. Simulate with a
  short directional blur, not a smear.
- Camera moves: ease in and out, add 0.5–1.5px of handheld noise on a slow drift, and
  hold still during dialogue.
- Holds are shots. A 12-frame hold after a settle reads as confidence.

---

## 7. Code patterns that keep it sharp

**Layer stack (SVG or divs), bottom to top:**

```html
<div class="frame">
  <div class="bg far"></div>      <!-- blurred, parallax -->
  <div class="bg mid"></div>
  <svg class="char">…</svg>       <!-- rig → construction → silhouette → paint → line -->
  <div class="fx bloom"></div>    <!-- screen blend -->
  <div class="fx grain"></div>    <!-- overlay, animated seed -->
  <div class="fx vignette"></div>
</div>
```

- **SVG** for characters and props: crisp at any size, easy to mask, cheap to hold.
- **Canvas 2D** for particles: rain, sparks, sakura, embers. One canvas, one draw loop.
- **WebGL / shader** only for bloom, grain, DOF and chromatic aberration — the passes that
  would be slow in DOM.
- Drive everything from **one timeline** (GSAP, Web Animations, or the host's frame
  engine) with a fixed 24fps tick. Never animate from `requestAnimationFrame` deltas that
  drift — the film must render identically every run.
- Seed every random: `mulberry32(seed)` for grain, rain, hair noise. Deterministic output
  is a delivery requirement, not a nicety.
- Precompute paths once; per frame, change transforms and `d` only where you must. A
  character built from 60 nodes should animate at 60fps on a laptop.

```js
const rnd = (s => () => (s = s * 16807 % 2147483647) / 2147483647)(42);
const FRAME = 1 / 24;
```

---

## 8. Verification — do these before you call it realistic

1. **Black-fill test**: fill the character solid black. Does the pose read? If not, fix the
   silhouette, not the shading.
2. **Squint test**: blur the frame to 8px. Do value groups still separate? If it turns to
   mud, the shadow tone is too close to the base.
3. **Flip test**: play at 12fps and then at 24fps. Jitter means spacing is uneven; mush
   means too few drawings.
4. **Palette lock**: count the hexes in the frame. More than the sheet's 8–12 means you
   drifted.
5. **Light consistency**: put shot 1 and shot 5 side by side. Same key side? Same
   temperature? Same contrast ratio?
6. **Full-screen test**: at 100% on a 1080p frame, no line should be under 1px, no
   gradient should band, and no edge should alias into a stair-step.
7. **Determinism**: render twice from the same seed. The files should be identical.
8. **Sliver check**: zoom to 200% along every silhouette. Any 1–2px line of base colour that is
   brighter than both sides is a shade pass whose path drifted from the shape it shades.

Report what passed. If a check fails and you shipped anyway, say which one and why.
