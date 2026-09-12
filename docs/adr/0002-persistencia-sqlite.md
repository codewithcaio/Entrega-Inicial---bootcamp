# ADR-0002: SQLite como banco de dados nesta fase

- **Status**: Aceito
- **Data**: 2026-09-11
- **Decisores**: equipe do projeto

## Contexto
O projeto precisa de persistência real (não apenas dados em memória, que se perderiam a cada
restart), mas ainda estamos na fase de especificação/validação do domínio, sem requisito de
concorrência multiusuário em produção nem de deploy em nuvem.

## Decisão
Usar **SQLite** via SQLAlchemy, com o arquivo do banco montado como volume no
`docker-compose.yml`, e **SQLite em memória** (`sqlite:///:memory:`) nos testes automatizados
para isolamento total entre casos de teste.

## Alternativas consideradas
- **PostgreSQL via Docker**: mais próximo de um cenário de produção, mas adiciona um
  container extra, healthcheck e configuração de rede só para esta fase inicial — decidimos
  adiar para quando o RNF de concorrência/produção existir de fato (ver `REFINEMENTS.md`).
- **Persistência em memória (dict) sem SQLAlchemy**: mais rápido de implementar, mas não
  demonstra separação em camadas (repositório/ORM) nem prepara o projeto para trocar de banco
  depois — usar SQLAlchemy desde já isola essa decisão numa única camada.

## Consequências
- `docker-compose up` sobe o ambiente completo sem depender de outro serviço externo.
- Troca futura para PostgreSQL exige driver, configuração e uma estratégia transacional
  própria para preservar a exclusão de reservas concorrentes (ver ADR-0005).
- Custo: SQLite não é adequado para escrita concorrente pesada; documentado como limitação
  conhecida, não como decisão definitiva de arquitetura.
