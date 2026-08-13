#!/usr/bin/env python3
import time
import urllib.parse
import requests

IP, PORT = "154.57.164.82", 31059
BASE = f"http://{IP}:{PORT}"
SSO = f"sso.edulearn.htb:{PORT}"
CID = "1a2abb8b-9bb5-4463-8f74-d7b129bb7040"
s = requests.Session()

def req(method, path, **kwargs):
    headers = {"Host": SSO}
    headers.update(kwargs.pop("headers", {}))
    return s.request(method, BASE + path, headers=headers, timeout=20, **kwargs)

email = f"modes{int(time.time())}@x.htb"
password = "password123"
req("POST", "/api/register", json={"email": email, "password": password, "name": "Modes"})
req("POST", "/api/login", json={"email": email, "password": password})

for mode in ("query", "fragment", "form_post"):
    redirect = f"http://edulearn.htb:{PORT}/oauth/callback/hold-{mode}"
    params = urllib.parse.urlencode({
        "response_type": "code", "response_mode": mode, "client_id": CID,
        "scope": "email name", "redirect_uri": redirect,
    })
    r = req("GET", "/oauth/authorize?" + params, allow_redirects=False)
    if r.status_code == 200:
        r = req("POST", "/oauth/authorize", data={
            "client_id": CID, "scope": "email name", "redirect_uri": redirect,
            "state": "", "approved": "true",
        }, allow_redirects=False)
    print(mode, r.status_code, r.headers.get("location"), r.headers.get("content-type"), flush=True)

for path in ("/.well-known/openid-configuration", "/oauth/clients", "/clients",
             "/register-client", "/logout", "/oauth/logout"):
    r = req("GET", path, allow_redirects=False)
    print("route", path, r.status_code, r.headers.get("location"), flush=True)
