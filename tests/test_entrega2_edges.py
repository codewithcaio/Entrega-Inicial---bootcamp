"""Issue #28: limites e efeitos observáveis pela API, conforme SPEC RN01-RN07."""
from datetime import datetime, timedelta

import pytest

from tests.conftest import future_slot


def reserve(client, room_id, user_id, start, end, attendees=2):
    return client.post('/api/v1/bookings', json={
        'room_id': room_id, 'user_id': user_id,
        'start_time': start.isoformat(), 'end_time': end.isoformat(),
        'attendees_count': attendees,
    })


def availability(client, room_id, day):
    response = client.get(f'/api/v1/rooms/{room_id}/availability',
                          params={'date': day.isoformat()})
    assert response.status_code == 200, response.text
    return [(datetime.fromisoformat(slot['start']), datetime.fromisoformat(slot['end']))
            for slot in response.json()]


@pytest.mark.parametrize('duration', [
    timedelta(0), timedelta(minutes=-1), timedelta(minutes=15, microseconds=-1),
    timedelta(hours=8, microseconds=1),
], ids=['zero', 'fim-antes-inicio', 'abaixo-15-min', 'acima-8-h'])
def test_api_rejects_invalid_duration_without_persisting(
    client, room_factory, user_factory, duration,
):
    """RN02/RNF05: rejeição HTTP específica e nenhuma reserva persistida."""
    room, user = room_factory(), user_factory()
    start, _ = future_slot(hour=8)
    response = reserve(client, room['id'], user['id'], start, start + duration)
    assert response.status_code == 422, response.text
    assert isinstance(response.json()['detail'], str)
    assert response.json()['detail']
    bookings = client.get(f"/api/v1/users/{user['id']}/bookings")
    assert bookings.status_code == 200
    assert bookings.json() == []


@pytest.mark.parametrize('duration', [timedelta(minutes=15), timedelta(hours=8)],
                         ids=['minimo-exato', 'maximo-exato'])
def test_api_accepts_exact_duration_limits(client, room_factory, user_factory, duration):
    """RN02/RN03: limites inclusivos também devem funcionar pela API."""
    room, user = room_factory(), user_factory()
    start, _ = future_slot(hour=8)
    end = start + duration
    response = reserve(client, room['id'], user['id'], start, end)
    assert response.status_code == 201, response.text
    assert response.json()['start_time'] == start.isoformat()
    assert response.json()['end_time'] == end.isoformat()


def test_api_accepts_exact_room_capacity(client, room_factory, user_factory):
    """RN04: a capacidade é um limite inclusivo, não exclusivo."""
    room, user = room_factory(capacity=8), user_factory()
    start, end = future_slot()
    response = reserve(client, room['id'], user['id'], start, end, attendees=8)
    assert response.status_code == 201, response.text
    assert response.json()['attendees_count'] == 8


@pytest.mark.parametrize('missing', ['room', 'user'])
def test_missing_entity_precedes_business_rule_validation(
    client, room_factory, user_factory, missing,
):
    """RN07: entidade ausente retorna 404 antes do intervalo invertido."""
    room, user = room_factory(), user_factory()
    start, _ = future_slot()
    response = reserve(client, 99999 if missing == 'room' else room['id'],
                       99999 if missing == 'user' else user['id'],
                       start, start - timedelta(minutes=15))
    assert response.status_code == 404, response.text


def test_structural_validation_precedes_missing_entity(client):
    """SPEC seção 4.4: corpo inválido é rejeitado antes da busca de entidades."""
    start, end = future_slot()
    response = reserve(client, 99999, 99999, start, end, attendees=0)
    assert response.status_code == 422, response.text
    assert any(error['loc'][-1] == 'attendees_count' for error in response.json()['detail'])


def test_cancel_restores_availability_without_other_room_interference(
    client, room_factory, user_factory,
):
    """RF08/RF11: cancelar libera a sala; reservas de outra sala não a ocupam."""
    room, other, user = room_factory(), room_factory(name='Outra'), user_factory()
    start, end = future_slot(hour=10)
    first = reserve(client, room['id'], user['id'], start, end)
    assert first.status_code == 201
    assert reserve(client, other['id'], user['id'], start, end).status_code == 201
    assert availability(client, room['id'], start.date()) == [
        (start.replace(hour=8), start), (end, start.replace(hour=20)),
    ]
    booking_id = first.json()['id']
    assert client.delete(f'/api/v1/bookings/{booking_id}').status_code == 204
    assert client.delete(f'/api/v1/bookings/{booking_id}').status_code == 204
    assert availability(client, room['id'], start.date()) == [
        (start.replace(hour=8), start.replace(hour=20)),
    ]


def test_adjacent_bookings_leave_no_false_gap(client, room_factory, user_factory):
    """RN01/RF11: reservas adjacentes não geram um intervalo livre de duração zero."""
    room, user = room_factory(), user_factory()
    start, middle = future_slot(hour=10)
    end = middle + timedelta(hours=1)
    assert reserve(client, room['id'], user['id'], start, middle).status_code == 201
    assert reserve(client, room['id'], user['id'], middle, end).status_code == 201
    assert availability(client, room['id'], start.date()) == [
        (start.replace(hour=8), start), (end, start.replace(hour=20)),
    ]


def test_full_business_day_has_no_availability(client, room_factory, user_factory):
    """RF11: reservas válidas de 8h e 4h podem ocupar todo o expediente."""
    room, user = room_factory(), user_factory()
    start, middle = future_slot(hour=8, duration_hours=8)
    end = start.replace(hour=20)
    assert reserve(client, room['id'], user['id'], start, middle).status_code == 201
    assert reserve(client, room['id'], user['id'], middle, end).status_code == 201
    assert availability(client, room['id'], start.date()) == []


@pytest.mark.parametrize('endpoint', [
    '/api/v1/rooms/99999/bookings', '/api/v1/rooms/99999/availability',
    '/api/v1/users/99999/bookings',
])
def test_missing_entity_read_endpoints_return_404(client, endpoint):
    start, _ = future_slot()
    response = client.get(endpoint, params={'date': start.date().isoformat()})
    assert response.status_code == 404, response.text


def test_user_history_keeps_cancelled_and_excludes_other_users(
    client, room_factory, user_factory,
):
    """RF08/RF10: cancelamento preserva histórico e a consulta isola o usuário."""
    room, user = room_factory(), user_factory()
    other = user_factory(name='Outro', email='outro@example.com')
    start, end = future_slot(hour=10)
    cancelled = reserve(client, room['id'], user['id'], start, end)
    assert cancelled.status_code == 201
    assert client.delete(f"/api/v1/bookings/{cancelled.json()['id']}").status_code == 204
    assert reserve(client, room['id'], other['id'], start, end).status_code == 201
    response = client.get(f"/api/v1/users/{user['id']}/bookings")
    assert response.status_code == 200
    assert [(item['id'], item['status']) for item in response.json()] == [
        (cancelled.json()['id'], 'CANCELLED'),
    ]
