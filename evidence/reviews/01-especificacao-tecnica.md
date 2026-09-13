# Revisão formal — Especificação Técnica (SDD)

PR original: #1 (feature/especificacao-tecnica), mesclada sem aprovação formal registrada
antes do merge. Esta PR reabre o escopo para revisão explícita, sem alterar o conteúdo já
validado.

## Escopo revisado
- docs/SPEC.md: requisitos funcionais (RF01-RF11) e não funcionais (RNF01-RNF06)
- Entidades: Room, User, Booking
- Regras de negócio RN01-RN07 (intervalo válido, não reservar no passado, horário comercial,
  capacidade vs. participantes, conflito de horário)
- Contratos de API (secao 5 do SPEC.md) conferidos contra src/app/schemas.py

## Checklist do revisor
- [ ] RF/RNF ainda refletem o sistema implementado
- [ ] RN01-RN07 sem ambiguidade
- [ ] Contratos de API batem com schemas.py
- [ ] Aprovado antes do merge (ver aba Files changed desta PR)
