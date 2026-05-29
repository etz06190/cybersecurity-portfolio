# Detections

KQL detection rules for Microsoft Sentinel. Each rule is its own file with metadata, the query, deployment notes, and a brief threat model.

## Structure

Each detection file follows this template:

```kql
// Detection: Brief descriptive title
// Author: Eric Torzuoli
// Created: YYYY-MM-DD
// MITRE ATT&CK: Txxxx.xxx (technique ID + name)
// Severity: Low | Medium | High | Critical
// Data sources: Table1, Table2
//
// What it detects:
//   One-paragraph description of the threat and how the query catches it.
//
// False positive scenarios:
//   - Scenario 1
//   - Scenario 2
//
// Tuning notes:
//   How to adapt thresholds, allowlists, etc.

<KQL query here>
```

## Naming convention

`category-shortname.kql`, lowercased, dashes not underscores.

Examples:
- `auth-impossible-travel.kql`
- `persistence-scheduled-task-creation.kql`
- `exfil-large-data-egress.kql`

## Categories

- `auth-` — authentication and identity
- `persistence-` — persistence mechanisms
- `lateral-` — lateral movement
- `exfil-` — exfiltration
- `cmd-` — command and control
- `recon-` — reconnaissance
- `defense-` — defense evasion
- `priv-` — privilege escalation

## Status

No detections yet. First detection target: Week 5 of Phase 1.
