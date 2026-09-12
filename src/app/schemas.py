"""Schemas Pydantic — contratos de entrada/saída (SPEC.md seção 5)."""
from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# ---------- Room ----------
class RoomCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    capacity: int = Field(gt=0)
    location: str = Field(min_length=1, max_length=120)


class RoomOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    capacity: int
    location: str


# ---------- User ----------
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str


# ---------- Booking ----------
class BookingCreate(BaseModel):
    room_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    attendees_count: int = Field(gt=0)

    @field_validator("start_time", "end_time")
    @classmethod
    def normalize_utc(cls, value: datetime) -> datetime:
        """Datas sem offset são UTC; datas com offset são convertidas para UTC."""
        if value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    attendees_count: int
    status: str
    created_at: datetime


class AvailabilitySlot(BaseModel):
    start: datetime
    end: datetime
