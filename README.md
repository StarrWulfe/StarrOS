# StarrOS

This repository is the canonical source of truth for StarrOS planning, execution, review, and delivery.

## Workflow

1. J7 authors or refines planning artifacts locally with Claude.
2. Stable artifacts are committed here immediately.
3. San reads this repo, reviews for contradictions, and generates/updates kanban work from the documented plan.
4. Wolves execute only from repo-backed tasks and attached packet files.
5. External coding workers are allowed only on approved leaf cards with explicit scope.

## Status (2026-07-09)

- Doc-canon pass: complete (PR #2 merged at `d6d0595`). Spec + 5 companion docs + cross-file normalize landed.
- Shakedown audit: complete (PR #6 merged at `d6d0595`). Dossier at `documents/audits/claude-shakedown-2026-07-09.md`.
- Multiplex target decision: complete (PR #7 merged). ADR-0004 — per-wolf gateways canonical; multiplex adoption dropped.
- Pre-Sprint-0 hardening: in flight (branch `docs/pre-sprint0-hardening`).
- Sprint 0: gated on the hardening PR landing.

## First milestones

All five closed (see `kanban/backlog.md` Epic E0):

- [x] Finalize `docs/playbook.md`
- [x] Finalize `kanban/backlog.md`
- [x] Finalize `packets/leaf-card-template.md` (incl. `report_back_channel` field)
- [x] Approve `prompts/san-handoff.md`
- [x] Let San create Sprint 0 from the backlog (gated on hardening)