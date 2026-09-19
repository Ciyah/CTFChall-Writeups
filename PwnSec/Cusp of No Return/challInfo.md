---
ctf: PwnSec
title: Cusp of No Return
category: crypto
difficulty: unknown
tags: []
flag_format: pwnsec{}
date: 2026-09-13
---

# Cusp of No Return

## Challenge
The curve survived. Its marking did not.

Our archivist kept a finite shadow of a punctured elliptic curve, two arithmetic symmetries, and several recollections of the same missing cusp. Every recollection was based somewhere else. Every orientation was forgotten.

Recover the isogeny. There is no return address.

Your challenge instance is generated per deployment — download instance.json from your running instance.
.
- @Curiosity

## Approach

The 15-by-15 records are conjugated exponentials of a five-dimensional free
nilpotent Lie algebra. Apply `log_unipotent` to the two generators and rebuild
the abstract basis

```
X, Y, Z=[X,Y], U=[X,Z], V=[Y,Z].
```

Express every other logarithm in that basis, separately over `5^64` and
`7^48`. For each of the first two cusp records, normalize its `(Z,U,V)`
coordinates by the unit `Z` coordinate. Their difference is projectively the
hidden vector `v`: line 92 deliberately makes the two transport parameters
differ by a unit, while lines 97-98 publish points whose direction contains
the secret.

The second leak is at lines 81-85 and 112 of `public/generate.py`. Publishing
the images of both generators under the known Frobenius and CM actions exposes
`M^-1 F M` and `M^-1 I M`. Solve the simultaneous linear equations
`T*C = action*T`; their kernel gives `T=M` up to a harmless scalar. Thus
`T*v` is projectively `(1,s)`, revealing the secret slope locally. Combine the
two slopes with CRT.

Finally compute `R=P+sQ`, run the supplied 5- and 7-isogeny chain, derive the
AES key from its final j-invariant, and authenticate/decrypt the GCM seal.

Reproduce with:

```sh
python3 solve.py instance.json
```

## Tools

Python 3 and the supplied `public/algebra.py` / `public/curve.py` routines.

## Lessons

Random conjugation does not hide invariant Lie-algebra structure. Publishing
two independent known outer actions also fixes the supposedly secret marking
up to scalar, which is sufficient to recover projective data.

## Flag

`pwnsec{0ee34ba7554e8402}`
