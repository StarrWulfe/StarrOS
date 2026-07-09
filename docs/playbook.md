# StarrOS Playbook

Status: v1
Owner: J7
Reviewers: San, Jigo, Ishii, Kohroku
Canonical: this file is the playbook; the canonical architecture is `specs/starros-stack-spec.md`.

## Purpose

Define how StarrOS is built end-to-end through a repo-first, kanban-driven workflow.

## Companion docs (read with this playbook)

- `specs/starros-stack-spec.md` — architecture
- `docs/runtime-state.md` — live state (what's broken right now)
- `docs/persistence-boundaries.md` — where durable state lives
- `docs/external-workers.md` — external coder workers policy
- `decisions/0003-canonical-spec-boundaries.md` — spec vs companion doc boundaries

## Core rules

- This repository is the canonical planning and execution surface (ADR 0001).
- No hidden planning artifacts are authoritative unless committed here.
- San orchestrates; wolves specialize; external coder workers implement only bounded, approved leaf cards (`docs/external-workers.md`).
- High-risk changes require explicit human approval (J7) per the destructive-op discipline in `system/j7-homelab-environment` skill.
- Every completed card must produce artifacts, logs, and a review outcome.

## Required sections (of any new playbook addendum or wolf SOP)

- Executive intent
- Wolf responsibilities
- Kanban states and transitions (link `kanban/board-schema.md`)
- Spec workflow (link `specs/starros-stack-spec.md`)
- Review/sign-off protocol (Jigo; Ishii for NixOS; J7 for destructive)
- Artifact contract (link `docs/persistence-boundaries.md`)
- Escalation rules (link `prompts/jigo-review.md`)
- Anti-patterns
- Phase-based delivery sequence (link `kanban/backlog.md`)
