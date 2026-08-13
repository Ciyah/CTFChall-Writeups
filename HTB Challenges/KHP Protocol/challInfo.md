---
ctf: HTBLabs
title: KHP Protocol
category: pwn
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# KHP Protocol

## Challenge
Welcome to Operation Red Roch, Your mission, should you choose to accept it. Find a zero day in this protocol to gain access in the system. Your exploit will be used by our Red Team in their next mission. Good luck. IP:154.57.164.82:31149

## Approach

The registration format is `REKE user:role key;`. Each registered key is
formatted with an unbounded `sprintf` into an 84-byte heap allocation.

1. Register a fake `admin` credential in memory.
2. Register a temporary key, then issue a failing `AUTH` to make the server
   allocate and cache the key database immediately after that key's chunk.
3. Free the temporary key with `DEKE`.
4. Register another key, recycling the freed chunk, and overflow through its
   84-byte data region, 4 alignment bytes, and the next 8-byte chunk header.
5. Inject the fake admin credential into the cached database contents.
6. Authenticate the original fake-admin key. `strstr` now finds it in the
   corrupted database, and `AUTH` sets the global role to `admin`.
7. Run `EXEC` and read `flag.txt` from the resulting shell.

Run the exploit with:

```sh
python3 solve.py
```

## Tools

- Python 3 sockets
- Netcat for protocol reconnaissance

## Lessons

- Fixed-size heap allocations are not safe when populated with unbounded
  formatting functions such as `sprintf`.
- Freeing and reallocating an equal-sized chunk gives predictable placement,
  allowing an adjacent heap object to be targeted.
- Authentication must not trust a mutable cached database or use substring
  matching to establish credential existence.

## Flag

`HTB{redacted}`
