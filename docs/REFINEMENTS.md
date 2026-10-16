# Registro de Refinamentos da Especificação

Este arquivo documenta mudanças na `SPEC.md` feitas **depois** da primeira versão, motivadas
por testes, revisão do grupo ou ambiguidade descoberta durante a implementação. O objetivo é
deixar rastreável *por que* a spec mudou — sem isso, ADRs e testes ficam desalinhados da
especificação "oficial".

## R-001 — Cancelamento de reserva inexistente vs. já cancelada

- **Origem**: escrevendo `test_edge_cases.py`, ficou ambíguo o que deveria acontecer ao
  cancelar (a) uma reserva que nunca existiu e (b) uma reserva que já estava cancelada. A
  primeira versão da spec só dizia "permite cancelar uma reserva".
- **Decisão do grupo**: (a) deve retornar `404` (erro real — o cliente está referenciando algo
  que não existe); (b) deve ser idempotente e retornar sucesso (`204`), já que o estado final
  desejado ("a reserva está cancelada") já é verdade.
- **Mudança na spec**: adicionada a regra **RN06** na seção 4.4 e o caso de teste
  correspondente em `test_edge_cases.py::test_cancel_already_cancelled_is_idempotent` e
  `test_cancel_nonexistent_returns_404`.

## R-002 — Reserva "atravessando" o expediente

- **Origem**: um teste de borda perguntou o que acontece com uma reserva das 19:30 às 20:30,
  quando o expediente termina às 20:00. A primeira versão da spec não deixava claro se a regra
  de expediente valia só para `start_time` ou para o intervalo inteiro.
- **Decisão do grupo**: os dois limites (`start_time` e `end_time`) precisam estar dentro da
  janela de expediente do mesmo dia — não basta começar dentro do horário.
- **Mudança na spec**: RN03 (seção 4.4) reescrita para deixar isso explícito. Teste:
  `test_edge_cases.py::test_booking_ending_after_business_hours_rejected`.

## R-003 — Corte de escopo: sem múltiplos fusos horários nesta fase

- **Origem**: durante a decomposição em unidades (`SPEC.md` seção 6), surgiu a dúvida sobre
  suportar salas em escritórios de fusos diferentes.
- **Decisão do grupo**: fora de escopo na Fase 1 — todo o sistema assume um único fuso
  horário (UTC, conforme R-004). Se o projeto evoluir para múltiplos escritórios, isso vira uma nova
  entrada nos Requisitos Funcionais de uma fase futura, com seu próprio ADR.
- **Mudança na spec**: adicionado explicitamente à seção 1 ("Visão Geral do Problema", lista
  de fora de escopo).

## Como registrar um novo refinamento

1. Edite `docs/SPEC.md` com a mudança.
2. Adicione uma entrada aqui com: origem (que teste/revisão motivou), decisão do grupo, e qual
   teste passou a cobrir o caso.
3. Se a mudança afeta uma decisão arquitetural (não só uma regra de negócio pontual), crie
   também um novo ADR em `docs/adr/`.

## R-004 — Normalização de datas para UTC (2026-09-11)
Origem: revisão identificou TypeError com offset. Decisão implementada nesta revisão:
normalizar entradas para UTC sem offset antes das regras; datas sem offset já representam UTC.
SPEC seção 8 e `tests/test_revision.py` registram contrato e regressões. A indicação
de aprovação pendente pertencia ao registro de 11/09. O PR #18 contém uma revisão
documental posterior; ela não constitui aprovação retroativa do merge original.

## R-005 — Intervalo de datas RF09 (2026-09-11)
Origem: requisito prometia intervalo, mas API só aceitava um dia. A consulta agora aceita
start_date/end_date inclusivos, preserva date e rejeita combinações inválidas.
Testes verificam extremos, canceladas, outras salas e parâmetros inválidos.

## R-006 — Configuração e harness reproduzível (2026-09-11)
Origem: Docker não copiava scripts, .env não era carregado e a cobertura parcial era descrita
como total. Corrigidos Docker/Compose, precedência de configuração, harness Python portátil,
logs persistidos e medição de toda app com meta específica para services.
A pendência Docker desse registro foi resolvida pela execução real de Gabriel em
12/09/2026: 78 testes aprovados, 55 avisos e código de saída 0. Os arquivos estão
ligados em [EXECUTION_REPORT.md](EXECUTION_REPORT.md). A execução Docker final da
Entrega 2 ainda deve ser identificada separadamente na Issue #34.

## R-007 — Escrita concorrente SQLite (2026-09-11)
Origem: consulta de conflito e inserção separadas permitiam uma corrida.
Decisão: transação BEGIN IMMEDIATE antes das leituras das escritas, válida entre conexões e
processos do mesmo arquivo SQLite; timeout retorna 503. Teste dispara duas requisições em
conexões independentes e verifica respostas 201/409 e apenas uma reserva persistida.

## R-008 - Registro da falha de governança e das revisões posteriores (2026-09-13)
Origem: revisao do Gabriel identificou que as 7 PRs iniciais foram mescladas sem uma aprovacao
("Approved these changes") registrada antes do merge, exigida pelo enunciado da entrega.
Decisão: foram criados novos PRs #16-#22 para revisar registros documentais das
áreas já implementadas. Esses PRs não reabriram nem desfizeram os merges dos PRs
#1-#7. As aprovações posteriores não são retroativas ao código original.
Para as novas tarefas, o fluxo exige revisão humana e checks antes de cada merge.
Essa entrada descreve um refinamento do processo, não uma mudança na API.

## R-009 - Remoção de utcnow preservando o contrato UTC (2026-10-15)

Origem: a execução local de referência apresentou 78 testes aprovados e 55 avisos,
54 deles associados a `datetime.utcnow()` no projeto. A chamada é descontinuada
no Python 3.12. A geração de datas passou a usar UTC explícito, removendo o offset
para preservar o armazenamento e as respostas já definidos na SPEC seção 8.

Não há mudança de contrato de API ou regra de negócio. O teste de criação agora
verifica também o formato e o instante UTC de `created_at`. A suíte manteve os
78 testes aprovados; os avisos caíram para um, originado em Starlette/AnyIO.
O [comparativo e os logs](AVISOS_DEPRECACAO.md) registram os resultados reais e a
limitação externa restante. A alteração foi integrada pelo [PR #36](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/36).
A aprovação humana e os checks devem ser consultados no histórico desse PR; o
resultado local isolado não os substitui.

## R-010 - Ampliação dos testes sem mudança de contrato (2026-10-15)

- **Origem:** a Issue #28 pediu inspeção dos casos de borda. Os cenários básicos
  já existiam, mas faltavam algumas verificações ponta a ponta dos limites e dos
  efeitos das operações na disponibilidade e no histórico.
- **Decisão:** acrescentar 17 casos usando os contratos existentes, incluindo
  limites exatos, ausência de persistência em erro, prioridade de validação,
  isolamento e cancelamento. Não redefinir regras apenas para justificar testes novos.
- **Resultado:** 95 testes locais aprovados, um aviso externo e nenhuma falha nova
  revelada por esses 17 casos. Não foi necessária uma correção adicional de código.
- **Evidência:** [TESTES_BORDA_ENTREGA2.md](TESTES_BORDA_ENTREGA2.md), testes em
  `tests/test_entrega2_edges.py` e PR #38.

## R-011 - Consolidação documental da SPEC v1.2 (Entrega 2)

- **Origem:** Issue #29 e revisão dos documentos identificaram pendências antigas
  de Docker/CI ainda descritas como atuais e ausência de um mapa consolidado dos
  refinamentos para testes e requisitos.
- **Decisão:** preservar RF01-RF11 e RN01-RN07 e acrescentar rastreabilidade e
  critérios da Entrega 2 na seção 9 da SPEC. Diferenciar mudança de contrato,
  correção de implementação, ampliação de testes e ajuste de processo.
- **Validação:** conferir links, referências aos testes e os registros existentes.
  Esta atualização é documental e não representa nova execução Docker ou
  homologação humana automática de decisões anteriores.

## Matriz do loop de re-especificação

| Registro | Gatilho observado ou registrado | Decisão / ajuste | Evidência de validação |
|---|---|---|---|
| R-001 | Ambiguidade entre reserva ausente e já cancelada | 404 para ausência; 204 idempotente para cancelamento repetido | `test_cancel_nonexistent_returns_404`; `test_cancel_already_cancelled_is_idempotent` |
| R-002 | Ambiguidade sobre reserva que ultrapassa o expediente | Validar os dois limites no mesmo dia | `test_booking_ending_after_business_hours_rejected` |
| R-003 | Dúvida de escopo sobre escritórios em fusos diferentes | Manter único expediente UTC; múltiplos escritórios fora do escopo | SPEC seção 1 e validações UTC de R-004 |
| R-004 | Erro ao comparar datas com e sem offset | Normalizar para UTC antes de aplicar regras | `test_offset_dates_are_normalized_and_conflict`; `test_mixed_offset_and_naive_date` |
| R-005 | RF09 prometia intervalo, mas a implementação só aceitava dia | Aceitar início/fim inclusivos e rejeitar filtros incompatíveis | `test_range_includes_both_dates_excludes_cancelled_and_other_rooms`; `test_invalid_range_rejected` |
| R-006 | Scripts ausentes no Docker, `.env` sem efeito e cobertura descrita incorretamente | Corrigir empacotamento, configuração e harness | Teste de precedência do `.env`; logs Docker originais de 12/09/2026 |
| R-007 | Consulta de conflito e inserção separadas permitiam corrida | Adquirir `BEGIN IMMEDIATE` antes de ler e gravar | `test_concurrent_booking_only_one_confirmed`, com duas conexões reais |
| R-008 | Merges iniciais sem aprovação formal prévia | Registrar a limitação histórica e exigir revisão para novos PRs | Histórico dos PRs originais e das revisões posteriores |
| R-009 | 54 avisos de `utcnow()` no código e nos testes | Trocar a API de geração sem alterar o contrato UTC | Comparativo 55 para 1 aviso e validação de `created_at` |
| R-010 | Cobertura ponta a ponta incompleta dos limites | Acrescentar 17 casos; contrato preservado | Suíte local com 95/95 aprovados |
| R-011 | Documentos com pendências antigas e rastreabilidade dispersa | Consolidar a SPEC v1.2 e este histórico | Revisão documental no PR da Issue #29 |

## Como aplicar o ciclo nos próximos ajustes

1. Registrar o problema e sua origem real: teste que falhou, revisão ou ambiguidade.
2. Classificar se há mudança de contrato ou erro de implementação do contrato existente.
3. Se mudar o contrato, atualizar a SPEC e registrar a decisão antes da implementação.
4. Se afetar arquitetura, criar ou revisar o ADR correspondente.
5. Implementar a correção e acrescentar testes que verifiquem o comportamento esperado.
6. Executar o harness e preservar ambiente, logs, código de saída e cobertura.
7. Solicitar revisão do outro integrante e aprovar os checks antes do merge.

Os registros iniciais são preservados como histórico recebido, sem inventar logs
de falha que não foram guardados. Os resultados posteriores comprovam as execuções
identificadas, não todos os passos anteriores do desenvolvimento.
