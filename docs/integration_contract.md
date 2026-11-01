# Integration contract — agree with teammates before final handoff

## Member 2: recognition engine
- Label is lowercase English; display translations are separate.
- Static sample is `landmarks`: shape `(21,3)`; flattening gives 63 values if agreed.
- Run `normalize_landmarks` on live landmarks exactly as for training data.
- This starter collector stores the first detected hand only. If the vocabulary requires two hands, agree a two-hand feature layout first.
- Euclidean nearest-neighbor threshold must be calibrated on held-out participant/session samples. Report false accepts/rejects, not only training accuracy.
- Do not train a static nearest-neighbor classifier on dynamic sequences. Either use a sequence-aware approach or scope movement-based signs out of the first release.

## Member 3: Kannada UI and speech
- Keep machine labels and Kannada display strings separate. Use the reviewed vocabulary table as the source of truth.
- Do not claim the system translates arbitrary ISL; it recognizes only the selected trained grocery vocabulary.

## Member 4: API/backend
- Agree whether Python MediaPipe inference runs server-side or landmarks are sent from the client. A browser webcam is not automatically available to a Python process.
- Define request/response schema, confidence/distance field, no-hand status, unknown/low-confidence status and errors.
- Test with a known sample, no hand, out-of-vocabulary gesture, camera failure and malformed payload.

## Shared
- Agree model/sign label version, normalization version, handedness/mirroring, and static/dynamic policy.
- Do not commit private videos or the downloaded model binary without team approval.
