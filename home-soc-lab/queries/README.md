# Queries

KQL queries for threat hunting, investigation, and routine SIEM operations. The main reference is `kql-cookbook.md` — a growing collection of queries by category.

## Files

- `kql-cookbook.md` — the main reference (start here)
- `hunting/` — ad-hoc threat hunting queries (added as situations arise)
- `investigations/` — saved queries from specific incident investigations

## How to use

Copy a query from the cookbook, paste into Sentinel Logs blade or any KQL-compatible environment, adjust time ranges and table names as needed. Most queries are written against generic Sentinel tables (SigninLogs, AzureActivity, OfficeActivity, etc.) but some assume specific custom logs (Zeek, Pi-hole) that come online in Week 5+.
