---
ctf: HTBLabs
title: emo
category: forensics
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# emo

## Challenge
WearRansom ransomware just got loose in our company. The SOC has traced the initial access to a phishing attack, a Word document with macros. Take a look at the document and see if you can find anything else about the malware and perhaps a flag.

## Approach

1. Identify `emo.doc` as an OLE/Compound File Word document.
2. Extract its VBA with `olevba`. `Document_open` calls
   `Get4ipjzmjfvp.X8twf_cydt6`.
3. Recover the document text with `catdoc`. The macro removes the marker
   `][(s)]w`, keeps the first 50 characters, and then keeps every second
   character from position 51 onward. This reconstructs a hidden PowerShell
   command.
4. Remove the one-character junk prefix from the command's Base64 payload,
   Base64-decode it, and interpret the result as UTF-16LE PowerShell.
5. The PowerShell constructs `$FN5ggmsH` from integer arrays. It XORs every
   byte with `0xdf` before Base64-encoding the malware configuration. Applying
   that XOR to the static prefix gives:

   ```text
   id:M8nHJyeR;int:3000;jit:500;flag:HTB{4n0th3R_d4Y_AnoThEr_pH1Sh};url:
   ```

## Tools

- `file`, `7z`
- `olevba` from `oletools`
- `catdoc`
- Python (offline Base64, UTF-16LE, and XOR decoding)

## Lessons

- The large visible document body is an encoded command, not ordinary prose.
- Most VBA statements are junk; the meaningful transformations are marker
  removal and odd-position extraction.
- Static decoding of the PowerShell's configuration array is sufficient; the
  malware and its download URLs never need to be executed or contacted.

## Flag

`HTB{4n0th3R_d4Y_AnoThEr_pH1Sh}`
