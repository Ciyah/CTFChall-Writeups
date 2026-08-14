#!/usr/bin/env python3
import json
import sys

from fast_recover import N, division_tail, parse_groups

# Expression (A, B, C, t) represents (A*d + B*n + C) / 2^t.
def combine(left, right, subtract=False):
    a1,b1,c1,t1=left; a2,b2,c2,t2=right
    t=max(t1,t2); f1=1<<(t-t1); f2=1<<(t-t2); sign=-1 if subtract else 1
    return (a1*f1+sign*a2*f2,b1*f1+sign*b2*f2,c1*f1+sign*c2*f2,t)


def feasible(residue, precision, limit, lower=0):
    modulus=1<<precision
    first=lower+((residue-lower)%modulus)
    return first<limit


def impose(states, index, parity):
    output=[]
    for state in states:
        d,n,dp,np,u,v,x1,x2,side=state
        a,b,c,shift=state[index]
        needed=shift+1
        # Every expression is exclusively in d or n (or constant).
        if a:
            target_precision=min(needed,512)
            candidates=[d]
            for bit in range(dp,target_precision):
                candidates=[r+(choice<<bit) for r in candidates for choice in (0,1)]
            for rd in candidates:
                if (a*rd+b*n+c-(parity<<shift))%(1<<needed)==0 and feasible(rd,target_precision,N*N,1):
                    values=list(state); values[0]=rd; values[2]=target_precision
                    output.append(tuple(values))
        elif b:
            target_precision=min(needed,256)
            candidates=[n]
            for bit in range(np,target_precision):
                candidates=[r+(choice<<bit) for r in candidates for choice in (0,1)]
            for rn in candidates:
                if (a*d+b*rn+c-(parity<<shift))%(1<<needed)==0 and feasible(rn,target_precision,N):
                    values=list(state); values[1]=rn; values[3]=target_precision
                    output.append(tuple(values))
        elif (c-(parity<<shift))%(1<<needed)==0:
            output.append(state)
    return output


def evaluate(expr,d,n):
    a,b,c,t=expr; value=a*d+b*n+c
    return value//(1<<t) if value%(1<<t)==0 else None

def expression_bounds(expr):
    a,b,c,t=expr
    low=c+(a if a>0 else a*(N*N-1))+(0 if b>0 else b*(N-1))
    high=c+(a*(N*N-1) if a>0 else a)+(b*(N-1) if b>0 else 0)
    return low//(1<<t),high//(1<<t)


def recover(sample):
    s=int(sample['s'],0)
    groups=parse_groups(division_tail(sample['trace']))
    # d = masked denominator, n = reduced numerator passed to binary division.
    states=[(0,0,0,0,(1,0,0,0),(0,0,N,0),(0,1,0,0),(0,0,0,0),True)]
    for gi,parities in enumerate(groups):
        advanced=[]
        for state in states:
            side_u=True if gi==0 else state[8]
            partial=[state]
            for coefficient_parity in parities:
                vi=4 if side_u else 5; xi=6 if side_u else 7
                partial=impose(partial,vi,0)
                partial=impose(partial,xi,coefficient_parity)
                shifted=[]
                for item in partial:
                    values=list(item)
                    a,b,c,t=values[vi]; values[vi]=(a,b,c,t+1)
                    a,b,c,t=values[xi]
                    values[xi]=(a,b,c+coefficient_parity*N*(1<<t),t+1)
                    shifted.append(tuple(values))
                partial=shifted
            partial=impose(impose(partial,4,1),5,1)
            if gi==len(groups)-1:
                advanced.extend(partial); continue
            for item in partial:
                for branch_u in (True,False):
                    values=list(item)
                    diff=combine(item[4],item[5],True)
                    low,high=expression_bounds(diff)
                    if branch_u and high<0: continue
                    if not branch_u and low>=0: continue
                    if branch_u:
                        values[4]=diff
                        values[6]=combine(item[6],item[7],True)
                    else:
                        values[5]=combine(item[5],item[4],True)
                        values[7]=combine(item[7],item[6],True)
                    values[8]=branch_u; advanced.append(tuple(values))
        states=list(set(advanced))
        print(gi,len(states),max((x[2] for x in states),default=0),max((x[3] for x in states),default=0),flush=True)
        if not states: break

    answers=set()
    for d,n,dp,np,u,v,x1,x2,side in states:
        if dp<512 or np<256 or not (0<d<N*N and 0<=n<N): continue
        if (s*d-n)%N: continue
        uu,vv=evaluate(u,d,n),evaluate(v,d,n)
        if uu is not None and vv is not None and (uu==1 or vv==1): answers.add(d)
    return answers


if __name__=='__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else "sample.json"
    with open(path,encoding='ascii') as source:
        print([hex(x) for x in recover(json.load(source))])
