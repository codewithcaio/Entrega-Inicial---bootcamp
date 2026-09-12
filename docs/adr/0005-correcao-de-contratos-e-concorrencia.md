# ADR-0005 — UTC, consultas e concorrência SQLite

- Data: 2026-09-11
- Status: implementado nesta revisão; revisão humana do grupo pendente.

## Problema
Datas com offset causavam erro; RF09 não tinha intervalo implementado; a verificação de
conflito seguida de inserção não garantia exclusão de reservas concorrentes.

## Decisão
Normalizar entradas para UTC sem offset e declarar o contrato de saída. Implementar intervalo
inclusivo sem remover o filtro de um dia. Serializar escritas SQLite com BEGIN IMMEDIATE antes
de qualquer leitura de decisão; manter até commit/rollback. Espera limitada a 30 segundos,
com retorno 503 em caso de banco ocupado. Aplicar também a cadastros únicos e cancelamentos.

## Consequências
Uma reserva concorrente aguarda e então observa a reserva confirmada pelo outro escritor.
Há apenas um escritor SQLite por vez, aceitável nesta fase. Migrar para PostgreSQL requer
estratégia própria de lock/constraint e testes novos; não basta trocar DATABASE_URL.
Cobertura inclui teste com arquivo real e conexões independentes; não é teste de carga.
