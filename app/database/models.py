from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class Tarefa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(index=True)
    descricao: Optional[str] = None
    responsavel: str
    status: str = Field(default="pendente")
    data_criacao: datetime = Field(default_factory=datetime.now)

    # A chave estrangeira: Guarda o ID de quem criou a tarefa 
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")

    # Relacionamento no Python para acessar o objeto do usuário direto
    usuario: Optional[Usuario] = Relationship(back_populates="tarefas")



class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True, index=True) # Email não pode repetir
    senha_hash: str                             # Guarda a senha criptograda
    role: str = Field(default="user")           # "user" ou "admin"

    # Relacionamento: Um usuário pode ter várias tarefas
    tarefas: List["Tarefa"] = Relationship(back_populates="usuario")
