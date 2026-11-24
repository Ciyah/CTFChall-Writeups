#!/usr/bin/env python3
"""
Captured Whispers — Curtin CTF 2026
Category: IoT | Points: 260

The UART transcript (decoded from Chall.sal at 4800 baud, 7N1 inverted)
contained this line from /etc/motd:

    zJLgHX&fTX'sHI+xzZ\\xSV_d}tLKSi

XOR with 0x1E yields a Base64-encoded flag body.
"""

import base64

MOTD_LINE = rb"zJLgHX&fTX'sHI+xzZ\xSV_d}tLKSi"
XOR_KEY = 0x1E

encoded = bytes(b ^ XOR_KEY for b in MOTD_LINE)

# Restore padding stripped during transmission
padded = encoded + b"=" * (-len(encoded) % 4)

body = base64.b64decode(padded, validate=True).decode("ascii")
flag = f"CURTIN_CTF{{{body}}}"

print(flag)
