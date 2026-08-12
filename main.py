"""Módulo principal da aplicação FastAPI.

Este arquivo é responsável por inicializar a API, incluir os roteadores
de endpoints (Usuários, Tarefas, Autenticação) e executar eventos de inicialização.
"""

from fastapi import FastAPI
from app.database.db import inicializar_banco
from app.routers import auth, tarefas, usuarios

# Instância principal do FastAPI com metadados para a documentação interativa
app = FastAPI(
    title="API de Gerenciamento de Tarefas",
    description="API RESTful para gerenciamento de tarefas pessoais com autenticação JWT e PostgreSQL.",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    """Evento executado automaticamente ao iniciar a aplicação.

    Garante a criação de todas as tabelas no banco de dados caso ainda não existam.
    """
    inicializar_banco()


# Inclusão dos roteadores (os prefixos e tags já estão definidos em cada arquivo de rota)
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tarefas.router)


@app.get("/", tags=["Health Check"])
def health_check():
    """Endpoint de checagem para verificar se a API está online."""
    return {"status": "ok", "mensagem": "API de Gerenciamento de Tarefas está rodando perfeitamente!"}