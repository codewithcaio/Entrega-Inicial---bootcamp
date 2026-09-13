# Revisão formal — Modelo de Dados e Regras de Negócio

PR original: #3 (feature/modelo-e-regras-negocio), mesclada sem aprovação formal registrada
antes do merge. Esta PR reabre o escopo para revisão explícita.

## Escopo revisado
- src/app/models.py: Room, User, Booking (+ BookingStatus: CONFIRMED/CANCELLED)
- src/app/services/booking_service.py: validate_interval, validate_not_in_past,
  validate_business_hours, validate_capacity, has_conflict, compute_availability
- Normalização de datas para UTC (src/app/schemas.py, field_validator)
- Proteção de concorrência SQLite com BEGIN IMMEDIATE (src/app/database.py)

## Checklist do revisor
- [ ] Regras de negócio isoladas em services/ (testáveis sem FastAPI/DB)
- [ ] Normalização de datas e lock de concorrência cobertos por teste
- [ ] Aprovado antes do merge (ver aba Files changed desta PR)
