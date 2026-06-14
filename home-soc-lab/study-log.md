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
### Day 9 — Azure Activity Connector

Status: Complete. AzureActivity table populating with real subscription activity.

What I did:
1. Located the Azure Activity connector via Sentinel → Data connectors →
   Content hub → Azure Activity (the Status filter on the Data Connectors
   list was stuck and wouldn't show unconnected connectors).
2. Launched Azure Policy Assignment wizard with subscription scope and
   law-homesoc as the target workspace.
3. First remediation failed: Microsoft.PolicyInsights resource provider
   not registered. Fixed by registering it in Subscriptions → Resource
   providers. Also registered Microsoft.Insights to be safe.
4. Triggered new remediation. Policy compliance dashboard showed
   non-compliant / pending for a while, but the actual diagnostic setting
   (named subscriptionToLa) was created at the subscription level and is
   forwarding all 8 categories to law-homesoc.
5. Verified end-to-end: AzureActivity | take 50 returns rows with real
   subscription activity including policy evaluations and resource
   deployments.

Key learnings:
- Azure resource providers must be explicitly registered per subscription
  before their features become available. PolicyInsights is required for
  any policy remediation task. This is a one-time setup gotcha.
- Policy compliance dashboards lag behind actual configuration state by
  ~30 minutes. When troubleshooting, check the underlying mechanism
  (diagnostic settings page) for ground truth, not the abstraction layer
  (compliance scores).
- Sentinel's Data Connectors UI has a stuck Status filter bug. Content
  Hub is the working alternative path to install/configure connectors in
  2026.
- Log ingestion is not real-time. Even after configuration succeeds, data
  takes 10-30 minutes to appear in queries. Critical operational knowledge
  for detection engineering.

Time spent: ~2 hours including troubleshooting (vs 1 hour planned).


### Day 11 — Sentinel Ninja Training: Architecture, Data Collection, Analytics Rules

Status: Complete.

What I learned:
- The current Ninja Training is role-based (Architect / Engineer / Analyst),
  not module-based — adapted my reading to pull from all three tracks
- Five connector mechanisms in 2026: service-to-service, AMA, CCF,
  Logs Ingestion API, Syslog/CEF
- Three storage tiers with different cost/query trade-offs
- ASIM normalizes log sources into common schemas so one detection
  covers many sources
- Four analytics rule types: Scheduled (90% of my work), NRT, Microsoft
  Security, Fusion
- Entity mapping + MITRE tagging are non-negotiable for every rule
- Defender XDR portal is the future — Sentinel migrates there by March 2027

Key insight:
Cost optimization in Sentinel is mostly about filtering at ingest with
DCRs. Ingestion is expensive; retention is cheap. The architectural
choices that matter most are connector types and tier placement.

Time spent: ~1.5 hours.

Next: Day 12 — Pi imaging.---
### pi1-sensor: complete

Status: Operational. ssh pi1-sensor works from WSL with key auth.

Final configuration:
- Hostname: pi1-sensor
- IP: 192.168.1.50 (static via nmcli; outside AT&T DHCP pool)
- OS: Pi OS Lite 64-bit Bookworm, kernel 6.18.33
- Network: Ethernet only, WiFi disabled
- SSH: id_ed25519 key auth via ~/.ssh/config alias

Friction overcome along the way:
- Underpowered USB-C supply caused red-green-red boot failures; swapped to proper 5V/3A
- WSL2 doesn't resolve .local hostnames via mDNS
- AT&T router DHCP pool starts at .64, so .50 is in the static range
- WSL2 regenerates /etc/hosts on restart; switched to ~/.ssh/config which survives
- SSH keys were in WSL the whole time (id_ed25519), I just had to find them

Time invested: ~5 hours across sessions

Next: pi2-services imaging using the same workflow
### pi2-services: setup complete

Status: Fully operational with static IP and persistent SSH access.
Hardware prerequisite for Week 3 Pi-hole deploy, completed early.

Final state:
- Hostname: pi2-services (corrected from mis-imaged pi2-sensor)
- IP: 192.168.1.51 (static, via NetworkManager on the Pi, below the
  AT&T DHCP pool start of .64 so no conflict possible)
- Gateway: 192.168.1.254 (confirmed via `ip route | grep default`)
- OS: Pi OS Lite 64-bit Bookworm
- Connection profile: netplan-eth0 (netplan-generated NM profile,
  same name as pi1 since identical hardware/onboard eth0)
- WiFi: disabled persistently via `sudo nmcli radio wifi off`
- SSH: ED25519 key auth working from laptop, no password required
- SSH alias: pi2-services already present in ~/.ssh/config, points to .51
- Persistence: confirmed surviving `wsl --shutdown` restart

Friction overcome:
- Imaged with wrong hostname (pi2-sensor). Fixed with
  `sudo hostnamectl set-hostname pi2-services`.
- /etc/hosts still pinned the old name on the 127.0.1.1 line
  (duplicated: "pi2-sensor pi2-sensor"). Caused "sudo: unable to
  resolve host" warning on every sudo. Fixed by editing to pi2-services.
- Public key was NOT injected at imaging, so key auth failed and
  fell back to password. Fixed with
  `ssh-copy-id -i ~/.ssh/id_ed25519.pub pi2-services`.
- WSL2 still cannot resolve .local mDNS, so reached the Pi at its
  DHCP address (192.168.1.129) first, set static, then used the
  ~/.ssh/config alias.

Static IP command used:
  sudo nmcli connection modify "netplan-eth0" \
    ipv4.method manual \
    ipv4.addresses 192.168.1.51/24 \
    ipv4.gateway 192.168.1.254 \
    ipv4.dns "192.168.1.254"

Reachable via: ssh pi2-services

Carry-forward notes for Week 3 Pi-hole install:
- Use `ssh pi2-services` not pi2-services.local (WSL mDNS limitation).
- Verify admin UI at http://192.168.1.51/admin not the .local name.
- DNS resilience decision still open: sole resolver with tested
  rollback (clean telemetry) vs secondary DNS on router (leaks
  queries, blinds logging). Secondary-DNS "backup" is a trap for a
  telemetry-focused build.

Still open (Day 13 hardening, both Pis):
- Disable SSH password auth (PasswordAuthentication no) now that key
  auth is confirmed. pi2 proved it still accepts passwords, which is
  exactly what should be turned off.

Next: pi1/pi2 password-auth hardening, then Week 3 (Sentinel Ninja
L100, KQL intermediate, M365 connector, Pi-hole deploy).
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
