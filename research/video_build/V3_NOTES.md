# v3 videos: Ronaldinho (97.6 s) and Mudryk x Gordon (111.7 s)
Files: `football_ronaldinho_v3.mp4`, `football_mudryk_gordon_v1.mp4` (1080x1920, 30 fps, about -14.5 LUFS).
Palmier projects: "Ronaldinho at 46 v3b", "Mudryk and the dump truck v1c". Rebuild: `python3 build3.py ron|mud`, export `python3 exp3.py ron|mud`.
Voice: Kokoro bm_george (local, free). Music: Seth_Makes_Sounds "Phonk Song [preview]" CC0, drop aligned to the story. SFX: CC0 Freesound (crowd, kicks, ambience; links in sfx/) plus a synthesised whistle.
Animated cards: HyperFrames HTML (hf/cards.py), rendered to clips/hf_*.mp4.
Scripts: SCRIPT_DRAFTS.md (drafts + fact pack), v3/scripts.json (final spoken text). Comedy punch-up by a separate writer agent; facts checked against the fact pack.
Interview: "В гостях у Дмитра Гордона" (YouTube Sl5PO_x9L94, 18 Nov 2026), spoken Russian; English captions written from a local Whisper transcript, so check wording before publishing.
## Codex inserts (6 x 2 s)
Prompt: FLIPBOOK2_PROMPT.md. When the frames arrive in gfx/flip2/, run:
  FLIPBASE=gfx/flip2 OUTPREFIX=flip2_ python3 assemble_flipbook.py R1 15   (same for R2 R3 M1 M2 M3)
then `python3 build3.py ron` and `python3 build3.py mud` (slots pick up clips/flip2_<ID>.mp4 automatically; until then they show footage).
