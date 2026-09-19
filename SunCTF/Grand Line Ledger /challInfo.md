---
ctf: SunCTF
title: Grand Line Ledger 
category: crypto
difficulty: unknown
tags: []
flag_format: sunctf26{...}
date: 2026-09-05
---

# Grand Line Ledger 

## Challenge
The Straw Hats' signing ledger needs two captains to approve a route. Nami's abort handling is keeping the wrong voyage counters. Recover the treasure key, then complete its fresh verification slip before the Marines audit the logbook. https://grand-line.chal.sunwaycybersecurityclub.org

## Approach

`GET /manifest` disclosed a two-party Schnorr-style signature:

```text
p = 309967783371909964659037772809563145007
q = 154983891685954982329518886404781572503
g = 4
z_i = k_i + e*x_i mod q
e = SHA256(message|R1|R2) mod q
```

The exact flaw is in abort counter handling. When `abort` names a captain, the
server returns both partial responses but does not commit that captain's voyage
counter. Repeating that abort therefore reuses the named captain's nonce and
commitment. The other captain's counter does advance, changing the aggregate
commitment and challenge.

I made two requests with `abort: 1` in the same session:

```sh
curl -c /tmp/grand_a1.cookie -X POST https://grand-line.chal.sunwaycybersecurityclub.org/sign \
  -H 'Content-Type: application/json' --data '{"message":"route-a","abort":1}'
curl -b /tmp/grand_a1.cookie -X POST https://grand-line.chal.sunwaycybersecurityclub.org/sign \
  -H 'Content-Type: application/json' --data '{"message":"route-b","abort":1}'
```

Captain 1 reused `R1 = 236842109031938113430778730205367915219`:

```text
(e1,z1) = (97529307391594492852334140198608977695,
           88542634649764372807412368175738322988)
(e2,z2) = (107304008608069314629356496703075806743,
           124377610424660534795982117998096298027)
```

Likewise, two requests with `abort: 2` in a fresh session reused
`R2 = 299445099757222694011892175063020641074`:

```sh
curl -c /tmp/grand_a2.cookie -X POST https://grand-line.chal.sunwaycybersecurityclub.org/sign \
  -H 'Content-Type: application/json' --data '{"message":"route-c","abort":2}'
curl -b /tmp/grand_a2.cookie -X POST https://grand-line.chal.sunwaycybersecurityclub.org/sign \
  -H 'Content-Type: application/json' --data '{"message":"route-d","abort":2}'
```

```text
(e3,z3) = (125142015023417816745492033409744825479,
           20154842162179941119655817888914600556)
(e4,z4) = (89198829248274408408712898036626379110,
           120743275313867407779123696386484492251)
```

For a reused nonce, subtracting the equations eliminates `k`:

```python
x1 = (z1-z2) * pow(e1-e2, -1, q) % q
x2 = (z3-z4) * pow(e3-e4, -1, q) % q
# x1 = 5895215282834040485530921312895606690
# x2 = 66149588755171062080739061764293221898
secret = (2*x1-x2) % q
# secret = 100624733496452001219841667266279563985
```

The last expression is Lagrange interpolation at zero for shares `f(1)` and
`f(2)`. As a check, `g^x1 mod p` and `g^x2 mod p` exactly matched both public
shares in the manifest.

Finally, `GET /proof` pointed to the proof service. Its fresh challenge required:

```python
key = SHA256(b"100624733496452001219841667266279563985").digest()
response = HMAC_SHA256(
    key,
    b"proof-v1|grand-line-ledger|9xwXAnICZfvCDrzf0I7JxDuO|am7sgb9quWQ2JL5yuAKtvPA_i6sMV3Ln4iyaHgZ7Ib4"
).hexdigest()
# ef1d188ef27f2cd7a8bb878d509a1aad8a00b55e3b1fc5b33b0f0fabac7446f1
```

Submitting that response with its token to
`POST /v1/crypto/grand-line-ledger/claim` returned the flag. Proof tokens are
short-lived, so a reproduction must request a fresh token and recompute the HMAC.

## Tools

- `curl`
- Python 3 (`hashlib`, `hmac`, modular arithmetic)

## Lessons

Never reuse a Schnorr nonce. Transactional abort logic must advance or burn all
nonces whose commitments or partial responses have been exposed.

## Flag

`sunctf26{one_piece_treasure_39715b6e18b061d3b4961774}`
