from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=False, unique=True)
    role: Mapped[str] = mapped_column(nullable=False)


class ChatMessage(db.Model):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    sender: Mapped[str] = mapped_column(nullable=False)
    attachments: Mapped[str] = mapped_column(nullable=True)


class Announcement(db.Model):
    __tablename__ = "announcements"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[str] = mapped_column(nullable=False)
    sender: Mapped[str] = mapped_column(nullable=False)  # Sender username
    receiver: Mapped[str] = mapped_column(nullable=False)  # Receiver username
    title: Mapped[str] = mapped_column(nullable=False)  # Announcement title
    content: Mapped[str] = mapped_column(nullable=False)
