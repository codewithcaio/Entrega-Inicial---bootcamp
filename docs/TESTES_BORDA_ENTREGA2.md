# Testes de borda e inspeção lógica - Entrega 2

Tarefa: [Issue #28](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/issues/28).
Preparação: OpenAI Codex desktop, a pedido de Gabriel Vieira Souza.
Base: develop após a sincronização do PR #37, commit `689b6fe`.

## Casos já existentes

Os cenários citados na Issue #28 já tinham cobertura na suíte inicial: reservas
adjacentes, expediente, intervalo invertido, cancelamento repetido e entidades
inexistentes. A inspeção comparou os testes existentes com a SPEC; novos testes
foram acrescentados para comportamentos observáveis pela API ainda sem a mesma
verificação ponta a ponta.

## Ampliação da cobertura

O arquivo [test_entrega2_edges.py](../tests/test_entrega2_edges.py) acrescenta
17 casos, contando as parametrizações:

| Grupo | Casos | Regra ou requisito | Resultado esperado |
|---|---|---|---|
| Duração inválida pela API | 4 | RN02, RNF05 | HTTP 422 com motivo e sem persistência: zero, inversão, um microssegundo abaixo de 15 minutos ou acima de 8 horas |
| Duração nos limites exatos | 2 | RN02, RN03 | HTTP 201 para exatamente 15 minutos e 8 horas |
| Capacidade exata | 1 | RN04 | HTTP 201 quando participantes igualam a capacidade |
| Entidade ausente e intervalo invertido | 2 | RN07 | HTTP 404 antes da validação de negócio |
| Corpo inválido e entidades ausentes | 1 | SPEC seção 4.4 | HTTP 422 estrutural antes da busca de entidades |
| Cancelamento e isolamento entre salas | 1 | RF08, RF11 | Cancelamento idempotente libera a disponibilidade e outra sala não interfere |
| Disponibilidade de reservas adjacentes | 1 | RN01, RF11 | Nenhum intervalo livre falso entre reservas encostadas |
| Expediente completamente ocupado | 1 | RF11 | Lista de disponibilidade vazia com reservas válidas de 8h e 4h |
| Consultas de entidades ausentes | 3 | RF09, RF10, RF11 | HTTP 404 nas consultas de reservas e disponibilidade |
| Histórico e isolamento entre usuários | 1 | RF08, RF10 | Reserva cancelada permanece no histórico, sem reservas de outro usuário |

## Resultado real

Execução Python local no Windows, em 15/10/2026 às 23:50:40 UTC:

- 95 testes aprovados de 95 executados: 100% de passagem.
- 0 falhas e 0 erros; `EXIT_CODE=0`.
- 1 aviso externo de Starlette/AnyIO, já descrito em
  [AVISOS_DEPRECACAO.md](AVISOS_DEPRECACAO.md).
- 2,12 s de execução do pytest; não é medição de desempenho da API.
- Cobertura total: 310 de 328 linhas executáveis, 94,51% (95% arredondado).
- Cobertura de serviços: 100%; routers de salas: 100%.

Nenhum desses 17 casos novos falhou na versão inspecionada. Portanto esta etapa
não declara uma nova correção de código nem uma mudança de especificação.
As correções anteriores de UTC, intervalo, configuração e concorrência seguem
documentadas em [REFINEMENTS.md](REFINEMENTS.md) e no ADR-0005. A consolidação
do loop de re-especificação pertence à Issue #29.

Este resultado é local, não Docker, e não substitui a execução final da Issue #34.

## Reprodução

Na raiz do projeto, com as dependências instaladas:

```powershell
$env:PYTEST_ADDOPTS='--basetemp=../bordas28-tmp'
python scripts/run_tests.py
```

A opção escolhe uma pasta temporária acessível; nenhum filtro de avisos foi usado.

## Evidências completas

- [Log do harness](../evidence/tests/20261015T235040608066Z/pytest.log)
- [Ambiente e código de saída](../evidence/tests/20261015T235040608066Z/environment.json)
- [Cobertura JSON](../evidence/tests/20261015T235040608066Z/coverage.json)
- [JUnit](../evidence/tests/20261015T235040608066Z/junit.xml)

Alteração preparada para revisão humana e integração por PR na develop. O resultado
dos checks remotos e a aprovação devem ser conferidos no PR correspondente.
