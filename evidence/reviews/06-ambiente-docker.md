# Revisão formal — Ambiente Docker

PR original: #6 (feature/ambiente-docker), mesclada sem aprovação formal registrada antes do
merge. Esta PR reabre o escopo para revisão explícita.

## Escopo revisado
- Dockerfile: copia src/, tests/, docs/, scripts/ e dá permissão de execução ao harness
- docker-compose.yml: sobe a API com volume de dados persistente
- .github/workflows/tests.yml: job docker-test builda e roda o container de verdade no
  runner do GitHub Actions

## Checklist do revisor
- [ ] Dockerfile copia todos os diretórios usados pelo harness
- [ ] Job docker-test do CI salva os logs em evidence/docker/
- [ ] Aprovado antes do merge (ver aba Files changed desta PR)
