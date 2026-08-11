---
ctf: HTBLabs
title: Diagnostic
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Diagnostic

## Challenge
Our SOC has identified numerous phishing emails coming in claiming to have a document about an upcoming round of layoffs in the company. The emails all contain a link to diagnostic.htb/layoffs.doc. The DNS for that domain has since stopped resolving, but the server is still hosting the malicious document (your docker). Take a look and figure out what's going on. IP: 154.57.164.82:32131

## Approach

1. Requested `/layoffs.doc` from the supplied service. Despite the `.doc`
   extension, `file` identified it as an OOXML ZIP archive.
2. Inspected `word/_rels/document.xml.rels` and found an external linked OLE
   object with the `htmlfile` ProgID:
   `http://diagnostic.htb:32131/223_index_style_fancy.html!`.
3. Retrieved that HTML stage. It invokes `ms-msdt` with the
   `PCWDiagnostic` handler (the Follina/MSDT technique) and embeds an
   obfuscated PowerShell command.
4. Base64-decoded the inner PowerShell and resolved its format strings. It:
   - creates the filename
     `HTB{msDt_4s_A_pr0toC0l_h4nDl3r...sE3Ms_b4D}.exe`;
   - downloads `https://automation.diagnostic.htb/2/n.exe` to
     `C:\Windows\Tasks\<filename>`;
   - executes the downloaded file.
5. Removed the final `.exe` suffix to obtain the flag.

## Tools

- `curl`
- `file`
- `unzip`
- Python `base64`

## Lessons

- Modern Office documents are ZIP containers even when served with a legacy
  `.doc` extension.
- OOXML relationship files can expose remote OLE/template payloads without
  opening the document.
- PowerShell's `-f` format operator is easily reversed by substituting each
  numbered placeholder with the corresponding array element.

## Flag

`HTB{msDt_4s_A_pr0toC0l_h4nDl3r...sE3Ms_b4D}`
