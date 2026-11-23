# v3 integration (Codex comic frames)

Scope delivered by Codex and integrated: 4,956 frames, 148 sequences, videos 011-020 and 034 (all 11 pass `codex/v3/check_v3.py`).
Videos 021-100 (except 034) have no approved comic art yet (remaining 35,316 frames); their exports stay at v2.

Pipeline:
1. `python3 v3/to_clips.py NNN ...` - PNG sequences (24 fps) to 30 fps clips in `v3/seq/NNN/`.
2. `python3 v3/assemble_v3.py NNN` - same assembler as v2 but uses `codex/v3/plan_v3.json` (scenes plus micro-inserts such as the question card, black beat, interview panel and 1-second gag), start times shifted by the v2 ASR timing, and a cover cut from the HOOK scene with the portrait About Football badge. Output: `FINAL_100_v3/videos/`.
3. `python3 v3/verify_seq_v3.py NNN ...` (frame-exact placement) and `python3 v3/verify_v3.py NNN ...` (format, loudness, cover, captions).

Interviews: interview panels use only words from the narration; no real interview footage is inserted (rights).
