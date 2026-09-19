# AttckDef Range — player handout

A local attack/defence training game, run under SUNCTF AD rules. This tarball has everything you get: the service
source, and yesterday's published attack data.

## The game

- A gameserver plants one flag into the `notestore` flag store every
  **120-second tick**, under the reserved `gameserver` account. Flags look
  like `SUN26` + 24 chars and stay valid for a few ticks.
- The flag-ID feed (`/api/flag_ids`) tells you *where* each tick's flag
  lives: `gameserver:NOTE-<tick>-<hex>`.
- The submission server (`/api/submit`) grades `flag_id` + `flag` pairs:
  `accepted`, `old`, `invalid`, `own`. Only gameserver flags count.
- The scoreboard shows six other teams and you (`Sunway CSC`).
- You need a `notestore` account to use the service API
  (`/api/register` / `/api/login`).

## The attack data

`old_attack.pcap` is yesterday's game network. One team — Scap3G04T
(`10.60.4.2`) — exploited this service five times. Their note IDs and flags
are expired, and the league flag in their accepted submissions is from
staging. Everything else in the capture is ordinary traffic.

## Files

```
README.md        this file
old_attack.pcap  yesterday's attack data
source/          the service source, exactly as deployed
```

## Win condition

Submit the flag :D
