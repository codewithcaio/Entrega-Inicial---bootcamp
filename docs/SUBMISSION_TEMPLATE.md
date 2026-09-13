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
Claude Code é declarado na documentação original. A revisão atual foi assistida pelo Codex
desktop com terminal; não foi uma sessão de Codex CLI. Evidência da ferramenta: PENDENTE anexar captura/registro.

## Execução do harness
Local: `python scripts/run_tests.py`.
Docker: `docker compose up --build --wait`, seguido de
`docker compose run --rm api python scripts/run_tests.py`.

Resultado local observado na revisão: 78 testes passaram; services 100%; app aproximadamente 94%.
Logs originais em evidence/tests/ e resumo em docs/EXECUTION_REPORT.md.
**Execução no ambiente Docker: PENDENTE.** Inserir abaixo evidências reais após executar.

## Evidências a inserir no PDF
1. Resultado do harness no Docker, com data, ambiente e código de saída.
2. Aplicação saudável e logs de inicialização do container.
3. Links/prints de Issues atribuídas, branches e PRs com comentários e aprovações reais.
4. Registro da interação com o assistente e alterações correspondentes.

## Governança
Divisão de tarefas e responsáveis: Caio da Silva Diniz — especificação técnica (#8),
configuração do agente de IA (#9), endpoints da API (#11), ambiente Docker e CI (#13).
Gabriel Vieira Souza — models/schemas e regras de negócio (#10), suíte de testes e test
harness (#12), governança do projeto (#14).

Issues/Project: quadro GitHub Projects "SalaFácil — Entrega 1", 7 issues (uma por área),
todas movidas para Done, com responsável atribuído em cada uma (ver acima).

PRs e respectivas aprovações antes de merge: PRs #1-#7 mescladas inicialmente sem aprovação
formal registrada antes do merge. Identificado o gap em revisão do time e corrigido: as 7
áreas foram reabertas como PRs novas (feature/revisao-*), cada uma com o escopo documentado em
evidence/reviews/ e aprovação (Review changes -> Approve) do revisor registrada antes do
merge. Ver histórico de cada PR feature/revisao-* para o registro completo.

## Conferência final
Substituir todos os PENDENTE, inserir imagens/logs, verificar acesso ao repositório,
exportar este documento para um único PDF e conferir a leitura. Cada integrante deve
submeter o PDF conforme o enunciado. Não declarar como realizado o que ainda está pendente.
