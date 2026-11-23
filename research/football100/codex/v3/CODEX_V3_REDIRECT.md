STOP and change direction for everything you have not finished (and redo every poster you already drew). Read this instead of the "plain top and bottom band" and "framed panel" instructions of the older prompt.

What was wrong: the poster looked generic ("STAFF JOB OFFER"), the art did not fill the 9:16 screen (empty blue bands, a framed box in the middle), the name label was covered, and the headline was not the news. Fix all of it.

NEW DIRECTION: each video is a short SEQUENTIAL COMIC STORY, like an episode of a Simpsons-style sitcom. Original yellow-skinned characters with that look (round eyes, overbite, flat colours, thin outline). Not Homer, not any existing character. Simple image generations, one image per story beat, each image full-bleed 1080x1920: the art fills the WHOLE screen, no frame, no empty bands. Text-free zones (top 12 percent, bottom 20 percent) still contain art, only no letters.

STORY ORDER (linear, logical, same characters and place throughout):
1. PRESENT the news: who, what happened. Title 2-7 words.
2. BACKGROUND: how we got here (1-2 images, flashback look, caption EARLIER or a year).
3. REVEAL the twist or punchline fact, with a big funny reaction.
Every image has its own clear title (2-7 words) and one message; each image builds on the previous one. Use the narration in codex/v3/plan/NNN.md as the script. Write story3/NNN/STORY.md first: one line per image (beat, title, message, who is in it, where). Then draw.

CHARACTERS: the real player is a recognisable CARICATURE (exaggerated head, signature hair or beard, kit colour and number, signature prop, NAME label placed where nothing covers it). Plus two original side characters: a hero fan and a reporter. Realistic enough that anyone knows who it is at a glance. No real crests or logos, no franchise characters.

INSERTS IN EVERY VIDEO (separate images):
- a QUESTION card: full-screen bold colour or black, one question of 2-7 words;
- a BLACK-SCREEN beat: black with ONE word (WAIT. / SERIOUSLY? / OOF.), I will hold it 0.4 s;
- an INTERVIEW panel: reporter with a plain microphone and the player caricature, label REPORTER ASKS, speech bubble using ONLY words from the narration, never an invented quote;
- a ONE-SECOND GAG: a visual pun on the story (a prop, a sign, a reaction), as a joke, not an explanation.

TEXT: main 2-7 words per image, huge, outlined, readable on a phone; 2-3 tiny emotion words allowed (HA, OOF, WAIT WHAT). Never over faces.

POSTER = the strongest image of the story (the REVEAL moment). Headline = the news in 2-7 words (example: 985 GOALS. STILL RESTED?). Caricature in the middle, one prop that carries the claim, the fan reacting, full-bleed. The About Football badge (brand/portrait/aboutfootball_corner_badge.png) small at lower left, x=60, bottom edge y=1500, never covering the name label. Test: a stranger says WHO it is about and WHAT the news is within one second.

OUTPUT: story3/NNN/p01.png ... in story order (5-8 images including the inserts), story3/NNN/STORY.md, poster3/NNN.png (1080x1920 opaque PNG). I will animate the images (push-ins, shakes, transitions) and cut them into the video; if a beat needs real motion, add 12-24 consecutive frames of that beat as story3/NNN/mXX/f0001.png... (consecutive edits of the same image). Do NOT build code vector rigs.

ORDER OF WORK across all 90 videos (011-100): wave 0 = STORY.md + poster3 for every video; wave 1 = present images; wave 2 = background images; wave 3 = reveal + inserts. Resume after a break from the first missing file. Keep logging in anim3/PROGRESS.md.
