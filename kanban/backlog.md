# Backlog Seed

> **Source of truth:** `specs/starros-stack-spec.md` §11 names the phases; this file holds the per-card plan.
> **Update:** after each phase, move cards into `sprints/` and keep a thin row here for tracking.

## Epic E0 — Foundations (doc-canon pass)

- [ ] E0-T1 Finalize playbook (docs/playbook.md) — link companion docs
- [ ] E0-T2 Finalize backlog structure (this file)
- [ ] E0-T3 Finalize packet template (packets/leaf-card-template.md) — add `report_back_channel` field
- [ ] E0-T4 San review and kanbanization
- [ ] E0-T5 Spec cleanup + 5 new companion docs — author: San, reviewer: Jigo

## Epic E1 — StarrOS doc canon (this PR)

- [ ] E1-T1 Trim `specs/starros-stack-spec.md` to integration-overview only — author: San
- [ ] E1-T2 Author `docs/runtime-state.md` (live state) — author: San
- [ ] E1-T3 Author `specs/gbrain-substrate.md` (project substrate) — author: San + Ashitaka
- [ ] E1-T4 Author `docs/persistence-boundaries.md` (durable-info map) — author: San
- [ ] E1-T5 Author `docs/external-workers.md` (CLI workers policy) — author: Okkoto + Jigo
- [ ] E1-T6 Author `decisions/0003-canonical-spec-boundaries.md` — author: San + J7
- [ ] E1-T7 Cross-file normalize (playbook, workflow, packet, prompts) — author: San

## Epic E2 — Data and orchestration

- [ ] E2-T1 GBrain substrate definition (was "OKF/GBrain") → see `specs/gbrain-substrate.md`
- [ ] E2-T2 Mnemosyne integration policy — owner: Kohroku
- [ ] E2-T3 Kanban REST / backend adapter — owner: San + Okkoto
- [ ] E2-T4 Wolf task execution flow (E2E diagram test) — owner: San

## Epic E3 — Runtime ops (mapped to rollout phases)

- [ ] E3-T1 Multiplex + Ashitaka :8643 (Phase P0) — owner: Ishii
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
