# Workflow

## Recommended sequence

1. Draft planning artifacts locally with Claude.
2. Commit stable revisions to this repo (ADR 0001).
3. Ask San to review the committed artifacts and convert them into execution-ready work (`kanban/board-schema.md`).
4. Allow wolves to expand cards only within the documented scope.
5. Use external coder workers (Claude Code, OpenCode, Kilocode, Gemini, Copilot) on Mononoke **only** for bounded, approved leaf cards — see `docs/external-workers.md` for the full policy.
6. Jigo reviews per the reviewer's lens (`prompts/jigo-review.md`).
7. Ishii reviews any change touching `/etc/nixos/nix/services/`.
8. J7 signs off on destructive operations (destructive-op discipline).
9. After merge, the spec (if changed) and `docs/runtime-state.md` are updated in the same PR.
