#!/usr/bin/env python3
"""Reconcile two independent annotations of one batch.
  reconcile.py NN            -> prints disagreements (JSON) that need adjudication
  reconcile.py NN --apply    -> merges A+B (+ annot/ADJ_NN.json decisions) into final/NN.json and writes final/agreement_NN.json
ADJ_NN.json format: {"<no>": {"<field>": <chosen value>, ...}}  (field names as in taxonomy.FIELDS; risk_flags takes a list)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import taxonomy as T
D = os.path.dirname(os.path.abspath(__file__))
nn = sys.argv[1]; apply = "--apply" in sys.argv
A = {r["no"]: r for r in json.load(open(f"{D}/annot/A_{nn}.json"))}
B = {r["no"]: r for r in json.load(open(f"{D}/annot/B_{nn}.json"))}
assert set(A) == set(B), f"A/B number sets differ: {sorted(set(A) ^ set(B))}"
adj = json.load(open(f"{D}/annot/ADJ_{nn}.json")) if os.path.exists(f"{D}/annot/ADJ_{nn}.json") else {}
INT_FIELDS = T.SCORES_15 + ["humour_intensity", "virality_pred"]
dis = []; agree = {}; merged = []
PR = {"P1": 1, "P2": 2, "P3": 3}
for no in sorted(A):
    a, b, m = A[no], B[no], {}
    for f in T.SINGLE_ENUM + ["hook_type_alt"]:
        agree.setdefault(f, []).append(a[f] == b[f])
        if a[f] == b[f]: m[f] = a[f]
        else:
            dis.append({"no": no, "field": f, "A": a[f], "B": b[f]}); m[f] = adj.get(str(no), {}).get(f, a[f])
    for f in INT_FIELDS:
        d = abs(a[f] - b[f]); lim = 2 if f == "virality_pred" else 1
        agree.setdefault(f, []).append(d <= lim)
        if d <= lim: m[f] = round((a[f] + b[f]) / 2, 1)
        else:
            dis.append({"no": no, "field": f, "A": a[f], "B": b[f]}); m[f] = adj.get(str(no), {}).get(f, round((a[f] + b[f]) / 2, 1))
    fa, fb = set(a["risk_flags"]) - {"none"}, set(b["risk_flags"]) - {"none"}
    agree.setdefault("risk_flags", []).append(fa == fb)
    if fa != fb:
        dis.append({"no": no, "field": "risk_flags", "A": sorted(fa), "B": sorted(fb)})
        chosen = adj.get(str(no), {}).get("risk_flags", sorted(fa | fb))
    else: chosen = sorted(fa)
    m["risk_flags"] = chosen or ["none"]
    for f in ["hook_type_why", "hook_basis_detail", "story_summary", "poster_issue", "poster_change"]: m[f] = a[f] or b[f]
    ch = {}
    for c in a["changes"] + b["changes"]:
        k = c["category"]
        if k not in ch or PR[c["priority"]] < PR[ch[k]["priority"]]: ch[k] = c
    if len(ch) > 1: ch.pop("none", None)
    m["changes"] = sorted(ch.values(), key=lambda c: PR[c["priority"]])
    m["no"] = no; m["annotator_agreement"] = None
    merged.append(m)
if not apply:
    print(json.dumps(dis, ensure_ascii=False)); print(f"# {len(dis)} disagreements in batch {nn}", file=sys.stderr); sys.exit(0)
errs = []
for m in merged: T.validate_record(m, errs, "merged ")
for m in merged:
    n_dis = sum(1 for d in dis if d["no"] == m["no"]); m["annotator_agreement"] = round(1 - n_dis / (len(T.SINGLE_ENUM) + 1 + len(INT_FIELDS) + 1), 2)
if errs: print("\n".join(errs[:30])); sys.exit(1)
json.dump(merged, open(f"{D}/final/{nn}.json", "w"), ensure_ascii=False, indent=1)
json.dump({f: round(sum(v) / len(v), 3) for f, v in agree.items()}, open(f"{D}/final/agreement_{nn}.json", "w"), indent=1)
print(f"batch {nn}: merged {len(merged)} records, {len(dis)} disagreements, adjudicated fields: {sum(len(v) for v in adj.values())}")
