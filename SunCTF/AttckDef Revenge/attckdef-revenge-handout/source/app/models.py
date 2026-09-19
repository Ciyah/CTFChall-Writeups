from typing import Optional

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    status: str
    token: Optional[str] = None
    username: Optional[str] = None
    message: Optional[str] = None


class MeResponse(BaseModel):
    username: str
    active_notes: int


class CreateNoteRequest(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)


class NotePublic(BaseModel):
    tick_id: int
    owner_username: str
    note_id: str
    title: str
    created_at: str
    expires_at: str


class NoteOwned(NotePublic):
    token: str
    content: str


class CreateNoteResponse(BaseModel):
    status: str
    note: NoteOwned


class CheckTokenResponse(BaseModel):
    status: str
    message: str
    content: Optional[str] = None


class SubmitRequest(BaseModel):
    flag_id: str
    flag: str


class SubmitResponse(BaseModel):
    status: str
    reason: Optional[str] = None
    points: Optional[int] = None
    flag: Optional[str] = None
    message: str


class FlagIdsResponse(BaseModel):
    service: str
    ticks: list[dict]


class GameStatusResponse(BaseModel):
    tick_seconds: int
    current_tick: int
    seconds_remaining: int
    grace_seconds: int
    services: list[dict]


class ErrorResponse(BaseModel):
    status: Optional[str] = None
    detail: Optional[str] = None
    message: Optional[str] = None
