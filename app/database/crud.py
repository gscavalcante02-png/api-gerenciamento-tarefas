from sqlmodel import Session, select
from app.database.models import Tarefa, Usuario
from app.core.security import gerar_hash_senha

# ==========================================
#   CRUD DE USUÁRIOS
# ==========================================

def criar_usuario(session: Session, nome: str, email: str, senha_limpa: str) -> Usuario:
    # 1. Transforma a senha em texto limpo num hash seguro
    senha_criptografada = gerar_hash_senha(senha_limpa)

    # 2. Cria o objeto do Usuário com a senha já protegida
    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=senha_criptografada
    )

    # 3. Salva no PostgreSQL
    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)
    return novo_usuario

def buscar_usuario_por_email(session: Session, email: str) -> Usuario | None:
    """Útil para a hora do Login ou para verificar se o email já existe antes de cadastrar."""
    statement = select(Usuario).where(Usuario.email == email)
    return session.exec(statement).first()


# ==========================================
#  CRUD DE TAREFAS (Atualizado com usuário)
# ==========================================


def criar_tarefa(
        session: Session,
        titulo: str,
        responsavel: str,
        usuario_id: int,    # Agora precisamos saber QUEM é o dono
        descricao: str = None
    )  -> Tarefa:

        nova_tarefa = Tarefa(
            titulo=titulo,
            descricao=descricao,
            responsavel=responsavel,
            usuario_id=usuario_id   # Amarra a tarefa a usuário correspondente
        )

        session.add(nova_tarefa)
        session.commit()
        session.refresh(nova_tarefa)
        return nova_tarefa


def listar_tarefas_do_usuario(session: Session, usuario_id: int):
    statement = select(Tarefa).where(Tarefa.usuario_id == usuario_id)
    resultados = session.exec(statement).all()
    return resultados
    
   
def buscar_por_responsavel(session: Session, nome: str):
    # O .contains(nome) busca nomes parecidos (ex: "Ana" acha "Ana Maria")
    comando = select(Tarefa).where(Tarefa.responsavel.contains(nome))
    resultados = session.exec(comando)
    return resultados.all()

def deletar_tarefa(session: Session, tarefa_id: int):
    tarefa = session.get(Tarefa, tarefa_id) #Busca pelo ID
    if tarefa: 
        session.delete(tarefa)              # Marca para apagar       
        session.commit()                    # Salva a alteração
        return True
    return False

def concluir_tarefa(session: Session, tarefa_id: int):
    tarefa = session.get(Tarefa, tarefa_id)
    if tarefa: 
        tarefa.status = "concluida" # Altera o atributo no Python
        session.add(tarefa)         # Prepara para atualizar
        session.commit()            # Aplica a mudança no Postgres
        session.refresh(tarefa)     # Pega o objeto atualizado
        return tarefa
    return None