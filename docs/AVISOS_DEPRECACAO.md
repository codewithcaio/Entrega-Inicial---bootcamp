# Correção de avisos de depreciação - Issue #32

Data da verificação: 15/10/2026. Execuções Python locais no Windows, realizadas pelo
OpenAI Codex desktop a pedido de Gabriel Vieira Souza. Não são execuções Docker.

## Antes e depois

| Medida | Antes | Depois |
|---|---|---|
| Testes aprovados | 78 de 78 | 78 de 78 |
| Falhas/erros | 0 | 0 |
| Avisos de depreciação | 55 | 1 |
| Duração do pytest | 1,57 s | 1,48 s |
| Cobertura total de app | 93,60% | 93,60% |
| Cobertura de services | 100% | 100% |
| Código de saída | 0 | 0 |

Os tempos são observações dessas execuções, não um benchmark de desempenho.

## Causas e alterações

Dos 55 avisos observados, 54 vieram de `datetime.utcnow()`: 29 na geração das datas
de teste, 24 no valor padrão de `Booking.created_at` e um no teste de reserva no
passado. As chamadas foram substituídas por
`datetime.now(timezone.utc).replace(tzinfo=None)`.

A obtenção do instante é explicitamente UTC. O offset é removido apenas para
preservar o contrato existente da SPEC, que armazena e retorna UTC sem sufixo.
O valor de `created_at` continua sendo calculado a cada inserção, por callable
do SQLAlchemy. Não foi substituído por um instante fixo na importação do módulo.

O teste de criação de reserva agora também verifica que `created_at` é retornado
sem offset e está entre os instantes UTC anteriores e posteriores à requisição.
Os demais testes continuam cobrindo datas com offset, limites e concorrência.

Arquivos de código e testes alterados:

- `src/app/models.py`
- `tests/conftest.py`
- `tests/test_edge_cases.py`
- `tests/test_bookings.py`

## Aviso externo preservado

Resta um aviso em `starlette/testclient.py:40`: Starlette 0.38.6 usa
`anyio.abc.BlockingPortal`, alias descontinuado pelo AnyIO 4.15.1 do ambiente
observado. A mensagem recomenda `anyio.from_thread.BlockingPortal`.

Esse aviso pertence à dependência, não a uma chamada do SalaFácil. Não foram
adicionados filtros de warnings, alterações em bibliotecas instaladas ou
rebaixamentos de dependências para ocultá-lo. Não foram observados avisos de
configuração antiga do Pydantic nessa execução.

Eliminar o aviso restante requer avaliar uma atualização compatível do conjunto
FastAPI/Starlette/AnyIO e repetir os testes. Não se deve declarar zero avisos nem
a eliminação completa das depreciações com esta alteração. O resultado desta
etapa é: 54 avisos do projeto eliminados e uma limitação externa documentada.

## Reprodução e evidências

Com as dependências instaladas, na raiz do projeto:

```powershell
$env:PYTEST_ADDOPTS='--basetemp=../avisos32-after-tmp'
python scripts/run_tests.py
```

O `--basetemp` apenas seleciona uma pasta temporária acessível neste ambiente.
Não suprime avisos. O ambiente observado usou Python 3.12.14, FastAPI 0.115.0,
Starlette 0.38.6, AnyIO 4.15.1, SQLAlchemy 2.0.35, pytest 8.3.3 e pytest-cov 5.0.0.
As dependências transitivas podem variar em outra instalação; por isso a contagem
de avisos deve ser conferida também no CI e na execução Docker final.

- Antes: [log](../evidence/tests/20261015T232801169073Z/pytest.log),
  [ambiente](../evidence/tests/20261015T232801169073Z/environment.json),
  [cobertura](../evidence/tests/20261015T232801169073Z/coverage.json) e
  [JUnit](../evidence/tests/20261015T232801169073Z/junit.xml).
- Depois: [log](../evidence/tests/20261015T232828776932Z/pytest.log),
  [ambiente](../evidence/tests/20261015T232828776932Z/environment.json),
  [cobertura](../evidence/tests/20261015T232828776932Z/coverage.json) e
  [JUnit](../evidence/tests/20261015T232828776932Z/junit.xml).

## Referências técnicas

- [Python 3.12: depreciação de utcnow e uso de UTC](https://docs.python.org/3.12/whatsnew/3.12.html#datetime).
- [Registro upstream do alias BlockingPortal no TestClient](https://github.com/Kludex/starlette/issues/3497).
- [Código do TestClient na versão Starlette 0.38.6](https://github.com/encode/starlette/blob/0.38.6/starlette/testclient.py).
