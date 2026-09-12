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
SPEC seção 8 e `tests/test_revision.py` registram contrato e regressões. Aprovação do grupo pendente.

## R-005 — Intervalo de datas RF09 (2026-09-11)
Origem: requisito prometia intervalo, mas API só aceitava um dia. A consulta agora aceita
start_date/end_date inclusivos, preserva date e rejeita combinações inválidas.
Testes verificam extremos, canceladas, outras salas e parâmetros inválidos.

## R-006 — Configuração e harness reproduzível (2026-09-11)
Origem: Docker não copiava scripts, .env não era carregado e a cobertura parcial era descrita
como total. Corrigidos Docker/Compose, precedência de configuração, harness Python portátil,
logs persistidos e medição de toda app com meta específica para services.
Docker permanece pendente de execução real neste computador.

## R-007 — Escrita concorrente SQLite (2026-09-11)
Origem: consulta de conflito e inserção separadas permitiam uma corrida.
Decisão: transação BEGIN IMMEDIATE antes das leituras das escritas, válida entre conexões e
processos do mesmo arquivo SQLite; timeout retorna 503. Teste dispara duas requisições em
conexões independentes e verifica respostas 201/409 e apenas uma reserva persistida.
