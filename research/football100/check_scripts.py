import json,glob,re
A={a["no"]:a for a in json.load(open("scripts/assign.json"))}
BAD=re.compile(r"doping|banned substance|cancer|illness|injur|cruciate|hospital|funeral|died|death|war\b|invasion|wife|husband|children|his son|his daughter|divorce|arrest|lawsuit|trial|jail|prison|racis",re.I)
ok=0;bad=[]
for no in sorted(A):
    p=f"scripts/{no:03d}.json"
    try: j=json.load(open(p))
    except Exception as e: bad.append((no,"missing/invalid")); continue
    t=" ".join(l["vo"] for l in j["lines"]); n=len(t); lim=A[no]["limit_chars"]; pr=[]
    if n>lim: pr.append(f"len {n}>{lim}")
    if "aboutfootball dot UK" not in j["lines"][-1]["vo"]: pr.append("cta")
    if j["voice"]!=A[no]["voice"]: pr.append("voice")
    m=BAD.findall(t)
    if m: pr.append("words:"+",".join(set(x.lower() for x in m)))
    if A[no]["comic"] and len(j.get("inserts",[]))!=3: pr.append(f"inserts {len(j.get('inserts',[]))}")
    if pr: bad.append((no,"; ".join(pr)))
    else: ok+=1
print("ok",ok,"of",len(A)); [print(b) for b in bad]
