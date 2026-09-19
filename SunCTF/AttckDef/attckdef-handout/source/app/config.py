from pathlib import Path
import os

TICK_SECONDS = int(os.getenv("TICK_SECONDS", "120"))
GRACE_SECONDS = int(os.getenv("GRACE_SECONDS", "20"))
SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", "3600"))
TICK_EPOCH_OFFSET = int(os.getenv("TICK_EPOCH_OFFSET", "0"))

FLAG_LIFETIME_TICKS = int(os.getenv("FLAG_LIFETIME_TICKS", "5"))
MAX_ACTIVE_NOTES_PER_USER = int(os.getenv("MAX_ACTIVE_NOTES_PER_USER", "5"))
MAX_TITLE_LEN = 80
MAX_CONTENT_LEN = 2048
MAX_TOKEN_LEN = 64

NOTE_ID_PREFIX = os.getenv("NOTE_ID_PREFIX", "NOTE")

KX7_MQR_WPL = float(os.getenv("KX7_MQR_WPL", "10"))
JB3_NVH_YTS = float(os.getenv("JB3_NVH_YTS", "3"))
CAPTCHA_EVERY = int(os.getenv("CAPTCHA_EVERY", "3"))
CAPTCHA_TTL_SECONDS = int(os.getenv("CAPTCHA_TTL_SECONDS", "300"))

GAMESERVER_USERNAME = os.getenv("GAMESERVER_USERNAME", "gameserver")

DB_PATH = os.getenv("DB_PATH", str(Path(__file__).resolve().parent.parent / "attckdef.db"))

_REPO_HANDOUT = Path(__file__).resolve().parent.parent.parent / "handout"
ATTACK_DATA_DIR = Path(
    os.getenv(
        "ATTACK_DATA_DIR",
        "/app/attack-data" if Path("/app/attack-data").exists() else str(_REPO_HANDOUT),
    )
)

FINAL_FLAG = os.getenv(
    "FLAG",
    Path("/flag.txt").read_text().strip()
    if Path("/flag.txt").exists()
    else "sunctf26{this_is_not_a_real_flag}",
)
