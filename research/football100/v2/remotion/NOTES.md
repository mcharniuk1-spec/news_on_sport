# NOTES: Remotion interlude library (agent A)

Remotion 4.0.290 / React 18.3.1, system Chrome (`/Applications/Google Chrome.app`), no extra npm packages. Fonts are macOS system fonts referenced by name
(Arial Rounded MT Bold, Arial Black, Impact, DIN Condensed, Comic Sans MS, Marker Felt, Rockwell, Georgia, Courier New): available to Chrome on this Mac, nothing downloaded.

## Architecture
`render.mjs` -> bundle -> composition `Interlude` (inputProps `{no, style, seqId, type, content, frames24, index, cast, prop, accent}`; `calculateMetadata`: frames = round(frames24/24*30), 30 fps, 1080x1920)
-> `Interlude.tsx`: theme from style (`getTheme(style, no)`; FLAT-POP rotates through 6 palette variants by video number), `SceneCtx` (theme, t, frame, dur, seed, cast, prop) ->
template by `type` (`templates/index.ts`) -> `Texture` overlay -> transition IN (frames 0..7) / OUT (last 8 frames). All art is SVG; everything reads colours only from `theme.palette`.
Determinism: no Math.random; `core/rng.ts` (hash + mulberry32) seeded by `${no}-${seqId}`.

## File map (src/)
| file | what |
|---|---|
| `core/vocab.ts` | SINGLE SOURCE of vocab lists (poses, emotes, props, bgs, anims, boards, transitions...). `node gen_vocab.mjs` -> `vocab.json` (validate.py) and refreshes DSL.md lists |
| `core/ease.ts, rng.ts, color.ts, text.ts, ctx.tsx` | easing (back/elastic/bounce/spring), seeded PRNG, colour mix/shade, `fitText` (canvas-measured auto-fit, never overflows), scene context + safe-zone consts |
| `theme/themes.ts` | 9 themes: palette tokens, skins/hairs/shirts, outline width, texture, eye style, limb style (straight/rubber), cutout shadow, line-boil, fonts, motion personality |
| `rig/Actor.tsx` | THE character: `<Actor role pose emote x y scale flip t talk look hold skin hair shirt number id squash rot lift bust/>` (feet anchored). IK arms, FK legs, auto ground contact, breathing, blink, lip flap, squash/stretch, pose timelines with overshoot blend, hand-held props |
| `rig/poses.ts, Face.tsx, Hair.tsx, roles.ts` | 26 poses (+`cyc` loops so nothing is static), 12 emotes with FX (sweat, zzz, tears, hearts, dizzy stars), 14 hair/headwear styles, 14 roles |
| `props/draw.tsx` | 97 flat-vector props/icons (centred, ~200 units). `props/Prop.tsx`: `<Prop kind x y scale rot anim t0 text amp/>`, `props/anim.ts`: the 14 presets (entrances settle then idle-float) |
| `bg/Backgrounds.tsx` | 18 animated backgrounds `<Background kind shift/>` |
| `ui/Boards.tsx` | `Board` (sign, neon, stamp, typed, ticket, scoreboard), `Panel`, `Bubble` (speech/thought), `LowerThird`, `Ticker`, `PollBar`, `countStr` (number counters) |
| `ui/Txt.tsx, Fx.tsx, Texture.tsx` | `FitText`; confetti, sparkles, speed lines, puffs, shockwave, `Burst` (sfx star), `shakeAt`; halftone / paper grain / scanlines / speed-line overlays |
| `transitions/transitions.tsx` | 15 transitions `(cover 0..1) => svg`; IN uses cover=(1-p)^2, OUT p^2 so neighbouring frames always differ; pair chosen by `transitionPair(no, index)` |
| `templates/{Hook,News,Interview,Provoc,Stats}.tsx` | the five non-comic templates (casting helpers `castFor` / `distinctFrom` in `templates/common.tsx`, `lookOf` in `rig/Actor.tsx`) |
| `templates/Comic.tsx`, `props/PropFace.tsx` | the COMIC engine and the prop-face overlay (agent B) |
| `dev/Sheets.tsx` | dev-only `RigSheet`, `PropSheet`, `BgSheet` compositions |
| tools: `tools/still.mjs` (`--content F --seq s01 --frames 3,20`, or `--id RigSheet --props`), `stylegrid.mjs` (9 styles x 5 types), `transgrid.mjs`, `framecheck.py`; `../tools/contact.py` |

## COMIC engine (agent B)
`templates/Comic.tsx` (registered in `templates/index.ts`; `ComicPlaceholder.tsx` is now unused). Full authoring reference: DSL.md chapter COMIC. Validation: `validate.py` section `BEGIN/END COMIC RULES` (+ `_check_comic_beat`, `validate_comic_final`).
* **Structure**: `resolve()` turns the authored beats into absolute seconds + normalised states (BEAT inherits actors / props / bubble). The comic is drawn in a fixed rounded PANEL (`PANEL` const: x 30..1050, y 234..1532) inside an `overflow:hidden` div; the camera
  (`push|pan|shake|zoom-out`, punch on TWIST, sfx shake) is a CSS transform on the inner 1080x1920 div, so camera moves never touch the frame. Outside the panel: board colour + drifting accent dots, ink border, soft shadow.
* **Tracks**: actors by cast id, props by `kind#occurrence`. Same track in consecutive beats -> position/scale/rot tween with `outBack` over `BW` = 0.3 s. A new actor RUNS in from the nearest edge (EN = 0.38 s), an absent one runs out, a > 140 px move uses the `run` pose
  (pose timeline built by `poseSpec`, blended by the rig with overshoot + squash pulse). Props: entrance anims only on first appearance, text change = split-flap flip, disappearing prop shrinks. Prop `face` (props/PropFace.tsx) = googly eyes + mouth for any prop.
* **Silent BEAT**: inherited state, no sfx/fx/cam, vignette, everybody looks at the recurring/first prop (`@gag` gaze). **TWIST**: white flash 0.12 s + camera punch + ring from the gag prop, then slow push.
* Extras added to shared files: `Bubble` accepts `children` (icon bubbles); `sticker` prop draws a ball motif (or `text`); `Crowd` has a travelling wave; vocab `FX_KINDS`, `LAYERS`, `HANDS`. Name/caption plates (`label`) are drawn by `Plate` inside Comic.tsx.
* **Cost**: a 2.0 s comic (60 frames) renders in ~4 s at `--concurrency 2` (same as the other types); no Math.random anywhere.

## 016 review round (safe zones, casting, fall rule)
* Entrances respect the safe zones: `Board` sign = scale slam (wires 56 px), stamp = small slam (1.16x), typed = scale pop; `Ticker` (`from='side'`) and name boards slide from the side. HOOK board y 282..678, hero lowered (feet 1566, scale 1.6), confetti/sparkles/shockwaves are drawn BEHIND the board.
* NEWS layout: card y 240..1132, figure feet 1118 (scale 1.6), lower third y 1146, ticker y 1384..1450. STATS: cards y 266..1500; score values flip from "?-?" instead of counting through a wrong score. PROVOC: bars x 490 w 880, crown badge in its own slot at x 985, winner effects behind the board/bars, fans enter from the sides, feet y 1500, scale 0.82.
* Casting: NEWS/INTERVIEW subject = `cast` entry matching `actor` / `subject_cast` / a word of the name (same id => same hair style, colours, number as the comic); the INTERVIEW reporter gets a different hair colour/style (`distinctFrom`). `suit` prop is now a jacket with sleeves.
* COMIC engine: name plates float above the head; camera zoom is limited by the extents of everything on stage (`reachOf`, `fallRect`); sfx burst is clamped into the visible panel; `fall` boxes are nudged inside the panel; smoke rise scales with `size`.
* validate.py: sfx whole-burst extent, fall-box inside/collision rules, label+bubble clash, standing-reach WARN. Flat first/last frames of every clip are the transition covers by design (verify.py needs them); frames = round half up (see SPEC_INTERLUDES.md).

## How to add
* **prop/icon**: add name to `PROPS` in `core/vocab.ts`; add `'name': (k) => <g>..</g>` in `props/draw.tsx` (use `k.pal`, `k.S` outline props, `k.t`); `node gen_vocab.mjs`.
* **pose**: add `name: P({...})` in `rig/poses.ts` (hand targets `hL/hR` are in rig space, legs `[hip,knee]`, `cyc` for loops) and the name to `POSES` in vocab.ts.
* **emote**: add to `EMOTE_DEFS` in `rig/Face.tsx` + `EMOTES` in vocab.ts. **role**: `rig/roles.ts` + `ROLES`.
* **background**: function in `BG` (`bg/Backgrounds.tsx`) + `BGS`. **transition**: function in `TR` + `TRANSITIONS` (15 now; the pair formula uses `TRANSITIONS.length`).
* **board / template type**: `ui/Boards.tsx` + `BOARDS`; templates in `templates/`, registry `templates/index.ts`, validator in `validate.py`.
* **theme**: entry in `THEMES` (`theme/themes.ts`); label must be in `STYLES`.

## Verified (video 016, FLAT-/SITCOM theme; video 043 CUTOUT-PAPER test in review/_styletest)
All 8 mp4: h264, yuv420p (bt709 tv range), 1080x1920, 30 fps, no audio, faststart, correct frame counts; `framecheck.py` finds no identical neighbouring frames (min mean diff on 108x192 thumbs 0.109 / 255).
Render time at `--concurrency 2` (no other load): 2.0 s clip (60 frames) 3.8 s; 1.5 s clip 3.0 s; whole video of 8 clips ~28 s incl. bundling.

## Known weaknesses
* Characters are front-view only (flip just mirrors); no turnaround, so "walking away" / profile actions are approximated with poses.
* Prop silhouettes are simple (scarf, chart-down arrowhead, ball centre patch are the weakest); no real logos by design.
* Background floors are plain and large in the bottom safe zone; backdrops are not parallaxed with real depth.
* `INK-COMIC` Impact "0" resembles "O" at small sizes; DIN Condensed (ANIME/SCIFI) labels render small because the font is narrow.
* NEWS fact line wraps to 2 small lines for 8-10 word facts; keep facts <= 7 words for punch.
* Hook "hit" burst + confetti happen ~0.55 s before the end, so they overlap the OUT transition by design.
* COMIC: characters are front-view only, so "walking away"/profile gags are approximated with poses and `flip`; `fall` is a tilted floating figure with a big box (x -200..+370, y -335..-80 per unit scale; see DSL FALL rule: use depth rows / flip, validate.py rejects overlaps); the panel leaves ~380 px of plain board colour under the comic (bottom safe zone); the comic 'suit' is a jacket overlay (layering illusion);
  held props follow the hand but have no grip pose; prop `face` is a generic googly face (the scoreboard keeps its digits, eyes sit on top); label plates are ASCII/Latin fonts only; the suit-on-torso trick (suit prop over the actor) is a layering illusion, not a real outfit swap.
