---
ctf: HTBLabs
title: ShinyHunter
category: misc
difficulty: unknown
tags: [prng, python, timing, lcg]
flag_format: HTB{...}
date: 2026-08-11
---

# ShinyHunter

## Challenge

Can you beat the odds, can you become the very best? IP:154.57.164.78:32133

## Approach

The service gives the player one of three starter Poketmon. Each starter has a
nominal shiny probability of only `8 / 65536`, and the flag is printed only
when the selected starter is shiny.

Reviewing `chall.py` showed that the result is predictable. The seed is built
from two values that the player can learn or control:

```python
time_passed = time.time() - boot_time
formatted_time = int(time_passed)
initial_seed = formatted_time + int(device_mac.replace(":", ""), 16)
seed = (1664525 * initial_seed + 1013904223) % 2**32
```

The device MAC is printed in the opening banner. The simulated dead battery
also resets `system_time` to zero, so the remaining time component is merely
the number of seconds since `boot_time`. Crucially, the program does not
calculate this value until the player submits their name. Delaying that input
therefore lets us choose the integer time component.

### Replaying the random number generator

Python's global `random` generator is repeatedly reseeded by the service. To
predict a result, the solver must reproduce both the seed and every random call
in its original order:

1. Seed with `seed` and generate the 16-bit trainer ID (`tid`) and secret ID
   (`sid`).
2. For starter index `i`, reseed with `seed + i`.
3. Generate six stats with `randint(20, 31)`.
4. Generate the nature with a choice from 25 entries.
5. Generate the 32-bit personality ID (`pid`).
6. Apply the same shiny test:

```python
shiny_value = tid ^ sid ^ (pid & 0xffff) ^ (pid >> 16)
is_shiny = shiny_value < 8
```

The solver tests all three starters for each possible elapsed second. I used
the range 25 through 45 seconds, which leaves enough time for the scripted
dialogue and server scheduling overhead. When a winning `(elapsed, starter)`
pair is found, it waits until that precise second, submits the name, advances
through the remaining dialogue, and selects the predicted starter.

The initial banner is timestamped locally. Since the server assigns
`boot_time` immediately after the banner's two-second sleep, the submission
deadline can be estimated as:

```python
deadline = banner_received_at + 2 + desired_elapsed
```

A small `0.10` second offset keeps the server safely inside the intended
integer-second window. Multiple workers request fresh sessions in parallel;
unhelpful MAC addresses are discarded immediately. Expanding the time window
means each MAC supplies many candidate seeds, making this substantially faster
than waiting for a shiny at the fixed initial prompt time.

Run the included solver with:

```bash
python3 solve.py
```

Successful output:

```text
candidate #553: f0:57:86:57:54:d1, elapsed 31, starter 1
FLAG: HTB{redacted}
```

## Tools

- Python 3
- `socket` for interacting with the TCP service
- `threading` for checking several sessions concurrently
- The provided `chall.py` source for reconstructing the PRNG call sequence

## Lessons

- A deterministic PRNG is unsuitable for security-sensitive rarity checks
  when its seed inputs are disclosed or attacker-controlled.
- Predicting Python's `random` output requires replaying every call in exactly
  the same order, including apparently unrelated stats and nature generation.
- Truncating a timestamp to an integer creates a large and forgiving timing
  window.
- An interactive input prompt can become a seed-control primitive when elapsed
  time is calculated only after that input is received.

## Flag

`HTB{redacted}`
