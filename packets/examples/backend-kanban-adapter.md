# Example Packet: Backend Kanban Adapter

> **HISTORICAL — Mission Control paused** (J7 2026-07-09). This packet was authored against the Mission Control app paths, which are paused. Kept for the packet-shape exemplar; do not copy verbatim. See `kanban/backlog.md` E3-T3 for revival.

## Metadata
- Card ID: API-001
- Title: Build kanban adapter endpoint
- Epic: Data and orchestration (Mission Control adjacent — paused)
- Owner wolf: okkoto
- Reviewer wolf: ishii
- Implementation mode: claude
- **Report-back channel:** `card.report_back_channel` (per `docs/external-workers.md` §6)

## Goal
Expose a bounded backend endpoint that reads seeded kanban data for Mission Control.

## Allowed paths
- apps/mission-control-api/**

## Forbidden paths
- nix/**
- secrets/**
- auth/**

## Acceptance criteria
- Endpoint returns seeded board data
- Tests cover success and malformed-card cases
- No changes outside allowed paths