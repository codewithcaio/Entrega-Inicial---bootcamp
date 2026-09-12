"""Testes de integração de reservas (RF04-RF11) via TestClient + SQLite em memória.

Casos de borda mais finos (limites de horário, cancelamento idempotente etc.) ficam em
test_edge_cases.py — aqui cobrimos os caminhos principais descritos na SPEC.md seção 5.
"""
from __future__ import annotations

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


def test_create_booking_success(client, room_factory, user_factory):
    room = room_factory(capacity=8)
    user = user_factory()
    start, end = future_slot(hour=10)

    response = _create_booking(client, room["id"], user["id"], start, end)
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "CONFIRMED"
    assert body["room_id"] == room["id"]
    assert body["user_id"] == user["id"]


def test_create_booking_room_not_found_returns_404(client, user_factory):
    user = user_factory()
    start, end = future_slot(hour=10)
    response = _create_booking(client, 9999, user["id"], start, end)
    assert response.status_code == 404


def test_create_booking_user_not_found_returns_404(client, room_factory):
    room = room_factory()
    start, end = future_slot(hour=10)
    response = _create_booking(client, room["id"], 9999, start, end)
    assert response.status_code == 404


def test_create_booking_conflicting_time_returns_409(client, room_factory, user_factory):
    room = room_factory(capacity=8)
    user = user_factory()
    start, end = future_slot(hour=10)

    first = _create_booking(client, room["id"], user["id"], start, end)
    assert first.status_code == 201

    second = _create_booking(client, room["id"], user["id"], start, end)
    assert second.status_code == 409


def test_create_booking_exceeding_capacity_returns_422(client, room_factory, user_factory):
    room = room_factory(capacity=4)
    user = user_factory()
    start, end = future_slot(hour=10)

    response = _create_booking(client, room["id"], user["id"], start, end, attendees=5)
    assert response.status_code == 422


def test_cancel_booking_success(client, room_factory, user_factory):
    room = room_factory()
    user = user_factory()
    start, end = future_slot(hour=10)

    created = _create_booking(client, room["id"], user["id"], start, end).json()
    response = client.delete(f"/api/v1/bookings/{created['id']}")
    assert response.status_code == 204


def test_cancelled_slot_can_be_rebooked(client, room_factory, user_factory):
    """Depois de cancelar, o mesmo horário deve voltar a ficar disponível (RN01 só considera
    reservas CONFIRMED)."""
    room = room_factory()
    user = user_factory()
    start, end = future_slot(hour=10)

    first = _create_booking(client, room["id"], user["id"], start, end).json()
    client.delete(f"/api/v1/bookings/{first['id']}")

    second = _create_booking(client, room["id"], user["id"], start, end)
    assert second.status_code == 201


def test_list_room_bookings_for_day(client, room_factory, user_factory):
    room = room_factory()
    user = user_factory()
    start, end = future_slot(hour=10)
    _create_booking(client, room["id"], user["id"], start, end)

    response = client.get(f"/api/v1/rooms/{room['id']}/bookings", params={"date": start.date().isoformat()})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_room_availability(client, room_factory, user_factory):
    room = room_factory()
    user = user_factory()
    start, end = future_slot(hour=10, duration_hours=1)
    _create_booking(client, room["id"], user["id"], start, end)

    response = client.get(f"/api/v1/rooms/{room['id']}/availability", params={"date": start.date().isoformat()})
    assert response.status_code == 200
    slots = response.json()
    # o horário reservado (10h-11h) não deve aparecer como slot livre
    for slot in slots:
        slot_start_hour = int(slot["start"][11:13])
        slot_end_hour = int(slot["end"][11:13])
        assert not (slot_start_hour <= 10 < slot_end_hour)


def test_list_user_bookings(client, room_factory, user_factory):
    room = room_factory()
    user = user_factory()
    start, end = future_slot(hour=10)
    _create_booking(client, room["id"], user["id"], start, end)

    response = client.get(f"/api/v1/users/{user['id']}/bookings")
    assert response.status_code == 200
    assert len(response.json()) == 1
