"""Configuração de conexão com o banco (SQLAlchemy).

DATABASE_URL vem de variável de ambiente para permitir trocar entre o arquivo SQLite usado em
desenvolvimento/Docker e o SQLite em memória usado nos testes (ver docs/adr/0002).
"""
from __future__ import annotations

from pathlib import Path

from fastapi import Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import DATABASE_URL


# SQLite precisa desse flag para funcionar corretamente com múltiplas threads (o servidor
# ASGI pode atender requisições em threads diferentes).
connect_args = {"check_same_thread": False, "timeout": 30} if DATABASE_URL.startswith("sqlite") else {}

if not DATABASE_URL.startswith("sqlite"):
    raise ValueError("Esta versão suporta SQLite; outros bancos exigem estratégia de concorrência própria.")

if DATABASE_URL.startswith("sqlite:///") and DATABASE_URL != "sqlite:///:memory:":
    # Cobre tanto caminho relativo ("sqlite:///./data/x.db") quanto absoluto
    # ("sqlite:////app/data/x.db", usado no container) — garante que o diretório do
    # arquivo exista antes do SQLAlchemy tentar abrir o arquivo.
    raw_path = DATABASE_URL.replace("sqlite:///", "", 1)
    db_path = Path(raw_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency do FastAPI: entrega uma sessão por requisição e garante o fechamento."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_write_db(db=Depends(get_db)):
    """Reserva a escrita ANTES das leituras para impedir check-then-insert concorrente.

    O lock pertence ao arquivo SQLite, portanto também coordena processos distintos.
    """
    try:
        db.execute(text("BEGIN IMMEDIATE"))
        yield db
    except OperationalError as exc:
        db.rollback()
        if "locked" in str(exc).lower() or "busy" in str(exc).lower():
            raise HTTPException(status_code=503, detail="Banco ocupado; tente novamente.", headers={"Retry-After": "1"}) from exc
        raise
    finally:
        db.rollback()


def init_db() -> None:
    """Cria as tabelas caso não existam. Chamado no startup da aplicação."""
    from . import models  # noqa: F401  (garante que os models sejam registrados no Base)

    Base.metadata.create_all(bind=engine)
