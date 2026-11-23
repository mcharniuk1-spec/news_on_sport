# Pipeline (methods and instructions)

1. **Collect and analyse**: `research/collect.py`, `yt_scan.py`, `yt_pick.py`, `yt_topics.py`, `transcripts.py`, `process*.py`, `build_db.py`, `gen_report.py` -> `football_shorts.db`, `transcripts.json`, `shorts_profiles.json`, topics and report.
2. **News**: `football100/news/lane_*.json` -> `dedupe.py` -> `clusters.json` -> `db/f100.sqlite` (`fdb.py` is the query tool).
3. **Scripts**: `assign.py` (voice/style/limit) -> write `scripts/NNN.json` (rules in `docs/SCRIPT_RULES.md`) -> `check_scripts.py`.
4. **Voice**: `voice_kokoro.py` (local Kokoro) and `dl_el.py` (ElevenLabs). Needs your own keys as environment variables.
5. **Footage**: `fetch_footage.py` (yt-dlp; respect rights).
6. **Animated interludes**: plan in `codex/v2/` (761 sequences, 24 fps frame budgets). Videos made with Codex PNG frames use `v2/tools/anim_to_clips.py`; the rest are rendered by the Remotion library in `v2/remotion` (`DSL.md`, `render.mjs`, `validate.py`) from `v2/content/NNN.json`.
7. **Assembly (ffmpeg only)**: `v2/tools/asr.py` (faster-whisper word timings) -> `v2/tools/timing.py` -> `v2/assemble.py NNN` (footage with zoom/dissolves, interludes, karaoke subtitles, cards, music, loudnorm -14.5 LUFS, cover as first 3 frames).
8. **Verify**: `v2/verify.py` and `v2/tools/check_clips.py`.
9. **Report**: `report/build_features.py` and `report/export_report.py` -> `FINAL_100/football100_report.xlsx`.
