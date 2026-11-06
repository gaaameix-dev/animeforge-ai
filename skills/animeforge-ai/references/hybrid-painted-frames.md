# Painted frames — the hybrid pipeline

Read this when someone points at a frame and says "this quality". Frames like that — soft
painted shading, hair drawn as hundreds of weighted strokes, a city with five thousand
hand-placed lights — are **not** produced by writing SVG by hand. They come from an image
model (or a studio). Pretending otherwise wastes everyone's day.

The honest split:

| Job | Who does it |
| --- | --- |
| Composition, blocking, camera, palette, shot timing | code |
| The painted surface of each frame | an image model or an artist |
| Continuity between shots | code, with locked references and seeds |
| Assembly, subtitles, edit, export | code |

If no image or video tool is connected, you cannot deliver frames in that class. Say so in
one sentence and hand over the shot list and prompts. Do not generate a vector approximation
and call it the same thing.

---

## 1. What code does first

Never prompt before the frame is planned. For each shot, code produces:

- **Blocking**: camera height, lens, subject position, horizon line, foreground/mid/background
  planes. A rough greyscale layout (rectangles and ellipses) is enough — it is the contract.
- **Palette**: 6–10 hexes, warm/cool split named, key direction named.
- **Light**: key angle and colour temperature, fill, rim side, contrast ratio.
- **Reference set**: the character sheet, the location sheet, and the approved still from the
  previous shot.

That layout image is also the best prompt ingredient you have — pass it to the model as an
image-to-image or composition reference where the tool supports it.

## 2. The prompt, in the order that matters

```
[style anchor] + [subject and action] + [composition] + [light] + [palette] + [lens/finish] + [negatives]
```

- **Style anchor**: name the medium, not a studio — "2D anime key visual, cel-shaded with soft
  painted gradients, thin ink line work, film grain". Naming a living studio or a specific
  show is a rights problem and usually a worse prompt.
- **Composition**: "close-up, 85mm, subject right of centre, horizon at lower third" — this is
  where the code layout pays off.
- **Light**: "single warm key from behind-right at 3200K, cool sky fill at 20%, hard-edged
  cast shadow across the cheek".
- **Palette**: the hexes, as words: "warm amber #ffc06a against cold navy #0a1526".
- **Negatives**: "no text, no watermark, no extra fingers, no lens distortion, no western
  cartoon proportions".

## 3. Continuity, which is where models fail

- Keep a **character sheet** image and attach it to every shot prompt.
- Lock the **seed** where the tool allows it; change one variable at a time.
- Re-use the same palette words in every prompt, in the same order.
- Generate the **wide shot before the close-up** — a close-up invented first will not match the
  wide you make afterwards.
- Keep a shot log: prompt, seed, model, date, verdict. You will need to regenerate.

## 4. Assembly back in code

Once frames exist:

1. Normalise to one resolution and colour space.
2. Time them on the 24fps timeline from Stage L — holds, cuts, the sakuga shot.
3. Add grain, vignette and the grade as one shared pass, so every frame matches.
4. Burn subtitles from the dialogue in the script, not from memory.
5. Export at the delivery spec; verify with a real playback, not a thumbnail.

## 5. QA for painted frames

- Character identity across shots: face shape, hair silhouette, outfit, palette.
- Light direction consistent with the rig written in the brief.
- Hands, eyes and text — the three things models break. Check them at 100%.
- Nothing claimed as rendered that you have not opened and looked at.

## 6. When the tool is not there

Deliver, and label it plainly:

- the shot list with timings
- one prompt per shot, in the structure above
- the palette and light rig sheet
- the character and location sheet requirements
- the assembly instructions

That is a real deliverable. A vector drawing that pretends to be the painted frame is not.
