# Colaboração, experiência e revisão entre pares — Entrega 2

Gabriel Vieira Souza (RA 22552446) e Caio da Silva Diniz (RA 22552405).
Registro consolidado em 16/10/2026.

## Participação conjunta

O grupo declara que os dois integrantes realizaram o trabalho conjuntamente,
com participação equilibrada. A distribuição abaixo apresenta frentes
complementares de atuação; não representa contagem individual de horas, linhas
de código ou percentual de autoria de cada arquivo. A conta que publica um PR
não identifica, sozinha, todas as pessoas que contribuíram para sua elaboração.

| Frente | Participação do grupo e registro disponível |
|---|---|
| Especificação, regras e arquitetura | Trabalho conjunto de Gabriel e Caio, relacionando SPEC, refinamentos e ADRs. |
| Correções, testes e documentação | Trabalho conjunto de consolidação; Gabriel conduziu a interação registrada com Codex e a publicação dos PRs; Caio participou da revisão registrada no GitHub. |
| Ferramentas de IA | Gabriel utilizou Codex desktop; o grupo informou que Caio utilizou Claude Code como apoio ao trabalho. Não se atribui uma tarefa específica ao Claude sem registro adicional. |
| Execução final do Docker | Realizada por Gabriel em seu computador, com 95 testes aprovados e saída 0; os arquivos do harness são a evidência dessa execução. |
| Revisão e aceite | As contas autoras e revisoras de cada PR estão discriminadas abaixo, sem transformar comentário em aprovação formal. |

## Relatos dos integrantes

### Gabriel Vieira Souza

Participei com Caio da consolidação das correções, dos testes e da documentação
do SalaFácil. Utilizei o Codex desktop como apoio e executei a validação final no
Docker, preservando os arquivos do harness. Organizar branches, uploads e o
destino dos PRs foi um desafio concreto nesta etapa. Aprendi a conferir as
orientações do assistente e a distinguir passagem dos testes, cobertura e
aprovação humana antes de considerar uma alteração concluída.

### Caio da Silva Diniz

Participei com Gabriel da consolidação do projeto e da revisão das alterações
da Entrega 2, utilizando também Claude Code como ferramenta de apoio.
Minha participação nas revisões está registrada na conta codewithcaio.
A experiência destacou a necessidade de relacionar especificação, testes e
decisões técnicas e de conferir a branch de destino antes do merge.
O aprendizado foi que o apoio da IA e os checks automáticos não substituem
a responsabilidade dos integrantes pela análise e pelo aceite das mudanças.

## Autoria e revisão registradas no GitHub

Os nomes abaixo representam as contas registradas pelo GitHub. A descrição de
trabalho conjunto acima é a declaração do grupo, distinta desse registro de contas.

| PR | Escopo e destino | Autor | Revisor | Registro anterior ao merge |
|---|---|---|---|---|
| [#35](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/35) | Índice dos ADRs; develop | gabrielvieira05 | codewithcaio | Aprovação formal (APPROVED) |
| [#36](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/36) | Depreciações; main | gabrielvieira05 | codewithcaio | Aprovação formal (APPROVED) |
| [#37](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/37) | Sincronização main → develop; develop | gabrielvieira05 | codewithcaio | Aprovação formal (APPROVED) |
| [#38](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/38) | Testes de borda; main | gabrielvieira05 | codewithcaio | Aprovação formal (APPROVED) |
| [#39](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/39) | Sincronização main → develop; develop | gabrielvieira05 | codewithcaio | Comentário (COMMENTED), sem APPROVED |
| [#40](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/40) | SPEC e refinamentos; develop | gabrielvieira05 | codewithcaio | Aprovação formal (APPROVED) |
| [#41](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/41) | README e fluxo; develop | gabrielvieira05 | codewithcaio | Aprovação formal (APPROVED) |
| [#42](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/42) | Análise de IA; develop | gabrielvieira05 | codewithcaio | Aprovação formal (APPROVED) |
| [#43](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/43) | Execução Docker; develop | gabrielvieira05 | codewithcaio | Aprovação formal (APPROVED) |
| [#44](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/44) | Integração final; main | gabrielvieira05 | codewithcaio | Aprovação formal (APPROVED) |
| [#45](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/45) | Link dos ADRs; develop | gabrielvieira05 | codewithcaio | Aprovação formal (APPROVED) |
| [#46](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/46) | Correção na main; main | gabrielvieira05 | codewithcaio | Aprovação formal (APPROVED) |

O PR #39 registra comentário de Caio antes do merge, mas não aprovação formal.
Os PRs iniciais #1–#7 também não possuem aprovação formal prévia registrada.
Essas limitações são preservadas; uma revisão posterior não é retroativa.
Revisão entre pares existe quando um integrante examina a mudança do outro;
esta tabela não afirma que houve revisão nos dois sentidos nesta sequência de PRs.

## Desvios de processo e correção

Os PRs [#36](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/36)
e [#38](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/38)
foram abertos e integrados com destino main, embora o fluxo definido em
CONTRIBUTING previsse feature → develop → main. Nesta sequência, a orientação
do assistente e a conferência manual da branch de destino não evitaram o desvio.
Não foi uma exceção técnica planejada. Os PRs
[#37](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/37) e
[#39](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/39)
sincronizaram posteriormente o conteúdo com develop. O aprendizado foi conferir
explicitamente base e compare antes de criar ou aprovar um PR.

O [PR #27](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/27),
aberto por codewithcaio, propôs um template de PR e foi fechado sem merge.
Já existia `.github/PULL_REQUEST_TEMPLATE.md`; a proposta acrescentava
`.github/pull_request_template.md`. A tarefa redundante mostra a necessidade
de pesquisar o repositório antes de seguir uma sugestão do assistente.
O fechamento sem merge evitou incorporar a duplicação.

## Limites da assistência e revisão humana

Sugestões podem ser redundantes ou apontar a branch errada sem que a suíte de
testes detecte esse problema de processo. Além do código, a equipe precisa
conferir escopo, arquivos existentes, destino do PR, links e evidências.
Textos de review sugeridos por IA só devem ser adotados após a leitura e a
conferência efetiva pelo revisor; gerar ou colar um comentário não realiza a revisão.

O uso de Claude Code por Caio foi informado pelo grupo; esta atualização não
adiciona uma captura ou log de sessão dessa ferramenta. Não há benchmark
equivalente entre Claude Code, Codex desktop, Codex CLI, Cursor e Antigravity.
Os números da suíte não permitem atribuir produtividade ou taxa de erro a um modelo.
