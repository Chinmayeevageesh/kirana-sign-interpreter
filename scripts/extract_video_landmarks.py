import sys, csv, json, re
from pathlib import Path
import cv2

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.landmark_processing.extractor import HandLandmarkDetector
from src.landmark_processing.preprocessing import normalize_landmarks

RAW = ROOT / "Kirana_ISL_Synthetic_Dataset" / "raw"
OUT = ROOT / "Kirana_ISL_Synthetic_Dataset" / "processed" / "landmarks.jsonl"
META = ROOT / "Kirana_ISL_Synthetic_Dataset" / "metadata" / "samples.csv"
REPORT = ROOT / "Kirana_ISL_Synthetic_Dataset" / "reports" / "landmark_extraction_report.csv"

OUT.parent.mkdir(parents=True, exist_ok=True)
META.parent.mkdir(parents=True, exist_ok=True)
REPORT.parent.mkdir(parents=True, exist_ok=True)

metadata = []
report = []

with OUT.open("w", encoding="utf-8") as output:
    for folder in sorted(RAW.iterdir()):
        if not folder.is_dir():
            continue

        label = folder.name.lower()
        videos = list(folder.glob("*.mp4"))
        extracted = 0
        failed = 0

        for video in videos:
            cap = cv2.VideoCapture(str(video))
            if not cap.isOpened():
                failed += 1
                continue

            fps = cap.get(cv2.CAP_PROP_FPS)
            if not fps or fps <= 0:
                fps = 25

            frames = []
            frame_index = 0
            last_timestamp = -1

            try:
                with HandLandmarkDetector(
                    model_path=str(ROOT / "models" / "hand_landmarker.task"),
                    video_mode=True
                ) as detector:
                    while True:
                        ok, frame = cap.read()
                        if not ok:
                            break

                        if frame_index % 5 == 0:
                            timestamp = max(
                                int(frame_index * 1000 / fps),
                                last_timestamp + 1
                            )
                            last_timestamp = timestamp

                            hands = detector.detect(frame, timestamp_ms=timestamp)

                            if hands:
                                normalized = normalize_landmarks(hands[0])
                                frames.append({
                                    "timestamp_ms": timestamp,
                                    "landmarks": normalized.tolist()
                                })

                        frame_index += 1
            except Exception as e:
                print(f"FAILED: {video.name}: {e}")
                failed += 1
                cap.release()
                continue

            cap.release()

            if not frames:
                print(f"NO HAND DETECTED: {video.name}")
                failed += 1
                continue

            sample_id = re.sub(r"[^a-zA-Z0-9_-]", "_", video.stem)
            sample_id = f"{label}_{sample_id}"

            sample = {
                "schema_version": "1.0",
                "sample_id": sample_id,
                "label": label,
                "participant_id": "external_youtube",
                "session_id": "youtube_import",
                "sign_type": "dynamic",
                "source_type": "youtube",
                "quality": "needs_review",
                "frames": frames
            }

            output.write(json.dumps(sample) + "\n")
            metadata.append({
                "sample_id": sample_id,
                "label": label,
                "synthetic_subject_id": "external_youtube",
                "source_type": "youtube",
                "generation_method": "existing_youtube_video",
                "sign_type": "dynamic",
                "recording_path": str(video.relative_to(ROOT)),
                "landmark_extraction_status": "success",
                "vocabulary_verification_status": "unverified",
                "review_status": "needs_review"
            })
            extracted += 1
            print(f"EXTRACTED: {label} - {len(frames)} frames")

        report.append({
            "label": label,
            "videos_available": len(videos),
            "landmark_samples_extracted": extracted,
            "extraction_failed": failed,
            "status": "completed",
            "notes": "External YouTube videos; signs require verification"
        })

columns = [
    "sample_id", "label", "synthetic_subject_id", "source_type",
    "generation_method", "sign_type", "recording_path",
    "landmark_extraction_status", "vocabulary_verification_status",
    "review_status"
]
with META.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(metadata)

report_columns = [
    "label", "videos_available", "landmark_samples_extracted",
    "extraction_failed", "status", "notes"
]
with REPORT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=report_columns)
    writer.writeheader()
    writer.writerows(report)

print("\nDONE")
print("Videos processed:", sum(r["videos_available"] for r in report))
print("Samples extracted:", len(metadata))
print("Failed videos:", sum(r["extraction_failed"] for r in report))
print("Landmarks saved:", OUT)
