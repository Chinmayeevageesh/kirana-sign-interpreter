from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable

REQUIRED_KEYS = {"schema_version", "sample_id", "label", "participant_id",
                 "session_id", "sign_type", "source_type", "quality"}
STATIC_KEYS = {"landmarks"}
DYNAMIC_KEYS = {"frames"}

def validate_sample_shape(sample: dict) -> list[str]:
    """Validate common metadata and static/dynamic payload shape without NumPy."""
    errors = []
    for key in REQUIRED_KEYS:
        if key not in sample or sample[key] in (None, ""):
            errors.append(f"missing_or_empty:{key}")
    sign_type = sample.get("sign_type")
    if sign_type not in ("static", "dynamic"):
        errors.append("invalid:sign_type")
    if sign_type == "static" and "landmarks" not in sample:
        errors.append("missing:landmarks")
    if sign_type == "dynamic" and "frames" not in sample:
        errors.append("missing:frames")
    if sign_type == "dynamic" and not isinstance(sample.get("frames"), list):
        errors.append("invalid:frames")
    return errors

def append_sample(sample: dict, path: str | Path) -> None:
    """Append one JSON object per line; caller should validate landmarks first."""
    errors = validate_sample_shape(sample)
    if errors:
        raise ValueError("Invalid sample: " + ", ".join(errors))
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(sample, ensure_ascii=False, allow_nan=False) + "\n")

def load_jsonl(path: str | Path) -> list[dict]:
    """Read JSONL and report malformed line numbers."""
    p = Path(path)
    if not p.exists():
        return []
    records = []
    with p.open(encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
    return records

def write_json(path: str | Path, data: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
