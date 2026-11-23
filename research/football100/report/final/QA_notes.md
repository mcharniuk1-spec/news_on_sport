# Cross-corpus QA notes (104 videos, 11 batches)

Corrections file: `final/CORRECTIONS.json` (73 records, 0 validation errors under `taxonomy.validate_record`; also validated after applying all corrections to all 104 records).

## What was checked
1. Table of all merged records printed and reviewed (hook_type, hook_basis, topic, structure, humour, virality, hook_strength, agreement).
2. (a) Taxonomy drift: batch-by-batch counts of hook_type, story_structure, cta_opener_type, risk flags, timeliness.
3. (b) Score drift: per-batch means and a regression of virality_pred on the seven sub-scores.
4. (c) hook_type against the first sentence of every ctx file (all 104 hook_text strings read).
5. (d) risk_flags against features.json (single_source, over_length, comic/betting, overlap, footage).
6. (e) generic or inconsistent `changes` (priority drift, repeated generic CTA actions).
7. End-to-end spot checks (ctx + record read in full): 3, 5, 7, 9, 10, 11, 12, 13, 19, 20, 23, 29, 32, 36, 41, 44, 45, 46, 59, 67, 74, 76, 77, 87, 88, 89, 93, 95, 904 (29 records).

## Findings and corrections

### Taxonomy drift (corrected)
- **timeliness (16 records).** Batches 8 and 9 labelled news dated 2026-11-01..11-12 as `breaking_week`. Batches 4, 5, 6, 7, 10 used `recent_month` for everything up to 11-12 and `breaking_week` from 11-13. Set to `recent_month` for 71-83, 51, 84, 85 (all news_date <= 2026-11-12). No correction possible for bo/split items (no news_date).
- **cta_opener_type (4 records: 3, 9, 22, 27).** The opener "Want the next story before it breaks?" was `tease_next` in batches 1 and 3 but `question` in the other 21 videos that use it. Set to `question`.
- **hook_type (7).** "Kaka cried ... Nobody blamed the onions." (event, then jab) was `news_flash`; video 11 ("Argentina have offered Messi a staff job. Presumably with a clipboard.") uses the same pattern and is `roast_jab`. Set 7 to `roast_jab` (alt `news_flash`).

### risk_flags (corrected)
- **overlap_other_video missing** on 9 and 10 (both use the six-months-at-Al-Hilal beat, 10's own changes say so), 12 (Ballon d'Or fifth beat overlaps 19), and 41, 44, 46 (three Palace/Sage/Frank stories, each lists the others in merge_or_drop). Added. 9 also got the reciprocal merge_or_drop change.
- **betting_under18_appeal inconsistent (12 records).** Flagged in 29 of 41 comic videos with a betting CTA, silently skipped in batches 3, 7, 10. Applied the definition literally (comic == true and CTA contains "betting"): added to 21, 22, 23, 24, 25, 27, 61, 93, 96, 97, 99, 100. The 8 comic videos whose CTA says "free tips/results" rather than "betting" (5 flagged, 3 not) were left as annotated (judgement call).
- **off_topic_footage_risk** added to 48 and 76 (their own footage_match changes say footage may not match).
- **unverified_claim** added to 95 (same "reported 75m" fee as 93, which carries it).
- **over_length**: all 10 flagged records have flag_over_char_limit true and no record with the code flag is missing it. No change.
- **single_source**: all 57 news items with news_n_domains == 1 are flagged (consistent). 36 (2 sources, 2 domains) is flagged for a claim that rests on Goal only; n_sources is small so it does not contradict the rule. Kept. For bo/split items the flag is claim-specific and cannot be checked against features (no domain counts); batch 1 has no URLs in facts_used so it cannot be audited.
- Not changed but doubtful: `sensitive_topic` on 87 (FIFA politics) and 89 (children photo) stretches the definition (health, family, legal, war, race, doping, injury). Only two records carry it.

### Changes (corrected)
- **vary_cta priority drift.** Same issue (repeated CTA opener) was P1 in 8 records, P2 in 50, P3 in 29, depending on batch. Normalised to P2 for all videos whose opener repeats >= 20 times (27 records). 89 (children plus betting CTA, opener unique) is a different issue and stays P1.
- **Generic vary_cta text.** 23 records had actions like "Rotate the CTA opener used in 32 videos". Replaced with the quoted opener, its true repeat count and "with a line tied to this story". 45 (opener used in 25 videos) had no vary_cta item; added.
- **hook_rewrite priority drift.** P1 was given to hooks scored 3.0-4.0 (batch 7 gave P1 to 6 of 6) while a hook scored 2.0 got P2 (15) and a 2.5 hook got P2 (77). Rule applied: P1 only when hook_strength <= 2.5. Downgraded to P2: 19, 36, 38, 46, 53, 61, 62, 64, 66, 83. Upgraded to P1: 15, 77.
- **88.** Removed an `improve_humour` item that was really a CTA/tone note (duplicates its vary_cta item).

### Score drift (no correction)
- Batch means of hook_strength range 3.25-3.80 (overall 3.54), virality_pred 4.40-6.10 (overall 5.22). Spread is inside sampling noise for n=10.
- virality_pred is well explained by the sub-scores (R2 0.93; shareability weight 1.15, hook_strength 0.42). Mean residual per batch is within +-0.3 except batch 11 (+0.98, n=4). No content-free batch shift; left unchanged. Batches 1-3 are lower on virality because they are bo (Ballon d'Or retrospective) pieces with low UK fit, which is a content reason.

### hook_type vs first sentence (no further correction)
All other hook_type labels match the first sentence. Borderline, left as annotated: 13 (question-with-answer, `question`) vs 21, 22, 25, 27, 30 (rhetorical question-form claims labelled by their content); 45, 48, 95 (`news_flash`/fee or count inside a plain announcement, alt `stat_shock`).

### Not corrected, flag for the next annotation round
- `verify_fact` priority is not tied to any rule (P2 on unverified_claim records in batch 7, P1 on records without that flag elsewhere). Needs a rule before the next batch.
- `merge_or_drop` is used for "low UK appeal, swap the story" in 5, 48, 90, which is not what the category means (overlap). Consider a separate category.
- `risk_flags` agreement between annotator pairs is the weakest field (0.0-0.4 in most batches): treat the flags as indicative; the code-checkable ones (over_length, single_source for news, overlap, betting) are now consistent.
- twist_position (agreement 0.4-0.5) and hook_type_alt (0.4-0.6) are noisy; avoid analysis on them.
- Video 89 facts_used repeats one fact four times (upstream context bug, not a label issue).
