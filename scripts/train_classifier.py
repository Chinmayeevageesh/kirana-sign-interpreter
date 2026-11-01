
import json
from pathlib import Path
from collections import Counter

import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "Kirana_ISL_Synthetic_Dataset" / "processed" / "landmarks.jsonl"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "grocery_classifier.joblib"

X, y = [], []

with DATA.open("r", encoding="utf-8") as file:
    for line in file:
        sample = json.loads(line)
        frames = sample.get("frames", [])

        if not frames:
            continue

        # Average the 21 hand landmarks across video frames
        frame_arrays = []
        for frame in frames:
            points = np.asarray(frame["landmarks"], dtype=np.float32)
            if points.shape == (21, 3) and np.isfinite(points).all():
                frame_arrays.append(points)

        if not frame_arrays:
            continue

        features = np.mean(frame_arrays, axis=0).flatten()
        X.append(features)
        y.append(sample["label"])

counts = Counter(y)
print("Samples per grocery:", dict(counts))

if len(counts) < 2 or min(counts.values()) < 2:
    print("\nNOT ENOUGH INDEPENDENT SAMPLES.")
    print("Collect more labelled videos from different performances.")
    print("Aim for at least 20 samples per grocery.")
    raise SystemExit(1)

X = np.asarray(X)
y = np.asarray(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)
model.fit(X_train, y_train)

print("\nTest results:")
print(classification_report(y_test, model.predict(X_test), zero_division=0))

MODEL_DIR.mkdir(exist_ok=True)
joblib.dump(model, MODEL_PATH)
print("\nModel saved to:", MODEL_PATH)
