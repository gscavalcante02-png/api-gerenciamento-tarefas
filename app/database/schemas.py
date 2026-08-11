from pydantic import BaseModel

# O Schema (Classe) que define o que o front-end envia no corpo da requisição

class TarefaCreate(BaseModel):
    titulo: str
    responsavel: str
    descricao: str | None = None

class TarefaResponse(TarefaCreate):
    id: int
    concluida: bool
    usuario_id: int

    class Config:
        from_attributes = True