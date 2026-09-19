from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import routes_game, routes_service
from .config import ATTACK_DATA_DIR, TICK_SECONDS
from .db import init_db
from .gameserver import start_gameserver_thread

BASE_DIR = Path(__file__).resolve().parent

DESCRIPTION = """
AttckDef Revenge
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_gameserver_thread()
    yield


app = FastAPI(
    title="AttckDef Revenge",
    description=DESCRIPTION,
    version="2.3.26",
    lifespan=lifespan,
)

app.include_router(routes_service.router)
app.include_router(routes_game.router)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def _page(request: Request, name: str, **ctx):
    return templates.TemplateResponse(
        request, name, {"tick_seconds": TICK_SECONDS, **ctx}
    )


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def console(request: Request):
    return _page(request, "console.html")


@app.get("/scoreboard", response_class=HTMLResponse, include_in_schema=False)
def scoreboard_page(request: Request):
    return _page(request, "scoreboard.html")


@app.get("/flag-ids", response_class=HTMLResponse, include_in_schema=False)
def flag_ids_page(request: Request):
    return _page(request, "flag_ids.html")


@app.get("/submit", response_class=HTMLResponse, include_in_schema=False)
def submit_page(request: Request):
    return _page(request, "submit.html")


@app.get("/attack-data", response_class=HTMLResponse, include_in_schema=False)
def attack_data_page(request: Request):
    pcap = ATTACK_DATA_DIR / "old_attack.pcap"
    size = f"{pcap.stat().st_size / (1024 * 1024):.1f} MiB" if pcap.exists() else None
    return _page(request, "attack_data.html", pcap_size=size)


@app.get("/attack-data/old_attack.pcap", include_in_schema=False)
def attack_data_download():
    pcap = ATTACK_DATA_DIR / "old_attack.pcap"
    return FileResponse(pcap, media_type="application/vnd.tcpdump.pcap",
                        filename="old_attack.pcap")


@app.get("/service", response_class=HTMLResponse, include_in_schema=False)
def service_index(request: Request):
    return _page(request, "service/index.html")


@app.get("/service/register", response_class=HTMLResponse, include_in_schema=False)
def service_register(request: Request):
    return _page(request, "service/register.html")


@app.get("/service/login", response_class=HTMLResponse, include_in_schema=False)
def service_login(request: Request):
    return _page(request, "service/login.html")


@app.get("/service/notes", response_class=HTMLResponse, include_in_schema=False)
def service_notes(request: Request):
    return _page(request, "service/notes.html")


@app.get("/service/new", response_class=HTMLResponse, include_in_schema=False)
def service_new(request: Request):
    return _page(request, "service/new.html")


@app.get("/service/share", response_class=HTMLResponse, include_in_schema=False)
def service_share(request: Request):
    return _page(request, "service/share.html")
