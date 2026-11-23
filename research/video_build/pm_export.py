import json, mcp, time, sys
ids=json.load(open("v2_ids.json")); P=ids["P"]; s=mcp.session()
tl,out=sys.argv[1],sys.argv[2]
r=mcp.call(s,"export_project",{"projectId":P,"timelineId":tl,"mode":"video","outputPath":out})
t=r["result"]["content"][0]["text"]; print(t[:200])
for i in range(60):
    time.sleep(4); t=mcp.call(s,"manage_exports",{"projectId":P,"action":"list"})["result"]["content"][0]["text"]
    if out.split("/")[-1] in t and '"status":"completed"' in t.split(out.split("/")[-1])[1][:300]: print("done"); break
