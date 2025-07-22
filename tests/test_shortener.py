import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_shorten_url(client):
    res = client.post("/api/shorten", json={"url": "https://www.example.com"})
    assert res.status_code == 201
    data = res.get_json()
    assert "short_code" in data and len(data["short_code"]) == 6
    assert data["short_url"].endswith(data["short_code"])

def test_shorten_invalid_url(client):
    res = client.post("/api/shorten", json={"url": "not a url"})
    assert res.status_code == 400

def test_redirect_existing(client):
    res = client.post("/api/shorten", json={"url": "https://redirect.com"})
    short_code = res.get_json()["short_code"]
    redirect_res = client.get(f"/{short_code}")
    assert redirect_res.status_code == 302
    assert redirect_res.headers['Location'] == "https://redirect.com"

def test_redirect_nonexistent(client):
    res = client.get("/xyz123")
    assert res.status_code == 404

def test_stats(client):
    res = client.post("/api/shorten", json={"url": "https://stats.com"})
    short_code = res.get_json()["short_code"]
    client.get(f"/{short_code}")
    stats_res = client.get(f"/api/stats/{short_code}")
    data = stats_res.get_json()
    assert data["url"] == "https://stats.com"
    assert data["clicks"] >= 1
    assert "created_at" in data
