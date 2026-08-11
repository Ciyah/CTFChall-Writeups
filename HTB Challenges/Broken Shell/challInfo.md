---
ctf: HTBLabs
title: Broken Shell
category: misc
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Broken Shell

## Challenge
We've built a secure sandbox environment that only allows specific symbols and numbers. It's designed to be inescapable—security at its best IP: 154.57.164.82:32658

## Approach

The input filter permits only digits and shell metacharacters, but it also permits
Bash parameter expansion. Triggering `${0}` showed that the restricted shell's
script path is `/home/restricted_user/broken_shell.sh`. Characters can therefore
be extracted from that path with `${0:offset:length}` and concatenated into
otherwise-forbidden command names.

Build and run `ls` (`l` is offset 32, `s` is offset 8):

```bash
${0:32:1}${0:8:1}
```

This revealed `this_is_the_flag_gg`. Build `more` from offsets 3, 2, 6, and 4,
then select the 19-character filename using question-mark globbing:

```bash
${0:3:1}${0:2:1}${0:6:1}${0:4:1} ???????????????????
```

## Tools

- `nc`
- Bash parameter substring expansion and pathname globbing

## Lessons

Character allowlists do not make evaluation by a shell safe. Bash expansions can
synthesize filtered characters from existing variables before command execution.

## Flag

`HTB{redacted}`
