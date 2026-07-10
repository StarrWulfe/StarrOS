# StarrOS Stack Spec — Canonical

> **Status:** v2 — J7 cleanup pass (2026-07-09). Authoritative starting point for everything in this repo. See `decisions/0003-canonical-spec-boundaries.md` for what belongs here vs elsewhere.

## 0. Scope: target architecture vs current implementation state

This spec is the **target architecture** — what StarrOS is meant to be when the rollout lands.

Where the rollout has not landed, this spec does **not** document the workaround state. Workarounds, broken services, and ephemeral runtime facts live in `docs/runtime-state.md` (a deliberately short, frequently-updated companion doc).

**What this spec does:**

- Defines the canonical components, ownership, and inter-call graph.
- Names the source-of-truth for every concern.
- Records architectural decisions (ADRs).
- Lists the rollout phases at the **plan level**; detailed per-card work lives in `kanban/backlog.md`.

**What this spec does NOT do:**

- Track live port maps, broken services, or deployment drift → `docs/runtime-state.md`.
- List per-card backlog items → `kanban/backlog.md`.
- Define policy for external coder workers → `docs/external-workers.md`.
- Define where durable state lives → `docs/persistence-boundaries.md`.

## 1. Purpose

StarrOS is the AI workspace and control plane for Mononoke. It binds together the **wolfpack** (Hermes-Agent profiles), **San** (sovereign orchestrator), the **workspace shell** (Mission Control), and **repo-backed planning** (Forgejo) into a spec-driven, review-gated, audit-friendly surface for J7's day-to-day work.

## 2. Core architecture (target)

1. **San is the sovereign orchestrator.** All inbound requests land on San first; San classifies via `wolf-council-routing` and either handles solo or dispatches to wolves.
2. **The wolfpack is ten specialized wolves** with separate Hermes profiles (`~/.hermes/profiles/<wolf>/`), each with its own `SOUL.md`, `config.yaml`, `.env`, `state.db`, `skills/` mount, Matrix identity, Stalwart mailbox, and Telegram bot. Wolves are real runtime identities, not prompt personas.
3. **Gateway state (target, per ADR-0004):** the canonical default is **one gateway per active wolf** (`hermes-gateway@<wolf>.service` units). Multiplexing wolf traffic through a single gateway was attempted and not adopted — see ADR-0004. Coexistence drift is a known issue; see `docs/runtime-state.md` §2 (service map) and §3 (broken/degraded) for current status, and Phase P0 of the rollout for the fix (scope: bind Ashitaka's `:8643` unit; no multiplex-adoption work).
4. **Mission Control** is the workspace shell. It is currently paused; see `docs/runtime-state.md` §2 (service map, row: Mission Control) and the rollout's Phase P2.
5. **The stock Hermes Dashboard** (Mononoke `:9119`) is a tab inside Mission Control when Mission Control is live, and an independent operational surface until then.
6. **Mononoke is the primary host** for deployment, runtime, and the NixOS service definition layer. Outpost and Yoseba host delegated services (Synapse, Stalwart, headscale, etc.).
7. **Repo-backed planning is the source of truth** (ADR 0001). Chat, Mnemosyne, and per-profile state DBs are operational stores, not planning stores.

## 3. Components (target)

| Component | Role | Owner | Live? |
|---|---|---|---|
| San gateway | Sovereign orchestrator | San (with J7 oversight) | yes |
| 10 wolves (Ashitaka, Ishii, Jigo, Kohroku, Mokku, Moro, Nago, Okkoto, Toki, Yakkuru) | Specialized agents with SOUL.md + skills + Matrix + Telegram + Stalwart identities | per wolf | yes |
| Mission Control | Workspace shell (Next.js 15) | Nago (with Ishii NixOS) | **paused** |
| Hermes Dashboard (`:9119`) | Operational surface until Mission Control resumes | San | yes |
| Forgejo (`:3001`) | Repo of record | Toki (operator) | yes (LAN; public 404 — see runtime-state) |
| Kanban (Hermes Kanban) | Runtime task execution | San | yes |
| Nextcloud (`:11080`) | Long-form docs / shared vault | Nago | yes (empty — see runtime-state) |
| CryptPad | Real-time collab | Okkoto + Nago | no (Phase P7) |
| Karakeep (`keep.starrwulfe.xyz`) | Bookmarking | Mokku (taxonomy) | yes |
| Mnemosyne (SQLite + dashboard) | Primary memory | Kohroku | yes (dashboard down — see runtime-state) |
| **GBrain** | Project substrate (in scope per J7 2026-07-09) | TBD (see `specs/gbrain-substrate.md`) | no |
| External coder workers (5 CLIs) | Bounded leaf-card implementation only | Okkoto (operator) | partial (4/5 installed) |
| BSM secrets | Runtime secret store | J7 (token) + San (consumer) | yes |
| agenix secrets | NixOS-service-layer secrets | Ishii | partial |
| Matrix Synapse (Outpost) | Real-time comms | Okkoto + Ishii (provisioning) | yes |
| Stalwart mail (Yoseba) | Per-wolf mailboxes | Yakkuru (PIM) | yes (mailboxes declared; IMAP IDLE not wired) |
| SearXNG (`search.starrwulfe.xyz`) | Web search | San (consumer) | yes |

**Historical-only (not in target scope):** Honcho (semantic memory stack — decommission pending 2026-07-09, see `docs/runtime-state.md` §2; container still running, stop is an outstanding action item); Hermes Workspace flake input (intentionally killed 2026-07-09 — not the same as the target `Mission Control` row above; see ADR 0003 for terminology).

## 4. Execution model

1. J7's request arrives at San over **Telegram** (`Mononoke 🐺 Wolfpack` group / DMs) or **Matrix** (DM `!zOoWwklQhpaaSSYnDx:mtrx.starrwulfe.xyz`).
2. San classifies intent via `wolf-council-routing` (Ashitaka's charter for cross-domain decomposition).
3. San normalizes the request into **structured cards** in a kanban board (`hermes kanban`; SQLite per board; schema in `kanban/board-schema.md`).
4. San dispatches wolves **one-by-one or in groups** via `delegate_task` or directly per-wolf routing.
5. Each wolf's work produces **artifacts, logs, and review outcomes** committed to the repo (or Nextcloud when identity is wired).
6. Jigo reviews exception requests and elevated-risk actions. Ishii reviews policy/access changes. San surfaces outcomes to J7.
7. Work is **spec-driven, repo-backed, reviewable, and approval-gated** per ADR 0001 + ADR 0002.

### 4.1 Slack tolerances

| Action | Authority |
|---|---|
| Wording-level doc edits | wolf solo |
| Kanban card moves / state transitions | wolf solo |
| `~/.hermes/profiles/<w>/config.yaml` edits | wolf solo |
| External coder workers on a leaf card | Jigo review + packet (see `docs/external-workers.md`) |
| Module edits in `/etc/nixos/nix/services/` | Ishii review + J7 sign-off (destructive-op discipline) |
| Changes to ADRs, kanban schema, packet template | San + Jigo + J7 |

## 5. Repo and tasking model

- **Forgejo is the canonical planning and execution surface** (ADR 0001). Repo: `j7/StarrOS` on `code.starrwulfe.xyz`.
- **Directory layout** (each doc has one job — see `decisions/0003-canonical-spec-boundaries.md`):
  - `specs/` — canonical architecture & subsystem definitions
  - `docs/` — operational playbooks, runtime state, persistence boundaries, external-worker policy
  - `kanban/` — board schema, backlog, sprint slices
  - `packets/` — leaf-card templates + worked examples
  - `prompts/` — wolf agent prompts (san-handoff, jigo-review, fable-global)
  - `decisions/` — ADRs
- **Laptop Claude sessions are drafting environments, not authoritative storage** (ADR 0001). If an artifact matters, it must be committed.
- **Hermes Kanban is canonical** for runtime task execution; Nextcloud Deck is secondary, not bound to Hermes.
- **External coder workers (5 CLIs)** are allowed only for bounded, approved leaf cards per `docs/external-workers.md` and `packets/leaf-card-template.md`.

## 6. Secrets and config model

- **Nix manages structural deployment** via `/etc/nixos/nix/services/` (wolfpack.nix, matrix.nix, nextcloud.nix, etc.).
- **BSM is the runtime secret store**; syncs into `~/.hermes/.env` on each Hermes start. BSM project `ae34e394-8179-4bac-ade5-b45a00e6fd92`; bootstrap `BWS_ACCESS_TOKEN` in `~/.hermes/.env`.
- **agenix** handles only NixOS-service-layer secrets (e.g. `amb-redis-<w>-password.age`).
- **Per-wolf secret naming** (canonicalized):
  - BSM: `<SERVICE>_<CREDENTIAL>` in shared `.env`; per-wolf override via `hermes secrets bitwarden set --profile <wolf> <KEY> <value>`.
  - agenix: `<service>-<wolf>-<purpose>.age` (e.g. `amb-redis-ashitaka-password.age`).
- **Rotation**: BSM rotations do **not** require a rebuild; agenix rotations do.

## 7. UX / workspace model

- **Mission Control** is the target workspace shell: Next.js 15 + TanStack Start/Router + Tailwind 4 + xterm.js + Monaco editor. **Currently paused** (see `docs/runtime-state.md`).
- **Mission Control target design**:
  - 6 primary tabs: Overview · Agents · Tasks · Schedule · Content · Council (per Megapack Subproject 2 design, Nago-led)
  - Data source: `wolfpack.db` SQLite, per the canonical data contract (`wolfpack-dashboard-data-contract.md`)
  - Embedded panes: Hermes Dashboard (`:9119`), Eye-of-Hermes PWA (`:9120` proxied at `/widget/`)
- **Web-first**; desktop wrapper is out of scope for v1.
- **AionUI** UX-pattern addendum slot: `specs/aionui-addendum.md` (placeholder; see Open Decisions).

## 8. Memory and state

- **Mnemosyne is the primary memory layer** (per J7 2026-07-09). Single shared SQLite with logical `author_id` / `channel_id` scoping. DB live, dashboard `:8765` status in `docs/runtime-state.md`.
- **GBrain** is in scope as the project substrate; see `specs/gbrain-substrate.md`.
- **Per-profile `state.db`** is session-transcript only; not a planning store.
- For "where does durable info live?" see `docs/persistence-boundaries.md`.

## 9. End-to-end task flow (target)

```
[J7 sends a request]
    │
    ▼  Telegram group OR Matrix DM
[San gateway]
    │  classify intent (wolf-council-routing)
    │  if multi-domain → Ashitaka for decomposition
    ▼
[Per-wolf gateway (or Ashitaka for dispatch)]
    │  read SOUL.md → load role + skills + dimensions
    │  open or attach to kanban card
    │  read packet if leaf card
    │  if destructive → state blocker → propose declarative candidate → ask J7
    │  if new project → create a dedicated Matrix room with all wolves as members;
    │   wolves post status (claimed / started / blocked / done) per J7 directive
    ▼
[Wolf executes]
    │  uses terminal / file / web / browser / delegate_task / skill tools
    │  writes artifacts to repo (commit + PR), Nextcloud, or Mnemosyne
    ▼
[Wolf logs outcome]
    │  posts reply to Matrix DM + project-status Matrix room
    │  updates kanban card
    │  writes artifacts to agreed paths
    ▼
[Jigo / Ishii / J7 review as needed]
    ▼
[J7 sees outcome in Telegram/Matrix + kanban + repo]
```

## 10. Source-of-truth map

| Concern | Authoritative file | Owner |
|---|---|---|
| Wolf identity & charter | `~/.hermes/profiles/<wolf>/SOUL.md` | per wolf (San sign-off) |
| Wolf agent card | `/nas/hdd/agent-shared/agent-cards/wolves/<wolf>.yaml` | Ashitaka |
| Wolf profile config | `~/.hermes/profiles/<wolf>/config.yaml` | per wolf |
| Wolf systemd unit | `/etc/nixos/nix/services/wolfpack.nix` | Ishii |
| **Mission Control target** | `specs/starros-stack-spec.md` §7 | Nago |
| **Mission Control source** | `~/.hermes/hermes-workspace-src/` | Nago |
| **Mission Control NixOS module** | `/etc/nixos/nix/services/hermes-workspace.nix` | Ishii |
| **GBrain substrate** | `specs/gbrain-substrate.md` | TBD (Phase P11) |
| **Runtime state** | `docs/runtime-state.md` | San + Kohroku |
| **Persistence boundaries** | `docs/persistence-boundaries.md` | San |
| **External coder workers policy** | `docs/external-workers.md` | Okkoto |
| Kanban schema | `kanban/board-schema.md` | San |
| Backlog seed | `kanban/backlog.md` | San |
| Leaf-card packet | `packets/leaf-card-template.md` | per wolf |
| Wolfpack DB schema (runtime) | `wolfpack.nix` inline SQL + `wolfpack-dashboard-data-contract.md` | Okkoto |
| Secrets (runtime) | `~/.hermes/.env` (BSM-synced) | J7 + San |
| Secrets (NixOS layer) | `/etc/nixos/secrets/*.age` | Ishii |
| Architectural decisions | `decisions/000N-*.md` (ADR format) | J7 (author) + wolves (review) |
| Destructive-op discipline | `system/j7-homelab-environment` skill | Ishii + J7 |

## 11. Rollout

The detailed phase plan lives in `kanban/backlog.md`. Headline:

| Phase | Title | Status |
|---|---|---|
| P0 | Fix Ashitaka gateway binding, port 8643 (per ADR-0004; multiplex adoption dropped) | in progress |
| P1 | wolfpack.nix adoption | planned |
| P2 | Mission Control revival | paused (J7 2026-07-09) |
| P3 | Per-wolf Nextcloud identity | not started |
| P4 | Mnemosyne dashboard restore | not started |
| P5 | Karakeep OIDC end-to-end | live, smoke pending |
| P6 | External coder workers: add Claude Code | in progress (4/5) |
| P7 | CryptPad enable + WebAuthn | not started |
| P8 | Phase 1C ACL finalization (amb-redis per-wolf) | in progress |
| P9 | 9 missing Agent Cards | in progress (2/11) |
| P10 | Outpost Traefik fix (`code.starrwulfe.xyz` → 100.77.7.1:3001) | not started |
| P11 | GBrain substrate spec | **not started — this PR's companion spec** |
| P12 | Talk routing fix | not started |
| P13 | Per-wolf git signing identities | not started |

Detailed per-card work, owner_wolf, and reviewer_wolf: see `kanban/backlog.md`.

## 12. Architectural decisions

| ADR | Title |
|---|---|
| 0001 | Repo is the source of truth |
| 0002 | Human authors playbook v0 |
| 0003 | Canonical spec boundaries (this spec belongs in `specs/`, ephemeral state in `docs/`) |

## 13. Recommendations (non-binding)

- **Add `docs/runtime-state.md` and `docs/persistence-boundaries.md` to the `prompts/san-handoff.md` reading list** so future San runs ingest them as ground truth.
- **Reduce the spec drift rate** by re-running the cleanup pass whenever a new doc is added; link from `decisions/0003-canonical-spec-boundaries.md`.
- **Treat `kanban/backlog.md` as the authoritative per-phase plan**; this spec links to it, not the other way around.

## 14. Provenance

- v1.0 (2201 bytes, J7 original) — commit sha `908aae4a4b…` on `main`
- v1.1 (26995 bytes, San canonicalization) — commit `21dee6d` on branch `spec/starros-stack-canonicalization` (PR #1, open)
- v2.0 (this revision, doc-canon pass) — pending (PR #2)
