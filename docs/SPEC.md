# Especificação Técnica — SalaFácil (Sistema de Reserva de Salas de Reunião)

Especificação técnica no fluxo SDD (Spec-Driven Development), consolidada para a
Entrega 2 em 15/10/2026. A versão v1.2 mantém os contratos da v1.1 e acrescenta
rastreabilidade dos refinamentos e critérios de validação. Não introduz novos
endpoints nem altera as regras de negócio. Mudanças de contrato devem atualizar
este documento e ser registradas em [REFINEMENTS.md](REFINEMENTS.md).

## 1. Visão Geral do Problema

Empresas com escritórios híbridos costumam ter poucas salas de reunião e muita gente tentando
reservar o mesmo horário, o que gera conflitos resolvidos "na marra" (WhatsApp, planilha,
post-it na porta). O **SalaFácil** é uma API REST que centraliza a reserva de salas de reunião
de um escritório, garantindo que:

- duas reservas nunca se sobrepõem na mesma sala;
- reservas respeitam capacidade da sala e horário de expediente;
- qualquer pessoa do time consegue consultar disponibilidade e histórico de reservas.

O sistema **não** cobre (fora de escopo nesta fase): autenticação/autorização real (usamos um
identificador simples de usuário), notificações por e-mail, recorrência de reservas, e
múltiplos escritórios/fusos horários — ver `docs/REFINEMENTS.md` para o motivo desses cortes.

## 2. Requisitos Funcionais (RF)

| ID | Requisito |
|----|-----------|
| RF01 | O sistema deve permitir cadastrar uma sala de reunião (nome, capacidade, localização). |
| RF02 | O sistema deve permitir listar todas as salas e consultar uma sala específica. |
| RF03 | O sistema deve permitir cadastrar um usuário (nome, e-mail). |
| RF04 | O sistema deve permitir criar uma reserva para uma sala, informando usuário, sala, horário de início e fim, e número de participantes. |
| RF05 | O sistema deve rejeitar a criação de uma reserva que se sobreponha, na mesma sala, a uma reserva já existente e ativa. |
| RF06 | O sistema deve rejeitar reservas fora do horário de expediente configurado (`BUSINESS_HOURS_START`–`BUSINESS_HOURS_END`). |
| RF07 | O sistema deve rejeitar reservas cujo número de participantes exceda a capacidade da sala. |
| RF08 | O sistema deve permitir cancelar uma reserva existente (cancelamento lógico — a reserva deixa de ocupar o horário, mas o registro é preservado). |
| RF09 | O sistema deve permitir listar as reservas de uma sala em um intervalo de datas. |
| RF10 | O sistema deve permitir listar as reservas de um usuário. |
| RF11 | O sistema deve permitir consultar a disponibilidade de uma sala (quais horários estão livres num dia). |

## 3. Requisitos Não-Funcionais (RNF)

| ID | Requisito |
|----|-----------|
| RNF01 | A API deve responder em formato JSON e seguir os códigos de status HTTP convencionais (2xx sucesso, 4xx erro de cliente/regra de negócio, 5xx erro inesperado). |
| RNF02 | A detecção de conflito de horário deve ser uma função pura e isolada (`services/booking_service.py`), testável sem subir a API HTTP. |
| RNF03 | O ambiente deve ser reprodutível via Docker (`docker-compose up`) sem passos manuais além de definir variáveis de ambiente. |
| RNF04 | O projeto deve ter cobertura de testes automatizados para as regras de negócio críticas (conflito de horário, capacidade, expediente) — meta mínima: 80% de cobertura em `services/`. |
| RNF05 | Erros de validação devem retornar mensagem clara o suficiente para debug (não apenas "erro 400"). |
| RNF06 | O tempo de resposta de qualquer endpoint em ambiente local não deve depender de I/O externo (o SQLite é local; não há chamadas de rede de terceiros). |

## 4. Entidades e Regras de Negócio

### 4.1 Room (Sala)
- `id`, `name` (único), `capacity` (inteiro > 0), `location`.

### 4.2 User (Usuário)
- `id`, `name`, `email` (único, formato validado).

### 4.3 Booking (Reserva)
- `id`, `room_id`, `user_id`, `start_time`, `end_time`, `attendees_count`, `status`
  (`CONFIRMED` | `CANCELLED`), `created_at`.

### 4.4 Regras de negócio (invariantes)
1. **RN01 — Sem sobreposição**: para a mesma sala, não podem existir duas reservas com
   `status = CONFIRMED` cujos intervalos `[start_time, end_time)` se interceptem. Reservas
   `CANCELLED` não contam para essa checagem.
2. **RN02 — Intervalo válido**: `start_time` deve ser estritamente menor que `end_time`.
   Duração mínima: 15 minutos. Duração máxima: 8 horas.
3. **RN03 — Expediente**: `start_time` e `end_time` devem estar dentro da janela de expediente
   do mesmo dia (não é permitido reservar da noite para a madrugada atravessando o expediente).
4. **RN04 — Capacidade**: `attendees_count` deve ser `>= 1` e `<= room.capacity`.
5. **RN05 — Sem reserva no passado**: `start_time` não pode ser anterior ao instante atual da
   requisição.
6. **RN06 — Cancelamento idempotente**: cancelar uma reserva já cancelada não é erro (é
   no-op), mas cancelar uma reserva inexistente retorna 404.
7. **RN07 — Sala/usuário devem existir**: criar reserva para `room_id` ou `user_id`
   inexistente retorna 404 antes das demais checagens de negócio. A validação estrutural do corpo ocorre primeiro e pode retornar 422.

## 5. Contratos de Entrada/Saída (API)

Prefixo base: `/api/v1`

### `POST /rooms`
Request:
```json
{ "name": "Sala Vermelha", "capacity": 8, "location": "3º andar" }
```
Response `201`:
```json
{ "id": 1, "name": "Sala Vermelha", "capacity": 8, "location": "3º andar" }
```
Erros: `409` nome duplicado; `422` capacidade inválida.

### `GET /rooms` / `GET /rooms/{id}`
Response `200`: lista ou objeto Room. `404` se `id` não existe.

### `POST /users`
Request: `{ "name": "Caio Diniz", "email": "caio@example.com" }`
Response `201`: objeto User. Erros: `409` e-mail duplicado; `422` e-mail inválido.

### `POST /bookings`
Request:
```json
{
  "room_id": 1,
  "user_id": 1,
  "start_time": "2026-09-15T14:00:00",
  "end_time": "2026-09-15T15:00:00",
  "attendees_count": 5
}
```
Response `201`: objeto Booking com `status: "CONFIRMED"`.
Erros:
- `404` sala ou usuário não existe (RN07)
- `409` conflito de horário (RN01)
- `422` intervalo inválido (RN02), fora de expediente (RN03), capacidade excedida (RN04),
  reserva no passado (RN05) — corpo do erro traz `{"detail": "<motivo específico>"}`.

### `DELETE /bookings/{id}`
Response `204` (cancelamento). `404` se a reserva não existe.

### `GET /rooms/{id}/bookings`
Aceita `date=YYYY-MM-DD` para um dia OU `start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
para um intervalo inclusivo. Retorna `200` com reservas `CONFIRMED` que interceptam o
intervalo, ordenadas por início e ID. Retorna `422` para filtros ausentes, incompletos,
misturados ou invertidos; `404` para sala inexistente.

### `GET /rooms/{id}/availability?date=YYYY-MM-DD`
Response `200`: lista de intervalos livres dentro do expediente naquele dia, calculada a
partir das reservas `CONFIRMED` existentes.

### `GET /users/{id}/bookings`
Response `200`: lista de reservas (todas, com `status`) do usuário.

## 6. Decomposição em Unidades (componentes testáveis isoladamente)

```
booking_service.py
  ├─ has_conflict(existing_bookings, new_start, new_end) -> bool          [pura, sem DB]
  ├─ validate_business_hours(start, end, hours_start, hours_end) -> None  [levanta ValueError]
  ├─ validate_capacity(attendees, room_capacity) -> None
  ├─ validate_interval(start, end) -> None
  └─ compute_availability(existing_bookings, day, hours_start, hours_end) -> list[slot]

routers/rooms.py      -> depende apenas de database + schemas
routers/users.py      -> depende apenas de database + schemas
routers/bookings.py   -> orquestra booking_service + repositórios de rooms/users/bookings
```

Essa separação existe para permitir testar toda a lógica de negócio (a parte que mais muda e
mais quebra) sem precisar subir a aplicação HTTP nem o banco — os testes de `booking_service`
usam apenas objetos Python em memória.

## 7. Critérios de aceite originais (Entrega 1)

Os critérios abaixo são preservados como requisitos da primeira fase, sem tratar
o checkbox antigo como evidência de homologação. Os resultados observados estão
nos relatórios de execução; a homologação depende da revisão humana correspondente.

- Endpoints de salas, usuários e reservas conforme os contratos da seção 5.
- RN01-RN07 cobertas por testes automatizados.
- Docker Compose sobe a API em `http://localhost:8000/docs`.
- Harness executa todos os testes e preserva os resultados e o código de saída.

## 8. Contratos complementares da v1.1

- Horários de expediente, filtros de data e respostas usam UTC. Datas recebidas sem offset
  são UTC; datas com offset são normalizadas para UTC antes das regras e persistidas sem offset.
  Não há configuração de múltiplos fusos/escritórios nesta fase.
- O início do expediente deve ser anterior ao fim; configuração inválida impede a inicialização.
- As escritas SQLite adquirem `BEGIN IMMEDIATE` antes de ler os dados da decisão. Reservas
  concorrentes no mesmo horário devem produzir uma criação (201) e um conflito (409).
  Se a espera pelo banco exceder o timeout de 30s, responde 503 com `Retry-After: 1`.
- O banco suportado nesta versão é SQLite. A migração requer nova decisão de concorrência.
- O harness é `python scripts/run_tests.py`; gera logs, JUnit e cobertura de toda `app`,
  verifica a meta de 80% para services e preserva código de saída não zero em caso de falha.

## 9. Rastreabilidade e validação da Entrega 2 (v1.2)

O ciclo de refinamento parte de uma falha observada, uma ambiguidade ou um feedback
da equipe. A decisão deve ser explicitada antes de ajustar o contrato; depois são
atualizados implementação e testes, seguidos da execução e revisão humana do PR.
O histórico detalhado está em [REFINEMENTS.md](REFINEMENTS.md).

| Contrato | Decisão consolidada | Referência de teste |
|---|---|---|
| RN01 / RF05 | Intervalos semiabertos; reservas adjacentes não conflitam | `test_booking_conflicts.py::TestHasConflict`; `test_entrega2_edges.py::test_adjacent_bookings_leave_no_false_gap` |
| RN02 | Duração mínima de 15 minutos e máxima de 8 horas, ambas inclusivas | `test_entrega2_edges.py::test_api_accepts_exact_duration_limits`; `test_api_rejects_invalid_duration_without_persisting` |
| RN03 | Início e fim no expediente do mesmo dia | `test_edge_cases.py::test_booking_ending_after_business_hours_rejected`; `test_booking_conflicts.py::TestValidateBusinessHours` |
| RN04 | Participantes entre 1 e a capacidade da sala, inclusive | `test_entrega2_edges.py::test_api_accepts_exact_room_capacity`; `test_bookings.py::test_create_booking_exceeding_capacity_returns_422` |
| RN05 | Recusar início no passado, comparando instantes UTC | `test_edge_cases.py::test_booking_in_the_past_rejected`; `test_revision.py::test_offset_dates_are_normalized_and_conflict` |
| RN06 / RF08 | Cancelamento idempotente; registro permanece no histórico e libera a disponibilidade | `test_entrega2_edges.py::test_cancel_restores_availability_without_other_room_interference`; `test_user_history_keeps_cancelled_and_excludes_other_users` |
| RN07 | Validação estrutural antes da busca; entidades ausentes antes das regras de negócio | `test_entrega2_edges.py::test_structural_validation_precedes_missing_entity`; `test_missing_entity_precedes_business_rule_validation` |
| RF09 | Dia ou intervalo inclusivo; rejeitar filtros ausentes, misturados ou invertidos | `test_revision.py::test_range_includes_both_dates_excludes_cancelled_and_other_rooms`; `test_invalid_range_rejected` |
| RF11 | Apenas reservas confirmadas da sala afetam a disponibilidade | `test_entrega2_edges.py::test_full_business_day_has_no_availability`; `test_cancel_restores_availability_without_other_room_interference` |
| Configuração e concorrência | `.env` respeita precedência; escrita adquire lock antes da decisão | `test_revision.py::test_dotenv_loaded_and_explicit_environment_wins`; `test_concurrent_booking_only_one_confirmed` |

### Evidências e critérios de aceitação

- Todos os testes executados devem passar, sem ocultar falhas ou avisos.
- A meta RNF04 permanece 80% de cobertura de serviços. Passagem de 100% dos testes
  não significa cobertura de 100% do código.
- O relatório de [testes de borda](TESTES_BORDA_ENTREGA2.md) registra uma execução
  local com 95/95 aprovados, cobertura total de 94,51% e serviços em 100%.
- As mudanças de depreciação preservam UTC sem offset e a geração de `created_at`
  por inserção; ver [comparativo](AVISOS_DEPRECACAO.md).
- Os 17 testes novos passaram na implementação existente. Eles ampliam a validação,
  mas não demonstram, por si, uma nova falha lógica ou mudança de requisito.
- A execução Docker final da versão integrada deve ser registrada na Issue #34.
  Resultados locais e resultados Docker devem ser identificados separadamente.
- Cada PR deve indicar escopo, critérios de aceitação, validação e revisão do outro
  integrante antes do merge. Não há aprovação retroativa dos PRs originais #1-#7.

### Limites preservados

Autenticação/autorização real, recorrência, notificações e múltiplos escritórios
continuam fora do escopo definido na seção 1. A aprovação da suíte não é evidência
de segurança para exposição pública, de teste de carga ou de ausência total de bugs.
