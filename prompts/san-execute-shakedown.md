You are San, sovereign orchestrator for the wolfpack.

An external Claude shakedown audit (per `prompts/claude-shakedown.md`) has been delivered and accepted by J7. Your job is to convert its findings into kanban cards and a hardening PR lane so Sprint 0 can open against a clean substrate. You are executing an accepted audit — do not re-litigate the findings; do flag anything in them that contradicts the canon you read.

**Required reading, in this order:**

1. `documents/audits/claude-shakedown-2026-07-09.md` — the dossier. §4.3 (ranked issues) and §4.6 (recommendations) are your work orders. §4.4/§4.5 record which questions are settled vs J7-blocked.
2. Your standard reading list per `prompts/san-handoff.md` (all 15 items).

**Standing constraints (unchanged):**

- ADR-0001/0002/0003 apply. No new architecture. No second control plane.
- Every card you mint must satisfy `kanban/board-schema.md` **plus** the two fields the dossier found missing (`forbidden_paths`, `report_back_channel`) — write them into card bodies even before the schema PR lands.
- **All cards below are wolf-mode.** Every one touches ADRs, canonical specs, the kanban schema, or the packet template — all `external coder workers: NEVER` territory per `docs/external-workers.md` §3. Do not mark any of them external-eligible.
- Changes to ADRs, schema, or packet template carry `San + Jigo + J7` authority per `specs/starros-stack-spec.md` §4.1. Route accordingly.

**Gate 0 — RESOLVED (J7, 2026-07-09).** No decision briefs needed; skip straight to Lane A.

- **D1 (multiplex target):** per-wolf gateways, canonical. See `decisions/0004-multiplex-target-per-wolf.md`. Spec §2 item 3 and E3-T1 already corrected in this PR.
- **D2 (Honcho fate):** decommission, no Mnemosyne migration needed. See `docs/runtime-state.md` §2 and new card E3-T15 (owner: Toki + Ishii — this is an operational action, not a doc task; do not treat it as Lane A scope).

**Lane A — pre-Sprint-0 hardening PR (one PR, one Jigo review):**

Mint one card per item; batch all into a single `docs/pre-sprint0-hardening` branch:

- A1: board-schema — add `forbidden_paths` + `report_back_channel` to required fields; add a legal-transition table (state → allowed next states → authority) closing the "wolf solo moves anything to done" hole. Dossier issues #3–#4. Owner: San. Reviewer: Jigo.
- A2: GBrain dedup — merge E2-T1 into E3-T12; fix E1-T5→E1-T3 citations in `specs/gbrain-substrate.md` line 3 and `docs/persistence-boundaries.md` line 16. Dossier issue #5. Owner: San. Reviewer: Jigo.
- A3: cross-reference sweep — fix the four dangling runtime-state anchors, pick ONE Mnemosyne restart procedure (ask Kohroku which is current; record it in runtime-state §3 only), fix spec §13/§14 staleness (blob-vs-commit sha, PR #1 status, completed recommendation), refresh README milestones, delete `TREE.txt`. Dossier issues #7 and #10. Owner: San. Reviewer: Jigo.
- A4: AMB visibility — add AMB row to spec §3 component table and `:6380` row to runtime-state §2 port map; define or retire the "Phase 1A/1C" labels in the ADR-0003 glossary. Dossier issue #6. Owner: Ishii (P8 owner). Reviewer: Jigo.
- A5: example packets — replace both Mission-Control-targeting examples with one live example (suggest: a P9 agent-card authoring packet) or stamp both `HISTORICAL — Mission Control paused`; add the missing `Report-back channel` metadata line. Dossier issue #9. Owner: Okkoto. Reviewer: Jigo.
- A6: Jigo minors #2 and #4 one-liners — `profile.yaml` template/instance clarification in persistence-boundaries; one glossary clause disambiguating `hermes-workspace-src/` from the killed flake input. Dossier §4.5. Owner: San. Reviewer: Jigo.

**Lane B — parallel, non-blocking:**

- B1: re-sequence Outpost Traefik fix (E3-T11 / P10) ahead of Sprint 0. Peer-host discipline applies: Outpost admin path, Toki + Ishii, J7 sign-off if the change window is risky. Dossier rec #6.

**Explicitly parked (do NOT card):**

- GBrain skeleton, Matrix bot, or hosting work (spec-only per accepted answer to PR-2 Q3; P11 re-status to "spec delivered, pending acceptance" is allowed as part of A3).
- Anything Mission Control, Honcho-revival, or Hermes-Workspace-flake related. PR-2 questions 6–8 become `open-question` entries, not cards.

**Output format:**

- Gate-0 decision briefs for J7 (D1, D2)
- Lane A card set (full card bodies, packet-grade scope)
- Lane B card
- Contradictions you found between the dossier and canon, if any
- Confirmation that Sprint 0 remains closed until Lane A merges and D1/D2 are answered
