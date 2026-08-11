from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.database.db import get_session
from app.database import crud
from app.core.security import verificar_senha 
from app.core.jwt import criar_token_acesso


router = APIRouter()

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    Busca o usuário no banco de e-mail
    Nota: O OAuth2PasswordRequestForm guarda o e-mail/login dentro do campo '.username'
    """
    usuario = crud.buscar_usuario_por_email(session, email=form_data.username)

    # Se o usuário não existir OU a senha estiver incorreta: 
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail ou senha incorretos."
        )

    # Se deu tudo certo, criamos o Token com o e-mail no campo 'sub'
    token = criar_token_acesso(dados={"sub": usuario.email})

    # Retornamos o token no padrão que o OAuth2 exige
    return {
        "access_token": token,
        "token_type": "bearer"
    }