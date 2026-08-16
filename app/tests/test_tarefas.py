def test_criar_tarefa(client, token_usuario):
    """Garante que um usuário autenticado consegue criar uma tarefa."""

    response = client.post(
        "/tarefas",
        json={"titulo": "Estudar pytest", "responsavel": "Guilherme", "descricao": "Praticar fixtures"},
        headers={"Authorization": f"Bearer {token_usuario}"}
    )

    assert response.status_code == 201
    assert response.json()["titulo"] == "Estudar pytest"

def test_concluir_tarefa(client, token_usuario):
    """Garante que o dono de uma tarefa consegue concluí-la."""

    resposta_criar = client.post(
        "/tarefas/",
        json={"titulo": "Tarefa a concluir", "responsavel": "A", "descricao": "..."},
        headers={"Authorization": f"Bearer {token_usuario}"}
    )
    id_tarefa = resposta_criar.json()["id"]

    response = client.patch(
        f"/tarefas/{id_tarefa}/concluir",
        headers={"Authorization": f"Bearer {token_usuario}"}
    )

    assert response.status_code == 200

def test_usuario_nao_conclui_tarefa_de_outro(client, token_usuario, token_outro_usuario):
    """Garante que um usuário não consegue concluir a tarefa de outro."""

    resposta_criar = client.post(
        "/tarefas/",
        json={"titulo": "Tarefa do A", "responsavel": "A", "descricao": "..."},
        headers={"Authorization": f"Bearer {token_usuario}"}
    )
    id_tarefa = resposta_criar.json()["id"]

    response = client.patch(
        f"tarefas/{id_tarefa}/concluir",
        headers={"Authorization": f"Bearer {token_outro_usuario}"}
    )

    assert response.status_code == 404


def test_usuario_nao_ve_tarefa_de_outro(client, token_usuario, token_outro_usuario):
    """Garante que a listagem de tarefas de um usuário nunca inclui tarefas de outro."""

    # Usuário A cria uma tarefa
    resposta_criar_a = client.post(
        "/tarefas/",
        json={"titulo": "Tarefa do A", "responsavel": "A", "descricao": "..."},
        headers={"Authorization": f"Bearer {token_usuario}"}
    )
    id_tarefa_a = resposta_criar_a.json()["id"]

    # Usuário B cria uma tarefa diferente
    resposta_criar_b = client.post(
        "/tarefas/",
        json={"titulo": "Tarefa do B", "responsavel": "B", "descricao": "..."},
        headers={"Authorization": f"Bearer {token_outro_usuario}"}
    )
    id_tarefa_b = resposta_criar_b.json()["id"]
    # Usuário A pede a própria lista
    response = client.get(
        "/tarefas/",
        headers={"Authorization": f"Bearer {token_usuario}"}
    )

    ids = [tarefa["id"] for tarefa in response.json()]

    assert id_tarefa_a in ids
    assert id_tarefa_b not in ids

def test_deletar_tarefa(client, token_usuario):
    """Garante que um dono consiga apagar uma tarefa """

    resposta_criar = client.post(
        "/tarefas/",
        json={"titulo": "Tarefa a concluir", "responsavel": "A", "descricao": "..."},
        headers={"Authorization": f"Bearer {token_usuario}"}
    )
    id_tarefa = resposta_criar.json()["id"]

    response = client.delete(
        f"/tarefas/{id_tarefa}",
        headers={"Authorization": f"Bearer {token_usuario}"}
    )

    assert response.status_code == 204

def test_usuario_nao_deleta_tarefa_de_outro(client, token_usuario, token_outro_usuario):
    """Garante que um usuário não consegue deletar a tarefa de outro."""

    resposta_criar = client.post(
        "/tarefas/",
        json={"titulo": "Tarefa do A", "responsavel": "A", "descricao": "..."},
        headers={"Authorization": f"Bearer {token_usuario}"}
    )
    id_tarefa = resposta_criar.json()["id"]

    response = client.delete(
        f"/tarefas/{id_tarefa}",
        headers={"Authorization": f"Bearer {token_outro_usuario}"}
    )

    assert response.status_code == 404