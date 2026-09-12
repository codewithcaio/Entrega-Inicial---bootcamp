# SalaFácil — API de reserva de salas

Projeto para a Entrega 1: ambiente, especificação técnica e Test Harness.
API em Python 3.12, FastAPI, SQLAlchemy e SQLite. Permite cadastrar salas e usuários,
criar/cancelar reservas e consultar ocupação/disponibilidade. Documentação interativa: `/docs`.

## Equipe e repositório

| Nome completo | RA |
|---|---|
| Gabriel Vieira Souza | 22552446 |
| Caio da Silva Diniz | 22552405 |

Repositório GitHub: **PENDENTE**. O ZIP não comprova branches, Issues, PRs ou revisões.
O roteiro está em [CONTRIBUTING.md](CONTRIBUTING.md).

## Execução com Docker

Pré-requisitos: Docker com daemon ativo e Docker Compose v2 com suporte a `--wait`.
Extraia este projeto, abra o terminal na pasta que contém este README e copie
`.env.example` para `.env` se quiser personalizar o expediente.

```bash
docker compose up --build --wait
docker compose run --rm api python scripts/run_tests.py
```

Abra http://localhost:8000/docs ou http://localhost:8000/health.
O harness também pode ser chamado com `docker compose run --rm api bash scripts/run_tests.sh`.
Os logs dos testes são salvos em `evidence/tests/<data-hora-UTC>/` no computador,
por uma montagem de pasta no Compose. Incluem saída bruta, metadados, JUnit e cobertura JSON.

Para capturar a aplicação e depois encerrar:

```bash
docker compose logs --no-color > evidence/docker/compose.log
docker compose ps -a > evidence/docker/status.txt
docker compose down
```

O volume `booking-data` preserva o banco ao encerrar. No Docker, `DATABASE_URL` é fixado em
`sqlite:////app/data/booking.db` para manter o banco dentro do volume; o `.env` personaliza
`BUSINESS_HOURS_START` e `BUSINESS_HOURS_END`.

**Status desta revisão:** Docker não pôde ser executado neste computador. A configuração foi
corrigida e existe um job Docker no GitHub Actions; uma execução futura bem-sucedida ainda
precisa ser obtida e anexada. Não apresente logs Python locais como execução Docker.

## Execução local — Windows / PowerShell

Pré-requisito: Python 3.12 disponível como `python`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir src --reload
```

Em outro terminal, na mesma pasta:

```powershell
.\.venv\Scripts\python.exe scripts/run_tests.py
```

## Execução local — Linux / macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python -m uvicorn app.main:app --app-dir src --reload
# Em outro terminal:
.venv/bin/python scripts/run_tests.py
```

A aplicação carrega o `.env` da raiz; variáveis já definidas no terminal têm prioridade.
Os testes usam configuração fixa (08:00–20:00 UTC) e bancos isolados, sem usar o banco pessoal.

## Contrato de horários e consultas

Todos os horários de negócio são **UTC**. Entradas sem offset são interpretadas como UTC;
entradas com `Z`, `+00:00` ou outro offset são convertidas para UTC. As respostas e o SQLite
armazenam/exibem UTC sem sufixo. Por exemplo, 07:00−03:00 corresponde a 10:00 UTC.
Use datas futuras ao experimentar a criação de reservas.

- Um dia: `GET /api/v1/rooms/1/bookings?date=2026-09-15`
- Intervalo inclusivo: `GET /api/v1/rooms/1/bookings?start_date=2026-09-15&end_date=2026-09-20`
- Não misture `date` com os parâmetros do intervalo; entradas incompletas/invertidas retornam 422.

## Test Harness e evidências

Execução desta revisão: **78 testes passaram**, cobertura total de `app` arredondada em **94%**
e cobertura de `services` em **100%**. O harness reprova cobertura de services inferior a 80%.
Veja [o relatório real](docs/EXECUTION_REPORT.md) e [o guia de evidências](evidence/README.md).

Há testes de regras isoladas, API com SQLite em memória e concorrência com duas conexões
ao mesmo arquivo SQLite temporário. Os testes de regressão cobrem offsets de data, consulta
por intervalo e carregamento do `.env`. Warnings presentes nos logs não são falhas de teste.

GitHub Actions tem jobs Python e Docker e publica os respectivos logs como artefatos.
A mera presença do workflow não comprova que ele já foi executado no GitHub.

## Especificação, decisões e assistente de código

- [SPEC.md](docs/SPEC.md): requisitos, contratos e componentes.
- [REFINEMENTS.md](docs/REFINEMENTS.md): registro dos ajustes.
- [ADRs](docs/adr/): stack, SQLite, testes, IA e correções desta revisão.
- [Registro da revisão assistida](evidence/ai/REVISION.md): trabalho realizado nesta conversa.
- `.claude/CLAUDE.md`, `.cursorrules` e `AGENTS.md`: contexto e regras para assistentes.

O projeto original declara uso de Claude Code. Esta revisão foi assistida pelo Codex no app
desktop, com execução de comandos no terminal. Isso **não é evidência de uma sessão do Codex CLI**.
O enunciado aceita ao menos uma ferramenta de auxílio a código. Se o grupo declarar uso de
Claude Code ou Codex CLI, anexe também a interação real correspondente, sem inventar histórico.

## Decisões arquiteturais resumidas

FastAPI/Pydantic implementam os contratos HTTP; services concentra validações puras;
routers orquestram acesso ao banco. SQLite atende à entrega inicial. Operações de escrita
adquirem `BEGIN IMMEDIATE` antes de consultar e gravar, evitando a corrida de reservas;
se o banco permanecer ocupado além do timeout, a API retorna 503 com orientação para repetir.
Esta versão suporta SQLite; migrar para outro banco exige revisar a estratégia transacional.

## Preparação da entrega

Use [SUBMISSION_TEMPLATE.md](docs/SUBMISSION_TEMPLATE.md) como texto-base do PDF.
Preencha o link e as evidências Docker e links das Issues/PRs reais.
Cada integrante deve submeter o PDF conforme o enunciado.
Veja [CHANGELOG_REVIEW.md](docs/CHANGELOG_REVIEW.md) para as correções e pendências.
