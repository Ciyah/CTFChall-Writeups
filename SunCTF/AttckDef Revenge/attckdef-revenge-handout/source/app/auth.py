import hashlib
import hmac
import re
import secrets
import time
from typing import Optional

from fastapi import Depends, Header, HTTPException, Request
from fastapi.security.utils import get_authorization_scheme_param

from .config import GAMESERVER_USERNAME, SESSION_TTL_SECONDS
from .db import get_db

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,24}$")
PBKDF2_ITERATIONS = 120_000


class AuthError(HTTPException):
    def __init__(self, detail: str = "authentication required"):
        super().__init__(status_code=401, detail=detail)


def _hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt), PBKDF2_ITERATIONS
    ).hex()


def create_user(username: str, password: str) -> None:
    if not USERNAME_RE.match(username):
        raise AuthError("username must be 3-24 chars of [a-zA-Z0-9_]")
    if username.lower() == GAMESERVER_USERNAME.lower():
        raise AuthError("that username is reserved by the gameserver")
    if len(password) < 6:
        raise AuthError("password must be at least 6 characters")
    salt = secrets.token_hex(16)
    pass_hash = _hash_password(password, salt)
    from datetime import datetime, timezone

    created = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        if conn.execute(
            "SELECT 1 FROM users WHERE username = ?", (username,)
        ).fetchone():
            raise AuthError("username already registered")
        conn.execute(
            "INSERT INTO users (username, pass_hash, salt, created_at) VALUES (?,?,?,?)",
            (username, pass_hash, salt, created),
        )


def verify_user(username: str, password: str) -> bool:
    with get_db() as conn:
        row = conn.execute(
            "SELECT pass_hash, salt FROM users WHERE username = ?", (username,)
        ).fetchone()
    if row is None:
        return False
    return hmac.compare_digest(row["pass_hash"], _hash_password(password, row["salt"]))


def create_session(username: str) -> str:
    token = secrets.token_hex(32)
    with get_db() as conn:
        conn.execute("DELETE FROM sessions WHERE expires_at < ?", (time.time(),))
        conn.execute(
            "INSERT INTO sessions (token, username, expires_at) VALUES (?,?,?)",
            (token, username, time.time() + SESSION_TTL_SECONDS),
        )
    return token


def destroy_session(token: str) -> None:
    with get_db() as conn:
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))


def _user_for_token(token: str) -> Optional[str]:
    with get_db() as conn:
        row = conn.execute(
            "SELECT username FROM sessions WHERE token = ? AND expires_at > ?",
            (token, time.time()),
        ).fetchone()
    return row["username"] if row else None


def get_current_user(
    request: Request,
    authorization: str = Header(default=""),
) -> str:
    scheme, param = get_authorization_scheme_param(authorization)
    token = param if scheme.lower() == "bearer" else ""
    if not token:
        token = request.cookies.get("session", "")
    if not token:
        raise AuthError()
    username = _user_for_token(token)
    if username is None:
        raise AuthError("session expired or unknown")
    return username
