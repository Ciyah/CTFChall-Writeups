import random
import time
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .config import (
    FINAL_FLAG,
    GAMESERVER_USERNAME,
    GRACE_SECONDS,
    TICK_EPOCH_OFFSET,
    TICK_SECONDS,
)
from .db import get_db
from .gameserver import game_start_tick
from .models import (
    ErrorResponse,
    FlagIdsResponse,
    GameStatusResponse,
    SubmitRequest,
    SubmitResponse,
)
from .tick import (
    get_active_note,
    get_note,
    get_recent_notes_for_owner,
    seconds_until_next_tick,
)

router = APIRouter(prefix="/api", tags=["game platform"])

POINTS_PER_FLAG = 50

BOT_TEAMS = [
    ("kopicincau", "10.60.1.2"),
    ("anti_1337", "10.60.2.2"),
    ("reunionjr", "10.60.3.2"),
    ("Scap3G04T", "10.60.4.2"),
    ("GPT-1010", "10.60.5.2"),
    ("kena paksa", "10.60.6.2"),
]
PLAYER_TEAM = ("Sunway CSC", "10.60.7.2")


def _current_tick_id() -> int:
    return int(time.time() // TICK_SECONDS) - TICK_EPOCH_OFFSET


@router.get(
    "/game/status",
    summary="Game clock and service states",
    response_model=GameStatusResponse,
)
def game_status():
    return {
        "tick_seconds": TICK_SECONDS,
        "current_tick": _current_tick_id(),
        "seconds_remaining": seconds_until_next_tick(),
        "grace_seconds": GRACE_SECONDS,
        "services": [{"name": "notestore", "state": "online"}],
    }


@router.get(
    "/flag_ids",
    summary="Published flag IDs (current and recent ticks)",
    response_model=FlagIdsResponse,
    responses={503: {"model": ErrorResponse, "description": "Gameserver between ticks."}},
)
def flag_ids():
    recent = get_recent_notes_for_owner(GAMESERVER_USERNAME, ticks=6)
    if not recent:
        deadline = time.time() + 3
        while not recent and time.time() < deadline:
            time.sleep(0.1)
            recent = get_recent_notes_for_owner(GAMESERVER_USERNAME, ticks=6)
        if not recent:
            return JSONResponse(
                status_code=503,
                content={"status": "NO_TICK_YET", "message": "Gameserver has not planted a flag yet. Retry shortly."},
            )
    ticks = [
        {
            "tick": row["tick_id"],
            "flag_ids": [f"{GAMESERVER_USERNAME}:{row['note_id']}"],
            "expires_at": row["expires_at"],
        }
        for row in recent
    ]
    return {"service": "notestore", "ticks": ticks}


@router.post(
    "/submit",
    summary="Submission server — grade a flag_id + flag pair",
    response_model=SubmitResponse,
    responses={403: {"model": SubmitResponse, "description": "Flag rejected."}},
)
def submit(body: SubmitRequest):
    rejected = JSONResponse(
        status_code=403,
        content={"status": "rejected", "reason": "invalid",
                 "message": "That pair does not match any planted flag."},
    )
    if ":" not in body.flag_id:
        return rejected
    owner_username, note_id = body.flag_id.split(":", 1)
    if owner_username != GAMESERVER_USERNAME:
        return JSONResponse(
            status_code=403,
            content={"status": "rejected", "reason": "own",
                     "message": "That is not a gameserver flag."},
        )
    note = get_note(note_id)
    if note is None or note["owner_username"] != GAMESERVER_USERNAME:
        return rejected
    if get_active_note(note_id) is None:
        _record(note_id, body.flag, "old")
        return JSONResponse(
            status_code=403,
            content={"status": "rejected", "reason": "old",
                     "message": "That flag expired with its tick."},
        )
    if note["content"] != body.flag:
        _record(note_id, body.flag, "invalid")
        return rejected

    _record(note_id, body.flag, "accepted")
    return {
        "status": "accepted",
        "points": POINTS_PER_FLAG,
        "flag": FINAL_FLAG,
        "message": "Flag accepted. League flag awarded!",
    }


def _record(note_id: str, flag_value: str, status: str) -> None:
    with get_db() as conn:
        conn.execute(
            "INSERT INTO submissions (tick_id, flag_id, flag_value, status, created_at)"
            " VALUES (?,?,?,?,?)",
            (
                _current_tick_id(),
                f"{GAMESERVER_USERNAME}:{note_id}",
                flag_value[:128],
                status,
                datetime.now(timezone.utc).isoformat(),
            ),
        )


@router.get(
    "/submissions/recent",
    summary="Your recent submission results",
)
def recent_submissions():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT tick_id, flag_id, status, created_at FROM submissions"
            " ORDER BY id DESC LIMIT 20"
        ).fetchall()
    return [dict(r) for r in rows]


@router.get(
    "/scoreboard",
    summary="Simulated game scoreboard",
)
def scoreboard():
    elapsed = max(0, min(_current_tick_id() - game_start_tick(), 720))
    teams = []
    for idx, (name, ip) in enumerate(BOT_TEAMS, start=1):
        rng = random.Random((idx << 20) ^ 0x5EED)
        attack = sum(rng.choice((0, 10, 25, 25, 50)) for _ in range(elapsed))
        defense = elapsed * 10
        teams.append({
            "name": name, "ip": ip, "you": False,
            "attack": attack, "defense": defense, "sla": 100.0,
            "total": attack + defense,
        })
    with get_db() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM submissions WHERE status = 'accepted'"
        ).fetchone()
    accepted = int(row["n"])
    teams.append({
        "name": PLAYER_TEAM[0], "ip": PLAYER_TEAM[1], "you": True,
        "attack": accepted * POINTS_PER_FLAG,
        "defense": elapsed * 10,
        "sla": 100.0,
        "total": accepted * POINTS_PER_FLAG + elapsed * 10,
    })
    teams.sort(key=lambda t: t["total"], reverse=True)
    for rank, team in enumerate(teams, start=1):
        team["rank"] = rank
    return {"tick": _current_tick_id(), "teams": teams}
