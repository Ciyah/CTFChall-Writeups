---
ctf: HTBLabs
title: SSOS
category: web
difficulty: hard
tags: [oauth, csrf, race-condition, bot, cookie-tossing]
flag_format: HTB{...}
date: 2026-08-13
---

# SSOS

## Challenge

> Homework? Never heard of her. Let's dance.

The challenge consists of three services behind Nginx:

- `edulearn.htb`: an Express application where teachers create assignments and students submit work.
- `sso.edulearn.htb`: a Go/Gin OAuth provider.
- An internal Puppeteer bot that initializes the site and accepts URLs through EduLearn's report feature.

The remote address changes whenever the instance is restarted. Requests must go to the supplied IP and port while preserving either `edulearn.htb:<port>` or `sso.edulearn.htb:<port>` in the `Host` header.

The final solver is [ssos_solve.py](./ssos_solve.py).

## Executive summary

The flag is not stored in a directly readable file or API. During startup, the bot submits `process.env.FLAG` as homework. The intended account is `student@edulearn.htb`, whose password is randomly generated at container startup.

The exploit combines four weaknesses:

1. A startup race lets us register `student@edulearn.htb` before the bot.
2. The bot uses one shared Puppeteer browser and cookie jar for teacher setup, student setup, and reported URLs.
3. `loginSSO(email, password)` ignores both arguments and authorizes whichever SSO user is currently represented by the shared `token` cookie.
4. The unrestricted report feature lets us make the bot submit a cross-site login form that replaces that cookie with our known student's token.

When the bot later calls `loginSSO()` and submits the flag, EduLearn identifies it as our student. We can then log in normally and read our own submission.

## Source review

### Where the flag enters the application

The important startup sequence is in `bot/index.js`:

```javascript
async function initialSetup() {
    const teacherEmail = "teacher@edulearn.htb";
    await loginUser(teacherEmail, teacherPassword);
    await loginSSO(teacherEmail, teacherPassword);

    for (const assignmentContent of sampleAssignments) {
        await createAssignment(assignmentContent, false);
    }

    const studentPassword = process.env.STUDENT_PASSWORD || (await randomPassword());
    const studentEmail = "student@edulearn.htb";

    await registerUser(studentEmail, studentName, studentPassword);
    await loginUser(studentEmail, studentPassword);
    await loginSSO(studentEmail, studentPassword);
    await submitFlagToAssignment();

    await loginUser(teacherEmail, teacherPassword);
    await loginSSO(teacherEmail, teacherPassword);
}
```

`submitFlagToAssignment()` types the environment variable into the first assignment:

```javascript
await page.type('textarea[name="content"]', process.env.FLAG);
await page.click('button[type="submit"]');
```

Therefore, the objective is to control the EduLearn identity at this exact startup step.

### The OAuth helper ignores its credentials

`loginSSO()` accepts an email and password but never uses them:

```javascript
async function loginSSO(email, password) {
    const page = await browser.newPage();
    const callbackUrl = encodeURIComponent(`${CLIENT_INTERNAL}/oauth/callback`);
    await page.goto(
        `${SSO_INTERNAL}/oauth/authorize?response_type=code&redirect_uri=${callbackUrl}` +
        `&scope=email%20name&client_id=${CLIENT_ID}`
    );
    // Approve if necessary...
}
```

The SSO middleware decides the user exclusively from the browser's `token` cookie. This makes the shared cookie jar the real authentication boundary.

### The report feature exposes the shared browser

Any authenticated EduLearn user may submit an arbitrary URL:

```javascript
app.post("/submit-url", isAuthenticated, async (req, res) => {
    await fetch("http://localhost:3001/visit-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: req.body.url }),
    });
});
```

The bot performs no scheme or host validation:

```javascript
await page.goto(url, { waitUntil: "networkidle0", timeout: 30000 });
```

This permits `data:text/html,...` documents as well as ordinary HTTP URLs.

### Login CSRF changes the SSO cookie

The SSO login endpoint sets its JWT cookie without an explicit `SameSite` policy:

```go
c.SetCookie("token", token, 3600, "/", "", false, true)
```

The handler also calls `ShouldBindJSON` directly:

```go
if err := c.ShouldBindJSON(&input); err != nil { ... }
```

We can construct a top-level `text/plain` form navigation whose serialized body is valid JSON. The form is:

```html
<form id="f" method="POST" enctype="text/plain"
      action="http://sso.edulearn.htb:1337/api/login">
  <input name='{"email":"student@edulearn.htb",
                "password":"KnownPass123!","x":"'
         value='"}'>
</form>
<script>document.getElementById("f").submit()</script>
```

For `text/plain` forms, the browser serializes controls as `name=value`. The resulting body is effectively:

```json
{"email":"student@edulearn.htb","password":"KnownPass123!","x":"="}
```

That is valid JSON. The login response replaces the shared browser's SSO `token` cookie with a JWT for our known account.

## Exploitation

### 1. Win the registration race

Restart the instance and immediately send concurrent registrations for:

```text
email:    student@edulearn.htb
password: KnownPass123!
name:     S
```

The solver uses twelve short-lived workers. Multiple requests can produce a misleading result: one request may create the user while another observes the subsequent duplicate-user error first. For that reason, the solver verifies ownership by attempting a login with the known password before declaring the race lost.

Winning changes the bot's later behavior:

- Its attempt to register the same email fails.
- Its attempt to log in with the randomly generated password also fails.
- We retain valid credentials for the special student account.

### 2. Create an EduLearn session and OAuth approval

The report endpoint requires an authenticated EduLearn session. The solver:

1. Logs into the SSO using the known student credentials.
2. Requests `GET /auth` on EduLearn.
3. Follows the OAuth authorization request on the SSO.
4. Approves the client if this is the first request.
5. Sends the authorization code to `/oauth/callback` on EduLearn.

Completing approval in advance is useful because later authorization requests can redirect immediately without waiting for a consent click.

### 3. Wait for exactly three assignments

Timing is the subtle part of the exploit.

Sending the malicious bot URL too early can race `initBrowser()`. The bot's lazy initialization is not concurrency-safe:

```javascript
if (!browser) {
    browser = await puppeteer.launch(...);
}
```

During testing, early or concurrent report floods disrupted initialization and produced instances with no assignments or flag at all.

Waiting too long is also fatal because the bot quickly moves from its third assignment to student login and flag submission.

The reliable synchronization point is the appearance of all three public assignments. The solver polls the EduLearn home page every 50 ms and sends exactly one bot request as soon as the third distinct assignment ID appears. At this point:

- Puppeteer is definitely initialized.
- Teacher assignment creation has completed.
- The bot has not yet completed its broken student login/OAuth sequence.

### 4. Replace the bot's SSO cookie

Immediately after the third assignment appears, the solver submits the encoded `data:` document to `/submit-url`.

The bot loads the document and its script submits the JSON-shaped form to the internal SSO origin. A `302` from EduLearn's `/submit-url` confirms the bot service completed the visit. The login response installs our student's SSO token into the shared browser.

### 5. Let the bot submit the flag as us

The bot proceeds with startup:

1. Its registration of `student@edulearn.htb` fails because we own it.
2. Its password login fails because it uses the random password, not ours.
3. `loginSSO(studentEmail, studentPassword)` ignores those arguments.
4. The OAuth flow uses the SSO cookie planted by our form.
5. The callback creates an EduLearn session for our student.
6. `submitFlagToAssignment()` stores the flag as our submission.

### 6. Read the flag normally

The solver repeatedly creates a fresh OAuth session using our known credentials, enumerates assignments and submission links, and searches accessible pages with:

```python
FLAG_RE = re.compile(r"HTB\{[^}\s]+\}")
```

Because we are now the flag submission's author, no authorization bypass is required.

## Usage

Install the only external dependency:

```bash
python3 -m pip install requests
```

Restart the challenge instance. As soon as HTB provides the new endpoint, run:

```bash
python3 ssos_solve.py <IP> <PORT>
```

The successful run looked like this:

```text
[+] target 154.57.164.72:31550
[+] Phase 0: hammering student registration (concurrent)...
[+] WON registration race
[+] Phase 1: establishing client session + approval for student@edulearn.htb
[+] Phase 2: waiting precisely for the third assignment ...
[+] Phase 3: sending one cookie-swap visit ...
[+] Phase 4: polling target account for the flag immediately...
[+] cookie-swap visit 1/1: HTTP 302
[+] FLAG: HTB{...}
```

If the registration race is lost, restart the instance. A fallback account cannot reliably recover the existing flag because the bot's successful random-password login restores the intended student before submitting it.

## Unsuccessful approaches and lessons

### Reaction-based stored XSS

`app.js` writes reaction keys into `innerHTML`, which initially looks exploitable. The server, however, restricts reactions to a fixed allowlist:

```javascript
const allowedEmojis = ["👍", "❤️", "🤔", "🎯", "🔥"];
```

Arbitrary HTML receives `400 Invalid emoji`.

### Submission sanitizer tricks

Submissions are rendered with EJS's raw output tag, but `sanitize-html` only permits a small tag and attribute set. Several mutation-XSS, dangling-markup, SVG, event-handler, and raw-text wrapper ideas did not yield reliable execution in the remote browser.

### OAuth redirect-path traversal

The Go provider validates callback paths using `strings.HasPrefix`, so paths such as `/oauth/callback/../../profile` pass validation and normalize elsewhere in the browser. This is a real weakness, but leaking or redeeming the teacher's authorization code still required a dependable script-execution or exfiltration primitive. The startup cookie swap is simpler and was the working route.

### Referrer leakage

Redirecting a teacher authorization code onto a page containing an external avatar only leaked the origin:

```text
Referer: http://edulearn.htb:1337/
```

Chrome's default `strict-origin-when-cross-origin` policy strips the path and query, so the OAuth code does not reach an external webhook.

### Flooding the report endpoint

Repeated or overly early bot visits can interfere with the bot's own browser initialization. The successful exploit uses one request synchronized immediately after the third assignment, not a request flood.

## Remediation

Several independent changes would break the exploit chain:

- Do not share one browser context across privileged setup, untrusted URL visits, and different users.
- Create an isolated incognito/browser context for each reported URL.
- Reject non-HTTP(S) schemes and enforce a strict destination allowlist in `/submit-url`.
- Make `loginSSO()` actually authenticate the intended user or remove its unused credential parameters.
- Set cookies with explicit `Secure` and `SameSite=Strict` or an appropriate `Lax` policy.
- Require CSRF protection on login and other state-changing endpoints.
- Do not place secret-dependent initialization behind a raceable, externally reachable startup sequence.
- Handle duplicate registration with a proper conflict response and ensure bot setup aborts on failed registration or login.
- Initialize Puppeteer once before accepting report requests.

## Flag

```text
HTB{redacted}
```
