from fastapi.testclient import TestClient

from api.autofill import app, detect_provider

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_supported_provider_and_subdomain():
    assert detect_provider("https://example.qualtrics.com/survey") == "Qualtrics"
    assert detect_provider("https://surveyjunkie.com/") == "Survey Junkie"


def test_domain_suffix_spoof_does_not_match():
    assert detect_provider("https://qualtrics.com.attacker.example/") is None


def test_unknown_provider_is_reported_without_error():
    response = client.post("/api/detect", json={"url": "https://example.org/survey"})
    assert response.status_code == 200
    assert response.json()["provider"] == "Unknown"


def test_invalid_scheme_is_rejected():
    response = client.post("/api/detect", json={"url": "javascript:alert(1)"})
    assert response.status_code == 422


def test_localhost_is_rejected():
    response = client.post("/api/detect", json={"url": "http://localhost/survey"})
    assert response.status_code == 422


def test_suggestions_are_explicitly_disabled():
    response = client.post("/api/suggest")
    assert response.status_code == 501
