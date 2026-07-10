# Board Schema

> **Source-of-truth:** this file. Backed by ADR-0001 (repo is canonical) and the lane-A hardening (2026-07-09) closing the schema/policy gap flagged in `documents/audits/claude-shakedown-2026-07-09.md` issues #3 and #4.

## Core states

- inbox
- clarified
- ready-for-design
- ready-for-implementation
- in-external-implementation
- awaiting-wolf-review
- changes-requested
- ready-to-merge
- done
- blocked

## Required card fields

- card_id
- title
- epic
- owner_wolf
- reviewer_wolf
- implementation_mode
- dependencies
- spec_paths
- allowed_paths
- **forbidden_paths** — non-empty list; required by `docs/external-workers.md` §4
- **report_back_channel** — Matrix room id or `card.report_back_channel`; required by `docs/external-workers.md` §4
- acceptance_criteria
- artifact_paths
- status

## Legal transitions

A card's `status` may only change per the table below. Any transition not listed requires a new ADR. Authority column names who may perform the transition; "wolf solo" means the card's `owner_wolf` may move it; reviewer means the `reviewer_wolf` (or Jigo by default); J7 means explicit J7 sign-off per destructive-op discipline.

| From | To | Authority |
|---|---|---|
| inbox | clarified | wolf solo |
| clarified | ready-for-design | wolf solo |
| clarified | blocked | wolf solo |
| ready-for-design | ready-for-implementation | reviewer (after packet sign-off) |
| ready-for-design | blocked | wolf solo |
| ready-for-implementation | in-external-implementation | reviewer + Jigo (per external-workers §5) |
| ready-for-implementation | awaiting-wolf-review | owner_wolf (after wolf execution) |
| in-external-implementation | awaiting-wolf-review | owner_wolf (worker report-back received) |
| in-external-implementation | changes-requested | Jigo (post-flight review) |
| awaiting-wolf-review | changes-requested | reviewer |
| awaiting-wolf-review | ready-to-merge | reviewer (acceptance criteria pass) |
| changes-requested | ready-for-implementation | wolf solo (after fixes) |
| ready-to-merge | done | J7 (post-merge) |
| any | blocked | wolf solo |
| blocked | (previous state) | wolf solo |

**Critical holes closed by this table:**

- No path moves a card to `done` without J7 sign-off, even though `specs/starros-stack-spec.md` §4.1 says "kanban card moves — wolf solo." Solo applies to inter-state moves, not to the `done` terminus.
- External-implementation cards require Jigo at `awaiting-wolf-review → ready-to-merge` (per external-workers §5 post-flight review); without this row, Jigo review was structurally bypassable.
- `done` is a terminal state; cards leaving `done` require a new card id (no resurrection of closed work).