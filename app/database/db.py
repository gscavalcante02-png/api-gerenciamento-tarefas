"""Módulo de Conexão e Gerenciamento do Banco de Dados.

Configura o motor de conexão (Engine) do SQLAlchemy com o driver 'psycopg' v3,
gerencia o ciclo de vida das sessões (SessionLocal) e disponibiliza
funções utilitárias para injeção de dependência e inicialização de tabelas.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlmodel import Session, SQLModel

from app.core.config import settings

# Monta a URL de conexão do PostgreSQL utilizando as credenciais carregadas do .env
DATABASE_URL = (
    f"postgresql+psycopg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

# Engine central do SQLAlchemy
# echo=True exibe no terminal os comandos SQL gerados durante as operações
engine = create_engine(DATABASE_URL, echo=True)

# Fábrica para geração de sessões síncronas do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa legada para compatibilidade de mapeamento ORM
Base = declarative_base()


def get_session() -> Generator[Session, None, None]:
    """Injeção de dependência para fornecer uma sessão do banco de dados por requisição.

    Abre uma nova sessão a cada chamada e garante o fechamento correto (db.close())
    ao finalizar a execução da rota, mesmo que ocorram exceções.

    Yields:
        Session: Sessão ativa para interagir com o PostgreSQL.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def inicializar_banco() -> None:
    """Cria todas as tabelas mapeadas nos modelos (SQLModel) diretamente no banco.

    Executado durante a inicialização da aplicação FastAPI.
    """
    # Garante a importação dos modelos para que o SQLModel registre a metadata das tabelas
    from app.database import models  # noqa: F401

    SQLModel.metadata.create_all(bind=engine)