---
ctf: "Curtin CTF 2026"
title: "Misc 1"
category: "misc"
difficulty: ""
tags: []
flag_format: "CTF{...}"
date: "2026-11-21"
---

## Challenge

Connect to 56.69.151.28:8000 and find the flag

## Approach

**Phase 1 — Analyze**
No local files provided. Challenge is purely remote: connect to a shell via netcat.

**Phase 2 — Recon**
1. Connected to the remote shell: `nc 56.69.151.28 8000`
2. Ran `ls -la` in the home directory, which revealed a hidden file `.flag` (note the leading dot, making it hidden from plain `ls`).

**Phase 3 — Infiltrate**
3. Attempted `cat .flag` but mistyped it as `cat .lag` — shell returned "No such file or directory".
4. Used the glob pattern `cat .?lag` to match the hidden file (`.` + any single char + `lag`), which resolved to `.flag` and printed the flag.

```
nc 56.69.151.28 8000
ls -la          # reveals .flag hidden file
cat .?lag       # glob matches .flag → prints flag
```

## Tools

- `nc` (netcat) — connect to remote shell
- Bash glob (`?`) — wildcard to match single character

## Lessons

- Hidden files (dotfiles) won't show without `ls -la`; always check for them on a new shell.
- Glob patterns (`?`, `*`) can be used in `cat` to match filenames when you can't type a character directly or want to avoid exact name issues.

## Flag

`CURTIN_CTF{redacted}`

