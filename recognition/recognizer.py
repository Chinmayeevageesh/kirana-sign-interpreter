import numpy as np


class SignRecognizer:

    def __init__(self, distance_threshold=0.15):
        self.distance_threshold = distance_threshold
        self.X_train = []
        self.y_train = []

    # Prepare a sign sequence
    def preprocess(self, landmarks):

        points = np.asarray(landmarks, dtype=float)

        # Accept a single frame
        if points.shape == (21, 3):
            points = points[np.newaxis, :, :]

        if points.ndim != 3 or points.shape[1:] != (21, 3):
            raise ValueError(
                "Expected landmarks with shape (frames, 21, 3)"
            )

        if len(points) == 0 or not np.all(np.isfinite(points)):
            raise ValueError("Invalid landmark values")

        return points

    # Train using reference sign sequences
    def fit(self, X, y):

        if len(X) != len(y) or len(y) == 0:
            raise ValueError("Invalid training data or labels")

        self.X_train = [
            self.preprocess(sequence) for sequence in X
        ]

        self.y_train = np.asarray(y)

        return self

    # Euclidean distance between two frames
    def frame_distance(self, frame1, frame2):

        distances = np.linalg.norm(frame1 - frame2, axis=1)

        return float(np.mean(distances))

    # Dynamic Time Warping for different sequence lengths
    def dtw_distance(self, sequence1, sequence2):

        n = len(sequence1)
        m = len(sequence2)

        dp = np.full((n + 1, m + 1), np.inf)
        dp[0, 0] = 0.0

        for i in range(1, n + 1):
            for j in range(1, m + 1):

                cost = self.frame_distance(
                    sequence1[i - 1],
                    sequence2[j - 1]
                )

                dp[i, j] = cost + min(
                    dp[i - 1, j],
                    dp[i, j - 1],
                    dp[i - 1, j - 1]
                )

        # Average cost along the alignment path
        return float(dp[n, m] / (n + m))

    # Predict the grocery sign
    def predict(self, landmarks):

        if len(self.X_train) == 0:
            raise RuntimeError("Train the recognizer first")

        query = self.preprocess(landmarks)

        distances = [
            self.dtw_distance(query, reference)
            for reference in self.X_train
        ]

        nearest_index = int(np.argmin(distances))
        min_distance = distances[nearest_index]

        if min_distance > self.distance_threshold:

            return {
                "label": None,
                "distance": min_distance,
                "recognized": False,
                "status": "unknown"
            }

        return {
            "label": str(self.y_train[nearest_index]),
            "distance": min_distance,
            "recognized": True,
            "status": "recognized"
        }
