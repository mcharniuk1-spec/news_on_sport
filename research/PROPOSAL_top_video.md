# Proposal: the Short most likely to win, based on the 220-video sample

## What the data says (sample: 110 Shorts, 110 long; see `REPORT_frame_by_frame.md`)

| Finding | Evidence |
|---|---|
| Single-name news hooks beat generic skills. | FutVibes (2.03M subs) posts news-as-headline Shorts: avg 1.31M views, like rate 2.13%, **14–28 cuts per 30 s**. "Portugal got destroyed 4-0 in their first game without Ronaldo" 1.47M; "Bernardo Silva banned from Portugal after supporting Ronaldo" 1.29M. |
| Format is stable and cheap. | 30–33 s. Bold white italic caps, black outline, **one word per beat**, centred. Stills, tweet/post screenshot cards, stat cards, split-screen meme. Little true motion video. |
| A cheap "NOW vs THEN" static format also scales. | Gau3am: 5 of 10 top Shorts, avg 2.49M, ~21 s, cut-out stills on white background, skull emoji, crossfades. |
| Controversy compilations with a live scoreboard bug do the best volume. | Nost FC avg 3.95M; "Most CONTROVERSIAL Matches" 48–59 s. But nearly all of it is broadcast footage (rights risk high). |
| The month's dominant subject is Lamine Yamal and the Ballon d'Or. | Trending Shorts (avg 47M, driven by one 308M outlier) are nearly all Yamal. The 4 AI-generated videos average 14.3M (n=4, too few to trust). |
| Confirmed news this month (multiple outlets). | Ballon d'Or 26 Oct, won by Harry Kane. Yamal won the Kopa Trophy (one source). El Clásico 25 Oct, Real Madrid 2-1, Mbappé scored twice. Ronaldo announced retirement from Portugal on 5 Nov after a public dispute with coach Jorge Jesus. |

## Recommended Short

**Topic:** Ronaldo quits Portugal after the Jorge Jesus feud, told as a 30-second "who really wins" story.
**Why this one:** it combines a person, a feud, a fixed date, and a built-in follow-up (the No. 7 shirt). FutVibes Ronaldo/Portugal stories already sit at 1.3–1.5M. It is confirmed news, not a rumour.
**Format:** 9:16, 30 s, 15 frames at 2 s, one-word-per-beat captions, 14–16 cuts.
**Must verify before publishing:** exact wording of the retirement statement, the No. 7 handover timing, and any detail of the Jesus dispute. Sources called the dispute "reported". Write "reportedly" in captions. Do not invent quotes.

### Full voice-over (about 80 words, ~30 s)

> Cristiano Ronaldo just retired from Portugal. Not a quiet goodbye. It followed a public fight with his own coach, Jorge Jesus. Reports say he had a retirement letter ready after the World Cup. The federation president talked him out of it. Not anymore. 234 caps. 146 goals. Six World Cups. He keeps playing for his club, but the Portugal No. 7 shirt is now up for grabs. So who wears it next? Comment your pick. And who was right: Ronaldo or Jesus?

### Frame by frame (each frame = 2 s)

| # | t | Frame type | Visual | Caption (one word per beat) | Transition in | Source / generation |
|---|---|---|---|---|---|---|
| 1 | 0 | Generated still, punch-in | Empty Portugal dressing room, red shirt with a big **7** on a hook, single spotlight | RONALDO / RETIRED | Hard cut, zoom-in 1.0→1.15 | AI image, no real face |
| 2 | 2 | Generated still | Stylised silhouette of a player walking out through a tunnel, stadium light ahead | NOT A QUIET GOODBYE | Whip pan | AI image |
| 3 | 4 | Real-footage card (screenshot of official post, blurred name optional) | Social post card, black box, white text: "Announcement, 5 Nov" | 5 NOV | Pop-in card | Own graphic; check text against the real post |
| 4 | 6 | Generated still | Two stylised figures facing off across a touchline, no identifiable face; Jesus tagged by caption only | FIGHT / WITH HIS COACH | Hard cut | AI image |
| 5 | 8 | Graphic card | Name tag "JORGE JESUS · Portugal coach" over flat colour | JORGE JESUS | Flash cut | Own graphic |
| 6 | 10 | Generated still + stamp | Hand writing on paper, letter stamped "READY" (no readable real text) | A LETTER / WAS READY | Zoom out | AI image |
| 7 | 12 | Generated still | Man in suit stopping a player at a door, back view | THE PRESIDENT / STOPPED HIM | Hard cut | AI image |
| 8 | 14 | Graphic stat card | "NOT ANYMORE" large, red flash | NOT ANYMORE | Flash, 3-frame shake | Own graphic |
| 9 | 16 | Stat card | **234** caps, count-up animation | 234 CAPS | Pop-in | Own graphic |
| 10 | 18 | Stat card | **146** goals, count-up | 146 GOALS | Pop-in | Own graphic |
| 11 | 20 | Stat card | **6** World Cups, six small trophy icons | 6 WORLD CUPS | Pop-in | Own graphic |
| 12 | 22 | Generated still | Pitch at night, club-colour scarf, stylised player | STILL PLAYING / FOR HIS CLUB | Crossfade | AI image |
| 13 | 24 | Generated still | Red No. 7 shirt on empty hanger, spotlight | NO. 7 / UP FOR GRABS | Zoom-in | AI image (matches frame 1 for a loop) |
| 14 | 26 | Split-screen graphic | Left: question mark in a 7. Right: comment-bubble icon | WHO WEARS IT? | Split wipe | Own graphic |
| 15 | 28 | End card | "Ronaldo or Jesus? Comment" with like/comment icons | COMMENT / YOUR PICK | Hold last 2 s | Own graphic |

### Production notes

- **Likeness and rights:** the plan uses generated or abstract images and own graphics. Do not generate photoreal fake photos of real people presented as real. Label AI art ("AI illustration") in the description. Do not put invented quotes in anyone's mouth. Where a real person is named, the caption must stay on reported facts.
- **Reusing existing clips:** of 293 reuse segments flagged in the sample, 212 are high rights risk (broadcast footage), 63 medium, 18 low. Muting and stripping subtitles does not remove the footage copyright. Use licensed or own-recorded material, or the generated frames above.
- **Look to match FutVibes:** bold white italic caps with black outline, centred, one word per beat, stat and post cards, 14–16 cuts per 30 s.
- **Tools (per project CLAUDE.md):** generation via fal.ai (billing was exhausted at last check, confirm first) or a licensed alternative; assembly and captions via CapCut/Palmier or HyperFrames/Remotion for the stat-card animations; FFmpeg for QC. None of these was exercised in this run.
- **Test plan:** publish 3 variants (hook "RONALDO RETIRED", "RONALDO VS JESUS", "WHO WEARS NO. 7") and compare 2-hour views and like rate.
