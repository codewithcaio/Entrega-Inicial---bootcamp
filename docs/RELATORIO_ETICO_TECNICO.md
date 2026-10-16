# Análise comparativa e ético-técnica do uso de IA — SalaFácil

Entrega 2 · Issue #31 · Consolidação: 16/10/2026.

| Integrante | RA |
|---|---|
| Gabriel Vieira Souza | 22552446 |
| Caio da Silva Diniz | 22552405 |

Repositório: [Entrega-Inicial---bootcamp](https://github.com/codewithcaio/Entrega-Inicial---bootcamp).
Preparação assistida pelo OpenAI Codex desktop, a pedido de Gabriel. Este texto
integra a documentação do projeto e deve compor o PDF consolidado da Entrega 2.

## 1. Método e limites da comparação

A análise combina evidências do projeto com documentação oficial consultada em
16/10/2026. São três níveis diferentes de evidência:

- **Uso comprovado:** Gabriel utilizou o OpenAI Codex no aplicativo desktop.
  As capturas [README](../evidence/ai/codex-readme.png) e
  [relatório](../evidence/ai/codex-relatorio.png), os arquivos preparados e os
  logs registram atividades de inspeção, edição, testes e documentação.
- **Declaração original:** o [ADR-0004](adr/0004-uso-de-agente-ia.md) registra
  Claude Code e seu contexto. Essa declaração não equivale a uma sessão observada
  nesta revisão. A presença de configurações para um assistente também não
  comprova que ele foi executado.
- **Avaliação documental:** Codex CLI, Cursor e Antigravity foram comparados por
  suas documentações. Não há experimento equivalente registrado com essas três
  ferramentas no SalaFácil. Codex desktop e Codex CLI são interfaces distintas;
  as capturas do aplicativo não devem ser rotuladas como uso do CLI.

Não foi realizado benchmark controlado entre ferramentas. Não há base para
classificar qual gera menos defeitos, custa menos ou economiza mais tempo neste
projeto. Recursos e permissões variam por versão, plataforma, conta e configuração.

## 2. Matriz comparativa

| Ferramenta e base da análise | Pontos fortes para o fluxo SDD | Limitações e cuidado necessário | Impacto demonstrado no SalaFácil |
|---|---|---|---|
| **OpenAI Codex desktop — uso comprovado por Gabriel** | Na interação registrada, reuniu inspeção de arquivos, alterações, execução de testes e preparação de documentação. Permitiu confrontar requisitos com resultados concretos. | A resposta do agente precisa ser conferida nos arquivos e logs. Orientações de upload e escolha da branch exigiram acompanhamento humano; gerar um documento não comprova publicação ou aprovação. | Apoio à revisão inicial e às correções/documentação da Entrega 2. Os resultados das seções 3 e 7 são observações do processo, sem atribuição causal exclusiva ao modelo. |
| **Claude Code — declaração original e pesquisa documental** | O projeto já registra contexto para o agente e uma decisão de arquitetura sobre seu uso. A documentação descreve modos de permissão e isolamento que podem apoiar trabalho sobre o repositório. | O efeito das proteções depende do modo e da configuração. Permissão para executar uma ação não comprova que ela está correta. Não foi observada uma sessão original para comparar qualidade ou produtividade. | Escolha declarada no ADR-0004. Contribuição por arquivo, taxa de acerto e desempenho não foram medidos. Fonte: [segurança do Claude Code](https://code.claude.com/docs/en/security). |
| **Codex CLI — pesquisa documental** | Permite inspecionar, editar e executar comandos pelo terminal; pode incorporar instruções do projeto e integrar tarefas ao fluxo de desenvolvimento. | Requer familiaridade com terminal e conferência de mudanças e comandos. A documentação de capacidade não demonstra o resultado que teria neste projeto. | Não houve sessão do executável CLI comprovada nesta revisão; não se transferem automaticamente as evidências do aplicativo. Fonte: [Codex CLI](https://developers.openai.com/codex/cli/). |
| **Cursor — pesquisa documental** | Integra assistência à edição e ao contexto do projeto; a documentação descreve revisão de ações sensíveis e controle de acesso a arquivos. | Edições e comandos podem produzir efeitos antes de uma revisão completa, dependendo da configuração e de processos que recarregam arquivos. As aprovações não eliminam alucinação ou injeção de instruções. | Não há sessão prática comprovada. O arquivo `.cursorrules` é contexto disponível, não prova de utilização. Fonte: [Agent Security](https://cursor.com/docs/agent/security). |
| **Antigravity — pesquisa documental** | Os planos e artefatos tornam a proposta do agente inspecionável antes da execução; a política de revisão permite organizar pontos de intervenção humana. | A política selecionada altera quando o agente pausa. Um plano legível ainda pode conter premissas erradas e precisa ser comparado à especificação e ao diff. | Não há execução registrada no SalaFácil. O benefício descrito é potencial, sem métrica prática atribuída. Fonte: [Artifact review](https://antigravity.google/docs/artifact-review). |

A conclusão aplicável ao grupo é metodológica: contexto versionado, alterações
pequenas e validação independente permitem avaliar qualquer assistente. A marca
ou a fluência da resposta não substituem esses critérios.

## 3. Qualidade das especificações e do código: casos verificáveis

O [registro de refinamentos](REFINEMENTS.md) e o
[índice dos ADRs](adr/README.md) ligam requisitos a decisões e consequências.
A contribuição da assistência foi organizar e implementar trabalho verificável;
a aceitação dependeu dos contratos, testes, revisão e evidências.

| Caso | Evidência e resultado | Interpretação crítica |
|---|---|---|
| Datas e contratos da API | SPEC e refinamentos registram UTC, intervalos, validação e precedência dos erros. | Uma solução aparentemente plausível pode divergir da regra; a especificação precisa declarar o comportamento observável. |
| Concorrência em SQLite | O ADR-0005 e os refinamentos registram a estratégia transacional. | Um teste sequencial de criação não basta para demonstrar proteção contra duas reservas simultâneas. A correção exige examinar a transação e os testes específicos. |
| Depreciação de `utcnow` | [Comparativo](AVISOS_DEPRECACAO.md): 78 testes aprovados; avisos de 55 para 1 após a correção. | O aviso externo restante foi declarado. Ocultar avisos não seria corrigir a origem do problema. |
| Novos cenários de borda | [Relatório](TESTES_BORDA_ENTREGA2.md): 17 casos adicionais, total de 95 aprovados. | Os novos casos passaram na implementação existente; não comprovam a descoberta de 17 defeitos. A ampliação fortalece a verificação, sem provar ausência de erros. |
| Documentação e publicação | Houve correção de links para o local efetivo dos logs e sincronização de branches pelos PRs #37 e #39. | A orientação textual e o arquivo local não bastam: caminho publicado, branch de destino e conteúdo final precisam de conferência. |

Esses casos não constituem comparação experimental entre modelos. Não foi medida
a quantidade de defeitos produzidos por cada ferramenta nem a produtividade sem IA.

## 4. Alucinação, código inseguro e ações destrutivas

Um agente pode sugerir uma API inexistente, interpretar uma regra incorretamente,
remover uma proteção ou executar um comando com alcance maior que o pedido. No
SalaFácil, pontos sensíveis incluem normalização de datas, sobreposição de
reservas, tratamento de erros e persistência. Código que executa pode ainda
violar os contratos da SPEC.

Também é necessário separar instruções autorizadas de conteúdo consultado.
Comentários, documentos, páginas e saídas de ferramentas podem conter comandos
maliciosos ou instruções fora da tarefa. A OWASP descreve esse risco como
[injeção de instruções em modelos](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).
A existência de uma instrução em um arquivo não autoriza sua execução.

O fluxo adotado ou proposto para controlar esses riscos é:

1. Vincular o pedido a uma Issue, à SPEC e a critérios observáveis.
2. Trabalhar em branch própria e limitar a alteração ao escopo autorizado.
3. Conferir o diff, sobretudo exclusões, comandos, dependências e transações.
4. Executar testes pertinentes e preservar saída, ambiente e código de saída.
5. Exigir revisão humana e verificar o destino do PR antes do merge.
6. Manter ações destrutivas, publicação e acesso externo sujeitos à autorização
   correspondente; não ampliar permissões apenas para eliminar uma falha.

Os 95 testes aprovados não equivalem a uma auditoria de segurança. Não há neste
material comprovação de teste de invasão, carga ou homologação de produção.
A aplicação acadêmica também não deve ser apresentada como tendo autenticação
completa: aceitar um identificador de usuário não comprova a identidade de quem
faz a requisição. Uma implantação com dados reais exigiria avaliar autenticação,
autorização e outras proteções antes do uso.

## 5. Privacidade, vazamento e confidencialidade

Fornecer contexto ao assistente pode expor código, dados de reservas, nomes,
e-mails, credenciais e conteúdo dos logs. Um repositório público aumenta a
necessidade de conferir o que será publicado. O `.gitignore` ajuda a evitar o
versionamento de arquivos, mas não é, por si só, uma barreira de acesso para IA.

Para este projeto, devem ser usados dados de teste e apenas os arquivos
necessários ao pedido. Antes de enviar logs e capturas, conferir segredos,
caminhos pessoais, abas de navegador e informações de terceiros. Os nomes e RAs
exigidos na submissão não justificam publicar outros dados pessoais.

A equipe deve verificar as políticas da conta e do produto efetivamente usados
quanto a armazenamento, retenção, treinamento e compartilhamento. Não se presume
que todas as ferramentas ou modalidades de assinatura tratem os dados da mesma
forma. Permissões mínimas e aprovação de conexões externas reduzem exposição,
mas não demonstram que nunca ocorreu vazamento.

Não foi realizada auditoria completa de privacidade ou busca certificada de
segredos. O relatório descreve riscos e controles; não atesta ausência de exposição.

## 6. Propriedade intelectual e direitos autorais

Uma sugestão de IA não deve ser tratada como prova de originalidade ou de licença
compatível. Trechos de origem identificável precisam ter sua procedência e
condições verificadas; dependências e avisos de terceiros devem ser preservados.
A equipe permanece responsável por revisar o material incorporado e por declarar
o uso de assistência na atividade acadêmica.

Na base inspecionada para este documento não foi localizado arquivo de licença
com nome `LICENSE` ou `COPYING`. Isso é uma pendência de definição pelos autores,
não autorização para o agente escolher uma licença em nome deles. O GitHub
explica que publicar o código e conceder uma licença de reutilização são decisões
distintas: [Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

Esta análise não determina a titularidade de cada trecho gerado nem fornece uma
conclusão jurídica sobre direitos autorais. Para a entrega, a medida concreta é
manter autoria humana, assistência de IA, referências e dependências identificadas,
e evitar prometer permissões de reutilização ainda não definidas pelo grupo.

## 7. Homologação humana no SDD e governança

No desenvolvimento orientado por especificação, o agente pode propor código,
testes e documentação. Cabe aos integrantes verificar se o resultado resolve o
problema, respeita o escopo e possui evidências suficientes para ser aceito.

O processo de aceitação deve percorrer: **Issue → SPEC/ADR → branch → alteração
→ testes → PR com evidências → revisão por outro integrante → merge**. Quando os
testes revelarem uma lacuna de contrato, registrar o motivo e a decisão em
REFINEMENTS e atualizar a SPEC antes de aceitar o novo comportamento.

O projeto tem uma limitação histórica explícita: os PRs iniciais #1–#7 foram
mesclados sem aprovação formal prévia registrada. As revisões documentais
posteriores não criam aprovações retroativas. Uma aprovação do índice de ADRs
também não significa nova homologação de todo o código original.

Exemplos de rastreabilidade:

- [PR #25](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/25): execução Docker histórica, evidências e declaração do uso de Codex.
- [PR #35](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/35): índice de decisões e trade-offs.
- [PR #36](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/36): correção de depreciação e comparação antes/depois.
- [PR #38](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/38): ampliação dos testes de borda.
- [PR #40](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/40): refinamentos e especificação consolidada.
- [PR #41](https://github.com/codewithcaio/Entrega-Inicial---bootcamp/pull/41): README final e fluxo da aplicação.

Os comentários de revisão devem refletir uma conferência real. Um texto sugerido
por IA para o revisor só pode ser adotado depois dessa conferência; colar uma
aprovação não executa uma revisão. Gabriel e Caio continuam responsáveis pela
homologação, mesmo quando o agente executa ferramentas ou os checks passam.

## 8. Relato sintético da experiência

Este relato resume fatos registrados no desenvolvimento; não atribui falas,
sentimentos, horas trabalhadas ou uso de ferramentas não comprovados aos integrantes.

O trabalho partiu de uma API com especificação, ADRs e harness de testes. A revisão
assistida ajudou a relacionar contratos de datas, validação e concorrência ao
código e a transformar resultados de execução em documentação rastreável. Na
Entrega 2, o foco foi consolidar decisões, reduzir depreciações e reforçar os
cenários de borda, preservando os limites do problema original.

Gabriel conduziu a interação comprovada com o Codex desktop e as etapas manuais
de publicação. Os PRs registram a participação de revisão de Caio nos trabalhos
referenciados; essa revisão precisa ser avaliada pelo seu conteúdo e escopo, sem
inferir que todo trecho do projeto foi novamente auditado.

Um aprendizado técnico foi manter separadas as medições de cada ambiente:

| Execução registrada | Testes aprovados | Avisos | Duração do pytest | Cobertura total | Saída |
|---|---:|---:|---:|---:|---:|
| Docker histórico, 12/09/2026 | 78 | 55 | 1,67 s | 93,60% | 0 |
| Python local após correção de depreciação, 15/10/2026 UTC | 78 | 1 | 1,48 s | 93,60% | 0 |
| Python local com novos testes de borda, 15/10/2026 UTC | 95 | 1 | 2,12 s | 94,51% | 0 |
| Docker final, 16/10/2026 UTC | 95 | 1 | 2,16 s | 94,51% | 0 |

Todas essas execuções passaram os testes coletados, mas a contagem e o tempo não
são intercambiáveis. A cobertura de services foi de 100% nas execuções relatadas;
isso não significa cobertura total da aplicação ou prova de correção completa.
Os registros estão no [relatório de execução](EXECUTION_REPORT.md), no
[comparativo de avisos](AVISOS_DEPRECACAO.md) e no
[relatório dos novos testes](TESTES_BORDA_ENTREGA2.md).

Outro aprendizado foi operacional: conferir a branch de destino, o local de
upload e os links publicados faz parte da qualidade da entrega. A assistência
foi útil para preparar material, mas as dificuldades nesses passos mostram que
orientações precisam ser concretas e verificáveis. A comunicação em equipe deve
explicar o que mudou, como foi validado e o que permanece pendente.

## 9. Condições para a entrega final

Este documento cobre comparação, quatro pilares ético-técnicos e relato de
experiência. A execução Docker de 16/10/2026 foi conferida nos quatro arquivos
do harness: 95 aprovados, um aviso e saída 0. O [relatório](EXECUTION_REPORT.md)
registra os resultados da Issue #34. Resta revisar/integrar essa atualização,
conferir a integração final na main e consolidar o PDF com identificação,
repositório, resultados e PRs.

A escolha de uma licença e a revisão da dependência que mantém um aviso externo
são melhorias registradas; não foram silenciosamente implementadas nesta tarefa.
A revisão deste relatório deve conferir fatos, links, limites das conclusões e
adequação ao enunciado, além da clareza do texto.

## 10. Referências e evidências

Fontes oficiais consultadas em 16/10/2026; suas descrições são documentais e não
comprovam utilização prática no projeto:

1. [OpenAI — Codex CLI](https://developers.openai.com/codex/cli/).
2. [Anthropic — Security, Claude Code](https://code.claude.com/docs/en/security).
3. [Cursor — Agent Security](https://cursor.com/docs/agent/security).
4. [Google — Antigravity Artifact review](https://antigravity.google/docs/artifact-review).
5. [OWASP — LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).
6. [GitHub — Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

Evidências locais: [registro factual de IA](../evidence/ai/REVISION.md),
[SPEC](SPEC.md), [refinamentos](REFINEMENTS.md), [ADRs](adr/README.md),
[histórico](CHANGELOG_REVIEW.md) e relatórios ligados nas seções anteriores.
