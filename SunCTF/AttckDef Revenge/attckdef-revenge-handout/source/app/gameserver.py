import logging
import secrets
import threading
import time

from .config import GAMESERVER_USERNAME, TICK_EPOCH_OFFSET, TICK_SECONDS
from .tick import create_note, get_latest_note_for_owner

log = logging.getLogger("gameserver")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [gameserver] %(message)s")

FLAG_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

NOTE_TITLES = [
    "weekend plans",
    "groceries",
    "bookmarks to read",
    "wifi password rotation",
    "standup notes",
    "ideas backlog",
    "reading list",
    "meeting minutes 07/14",
    "packing checklist",
    "gift ideas",
    "gym routine",
    "recipe: lentil soup",
    "call the bank",
    "budget for july",
    "plant watering schedule",
    "movies to watch",
    "car service reminder",
    "conference talk draft",
    "bookshelf measurements",
    "holiday shortlist",
    "quotes i liked",
    "hardware wishlist",
    "tax documents checklist",
    "training log w29",
]

_started_at_tick: int | None = None


def game_start_tick() -> int:
    global _started_at_tick
    if _started_at_tick is None:
        _started_at_tick = _current_tick_id()
    return _started_at_tick


def _current_tick_id() -> int:
    return int(time.time() // TICK_SECONDS) - TICK_EPOCH_OFFSET


def generate_flag() -> str:
    return "SUN26" + "".join(secrets.choice(FLAG_ALPHABET) for _ in range(24))


def _plant_flag_for_tick(tick_id: int) -> dict:
    title = NOTE_TITLES[tick_id % len(NOTE_TITLES)]
    return create_note(
        owner_username=GAMESERVER_USERNAME,
        title=title,
        content=generate_flag(),
    )


def _gameserver_loop():
    game_start_tick()
    while True:
        try:
            tick_id = _current_tick_id()
            latest = get_latest_note_for_owner(GAMESERVER_USERNAME)
            if latest is None or latest["tick_id"] != tick_id:
                note = _plant_flag_for_tick(tick_id)
                log.info("planted flag at %s for tick %s", note["note_id"], tick_id)
        except Exception:
            log.exception("gameserver iteration failed")
        time.sleep(2)


def start_gameserver_thread() -> threading.Thread:
    t = threading.Thread(target=_gameserver_loop, daemon=True, name="gameserver")
    t.start()
    return t
