#!/usr/bin/env python3
import sys
sys.path.insert(0, "vendor")
from itertools import combinations
from fpylll import IntegerMatrix, LLL, CVP, BKZ, GSO, FPLLL, Enumeration, EvaluatorStrategy
from lattice_test import add, mul, scale as pscale, linear


def recover_errors(p, n, k, ts, hs, tail_weight=16):
    B = 1 << (n-k)
    nv = len(ts)
    bases = [h*B for h in hs]
    zs = [linear(nv, bases[i], {i:1}) for i in range(nv)]
    equations = []
    zero = (0,)*nv
    for i,j,l in combinations(range(nv),3):
        # (tl-ti) zl (zi-zj) - (tj-ti) zj (zi-zl) = 0 mod p
        f = add(
            pscale(mul(zs[l], add(zs[i], pscale(zs[j],-1))), ts[l]-ts[i]),
            pscale(mul(zs[j], add(zs[i], pscale(zs[l],-1))), -(ts[j]-ts[i])))
        C = f.get(zero,0) % p
        A=[]
        for v in range(nv):
            u=[0]*nv; u[v]=1
            A.append(f.get(tuple(u),0) % p)
        equations.append((C,A))

    m=len(equations); dim=m+nv
    S=tail_weight*B
    M=IntegerMatrix(dim,dim)
    for i in range(m):
        M[i,i]=p
    for v in range(nv):
        for i,(_,A) in enumerate(equations):
            M[m+v,i]=A[v]
        M[m+v,m+v]=S
    target=[(-C)%p for C,_ in equations]+[S*(B//2)]*nv
    print('linear CVP dimension',dim,flush=True)
    LLL.reduction(M,delta=.99,eta=.501)
    BKZ.reduction(M, BKZ.Param(block_size=40, max_loops=8), float_type='mpfr', precision=256)
    close=list(CVP.closest_vector(M,target,method='proved'))
    es=[close[m+v]//S for v in range(nv)]
    dirs=[]
    for rr in range(dim):
        d=[int(M[rr,m+v])//S for v in range(nv)]
        if any(d) and all(abs(x)<2*B for x in d):
            dirs.append(d)
    print('tangent directions',[(max(abs(x) for x in d).bit_length()) for d in dirs[:6]],flush=True)
    def on_curve(ee):
        zz=[hs[i]*B+ee[i] for i in range(nv)]
        for i in range(2,nv):
            if (i*zz[i]*(zz[0]-zz[1])-zz[1]*(zz[0]-zz[i]))%p: return False
        return True
    for da,db in combinations(dirs[:8],2):
        for ca in range(-128,129):
            for cb in range(-128,129):
                ee=[es[v]+ca*da[v]+cb*db[v] for v in range(nv)]
                if all(0<=x<B for x in ee) and on_curve(ee): return ee
    if all(0 <= e < B for e in es) and verify(p,ts,hs,n,k,es)[2]: return es
    # Kannan embedding turns this bounded-distance CVP instance into SVP.
    E=IntegerMatrix(dim+1,dim+1)
    for i in range(dim):
        for j in range(dim): E[i,j]=M[i,j]
    for j,x in enumerate(target): E[dim,j]=x
    embed=32*B*B
    E[dim,dim]=embed
    LLL.reduction(E,delta=.999,eta=.501)
    BKZ.reduction(E, BKZ.Param(block_size=40, max_loops=8), float_type='mpfr', precision=256)
    gso=GSO.Mat(E,float_type='mpfr');gso.update_gso()
    enum=Enumeration(gso,nr_solutions=10000,strategy=EvaluatorStrategy.BEST_N_SOLUTIONS)
    sols=enum.enumerate(0,dim+1,4*gso.get_r(0,0),0)
    print('enumerated',len(sols),'nodes',enum.get_nodes(),flush=True)
    for _,co in sols:
        row=[sum(int(round(co[i]))*int(E[i,j]) for i in range(dim+1)) for j in range(dim+1)]
        if abs(row[-1]) != embed: continue
        sg=1 if row[-1]==-embed else -1
        cc=[target[j]+sg*row[j] for j in range(dim)]
        ee=[cc[m+v]//S for v in range(nv)]
        if all(0<=x<B for x in ee) and verify(p,ts,hs,n,k,ee)[2]: return ee
    for rr in range(dim+1):
        row=[int(E[rr,j]) for j in range(dim+1)]
        if abs(row[-1]) != embed:
            continue
        # row = lattice_point - target (or its negative)
        sg = 1 if row[-1] == -embed else -1
        close=[target[j] + sg*row[j] for j in range(dim)]
        es=[close[m+v]//S for v in range(nv)]
        if all(0 <= e < B for e in es):
            return es
    return None


def recover_lifted(p,n,k,ts,hs):
    B=1<<(n-k); nv=len(ts); bases=[h*B for h in hs]
    zs=[linear(nv,bases[i],{i:1}) for i in range(nv)]
    pairs=list(combinations(range(nv),2)); variables=[('e',i) for i in range(nv)]+[('q',ij) for ij in pairs]
    eq=[]; zero=(0,)*nv
    for i,j,l in combinations(range(nv),3):
        f=add(pscale(mul(zs[l],add(zs[i],pscale(zs[j],-1))),ts[l]-ts[i]),
              pscale(mul(zs[j],add(zs[i],pscale(zs[l],-1))),-(ts[j]-ts[i])))
        coeff=[]
        for typ,idx in variables:
            m=[0]*nv
            if typ=='e':m[idx]=1
            else:m[idx[0]]=m[idx[1]]=1
            coeff.append(f.get(tuple(m),0)%p)
        eq.append((f.get(zero,0)%p,coeff))
    piv={}; indep=[]
    for C,A in eq:
        vec={i:x%p for i,x in enumerate(A) if x%p}
        while vec:
            j=min(vec)
            if j not in piv:
                inv=pow(vec[j],-1,p); vec={i:x*inv%p for i,x in vec.items() if x*inv%p}
                piv[j]=vec;indep.append((C,A));break
            q=vec[j]
            for i,x in piv[j].items():
                vec[i]=(vec.get(i,0)-q*x)%p
                if not vec[i]:del vec[i]
    eq=indep
    m=len(eq); r=len(variables); dim=m+r; W=B*B
    M=IntegerMatrix(dim,dim)
    for i in range(m):M[i,i]=p*W
    tail_scales=[]; tail_targets=[]
    for x,(typ,_) in enumerate(variables):
        for i,(_,A) in enumerate(eq):M[m+x,i]=A[x]*W
        S=B if typ=='e' else 1
        bound=B if typ=='e' else B*B
        M[m+x,m+x]=S;tail_scales.append(S);tail_targets.append(S*(bound//2))
    target=[((-C)%p)*W for C,_ in eq]+tail_targets
    print('lifted CVP dimension',dim,flush=True)
    LLL.reduction(M,delta=.99,eta=.501,method='proved',float_type='mpfr',precision=768)
    close=list(CVP.closest_vector(M,target,method='fast'))
    vals=[close[m+x]//tail_scales[x] for x in range(r)]
    es=vals[:nv]; qs=vals[nv:]
    if all(0<=e<B for e in es) and all(q==es[i]*es[j] for q,(i,j) in zip(qs,pairs)):
        return es
    return None


def verify(p,ts,hs,n,k,es):
    B=1<<(n-k)
    zs=[h*B+e for h,e in zip(hs,es)]
    den=(zs[0]-zs[1])%p
    u=((ts[1]*zs[1]-ts[0]*zs[0])*pow(den,-1,p))%p
    v=zs[0]*(u+ts[0])%p
    return u,v,all(v*pow(u+t,-1,p)%p==z for t,z in zip(ts,zs))


if __name__=='__main__':
    import secrets
    import sympy as sp
    n=512;k=58*n//100;p=int(sp.randprime(1<<(n-1),1<<n))
    u0=secrets.randbelow(p);v0=secrets.randbelow(p-1)+1;ts=list(range(8))
    vals=[v0*pow(u0+t,-1,p)%p for t in ts]
    hs=[z>>(n-k) for z in vals]
    es=recover_errors(p,n,k,ts,hs)
    print(es)
    print('errors right',es==[z&((1<<(n-k))-1) for z in vals] if es else False)
    print(verify(p,ts,hs,n,k,es) if es else None)
