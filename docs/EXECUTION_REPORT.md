# Relatório real da revisão — 2026-09-11

Ambiente: Windows 10, Python 3.12.14, dependências de requirements.txt em ambiente virtual isolado.
Comando executado: `python scripts/run_tests.py`.

Resultado: **78 passed**, código de saída **0**. Cobertura total de app: **93,60%**
(94% arredondado no terminal); services: **100%**, acima da meta de 80%.
Warnings de depreciação constam na saída bruta; não foram ocultados.

- [Saída completa e código de saída](../evidence/tests/20260911T210820055929Z/pytest.log)
- [Ambiente e comando completo](../evidence/tests/20260911T210820055929Z/environment.json)
- [Cobertura por arquivo](../evidence/tests/20260911T210820055929Z/coverage.json)
- [JUnit](../evidence/tests/20260911T210820055929Z/junit.xml)
- [Dependências instaladas na revisão](../evidence/tests/review-environment.txt)

As 13 regressões adicionais abrangem offsets (incluindo fusos diferentes), datas mistas,
intervalo inclusivo, exclusão de canceladas/outras salas, parâmetros inválidos, .env e
duas requisições concorrentes em conexões independentes ao mesmo SQLite temporário.

## Limitações e próxima evidência
Não foi encontrado Docker disponível neste ambiente, portanto nenhum build/container foi
executado nesta revisão. O job Docker foi preparado no workflow, mas ainda não rodou no GitHub.
Execute os comandos do README para gerar evidências do ambiente padronizado.
O relatório antigo está preservado em EXECUTION_REPORT_ORIGINAL.md como material histórico
fornecido pelo autor do ZIP; ele não comprova a versão atual.
