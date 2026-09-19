---
ctf: PwnSec
title: tap tap
category: crypto
difficulty: unknown
tags: []
flag_format: pwnsec{}
date: 2026-09-12
---

# tap tap

## Challenge
tap tap, who's there?

- @Tsumi

## Approach

1. `chall.py` implements an order-25 Fibonacci LFSR modulo a secret 128-bit
   prime. It releases 180 consecutive values after shifting each one right by
   48 bits. Thus every sample exposes 80 of its 128 bits.
2. The flaw is `Y = [ai >> 48 ...]`: truncation does not remove the LFSR's
   linear structure. In addition, `p` is constrained to
   `2^128 - 2^50 < p < 2^128 - 2^48`, which enables the unknown-modulus
   truncated-LFSR lattice attack.
3. The solver builds the 180-dimensional unknown-modulus lattice with
   `r=t=90`, reduces it, and treats short rows as annihilating polynomials.
   GCDing 12 pairwise resultants recovers
   `p = 340282366920938463463374127620052448857`. Polynomial GCD modulo `p`
   then gives the degree-25 characteristic polynomial. A 53-dimensional
   Kannan embedding recovers the missing low 48 bits of 52 outputs, after
   which the recurrence is rewound by 25 terms and extended over all 180
   leaked outputs.
4. Hashing the reconstructed 205-element `A` exactly as the challenge does,
   expanding it with SHAKE-256, and XORing it with the ciphertext produces the
   flag.

Reproduce with:

```sh
python3 -m pip install --target /tmp/taptap-pylibs fpylll cysignals python-flint
PYTHONPATH=/tmp/taptap-pylibs python3 solve.py
```

## Tools

- Python 3
- `fpylll` / `cysignals` for LLL and BKZ
- `python-flint` for integer resultants and finite-field polynomial GCDs

## Lessons

Hiding low bits is not sufficient to secure a linear generator. With enough
consecutive high-bit samples—and especially when the modulus is known to be
near a power of two—the hidden pieces become a bounded lattice problem.

## Flag

`pwnsec{wR17in6_17_t0oK_m3_thRe3__d4y5_d1d_4I_50lv3_i7_1n_thRe3_53c0nDs??}`
