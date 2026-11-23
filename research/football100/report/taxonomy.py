#!/usr/bin/env python3
"""Single source of truth for the football-100 video classification (taxonomy + record schema + validator).
Run `python3 taxonomy.py` to print the definitions. Import ENUMS / validate_record from other scripts."""
import json, sys

ENUMS = {
 "hook_type": {  # what the FIRST sentence does
  "contrast_twist": "Two opposing facts back to back, X then Y ('Three-nil down at half-time. Three-all at full time.')",
  "stat_shock": "Opens on a number, record, fee or count as the shock ('Forty-three games unbeaten...')",
  "question": "Direct question to the viewer ('How long can a midfielder hesitate...?')",
  "bold_claim": "Surprising or provocative statement or prediction stated as fact ('The champions lost to League Two. Yes, really.')",
  "roast_jab": "Playful jab at a person or club in the very first sentence ('...Presumably with a clipboard.')",
  "curiosity_gap": "Odd or mysterious detail with the payoff withheld ('Milan once bought a striker after watching a VHS tape.')",
  "quote_led": "Opens with someone's words or a reported statement",
  "news_flash": "Plain announcement of what happened, no extra device ('Argentina have offered Messi a job.')",
 },
 "hook_basis": {  # real-world material the hook rests on
  "scoreline_result": "A final score or match outcome",
  "comeback_collapse": "A lead thrown away or a comeback (within one match)",
  "upset": "A weaker side beating a stronger one",
  "transfer_fee_or_bid": "A fee, price or bid figure",
  "transfer_rumour": "A reported interest, link or tracking story without a done deal",
  "contract_or_job": "Appointment, sacking, new contract, job offer",
  "quote_or_interview": "Something a person said",
  "record_or_milestone": "A record, first, or milestone",
  "viral_or_social": "A viral clip, photo, view count or social post",
  "controversy_or_discipline": "Red card, ban, scandal, rule-breaking",
  "prediction_or_pundit": "A forecast or opinion by a pundit or player",
  "career_irony": "Past glory against present/after-effects (Ballon d'Or then flop, etc.)",
  "stats_oddity": "An odd statistic not tied to one result",
 },
 "topic_primary": {  # what the story is about
  "match_report": "Result and key moments of one match",
  "giant_killing": "Upset story, lower side beats bigger side",
  "comeback": "Comeback or collapse story",
  "transfer_story": "Transfer, bid, fee or rumour",
  "manager_news": "Appointment, sacking, touchline or tactics story about a coach",
  "player_form": "A player's current form, minutes or role",
  "record_milestone": "Record, milestone, league-table achievement",
  "discipline_controversy": "Cards, bans, scandals, rule breaches",
  "pundit_prediction": "Opinion or forecast",
  "legacy_retrospective": "Career retrospective of a past Ballon d'Or-type star",
  "viral_moment": "Viral video, photo, social buzz",
  "club_ownership_finance": "Owners, money, club project",
 },
 "scope": {
  "premier_league": "Premier League clubs or players",
  "english_other": "English cups, Championship, League One/Two, England national team",
  "europe_club": "Champions League, Europa League, other European club football",
  "la_liga": "Spanish league clubs",
  "serie_a": "Italian league clubs",
  "other_leagues": "Bundesliga, Ligue 1, MLS, Brazil, etc.",
  "international": "National teams (non-England)",
  "mixed_career": "Spans many clubs, no single competition",
 },
 "subject_type": {"player": "", "manager": "", "club_team": "", "owner_or_other": ""},
 "timeliness": {
  "breaking_week": "News from the last week or so",
  "recent_month": "Recent, within roughly a month",
  "evergreen_retro": "Evergreen or retrospective, not tied to a date",
 },
 "uk_relevance": {"high": "English club/player/UK angle is central", "medium": "Big European name or story with some UK link", "low": "Little UK link"},
 "story_structure": {
  "twist_payoff": "Setup, build, one twist, payoff line, CTA",
  "chronological_recap": "Events told in the order they happened",
  "stat_stack": "Fact, fact, fact, punchline (list-like)",
  "irony_then_vs_now": "Past against present contrast carries the story",
  "question_answer": "Opens with a question and spends the video answering it",
  "roast_and_praise": "Alternating jab and praise beats",
  "rumour_explainer": "Claim, who, why, doubt (rumour handling)",
 },
 "twist_position": {"early": "twist in the first third", "middle": "twist in the middle third", "late": "twist in the last third before the CTA", "none": "no real twist"},
 "payoff_type": {
  "punchline": "A joke line closes the story",
  "shock_stat": "A surprising number closes the story",
  "callback_to_hook": "Last story line returns to the hook idea",
  "open_question": "Ends on an unanswered question or a prompt to think",
  "praise_line": "Admiring close",
  "none": "Flat ending, no payoff",
 },
 "humour_type": {
  "roast": "Direct teasing of a person or club",
  "understatement": "Calm or ironic understatement",
  "sarcasm": "Sarcastic remark",
  "wordplay": "Pun or wordplay",
  "absurd_comparison": "Silly comparison or image",
  "deadpan_stat": "Number delivered as the joke",
  "callback": "Joke that returns to an earlier line",
  "none": "No real humour",
 },
 "humour_target": {"player": "", "club": "", "manager": "", "pundit_media": "", "fans_league": "", "situation": "", "none": ""},
 "dominant_emotion": {
  "awe": "", "schadenfreude": "", "amusement": "", "curiosity": "", "outrage": "", "nostalgia": "", "sympathy": "", "surprise": "",
 },
 "comment_bait": {
  "none": "No reason to comment",
  "direct_question": "Asks the viewer something explicit",
  "hot_take": "Contains an opinion people may argue with",
  "prediction_prompt": "Invites a prediction",
  "fan_rivalry": "Touches a club rivalry that triggers fans",
 },
 "cta_opener_type": {
  "question": "CTA opens with a question to the viewer",
  "mates_social": "CTA uses 'your mates' or other social proof",
  "tease_next": "CTA teases the next story or news",
  "imperative_offer": "Direct offer of tips/news/predictions",
  "other": "Other",
 },
 "risk_flag": {
  "sensitive_topic": "Touches health, family, legal, war, race, doping or injury",
  "unverified_claim": "Rests on an unchecked number, quote or rumour",
  "single_source": "Facts come from only one source",
  "over_length": "Spoken text exceeds the voice-engine character limit shown in the context (41-80 s is allowed by the brief; do not flag length alone)",
  "negative_real_person": "Roast of a named real person that could read as defamation",
  "betting_under18_appeal": "Cartoon or youth appeal combined with the betting CTA",
  "off_topic_footage_risk": "Footage may not match the story",
  "overlap_other_video": "Same story as another video in the set",
  "none": "No flag",
 },
 "change_category": {
  "hook_rewrite": "Rewrite the first sentence",
  "add_comment_bait": "Add a question or hot take that triggers comments",
  "vary_cta": "Change the repeated CTA opener",
  "verify_fact": "Check a number, quote or claim against a primary source",
  "shorten": "Cut length",
  "stronger_twist": "Move or add a twist/payoff",
  "improve_humour": "Sharpen or add a joke",
  "poster_title": "Change the cover headline",
  "poster_hero_art": "Replace the footage frame with drawn hero art",
  "add_second_source": "Find a second source",
  "footage_match": "Fix footage to match the story",
  "merge_or_drop": "Overlaps another video: merge, differentiate or drop",
  "none": "No change",
 },
 "priority": {"P1": "fix before publishing", "P2": "fix in the next batch", "P3": "nice to have"},
}
SCORES_15 = ["hook_strength", "story_clarity", "humour_quality", "shareability", "comment_potential", "uk_fit", "novelty", "poster_title_sells_hook", "poster_joke_quality"]
TEXT = {"hook_type_why": 25, "hook_basis_detail": 30, "story_summary": 30, "poster_issue": 30, "poster_change": 30}
SINGLE_ENUM = ["hook_type", "hook_basis", "topic_primary", "scope", "subject_type", "timeliness", "uk_relevance", "story_structure",
               "twist_position", "payoff_type", "humour_type", "humour_target", "dominant_emotion", "comment_bait", "cta_opener_type"]
FIELDS = ["no"] + SINGLE_ENUM[:1] + ["hook_type_alt", "hook_type_why"] + SINGLE_ENUM[1:2] + ["hook_basis_detail", "story_summary"] + SINGLE_ENUM[2:] + \
         ["humour_intensity"] + SCORES_15 + ["virality_pred", "poster_issue", "poster_change", "risk_flags", "changes"]


def validate_record(r, errs, tag=""):
    def bad(m): errs.append(f"{tag}#{r.get('no')}: {m}")
    for f in FIELDS:
        if f not in r: bad(f"missing {f}")
    for f in SINGLE_ENUM:
        if f in r and r[f] not in ENUMS[f]: bad(f"{f}={r[f]!r} not in enum")
    if r.get("hook_type_alt") not in list(ENUMS["hook_type"]) + ["none"]: bad("hook_type_alt invalid")
    for f, n in TEXT.items():
        v = r.get(f)
        if not isinstance(v, str): bad(f"{f} must be a string")
        elif len(v.split()) > n + 8: bad(f"{f} too long ({len(v.split())} words)")
    for f in SCORES_15:
        v = r.get(f)
        if not isinstance(v, (int, float)) or not 1 <= v <= 5: bad(f"{f}={v!r} must be 1..5")
    if not isinstance(r.get("humour_intensity"), (int, float)) or not 0 <= r["humour_intensity"] <= 3: bad("humour_intensity must be 0..3")
    if not isinstance(r.get("virality_pred"), (int, float)) or not 1 <= r["virality_pred"] <= 10: bad("virality_pred must be 1..10")
    rf = r.get("risk_flags")
    if not isinstance(rf, list) or not rf or any(x not in ENUMS["risk_flag"] for x in rf): bad("risk_flags must be a non-empty list of enum values")
    elif "none" in rf and len(rf) > 1: bad("risk_flags: 'none' cannot be combined")
    ch = r.get("changes")
    if not isinstance(ch, list) or not ch: bad("changes must be a non-empty list")
    else:
        for c in ch:
            if not isinstance(c, dict) or c.get("priority") not in ENUMS["priority"] or c.get("category") not in ENUMS["change_category"] or not isinstance(c.get("action"), str):
                bad(f"bad change item {c!r}")
    return errs


def validate_file(path, expect=None):
    errs = []
    try: rows = json.load(open(path))
    except Exception as e: return [f"cannot parse {path}: {e}"]
    if not isinstance(rows, list): return ["top level must be a JSON list of records"]
    for r in rows: validate_record(r, errs)
    nos = [r.get("no") for r in rows]
    if len(set(nos)) != len(nos): errs.append("duplicate no")
    if expect is not None and sorted(nos) != sorted(expect): errs.append(f"expected nos {sorted(expect)} got {sorted(nos)}")
    return errs


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        exp = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
        e = validate_file(sys.argv[2], exp); print("OK" if not e else "\n".join(e[:40])); sys.exit(1 if e else 0)
    for k, v in ENUMS.items():
        print(f"\n[{k}]")
        for a, b in v.items(): print(f"  {a}" + (f": {b}" if b else ""))
    print("\nScores 1..5:", ", ".join(SCORES_15), "| virality_pred 1..10 | humour_intensity 0..3")
    print("Text limits (words):", TEXT)
    print("Record fields:", FIELDS)
