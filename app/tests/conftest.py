# tests/conftests.py
import pytest
from typing import Generator
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from main import app
from app.database.db import get_session


# Cria um banco SQLite só em memória - nasce e morre com o teste
engine_teste = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    """Cria um banco SQLite temporário em memória, entrega uma sessão
    pronta pro teste usar, e apaga tudo assim que o teste terminar.
    """
    SQLModel.metadata.create_all(engine_teste)  # cria todas as tabelas nesse banco falso
    with Session(engine_teste) as session:
        yield session   # entrega a sessão pronta pro teste usar
    SQLModel.metadata.drop_all(engine_teste)    # apaga tudo depois que o teste termina

@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Cria um TestClient da aplicação, substituindo get_session pela
    sessão de teste — assim as rotas usam o banco temporário sem saber disso.
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield  client

    app.dependency_overrides.clear()

@pytest.fixture(name="token_usuario")
def token_usuario_fixture(client: TestClient) -> str:
    """Cadastra um usuário de teste, faz login, e devolve o token pronto para usar."""

    client.post("/usuarios/", json={
        "nome": "Dono Tarefa",
        "email": "dono.tarefa@exemplo.com",
        "senha": "senha123"
    })

    response = client.post("/auth/login", data={
        "username": "dono.tarefa@exemplo.com",
        "password": "senha123"
    })

    return response.json()["access_token"]

@pytest.fixture(name="token_outro_usuario")
def token_outro_usuario_fixture(client: TestClient) -> str:
    """Cadastra um segundo usuário de teste, faz login, e devolve o token dele."""

    client.post("/usuarios/", json={
        "nome": "Outro Dono",
        "email": "outro.dono@exemplo.com",
        "senha": "senha456"
    })

    response = client.post("/auth/login", data={
        "username": "outro.dono@exemplo.com",
        "password": "senha456"
    })

    return response.json()["access_token"]