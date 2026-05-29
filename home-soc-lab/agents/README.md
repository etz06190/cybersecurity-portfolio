# Agents

AI-assisted triage and investigation code using the Anthropic Claude API. The Phase 1 deliverable is a working triage agent that consumes Sentinel alerts and produces structured investigation reports.

## Planned components (later weeks)

- `triage/` — alert ingestion and initial classification
- `investigator/` — multi-step investigation across data sources
- `summarizer/` — incident summary generation for stakeholder reports
- `prompts/` — reusable prompt templates for triage workflows

## Phase 1 scope

- Week 1: API setup and hello-world test (done)
- Weeks 6-8: First triage prototype consuming sample alerts
- Weeks 9-12: Full pipeline integration with Sentinel webhook → agent → response
- Week 13: Public blog post on lessons learned

## Conventions

- All API keys via environment variables, never hardcoded
- Token usage logged to local file for cost tracking
- Each agent run produces a structured JSON output plus a markdown summary
- Test against historical alerts before any live deployment

## Cost discipline

- Anthropic spending limit set to $25/month in workspace settings
- Local token counter to flag runaway calls
- Use Claude Sonnet for routine triage; reserve Opus for high-severity escalation
