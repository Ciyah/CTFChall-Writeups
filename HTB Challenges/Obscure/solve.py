#!/usr/bin/env python3
"""Decode the commands and responses exchanged with support.php."""

import base64
import re
import subprocess
import zlib
from pathlib import Path


PCAP = Path("Obscure/19-05-21_22532255.pcap")
KEY = b"80e32263"
START = b"6f8af44abea0"
END = b"351039f4a7b5"


def xor(data: bytes) -> bytes:
    return bytes(byte ^ KEY[i % len(KEY)] for i, byte in enumerate(data))


def decode_message(body: bytes) -> bytes:
    encoded = re.search(START + b"(.+?)" + END, body).group(1)
    encoded += b"=" * (-len(encoded) % 4)
    return zlib.decompress(xor(base64.b64decode(encoded)))


def packets(display_filter: str):
    output = subprocess.check_output(
        [
            "tshark", "-r", str(PCAP), "-Y", display_filter,
            "-T", "fields", "-E", "separator=|",
            "-e", "frame.number", "-e", "http.file_data",
        ],
        text=True,
        stderr=subprocess.DEVNULL,
    )
    for line in output.splitlines():
        frame, body_hex = line.split("|", 1)
        yield frame, bytes.fromhex(body_hex)


requests = list(packets('http.request.method == "POST"'))
streams = "1,23,24,25"
responses = list(packets(f"http.response && tcp.stream in {{{streams}}}"))

for (request_frame, request), (response_frame, response) in zip(requests, responses):
    command = decode_message(request).decode(errors="replace")
    result = decode_message(response)
    print(f"request frame {request_frame}: {command}")
    print(f"response frame {response_frame}: {result.decode(errors='replace')}")

# The last command's output is itself Base64-encoded file data.
database_b64 = decode_message(responses[-1][1]).strip()
Path("pwdb.kdbx").write_bytes(base64.b64decode(database_b64))
print("wrote pwdb.kdbx")
