# Codex task: six 2-second cartoon flipbook inserts (real footballers, funny caricatures)

**Paste everything below the line into Codex.**

---

Work in `<PROJECT_ROOT>/research/video_build/gfx/flip2/`. Make six short frame-by-frame cartoon animations, each exactly **30 drawings** (15 drawings per second, 2.0 s), for two football Shorts. They are comic inserts that must feel like fast hand-drawn motion, not slideshows.

## Who is in them (real people, as caricatures)
Reference stills are in `refs/`. Study them and draw a recognisable but clearly **cartoon caricature** of each person. Never photorealistic. Friendly, flattering, funny, no body-shaming, no mockery of health, injuries, family, doping, politics or war.
- **Ronaldinho**: `refs/ronaldinho_smile_young.png` (big toothy smile, dark wavy hair, headband), `refs/ronaldinho_2002_run.png`, `refs/ronaldinho_2026_ravenna.png` (age 46: headband, short stubble, white shirt), `refs/ronaldinho_back_10.png`.
- **Mudryk (Mykhailo Mudryk)**: `refs/mudryk_2026_gordon.png` and `refs/mudryk_2026_gordon_b.png` (current look: blond slicked-back hair, short beard, small earring), `refs/mudryk_2026_spurs.png`, `refs/mudryk_2022_a.png`, `refs/mudryk_2022_b.png` (2022: lighter swept hair, clean-shaven).
Kits are generic: plain shirts, no club crests, no sponsor logos, no brand names, no readable text. The only readable characters allowed are numerals where stated.

## Style
Bold comic/sticker cartoon, thick black outlines, flat saturated colours, simple cel shading, strong squash-and-stretch, smear frames on fast moves, speed lines, funny and loud. Vertical **1080x1920**. Keep rows 1300-1700 mostly empty (captions go there). Use the same look as your previous flipbook (cake, slippers, grandad): same line weight, same shapes.

## Method (this worked last time, do it again)
1. For each scene draw an opaque background plate `bg_<ID>.png` (no subject) and a character/prop reference sheet `ref_<ID>.png`.
2. Draw the subject frames as **transparent RGBA PNG, 1080x1920**, named `<ID>_001.png` ... `<ID>_030.png`, in folder `gfx/flip2/<ID>/`. Same canvas every frame, same coordinate system, only the moving parts change. Do not redraw the background in subject frames.
3. Work in batches of 6 frames, editing the previous frame. After each scene, make `contact_<ID>.png` (all 30 frames in a grid) and fix any frame where size, colours or line weight jump.
4. If transparency is impossible, draw on flat pure magenta #FF00FF and tell me.
5. Make the last frame calm enough to cut away from; make the first frame an anticipation pose. Each scene must read well in 2 seconds.

## Scenes
Frames are numbered 1-30 (15 per second).

### R1 "Twenty-three" (Ronaldinho aged 13)
Plate: small bright street pitch, one goal, warm sunset sunburst. Subject: tiny cartoon boy Ronaldinho (big smile, no headband) and a generic goalkeeper in the goal.
- 1-4: boy bounces a ball, anticipation, grin to camera.
- 5-24: he fires balls one after another, rapid-fire (a new ball every 2 frames, each leaving a streak); balls pile up in the net, the goalkeeper gets buried to the eyes in balls.
- 25-30: the last ball drops, boy takes a bow, goalkeeper's hand pops out of the balls with a tiny thumbs-up.

### R2 "The curl" (Ronaldinho adult, 2002 style)
Plate: dusk stadium with blurred crowd, penalty-area lines, one goal. Subject: adult cartoon Ronaldinho (headband, long dark hair, generic blue shirt with the number 11), a wall of three generic defenders, a generic keeper.
- 1-6: run-up, stand over the ball, smear on the kick (frame 6).
- 7-24: ball curls around the wall in an exaggerated spiral with a glowing trail, keeper dives the wrong way in slow stretch.
- 25-30: net ripples, ball spins in the top corner, Ronaldinho does a calm shrug.

### R3 "No more excuses" (Ronaldinho aged 46 and a Sunday-league uncle)
Plate: scruffy park pitch at 10 am, mist, one tree. Subject: a generic cartoon uncle with a round belly, shin pads over his socks, holding a long paper scroll of excuses; Ronaldinho aged 46 in a white shirt and headband.
- 1-8: uncle unrolls the excuse scroll, it hits the floor and keeps rolling.
- 9-20: Ronaldinho enters juggling a ball with feet, knee, head, shoulders, effortless, ball never drops.
- 21-30: Ronaldinho taps the ball onto the uncle's belly, uncle looks at the scroll, tears it up sheepishly, shrugs, both smile.

### M1 "Speed" (Mudryk)
Plate: long straight athletics track, bright blue sky, speed-line sunburst. Subject: cartoon Mudryk (blond slicked-back hair, short beard) in a plain orange training top, a tiny referee, a snail, a pigeon, a round speedometer dial.
- 1-5: crouched start, anticipation, hair perfectly still.
- 6-22: explosive sprint, long smears, dust clouds, he overtakes the pigeon and the snail, the referee spins in his wind, the dial needle swings round.
- 23-30: sudden stop, hair still perfect, dial shows **37.4** (numerals allowed only here), he blows on his fingernails, cool.

### M2 "Before tax" (Mudryk)
Plate: tidy office, desk, wooden panel wall, warm lamp. Subject: cartoon Mudryk in a white shirt, a giant paper payslip, a pile of gold coins with a pound sign, a very tall generic cartoon tax inspector in a bowler hat holding an open briefcase.
- 1-6: Mudryk happily opens the payslip, a big pile of gold coins appears.
- 7-22: coins fly in streams from the pile into the briefcase, the taxman grins and grows, Mudryk's eyes get wider, the pile shrinks.
- 23-30: only three tiny coins are left, Mudryk holds one up between finger and thumb, raises an eyebrow, the taxman tips his hat.

### M3 "Dump truck" (Mudryk)
Plate: building site with sand piles, big sky. Subject: cartoon Mudryk (orange training top, arms crossed), a big yellow dump truck backing in, grey boulders.
- 1-6: Mudryk stands cool, truck reverses in with beeping smear.
- 7-20: truck tips, boulders slowly pour onto him, the pile reaches his shoulders, he does not flinch, one eyebrow goes up.
- 21-30: he bursts out of the pile in a super-fast sprint, boulders fly, truck driver covers his eyes.

## Deliverables
`bg_<ID>.png`, `ref_<ID>.png`, `contact_<ID>.png`, `<ID>/<ID>_001.png ... _030.png` for IDs R1, R2, R3, M1, M2, M3 (180 frames + 18 plates, reference sheets and contact sheets). When done, list every file written and tell me which scenes (if any) are not transparent.
