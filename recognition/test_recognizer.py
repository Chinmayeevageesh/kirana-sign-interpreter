import unittest
import numpy as np

from data_loader import load_dataset
from recognition.recognizer import SignRecognizer


class TestSignRecognizer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dataset = load_dataset()

        X = [sample["frames"] for sample in cls.dataset]
        y = [sample["label"] for sample in cls.dataset]

        cls.recognizer = SignRecognizer(distance_threshold=0.15)
        cls.recognizer.fit(X, y)

    def test_all_reference_samples(self):
        for sample in self.dataset:
            with self.subTest(label=sample["label"]):
                result = self.recognizer.predict(sample["frames"])

                self.assertEqual(result["label"], sample["label"])
                self.assertTrue(result["recognized"])

    def test_unknown_sign_rejection(self):
        unknown_input = np.full((5, 21, 3), 100.0)

        result = self.recognizer.predict(unknown_input)

        self.assertIsNone(result["label"])
        self.assertFalse(result["recognized"])
        self.assertEqual(result["status"], "unknown")

    def test_invalid_landmark_shape(self):
        with self.assertRaises(ValueError):
            self.recognizer.predict(np.zeros((10, 10)))

    def test_empty_training_data(self):
        recognizer = SignRecognizer()

        with self.assertRaises(RuntimeError):
            recognizer.predict(np.zeros((21, 3)))


if __name__ == "__main__":
    unittest.main(verbosity=2)

