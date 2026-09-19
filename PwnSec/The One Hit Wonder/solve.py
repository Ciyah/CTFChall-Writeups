#!/usr/bin/env python3
import socket
import ssl
from determinant_attack import build, numeric_root

HOST = "dafa4318927a3ef7.chal.ctf.ae"


class Tube:
    def __init__(self):
        raw = socket.create_connection((HOST, 443))
        self.s = ssl.create_default_context().wrap_socket(raw, server_hostname=HOST)
        self.buf = b""

    def recvuntil(self, marker):
        while marker not in self.buf:
            chunk = self.s.recv(4096)
            if not chunk:
                raise EOFError(self.buf)
            self.buf += chunk
        end = self.buf.index(marker) + len(marker)
        out, self.buf = self.buf[:end], self.buf[end:]
        return out

    def sendline(self, value):
        self.s.sendall(str(value).encode() + b"\n")


def collect():
    io = Tube()
    io.recvuntil(b"> ")
    io.sendline(1)
    info = io.recvuntil(b"> ").decode()
    lines = info.splitlines()
    p = int(lines[0].split("=")[1])
    n = int(lines[1].split("=")[1])
    k = int(lines[2].split("=")[1])
    ys = []
    for x in range(8):
        io.sendline(2)
        io.recvuntil(b"x = ")
        io.sendline(x)
        reply = io.recvuntil(b"> ").decode().splitlines()
        ys.append(int(reply[1].split("=")[1]))
    return io, p, n, k, ys


if __name__ == "__main__":
    io, p, n, k, ys = collect()
    ts = list(range(8))
    for depth in (2, 3):
        rows, B = build(p, n, k, ts, ys, depth)
        if len(rows) < 8:
            continue
        errors = numeric_root(rows, B, 8, tries=30)
        if errors is None:
            continue
        zs = [h * B + e for h, e in zip(ys, errors)]
        u = ((ts[1] * zs[1] - ts[0] * zs[0]) * pow(zs[0] - zs[1], -1, p)) % p
        v = zs[0] * (u + ts[0]) % p
        if not all(v * pow(u+t, -1, p) % p == z for t, z in zip(ts, zs)):
            continue
        io.sendline(4)
        io.recvuntil(b"a = ")
        io.sendline(u)
        io.recvuntil(b"b = ")
        io.sendline(v)
        print(io.recvuntil(b"}").decode())
        break
    else:
        raise RuntimeError("lattice/root recovery failed")
