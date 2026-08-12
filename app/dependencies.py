"""Módulo de injeções de dependência da aplicação.

Contém as funções de validação de segurança e autenticação que são
executadas antes de processar as requisições das rotas protegidas.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session

from app.core.config import settings
from app.database import crud
from app.database.db import get_session
from app.database.models import Usuario

# Indica ao Swagger onde fica a rota de login para obter o token Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> Usuario:
    """Valida o Token JWT enviado no cabeçalho Authorization e retorna o usuário autenticado.

    Args:
        token: Token JWT extraído do cabeçalho da requisição.
        session: Sessão ativa do banco de dados.

    Returns:
        Usuario: Objeto do usuário autenticado retornado do banco.

    Raises:
        HTTPException: 401 Unauthorized se o token for inválido, expirado ou o usuário não existir.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de acesso inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o token utilizando a chave secreta e o algoritmo configurados
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Busca o usuário associado ao e-mail extraído do token
    usuario = crud.buscar_usuario_por_email(session, email=email)
    if usuario is None:
        raise credentials_exception

    return usuario