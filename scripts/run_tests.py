"""Harness portátil: execução real, cobertura completa e logs persistidos."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output = root / "evidence" / "tests" / stamp
    output.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-m", "pytest", "-v", "--cov=app",
               "--cov-report=term-missing", f"--cov-report=json:{output / 'coverage.json'}",
               f"--junitxml={output / 'junit.xml'}"]
    env = os.environ.copy()
    env.update(PYTHONIOENCODING="utf-8", DATABASE_URL="sqlite:///:memory:",
               BUSINESS_HOURS_START="08:00", BUSINESS_HOURS_END="20:00")
    metadata = {"started_at_utc": stamp, "python": sys.version,
                "platform": platform.platform(), "command": command,
                "environment": env.get("EXECUTION_ENVIRONMENT", "local"),
                "test_database": "SQLite em memória e arquivos temporários",
                "test_business_hours_utc": "08:00–20:00"}
    with (output / "pytest.log").open("w", encoding="utf-8") as log:
        header = json.dumps(metadata, ensure_ascii=False, indent=2) + "\n"
        log.write(header)
        print(header, flush=True)
        process = subprocess.Popen(command, cwd=root, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, encoding="utf-8")
        for line in process.stdout:
            log.write(line)
            print(line, end="", flush=True)
        result = process.wait()
        coverage_file = output / "coverage.json"
        if coverage_file.exists():
            files = json.loads(coverage_file.read_text(encoding="utf-8"))["files"]
            services = [v["summary"] for k, v in files.items()
                        if "/services/" in k.replace("\\", "/")]
            statements = sum(v["num_statements"] for v in services)
            covered = sum(v["covered_lines"] for v in services)
            percent = 100 * covered / statements if statements else 0
            metadata["services_coverage_percent"] = percent
            if percent < 80:
                result = result or 1
            log.write(f"\nCobertura de services: {percent:.2f}% (mínimo 80%)\n")
        else:
            result = result or 1
        metadata["exit_code"] = result
        log.write(f"EXIT_CODE={result}\n")
    (output / "environment.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nEXIT_CODE={result}; evidências: {output}")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
