---
ctf: HTBLabs
title: JerryTok
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# JerryTok

## Challenge
Welcome to JerryTok, your portal to the nearest jerryboree, where mediocrity is celebrated! Dive into the daily escapades of the wonderfully average, from mundane mishaps to modest triumphs. Share your moments, connect, and laugh as you find glory in the ordinary. Join now and embrace the delightfully dull at your local jerryboree! IP:154.57.164.78:30429

## Approach

The `location` query parameter is interpolated into a string passed to
Twig's `createTemplate()`, resulting in SSTI. PHP command execution functions
and access outside `/www` are blocked, but Twig callbacks still expose useful
two-argument PHP functions.

1. Use Twig's `reduce("file_put_contents", path)` to write `.htaccess` and a
   shell CGI script beneath `/www/public`.
2. Enable `ExecCGI` and associate `.sh` files with the CGI handler.
3. Invoke `chmod(path, 0755)` through Twig's two-argument `sort()` comparator.
4. Request the CGI script, which runs the SUID `/readflag` binary outside PHP's
   `disable_functions` and `open_basedir` restrictions.

## Tools

- `curl`
- Python 3 (`solve.py`)

## Lessons

PHP restrictions do not constrain other interpreters launched by the web
server. Writable `.htaccess` files plus `mod_cgi` can turn a file-write
primitive into code execution.

## Flag

`HTB{redacted}`
