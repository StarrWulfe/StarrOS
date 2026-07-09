# Example Packet: UI Preview Panel

## Metadata
- Card ID: UI-001
- Title: Build Preview panel v1
- Epic: Mission Control shell
- Owner wolf: nago
- Reviewer wolf: jigo
- Implementation mode: claude

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
