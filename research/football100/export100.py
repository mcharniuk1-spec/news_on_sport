import json, sys, os, time
VB="<PROJECT_ROOT>/research/video_build"; H="<PROJECT_ROOT>/research/football100"
sys.path.insert(0,VB); import mcp
no=int(sys.argv[1]); ids=json.load(open(f"{H}/builds/{no:03d}_ids.json")); P=ids["P"]; s=mcp.session()
out=f"{H}/builds/{no:03d}_raw.mp4"
mcp.call(s,"set_project_settings",{"projectId":P,"timelineId":ids["TL"],"width":1080,"height":1920})
r=mcp.call(s,"export_project",{"projectId":P,"timelineId":ids["TL"],"mode":"video","outputPath":out}); print(r["result"]["content"][0]["text"][:100])
for i in range(160):
    time.sleep(5); t=mcp.call(s,"manage_exports",{"projectId":P,"action":"list"})["result"]["content"][0]["text"]
    e=[x for x in json.loads(t)["exports"] if x["filename"]==os.path.basename(out)]
    if e and e[0]["status"]=="completed": print("done"); break
    if e and e[0]["status"] in("failed","cancelled"): print(e[0]); sys.exit(1)
