from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Tarefa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(index=True)
    descricao: Optional[str] = None
    responsavel: str
    status: str = Field(default="pendente")
    data_criacao: datetime = Field(default_factory=datetime.now)
