import time

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from . import ratelimit
from .auth import (
    AuthError,
    create_session,
    create_user,
    destroy_session,
    get_current_user,
    verify_user,
)
from .config import (
    JB3_NVH_YTS,
    KX7_MQR_WPL,
    MAX_ACTIVE_NOTES_PER_USER,
    MAX_CONTENT_LEN,
    MAX_TITLE_LEN,
    MAX_TOKEN_LEN,
)
from .models import (
    AuthResponse,
    CheckTokenResponse,
    CreateNoteRequest,
    CreateNoteResponse,
    LoginRequest,
    MeResponse,
    NoteOwned,
    NotePublic,
    RegisterRequest,
)
from .tick import (
    cleanup_expired_notes,
    count_active_notes_for_user,
    create_note,
    get_active_note,
    list_active_notes,
    list_notes_for_owner,
)

router = APIRouter(prefix="/api", tags=["notestore"])


@router.post("/register", summary="Create an account", response_model=AuthResponse)
def register(body: RegisterRequest):
    try:
        create_user(body.username, body.password)
    except AuthError as exc:
        return JSONResponse(status_code=400, content={"status": "REJECTED", "message": exc.detail})
    token = create_session(body.username)
    return {"status": "REGISTERED", "token": token, "username": body.username}


@router.post("/login", summary="Sign in and receive a bearer token", response_model=AuthResponse)
def login(body: LoginRequest):
    if not verify_user(body.username, body.password):
        return JSONResponse(
            status_code=401,
            content={"status": "DENIED", "message": "bad username or password"},
        )
    token = create_session(body.username)
    return {"status": "SIGNED_IN", "token": token, "username": body.username}


@router.get("/me", summary="Who am I", response_model=MeResponse)
def me(username: str = Depends(get_current_user)):
    return {"username": username, "active_notes": count_active_notes_for_user(username)}


@router.post("/logout", summary="Destroy the current session token", response_model=AuthResponse)
def logout(username: str = Depends(get_current_user), authorization: str = ""):
    token = authorization.removeprefix("Bearer ").strip()
    if token:
        destroy_session(token)
    return {"status": "SIGNED_OUT", "username": username}


@router.post(
    "/notes",
    summary="Store a new note",
    response_model=CreateNoteResponse,
    responses={429: {"description": "Active-note quota reached."}},
)
def create(body: CreateNoteRequest, username: str = Depends(get_current_user)):
    cleanup_expired_notes()
    if count_active_notes_for_user(username) >= MAX_ACTIVE_NOTES_PER_USER:
        return JSONResponse(
            status_code=429,
            content={
                "status": "QUOTA",
                "message": f"Active-note quota reached ({MAX_ACTIVE_NOTES_PER_USER}). Notes expire after a few ticks.",
            },
        )
    note = create_note(
        owner_username=username,
        title=body.title[:MAX_TITLE_LEN],
        content=body.content[:MAX_CONTENT_LEN],
    )
    return {"status": "STORED", "note": note}


@router.get(
    "/notes",
    summary="Public note listing (tokens and contents are never listed)",
    response_model=list[NotePublic],
)
def notes(limit: int = Query(default=100, le=500)):
    cleanup_expired_notes()
    return list_active_notes(limit)


@router.get(
    "/notes/mine",
    summary="Your own notes — share tokens and contents included",
    response_model=list[NoteOwned],
)
def my_notes(username: str = Depends(get_current_user)):
    return list_notes_for_owner(username)


@router.get(
    "/notes/validate-token",
    summary="Type-ahead share-token check used by the share dialog",
    description=(
        "Checks a share token against a note. Rate-limited: after a few checks "
        "the caller must solve a math captcha before the next one."
    ),
    response_model=CheckTokenResponse,
    responses={
        404: {"model": CheckTokenResponse, "description": "Note not found."},
        429: {"description": "Captcha required before further checks."},
    },
)
def validate_token(
    note_id: str = Query(..., description="The note identifier."),
    token: str = Query(..., description="The share token to check.", max_length=MAX_TOKEN_LEN),
    captcha_id: str = Query(default="", description="Captcha challenge id, when demanded."),
    captcha_answer: str = Query(default="", description="Answer to the captcha challenge."),
    username: str = Depends(get_current_user),
):
    captcha_solved = False
    if ratelimit.needs_captcha(username):
        if captcha_id or captcha_answer:
            if not ratelimit.verify(captcha_id, captcha_answer):
                return JSONResponse(
                    status_code=403,
                    content={
                        "status": "CAPTCHA_FAILED",
                        "message": "Wrong or expired captcha. Solve the new one.",
                        **ratelimit.challenge(),
                    },
                )
            ratelimit.reset(username)
            captcha_solved = True
        else:
            return JSONResponse(
                status_code=429,
                content={
                    "status": "CAPTCHA_REQUIRED",
                    "message": "Too many checks. Solve the captcha, then resend with captcha_id and captcha_answer.",
                    **ratelimit.challenge(),
                },
            )

    note = get_active_note(note_id)
    if note is None:
        return JSONResponse(
            status_code=404,
            content={"status": "NOTE_NOT_FOUND", "message": "No such note."},
        )

    submitted = token
    on_file = note["token"]
    ack = {"status": "OK", "message": "Request processed."}

    def _ack(delay: float) -> JSONResponse:
        time.sleep(delay)
        return JSONResponse(status_code=200, content=dict(ack))

    def _release() -> JSONResponse:
        body = dict(ack)
        body["content"] = note["content"]
        return JSONResponse(status_code=200, content=body)

    if not submitted:
        return _ack(JB3_NVH_YTS)

    if not captcha_solved:
        ratelimit.record_verdict(username)

    if submitted == on_file:
        return _release()

    if on_file.startswith(submitted):
        return _ack(KX7_MQR_WPL)

    return _ack(JB3_NVH_YTS)


@router.get(
    "/notes/{note_id}",
    summary="Public metadata for one note (no token, no content)",
    response_model=NotePublic,
    responses={404: {"description": "Note not found."}},
)
def note_detail(note_id: str):
    note = get_active_note(note_id)
    if note is None:
        return JSONResponse(
            status_code=404,
            content={"status": "NOTE_NOT_FOUND", "message": "No such note on the active listing."},
        )
    return {
        k: note[k]
        for k in ("tick_id", "owner_username", "note_id", "title", "created_at", "expires_at")
    }
