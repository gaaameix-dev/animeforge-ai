---
description: Draw an anime shot in code (SVG/Canvas/CSS) so it reads as hand-drawn — construction, shading, line, light rig, motion
argument-hint: <shot description> [duration] [16:9|9:16] [ones|twos]
allowed-tools: Read, Write, Edit, Bash
---

Draw this shot in code with the `animeforge-ai` skill: $ARGUMENTS

First read `references/code-rendering.md` from the skill folder. Then work in this order — do not skip a pass:

1. **Spec** — shot size, lens (24/35/50/85mm), key vector and colour temperature, contrast ratio, palette (8–12 hexes), duration, drawing rate (acting on twos, effects on ones), hold length.
2. **Construction** — landmarks, ribcage/pelvis, limb tubes. Write them as a hidden `#rig` group so the drawing can be corrected later.
3. **Silhouette** — one merged shape. Fill it black and check the pose reads before going further.
4. **Clumps and features** — hair as 5–9 closed clumps, cloth folds off shoulder/elbow/knee/waist, then eyes, brows, mouth, ear.
5. **Line** — varied `stroke-width`, coloured with a dark tint of the local colour, never pure black.
6. **Paint** — base, ambient occlusion, core shadow, terminator softness, reflected light, rim, specular, colour bounce. Cooler, more saturated shadows.
7. **Light and atmosphere** — same key as the rest of the film, haze per depth plane, bloom on the top 5% of highlights, grain at 2–4%.
8. **Motion** — one fixed 24fps timeline, seeded randomness, 180° shutter blur, eased camera move, hold after the settle.

Write it to `animeforge/<slug>/frames/shot-01/index.html` plus a timeline file, and tell the user the exact command that plays it.

Then run the verification list from the reference and report it plainly: black-fill test, squint test, flip test at 12 and 24fps, palette count, light consistency against the other shots, full-screen test, determinism. A frame you have not actually rendered and looked at is **planned**, not verified — say which.
