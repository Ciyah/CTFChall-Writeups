---
ctf: HTBLabs
title: Fishy HTTP
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Fishy HTTP

## Challenge
I found a suspicious program on my computer making HTTP requests to a web server. Please review the provided traffic capture and executable file for analysis. (Note: Flag has two parts)

## Approach

The executable is a self-contained .NET 8 bundle. Its embedded `MyProject.dll`
implements two covert encodings:

1. HTTP response HTML tags map to hexadecimal nibbles (`cite` = `0`, `h1` =
   `1`, ..., `blockquote` = `f`). Decoding the opening tags gives commands such
   as `whoami`, `systeminfo`, and a `type HTB{Th4ts_d07n37_` command.
2. Command output is Base64-encoded. Each Base64 character is hidden as the
   first character of a random dictionary word in the POST `feedback` field.
   Taking the first character of every token and decoding Base64 reveals the
   command output, including the second fragment
   `h77P_s73417hy_revSHELL}`.

Run `python3 solve.py` from this directory to decode both directions and join
the fragments.

## Tools

- tshark
- ILSpy
- Python 3

## Lessons

HTTP content can look like harmless randomized HTML while its structure—not
its visible text—carries data. Analyze both request and response directions
when a challenge states that a flag is split.

## Flag

`HTB{Th4ts_d07n37_h77P_s73417hy_revSHELL}`
