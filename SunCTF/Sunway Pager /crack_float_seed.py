import math, random

t0=1788680513.0035118
t1=1788680513.263055
needle=bytes.fromhex("7356ddc9675baf312017dcc244d28895")
f=t0
n=0
while f <= t1:
    for mode in range(3):
        r=random.Random(f)
        if mode == 0:
            got=bytes(r.getrandbits(8) for _ in range(38+len(needle)))[38:]
        elif mode == 1:
            r.randbytes(38); got=r.randbytes(256)[:len(needle)]
        else:
            got=r.randbytes(38+len(needle))[38:]
        if got == needle:
            print("MATCH",repr(f),mode)
    f=math.nextafter(f, math.inf)
    n += 1
print("tested",n)
