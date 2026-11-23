# CODEX KICKOFF: draw all flipbook inserts for the 100 football Shorts

You work inside the project folder `research/football100`. Read `codex/CODEX_MASTER_PROMPT.md` first. It is the full rulebook: output format, style labels, safety, craft and checklist. This message only tells you what to do and in which order.

## Goal
Draw 261 hand-drawn 2-second flipbook scenes (12 frames each, 3132 PNG files in total). They are inserted into 100 vertical football Shorts as cutaways, about 10-12 percent of the running time. Scene files are `codex/scenes_batch_01.md` ... `scenes_batch_44.md` (6 scenes each, the last one has 3).

## Work loop (resume-safe)
1. Run `python3 codex/check_flip.py --todo`. It prints the scene ids that still need drawing. A scene that passes is finished: never redraw it.
2. Take the first scene id on that list. Open its batch file, read the scene block (style, characters, story, 12-row beat table).
3. Make sure `flip/_sheets/<STYLE>.png` exists for the scene style. If it does not, draw it first (rules in the master prompt, section 2).
4. Draw f01, then draw f02 ... f12 one after another by editing the previous frame (image-to-image). Keep characters, background, palette and camera identical. Save each frame at once to `flip/NNN_k/fNN.png`.
5. After the scene, run `python3 codex/check_flip.py --fix --batch NN` (NN = batch number). Redraw only the frames it reports. The script flattens alpha and resizes a 9:16 image to 1080x1920, so a generator size of 1024x1792 or similar is fine.
6. Append one line to `flip/PROGRESS.md`: `NNN_k done` (or `NNN_k done, note: <changed beat or refusal and substitute>`).
7. Go to the next scene. After the last scene of a batch print `BATCH NN DONE` with the short report from master prompt section 7. Then continue with the next batch without waiting, unless I say stop.
8. If you run out of session, time or image quota, stop cleanly after the current scene. A new session starts again at step 1 and loses nothing.

## Hard rules (short version)
- Exactly `flip/NNN_k/f01.png ... f12.png`, no other files in the folder. 12 distinct drawings, 1080x1920, opaque, 9:16.
- Fixed camera, same characters and background in all 12 frames. Setup 1-3, gag 4-8, silent beat 9, twist 10-12 as the beat table says.
- Keep action in the centre: leave the top 12 percent and the bottom 18 percent plain background (captions and UI cover them).
- Text only when the story quotes a word or number. Spell it exactly, in large block letters.
- Original cartoon characters only: no logos, no real badges, no photos, no franchise characters. If the generator refuses a named person, draw a fictional cartoon player with the same role and a distinctive prop, and keep going.
- Nothing about injuries, illness, drugs, crime, family, politics, religion, violence or sex. Replace such a beat with a harmless gag with the same setup/gag/twist and note it in `flip/PROGRESS.md`.
- Do not ask me questions unless a scene file is missing. Do not edit `scripts/`, `deliver/`, `FINAL_100/`, `clips/` or any `.py` file.

## When the work ends
Run `python3 codex/check_flip.py`. When it prints `261/261 scenes pass`, reply `ALL SCENES DONE` with: number of redrawn frames, list of changed beats, list of substitutions for refused names. If fewer than 261 pass, reply with the count and the first 10 failing ids, and stop.
