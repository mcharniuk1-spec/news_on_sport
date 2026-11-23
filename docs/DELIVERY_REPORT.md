# Delivery report: 100 Shorts (v2, interludes integrated)

Final files (not in this repo): `research/football100/FINAL_100_v2/videos/NNN_<slug>.mp4` (100 files, 1.84 GB). Earlier exports are untouched in `FINAL_100/` and `deliver/`.

## What was built
- Videos 001-015: Codex frame-by-frame interludes (116 sequences, 4,938 PNG at 24 fps), conformed to 30 fps.
- Videos 016-100: 645 interludes created with Remotion (`research/football100/v2/remotion`, DSL in `DSL.md`), content in `v2/content/NNN.json`.
- Assembly with FFmpeg only (`v2/assemble.py`): footage with zoom and dissolves, interludes at their narration timecodes, karaoke subtitles (<=5 words, 2 lines), headline cards outside interludes, music + whoosh, loudness -14.5 LUFS, poster as the first 3 frames.

## Checks (all executed)
| Check | Result |
|---|---|
| 100 files open, 1080x1920, 30 fps, H.264 yuv420p, AAC stereo 44.1 kHz | 100/100 |
| Duration equals the planned timeline | 100/100 |
| Integrated loudness about -14.5 LUFS, true peak below -1 dBFS | 100/100 |
| First frame equals the poster, poster not held longer than 3 frames | 100/100 |
| Subtitles visible at sampled spoken times (>=70 % of samples) | 100/100 |
| Outro card present at the end, no black or frozen frames | 100/100 |
| Interlude clips: format, frame count, no identical neighbouring frames, no blank frames (`v2/tools/check_clips.py`) | 761/761 |
| Frame-exact placement of every interlude (median offset of 0 to 1 frame, pixel diff < 1 on most; `v2/verify_seq.py`) | 761/761 in 100/100 videos |

Known limits: two poll cards (021 s08, 022 s06) have weaker label contrast; some characters are generic stand-ins (animals look like bears). Footage is third-party match footage: review rights before wide publication.
