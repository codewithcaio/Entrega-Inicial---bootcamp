# ADR-0004: Uso de agente de IA (Claude Code) no fluxo SDD

- **Status**: Aceito
- **Data**: 2026-09-11
- **Decisores**: equipe do projeto

## Contexto
O bootcamp exige orquestração documentada de pelo menos uma ferramenta de geração de código
assistida por IA, integrada ao fluxo Spec-Driven Development: a especificação (`SPEC.md`) deve
vir antes do código, e o código deve ser gerado/validado a partir dela — não o contrário.

## Decisão
Usar **Claude Code** como agente de geração de código, com as regras de contexto do projeto
registradas em `.claude/CLAUDE.md` (versionado no repositório). O fluxo adotado foi:

1. Escrever/ajustar `docs/SPEC.md` (contratos e regras de negócio) manualmente/com apoio do
   agente.
2. Pedir ao agente para gerar o código de `services/`, `routers/` e `models` a partir da
   especificação, sem inventar regra que não estivesse documentada.
3. Pedir ao agente para gerar a suíte de testes cobrindo RN01–RN07 e os edge cases.
4. Rodar os testes; qualquer falha ou ambiguidade encontrada durante os testes gerou um ajuste
   na SPEC.md, registrado em `docs/REFINEMENTS.md`, antes de alterar o código.

## Alternativas consideradas
- **Cursor**: também compatível com o fluxo SDD (`.cursorrules`); não usado nesta fase para
  manter um único agente documentado, mas a estrutura de `.claude/CLAUDE.md` é equivalente e
  portável para `.cursorrules` se o grupo trocar de ferramenta depois.
- **Gerar código livremente sem spec prévia**: rejeitado por contrariar o objetivo da entrega
  (SDD) — o risco é o agente "inventar" regra de negócio não combinada com o grupo.

## Consequências
- Toda regra de negócio implementada é rastreável até um item da `SPEC.md` (RF/RNF/RN).
- Divergências entre o que foi pedido e o que os testes revelaram como necessário ficam
  registradas em `docs/REFINEMENTS.md`, em vez de silenciosamente reescritas.
- Custo: exige disciplina do grupo para não pular a etapa de atualizar a spec antes de pedir
  código novo ao agente.
