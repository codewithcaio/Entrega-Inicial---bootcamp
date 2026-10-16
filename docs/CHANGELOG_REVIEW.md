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

## Itens ainda necessários para consolidar a Entrega 2

- Revisão e integração da documentação/evidências da Issue #34: execução Docker
  conferida em 16/10, com 95 aprovados, 1 aviso, 2,16 s e saída 0.
- Revisão dos PRs, integração final e PDF consolidado da Entrega 2.

Não se exige nova funcionalidade fora da SPEC para substituir esses itens de documentação,
validação e análise crítica. As contagens de testes são vinculadas às execuções indicadas.
