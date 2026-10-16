# Evidências do SalaFácil

## Entrega 2 — execução final

Gabriel executou o Docker em 16/10/2026. Resultado: 95 aprovados, 0 falhas,
0 erros, 0 ignorados, 1 aviso, 2,16 s de pytest, 94,51% de cobertura de app,
100% de services e código de saída 0.

- [Log](tests/20261016T163245717898Z/pytest.log), [ambiente](tests/20261016T163245717898Z/environment.json),
  [cobertura](tests/20261016T163245717898Z/coverage.json) e [JUnit](tests/20261016T163245717898Z/junit.xml).
- [Conferência e hashes das cópias](tests/20261016T163245717898Z/VERIFICATION.json).
- [Build e Healthy](docker/build-healthy-entrega2.png).
- [95 testes Docker](docker/tests-docker-entrega2.png).
- [Relatório completo](../docs/EXECUTION_REPORT.md).

As capturas mostram o conflito com um container antigo e sua resolução. Os quatro
arquivos originais do harness foram preservados byte a byte. O aviso externo não
foi omitido. Esta atualização não declara aprovação do seu próprio PR nem da
integração final antes de acontecerem.

## Evidências históricas

- `tests/20260911T210820055929Z/`: Python local da primeira revisão.
- `tests/20260912T200934816939Z/`: Docker histórico: 78 testes, 55 avisos, 1,67 s.
- `docker/build-healthy.png` e `docker/tests-docker.png`: capturas da Entrega 1.
- `github/`: capturas históricas do Actions; conferir cada execução atual separadamente.
- `ai/`: registro factual e capturas do Codex desktop por Gabriel.
- `reviews/`: revisões documentais posteriores; não são aprovações retroativas.

O modelo `docs/SUBMISSION_TEMPLATE.md` pertence à Entrega 1. Para a Entrega 2,
usar [SUBMISSION_ENTREGA2.md](../docs/SUBMISSION_ENTREGA2.md).
