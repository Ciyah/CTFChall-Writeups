#!/usr/bin/env python3
import re
import socket
import sys


HOST = sys.argv[1] if len(sys.argv) > 1 else "154.57.164.82"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 31793

player_re = re.compile(rb"^Player (\d+): ([1-6 ]+)$")


def solve() -> None:
    scores: dict[int, int] = {}
    ready_sent = False
    buf = b""

    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        sock.settimeout(30)
        while True:
            chunk = sock.recv(65536)
            if not chunk:
                break
            sys.stdout.buffer.write(chunk)
            sys.stdout.buffer.flush()
            buf += chunk

            if not ready_sent and b"Are you ready?" in buf and buf.endswith(b"> "):
                sock.sendall(b"1\n")
                ready_sent = True

            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                line = line.rstrip(b"\r")
                match = player_re.match(line)
                if match:
                    player = int(match.group(1))
                    scores[player] = sum(map(int, match.group(2).split()))
                elif line == b"Who wins this round?":
                    # Python's challenge picks the last entry on equal scores.
                    winner = max(scores, key=lambda p: (scores[p], p))
                    sock.sendall(f"{winner}\n".encode())
                    scores.clear()


if __name__ == "__main__":
    solve()
