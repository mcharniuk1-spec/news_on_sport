# How the 100 video texts were written (rules)

Source: the news database (800 deduplicated stories) + analysis of about 2,000 YouTube videos/Shorts.
Each text is `research/football100/scripts/NNN.json` with `lines[]` = `{vo, card, sfx, footage}`; the last line is always the call to action.

## Format
- 100 Shorts, 30-40 s typical (range 30-80 s), English for a UK audience, 18+.
- Voices: 67 videos on a local Kokoro voice, 33 on ElevenLabs `eleven_flash_v2_5` (3 voices x 11 videos). ElevenLabs scripts stay near 600 characters.
- Every script ends with the CTA containing `aboutfootball dot UK`.
- `card` = a short on-screen headline for the line; `footage` = search terms for the visuals.
- 49 videos get a comic-universe treatment (9 style labels: SITCOM-YELLOW, CUTOUT-PAPER, INK-COMIC, ACTION-ANIME, RUBBER-SLAPSTICK, STRIP-MINIMAL, SCIFI-DEADPAN, CLEAR-LINE, FLAT-POP).

## Writing rules
1. Hook in the first line: a contradiction, a question, or a surprising number from the news; one new fact per beat.
2. Every name, number and date must appear in the news database or a verified source; mark uncertain items "reported, not confirmed".
3. Ballon d'Or winners: what happened lately (last ~90 days), at most 3 sentences of past context; admiring and teasing tone, real numbers.
4. Safe-joke limits: no jokes about doping, health, injuries, war, family, legal troubles, politics, religion or sex. No invented quotes. No betting prompts, odds or bookmakers in the visuals or text.
5. Short sentences, one idea per sentence; no filler; vary the endings so comment bait and CTA do not repeat.
6. Subtitles: at most 5 words per chunk, 2 lines, active word highlighted. Cards appear only when no animated interlude covers the screen.

## Automatic check
`python3 research/football100/check_scripts.py` verifies length limit, CTA, voice assignment, banned topics (regex) and the number of comic inserts.
