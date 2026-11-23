import json, mcp, time, sys, os
which=sys.argv[1]; ids=json.load(open(f"v3_{which}_ids.json")); P=ids["P"]; s=mcp.session()
out=os.path.abspath(f"v3_{which}_raw.mp4")
mcp.call(s,"set_project_settings",{"projectId":P,"timelineId":ids["TL"],"width":1080,"height":1920})
r=mcp.call(s,"export_project",{"projectId":P,"timelineId":ids["TL"],"mode":"video","outputPath":out}); print(r["result"]["content"][0]["text"][:120])
for i in range(120):
    time.sleep(5); t=mcp.call(s,"manage_exports",{"projectId":P,"action":"list"})["result"]["content"][0]["text"]
    j=json.loads(t)["exports"]; e=[x for x in j if x["filename"]==os.path.basename(out)]
    if e and e[0]["status"]=="completed": print("done"); break
    if e and e[0]["status"] in ("failed","cancelled"): print(e[0]); break
