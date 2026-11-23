# Codex flipbook inserts (football100)
FAST PATH: paste `CODEX_RUN_ALL.md` once. Codex loops over all 261 scenes by itself (resume-safe via `python3 codex/check_flip.py --todo`, log in `flip/PROGRESS.md`). Steps below are the manual variant.
When Codex is done: `python3 codex/check_flip.py` must print 261/261, then tell Claude to run the final assembly (frames_to_clips -> build100 -> deliver -> cover_frame -> report).

1. Open Codex in this project folder (`research/football100`). Paste `CODEX_MASTER_PROMPT.md` as the first message.
2. Attach or paste `scenes_batch_01.md`. Codex draws 6 scenes (12 frames each) and replies `BATCH 01 DONE`. Repeat for batches 02..44 (261 scenes, 100 videos).
3. Frames must land at `flip/NNN_k/f01.png ... f12.png` (NNN = video no, k = insert no). Character sheets go to `flip/_sheets/`.
4. Quick check: `ls flip/*/ | grep -c png` should be 12 x scenes; `python3 codex/frames_to_clips.py` lists any folder with missing frames.
5. Build clips: `python3 codex/frames_to_clips.py` (all) or `... 007_2 007_3` (some); add `--force` to rebuild. Output: `clips/flip_NNN_k.mp4` (1080x1920, 30 fps, 12 frames at 6/s = 2.0 s).
6. `build100.py NNN` picks `clips/flip_NNN_k.mp4` up automatically (a 2.0 s cutaway after the line given by `after_line`). Missing clips are skipped silently, so check all clips exist first.
7. Regenerate the scene files after editing any `scripts/NNN.json` inserts: `python3 codex/build_scenes.py`.
8. `codex/add_inserts.py` (already run) added the 2-3 story inserts per non-comic video and repaired `after_line`. Backup of the original scripts: `scripts.bak_inserts/`.
