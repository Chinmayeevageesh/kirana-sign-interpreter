# Kirana Sign Interpreter – Member 1 Handover Report

## Role
Sign Vocabulary, Dataset and Landmark Processing

## Grocery Vocabulary
1. Rice
2. Milk
3. Sugar
4. Salt
5. Oil
6. Dal
7. Wheat
8. Tea
9. Coffee
10. Biscuit

## Technology
- Python
- OpenCV
- MediaPipe
- 21 hand landmarks
- Landmark normalization

## Work Completed
- Set up the Python environment and installed dependencies.
- Added 10 initial grocery video samples from YouTube.
- Extracted hand landmarks from all 10 videos.
- Generated processed landmark JSONL data.
- Collected one additional Rice sample using the webcam.
- Generated sample metadata CSV with source URL information.
- Generated train, validation and test split CSV files.
- Generated dataset validation and summary reports.
- Created project file inventory.
- Successfully completed 10 unit tests.

## Latest Dataset Results
- Total records: 11
- Valid records: 11
- Invalid records: 0
- Duplicate sample IDs: 0
- YouTube samples: 10
- Webcam samples: 1 (Rice)
- Extracted YouTube landmark frames: 55

## Dataset Limitations
- The initial prototype contains one YouTube video per grocery label.
- Rice has one additional webcam sample.
- The YouTube sign references have not been independently verified against reliable ISL sources.
- The current dataset is suitable for testing the landmark extraction and validation pipeline, not for claiming reliable recognition accuracy.
- Extracted frames are not independent samples.

## Source Documentation
- YouTube source URLs are recorded in the metadata CSV.
- Webcam sample metadata is stored in the processed dataset.
- Vocabulary verification status remains unverified pending independent ISL review.

## Pending Work
- Verify the 10 grocery signs against reliable ISL references.
- Review the YouTube source-to-label mapping.
- Coordinate with Member 2 for recognition algorithm integration.
- Support Member 4 during backend integration if required.
- Perform final dataset validation after any further changes.

## Important
The landmark extraction, preprocessing and validation pipeline is working. The current dataset is a small prototype dataset. It should not be presented as a large or fully verified ISL training dataset.