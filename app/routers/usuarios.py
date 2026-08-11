from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database.db import get_session
from app.database import crud
from app.database.models import Usuario

router = APIRouter()

@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(
    nome: str,
    email: str,
    senha: str, 
    session: Session = Depends(get_session)
):
    # 1. Verifica se o email já está cadastrado no banco
    usuario_existente = crud.buscar_usuario_por_email(session, email)
    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado no sistema."
        )

    # 2. Cria o novo usuário com a senha hash
    novo_usuario = crud.criar_usuario(session, nome, email, senha)
    return novo_usuario


@router.get("/{usuario_id}/tarefas")
def listar_tarefas_do_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    return crud.listar_tarefas_do_usuario(session, usuario_id)