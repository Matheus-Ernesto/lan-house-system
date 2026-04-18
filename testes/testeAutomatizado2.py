import requests

# URL base da sua API
BASE_URL = "http://localhost:8000"

def test_get_estados_success( ):
    print("\nExecutando Teste Python: Listar Estados (Sucesso)")
    response = requests.get(f"{BASE_URL}/estados")
    
    # Verifica se o status code é 200
    assert response.status_code == 200, f"Esperado Status 200, mas recebeu {response.status_code}"
    
    # Verifica se a resposta contém a chave 'estados' e se é uma lista não vazia
    data = response.json()
    assert "estados" in data, "Resposta JSON não contém a chave 'estados'"
    assert isinstance(data["estados"], list), "'estados' não é uma lista"
    assert len(data["estados"]) > 0, "A lista de estados está vazia"
    
    print("Teste Python: Listar Estados (Sucesso) - PASSOU")
    print(f"Resposta: {data}")

# Para executar este teste, você pode chamar a função diretamente:
if __name__ == "__main__":
    test_get_estados_success()
import requests

# URL base da sua API
BASE_URL = "http://localhost:8000"

def test_login_invalid_password_failure( ):
    print("\nExecutando Teste Python: Login com Senha Incorreta (Falha Esperada)")
    # Assumindo que 'admin@admin.com' é um email válido, mas 'senha_errada' é inválida
    response = requests.post(f"{BASE_URL}/login?email=joao.silva@email.com&senha=senha_errada")
    
    # Verifica se o status code é 401
    assert response.status_code == 401, f"Esperado Status 401, mas recebeu {response.status_code}"
    
    # Verifica se a mensagem de erro é a esperada
    data = response.json()
    assert "detail" in data, "Resposta JSON não contém a chave 'detail'"
    assert data["detail"] == "Senha incorreta", f"Mensagem de erro inesperada: {data['detail']}"
    
    print("Teste Python: Login com Senha Incorreta (Falha Esperada) - PASSOU")
    print(f"Resposta: {data}")

# Para executar este teste, você pode chamar a função diretamente:
if __name__ == "__main__":
    test_login_invalid_password_failure()