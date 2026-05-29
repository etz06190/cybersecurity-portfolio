# home-soc-lab

A personal security operations lab for hands-on detection engineering, threat hunting, and incident triage. Built incrementally over 13 weeks of structured Phase 1 work, with new KQL detections, Sigma rules, and AI-assisted triage tooling added each week. This is a working portfolio — expect content to be rough early and improve as the lab matures.

## Why this exists

I'm transitioning from ERP/CRM systems administration to a security engineering role with a Blue Team specialization (SANS BS in Applied Cybersecurity). This repo is the externally visible artifact of that transition: real detections, real queries, real lab infrastructure, with the study log showing what was learned, what hurt, and what got rebuilt.

## Structure

```
home-soc-lab/
├── README.md              # this file, updated weekly
├── architecture/          # network and data flow diagrams
├── detections/            # KQL detection rules for Sentinel
├── sigma/                 # Sigma format conversions for portability
├── queries/               # KQL cookbook and threat hunting queries
├── agents/                # AI triage and investigation code
├── tools/                 # sysmon-parser and other utilities
├── blog/                  # drafts and published writeups
├── notes/                 # course notes (Sentinel Ninja, etc.)
└── study-log.md           # weekly journal: what learned, what hurt
```

## Phase 1 progress

Working through a 13-week structured Phase 1 roadmap covering Sentinel Ninja L100/L200, KQL fluency, home lab buildout (Pi sensors running Zeek + Cowrie, Sysmon on endpoint, Pi-hole DNS telemetry), AI-assisted triage agent development, and a public detection portfolio.

Current week: **Week 1 — Foundation Setup**

See [study-log.md](./study-log.md) for week-by-week progress notes.

## Stack and tools

- **SIEM:** Microsoft Sentinel (Azure free tier + Log Analytics)
- **Endpoint telemetry:** Sysmon (Olaf Hartong's modular config)
- **Network telemetry:** Zeek on Raspberry Pi (port mirror from managed switch)
- **DNS telemetry:** Pi-hole
- **Deception:** Cowrie SSH honeypot
- **Detection format:** KQL primary, Sigma for portability
- **AI tooling:** Anthropic Claude API for triage and investigation agents
- **Languages:** Python (agents, tooling), KQL (detections, queries)

## License

MIT for code in `tools/` and `agents/`. CC BY-SA 4.0 for written content in `blog/` and `notes/`. See [LICENSE](./LICENSE) for details.

## Contact

Questions or comments welcome via GitHub issues.
