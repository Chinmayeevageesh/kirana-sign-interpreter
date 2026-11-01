import json
from pathlib import Path
import numpy as np

DATASET_PATH = (
    Path(__file__).resolve().parent
    / "Kirana_ISL_Synthetic_Dataset"
    / "processed"
    / "landmarks.jsonl"
)

def load_dataset():
    samples = []

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            record = json.loads(line)

            if record.get("source_type") != "youtube":
                continue

            frames = []

            for frame in record.get("frames", []):
                landmarks = np.asarray(
                    frame["landmarks"], dtype=float
                )

                if landmarks.shape != (21, 3):
                    raise ValueError(
                        f"Invalid landmarks on line {line_number}"
                    )

                frames.append(landmarks)

            if not frames:
                continue

            samples.append({
                "label": record["label"],
                "sample_id": record["sample_id"],
                "frames": np.asarray(frames)
            })

    if not samples:
        raise ValueError("No valid YouTube samples found")

    return samples

