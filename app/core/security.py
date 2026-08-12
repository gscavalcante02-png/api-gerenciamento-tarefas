"""Módulo de utilitários de segurança e criptografia.

Contém funções para hashing de senhas com bcrypt e operações
de geração.
"""

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
