# Relatório de execução — atualizado em 13/09/2026

## 1. Execução real no Docker

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

## 2. Arquivos comprobatórios

- [Print da construção e container Healthy](../evidence/docker/build-healthy.png)
- [Print do resultado dos testes no Docker](../evidence/docker/tests-docker.png)
- [Log completo do harness](../evidence/tests/20260912T200934816939Z/pytest.log)
- [Ambiente, comando interno e código de saída](../evidence/tests/20260912T200934816939Z/environment.json)
- [Cobertura por arquivo](../evidence/tests/20260912T200934816939Z/coverage.json)
- [Relatório JUnit](../evidence/tests/20260912T200934816939Z/junit.xml)

Os prints foram fornecidos por Gabriel. Os arquivos brutos foram copiados da pasta
`evidence/tests/20260912T200934816939Z` do projeto executado em seu computador, sem alterar seu conteúdo.

## 3. GitHub Actions

O [print de execução do Actions](../evidence/github/actions-sucesso.png) fornecido pelo
integrante mostra o workflow `Test Harness` com `Success`, jobs `test` e `docker-test`
aprovados, execução por push na branch `develop`, commit `fd58d65`, duração total de 38 s
e dois artefatos. O resumo contém avisos de depreciação do Node.js nas actions utilizadas.

Essa captura comprova o status mostrado dessa execução remota. A contagem de 78 testes e
as métricas detalhadas acima são da execução Docker local, conferida nos arquivos brutos;
não foram inferidas a partir do resumo do Actions. A [execução posterior na main](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/actions/runs/34778178346), após o PR #24,
também foi conferida com resultado `success` em 13/09/2026. Aprovação de testes não comprova revisão humana anterior ao merge.

## 4. Histórico e limites

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
representam uma nova execução Docker nesta atualização documental. O PDF não foi alterado.

## 5. Uso do OpenAI Codex

Gabriel Vieira Souza utilizou o **OpenAI Codex no aplicativo desktop** para revisar o
projeto e corrigir esta documentação com os resultados reais. Evidências: [pedido e README](../evidence/ai/codex-readme.png)
e [resposta e relatório](../evidence/ai/codex-relatorio.png). O Docker foi executado por Gabriel.
As capturas não são evidência de Codex CLI.
