# Skill Stubs — StarrOS

> **Purpose:** One-paragraph stubs for every runtime skill that canonical StarrOS docs cite but which previously had no in-repo description. Authored 2026-07-10 per Jigo review of PR #8 (top issue #6). Each stub is a *pointer*, not a copy — for full implementation, see the canonical skill location referenced in each stub's "Canonical home" line.
>
> **Maintainer:** San (E5 epic owner) · Reviewer: Jigo (per `prompts/jigo-review.md`).
>
> **Why this directory exists.** Sprint 0 / Sprint 1 docs (`specs/starros-stack-spec.md`, `decisions/0003-…`, `documents/audits/claude-shakedown-2026-07-09.md:83`) reference several runtime skills (`jigo-review`, `nixos-host-operations`, `j7-homelab-environment`, etc.) by name. Without in-repo stubs, citation drift follows — a reader cannot tell whether a referenced skill is canonical, deprecated, or aspirational. These stubs close the gap.

## Stubs

| Skill | Stub | Canonical home | Version (when stubbed) |
|---|---|---|---|
| `jigo-review` | [`jigo-review.md`](./jigo-review.md) | `/home/san/.hermes/skills/jigo-review/SKILL.md` | (see canonical) |
| `nixos-host-operations` | [`nixos-host-operations.md`](./nixos-host-operations.md) | `/home/san/.hermes/skills/devops/nixos-host-operations/SKILL.md` | 3.14.0 |
| `j7-homelab-environment` | [`j7-homelab-environment.md`](./j7-homelab-environment.md) | `/home/san/.hermes/skills/system/j7-homelab-environment/SKILL.md` | 1.0.0 |

## What a stub is, and is not

**Is:** A one-paragraph description suitable for inclusion in a citation, a doc cross-reference, or a "what is this skill?" tooltip. Tells the reader: purpose, when to load, what it forbids.

**Is not:** The full skill implementation. Do not duplicate the canonical SKILL.md body here — paths change, scripts move, references get added. A stub that drifts from its canonical is worse than no stub.

## Adding a new stub

When a new runtime skill appears in canonical docs:

1. Author `documents/skill-stubs/<skill-name>.md` with the one-paragraph template (Purpose / When to load / What it forbids / Canonical home).
2. Add a row to the table above with the canonical home path and current version.
3. Open a kanban card under Epic E5 (`kanban/backlog.md` E5 epic) for any review pass needed.

## Review cadence

Jigo reviews stub drift on every doc-canon PR (per `prompts/jigo-review.md` lens). A stub that no longer matches its canonical home is a Class 3 issue (citation drift) and must be re-stated or removed.