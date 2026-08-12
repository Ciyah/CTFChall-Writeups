---
ctf: HTBLabs
title: Rega's Town
category: rev
difficulty: unknown
tags: [rust, regex, static-analysis]
flag_format: HTB{...}
date: 2026-08-12
---

# Rega's Town

## Challenge

Welcome to Rega Town, a quaint little place where everyone communicates through the magic of patterns and rules

## Approach

The supplied file is a 64-bit Rust ELF with symbols and debug information intact:

```console
$ file "Rega's Town/dist/rega_town"
ELF 64-bit LSB pie executable, x86-64, dynamically linked, with debug_info, not stripped
```

Running it shows that it expects a passphrase:

```console
$ ./rega_town
Welcome to our secret town!
Enter secret passphrase:
```

### Finding the validation functions

Because the binary is not stripped, its application functions are visible in the symbol table:

```console
$ nm -C rega_town | rg 'rega_town::'
rega_town::filter_input
rega_town::multiply_characters
rega_town::check_input
rega_town::main
```

`filter_input` constructs and applies eight regular expressions. Their string pointers and lengths can be recovered from the static array at virtual address `0x3d52a0`. The patterns are:

```regex
(?:^[\x48][\x54][\x42]).*
^.{3}(\x7b).*(\x7d)$
^[[:upper:]]{3}.[[:upper:]].{3}[[:upper:]].{3}[[:upper:]].{3}[[:upper:]].{4}[[:upper:]].{2}[[:upper:]].{3}[[:upper:]].{4}$
(?:.*\x5f.*)
(?:.[^0-9]*\d.*){5}
.{24}\x54.\x65.\x54.*
^.{4}[X-Z]\d._[A]\D\d.................[[:upper:]][n-x]{2}[n|c].$
.{11}_T[h|7]\d_[[:upper:]]\dn[a-h]_[O]\d_[[:alpha:]]{3}_.{5}
```

Together, these establish a 33-character `HTB{...}` value and many fixed or constrained positions. In particular, the string has the following shape:

```text
HTB{redacted}
```

Here, `d` represents a decimal digit and the remaining character classes are further restricted by the expressions above.

### Recovering each word

`check_input` divides the candidate into seven slices and calls `multiply_characters` on each. That function converts every character to its Unicode/ASCII value and returns their `u128` product. Each result must equal a hard-coded constant:

| Positions | Required product | Matching characters |
|---:|---:|:---|
| 4–6 | `0x7a070` | `Y0u` |
| 8–10 | `0x5c436` | `Ar3` |
| 12–14 | `0x6cc60` | `Th3` |
| 16–19 | `0x27b5776` | `K1ng` |
| 21–22 | `0x10f9` | `O7` |
| 24–26 | `0xd76a0` | `The` |
| 28–31 | `0x7465a58` | `Town` |

For example, the fifth constraint is:

```text
ord('O') * ord('7') = 79 * 55 = 4345 = 0x10f9
```

Applying the regex restrictions while factoring or brute-forcing each small slice produces:

```text
HTB{redacted}
```

### Verification

```console
$ printf '%s\n' 'HTB{redacted}' | ./rega_town
Welcome to our secret town!
Enter secret passphrase:
Correct one of us!!
```

## Tools

- `file` — identified the executable and available debug information
- `strings` and `nm` — located messages and application symbols
- `objdump` — disassembled the three validation functions
- `gdb` — inspected the embedded regex pointer table and debug line data
- Python — brute-forced the small character-product constraints

## Lessons

- Always inspect symbols before beginning deeper decompilation; Rust names made the validation stages explicit here.
- Embedded regexes can reveal most of an input's structure without reconstructing the regex-library internals.
- Combining positional character classes with multiplicative ASCII constraints reduces each slice to a tiny search space.

## Flag

`HTB{redacted}`
