# DSL: authoring content for Football100 interludes

Write ONE file per video: `H/v2/content/NNN.json` (H = `<PROJECT_ROOT>/research/football100`).
Then run (from `H/v2/remotion`):

```
python3 validate.py ../content/NNN.json                      # must print OK  (add --comics-only to check just the COMIC entries while authoring)
node render.mjs --content ../content/NNN.json [--only s01,s03] [--out ../seq/NNN] [--concurrency 2]
python3 ../tools/contact.py NNN                              # -> H/v2/review/NNN/contact.png ; look at it, then at full frames
python3 ../tools/framecheck.py ../seq/NNN/*.mp4              # contract + "no identical neighbouring frames"
```

Authors rely ONLY on this file, `codex/v2/plan/NNN.md` and `scripts/NNN.json`. The `validate.py` errors are exact: fix every one.

## 1. File shape

```json
{ "no": 16, "style": "SITCOM-YELLOW", "prop": "sticker", "accent": "#ffd23f",
  "cast": { "modric": {"role": "player", "number": "10", "shirt": "#e8505b", "hair": "#6b4a2a", "skin": "#ffd23f"} },
  "sequences": { "s01": {...}, "s02": {...} } }
```
* `style` = the label of the video in plan.json (never change it). `accent?` overrides the theme accent colour for the whole video (optional, rarely needed).
* `sequences` has EXACTLY the ids of plan.json, each with `"type"` equal to the plan type (`COMIC1/2/3` in the plan md are all type `COMIC`).
* `cast` ids are free names; `role` is a ROLES value; `skin/hair/shirt` are optional `#rrggbb`; `number` 1-2 digits. Used by COMIC (and the shirt number on kit roles).
* `prop` = the recurring comic prop (required when the video has COMIC sequences).
* Every type also accepts `bg` (a BGS value) and `accent` (#hex). Omit them: the code picks a backdrop deterministically from the style/video.
* Everything else (palette, outline, textures, fonts, transitions IN/OUT, camera push, motion) comes from the style theme. Never write colours except `accent` and cast colours.

## 2. Vocabularies (generated from `src/core/vocab.ts`; do not invent names)

STYLES: <!--VOCAB:STYLES-->
`SITCOM-YELLOW`, `CUTOUT-PAPER`, `INK-COMIC`, `ACTION-ANIME`, `RUBBER-SLAPSTICK`, `STRIP-MINIMAL`, `SCIFI-DEADPAN`, `CLEAR-LINE`, `FLAT-POP`  (9)
<!--/VOCAB-->

ROLES: <!--VOCAB:ROLES-->
`striker`, `keeper`, `reporter`, `coach`, `referee`, `fan`, `legend`, `mascot`, `kid`, `pundit`, `boss`, `player`, `rookie`, `staff`  (14)
<!--/VOCAB-->

POSES (pose names for COMIC actors): <!--VOCAB:POSES-->
`idle`, `kick`, `run`, `celebrate`, `shrug`, `point`, `sit`, `cry`, `shock`, `think`, `hold`, `fall`, `dance`, `sleep`, `wave`, `shush`, `facepalm`, `jump`, `bow`, `cheer`, `tired`, `present`, `headscratch`, `thumbsup`, `lean`, `crouch`  (26)
<!--/VOCAB-->

EMOTES: <!--VOCAB:EMOTES-->
`neutral`, `happy`, `shock`, `angry-cheeky`, `smug`, `sweat`, `sleepy`, `cry`, `love`, `dizzy`, `sad`, `wink`  (12)
<!--/VOCAB-->

GESTURES (INTERVIEW `answer.gesture`, a subset of POSES): <!--VOCAB:GESTURES-->
`shrug`, `point`, `thumbsup`, `wave`, `think`, `shush`, `present`, `facepalm`, `cheer`, `headscratch`, `hold`, `idle`  (12)
<!--/VOCAB-->

PROPS = ICONS (every prop can be an icon; icons are drawn flat in the theme palette): <!--VOCAB:PROPS-->
`ball`, `trophy`, `shirt`, `boot`, `whistle`, `stopwatch`, `scoreboard`, `flag`, `cone`, `bench`, `armchair`, `sofa`, `goal`, `bucket`, `cake`, `car`, `cassette`, `bag`, `phone`, `camera`, `microphone`, `clipboard`, `card-red`, `card-yellow`, `coin`, `medal`, `crown`, `megaphone`, `tv`, `cup`, `pizza`, `door`, `key`, `calendar`, `tag`, `mug`, `umbrella`, `balloon`, `suitcase`, `rocket`, `clock`, `magnifier`, `lightbulb`, `crate`, `ladder`, `bin`, `paper-plane`, `ticket`, `star`, `heart`, `fire`, `bolt`, `thumbs-up`, `thumbs-down`, `check`, `cross`, `question`, `exclaim`, `globe`, `chart-up`, `chart-down`, `gloves`, `suit`, `hanger`, `envelope`, `notepad`, `laptop`, `headphones`, `pen`, `hourglass`, `gift`, `donut`, `glasses`, `bell`, `siren`, `cap`, `scarf`, `newspaper`, `padlock`, `ribbon`, `boots`, `net`, `table`, `podium-box`, `shelf`, `sticker`, `speech-dots`, `heart-broken`, `sweat-drop`, `tie`, `chair`, `desk`, `plant`, `lamp`, `screen`, `arrow`, `pitch-board`  (97)
<!--/VOCAB-->

BGS (backgrounds): <!--VOCAB:BGS-->
`stadium`, `pitch`, `tunnel`, `dressing-room`, `studio`, `street`, `office`, `living-room`, `press-room`, `night-city`, `podium`, `bench-area`, `training`, `plain-colour`, `boardroom`, `pub`, `sky`, `kitchen`  (18)
<!--/VOCAB-->

ANIMS (prop animation presets): <!--VOCAB:ANIMS-->
`drop`, `slide-l`, `slide-r`, `bounce`, `shake`, `grow`, `shrink`, `spin`, `float`, `arc`, `pulse`, `pop`, `wobble`, `orbit`  (14)
<!--/VOCAB-->

BOARDS (HOOK question boards): <!--VOCAB:BOARDS-->
`sign`, `neon`, `stamp`, `typed`, `ticket`, `scoreboard`  (6)
<!--/VOCAB-->

MOODS (PROVOC): <!--VOCAB:MOODS-->
`cheeky`, `smug`, `shock`, `love`, `fun`, `angry`, `sleepy`  (7)
<!--/VOCAB-->

CAMS (COMIC beats): <!--VOCAB:CAMS-->
`push`, `shake`, `pan`, `zoom-out`  (4)
<!--/VOCAB-->

SFX_WORDS (the only words allowed as comic sound effects): <!--VOCAB:SFX_WORDS-->
`BANG`, `POP`, `THUD`, `WHOOSH`, `CREAK`, `DING`, `CLANG`  (7)
<!--/VOCAB-->

SUFFIXES (STATS value suffix): <!--VOCAB:SUFFIXES-->
`%`, `+`, `x`, `k`, `m`, `s`, `'`  (7)
<!--/VOCAB-->

FX_KINDS (COMIC beat `fx`): <!--VOCAB:FX_KINDS-->
`smoke`, `sparkle`, `confetti`, `dust`, `speed`  (5)
<!--/VOCAB-->

LAYERS (COMIC prop `layer`): <!--VOCAB:LAYERS-->
`back`, `front`  (2)
<!--/VOCAB-->

HANDS (COMIC actor `hold.hand`): <!--VOCAB:HANDS-->
`R`, `L`, `both`  (3)
<!--/VOCAB-->

TRANSITIONS (15, picked automatically per sequence, in + out differ): <!--VOCAB:TRANSITIONS-->
`wipe-diag`, `iris`, `blinds`, `checker`, `ball-roll`, `panels`, `star-iris`, `dots`, `stripes`, `curtain`, `zigzag`, `flash-slam`, `ink-splat`, `hex-shutter`, `wave`  (15)
<!--/VOCAB-->

If a story needs something missing (a prop, background, pose...), do NOT work around it: add it to the library (see NOTES.md "How to add") and rerun `node gen_vocab.mjs`.

## 3. Text rules (enforced by validate.py)
* On-screen text is ONLY: strings from the video's "Allowed on-screen text" list, phrases copied from the narration, the questions/poll strings you write for HOOK/PROVOC (facts from the narration only), `REPORTER ASKS`, comic sfx words, and numbers that appear in the narration / card text (the validator knows "seven-nil" = 7 and 0, "twice" = 2, "ninety-first" = 91).
* Never: betting / odds / bookmakers wording, injuries, illness, drugs, crime, family, politics, religion, violence, sex, insults. No invented quotes for real people. No real crests, logos, photos, franchise characters: people are generic cartoons (a "caricature of X" = a cast member with a distinctive colour/prop and the NAME on a board).
* Safe zones are handled by the templates (top 12 % and bottom 20 % stay free of text). Since the 016 review this holds for EVERY frame, entrances included: boards slam in by SCALE (never dropped from above), tickers/name boards slide in from the SIDE,
  settled boxes: HOOK board y 282..678, NEWS ticker y 1384..1450, INTERVIEW name board bottom <= 1493, STATS cards y 266..1500 (3 cards), PROVOC fans' feet y 1500. The comic panel's own plates stay inside it.
* STATS labels may be copied from the narration (e.g. "Spain won", "Croatia scored once") as well as from the allowed list: `validate.py` accepts narration phrases on purpose (source='strict' = a contiguous phrase of the narration or an allowed text).
  A score value ("2-1") never counts up through a wrong score: it flips like a split-flap card from "?-?" to the final digits.

## 4. Types

### HOOK  (first sequence, ~1.5 s)
Fields: `q` (<= 8 words, ends with `?`), `prop` (icon), `emote`, `board` (one of BOARDS); optional `role` (who reacts; default picked), `prop_text` (only for prop `scoreboard`, form `"7:0"`).
```json
{ "type": "HOOK", "q": "How do you lose 7-0 as captain?", "prop": "scoreboard", "prop_text": "7:0", "emote": "shock", "board": "sign" }
```
Vary the `board` between videos: sign (hanging, swings), neon (flickers on), stamp (slams), typed (typewriter), ticket, scoreboard (LED letters). The question must share a content word with the narration.

### NEWS  (player / story card)
Fields: `name` (<= 4 words: the subject / allowed text), `fact` (<= 10 words, copied from the narration or an allowed text), `ticker` (EXACTLY one allowed on-screen text), `icons` (exactly 3), `role`; optional `dateline` (<= 4 words from the sources), `actor` (a `cast` id).
**Casting**: the figure IS the comic character: `actor` (or, if omitted, a cast id equal to a word of `name`: "Luka Modric" -> `cast.modric`) gives the NEWS figure the same role, hair, shirt colour and number as in the comics. Only when no cast id matches is `role` used with a generic look.
```json
{ "type": "NEWS", "name": "Luka Modric", "fact": "Modric has six Champions League titles", "ticker": "Six Champions Leagues", "icons": ["trophy","medal","star"], "role": "player" }
```
Icons pop in one by one (trophy pulses, ball bounces, whistle wobbles...). Pick icons that match the narration words in order.

### INTERVIEW
Fields: `label` (exactly `REPORTER ASKS`), `bubble` (<= 9 words: a phrase of the narration in this window OR a reporter question ending with `?`), `answer` `{icon, gesture, emote?}` (the subject answers with a gesture + icon, no words), `subject` (name board text); optional `reporter_role`, `subject_role`, `subject_cast` (a `cast` id).
**Casting**: the subject is the comic character (`subject_cast`, else the cast id equal to a word of `subject`: "Luka Modric" -> `cast.modric`); the reporter is always drawn with a different hair colour/style so the two never read swapped. A bubble that is a narration phrase (not a `?` question) is drawn quoted-style (quote badge).
```json
{ "type": "INTERVIEW", "label": "REPORTER ASKS", "bubble": "would do a great job in Real Madrid's administration", "answer": {"icon": "suit", "gesture": "shrug"}, "subject": "Luka Modric" }
```

### PROVOC  (two-option vote, never about a person's character/body/private life, never betting)
Fields: `q` (<= 7 words, ends `?`), `a`, `b` (<= 3 words each), `split` `[n, m]` (integers, sum 100, each >= 5), `mood` (MOODS: how the two reacting fans look).
```json
{ "type": "PROVOC", "q": "A 1880 football gift: classy or odd?", "a": "Classy", "b": "Odd", "split": [64, 36], "mood": "cheeky" }
```
The larger side wins (crown, pulse, confetti).

### STATS  (icon + number montage)
Fields: `items` 2 or 3 x `{icon, value, label, suffix?}`; `value` = digits string ("2", "2-1", "73"; every number must appear in narration/allowed text), `label` <= 3 words copied from the sources, `suffix` one of SUFFIXES.
```json
{ "type": "STATS", "items": [ {"icon":"ball","value":"2","label":"Merino scores twice"}, {"icon":"flag","value":"2-1","label":"Spain won"}, {"icon":"whistle","value":"1","label":"Croatia scored once"} ] }
```
Numbers count up with bouncy easing, one card after another.

### COMIC  (a 2 s cartoon with one gag and one twist)

A COMIC is a tiny comic strip drawn inside a rounded PANEL. The panel is fixed (x 30..1050, y 234..1532: the safe zone). The background, actors, props and effects live inside it,
and the camera (`push`, `pan`, `shake`, `zoom-out`) moves INSIDE the panel. Everything is authored as BEATS; the engine tweens between beats for you.

Fields of the comic entry: `bg` (BGS value, default backdrop), `beats` (4 or 5), optional `accent`.
(The first spec draft said 3-4 beats. The silent BEAT is mandatory, so the rule is: SETUP, GAG, optional 2nd GAG, BEAT, TWIST = 4 or 5 beats.)

#### Phases and timing (fractions of the clip; a 2.0 s clip = 60 frames at 30 fps)
| phase | t0 .. t1 (use this) | what happens | engine behaviour |
|---|---|---|---|
| SETUP | 0 .. 0.26 | the situation, readable by 0.25 s (the 0.25 s IN transition covers the first frames) | actors pop in (squash), props enter with their `anim` |
| GAG | 0.26 .. 0.52 (or two steps 0.26-0.42 and 0.42-0.54) | one escalating action: something moves, falls, grows, arrives. New actors RUN in from the nearest edge, moved actors RUN to the new spot, props tween to the new x/y/scale/rot | pose blends with overshoot, squash pulse on change, sfx burst + shake |
| BEAT | 0.54 .. 0.64 (0.06-0.16 allowed) | SILENT BEAT: everyone freezes and LOOKS at the gag prop. No sfx, no fx, no cam | actors/props are inherited, only breathing / blink / prop idle drift move; soft vignette |
| TWIST | 0.64 .. 1.0 (>= 0.30 allowed) | the punchline pose, held while the OUT transition covers it. The recurring prop must be on screen here | white flash, camera punch, ring from the gag prop, then a slow push |

`t0` of every beat must equal `t1` of the previous one; the last `t1` is 1. Put the punchline in the TWIST beat, not earlier: the viewer must READ the gag in ~1.5 s at phone size:
ONE gag, ONE twist, big figures, at most 3 actors.

#### Beat fields
```
{ "phase": "GAG", "t0": 0.26, "t1": 0.52,
  "bg": "pub",                                   // optional: crossfade to another backdrop
  "actors": [ {id, x, y, pose?, emote?, flip?, scale?, hold?, label?, look?, talk?, lift?, rot?} ],
  "props":  [ {kind, x, y, scale?, anim?, rot?, flip?, text?, face?, label?, layer?} ],
  "sfx":    {"text": "BANG", "x": 540, "y": 700, "r": 170},      // r optional (90-260)
  "bubble": {"who": "modric", "text": "?"}  or  {"who": "modric", "icon": "heart", "thought": true},
  "cam":    "push",                              // push | pan | shake | zoom-out (default: TWIST pushes slowly)
  "fx":     [ {"kind": "smoke", "x": 700, "y": 470, "size": 1} ] }
```
`actors` and `props` are REQUIRED in SETUP / GAG / TWIST and may be omitted in BEAT (inherited; if you list them they must equal the previous beat).

* **actors**: `id` = a key of the top-level `cast`. `x` = centre of the feet (60..1020), `y` = feet (900..1535; normal floor = 1440). `scale` default 1.3: figure height = 505 x scale x role scale
  (rookie 0.9, kid 0.78). The biggest actor of every beat must be >= 560 px (scale >= 1.15; rookies >= 1.25). `pose` (POSES, default idle), `emote` (EMOTES, default neutral), `flip` (mirror, true = faces left),
  `talk` (lip flap), `look` (`"cam"`, another cast id or a prop kind; in BEAT/TWIST everybody automatically looks at the recurring/first prop), `lift` px / `rot` deg (airborne, tilted),
  `hold` = `{kind, hand: R|L|both, scale?, rot?, dx?, dy?, anim?}` (a prop glued to the hand, follows the arm), `label` = name plate floating ABOVE the head (<= 3 words copied from the narration or allowed text; the camera push crops anything under the feet, so the plate never goes there). Do not give the same actor a `label` and a `bubble` in one beat (both open above the head: validate.py rejects it).
  The same `id` in consecutive beats is ONE character that moves: if x changes by more than 140 px the figure RUNS there. An id that is absent from a beat leaves running (and may return later).
* **props**: `kind` (PROPS), `x`,`y` = CENTRE (the panel is y 235..1530), `scale` default 1.6 (one prop is ~200 px at scale 1: a "big gag prop" is scale 2.4-3, an accessory 0.5-1),
  `anim` (ANIMS; the entrance presets drop/slide-l/slide-r/grow/shrink/pop/arc play once when the prop first appears, the others loop), `rot`, `flip`,
  `text` digits only (`"7:0"` on a scoreboard, `"90"`; every number must be in the narration), `face` = any EMOTES name: the prop gets googly eyes and a mouth (a scoreboard "with a face"),
  `label` = caption plate under the prop (<= 3 words copied from the narration or allowed text),
  `layer` back|front (furniture such as bench, door, desk, table, tv, net, goal is drawn BEHIND the actors by default; scoreboard and everything else in front).
  The same kind (and same occurrence order) in consecutive beats is the SAME prop: it tweens to the new x/y/scale/rot. If `text` changes it FLIPS like a split-flap card. If it is missing in the next beat it shrinks away. Entrance anims are ignored on a continuing prop.
* **sfx**: only SFX_WORDS. Burst + ring + screen shake at the beat start; it fades after ~0.5 s. Keep it away from faces (put it in empty sky or floor).
  The WHOLE burst must fit: `x +- 1.12 r` inside 54..1026 and `y +- 1.12 r` inside 254..1480 (`r` defaults to 190; validate.py checks the extent, not just the centre; the engine also clamps it into the visible panel after the camera zoom) and it must not sit on a falling figure (that is the gag).
* **bubble**: `who` = actor id (or a prop kind). Give EITHER `text` OR `icon`. `text` is `?`, `!`, `?!`, `...` or a phrase of <= 4 words copied from the narration (the validator checks). `icon` = any PROPS name (heart, cross, question, exclaim, lightbulb...). `thought: true` draws a thought cloud. A bubble persists through the following silent BEAT.
* **fx**: `smoke` (rising puffs; rises `260 x size` px, so keep y - 260 x size - 60 >= 250), `dust`, `sparkle`, `confetti`, `speed` (radial speed lines), at x,y. They last while the beat lasts.
* **cam**: moves the view inside the panel. `shake` is for impacts, `push` toward the action, `pan` for chases, `zoom-out` to reveal. The zoom is automatically limited so no figure/prop is cropped at the left/right panel edge (extents: standing body 105 px, wide-arm poses 165 px per unit of scale x role scale).

#### FALL rule (enforced)
The `fall` pose lies tilted 84 degrees and floats: its box is **x -200..+370, y -335..-80** per unit of (scale x role scale) around the feet point (mirrored by `flip`). So a fallen rookie at scale 0.9 is ~460 px wide. validate.py rejects (a) a fall box that leaves x 70..1010, (b) two fall boxes (or a fall box and a standing figure) that touch (gap < 8 px). 300 px spacing is NOT enough at scale 1: use different depth rows (feet y 1440 front, ~1150 back with a smaller scale), alternate `flip`, or lower the scale. The engine also nudges a faller back into the panel.

#### The recurring prop and the callback (enforced)
The top-level `prop` appears in EVERY comic of the video and is still on screen in its TWIST beat (stick it on something, hold it, let it drop in with `drop`). The LAST comic must also reuse at least one prop kind
of the FIRST comic (other than the recurring prop): the validator prints the candidates. Cast ids that no comic uses produce a WARN.

#### Layout cheat sheet (canvas px; panel x 30..1050, y 234..1532)
* Hero alone: x 300 or 780, feet y 1440, scale 1.35-1.5. Two actors: x 270 and 800, scale 1.25-1.4 (heads must not overlap: head width = 200 x scale). Three small ones: x 150 / 340 / 530 at scale <= 1.0, plus a hero at x 880 (scale 1.4).
* Head top y = feet y - 505 x scale. Put the big gag prop above or beside the heads (y 520-900) so nothing covers a face. Bubbles open above the speaker's head (max one per beat).
* A prop worn on the body: suit on the torso at (hero x, feet y - 300 x scale) with scale 1.45 for hero scale 1.4; boots at the feet; a held prop: use `hold`.
* Nothing important at y < 330 or y > 1470 (the camera push crops about 5 percent at the panel edges).

#### Writing a gag that reads in 1.5 s
1. ONE object or character is the subject (the "gag prop": give it a `face`, scale 2.4-3, keep it the largest thing). 2. SETUP shows the problem in the first frame (smoke, 7:0, a pile of rookies).
3. GAG moves exactly one thing a long distance (a card slides to the scoreboard, a rookie falls, a suit jumps onto the hero). 4. BEAT: nobody moves, they stare. 5. TWIST changes the face / text / pose of the gag prop (flip to 0:0, a padlock drops, a boot pops).
The same JSON gets another palette, outline, texture and fonts per `style`.

#### Worked example 1: SITCOM-YELLOW (video 016, s02: the scoreboard with a face)
cast: `{"modric": {"role": "player", "number": "10", "shirt": "#e8505b", "hair": "#6b4a2a"}, "rookie": {"role": "rookie", "shirt": "#4f8fd6"}, "rookie2": {"role": "rookie", "shirt": "#3fb8af", "hair": "#2b2b3a"}, "rookie3": {"role": "rookie", "shirt": "#f4a259", "hair": "#a03a2a"}, "staff": {"role": "staff"}}`
```json
{ "type": "COMIC", "bg": "stadium", "beats": [
  {"phase": "SETUP", "t0": 0, "t1": 0.26, "actors": [{"id": "modric", "x": 300, "y": 1440, "pose": "present", "emote": "sweat", "scale": 1.4, "label": "Luka Modric"}], "props": [{"kind": "scoreboard", "x": 765, "y": 780, "scale": 2.7, "text": "7:0", "face": "shock"}, {"kind": "sticker", "x": 640, "y": 1090, "scale": 0.9}], "fx": [{"kind": "smoke", "x": 765, "y": 530, "size": 0.7}]},
  {"phase": "GAG", "t0": 0.26, "t1": 0.52, "actors": [{"id": "modric", "x": 300, "y": 1440, "pose": "present", "emote": "sweat", "scale": 1.4, "label": "Luka Modric"}], "props": [{"kind": "scoreboard", "x": 765, "y": 780, "scale": 2.7, "text": "7:0", "face": "neutral"}, {"kind": "sticker", "x": 740, "y": 1010, "scale": 1.05, "anim": "shake"}], "cam": "push", "fx": [{"kind": "smoke", "x": 765, "y": 530, "size": 0.7}]},
  {"phase": "BEAT", "t0": 0.52, "t1": 0.64},
  {"phase": "TWIST", "t0": 0.64, "t1": 1.0, "actors": [{"id": "modric", "x": 300, "y": 1440, "pose": "cheer", "emote": "wink", "scale": 1.4}], "props": [{"kind": "scoreboard", "x": 765, "y": 780, "scale": 2.7, "text": "0:0", "face": "happy"}, {"kind": "sticker", "x": 920, "y": 1100, "scale": 1.0}], "sfx": {"text": "DING", "x": 280, "y": 470, "r": 150}, "fx": [{"kind": "sparkle", "x": 765, "y": 780}]}
] }
```
#### Worked example 2: INK-COMIC (video 021, s06: press room, a padlock snaps on the quote)
cast: `{"nedved": {"role": "boss", "hair": "#f2d16b", "shirt": "#4a6fa5"}, "striker1": {"role": "striker", "shirt": "#d94f4f", "number": "9"}, "striker2": {"role": "striker", "shirt": "#3fb8af", "number": "11"}, "fanA": {"role": "fan", "shirt": "#d94f4f"}, "fanB": {"role": "fan", "shirt": "#4f8fd6"}, "reporter1": {"role": "reporter"}, "reporter2": {"role": "reporter", "hair": "#2b2b3a"}}`
```json
{ "type": "COMIC", "bg": "press-room", "beats": [
  {"phase": "SETUP", "t0": 0, "t1": 0.26, "actors": [{"id": "nedved", "x": 330, "y": 1440, "pose": "idle", "emote": "smug", "scale": 1.4}, {"id": "reporter1", "x": 800, "y": 1440, "pose": "hold", "emote": "neutral", "scale": 1.2, "flip": true}], "props": [{"kind": "microphone", "x": 560, "y": 980, "scale": 1.3}, {"kind": "scoreboard", "x": 800, "y": 560, "scale": 1.4, "text": "0:14", "face": "sleepy"}]},
  {"phase": "GAG", "t0": 0.26, "t1": 0.52, "actors": [{"id": "nedved", "x": 330, "y": 1440, "pose": "shrug", "emote": "angry-cheeky", "scale": 1.4}, {"id": "reporter1", "x": 800, "y": 1440, "pose": "point", "emote": "shock", "scale": 1.2, "flip": true}], "props": [{"kind": "microphone", "x": 560, "y": 980, "scale": 1.3}, {"kind": "scoreboard", "x": 800, "y": 560, "scale": 1.4, "text": "0:14", "face": "sleepy"}], "bubble": {"who": "nedved", "text": "not up for discussion"}},
  {"phase": "BEAT", "t0": 0.52, "t1": 0.64},
  {"phase": "TWIST", "t0": 0.64, "t1": 1.0, "actors": [{"id": "nedved", "x": 330, "y": 1440, "pose": "shush", "emote": "smug", "scale": 1.4}, {"id": "reporter1", "x": 800, "y": 1440, "pose": "facepalm", "emote": "sweat", "scale": 1.2, "flip": true}], "props": [{"kind": "microphone", "x": 560, "y": 980, "scale": 1.3}, {"kind": "scoreboard", "x": 800, "y": 560, "scale": 1.4, "text": "0:14", "face": "sleepy"}, {"kind": "padlock", "x": 360, "y": 640, "scale": 1.1, "anim": "drop"}], "sfx": {"text": "CLANG", "x": 560, "y": 800, "r": 150}}
] }
```
#### Worked example 3: RUBBER-SLAPSTICK (video 035, s03: the drone camera, `hold`, a moving ball; recurring `"prop": "camera"`)
cast: `{"striker": {"role": "striker", "shirt": "#d94f4f", "number": "7"}, "keeper": {"role": "keeper"}, "coach": {"role": "coach"}, "rival": {"role": "coach", "shirt": "#3f6fb5", "hair": "#d6d2c6"}}`
```json
{ "type": "COMIC", "bg": "training", "beats": [
  {"phase": "SETUP", "t0": 0, "t1": 0.26, "actors": [{"id": "striker", "x": 270, "y": 1440, "pose": "wave", "emote": "happy", "scale": 1.35}, {"id": "keeper", "x": 760, "y": 1440, "pose": "crouch", "emote": "sweat", "scale": 1.3, "flip": true}], "props": [{"kind": "camera", "x": 540, "y": 520, "scale": 1.5, "anim": "float", "face": "smug"}, {"kind": "ball", "x": 760, "y": 1260, "scale": 2.2}]},
  {"phase": "GAG", "t0": 0.26, "t1": 0.5, "actors": [{"id": "striker", "x": 270, "y": 1440, "pose": "point", "emote": "smug", "scale": 1.35}, {"id": "keeper", "x": 760, "y": 1440, "pose": "crouch", "emote": "sweat", "scale": 1.3, "flip": true}], "props": [{"kind": "camera", "x": 540, "y": 520, "scale": 1.5, "anim": "float", "face": "smug"}, {"kind": "ball", "x": 350, "y": 1330, "scale": 2.2, "anim": "spin"}], "cam": "push", "sfx": {"text": "WHOOSH", "x": 560, "y": 1000}},
  {"phase": "BEAT", "t0": 0.5, "t1": 0.62},
  {"phase": "TWIST", "t0": 0.62, "t1": 1.0, "actors": [{"id": "striker", "x": 270, "y": 1440, "pose": "shock", "emote": "shock", "scale": 1.35}, {"id": "keeper", "x": 760, "y": 1440, "pose": "thumbsup", "emote": "wink", "scale": 1.3, "flip": true, "hold": {"kind": "thumbs-up", "hand": "R", "scale": 0.55}}], "props": [{"kind": "camera", "x": 540, "y": 520, "scale": 1.5, "face": "happy"}, {"kind": "ball", "x": 350, "y": 1330, "scale": 2.2}], "sfx": {"text": "DING", "x": 780, "y": 780}}
] }
```

#### COMIC do / don't
DO keep the recurring prop in the TWIST beat. DO move at most two things per GAG step. DO use `face` for living objects. DO vary bg / camera / props between videos.
DO run `python3 validate.py FILE --comics-only` while iterating (it checks only the comics) and look at the contact sheet plus 2 full frames per comic.
DON'T write text on props except digits and allowed phrases (signs from the brief such as "NOT UP FOR DISCUSSION" are only allowed if the phrase is in the narration: use `bubble.text` for it, or an icon).
DON'T put a sfx on the silent BEAT. DON'T skip the BEAT. DON'T move actors in the BEAT. DON'T use real crests, logos or photos (a caricature = a cast colour + a prop + `label`).
DON'T place the gag prop under the hero's face. DON'T give a TWIST less than 0.30 of the clip. DON'T use more than 4 actors / 7 props in a beat. DON'T invent names for poses or props (add them to the library, see NOTES.md).

#### Common mistakes (all caught by validate.py)
`t0 must continue from previous t1` (gap or overlap), `SETUP must end between 0.18 and 0.34`, `no hero figure big enough` (scale too small), `recurring prop must still be on screen in the TWIST beat`,
`the last comic must call back to the first comic`, `the silent BEAT cannot add, remove or move props` / `freezes the action`, `bubble.text is not copied from the narration`, `sfx.text must be one of ...`, `x outside 60..1020`.

## 5. Do / Don't
DO keep text short; DO use different icons/boards between videos; DO read the contact sheet and 2-3 full frames per type after rendering.
DON'T put text that is not in the sources; DON'T use `bet`, `odds`, `tips` in your own strings; DON'T exceed word limits (the validator counts words); DON'T rename sequence ids; DON'T edit anything outside `H/v2/` .

## 6. Timing (for reference)
Every clip = `round(plan_frames/24*30)` frames at 30 fps (36 -> 45 = 1.5 s, 42 -> 53, 48 -> 60). 0.25 s transition IN at the start, 0.25 s transition OUT at the end (included in those frames). Elements enter at ~0.2-0.5 s and the "hit" lands near the end: 1.5 s clips are tight, so do not write long text.
