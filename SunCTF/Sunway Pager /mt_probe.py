import random
import re
import socket

HOST = "pager.chal.sunwaycybersecurityclub.org"
PORT = 3838

def recv_prompt(s):
    data = b""
    while not data.endswith(b"command> "):
        chunk = s.recv(8192)
        if not chunk:
            raise EOFError(data)
        data += chunk
    return data

def undo_right(y, shift):
    x = 0
    for pos in range(32 - shift, -shift, -shift):
        width = min(shift, 32 - max(pos, 0))
        p = max(pos, 0)
        mask = ((1 << width) - 1) << p
        x |= (y ^ (x >> shift)) & mask
    return x & 0xffffffff

def undo_left(y, shift, mask):
    x = 0
    for pos in range(0, 32, shift):
        m = ((1 << min(shift, 32 - pos)) - 1) << pos
        x |= (y ^ ((x << shift) & mask)) & m
    return x & 0xffffffff

def untemper(y):
    y = undo_right(y, 18)
    y = undo_left(y, 15, 0xefc60000)
    y = undo_left(y, 7, 0x9d2c5680)
    y = undo_right(y, 11)
    return y

def clone_and_check(blob, endian):
    words = [int.from_bytes(blob[i:i+4], endian) for i in range(0, len(blob), 4)]
    state = tuple(untemper(x) for x in words[:624]) + (624,)
    r = random.Random()
    r.setstate((3, state, None))
    predicted = b"".join(r.getrandbits(32).to_bytes(4, endian) for _ in range(len(words)-624))
    actual = blob[624*4:]
    print(endian, "held-out match:", predicted == actual)
    if predicted != actual:
        print(" predicted", predicted[:16].hex())
        print(" actual   ", actual[:16].hex())

s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(60)
recv_prompt(s)
s.sendall(b"GETFLAG\n")
flag_reply = recv_prompt(s)
flag_ct = bytes.fromhex(re.search(rb"([0-9a-f]{60,})", flag_reply).group(1).decode())
print("flag", len(flag_ct), flag_ct.hex())

chunks = []
for i in range(11):
    s.sendall(("ENC hex:" + "00" * 256 + "\n").encode())
    reply = recv_prompt(s)
    matches = re.findall(rb"(?m)^([0-9a-f]{512})\r?$", reply)
    if not matches:
        raise ValueError(repr(reply))
    chunks.append(bytes.fromhex(matches[-1].decode()))
    print("query", i + 1, chunks[-1][:8].hex())
s.close()

blob = b"".join(chunks)
clone_and_check(blob, "little")
clone_and_check(blob, "big")
