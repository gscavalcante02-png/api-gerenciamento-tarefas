"""Módulo de Schemas Pydantic para Usuários."""

from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioCreate(BaseModel):
    """Schema para o corpo da requisição ao cadastrar um novo usuário."""

    nome: str
    email: EmailStr
    senha: str


class UsuarioResponse(BaseModel):
    """Schema para o retorno do usuário (sem expor a senha!)."""

    id: int
    nome: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)