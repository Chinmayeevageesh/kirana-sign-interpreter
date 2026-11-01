
import numpy as np

# Synthetic landmark data for testing the algorithm.
# These are NOT actual ISL gesture recordings.

rng = np.random.default_rng(42)

GROCERY_LABELS = ["rice", "milk", "sugar"]

# Give each dummy label a different artificial landmark pattern.
prototypes = {
    "rice":  np.full((21, 3), 0.20),
    "milk":  np.full((21, 3), 0.50),
    "sugar": np.full((21, 3), 0.80),
}

def create_dummy_dataset(samples_per_label=10):
    samples = []
    labels = []

    for label, prototype in prototypes.items():
        for _ in range(samples_per_label):
            landmarks = prototype + rng.normal(
                loc=0.0,
                scale=0.01,
                size=(21, 3)
            )

            samples.append(landmarks)
            labels.append(label)

    return np.array(samples), np.array(labels)


if __name__ == "__main__":
    X, y = create_dummy_dataset()

    print("Dataset shape:", X.shape)
    print("Labels shape:", y.shape)
    print("Labels:", np.unique(y))
