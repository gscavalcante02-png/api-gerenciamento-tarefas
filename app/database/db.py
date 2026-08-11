import os 
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from app.database.models import Tarefa, Usuario

# 1. Carrega as váriaveis de ambiente .env
load_dotenv()

# 2. Pega a URL de conexão de arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Cria o motor (engine) de conexão com PostgreSQL 
# echo=True faz o SQLModel mostrar no terminal os comandos SQL que está rodando 
engine = create_engine(DATABASE_URL, echo=True)

# 4. Função que cria as tabelas no banco se elas não existirem 
def inicializar_banco():
    # ⚠️ Apaga as tabelas antigas para recriar com as colunas novas
    SQLModel.metadata.create_all(engine)


# 5. Função que abre uma "sessão" para fazermos operações no banco
def get_session():
    with Session(engine) as session:
        yield session



# Bloco de teste temporário
if __name__ == "__main__":
    print("Tentando conectar ao banco...")
    inicializar_banco()
    print("✅ Conexão realizada com sucesso!")