# Flipbook animation for the Ronaldinho Short (cartoon frame-by-frame)

## Idea
Replace the two single placeholder stills with three short hand-drawn style animations, drawn frame by frame. Codex draws only the **moving subject on a transparent background**. A fixed background plate is drawn once per scene, so the background never wobbles. I composite the frames with `assemble_flipbook.py` and drop the result into the Palmier timeline.

## Frame rate and counts
Project fps is 30. Cartoons are drawn "on twos", so we use **15 drawings per second**, each held for 2 video frames. That reads as animation, not slideshow, and keeps the count realistic.

| Scene | Where in the video | Length | Drawings (15/s) | If you want smoother (24/s) |
|---|---|---|---|---|
| A. "The joke" | 3.4-5.0 s (replaces cake still) | 1.6 s | 24 | 38 |
| B. "Slippers to golden boots" | 15.2-16.8 s (replaces boots still) | 1.6 s | 24 | 38 |
| C. "Grandad sprint" sticker | 16.6-18.4 s, overlay on the smile close-up | 1.8 s, loops | 27 | 43 |
| Total | | | **75 images** | 119 images |

Start with 15/s. Only go to 24/s if the result looks choppy.
Note: scene A grows by 0.4 s and B by 0.2 s, so I will re-time the edit when the frames arrive.

## File layout (inside `<PROJECT_ROOT>/research/video_build/gfx/flip/`)
- `bg_A.png`, `bg_B.png`: background plates, 1080x1920, opaque. No scene C plate (it is an overlay).
- `A/A_001.png` ... `A/A_024.png`, `B/B_001.png` ... `B/B_024.png`, `C/C_001.png` ... `C/C_027.png`: subject frames, 1080x1920 PNG with **transparent background** (RGBA), same canvas size every frame so positions line up.

## Shared style (put this first in every request)
Bold comic/sticker cartoon, thick black outlines, flat saturated colours, simple cel shading, squash-and-stretch, slightly messy hand-drawn energy, funny and loud. Vertical 1080x1920. Keep the lower third (rows 1300-1700) mostly empty, captions go there. **No real people or real faces, no logos, no brand names, no readable text.** Characters are generic cartoon figures.

## Method for consistency
1. Draw each plate and one **character/prop reference sheet** first, and stick to it.
2. Draw frames in order, **in batches of 6**. For every frame, edit the previous frame: "same canvas, same style, change only what the table says". Never redraw the background in subject frames.
3. After each scene, make a contact sheet of all frames and check that size, colours and outline thickness do not jump. Redraw any frame that jumps.
4. If transparent PNG is not possible, draw the subject on flat pure magenta (#FF00FF) and say so. I key it out with `KEY=1`.

## Scene A: "The joke" (24 drawings)
Plate `bg_A.png`: warm yellow/orange sunburst, a dark green pitch stripe at the bottom, soft spotlight circle in the middle, empty.
Subject: one giant birthday cake with a party hat, 46 candles, a wide cartoon face on the cake side that can wink.

| Frames | Action |
|---|---|
| 1-4 | Cake drops in from above, squash on landing (frame 4 is the flattest), candles unlit |
| 5-8 | Cake stretches back up, face opens its eyes |
| 9-16 | Candles light one after another, a wave from left to right (about 6 per frame), flames flicker |
| 17-20 | Cake laughs: whole body shakes, eyes squeezed, tears fly out |
| 21-24 | Party horn pops out, confetti burst, last frame holds a big glowing "46" made of candle flames |

## Scene B: "Slippers to golden boots" (24 drawings)
Plate `bg_B.png`: deep purple and navy sunburst, spotlight circle, green pitch stripe at the bottom, empty.
Subject: a pair of fluffy brown slippers and a walking stick, then a pair of glowing golden football boots, and a football.

| Frames | Action |
|---|---|
| 1-8 | Slippers shuffle in from the left, slow and tired (small hops), stick tapping |
| 9-12 | Lightning bolt hits the slippers, white flash frame (frame 10 is almost all white) |
| 13-16 | Slippers smear and morph into golden boots, sparkles |
| 17-20 | Boots wind up, a football appears, strong squash on the kick |
| 21-24 | Football flies out to the right with speed lines, boots stay in a hero pose with sparkles |

## Scene C: "Grandad sprint" overlay sticker (27 drawings, seamless loop)
No plate: transparent frames only, placed over the smile close-up.
Subject: a generic cartoon grandad in a tracksuit and flat cap (no real person), running very fast along the bottom with dust clouds, dribbling a football.

| Frames | Action |
|---|---|
| 1-9 | Run cycle, 9 drawings (contact, down, pass, up), body leaning forward |
| 10-18 | Same run cycle again with small variation, flat cap flapping, dust puffs |
| 19-27 | Third cycle, the cap flies off, speed lines. Frame 27 must match frame 1 so it loops |

## Prompt to give Codex (paste as is)

```text
Create a short cartoon flipbook, drawn frame by frame, as PNG files in
<PROJECT_ROOT>/research/video_build/gfx/flip/ .
Follow FLIPBOOK_PROMPT.md in that folder's parent (video_build) for the frame tables.
Style: bold comic/sticker cartoon, thick black outlines, flat saturated colours, simple cel shading, squash-and-stretch, funny and loud. Vertical 1080x1920. Lower third (rows 1300-1700) mostly empty. No real people or faces, no logos, no readable text.

Work in this order:
1. Draw bg_A.png and bg_B.png (opaque background plates, no subject).
2. Draw one reference sheet per scene (cake, slippers/boots, grandad) and keep to it.
3. Draw the subject frames for scene A (A_001..A_024), B (B_001..B_024), C (C_001..C_027).
   Every subject frame: 1080x1920 PNG, TRANSPARENT background, same canvas and the subject placed in the same coordinate system as the previous frame. Make each frame by editing the previous one in batches of 6, changing only what the table says. Do not redraw the background in subject frames.
4. After each scene, build a contact sheet of its frames and fix any frame where size, colours or line thickness jump.
If transparency is impossible, draw subjects on flat pure magenta #FF00FF and tell me.
When done, list every file written.
```

## After Codex finishes (my part)
```bash
python3 assemble_flipbook.py A 15
python3 assemble_flipbook.py B 15
python3 assemble_flipbook.py C 15   # alpha .mov overlay, no plate
```
Then I import `clips/flipA.mp4`, `clips/flipB.mp4`, `clips/flipC.mov` into Palmier, swap them for the stills, re-time the edit and re-export.
