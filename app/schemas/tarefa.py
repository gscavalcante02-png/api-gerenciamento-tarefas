"""Módulo de Schemas Pydantic para Tarefas.

Define a validação de dados de entrada (requisições HTTP) e
saída (respostas JSON) para as operações relacionadas às Tarefas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TarefaBase(BaseModel):
    """Schema base com atributos comuns de uma tarefa."""

    titulo: str
    responsavel: str
    descricao: Optional[str] = None


class TarefaCreate(TarefaBase):
    """Schema para o corpo da requisição ao criar uma nova tarefa.

    Herda os campos de TarefaBase (titulo, responsavel, descricao).
    """

    pass


class TarefaUpdate(BaseModel):
    """Schema para o corpo da requisição ao atualizar uma tarefa.

    Todos os campos são opcionais para permitir atualizações parciais.
    """

    titulo: Optional[str] = None
    responsavel: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[str] = None


class TarefaResponse(TarefaBase):
    """Schema para a resposta JSON retornada pela API ao consultar tarefas.

    Inclui os campos gerados pelo banco de dados (id, status, data e usuario_id).
    """

    id: int
    status: str
    data_criacao: datetime
    usuario_id: int

    # Configuração para conversão automática de objetos ORM / SQLModel em dicionários Pydantic
    model_config = ConfigDict(from_attributes=True)