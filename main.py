from fastapi import FastAPI
from app.database.db import inicializar_banco
from app.routers import usuarios, tarefas, auth

app = FastAPI(title="Gerenciador de Tarefas com Usuários")

@app.on_event("startup")
def on_startup():
    inicializar_banco()

# Inclui os módulos de rotas registrados
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(tarefas.router, prefix="/tarefas", tags=["Tarefas"])
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])