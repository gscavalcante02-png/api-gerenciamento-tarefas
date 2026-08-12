"""Módulo de utilitários de segurança e criptografia.

Contém funções para hashing de senhas com bcrypt e operações
de geração e validação de tokens JWT.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Configura o algoritmo Bcrypt para criptografia de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def gerar_hash_senha(senha: str) -> str:
    """Recebe a senha em texto limpo e retorna o hash criptografado."""
    return pwd_context.hash(senha)


def verificar_senha(senha_limpa: str, hash_salvo: str) -> bool:
    """Compara a senha digitada pelo usuário com o hash salvo no banco."""
    return pwd_context.verify(senha_limpa, hash_salvo)


def criar_token_acesso(dados: dict, tempo_expiracao: Optional[timedelta] = None) -> str:
    """Gera um novo token JWT assinado."""
    payload = dados.copy()

    if tempo_expiracao:
        expira = datetime.now(timezone.utc) + tempo_expiracao
    else:
        expira = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload.update({"exp": expira})

    token_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token_jwt


def decodificar_token_acesso(token: str) -> dict:
    """Decodifica e valida a assinatura e expiração do token JWT."""
    excecao_autenticacao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        identificacao_usuario: str = payload.get("sub")
        if identificacao_usuario is None:
            raise excecao_autenticacao

        return payload

    except JWTError:
        raise excecao_autenticacao