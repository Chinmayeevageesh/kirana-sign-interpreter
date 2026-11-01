"""Create clearly synthetic records for testing only; never use as training data."""
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from landmark_processing.dataset import append_sample
from landmark_processing.preprocessing import normalize_landmarks
rng = np.random.default_rng(7)
path = ROOT / "data/sample_dataset/synthetic_test_samples.jsonl"
path.parent.mkdir(parents=True, exist_ok=True)
if path.exists(): path.unlink()
for label in ("rice", "milk", "sugar"):
    for i in range(3):
        # Random points are only a software fixture, not human sign data.
        pts = rng.normal(size=(21, 3)).astype(float)
        pts[0] = [0, 0, 0]
        sample = {
            "schema_version":"1.1", "sample_id":f"SYN-{label}-{i+1}",
            "label":label, "participant_id":"SYNTHETIC", "session_id":"TEST",
            "sign_type":"static", "landmarks":normalize_landmarks(pts).tolist(),
            "frames":None, "source_type":"synthetic_test_only",
            "quality":{"review_status":"synthetic_not_real_data"}
        }
        append_sample(sample, path)
print(f"Wrote synthetic test fixture to {path}. DO NOT train/evaluate on it.")
