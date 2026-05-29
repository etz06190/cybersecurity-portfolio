# Architecture

Network and data flow diagrams for the home SOC lab. Each diagram is committed as both source (draw.io XML) and rendered PNG.

## Files

- `current-state.png` — home network before the lab buildout
- `current-state.drawio` — editable source
- `target-state.png` — final Phase 1 architecture with managed switch, port mirror, two Pis, and Sentinel telemetry forwarding
- `target-state.drawio` — editable source
- `data-flows.png` — telemetry sources to Sentinel pipeline (added Week 5)

## Conventions

- Use draw.io (or diagrams.net) for editable diagrams
- Export PNG at 2x resolution for retina/HDPI displays
- Update diagrams whenever the lab topology changes
- Keep a brief diff note in the commit message describing what changed

## Diagram update history

- Week 1: initial current-state and target-state diagrams
- (subsequent updates logged as diagrams change)
