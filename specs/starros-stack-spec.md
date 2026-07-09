# StarrOS Stack Spec — Canonical

> **Status:** v1 — drafted by San from prior research + repo state (commit sha `cdaaa0263…` on main). Supersedes the 2201-byte stub. Hold for J7 review before PR.
>
> **Scope of this file:** single canonical spec for the StarrOS stack. Other files (`docs/playbook.md`, `kanban/board-schema.md`, etc.) remain authoritative for their domains; this spec is the **integration overview** that ties them together.
>
> **Supersedes:** `Project StarrOS` (absorbed as Project Megapack Subproject 2 per J7 directive 2026-06-13; see `agent-shared/projects/starrOS-to-megapack-transfer.md`).
>
> **Edit history:**
> - v1.0 (2201 bytes, J7 original) — commit sha `908aae4a4b…`
> - v1.1 (San canonicalization, this revision) — per J7 edits 2026-07-09:
>   - **Hermes Workspace killed intentionally** by J7 (repeated crashes); revisit later — NOT a flake-input bug.
>   - **Ashitaka** is intended to bind **port 8643** (currently unbound; PID 20888 alive but no port — was a misdiagnosis as duplicate-multiplex).
>   - **Multiplex status:** **running** on `:8642` (PID 490006), with `multiplex_profiles: false`. Multiplex is **not** paused — J7's belief is corrected.
>   - **GBrain is in scope; Honcho is out of scope** (j7 directive 2026-07-09).
>   - **Karakeep is live** at `https://keep.starrwulfe.xyz` (HTTP 200, PocketID OIDC). Mnemosyne dashboard `:8765` is currently **down**, not "running on some port."
>   - **CryptPad will be added** (P7 phase below).
>   - **External coder workers** in scope: OpenCode, Kilocode-cli, Gemini-cli, Copilot-cli (already installed at `/run/current-system/sw/bin/`) + **Claude Code** (to be added).

---

## 1. Purpose

StarrOS is the AI workspace and control plane for Mononoke. It binds together the **wolfpack** (Hermes-Agent profiles), **San** (sovereign orchestrator), **Mission Control** (the workspace shell), and **repo-backed planning** (Forgejo) into one spec-driven, review-gated, audit-friendly surface for J7's day-to-day work.

Mission Control is the **workspace shell**. The stock Hermes Dashboard remains a subsystem/tab inside Mission Control — it is not the primary surface.

---

## 2. Architectural Layers

| Layer | Component | Current state | Source of truth |
|---|---|---|---|
| Host | Mononoke (NixOS, 100.77.7.1) | live | `system/j7-homelab-environment` skill |
| Host | Outpost VPS (100.77.7.2) | live | same |
| Host | Yoseba (Arch, 45.79.220.12) | live | same |
| Agent runtime | Hermes-Agent (Nous Research fork, v0.18.0) | live on `:8642` (multiplex) + per-wolf ports `8644-8652` | `~/.hermes/hermes-agent/` |
| Orchestration | San + 10 wolves (Ashitaka, Ishii, Jigo, Kohroku, Mokku, Moro, Nago, Okkoto, Toki, Yakkuru) | live as 11 systemd user units + 1 system multiplex | `~/.hermes/profiles/<wolf>/SOUL.md` |
| Workspace shell | Mission Control (= `hermes-workspace-src` Next.js app on `:3002`) | **NOT live** — service dead; flake input `inputs.hermes-workspace` no longer resolves | `~/.hermes/cron/output/2026-07-07_wolfpack_audit_round2.md` §10 |
| Repo of record | Forgejo on Mononoke (`:3001`) at `code.gatewood.xyz` + `code.starrwulfe.xyz` | live (LAN only — public host 404 due to Outpost Traefik pointing `127.0.0.1:3001` instead of `100.77.7.1:3001`) | ADR 0001 |
| Kanban | Hermes Kanban (per-board SQLite at `~/.hermes/kanban/boards/<slug>/`) | 13 live boards | `kanban/board-schema.md` |
| Long-form docs | Nextcloud (Hub 10 v33.0.5.1) at `:11080` | live but empty | `~/.hermes/profiles/san/config.yaml` → `extraApps` |
| Real-time collab | CryptPad (`/etc/nixos/nix/services/cryptpad.nix`) | **NOT live** — module written but `enable = true` line absent | `cryptpad.nix` header comment |
| Bookmarking | **Karakeep** at `https://keep.starrwulfe.xyz` (PocketID OIDC) | **live** (HTTP 200; not on Mononoke podman list — backed by Outpost or external) | `keep.starrwulfe.xyz` |
| Memory | Mnemosyne (SQLite 174 MB WAL at `~/.hermes/mnemosyne/data/mnemosyne.db`) | DB live, **dashboard `:8765` down** | `~/.hermes/mnemosyne/` |
| **GBrain substrate** (j7 in-scope) | TBD | not defined — see Open Decisions §11 | — |
| ~~Honcho semantic memory~~ | REMOVED from scope per J7 2026-07-09 | Mnemosyne is canonical memory; Honcho podman stack may be torn down in a future phase | — |
| Secrets | BSM (canonical, synced into `~/.hermes/.env`) + agenix (NixOS-managed, per-wolf passwords `amb-redis-<w>-password.age`) | BSM live; agenix per-wolf files not yet provisioned | `~/.hermes/.env` + `/etc/nixos/secrets/` |
| Matrix | Synapse on Outpost at `mtrx.starrwulfe.xyz` | live; 11 bot accounts `@<wolf>:mtrx.starrwulfe.xyz` | `system/j7-homelab-environment` skill |
| External coder workers | OpenCode · Kilocode-cli · Gemini-cli · Copilot-cli (`/run/current-system/sw/bin/`) + **Claude Code** (planned add) | 4/5 installed | `which opencode kilocode gemini copilot` |

---

## 3. Core Architecture

- **San is the sovereign orchestrator.** All inbound requests land on San first; San classifies via `wolf-council-routing` and either handles solo or dispatches to wolves.
- **The wolfpack is ten specialized wolves** with separate Hermes profiles (`~/.hermes/profiles/<wolf>/`), each with its own:
  - `SOUL.md` (identity + operating boundaries + dimensions)
  - `config.yaml` (model, providers, behavior)
  - `.env` (secrets — per-bot tokens)
  - `state.db` (per-profile session SQLite)
  - `skills/` mount (21–53 entries per wolf vs 59 in shared pool)
  - Matrix identity `@<wolf>:mtrx.starrwulfe.xyz`
  - Stalwart mailbox `<wolf>@agent.starrwulfe.xyz`
  - Telegram bot `@Srwf<Wolf>Bot`
- **Wolves are real runtime identities, not prompt personas.** Each runs as its own `hermes-gateway-<wolf>.service` systemd user unit under the shared `san` Linux user.
- **Multiplex state (live, intentional):** a single `hermes-gateway.service` (system unit, PID 490006) holds the API server on `:8642`. `multiplex_profiles: false` in `~/.hermes/config.yaml` means profile multiplexing is OFF — the multiplex serves as the canonical San gateway, while 10 per-wolf units coexist on `8644-8652` (one port each, alphabetical by systemd instantiation order).
- **Ashitaka is intended to bind port 8643** (currently unbound — PID 20888 is alive but no listener; debug needed). Misdiagnosis corrected: this is **not** a duplicate-multiplex hazard.
- **Mission Control is the main workspace shell** (currently paused — see §12 P2 and Rollout Plan).
- **The stock Hermes Dashboard (`http://100.77.7.1:9119`) is a tab inside Mission Control**, not a peer surface.
- **Mononoke is the primary host** for deployment, runtime, and the NixOS service definition layer.

---

## 4. Execution Model

1. J7's request arrives at San over **Telegram** (`Mononoke 🐺 Wolfpack` group / DMs) or **Matrix** (DM `!zOoWwklQhpaaSSYnDx:909f1eb71731`).
2. San classifies intent via `wolf-council-routing` (Ashitaka's charter for cross-domain decomposition).
3. San normalizes the request into **structured cards** in a kanban board (`hermes kanban` CLI; SQLite per board).
4. San dispatches wolves **one-by-one or in groups** via `delegate_task` (up to 3 concurrent children) or directly per-wolf routing.
5. Each wolf's work produces **artifacts, logs, and review outcomes** committed to the repo or written to a Nextcloud vault path.
6. Jigo (Verifier) reviews exception requests and elevated-risk actions. Ishii (NixOS Consul) reviews policy/access changes. San surfaces outcomes to J7.
7. Work is **spec-driven, repo-backed, reviewable, and approval-gated** per ADR 0001 + ADR 0002.

### 4.1 Slack tolerances
- Wording-level changes: wolf solo, no human sign-off.
- Config edits in `~/.hermes/profiles/<w>/config.yaml`: wolf solo.
- Module edits in `/etc/nixos/nix/services/`: **requires Ishii review + J7 sign-off** per `destructive-operation-discipline` (skill `system/j7-homelab-environment`).
- Card creation / kanban state moves: wolf solo.
- External coder workers (Claude Code, Codex): **only for bounded, approved leaf cards** (per `docs/playbook.md` "External coding workers allowed only for bounded, approved leaf cards").

---

## 5. Repo and Tasking Model

- **Forgejo is the canonical planning and execution surface** (ADR 0001). Repo: `j7/StarrOS` on `code.starrwulfe.xyz`.
- **Specs, playbooks, prompts, backlog definitions, and packet templates** all live in the repo at `specs/`, `docs/`, `kanban/`, `packets/`, `prompts/`, `decisions/`.
- **Laptop Claude sessions are drafting environments, not authoritative storage** (ADR 0001). If an artifact matters, it must be committed.
- **External coding workers (Claude Code, Codex) are allowed only for bounded, approved leaf cards** (`packets/leaf-card-template.md`).
- **San and the wolves operate from repo-backed artifacts**, not private chat history.
- **Kanban schema** lives at `kanban/board-schema.md`. The 10 core states: `inbox → clarified → ready-for-design → ready-for-implementation → in-external-implementation → awaiting-wolf-review → changes-requested → ready-to-merge → done` (+ `blocked`).
- **Hermes Kanban is canonical** for runtime task execution (per `starrOS-to-megapack-transfer.md` decision #2). Nextcloud Deck is **secondary**, not bound to Hermes.

---

## 6. Secrets and Config Model

- **Nix manages structural deployment and service topology** via `/etc/nixos/nix/services/wolfpack.nix` (10 wolves) + `services.hermes-workspace.nix` (Mission Control) + per-service modules.
- **Hermes manages runtime secrets through the built-in Bitwarden Secrets Manager skill** (`system/bitwarden-secrets`). BSM project ID `ae34e394-8179-4bac-ade5-b45a00e6fd92`; bootstrap token `BWS_ACCESS_TOKEN` in `~/.hermes/.env`.
- **Secrets should not require rebuilds to rotate** — BSM-synced into `.env` on next Hermes start. agenix-managed secrets DO require a rebuild (acceptable for NixOS service credentials like `amb-redis-<w>-password`).
- **Runtime `.env` state is Bitwarden-backed, not SOPS-owned.** agenix handles only NixOS-service-layer secrets.
- **Per-wolf secret naming convention:**
  - BSM: `<SERVICE>_<CREDENTIAL>` in shared `.env` (e.g. `TELEGRAM_BOT_TOKEN`); per-wolf override via `hermes secrets bitwarden set --profile <wolf> <KEY> <value>`.
  - agenix: `amb-redis-<w>-password.age` (12 slots: admin + 10 wolves + 1 reserved). Per-wolf files **not yet provisioned** on disk as of audit; ACL module is rendered but `aclfile` directive not yet wired into systemd (`/etc/nixos/nix/services/amb-redis.nix` Phase 1C partial).
- **Hash-only ACL pattern** (currently adopted as workaround for agenix builder-PATH gap): SHA256 hashes of wolf passwords embedded as literal Nix attrset (`passwordHashes`) in `amb-redis-acl-hashes.nix`. Hashes are not secrets — they verify but do not recover passwords.

---

## 7. UX / Workspace Model

- **Mission Control** (the canonical workspace shell) — Next.js 15 + TanStack Start/Router + Tailwind 4 + xterm.js + Monaco editor (`hermes-workspace-src/FEATURES-INVENTORY.md`). Currently **NOT live** (see §10 blockers).
- **Mission Control shell design (target):**
  - **6 primary tabs**: Overview · Agents · Tasks · Schedule · Content · Council (per Megapack Subproject 2 design, Nago-led)
  - **Live data source**: `wolfpack.db` SQLite via `wolfpack-dashboard-data-contract.md` (canonical per-view SQL + JSON contract)
  - **Embedded panes**:
    - Stock Hermes Dashboard (`:9119`) — basic-auth-gated `j7`/scrypt
    - Eye-of-Hermes PWA widget (`:9120` proxied at `/widget/`, 8-segment status: TG/RSND/KBN/WB/KB/WC/GH/TOKEN)
- **Web-first is preferred; desktop wrapper is optional and out of scope for v1.**
- **AionUI** UX-pattern addendum slot exists at `specs/aionui-addendum.md` (currently a placeholder; see Open Decisions §11).

---

## 8. Known uncertainty / needs confirmation

The following are open as of this revision — see §11 Open Decisions for full treatment.

- **GBrain** — referenced in `kanban/backlog.md` E2-T1 ("OKF/GBrain substrate") and `prompts/fable-global.md`. **In scope per J7 2026-07-09** but **no definition, repo, or module exists**. Decision: define a "wolfpack substrate" spec doc + add Phase P11.
- **Mnemosyne integration policy** — backlogs E2-T2. Mnemosyne dashboard `:8765` is **down** (not "running on some port"). Scope (per-wolf vs shared with prefixes) is established (shared DB with `author_id`/`channel_id` scoping) but **promotion-to-per-wolf-DB policy** is not set.
- **Ashitaka port 8643** — PID 20888 alive, but no listener bound to `:8643`. The default port assignment in `wolfpack.nix` places ashitaka on `:8643`. Debug needed before port-mapping assumption is solid.
- **Multiplex-vs-per-wolf coexistence** — both the multiplex (`:8642`) and 10 per-wolf gateways run simultaneously; canonical P0–P12 rebuild from `megapack-deploy-playbook.md` has not been executed. `multiplex_profiles: false` confirms the per-wolf multiplex dispatch is OFF — the multiplex is a single gateway, not a router.
- **CryptPad** — module written, never enabled. J7 directive 2026-07-09: **add it**. See Phase P7.
- **Mnemosyne dashboard** — service crashed; restoration procedure documented in `nixos-host-operations` skill (`bsm-secret-fetch-for-environmentfile.sh`).
- **Per-wolf Agent Cards** — only `san.yaml` + `ashitaka.yaml` written; 9 missing despite SOUL.md + skill inventory being available.
- **Hermes Workspace** — **intentionally killed by J7** (recurrent crashes). Revisit in a future phase; do not allocate resources now.

---

## 9. Source-of-Truth Map

| Concern | Authoritative file | Owner |
|---|---|---|
| Wolf identity & charter | `~/.hermes/profiles/<wolf>/SOUL.md` | per wolf (San-sign-off) |
| Wolf agent card (machine-readable) | `/nas/hdd/agent-shared/agent-cards/wolves/<wolf>.yaml` | Ashitaka (per Phase 1C C8) |
| Wolf profile config | `~/.hermes/profiles/<wolf>/config.yaml` | per wolf |
| Wolf systemd unit | `/etc/nixos/nix/services/wolfpack.nix` | Ishii |
| Multiplex + per-wolf coexistence | `wolfpack.nix` + `nixos-host-operations/references/multiplexer-vs-per-wolf-drift-2026-06-27.md` | Ishii + Okkoto |
| Mission Control source | `~/.hermes/hermes-workspace-src/` | Nago |
| Mission Control NixOS module | `/etc/nixos/nix/services/hermes-workspace.nix` | Ishii |
| Mission Control flake input | `inputs.hermes-workspace` (external) — **broken** | Ishii + J7 |
| Kanban schema | `kanban/board-schema.md` | San |
| Backlog seed | `kanban/backlog.md` | San |
| Packets | `packets/leaf-card-template.md` + `packets/examples/` | per wolf |
| Wolfpack schema (canonical runtime) | `~/.hermes/wolfpack-schema.md` (per `wolfpack-dashboard-data-contract.md`) + `wolfpack.nix` inline SQL | Okkoto (builder) |
| Wolfpack dashboard data contract | `~/.hermes/skills/devops/hermes-multi-profile-architecture/references/wolfpack-dashboard-data-contract.md` | Okkoto |
| Honcho pipe | `/home/san/.config/systemd/user/session-feed-to-honcho.{service,timer}` + `~/.hermes/scripts/session-feed-to-honcho*.sh` | Toki |
| Secrets (runtime) | `~/.hermes/.env` (BSM-synced) | J7 + San |
| Secrets (NixOS layer) | `/etc/nixos/secrets/*.age` | Ishii |
| ACLA / per-wolf ACL hashes | `/etc/nixos/nix/services/amb-redis-acl*.nix` | Ishii |
| Architectural decisions | `decisions/000N-*.md` (ADR format) | J7 (author) + wolves (review) |
| Destructive op discipline | `system/j7-homelab-environment` skill §"Destructive Operation Discipline" | Ishii + J7 |
| Memory (primary) | `~/.hermes/mnemosyne/data/mnemosyne.db` | Kohroku |
| Memory (semantic) | `/var/lib/docker-compose/honcho/` (pgvector) | Mokku |
| Wiki (operational) | `/nas/hdd/agent-shared/wiki/` | Mokku |
| KB / playbook | `docs/playbook.md` + `docs/workflow.md` | San (review) + J7 (author) |

---

## 10. Component Ownership Map

| Component | Primary owner | Reviewer | Co-owner / notes |
|---|---|---|---|
| San gateway | San | J7 | sovereign |
| Per-wolf gateway (10×) | per wolf | per reviewer wolf | inherits OS user `san` |
| Multiplex | San | Ishii | live on `:8642`; coexisting with per-wolf until P0–P12 rebuild |
| **GBrain substrate** | TBD (J7 to define owner) | Jigo | in scope per J7 2026-07-09; no spec exists yet |
| Mission Control web app | Nago | Jigo | Next.js 15 source at `hermes-workspace-src`; **paused by J7** |
| ~~Hermes Workspace flake input~~ | Ishii | J7 | **no longer active**; revisit later |
| NixOS module library | Ishii | Jigo | `/etc/nixos/nix/services/` |
| Forgejo | Toki (operator) | Ishii | self-hosted on `:3001` |
| Nextcloud | Nago (content) | Ishii (NixOS) | `:11080`, 33.0.5.1 |
| CryptPad | Okkoto (deploy) + Nago (UX) | Ishii | **NOT live** (Phase P7 to enable) |
| Mnemosyne (SQLite + dashboard) | Kohroku | Jigo | DB live, dashboard `:8765` **down** |
| ~~Honcho (semantic memory)~~ | ~~Mokku~~ | ~~Kohroku~~ | **REMOVED from scope** per J7 2026-07-09 |
| Karakeep (bookmark) | Mokku (taxonomy) | Jigo | **live** at `keep.starrwulfe.xyz` (PocketID OIDC) |
| AMB broker (Redis 6380) | Okkoto (builder) | Ishii (NixOS) | Phase 1A live; Phase 1C ACL partial |
| BSM secrets | J7 (bootstrap token) + San (consumer) | Ishii | canonical store |
| agenix secrets | Ishii | San | Phase 1C partial — 11 per-wolf `.age` files not yet on disk |
| Matrix Synapse (Outpost) | Okkoto + Ishii (provisioning) | J7 | lives on Outpost, not Mononoke |
| Stalwart mail (Yoseba) | Yakkuru (PIM) | Ishii | live; wolves' mailboxes declared but IMAP IDLE not wired |
| SearXNG (search) | San (consumer) | Ishii | `search.starrwulfe.xyz` |
| Telegram bot fleet (11 bots) | San | J7 | `Mononoke 🐺 Wolfpack` group is the dispatch home |
| Eye-of-Hermes PWA widget | San (status) | J7 | live at `:9120` proxied `/widget/` |
| **External coder workers** (5 CLIs) | Okkoto (operator) | Jigo | OpenCode · Kilocode-cli · Gemini-cli · Copilot-cli installed; **Claude Code** to add |

---

## 11. End-to-End Task Flow (target)

```
[J7 sends a request]
    │
    ▼  Telegram group OR Matrix DM
[San gateway, multiplex :8642]
    │  classify intent (wolf-council-routing)
    │  if multi-domain → Ashitaka for decomposition
    │  if code → Okkoto
    │  if NixOS → Ishii
    │  if research → Moro
    │  if memory → Kohroku
    │  if design → Nago
    │  if ops → Toki
    ▼
[Per-wolf gateway (or Ashitaka for dispatch)]
    │  read SOUL.md → load role + skills + dimensions
    │  open or attach to kanban card (hermes kanban)
    │  read packet if leaf card (packets/leaf-card-template.md)
    │  if destructive → state blocker → propose declarative candidate → ask J7
    │  **if project is new → create a dedicated Matrix room with all wolves as members,
    │   and wolves post status updates (claimed / started / blocked / done) there**
    │   (J7 directive; not optional — single feed of pack state)
    ▼
[Wolf executes]
    │  uses terminal / file / web / browser / delegate_task / skill tools
    │  writes artifacts to:
    │    • repo (commit + PR) for spec / playbook changes
    │    • Nextcloud vault path for documents (when Nextcloud identity wired)
    │    • Mnemosyne remember() for durable memory
    │    • per-profile state.db for session transcript
    ▼
[Wolf logs outcome]
    │  posts reply to Matrix DM (Gatewood feed) + project-status Matrix room
    │  updates kanban card → moves state (e.g. done / changes-requested)
    │  writes artifacts to agreed paths
    ▼
[Jigo reviews if elevated-risk or cross-wolf]
    │  config-first review mandate (jigo-review SKILL §0.5)
    │  challenge code-level solutions that haven't exhausted config-level audit
    ▼
[Ishii reviews if access/policy]
    │
    ▼
[J7 sees outcome in Telegram/Matrix thread + kanban card + repo commit]
```

---

## 12. Rollout Phases (current → target)

| Phase | Scope | State | Gate to next |
|---|---|---|---|
| **P0 — Stabilize multiplex + fix Ashitaka port 8643** | Ashitaka PID 20888 must bind `:8643`; investigate why no listener; per-wolf units already on `8644-8652` | [PARTIAL] — multiplex live, Ashitaka unbound | `ss -tlnp` shows PID 20888 → `:8643` |
| **P1 — wolfpack.nix adoption** | `services.wolfpack.enable = true`; per-wolf user units managed by NixOS module instead of ad-hoc `hermes-cli install` | [PLANNED] — module imported but `enable = false` | `nixos-rebuild switch --flake .#mononoke` smoke + ashitaka + toki alwaysOn verification |
| **P2 — Hermes Workspace revisit (deferred)** | J7 directive: **do not allocate resources now**; revisit after Mnemosyne + CryptPad land. Source stays at `hermes-workspace-src/` for future revival. | [PAUSED by J7 2026-07-09] | (no gate) |
| **P3 — Per-wolf Nextcloud identity** | Provision 10 wolf accounts + app passwords; bind to Okkoto (builder) and Nago (content) workflows | [NOT DONE] | Smoke write+read each wolf's vault dir |
| **P4 — Mnemosyne dashboard restore** | Restart `:8765` service via `bsm-secret-fetch-for-environmentfile.sh` helper per `nixos-host-operations` skill | [BROKEN] | Dashboard returns 200; recall round-trip works |
| **P5 — Karakeep OIDC end-to-end** | Confirm OIDC login via Pocket ID works for j7; document any provisioning quirks; tear down orphan podman attempt at `:3030` (if exists) | [LIVE — OIDC smoke pending] | J7 can sign in via Pocket ID passkey |
| **P6 — External coder workers: add Claude Code** | `pip install` or Nix profile install; pin version; mirror `.env` token requirements to `~/.hermes/.env` | [4/5 INSTALLED] | `which claude` returns binary path |
| **P7 — CryptPad enable + WebAuthn** | `services.cryptpad.enable = true`; manual passkey enrollment for j7; route `crypt.gatewood.xyz` via cloudflared | [NOT DONE] | First admin login succeeds; smoke write+share pad |
| **P8 — Phase 1C ACL finalization** | Wire `aclfile` into systemd ExecStartPre; provision 11 `amb-redis-<w>-password.age` files; rotate broker password | [PARTIAL] | Per-wolf Redis ACL isolation verified |
| **P9 — 9 missing Agent Cards** | Author 9 `wolves/{wolf}.yaml` cards from existing SOUL.md + skill inventory + wolfpack.nix `wolfDef.skills` | [PARTIAL — 2/11] | `amb_client.py._load_declared_dimensions` returns 11 cards |
| **P10 — Outpost Traefik fix** | `code.starrwulfe.xyz` route points to `100.77.7.1:3001` (was `127.0.0.1:3001`) | [BROKEN] | Public Forgejo URL returns 200 |
| **P11 — GBrain substrate spec** | (NEW per J7 2026-07-09) Define what GBrain is — repo, schema, ownership. Author `specs/gbrain-substrate.md` | [NOT DONE] | Spec committed; backlog E2-T1 unblocked |
| **P12 — Talk (`talk.gatewood.xyz`) routing fix** | Cloudflare IP-resolution asymmetry → IPv6 ULA on cloudflared | [BROKEN] | Talk video round-trip works |
| **P13 — Per-wolf git signing identities** | Provision GPG/SSH key per wolf; bind to git config so commits assert per-wolf authorship | [NOT DONE] | `git log` shows wolf-attributed commits |

---

## 13. Top 10 Unresolved Questions / Risks

| # | Risk | Severity | Owner | Mitigation |
|---|---|---|---|---|
| 1 | Mnemosyne dashboard down — memory write-side works, audit/read-side dark | **Critical** | Kohroku | Restart per `bsm-secret-fetch-for-environmentfile.sh` |
| 2 | Per-wolf Nextcloud identity absent — only `san` has one; wolves would auth as `san` if they wrote to Nextcloud | **High** | Nago + Ishii | Provision script + work item |
| 3 | Multiplex coexistence drift — both multiplex and 10 per-wolf gateways running; P0–P12 Megapack rebuild never executed | **High** | Ishii + Okkoto | Phase P0+P1 (this spec §12) |
| 4 | Ashitaka port 8643 unbound — PID 20888 alive but no listener (debug needed before P1 cleanup) | **Medium** | Ishii | Phase P0 (this spec §12) |
| 5 | 9 missing Agent Cards — agent card bridge from SOUL.md not implemented | **Medium** | Ashitaka + Okkoto | Author from SOUL.md + skill inventory |
| 6 | **GBrain substrate undefined** — in scope per J7 2026-07-09 but no spec, repo, or owner | **Medium** | J7 (owner TBD) | Phase P11 (this spec §12) |
| 7 | External coder workers: Claude Code missing — 4/5 installed (OpenCode, Kilocode, Gemini, Copilot installed; Claude Code to add) | **Medium** | Okkoto | Phase P6 (this spec §12) |
| 8 | Outpost Traefik points to `127.0.0.1:3001` — `code.starrwulfe.xyz` 404'd | **Medium** | Ishii + Toki | One-line sed in `dynamic.toml` + Traefik HUP |
| 9 | Talk (`talk.gatewood.xyz`) Cloudflare IP-resolution asymmetry — IPv6 ULA on cloudflared | **Medium** | Ishii | Disable cloudflared route or fix DNS record |
| 10 | agenix per-wolf secret files not yet on disk — only master password file exists; Phase 1C ACL module not yet wired | **Medium** | Ishii | Generate 11 `.age` files + wire `aclfile` directive |

**Intentionally de-scoped** (per J7 directive 2026-07-09): Hermes Workspace revival (paused until later phase); Honcho semantic memory stack (removed from scope, Mnemosyne is canonical).

---

## 14. Recommendations (separate from spec)

These are non-binding suggestions for J7 to consider; they are NOT part of the canonical spec.

- **Define GBrain in a sibling spec** (`specs/gbrain-substrate.md`) before Phase P11 starts. Include ownership, schema, runtime topology, and how it differs from Mnemosyne (per the directive: GBrain **in**, Honcho **out**).
- **Land the canonicalized version of this spec as a PR** to `j7/StarrOS` `main` so it becomes the integration overview that other docs reference.
- **Add `specs/starros-stack-spec.md` to the `prompts/san-handoff.md` reading list** so future San runs ingest it as ground truth.
- **Diagnose why Ashitaka PID 20888 doesn't bind `:8643`** before P0 closes. May be a `--profile ashitaka` flag difference vs the working wolves (their cmdlines include `--profile <wolf>` — Ashitaka's does not; the missing `--replace` flag on the PID-20888 cmdline is consistent with the wolfpack.nix default port-order but not with the actual binding).

---

## 15. Provenance

This spec was authored by San from:

- The 2201-byte stub on `main` (commit sha `cdaaa0263…`, file sha `908aae4a…`)
- ADRs 0001 and 0002
- `docs/playbook.md` "Required sections"
- `kanban/{board-schema,backlog}.md`
- `wolfpack.nix` (`/etc/nixos/nix/services/wolfpack.nix`)
- `wolfpack-dashboard-data-contract.md` (`~/.hermes/skills/devops/hermes-multi-profile-architecture/references/`)
- `~/.hermes/wolf-souls/<wolf>/` and `~/.hermes/profiles/<wolf>/SOUL.md`
- `/nas/hdd/agent-shared/agent-cards/wolves/{san,ashitaka}.yaml`
- `/nas/hdd/agent-shared/wiki/projects/starrOS-to-megapack-transfer.md`
- The two prior San audit reports (`~/.hermes/cron/output/2026-07-07_mononoke_superapp_architecture_dossier.md` and `…_wolfpack_audit_round2.md`)

Ground-truth tag legend: `[WORKING]` verified live · `[PARTIAL]` wired but incomplete · `[PLANNED]` declared · `[BROKEN]` declared but failing · `[UNKNOWN]` not verifiable this pass.