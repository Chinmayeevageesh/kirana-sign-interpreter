# Dataset schema v1.1

Format: UTF-8 JSON Lines (`.jsonl`), one sample object per line.

## Static sample
- `schema_version`: `"1.1"`
- `sample_id`: unique string
- `label`: lowercase stable machine label, e.g. `"rice"`
- `participant_id`, `session_id`: anonymized IDs
- `sign_type`: `"static"`
- `landmarks`: 21 arrays of `[x,y,z]`, normalized
- `frames`: `null` for static records
- `source_type`: `"webcam"` or `"synthetic_test_only"`
- `quality`: object with review status and capture metadata

## Dynamic sample
Same metadata, but `sign_type` is `"dynamic"` and `frames` is a list of `{ "timestamp_ms": integer, "landmarks": 21×3 array }`. Each frame is normalized independently. This is a baseline format, not a complete temporal model; the recognition teammate must use a sequence-aware method.

## Coordinate policy
MediaPipe landmark x/y are image-normalized coordinates; z is relative. Preprocessing subtracts wrist point 0 and divides by the maximum XY distance from wrist. Same function must be used in training and inference.

## Validation
`validation.py` checks metadata, schema version, static shape/finiteness, dynamic sequence length and each frame's shape/finiteness. Report checks duplicate IDs and class/participant/session counts. The `labels_below_10_samples` field is a warning heuristic, not a statistical quality guarantee.

## Example record (illustrative schema only)
```json
{
  "schema_version": "1.1",
  "sample_id": "P01-S01-rice-ab12cd34",
  "label": "rice",
  "participant_id": "P01",
  "session_id": "S01",
  "sign_type": "static",
  "landmarks": [[0.0, 0.0, 0.0]],
  "frames": null,
  "source_type": "webcam",
  "quality": {"review_status": "needs_review"}
}
```
The example abbreviates `landmarks`; a real static sample must contain exactly 21 points.
