# CODEX V3 MASTER PROMPT: redraw all interludes and posters in a sitcom-yellow cartoon style (videos 011-100)

You work inside `research/football100`. This file is the full rulebook. The job: for the **90 videos 011-100** draw (a) a new **poster** per video and (b) **frame-by-frame animated interludes**: the old scenes redrawn in ONE style, plus MORE inserts. Plan: `codex/v3/plan_v3.json` (1,204 sequences, 40,272 frames at 24 fps) and one brief per video `codex/v3/plan/NNN.md` (narration with timestamps, allowed text, sequence table with start times and frame counts, the poster brief, the story and beat table of every comic).

Why this exists: the first version used nine mixed styles and plain boards. The channel needs ONE instantly recognisable, funny, simple look, posters that explain the story at a glance, and more cutaways so the picture changes every 1-2 seconds.

## 0. Outputs (exact)
- `poster3/NNN.png`: 1080x1920, opaque PNG, 9:16, one per video (90 files).
- `anim3/NNN/sKK/f0001.png ... fNNNN.png`: 1080x1920 opaque PNG, 24 fps, frame count exactly as in the plan table (all multiples of 6). 4 or 6 frames of transition in at the start and out at the end (4 for micro-inserts, 6 for scenes), different transition pair for every sequence of a video.
- `anim3/NNN/_sheet.png`: the character sheet of the video (see section 2), drawn first.
- `anim3/PROGRESS.md`: one line per finished item: `NNN poster done`, `NNN/sKK done` (add `, note: ...` for a changed beat or refusal).
- Do not touch `scripts/`, `deliver/`, `FINAL_100*/`, `clips/`, `v2/`, `anim/` or any existing `.py`. Own checker: `python3 codex/v3/check_v3.py` (do NOT use `codex/check_anim.py`).

## 1. The style (the "sitcom-yellow" look, inspired by classic Springfield-style TV animation)
Draw in a Simpsons-INSPIRED look with generic descriptors, original characters only:
- **Yellow skin** (#FFD90F family) on every human, round skull, large round white eyes with a small black pupil dot touching the eyelid, wide mouth, simple overbite or small chin line, four-fingered hands (three fingers and a thumb), rounded cartoon proportions, spiky or round simple hair shapes.
- Thin even dark outline (about 3 px at 1080 width, colour #1b1b1b), flat colour fills, one soft shadow tone, NO gradients on characters, NO textures. Backgrounds are flat, bright, slightly desaturated suburban-TV colours: sky blue, grass green, brick red, cream walls, pub carpet, sofa orange.
- Bold classic sitcom type for text: heavy rounded sans (Arial Black / Impact feel) in white or yellow with a thick dark outline and a small drop shadow, or black text on a cream sign.
- Football world: pub with a sofa and a big TV, stadium stands, pitch with stripes, press room with microphones, tunnel, dressing room, street with a kebab shop, training ground, TV studio with a desk.
- **Hard rules**: draw ORIGINAL characters. Never draw, copy or imitate any named character, family, logo, title card or catchphrase of any existing show or franchise. No couch-gag clones, no recognisable family. The look is a style, not a cast. Same for real people: a player is a *caricature identified by hair, beard, kit colour, number, one signature prop and a NAME label*; no photo likeness, no real club crest or sponsor logo, no real kit trademarks (use plain stripes and colours).
- Keep it SIMPLE: few shapes, big shapes, clear silhouettes, one joke per scene.

## 2. Cast and consistency
Before drawing anything for a video, draw `anim3/NNN/_sheet.png` (1080x1920): 2 or 3 recurring original characters with name tags (the HERO FAN, the REPORTER or PUNDIT, and the SUBJECT caricature of the video's main player or coach: identified by hair, kit colour, number, prop, name label), front view, 3/4 view, 3 expressions each (neutral, shock, smug), the recurring prop, the three most used backgrounds (flat, simple). Every sequence of that video must reuse exactly these characters, colours, proportions and props. Characters never change look between sequences. Across videos the style stays identical; only the cast and kit colours change.

## 3. Production method (this is how 40,272 frames become feasible)
- Do NOT generate every frame as an independent image. Build each sequence from the character sheet by **keyframes plus code in-betweening**: write deterministic Python (Pillow, and cairo or skia if available; the project already has Python 3) that draws the cast as vector shapes, poses them with joint rotations, and interpolates (ease, overshoot, squash and stretch, blink, breathing). Put reusable code in `anim3/_src/` (a `toolkit3.py` and per-batch scripts). You may use image generation for the character sheets, backgrounds and posters; fall back to code drawing when quota ends.
- Every frame of a sequence must be different from its neighbours: something moves in every frame (eyes, mouth, hands, props, background drift, camera push, particles). Held poses still get a tiny breathing or blink or drift.
- Animate "on twos" is NOT allowed: all 24 frames of a second are distinct drawings or distinct interpolations.
- Camera: use a slow push-in or a shake or a pan inside the scene; the frame itself never letterboxes.

## 4. Readability rules (the most important section)
- **Words on screen: main text 2 to 7 words per scene** (poster, sign, bubble or sticker combined), large: main text at least 110 px tall, secondary labels at least 64 px. Plus at most 2 or 3 tiny reaction words (OOF, WAIT, HA) of at least 56 px. Never paragraphs, never small print.
- Text only from the allowed list in the brief, the question or poll the brief asks you to write, the name label of a player, short onomatopoeia (BANG, POP, THUD, WHOOSH, DING, OOF) and numbers that appear in the narration. Spell exactly.
- Safe zones: top 12 percent (y < 230) and bottom 20 percent (y > 1536) carry NO text and no important element (subtitles and the Shorts interface live there). Also keep key text inside x = 60..900 (the right button column of the app covers x > 900 in the lower half). The scene background may fill all of it.
- Characters are BIG: the main character is at least 35 percent of the frame height. No tiny figures, no big empty middle, no label on top of a prop or a face.
- One idea per sequence. A viewer must read it in one glance at phone size.

## 5. Posters (`poster3/NNN.png`)
Purpose: the first frame and thumbnail of the Short. It must make people stop and must be **understood in one second**, in the same sitcom-yellow style, inside a comic panel.
1. Read the poster brief in `codex/v3/plan/NNN.md`. Decide the ONE thesis of the video from the narration (a fact, a contradiction, a number, a joke).
2. Compose one big comic panel with a thick black frame, a title burst and a clear picture of the story: the subject caricature in the middle (recognisable by hair, kit colour, number, signature prop and a name label), ONE hero prop that stands for the thesis (a VHS tape, a red card, a trophy, a ballon-d'Or-style golden ball, a scoreboard, a sofa...), and a second character (the hero fan) reacting with a funny face.
3. **Text budget**: main headline 2 to 7 words in total, huge and chunky (not the full channel title; a punchy distillation of the thesis, e.g. `985 GOALS. STILL RESTED?`). Plus 2 or 3 tiny comment or emotion bubbles of 1-3 words next to the characters (OOF, WAIT WHAT, HA). No other text except the name label.
4. Association test (apply before saving): a stranger must be able to say (a) who it is about, (b) what the claim or joke is. If not, simplify.
5. Brand: include the portrait-safe About Football badge `brand/portrait/aboutfootball_corner_badge.png` (560x150) at the lower left, x=60, bottom edge at y=1500 (inside the safe area, never under the bottom 20 percent, never at the right edge). Do not use any wide website logo or banner.
6. The headline sits between y=300 and y=1000, the characters between y=700 and y=1450. Top 12 percent and bottom 20 percent are plain colour. It must look good as a 270x480 thumbnail.

## 6. Brand and outro
The About Football mark and wordmark must fit the vertical screen: use only the assets in `brand/portrait/` (stacked lockup 1000x720 for big moments, corner badge 560x150). Keep 40 px side margins, never crop or stretch the logo, never place the wide web logo. The video's end card already exists (9:16); do not redraw it.

## 7. Sequence types (briefs in each video file; the sitcom-yellow style overrides any older style label)
- HOOK: slammed question board (max 8 words) over the hero fan reacting; end on a hard hit.
- NEWS: subject caricature + lower-third strip with the NAME and ONE fact from the narration, 2-3 icons that pop in step with the words.
- COMIC1/2/3: three chapters of the same story with the same cast and the recurring prop; the last chapter calls back to the first prop. Setup, gag in 3-4 escalating steps, a silent beat, a punchline twist (beat tables in the brief). Sitcom staging: living-room sofa, pub, press room, stands.
- INTERVIEW: reporter with a generic microphone (no logo), the subject answers; bubble text only from the narration or a reporter question; label REPORTER ASKS.
- PROVOC: two-option vote card (question max 7 words, two buttons of max 3 words each, bars filling, counter), cheeky, never about a person's character, never betting.
- STATS: 2-3 icon plus number pairs from the allowed text, bouncy counters, icons that act.
- **MICRO-INSERTS (new, 18-24 frames, ids s51 and up)**: REACTION (big face cut-in), STICKER (number or 1-3 word fact pops), THOUGHT (thought-bubble joke), CROWD (fans react), ZOOMFACE (fast push on the subject), TICKER (breaking-news strip). They exist to change the picture often. Keep each one to one beat.

## 8. Safety and content rules
- English only, UK audience, 18+. Cheeky, never abusive.
- No invented quotes for real people; no betting or odds wording; nothing about injuries, illness, drugs, crime, family, politics, religion, violence or sex. If a beat needs one of those, replace it with a harmless gag with the same setup, gag and twist and note it in `anim3/PROGRESS.md`.
- No real logos, crests, sponsors, photos, no franchise characters. If an image generator refuses a named person, draw the caricature by hair, kit colour, number and prop plus the name label.

## 9. Workflow (resume-safe, waves across all 90 videos)
Order by waves so every video gets the strongest assets first and a partial run is still usable:
- **Wave 0**: for every video 011-100: `_sheet.png` and `poster3/NNN.png`.
- **Wave 1**: HOOK, NEWS, COMIC1 and the micro-inserts of all videos.
- **Wave 2**: INTERVIEW, PROVOC, COMIC2.
- **Wave 3**: STATS and COMIC3.
Loop: run `python3 codex/v3/check_v3.py --todo --wave N` to list what is missing or failing, take the first id, read its brief, draw it, run `python3 codex/v3/check_v3.py --fix --video NNN` (flattens alpha, resizes 9:16 images to 1080x1920, reports duplicates, wrong counts and blank frames), then log in `anim3/PROGRESS.md`. Never redraw an item that passes. After each wave print `WAVE N DONE` with counts. If you run out of session, time or quota, stop cleanly after the current item; a new session resumes at the todo list.
Do not ask questions unless a brief file is missing.

## 10. Definition of done
`python3 codex/v3/check_v3.py` prints `90/90 posters, 1204/1204 sequences pass (40272/40272 frames)`. Then reply `ALL V3 ART DONE` with: number of redrawn frames, list of changed beats, list of substitutions for refused names. If fewer pass, give the count and the first 10 failing ids and stop.
