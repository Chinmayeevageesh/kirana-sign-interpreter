
import numpy as np

# Grocery labels for dummy testing
GROCERY_LABELS = ["rice", "milk", "sugar"]

# Generate artificial landmark patterns
rng = np.random.default_rng(42)

prototypes = {
    "rice": np.full((21, 3), 0.20),
    "milk": np.full((21, 3), 0.50),
    "sugar": np.full((21, 3), 0.80)
}


def create_dummy_dataset(samples_per_label=10):
    samples = []
    labels = []

    for label, prototype in prototypes.items():
        for _ in range(samples_per_label):

            landmarks = prototype + rng.normal(
                0.0, 0.01, size=(21, 3)
            )

            samples.append(landmarks)
            labels.append(label)

    return np.array(samples), np.array(labels)


if __name__ == "__main__":
    X, y = create_dummy_dataset()

    print("Dataset shape:", X.shape)
    print("Labels shape:", y.shape)
    print("Labels:", np.unique(y))
