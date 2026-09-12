# Especificação Técnica — SalaFácil (Sistema de Reserva de Salas de Reunião)

Documento de especificação inicial (SDD — Spec-Driven Development). Esta é a versão v1.1,
usada como contrato para gerar os componentes, os testes e o harness de validação. Alterações
devem atualizar este documento e ser registradas em `docs/REFINEMENTS.md`.

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

## 7. Critérios de Aceite da Fase (Entrega 1)

- [ ] Endpoints de `rooms`, `users` e `bookings` implementados conforme contratos acima.
- [ ] RN01–RN07 cobertas por teste automatizado (ver `docs/EXECUTION_REPORT.md`).
- [ ] `docker-compose up` sobe a API em `http://localhost:8000/docs` sem passos manuais extras.
- [ ] Suíte de testes roda com `./scripts/run_tests.sh` e todos os testes passam.

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
