# Kirana ISL Synthetic Dataset - STATUS: EMPTY (0 / 200)

**This ZIP contains no videos and no landmark data.** It has the folder structure, metadata schemas and honest
reports only. Synthetic video generation was requested, but no video-generation model was available in the
environment that built this package. Videos were not faked, and no landmarks were invented or randomly generated.

## Counts
| Label | Target videos | Videos generated | Landmark samples extracted | Vocabulary status |
|---|---|---|---|---|
| rice, milk, sugar, salt, oil, dal, wheat, tea, coffee, biscuit (each) | 20 | 0 | 0 | unverified_synthetic_gesture |
| **Total** | **200** | **0** | **0** | |

## Vocabulary verification
Search confirmed that ISLRTC publishes an official ISL dictionary (video-based, ~10,000 terms), but the individual
entries for these 10 words could not be retrieved or checked. **All 10 labels are `unverified_synthetic_gesture`.**
No gesture was defined or presented as authentic ISL.

## Structure
- `vocabulary/vocabulary_verification.csv` - per-label verification status
- `raw/<label>/` - empty (generated videos would go here)
- `processed/landmarks.jsonl` - empty (MediaPipe 21-landmark x,y,z sequences would go here)
- `metadata/samples.csv` - header only; columns as requested
- `reports/` - generation, landmark extraction and validation reports (all zero)
- `splits/` - header-only train/validation/test CSVs

## Intended use / limitations
If later populated with real generated videos, such data could only test pipeline plumbing (loading, MediaPipe
extraction, training loop). Synthetic data is not genuine ISL, is not verified, and must not be used as evidence that a
model works for real ISL users. Genuine human-collected samples must be kept clearly separate.
