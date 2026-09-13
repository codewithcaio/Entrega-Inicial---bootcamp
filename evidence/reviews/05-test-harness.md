# Revisão formal — Test Harness

PR original: #5 (feature/test-harness), mesclada sem aprovação formal registrada antes do
merge. Esta PR reabre o escopo para revisão explícita.

## Escopo revisado
- tests/: conftest.py (fixtures), test_booking_conflicts.py, test_rooms.py, test_users.py,
  test_bookings.py, test_edge_cases.py, test_revision.py
- scripts/run_tests.py: harness multiplataforma, evidências salvas em evidence/tests/
- Cobertura: 100% em services/, 94% no total (ver evidence/tests/)

## Checklist do revisor
- [ ] Suite cobre os casos de RN01-RN07 e as regressões de docs/REFINEMENTS.md
- [ ] Harness roda igual em Docker e localmente (scripts/run_tests.py)
- [ ] Aprovado antes do merge (ver aba Files changed desta PR)
