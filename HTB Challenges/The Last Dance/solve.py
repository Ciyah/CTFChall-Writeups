#!/usr/bin/env python3
from pathlib import Path


KNOWN_MESSAGE = (
    b"Our counter agencies have intercepted your messages and a lot "
    b"of your agent's identities have been exposed. In a matter of "
    b"days all of them will be captured"
)


def xor_bytes(*values: bytes) -> bytes:
    return bytes(map(lambda parts: parts[0] ^ parts[1] ^ parts[2], zip(*values)))


_, message_hex, flag_hex = Path("out.txt").read_text().splitlines()
message_ciphertext = bytes.fromhex(message_hex)
flag_ciphertext = bytes.fromhex(flag_hex)

# C_message = message XOR keystream, and C_flag = flag XOR keystream.
# Therefore C_message XOR message XOR C_flag = flag.
flag = xor_bytes(message_ciphertext, KNOWN_MESSAGE, flag_ciphertext)
print(flag.decode())
