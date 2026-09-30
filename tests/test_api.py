
import sys
import os

# Permette di importare l'applicazione
# dalla cartella app
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app.app import app


def test_home():

    app.testing = True

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["service"] == "Sentiment Analysis API"

    assert data["status"] == "running"


def test_predict_positive():

    app.testing = True

    client = app.test_client()

    response = client.post(
        "/predict",
        json={
            "review": "This product is amazing! I love it."
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "sentiment" in data

    assert "confidence" in data

    assert data["sentiment"] == "positive"

    assert 0 <= data["confidence"] <= 1


def test_predict_negative():

    app.testing = True

    client = app.test_client()

    response = client.post(
        "/predict",
        json={
            "review": "This product is terrible. I hate it."
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["sentiment"] == "negative"

    assert 0 <= data["confidence"] <= 1


def test_predict_neutral():

    app.testing = True

    client = app.test_client()

    response = client.post(
        "/predict",
        json={
            "review": "The product is okay, nothing special."
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["sentiment"] == "neutral"

    assert 0 <= data["confidence"] <= 1


def test_predict_without_review():

    app.testing = True

    client = app.test_client()

    response = client.post(
        "/predict",
        json={}
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data


def test_predict_invalid_review():

    app.testing = True

    client = app.test_client()

    response = client.post(
        "/predict",
        json={
            "review": 12345
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data



def test_metrics():

    app.testing = True

    client = app.test_client()

    response = client.get("/metrics")

    assert response.status_code == 200

    assert (
        "prediction_requests_total"
        in response.text
    )

    assert (
        "prediction_errors_total"
        in response.text
    )

    assert (
        "prediction_response_time_seconds"
        in response.text
    )

    assert (
        "system_cpu_usage_percent"
        in response.text
    )

    assert (
        "system_memory_usage_percent"
        in response.text
    )
