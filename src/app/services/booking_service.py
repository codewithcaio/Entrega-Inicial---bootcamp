"""Regras de negócio de reservas — SPEC.md seção 4.4 (RN01-RN07).

Módulo intencionalmente puro (sem FastAPI, sem SQLAlchemy — ver docs/adr/0003). Recebe e
devolve apenas tipos nativos do Python (datetime, dataclass simples), para que a suíte de
testes de unidade rode inteira em memória, sem banco de dados nem servidor HTTP.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta

MIN_DURATION = timedelta(minutes=15)
MAX_DURATION = timedelta(hours=8)


@dataclass(frozen=True)
class BookingInterval:
    """Representação mínima de uma reserva confirmada, usada só para checar conflito."""

    start: datetime
    end: datetime


class BusinessRuleViolation(ValueError):
    """Erro levantado quando uma regra de negócio (RNxx) é violada.

    Os routers capturam essa exceção e traduzem para HTTP 422 (ou 409, no caso de conflito
    de horário — ver ConflictError abaixo), preservando a mensagem específica (RNF05).
    """


class ConflictError(BusinessRuleViolation):
    """RN01 — sobreposição de horário na mesma sala."""


def validate_interval(start: datetime, end: datetime) -> None:
    """RN02 — start < end, duração mínima de 15min e máxima de 8h."""
    if start >= end:
        raise BusinessRuleViolation("O horário de início deve ser anterior ao horário de fim.")

    duration = end - start
    if duration < MIN_DURATION:
        raise BusinessRuleViolation(
            f"A reserva deve durar pelo menos {int(MIN_DURATION.total_seconds() // 60)} minutos."
        )
    if duration > MAX_DURATION:
        raise BusinessRuleViolation(
            f"A reserva não pode durar mais que {int(MAX_DURATION.total_seconds() // 3600)} horas."
        )


def validate_not_in_past(start: datetime, now: datetime) -> None:
    """RN05 — não é permitido reservar um horário que já passou."""
    if start < now:
        raise BusinessRuleViolation("Não é possível criar uma reserva em um horário no passado.")


def validate_business_hours(
    start: datetime, end: datetime, hours_start: time, hours_end: time
) -> None:
    """RN03 — start e end devem estar dentro do expediente do MESMO dia."""
    if start.date() != end.date():
        raise BusinessRuleViolation(
            "A reserva deve começar e terminar no mesmo dia, dentro do expediente."
        )
    if start.time() < hours_start or end.time() > hours_end:
        raise BusinessRuleViolation(
            f"Horário fora do expediente ({hours_start.strftime('%H:%M')}"
            f"–{hours_end.strftime('%H:%M')})."
        )


def validate_capacity(attendees_count: int, room_capacity: int) -> None:
    """RN04 — número de participantes entre 1 e a capacidade da sala."""
    if attendees_count < 1:
        raise BusinessRuleViolation("O número de participantes deve ser pelo menos 1.")
    if attendees_count > room_capacity:
        raise BusinessRuleViolation(
            f"Número de participantes ({attendees_count}) excede a capacidade da sala "
            f"({room_capacity})."
        )


def has_conflict(
    existing_bookings: list[BookingInterval], new_start: datetime, new_end: datetime
) -> bool:
    """RN01 — True se [new_start, new_end) intercepta algum intervalo já existente.

    Convenção de intervalo semiaberto [start, end): uma reserva terminando às 15:00 não
    conflita com uma começando às 15:00 (back-to-back é permitido).
    """
    for existing in existing_bookings:
        if new_start < existing.end and existing.start < new_end:
            return True
    return False


def compute_availability(
    existing_bookings: list[BookingInterval],
    day: date,
    hours_start: time,
    hours_end: time,
) -> list[BookingInterval]:
    """RN01/RN03 combinadas — devolve os intervalos livres dentro do expediente do dia.

    `existing_bookings` deve conter apenas reservas CONFIRMED daquele dia, já ordenadas ou
    não (a função ordena internamente).
    """
    day_start = datetime.combine(day, hours_start)
    day_end = datetime.combine(day, hours_end)

    busy = sorted(existing_bookings, key=lambda b: b.start)

    free_slots: list[BookingInterval] = []
    cursor = day_start
    for booking in busy:
        if booking.start > cursor:
            free_slots.append(BookingInterval(start=cursor, end=booking.start))
        cursor = max(cursor, booking.end)

    if cursor < day_end:
        free_slots.append(BookingInterval(start=cursor, end=day_end))

    return free_slots
