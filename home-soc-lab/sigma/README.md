# Sigma

Sigma format conversions of the KQL detections in `../detections/`. Sigma is a vendor-neutral detection format that can be converted to KQL, Splunk SPL, Elastic EQL, or other SIEM languages.

## Why both KQL and Sigma

Primary detections are written in KQL (because Sentinel is the home SIEM), but Sigma versions make the detection logic portable. Future employers using Splunk or Elastic can still benefit from the detection.

## Conversion workflow

1. Author the detection in KQL first (in `../detections/`)
2. Manually port the core logic to Sigma YAML here
3. Use sigmac or pysigma to validate and round-trip back to KQL
4. Note any logic that didn't translate cleanly in a comment

## File format

`category-shortname.yml` matching the KQL filename.

## Status

No conversions yet. Will populate as detections are authored in Week 5+.
