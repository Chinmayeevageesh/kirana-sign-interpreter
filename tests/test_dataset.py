import sys, tempfile, unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from landmark_processing.dataset import append_sample, load_jsonl
from landmark_processing.validation import validate_record, summarize

def sample(sample_id="T-001"):
    pts = np.zeros((21, 3)).tolist()
    pts[1] = [1.0, 0.0, 0.0]
    return {"schema_version":"1.1","sample_id":sample_id,"label":"rice",
      "participant_id":"P01","session_id":"S01","sign_type":"static",
      "landmarks":pts,"frames":None,"source_type":"test","quality":{}}

class TestDataset(unittest.TestCase):
    def test_jsonl_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "samples.jsonl"
            append_sample(sample(), path)
            self.assertEqual(load_jsonl(path)[0]["sample_id"], "T-001")
        self.assertEqual(validate_record(sample()), [])
    def test_missing_metadata_rejected_on_append(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                append_sample({"label":"rice"}, Path(d) / "x.jsonl")
    def test_duplicate_ids_reported(self):
        report = summarize([sample(), sample()])
        self.assertEqual(report["duplicate_sample_ids"], ["T-001"])
    def test_dynamic_sequence(self):
        s = sample()
        s["sign_type"] = "dynamic"
        s["frames"] = [{"timestamp_ms":0,"landmarks":s["landmarks"]},
                       {"timestamp_ms":33,"landmarks":s["landmarks"]}]
        s.pop("landmarks")
        self.assertEqual(validate_record(s), [])
    def test_bad_dynamic_sequence(self):
        s = sample()
        s["sign_type"] = "dynamic"
        s["frames"] = []
        s.pop("landmarks")
        self.assertIn("invalid:frames_need_at_least_2", validate_record(s))

if __name__ == "__main__": unittest.main()
