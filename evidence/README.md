# Evidências da entrega

- `tests/<data>/`: logs reais, ambiente, cobertura JSON e relatório JUnit da revisão local.
- `ai/REVISION.md`: registro factual da revisão assistida nesta conversa.
- `docker/`: reservado para execução real Docker; ainda pendente.
- `github/`: reservado para links/prints de Issues, PRs e reviews reais; ainda pendente.

O harness cria uma pasta nova a cada execução e preserva resultados anteriores.
Falhas e warnings fazem parte dos logs; o código de saída é registrado.
As dependências exatas da revisão Windows estão em `tests/review-environment.txt`;
esse arquivo é evidência do ambiente, não um lock de instalação multiplataforma.

## Captura restante
1. Rodar `docker compose up --build --wait` e registrar a aplicação saudável.
2. Rodar `docker compose run --rm api python scripts/run_tests.py`.
3. Salvar `docker compose logs --no-color` e status em docker/.
4. Registrar Issues atribuídas, PRs com revisão e aprovação anteriores ao merge.
5. Anexar a interação real do assistente escolhido e ligar alterações aos commits/PRs.
6. Inserir as evidências e identificação no modelo de submissão.
