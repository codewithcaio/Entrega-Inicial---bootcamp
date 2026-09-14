# Entrega 1 — SalaFácil

**MODELO PARA PREENCHER E EXPORTAR COMO PDF. Não é a entrega final completa.**

## Identificação
Disciplina/turma: Bootcamp III. Data da entrega: 13/09/2026.

| Nome completo | RA |
|---|---|
| Gabriel Vieira Souza | 22552446 |
| Caio da Silva Diniz | 22552405 |

Repositório público GitHub ou com acesso aos professores: https://github.com/codewithcaio/Entrega-Inicial---bootcamp

## Projeto e especificação
API de reserva de salas com cadastro de salas/usuários, validação de capacidade e expediente,
prevenção de conflitos, cancelamento e consulta de disponibilidade/ocupação.
Requisitos e contratos em docs/SPEC.md; refinamentos em docs/REFINEMENTS.md; decisões em docs/adr/.

## Ambiente e ferramentas
Python 3.12, FastAPI, SQLAlchemy, SQLite, pytest e pytest-cov. Dockerfile e Compose incluídos.
Claude Code é declarado na documentação original. Gabriel Vieira Souza utilizou o **OpenAI Codex no aplicativo desktop**,
com leitura/edição de arquivos e terminal; não foi uma sessão de Codex CLI.
Evidências: [pedido e README](../evidence/ai/codex-readme.png) e
[resultado no relatório](../evidence/ai/codex-relatorio.png).

## Execução do harness
Local: `python scripts/run_tests.py`.
Docker: `docker compose up --build --wait`, seguido de
`docker compose run --rm api python scripts/run_tests.py`.

Execução real por Gabriel no Docker Desktop/WSL2, em 12/09/2026 às 20:09:34 UTC:
**78 testes aprovados, 0 falhas, 55 avisos de depreciação, 1,67 s, cobertura total
de 93,60% (94% arredondado), services 100% e código de saída 0**.
Os 1,67 s são a duração do pytest. Os avisos foram preservados e não são falhas.
Logs e metadados em [evidence/tests/20260912T200934816939Z/](../evidence/tests/20260912T200934816939Z/);
detalhes em [EXECUTION_REPORT.md](EXECUTION_REPORT.md).

## Evidências disponíveis para o PDF
1. [Resultado dos testes Docker](../evidence/docker/tests-docker.png).
2. [Construção e container Healthy](../evidence/docker/build-healthy.png).
3. [Actions aprovado](../evidence/github/actions-sucesso.png) e [execução posterior na main](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/actions/runs/34778178346).
4. [Interação com o Codex](../evidence/ai/codex-readme.png) e [relatório produzido](../evidence/ai/codex-relatorio.png).
5. [Issues](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/issues?q=is%3Aissue+is%3Aclosed) e [PR #24](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/24).

## Governança
Divisão de tarefas e responsáveis: Caio da Silva Diniz — especificação técnica (#8),
configuração do agente de IA (#9), endpoints da API (#11), ambiente Docker e CI (#13).
Gabriel Vieira Souza — models/schemas e regras de negócio (#10), suíte de testes e test
harness (#12), governança do projeto (#14).

Issues/Project: quadro GitHub Projects "SalaFácil — Entrega 1", 7 issues (uma por área),
todas movidas para Done, com responsável atribuído em cada uma (ver acima).

Os PRs #1–#7 foram mesclados sem aprovação formal prévia registrada. Os PRs #16–#22
acrescentaram revisões documentais posteriores; suas aprovações não são retroativas aos
merges originais. O PR #23 atualizou o modelo de submissão com aprovação de Gabriel.
No [PR #24](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/24), Caio aprovou em 13/09/2026 às
19:34:31 UTC, antes do merge de develop na main às 19:35:50 UTC.

## Conferência final
Conferir a legibilidade das imagens e os links no PDF de entrega. Cada integrante deve
submeter o PDF conforme o enunciado. Esta atualização modifica os documentos-fonte e
adiciona evidências ao repositório; não modifica nem reexporta o PDF já preparado.
