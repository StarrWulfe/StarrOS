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
