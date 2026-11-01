# MediaPipe extraction

`src/landmark_processing/extractor.py` uses MediaPipe Tasks Hand Landmarker and OpenCV. Place the official `.task` model at `models/hand_landmarker.task`. The reusable detector supports still images and webcam VIDEO mode. It returns up to two detected hands; the starter collector uses the first detected hand.

Landmark order follows MediaPipe's 21-point hand topology (wrist, thumb, index, middle, ring, little finger landmarks). x/y are normalized to image dimensions; z is relative. They are not millimetres.

`normalize_landmarks`:
1. Validates exactly 21 finite 3D points.
2. Subtracts wrist point 0 from every point.
3. Scales all coordinates by the maximum XY distance from the wrist.
4. Rejects degenerate/zero-size inputs.

Limitations: this does not standardize hand rotation, camera viewpoint, handedness or mirroring. For signs using both hands, this baseline collector currently stores the first detected hand only. If the team's chosen signs require both hands, implement a two-hand representation before collecting the final dataset; do not assume the second hand can be ignored.
