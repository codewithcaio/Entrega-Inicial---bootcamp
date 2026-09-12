# Correções da revisão — 2026-09-11

- Docker inclui scripts; Compose permite expediente via .env e preserva logs no host.
- Harness Python funciona em Windows/Linux, guarda logs/JUnit/cobertura e aplica meta de services.
- CI contém jobs Python e Docker com upload de evidências; execução remota ainda não comprovada.
- Datas com offset são normalizadas para UTC antes da validação.
- Consulta de reservas aceita intervalo de datas inclusivo, além do filtro de um dia.
- Escritas SQLite são serializadas antes de ler/gravar; teste verifica reservas concorrentes.
- .env é carregado, com prioridade para variáveis explícitas; configuração inválida é rejeitada.
- README, SPEC, refinamentos e ADRs atualizados; cobertura agora inclui toda app.
- Modelo de PDF, pastas de evidências e registro factual da revisão assistida adicionados.

Resultado: 78 testes passaram localmente, 94% de cobertura total arredondada, services 100%.
Pendências: Docker real, link GitHub, Issues/PRs/reviews reais e PDF final preenchido.
