---
ctf: HTBLabs
title: Surprise Factor
category: crypto
difficulty: hard
tags: [ECDSA, side-channel, binary-GCD, factorization]
flag_format: HTB{...}
date: 2026-08-13
---

# Surprise Factor

## Result

The challenge was solved against `154.57.164.82:30129`.

```text
nonce       = 0x565ec594a2c7e53d4e6dea66e73dff423c06d9395bcfe600f1e04072a0a65eb
private key = 0xd3fb54a60ef1d2e2cc5e9faa79c4dd8f452216a44b5cdb905477216358eb6ff8
flag        = HTB{redacted}
```

The successful attack has four stages:

1. Request a signature while tracing the vulnerable binary division.
2. Reverse its extended-binary-GCD trace to recover the unreduced product
   `D = nonce_mask * nonce`.
3. Factor `D` and identify the nonce among its divisors using signature `r`.
4. Recover the ECDSA private key and submit it.

## Service and source review

The service accepts newline-delimited JSON. The two useful actions are:

```json
{"action":"sign","track":["half","add","sub","binary_division_odd_modulus","div"]}
{"action":"submit","d":"0x..."}
```

The signing code first blinds the scalar used for point multiplication. It
later reduces it back to the real ECDSA nonce `k`, creates a second random
mask `m`, and computes the signature through a masked division:

```python
current_nonce = mod(current_nonce, N)

nonce_mask = secrets.randbelow(N)
denominator = mul(nonce_mask, current_nonce)

numerator = add(hash_int, mul(r, privkey))
numerator = mul(nonce_mask, numerator)
s = div(numerator, denominator, N)
```

`div()` reduces only the numerator before calling the binary division:

```python
def div(a, b, modulus):
    a = mod(a, modulus)
    return _binary_division_odd_modulus(a, b, modulus)
```

Consequently, its inputs are:

```text
a = m * (h + r*d) mod N
D = m * k                    # not reduced modulo N
s = a * D^(-1) mod N
```

The mask cancels in the modular result, so the signature is valid. The flaw is
that the full approximately 512-bit product `D` enters a data-dependent binary
extended-GCD implementation while its internal operations are traceable.

## Trace acquisition

[`collect.py`](./collect.py) sends the tracing request and saves the response
as `sample.json`:

```sh
python3 collect.py
```

The successful sample contains 412,111 symbols:

```text
h   = 0x68fe5e0bf669eb494cf12aef9acbcad940d949a9b0a85f6988847075f72971e1
r   = 0x0758a81492daaa019dc159166329178eccf132509110dd93b672634acebb2a035
s   = 0x7abf0dbccfc5cd6d2e52648d38b77e68665d90b5241d1a1377b93b897e4a989a
Q.x = 0xf85c6c901010ec340330ed7bbce9db3a0ef34bcec49315639cdca27dcad3880e
Q.y = 0xf8faa51c421cb7052cb6238c18d2d7cc9e25657d80e8f45a4e72e7d06aeeb790
```

There are several binary-division markers because affine conversion also uses
inversion. Only the trace after the final `y` marker belongs to the division
that computes `s`. It contains 294 subtractions and 607 halving iterations.

## Decoding the trace grammar

The vulnerable routine maintains operands `(u, v)` and coefficients
`(x1, x2)`:

```python
u, v = D, N
x1, x2 = a, 0
```

For every even operand it halves both that operand and its coefficient:

```python
u = half(u)
if x1 is even:
    x1 = half(x1)
else:
    x1 = half(add(x1, N))
```

With `half`, `add`, and `sub` enabled, one halving iteration therefore has one
of two encodings:

```text
h,h       coefficient was even (parity bit 0)
h,a,h     coefficient was odd  (parity bit 1)
```

Each GCD subtraction updates an operand and its matching coefficient, so it
emits `s,s`. Splitting on those pairs produces a list of groups. Each group
contains the coefficient parity bits observed during the preceding halvings.

The trace does not directly reveal which subtraction branch ran:

```python
if u >= v:
    u  = u - v
    x1 = x1 - x2
else:
    v  = v - u
    x2 = x2 - x1
```

Naively choosing both branches at every group is exponential. The key to
pruning is an invariant that combines the public `s` with the leaked
coefficient parities.

## The coefficient invariant

At initialization:

```text
a  = s*D mod N
x1 = a       and u = D
x2 = 0       and v = N
```

Therefore:

```text
x1 = s*u mod N
x2 = s*v mod N
```

Both the conditional halving rule and subtraction preserve these congruences,
so at every later state:

```text
x1 ≡ s*u (mod N)
x2 ≡ s*v (mod N)
```

This is much stronger than modeling operand parity alone. It lets the decoder
initialize plausible terminal coefficients and reject an incorrect reverse
branch as soon as its exact coefficients become too large.

## Reversing the binary GCD

The loop terminates with either `(u, v) = (1, w)` or `(w, 1)`. The non-unit
operand `w` is even because the final operation was an odd-minus-odd
subtraction. For this sample it is only `58`.

For each small even `w`, the invariant gives the terminal coefficients up to
small multiples of `N`:

```text
unit coefficient  = s + t1*N
other coefficient = (s*w mod N) + t2*N
```

The final branch is also forced. If `u == 1`, the preceding subtraction must
have reduced `v`; if `v == 1`, it must have reduced `u`.

Every forward operation has a simple exact inverse. A subtraction is undone
with addition:

```text
u-branch: u_before  = u_after + v
          x1_before = x1_after + x2

v-branch: v_before  = v_after + u
          x2_before = x2_after + x1
```

If a forward coefficient halving used leaked parity `p`, then:

```text
x_after  = (x_before + p*N) / 2
x_before = 2*x_after - p*N
```

The matching operand is restored by multiplying it by two. Reversing a whole
group means processing its parity bits in reverse order.

[`xreverse_recover.py`](./xreverse_recover.py) performs this search and applies
the following exact boundary conditions at the original state:

```text
v  = N
x2 = 0
0 <= x1 < N
x1 = s*D mod N
0 < D < N^2
```

The coefficient range is configurable. A bound of `5*N` and terminal search
through `256` are sufficient for this sample:

```sh
.venv/bin/python -u xreverse_recover.py sample.json \
  --max-terminal 256 --bound 5 --cap 1000000
```

The state set quickly collapses to one candidate and returns:

```text
D = 0x3b9ae4c8454a66f555d1aa19382c4104cc22996e4564834a92f9099658f36af81acb87dce8233a67b0a8879d882aa4955e8da9aa72b711468051162fdf723b
```

This is a 502-bit integer. Forward simulation using this value exactly
reproduces all 294 subtraction groups, all 607 halvings, and terminal state
`(1, 58)`.

## Why `D mod N` is not the nonce

An early hypothesis was that `k = D mod N`. That is incorrect:

```text
D mod N = m*k mod N
```

The random mask is still present. The challenge title supplies the next step:
factor the integer product `D = m*k`.

The complete factorization is:

```text
D = 3
  * 349
  * 1545773
  * 6672923
  * 1392212131
  * 2909631091
  * 4518664483
  * 9622480222084166579
  * 82889966717512745654064507380623
  * 77341036545436718519905601418108235101550616001554018653
```

Small factors were found with `sympy.factorint`; GMP-ECM split the remaining
cofactors. The two large ECM splits used in this run were:

```text
61687757190015419052291246143708553288789326018782246091896481325150958193287238299462307209938602180468201
= 9622480222084166579
* 6410795945149186536714189722164176357723856573742298189926893347155473043502744312760819

6410795945149186536714189722164176357723856573742298189926893347155473043502744312760819
= 82889966717512745654064507380623
* 77341036545436718519905601418108235101550616001554018653
```

## Identifying the nonce and private key

There are only ten distinct prime factors, so all `2^10` divisor partitions
can be tested. Both `k` and `m = D/k` must lie in `[1, N)`. The real nonce is
identified by the ECDSA relation:

```text
x(k*G) mod N = r
```

[`finish_solve.py`](./finish_solve.py) enumerates the subsets, performs that
curve check, derives a private-key candidate, verifies it against the supplied
public key, and submits it:

```sh
python3 finish_solve.py
```

The correct partition is:

```text
k = 3 * 349 * 6672923 * 4518664483
    * 77341036545436718519905601418108235101550616001554018653

k = 0x565ec594a2c7e53d4e6dea66e73dff423c06d9395bcfe600f1e04072a0a65eb

m = D/k
  = 0x0b0ab2280fd532347c43234db8366f3ed7644b2a8d18ee7788ed8de3536080f1
```

ECDSA satisfies `s*k = h + r*d (mod N)`, hence:

```text
d = (s*k - h) * r^(-1) mod N
  = 0xd3fb54a60ef1d2e2cc5e9faa79c4dd8f452216a44b5cdb905477216358eb6ff8
```

The script verifies `d*G == Q` before submitting it. The service response was:

```json
{"valid":true,"flag":"HTB{redacted}"}
```

## Unsuccessful approaches and lessons

Several general-purpose approaches were tried before using the invariant:

- Forward branch enumeration exceeded 600,000 states around group 145 and
  continued growing exponentially.
- A full integer Z3 model generated roughly 695 KB of SMT-LIB constraints but
  exhausted memory during preprocessing.
- A 512-bit QF_BV model consumed a 5 GB solver limit during bit-blasting.
- cvc5 stayed memory-stable but did not solve the linear-integer model within
  five minutes.
- Reversing only `(u, v)` still left too many ambiguous subtraction paths.
- A beam search over operand sizes was fast but discarded the correct path.

The decisive improvement was to reverse `(u, v, x1, x2)` together and enforce
`xi ≡ s*operand_i (mod N)` from the terminal state onward. This turns an
exponential symbolic problem into a tiny exact state search.

## Files

- `Surprise Factor/crypto_surprise_factor/`: supplied challenge source
- `collect.py`: retrieves a traced signature from the active endpoint
- `sample.json`: successful signature and trace
- `solve.py`: trace parser and earlier SMT experiments
- `xreverse_recover.py`: successful reverse-GCD decoder
- `finish_solve.py`: divisor search, nonce/key recovery, and submission
- `fast_recover.py`, `exact_recover.py`, `bv_exact_recover.py`: unsuccessful
  enumeration and solver experiments retained for reference

## Flag

`HTB{redacted}`
