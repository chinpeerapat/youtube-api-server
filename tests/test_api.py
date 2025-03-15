"""
API endpoint tests
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "docs" in response.json()

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# Note: For actual YouTube API endpoints, consider using mocks to avoid
# making real API calls during tests
