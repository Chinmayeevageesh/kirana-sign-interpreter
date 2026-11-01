from pathlib import Path
import cv2
import mediapipe as mp

class HandLandmarkDetector:
    """Reusable MediaPipe Tasks detector for IMAGE or VIDEO mode."""
    def __init__(self, model_path="models/hand_landmarker.task", video_mode=False, num_hands=2):
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}. Download the official MediaPipe "
                "Hand Landmarker model bundle and save it at this path. See README.md."
            )
        self.video_mode = video_mode
        mode = (mp.tasks.vision.RunningMode.VIDEO if video_mode
                else mp.tasks.vision.RunningMode.IMAGE)
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(self.model_path)),
            running_mode=mode, num_hands=num_hands)
        self.detector = mp.tasks.vision.HandLandmarker.create_from_options(options)

    def detect(self, frame_bgr, timestamp_ms=None):
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        if self.video_mode:
            if timestamp_ms is None:
                raise ValueError("timestamp_ms is required in VIDEO mode")
            result = self.detector.detect_for_video(image, int(timestamp_ms))
        else:
            result = self.detector.detect(image)
        hands = []
        for hand in (result.hand_landmarks or []):
            hands.append([[float(p.x), float(p.y), float(p.z)] for p in hand])
        return hands

    def close(self):
        self.detector.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

def extract_landmarks_from_image(image_path, model_path="models/hand_landmarker.task"):
    image_path = Path(image_path)
    image_bgr = cv2.imread(str(image_path))
    if image_bgr is None:
        raise ValueError(f"Could not read image: {image_path}")
    with HandLandmarkDetector(model_path, video_mode=False) as detector:
        hands = detector.detect(image_bgr)
    return hands[0] if hands else None
