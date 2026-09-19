#!/usr/bin/env python3
import sys
sys.path.insert(0, "vendor")
from itertools import product
from math import isqrt
from fpylll import IntegerMatrix, LLL
import sympy as sp
from lattice_test import add, mul, scale, linear


def monomial(nv, exps, coeff=1):
    return {tuple(exps): coeff}


def centered_poly(f, p, lead):
    inv = pow(f[lead] % p, -1, p)
    out = {}
    for m, c in f.items():
        v = c * inv % p
        if v > p // 2:
            v -= p
        if v:
            out[m] = v
    return out


def build_rows(p, n, k, hs, box=2):
    B = 1 << (n-k)
    nv = 4
    a = [h*B for h in hs[:nv]]
    z = [linear(nv, a[i], {i: 1}) for i in range(nv)]
    fs = []
    for i in (2, 3):
        f = add(scale(mul(z[i], add(z[0], scale(z[1], -1))), i),
                scale(mul(z[1], add(z[0], scale(z[i], -1))), -1))
        lead = tuple(1 if j in (0, i) else 0 for j in range(nv))
        fs.append(centered_poly(f, p, lead))

    polys = []
    max_s = box
    for r in product(range(box+1), repeat=nv):
        # Maximize use of f0,f1 while preserving their selected leading monomial.
        best = (0, 0)
        for s0 in range(min(r[2], r[0])+1):
            for s1 in range(min(r[3], r[0]-s0)+1):
                if s0+s1 > sum(best):
                    best = (s0, s1)
        s0, s1 = best
        rem = list(r)
        rem[0] -= s0+s1; rem[2] -= s0; rem[3] -= s1
        g = monomial(nv, rem, p ** (max_s-s0-s1))
        for _ in range(s0): g = mul(g, fs[0])
        for _ in range(s1): g = mul(g, fs[1])
        polys.append(g)

    terms = sorted({m for g in polys for m in g}, key=lambda m:(sum(m),m))
    ti = {m:i for i,m in enumerate(terms)}
    M = IntegerMatrix(len(polys), len(terms))
    for i,g in enumerate(polys):
        for m,c in g.items():
            M[i,ti[m]] = c * B**sum(m)
    print('basis',len(polys),'x',len(terms),'maxdeg',max(map(sum,terms)), flush=True)
    LLL.reduction(M, delta=.99, eta=.501)
    rows=[]
    limit = p**max_s // isqrt(len(terms))
    for i in range(len(polys)):
        vec=[int(M[i,j]) for j in range(len(terms))]
        norm2=sum(v*v for v in vec)
        if norm2 >= limit*limit:
            continue
        g={}
        for m,j in ti.items():
            if vec[j]:
                assert vec[j] % B**sum(m) == 0
                g[m]=vec[j]//B**sum(m)
        rows.append(g)
    print('short exact candidates',len(rows), flush=True)
    return rows


def groebner_mod(rows, q, nv=4, take=12):
    xs=sp.symbols('x0:'+str(nv))
    expr=[]
    for g in rows[:take]:
        expr.append(sum((c%q)*sp.prod(xs[i]**m[i] for i in range(nv)) for m,c in g.items()))
    G=sp.groebner(expr,*xs,modulus=q,order='grevlex')
    print('gb',q,len(G.polys))
    for poly in G.polys:
        ex=poly.as_expr()
        pp=sp.Poly(ex,*xs,modulus=q)
        if pp.total_degree()==1:
            print(ex)
    return G


if __name__=='__main__':
    from secrets import randbelow
    n=512; k=58*n//100
    p=int(sp.randprime(1<<(n-1),1<<n)); u=randbelow(p); v=randbelow(p-1)+1
    hs=[(v*pow(u+i,-1,p)%p)>>(n-k) for i in range(4)]
    rows=build_rows(p,n,k,hs)
    groebner_mod(rows,101,take=min(16,len(rows)))
