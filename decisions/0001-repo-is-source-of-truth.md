# ADR 0001: Repo is the source of truth

Date: 2026-07-08
Status: Accepted

## Decision

Forgejo is the canonical source of truth for StarrOS planning and execution artifacts.

## Consequences

- Laptop Claude sessions are drafting environments, not authoritative storage.
- If an artifact matters, it must be committed here.
- San and the wolves operate from repo-backed artifacts, not private chat history.
