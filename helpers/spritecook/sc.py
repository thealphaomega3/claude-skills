#!/usr/bin/env python3
"""Call a SpriteCook MCP tool over HTTP with an API key read from a private file.

The key is read from ~/.config/spritecook/api_key and never printed, logged or
written anywhere else. Usage:

    sc.py <tool_name> '<json arguments>'
    sc.py tools                       # list tool names

Prints the tool's result (its text content parsed as JSON when possible).
"""
import json, os, sys, urllib.request, urllib.error

URL = "https://api.spritecook.ai/mcp/"
KEY_FILE = os.path.expanduser("~/.config/spritecook/api_key")


def key():
    try:
        with open(KEY_FILE) as f:
            k = f.read().strip()
    except FileNotFoundError:
        sys.exit("no key file at ~/.config/spritecook/api_key")
    if not k:
        sys.exit("key file is empty")
    return k


def post(body, session=None, timeout=200):
    headers = {
        "content-type": "application/json",
        "accept": "application/json, text/event-stream",
        "authorization": "Bearer " + key(),
        "mcp-protocol-version": "2025-06-18",
    }
    if session:
        headers["mcp-session-id"] = session
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            sid = r.headers.get("mcp-session-id")
            raw = r.read().decode()
            ctype = r.headers.get("content-type", "")
    except urllib.error.HTTPError as e:
        # never echo request headers; the body is the server's own message
        sys.exit("HTTP %d: %s" % (e.code, e.read().decode()[:400]))
    if not raw.strip():
        return None, sid
    if "text/event-stream" in ctype:
        msgs = [json.loads(l[5:]) for l in raw.splitlines() if l.startswith("data:") and l[5:].strip()]
        msg = next((m for m in reversed(msgs) if "result" in m or "error" in m), msgs[-1] if msgs else None)
    else:
        msg = json.loads(raw)
    return msg, sid


def session():
    msg, sid = post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                     "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                                "clientInfo": {"name": "tomebound-preview", "version": "1"}}})
    post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    return sid


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sid = session()
    if sys.argv[1] == "tools":
        msg, _ = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, sid)
        for t in msg["result"]["tools"]:
            print(t["name"])
        return
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    msg, _ = post({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                   "params": {"name": sys.argv[1], "arguments": args}}, sid)
    if "error" in msg:
        sys.exit("error: %s" % json.dumps(msg["error"])[:600])
    res = msg["result"]
    if res.get("structuredContent"):
        print(json.dumps(res["structuredContent"], indent=1))
        return
    for c in res.get("content", []):
        if c.get("type") == "text":
            try:
                print(json.dumps(json.loads(c["text"]), indent=1))
            except ValueError:
                print(c["text"])


if __name__ == "__main__":
    main()
