from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import init_db
from .routers import bookings, rooms, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="SalaFácil — API de Reserva de Salas de Reunião",
    description="Ver docs/SPEC.md no repositório para a especificação completa (RF/RNF/RN).",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


app.include_router(rooms.router)
app.include_router(users.router)
app.include_router(bookings.router)
