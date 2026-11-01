# Three-week Member 1 plan and acceptance checklist

## Week 1 — foundation
- [ ] Confirm the 8–10 item vocabulary with all members.
- [ ] Look up each exact concept in the official ISLRTC dictionary; record exact result/video URL and variants.
- [ ] Ask an ISL teacher/interpreter or Deaf ISL user to review signs and intended meanings.
- [x] Create project structure, schema, normalization and extraction modules.
- [x] Add synthetic fixture generation and unit tests.
- [ ] Install dependencies and official `.task` model on your computer; run tests there.
- [ ] Agree labels, static/dynamic sign types, hand/mirroring policy and feature format with teammates.

**Week 1 exit:** code runs locally; candidate signs and data contract are agreed; unverified signs remain clearly marked.

## Week 2 — real data and preprocessing
- [ ] Run a webcam smoke test with the model installed.
- [ ] Collect consented real samples from all four participants using the same protocol.
- [ ] Collect varied clean examples for each approved sign; target 30–50 samples per class as an initial project target, with all participants represented where feasible.
- [ ] Review samples, recollect poor detections and record source/reviewer metadata.
- [x] Implement static sample collection and optional dynamic frame-sequence capture.
- [x] Implement dataset validation report with class, participant, session and duplicate-ID summaries.
- [ ] Run validator on the real dataset and resolve errors.

**Week 2 exit:** reviewed real JSONL dataset exists; no synthetic samples are mixed into it; collection metadata and validation report are saved.

## Week 3 — quality, handoff and integration
- [ ] Check class balance and participant/session diversity; add samples to weak classes.
- [ ] Hold out participant/session samples for validation; never tune and report on the same data.
- [ ] Confirm with Member 2 the exact feature layout and shared preprocessing.
- [ ] Test no-hand, bad-frame, unknown gesture and low-confidence cases with the team.
- [ ] Confirm Member 3 Kannada strings and speech output use the reviewed vocabulary mapping.
- [ ] Confirm Member 4 API behavior and frontend-to-backend camera flow.
- [ ] Save final validation report, dataset version/date, known limitations and team sign-off.

**Week 3 exit:** Member 2 receives the agreed real dataset + schema + preprocessing contract; the team has tested at least one end-to-end path. Code in this ZIP alone does not mean the real-world exit criteria have been met.
