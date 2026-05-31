# Sentinel Ninja Notes

Personal notes from working through the Microsoft Sentinel Ninja Training.

Source: https://aka.ms/SentinelNinjaTraining (redirects to the current Microsoft Community Hub page).

These are not transcription. They capture:
- Things that surprised me
- Concepts I'll forget without writing them down
- Cross-references back to my own work
- Confusion points to revisit

---

## Introduction / Overview

The Sentinel platform is structured around four pillars:

### 1. Data Collection
Use data connectors to start ingesting your data into Microsoft Sentinel.
- Out-of-the-box data connectors
- Custom connectors
- Data normalization

### 2. Detect Threats
Detect previously undetected threats and minimize false positives using Microsoft's analytics and threat intelligence.
- Analytics — detect threats out-of-the-box
- MITRE ATT&CK coverage — understand security coverage by the framework
- Threat intelligence
- Watchlists
- Workbooks — visualize collected data

### 3. Investigate Threats
Investigate threats with AI and hunt for suspicious activities at scale.
- Incidents — navigate and investigate incidents
- Hunts — threat hunting
- Notebooks — Jupyter notebooks with Sentinel hunting capabilities

### 4. Respond to Incidents Rapidly
- Automation rules — automate threat response
- Playbooks — automate threat response with playbooks

### Significant platform change
After March 31, 2027, Microsoft Sentinel will no longer be supported in the Azure portal and will be available only in the Microsoft Defender portal.

---

### Things to remember

- The 4-pillar model (Collect → Detect → Investigate → Respond) applies to ALL SIEMs, not just Sentinel
- After March 31, 2027, Sentinel moves entirely to Defender portal — Azure portal access ends
- MITRE ATT&CK mapping is non-negotiable for modern detection engineering
- ASIM (Advanced Security Information Model) is Microsoft's data normalization layer — write one detection, works across multiple sources
- Three categories of detection in Sentinel: Analytics rules (scheduled KQL), Microsoft Security (pre-built), ML-based (Fusion + UEBA)

### Open questions

- How exactly does ASIM work when ingesting Pi-hole / Zeek custom data? (Week 5 problem)
- What's the difference between Hunts and scheduled Analytics rules — both run KQL?
- When does it make sense to use Notebooks vs Workbooks for visualization?
- What automation playbook would be useful for a home lab vs being overkill?

---

## Template for future sections

```markdown
## Section name

(notes here as I work through the section)

### Things that surprised me

### Things to remember

### Open questions

### Cross-references

- Related detection in detections/: ...
- Related cookbook query: ...
```
