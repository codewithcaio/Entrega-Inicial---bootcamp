"""Modelos SQLAlchemy — espelham as entidades da SPEC.md seção 4."""
from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class BookingStatus(str, enum.Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String(120), nullable=False)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="room")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="user")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    attendees_count: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus), nullable=False, default=BookingStatus.CONFIRMED
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    room: Mapped["Room"] = relationship(back_populates="bookings")
    user: Mapped["User"] = relationship(back_populates="bookings")
