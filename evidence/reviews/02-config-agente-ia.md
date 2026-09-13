# Revisão formal — Configuração do Agente de IA

PR original: #2 (feature/config-agente-ia), mesclada sem aprovação formal registrada antes
do merge. Esta PR reabre o escopo para revisão explícita.

## Escopo revisado
- CLAUDE.md / AGENTS.md: regras do fluxo SDD para os agentes de IA
- Regra: nunca implementar comportamento fora do docs/SPEC.md
- Regra: ambiguidade resolvida deve virar entrada em docs/REFINEMENTS.md
- Regra: lógica de negócio isolada em src/app/services/ (fora de routers/main)
- Regra: nenhum commit direto em main/develop, sempre via feature branch + PR

## Checklist do revisor
- [ ] Regras cobrem os agentes usados no projeto (Claude Code e Codex)
- [ ] Regras compatíveis com o fluxo de branches do repositório
- [ ] Aprovado antes do merge (ver aba Files changed desta PR)
