#!/usr/bin/env bash
# Executa o test harness completo (suíte pytest + relatório de cobertura).
# Uso: ./scripts/run_tests.sh          (ambiente local, precisa de venv ativado)
#      docker compose run --rm api ./scripts/run_tests.sh   (dentro do container)
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== SalaFácil — Test Harness =="
echo "Python: $(python --version)"
echo "Data/hora: $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
echo

python scripts/run_tests.py
