# CODEX KICKOFF v2: animate all 100 football Shorts at 24 fps

Work inside `research/football100`. Read `codex/CODEX_V2_MASTER_PROMPT.md` first, in full. It is the rulebook: output format, production method (keyframes plus code in-betweening), quality bar, sequence types, transition library, text rules, safety and checklist. This message only says what to do and in which order.

## Goal
Produce 32,646 PNG frames at 24 fps (1080x1920, opaque, every frame different) for 761 sequences, 288 to 396 frames per video (12 to 16.5 s), for all 100 Shorts. Hook questions, news cards, interview inserts, comic stories, provocation polls, stat-icon montages and animated transitions. The plan is `codex/v2/plan.json`; per-video briefs are `codex/v2/plan/NNN.md`.

## Do this now
1. The plan already exists. Do not regenerate it and do not edit `codex/v2/`.
2. Build the shared toolbox once: `anim/_src/toolkit.py` (easing, rig, outlined text, icons, lower-third, ticker, counter, poll bars, speech bubble, transitions, particles). Prove it on one test sequence before the real work.
3. Run the resume loop from section 9 of the master prompt: `python3 codex/check_anim.py --todo --wave 1`, then wave 2, then wave 3. First id first. Passed sequences are never redrawn.
4. Per sequence: read the plan, write the storyboard rows, render all N frames, run `python3 codex/check_anim.py --fix --video NNN`, fix only what it reports, append one line to `anim/PROGRESS.md`.
5. After every 10 videos of a wave print `WAVE W VIDEOS a-b DONE` with a 3-line report. Continue without waiting.
6. If image quota ends, continue with code-rendered art. If time or session ends, stop cleanly after the current sequence; the next session restarts at step 3 and loses nothing.

## Hard rules (short version)
- Folder `anim/NNN/sKK/` holds exactly `f0001.png ... fNNNN.png` (N from the plan). No other files there.
- 24 distinct drawings per second. Moving micro-motion on every frame (at least 3 px or 1.5 percent change). Never duplicate a frame.
- Keep the top 12 percent and bottom 18 percent free of important action and text. No subtitles, watermarks or logos.
- Main figure 40 to 60 percent of frame height, three depth layers, secondary motion, no text over props.
- On-screen text only from the plan's Allowed text, the narration, or the HOOK and PROVOC question you write from narration facts. No invented quotes, no new facts, no betting content, no real crests or photos.
- Do not edit `flip/`, `scripts/`, `deliver/`, `FINAL_100/`, `clips/` or any existing `.py` file. New files go under `anim/` only. Do not ask me questions unless a plan file is missing.

## When the work ends
Run `python3 codex/check_anim.py`. At `761/761 sequences pass (32646/32646 frames)` reply `ALL ANIMATION DONE` with the redrawn-frame count, changed beats, refusals and substitutes, and the sequences where code rendering replaced image generation. Otherwise reply with the count and the first 10 failing ids, and stop.
