# Example Packet: Backend Kanban Adapter

## Metadata
- Card ID: API-001
- Title: Build kanban adapter endpoint
- Epic: Data and orchestration
- Owner wolf: okkoto
- Reviewer wolf: ishii
- Implementation mode: claude

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
