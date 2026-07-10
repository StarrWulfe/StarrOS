# GBrain Substrate

> **Status:** DRAFT (2026-07-09) — in scope per J7 directive 2026-07-09. No implementation yet. See `kanban/backlog.md` E1-T3 (GBrain spec authoring) + rollout Phase P11.
> **Owner:** TBD (J7 to assign — likely Ashitaka for orchestration, Okkoto for build).
> **Related:** `specs/starros-stack-spec.md` §8 (memory), `docs/persistence-boundaries.md`, `kanban/backlog.md`.

## 1. Purpose

GBrain is the **project substrate** for StarrOS — the durable, queryable, per-project store of decisions, specs, and outcomes. It complements (does not replace) Mnemosyne:

- **Mnemosyne** is the *agent memory layer*: short notes, lessons learned, identity claims. Per-agent or shared with `author_id` / `channel_id` scoping.
- **GBrain** is the *project memory layer*: per-project spec history, decision logs with rationale, link graph between docs / cards / commits.

## 2. Confirmed facts

- "GBrain" is referenced in `kanban/backlog.md` E2-T1 ("OKF/GBrain substrate") and in `prompts/fable-global.md`. The legacy `OKF/` prefix is a typo; the project is **GBrain**.
- J7 directive 2026-07-09: **GBrain in scope; Honcho out.**
- The pack already has related substrates that GBrain must not duplicate: Mnemosyne (agent memory), `wolfpack.db` (per-wolf telemetry), Forgejo (repo of record), kanban (task state).

## 3. Assumptions (to validate)

- GBrain is **per-project**, not per-wolf and not global. Each StarrOS project gets its own GBrain partition or DB.
- GBrain is **append-only by default**; corrections create new entries that supersede old ones (no destructive edits).
- GBrain is **read-by-wolves**; only the owning wolf + San + the project's owner write.
- GBrain is **durable**; it does not lose data on container restart, profile re-creation, or human changeover.

## 4. What GBrain stores (proposed)

| Kind | Example | Source |
|---|---|---|
| Decision log entry | "We chose Forgejo over Gitea for X reason" | San / Ashitaka / Jigo when a decision is finalized |
| Spec version pointer | "Mission Control tab set is now Overview/Agents/Tasks/Schedule/Content/Council" | Project `specs/*.md` head commit |
| Open-question entry | "What does GBrain own vs Mnemosyne?" | San or J7 when a question is parked |
| Cross-card link | "Card A inherits from card B; card B references spec §X" | `hermes kanban` events |
| Acceptance-criteria diff | "Card X was accepted with these changes" | Jigo / J7 review outcome |
| Rollout phase evidence | "Phase P6 closed because P6-gate met" | San / J7 |

## 5. What GBrain does NOT store (proposed)

- **Agent working memory**: that is Mnemosyne.
- **Wolf runtime telemetry**: that is `wolfpack.db` (counts, errors, last-seen).
- **Code, specs, packets, ADRs**: those live in Forgejo (ADR 0001). GBrain points at them; it does not duplicate them.
- **Live port maps / broken services**: `docs/runtime-state.md`.
- **Secrets / tokens**: BSM.
- **Chat / Matrix / Telegram content**: those are operational stores; GBrain reads from them but does not retain transcripts.

## 6. How GBrain differs from Mnemosyne

| | Mnemosyne | GBrain |
|---|---|---|
| Scope | agent / pack | per-project |
| Granularity | short notes | structured records |
| Lifetime | rolling, episodic compression | append-only, durable |
| Read by | wolves + San | wolves + San + humans (read-only web view) |
| Write by | any wolf (with `author_id`) | San + project owner + J7 |
| Storage | SQLite at `~/.hermes/mnemosyne/data/mnemosyne.db` | TBD — see §7 |

## 7. Implementation boundaries (proposed)

- **Storage**: SQLite, one DB per project, at `/var/lib/gbrain/<project-slug>.db` (NVMe). No Postgres dependency in v1.
- **API**: HTTP + Matrix-bot API surface. Per-wolf access via `gbrain_client` Python module, mirror of `mnemosyne_remember` / `mnemosyne_recall`.
- **Matrix bot**: `@<project-slug>-brain:mtrx.starrwulfe.xyz` listens in the project's Matrix room; wolves can `/recall`, `/decide`, `/park-question`.
- **Retention**: indefinite (append-only).
- **Search**: FTS5 + tag filter.

## 8. How GBrain relates to existing systems

- **Repo (Forgejo)**: GBrain stores pointers (sha + path) to canonical docs, not the doc bodies. Repo is source of truth for content; GBrain is source of truth for the project's narrative thread.
- **Kanban (Hermes Kanban)**: every card state transition emits a GBrain event ("card C moved to done; spec §X updated").
- **Nextcloud**: GBrain archives quarterly snapshots of project state into the project's Nextcloud vault directory for human-readable audit.
- **Wolfpack runtime (`wolfpack.db`)**: GBrain does not own per-wolf runtime telemetry. Wolfpack remains the source of truth for "what is each wolf doing right now"; GBrain is the source of truth for "what did the project decide and why."

## 9. Open decisions for J7

- **Owner**: Ashitaka (orchestration), Okkoto (build), Mokku (taxonomy), or San (overall)? Recommendation: Ashitaka primary, Okkoto implementation.
- **Where GBrain lives**: Mononoke only, or also Outpost for redundancy? Recommendation: Mononoke only in v1; backup to `/nas/hdd/agent-shared/gbrain/` daily.
- **Granularity of "project"**: one GBrain per J7-named project, or one per StarrOS-wide initiative? Recommendation: one per J7-named project (e.g. `gbrain/agent-os-cryptpad-mvp`, `gbrain/starros-doc-canon`).
- **Matrix bot accounts**: created in v1, or API-only? Recommendation: API-only in v1, bot in v2.
- **What does Phase P11 actually deliver — spec only, or spec + a working skeleton?** Recommendation: spec only, since this PR is the spec; P11 commit then triggers a follow-up PR for the skeleton.
