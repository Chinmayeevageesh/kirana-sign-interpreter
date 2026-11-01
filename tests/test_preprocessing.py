import sys, unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from landmark_processing.preprocessing import normalize_landmarks, validate_landmarks

class TestPreprocessing(unittest.TestCase):
    def test_normalization(self):
        points = np.zeros((21, 3)); points[1] = [2, 0, .5]; points[2] = [0, 1, .2]
        result = normalize_landmarks(points)
        self.assertEqual(result.shape, (21, 3))
        np.testing.assert_allclose(result[0], [0, 0, 0])
        self.assertAlmostEqual(float(np.max(np.linalg.norm(result[:, :2], axis=1))), 1.0)
    def test_translation_invariance(self):
        rng = np.random.default_rng(3)
        points = rng.random((21, 3))
        np.testing.assert_allclose(normalize_landmarks(points), normalize_landmarks(points + [4, 5, 6]), atol=1e-5)
    def test_wrong_shape(self):
        with self.assertRaises(ValueError): validate_landmarks(np.zeros((20, 3)))
    def test_nonfinite(self):
        points = np.zeros((21, 3)); points[0, 0] = np.nan
        with self.assertRaises(ValueError): normalize_landmarks(points)
    def test_degenerate(self):
        with self.assertRaises(ValueError): normalize_landmarks(np.zeros((21, 3)))

if __name__ == "__main__": unittest.main()
