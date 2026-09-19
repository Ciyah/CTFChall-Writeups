import secrets
import threading
import time

from .config import CAPTCHA_EVERY, CAPTCHA_TTL_SECONDS

_lock = threading.Lock()
_counters: dict[str, int] = {}
_challenges: dict[str, tuple[int, float]] = {}

_OPS = (
    ("+", lambda a, b: a + b),
    ("-", lambda a, b: a - b),
    ("*", lambda a, b: a * b),
)


def _new_challenge() -> dict:
    a = secrets.randbelow(40) + 2
    b = secrets.randbelow(40) + 2
    sym, fn = _OPS[secrets.randbelow(len(_OPS))]
    if sym == "-" and b > a:
        a, b = b, a
    challenge_id = secrets.token_hex(8)
    with _lock:
        _challenges[challenge_id] = (fn(a, b), time.time() + CAPTCHA_TTL_SECONDS)
    return {"captcha_id": challenge_id, "question": f"{a} {sym} {b} = ?"}


def needs_captcha(username: str) -> bool:
    with _lock:
        return _counters.get(username, 0) >= CAPTCHA_EVERY


def challenge() -> dict:
    return _new_challenge()


def verify(challenge_id: str, answer: str) -> bool:
    with _lock:
        entry = _challenges.pop(challenge_id, None)
    if entry is None:
        return False
    expected, expires = entry
    if time.time() > expires:
        return False
    try:
        return int(str(answer).strip()) == expected
    except ValueError:
        return False


def record_verdict(username: str) -> None:
    with _lock:
        _counters[username] = _counters.get(username, 0) + 1


def reset(username: str) -> None:
    with _lock:
        _counters[username] = 0
