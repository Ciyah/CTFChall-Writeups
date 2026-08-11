#!/usr/bin/env python3
import random
import re
import socket
import threading
import time

HOST = "154.57.164.78"
PORT = 32133
STOP = threading.Event()
SEEN = 0
SEEN_LOCK = threading.Lock()


def lcg(seed):
    return (1664525 * seed + 1013904223) % (2**32)


def shiny_starter(mac, elapsed):
    seed = lcg(int(mac.replace(":", ""), 16) + elapsed)
    random.seed(seed)
    tid = random.randint(0, 65535)
    sid = random.randint(0, 65535)
    for starter in range(3):
        random.seed(seed + starter)
        for _ in range(6):
            random.randint(20, 31)
        random.choice(range(25))
        pid = random.randint(0, 2**32 - 1)
        if (tid ^ sid ^ (pid & 0xffff) ^ (pid >> 16)) < 8:
            return starter + 1
    return None


def recv_until(sock, marker, timeout=45):
    sock.settimeout(timeout)
    data = b""
    while marker not in data:
        chunk = sock.recv(65536)
        if not chunk:
            break
        data += chunk
    return data


def attempt(number):
    global SEEN
    if STOP.is_set():
        return
    try:
        sock = socket.create_connection((HOST, PORT), timeout=3)
        first = recv_until(sock, b"Game Library Synced:", 3)
        logo_time = time.monotonic()
    except OSError:
        try:
            sock.close()
        except UnboundLocalError:
            pass
        return
    match = re.search(rb"Mac Address: ([0-9a-f:]{17})", first)
    if not match:
        sock.close()
        return
    mac = match.group(1).decode()
    with SEEN_LOCK:
        SEEN += 1
        if SEEN % 250 == 0:
            print(f"checked {SEEN} MACs", flush=True)
    # With the built-in sleeps, the name is read 18 seconds after boot_time.
    result = next(((elapsed, shiny_starter(mac, elapsed))
                   for elapsed in range(25, 46)
                   if shiny_starter(mac, elapsed) is not None), None)
    if result is None:
        sock.close()
        return
    elapsed, choice = result
    print(f"candidate #{number}: {mac}, elapsed {elapsed}, starter {choice}", flush=True)
    data = first + recv_until(sock, b"Enter your name:", 40)
    # boot_time is assigned immediately after the initial logo's two-second sleep.
    delay = logo_time + 2 + elapsed + 0.10 - time.monotonic()
    if delay < 0:
        print("candidate expired before prompt", flush=True)
        sock.close()
        return
    time.sleep(delay)
    sock.sendall(b"hunter\n")
    data += recv_until(sock, b"Choose your starter Poketmon (1, 2, or 3):", 40)
    sock.sendall(f"{choice}\n".encode())
    while True:
        try:
            chunk = sock.recv(65536)
            if not chunk:
                break
            data += chunk
        except socket.timeout:
            break
    text = data.decode(errors="ignore")
    flag = re.search(r"HTB\{[^}]+\}", text)
    if flag:
        print("FLAG:", flag.group(0), flush=True)
        STOP.set()
    else:
        print("candidate missed (elapsed-time boundary?)", flush=True)
    sock.close()


def main():
    counter = [0]
    lock = threading.Lock()
    def worker():
        while not STOP.is_set():
            with lock:
                counter[0] += 1
                number = counter[0]
            attempt(number)
    threads = [threading.Thread(target=worker, daemon=True) for _ in range(12)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
