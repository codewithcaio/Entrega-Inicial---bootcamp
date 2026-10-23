# Encerramento da Entrega 3

## Validação e evidências

1. Revisar README, SPEC As-Built e código na branch de trabalho.
2. Executar na raiz, com Docker ativo:

```bash
docker compose up --build --wait
docker compose run --rm api python scripts/run_tests.py
```

O primeiro comando constrói e inicia a aplicação; o segundo executa o harness.
Preservar `pytest.log`, `environment.json`, `junit.xml` e `coverage.json` da nova
pasta `evidence/tests/<data-hora-UTC>/`, além do print do resumo e do estado Healthy.
Registrar `git rev-parse HEAD` antes da execução e eventuais alterações locais.
Os resultados de 16/10/2026 permanecem históricos, não substituem a nova execução.

3. Conferir criação de sala/usuário, reserva válida, rejeição de conflito,
   consulta de disponibilidade e cancelamento no Swagger `/docs`.
4. Inspecionar arquivos temporários, credenciais e código desativado antes do PR.
   Evidências históricas de testes devem ser preservadas e identificadas.
5. Abrir PR da feature para develop, obter aprovação formal do outro integrante
   e checks aprovados. Integrar develop na main por novo PR aprovado.
6. Conferir `test` e `docker-test` no commit final da main; publicar release estável
   `v1.0.0` vinculada a esse commit, com notas de funcionalidades, uso e limites.

## Demonstração (3 a 5 minutos)

- 0:00–0:30: integrantes, problema e proposta da API.
- 0:30–2:30: Swagger; criar sala/usuário e reserva futura dentro do expediente UTC;
  repetir o horário para mostrar conflito; consultar disponibilidade e cancelar.
- 2:30–3:30: executar o harness em tempo real e mostrar resumo/cobertura.
- 3:30–4:30: mostrar release, explicar limites e aprendizados do grupo.

Usar os IDs retornados pela API e dados fictícios. Reservas existentes podem
causar conflitos; escolher nomes/e-mails e horário livres. Verificar o acesso ao
link do vídeo sem depender da conta de quem gravou.

## Retrospectiva e PDF

Registrar o que o grupo realmente aprendeu: apoio de Codex desktop/Claude Code,
validação das sugestões, dificuldades de branches/revisão e relação entre SPEC,
implementação e testes. Ganhos de produtividade são qualitativos se não houve
medição; não inventar horas ou percentuais de economia.

O PDF final deve conter nomes/RA, resumo executivo, link da release, commit,
resultados da nova execução e cobertura, link do vídeo e lições aprendidas.
Preencher resultados, aprovação e links apenas após existirem.
