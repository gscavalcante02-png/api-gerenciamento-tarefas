from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from app.database.schemas import TarefaCreate, TarefaResponse
from app.database.db import get_session
from app.database import crud
from app.database.models import Tarefa
from app.core.security import obter_usuario_atual

router = APIRouter()



@router.post("/", response_model=Tarefa, status_code=status.HTTP_201_CREATED)
def criar_tarefa(
    tarefa: TarefaCreate,
    session: Session = Depends(get_session),
    usuario_atual = Depends(obter_usuario_atual)
):
    nova_tarefa = crud.criar_tarefa(
        session=session,
        titulo=tarefa.titulo,
        responsavel=tarefa.responsavel,
        usuario_id=usuario_atual.id, 
        descricao=tarefa.descricao
    )
    return nova_tarefa

@router.patch("/{tarefa_id}/concluir")
def rota_concluir_tarefa(
    tarefa_id: int,
    session: Session = Depends(get_session),
    usuario_atual = Depends(obter_usuario_atual)
):
    tarefa = crud.concluir_tarefa(session, tarefa_id, usuario_id=usuario_atual.id)
    if not tarefa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada ou não pertence a este usuário"
        )
    return tarefa

@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(
    tarefa_id: int,
    session: Session = Depends(get_session),
    usuario_atual = Depends(obter_usuario_atual)
):
    sucesso = crud.deletar_tarefa(session, tarefa_id, usuario_id=usuario_atual.id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada ou não pertence a este usuário"
        )
    return None