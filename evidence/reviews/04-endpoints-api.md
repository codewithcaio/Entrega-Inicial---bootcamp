# Revisão formal — Endpoints da API

PR original: #4 (feature/endpoints-api), mesclada sem aprovação formal registrada antes do
merge. Esta PR reabre o escopo para revisão explícita.

## Escopo revisado
- src/app/routers/rooms.py, users.py, bookings.py — orquestração via FastAPI, sem regra de
  negócio embutida (regra fica em services/)
- Parâmetros start_date/end_date em rooms.py para consulta de disponibilidade por intervalo
- Contratos de request/resposta conferidos contra src/app/schemas.py

## Checklist do revisor
- [ ] Routers não implementam regra de negócio diretamente
- [ ] Endpoints batem com os contratos do docs/SPEC.md
- [ ] Aprovado antes do merge (ver aba Files changed desta PR)
