from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Kirana Sign Interpreter API",
    description="Backend API for the Kirana Sign Interpreter project",
    version="0.1.0"
)

# CORS configuration for local frontend development
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

# Grocery names in Kannada
GROCERY_KANNADA = {
    "rice": "ಅಕ್ಕಿ",
    "milk": "ಹಾಲು",
    "sugar": "ಸಕ್ಕರೆ",
}


class RecognitionRequest(BaseModel):
    landmarks: list[list[float]] = Field(
        min_length=21,
        max_length=21
    )

    # Temporary testing field.
    # Remove after integrating real recognition.
    test_label: str | None = None


@app.get("/")
def home():
    return {
        "message": "Kirana Sign Interpreter API is running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/api/recognize")
def recognize(request: RecognitionRequest):

    # TEMPORARY dummy prediction.
    # Actual recognition will be integrated later.
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
        "distance": 0.12,
        "message": "Sign recognized successfully"
    }