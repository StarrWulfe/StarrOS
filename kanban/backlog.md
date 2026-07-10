# Backlog Seed

> **Source of truth:** `specs/starros-stack-spec.md` §11 names the phases; this file holds the per-card plan.
> **Update:** after each phase, move cards into `sprints/` and keep a thin row here for tracking.

## Epic E0 — Foundations (doc-canon pass)

- [x] E0-T1 Finalize playbook (docs/playbook.md) — link companion docs
- [x] E0-T2 Finalize backlog structure (this file)
- [x] E0-T3 Finalize packet template (packets/leaf-card-template.md) — add `report_back_channel` field
- [x] E0-T4 San review and kanbanization
- [x] E0-T5 Spec cleanup + 5 new companion docs — author: San, reviewer: Jigo

## Epic E1 — StarrOS doc canon (this PR)

- [x] E1-T1 Trim `specs/starros-stack-spec.md` to integration-overview only — author: San
- [x] E1-T2 Author `docs/runtime-state.md` (live state) — author: San
- [x] E1-T3 Author `specs/gbrain-substrate.md` (project substrate) — author: San + Ashitaka
- [x] E1-T4 Author `docs/persistence-boundaries.md` (durable-info map) — author: San
- [x] E1-T5 Author `docs/external-workers.md` (CLI workers policy) — author: Okkoto + Jigo
- [x] E1-T6 Author `decisions/0003-canonical-spec-boundaries.md` — author: San + J7
- [x] E1-T7 Cross-file normalize (playbook, workflow, packet, prompts) — author: San
- [x] E1-T8 Jigo review of doc-canon PR pair — fixes addressed in PR-3

## Epic E2 — Data and orchestration

- [ ] E2-T1 GBrain substrate definition (DEDUP — see E3-T12; same deliverable; subsumed by E3-T12 after Phase P11 was added; kept visible for E0 audit trail)
- [ ] E2-T2 Mnemosyne integration policy — owner: Kohroku
- [ ] E2-T3 Kanban REST / backend adapter — owner: San + Okkoto
- [ ] E2-T4 Wolf task execution flow (E2E diagram test) — owner: San

## Epic E3 — Runtime ops (mapped to rollout phases)

- [ ] E3-T1 Fix Ashitaka gateway binding :8643 (Phase P0, per ADR-0004) — owner: Ishii
- [ ] E3-T2 wolfpack.nix adoption (Phase P1) — owner: Ishii + Okkoto
- [ ] E3-T3 Mission Control revival (Phase P2, paused) — owner: Nago
- [ ] E3-T4 Per-wolf Nextcloud identity (Phase P3) — owner: Nago + Ishii
- [ ] E3-T5 Mnemosyne dashboard restore (Phase P4) — owner: Kohroku
- [ ] E3-T6 Karakeep OIDC end-to-end (Phase P5) — owner: Mokku
- [ ] E3-T7 Add Claude Code (Phase P6) — owner: Okkoto
- [ ] E3-T8 CryptPad enable + WebAuthn (Phase P7) — owner: Okkoto + Nago
- [ ] E3-T9 Phase 1C ACL finalization (Phase P8) — owner: Ishii
- [ ] E3-T10 9 missing Agent Cards (Phase P9) — owner: Ashitaka + Okkoto
- [ ] E3-T11 Outpost Traefik fix (Phase P10) — owner: Ishii + Toki
- [ ] E3-T12 GBrain substrate spec (Phase P11) — owner: San + Ashitaka
- [ ] E3-T13 Talk routing fix (Phase P12) — owner: Ishii
- [ ] E3-T14 Per-wolf git signing identities (Phase P13) — owner: Okkoto + Ishii
- [ ] E3-T15 Decommission Honcho podman unit, reclaim :8000 (per J7 2026-07-09 shakedown D2; no Mnemosyne migration needed) — owner: Toki + Ishii
- [ ] E3-T16 Outpost Traefik fix, re-sequenced ahead of Sprint 0 (dossier rec #6, pre-Sprint-0 hardening B1) — supersedes E3-T11 sequencing; owner: Ishii + Toki; **gate: J7 sign-off if change window is risky**; peer-host discipline (Outpost admin path, not Mononoke). One-line sed + Traefik HUP per `docs/runtime-state.md` §3 #3.

## Epic E4 — Pre-Sprint-0 hardening lane (this PR)

- [x] E4-A1 board-schema: add `forbidden_paths` + `report_back_channel` + legal-transition table — author: San, reviewer: Jigo
- [x] E4-A2 GBrain dedup (E2-T1 vs E3-T12) + E1-T5 → E1-T3 citation fix — author: San, reviewer: Jigo
- [x] E4-A3 cross-reference sweep + Mnemosyne restart procedure + spec §13/§14 provenance + README milestones + delete `TREE.txt` (Mnemosyne restart pick pending Kohroku) — author: San, reviewer: Jigo
- [x] E4-A4 AMB visibility in spec §3 + runtime-state §2 port map + Phase 1A/1C labels defined — author: Ishii, reviewer: Jigo
- [x] E4-A5 example packets: stamp Mission-Control examples HISTORICAL + add Report-back channel field — author: Okkoto, reviewer: Jigo
- [x] E4-A6 Jigo minors #2 (profile.yaml template/instance) + #4 (hermes-workspace-src disambiguation) — author: San, reviewer: Jigo
- [x] E4-B1 re-sequence Outpost Traefik fix ahead of Sprint 0 (see E3-T16) — author: San, reviewer: Jigo

## Epic E5 — Skill stub hardening lane (Jigo minor #6)

- [ ] E5-T1 Open Epic E5 + author `documents/skill-stubs/{README.md, jigo-review.md, nixos-host-operations.md, j7-homelab-environment.md}` — author: San, reviewer: Jigo. See file-system kanban card `t_c9d4a6b2`. Triggered by Jigo review of PR #8 (top issue #6).

## Epic E6 — AMB Substrate integration (per `specs/AMB-Substrate.md`; placement PR closes the design-contract half; implementation cards follow)

> **Design contract:** `specs/AMB-Substrate.md` (placed in this PR). Sourced from external review of `a2a-amb-kanban-prexx-20260630` and reconciled with `kanban/board-schema.md`. Implementation cards below; see `specs/AMB-Substrate.md` §10 for the J7 decisions that block them.

### E6 P — precondition

- [ ] E6-P1 San — Flake hygiene fix (dirty `flake.lock`, NAR hash mismatch on `path:/home/san/.hermes/hermes-agent`). NOT an AMB defect; gates A3 config injector + B3 consumer daemon. **Block runtime lanes silently if not done first.**

### E6 Lane 1 — make the bus carry traffic (per spec §9 items 1–3, D-AMB-4)

- [ ] E6-L1-1 Ishii (wolf-mode) — Re-render the amb-redis ACL to grant per-wolf `+xadd` on own `:status`/`:dispatch` outbound + peer inbox channels; canonicalize on the colon form `amb:<wolf>:dispatch`; mark dotted `amb:wolf.<w>.*` legacy-to-retire; enforce D-AMB-3 (San-only broadcast at ACL). Gated on E6-P1.
- [ ] E6-L1-2 Ishii + Okkoto (wolf-mode) — Deploy the B3 `hermes-amb-consumer@.service` so at least one wolf registers a group and end-to-end XADD→XREADGROUP→XACK runs. Gated on E6-P1 + E6-L1-1.

### E6 Lane 2 — loop safety (per spec §5 + §6 rules 3–5; blocked on Gate 0)

> Gate 0 decisions D-AMB-1, D-AMB-2 must be ratified by J7 before Lane 2 starts. L2-3..L2-5 are chained on L2-1.

- [ ] E6-L2-1 Okkoto — Envelope v1.1: add `context_id` (required for multi-step) + promote `task_id` to header; pin stream field key to `data` (retire `e`); populate `message_id` post-XADD. Blocked on D-AMB-2. **Most external-worker-eligible card if any is.**
- [ ] E6-L2-2 Okkoto + Ishii deploy (wolf-mode) — Classify-first gateway wiring: wire B2 `Disposition` to gateway action-set executor so `needs_llm_turn` is the ONLY path to an LLM turn; prohibit auto-invoke. Blocked on D-AMB-1.
- [ ] E6-L2-3 Okkoto (wolf-mode) — Turn-budget guard: drop auto-messages once `context_id` exceeds budget (default 6); escalate to San/J7. Blocked on E6-L2-1.
- [ ] E6-L2-4 Okkoto (wolf-mode) — Dedup / idempotency: implement `hermes_amb.dedup.DedupHelper`. Reprocessing a `message_id` is a no-op. Mandatory under at-least-once delivery.
- [ ] E6-L2-5 Okkoto (wolf-mode) — Extend self-echo suppression from the Matrix-fallback path to the AMB broadcast/dispatch path.

### E6 Lane 3 — state↔signal chain (per spec §7; blocked on Lane 1 + L2-1; founding-incident fix)

> Lane 3 cannot be marked done until both E6 Lane 1 and E6-L2-1 land. The T11→Okkoto dispatch miss (`t_a637df43`) is the founding incident this lane resolves.

- [ ] E6-L3-1 Okkoto + San — Kanban→AMB fan-out: add the ~45 LOC sibling row-diff branch in `kanban_watchers.py:113` to publish one event to `amb:kanban:task:completed` with `task_id` + `context_id` on `done` transitions.
- [ ] E6-L3-2 San — San dispatch rule consumes `amb:kanban:task:completed`; if the card defines a next assignee, create the next card and write to `amb:<next>:dispatch`. Verify against `specs/AMB-Substrate.md` §7's loop-safety argument before marking done.

### E6 Lane 4 — storm backstop (per spec §6; can run parallel)

- [ ] E6-L4-1 Ishii (wolf-mode) — CircuitBreaker per `mnemosyne-boundary-crossings.md` §4 (N=3, T_dwell=300s, per-wolf, one-shot); trips outbound on storm; emits `amb:circuit:open`. Pair with Phase 1E `tests/amb-degradation.nix` nixosTest.
