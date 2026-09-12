# ADR-0003: Separar regras de negócio em serviço puro para testabilidade

- **Status**: Aceito
- **Data**: 2026-09-11
- **Decisores**: equipe do projeto

## Contexto
As regras mais arriscadas do sistema (RN01–RN07 na `SPEC.md`) são exatamente as que mais
mudam durante a especificação e as que mais geram bugs sutis (comparação de intervalos de
tempo, limites de borda). Testar essas regras só "de fora para dentro", via requisições HTTP
contra um banco real, deixaria a suíte lenta e os testes de edge case difíceis de escrever.

## Decisão
Isolar toda a lógica de decisão (conflito de horário, validação de expediente, capacidade,
cálculo de disponibilidade) em funções puras dentro de `src/app/services/booking_service.py`,
sem nenhuma dependência de banco de dados ou de FastAPI. Os routers apenas orquestram: buscam
dados, chamam o serviço, e traduzem o resultado em resposta HTTP.

## Alternativas consideradas
- **Validação dentro dos routers/endpoints**: mais rápido de escrever no início, mas mistura
  regra de negócio com camada HTTP e obriga todo teste a passar por `TestClient` — mais lento
  e mais difícil de cobrir edge cases combinatórios (ex.: todas as combinações de sobreposição
  de intervalo).
- **Validação dentro dos models SQLAlchemy**: acopla a regra de negócio ao ORM, dificultando
  testar sem banco.

## Consequências
- A suíte inclui testes de unidade rápidos (`test_booking_conflicts.py`, sem banco/HTTP),
  integração e casos de borda (`test_bookings.py`, `test_edge_cases.py`, `test_rooms.py`,
  `test_users.py`, via `TestClient` + SQLite em memória). `test_revision.py` inclui
  concorrência com conexões independentes ao mesmo arquivo SQLite temporário.
- Cobertura de `services/` pode ser medida isoladamente (meta RNF04: 80%+).
- Custo: uma camada extra de indireção (routers chamando services) que precisa ser mantida
  consistente com a SPEC.md a cada mudança de regra.
