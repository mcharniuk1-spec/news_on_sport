# SPEC: Remotion animated interludes for Football100 Shorts 016-100

Project root: `<PROJECT_ROOT>/research/football100` (call it `H`). Remotion checkout: `H/v2/remotion`
(remotion, @remotion/cli, @remotion/bundler, @remotion/renderer 4.0.290 and react 18.3.1 are already installed with a lockfile;
you may add other `@remotion/*` packages at exactly 4.0.290). Google Chrome is at `/Applications/Google Chrome.app`.
Using Remotion's own managed Chrome download is authorised (the user asked for Remotion).

## 1. What we are building
100 vertical (1080x1920) English football Shorts for a UK audience (CTA aboutfootball.uk, 18+). Each Short has 7-9 animated
cutaway "interludes" planned in `H/codex/v2/plan.json` and `H/codex/v2/plan/NNN.md` (read `plan/016.md` first: narration with
timestamps, allowed on-screen text, a sequence table, per-sequence briefs, comic story and beat tables).
Videos 001-015 already have Codex PNG interludes (`H/anim/NNN/sKK/f0001.png...`, 24 fps, 1080x1920): LOOK AT THEM FIRST
(`H/anim/001/s01/f0010.png`, `s03`, `s04`, `s06`, `s07`, `H/anim/011/...`, `H/anim/012/...`) and match or beat that visual language:
flat vector cartoon, thick dark ink outline (#211c32), round-headed characters with big eyes, panel frames, pastel stadium stripes,
chunky rounded text boards. Videos 016-100 must LOOK like the same series, so the character rig, board style, icons and type
treatment have to be consistent across all 85 videos while the nine style labels change the palette/texture/line.

Your code renders ONLY the interludes. Footage, voice, subtitles, music and export are done elsewhere (ffmpeg). Each interlude is
an opaque full-frame mp4 that REPLACES the footage for its time window.

## 2. Output contract (hard)
- One mp4 per sequence: `H/v2/seq/NNN/sKK.mp4`, H.264, yuv420p, 1080x1920, **30 fps**, no audio, opaque, CRF <= 16, `-movflags +faststart`.
- Duration of an interlude = `floor(plan_frames / 24 * 30 + 0.5)` frames at 30 fps, i.e. **round HALF UP** (JS `Math.round`; NOT Python's banker's `round()`, which turns 52.5 into 52).
  `plan_frames` is `frames` of the sequence in plan.json; e.g. 36 -> 45 frames = 1.5 s, 42 -> 53 frames (52.5 rounds up), 48 -> 60. Every checker (check_clips.py, verify.py, assemble) must use this rule.
- The first 0.25 s is a TRANSITION IN and the last 0.25 s a TRANSITION OUT. In the implementation a transition is exactly **8 frames = 0.267 s** (`TRANS_FRAMES = 8`, 7.5 frames rounded up so the cover is exactly 1.0 on the boundary frame); it is "0.25 s" in this spec. Transitions are graphic wipes/irises/slams that reveal/cover the scene.
  **The very first and very last frame of every clip are the full flat COVER (one colour) by design**: `verify.py` requires "first frame == cover" so the footage cut hides behind it. Checkers that test "blank frame" or
  "first/middle/last differ" must exempt frame 0 and frame N-1 (the middle frame and every other frame are never flat). `tools/check_clips.py` already does this (blank = mean luma extremes only).
  Pick a different
  pair from a transition library (>= 12 transitions) per sequence, chosen deterministically from the sequence index so neighbouring sequences differ.
- Nothing may be static for more than ~0.3 s: breathing, blinking, floating props, drifting backgrounds, pulsing UI, counters, particles, camera push.
  Use easing (back/elastic/bounce), anticipation, overshoot, squash and stretch. No two neighbouring frames identical anywhere inside the clip.
- Safe zones: keep the top 12 % (y < 230) and bottom 20 % (y > 1536) free of important content/text (subtitles and the UI of the app sit there);
  background colour/pattern may fill them. Main action lives in the middle band; figures must be BIG (hero character >= 30 % of frame height).
  No tiny figures, no big empty middle, no label overlapping a prop.
- Nine style labels (field `style` in plan.json): SITCOM-YELLOW, CUTOUT-PAPER, INK-COMIC, ACTION-ANIME, RUBBER-SLAPSTICK, STRIP-MINIMAL, SCIFI-DEADPAN,
  CLEAR-LINE, FLAT-POP. Each is a THEME object (palette, skin/hair/shirt sets, line weight, texture overlay such as halftone / paper grain / scanlines / speed lines,
  motion personality, title font). One shared character rig and shared prop library re-skinned by the theme. Fonts: bundle local fonts via `@remotion/fonts`
  or CSS `@font-face` from files that exist on this Mac (`/System/Library/Fonts/Supplemental/Impact.ttf`, `Arial Black.ttf`, `Comic Sans MS Bold.ttf`; you may
  also use Google Fonts through `@remotion/google-fonts` if it works offline-cached; keep text bold, high contrast, readable at phone size).
- Allowed text: only the strings from the per-video "Allowed on-screen text" list in `plan/NNN.md`, plus the questions/poll strings the author writes for
  HOOK/PROVOC (facts only from the narration), the label `REPORTER ASKS`, short onomatopoeia SFX words in comics (BANG, POP, THUD, WHOOSH, CREAK, DING, CLANG), and
  numbers that appear in the narration/card text. Never invent quotes for a real person. No betting, odds, bookmakers or "bet" wording. Nothing about injuries, illness,
  drugs, crime, family, politics, religion, violence or sex. No real club crests, real logos, photos or franchise characters: original generic cartoon characters only
  (a "caricature of X" means a generic cartoon player with a distinctive prop/colour and the NAME written on a board). 18+ UK tone: cheeky, never abusive.

## 3. Content model (what authors write per video)
File: `H/v2/content/NNN.json`. One object:
```
{ "no": 16, "style": "<label from plan>", "prop": "<recurring comic prop>",
  "cast": { "<id>": {"role":"striker|keeper|reporter|coach|referee|fan|legend|mascot|kid|pundit|boss", "skin?":"#hex", "hair?":"#hex", "shirt?":"#hex", "number?":"7"} },
  "sequences": { "s01": {...}, "s02": {...}, ... } }
```
`sequences` has exactly the ids listed for that video in plan.json. Each entry has `type` and the fields below (the Remotion code defines the final vocabulary and
the validator enforces it; the lists here are the minimum to support):

- `HOOK`: `q` (<= 8 words, ends with `?`), `prop` (icon name), `emote`, `board` (sign|neon|stamp|typed|ticket|scoreboard).
- `NEWS` (player / story description card): `name` (<= 4 words), `fact` (<= 10 words, copied from narration/allowed text), `ticker` (allowed card text), `icons` (3 icon names),
  `role` (character role for the figure), `dateline?`.
- `INTERVIEW`: `label` ("REPORTER ASKS"), `bubble` (<= 9 words, a phrase from narration of the window OR a reporter question), `answer` ({icon, gesture}), `subject` (name, board only).
- `PROVOC` (two-option vote): `q` (<= 7 words), `a`, `b` (<= 3 words each), `split` ([n,m] summing to 100), `mood`.
- `STATS` (icon + number montage): `items` 2-3 x {`icon`, `value` (number or short string that appears in allowed text/narration), `label` (<= 3 words), `suffix?`}.
- `COMIC`: `bg` (default background), `beats` 3-4 x {`phase` SETUP|GAG|BEAT|TWIST, `t0`,`t1` (0..1 of clip, covering SETUP -> GAG -> silent BEAT -> TWIST like the plan's beat table),
  `bg?`, `actors` [{`id`,`x`,`y`,`pose`,`emote`,`flip`,`scale`}], `props` [{`kind`,`x`,`y`,`scale`,`anim`}], `sfx?` {text,x,y}, `bubble?` {who,text}, `cam?` (push|shake|pan|zoom-out)}.
  The recurring `prop` appears in every COMIC of the video; the LAST comic calls back to the first comic's prop. The comic story is in the plan brief; the cartoon cast is in `cast`.
  Poses (minimum): idle, kick, run, celebrate, shrug, point, sit, cry, shock, think, hold, fall, dance, sleep, wave, shush, facepalm. Emotes: neutral, happy, shock, angry-cheeky, smug, sweat, sleepy, cry, love, dizzy.
  Props (minimum 45): ball, trophy, shirt, boot, whistle, stopwatch, scoreboard, flag, cone, bench, armchair, sofa, goal, bucket, cake, car, cassette, bag, phone, camera, microphone, clipboard,
  card-red, card-yellow, coin, medal, crown, megaphone, tv, cup, pizza, door, key, calendar, tag, mug, umbrella, balloon, suitcase, rocket, clock, magnifier, lightbulb, crate, ladder, bin, paper-plane, ticket.
  Backgrounds (minimum 14): stadium, pitch, tunnel, dressing-room, studio, street, office, living-room, press-room, night-city, podium, bench-area, training, plain-colour.
  Anim presets: drop, slide-l, slide-r, bounce, shake, grow, shrink, spin, float, arc, pulse, pop, wobble, orbit.
  Anything an author needs that is missing must be added by YOU to the library, not worked around.

All types share: `accent?` colour override. Everything not specified is chosen by code from the style theme (so authors write JSON only).

## 4. Deliverables (write them under H/v2)
1. `remotion/src/**`: theme system (9 themes), character rig (SVG, parametric, blink/breathe/lip-flap/pose blending), icon+prop library, backgrounds, text boards, transition library,
   one React component per type + the shared `Interlude` composition (registered in `Root.tsx`, `calculateMetadata` from props, fps 30, 1080x1920).
2. `remotion/render.mjs`: CLI `node render.mjs --content H/v2/content/NNN.json [--only s01,s03] [--out H/v2/seq/NNN] [--concurrency 2]`. Bundles once, renders each requested sequence to `--out/sKK.mp4`,
   prints one JSON line per sequence `{"seq":"s01","frames":45,"sec":12.3,"ok":true}`. Reads plan frames from `H/codex/v2/plan.json`. A process-wide lock is NOT needed; several processes may run in parallel (use unique tmp dirs).
3. `remotion/validate.py` (python3, stdlib only): `python3 validate.py H/v2/content/NNN.json` -> exit 0 and `OK`, or a list of precise errors (unknown field/pose/prop/bg, word limits, text not in allowed list/narration, missing sequence id,
   type mismatch with plan, polls whose split does not sum to 100, comic without recurring prop, last comic without callback, etc.). Be strict: this is the authors' safety net.
4. `remotion/DSL.md`: the complete authoring reference (exact vocabularies as generated lists, one worked example per type, do/don't list). Authors (other agents) will rely ONLY on this file, `plan/NNN.md`, and `scripts/NNN.json`.
5. `v2/tools/contact.py` (python3 + Pillow): `python3 contact.py NNN` writes `H/v2/review/NNN/contact.png` (one row per sequence, 6 evenly spaced frames, 180x320 each, labelled) from `H/v2/seq/NNN/*.mp4` using ffmpeg.
6. `v2/content/016.json` (+ rendered `v2/seq/016/*.mp4`) as the worked reference for all types and a first quality test, and a timing report (seconds to render a 2 s clip at concurrency 2).

## 5. Quality bar (self-review with your own eyes; read the PNGs with the Read tool)
Render, build a contact sheet, view full-size frames of each type, then fix: text clipping, overlap, off-screen props, tiny figures, empty space, flat motion, identical frames, jarring colour, unreadable type.
Compare against the Codex frames in `H/anim/001..015`. Every type must feel alive (secondary motion) and read at phone size. Do not stop at "it renders".

## 6. Rules of the road
- Write only inside `H/v2/` (and read from anywhere under `H/`). Never edit `H/anim/`, `H/codex/`, `H/scripts/`, `H/deliver/`, `H/FINAL_100/`, any existing `.py` in `H/`, or the user's global config.
- Do NOT run `H/codex/check_anim.py`. Do not use Palmier. No network downloads other than npm packages `@remotion/*@4.0.290` and Remotion's Chrome.
- CPU is shared with other jobs: render with `--concurrency 2` (or lower), use `nice -n 10` for long loops.
- Be deterministic: no `Math.random()` at render time (use a seeded PRNG from the sequence id) so re-renders are identical.
