"""Fixtures compartilhadas: banco SQLite em memória, isolado por teste (ver docs/adr/0002)."""
from __future__ import annotations

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session, monkeypatch):
    # O startup dos testes não deve abrir/criar o banco de desenvolvimento.
    monkeypatch.setattr("app.main.init_db", lambda: None)
    def _override_get_db():
        try:
            yield db_session
        finally:
            db_session.rollback()

    app.dependency_overrides[get_db] = _override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture()
def room_factory(client):
    def _make(name="Sala Vermelha", capacity=8, location="3º andar"):
        response = client.post(
            "/api/v1/rooms", json={"name": name, "capacity": capacity, "location": location}
        )
        assert response.status_code == 201, response.text
        return response.json()

    return _make


@pytest.fixture()
def user_factory(client):
    def _make(name="Caio Diniz", email="caio@example.com"):
        response = client.post("/api/v1/users", json={"name": name, "email": email})
        assert response.status_code == 201, response.text
        return response.json()

    return _make


def future_slot(hour: int = 10, duration_hours: int = 1, days_ahead: int = 1):
    """Devolve (start, end) datetimes no futuro, sempre dentro do expediente 08:00-20:00,
    calculados a partir de 'agora' para que os testes nunca fiquem obsoletos (RN05).
    """
    base_day = (datetime.utcnow() + timedelta(days=days_ahead)).replace(
        hour=hour, minute=0, second=0, microsecond=0
    )
    return base_day, base_day + timedelta(hours=duration_hours)


def iso(dt: datetime) -> str:
    return dt.isoformat()
