#!/usr/bin/env python3
import sys
sys.path.insert(0, "vendor")
from itertools import combinations, product
from fpylll import IntegerMatrix, LLL


def add(a, b):
    out = a.copy()
    for m, c in b.items():
        out[m] = out.get(m, 0) + c
        if not out[m]:
            del out[m]
    return out


def mul(a, b):
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(x + y for x, y in zip(ma, mb))
            out[m] = out.get(m, 0) + ca * cb
    return out


def scale(a, c):
    return {m: c * v for m, v in a.items()}


def linear(nvars, const, terms):
    z = {(0,) * nvars: const}
    for idx, coeff in terms.items():
        m = [0] * nvars
        m[idx] = 1
        z[tuple(m)] = coeff
    return z


def solve_errors(p, n, k, hs, depth=2):
    B = 1 << (n - k)
    bases = [h * B for h in hs]
    nv = len(bases)
    zs = [linear(nv, a, {i: 1}) for i, a in enumerate(bases)]
    fs = []
    for i in range(2, nv):
        # i*z_i*(z_0-z_1) - z_1*(z_0-z_i) == 0 (mod p)
        f = add(scale(mul(zs[i], add(zs[0], scale(zs[1], -1))), i),
                scale(mul(zs[1], add(zs[0], scale(zs[i], -1))), -1))
        fs.append(f)

    base_relations = []
    for w in range(1, depth + 1):
        for inds in combinations(range(len(fs)), w):
            g = {(0,) * nv: 1}
            for idx in inds:
                g = mul(g, fs[idx])
            base_relations.append((g, w))

    terms = sorted(product(range(depth + 1), repeat=nv), key=lambda m: (sum(m), m))
    ti = {m: i for i, m in enumerate(terms)}
    # Every monomial shift whose support stays inside the phase-d term set is
    # a free congruence.  Keep a maximum-rank set, preferring weight d rows.
    candidates = []
    for g, weight in reversed(base_relations):
        for shift in terms:
            sg = {}
            okay = True
            for mon, coeff in g.items():
                sm = tuple(a + b for a, b in zip(mon, shift))
                if sm not in ti:
                    okay = False
                    break
                sg[sm] = coeff
            if okay:
                candidates.append((sg, weight))
    q = 2147483647
    pivots = {}
    relations = []
    for g, weight in candidates:
        vec = {ti[m]: c % q for m, c in g.items() if c % q}
        while vec:
            pivot = min(vec)
            if pivot not in pivots:
                inv = pow(vec[pivot], -1, q)
                vec = {j: c * inv % q for j, c in vec.items() if c * inv % q}
                pivots[pivot] = vec
                relations.append((g, weight))
                break
            factor = vec[pivot]
            pv = pivots[pivot]
            for j, c in pv.items():
                vec[j] = (vec.get(j, 0) - factor * c) % q
                if not vec[j]:
                    del vec[j]
    maxdeg = max(map(sum, terms))
    rows = len(terms) + len(relations)
    M = IntegerMatrix(rows, rows)
    common = B ** maxdeg
    for j, m in enumerate(terms):
        M[j, j] = B ** (maxdeg - sum(m))
    for col, (g, weight) in enumerate(relations, len(terms)):
        for m, coeff in g.items():
            M[ti[m], col] = coeff * common
        M[col, col] = (p ** weight) * common
    print("lattice", rows, "terms", len(terms), "relations", len(relations), "degree", maxdeg,
          "weight", sum(w for _, w in relations))
    LLL.reduction(M, delta=0.99, eta=0.501)
    target0 = common
    one = (0,) * nv
    for rr in range(min(rows, 40)):
        row = [int(M[rr, j]) for j in range(rows)]
        if all(x == 0 for x in row[len(terms):]) and abs(row[ti[one]]) == target0:
            sign = 1 if row[ti[one]] > 0 else -1
            es = []
            for i in range(nv):
                m = [0] * nv
                m[i] = 1
                es.append(sign * row[ti[tuple(m)]] // (B ** (maxdeg - 1)))
            return es
    return None


if __name__ == "__main__":
    p = 1984346863717798023066695980738244268696469265829857414485314401858860336957043620300874901206591899123013663345899264529249829074392403977185809373864268317960203009281909170720311068287524897098165568326823508810872179674425401789683052386208630901516891181355489869477368839434216418671564381951683837535422633888442789353584326493367432312419571045037507196038152207419175944434802057100041579784573308702699586001046643858837705946438644735933528963469020201
    hs = [6677635742671494327324309427726936681648874825113335056999689006691863161397461413885563666797081056512008165096772577556354363555020144524725149560458118834582983249544779403485506396393182777718976785522762546437124539173127652645696479149554445954769724359329756570, 5723056222390063294584522090027174335845459606191864730918829854334248817532402262983801041441096895270547545161218172164815675215271457868408836385417981625091178984232317302330064943722913581217587265823833925597455994775263692716753008851659489414122633038512103153, 38470467365228984991251729378361735620646197018494991017575246278312351098306454406951468055783663484994136671320568723499978317396779801103163702494048359984066019001592153848917152552770447915661838422870569342382876122901927325627000545945713398831504320964336916, 1842426666108336536507150231064301091613124205950283976232083875678006301639894363768346081518423928011441166360111881326244011849288318966788707435588806356486057211242826253984132049394300670361677990255398050393787839296478606801918648445967355273037649891369325753, 78189826782705566124686070694264673603661810648761409249333288939812544539379617639868923912020007146525898383222100283464368541389491097366443853685840545453165372669121174287371583201776142302246553874806021844703462859286648423256552983345080776810473787654638320, 6600693869224110795089187427758859680218530429664016749020493479573387961619533545815960390596087185130165779818537321849563818853279756998241601962054092477803190356370584627840054923140256574319268873065266143106223250294272081499516883996600857318399256981667017929, 3171456500185891949527569398815486662617608277263512207096844957918180359267974350657181179580875022941564590393945662851394544949921357553429640795555251722949018790065102287195810252820599062036569937149893289904841662740134987639427460473498116608962742148816798110, 5815741237218693924430158968377262741004772398737088564670044054219472613406951360298064878207419948193138928149581113292748902871464677768646814255724790499570120312697955955641525897877943084341646310808063478911212484636974527195707529921391199807814120324147389768]
    es = solve_errors(p, 1536, 890, hs[:4], depth=2)
    print(es)
    if es:
        zs = [(h << 646) + e for h, e in zip(hs, es)]
        u = ((zs[1] * 1 - zs[0] * 0) * pow(zs[0] - zs[1], -1, p)) % p
        v = zs[0] * u % p
        print("u", u)
        print("v", v)
        print(all((v * pow(u+i, -1, p)) % p == zs[i] for i in range(8)))
