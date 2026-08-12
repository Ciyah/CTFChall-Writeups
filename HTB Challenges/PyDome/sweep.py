#!/usr/bin/env python3
import hashlib, socket, random
from concurrent.futures import ThreadPoolExecutor, as_completed

HOST, PORT = "154.57.164.76", 31595
story = open("story_leaked.txt").read()
digest = hashlib.sha256(b"").hexdigest()
indices = [story.index(c) for c in digest]

def payload(n):
    real = min(n, 64)
    fields = [chr(i) if p < real else str(i) for p, i in enumerate(indices)]
    fields += ["xx"] * (n - real)
    fields += ["999999"] * (100 - len(fields))
    assert len(fields) == 100
    return (",".join(fields) + "\n").encode()

def test(n):
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            sock.settimeout(4); sock.recv(4096)
            route = random.Random(n).sample(range(101), 5)
            for attempt, width in enumerate(route):
                sock.sendall(payload(width))
                data = b""
                while b"HTB{" not in data and b"Try again" not in data:
                    part = sock.recv(65536)
                    if not part: break
                    data += part
                if b"HTB{" in data:
                    return (n, attempt), data
            return (n, 4), data
    except OSError:
        return (n, -1), b""

with ThreadPoolExecutor(max_workers=20) as pool:
    for future in as_completed([pool.submit(test, n) for n in range(3000)]):
        n, data = future.result()
        if b"HTB{" in data:
            print("N", n, data.decode(errors="replace"))
            raise SystemExit
print("no hit")
