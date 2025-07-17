import pytest
from fastapi.testclient import TestClient
from app import app
import os
import tempfile
import json

client = TestClient(app)

class TestHealthCheck:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data

class TestChatAPI:
    def test_chat_endpoint(self):
        payload = {
            "message": "Find jewelry offers in Kolhapur",
            "language": "en"
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "language" in data
        assert data["language"] == "en"

    def test_chat_invalid_language(self):
        payload = {
            "message": "Test message",
            "language": "invalid"
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200  # Should still work with fallback

    def test_chat_empty_message(self):
        payload = {
            "message": "",
            "language": "en"
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 400

class TestOffersAPI:
    def test_get_offers(self):
        response = client.get("/api/offers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_offers_with_city_filter(self):
        response = client.get("/api/offers?city=kolhapur")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_offers_with_category_filter(self):
        response = client.get("/api/offers?category=jewelry")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_offers_with_limit(self):
        response = client.get("/api/offers?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5

    def test_add_offer(self):
        payload = {
            "store_name": "Test Store",
            "city": "Test City",
            "category": "jewelry",
            "offer_text": "Test offer",
            "price_range": "₹1000 - ₹10000",
            "valid_till": "2025-12-31",
            "source": "test"
        }
        response = client.post("/api/offers", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["store_name"] == "Test Store"
        assert data["city"] == "Test City"

class TestCitiesAPI:
    def test_get_cities(self):
        response = client.get("/api/cities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

class TestCategoriesAPI:
    def test_get_categories(self):
        response = client.get("/api/categories")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

class TestOCRAPI:
    def test_ocr_without_file(self):
        response = client.post("/ocr")
        assert response.status_code == 422

    def test_ocr_with_invalid_file(self):
        with tempfile.NamedTemporaryFile(suffix=".txt") as f:
            f.write(b"test content")
            f.flush()
            response = client.post(
                "/ocr",
                files={"file": ("test.txt", f, "text/plain")},
                data={"language": "en"}
            )
            assert response.status_code == 200

class TestVoiceAPI:
    def test_transcribe_without_file(self):
        response = client.post("/voice/transcribe")
        assert response.status_code == 422

    def test_synthesize(self):
        payload = {
            "message": "Test message for synthesis",
            "language": "en"
        }
        response = client.post("/voice/synthesize", json=payload)
        assert response.status_code == 200
        assert response.headers["content-type"] == "audio/wav"

class TestTwilioWebhook:
    def test_twilio_webhook_greeting(self):
        form_data = {
            "From": "+1234567890",
            "Body": "hi"
        }
        response = client.post("/webhook/twilio", data=form_data)
        assert response.status_code == 200
        assert "application/xml" in response.headers["content-type"]

    def test_twilio_webhook_offers_query(self):
        form_data = {
            "From": "+1234567890",
            "Body": "gold offers in Kolhapur"
        }
        response = client.post("/webhook/twilio", data=form_data)
        assert response.status_code == 200
        assert "application/xml" in response.headers["content-type"]

class TestErrorHandling:
    def test_404_endpoint(self):
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_invalid_json(self):
        response = client.post("/api/chat", data="invalid json")
        assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__]) 