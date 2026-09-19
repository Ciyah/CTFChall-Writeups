import random

t0 = 1788680513.1035118
t1 = 1788680513.163055
flag_len = 38
observed = bytes.fromhex(
    "7356ddc9675baf312017dcc244d288950d0ed42f8b41a6c7a42a5b1ab9ce594e"
    "5824e54a63d9c5f992615d03bb91be446efa16de5cf05e6bc83ab61b2f9cafa8"
    "e85e4903c2d67a78d6f587c1952d26c06cfc1a2be8e5980c766686304254d44d"
    "8b18ea6fc7831b887ddf254324f656245685d033c704cbc02f36393fa44c184da"
    "81037e11bd8f48bda8c5435d9c27a18b20023997f07a30c9bc0ef48322582c70"
    "03d425516339f8f89c15b0bc4d134ea33b57f8274dbb9069142e9a56d7039136"
    "b5acb8784a7645103d8dbcb15b51f683d3fd182c829902b37508876d4786c7a9"
    "fa35bd1d854b40edac1ee18aef10d5c1a229a080837c443791391492cb349ab"
)

def check(seed):
    r = random.Random(seed)
    a = bytes(r.getrandbits(8) for _ in range(flag_len + 8))
    if a[flag_len:] == observed[:8]:
        return "getrandbits8"
    r = random.Random(seed)
    a = bytes(r.randrange(256) for _ in range(flag_len + 8))
    if a[flag_len:] == observed[:8]:
        return "randrange256"
    r = random.Random(seed)
    r.randbytes(flag_len)
    if r.randbytes(len(observed)) == observed:
        return "randbytes-calls"
    r = random.Random(seed)
    if r.randbytes(flag_len + len(observed))[flag_len:] == observed:
        return "randbytes-stream"

candidates = set()
for delta in range(-3, 4):
    candidates.add(int(t0) + delta)
for scale in (1_000, 1_000_000):
    lo = int((t0 - 0.5) * scale)
    hi = int((t1 + 0.5) * scale)
    candidates.update(range(lo, hi + 1))

print("testing", len(candidates), "seeds")
for seed in candidates:
    kind = check(seed)
    if kind:
        print("MATCH", seed, kind)
