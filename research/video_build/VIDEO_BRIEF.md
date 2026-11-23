# Ronaldinho at 46: Short v1 (18.6 s, 9:16, British English)

File: `ronaldinho_comeback_short_v1.mp4` (1080x1920, 30 fps, H.264 + AAC).
Palmier project: "Ronaldinho Comeback Short" (`~/Documents/Palmier Pro/`). Rebuild scripts: `pm_import.py`, `pm_build1.py`..`pm_build3.py`, `insp.py`. `mcp.py` is a small client for the Palmier HTTP MCP (`127.0.0.1:19789/mcp`).

## Top 10 news in the 110-Short sample (news-style Shorts, by views)

| # | Story | Source Short | Views | Checked |
|---|---|---|---|---|
| 1 | **Ronaldinho, 46, returns to pro football with Ravenna (Serie C)** | FutVibes `n-GfaJGc0NA` | 1.63M | Yes, several outlets (SI, Business Today, Flashscore) |
| 2 | Ronaldinho's first Ravenna training session | FutVibes `rMWP08YBVlM` | 1.62M | Yes (same story) |
| 3 | Portugal lose 4-0 in first game without Ronaldo | FutVibes `VKMNvcj5-6Q` | 1.47M | No |
| 4 | Why PSG give every player a Bentley | FutVibes `6RlxDcWmf5s` | 1.30M | No |
| 5 | Bernardo Silva "banned" from Portugal after backing Ronaldo | FutVibes `13kE1aJpg-o` | 1.29M | No |
| 6 | Doué's first training after losing a tooth | FutVibes `EnpbLBBfPgw` | 1.27M | No |
| 7 | Portugal's new No. 7 gets a mocking nickname | FutVibes `ESQ-x9nVcWc` | 1.25M | No |
| 8 | Jobe Bellingham's England debut | FutVibes `nl8h1aql_uU` | 1.17M | No |
| 9 | Yamal found in GTA 6 | FutVibes `aPVgbkOZP8I` (trending version 45.7M) | 1.17M | No |
| 10 | Real Madrid "mog" Barcelona's 2027 kits | FutVibes `Rqn7IH-dQXs` | 0.95M | No |

Why #1: highest views among news items, confirmed by independent outlets, built-in comedy (a 46-year-old in a third-division side), and plenty of real footage of the same person.

## Voice-over (robotic UK voice: macOS "Daniel" + tremolo/echo)

> Ronaldinho. Forty-six years old. Eleven years without pro football. Everyone said it is a joke. Third division. White shirt. Flares. Smoke. Chaos. Brutal league. Ravenna two, Forlì nil. Retired? Never. Who is next? Your grandad?

Facts used (from news reports): age 46, last played for Fluminense in 2015 (about 11 years), signed for Serie C club Ravenna, Ravenna beat Forlì 2-0 on his return. Not used: any claim about who scored or his own goals.

## Shot list (frame-by-frame logic follows the FutVibes style: one caption beat per 1-2 s, flash on every cut, punch-in zoom on every shot)

| t (s) | Shot | Source | Caption | Effect |
|---|---|---|---|---|
| 0.0-1.8 | Tunnel walk | UOL Esporte `bQ7Q-Jh8bN8` 0-1.8 s | BREAKING / RONALDINHO | zoom in, flash cut |
| 1.8-3.4 | Close-up, beanie and glasses | UOL `bQ7Q-Jh8bN8` 5.2 s | 11 YEARS | zoom out |
| 3.4-4.6 | **Generated still 1:** birthday cake with 46 candles | `gfx/gen_01_cake.png` (placeholder) | A JOKE?! + laughing emoji | glow, zoom |
| 4.6-6.1 | Warm-up close-up | SVMM `feRjEy72wvE` 38.6 s | THIRD DIVISION | zoom |
| 6.1-7.5 | Walk-out with mascot | SVMM 51 s | WHITE SHIRT | zoom out |
| 7.5-9.1 | Flares and smoke | IRFHD `EqnmzLHXZrw` 0 s | FLARES / SMOKE / CHAOS + fire emoji | glow, zoom |
| 9.1-10.6 | Tackle | SVMM 217.4 s | BRUTAL LEAGUE | shake, motion blur |
| 10.6-11.8 | Wide goalmouth | SVMM 204.5 s | THEN... + skull emoji | zoom |
| 11.8-13.8 | Score card (own graphic) | `gfx/card_pitch.png` + text | RAVENNA 2-0 FORLÌ, SERIE C | slide-up, pop-in |
| 13.8-15.2 | Close-up, side | SVMM 253.5 s | STILL GOT IT? | zoom |
| 15.2-16.6 | **Generated still 2:** old slippers to golden boots | `gfx/gen_02_boots.png` (placeholder) | RETIRED? NEVER. | glow |
| 16.6-18.4 | Smile close-up | SVMM 265 s | WHO'S NEXT? / YOUR GRANDAD? | zoom |

Audio: synthesised 140 bpm beat (-17 dB), whoosh/hit/glitch/ding/womp effects (-6 dB), voice (+2 dB). All source-video sound was removed.

## Open points

- Both generated stills are rough placeholders. Replace them with the Codex output (prompt below), keeping the same file names, then re-import in Palmier and swap the clip (or rerun `pm_build1.py`).
- Footage is broadcast and UOL/Instagram material. The sound and on-screen text are removed, but the picture is still third-party. Treat this as an internal draft; before publishing, get rights or replace shots with licensed clips.
- The UOL clips carried a burned-in "WARM UP" sticker. It is blurred out and sits under the captions, so the blur band is visible as a soft strip.
- Palmier is signed out (no credits), so no paid generation was used. Voice and sound effects are local and free.

## Prompt for Codex (GPT Image)

```text
Create two vertical 1080x1920 PNG images for a funny football news Short. Style: bold comic/sticker illustration, thick black outlines, flat saturated colours, radial sunburst background, high contrast, slightly messy hand-drawn energy. Leave the lower third (rows 1300-1700) visually calmer because captions go there. No real people, no faces of real players, no logos, no brand names, no readable text or numbers except where stated.

1) File gen_01_cake.png: a giant birthday cake on a football pitch, covered in many burning candles that form the number "46", a crown-shaped party hat on top, confetti, and a cartoon football wearing sunglasses next to it. Warm yellow and orange sunburst background.

2) File gen_02_boots.png: split composition, top half a pair of worn, fluffy brown retirement slippers with a walking stick, a big yellow arrow in the middle, bottom half a glowing pair of golden football boots with sparkles and speed lines. Deep purple and navy sunburst background. No text.

Save both files at exactly 1080x1920, PNG, no transparency, in <PROJECT_ROOT>/research/video_build/gfx/ (overwrite the placeholders).
```
