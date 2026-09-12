# ADR-0001: Uso de Python + FastAPI para a API

- **Status**: Aceito
- **Data**: 2026-09-11
- **Decisores**: equipe do projeto

## Contexto
Precisávamos entregar, no prazo curto da Fase 1, uma API REST com regras de negócio não
triviais (conflito de horário, validação de capacidade/expediente) e um harness de testes
robusto, além de documentação OpenAPI para facilitar o code review entre o grupo.

## Decisão
Usar **Python 3.12 + FastAPI** para a API, **SQLAlchemy** como ORM sobre **SQLite**, e
**pytest** como framework de testes.

## Alternativas consideradas
- **Node.js + Express/TypeScript**: também atenderia, mas FastAPI gera documentação OpenAPI
  (`/docs`) automaticamente a partir dos schemas Pydantic, o que reduz trabalho manual de
  documentar contratos de entrada/saída — útil justamente para a especificação exigida nesta
  fase.
- **Django REST Framework**: mais "baterias inclusas" do que o projeto precisa nesta fase;
  overhead de configuração desnecessário para uma API pequena e um bootcamp com prazo curto.

## Consequências
- Ganhamos validação de schema "de graça" via Pydantic (contratos da SPEC.md viram código
  quase 1:1).
- Testamos a API com `TestClient` do FastAPI/httpx sem precisar de um servidor rodando.
- Custo: parte do time com mais familiaridade em Node precisou de um ramp-up rápido em
  Python — mitigado usando um agente de IA (ver ADR-0004) para gerar boilerplate inicial.
