---
ctf: HTBLabs
title: r0bob1rd
category: pwn
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# r0bob1rd

## Challenge
I am developing a brand new game with robotic birds. Would you like to test my progress so far? IP:154.57.164.82:32710

## Approach

### Binary analysis

The binary is a 64-bit, dynamically linked ELF. It is not stripped and is not
PIE, so its code and data addresses remain fixed. NX and a stack canary are
enabled, but the binary only has partial RELRO. Consequently, entries in the
PLT/GOT remain writable.

The important fixed addresses are:

| Symbol | Address |
|---|---:|
| `operation` | `0x400aca` |
| `__stack_chk_fail@GOT` | `0x602028` |
| `printf@GOT` | `0x602030` |

The supplied libc contains these symbol offsets:

| Symbol | libc offset |
|---|---:|
| `printf` | `0x61c90` |
| `system` | `0x52290` |

### Vulnerabilities

The bird selection is checked, but the invalid-index branch calculates an
address relative to `robobirdNames` and passes that address to `%s`:

```c
if (choice >= 0 && choice <= 9)
    printf("You've chosen: %s\n", robobirdNames[choice]);
else
    printf("You've chosen: %s\n", &robobirdNames[choice]);
```

Since `robobirdNames` starts at `0x6020a0`, index `-14` points at `0x602030`,
which is `printf@GOT`:

```text
0x6020a0 + (-14 * 8) = 0x602030
```

Printing this address with `%s` leaks the raw resolved `printf` pointer. The
libc base and `system` address can therefore be calculated as follows:

```text
libc_base = leaked_printf - 0x61c90
system     = libc_base + 0x52290
```

The more direct vulnerability is in the description handling:

```c
fgets(description, 0x6a, stdin);
printf(description);
```

Passing attacker-controlled input directly to `printf` creates a format-string
vulnerability. The description begins at positional argument 8, so addresses
appended after 80 bytes occur at arguments 18, 19, and 20. Positional `%hn`
writes can therefore replace a 64-bit GOT value in three two-byte pieces.

There is also a useful interaction with the stack canary. The description is
104 bytes away from the canary. A 104-byte payload followed by a newline makes
`fgets` place that newline over the canary's normally zero first byte. This
guarantees that the function calls `__stack_chk_fail` after processing the
format string.

### Exploitation

The exploit proceeds in three passes through `operation`:

1. Send bird index `-14` and leak `printf` from its GOT entry. Use the supplied
   libc offsets to calculate `system` despite ASLR.
2. Use `%hn` writes to replace `__stack_chk_fail@GOT` with `operation`. Make the
   payload exactly 104 bytes so that its newline corrupts the canary. The failed
   check now calls `operation` instead of terminating, giving another input.
3. On the second pass, replace `printf@GOT` with the calculated address of
   `system`. Corrupt the canary again, causing the already-modified
   `__stack_chk_fail` entry to invoke `operation` for a third time.

During the third pass, every call through `printf@GOT` invokes `system`. After
selecting bird 0, the description `sh` reaches the original vulnerable call:

```text
printf(description) -> system("sh")
```

This opens a shell on the service. Reading `flag*` returns the flag.

### Reproduction

The complete exploit is in `solve.py` and uses only the Python standard
library:

```bash
python3 solve.py
```

Successful output includes:

```text
[+] flag: HTB{redacted}
```

## Tools

- `readelf`, `objdump`, `nm`, `strings`
- Python sockets and `struct`

## Lessons

- An overlong `fgets` interaction can be useful even with a stack canary when
  `__stack_chk_fail` itself is writable.
- Re-entering a vulnerable function can turn one format-string input into a
  staged exploit.

## Flag
HTB{redacted}
