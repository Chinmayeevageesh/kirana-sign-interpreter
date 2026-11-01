# Real data collection protocol

## Before recording
- Obtain consent from each participant. Explain the purpose and where data will be stored/shared.
- Agree on the exact sign and meaning with an ISL teacher/interpreter or Deaf ISL user.
- Use the same label spelling across all participants.
- Prefer a plain background, steady light, visible wrist and fingertips, and a camera around chest/hand height.
- Keep the entire hand in frame. Avoid strong backlight, motion blur, occlusion and jewellery that hides joints.
- Decide and document left/right hand, camera mirroring and orientation policy. Do not silently mix policies.

## Collection procedure
1. Create a unique participant ID (`P01`–`P04`) and session ID (`S01`, `S02`, etc.). Avoid names in public datasets.
2. Start `scripts/collect_webcam.py` with the exact reviewed machine label.
3. Static: make the sign, hold it still, wait for hand detection, press SPACE. Change the angle/distance slightly between samples while keeping the sign correct.
4. Dynamic: only if movement is essential; press R, perform one complete sign, press R again.
5. Collect multiple examples across all participants and at least two sessions if possible. Aim initially for 30–50 clean samples per class across people; this is a project target, not a guarantee of model performance. Ensure each class has contributions from all four participants where feasible.
6. Review the data report. Mark questionable signs/samples for review and recollect them. Do not edit landmark coordinates manually to make samples look better.
7. Keep original videos only if needed and consented to. The provided collector stores landmarks, not video. Restrict access to raw data and avoid committing personal recordings to a public repository.

## Record-level metadata
- `sample_id`: unique, generated ID
- `label`: stable lowercase English machine label
- `participant_id`, `session_id`
- `sign_type`: static or dynamic
- `source_type`: webcam
- `quality.review_status`: initially `needs_review`; update after human review
- `quality.captured_at_utc`, `quality.frame_count`, normalization policy

## Quality checks
Reject/recollect when hand is cut off, no hand is detected, fingertips/wrist are occluded, frames are blurry, the performed sign is uncertain, or the participant uses a different sign than the approved reference. Data should reflect natural variation, not just nearly identical repetitions from one person.
