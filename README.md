# 🚀 API de Gerenciamento de Tarefas

API RESTful completa para gerenciamento de tarefas pessoais com autenticação de usuários, construída com **FastAPI**, **SQLAlchemy / SQLModel**, **PostgreSQL** e segurança baseada em **Tokens JWT**.

---

## 📌 Funcionalidades

- 🔒 **Autenticação e Segurança:**
  - Cadastro de novos usuários com senha criptografada (_Bcrypt_).
  - Autenticação via login gerando token **JWT (JSON Web Token)**.
  - Rotas protegidas (cada usuário só pode visualizar, editar e deletar as suas próprias tarefas).

- 📝 **Gerenciamento de Tarefas (CRUD):**
  - Criar tarefas associadas ao usuário logado.
  - Listar apenas as tarefas pertencentes ao usuário autenticado.
  - Marcar tarefas como concluídas (`PATCH`).
  - Remover tarefas (`DELETE`).

- 📖 **Documentação Interativa:**
  - Documentação Swagger UI gerada automaticamente pelo FastAPI.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.12+
- **Framework Web:** FastAPI
- **Servidor ASGI:** Uvicorn
- **ORM / Banco de Dados:** SQLModel / SQLAlchemy & PostgreSQL
- **Validação de Dados:** Pydantic (com `email-validator`)
- **Segurança:** Passlib (Bcrypt) & PyJWT

---

## 📁 Estrutura do Projeto

```text
projeto_tarefas/
│
├── app/
│   ├── core/           # Configurações de segurança e hash de senha
│   ├── database/       # Conexão com banco de dados e funções CRUD
│   ├── routers/        # Endpoints (auth, usuarios, tarefas)
│   ├── schemas/        # Schemas de validação do Pydantic
│   ├── dependencies.py # Injeção de dependências (Autenticação JWT)
│   └── main.py         # Arquivo principal de inicialização da API
│
├── .env                # Variáveis de ambiente (não versionado)
├── .gitignore          # Arquivos ignorados pelo Git
└── requirements.txt    # Dependências do projeto
```
