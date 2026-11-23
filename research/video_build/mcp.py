import json, sys, urllib.request, re
URL="http://127.0.0.1:19789/mcp"
def _post(body, sid=None):
    h={"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
    if sid: h["MCP-Session-Id"]=sid
    r=urllib.request.urlopen(urllib.request.Request(URL,json.dumps(body).encode(),h),timeout=300)
    return r.headers.get("MCP-Session-Id"), r.read().decode()
def session():
    sid,_=_post({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"cc","version":"1"}}})
    _post({"jsonrpc":"2.0","method":"notifications/initialized"},sid)
    return sid
def rpc(sid,method,params=None,i=2):
    _,t=_post({"jsonrpc":"2.0","id":i,"method":method,"params":params or {}},sid)
    for blk in t.split("\n\n"):
        m=re.search(r"data: (\{.*\})",blk)
        if m: return json.loads(m.group(1))
def call(sid,name,args): return rpc(sid,"tools/call",{"name":name,"arguments":args})
if __name__=="__main__":
    s=session()
    if sys.argv[1]=="tools":
        for t in rpc(s,"tools/list")["result"]["tools"]: print(t["name"],"-",t["description"][:90].replace("\n"," "))
    else:
        print(json.dumps(call(s,sys.argv[1],json.loads(sys.argv[2])),indent=1)[:6000])
