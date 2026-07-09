# StarrOS

This repository is the canonical source of truth for StarrOS planning, execution, review, and delivery.

## Workflow

1. J7 authors or refines planning artifacts locally with Claude.
2. Stable artifacts are committed here immediately.
3. San reads this repo, reviews for contradictions, and generates/updates kanban work from the documented plan.
4. Wolves execute only from repo-backed tasks and attached packet files.
5. External coding workers are allowed only on approved leaf cards with explicit scope.

## First milestones

- Finalize `docs/playbook.md`
- Finalize `kanban/backlog.md`
- Finalize `packets/leaf-card-template.md`
- Approve `prompts/san-handoff.md`
- Let San create Sprint 0 from the backlog
