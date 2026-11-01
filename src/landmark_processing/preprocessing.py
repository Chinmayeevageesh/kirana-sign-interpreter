from __future__ import annotations
import numpy as np

def validate_landmarks(landmarks) -> np.ndarray:
    """Validate and return finite float32 landmarks with shape (21, 3)."""
    arr = np.asarray(landmarks, dtype=np.float32)
    if arr.shape != (21, 3):
        raise ValueError(f"Expected shape (21, 3); got {arr.shape}")
    if not np.isfinite(arr).all():
        raise ValueError("Landmarks contain NaN or infinite values")
    return arr

def normalize_landmarks(landmarks, eps: float = 1e-8) -> np.ndarray:
    """Translate wrist to origin and scale by maximum XY radius.

    Output is (21, 3). This reduces translation/hand-size variation but does
    not normalize rotation. MediaPipe z is relative, not physical depth.
    Do not collapse movement-based signs to one frame.
    """
    arr = validate_landmarks(landmarks).copy()
    arr -= arr[0]
    scale = float(np.max(np.linalg.norm(arr[:, :2], axis=1)))
    if not np.isfinite(scale) or scale < eps:
        raise ValueError("Cannot normalize a zero-size or degenerate hand")
    arr /= scale
    return arr.astype(np.float32)
