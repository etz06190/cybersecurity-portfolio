# Phase 1 Roadmap

13-week structured plan for building the home SOC lab. Acceptance criteria below match the detailed roadmap document.

Use this file as a quick reference. The lived progress (what was hard, what surprised you) lives in `study-log.md`.

---

## Week 1 — Foundation Setup (8 hours)

**Mission:** Get every account, every order, and every infrastructure piece initiated so nothing bottlenecks later weeks.

- [ ] GitHub repo `home-soc-lab` exists with directory structure and README
- [ ] Azure free trial active, Sentinel workspace `law-homesoc` created
- [ ] $25/month budget alert set on `rg-homesoc-eastus`
- [ ] Anthropic API key working, $25/month spending limit set
- [ ] Sentinel Ninja L100 Module 1 complete
- [ ] All hardware ordered with delivery dates noted
- [ ] Current and target network architecture diagrams committed
- [ ] Tracking board has Weeks 2-13 stubbed with acceptance criteria

---

## Week 2 — Sentinel Fundamentals + KQL Basics (10 hours)

**Mission:** Build core Sentinel knowledge through the current Ninja Training, get comfortable with basic KQL, connect Azure Activity Logs as your first data source, get both Raspberry Pis on the network.

### Sentinel learning (3-4 hours)
- [ ] Ninja Training: complete the "Onboard Microsoft Sentinel" section
- [ ] Ninja Training: complete the "Collect data" section
- [ ] Ninja Training: complete the introduction to "Threat detection" / Analytics rules
- [ ] Notes captured in `notes/sentinel-ninja.md`

### KQL practice (3-4 hours)
- [ ] Complete Microsoft Learn path: "Write your first query with Kusto Query Language"
- [ ] 20+ KQL queries documented in `queries/kql-cookbook.md` covering:
  - `where`, `project`, `summarize`, `count`, `take`, `top` (basics)
  - `bin()`, `ago()`, `between()`, `render timechart` (time-based)
  - `extend`, `parse`, `parse_json` (parsing)
  - Basic `join` and `let` patterns

### Sentinel data connection (1-2 hours)
- [ ] Azure Activity logs connector enabled in Sentinel
- [ ] Data verified flowing: `AzureActivity | take 10` returns rows
- [ ] At least 2 cookbook queries reference real `AzureActivity` data

### Pi setup (2 hours)
- [ ] Both Pi 4s booted and on home network
- [ ] Static IP addresses assigned (.50 for sensor Pi, .51 for utility Pi)
- [ ] SSH key auth working (password auth disabled)
- [ ] OS fully updated
- [ ] Hostnames set: `pi-sensor` and `pi-utility`
- [ ] Architecture diagram updated with actual IPs

### NOTE on roadmap translation
The original roadmap referenced "L100 Module 1-4" structure from the older
Sentinel Ninja Training (pre-October 2024). Microsoft has since reorganized
into a single role-based blog at aka.ms/SentinelNinjaTraining. This week's
acceptance criteria map the original intent to current Microsoft content.


## Week 3 — Sentinel Ninja L1 Complete + Pi-hole (10 hours)

**Mission:** Finish Sentinel Ninja L100, level up KQL, connect M365 logs, deploy Pi-hole.

- [ ] Sentinel Ninja L100 complete
- [ ] M365 logs flowing into Sentinel (OfficeActivity table verified)
- [ ] 30+ KQL queries in cookbook (with `join`, `let`, `parse`)
- [ ] Pi-hole operational on Pi 2 with web UI accessible
- [ ] Home router using Pi-hole as primary DNS

---

## Week 4 — Managed Switch + Pi Network Sensor (10 hours)

**Mission:** Insert managed switch, configure port mirroring, deploy Zeek on Pi 1, install Sysmon on home Windows PC.

- [ ] Managed switch inserted into network, port mirroring configured
- [ ] Zeek capturing traffic on Pi 1
- [ ] Sysmon installed on home Windows PC with Olaf Hartong's config
- [ ] (To be expanded from full roadmap)

---

## Week 5 — Telemetry Forwarding to Sentinel (12 hours)

**Mission:** Forward Sysmon, Zeek, and Pi-hole telemetry to Sentinel; write first detections.

- [ ] All three telemetry sources flowing to Sentinel custom tables
- [ ] First 2-3 detection rules in `detections/`
- [ ] Sigma conversions in `sigma/`
- [ ] (To be expanded from full roadmap)

---

## Weeks 6-12

(Acceptance criteria to be filled in from the detailed roadmap as you reach each week)

---

## Week 13 — Phase 1 Wrap (8 hours)

**Mission:** Public blog post, portfolio review, Phase 2 prep.

- [ ] Headline blog post published
- [ ] README.md updated with final Phase 1 state
- [ ] Lessons learned documented in study-log.md
- [ ] Phase 2 plan drafted

---

## Background track (continuous, 2-3 hrs/week)

Hardware and OS internals work running in parallel with the primary track:

- [ ] CS:APP reading progress (target: chapters 1-5 by end of Phase 1)
- [ ] GDB practice (small C programs, examining memory)
- [ ] Occasional Raspberry Pi Pico exercises
