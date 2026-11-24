---
ctf: "Curtin CTF 2026"
title: "Misc 2"
category: "misc"
difficulty: ""
tags: ["env-vars", "shell", "linux"]
flag_format: "CURTIN_CTF{...}"
date: "2026-11-21"
solved: true
---

## Challenge

Connect to `56.69.151.28:8001` and find the flag.

## Approach

**Phase 1 — Analyze**

No files were provided. The challenge is a live netcat service, so analysis
begins at connection time.

**Phase 2 — Recon**

1. Connected to the service and landed in an interactive shell as `ctfuser`:

   ```bash
   nc 56.69.151.28 8001
   ctfuser@afb4529ab344:~$
   ```

2. Standard shell enumeration found nothing on disk:

   ```bash
   id                                  # uid=1001(ctfuser), no interesting groups
   sudo -l                             # (empty)
   ls -la /                            # no /flag; /root is mode 700
   find / -iname '*flag*' 2>/dev/null  # only /sys/... kernel flags — red herrings
   ```

3. With no flag file on the filesystem, shifted attention to the shell
   environment and startup files. Inspected `~/.bashrc`:

   ```bash
   cat ~/.bashrc
   ```

   The tail of `.bashrc` suppresses history and exports the flag:

   ```sh
   export HISTFILESIZE=0
   export HISTSIZE=0
   unset HISTFILE
   export FLAG=CURTIN_CTF{redacted}
   ```

**Phase 3 — Infiltrate**

4. Retrieved the flag directly from the environment:

   ```bash
   echo "$FLAG"
   # CURTIN_CTF{redacted}
   ```

   Alternatively: `env | grep -i flag`

## Tools

- `nc` (netcat)
- Standard shell built-ins: `id`, `sudo`, `ls`, `find`, `cat`, `echo`, `env`

## Lessons

When a shell drops you into a container/remote box and there is no flag on
disk, check the **environment** and **shell startup files** before giving up:
`.bashrc`, `.profile`, `.bash_profile`, `/etc/profile`, `/etc/environment`.
The commands `env`, `echo $FLAG`, and reading the rc files are the first
things to try right alongside the filesystem search.

The challenge name and the flag content (`3nv_v@rs` = "env vars") are both
direct hints.

## Flag

```
CURTIN_CTF{redacted}
```

