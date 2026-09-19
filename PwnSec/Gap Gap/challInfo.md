---
ctf: PwnSec
title: Gap Gap
category: crypto
difficulty: unknown
tags: []
flag_format: pwnsec{}
date: 2026-09-12
---

# Gap Gap

## Challenge
There are two gaps in this RSA key.

One gap is in the private exponent. The other is hiding between a shared divisor and the modulus.

- @chamaaaa

## Approach
1. From `p = 2ga+1`, `q = 2gb+1`, and `h = pb+a`, expand the
   public modulus:

   ```text
   N - 1 = 4g^2ab + 2g(a+b) = 2g(2gab+a+b) = 2gh
   ```

   The code also sets `lambda = 2gab`, so `ed-1 = k*lambda` is divisible
   by `2g`. Consequently:

   ```text
   gcd(N-1, ed-1) = 2g
   ```

   (The generation checks make the unwanted cofactors coprime.)

2. Write the leaked exponent as
   `d = d_known + x*10^47`, where `0 <= x < 10^30`. After removing the
   common factor 2, `x` is a small root of

   ```text
   (e*d_known-1)/2 + (e*10^47/2)*x == 0 (mod g)
   ```

   Here `g` is an unknown 600-bit divisor of `(N-1)/2`, a 2047-bit
   integer. A univariate Howgrave-Graham/Coppersmith lattice (`m=3`,
   `t=7`, `X=10^30`) recovers the 100-bit root.

3. Exact reproduction commands:

   ```bash
   python3 -m pip install --target .deps fpylll cysignals
   python3 solve.py public/live_output.txt
   ```

   The recovered decimal block is:

   ```text
   695749151285857004205253701502
   ```

4. Reconstructing `d` gives `2g = gcd(N-1, ed-1)`. Since
   `h = lambda+a+b` and `ed-1 = k*lambda`, `k` is within a few integers
   of `ed/h`. Testing that tiny interval recovers `lambda`, then
   `p+q = 2g(h-lambda)+2`. The resulting quadratic factors `N`.
   Finally, `pow(c, d, N)` converts to the flag bytes.

## Tools

- Python 3
- SymPy (polynomial construction and exact roots)
- fpylll (LLL reduction)

## Lessons

Leaking all but 30 decimal digits of `d` becomes fatal when the modulus
construction makes `N-1` and `ed-1` share a large hidden factor. Unknown-factor
Coppersmith recovers substantially more than brute force could reach.

## Flag

The bundled `public/output.txt` decrypts to a decoy. Solving the values emitted
by the live instance gives:

`pwnsec{7d2a8255d8c8a9e4}`
