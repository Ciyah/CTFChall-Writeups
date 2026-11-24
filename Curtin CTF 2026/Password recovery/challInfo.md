---
ctf: "Curtin CTF 2026"
title: "Password recovery"
category: "Misc"
difficulty: "Medium"
tags: ["password-cracking", "yescrypt", "shadow-file", "policy-based-wordlist"]
flag_format: "CURTIN_CTF{...}"
date: "2026-11-21"
solved: true
---

## Challenge

Bob has forgotten his Linux login password, but has a copy of the machine's shadow file. The organisation Bob works at has a 90 day password rotation policy and requires at least one uppercase, lowercase, number and special character. Help him recover his password.

**Machine:** `56.69.151.28:8005` · **Points:** 250 · **Flag format:** `CURTIN_CTF{redacted}`

## Approach

### Phase 1 — Analyze

The challenge provides a remote shell as `bob` and a readable `~/shadow` file. The key hints are:
- Password policy: ≥1 upper, lower, digit, special character
- 90-day rotation policy
- Last changed: shadow field 3 = `20776` days since epoch ≈ 2026-11-17

Extracted Bob's hash line:
```
bob:!$y$j9T$sszMf9cL1urXxj0uB8he/1$H0uyA2n1PL2CeHKI1zuFUmaysLKzNV6/VyHbd7w7f75:20776:0:99999:7:::
```

Hash analysis:
- Leading `!` = account locked flag (strip for cracking; real hash starts at `$y$`)
- `$y$` prefix = **yescrypt** (modern default on Debian/Ubuntu, memory-hard like scrypt)
- This is NOT `$6$` (sha512crypt) — hashcat didn't support yescrypt at the time

### Phase 2 — Recon / Hypothesis

yescrypt is deliberately slow; brute-forcing rockyou would be impractical. The policy + 90-day rotation forces a **human-memorable, recently-changed** password. The overwhelmingly common corporate pattern that satisfies all four character class requirements and rotates quarterly is:

```
<Season|Month><Year><symbol>    e.g. Winter2026!   Autumn2026@   Nov2026#
```

With last-change ~Nov 2026, the current quarter is **Winter/Autumn 2026**. The candidate space is tiny: seasons/months × a few years × a few symbols = ~hundreds of guesses.

### Phase 3 — Crack

Python 3.13 removed the `crypt` module; call **libcrypt** directly via `ctypes`:

```python
import ctypes, ctypes.util

lib = ctypes.CDLL(ctypes.util.find_library('crypt') or 'libcrypt.so.1')
lib.crypt.restype  = ctypes.c_char_p
lib.crypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

full = '$y$j9T$sszMf9cL1urXxj0uB8he/1$H0uyA2n1PL2CeHKI1zuFUmaysLKzNV6/VyHbd7w7f75'

def chk(pw):
    r = lib.crypt(pw.encode(), full.encode())
    return r is not None and r.decode() == full

seasons = ['Spring','Summer','Autumn','Fall','Winter']
months  = ['January','February','March','April','May','June','July','August',
           'September','October','November','December','Nov','Dec','Oct']
years   = ['2026','2025','2024','26','25','24']
syms    = ['!','@','#','$','%','&','*','?','.','_']

for b in seasons + months:
    for y in years:
        for s in syms:
            for w in (b+y+s, b+s+y, b+y):
                if chk(w):
                    print("PASSWORD:", w); raise SystemExit
```

Result: `Winter2026@`

Verification: `W` (upper) + `inter` (lower) + `2026` (digit) + `@` (special) — policy satisfied.

Alternative: John the Ripper via `--format=crypt` (uses libcrypt for yescrypt):
```bash
echo 'bob:$y$j9T$sszMf9cL1urXxj0uB8he/1$H0uyA2n1PL2CeHKI1zuFUmaysLKzNV6/VyHbd7w7f75' > h
john --format=crypt --mask='?u?l?l?l?l?l2026?s' h
```

## Tools

- `nc` — connect to the remote shell
- Python `ctypes` + libcrypt — yescrypt hash verification (Python 3.13 removed `crypt` module)
- John the Ripper (`--format=crypt`) — alternative cracker with yescrypt support

## Lessons

- **Password policies create predictable passwords.** "≥1 of each class + 90-day rotation" pushes users toward `Season+Year+Symbol` patterns, collapsing the real keyspace to a few hundred guesses — crackable even against a slow hash like yescrypt.
- **Match the attack to the clue, not the dictionary.** Against a slow hash, a 100-entry targeted list beats a 14-million-entry rockyou run.
- **yescrypt (`$y$`) ≠ sha512crypt (`$6$`).** Always identify the `$id$` prefix first; hashcat lacked yescrypt support at the time — use John (`--format=crypt`) or libcrypt via `ctypes`.
- **Account lock flag (`!`)** at the start of the hash field doesn't affect cracking — strip it and use the hash starting from `$y$`.
- Defensively: long passphrases + breach-password blocklists beat complexity rules; never leave a readable shadow copy in a home directory.

## Flag

```
CURTIN_CTF{redacted}
```
