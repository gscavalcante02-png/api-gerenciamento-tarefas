"""Módulo de operações CRUD (Create, Read, Update, Delete).

Contém as funções responsáveis por executar as consultas SQL e interagir
diretamente com o banco de dados PostgreSQL através do SQLAlchemy / SQLModel.
"""

from typing import List, Optional
from sqlmodel import Session, select

from app.core.security import gerar_hash_senha
from app.database.models import Tarefa, Usuario

from sqlalchemy import select
from sqlalchemy.orm import Session

# ==========================================
# 👤 OPERAÇÕES CRUD DE USUÁRIOS
# ==========================================

def criar_usuario(session: Session, nome: str, email: str, senha_limpa: str) -> Usuario:
    """Cria um novo usuário no banco de dados com a senha criptografada.

    Args:
        session: Sessão ativa do banco de dados.
        nome: Nome completo do usuário.
        email: Endereço de e-mail do usuário.
        senha_limpa: Senha fornecida em texto puro para ser convertida em hash.

    Returns:
        Usuario: Objeto do usuário recém-criado e persistido no banco.
    """
    senha_criptografada = gerar_hash_senha(senha_limpa)

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=senha_criptografada
    )

    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)
    return novo_usuario


def buscar_usuario_por_email(session: Session, email: str) -> Optional[Usuario]:
    """Busca um usuário no banco de dados através do seu e-mail.

    Útil para validação de login e verificação de duplicidade de e-mail no cadastro.

    Args:
        session: Sessão ativa do banco de dados.
        email: E-mail que se deseja pesquisar.

    Returns:
        Optional[Usuario]: Retorna a instância do Usuario se encontrado, ou None.
    """
    statement = select(Usuario).where(Usuario.email == email)
    return session.scalars(statement).first()


# ==========================================
# 📋 OPERAÇÕES CRUD DE TAREFAS
# ==========================================

def criar_tarefa(
    session: Session,
    titulo: str,
    responsavel: str,
    usuario_id: int,
    descricao: Optional[str] = None
) -> Tarefa:
    """Cadastra uma nova tarefa vinculada a um usuário específico.

    Args:
        session: Sessão ativa do banco de dados.
        titulo: Título da tarefa.
        responsavel: Nome do responsável pela execução.
        usuario_id: ID do usuário proprietário da tarefa.
        descricao: Detalhes opcionais sobre a tarefa.

    Returns:
        Tarefa: Objeto da tarefa persistido no banco de dados.
    """
    nova_tarefa = Tarefa(
        titulo=titulo,
        descricao=descricao,
        responsavel=responsavel,
        usuario_id=usuario_id
    )

    session.add(nova_tarefa)
    session.commit()
    session.refresh(nova_tarefa)
    return nova_tarefa


def listar_tarefas_do_usuario(session: Session, usuario_id: int) -> List[Tarefa]:
    """Retorna todas as tarefas registradas pertencentes a um determinado usuário.

    Args:
        session: Sessão ativa do banco de dados.
        usuario_id: ID do usuário autenticado.

    Returns:
        List[Tarefa]: Lista de tarefas encontradas.
    """
    statement = select(Tarefa).where(Tarefa.usuario_id == usuario_id)
    return list(session.scalars(statement).all())


def buscar_por_responsavel(session: Session, nome: str, usuario_id: int) -> List[Tarefa]:
    """Busca tarefas do usuário autenticado pelo nome parcial do responsável.

    Args:
        session: Sessão ativa do banco de dados.
        nome: Termo ou parte do nome a ser pesquisado.
        usuario_id: ID do usuário proprietário.

    Returns:
        List[Tarefa]: Lista de tarefas filtradas.
    """
    statement = select(Tarefa).where(
        Tarefa.usuario_id == usuario_id,
        Tarefa.responsavel.contains(nome)
    )
    return list(session.scalars(statement).all())


def concluir_tarefa(session: Session, tarefa_id: int, usuario_id: int) -> Optional[Tarefa]:
    """Atualiza o status de uma tarefa para 'concluida'.

    Garante que o usuário só consiga alterar suas próprias tarefas.

    Args:
        session: Sessão ativa do banco de dados.
        tarefa_id: ID da tarefa a ser concluída.
        usuario_id: ID do usuário autenticado.

    Returns:
        Optional[Tarefa]: Retorna a tarefa atualizada ou None se não encontrada.
    """
    statement = select(Tarefa).where(
        Tarefa.id == tarefa_id,
        Tarefa.usuario_id == usuario_id
    )
    tarefa = session.scalars(statement).first()

    if tarefa:
        tarefa.status = "concluida"
        session.add(tarefa)
        session.commit()
        session.refresh(tarefa)
        return tarefa

    return None


def deletar_tarefa(session: Session, tarefa_id: int, usuario_id: int) -> bool:
    """Remove permanentemente uma tarefa pertencente ao usuário informado.

    Args:
        session: Sessão ativa do banco de dados.
        tarefa_id: ID da tarefa a ser excluída.
        usuario_id: ID do usuário autenticado.

    Returns:
        bool: True se excluído com sucesso, False se a tarefa não for encontrada.
    """
    statement = select(Tarefa).where(
        Tarefa.id == tarefa_id,
        Tarefa.usuario_id == usuario_id
    )
    tarefa = session.scalars(statement).first()

    if tarefa:
        session.delete(tarefa)
        session.commit()
        return True

    return False