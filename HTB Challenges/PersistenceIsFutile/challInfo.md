---
ctf: HTBLabs
title: PersistenceIsFutile
category: forensics
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# PersistenceIsFutile

## Challenge
Hackers made it onto one of our production servers 😅. We've isolated it from the internet until we can clean the machine up. The IR team reported eight difference backdoors on the server, but didn't say what they were and we can't get in touch with them. We need to get this server back into prod ASAP - we're losing money every second it's down. Please find the eight backdoors (both remote access and privilege escalation) and remove them. Once you're done, run /root/solveme as root to check. You have SSH access and sudo rights to the box with the connections details attached below. IP: 154.57.164.82:32161

## Approach

Connected over SSH as `user` and used the supplied sudo access. A baseline run of
`/root/solveme` showed all eight issues outstanding. Enumeration of MOTD hooks,
cron jobs, SSH keys, shell startup files, SUID executables, processes, and local
accounts identified these persistence mechanisms:

1. MOTD reverse shell: `/etc/update-motd.d/30-connectivity-check` and
   `/var/lib/private/connectivity-check`.
2. Daily SSH-key reinsertion: `/etc/cron.daily/pyssh` and
   `/lib/python3/dist-packages/ssh_import_id_update`.
3. The `nobody@nothing` key in `/root/.ssh/authorized_keys`.
4. A reverse-shell `cat` alias in `/home/user/.bashrc`.
5. An `alertd` bind shell launched from `/root/.bashrc`, with the renamed binary
   at `/usr/bin/alertd`.
6. The `user` crontab executing commands retrieved from an attacker-controlled
   DNS TXT record.
7. `/etc/cron.daily/access-up`, which regenerated random SUID bash copies.
8. Five SUID shell copies (`/home/user/.backdoor`, `/usr/bin/dlxcrw`,
   `/usr/bin/mgxttm`, `/usr/sbin/afdluk`, and `/usr/sbin/ppppd`) plus a modified
   `gnats` account.

Removed the malicious scripts, jobs, keys, aliases, binaries, and running
processes. Restored `gnats` to GID 41, shell `/usr/sbin/nologin`, and a locked
password (`*`). A final `sudo /root/solveme` reported every issue fully
remediated.

## Tools

- SSH
- Standard Linux process, account, cron, hashing, and filesystem utilities

## Lessons

- Remove both a persistence payload and every mechanism that recreates it.
- Timestamp checks alone miss copied binaries whose times were cloned from a
  legitimate executable; hashes and SUID enumeration expose them.
- Login-time hooks, shell aliases, system accounts, and DNS are all viable
  persistence surfaces.

## Flag

`HTB{redacted}`
