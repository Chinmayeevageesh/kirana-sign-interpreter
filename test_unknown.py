import numpy as np
from data.load_dataset import load_dataset
from recognition.recognizer import SignRecognizer

dataset = load_dataset()

X = [sample["frames"] for sample in dataset]
y = [sample["label"] for sample in dataset]

recognizer = SignRecognizer(distance_threshold=0.15)
recognizer.fit(X, y)

# Create an artificial input far from the reference landmarks
unknown_input = np.full((5, 21, 3), 100.0)

result = recognizer.predict(unknown_input)

print("UNKNOWN SIGN TEST")
print("-----------------")
print("Predicted label:", result["label"])
print("Distance:", result["distance"])
print("Recognized:", result["recognized"])
print("Status:", result["status"])
