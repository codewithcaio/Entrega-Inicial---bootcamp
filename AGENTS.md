# Orientações do projeto

- Leia docs/SPEC.md antes de alterar código. Atualize a especificação e REFINEMENTS.md para mudanças de contrato.
- Mantenha regras puras em services e contratos em schemas. Horários seguem UTC.
- Preserve a transação SQLite antes de leituras em operações de escrita.
- Execute python scripts/run_tests.py e registre evidências reais; nunca invente resultados.
- Use branches de trabalho e PRs revisados conforme CONTRIBUTING.md. Não publique nem faça merge sem autorização.
- Não declare execução de Docker/CLI ou aprovação humana quando não aconteceram.
