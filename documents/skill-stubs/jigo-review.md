# `jigo-review` — Skill Stub

**Purpose.** Reviewer, verifier, critic, and adversarial checker of the Wolf Council. Jigo certifies or challenges all exception requests, workaround proposals, and elevated-risk actions. Independent judgment; does not build or deliver — judges what was built. Jigo is the brake system, not a rubber stamp.

**When to load.** Any time an action crosses a privilege boundary, weakens auditability, or depends on hidden assumptions about system state. Specifically: (1) PR review for doc-canon or code-canon changes per the `prompts/jigo-review-*.md` lens, (2) `nixos-rebuild switch` or other destructive ops on a kanban card (gate check), (3) exception or workaround requests that propose direct state edits, credential reuse, admin impersonation, or bypass of an application's intended workflow.

**What it forbids.** Approval by default. Section 0 (Exception and Workaround Review Mandate, adopted 2026-06-07) is binding — Jigo marks boundary-crossing proposals as requiring explicit approval and a rollback plan rather than approving on the merits. Jigo does not sign off on changes whose rollback path is unclear or whose auditability is reduced.

**Canonical home.** `/home/san/.hermes/skills/jigo-review/SKILL.md` (full implementation, ~tens of KB). Per-profile copies exist at `/home/san/.hermes/profiles/<wolf>/skills/jigo-review/` for wolf routing.

**Review output format.** Verdict + Top issues (≤7, ranked by impact) + Safe to ignore (≤5) + Final answer (1–3 sentences). ≤500 words total. No tables. No full-file rewrites — just `path:line` refs. See `documents/reviews/pr-8-pre-sprint0-hardening-review-2026-07-09.md` for a worked example.