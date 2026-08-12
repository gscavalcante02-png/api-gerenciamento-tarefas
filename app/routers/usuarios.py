"""Módulo de rotas para gerenciamento de usuários.

Contém os endpoints para cadastro de novos usuários e consulta
de tarefas atreladas ao usuário autenticado.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import crud
from app.database.db import get_session
from app.dependencies import obter_usuario_atual
from app.database.models import Usuario
from app.schemas.tarefa import TarefaResponse
from app.schemas.usuario import UsuarioCreate, UsuarioResponse

# Define o prefixo '/usuarios' e a tag para agrupar no Swagger UI
router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo usuário",
)
def cadastrar_usuario(
    usuario_data: UsuarioCreate,
    session: Session = Depends(get_session),
):
    """Cadastra um novo usuário no sistema.

    - **nome**: Nome completo do usuário.
    - **email**: Endereço de e-mail único.
    - **senha**: Senha em texto puro (será salva como hash criptografado).

    Raises:
        HTTPException: 400 BAD REQUEST se o e-mail já estiver cadastrado.
    """
    # 1. Verifica se o e-mail já está cadastrado no banco de dados
    usuario_existente = crud.buscar_usuario_por_email(session, usuario_data.email)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado no sistema.",
        )

    # 2. Cria o novo usuário gerando o hash de senha
    novo_usuario = crud.criar_usuario(
        session=session,
        nome=usuario_data.nome,
        email=usuario_data.email,
        senha_limpa=usuario_data.senha,
    )

    return novo_usuario


@router.get(
    "/me/tarefas",
    response_model=List[TarefaResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista as tarefas do usuário autenticado",
)
def listar_minhas_tarefas(
    session: Session = Depends(get_session),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    """Retorna a lista completa de tarefas pertencentes ao usuário logado na sessão."""
    return crud.listar_tarefas_do_usuario(session, usuario_id=usuario_atual.id)