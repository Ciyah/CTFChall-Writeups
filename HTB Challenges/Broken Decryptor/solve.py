#!/usr/bin/env python3
import socket
import sys


HOST = sys.argv[1] if len(sys.argv) > 1 else "154.57.164.66"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 32353
SAMPLES = int(sys.argv[3]) if len(sys.argv) > 3 else 5000


class Protocol:
    def __init__(self, sock):
        self.sock = sock
        self.buffer = b""

    def recvuntil(self, marker):
        while marker not in self.buffer:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise EOFError(self.buffer)
            self.buffer += chunk
        end = self.buffer.index(marker) + len(marker)
        data, self.buffer = self.buffer[:end], self.buffer[end:]
        return data


def choose(io, option, prompt=None, value=None):
    io.recvuntil(b"Your option: ")
    io.sock.sendall(str(option).encode() + b"\n")
    if prompt is not None:
        io.recvuntil(prompt)
        io.sock.sendall(value + b"\n")
    raw = io.recvuntil(b"\n")
    line = raw.splitlines()[-1]
    try:
        return bytes.fromhex(line.decode())
    except ValueError:
        raise RuntimeError(f"unexpected server response: {raw!r}")


def collect_batch(io, payload, count):
    """Pipeline requests to avoid paying one network round trip per sample."""
    io.recvuntil(b"Your option: ")
    io.sock.sendall(payload * count)
    samples = []
    for i in range(count):
        if payload.startswith(b"2\n"):
            io.recvuntil(b"Enter plaintext: ")
        raw = io.recvuntil(b"\n")
        try:
            samples.append(bytes.fromhex(raw.strip().decode()))
        except ValueError:
            raise RuntimeError(f"unexpected server response: {raw!r}")
        if i + 1 < count:
            io.recvuntil(b"Your option: ")
    return samples


def missing_values(samples):
    width = len(samples[0])
    result = bytearray()
    for i in range(width):
        seen = {sample[i] for sample in samples}
        missing = set(range(256)) - seen
        if len(missing) != 1:
            raise RuntimeError(
                f"byte {i}: expected one missing value, got {len(missing)}; "
                "increase the sample count"
            )
        result.append(missing.pop())
    return bytes(result)


def main():
    with socket.create_connection((HOST, PORT)) as sock:
        io = Protocol(sock)
        flags = collect_batch(io, b"1\n", SAMPLES)
        width = len(flags[0])
        if any(len(x) != width for x in flags):
            raise RuntimeError("flag ciphertext lengths changed")

        zeros = b"00" * width
        known = collect_batch(io, b"2\n" + zeros + b"\n", SAMPLES)

    masked_flag = missing_values(flags)  # AES stream XOR flag
    stream = missing_values(known)       # AES stream XOR zeroes
    flag = bytes(a ^ b for a, b in zip(masked_flag, stream))
    print(flag.decode())


if __name__ == "__main__":
    main()
