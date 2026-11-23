# Voice (ElevenLabs, one run) and music plan

## 1. Voice: one single generation
Goal: one intense, emotional British male voice (free library voice), one take for the whole script, then I cut it into lines by silence detection and place each line on the beats.

Settings to ask for when the connector is available:
- Model: `eleven_v3` if the free plan allows it (supports audio tags). Otherwise `eleven_multilingual_v2` with the plain text.
- Voice: pick from the free library after a `search voices` call. Wanted: British, male, energetic, slightly cheeky "football pundit" tone. No real person's voice and no cloning.
- Stability low (about 0.3) for more emotion, style high, speaker boost on.
- Output: `mp3_44100_128`, saved to `audio/el_take1.mp3`.

Text version for `eleven_v3` (tags are directions, not spoken):
```text
[excited] Ronaldinho. Forty-six years old! [pause] Eleven years. No pro football. [laughs] Everyone said: it's a joke. [serious] Third division. White shirt. [shouting] Flares! Smoke! Chaos! [dramatic] Brutal league. [calm] Ravenna two. Forlì nil. [proud] Retired? Never. [playful] Who's next? Your grandad?
```
Plain version (v2 / no tags):
```text
Ronaldinho. Forty-six years old! Eleven years. No pro football. Everyone said: it's a joke. Third division. White shirt. Flares! Smoke! Chaos! Brutal league. Ravenna two. Forlì nil. Retired? Never. Who's next? Your grandad?
```
About 230 characters, roughly 230 credits of the 10,000 monthly free credits (about 10 minutes of audio). One run is enough; I will not regenerate unless you ask.

Licence note (third-party sources, not the official terms page): the Free plan is reported as non-commercial with attribution ("elevenlabs.io" in the title). The cheapest paid plan (about $6 a month, reported) adds a commercial licence. Check the official terms before publishing.

## 2. Music: what is realistic
- Viral TikTok/Reels hit songs are commercial releases. They are not in the free libraries, and I cannot download them.
- **Meta Sound Collection**: free, but reported as licensed only for use inside Meta products (Facebook, Instagram). Not for YouTube Shorts or TikTok. Needs a login, manual download.
- **TikTok Commercial Music Library**: free for business accounts, scope of use outside TikTok not confirmed. Needs a login, manual download.
- **YouTube Audio Library**: free, "use allowed" is shown per track; safest for YouTube Shorts.
- **Best "viral" route**: export the video with voice and effects only, and add the trending sound inside TikTok or Instagram when uploading. That is how football edits get the trending sound and avoids licence trouble.

Track brief for a free-library pick (I will shortlist from what you download):
| Need | Spec |
|---|---|
| Length | 18.6 s video; a track with a drop or hard hit at 0 s and a strong end |
| Tempo | 130-150 BPM (football edits, phonk or trap, aggressive but not too dark) |
| Mood | cocky, comic, high energy; room for voice (no vocals) |
| Structure | build 0-11 s, drop at the score card (11.8 s), outro hit at 16.6 s |

When a track is chosen I run `detect_beats` in Palmier and move the cuts to the beat grid.

## 3. Timing map to place voice lines (current cut grid)
| Line | Start (s) |
|---|---|
| Ronaldinho. Forty-six years old | 0.1 |
| Eleven years. No pro football | 1.7 |
| It's a joke | 3.45 |
| Third division. White shirt | 4.7 |
| Flares! Smoke! Chaos! | 7.5 |
| Brutal league | 9.2 |
| Ravenna two. Forlì nil | 11.8 |
| Retired? Never | 15.3 |
| Who's next? Your grandad? | 16.7 |
