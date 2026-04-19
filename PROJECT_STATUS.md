# Project Status

INAV PID Tuner is a prototype Blackbox-log analysis tool for INAV tuning.

## Available In This Repository

- FastAPI upload endpoint.
- Blackbox decoding wrapper using `blackbox_decode`.
- PID error, D-term noise, and gyro-noise metric extraction.
- Rule-based PID/filter recommendation logic.
- Simple browser UI.

## Validation Status

Treat the recommendations as tuning guidance, not as automatic settings to apply
blindly. Review every CLI suggestion, make small changes, and verify with
another flight log.

## Review Needed

- More example logs from different aircraft.
- Better thresholds for different frame sizes and aircraft types.
- Safer recommendation wording.
- UI improvements for comparing before/after logs.

## Safety

Bad PID or filter settings can make an aircraft unstable. Apply changes slowly,
test in safe conditions, and keep a known-good configuration backup.

