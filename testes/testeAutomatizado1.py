import requests
import pytest

BASE_URL = "http://localhost:8000"

def test_login_success():
    """Testa o login com credenciais válidas."""
    # Assumindo que existe um usuário com email 'admin@admin.com' e senha 'admin'
    # no banco de dados servidor.db
    response = requests.post(f"{BASE_URL}/login?email=joao.silva@email.com&senha=$2b$12$LQv3c1yqBWVHxkd0LHAkKeYF5ZEhLpUZqXqXqXqXqXqXqXqXqXq")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["message"] == "Login realizado com sucesso"
    print(f"\nLogin Sucesso: {data}")

def test_login_failure_invalid_password():
    """Testa o login com senha inválida."""
    response = requests.post(f"{BASE_URL}/login?email=joao.silva@email.com&senha=senha_errada")
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Senha incorreta"
    print(f"\nLogin Falha (Senha Incorreta): {data}")

def test_get_estados():
    """Testa a listagem de estados."""
    response = requests.get(f"{BASE_URL}/estados")
    assert response.status_code == 200
    data = response.json()
    assert "estados" in data
    assert isinstance(data["estados"], list)
    assert len(data["estados"]) > 0
    print(f"\nListagem de Estados: {data}")

def test_get_nonexistent_user_info():
    """Testa a busca de informações de um usuário inexistente."""
    response = requests.post(f"{BASE_URL}/getContaInfo/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Usuário não encontrado"
    print(f"\nBuscar Usuário Inexistente: {data}")

if __name__ == "__main__":
    pytest.main([__file__])
