# External Coder Workers

> **Purpose:** policy for using CLI-based external coder workers (Claude Code, OpenCode, Kilocode, Gemini, Copilot) within StarrOS. **External coder workers are not agents; they are bounded leaf-card implementers.**
> **Owner:** Okkoto (operator + skill gate) + Jigo (reviewer) + J7 (escalation).
> **Source-of-truth:** this file is canonical for the policy; per-leaf-card scope lives in the card's packet.

## 1. Approved tools (in scope)

| Tool | Path | Status |
|---|---|---|
| OpenCode | `/run/current-system/sw/bin/opencode` | installed (Phase P6) |
| Kilocode-cli | `/run/current-system/sw/bin/kilocode` | installed (Phase P6) |
| Gemini-cli | `/run/current-system/sw/bin/gemini` | installed (Phase P6) |
| Copilot-cli | `/run/current-system/sw/bin/copilot` | installed (Phase P6) |
| Claude Code | not yet installed | **Phase P6 to add** |

These are the only 5 external coder workers in scope as of 2026-07-09. Adding a 6th requires an ADR.

## 2. When external coder workers may be used

- **Allowed**: a card in `ready-for-implementation` or `in-external-implementation` state with a complete `packets/leaf-card-template.md` packet attached.
- **Allowed scope**: exactly the `allowed_paths` in the packet.
- **Required mode**: the leaf card's `implementation_mode` field is `claude` (or the appropriate tool name).
- **Required authority**: the wolf named in the card's `owner_wolf` field is the operator who launches the worker.
- **Required review**: Jigo (per `jigo-review` skill §0.5 config-first mandate) before merge.

## 3. When external coder workers may NOT be used

- **Never** on architecture decisions (San, Ashitaka, J7, or the relevant charter-owner wolf only).
- **Never** on `/etc/nixos/nix/services/` modules (Ishii only; full wolfpack review required).
- **Never** on secret material (BSM tokens, agenix keys, `.env`).
- **Never** on ADR or canonical-spec content (San or J7 only).
- **Never** on a card whose `implementation_mode` is not `claude` (or other approved external tool) — wolves handle non-external-mode cards themselves.
- **Never** outside the card's `allowed_paths`. If the worker needs to read or write outside, it must stop and surface the gap (San or operator).

## 4. Leaf-card requirement (enforced by packet template)

A card may not be marked `in-external-implementation` unless all of:

- `packets/leaf-card-template.md` is fully filled in (Metadata, Goal, Inputs, Scope, Constraints, Acceptance criteria, Commands, Expected outputs, Report-back format).
- `card.allowed_paths` and `card.forbidden_paths` (packet mirror) are non-empty.
- `card.report_back_channel` is set (see §6).
- Jigo has reviewed the packet (or explicitly waived review for this card type).

## 5. Review requirement

Every external-worker artifact must pass:

1. **San (preflight)**: packet completeness, scope match.
2. **Okkoto (operator)**: worker launched in a sandboxed workspace (allowed paths only), token budget respected.
3. **Jigo (post-flight)**: code matches `acceptance_criteria`; no scope violations; tests pass.

If any of the three fail, the card returns to `changes-requested`.

## 6. Artifact / report-back requirement

- **Where artifacts land**: `changed files` declared in the packet's `Expected outputs`. No surprise files.
- **Report-back format**: see `packets/leaf-card-template.md` §"Report-back format" — Summary, Files changed, Commands run + results, Risks / open questions, Ready for review? yes/no.
- **Report-back channel**: `card.report_back_channel` — typically the project's Matrix room. The worker writes the report there; the operator wolf posts a kanban-comment with the same report.

## 7. Naming normalization across repo docs

Use these exact terms in all repo docs (specs, decisions, prompts, packets, kanban):

| ✅ Use | ❌ Avoid |
|---|---|
| external coder workers | external coders / external workers / external coding workers |
| Claude Code | claude-code / `claude` binary |
| OpenCode | opencode / `opencode` binary |
| Kilocode-cli | kilocode / kilo |
| Gemini-cli | gemini-cli / gemini |
| Copilot-cli | copilot / copilot-cli |

## 8. Anti-patterns

- Launching a worker without a packet ("just try this").
- Hand-waving scope with "small refactor" or "tidy up."
- Reporting "all done" without a report-back message.
- Letting the worker edit ADR 0001 / 0002 / 0003, the canonical spec, or any secret-bearing file.
- Skipping Jigo review because "the change is trivial."

## 9. Escalation

- **San**: packet is ambiguous, scope disputes, scope creep.
- **Jigo**: review bypass attempts, code-level vs config-level disputes.
- **J7**: destructive ops, new external tool introduction, multi-card external-worker use.
