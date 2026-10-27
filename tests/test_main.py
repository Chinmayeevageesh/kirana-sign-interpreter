from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Dummy landmarks for testing only.
# These are NOT real hand landmarks.
DUMMY_LANDMARKS = [
    [0.1, 0.2, 0.0] for _ in range(21)
]


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Kirana Sign Interpreter API is running"
    )


def test_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recognize_rice():
    response = client.post(
        "/api/recognize",
        json={
            "landmarks": DUMMY_LANDMARKS,
            "test_label": "rice"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recognized"] is True
    assert data["label"] == "rice"
    assert data["kannada"] == "ಅಕ್ಕಿ"
    assert data["distance"] == 0.12


def test_recognize_milk():
    response = client.post(
        "/api/recognize",
        json={
            "landmarks": DUMMY_LANDMARKS,
            "test_label": "milk"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recognized"] is True
    assert data["label"] == "milk"
    assert data["kannada"] == "ಹಾಲು"


def test_recognize_sugar():
    response = client.post(
        "/api/recognize",
        json={
            "landmarks": DUMMY_LANDMARKS,
            "test_label": "sugar"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recognized"] is True
    assert data["label"] == "sugar"
    assert data["kannada"] == "ಸಕ್ಕರೆ"


def test_unknown_sign():
    response = client.post(
        "/api/recognize",
        json={
            "landmarks": DUMMY_LANDMARKS,
            "test_label": "unknown_item"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recognized"] is False
    assert data["label"] is None
    assert data["kannada"] is None


def test_missing_landmarks():
    response = client.post(
        "/api/recognize",
        json={
            "test_label": "rice"
        }
    )

    assert response.status_code == 422


def test_less_than_21_landmarks():
    response = client.post(
        "/api/recognize",
        json={
            "landmarks": DUMMY_LANDMARKS[:20],
            "test_label": "rice"
        }
    )

    assert response.status_code == 422


def test_more_than_21_landmarks():
    response = client.post(
        "/api/recognize",
        json={
            "landmarks": DUMMY_LANDMARKS + [[0.1, 0.2, 0.0]],
            "test_label": "rice"
        }
    )

    assert response.status_code == 422


def test_invalid_landmark_value():
    invalid_landmarks = [
        [0.1, 0.2, 0.0] for _ in range(21)
    ]

    invalid_landmarks[0] = ["invalid", 0.2, 0.0]

    response = client.post(
        "/api/recognize",
        json={
            "landmarks": invalid_landmarks,
            "test_label": "rice"
        }
    )

    assert response.status_code == 422