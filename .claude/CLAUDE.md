# Regras de contexto para agentes de IA neste projeto

Este arquivo é lido por agentes de codificação (Claude Code e compatíveis) antes de gerar ou
alterar código neste repositório. Ele existe para manter o fluxo **Spec-Driven Development
(SDD)**: a especificação manda, o código obedece.

## Ordem de trabalho obrigatória

1. **Nunca implemente uma regra de negócio que não esteja em `docs/SPEC.md`.** Se o pedido do
   usuário exigir uma regra nova ou uma mudança de regra existente, pare e primeiro proponha a
   mudança na `SPEC.md` (e, se for uma decisão arquitetural, um ADR em `docs/adr/`).
2. Se a implementação revelar uma ambiguidade ou lacuna na spec (ex.: "o que fazer se X e Y
   acontecerem ao mesmo tempo?"), registre a decisão tomada em `docs/REFINEMENTS.md` antes de
   codificar — não decida silenciosamente e siga em frente.
3. Toda regra de negócio (RN01, RN02, ...) deve ter pelo menos um teste correspondente. Ao
   adicionar/alterar uma RN na spec, adicione/altere o teste na mesma tarefa.
4. Não crie dependências externas (serviços de terceiros, APIs pagas, bibliotecas grandes) sem
   que isso esteja refletido em um ADR.

## Arquitetura do projeto (resumo — ver `docs/SPEC.md` seção 6 para detalhes)

- `src/app/services/booking_service.py`: **única** camada com lógica de negócio (conflito de
  horário, validação de expediente/capacidade/intervalo, cálculo de disponibilidade). Deve
  permanecer livre de dependência de banco de dados ou do FastAPI — só recebe e devolve dados
  Python simples (isso é o que permite testá-la em memória, sem subir a API).
- `src/app/routers/*.py`: só orquestra — busca dados, chama `booking_service`, traduz o
  resultado em resposta HTTP. Não deve conter `if` de regra de negócio.
- `src/app/models.py`: modelos SQLAlchemy (tabelas).
- `src/app/schemas.py`: schemas Pydantic (contrato de entrada/saída da API — devem espelhar a
  seção 5 da `SPEC.md`).

## Estilo e convenções

- Python 3.12, type hints em toda função pública.
- Mensagens de erro de validação devem ser específicas (ex.: `"Horário fora do expediente
  (08:00–20:00)"`, nunca só `"erro"` ou `"inválido"`) — ver RNF05.
- Testes com `pytest`; testes de `booking_service` não devem importar FastAPI nem SQLAlchemy.
- Commits e nomes de branch em português ou inglês são aceitos, mas devem ser consistentes
  dentro de uma mesma branch/PR.

## Fluxo de branches (ver `CONTRIBUTING.md` para detalhes)

Agentes de IA não devem commitar diretamente em `main` nem em `develop`. Qualquer alteração
gerada deve ir para uma branch `feature/<descrição-curta>` a partir de `develop`, com PR
aberto para revisão humana do grupo antes do merge.

## Como este arquivo foi usado nesta entrega

Registro para fins de avaliação (item "Configuração de Agentes de IA" da Entrega 1): este
arquivo foi criado antes da geração do código-fonte e dos testes. O agente (Claude Code) foi
instruído a seguir `docs/SPEC.md` como fonte da verdade e a registrar em
`docs/REFINEMENTS.md` qualquer ajuste de regra necessário durante a implementação — ver esse
arquivo para o histórico real de decisões tomadas durante a geração deste projeto.
