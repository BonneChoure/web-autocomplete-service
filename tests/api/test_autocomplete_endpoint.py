import pytest
from fastapi.testclient import TestClient

from web_autocomplete_service.config import get_settings
from web_autocomplete_service.main import app

settings=get_settings()

def test_usual_query(client):
    response = client.get("/autocomplete", params={"query":"crypt"})
    assert response.status_code == 200
    assert response.json() == ["cryptanalysis", "cryptographers", "cryptographic algorithm", "cryptography"]

def test_no_match_returns_empty_json_array(client):
    response = client.get("/autocomplete", params={"query":"bakery"})
    assert response.status_code == 200
    assert response.json() == []

def test_missing_query_returns_422(client):
    response = client.get("/autocomplete")
    assert response.status_code == 422

def test_empty_query_returns_422(client):
    response = client.get("/autocomplete", params={"query":""})
    assert response.status_code == 422

def test_too_long_query_returns_422(client):
    response = client.get("/autocomplete", params={"query": "a" * (settings.max_query_length + 1)})
    assert response.status_code == 422

@pytest.mark.parametrize("prefix", ["😄", "有效", "<", "!", "\x00", "\u00a3"])
def test_special_characters_does_not_return_500(client, prefix):
    assert client.get("/autocomplete", params={"query": prefix}).status_code in (200, 422)

def test_unexpected_error_returns_generic_500(monkeypatch):
    def raise_exception(*args, **kwargs):
        raise Exception("Test Exception")
    
    monkeypatch.setattr("web_autocomplete_service.routers.autocomplete.get_autocomplete_terms", raise_exception)

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/autocomplete", params={"query": "crypt"})

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}