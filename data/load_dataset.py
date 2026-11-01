
import json
import numpy as np
from pathlib import Path


DATASET_PATH = Path(__file__).parent / "processed" / "landmarks.jsonl"


def load_dataset():

    samples = []

    with open(DATASET_PATH, "r") as file:

        for line in file:

            if not line.strip():
                continue

            record = json.loads(line)

            # Use only YouTube reference samples
            if record.get("source_type") != "youtube":
                continue

            frames = []

            for frame in record["frames"]:

                landmarks = np.asarray(
                    frame["landmarks"],
                    dtype=float
                )

                if landmarks.shape != (21, 3):
                    raise ValueError(
                        f"Invalid landmarks in {record['sample_id']}"
                    )

                frames.append(landmarks)

            samples.append({
                "label": record["label"],
                "sample_id": record["sample_id"],
                "frames": np.asarray(frames)
            })

    return samples


if __name__ == "__main__":

    dataset = load_dataset()

    print("Dataset loaded successfully!")
    print("Number of samples:", len(dataset))

    for sample in dataset:
        print(
            sample["label"],
            "->",
            sample["frames"].shape
        )
