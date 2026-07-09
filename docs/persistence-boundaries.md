# Persistence Boundaries

> **Purpose:** single answer to "where do I write this?" — concern → canonical store → write path → reader(s) → retention purpose → examples.
> **Owner:** San
> **Source-of-truth:** this file is a *map*; each row's "canonical store" column points at the source-of-truth doc for that store.

| Concern | Canonical store | Write path | Reader(s) | Retention | Example |
|---|---|---|---|---|---|
| Planning artifacts (specs, ADRs, playbooks, packets, prompts, kanban seed) | `j7/StarrOS` repo on Forgejo | git commit + PR (review gate per `docs/playbook.md`) | San, wolves, J7, reviewers | Indefinite (git history) | `specs/starros-stack-spec.md`, `decisions/0001-…md` |
| Runtime state (live ports, broken services, drift) | `docs/runtime-state.md` (this repo) | PR after audit | San + J7 + ops wolves | Rewritten weekly; supersedes previous | "Ashitaka PID 20888 alive but unbound on :8643" |
| Per-wolf canonical identity (SOUL.md, profile.yaml, dimensions) | `~/.hermes/profiles/<wolf>/SOUL.md` and `profile.yaml` | `wolfpack.nix` activationScript seeds defaults; San signs off on changes | the wolf + San + J7 | Versioned; backup on NixOS rebuild | `~/.hermes/profiles/ashitaka/SOUL.md` |
| Per-wolf runtime config (`config.yaml` — model, tools, agents) | `~/.hermes/profiles/<wolf>/config.yaml` | the wolf edits via terminal | the wolf + San (audit) | Versioned; rotates on model change | `~/.hermes/profiles/okkoto/config.yaml` |
| Per-wolf session transcript (current conversation) | `~/.hermes/profiles/<wolf>/state.db` (SQLite) | the wolf writes on every turn | the wolf + session_search | Rolling; 90d retention | current Telegram DM |
| Pack telemetry (counts, errors, last-seen per wolf) | `wolfpack.db` (SQLite, declared by `wolfpack.nix` activationScript) | per-wolf gateway writes on activity | Mission Control dashboard (Phase P2) + San | Indefinite (rotates after 1y) | wolf row in `wolves` table |
| Agent memory (lessons, claims, scratch) | Mnemosyne (`~/.hermes/mnemosyne/data/mnemosyne.db`) | `mnemosyne_remember` (per-wolf) | any wolf via `mnemosyne_recall` | BEAM tiers; rolling episodic | "Ashitaka routing heuristic" |
| Project substrate (per-project decisions, spec history, open questions) | **GBrain** (TBD) — `specs/gbrain-substrate.md` | per-wolf `gbrain_client` API; project-Matrix-bot listener | San + project owner + J7 | Indefinite (append-only) | "E1-T5 GBrain spec drafted 2026-07-09" |
| Bookmark / link archive | Karakeep (`keep.starrwulfe.xyz`) | Mokku or any wolf via OIDC | any wolf + J7 | Indefinite | tagged bookmarks under `mokku/` |
| Real-time colab docs | CryptPad (TBD) | per-wolf (Phase P7) | any wolf + J7 | Indefinite | shared CryptPad for the Megapack design review |
| Long-form docs (current/vault) | Nextcloud (`cloud.gatewood.xyz`) | per-wolf via OIDC (Phase P3) | any wolf + J7 | Indefinite | `/Megapack/Playbook-2026-Q3.md` |
| Card state (kanban) | Hermes Kanban (per-board SQLite at `~/.hermes/kanban/boards/<slug>/kanban.db`) | wolves via `hermes kanban` CLI; San via dispatch | San + wolves + J7 | Indefinite; archived boards frozen | `agent-os-cryptpad-mvp/kanban.db` |
| Email | Stalwart (Yoseba) — per-wolf mailbox `<wolf>@agent.starrwulfe.xyz` | per-wolf via SMTP submission | per-wolf via IMAP IDLE (planned) | Indefinite | wolf's mailbox |
| Chat (real-time) | Matrix (Synapse on Outpost) | per-wolf via Matrix client | per-wolf + J7 + room members | Indefinite (server-side) | `!JLSvRb…` StarrOS Development room |
| Public chat dispatch | Telegram (`Mononoke 🐺 Wolfpack` group + per-bot DMs) | per-wolf via Telegram bot | J7 + group members | Indefinite (server-side) | alerts thread 11691 |
| Web search | SearXNG (`search.starrwulfe.xyz`) | per-wolf via Hermes web search tool | per-wolf | 90d cached results | open-web-search v0.18.0 |
| Secrets — runtime | BSM (synced to `~/.hermes/.env`) | `hermes secrets bitwarden set` or BSM web UI | each wolf (own scope) | BSM-managed | `TELEGRAM_BOT_TOKEN` |
| Secrets — NixOS service layer | agenix (`/etc/nixos/secrets/*.age`) | agenix rekey + NixOS rebuild | the NixOS service owner | indefinite (age) | `amb-redis-ashitaka-password.age` |
| Audit logs | `~/.hermes/logs/*.log` (per-wolf) | each wolf on activity | San + J7 (audit) | rolling 30d | `~/.hermes/logs/gateway-<wolf>.log` |
| Build artifacts / drop-off | `~/.hermes/audio_cache/`, `~/.hermes/Downloads/`, `~/.hermes/voice-memos/` | the wolf | the wolf | manual | TTS outputs, generated images |

## Notes

- **Mnemosyne and GBrain are siblings**, not parent/child. Mnemosyne = agent memory; GBrain = project memory.
- **Per-profile `state.db` is ephemeral** — it is the live conversation, not the durable record. After 90d it rolls; for long-term storage, the wolf or San should `mnemosyne_remember` the durable parts.
- **Heroes are 12, not 13.** Honcho is removed from scope per J7 2026-07-09 (see `docs/runtime-state.md` §"De-scoped" historical note).
