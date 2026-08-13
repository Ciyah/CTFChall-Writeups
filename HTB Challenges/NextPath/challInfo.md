---
ctf: HTBLabs
title: NextPath
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# NextPath

## Challenge
Find the next path in your career or even some vulnerabilities along the way. Anyway, good luck on your travels!
IP: 154.57.164.65:31644

## Approach

The `/api/team` endpoint can be exploited by supplying `id` twice. Next.js
parses repeated parameters as an array, which creates three useful type
confusions:

1. `ID_REGEX.test(query.id)` stringifies the array. A second value of `\n1`
   satisfies the multiline numeric regex.
2. `query.id.includes("/")` and `.includes("..")` perform exact array-element
   checks, so traversal characters inside the first value are not detected.
3. Concatenating the array with `.png` stringifies it with a comma. A crafted
   first path normalizes to exactly 100 characters, so `slice(0, 100)` removes
   the comma, second value, and `.png` suffix.

The path uses repeated `/proc/thread-self/root` symlinks as aliases for `/` so
it remains long after `path.join()` normalization while still resolving to
`/flag.txt`.

Run:

```bash
python3 solve.py
```

## Tools

- Python standard library (`urllib`)

## Lessons

- Validate both the type and contents of query parameters.
- Avoid multiline regexes for whole-string validation.
- String truncation is not a safe path-security boundary.

## Flag

`HTB{redacted}`
