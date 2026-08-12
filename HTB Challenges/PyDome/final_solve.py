#!/usr/bin/env python3
import hashlib
import socket

HOST, PORT = "154.57.164.76", 31595
story = open("story_leaked.txt").read()
target = hashlib.sha256(b"").hexdigest()

fields = []
for pos, char in enumerate(target):
    candidates = [i for i, c in enumerate(story) if c == char]
    index = next(i for i in candidates if not chr(i).isdigit() and chr(i) not in ",\r\n")
    fields.append(chr(index))

# These enter non_int_arr, but ord("xx") raises and therefore they never enter
# int_arr. This makes the diagnostic loop consume 100 randrange(100) calls
# while the selected story output remains exactly the 64-byte digest.
fields += ["xx"] * 36
assert len(fields) == 100
payload = (",".join(fields) + "\n").encode()
with socket.create_connection((HOST, PORT), timeout=5) as sock:
    sock.settimeout(5)
    print(sock.recv(4096).decode(), end="")
    for _ in range(5):
        sock.sendall(payload)
        data = b""
        try:
            while True:
                part = sock.recv(65536)
                if not part:
                    break
                data += part
                if b"HTB{" in data or b"Try again" in data:
                    break
        except TimeoutError:
            pass
        if b"HTB{" in data or b"Level 4/4 PASSED" in data:
            print(data.decode(errors="replace"))
            break
