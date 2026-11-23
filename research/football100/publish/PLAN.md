# YouTube publishing plan (channel "About Football")

## Status
- Test batch: 9 Shorts (001-009) are public on the channel, published through YouTube Studio in a signed-in Chrome session (see `published.json`, `published.md`). All 9 have the new provocative caps title and the long human-style description; descriptions were verified in the Content list.
- Video 010: the upload was refused with "Daily upload limit reached" (unverified channel). Retry after 24 hours or after phone verification.
- Remaining 91 (010-100): final copy is ready in `metadata_v2/NNN.json` (and merged into `youtube_metadata.json/csv`); not published. Start only on the owner's go-ahead.

## What works / what does not
| Route | Result |
|---|---|
| YouTube Studio in Chrome (signed-in profile) + file-input upload | Works. Upload, title, description, "not made for kids", Public, Publish all verified on the test batch |
| YouTube Data API v3 with the API key in `utube.yml` | Key is rejected by the API ("API key not valid"). Even a valid API key cannot upload: `videos.insert` needs OAuth 2.0 (scope `youtube.upload`) |
| Automation for the rest | Needs an OAuth client (Desktop app type) in a Google Cloud project with YouTube Data API v3 enabled; one-time consent for the channel; then `publish/upload_api.py` (to write) uploads from `FINAL_100_v2/videos` at full quality |

## Constraints to plan for
- Browser upload tool limit: 10 MB per file, so Studio uploads use re-encoded copies (`make_upload_copies.sh`, ~1.4 Mbps). Full-quality masters are in `FINAL_100_v2/videos` (1.8 GB); the OAuth/API route uploads those instead.
- New / unverified channels have a daily upload cap (roughly 10-15 per day) and links in descriptions are not clickable until phone verification. Plan ~10 per day: 9 days for the remaining 90, or verify the channel first.
- Quota (API route): `videos.insert` costs 1,600 units; the default 10,000 units/day allows 6 uploads/day unless a quota extension is granted.
- Rights: the videos use third-party match footage. Review claims after upload (Studio > Content > Restrictions); consider a rights check before bulk publishing.
- Synthetic voice: narration is generated (Kokoro / ElevenLabs). Cartoon visuals, no real-person likeness; "altered content" disclosure set to No.

## Lessons from the test batch
- Typing the description inside the upload wizard right after the upload often did not persist (the video went public with "Add description"). Reliable: publish, then open `studio.youtube.com/video/<ID>/edit`, replace the title/description and press Save; or fill the description in a saved draft ("Edit draft") once checks are complete.
- Publish is disabled while the wizard shows "Saving..."; wait ~5 s on the Visibility step before pressing Publish.
- The wizard hits the daily limit after 9 uploads on this unverified channel.

## Per-video procedure (Studio, ~3 browser calls)
1. Open `https://studio.youtube.com/channel/<CHANNEL_ID>/videos/upload?d=ud`.
2. Upload `publish/upload/NNN.mp4` to the hidden file input.
3. Title and description from `youtube_metadata.json`; Audience: "No, it's not Made for Kids"; Next x3; Visibility: Public; Publish.
4. Record the Shorts URL in `published.json`.

## Schedule suggestion
Day 1: 011-020, day 2: 021-030, ... day 9: 091-100 (or all at once via API after verification and quota extension). Optional: schedule publication times (18:00 UK) in the Visibility step.
