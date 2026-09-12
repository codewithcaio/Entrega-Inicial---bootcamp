"""Testes de integração dos endpoints de sala (RF01, RF02) via TestClient + SQLite em memória."""
from __future__ import annotations


def test_create_room_success(client):
    response = client.post(
        "/api/v1/rooms", json={"name": "Sala Azul", "capacity": 4, "location": "2º andar"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Sala Azul"
    assert body["capacity"] == 4
    assert "id" in body


def test_create_room_duplicate_name_returns_409(client, room_factory):
    room_factory(name="Sala Azul")
    response = client.post(
        "/api/v1/rooms", json={"name": "Sala Azul", "capacity": 10, "location": "outro andar"}
    )
    assert response.status_code == 409


def test_create_room_invalid_capacity_returns_422(client):
    response = client.post(
        "/api/v1/rooms", json={"name": "Sala Inválida", "capacity": 0, "location": "x"}
    )
    assert response.status_code == 422


def test_list_rooms_returns_all_created(client, room_factory):
    room_factory(name="Sala A")
    room_factory(name="Sala B")
    response = client.get("/api/v1/rooms")
    assert response.status_code == 200
    names = {r["name"] for r in response.json()}
    assert names == {"Sala A", "Sala B"}


def test_get_room_by_id_success(client, room_factory):
    room = room_factory(name="Sala C")
    response = client.get(f"/api/v1/rooms/{room['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Sala C"


def test_get_room_not_found_returns_404(client):
    response = client.get("/api/v1/rooms/9999")
    assert response.status_code == 404
