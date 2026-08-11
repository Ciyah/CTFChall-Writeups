---
ctf: HTBLabs
title: Exatlon
category: rev
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Exatlon

## Challenge
Can you find the password?

## Approach

The supplied file, `Exatlon/exatlon_v1`, is a statically linked 64-bit ELF
binary. Running `strings` revealed the `UPX!` signature, indicating that the
binary was packed with UPX.

I unpacked a temporary copy to avoid modifying the original challenge file:

```bash
cp Exatlon/exatlon_v1 /tmp/exatlon_v1
upx -d /tmp/exatlon_v1
```

The unpacked binary retained its symbols, including `main` and the custom
function `exatlon(std::string const&)`. Disassembling `exatlon` showed that it
processes each password character as follows:

1. Read one character from the supplied password.
2. Shift its integer value left by four bits (`character << 4`).
3. Convert the result to a decimal string.
4. Append a space and repeat for every character.

`main` compares the resulting string against this sequence stored in
`.rodata`:

```text
1152 1344 1056 1968 1728 816 1648 784 1584 816 1728 1520 1840 1664 784 1632 1856 1520 1728 816 1632 1856 1520 784 1760 1840 1824 816 1584 1856 784 1776 1760 528 528 2000
```

A four-bit left shift is multiplication by 16, so the operation can be
reversed by dividing every number by 16 and converting each result to its
ASCII character:

```bash
python3 -c 's="1152 1344 1056 1968 1728 816 1648 784 1584 816 1728 1520 1840 1664 784 1632 1856 1520 1728 816 1632 1856 1520 784 1760 1840 1824 816 1584 1856 784 1776 1760 528 528 2000"; print("".join(chr(int(x)//16) for x in s.split()))'
```

This produces the password. Supplying it to the original packed binary
returns `[+] Looks Good ^_^`, confirming the result.

## Tools

- `file` — identified the executable format.
- `strings` — found the UPX signature and visible program messages.
- `upx` — unpacked a temporary copy of the executable.
- `nm` — located the preserved C++ symbols.
- `objdump` — disassembled `main` and `exatlon` and inspected `.rodata`.
- Python — reversed the numeric transformation.

## Lessons

- Check binaries for common packer signatures before beginning deeper static
  analysis.
- Work on a temporary copy when unpacking or otherwise transforming a supplied
  challenge artifact.
- A left shift by four bits is equivalent to multiplication by 16; reversing
  this simple encoding only requires division by 16.
- Preserved symbols can make an otherwise large, statically linked binary much
  easier to analyze.

## Flag

`HTB{redacted}`
