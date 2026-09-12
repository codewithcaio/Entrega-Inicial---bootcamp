from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db, get_write_db

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("", response_model=schemas.UserOut, status_code=201)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_write_db)):
    existing = db.execute(select(models.User).where(models.User.email == payload.email)).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=409, detail=f"Já existe um usuário com o e-mail '{payload.email}'.")

    user = models.User(name=payload.name, email=payload.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.execute(select(models.User)).scalars().all()


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Usuário {user_id} não encontrado.")
    return user


@router.get("/{user_id}/bookings", response_model=list[schemas.BookingOut])
def list_user_bookings(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Usuário {user_id} não encontrado.")
    return db.execute(
        select(models.Booking).where(models.Booking.user_id == user_id)
    ).scalars().all()
