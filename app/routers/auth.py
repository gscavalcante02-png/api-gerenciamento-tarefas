"""Módulo de rotas para autenticação de usuários.

Gerencia o endpoint de login, validando credenciais de acesso e
emitindo tokens JWT de autorização no padrão OAuth2.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.security import criar_token_acesso, verificar_senha
from app.database import crud
from app.database.db import get_session

# Define o prefixo '/auth' e agrupa as rotas sob a tag 'Autenticação'
router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Realiza o login do usuário e gera o token JWT",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """Autentica o usuário com base no e-mail e na senha informados.

    - **username**: E-mail do usuário registrado (campo padrão do OAuth2).
    - **password**: Senha do usuário em texto puro.

    Returns:
        dict: Objeto contendo o token de acesso (access_token) e o tipo do token (bearer).

    Raises:
        HTTPException: 401 UNAUTHORIZED se o e-mail não existir ou a senha for incorreta.
    """
    # 1. Busca o usuário no banco de dados pelo e-mail enviado no campo 'username'
    usuario = crud.buscar_usuario_por_email(session, email=form_data.username)

    # 2. Valida se o usuário existe e se a senha confere com o hash salvo
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Gera o token de acesso JWT com o e-mail do usuário no atributo 'sub'
    token = criar_token_acesso(dados={"sub": usuario.email})

    # 4. Retorna a resposta no formato padrão do OAuth2
    return {
        "access_token": token,
        "token_type": "bearer",
    }