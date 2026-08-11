#!/usr/bin/env python3
import socket
from concurrent.futures import ThreadPoolExecutor

HOST = "154.57.164.82"
PORT = 32481


class Remote:
    def __init__(self):
        self.s = socket.create_connection((HOST, PORT))
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.buf = b""
        self.until(b"Option: ")

    def until(self, marker):
        while marker not in self.buf:
            chunk = self.s.recv(65536)
            if not chunk:
                raise EOFError(self.buf)
            self.buf += chunk
        pos = self.buf.index(marker) + len(marker)
        out, self.buf = self.buf[:pos], self.buf[pos:]
        return out

    def sendline(self, value):
        self.s.sendall(str(value).encode() + b"\n")

    def below_n(self, value):
        self.s.sendall(b"2\n" + hex(value)[2:].encode() + b"\n")
        reply = self.until(b"Option: ")
        return b"Thanks" in reply

    def batch_below_n(self, values):
        payload = b"".join(b"2\n" + hex(v)[2:].encode() + b"\n"
                           for v in values)
        self.s.sendall(payload)
        answers = []
        for _ in values:
            reply = self.until(b"Option: ")
            answers.append(b"Thanks" in reply)
        return answers

    def ciphertext(self):
        self.sendline(1)
        line = self.until(b"\n")
        value = int(line.split(b"Ciphertext: ", 1)[1], 16)
        self.until(b"Option: ")
        return value


def recover_modulus(r):
    # Bracket all normal RSA sizes in one pipelined request.
    exponents = list(range(128, 8193, 128))
    answers = r.batch_below_n([1 << x for x in exponents])
    first_over = answers.index(False)
    high = 1 << exponents[first_over]
    low = 1 << (exponents[first_over] - 128)
    print(f"bracketed at {high.bit_length()} bits", flush=True)

    # Pipeline 127 ordered thresholds at a time: one response batch yields 7 bits.
    fanout = 128
    while high - low > 1:
        width = high - low
        points = [low + width * i // fanout for i in range(1, fanout)]
        # Near the end integer division can duplicate points.
        points = sorted(set(points))
        answers = r.batch_below_n(points)
        count_below = sum(answers)
        bounds = [low, *points, high]
        low, high = bounds[count_below], bounds[count_below + 1]
        print(f"search: {(high-low).bit_length()} bits left", flush=True)
    return high


def one_comparison(value):
    r = Remote()
    result = r.below_n(value)
    r.s.close()
    return result


def recover_modulus_parallel(workers=64):
    # Coarsely bracket all plausible RSA sizes in one parallel round.
    exponents = list(range(128, 8193, 128))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        answers = list(pool.map(one_comparison, (1 << x for x in exponents)))
    first_over = answers.index(False)
    high = 1 << exponents[first_over]
    low = 1 << (exponents[first_over] - 128)
    print(f"bracketed N at {high.bit_length()} bits", flush=True)

    # A 64-way partition extracts about six bits per network round.
    with ThreadPoolExecutor(max_workers=workers) as pool:
        while high - low > 1:
            width = high - low
            points = [low + width * i // (workers + 1)
                      for i in range(1, workers + 1)]
            answers = list(pool.map(one_comparison, points))
            count_below = sum(answers)
            bounds = [low, *points, high]
            low, high = bounds[count_below], bounds[count_below + 1]
            print(f"binary search: {(high-low).bit_length()} bits left", flush=True)
    return high


if __name__ == "__main__":
    remote = Remote()
    c = remote.ciphertext()
    n = recover_modulus(remote)
    print(f"c = {c:#x}")
    print(f"n = {n:#x}")
