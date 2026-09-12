"""Casos de borda end-to-end (via API), ligados diretamente a docs/REFINEMENTS.md.

Cada teste aqui referencia o item de refinamento ou a regra de negócio (RNxx) que motivou o
caso, para manter rastreabilidade com docs/SPEC.md.
"""
from __future__ import annotations

from datetime import timedelta

from tests.conftest import future_slot, iso


def _create_booking(client, room_id, user_id, start, end, attendees=2):
    return client.post(
        "/api/v1/bookings",
        json={
            "room_id": room_id,
            "user_id": user_id,
            "start_time": iso(start),
            "end_time": iso(end),
            "attendees_count": attendees,
        },
    )


# ---------- R-001 (docs/REFINEMENTS.md) — cancelamento ----------

def test_cancel_nonexistent_returns_404(client):
    response = client.delete("/api/v1/bookings/12345")
    assert response.status_code == 404


def test_cancel_already_cancelled_is_idempotent(client, room_factory, user_factory):
    room = room_factory()
    user = user_factory()
    start, end = future_slot(hour=10)
    booking = _create_booking(client, room["id"], user["id"], start, end).json()

    first_cancel = client.delete(f"/api/v1/bookings/{booking['id']}")
    second_cancel = client.delete(f"/api/v1/bookings/{booking['id']}")

    assert first_cancel.status_code == 204
    assert second_cancel.status_code == 204  # no-op, não é erro


# ---------- R-002 (docs/REFINEMENTS.md) — expediente nos dois limites ----------

def test_booking_ending_after_business_hours_rejected(client, room_factory, user_factory):
    room = room_factory()
    user = user_factory()
    start, _ = future_slot(hour=19, duration_hours=0)
    start = start.replace(minute=30)
    end = start + timedelta(hours=1)  # termina 20:30, depois do expediente (20:00)

    response = _create_booking(client, room["id"], user["id"], start, end)
    assert response.status_code == 422


def test_booking_starting_before_business_hours_rejected(client, room_factory, user_factory):
    room = room_factory()
    user = user_factory()
    start, end = future_slot(hour=6, duration_hours=1)  # começa antes das 08:00

    response = _create_booking(client, room["id"], user["id"], start, end)
    assert response.status_code == 422


def test_booking_within_business_hours_at_the_edges_is_accepted(client, room_factory, user_factory):
    room = room_factory()
    user = user_factory()
    start, end = future_slot(hour=19, duration_hours=1)  # 19:00-20:00, exatamente no limite

    response = _create_booking(client, room["id"], user["id"], start, end)
    assert response.status_code == 201


# ---------- Outros edge cases das regras de negócio ----------

def test_booking_in_the_past_rejected(client, room_factory, user_factory):
    room = room_factory()
    user = user_factory()
    from datetime import datetime

    start = datetime.utcnow() - timedelta(days=1)
    end = start + timedelta(hours=1)

    response = _create_booking(client, room["id"], user["id"], start, end)
    assert response.status_code == 422


def test_booking_shorter_than_minimum_duration_rejected(client, room_factory, user_factory):
    room = room_factory()
    user = user_factory()
    start, _ = future_slot(hour=10)
    end = start + timedelta(minutes=5)

    response = _create_booking(client, room["id"], user["id"], start, end)
    assert response.status_code == 422


def test_booking_longer_than_maximum_duration_rejected(client, room_factory, user_factory):
    room = room_factory()
    user = user_factory()
    start, _ = future_slot(hour=8)
    end = start + timedelta(hours=9)

    response = _create_booking(client, room["id"], user["id"], start, end)
    assert response.status_code == 422


def test_back_to_back_bookings_in_same_room_are_both_accepted(client, room_factory, user_factory):
    """RN01 usa intervalo semiaberto [start, end): reservas encostadas não conflitam."""
    room = room_factory()
    user = user_factory()
    start, end = future_slot(hour=10, duration_hours=1)

    first = _create_booking(client, room["id"], user["id"], start, end)
    second = _create_booking(client, room["id"], user["id"], end, end + timedelta(hours=1))

    assert first.status_code == 201
    assert second.status_code == 201


def test_same_time_different_rooms_both_accepted(client, room_factory, user_factory):
    room_a = room_factory(name="Sala A")
    room_b = room_factory(name="Sala B")
    user = user_factory()
    start, end = future_slot(hour=10)

    response_a = _create_booking(client, room_a["id"], user["id"], start, end)
    response_b = _create_booking(client, room_b["id"], user["id"], start, end)

    assert response_a.status_code == 201
    assert response_b.status_code == 201


def test_zero_attendees_rejected(client, room_factory, user_factory):
    room = room_factory(capacity=8)
    user = user_factory()
    start, end = future_slot(hour=10)

    response = _create_booking(client, room["id"], user["id"], start, end, attendees=0)
    assert response.status_code == 422
