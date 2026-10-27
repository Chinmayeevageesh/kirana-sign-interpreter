
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Kirana Sign Interpreter API")

# Allow our local website to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

GROCERY_KANNADA = {
    "rice": "ಅಕ್ಕಿ",
    "milk": "ಹಾಲು",
    "sugar": "ಸಕ್ಕರೆ",
}

class RecognitionRequest(BaseModel):
    landmarks: list[list[float]] = Field(min_length=21, max_length=21)

    # Temporary field for testing the website.
    # Remove it when real recognition is integrated.
    test_label: str | None = None

@app.get("/")
def home():
    return {
        "message": "Kirana Sign Interpreter API is running"
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/recognize")
def recognize(request: RecognitionRequest):
    # TEMPORARY dummy prediction.
    # Later, call the real landmark recognition module here.
    label = request.test_label

    if label not in GROCERY_KANNADA:
        return {
            "recognized": False,
            "label": None,
            "kannada": None,
            "distance": None,
            "message": "Sign not recognized"
        }

    return {
        "recognized": True,
        "label": label,
        "kannada": GROCERY_KANNADA[label],
        "distance": 0.12,  # Dummy value, not a real measurement
        "message": "Sign recognized successfully"
    }