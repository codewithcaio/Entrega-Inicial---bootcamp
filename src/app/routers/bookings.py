from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..config import BUSINESS_HOURS_END, BUSINESS_HOURS_START
from ..database import get_write_db
from ..services import booking_service

router = APIRouter(prefix="/api/v1/bookings", tags=["bookings"])


@router.post("", response_model=schemas.BookingOut, status_code=201)
def create_booking(payload: schemas.BookingCreate, db: Session = Depends(get_write_db)):
    # RN07 — sala e usuário precisam existir antes de qualquer outra checagem
    room = db.get(models.Room, payload.room_id)
    if room is None:
        raise HTTPException(status_code=404, detail=f"Sala {payload.room_id} não encontrada.")

    user = db.get(models.User, payload.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Usuário {payload.user_id} não encontrado.")

    try:
        booking_service.validate_interval(payload.start_time, payload.end_time)
        booking_service.validate_not_in_past(payload.start_time, datetime.now(timezone.utc).replace(tzinfo=None))
        booking_service.validate_business_hours(
            payload.start_time, payload.end_time, BUSINESS_HOURS_START, BUSINESS_HOURS_END
        )
        booking_service.validate_capacity(payload.attendees_count, room.capacity)
    except booking_service.BusinessRuleViolation as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    existing = db.execute(
        select(models.Booking).where(
            models.Booking.room_id == payload.room_id,
            models.Booking.status == models.BookingStatus.CONFIRMED,
        )
    ).scalars().all()
    existing_intervals = [
        booking_service.BookingInterval(start=b.start_time, end=b.end_time) for b in existing
    ]

    if booking_service.has_conflict(existing_intervals, payload.start_time, payload.end_time):
        raise HTTPException(
            status_code=409,
            detail="A sala já está reservada nesse horário (conflito com outra reserva confirmada).",
        )

    booking = models.Booking(
        room_id=payload.room_id,
        user_id=payload.user_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        attendees_count=payload.attendees_count,
        status=models.BookingStatus.CONFIRMED,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/{booking_id}", status_code=204)
def cancel_booking(booking_id: int, db: Session = Depends(get_write_db)):
    booking = db.get(models.Booking, booking_id)
    if booking is None:
        # RN06 — cancelar reserva inexistente é erro real
        raise HTTPException(status_code=404, detail=f"Reserva {booking_id} não encontrada.")

    # RN06 — cancelar uma reserva já cancelada é idempotente (no-op), não é erro
    if booking.status != models.BookingStatus.CANCELLED:
        booking.status = models.BookingStatus.CANCELLED
        db.commit()
    return None
