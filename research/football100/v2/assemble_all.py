#!/usr/bin/env python3
"""Run assemble.build for many videos in parallel (separate work dir per video). Usage: assemble_all.py [-j 4] NNN ...  (default all 100)"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
a = sys.argv[1:]; J = 4
if "-j" in a: i = a.index("-j"); J = int(a[i + 1]); del a[i:i + 2]
nos = [int(x) for x in a] or list(range(1, 101))
def go(no):
    r = subprocess.run(["python3", f"{H}/assemble.py", str(no)], capture_output=True, text=True, cwd=R)
    return no, r.returncode, (r.stdout.strip().splitlines() or [""])[-1] + (" " + r.stderr[-300:] if r.returncode else "")
with ThreadPoolExecutor(J) as ex:
    for no, rc, msg in ex.map(go, nos): print("OK " if rc == 0 else "FAIL", no, msg, flush=True)
