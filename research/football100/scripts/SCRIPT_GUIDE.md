# Script guide for the football-100 Shorts (English, UK audience)

Data: `cd <PROJECT_ROOT>/research/football100`, then `python3 fdb.py get news <id>` (a news event) or `python3 fdb.py get bo "<Name>"` (a Ballon d'Or winner pack). Plan: `scripts/assign.json` (find your `no`). Use ONLY facts found in that data. Never invent a number, quote, date or name. Do not read other large files.

## What the video is
A 30-40 s vertical Short (some 45-60 s) that tells a news story about the footballer or club: what happened lately, why it matters, the twist. Voice-over by one narrator. It is NOT about the website; the website appears only in the last line.

## Shape (state -> question -> action -> changed state)
1. HOOK (<= 12 words): a question, a number or a provocation. No "Hello", no "Today".
2. WHY YOU CARE (1 sentence).
3. 2-4 BEATS: one fact per sentence, one cognitive job per beat. Each beat ends on a small joke or a sharp turn.
4. TWIST / PAYOFF: the funniest or most surprising fact, last before the CTA.
5. CTA (fixed, last line, 10-16 words). Rotate the wording, always say "aboutfootball dot UK" (spoken) and offer betting tips, match news and predictions. Examples:
   - "Want the next story before it breaks? Betting tips, news and predictions at aboutfootball dot UK."
   - "Think you can call the next one? Free tips, results and predictions at aboutfootball dot UK."
   - "Your mates will never guess this. Match news and betting tips at aboutfootball dot UK."
   Never promise wins or guaranteed profit.

## Voice and humour
- Simple, clear English. Short sentences (<= 14 words). No heavy local slang. Spoken style, contractions are fine.
- Think stand-up comedian with football knowledge: specific, observational, friendly roast. Tease the past or the present of the star (hair, celebrations, transfers, trophy droughts, social media, odd stats). Also praise with a real number. Be admiring AND cheeky.
- Jokes must rest on documented facts. Do not exaggerate claims about real people.
- FORBIDDEN as joke material: doping, health, injuries, war, family, legal troubles, anything marked sensitive:true, nationality or race. Report those facts only if neutral and needed.
- One or two sound-effect cues are fine as a field (not spoken).

## Length (hard limits)
- Voice characters (all spoken lines together, including the CTA): ElevenLabs videos <= 600 characters (about 33 s). Kokoro videos: aim 520-720 characters; at most 1100.
- Numbers in speech: write them as words where natural ("twenty-three"), keep scores like "two-nil".

## Output: write `scripts/NN.json` (NN = zero-padded `no`), valid JSON
```
{"no":N,"subject":"...","title":"<= 60 chars, on-screen title","voice":"kokoro|EL_A|EL_B|EL_C",
 "comic":true|false,"style":"<from assign.json or null>",
 "lines":[{"vo":"spoken sentence(s)","card":"<= 4 words on-screen keyword or null","sfx":"optional cue","footage":"what to show: clean match/press clip idea"}],
 "chars":N,"est_seconds":N,
 "footage_terms":["3-5 YouTube search phrases for clean footage"],
 "inserts":[{"after_line":i,"story":"setup -> gag -> twist in 1-2 sentences","characters":"who, caricature","seconds":2}],
 "facts_used":["fact text + id/url"],"comic_score":1-10,"notes":"risks, unverified bits"}
```
- Non-comic videos: 0-1 inserts. Comic videos (comic:true): exactly 3 inserts, each a small STORY (setup, gag, unexpected twist) in the given style, using generic stylised characters and caricatures of the real footballers (never real-person photos, never named franchise characters, no logos).
- The last line must be the CTA. `chars` = total length of all `vo` strings.
