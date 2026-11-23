# news_on_sport: football news + Shorts analysis + 100-video production kit

Everything needed to understand, repeat and extend a batch of **100 vertical English football Shorts for a UK audience**
(CTA: aboutfootball.uk, 18+). **No video, audio or image files are in this repository** (they are large and are rebuilt by the scripts).

## What is here
| Path | Content |
|---|---|
| `research/football100/news/` | News harvest: 30 lane files (`lane_01..30.json`, 1,104 raw items), `clusters.json` (800 deduplicated stories) and `dedupe.py` |
| `research/football100/db/f100.sqlite` | The working database: `news` (800 analysed, deduplicated news items, FTS indexed), `bo` (Ballon d'Or winners), `frames` (220 frame records) |
| `research/football100/corpus/` | Corpus of analysed YouTube channels/videos: `corpus_all.json` (2,227 videos), `shorts_meta.jsonl` (1,000 Shorts), `long_meta.jsonl` (1,227 long videos), `long_pool.jsonl` (31,245 candidates), search logs, `subs/` (subtitle transcripts) |
| `research/*.json`, `research/football_shorts.db`, `research/subs/` | First analysis round: 220 videos with transcripts (`transcripts.json`), 193 Shorts profiles (`shorts_profiles.json`), channel stats, topics, frame-by-frame report, SQLite with `channels`, `videos`, `frames` (4,942 sampled frames), `reuse_segments` |
| `research/*.py` | Collection and analysis tools: `collect.py`, `yt_scan.py`, `yt_pick.py`, `yt_topics.py`, `transcripts.py`, `process*.py`, `build_db.py`, `gen_report.py` |
| `research/football100/scripts/` | **The 100 video texts**: `NNN.json` (lines of narration `vo`, on-screen `card`, footage search terms, inserts) plus `assign.json` (voice, style, character limit per video) |
| `docs/SCRIPT_RULES.md` | **Rules for how the texts were written** and how they are checked (`check_scripts.py`) |
| `docs/PIPELINE.md` | Methods and step-by-step instructions for the whole pipeline |
| `research/football100/codex/` | Prompts for the animated interludes (v1 flipbook and v2 24 fps frame-by-frame), per-video plan `v2/plan/NNN.md`, `plan.json` |
| `research/football100/v2/` | v2 production: Remotion library (`remotion/src`, `DSL.md`), per-video interlude content (`content/NNN.json`), assembler (`assemble.py`), captions, timing, verification |
| `research/football100/report/` | Analytics workbook builder and labels (hook type, topic, structure, voice) |
| `research/football100/FINAL_100/` | `football100_report.xlsx/.csv`, `index.csv` (metadata of the 100 videos, no media) |

## Reproduce
See `docs/PIPELINE.md`. Large inputs (footage, voice, rendered clips, final MP4s) are not versioned.
Secrets (API keys, OAuth tokens) are never stored here: provide them as environment variables.

## Data notes
- The analysed YouTube data (titles, stats, transcripts, frame descriptions) was collected for analysis of formats, hooks and topics. Transcripts belong to their original creators; use them for research, not republication.
- News items are summaries and links of public reporting; every factual claim in the scripts was written from them and must stay traceable.
