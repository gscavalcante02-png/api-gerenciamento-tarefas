from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM 
from app.database.db import get_session
from app.database import crud

# Configura o algoritmo Bcrypt como pardão para criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def gerar_hash_senha(senha: str) -> str:
    """Receba a senha em texto limpo e retorna o hash indecifrável."""
    return pwd_context.hash(senha)

def verificar_senha(senha_limpa: str, hash_salvo: str) -> bool:
    """Compara a senha digitada pelo usuário com o hash que está salvo no banco.
    Retorna True se forem correspondendtes e False caso contrário.
    """ 
    return pwd_context.verify(senha_limpa, hash_salvo)

# Informa ao FastAPI em qual rota o cliente busca o token se não estiver autenticado
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session) 
):
    exception_unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try: 
        # Decodifica o token usando a mesma CHAVE_SECRETA e ALGORITMO
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extrai o e-mail (ou ID) do utilizador armazenado no campo "sub"
        email: str = payload.get("sub")
        if email is None:
            raise exception_unauthorized

    except JWTError:
        raise exception_unauthorized

    usuario = crud.buscar_usuario_por_email(session, email=email)

    if usuario is None:
        raise exception_unauthorized

    return usuario    # Por agora, devolvemos o e-mail extráido do token