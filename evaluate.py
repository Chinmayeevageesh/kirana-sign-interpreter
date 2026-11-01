from data.load_dataset import load_dataset
from recognition.recognizer import SignRecognizer

# Load the 10 YouTube reference samples
dataset = load_dataset()

X = [sample["frames"] for sample in dataset]
y = [sample["label"] for sample in dataset]

# Train the recognizer
recognizer = SignRecognizer(distance_threshold=0.15)
recognizer.fit(X, y)

print("\nREAL DATASET RECOGNITION TEST")
print("-" * 35)

correct = 0

for sample in dataset:

    result = recognizer.predict(sample["frames"])

    print(
        f'{sample["label"]:10} -> '
        f'{result["label"]:10} '
        f'Distance: {result["distance"]:.4f}'
    )

    if result["label"] == sample["label"]:
        correct += 1

print("-" * 35)
print(f"Self-match results: {correct}/{len(dataset)}")
print("Note: These are training-sample self-matches, not independent accuracy.")
