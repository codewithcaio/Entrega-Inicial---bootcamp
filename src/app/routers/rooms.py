from __future__ import annotations

from datetime import date as date_type
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..config import BUSINESS_HOURS_END, BUSINESS_HOURS_START
from ..database import get_db, get_write_db
from ..services import booking_service

router = APIRouter(prefix="/api/v1/rooms", tags=["rooms"])


@router.post("", response_model=schemas.RoomOut, status_code=201)
def create_room(payload: schemas.RoomCreate, db: Session = Depends(get_write_db)):
    existing = db.execute(select(models.Room).where(models.Room.name == payload.name)).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=409, detail=f"Já existe uma sala chamada '{payload.name}'.")

    room = models.Room(name=payload.name, capacity=payload.capacity, location=payload.location)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@router.get("", response_model=list[schemas.RoomOut])
def list_rooms(db: Session = Depends(get_db)):
    return db.execute(select(models.Room)).scalars().all()


@router.get("/{room_id}", response_model=schemas.RoomOut)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.get(models.Room, room_id)
    if room is None:
        raise HTTPException(status_code=404, detail=f"Sala {room_id} não encontrada.")
    return room


def _confirmed_bookings_for_day(db: Session, room_id: int, day: date_type) -> list[models.Booking]:
    day_start = datetime.combine(day, datetime.min.time())
    day_end = datetime.combine(day, datetime.max.time())
    return db.execute(
        select(models.Booking).where(
            models.Booking.room_id == room_id,
            models.Booking.status == models.BookingStatus.CONFIRMED,
            models.Booking.start_time <= day_end,
            models.Booking.end_time >= day_start,
        )
    ).scalars().all()


@router.get("/{room_id}/bookings", response_model=list[schemas.BookingOut])
def list_room_bookings(
    room_id: int,
    date: date_type | None = Query(None),
    start_date: date_type | None = Query(None),
    end_date: date_type | None = Query(None),
    db: Session = Depends(get_db),
):
    room = db.get(models.Room, room_id)
    if room is None:
        raise HTTPException(status_code=404, detail=f"Sala {room_id} não encontrada.")
    if date is not None:
        if start_date is not None or end_date is not None:
            raise HTTPException(status_code=422, detail="Use date OU start_date e end_date.")
        start_date = end_date = date
    if start_date is None or end_date is None or start_date > end_date:
        raise HTTPException(status_code=422, detail="Informe date ou um intervalo válido com start_date e end_date.")
    range_start = datetime.combine(start_date, datetime.min.time())
    range_end = datetime.combine(end_date, datetime.max.time())
    return db.execute(select(models.Booking).where(
        models.Booking.room_id == room_id,
        models.Booking.status == models.BookingStatus.CONFIRMED,
        models.Booking.start_time <= range_end,
        models.Booking.end_time > range_start,
    ).order_by(models.Booking.start_time, models.Booking.id)).scalars().all()


@router.get("/{room_id}/availability", response_model=list[schemas.AvailabilitySlot])
def get_room_availability(room_id: int, date: date_type = Query(...), db: Session = Depends(get_db)):
    room = db.get(models.Room, room_id)
    if room is None:
        raise HTTPException(status_code=404, detail=f"Sala {room_id} não encontrada.")

    bookings = _confirmed_bookings_for_day(db, room_id, date)
    intervals = [
        booking_service.BookingInterval(start=b.start_time, end=b.end_time) for b in bookings
    ]
    free_slots = booking_service.compute_availability(
        intervals, date, BUSINESS_HOURS_START, BUSINESS_HOURS_END
    )
    return [schemas.AvailabilitySlot(start=slot.start, end=slot.end) for slot in free_slots]
