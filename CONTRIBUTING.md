# Guia de Contribuição — Governança do Projeto

Este documento define como o grupo trabalha neste repositório: branches, Pull Requests, code
review e organização de tarefas. **Commits diretos em `main` ou `develop` são proibidos.**

## 1. Estrutura de branches

- **`main`**: sempre estável e "entregável". Só recebe merge vindo de `develop` (ou de uma
  `hotfix/*`, em caso de correção urgente), via Pull Request aprovado.
- **`develop`**: branch de integração. Reúne as features já revisadas que ainda vão compor a
  próxima entrega.
- **`feature/<descrição-curta>`**: uma branch por tarefa/issue, criada a partir de `develop`
  (ex.: `feature/endpoint-disponibilidade-sala`, `feature/validacao-capacidade`).
- **`hotfix/<descrição-curta>`**: correção urgente direto a partir de `main`, quando algo
  quebrado já está na branch estável.

Fluxo de uma tarefa:
```
develop --(cria)--> feature/minha-tarefa --(commits)--> PR para develop --(review + aprovação)--> merge
```
Periodicamente (a cada entrega/sprint), abre-se um PR de `develop` para `main`.

## 2. Pull Requests

Todo PR deve:
1. Ter um título claro referenciando a issue relacionada (ex.: `feat: valida capacidade da sala (#12)`).
2. Descrever o que mudou e por quê (ligar à `docs/SPEC.md` quando aplicável — qual RF/RNF/RN
   está sendo implementada).
3. Ser revisado por **pelo menos um outro membro do grupo** antes do merge — comentários e
   aprovação ficam registrados no histórico do PR (é isso que a Entrega 1 pede como evidência
   de "Code Review & PRs").
4. Passar pela suíte de testes (`./scripts/run_tests.sh`) antes de pedir review.
5. Ser mesclado com "Squash and merge" ou "Merge commit" (o grupo escolhe um padrão e mantém
   consistente) — nunca com force-push em cima do histórico compartilhado.

Sugestão de checklist para a descrição do PR (ver também `.github/PULL_REQUEST_TEMPLATE.md`):
- [ ] Código segue a `docs/SPEC.md` atual (ou a `docs/SPEC.md` foi atualizada junto)
- [ ] Testes novos/atualizados cobrindo a mudança
- [ ] `./scripts/run_tests.sh` passou localmente
- [ ] Sem regra de negócio nova sem entrada correspondente em `docs/REFINEMENTS.md`

## 3. Organização de tarefas (GitHub Projects/Issues)

1. Criar um **GitHub Project** (quadro Kanban: `To do` / `In progress` / `In review` / `Done`).
2. Cada requisito funcional/não-funcional da `docs/SPEC.md` vira pelo menos uma **Issue**
   (ex.: "RF05 — Rejeitar reserva sobreposta", "RNF04 — Cobertura de testes em services/").
3. Cada Issue é atribuída a um membro do grupo e linkada à branch/PR que a resolve (o GitHub
   faz esse link automaticamente se o PR mencionar `closes #<número da issue>`).
4. Isso é o que evidencia, para a correção, a "divisão de tarefas" e "decomposição do problema
   em tarefas independentes" pedida na Entrega 1.

## 4. Code review — o que revisar

- A mudança está de acordo com `docs/SPEC.md`? Se não, o PR deveria vir junto com uma mudança
  na spec (e, se for o caso, uma entrada em `docs/REFINEMENTS.md`).
- Regra de negócio nova está em `src/app/services/booking_service.py` (não dentro de um
  router) — ver `docs/adr/0003-estrategia-de-testes.md`.
- Existe teste cobrindo o caminho feliz **e** pelo menos um caso de borda?
- Mensagens de erro são específicas o suficiente para debug (RNF05)?

## 5. Uso de agentes de IA neste fluxo

Ver `.claude/CLAUDE.md` (ou `.cursorrules`). Qualquer código gerado por um agente de IA segue
as mesmas regras acima: vai para uma `feature/*`, abre PR, passa por review humano — o agente
não deve commitar direto em `develop`/`main`.
