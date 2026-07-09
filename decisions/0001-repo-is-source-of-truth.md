# ADR 0001: Repo is the source of truth

Date: 2026-07-08
Status: Accepted
Related: ADR 0003 (canonical spec boundaries)

## Decision

Forgejo `j7/StarrOS` is the canonical source of truth for StarrOS planning and execution artifacts. The repo's `docs/`, `specs/`, `kanban/`, `packets/`, `prompts/`, and `decisions/` trees are authoritative; the canonical architecture lives in `specs/`, while `docs/` carries operational and policy docs (see `decisions/0003`).

## Consequences

- Laptop Claude sessions are drafting environments, not authoritative storage.
- If an artifact matters, it must be committed here.
- San and the wolves operate from repo-backed artifacts, not private chat history.
- `docs/runtime-state.md` is a deliberate exception: it is the only canonical doc that is expected to be rewritten weekly; supersedes itself rather than accreting.
- All architectural decisions go in `decisions/000N-*.md` as ADRs.
