---
ctf: PwnSec
title: PHault
category: web
difficulty: unknown
tags: []
flag_format: pwnsec{}
date: 2026-09-12
---

# PHault

## Challenge
slop slop go away Come again another day Be the person that you fear Slop slop go away -Fat Mesh

- @ANAS

## Approach
1. A request to `/` disclosed the complete PHP source through
   `highlight_file(__FILE__, true)`. The only input was the numeric-looking `id`
   parameter.
2. The query concatenates `$_GET["id"]` directly into SQL:
   `SELECT username FROM users WHERE id = <id>`. Both query failure and query
   success print the same text, and the shutdown handler pads requests to two
   seconds, defeating ordinary Boolean and short timing probes.
3. A non-timing oracle exists because the code always calls
   `$res->fetch_row()`. Appending `INTO @variable` makes a successful `SELECT`
   return boolean `true`; PHP then throws a fatal error by calling `fetch_row()`
   on that boolean. In contrast, selecting multiple rows into one variable makes
   MySQL reject the query, reaching the normal `if (!$res) die(...)` branch.

   Oracle payload shape:

   ```sql
   0 OR id=1 OR NOT(<condition>) INTO @phault
   ```

   If `<condition>` is true, only `id=1` is selected and the fatal response is
   4744 bytes. If it is false, all user rows are selected and the ordinary error
   response is 4557 bytes.

   These predicates located the data:

   ```sql
   EXISTS(SELECT 1 FROM information_schema.tables
          WHERE table_schema=DATABASE() AND table_name='flag')
   EXISTS(SELECT 1 FROM information_schema.columns
          WHERE table_schema=DATABASE() AND column_name='flag')
   ```

4. `solve.py` first binary-searches
   `LENGTH((SELECT flag FROM flag LIMIT 1))`, then recovers the seven ASCII bits
   of every character with predicates of this form:

   ```sql
   (ASCII(SUBSTRING((SELECT flag FROM flag LIMIT 1),1,1)) & 1) != 0
   ```

   Run it with:

   ```console
   $ python3 solve.py --workers 16
   [+] flag length: 24
   [+] flag: pwnsec{129046f7d25a7e1b}
   ```

## Tools

- `curl` for source retrieval and oracle validation
- Python standard library for the concurrent extractor

## Lessons

- Identical application messages do not imply identical execution paths.
- `SELECT ... INTO` changes the result type returned by `mysqli::query`, which
  can expose a PHP fatal-error oracle when the caller assumes a result object.
- Cardinality errors provide a deterministic alternative when timing is padded
  or noisy.

## Flag

`pwnsec{129046f7d25a7e1b}`
