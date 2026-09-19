import numpy as np

t0=1788680513.1035118; t1=1788680513.163055
needle=bytes.fromhex("7356ddc9675baf312017dcc244d28895")
seeds=set(range(int(t0)-5,int(t1)+6))
for scale in (1000, 1_000_000):
    seeds.update(range(int((t0-.5)*scale),int((t1+.5)*scale)+1))
print("testing",len(seeds))
for seed in seeds:
    for kind in ("pcg-int","pcg-bytes","mt-int","mt-bytes"):
        try:
            if kind.startswith("pcg"):
                r=np.random.default_rng(seed)
                if kind.endswith("int"):
                    x=r.integers(0,256,size=38+len(needle),dtype=np.uint8).tobytes()[38:]
                else:
                    x=r.bytes(38+len(needle))[38:]
            else:
                r=np.random.RandomState(seed & 0xffffffff)
                if kind.endswith("int"):
                    x=r.randint(0,256,size=38+len(needle),dtype=np.uint8).tobytes()[38:]
                else:
                    x=r.bytes(38+len(needle))[38:]
            if x==needle: print("MATCH",seed,kind)
        except Exception: pass
