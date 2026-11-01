# Kirana Sign Interpreter — Member 1 package (Weeks 1–3)

Member 1 owns the vocabulary register, dataset collection protocol, MediaPipe hand-landmark extraction, normalization, dataset creation/quality checks, and the data contract for the recognition teammate.

## What is implemented in this package
- MediaPipe Tasks hand detector for still images and webcam video.
- Webcam collection for **static samples** (SPACE) and **dynamic sequences** (R to start/stop).
- 21-point (x, y, z) validation and wrist-origin / maximum-XY-radius normalization.
- JSON Lines dataset storage, metadata, static/dynamic schema, dataset validation/report, duplicate sample-ID check and class/participant/session summaries.
- Synthetic fixture generation for software tests only; these are **not real sign data**.
- Documentation for the three-week work plan, vocabulary verification, data collection, extraction and integration.

## Honest completion boundary
Code can be prepared here, but it cannot truthfully collect your team’s recordings or verify each grocery sign on behalf of an ISL signer. The vocabulary register has the official source links but each candidate's exact sign still needs to be looked up and reviewed. A model file and working webcam are also required to run collection. Do not present synthetic data as a real training dataset.

## Setup (Windows PowerShell)
Use a Python version supported by the installed MediaPipe package. Python 3.11 is a practical starting point, but check current MediaPipe compatibility for your machine.

```powershell
cd path\to\Kirana_Sign_Interpreter_Member1_Weeks1-3
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` instead of activating.

### MediaPipe model file
Download the official **Hand Landmarker** task model from the MediaPipe Hand Landmarker documentation:
https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker
Save the downloaded `.task` file as `models/hand_landmarker.task`. This repository intentionally does not bundle the model binary.

## Run software tests and make a test fixture
```powershell
python -m unittest discover -s tests -v
python scripts/create_dummy_dataset.py
python scripts/validate_dataset.py --input data/sample_dataset/synthetic_test_samples.jsonl --report data/processed/synthetic_validation_report.json
```
The synthetic file only tests the software. Never train or report model accuracy using it.

## Collect real static samples
Start with a confirmed sign and a consistent setup. Example:
```powershell
python scripts/collect_webcam.py --label rice --participant P01 --session S01 --sign-type static
```
- The webcam window shows whether a hand is detected.
- Hold the sign steady and press **SPACE** to save one sample.
- Repeat for each sign and participant. Press **Q** to quit.
- The default output is `data/raw/samples.jsonl`.
- Do not record a label until the sign is verified. Use the exact stable machine label from the vocabulary register.

## Collect a dynamic sign
Only use this when the reviewed sign genuinely depends on movement. Example:
```powershell
python scripts/collect_webcam.py --label milk --participant P01 --session S01 --sign-type dynamic
```
Press **R** to begin, perform the sign, then press **R** to stop and save. It stores normalized landmark frames, not raw video. The minimum default is 5 detected frames; the validator requires at least 2.

## Validate real data
```powershell
python scripts/validate_dataset.py --input data/raw/samples.jsonl --report data/processed/validation_report.json
```
Exit code 1 means invalid rows or duplicate sample IDs were found. Read the report and fix the causes before handoff. Review class balance and the per-participant/per-session counts manually too.

## Before handing off to Member 2
- Agree whether they need 63 flattened values or 21×3 arrays. This package stores 21×3 arrays.
- Use this exact preprocessing for both saved training samples and live inference.
- Agree on left/right-hand policy and whether to mirror camera frames. Do not mix mirrored and unmirrored samples without a policy.
- Agree a threshold using a validation set; do not tune and report accuracy on the same samples.
- Static nearest-neighbor recognition does not correctly represent movement-based signs. Dynamic signs need a sequence-aware feature/model or should be excluded from the first demo.
- Send the teammate the verified vocabulary mapping and only reviewed, valid real data. Share this repo's integration contract.

## Important limits
Normalization removes translation and approximate hand-size variation; it does not normalize rotation, viewpoint, handedness, camera mirroring, or signing speed. MediaPipe z is relative and is not a physical depth measurement. Quality review and diverse real samples remain necessary.
