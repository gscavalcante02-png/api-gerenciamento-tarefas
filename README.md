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

## 🚀 Como Rodar o Projeto

### Pré-requisitos

- Python 3.12+
- PostgreSQL instalado e rodando

### Passo a passo

1. Clone o repositório:

```bash
git clone https://github.com/gscavalcante02-png/api-gerenciamento-tarefas.git
cd api-gerenciamento-tarefas
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:

```bash
cp .env.example .env
```

Depois, edite o `.env` com suas credenciais do PostgreSQL e uma `SECRET_KEY` própria.

4. Inicie o servidor:

```bash
uvicorn main:app --reload
```

5. Acesse a documentação interativa em: `http://localhost:8000/docs`

## 📋 Exemplo de Uso

### 1. Cadastrar um usuário

`POST /usuarios/`

```json
{
  "nome": "Seu Nome",
  "email": "seu.email@exemplo.com",
  "senha": "suaSenhaSegura"
}
```

### 2. Fazer login

`POST /auth/login` (formulário, campos `username` e `password`)

- `username`: seu e-mail
- `password`: sua senha

Retorna:

```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

### 3. Criar uma tarefa (autenticado)

`POST /tarefas/` — envie o token no header `Authorization: Bearer <token>`

```json
{
  "titulo": "Estudar SQLModel",
  "responsavel": "Seu Nome",
  "descricao": "Revisar relacionamentos N:N"
}
```

## 📖 Documentação

A documentação completa e interativa (Swagger UI) fica disponível automaticamente em `/docs` assim que o servidor estiver rodando.

## 👤 Autor

Desenvolvido por **Guilherme** como projeto de estudo prático em Python back-end.
