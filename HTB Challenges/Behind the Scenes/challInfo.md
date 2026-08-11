---
ctf: HTBLabs
title: Behind the Scenes
category: rev
difficulty: easy
tags: [elf, signals, anti-disassembly, ud2]
flag_format: HTB{...}
date: 2026-08-11
---

# Behind the Scenes

## Challenge
After struggling to secure our secret strings for a long time, we finally figured out the solution to our problem: Make decompilation harder. It should now be impossible to figure out how our programs work

## Approach

I first identified the supplied file and inspected its strings and symbols:

```bash
file Behind\ the\ Scenes/rev_behindthescenes/behindthescenes
strings -a Behind\ the\ Scenes/rev_behindthescenes/behindthescenes
nm -an Behind\ the\ Scenes/rev_behindthescenes/behindthescenes
```

The file is a non-stripped, 64-bit PIE ELF. Its symbol table exposes both `main`
and a function named `segill_sigaction`, suggesting that the program handles
illegal-instruction signals.

Disassembling those functions confirmed the trick:

```bash
objdump -d -Mintel Behind\ the\ Scenes/rev_behindthescenes/behindthescenes
objdump -s -j .rodata Behind\ the\ Scenes/rev_behindthescenes/behindthescenes
```

At startup, `main` registers `segill_sigaction` as the handler for `SIGILL` and
then repeatedly executes `UD2`. `UD2` is a two-byte instruction that deliberately
raises an invalid-opcode exception. The signal handler accesses the saved CPU
context and advances the instruction pointer by two bytes, allowing execution to
continue immediately after each `UD2`.

These interspersed instructions make the control flow harder for a decompiler to
recover, but they do not conceal the actual comparisons. The program requires a
12-character argument and checks it in four three-byte chunks against strings in
`.rodata`:

| Offset | Compared value |
| ---: | --- |
| 0 | `Itz` |
| 3 | `_0n` |
| 6 | `Ly_` |
| 9 | `UD2` |

Concatenating the chunks gives the password:

```text
Itz_0nLy_UD2
```

Running the binary with that value prints the flag:

```bash
./behindthescenes Itz_0nLy_UD2
# > HTB{redacted}
```

## Tools

- `file` — identify the executable format and architecture
- `strings` — inspect embedded printable data
- `nm` — list symbols from the non-stripped binary
- `objdump` — disassemble the program and dump `.rodata`

## Lessons

- Signal handlers can deliberately alter a saved execution context before the
  program resumes.
- On x86-64, `UD2` is a two-byte guaranteed-invalid instruction commonly used to
  generate `SIGILL` intentionally.
- Anti-disassembly techniques may confuse automated decompilers while remaining
  straightforward to understand from raw assembly and program data.
- Meaningful symbol names in a non-stripped binary can quickly reveal the intended
  reverse-engineering path.

## Flag

`HTB{redacted}`
