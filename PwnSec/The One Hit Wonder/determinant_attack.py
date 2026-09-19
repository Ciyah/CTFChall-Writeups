#!/usr/bin/env python3
import sys
sys.path.insert(0,'vendor')
from itertools import combinations, permutations, product
from math import prod, isqrt
from fpylll import IntegerMatrix, LLL
import sympy as sp
import numpy as np
from scipy.optimize import least_squares
import mpmath as mp
from lattice_test import add,mul,scale


def parity(perm):
    return -1 if sum(perm[i]>perm[j] for i in range(len(perm)) for j in range(i+1,len(perm)))&1 else 1


def det_poly(rows,nv):
    out={}
    for pm in permutations(range(len(rows))):
        g={(0,)*nv:parity(pm)}
        for i,j in enumerate(pm):g=mul(g,rows[i][j])
        out=add(out,g)
    return out


def fundamental(indices,q,ts,bases,p,nv,cache):
    key=(tuple(indices),q)
    if key in cache:return cache[key]
    if q==0:
        m=[0]*nv;m[indices[0]]=1
        return {tuple(m):1}
    rows=[]
    for idx in indices:
        xb={(0,)*nv:bases[idx]};m=[0]*nv;m[idx]=1;xb[tuple(m)]=1
        row=[]
        for power in range(q,-1,-1):row.append(scale(xb,ts[idx]**power))
        for power in range(q-1,-1,-1):row.append({(0,)*nv:ts[idx]**power})
        rows.append(row)
    f=det_poly(rows,nv); modulus=p**q
    lead=[0]*nv
    for i in sorted(indices)[-(q+1):]:lead[i]=1
    lc=f[tuple(lead)]%modulus;inv=pow(lc,-1,modulus)
    f={m:(c*inv)%modulus for m,c in f.items() if (c*inv)%modulus}
    cache[key]=f
    return f


def compositions(total,length):
    if length==1:yield (total,);return
    for x in range(total+1):
        for rest in compositions(total-x,length-1):yield (x,)+rest


def witness(S,nv):
    S=set(S);s=len(S);univ=set(range(nv))
    for k in range(s-1,-1,-1):
        L=s-k
        for qs in compositions(k,L):
            def rec(j,left,groups,tops):
                if j==L:
                    if tops==S:return groups
                    return None
                size=2*qs[j]+1
                for A in combinations(sorted(left),size):
                    top=set(sorted(A)[-(qs[j]+1):])
                    if not top<=S or tops&top:continue
                    z=rec(j+1,left-set(A),groups+[A],tops|top)
                    if z is not None:return z
                return None
            groups=rec(0,univ,[],set())
            if groups is not None:return k,qs,groups
    raise ValueError(S)


def build(p,n,k,ts,hs,d=3):
    nv=len(ts);B=1<<(n-k);bases=[h*B for h in hs];zero=(0,)*nv;cache={}
    mons=[S for s in range(d+2) for S in combinations(range(nv),s)]
    shifts=[]
    for S in mons:
        if not S:shifts.append({zero:p**d});continue
        kk,qs,groups=witness(S,nv)
        g={zero:p**(d-kk)}
        for q,A in zip(qs,groups):g=mul(g,fundamental(A,q,ts,bases,p,nv,cache))
        shifts.append(g)
    termmons=[]
    for S in mons:
        m=[0]*nv
        for i in S:m[i]=1
        termmons.append(tuple(m))
    ti={m:i for i,m in enumerate(termmons)};w=len(mons)
    M=IntegerMatrix(w,w)
    for i,g in enumerate(shifts):
        for m,c in g.items():M[i,ti[m]]=c*B**sum(m)
    print('determinant lattice',w,'d',d,flush=True)
    LLL.reduction(M,delta=.99,eta=.501)
    limit=p**d//isqrt(w);rows=[]
    for i in range(w):
        vec=[int(M[i,j]) for j in range(w)]
        if sum(x*x for x in vec)>=limit*limit:continue
        rows.append({m:vec[j]//B**sum(m) for m,j in ti.items() if vec[j]})
    print('exact rows',len(rows),flush=True)
    print('degrees',[max(map(sum,g)) for g in rows[:12]],flush=True)
    return rows,B


def roots_mod(rows,q,nv,take=None):
    xs=sp.symbols('x0:'+str(nv));expr=[]
    for g in rows[:take]:expr.append(sum((c%q)*prod(xs[i] for i,e in enumerate(m) if e) for m,c in g.items()))
    G=sp.groebner(expr,*xs,modulus=q,order='grevlex')
    vals={}
    for po in G.polys:
        P=sp.Poly(po,*xs,modulus=q)
        terms=P.terms()
        if len(terms)==2 and P.total_degree()==1:
            const=0;var=None;coef=None
            for m,c in terms:
                if sum(m)==0:const=int(c)%q
                else:var=m.index(1);coef=int(c)%q
            vals[var]=(-const*pow(coef,-1,q))%q
    return vals


def numeric_root(rows,B,nv,tries=12):
    use=rows[:max(nv,min(len(rows),32))]
    packed=[]
    for g in use:
        cc=[(m,c*B**sum(m)) for m,c in g.items()]
        norm=max(abs(c) for _,c in cc)
        packed.append([(m,float(c/norm)) for m,c in cc])
    def fun(x):
        return np.array([sum(c*prod(x[i] for i,e in enumerate(m) if e) for m,c in g) for g in packed])
    def jac(x):
        J=np.zeros((len(packed),nv))
        for r,g in enumerate(packed):
            for m,c in g:
                ids=[i for i,e in enumerate(m) if e]
                for i in ids:J[r,i]+=c*prod(x[j] for j in ids if j!=i)
        return J
    starts=[np.full(nv,.5)]+[np.random.default_rng(i).random(nv) for i in range(tries)]
    sols=[]
    for st in starts:
        z=least_squares(fun,st,jac=jac,bounds=(0,1),xtol=1e-14,ftol=1e-14,gtol=1e-14,max_nfev=3000)
        if np.linalg.norm(fun(z.x))<1e-7:sols.append(z.x)
    print('numeric candidates',len(sols),flush=True)
    mp.mp.dps=max(100,int(B.bit_length()*.32)+40)
    exact=rows[:nv]
    funcs=[]
    for g in exact:
        cc=[(m,mp.mpf(c)*mp.mpf(B)**sum(m)) for m,c in g.items()]
        norm=max(abs(c) for _,c in cc)
        funcs.append(lambda *x,cc=cc,norm=norm:sum(c*prod(x[i] for i,e in enumerate(m) if e) for m,c in cc)/norm)
    for sol in sols:
        try:
            rr=mp.findroot(tuple(funcs),tuple(map(mp.mpf,sol)),tol=mp.mpf(2)**(-B.bit_length()-20),maxsteps=100,solver='mdnewton')
            es=[int(mp.nint(x*B)) for x in rr]
            if all(0<=e<B for e in es):return es
        except (ValueError,ZeroDivisionError):pass
    return None


if __name__=='__main__':
    import secrets
    n=256;k=58*n//100;p=int(sp.randprime(1<<(n-1),1<<n));u=secrets.randbelow(p);v=secrets.randbelow(p-1)+1
    ts=list(range(8));zz=[v*pow(u+t,-1,p)%p for t in ts];hs=[z>>(n-k) for z in zz]
    for d in (2,3):
        rows,B=build(p,n,k,ts,hs,d)
        es=numeric_root(rows,B,8)
        print('root?',es==[z&(B-1) for z in zz] if es else None)
