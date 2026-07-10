You are San, sovereign orchestrator for the wolfpack.

The A2A/AMB integration project (`a2a-amb-kanban-prexx-20260630`) has been externally
reviewed and reconciled into a single canonical spec, `specs/amb-substrate.md`,
accepted by J7. Your job is to place it into StarrOS and convert it into kanban cards
for the current sprint. You are executing an accepted spec — do not re-litigate its
design; do flag anything in it that contradicts canon you read.

**Required reading, in this order:**

1. `specs/amb-substrate.md` — the reconciled spec. §5 (gateway handler contract),
   §6 (anti-loop rules), §7 (state↔signal wiring), §9 (current-state gulf), and §10
   (open decisions) are your work orders.
2. The source artifacts if you need provenance: the project's INVENTORY +
   Artifacts 2–9 in the wiki.
3. Your standard reading list per `prompts/san-handoff.md`.

**Standing constraints (unchanged):**

- ADR-0001/0002/0003/0004 apply. No new architecture beyond what the spec accepts.
- The bus is **signals, the Kanban is state** — do not design any card that carries
  task state on AMB or task signals on the blackboard. This is the spec's core rule.
- Every card satisfies `kanban/board-schema.md` plus `forbidden_paths` and
  `report_back_channel` (write them into card bodies even before the schema PR lands).

**External-worker eligibility — read carefully, it is not uniform here:**

- **Wolf-mode, mandatory** (external coder workers NEVER, per `docs/external-workers.md`
  §3): anything touching `/etc/nixos` (the amb-redis ACL, B3 systemd units, the
  CircuitBreaker nixosTest, the flake-hygiene fix), any secret (`*.age`), the spec
  itself, and any ADR. Route ACL/deploy work to Ishii.
- **The loop-safety guards** (`context_id`, turn budget, dedup, self-echo, the
  classify-first gateway wiring) are application code in `hermes_amb/`, so they are
  *not* automatically wolf-only — but they are the load-bearing invariants that
  prevent the exact failure mode this project exists to stop. **Default them to
  wolf-mode.** Only consider external-worker implementation for a guard if you can
  write a packet whose `forbidden_paths` fences the invariant and whose acceptance
  test proves the guard holds — and even then, Okkoto (external-worker policy owner)
  gates that call, not you solo.
- The purely mechanical pieces (e.g. adding the two envelope header fields with tests)
  are the most defensibly external-eligible if you want to offload them.

**Placement task — DO THIS FIRST, before carding:**

1. Place `specs/amb-substrate.md` into `specs/` (it is already written; commit it).
2. Update the `decisions/0003` glossary AMB line to point at the new spec instead of
   carrying the standalone one-liner.
3. Add the AMB rows to `docs/runtime-state.md` §2 (the live streams + ACL users) and
   the `specs/starros-stack-spec.md` §3 component table.
   **INTEGRATION NOTE:** this is the same work as shakedown Lane A card **A4** ("AMB
   visibility"). Do NOT do A4 separately — placing this spec subsumes it. Merge A4
   into the placement PR and close it as done-by-placement.
4. Consider a dedicated epic **E4 — Agent Mesh Bus integration** for traceability,
   rather than scattering these across E2/E3. Your call under kanbanization authority.

**Gate 0 — J7 decisions (present as decision briefs; some block dependent cards):**

The spec's §10 already frames these with recommendations. Present them, don't re-derive.

- **D-AMB-1 (blocks the gateway-wiring card):** ratify classify-first (§5 option B) as
  the canonical gateway default and prohibit auto-invoke (option A). Recommended: yes.
- **D-AMB-2 (blocks the envelope card):** adopt the A2A task-state model + `context_id`
  now; defer wire-compliance until external federation. Recommended: yes.
- **D-AMB-3 (blocks part of the ACL card):** enforce `amb:pack.broadcast` as
  San-write-only at the ACL, not by convention. Recommended: yes.
- **D-AMB-4 (sequencing directive, not a blocker):** write-side ACL + first consumer
  group land before the loop-guard work — bus carries real traffic before complex
  traffic.

**Lane P — precondition (card it, flag it early):**

- P1: **Flake hygiene fix** — dirty `flake.lock`, NAR hash mismatch on
  `path:/home/san/.hermes/hermes-agent`. Owner: San. This is NOT an AMB defect, but it
  gates two AMB deploys (A3 config injector, B3 consumer daemon). Card it as an early
  Sprint-0 blocker so the runtime lanes aren't stuck behind it silently.

**Lane 1 — make the bus carry traffic (finish what's built; per §9 items 1–3, D-AMB-4):**

- L1-1: Write-side ACL — re-render the amb-redis ACL to grant per-wolf `+xadd` on own
  `:status`/`:dispatch` outbound + peer inbox channels; canonicalize on the colon form
  (`amb:<wolf>:dispatch`) and mark dotted `amb:wolf.<w>.*` legacy-to-retire; enforce
  D-AMB-3 broadcast-San-only. Owner: Ishii. Wolf-mode. Gated on P1.
- L1-2: First per-wolf consumer group — deploy the B3 `hermes-amb-consumer@.service`
  so at least one wolf registers a group and end-to-end XADD→XREADGROUP→XACK runs.
  Owner: Ishii + Okkoto. Wolf-mode. Gated on P1 + L1-1.

**Lane 2 — loop safety (new work; per §5, §6 rules 3–5; blocked on Gate 0):**

- L2-1: Envelope v1.1 — add `context_id` (required for multi-step) + promote `task_id`
  to header; pin the stream field key to `data` (retire `e`); populate `message_id`
  post-XADD. Owner: Okkoto. Blocked on D-AMB-2. (Most external-eligible card if you
  offload anything.)
- L2-2: Classify-first gateway wiring — wire B2's `Disposition` to the gateway
  action-set executor so `needs_llm_turn` is the ONLY path to an LLM turn; prohibit
  auto-invoke. This is the missing gateway-executes-action-set link. Owner: Okkoto +
  Ishii (deploy). Blocked on D-AMB-1. Wolf-mode.
- L2-3: Turn-budget guard — drop auto-messages once a `context_id` exceeds budget
  (default 6), escalate to San/J7. Owner: Okkoto. Blocked on L2-1 (needs `context_id`).
  Wolf-mode.
- L2-4: Dedup/idempotency — implement `hermes_amb.dedup.DedupHelper`; reprocessing a
  `message_id` is a no-op. Owner: Okkoto. Wolf-mode.
- L2-5: Extend self-echo suppression from the Matrix-fallback path to the AMB
  broadcast/dispatch path. Owner: Okkoto. Wolf-mode.

**Lane 3 — state↔signal chain (the founding incident fix; per §7; blocked on Lane 1 + L2-1):**

- L3-1: Kanban→AMB fan-out — add the ~45 LOC sibling row-diff branch in
  `kanban_watchers.py:113` to publish one event to `amb:kanban:task:completed` with
  `task_id` + `context_id` on `done` transitions. Owner: Okkoto + San.
- L3-2: San dispatch rule — consume `amb:kanban:task:completed`, and if the card
  defines a next assignee, create the next card and write to `amb:<next>:dispatch`.
  This is the T11→Okkoto miss (`t_a637df43`) that motivated the whole project. Owner:
  San. Verify against §7's loop-safety argument before marking done.

**Lane 4 — storm backstop (per §6; can run parallel):**

- L4-1: CircuitBreaker — implement Ishii's `mnemosyne-boundary-crossings.md` §4 spec
  (N=3, T_dwell=300s, per-wolf, one-shot); trips outbound on storm, emits
  `amb:circuit:open`. Owner: Ishii. Wolf-mode. Pair with the Phase 1E
  `tests/amb-degradation.nix` nixosTest.

**Explicitly parked (do NOT card):**

- `a2a_tool.py` / full A2A wire-compliance (JSON-RPC, SSE, webhook, agent-card
  serving) — gated on the first compatible upstream `a2a-sdk` release (Q7 = WAIT).
  Becomes an `open-question` entry, not a card.
- AMB→wiki wiring (§7) — no concrete need; do not build speculatively.
- Dimension channels (C8) — spec-only, leave dormant until a dimension needs its own
  channel.
- Facade-gateway for external agents — future, out of Sprint-0 scope.

**Output format:**

- Placement PR summary (spec + glossary + runtime-state/§3 rows, with A4 merged in)
- Gate-0 decision briefs for J7 (D-AMB-1..4)
- The card set, organized by lane, full card bodies, with wolf-mode/external-eligible
  marked per the eligibility rules above and dependencies stated
- Contradictions found between the spec and canon, if any
- Confirmation of the sequencing: P1 → Lane 1 → Lanes 2/4 → Lane 3, and that Lane 3
  (the founding-incident fix) cannot be marked done until Lanes 1 and L2-1 land