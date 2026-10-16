# Histórico das correções e refinamentos

## Revisão de 11/09/2026 (registro histórico)

- Docker inclui scripts; Compose permite expediente via .env e preserva logs no host.
- Harness Python funciona em Windows/Linux, guarda logs/JUnit/cobertura e aplica meta de services.
- CI contém jobs Python e Docker com upload de evidências; naquele momento,
  a execução remota ainda não havia sido comprovada.
- Datas com offset são normalizadas para UTC antes da validação.
- Consulta de reservas aceita intervalo de datas inclusivo, além do filtro de um dia.
- Escritas SQLite são serializadas antes de ler/gravar; teste verifica reservas concorrentes.
- .env é carregado, com prioridade para variáveis explícitas; configuração inválida é rejeitada.
- README, SPEC, refinamentos e ADRs atualizados; cobertura agora inclui toda app.
- Modelo de PDF, pastas de evidências e registro factual da revisão assistida adicionados.

Resultado: 78 testes passaram localmente, 94% de cobertura total arredondada, services 100%.
Naquela revisão estavam pendentes Docker real, link GitHub, Issues/PRs/reviews
e o preenchimento do PDF. Essas anotações descrevem 11/09, não o estado atual.

## Evidências posteriores da Entrega 1

- Em 12/09, Gabriel executou o Docker: 78 testes aprovados, código de saída 0.
  Os logs e capturas estão ligados em [EXECUTION_REPORT.md](EXECUTION_REPORT.md).
- Os PRs #24 e #25 integraram a entrega inicial e sua atualização documental.
- Os PRs #1-#7 não tiveram aprovação formal prévia registrada. Revisões documentais
  posteriores não corrigem retroativamente esse histórico.
- O PDF da primeira entrega foi preparado separadamente; não é o relatório da Entrega 2.

## Trabalho da Entrega 2

- Issue #33 / PR #35: índice dos cinco ADRs, com decisões e trade-offs.
- Issue #32 / PR #36: 54 avisos do projeto removidos; um aviso externo preservado.
  Comparativo em [AVISOS_DEPRECACAO.md](AVISOS_DEPRECACAO.md).
- PR #37: sincronização de main para develop.
- Issue #28 / PR #38: 17 casos adicionais; execução local com 95 aprovados,
  cobertura de 94,51% e serviços em 100%. Ver [relatório](TESTES_BORDA_ENTREGA2.md).
- Issue #29 / PR #40: consolidação documental da SPEC v1.2 e do loop de refinamentos.
- Issue #30 / PR #41: README final, arquitetura e diagrama de fluxo.
- Issue #31 / PR #42: [comparação, análise ético-técnica e experiência](RELATORIO_ETICO_TECNICO.md),
  preparada com separação entre uso observado, declaração original e pesquisa documental.

## Fechamento e complementos documentais

- PR #43: evidências Docker de 16/10/2026, com 95 aprovados, 1 aviso e saída 0.
- PR #44: integração da Entrega 2 na main, com revisão e checks anteriores ao merge.
- PRs #45 e #46: correção do link dos ADRs e integração na main.
- Complemento atual: participação conjunta declarada, uso informado de Claude
  Code por Caio, relatos individuais e tabela Autor/Revisor em
  [COLABORACAO_ENTREGA2.md](COLABORACAO_ENTREGA2.md).

O PR #39 tem comentário anterior ao merge, sem APPROVED registrado. Os PRs #36
e #38 entraram na main fora do fluxo previsto e foram sincronizados depois.
Esses registros são preservados, sem apresentar aprovações posteriores como retroativas.

Este complemento altera apenas a documentação e ainda depende de seu PR e
revisão humana. O PDF será atualizado depois da integração dessas alterações.
