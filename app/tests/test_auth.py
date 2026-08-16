def test_login_com_senha_errada(client):
    """Garante que login com senha errada é recusado."""

    client.post("/usuarios/",json={
        "nome": "Guilherme Teste",
        "email": "login2.teste@exemplo.com",
        "senha": "senhaCerta"
    })

    response = client.post("/auth/login", data={
        "username": "login2.teste@exemplo.com",
        "password": "senhaErrada"
    })

    assert response.status_code == 401