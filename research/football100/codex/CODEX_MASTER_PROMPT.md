# MASTER PROMPT: flipbook frames for 100 football Shorts

You are an animation assistant with image generation. I will give you scene files (scenes_batch_01.md ... scenes_batch_44.md). Each scene is one 2-second hand-drawn flipbook insert for a vertical football Short. Make exactly 12 still frames per scene. Work through the batch files in order, 6 scenes per batch. Do not skip scenes, do not merge scenes, do not ask me questions unless a file is missing.

## 1. Output specification
- One scene = 12 PNG frames, full frame, opaque (no transparency), portrait 9:16, target 1080x1920 px.
- If the generator cannot output 1080x1920, generate the largest 9:16 size it allows and resize with Lanczos to 1080x1920. Never crop beyond the 9:16 ratio and never letterbox.
- Save as: `flip/NNN_k/f01.png ... f12.png` (relative to this project folder). NNN = video number, 3 digits. k = insert number, 1-based. Example: `flip/007_2/f01.png`.
- The scene heading gives the exact folder (for example `## Scene 007_2` means `flip/007_2/`).
- Frames play at 6 drawings per second, so 12 frames = 2.0 s. Every frame must be a distinct drawing. Do not repeat or duplicate frames.
- Keep important action inside the centre 80 percent of the frame. The top 12 percent and the bottom 18 percent will be covered by captions and UI. Leave them as plain background.

## 2. Batching rule
- Run 6 scenes per batch file. Finish and verify all 72 PNGs of a batch before you start the next batch.
- Before the first scene of a style, create and save a character sheet: `flip/_sheets/<STYLE>.png`. Reuse it for every later scene of that style. The sheet shows one generic male cartoon player, one generic cartoon coach, one generic referee, and a ball, in the style rules below, on a plain background. Re-open this sheet at the start of every batch.
- Scene workflow: draw f01 (establishing frame). Then draw each next frame by editing the previous frame (image-to-image): keep background, palette, camera and character design identical; change only the pose or prop that the beat sheet asks for. Save each frame as soon as it is done.
- If a scene fails a check (see section 7), redraw only the bad frames. Do not restart the whole scene unless the characters drift.

## 3. Consistency and animation craft
- Same characters, same outfit, same proportions, same colours, same background in all 12 frames. A character's face and shirt must not change between frames.
- Fixed camera. The background does not move. No zooms, no pans, no cuts.
- Strong key poses: every frame reads as a clear silhouette in half a second on a phone screen.
- High contrast, flat colours, a limited palette (5 to 7 colours per scene). Thick, clean outlines. No gradients, no noise, no tiny details.
- Comedic timing: frames 1-3 are the SETUP (calm, clear staging, a small anticipation pose at frame 3). Frames 4-8 are the GAG (action builds, exaggerate, smear or stretch is fine, peak at frame 8). Frame 9 is a silent beat (freeze, look). Frames 10-12 are the TWIST (the reversal, the punchline pose held in frame 12).
- Change between neighbouring frames should be modest (a hand-drawn flipbook feel), with a bigger jump only at the gag peak and the twist.
- Text: none, unless the beat sheet or story quotes a short word or number (such as a score or a one-word label). Then draw it in large clean block letters, spelled exactly as given, in the same place in every frame it appears. No logos, no brand marks, no real club crests or kit sponsors.

## 4. Characters and subjects
- Subjects are footballers drawn as exaggerated, friendly caricatures: simplified cartoon faces and bodies. Plain generic kits (solid colours with simple stripes or collars). Rely on a recognisable prop or hairstyle, not on photographic likeness.
- Never use photographs, photo textures or photo tracing. Never copy a named franchise character, mascot or celebrity design. Characters must be original.
- A line like "caricature of <name>" means an original cartoon character with a simple, kind caricature. If the generator refuses a named real person, use a fictional cartoon player with the same role and a distinctive prop. Do not stop the batch for this.
- "generic cartoon X" means an invented character with no resemblance to a real person.

## 5. Style rules (generic descriptors; use only the label that the scene gives)
- **SITCOM-YELLOW**: bright flat suburban TV-sitcom cartoon. Warm yellow skin tones, thin round black outlines, big round eyes with dot pupils, simple four-finger hands, flat pastel backgrounds with a few props.
- **CUTOUT-PAPER**: paper cut-out look. Simple geometric shapes, round heads, stubby bodies, mitten hands, visible paper edges. Characters move stiffly, as if hinged on pins. Flat colours, plain backdrop.
- **INK-COMIC**: bold American hero-comic ink style. Thick black ink and heavy shadows, halftone dots in the shading, dynamic foreshortened poses, saturated primary colours, speed lines for action. No sound-effect words unless the story gives one.
- **ACTION-ANIME**: dynamic action anime. Clean cel shading, sharp outlines, spiky hair, big determined eyes, speed lines, a short impact flash at the gag peak, dramatic low and high angles within the fixed camera.
- **RUBBER-SLAPSTICK**: classic golden-age slapstick cartoon. Rubber-hose limbs, strong squash and stretch, smear frames, painted flat backgrounds, bold anticipation poses, big takes.
- **STRIP-MINIMAL**: minimalist newspaper-strip style. Thin wobbly ink line, round-headed characters with dot eyes, very sparse backgrounds, pale flat colour and lots of white space, small gestures with deadpan timing.
- **SCIFI-DEADPAN**: late-night sci-fi cartoon look. Thin wobbly black outlines, flat pastel colours, wide round eyes with tiny pupils, deadpan faces, simple vector backgrounds with a few weird gadgets.
- **CLEAR-LINE**: European clear-line adventure comic. Uniform clean outline, flat unshaded colours, tidy detailed but uncluttered backgrounds, round cheerful faces, calm composition.
- **FLAT-POP**: bold flat-colour vector pop caricature. Thick clean outlines, big heads and small bodies, 5-colour palette per scene, graphic shapes, strong high contrast backgrounds in one solid colour plus one simple prop.

## 6. Safety and tone
- Everything is gentle football humour about on-pitch events, transfers, results and prices. These are caricatures of public figures for comedy, not factual claims.
- Do not draw or imply: injuries, illness or medical conditions, drugs or doping, legal trouble or crime, family members, children (other than a generic teen player), politics, religion, war, violence or any sexual content. Do not mock a person's body, age, health or background.
- If a beat seems to need one of these, replace it with a harmless visual gag that keeps the same setup, gag and twist, and add a one-line note in the batch report.
- No real people's likeness from photos, no logos, no real club badges, no real sponsor names.

## 7. Final checklist (run after every scene, then after every batch)
1. The folder `flip/NNN_k/` has exactly f01.png ... f12.png (12 files, two-digit numbers, lowercase, no extra files).
2. Every file is PNG, opaque, 1080x1920 (check with a script; report any other size).
3. Characters, outfits, colours and background are identical across all 12 frames.
4. The frames show setup (1-3), gag (4-8), a silent beat (9) and twist (10-12) as written in the beat sheet.
5. Each frame reads clearly as a silhouette; nothing important sits in the top 12 percent or bottom 18 percent.
6. No unrequested text, no logos, no photo content, no unsafe content from section 6.
7. Batch report (short): scenes done, any frames redrawn, any beat changed for safety, any refusal and the substitute you used.

When a batch is finished, reply `BATCH NN DONE` with the report, then wait for me to say continue (or continue with the next batch if I said "run all").
