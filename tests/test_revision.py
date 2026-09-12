"""Regressões R-004–R-007: UTC, filtros, configuração e escrita concorrente."""
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta, timezone
import importlib.util
from pathlib import Path
import threading

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import sessionmaker

from app import models
from app.database import Base, get_db
from app.main import app
from tests.conftest import future_slot


def payload(room_id, user_id, start, end):
    return {"room_id": room_id, "user_id": user_id, "start_time": start.isoformat(),
            "end_time": end.isoformat(), "attendees_count": 2}


@pytest.mark.parametrize("offset", [0, -3, 5])
def test_offset_dates_are_normalized_and_conflict(client, room_factory, user_factory, offset):
    room, user = room_factory(), user_factory()
    start, end = future_slot()
    tz = timezone(timedelta(hours=offset))
    aware_start = start.replace(tzinfo=timezone.utc).astimezone(tz)
    aware_end = end.replace(tzinfo=timezone.utc).astimezone(tz)
    result = client.post("/api/v1/bookings", json=payload(room['id'], user['id'], aware_start, aware_end))
    assert result.status_code == 201, result.text
    assert result.json()['start_time'] == start.isoformat()
    duplicate = client.post("/api/v1/bookings", json=payload(room['id'], user['id'], start, end))
    assert duplicate.status_code == 409


def test_mixed_offset_and_naive_date(client, room_factory, user_factory):
    room, user = room_factory(), user_factory()
    start, end = future_slot()
    result = client.post("/api/v1/bookings", json=payload(room['id'], user['id'], start.replace(tzinfo=timezone.utc), end))
    assert result.status_code == 201, result.text


def test_range_includes_both_dates_excludes_cancelled_and_other_rooms(client, room_factory, user_factory):
    room, user = room_factory(), user_factory()
    other = room_factory(name="Outra sala")
    ids = []
    for day in [1, 2, 3, 4]:
        start, end = future_slot(days_ahead=day)
        result = client.post('/api/v1/bookings', json=payload(room['id'], user['id'], start, end))
        assert result.status_code == 201
        ids.append(result.json()['id'])
    client.delete(f'/api/v1/bookings/{ids[1]}')
    start, end = future_slot(days_ahead=1)
    assert client.post('/api/v1/bookings', json=payload(other['id'], user['id'], start, end)).status_code == 201
    result = client.get(f"/api/v1/rooms/{room['id']}/bookings", params={
        'start_date': start.date().isoformat(),
        'end_date': (start.date() + timedelta(days=2)).isoformat()})
    assert result.status_code == 200
    assert [b['id'] for b in result.json()] == [ids[0], ids[2]]


@pytest.mark.parametrize('params', [
    {}, {'start_date': '2026-09-15'}, {'end_date': '2026-09-15'},
    {'start_date': '2026-09-16', 'end_date': '2026-09-15'},
    {'date': '2026-09-15', 'start_date': '2026-09-15'}, {'date': 'inválida'}])
def test_invalid_range_rejected(client, room_factory, params):
    room = room_factory()
    assert client.get(f"/api/v1/rooms/{room['id']}/bookings", params=params).status_code == 422


def test_dotenv_loaded_and_explicit_environment_wins(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[1]
    copied = tmp_path / 'src' / 'app' / 'config.py'
    copied.parent.mkdir(parents=True)
    copied.write_text((root / 'src/app/config.py').read_text(encoding='utf-8'), encoding='utf-8')
    (tmp_path / '.env').write_text('BUSINESS_HOURS_START=09:15\nBUSINESS_HOURS_END=18:30\nDATABASE_URL=sqlite:///custom.db\n')
    monkeypatch.delenv('BUSINESS_HOURS_START', raising=False)
    monkeypatch.delenv('DATABASE_URL', raising=False)
    monkeypatch.setenv('BUSINESS_HOURS_END', '19:00')
    spec = importlib.util.spec_from_file_location('config_under_test', copied)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.BUSINESS_HOURS_START.isoformat() == '09:15:00'
    assert module.BUSINESS_HOURS_END.isoformat() == '19:00:00'
    assert module.DATABASE_URL == 'sqlite:///custom.db'


def test_concurrent_booking_only_one_confirmed(tmp_path, monkeypatch):
    """Duas conexões reais no MESMO arquivo; ambas tentam reservar juntas."""
    engine = create_engine(f"sqlite:///{(tmp_path / 'concurrent.db').as_posix()}",
                           connect_args={'check_same_thread': False, 'timeout': 10})
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    with sessions() as db:
        db.add(models.Room(id=1, name='Concorrente', capacity=8, location='A'))
        db.add(models.User(id=1, name='Teste', email='test@example.com'))
        db.commit()
    start_together = threading.Barrier(2)

    @event.listens_for(engine, 'before_cursor_execute')
    def synchronize(connection, cursor, statement, parameters, context, executemany):
        if statement == 'BEGIN IMMEDIATE':
            start_together.wait(timeout=10)

    def override_db():
        with sessions() as db:
            yield db

    monkeypatch.setattr('app.main.init_db', lambda: None)
    app.dependency_overrides[get_db] = override_db
    start, end = future_slot()
    data = payload(1, 1, start, end)

    def reserve():
        with TestClient(app) as client:
            return client.post('/api/v1/bookings', json=data).status_code

    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            statuses = list(pool.map(lambda _: reserve(), range(2)))
        assert sorted(statuses) == [201, 409]
        with sessions() as db:
            assert len(db.scalars(select(models.Booking)).all()) == 1
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
