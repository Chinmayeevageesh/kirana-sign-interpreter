from fastapi.testclient import TestClient

from data_loader import load_dataset
from main import app


def test_home_endpoint():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Kirana Sign Interpreter API is running"
    )


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["recognizer_ready"] is True


def test_recognize_rice():
    samples = load_dataset()
    rice_sample = next(s for s in samples if s["label"] == "rice")

    with TestClient(app) as client:
        response = client.post(
            "/api/recognize",
            json={"landmarks": rice_sample["frames"].tolist()},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["recognized"] is True
    assert data["label"] == "rice"
    assert data["kannada"] == "ಅಕ್ಕಿ"
    assert data["status"] == "recognized"


def test_recognize_milk():
    samples = load_dataset()
    sample = next(s for s in samples if s["label"] == "milk")

    with TestClient(app) as client:
        response = client.post(
            "/api/recognize",
            json={"landmarks": sample["frames"].tolist()},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["recognized"] is True
    assert data["label"] == "milk"
    assert data["kannada"] == "ಹಾಲು"


def test_recognize_sugar():
    samples = load_dataset()
    sample = next(s for s in samples if s["label"] == "sugar")

    with TestClient(app) as client:
        response = client.post(
            "/api/recognize",
            json={"landmarks": sample["frames"].tolist()},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["recognized"] is True
    assert data["label"] == "sugar"
    assert data["kannada"] == "ಸಕ್ಕರೆ"


def test_unknown_sign():
    unknown_landmarks = [
        [[100.0, 100.0, 100.0] for _ in range(21)]
        for _ in range(5)
    ]

    with TestClient(app) as client:
        response = client.post(
            "/api/recognize",
            json={"landmarks": unknown_landmarks},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["recognized"] is False
    assert data["label"] is None
    assert data["kannada"] is None
    assert data["status"] == "unknown"


def test_missing_landmarks():
    with TestClient(app) as client:
        response = client.post("/api/recognize", json={})

    assert response.status_code == 422


def test_empty_landmarks():
    with TestClient(app) as client:
        response = client.post(
            "/api/recognize",
            json={"landmarks": []},
        )

    assert response.status_code == 422


def test_less_than_21_landmarks():
    frame = [[0.1, 0.2, 0.0] for _ in range(20)]

    with TestClient(app) as client:
        response = client.post(
            "/api/recognize",
            json={"landmarks": [frame]},
        )

    assert response.status_code == 422


def test_more_than_21_landmarks():
    frame = [[0.1, 0.2, 0.0] for _ in range(22)]

    with TestClient(app) as client:
        response = client.post(
            "/api/recognize",
            json={"landmarks": [frame]},
        )

    assert response.status_code == 422


def test_invalid_landmark_value():
    frame = [[0.1, 0.2, 0.0] for _ in range(21)]
    frame[0] = ["invalid", 0.2, 0.0]

    with TestClient(app) as client:
        response = client.post(
            "/api/recognize",
            json={"landmarks": [frame]},
        )

    assert response.status_code == 422


def test_landmark_with_wrong_coordinate_count():
    frame = [[0.1, 0.2, 0.0] for _ in range(21)]
    frame[5] = [0.1, 0.2]

    with TestClient(app) as client:
        response = client.post(
            "/api/recognize",
            json={"landmarks": [frame]},
        )

    assert response.status_code == 422


def test_landmark_with_extra_coordinate():
    frame = [[0.1, 0.2, 0.0] for _ in range(21)]
    frame[5] = [0.1, 0.2, 0.0, 0.4]

    with TestClient(app) as client:
        response = client.post(
            "/api/recognize",
            json={"landmarks": [frame]},
        )

    assert response.status_code == 422

def test_non_finite_landmark_value():
    import pytest
    from pydantic import ValidationError
    from main import RecognitionRequest

    frame = [[0.1, 0.2, 0.0] for _ in range(21)]
    frame[0] = [float("nan"), 0.2, 0.0]

    with pytest.raises(ValidationError):
        RecognitionRequest(landmarks=[frame])