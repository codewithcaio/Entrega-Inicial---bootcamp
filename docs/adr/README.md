# Índice de decisões arquiteturais - SalaFácil

Este índice consolida os cinco Architecture Decision Records (ADRs) do projeto para
a Entrega 2. Cada ADR registra o contexto, a decisão e suas consequências. A tabela
resume os benefícios e os custos assumidos, sem substituir os documentos completos.

Tarefa relacionada: [Issue #33](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/issues/33).
Consolidação documental: 15/10/2026.

## Decisões e trade-offs

| ADR | Título e documento | Status registrado no ADR | Decisão e justificativa | Benefício | Custo ou limitação assumida |
|---|---|---|---|---|---|
| 0001 | [Python + FastAPI para a API](0001-escolha-de-stack.md) | Aceito | Usar Python 3.12, FastAPI, Pydantic, SQLAlchemy e pytest para implementar a API e validar seus contratos. | Validação de entrada, documentação OpenAPI e testes HTTP sem iniciar um servidor externo. | Exige familiaridade com Python e consistência entre schemas, contratos e regras de negócio. A documentação automática não substitui a especificação nem a revisão. |
| 0002 | [SQLite como banco de dados](0002-persistencia-sqlite.md) | Aceito | Persistir em SQLite por meio do SQLAlchemy e manter o arquivo em volume Docker; isolar os dados dos testes. | Ambiente simples, persistência real e execução sem um serviço de banco separado. | Escritas concorrentes pesadas são uma limitação. Migrar para PostgreSQL exige rever a estratégia transacional e os testes, além de trocar driver e configuração. |
| 0003 | [Serviço puro para testabilidade](0003-estrategia-de-testes.md) | Aceito | Separar decisões de negócio em funções puras de `booking_service.py`; deixar a orquestração HTTP e de persistência nos routers. | Testes unitários rápidos das regras, complementados por testes de integração e de concorrência. | A separação acrescenta uma camada que precisa permanecer alinhada à SPEC. Testes isolados das regras não comprovam, sozinhos, o comportamento completo da API. |
| 0004 | [Agente de IA no fluxo SDD](0004-uso-de-agente-ia.md) | Aceito | O ADR original escolhe Claude Code, com contexto em `.claude/CLAUDE.md`, para apoiar a implementação guiada pela SPEC e validada por testes. | Registra o contexto do assistente e torna explícita a sequência especificação, implementação e validação. | Requer revisão humana e manutenção da especificação. A declaração da ferramenta no ADR não comprova uma sessão de uso nem garante a correção do código gerado. |
| 0005 | [UTC, consultas e concorrência SQLite](0005-correcao-de-contratos-e-concorrencia.md) | Implementado nesta revisão; revisão humana do grupo pendente | Normalizar datas para UTC sem offset, aceitar intervalo inclusivo de datas e iniciar escritas SQLite com `BEGIN IMMEDIATE` antes das leituras de decisão. | Evita comparações inconsistentes de datas, atende à consulta por intervalo e protege a decisão de conflito entre escritores concorrentes. | Há um escritor SQLite por vez; a espera é limitada a 30 segundos e banco ocupado pode gerar HTTP 503. UTC exige conversão na apresentação ao usuário. O teste de concorrência não equivale a teste de carga. |

## Relação entre decisões, requisitos e validação

- **Stack e contratos:** o ADR-0001 sustenta a API JSON, os schemas e a documentação
  OpenAPI descritos na [SPEC](../SPEC.md).
- **Persistência e concorrência:** o ADR-0005 complementa o ADR-0002. Usar ORM não
  torna a transação de exclusão de reservas automaticamente portável entre bancos.
- **Regras e testes:** o ADR-0003 atende à separação das regras (RNF02) e à meta de
  cobertura de serviços (RNF04). A suíte combina testes de regras puras, endpoints
  e conexões independentes ao mesmo arquivo SQLite temporário.
- **Refinamento:** R-004, R-005 e R-007 em [REFINEMENTS.md](../REFINEMENTS.md)
  registram a origem das mudanças de UTC, consulta por intervalo e concorrência
  consolidadas no ADR-0005.
- **Resultados observados:** contagens, cobertura, ambiente e logs pertencem ao
  [relatório de execução](../EXECUTION_REPORT.md). Este índice não registra uma
  nova execução de testes.

## Ferramentas de IA e evidências

O ADR-0004 preserva a escolha declarada no material original: Claude Code. A revisão
posterior registra o uso do **OpenAI Codex no aplicativo desktop por Gabriel Vieira
Souza**, com evidências no [README do projeto](../../README.md#uso-de-ia-e-revisão-humana)
e no [relatório de execução](../EXECUTION_REPORT.md#5-uso-do-openai-codex).
São registros distintos; as capturas do aplicativo desktop não são evidência de
uma sessão do executável Codex CLI.

Este índice organiza as decisões existentes. A comparação de ferramentas e a
análise ético-técnica da Entrega 2 são tratadas na
[Issue #31](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/issues/31).

## Status e revisão humana

Os status da tabela reproduzem os documentos-fonte. Em especial, o ADR-0005 ainda
contém a indicação de revisão humana pendente. A presença de código implementado,
testes aprovados ou revisões documentais posteriores não altera esse status por si
só. Qualquer atualização deve identificar a decisão efetivamente revisada e ligar
o registro à aprovação humana correspondente.

Para novas decisões, usar o [modelo de ADR](template.md), registrar alternativas,
justificativa e consequências e atualizar este índice no mesmo PR. Mudanças de
contrato também devem atualizar a SPEC e o registro de refinamentos. O outro
integrante deve revisar as alterações antes do merge, conforme o
[guia de contribuição](../../CONTRIBUTING.md).
