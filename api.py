from fastapi import FastAPI, Depends
from sqlmodel import Session
from database.db import get_session, inicializar_banco
from database.models import Tarefa
from database.crud import criar_tarefa, listar_tarefa, buscar_por_responsavel, deletar_tarefa, concluir_tarefa

app = FastAPI()

@app.on_event("startup")
def on_startup():
    inicializar_banco()

@app.post("/tarefas")
def rota_criar_tarefa(tarefa: Tarefa, session: Session = Depends(get_session)):
    return criar_tarefa(session, tarefa)

@app.get("/tarefas")
def rota_listar_tarefas(session: Session = Depends(get_session)):
    return listar_tarefa(session)

@app.get("/tarefas/responsavel/{nome}")
def rota_buscar_responsavel(nome: str, session: Session = Depends(get_session)):
    return buscar_por_responsavel(session, nome)

@app.delete("/tarefa/{tarefa_id}")
def rota_deletar_tarefa(tarefa_id: int, session: Session = Depends(get_session)):
    sucesso = deletar_tarefa(session, tarefa_id)
    if not sucesso:
        return {"erro": "tarefa não encontrada"}
    return {"mensagem": "tarefa removida"}

@app.patch("/tarefa/{tarefa_id}/concluir")
def rota_concluir_tarefa(tarefa_id: int, session: Session = Depends(get_session)):
    tarefa = concluir_tarefa(session, tarefa_id)
    if not tarefa:
        return {"erro": "tarefa não encontrada"}
    return tarefa