import random
import secrets
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from .config import (
    FLAG_LIFETIME_TICKS,
    NOTE_ID_PREFIX,
    TICK_EPOCH_OFFSET,
    TICK_SECONDS,
)
from .db import get_db

_TOKEN_RNG = random.Random()


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _current_tick_id() -> int:
    return int(time.time() // TICK_SECONDS) - TICK_EPOCH_OFFSET


def seconds_until_next_tick() -> int:
    return TICK_SECONDS - (int(time.time()) % TICK_SECONDS)


def _generate_note_id() -> str:
    return f"{NOTE_ID_PREFIX}-{secrets.randbelow(90_000_000) + 10_000_000:08d}-{secrets.token_hex(3).upper()}"


def _generate_token() -> str:
    return str(uuid.UUID(int=_TOKEN_RNG.getrandbits(128)))


def create_note(owner_username: str, title: str, content: str) -> dict:
    now = utcnow()
    expires_at = now + timedelta(seconds=FLAG_LIFETIME_TICKS * TICK_SECONDS)
    note_id = _generate_note_id()
    token = _generate_token()
    tick_id = _current_tick_id()

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO notes (tick_id, owner_username, note_id, token, title, content, created_at, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tick_id,
                owner_username,
                note_id,
                token,
                title,
                content,
                now.isoformat(),
                expires_at.isoformat(),
            ),
        )

    return {
        "tick_id": tick_id,
        "owner_username": owner_username,
        "note_id": note_id,
        "token": token,
        "title": title,
        "content": content,
        "created_at": now.isoformat(),
        "expires_at": expires_at.isoformat(),
    }


def get_active_note(note_id: str) -> Optional[dict]:
    now_iso = utcnow().isoformat()
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM notes WHERE note_id = ? AND expires_at > ?",
            (note_id, now_iso),
        ).fetchone()
    return dict(row) if row else None


def get_note(note_id: str) -> Optional[dict]:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM notes WHERE note_id = ?", (note_id,)
        ).fetchone()
    return dict(row) if row else None


def get_latest_note_for_owner(owner_username: str) -> Optional[dict]:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM notes WHERE owner_username = ? ORDER BY id DESC LIMIT 1",
            (owner_username,),
        ).fetchone()
    return dict(row) if row else None


def get_recent_notes_for_owner(owner_username: str, ticks: int = 6) -> list[dict]:
    cutoff = _current_tick_id() - ticks
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM notes WHERE owner_username = ? AND tick_id >= ? ORDER BY tick_id DESC",
            (owner_username, cutoff),
        ).fetchall()
    return [dict(r) for r in rows]


def list_active_notes(limit: int = 100) -> list[dict]:
    now_iso = utcnow().isoformat()
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT tick_id, owner_username, note_id, title, created_at, expires_at
            FROM notes WHERE expires_at > ? ORDER BY id DESC LIMIT ?
            """,
            (now_iso, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def list_notes_for_owner(owner_username: str) -> list[dict]:
    now_iso = utcnow().isoformat()
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM notes WHERE owner_username = ? AND expires_at > ? ORDER BY id DESC",
            (owner_username, now_iso),
        ).fetchall()
    return [dict(r) for r in rows]


def count_active_notes_for_user(owner_username: str) -> int:
    now_iso = utcnow().isoformat()
    with get_db() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM notes WHERE owner_username = ? AND expires_at > ?",
            (owner_username, now_iso),
        ).fetchone()
    return int(row["n"])


def cleanup_expired_notes() -> None:
    now_iso = utcnow().isoformat()
    with get_db() as conn:
        conn.execute("DELETE FROM notes WHERE expires_at <= ?", (now_iso,))
