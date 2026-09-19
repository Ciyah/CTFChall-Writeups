import random

t0 = 1788680513.1035118
t1 = 1788680513.163055
needle = bytes.fromhex("7356ddc9675baf312017dcc244d28895")

seeds = set(range(int(t0) - 5, int(t1) + 6))
seeds.update(range(int((t0 - 2) * 1000), int((t1 + 2) * 1000) + 1))
print("seeds", len(seeds))
for seed in seeds:
    r = random.Random(seed)
    stream = bytes(r.getrandbits(8) for _ in range(4096))
    p = stream.find(needle)
    if p >= 0:
        print("MATCH getrandbits8", seed, p)

    r = random.Random(seed)
    stream = bytes(r.randrange(256) for _ in range(4096))
    p = stream.find(needle)
    if p >= 0:
        print("MATCH randrange", seed, p)

    r = random.Random(seed)
    stream = r.randbytes(4096)
    p = stream.find(needle)
    if p >= 0:
        print("MATCH randbytes-stream", seed, p)
