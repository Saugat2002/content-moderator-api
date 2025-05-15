import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings


settings = get_settings()

client = TestClient(app)
API_KEY = settings.API_KEY


def test_root_endpoint():
    """Test the root endpoint returns the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Content Moderator" in response.text


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_analyze_endpoint_no_api_key():
    """Test analyze endpoint without API key"""
    response = client.post("/api/v1/analyze", json={"text": "This is a test"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"


def test_analyze_endpoint_invalid_api_key():
    """Test analyze endpoint with invalid API key"""
    response = client.post(
        "/api/v1/analyze",
        json={"text": "This is a test"},
        headers={"X-API-Key": "invalid_key"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


def test_analyze_endpoint_empty_text():
    """Test analyze endpoint with empty text"""
    response = client.post(
        "/api/v1/analyze", json={"text": ""}, headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    assert "sentiment_score" in response.json()
    assert "sentiment" in response.json()


def test_analyze_endpoint_valid_request():
    """Test analyze endpoint with valid request"""
    response = client.post(
        "/api/v1/analyze",
        json={"text": "I love this product!"},
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 200
    result = response.json()
    assert "sentiment_score" in result
    assert "sentiment" in result
    assert "confidence" in result
    assert "dominant_emotion" in result
    assert "raw_scores" in result
