#!/usr/bin/env python3
"""Deduplicate and rank football100 news items.

Input : news/lane_*.json  (JSON arrays of news items)
Output: news_dedup.json, clusters.json, source_ranking.json (same folder as this script)

Pipeline
  1. load all lane files; drop items without url; low-confidence items are dropped
     only if the event cluster also has a non-low item (kept when nothing else covers it)
  2. normalise headline + entities (accents, club aliases, money, light stemming),
     IDF-weighted token-set Jaccard on headline+entities, plus URL equality
  3. union-find clustering with guards (date window, conflicting scorelines/money figures,
     same-URL roundup pages need a shared specific entity), then a coherence check that
     splits chained clusters
  4. merge each cluster into one item (best facts, union of urls -> "sources")
  5. source ranking per source_domain
  6. print counts: raw, after dedupe, per angle, per month

Usage: python3 dedupe.py [--debug]
"""
import glob
import json
import math
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- thresholds
T_HI = 0.62           # content-only merge: weighted Jaccard on headline+entities
T_URL_HI = 0.50       # same URL and this similar: merge (roundup pages have far lower scores)
T_URL = 0.35          # same URL, weaker similarity: needs headline agreement + a specific shared name
T_URL_HEAD = 0.25     # ... headline-only weighted Jaccard needed in that case
T_URL_HEAD_HI = 0.50  # same URL and headlines this similar: merge whatever the entity lists / dates say
T_URL_FACT = 0.30     # ... or the facts of the two items agree this much
T_MID = 0.50          # merge when facts also agree
T_FACT = 0.30         # facts-token agreement needed together with T_MID
MAX_DAY_GAP = 3       # events reported more than this many days apart are different
MAX_DAY_GAP_URL = 2   # same URL, different dates -> small gap only
SPLIT_LINK = 0.34     # coherence: member must be directly linked to this share of its cluster
SPECIFIC_IDF = 3.0    # a token this rare counts as a "specific" entity token
T_HEAD = 0.45         # headline-only weighted Jaccard for the same-day rule
RARE_IDF = 3.5        # tokens at least this rare count as "rare" shared evidence
MIN_RARE = 2          # same-day rule needs this many rare shared headline tokens
T_NEAR_SAME = 0.50    # same URL and similar wording merges regardless of reporting date
MAX_DAY_GAP_HI = 7    # very similar wording (>= T_GAP_HI) may be reported up to a week apart
T_GAP_HI = 0.75
T_COMB = 0.43         # same-day combined score 0.5*s + 0.25*headline + 0.25*facts
VERY_RARE_IDF = 5.0   # a name this rare (one player / small club) shared by two same-day items
T_SCORELINE = 0.35    # same scoreline + same day: lower bar on s
# ---------------------------------------------------------------------------

STOP = set("""a an the of to in on at for and or but with without after before as is are was were be been by from
his her their its this that these those into over under up down out off about than then them they he she it
has have had will would could should may might can not no new says say said saying set sets get gets got gone
amid per via vs v while when where who whom what which how why also still just only more most one two three
reportedly report reports reported according claims claim claimed latest news live now next first second
""".split())

# club / entity aliases -> canonical (applied on normalised text, longest first)
ALIASES = {
    "manchester united": "manutd", "man united": "manutd", "man utd": "manutd",
    "manchester city": "mancity", "man city": "mancity",
    "tottenham hotspur": "spurs", "tottenham": "spurs",
    "bayern munich": "bayern", "bayern munchen": "bayern", "fc bayern": "bayern",
    "paris saint germain": "psg", "paris sg": "psg",
    "inter milan": "inter", "internazionale": "inter",
    "ac milan": "acmilan",
    "atletico madrid": "atletico", "atletico de madrid": "atletico",
    "athletic club": "athletic", "athletic bilbao": "athletic",
    "newcastle united": "newcastle", "west ham united": "westham", "west ham": "westham",
    "wolverhampton wanderers": "wolves", "leeds united": "leeds",
    "nottingham forest": "forest", "borussia dortmund": "dortmund", "bvb": "dortmund",
    "borussia monchengladbach": "gladbach", "bayer leverkusen": "leverkusen",
    "rb leipzig": "leipzig", "real sociedad": "sociedad",
    "fc barcelona": "barcelona", "barca": "barcelona",
    "vinicius junior": "vinicius", "vini jr": "vinicius", "vinicius jr": "vinicius",
    "emiliano martinez": "emimartinez", "emi martinez": "emimartinez",
    "premier league": "premierleague", "champions league": "championsleague",
    "europa league": "europaleague", "world cup": "worldcup", "la liga": "laliga",
    "serie a": "seriea", "ligue 1": "ligue1",
    "fantasy premier league": "fpl",
}
ALIAS_RE = re.compile(r"\b(" + "|".join(sorted((re.escape(k) for k in ALIASES), key=len, reverse=True)) + r")\b")
MONEY_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:million|mln|m)\b")
SCORE_RE = re.compile(r"\b(\d{1,2})\s*[-:]\s*(\d{1,2})\b")


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm_text(s):
    s = strip_accents(str(s)).lower()
    s = s.replace("&", " and ").replace("'s", "").replace("’s", "")
    s = re.sub(r"[^a-z0-9.\-: ]", " ", s)
    s = ALIAS_RE.sub(lambda m: ALIASES[m.group(1)], s)
    s = MONEY_RE.sub(lambda m: m.group(1) + "m ", s)
    s = re.sub(r"\b(euros?|eur|pounds?|gbp|usd|dollars?)\b", " ", s)
    return s


def stem(t):
    if len(t) > 4 and t.endswith("ies"):
        return t[:-3] + "y"
    if len(t) > 4 and t.endswith("es") and t[-3] in "sxz":
        return t[:-2]
    if len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
        return t[:-1]
    return t


def tokens(s):
    out = []
    for t in re.split(r"[^a-z0-9]+", norm_text(s)):
        if not t or t in STOP:
            continue
        out.append(stem(t))
    return out


def day(d):
    try:
        y, m, dd = map(int, str(d)[:10].split("-"))
        return date(y, m, dd).toordinal()
    except Exception:
        return None


def scorelines(text):
    """Scorelines as unordered pairs: '0-2' and '2-0' describe the same match."""
    return {tuple(sorted((int(a), int(b)))) for a, b in SCORE_RE.findall(strip_accents(text))}


def money(text):
    return {float(x[:-1]) for x in re.findall(r"\b\d+(?:\.\d+)?m\b", norm_text(text))}


def money_conflict(a, b):
    """Both headlines quote money, and no figure in one is within 5% of a figure in the other."""
    if not a or not b:
        return False
    return not any(abs(x - y) <= 0.05 * max(x, y) for x in a for y in b)


class Item:
    __slots__ = ("i", "raw", "lane", "url", "dom", "day", "htok", "etok", "tok", "ftok", "scores", "money")

    def __init__(self, i, raw, lane):
        self.i, self.raw, self.lane = i, raw, lane
        self.url = (raw.get("url") or "").strip()
        self.dom = (raw.get("source_domain") or "").strip().lower()
        self.day = day(raw.get("date"))
        self.htok = set(tokens(raw.get("headline", "")))
        etok = set()
        for e in raw.get("entities", []):
            etok.update(tokens(e))
        self.etok = etok
        self.tok = self.htok | self.etok
        self.ftok = set(tokens(" ".join(raw.get("facts", []))))
        head = raw.get("headline", "")
        self.scores = scorelines(head)
        self.money = money(head)


def build_idf(items, attr):
    df = Counter()
    for it in items:
        df.update(getattr(it, attr))
    n = len(items)
    return {t: math.log((n + 1) / (c + 0.5)) + 0.2 for t, c in df.items()}


def wjac(a, b, idf):
    if not a or not b:
        return 0.0
    inter = sum(idf.get(t, 1.0) for t in a & b)
    union = sum(idf.get(t, 1.0) for t in a | b)
    return inter / union if union else 0.0


def load_all():
    items = []
    for f in sorted(glob.glob(os.path.join(HERE, "lane_*.json"))):
        lane = os.path.basename(f)[5:-5]
        with open(f, encoding="utf-8") as fh:
            data = json.load(fh)
        for raw in data:
            items.append(Item(len(items), raw, lane))
    return items


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def rare_shared(a, b, idf_h):
    return [t for t in (a.htok & b.htok) if idf_h.get(t, 0) >= RARE_IDF]


def compatible(a, b, s=0.0, nrare=0, hj=0.0):
    """Hard guards: dates close; scorelines / money figures in headlines must not conflict."""
    if a.day is not None and b.day is not None:
        gap = abs(a.day - b.day)
        if a.url == b.url:
            limit = 99 if (s >= T_NEAR_SAME or hj >= T_URL_HEAD_HI) else MAX_DAY_GAP_URL
        elif s >= T_GAP_HI:
            limit = MAX_DAY_GAP_HI
        elif nrare >= 4 and s >= 0.45:
            limit = 4          # same story re-dated by a later lane: many rare headline words agree
        else:
            limit = MAX_DAY_GAP
        if gap > limit:
            return False
    if a.scores and b.scores and not (a.scores & b.scores):
        return False
    if money_conflict(a.money, b.money):
        return False
    return True


def decide(a, b, idf_h, idf_f):
    """Return (merge?, score)."""
    s = wjac(a.tok, b.tok, idf_h)
    rare = rare_shared(a, b, idf_h)
    hj = wjac(a.htok, b.htok, idf_h)
    if not compatible(a, b, s, len(rare), hj):
        return False, 0.0
    fs = wjac(a.ftok, b.ftok, idf_f)
    same_url = bool(a.url) and a.url == b.url
    if s >= T_HI:
        return True, s
    if same_url:
        if s >= T_URL_HI or hj >= T_URL_HEAD_HI:
            return True, max(s, hj * 0.6)
        if s >= T_URL and fs >= T_URL_FACT:
            return True, s
        if s >= T_URL and hj >= T_URL_HEAD:
            # roundup page guard: must share a specific (rare) token in both entities and headline
            shared_e = [t for t in (a.etok & b.etok) if idf_h.get(t, 0) >= SPECIFIC_IDF]
            shared_h = [t for t in (a.htok & b.htok) if idf_h.get(t, 0) >= SPECIFIC_IDF]
            if shared_e and shared_h:
                return True, s
    if s >= T_MID and fs >= T_FACT:
        return True, s
    near_day = a.day is not None and b.day is not None and abs(a.day - b.day) <= 1
    if near_day:
        # same-day rules: different wording of one event
        if hj >= T_HEAD and len(rare) >= MIN_RARE and s >= 0.40:
            return True, s
        if hj >= 0.55 and len(rare) >= 3:            # headlines agree even if entity lists differ
            return True, max(s, hj * 0.6)
        if 0.5 * s + 0.25 * hj + 0.25 * fs >= T_COMB and len(rare) >= MIN_RARE:
            return True, s
        shared_all = [t for t in (a.tok & b.tok) if idf_h.get(t, 0) >= SPECIFIC_IDF - 0.5]
        very = [t for t in (a.etok & b.etok & a.htok & b.htok) if idf_h.get(t, 0) >= VERY_RARE_IDF]
        num = [t for t in (a.htok & b.htok) if t.isdigit() and idf_h.get(t, 0) >= 5.0]
        if num and len(shared_all) >= 3 and s >= 0.40:
            return True, s
        if len(rare) >= 3 and s >= 0.49:
            return True, s
        if very and hj >= 0.30 and s >= 0.38:       # same named player/club in headline + entities
            return True, s
        if s >= 0.40 and hj >= 0.30 and fs >= 0.30:  # three weak signals agree
            return True, s
    elif nrare_ok(a, b, rare, s):
        return True, s
    # match reports reported up to two days apart: same unordered scoreline, two rare shared tokens
    if a.day is not None and b.day is not None and abs(a.day - b.day) <= 2 and (a.scores & b.scores):
        shared_all = [t for t in (a.tok & b.tok) if idf_h.get(t, 0) >= SPECIFIC_IDF - 0.5]
        if s >= T_SCORELINE and len(shared_all) >= 2:
            return True, s
    return False, s


def nrare_ok(a, b, rare, s):
    """Items 2-4 days apart that agree on many rare headline words (same story reported late)."""
    return len(rare) >= 4 and s >= 0.45


def cluster(items, idf_h, idf_f):
    uf = UF(len(items))
    inv = defaultdict(list)
    for it in items:
        for t in it.tok:
            if idf_h.get(t, 0) >= 2.0:
                inv[t].append(it.i)
    cand = set()
    for ids in inv.values():
        if len(ids) > 400:
            continue
        for x in range(len(ids)):
            for y in range(x + 1, len(ids)):
                cand.add((ids[x], ids[y]))
    byurl = defaultdict(list)
    for it in items:
        byurl[it.url].append(it.i)
    for ids in byurl.values():
        for x in range(len(ids)):
            for y in range(x + 1, len(ids)):
                cand.add((ids[x], ids[y]))
    for a, b in cand:
        ok, _ = decide(items[a], items[b], idf_h, idf_f)
        if ok:
            uf.union(a, b)
    groups = defaultdict(list)
    for it in items:
        groups[uf.find(it.i)].append(it.i)
    final = []
    for members in groups.values():
        final.extend(split_incoherent(members, items, idf_h, idf_f))
    return final


def split_incoherent(members, items, idf_h, idf_f):
    """Undo chaining: A~B and B~C merged although A and C are different events.

    A member stays when it is directly linked (decide() true) to at least SPLIT_LINK of the other
    members; others are re-attached if they link to a kept member, or form their own cluster.
    """
    if len(members) <= 2:
        return [members]
    link = {}
    for x in range(len(members)):
        for y in range(x + 1, len(members)):
            link[(members[x], members[y])] = link[(members[y], members[x])] = decide(
                items[members[x]], items[members[y]], idf_h, idf_f)[0]
    frac = {a: sum(link[(a, b)] for b in members if b != a) / (len(members) - 1) for a in members}
    keep = [a for a in members if frac[a] >= SPLIT_LINK]
    if len(keep) == len(members):
        return [members]
    if not keep:
        keep = [max(members, key=lambda a: frac[a])]
    left = [a for a in members if a not in keep]
    out = [keep]
    still = []
    for a in left:
        if any(link[(a, b)] for b in keep):
            keep.append(a)
        else:
            still.append(a)
    if still:
        out.extend(split_incoherent(still, items, idf_h, idf_f) if len(still) < len(members) else [[a] for a in still])
    return out


# ------------------------------------------------------------------ merging
CONF_RANK = {"high": 3, "medium": 2, "low": 1}


def detail(it):
    r = it.raw
    return (CONF_RANK.get(r.get("confidence"), 0) >= 2,
            sum(len(f) for f in r.get("facts", [])) + len(r.get("background", "") or ""),
            len(r.get("facts", [])))


def merge_cluster(cid, members, items):
    its = sorted((items[i] for i in members), key=detail, reverse=True)
    best = its[0]
    r = best.raw
    facts, ft = [], []
    for it in its:
        for f in it.raw.get("facts", []):
            t = set(tokens(f))
            if any(len(t & u) / max(1, len(t | u)) > 0.5 for u in ft):
                continue
            facts.append(f)
            ft.append(t)
    facts = facts[:8]
    seen, sources = set(), []
    for it in its:
        for u in [it.url] + list(it.raw.get("extra_sources") or []):
            if u and u not in seen:
                seen.add(u)
                sources.append(u)
    domains = []
    for it in its:
        if it.dom and it.dom not in domains:
            domains.append(it.dom)
    ents, es = [], set()
    for it in its:
        for e in it.raw.get("entities", []):
            k = norm_text(e).strip()
            if k not in es:
                es.add(k)
                ents.append(e)
    foot, fs = [], set()
    for it in its:
        for t in it.raw.get("footage_terms", []) or []:
            if t.lower() not in fs:
                fs.add(t.lower())
                foot.append(t)
    angles = Counter(it.raw.get("angle") for it in its)
    top = angles.most_common()
    angle = r.get("angle") if angles[r.get("angle")] == top[0][1] else top[0][0]
    dates = sorted(str(it.raw.get("date")) for it in its if it.raw.get("date"))
    bg = max((it.raw.get("background", "") or "" for it in its), key=len)
    conf = max((it.raw.get("confidence") for it in its), key=lambda c: CONF_RANK.get(c, 0))
    return {
        "id": cid,
        "headline": r.get("headline"),
        "date": r.get("date"),
        "date_first": dates[0] if dates else None,
        "date_last": dates[-1] if dates else None,
        "angle": angle,
        "angles": dict(angles),
        "entities": ents,
        "facts": facts,
        "background": bg,
        "sensitive": any(bool(it.raw.get("sensitive")) for it in its),
        "confidence": conf,
        "footage_terms": foot[:8],
        "source_domain": r.get("source_domain"),
        "source_domains": domains,
        "sources": sources,
        "n_sources": len(sources),
        "n_domains": len(domains),
        "n_items_merged": len(its),
        "lanes": sorted({it.lane for it in its}),
        "member_headlines": [it.raw.get("headline") for it in its],
    }


# ------------------------------------------------------------- source ranking
def source_ranking(kept_items, merged):
    events_by_dom = Counter()
    for m in merged:
        for d in m["source_domains"]:
            events_by_dom[d] += 1
    by = defaultdict(list)
    for it in kept_items:
        by[it.dom or "(none)"].append(it)
    rows = []
    for dom, lst in by.items():
        n = len(lst)
        nf = [len(i.raw.get("facts", [])) for i in lst]
        fchars = [sum(len(f) for f in i.raw.get("facts", [])) / max(1, len(i.raw.get("facts", []))) for i in lst]
        bg = sum(1 for i in lst if len((i.raw.get("background") or "").strip()) >= 20) / n
        hi = sum(1 for i in lst if i.raw.get("confidence") == "high") / n
        rows.append({"source_domain": dom, "items": n, "events_covered": events_by_dom.get(dom, 0),
                     "avg_facts": round(sum(nf) / n, 3),
                     "avg_fact_chars": round(sum(fchars) / n, 1),
                     "background_share": round(bg, 3), "high_confidence_share": round(hi, 3)})
    mx_f = max(r["avg_facts"] for r in rows) or 1
    mx_c = max(r["avg_fact_chars"] for r in rows) or 1

    def raw_score(r):
        return (0.40 * r["avg_facts"] / mx_f + 0.25 * r["avg_fact_chars"] / mx_c
                + 0.20 * r["background_share"] + 0.15 * r["high_confidence_share"])

    # detail_score 0..100: facts/item 40%, fact length 25%, background 20%, high-confidence 15%;
    # shrunk toward the global mean (k = 10 items) so one lucky item cannot top the table
    glob_raw = sum(raw_score(r) for r in rows) / len(rows)
    K = 10
    for r in rows:
        r["detail_score"] = round(100 * (r["items"] * raw_score(r) + K * glob_raw) / (r["items"] + K), 2)
    rows.sort(key=lambda r: (-r["detail_score"], -r["items"], r["source_domain"]))
    for rank, r in enumerate(rows, 1):
        r["rank"] = rank
    return rows


# --------------------------------------------------------------------- main
def main():
    items = load_all()
    raw_n = len(items)
    print(f"raw items loaded: {raw_n} from {len(glob.glob(os.path.join(HERE, 'lane_*.json')))} lane files")

    with_url = [it for it in items if it.url]
    no_url = raw_n - len(with_url)
    for k, it in enumerate(with_url):
        it.i = k
    idf_h = build_idf(with_url, "tok")
    idf_f = build_idf(with_url, "ftok")

    clusters = cluster(with_url, idf_h, idf_f)

    kept_clusters, dropped_low = [], 0
    for mem in clusters:
        non_low = [i for i in mem if with_url[i].raw.get("confidence") != "low"]
        if non_low and len(non_low) < len(mem):
            dropped_low += len(mem) - len(non_low)
            mem = non_low
        kept_clusters.append(mem)
    low_only = sum(1 for m in kept_clusters if all(with_url[i].raw.get("confidence") == "low" for i in m))
    kept_clusters.sort(key=lambda m: (-len(m), min(with_url[i].raw.get("date", "") for i in m)))

    merged = [merge_cluster(f"ev{n:04d}", m, with_url) for n, m in enumerate(kept_clusters, 1)]
    kept_items = [with_url[i] for m in kept_clusters for i in m]

    out = lambda name: os.path.join(HERE, name)
    with open(out("news_dedup.json"), "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=1)
    with open(out("clusters.json"), "w", encoding="utf-8") as f:
        json.dump({m["id"]: m["member_headlines"] for m in merged}, f, ensure_ascii=False, indent=1)
    rank = source_ranking(kept_items, merged)
    with open(out("source_ranking.json"), "w", encoding="utf-8") as f:
        json.dump(rank, f, ensure_ascii=False, indent=1)

    print(f"dropped (no url): {no_url}")
    print(f"dropped (low confidence, event also covered by a non-low item): {dropped_low}")
    print(f"clusters made only of low-confidence items (kept, nothing else covers them): {low_only}")
    print(f"items entering merge: {len(kept_items)}")
    print(f"AFTER DEDUPE (merged events): {len(merged)}")
    print(f"events with >1 member: {sum(1 for m in merged if m['n_items_merged'] > 1)}; "
          f"largest cluster: {max(m['n_items_merged'] for m in merged)}")
    print("cluster size distribution:", dict(sorted(Counter(m['n_items_merged'] for m in merged).items())))
    print("per angle:", dict(Counter(m["angle"] for m in merged).most_common()))
    print("per month:", dict(sorted(Counter((m["date"] or "????-??")[:7] for m in merged).items())))
    print("top sources by detail_score:")
    for r in rank[:8]:
        print(f"   {r['rank']:>2}. {r['source_domain']:<24} items={r['items']:<4} avg_facts={r['avg_facts']:<5} "
              f"bg={r['background_share']:<5} score={r['detail_score']}")


if __name__ == "__main__":
    main()
