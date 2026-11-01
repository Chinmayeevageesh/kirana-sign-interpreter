import argparse, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from landmark_processing.dataset import load_jsonl, write_json
from landmark_processing.validation import summarize, validate_record

def main():
    ap = argparse.ArgumentParser(description="Validate a JSONL landmark dataset and write a report.")
    ap.add_argument("--input", default="data/raw/samples.jsonl")
    ap.add_argument("--report", default="data/processed/validation_report.json")
    args = ap.parse_args()
    input_path = ROOT / args.input
    records = load_jsonl(input_path)
    report = summarize(records)
    write_json(ROOT / args.report, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Report saved to {ROOT / args.report}")
    if report["invalid_records"] or report["duplicate_sample_ids"]:
        raise SystemExit(1)
if __name__ == "__main__":
    main()
