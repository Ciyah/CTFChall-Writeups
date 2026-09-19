import socket
import sys
import time

payload = open(sys.argv[1] if len(sys.argv) > 1 else "solve.c", "rb").read().rstrip(b"\n") + b"\n\n"
with socket.create_connection(("wastingtime.chal.sunwaycybersecurityclub.org", 1337)) as sock:
    sock.sendall(payload)
    start = time.monotonic()
    while True:
        data = sock.recv(4096)
        print(f"{time.monotonic() - start:8.3f} {data!r}", flush=True)
        if not data:
            break
