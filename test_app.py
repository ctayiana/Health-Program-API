import pytest
from api import app  

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_clients(client):
    response = client.get('/api/v1/clients')
    assert response.status_code == 200
    assert isinstance(response.json['data'], list)

def test_get_nonexistent_client(client):
    response = client.get('/api/v1/client/nonexistent-id')
    assert response.status_code == 404
    assert response.json['message'] == 'Client not found'

def test_get_health_programs(client):
    response = client.get('/api/v1/health-programs')  # Corrected URL here
    assert response.status_code == 200
    assert isinstance(response.json['data'], list)
