#!/usr/bin/env python3
"""Mechanical (code-computed) features for every video + compact context files for annotators.
Writes report/features.json and report/ctx/NNN.md. Safe to re-run."""
import glob, json, os, random, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R = f"{H}/report"
sys.path.insert(0, H)
import cover  # noqa: E402  (cover.py has a __main__ guard)

NUMW = re.compile(r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|nil|percent)\b", re.I)
EL = {"EL_A": ("Nathaniel", "9rR45HW0vcBmpCbkc4m9"), "EL_B": ("Marcus", "XPItcki6tTIlq8JhllXm"), "EL_C": ("Cedric M", "RC8oAA5RAiRVQbaOrbkz")}
nos = list(range(1, 101)) + [901, 902, 903, 904]
assign = {a["no"]: a for a in json.load(open(f"{H}/scripts/assign.json"))}
news = {n["id"]: n for n in json.load(open(f"{H}/news/news_dedup.json"))}


def sentences(t): return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t.strip()) if s.strip()]
def norm(s): return re.sub(r"[^a-z ]", "", s.lower()).strip()


def video_path(no):
    g = glob.glob(f"{H}/deliver/{no:03d}_*_small.mp4") or glob.glob(f"{H}/pilot/{no:03d}_*_small.mp4")
    return g[0] if g else None


def probe(p):
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())
    r = subprocess.run(["ffmpeg", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = re.findall(r"I:\s+(-?\d+\.\d+) LUFS", r); tp = re.findall(r"Peak:\s+(-?\d+\.\d+) dBFS", r)
    return d, (float(lufs[-1]) if lufs else None), (float(tp[-1]) if tp else None)


rows = {}
for no in nos:
    j = json.load(open(f"{H}/scripts/{no:03d}.json")); a = assign.get(no, {})
    lines = [l["vo"] if isinstance(l, dict) else l for l in j["lines"]]
    text = " ".join(lines); words = len(text.split()); hook = lines[0]; cta = lines[-1]
    sents = sentences(text); cta_open = sentences(cta)[0] if sentences(cta) else cta
    v = video_path(no); eng = "ElevenLabs" if str(j.get("voice", "")).startswith("EL") else "Kokoro"
    ev = news.get(a.get("ref")) if a.get("kind") == "news" else None
    vname, vid = (EL[j["voice"]] if eng == "ElevenLabs" else ("bm_george (British male)", "bm_george"))
    rnd = random.Random(no); rnd.random(); tilt = rnd.choice([-4, 4])
    hp = f"{H}/codex/hero/{no:03d}.png"
    cpng = f"{H}/deliver/{no:03d}_cover.png" if os.path.exists(f"{H}/deliver/{no:03d}_cover.png") else f"{H}/pilot/{no:03d}_cover.png"
    ins = j.get("inserts") or []
    flips = sum(os.path.exists(f"{H}/clips/flip_{no:03d}_{k}.mp4") for k in range(1, len(ins) + 1))
    lim = a.get("limit_chars", 1100)
    rows[no] = dict(
        no=no, group="main" if no <= 100 else "pilot_split", video_file=os.path.basename(v) if v else None, video_src=v, cover_src=cpng,
        subject=j.get("subject"), title=j.get("title"), source_kind=a.get("kind", "split"), source_ref=a.get("ref"), assign_angle=a.get("angle"), assign_hint=a.get("hint"),
        news_date=ev.get("date") if ev else None, news_domain=ev.get("source_domain") if ev else None, news_n_sources=ev.get("n_sources") if ev else None,
        news_n_domains=ev.get("n_domains") if ev else None, news_sensitive=ev.get("sensitive") if ev else None, news_confidence=ev.get("confidence") if ev else None,
        voice_engine=eng, voice_label=j.get("voice"), voice_name=vname, voice_id=vid,
        voice_model="eleven_flash_v2_5 (atempo 1.12)" if eng == "ElevenLabs" else "Kokoro-82M (speed 1.12)",
        words=words, chars=len(text), est_seconds=j.get("est_seconds"), limit_chars=lim, n_lines=len(lines), n_sentences=len(sents),
        avg_words_per_sentence=round(words / max(1, len(sents)), 1),
        hook_text=hook, hook_words=len(hook.split()), hook_chars=len(hook), hook_has_number=bool(NUMW.search(hook)), hook_has_question="?" in hook,
        hook_named_entities=len([w for w in re.findall(r"\b[A-Z][a-z']+", hook)[1:]]) ,
        cta_text=cta, cta_opener=cta_open, cta_opener_norm=norm(cta_open),
        comic=bool(j.get("comic")), comic_style=j.get("style"), n_inserts=len(ins), inserts_after_lines=[i.get("after_line") for i in ins], flip_clips_ready=flips,
        footage_clips=len(glob.glob(f"{H}/footage/{no:03d}/*.mp4")), footage_terms=len(j.get("footage_terms") or []), facts_used=len(j.get("facts_used") or []),
        script_comic_score=j.get("comic_score"), script_notes=j.get("notes"),
        cover_title=cover.hook(j).upper(), cover_joke=cover.joke(j).upper(), cover_burst=cover.BURSTS[no % len(cover.BURSTS)], cover_emoji="".join(cover.EMOJI[no % 4]),
        cover_sunburst="red" if no % 2 else "orange", cover_tilt_deg=tilt, cover_hero_source="codex hero art" if os.path.exists(hp) else "footage frame (comic filter v2)",
        cover_title_equals_script_title=bool(j.get("title")) and cover.hook(j).upper() == (j.get("title") or "").upper().rstrip(".,;:"),
        flag_over_char_limit=len(text) > lim, flag_over_40s=None, first_frame_cover="no (set by cover_frame.py)",
    )
# CTA opener repeats
from collections import Counter
cnt = Counter(r["cta_opener_norm"] for r in rows.values())
for r in rows.values(): r["cta_opener_repeat"] = cnt[r["cta_opener_norm"]]
# duration + loudness in parallel
def job(no):
    p = rows[no]["video_src"]
    return no, (probe(p) if p else (None, None, None))
with ThreadPoolExecutor(4) as ex:
    for no, (d, l, tp) in ex.map(job, nos):
        r = rows[no]; r["duration_s"] = round(d, 1) if d else None; r["loudness_lufs"] = l; r["true_peak_dbfs"] = tp
        r["words_per_second"] = round(r["words"] / d, 2) if d else None; r["flag_over_40s"] = bool(d and d > 40.5)
json.dump([rows[n] for n in nos], open(f"{R}/features.json", "w"), ensure_ascii=False, indent=1)

# compact context files for annotators
for no in nos:
    r = rows[no]; j = json.load(open(f"{H}/scripts/{no:03d}.json")); out = []
    out.append(f"# Video {no:03d}  ({r['group']})\nsubject: {r['subject']}\non-screen title: {r['title']}\nsource kind: {r['source_kind']} | angle: {r['assign_angle']} | hint: {r['assign_hint']}")
    if r["source_kind"] == "news": out.append(f"news date: {r['news_date']} | domain: {r['news_domain']} | n_sources: {r['news_n_sources']} (domains {r['news_n_domains']}) | sensitive: {r['news_sensitive']} | confidence: {r['news_confidence']}")
    out.append(f"voice: {r['voice_label']} {r['voice_name']} ({r['voice_engine']}) | duration {r['duration_s']}s | {r['words']} words / {r['chars']} chars (limit {r['limit_chars']}) | comic={r['comic']} style={r['comic_style']} | inserts planned {r['n_inserts']}")
    out.append("## Spoken lines (number: voice-over | on-screen card)")
    for i, l in enumerate(j["lines"], 1):
        vo = l["vo"] if isinstance(l, dict) else l; card = l.get("card") if isinstance(l, dict) else None
        out.append(f"{i}. {vo}" + (f"   [card: {card}]" if card else ""))
    out.append(f"## CTA opener repeated in {r['cta_opener_repeat']} videos of the set: \"{r['cta_opener']}\"")
    out.append(f"## Poster (cover image) text: headline = \"{r['cover_title']}\" | speech bubble joke = \"{r['cover_joke']}\" | burst word = \"{r['cover_burst']}\" | hero = {r['cover_hero_source']}")
    out.append("## facts_used\n" + "\n".join("- " + str(x)[:200] for x in (j.get("facts_used") or [])[:8]))
    out.append(f"## script notes (author's own risks)\n{j.get('notes')}")
    open(f"{R}/ctx/{no:03d}.md", "w").write("\n".join(out) + "\n")
print("features", len(rows), "ctx", len(glob.glob(f"{R}/ctx/*.md")))
print("over char limit:", [n for n in nos if rows[n]["flag_over_char_limit"]], "| over 40.5s:", [n for n in nos if rows[n]["flag_over_40s"]])
print("cta repeats:", cnt.most_common(4))
