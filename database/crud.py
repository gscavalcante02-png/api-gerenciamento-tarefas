from sqlmodel import Session, select
from database.models import Tarefa

def criar_tarefa(session: Session, tarefa: Tarefa) -> Tarefa:
    session.add(tarefa)
    session.commit()
    session.refresh(tarefa)
    return tarefa

def listar_tarefa(session: Session):
    comando = select(Tarefa)            # Prepara o "SELECT * FROM tarefa"
    resultados = session.exec(comando)  # Executa a busca
    return resultados.all()             # Retorna a lista de tarefas    

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