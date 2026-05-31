# Study Log

Weekly notes on the Phase 1 buildout. Honest about what worked, what didn't, and what I'd do differently. Not transcription of course content — that lives in `notes/`. This is reflection: what surprised me, what I'm still confused about, where I lost time.

Format: one section per week. Most recent week at the top.

---

## Week 1 — Foundation Setup

**Date range:** TBD
**Hours spent:** TBD / 8 budgeted

### What got done

- [x] GitHub repo created with directory structure
- [x] Azure free trial active, Sentinel workspace `law-homesoc` created in East US 2
- [x] Cost Management budget alert at $25/month on `rg-homesoc-eastus`
- [x] Anthropic API key working, spending limit set to $25/month
- [ ] Sentinel Ninja L100 Module 1 complete
- [ ] Hardware ordered (GS308E switch, USB-Ethernet, SSD, cables, SD cards)
- [ ] Current and target network architecture diagrams committed
- [ ] Phase 1 tracking board has Weeks 2-13 stubbed with acceptance criteria

### What surprised me

(fill in as you go)

### What I'm still confused about

(fill in as you go)

### Where I lost time

(fill in as you go)

### Next week's focus

Week 2: Sentinel Ninja L100 first half, KQL basics, Azure Activity Logs connector, Pi OS imaging.

---


### Day 4 — Sentinel Ninja Training: Introduction

**Status:** Complete. Section: Introduction + Overview.

**What I learned:**
- Sentinel structured around 4 pillars: Collect, Detect, Investigate, Respond
- This 4-pillar model is universal across SIEMs (Splunk, Elastic, QRadar, etc.)
- MITRE ATT&CK mapping is mandatory for modern detection engineering
- ASIM is Microsoft's data normalization layer — important for Week 5 custom connectors
- Significant: After March 31, 2027 Sentinel migrates entirely to Defender portal

**What surprised me:**
The Ninja Training was reorganized in late 2024 — it's now a single
role-based blog rather than discrete modules. Mapped "Module 1" to the
current Introduction section. Going forward, will use security-role-based
filtering and proceed in section order.

**Open questions raised:**
- How ASIM handles custom data sources like Pi-hole / Zeek (Week 5 problem)
- Hunts vs Analytics rules — both run KQL, what's the operational difference?
- When to use Notebooks vs Workbooks for analysis

**Time spent:** ~1 hour

**Next:** Day 5 — order hardware for the lab buildout.

---

## Template for future weeks

```markdown
## Week N — [Topic]

**Date range:** YYYY-MM-DD to YYYY-MM-DD
**Hours spent:** X / Y budgeted

### What got done

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

### What surprised me

### What I'm still confused about

### Where I lost time

### Next week's focus
```
