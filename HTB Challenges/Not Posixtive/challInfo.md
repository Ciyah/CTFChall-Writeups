---
ctf: HTBLabs
title: Not Posixtive
category: misc
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Not Posixtive

## Challenge
Luigi is not posixtive we can challenge his scripting abilities. He's convinced we cannot understand the secret hidden inside his l33t coding abilities. We can't let that slide IP:154.57.164.72:31530

## Approach

The challenge asks us to satisfy the following condition in `check_win()`:

```python
if (
    debug[0] != debug[1]
    and str(debug[0]) != str(debug[1])
    and hash(debug[0]) == hash(debug[1])
    and isinstance(debug[0], type(debug[1]))
):
    print(open('flag.txt').read())
```

Each value placed in `debug` is calculated by `execute()` as:

```python
result.returncode * mode
```

Therefore, we need two different integers of the same type whose Python hashes are
equal. Python reserves `-1` internally as an error indicator for hash functions, so
the integer hash implementation remaps it to `-2`. As a result:

```python
-1 != -2
str(-1) != str(-2)
hash(-1) == hash(-2) == -2
```

### Creating a negative mode

`check_operands()` only examines the first two input characters and rejects these
operators:

```text
+ - * / % = x o b
```

The bitwise complement operator `~` is not rejected. The two-character expression
`~0` is accepted by `eval()` and evaluates to `-1`, giving us the required negative
multiplier.

### Producing exit codes 1 and 2

The selected executable must be at most four alphabetic characters, while its two
arguments can contain alphabetic characters and dots. `grep` satisfies these input
filters and has useful exit statuses:

- Exit code `1`: the pattern was not found in an existing file.
- Exit code `2`: an error occurred, such as attempting to read a nonexistent file.

The two subprocess calls can therefore be arranged as follows:

```text
grep zzzz flag.txt  -> exit code 1
grep xxxx nope      -> exit code 2
```

With `mode = -1`, `execute()` returns:

```text
1 * -1 = -1
2 * -1 = -2
```

These values pass every part of the win condition because they differ in value and
string representation, have the same type, and have identical Python hashes.

### Final interaction

```text
1
~0
2
grep
3
flag.txt,nope
4
zzzz,xxxx
5
```

The corresponding menu choices are:

1. Set the mode to `~0` (`-1`).
2. Set the binary to `grep`.
3. Set the file arguments to `flag.txt` and `nope`.
4. Set the patterns to `zzzz` and `xxxx`.
5. Run the win check and print the flag.

## Tools

- Source-code review
- Python integer hash behavior
- `nc` for connecting to the remote challenge service
- GNU `grep` exit-status behavior

## Lessons

- Input blacklists are fragile; overlooking an equivalent operator such as `~` can
  undermine the intended restriction.
- Hash equality does not imply value equality.
- Python's special handling of the integer hash `-1` creates a convenient collision
  between `-1` and `-2`.
- Subprocess exit codes can be treated as controlled numeric values when command,
  argument, and return-code behavior are understood.
- Using `eval()` on input-derived expressions remains dangerous even with filtering.

## Flag

```text
HTB{redacted}
```
