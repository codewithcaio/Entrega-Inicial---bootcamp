# Entrega 1 — SalaFácil

**MODELO PARA PREENCHER E EXPORTAR COMO PDF. Não é a entrega final completa.**

## Identificação
Disciplina/turma: PENDENTE. Data da entrega: PENDENTE.

| Nome completo | RA |
|---|---|
| Gabriel Vieira Souza | 22552446 |
| Caio da Silva Diniz | 22552405 |

Repositório público GitHub ou com acesso aos professores: PENDENTE.

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
Divisão de tarefas e responsáveis: PENDENTE.
Issues/Project: PENDENTE. PRs e respectivas aprovações antes de merge: PENDENTE.

## Conferência final
Substituir todos os PENDENTE, inserir imagens/logs, verificar acesso ao repositório,
exportar este documento para um único PDF e conferir a leitura. Cada integrante deve
submeter o PDF conforme o enunciado. Não declarar como realizado o que ainda está pendente.
