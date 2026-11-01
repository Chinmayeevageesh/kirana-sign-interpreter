from data_loader import load_dataset
from recognition.recognizer import SignRecognizer

samples = load_dataset()

X = [sample["frames"] for sample in samples]
y = [sample["label"] for sample in samples]

model = SignRecognizer(distance_threshold=0.15)
model.fit(X, y)

print("Training completed!")
print("Training samples:", len(X))
print("Classes:", sorted(set(y)))

result = model.predict(X[0])

print("Test result:", result)
