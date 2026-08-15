def test_cadastrar_usuario(client):
    """Garante que cadastrar um usuário novo funciona e nunca expões a senha."""

    response = client.post("/usuarios/", json={          # simula um POST real, sem precisar do servidor ligado
        "nome": "Guilherme Teste",
        "email": "teste@exemplo.com",
        "senha": "senha123"
    })

    assert response.status_code == 201                  # confere se a API respondeu "criado com sucesso"
    assert response.json()["email"] == "teste@exemplo.com"  # confere se o e-mail certo na resposta
    assert "senha" not in response.json()               # confirma que aa senha nunca aparece na resposta


def test_nao_permite_email_duplicado(client):
    """Garante que cadastrar duas vezes o mesmo e-mail é bloqueado pela API."""

    dados = {"nome": "A", "email": "duplicado@exemplo.com", "senha": "123"}

    client.post("/usuarios/", json=dados)                   # primeiro cadastro - esse deve funcionar normalmente
    resposta_duplicada = client.post("/usuarios/", json=dados)  # segunda vez, mesmo e-mail de novo

    assert resposta_duplicada.status_code == 400            # confere se a API recusou a segunda tentativa