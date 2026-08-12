from datetime import datetime, timedelta, timezone
from jose import jwt,JWTError
from fastapi import HTTPException, status
from app.core.config import settings



def criar_token_acesso(dados: dict) -> str:
    # Fazemos uma cópia do dicionário recebido para não alterar o original
    dados_para_codificar = dados.copy()

    # Calculamos o momento exato em que token vai expirar
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Adicionamos a data de expiração no campo reservado 'exp' do JWT   
    dados_para_codificar.update({"exp": expiracao})

    # Assinamos e geramos a string do token JWT
    token_jwt = jwt.encode(dados_para_codificar, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token_jwt

def decodificar_token_acesso(token: str) -> dict:
    # Definimos a mensagem de erro padrão caso qualquer validação falhe
    excecao_autenticacao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Abre o token e verifica se a assinatura e o tempo de expiração estão válidos
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )

        # Pega a identificação do dono do token (o e-mail ou ID que guardamos no login)
        identificacao_usuario: str = payload.get("sub")

        if identificacao_usuario is None:
            raise excecao_autenticacao

        return payload

    except JWTError:
        raise excecao_autenticacao