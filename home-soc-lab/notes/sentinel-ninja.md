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

# Day 11 — Sentinel Architecture, Data Collection, Analytics Rules

## Important update to my mental model

The Sentinel Ninja Training is now structured by SECURITY ROLE rather than
numbered modules. Three tracks:
1. Security Architects — workspace design, data collection, log management
2. Security Engineers — KQL, analytics rules, SOAR, workbooks
3. Analyst — threat detection, incident response, hunting

I'm pulling sections from all three tracks for Phase 1. The role boundaries
are guidance, not strict reading lists.

---

## 1. Workspace Architecture

A Log Analytics workspace is the data store; Sentinel is the security
solution running on top of one workspace.

### Key properties of a workspace

- Has a Workspace ID (GUID) and Workspace Keys (secrets for ingest)
- Lives in one Azure region (data residency boundary)
- Contains tables (AzureActivity, Heartbeat, SecurityEvent, etc.)
- Has its own billing meter (ingestion cost)
- Can host multiple solutions in parallel (Sentinel, Application
  Insights, VM Insights, etc.)

### Region matters for

- Compliance (data residency requirements)
- Query latency
- Cost (some regions priced higher)
- Feature availability (some preview features region-locked)

### Multi-workspace patterns

| Pattern | When |
|---------|------|
| Single workspace | Small orgs / home labs (my case) |
| Per-region | Compliance-driven |
| Per business unit | Isolation-driven |
| MSSP multi-tenant | Cross-customer via Azure Lighthouse |

For my home lab: single workspace `law-homesoc` in East US 2 is correct.

---

## 2. Log Management & Cost Model

### Cost structure

Sentinel cost = Log Analytics ingestion + Sentinel surcharge.
Both billed per GB ingested per day.

| Tier | Cost (approx) | Query | Sentinel features | Use case |
|------|---------------|-------|-------------------|----------|
| Analytics | ~$5.22/GB | Full KQL | All work | Security-critical data |
| Basic | ~$0.60/GB | Limited KQL | Limited | High-volume incident-only data |
| Auxiliary | ~$0.15/GB | Restore-only | None | Compliance retention |

### Retention

- Free: 31-90 days depending on table
- Paid interactive: ~$0.10/GB/month
- Max interactive: 2 years (730 days)
- Max total with archive: 12 years (4,383 days)

### Key insight

**Ingestion is expensive; retention is cheap.** Optimize by:
1. Filtering at ingest with Data Collection Rules (DCR)
2. Tiering verbose data to Basic
3. Using summary rules for pre-aggregation
4. Commitment tiers for predictable high volume
5. Workspace consolidation in enterprise scenarios

### For my home lab

- All data goes to Analytics tier (volume is low)
- Default 90-day retention is fine
- Budget alert at $25 catches anomalies
- Will revisit tiering when Sysmon (Week 4) and Zeek (Week 4-5) come
  online if volume becomes significant

---

## 3. Data Collection — Five Connector Mechanisms

| Type | Mechanism | Examples I'll use |
|------|-----------|---------------------|
| Service-to-service | Diagnostic settings via Azure Policy | Azure Activity (done) |
| Azure Monitor Agent (AMA) | Agent + Data Collection Rules | Sysmon (Week 4) |
| Codeless Connector Framework (CCF) | YAML-defined SaaS connectors | M365 Defender, partner products |
| Logs Ingestion API | Direct REST API | Pi-hole, Zeek, Cowrie (Weeks 3-5) |
| Syslog/CEF | Network appliance forwarding via AMA | Not in Phase 1 |

### Deprecations to know

- **MMA (legacy Microsoft Monitoring Agent):** fully deprecated August 2024
- **HTTP Data Collector API:** deprecated September 14, 2026 — use Logs
  Ingestion API instead

Both of these matter for Phase 1 — I'll use AMA (not MMA) and Logs
Ingestion API (not HTTP Data Collector) when building custom integrations.

---

## 4. ASIM — Advanced Security Information Model

### The problem ASIM solves

Every log source uses different column names for the same concept:
- Windows DNS: `QueryName`
- Cisco Umbrella: `Domain`
- Pi-hole: `query`
- Some firewall: `dns_query_name`

Without normalization, I'd need 5 different detection rules to detect
"DNS lookup to a known-bad domain." With ASIM, one rule covers all sources.

### How ASIM works

1. Microsoft defines **standard schemas** for common security domains
2. Each schema specifies column names and types (e.g., `DnsQuery`,
   `SrcIpAddr`, `DstIpAddr`, `EventResult`)
3. **Parsers** translate raw data from a source into the standard schema
4. **Union parsers** combine multiple source parsers into one queryable
   interface

### Standard schemas relevant to my Phase 1

| Schema | What it normalizes | My future source |
|--------|---------------------|-------------------|
| ASim_Dns | DNS query/response logs | Pi-hole (Week 3) |
| ASim_NetworkSession | Connection-level network logs | Zeek (Week 4-5) |
| ASim_AuditEvent | Administrative actions | Azure Activity (done), Sysmon |
| ASim_Authentication | Sign-in events | M365 (Week 3 if added) |
| ASim_ProcessEvent | Process creation/termination | Sysmon (Week 4) |
| ASim_FileEvent | File creation/modification/deletion | Sysmon (Week 4) |
| ASim_RegistryEvent | Windows registry modifications | Sysmon (Week 4) |

### Trade-offs

- Pro: One detection rule covers multiple sources
- Pro: Easy to swap data sources (Pi-hole → Umbrella) without changing detections
- Con: Parse overhead at query time
- Con: Some fields don't map cleanly — information lost

---

## 5. Data Transformation (Data Collection Rules at ingest)

DCRs can filter, enrich, and project data BEFORE it hits the workspace.

### Three transformation types

1. **Filtering** — drop records (debug logs, health pings, known noise).
   Pay only for what lands in the workspace.
2. **Enrichment** — add computed fields (environment, business unit).
3. **Projection** — keep only needed columns.

### Impact

Well-designed DCRs can cut cost 50-80% on high-volume sources.
Example: Windows Security event 4624 fires constantly during normal
operations — a DCR can drop system account logons and keep only
interactive user logons.

### For my Phase 1

- No DCR on Azure Activity (already lean)
- Will design DCRs for Sysmon (Week 4) and Pi-hole (Week 3) when their
  volumes are visible

---

## 6. Analytics Rules — The Four Types

| Type | Frequency | What it is | Phase 1 relevance |
|------|-----------|------------|---------------------|
| Scheduled | 5min-14d | KQL on a timer | 90% of what I'll write |
| NRT (Near-Real-Time) | ~1 min | Lower latency, single-table | High-priority detections |
| Microsoft Security | Continuous | Pre-built by Microsoft | Enable for free coverage |
| Fusion | Continuous | ML-based correlation | Just enable; no authoring |

### When to use NRT vs Scheduled

Use NRT if a 5-minute delay matters (executive account compromise,
privilege escalation, data exfiltration in progress). Otherwise
Scheduled is more flexible.

---

## 7. The Detection Lifecycle
### Step-by-step

1. Rule runs on schedule against the workspace
2. If query returns rows, each row becomes an alert with metadata
3. Alerts get grouped into incidents (by entity, time, custom logic)
4. Incidents have severity, status, owner, linked entities
5. Automation rules can fire on incident creation
6. Analyst triages incident with the investigation graph for pivoting

---

## 8. Entity Mapping — Required for Every Rule

Map query output columns to entity types so Sentinel knows what each
column represents.

### Common entity types

- **Account** — user (UPN, SID, email)
- **Host** — computer or server name
- **IP** — IP address
- **File** — filename + optional hash
- **Process** — process name + PID
- **URL** — full URL
- **CloudApplication** — SaaS app identity
- **DnsResolution** — DNS query/answer

### Why entity mapping matters

1. **Investigation graph** — visual pivot through incident's entities and connections
2. **Cross-rule correlation** — connect alerts that share entities
3. **UEBA scoring** — risk profiles per user/host
4. **Threat intel matching** — IPs/domains auto-checked against TI feeds
5. **Investigation context** — analysts pivot from entity to all related events

**Skipping entity mapping makes rules technically work but eliminates
most investigation value. Always map entities.**

---

## 9. MITRE ATT&CK Tagging — Non-Negotiable

Every rule should be tagged with:
- **Tactic** — attacker goal (Initial Access, Execution, Persistence, etc.)
- **Technique** — specific method (e.g., T1078 Valid Accounts, T1110 Brute Force)
- **Sub-technique** — when applicable (T1110.001 Password Guessing)

### Why it matters

Sentinel's MITRE coverage view shows:
- Which techniques my rules detect
- Which techniques have NO coverage (gaps)
- Which techniques have multiple rules (potentially redundant)

Modern detection engineering requires this. Hiring managers ask about
MITRE coverage. Without tagging, I can't answer.

---

## 10. Severity Guidance

Severity = confidence × impact

| Severity | Meaning |
|----------|---------|
| Informational | Visibility only, no action |
| Low | Triage at convenience |
| Medium | Triage promptly during business hours |
| High | Triage immediately |

### Trade-offs

- High confidence + high impact = High severity
- Low confidence + high impact = Medium (might be FP, but investigate fast if real)
- High confidence + low impact = Low or Medium
- Low confidence + low impact = don't write the rule

---

## 11. Suppression and Grouping

### Suppression

Stops a rule from firing for N hours after it fires once. Useful for:
- Detections that should alert once per incident, not continuously
- Reducing alert fatigue from chatty rules

### Grouping

Combines multiple alerts into one incident. Without grouping, a
brute-force attack might generate 100 separate alerts. With grouping
by username, those 100 alerts become 1 incident.

Both essential for managing alert volume in production.

---

## 12. The Analyst Perspective (receiving end)

I'll be writing rules in Phase 1, not working as an analyst — but
understanding the analyst experience makes me a better rule author.

### What analysts do with the rules I write

- Work the **Incidents queue** as their primary interface
- Use the **investigation graph** for visual pivoting through entities
- Run **hunting queries** to find things detections might miss
- Use **threat intel matching** for auto-enrichment of incidents
- Use **workbooks** for dashboards and SOC metrics

### What makes a "good" rule from the analyst's perspective

- Clear title and description (the analyst can understand without context)
- Appropriate severity (not crying wolf, not missing real threats)
- Entity mapping for investigation pivoting
- MITRE tagging for coverage measurement
- Reasonable suppression to avoid alert fatigue
- Few false positives, or auto-close logic via automation rules

A rule that fires constantly without actionable context wastes analyst
time. A rule with good entity mapping and clear descriptions saves it.

---

## 13. Cross-Cutting Concepts

### The Defender XDR transition

By March 31, 2027, Sentinel migrates fully into the Defender portal.
The unified SOC platform combines SIEM (Sentinel) and XDR (Defender XDR).
For new deployments, this is the default architecture. My Phase 1 work
should consider this — the unified portal is where modern SOC operations
happen.

### Attack Disruption

Automated containment of high-confidence alerts. Sentinel + Defender XDR
can automatically isolate compromised users or devices. Worth knowing
exists for future investigation work.

### SOC Optimization

Microsoft's recommendation engine that analyzes my workspace and
suggests connectors to enable, rules to turn on, coverage gaps. Worth
checking periodically once I have more data sources.

### Summary rules

Pre-aggregate verbose data into smaller summary tables. Detections
query the small summary instead of the full firehose. Becomes relevant
once I have high-volume sources like Zeek.

### Sentinel Data Lake (2025+)

New architecture that decouples storage from compute. Cheap data lake
storage holds everything; on-demand compute spins up for queries.
Bleeding edge as of 2026 — not for Phase 1, but the direction Microsoft
is going.

---

## Open Questions to Revisit

- When does NRT make sense vs. Scheduled at 5-min intervals? Similar
  latency in practice — what's the operational difference beyond
  query complexity limits?
- How does ASIM normalization interact with my custom Pi-hole/Zeek
  forwarders? Do I write parsers myself, use existing community ones,
  or skip ASIM for custom sources?
- What's the realistic volume difference between Basic and Auxiliary
  tiers for my home lab? Is Basic worth the complexity for Sysmon noise?
- When does it make sense to use Summary Rules to pre-aggregate?
- How does Sentinel Data Lake (2025+) change the architecture? Is it
  worth restructuring my home lab to use it, or wait for Phase 2?
- Are there default Sentinel tables that consume cost I can't control
  (e.g., Heartbeat, AzureMetrics)?

---

## Key Takeaways for Phase 1

1. **One workspace is the right architecture for my home lab.**
   Multi-workspace is for enterprise scenarios that don't apply.

2. **Cost is driven by GB ingested per day.** Optimize via DCR filtering,
   not by avoiding features.

3. **Five connector mechanisms exist** — I'll use service-to-service
   (done), AMA (Week 4 Sysmon), Logs Ingestion API (Weeks 3-5 custom
   sources).

4. **ASIM lets one detection cover many sources.** Use it where parsers
   exist; consider for custom sources in Week 5+.

5. **Analytics Rules are the deliverable.** Scheduled rules are 90% of
   the work. Every rule needs entity mapping + MITRE tagging.

6. **MMA is dead. HTTP Data Collector dies Sept 2026.** Build on AMA
   and Logs Ingestion API only.

7. **The Defender XDR portal is the future.** By 2027, Sentinel lives
   there exclusively. Build a mental model that fits the unified platform.

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
