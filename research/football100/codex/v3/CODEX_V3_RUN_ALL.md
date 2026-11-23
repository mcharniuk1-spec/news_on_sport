# CODEX V3 KICKOFF: redraw posters and all interludes for videos 011-100 in the sitcom-yellow style

Work inside `research/football100`. Read `codex/v3/CODEX_V3_MASTER_PROMPT.md` first: it is the full rulebook (style, readability, posters, brand, method, workflow). This message only says what to do and in which order.

## Goal
- 90 posters: `poster3/NNN.png` (1080x1920).
- 1,204 animated sequences, 40,272 frames at 24 fps: `anim3/NNN/sKK/f0001.png...` (frame counts in `codex/v3/plan_v3.json`; briefs in `codex/v3/plan/NNN.md`). This includes new micro-inserts (ids s51 and up).
- Everything in ONE original sitcom-yellow cartoon look (yellow skin, flat colour, thin outline). Original characters only.

## Rules that matter most
1. Text is short: main text 2 to 7 words per scene or poster, plus at most 2-3 tiny reaction words. Big, outlined, readable at phone size.
2. Top 12 percent and bottom 20 percent of every frame: no text, nothing important. Key text inside x=60..900.
3. Posters: one big comic panel, the subject caricature (hair, kit colour, number, prop, NAME label), one hero prop for the thesis, a reacting fan; the About Football badge from `brand/portrait/aboutfootball_corner_badge.png` at the lower left (x=60, bottom edge at y=1500). Never a wide logo.
4. Characters big (35 percent of frame height or more). Same cast in every sequence of a video (draw `anim3/NNN/_sheet.png` first).
5. Build sequences with keyframes plus code in-betweening (Python in `anim3/_src/`), not 40,000 separate generations. Every frame distinct.
6. Safety: no invented quotes, no betting wording, none of the sensitive topics, no logos, crests, photos or existing show characters.

## Loop (resume-safe)
1. `python3 codex/v3/check_v3.py --todo --wave 0` lists missing posters (ids like `NNN/poster`). Do wave 0 for all 90 videos (sheet + poster). Then wave 1 (HOOK, NEWS, COMIC1, micro-inserts), wave 2 (INTERVIEW, PROVOC, COMIC2), wave 3 (STATS, COMIC3).
2. Take the first id, read its brief in `codex/v3/plan/NNN.md`, draw it.
3. `python3 codex/v3/check_v3.py --fix --video NNN` (flattens alpha, resizes 9:16 images, reports duplicates, wrong counts, blanks). Redraw only what it reports.
4. Append `NNN poster done` or `NNN/sKK done` (with `, note: ...` if you changed a beat) to `anim3/PROGRESS.md`.
5. After each wave print `WAVE N DONE`, then continue without waiting. If session or quota ends, stop cleanly after the current item; a new session starts again at step 1.

Do not edit `scripts/`, `deliver/`, `FINAL_100*/`, `clips/`, `v2/`, `anim/` or any existing `.py`. Do not run `codex/check_anim.py`. Do not ask questions unless a brief is missing.

## When it ends
`python3 codex/v3/check_v3.py` must print `90/90 posters, 1204/1204 sequences pass (40272/40272 frames)`. Then reply `ALL V3 ART DONE` with the number of redrawn frames, changed beats and name substitutions. Otherwise give the count and the first 10 failing ids.
