# Relatório de execução — Entrega 2

Atualizado em 16/10/2026. Tarefa: [Issue #34](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/issues/34).

## Execução final no Docker por Gabriel

Gabriel Vieira Souza executou o harness no Docker Desktop/WSL2, após baixar e
extrair a develop. O Codex desktop auxiliou a orientação e a conferência dos
arquivos fornecidos; não executou este Docker em nome de Gabriel.

```powershell
docker compose up --build --wait
docker compose run --rm api python scripts/run_tests.py
```

| Informação | Resultado conferido |
|---|---|
| Início do harness | 16/10/2026, 16:32:45.717898 UTC (13:32:45 em Brasília) |
| Identificador | `20261016T163245717898Z` |
| Ambiente | `docker-compose`; Linux / WSL2 / x86_64 |
| Python | 3.12.15 |
| Banco de testes | SQLite em memória e arquivos temporários |
| Expediente de teste | 08:00–20:00 UTC |
| Testes | 95 coletados, 95 aprovados, 0 falhas, 0 erros, 0 ignorados |
| Taxa de passagem | 100% |
| Duração do pytest | 2,16 s; JUnit: 2,163 s |
| Avisos | 1 aviso de depreciação externo |
| Cobertura total de app | 310/328 linhas: 94,51% (95% arredondado no terminal) |
| Cobertura de services | 100%; mínimo de 80% atendido |
| Código de saída | `EXIT_CODE=0` |

Trecho literal do log:

```text
======================== 95 passed, 1 warning in 2.16s =========================

Cobertura de services: 100.00% (mínimo 80%)
EXIT_CODE=0
```

A duração acima é do pytest, não do build. Passagem de 100% não significa
cobertura de 100% ou ausência comprovada de defeitos. O aviso restante vem de
`starlette/testclient.py:40`, pelo alias depreciado `anyio.abc.BlockingPortal`.
Não foi ocultado e não provocou falha. A atualização coordenada dessa dependência
continua como melhoria; não é apresentada como concluída.

### Evidências da execução final

- [Build, resolução do conflito e container Healthy](../evidence/docker/build-healthy-entrega2.png).
- [Resumo dos 95 testes no Docker](../evidence/docker/tests-docker-entrega2.png).
- [Log bruto](../evidence/tests/20261016T163245717898Z/pytest.log).
- [Ambiente e saída](../evidence/tests/20261016T163245717898Z/environment.json).
- [Cobertura exata](../evidence/tests/20261016T163245717898Z/coverage.json).
- [JUnit com 95 casos](../evidence/tests/20261016T163245717898Z/junit.xml).
- [Conferência adicional e SHA-256 das cópias](../evidence/tests/20261016T163245717898Z/VERIFICATION.json).

Os quatro arquivos do harness foram copiados sem alterar seus bytes; hashes
conferidos contra os originais fornecidos por Gabriel. Comparação do conteúdo de
34 arquivos de código, testes, scripts e configuração da pasta executada com a
develop `d329396` não encontrou diferenças, normalizando apenas CRLF/LF.
O harness não registra o commit Git e o ZIP não contém `.git`; essa conferência
não é uma atestação do commit embarcado na imagem.

### Incidente de inicialização e resolução

A primeira inicialização encontrou um container preexistente chamado
`salafacil-api`. Gabriel parou e renomeou o antigo para
`salafacil-api-backup-20261016`, sem solicitar exclusão de dados, e repetiu o
Compose. A captura mostra a nova inicialização como Healthy. Foi um conflito
de ambiente, não uma falha dos 95 testes. A captura preserva o erro e a resolução.

### Evolução e governança

A Entrega 1 registrava 78 testes, 55 avisos e 93,60% de cobertura. A Entrega 2
removeu 54 avisos originados no projeto e acrescentou 17 casos de borda, chegando
a 95 testes e 94,51% de cobertura. Os novos testes passaram na implementação
existente; não representam 17 defeitos novos corrigidos.

O [PR #42](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/42)
integrou o relatório ético-técnico à develop. Esta atualização da Issue #34 é
documental e ainda depende do seu próprio PR, revisão e integração. Depois,
conferir os checks do PR de develop para main e consolidar o PDF. Os resultados
locais não devem ser usados para atribuir métricas a uma execução específica do
GitHub Actions sem conferir seus artefatos.

## Registro histórico da Entrega 1

As seções abaixo preservam a execução anterior e suas referências. Seus números
não substituem o resultado final da Entrega 2 apresentado acima.

### 1. Execução real no Docker

Gabriel Vieira Souza executou o projeto em seu computador Windows usando Docker Desktop.
O print da construção mostra a imagem criada e o container `salafacil-api` com estado
`Healthy`. O harness foi executado dentro de um container pelo comando documentado abaixo.
Os resultados foram conferidos com o log bruto, os metadados, o JUnit e o JSON de cobertura
recuperados da pasta de evidências do projeto executado pelo integrante.

```bash
docker compose up --build --wait
docker compose run --rm api python scripts/run_tests.py
```

| Informação | Registro da execução |
|---|---|
| Início em UTC | 12/09/2026, 20:09:34.816939 |
| Identificação do ambiente | `docker-compose` |
| Plataforma do container | Linux / WSL2 / x86_64 |
| Python | 3.12.14 |
| Banco de testes | SQLite em memória e arquivos temporários |
| Expediente usado nos testes | 08:00–20:00 UTC |
| Resultado | 78 testes aprovados; 0 falhas; 0 erros |
| Duração informada pelo pytest | 1,67 s |
| Avisos | 55 avisos de depreciação |
| Cobertura total de `app` | 93,60% (94% arredondado) |
| Cobertura de `services` | 100%; meta mínima de 80% atendida |
| Código de saída | `EXIT_CODE=0` |

Trecho literal do log:

```text
======================= 78 passed, 55 warnings in 1.67s ========================

Cobertura de services: 100.00% (mínimo 80%)
EXIT_CODE=0
```

Os avisos referem-se a APIs em desuso, incluindo `datetime.utcnow()` e um alias do AnyIO
utilizado pelo Starlette. Eles foram preservados no log e não representaram falhas da suíte.
Os 1,67 s referem-se ao pytest, não à construção da imagem ou ao tempo total do Docker.

### 2. Arquivos comprobatórios

- [Print da construção e container Healthy](../evidence/docker/build-healthy.png)
- [Print do resultado dos testes no Docker](../evidence/docker/tests-docker.png)
- [Log completo do harness](../evidence/tests/20260912T200934816939Z/pytest.log)
- [Ambiente, comando interno e código de saída](../evidence/tests/20260912T200934816939Z/environment.json)
- [Cobertura por arquivo](../evidence/tests/20260912T200934816939Z/coverage.json)
- [Relatório JUnit](../evidence/tests/20260912T200934816939Z/junit.xml)

Os prints foram fornecidos por Gabriel. Os arquivos brutos foram copiados da pasta
`evidence/tests/20260912T200934816939Z` do projeto executado em seu computador, sem alterar seu conteúdo.

### 3. GitHub Actions

O [print de execução do Actions](../evidence/github/actions-sucesso.png) fornecido pelo
integrante mostra o workflow `Test Harness` com `Success`, jobs `test` e `docker-test`
aprovados, execução por push na branch `develop`, commit `fd58d65`, duração total de 38 s
e dois artefatos. O resumo contém avisos de depreciação do Node.js nas actions utilizadas.

Essa captura comprova o status mostrado dessa execução remota. A contagem de 78 testes e
as métricas detalhadas acima são da execução Docker local, conferida nos arquivos brutos;
não foram inferidas a partir do resumo do Actions. A [execução posterior na main](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/actions/runs/34778178346), após o PR #24,
também foi conferida com resultado `success` em 13/09/2026. Aprovação de testes não comprova revisão humana anterior ao merge.

### 4. Histórico e limites

A execução Python local de 11/09/2026 também obteve 78 testes aprovados e está preservada em
[seu log original](../evidence/tests/20260911T210820055929Z/pytest.log).
Ela foi realizada durante a revisão assistida pelo **OpenAI Codex no aplicativo desktop**.
A execução Docker de 12/09/2026 foi realizada por Gabriel e supre a antiga pendência de
validação do ambiente padronizado.

As 13 regressões adicionais cobrem normalização de offsets, datas mistas, filtros de intervalo,
exclusão de canceladas/outras salas, parâmetros inválidos, `.env` e concorrência SQLite.

O arquivo `EXECUTION_REPORT_ORIGINAL.md` é o relatório histórico recebido no ZIP original.
Suas ressalvas sobre ausência de Docker descrevem aquele momento, não a situação atual.
As métricas Docker acima são do registro de 12/09/2026, preservado integralmente; não
representam uma nova execução Docker nesta atualização documental. Na atualização histórica, o PDF não foi alterado.

### 5. Uso do OpenAI Codex

Gabriel Vieira Souza utilizou o **OpenAI Codex no aplicativo desktop** para revisar o
projeto e corrigir esta documentação com os resultados reais. Evidências: [pedido e README](../evidence/ai/codex-readme.png)
e [resposta e relatório](../evidence/ai/codex-relatorio.png). O Docker foi executado por Gabriel.
As capturas não são evidência de Codex CLI.
