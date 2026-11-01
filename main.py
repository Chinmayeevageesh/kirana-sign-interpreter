from contextlib import asynccontextmanager
from math import isfinite

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from data_loader import load_dataset
from recognition.recognizer import SignRecognizer

GROCERY_KANNADA = {
    "rice": "ಅಕ್ಕಿ",
    "milk": "ಹಾಲು",
    "sugar": "ಸಕ್ಕರೆ",
    "salt": "ಉಪ್ಪು",
    "oil": "ಎಣ್ಣೆ",
    "dal": "ಬೇಳೆ",
    "wheat": "ಗೋಧಿ",
    "tea": "ಚಹಾ",
    "coffee": "ಕಾಫಿ",
    "biscuit": "ಬಿಸ್ಕತ್ತು",
}

recognizer = SignRecognizer(distance_threshold=0.15)

@asynccontextmanager
async def lifespan(app: FastAPI):
    samples = load_dataset()
    X = [sample["frames"] for sample in samples]
    y = [sample["label"] for sample in samples]
    recognizer.fit(X, y)
    print(f"Recognizer trained with {len(samples)} samples")
    print(f"Labels: {sorted(set(y))}")
    yield

app = FastAPI(
    title="Kirana Sign Interpreter API",
    description="Backend API for the Kirana Sign Interpreter project",
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:8003",
        "http://localhost:8003",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class RecognitionRequest(BaseModel):
    landmarks: list[list[list[float]]] = Field(
        min_length=1,
        max_length=120,
    )

    @field_validator("landmarks")
    @classmethod
    def validate_landmarks(cls, frames):
        for frame_index, frame in enumerate(frames):
            if len(frame) != 21:
                raise ValueError(
                    f"Frame {frame_index} must contain 21 landmarks"
                )
            for point_index, point in enumerate(frame):
                if len(point) != 3:
                    raise ValueError(
                        f"Frame {frame_index}, landmark {point_index} "
                        "must contain 3 coordinates"
                    )
                if not all(isfinite(value) for value in point):
                    raise ValueError("Non-finite coordinate detected")
        return frames

@app.get("/")
def home():
    return {"message": "Kirana Sign Interpreter API is running"}

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "recognizer_ready": bool(recognizer.X_train),
    }

@app.post("/api/recognize")
def recognize(request: RecognitionRequest):
    try:
        result = recognizer.predict(request.landmarks)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail="Recognizer is not ready",
        ) from exc

    label = result["label"] if result["recognized"] else None

    return {
        **result,
        "kannada": GROCERY_KANNADA.get(label) if label else None,
        "message": (
            "Sign recognized successfully"
            if result["recognized"]
            else "Sign not recognized"
        ),
    }
