from collections import Counter
from .preprocessing import validate_landmarks

def _valid_points(points):
    try:
        validate_landmarks(points)
        return True
    except (TypeError, ValueError):
        return False

def validate_record(record: dict) -> list[str]:
    errors = []
    for key in ("sample_id", "label", "participant_id", "session_id", "sign_type", "source_type", "quality"):
        if key not in record or record[key] in (None, ""):
            errors.append(f"missing_or_empty:{key}")
    sign_type = record.get("sign_type")
    if sign_type not in ("static", "dynamic"):
        errors.append("invalid:sign_type")
    if sign_type == "static":
        if not _valid_points(record.get("landmarks")):
            errors.append("invalid:landmarks_shape_or_values")
    elif sign_type == "dynamic":
        frames = record.get("frames")
        if not isinstance(frames, list) or len(frames) < 2:
            errors.append("invalid:frames_need_at_least_2")
        else:
            for i, frame in enumerate(frames):
                points = frame.get("landmarks") if isinstance(frame, dict) else None
                if not _valid_points(points):
                    errors.append(f"invalid:frame_{i}_landmarks")
                    break
    if record.get("schema_version") != "1.1":
        errors.append("unsupported_or_missing:schema_version")
    return errors

def summarize(records: list[dict]) -> dict:
    rows = [(r.get("sample_id", f"row_{i+1}"), validate_record(r)) for i, r in enumerate(records)]
    ids = [r.get("sample_id") for r in records if r.get("sample_id")]
    duplicate_ids = sorted(k for k, count in Counter(ids).items() if count > 1)
    labels = Counter(r.get("label", "<missing>") for r in records)
    return {
        "total_records": len(records),
        "valid_records": sum(not e for _, e in rows),
        "invalid_records": sum(bool(e) for _, e in rows),
        "duplicate_sample_ids": duplicate_ids,
        "samples_per_label": dict(sorted(labels.items())),
        "samples_per_participant": dict(sorted(Counter(r.get("participant_id", "<missing>") for r in records).items())),
        "samples_per_session": dict(sorted(Counter(r.get("session_id", "<missing>") for r in records).items())),
        "sign_type_counts": dict(sorted(Counter(r.get("sign_type", "<missing>") for r in records).items())),
        "labels_below_10_samples": sorted(label for label, count in labels.items() if count < 10),
        "errors": [{"sample_id": sid, "errors": e} for sid, e in rows if e],
    }
