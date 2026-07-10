# Example Packet: UI Preview Panel

> **HISTORICAL — Mission Control paused** (J7 2026-07-09). This packet was authored against the Mission Control app paths, which are paused. Kept for the packet-shape exemplar; do not copy verbatim. See `kanban/backlog.md` E3-T3 for revival.

## Metadata
- Card ID: UI-001
- Title: Build Preview panel v1
- Epic: Mission Control shell (paused)
- Owner wolf: nago
- Reviewer wolf: jigo
- Implementation mode: claude
- **Report-back channel:** `card.report_back_channel` (per `docs/external-workers.md` §6)

## Goal
Build the initial Preview panel surface for viewing generated artifacts.

## Allowed paths
- apps/mission-control/src/panels/preview/**

## Forbidden paths
- apps/mission-control/src/auth/**
- infra/**

## Acceptance criteria
- Renders placeholder preview states
- Supports markdown/html/image placeholder modes
- Has tests for state switching
