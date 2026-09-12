"""Testes de integração dos endpoints de usuário (RF03) via TestClient + SQLite em memória."""
from __future__ import annotations


def test_create_user_success(client):
    response = client.post(
        "/api/v1/users", json={"name": "Ana Souza", "email": "ana@example.com"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Ana Souza"
    assert body["email"] == "ana@example.com"


def test_create_user_duplicate_email_returns_409(client, user_factory):
    user_factory(email="dup@example.com")
    response = client.post(
        "/api/v1/users", json={"name": "Outro Nome", "email": "dup@example.com"}
    )
    assert response.status_code == 409


def test_create_user_invalid_email_returns_422(client):
    response = client.post(
        "/api/v1/users", json={"name": "Sem Email Válido", "email": "não-é-email"}
    )
    assert response.status_code == 422


def test_get_user_not_found_returns_404(client):
    response = client.get("/api/v1/users/9999")
    assert response.status_code == 404
