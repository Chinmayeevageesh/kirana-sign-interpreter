"""Collect real static samples or short dynamic sequences from a webcam.

Static: press SPACE to save the current detected hand.
Dynamic: press R to start a sequence and R again to save it; Q exits.
This script stores normalized landmarks, not raw video. Get informed consent.
"""
import argparse, sys, time, uuid
from datetime import datetime, timezone
from pathlib import Path
import cv2

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from landmark_processing.extractor import HandLandmarkDetector
from landmark_processing.preprocessing import normalize_landmarks
from landmark_processing.dataset import append_sample

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--label", required=True, help="stable lowercase label, e.g. rice")
    ap.add_argument("--participant", required=True, help="e.g. P01")
    ap.add_argument("--session", required=True, help="e.g. S01")
    ap.add_argument("--sign-type", choices=["static", "dynamic"], default="static")
    ap.add_argument("--camera", type=int, default=0)
    ap.add_argument("--model", default="models/hand_landmarker.task")
    ap.add_argument("--output", default="Kirana_ISL_Synthetic_Dataset/processed/webcam_samples.jsonl")
    ap.add_argument("--min-frames", type=int, default=5)
    args = ap.parse_args()
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise SystemExit("Could not open webcam. Check camera permission or try --camera 1.")
    out_path = ROOT / args.output
    recording = False
    sequence = []
    frame_count = 0
    saved = 0
    start = time.monotonic()
    try:
        with HandLandmarkDetector(ROOT / args.model, video_mode=True, num_hands=2) as detector:
            print("Keep one hand fully visible. SPACE saves static; R starts/stops dynamic; Q quits.")
            while True:
                ok, frame = cap.read()
                if not ok:
                    print("Camera frame unavailable; stopping.")
                    break
                frame_count += 1
                ts = int((time.monotonic() - start) * 1000)
                hands = detector.detect(frame, ts)
                points = hands[0] if hands else None
                display = frame.copy()
                status = "HAND DETECTED" if points else "NO HAND DETECTED"
                cv2.putText(display, status, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, .7,
                            (0, 255, 0) if points else (0, 0, 255), 2)
                if args.sign_type == "dynamic":
                    cv2.putText(display, f"REC={recording} frames={len(sequence)}", (15, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, .65, (0, 200, 255), 2)
                cv2.imshow("Kirana Sign Interpreter - sample collection", display)
                key = cv2.waitKey(1) & 0xFF
                if args.sign_type == "static" and key == 32:
                    if points is None:
                        print("No hand detected; sample not saved.")
                        continue
                    norm = normalize_landmarks(points).tolist()
                    sample = make_sample(args, norm, "static", saved + 1)
                    append_sample(sample, out_path)
                    saved += 1
                    print(f"Saved {sample['sample_id']} -> {out_path}")
                elif args.sign_type == "dynamic":
                    if recording and points is not None:
                        sequence.append({"timestamp_ms": ts, "landmarks": normalize_landmarks(points).tolist()})
                    if key in (ord("r"), ord("R")):
                        if not recording:
                            recording = True
                            sequence = []
                            print("Recording sequence... perform the sign, then press R again.")
                        else:
                            recording = False
                            if len(sequence) < args.min_frames:
                                print(f"Discarded: only {len(sequence)} detected frames (minimum {args.min_frames}).")
                            else:
                                sample = make_sample(args, sequence, "dynamic", saved + 1)
                                append_sample(sample, out_path)
                                saved += 1
                                print(f"Saved dynamic sequence {sample['sample_id']} with {len(sequence)} frames.")
                            sequence = []
                if key == ord("q"):
                    break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    print(f"Finished. Samples saved this run: {saved}. Output: {out_path}")

def make_sample(args, payload, sign_type, count):
    return {
        "schema_version": "1.1",
        "sample_id": f"{args.participant}-{args.session}-{args.label}-{uuid.uuid4().hex[:8]}",
        "label": args.label.strip().lower().replace(" ", "_"),
        "participant_id": args.participant.strip(),
        "session_id": args.session.strip(),
        "sign_type": sign_type,
        "landmarks": payload if sign_type == "static" else None,
        "frames": payload if sign_type == "dynamic" else None,
        "source_type": "webcam",
        "quality": {"review_status": "needs_review", "frame_count": 1 if sign_type == "static" else len(payload),
                    "captured_at_utc": datetime.now(timezone.utc).isoformat(),
                    "normalization": "wrist_origin_max_xy_radius"},
    } | ({} if sign_type == "dynamic" else {"frames": None})

if __name__ == "__main__":
    main()

