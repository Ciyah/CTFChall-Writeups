---
ctf: SunCTF
title: Wasting Time 
category: misc
difficulty: unknown
tags: []
flag_format: sunctf26{...}
date: 2026-09-06
---

# Wasting Time 

## Challenge
Hope I could waste your time. Good luck.nc wastingtime.chal.sunwaycybersecurityclub.org 1337

## Approach
1. The supplied `challenge.py` is protected with PyArmor and targets CPython 3.11.
   Running it under 3.11 and tracing the decrypted code objects revealed that it
   accepts at most 3000 bytes of C, bans `#?%"'\`, compiles it, and executes the
   resulting binary for 20 randomized rounds.
2. Each round sends four little-endian `uint64_t` values (`start`, `stride`,
   `seed`, and instruction count), followed by 9-byte VM instructions and a pad
   the same length as the submitted source. The expected integer is produced by
   `orbit_vm(source, pad, start, stride, seed, program)`.
3. `generate_solve.py` creates a quote-free C quine. It packs the quine template
   into 64-bit decimal constants, reconstructs its exact 2935-byte source
   (including the newline appended by `read_source`), interprets the supplied VM,
   and prints the expected unsigned 64-bit result. It passed 100 random tests and
   all 20 rounds locally:

   ```sh
   cd wastingtime-player
   /tmp/cpython311-install/bin/python3.11 generate_solve.py
   gcc -std=gnu11 -O0 -w -o solve solve.c
   /tmp/cpython311-install/bin/python3.11 challenge.py < solve.c
   ```

4. The live deployment consistently deadlocked while starting round 4, despite
   rounds 1-3 succeeding. As a fallback, `probe.c` reads its verifier parent's
   `/proc/<ppid>/environ`. `extract_flag.py` changes one comparison per request
   and uses a two-second delay as a binary oracle for each `FLAG` byte:

   ```sh
   /tmp/cpython311-install/bin/python3.11 extract_flag.py
   ```

   The extractor recovered the flag through the closing `}`.

## Tools

- CPython 3.11.9
- GCC
- Python audit/profile hooks and `dis`
- `nc` / Python sockets

## Lessons

- The verifier hashes the source after appending a newline; omitting that byte
  causes every otherwise-correct quine result to fail.
- Passing a minimal environment to a child does not hide secrets if the child
  can read the same-UID parent's `/proc/<pid>/environ`.
- `preexec_fn` can deadlock in service deployments; timeouts do not help if the
  deadlock occurs before `Popen` returns.

## Flag

`sunway26{c0pycat_n3v3r_f0rg3ts_3v3ry_s1ngl3_byt3_1t_3v3r_wr0t3}`
