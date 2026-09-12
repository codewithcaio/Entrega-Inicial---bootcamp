# Relatório fornecido no ZIP original — histórico não revalidado

# Relatório de Execução do Test Harness — Entrega 1

Este relatório contém a saída **real** (não editada, apenas copiada) de duas execuções feitas
no ambiente de desenvolvimento antes desta entrega: (1) a suíte de testes automatizados via
`./scripts/run_tests.sh`, e (2) um teste manual "de fumaça" (smoke test) da API rodando de
verdade com `uvicorn`, exercitando os principais fluxos de sucesso e erro via `curl`.

> Ao reproduzir esta entrega, substitua estes logs pelos prints/logs gerados na *sua* máquina
> — ver `README.md` seção "Como gerar as evidências para o PDF do Moodle".

## 1. Ambiente em que os testes foram executados

```
Python: 3.11.15
Data/hora (UTC): 2026-09-11T19:16:06Z
Comando: ./scripts/run_tests.sh   (equivalente a: pytest -v --cov=app.services --cov=app.routers --cov-report=term-missing)
```

## 2. Saída completa da suíte de testes (pytest + cobertura)

```
== SalaFácil — Test Harness ==
Python: Python 3.11.15
Data/hora: 2026-09-11T19:16:06Z

============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-8.3.3, pluggy-1.6.0 -- /home/claude/meeting-room-booking/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/claude/meeting-room-booking
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.15.1, cov-5.0.0
collecting ... collected 65 items

tests/test_booking_conflicts.py::TestHasConflict::test_no_existing_bookings_never_conflicts PASSED [  1%]
tests/test_booking_conflicts.py::TestHasConflict::test_identical_interval_conflicts PASSED [  3%]
tests/test_booking_conflicts.py::TestHasConflict::test_new_booking_fully_inside_existing_conflicts PASSED [  4%]
tests/test_booking_conflicts.py::TestHasConflict::test_new_booking_fully_containing_existing_conflicts PASSED [  6%]
tests/test_booking_conflicts.py::TestHasConflict::test_partial_overlap_start_conflicts PASSED [  7%]
tests/test_booking_conflicts.py::TestHasConflict::test_partial_overlap_end_conflicts PASSED [  9%]
tests/test_booking_conflicts.py::TestHasConflict::test_back_to_back_end_equals_start_does_not_conflict PASSED [ 10%]
tests/test_booking_conflicts.py::TestHasConflict::test_back_to_back_before_does_not_conflict PASSED [ 12%]
tests/test_booking_conflicts.py::TestHasConflict::test_conflict_checked_against_multiple_existing_bookings PASSED [ 13%]
tests/test_booking_conflicts.py::TestValidateInterval::test_valid_interval_does_not_raise PASSED [ 15%]
tests/test_booking_conflicts.py::TestValidateInterval::test_end_before_start_raises PASSED [ 16%]
tests/test_booking_conflicts.py::TestValidateInterval::test_end_equal_start_raises PASSED [ 18%]
tests/test_booking_conflicts.py::TestValidateInterval::test_duration_below_minimum_raises PASSED [ 20%]
tests/test_booking_conflicts.py::TestValidateInterval::test_duration_exactly_minimum_is_valid PASSED [ 21%]
tests/test_booking_conflicts.py::TestValidateInterval::test_duration_above_maximum_raises PASSED [ 23%]
tests/test_booking_conflicts.py::TestValidateInterval::test_duration_exactly_maximum_is_valid PASSED [ 24%]
tests/test_booking_conflicts.py::TestValidateNotInPast::test_future_start_does_not_raise PASSED [ 26%]
tests/test_booking_conflicts.py::TestValidateNotInPast::test_past_start_raises PASSED [ 27%]
tests/test_booking_conflicts.py::TestValidateNotInPast::test_start_equal_now_is_valid PASSED [ 29%]
tests/test_booking_conflicts.py::TestValidateBusinessHours::test_inside_business_hours_does_not_raise PASSED [ 30%]
tests/test_booking_conflicts.py::TestValidateBusinessHours::test_start_before_opening_raises PASSED [ 32%]
tests/test_booking_conflicts.py::TestValidateBusinessHours::test_end_after_closing_raises PASSED [ 33%]
tests/test_booking_conflicts.py::TestValidateBusinessHours::test_ending_exactly_at_closing_is_valid PASSED [ 35%]
tests/test_booking_conflicts.py::TestValidateBusinessHours::test_spanning_two_days_raises PASSED [ 36%]
tests/test_booking_conflicts.py::TestValidateCapacity::test_within_capacity_does_not_raise PASSED [ 38%]
tests/test_booking_conflicts.py::TestValidateCapacity::test_exactly_at_capacity_is_valid PASSED [ 40%]
tests/test_booking_conflicts.py::TestValidateCapacity::test_above_capacity_raises PASSED [ 41%]
tests/test_booking_conflicts.py::TestValidateCapacity::test_zero_attendees_raises PASSED [ 43%]
tests/test_booking_conflicts.py::TestValidateCapacity::test_negative_attendees_raises PASSED [ 44%]
tests/test_booking_conflicts.py::TestComputeAvailability::test_no_bookings_whole_day_is_free PASSED [ 46%]
tests/test_booking_conflicts.py::TestComputeAvailability::test_single_booking_splits_day_in_two_slots PASSED [ 47%]
tests/test_booking_conflicts.py::TestComputeAvailability::test_booking_at_start_of_day_removes_first_slot PASSED [ 49%]
tests/test_booking_conflicts.py::TestComputeAvailability::test_booking_covering_whole_day_leaves_no_slots PASSED [ 50%]
tests/test_booking_conflicts.py::TestComputeAvailability::test_unordered_bookings_are_handled_correctly PASSED [ 52%]
tests/test_bookings.py::test_create_booking_success PASSED               [ 53%]
tests/test_bookings.py::test_create_booking_room_not_found_returns_404 PASSED [ 55%]
tests/test_bookings.py::test_create_booking_user_not_found_returns_404 PASSED [ 56%]
tests/test_bookings.py::test_create_booking_conflicting_time_returns_409 PASSED [ 58%]
tests/test_bookings.py::test_create_booking_exceeding_capacity_returns_422 PASSED [ 60%]
tests/test_bookings.py::test_cancel_booking_success PASSED               [ 61%]
tests/test_bookings.py::test_cancelled_slot_can_be_rebooked PASSED       [ 63%]
tests/test_bookings.py::test_list_room_bookings_for_day PASSED           [ 64%]
tests/test_bookings.py::test_get_room_availability PASSED                [ 66%]
tests/test_bookings.py::test_list_user_bookings PASSED                   [ 67%]
tests/test_edge_cases.py::test_cancel_nonexistent_returns_404 PASSED     [ 69%]
tests/test_edge_cases.py::test_cancel_already_cancelled_is_idempotent PASSED [ 70%]
tests/test_edge_cases.py::test_booking_ending_after_business_hours_rejected PASSED [ 72%]
tests/test_edge_cases.py::test_booking_starting_before_business_hours_rejected PASSED [ 73%]
tests/test_edge_cases.py::test_booking_within_business_hours_at_the_edges_is_accepted PASSED [ 75%]
tests/test_edge_cases.py::test_booking_in_the_past_rejected PASSED       [ 76%]
tests/test_edge_cases.py::test_booking_shorter_than_minimum_duration_rejected PASSED [ 78%]
tests/test_edge_cases.py::test_booking_longer_than_maximum_duration_rejected PASSED [ 80%]
tests/test_edge_cases.py::test_back_to_back_bookings_in_same_room_are_both_accepted PASSED [ 81%]
tests/test_edge_cases.py::test_same_time_different_rooms_both_accepted PASSED [ 83%]
tests/test_edge_cases.py::test_zero_attendees_rejected PASSED            [ 84%]
tests/test_rooms.py::test_create_room_success PASSED                     [ 86%]
tests/test_rooms.py::test_create_room_duplicate_name_returns_409 PASSED  [ 87%]
tests/test_rooms.py::test_create_room_invalid_capacity_returns_422 PASSED [ 89%]
tests/test_rooms.py::test_list_rooms_returns_all_created PASSED          [ 90%]
tests/test_rooms.py::test_get_room_by_id_success PASSED                  [ 92%]
tests/test_rooms.py::test_get_room_not_found_returns_404 PASSED          [ 93%]
tests/test_users.py::test_create_user_success PASSED                     [ 95%]
tests/test_users.py::test_create_user_duplicate_email_returns_409 PASSED [ 96%]
tests/test_users.py::test_create_user_invalid_email_returns_422 PASSED   [ 98%]
tests/test_users.py::test_get_user_not_found_returns_404 PASSED          [100%]

---------- coverage: platform linux, python 3.11.15-final-0 ----------
Name                                  Stmts   Miss  Cover   Missing
-------------------------------------------------------------------
src/app/routers/__init__.py               0      0   100%
src/app/routers/bookings.py              43      0   100%
src/app/routers/rooms.py                 49      2    96%   61, 69
src/app/routers/users.py                 32      3    91%   28, 36, 43
src/app/services/__init__.py              0      0   100%
src/app/services/booking_service.py      50      0   100%
-------------------------------------------------------------------
TOTAL                                   174      5    97%

======================== 65 passed, 1 warning in 1.55s =========================
EXIT_CODE=0
```

**Resumo**: 65/65 testes passaram (0 falhas, 0 erros). Cobertura de `services/` (a camada
crítica de regra de negócio, RNF04): **100%**. Cobertura total do projeto: **97%**.

## 3. Smoke test da API rodando de verdade (uvicorn + curl)

Além da suíte automatizada (que usa `TestClient`, sem precisar de um servidor de fato), a API
foi subida com `uvicorn` e exercitada via `curl` para confirmar que o binário real responde
como especificado — este é o mesmo processo que roda dentro do container Docker.

Log do servidor (`uvicorn app.main:app --host 0.0.0.0 --port 8000`):

```
INFO:     Started server process [1286]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:34124 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:34136 - "POST /api/v1/rooms HTTP/1.1" 201 Created
INFO:     127.0.0.1:34152 - "POST /api/v1/users HTTP/1.1" 201 Created
INFO:     127.0.0.1:34156 - "POST /api/v1/bookings HTTP/1.1" 201 Created
INFO:     127.0.0.1:34170 - "POST /api/v1/bookings HTTP/1.1" 409 Conflict
INFO:     127.0.0.1:34182 - "POST /api/v1/bookings HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:34190 - "GET /api/v1/rooms/1/availability?date=2026-09-12 HTTP/1.1" 200 OK
INFO:     127.0.0.1:34204 - "DELETE /api/v1/bookings/1 HTTP/1.1" 204 No Content
INFO:     127.0.0.1:34216 - "DELETE /api/v1/bookings/9999 HTTP/1.1" 404 Not Found
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
```

Respostas do cliente (`curl`), na ordem das chamadas acima:

```
### GET /health
{"status":"ok"}
HTTP_STATUS=200

### POST /api/v1/rooms
{"id":1,"name":"Sala Vermelha","capacity":8,"location":"3º andar"}
HTTP_STATUS=201

### POST /api/v1/users
{"id":1,"name":"Caio Diniz","email":"caio@example.com"}
HTTP_STATUS=201

### POST /api/v1/bookings (sucesso)
{"id":1,"room_id":1,"user_id":1,"start_time":"2026-09-12T10:00:00","end_time":"2026-09-12T11:00:00","attendees_count":5,"status":"CONFIRMED","created_at":"2026-09-11T19:16:28.449497"}
HTTP_STATUS=201

### POST /api/v1/bookings (conflito esperado -> 409)
{"detail":"A sala já está reservada nesse horário (conflito com outra reserva confirmada)."}
HTTP_STATUS=409

### POST /api/v1/bookings (capacidade excedida -> 422)
{"detail":"Número de participantes (99) excede a capacidade da sala (8)."}
HTTP_STATUS=422

### GET /api/v1/rooms/1/availability
[{"start":"2026-09-12T08:00:00","end":"2026-09-12T10:00:00"},{"start":"2026-09-12T11:00:00","end":"2026-09-12T20:00:00"}]
HTTP_STATUS=200

### DELETE /api/v1/bookings/1
HTTP_STATUS=204

### DELETE /api/v1/bookings/9999 (inexistente -> 404)
{"detail":"Reserva 9999 não encontrada."}
HTTP_STATUS=404
```

Esse resultado confirma, num servidor real (não só em teste): criação de sala/usuário,
criação de reserva com sucesso, rejeição de conflito de horário (RN01/409), rejeição de
capacidade excedida (RN04/422), cálculo de disponibilidade excluindo o horário ocupado, e
cancelamento (204) com idempotência/404 corretos (RN06).

## 4. Sobre a execução via Docker

O `Dockerfile` e o `docker-compose.yml` deste repositório foram escritos e revisados
manualmente (ver `docs/adr/0002-persistencia-sqlite.md`), mas **não puderam ser
`build`ados/executados no ambiente onde este relatório foi gerado**, por não haver um daemon
Docker disponível ali. A suíte de testes e o smoke test acima rodaram diretamente no ambiente
Python local (mesma versão de dependências do `requirements.txt`).

**Antes de gerar o PDF final para o Moodle, cada grupo deve rodar `docker compose up --build`
na própria máquina e capturar o print/log real dessa execução** — é isso que o item 4 da
entrega pede especificamente ("logs comprobatórios do pipeline de testes rodando no ambiente
padronizado"). O comando equivalente para rodar os testes dentro do container é:

```bash
docker compose run --rm api ./scripts/run_tests.sh
```

Ver `README.md` para o passo a passo completo.
