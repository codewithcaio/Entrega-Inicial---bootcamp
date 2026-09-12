"""Leitura de configuração via variáveis de ambiente (ver .env.example)."""
from __future__ import annotations

import os
from datetime import time
from pathlib import Path

from dotenv import load_dotenv

# O ambiente explícito prevalece sobre o .env na raiz do projeto.
load_dotenv(Path(__file__).resolve().parents[2] / '.env', override=False)

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./data/booking.db")


def _parse_hhmm(value: str) -> time:
    hours, minutes = value.strip().split(":")
    return time(hour=int(hours), minute=int(minutes))


BUSINESS_HOURS_START: time = _parse_hhmm(os.environ.get("BUSINESS_HOURS_START", "08:00"))
BUSINESS_HOURS_END: time = _parse_hhmm(os.environ.get("BUSINESS_HOURS_END", "20:00"))

if BUSINESS_HOURS_START >= BUSINESS_HOURS_END:
    raise ValueError("BUSINESS_HOURS_START deve ser anterior a BUSINESS_HOURS_END.")
