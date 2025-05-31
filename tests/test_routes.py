import pytest
import json
from app import create_app  # Importar a factory
from config import TestConfig  # Importar a configuração de teste
from flask.testing import FlaskClient
from flask.app import Flask

@pytest.fixture(scope='module')
def test_app() -> Flask:
    """Cria uma instância da aplicação Flask para testes."""
    app = create_app(TestConfig)
    return app

@pytest.fixture(scope='module')
def client(test_app: Flask) -> FlaskClient:
    """Fixture para o cliente de teste Flask."""
    with test_app.test_client() as client:
        yield client

@pytest.fixture(scope='function', autouse=True)
def clean_db(test_app: Flask):
    """Limpa o banco de dados de teste antes de cada teste."""
    with test_app.app_context():
        from app import mongo
        mongo.db.messages.delete_many({})
    yield

def test_health_check(client: FlaskClient):
    """Testa o endpoint /health."""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'active'
    assert json_data['message'] == 'HelpBot service is healthy.'

def test_create_message_success(client: FlaskClient):
    """Testa a criação de uma mensagem com sucesso."""
    payload = {"content": "Test message from pytest", "user_id": "pytest_user"}
    response = client.post('/api/v1/messages', json=payload)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['message'] == "Message created successfully."
    assert 'data' in json_data
    assert json_data['data']['content'] == payload['content']
    assert json_data['data']['user_id'] == payload['user_id']

def test_create_message_invalid_payload_empty_content(client: FlaskClient):
    """Testa a criação de mensagem com conteúdo vazio."""
    response = client.post('/api/v1/messages', json={"content": "", "user_id": "test_user"})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['success'] is False
    assert json_data['message'] == "Validation errors"
    assert 'errors' in json_data
    assert any(err['loc'] == ['content'] and 'ensure this value has at least 1 character' in err['msg'] for err in json_data['errors'])

def test_create_message_missing_content(client: FlaskClient):
    """Testa a criação de mensagem sem o campo 'content'."""
    response = client.post('/api/v1/messages', json={"user_id": "test_user"})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['success'] is False
    assert json_data['message'] == "Validation errors"
    assert any(err['loc'] == ['content'] and 'field required' in err['msg'] for err in json_data['errors'])

def test_list_messages_empty(client: FlaskClient):
    """Testa listar mensagens quando não há nenhuma."""
    response = client.get('/api/v1/messages')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['count'] == 0
    assert isinstance(json_data['data'], list)
    assert len(json_data['data']) == 0

def test_list_messages_with_data(client: FlaskClient):
    """Testa listar mensagens após criar algumas."""
    client.post('/api/v1/messages', json={"content": "Message 1", "user_id": "user1"})
    client.post('/api/v1/messages', json={"content": "Message 2", "user_id": "user2"})

    response = client.get('/api/v1/messages')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['count'] == 2
    assert len(json_data['data']) == 2
    assert json_data['data'][0]['content'] == "Message 2"  # Ordenado por timestamp desc

def test_get_specific_message_success(client: FlaskClient):
    """Testa buscar uma mensagem específica com sucesso."""
    create_response = client.post('/api/v1/messages', json={"content": "Specific message", "user_id": "specific_user"})
    message_id = create_response.get_json()['data']['_id']

    response = client.get(f'/api/v1/messages/{message_id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['data']['_id'] == message_id
    assert json_data['data']['content'] == "Specific message"

def test_get_specific_message_not_found(client: FlaskClient):
    """Testa buscar uma mensagem específica que não existe."""
    invalid_id = "60c72b2f9b1e8e001c8e4dba"
    response = client.get(f'/api/v1/messages/{invalid_id}')
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['success'] is False
    assert json_data['message'] == "Message not found."

def test_get_specific_message_invalid_id_format(client: FlaskClient):
    """Testa buscar uma mensagem com um ID em formato inválido."""
    response = client.get('/api/v1/messages/this-is-not-a-valid-objectid')
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['success'] is False
    assert json_data['message'] == "Invalid message ID format."
