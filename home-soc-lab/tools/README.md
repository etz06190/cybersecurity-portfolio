# Tools

Utility scripts for the home SOC lab. Things that don't belong in detections or agents but support the overall workflow.

## Planned tools

- `sysmon-parser/` — convert Sysmon Event Logs to clean JSON for Sentinel ingestion
- `log-shipper/` — Pi → Sentinel forwarder configs and helpers
- `cost-monitor/` — query Azure cost API and alert on unexpected spend
- `setup/` — one-off setup scripts (Pi configuration, Sentinel workspace bootstrap)

## Conventions

- Python for general utilities; shell for setup scripts
- Each tool has its own subdirectory with its own README explaining purpose and usage
- All tools work with environment variables for credentials, never hardcoded secrets
- Where applicable, include a `requirements.txt` for Python dependencies
