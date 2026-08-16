"""Módulo de rotas para gerenciamento de tarefas.

Contém os endpoints para criar, listar, alterar status e deletar tarefas,
garantindo que cada usuário só acesse e modifique os seus próprios dados.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import crud
from app.database.db import get_session
from app.database.models import Usuario
from app.dependencies import obter_usuario_atual
from app.schemas.tarefa import TarefaCreate, TarefaResponse

# Agrupa as rotas sob o prefixo '/tarefas' e a tag 'Tarefas' no Swagger
router = APIRouter(prefix="/tarefas", tags=["Tarefas"])


@router.post(
    "/",
    response_model=TarefaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova tarefa",
)
def criar_tarefa(
    tarefa: TarefaCreate,
    session: Session = Depends(get_session),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    """Cria uma nova tarefa atrelada automaticamente ao usuário autenticado.

    - **titulo**: Título descritivo da tarefa.
    - **responsavel**: Nome do responsável.
    - **descricao**: Detalhes adicionais (opcional).
    """
    nova_tarefa = crud.criar_tarefa(
        session=session,
        titulo=tarefa.titulo,
        responsavel=tarefa.responsavel,
        usuario_id=usuario_atual.id,
        descricao=tarefa.descricao,
    )
    return nova_tarefa


@router.get(
    "/",
    response_model=List[TarefaResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista as tarefas do usuário autenticado",
)
def listar_tarefas(
    session: Session = Depends(get_session),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    """Retorna todas as tarefas registradas para o usuário logado."""
    return crud.listar_tarefas_do_usuario(session, usuario_id=usuario_atual.id)


@router.patch(
    "/{tarefa_id}/concluir",
    response_model=TarefaResponse,
    status_code=status.HTTP_200_OK,
    summary="Marca uma tarefa como concluída",
)
def rota_concluir_tarefa(
    tarefa_id: int,
    session: Session = Depends(get_session),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    """Altera o status de uma tarefa específica para 'concluida'.

    Raises:
        HTTPException: 404 NOT FOUND se a tarefa não existir ou não pertencer ao usuário.
    """
    tarefa = crud.concluir_tarefa(session, tarefa_id, usuario_id=usuario_atual.id)
    if not tarefa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada ou não pertence a este usuário.",
        )
    return tarefa


@router.delete(
    "/{tarefa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove uma tarefa",
)
def deletar_tarefa(
    tarefa_id: int,
    session: Session = Depends(get_session),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    """Exclui permanentemente uma tarefa do banco de dados.

    Raises:
        HTTPException: 404 NOT FOUND se a tarefa não existir ou não pertencer ao usuário.
    """
    sucesso = crud.deletar_tarefa(session, tarefa_id, usuario_id=usuario_atual.id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada ou não pertence a este usuário.",
        )
    return None

