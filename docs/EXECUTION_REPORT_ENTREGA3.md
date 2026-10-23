# Relatório de execução e validação funcional — Entrega 3

## Identificação

- Projeto: SalaFácil — API de reserva de salas.
- Execução Docker e operações manuais: Gabriel Vieira Souza, em 23/10/2026.
- Início do harness: 18:41:42 UTC (15:41:42 em Brasília).
- Ambiente: Docker Compose, Python 3.12.15, Linux/WSL2 x86_64.
- Origem informada: ZIP da branch `feature/entrega3-final`.
- Identificador da execução: `20261023T184142747256Z`.

O ambiente foi construído com `docker compose up --build --wait` e o contêiner
atingiu o estado Healthy. Em seguida foi executado:

```bash
docker compose run --rm api python scripts/run_tests.py
```

O harness não registra o SHA Git e o projeto foi extraído de ZIP; portanto os
metadados desta execução não atestam, isoladamente, um commit ou tag. A versão
publicada deve ser relacionada às evidências e aos checks do commit final antes
da release. A versão 1.0.0 exibida no Swagger é a versão declarada da API.

## Resultados automatizados

| Indicador | Resultado verificado |
|---|---|
| Testes executados/aprovados | 95 / 95 — 100% de passagem |
| Falhas / erros / ignorados | 0 / 0 / 0 |
| Avisos | 1 DeprecationWarning de Starlette/AnyIO |
| Duração informada pelo pytest | 2,19 segundos |
| Cobertura total | 310 de 328 linhas executáveis: 94,51% |
| Cobertura dos serviços | 100% |
| Código de saída do harness | 0 |

O terminal arredonda a cobertura para 95%; o JSON registra
94,51219512195122%. Não confundir cobertura com aprovação de testes.
O aviso refere-se ao alias `anyio.abc.BlockingPortal` usado pelo TestClient da
dependência Starlette; o log o preserva integralmente.

### Cobertura por módulo

| Módulo | Linhas cobertas / executáveis | Cobertura |
|---|---|---|
| `src/app/config.py` | 13 / 14 | 92.86% |
| `src/app/database.py` | 22 / 36 | 61.11% |
| `src/app/main.py` | 15 / 16 | 93.75% |
| `src/app/models.py` | 34 / 34 | 100.00% |
| `src/app/routers/bookings.py` | 43 / 43 | 100.00% |
| `src/app/routers/rooms.py` | 57 / 57 | 100.00% |
| `src/app/routers/users.py` | 30 / 32 | 93.75% |
| `src/app/schemas.py` | 46 / 46 | 100.00% |
| `src/app/services/booking_service.py` | 50 / 50 | 100.00% |

Os testes cobrem regras puras, integração HTTP, limites de entrada, UTC,
cancelamento e concorrência em SQLite. A cobertura não demonstra teste de carga,
autenticação ou ausência total de defeitos.

## Evidências brutas

- [pytest.log](../evidence/tests/20261023T184142747256Z/pytest.log).
- [environment.json](../evidence/tests/20261023T184142747256Z/environment.json).
- [junit.xml](../evidence/tests/20261023T184142747256Z/junit.xml).
- [coverage.json](../evidence/tests/20261023T184142747256Z/coverage.json).

Os quatro arquivos foram conferidos entre si. As capturas recebidas documentam
a inicialização e a demonstração manual e foram preservadas para o PDF final.

## Validação funcional manual no Swagger

Operações executadas por Gabriel em `http://localhost:8000/docs` em 23/10/2026,
com dados fictícios. Os resultados abaixo foram lidos nas capturas de
**Server response**, não nos exemplos automáticos de respostas do Swagger.

| Operação e dados | Resultado esperado | Resultado observado |
|---|---|---|
| Criar sala “Sala Demonstracao Final”, capacidade 8, Primeiro andar | 201 e ID | 201, sala ID 1 |
| Criar “Usuario Demonstracao”, demo.final@example.com | 201 e ID | 201, usuário ID 1 |
| Reservar sala 1 para usuário 1, 26/10/2026, 14:00–15:00 UTC, 5 pessoas | 201, CONFIRMED | 201, reserva ID 1, CONFIRMED |
| Repetir exatamente a criação da reserva | 409, conflito | 409, mensagem de horário já reservado |
| Consultar disponibilidade da sala 1 em 26/10/2026 | 200, 08:00–14:00 e 15:00–20:00 | Dois intervalos correspondentes |
| Cancelar reserva 1 | 204, sem corpo | 204, sem corpo |
| Consultar novamente a disponibilidade | 200, 08:00–20:00 | Um intervalo único das 08:00 às 20:00 |

O fluxo observado confirma criação, bloqueio de duplicidade e liberação do
horário após cancelamento para esses dados. Essa demonstração complementa a suíte
automatizada; não representa revisão de PR pelo outro integrante.

## Revisão e publicação

Este relatório registra execuções reais anteriores ao fechamento da release.
A aprovação formal do PR pelo outro integrante, os checks na main e a publicação
da tag devem ser conferidos no GitHub antes da entrega. A demonstração em vídeo
de 3 a 5 minutos e o PDF consolidado completam os materiais de submissão.
