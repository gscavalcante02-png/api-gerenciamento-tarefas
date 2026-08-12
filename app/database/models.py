"""Módulo de Modelos da Base de Dados (ORM/SQLModel).

Define a estrutura das tabelas 'Usuario' e 'Tarefa' no PostgreSQL,
estabelecendo seus campos, chaves primárias, chaves estrangeiras
e os relacionamentos entre os objetos.
"""

from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Usuario(SQLModel, table=True):
    """Modelo ORM que representa a tabela de usuários no banco de dados.

    Atributos:
        id: Identificador único do usuário (Chave Primária).
        nome: Nome completo do usuário.
        email: Endereço de e-mail único usado para login.
        senha_hash: Senha criptografada armazenada com algoritmo de hash.
        role: Nível de permissão do usuário ("user" ou "admin").
        tarefas: Lista de tarefas associadas a este usuário (Relacionamento 1:N).
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True, index=True)
    senha_hash: str
    role: str = Field(default="user")

    # Relacionamento: Um usuário pode ter múltiplas tarefas associadas
    tarefas: List["Tarefa"] = Relationship(back_populates="usuario")


class Tarefa(SQLModel, table=True):
    """Modelo ORM que representa a tabela de tarefas no banco de dados.

    Atributos:
        id: Identificador único da tarefa (Chave Primária).
        titulo: Título principal da tarefa.
        descricao: Detalhes adicionais opcionais sobre a tarefa.
        responsavel: Nome ou identificador da pessoa responsável.
        status: Estado atual da tarefa (padrão: "pendente").
        data_criacao: Data e hora do cadastro no sistema.
        usuario_id: Chave estrangeira referenciando o ID do usuário criador.
        usuario: Objeto do usuário proprietário da tarefa (Relacionamento N:1).
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(index=True)
    descricao: Optional[str] = None
    responsavel: str
    status: str = Field(default="pendente")
    data_criacao: datetime = Field(default_factory=datetime.now)

    # Chave estrangeira que vincula a tarefa ao ID do usuário que a criou
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")

    # Relacionamento que permite acessar o objeto Usuario diretamente pela Tarefa
    usuario: Optional[Usuario] = Relationship(back_populates="tarefas")