# ADR 0003: Canonical spec boundaries

Date: 2026-07-09
Status: Accepted
Supersedes: none

## Context

`specs/starros-stack-spec.md` is the integration overview for StarrOS. As the spec grew during the 2026-07-09 cleanup pass, it accumulated runtime-state, broken-items, and debug-notebook cross-references that made it harder to read and easier to drift from.

## Decision

`specs/starros-stack-spec.md` is the **target architecture** only. It does not document:

- live ports, broken services, deployment drift → `docs/runtime-state.md`
- where durable state lives → `docs/persistence-boundaries.md`
- external coder worker policy → `docs/external-workers.md`
- per-card backlog / phase status → `kanban/backlog.md`

Operational ephemeral facts may appear in the spec *only* in two cases:

- They are part of the **target architecture** (e.g. "Mission Control is a Next.js 15 shell") and a single inline qualifier like `[currently paused]` is sufficient.
- They are needed to disambiguate from another component (e.g. "Hermes Workspace" vs "Mission Control" — see `decisions/0003` §Glossary).

## Consequences

- `specs/starros-stack-spec.md` shrinks and stabilizes; readers can rely on it as architecture, not as a snapshot.
- `docs/runtime-state.md` becomes the live companion; reviewers know to check both.
- `docs/persistence-boundaries.md` answers "where do I write this?" once.
- `docs/external-workers.md` answers "can this leaf card be done by Claude Code?" once.
- `kanban/backlog.md` remains the per-card plan; the spec links to it, not the other way around.

## Glossary (terminology discipline)

| Term | Meaning | Status |
|---|---|---|
| **StarrOS** | The whole project. | live |
| **wolfpack** | San + 10 wolves. | live |
| **Mission Control** | The target workspace shell (Next.js 15). | **paused** (J7 2026-07-09) |
| **Hermes Workspace** | The upstream `inputs.hermes-workspace` flake input that the Mission Control NixOS module imports. **Unrelated to the `hermes-workspace-src/` source directory** — that directory holds the paused Mission Control source code, not the killed flake input. | **killed** (J7 2026-07-09, intentionally — not the same as Mission Control) |
| **Hermes Dashboard** | Stock Hermes dashboard at `http://100.77.7.1:9119` (basic-auth `j7`/scrypt). | live; embedded in Mission Control when live |
| **Eye-of-Hermes** | PWA status widget at `:9120` proxied at `/widget/`. | live |
| **external coder workers** | The 5 CLIs in `docs/external-workers.md`. | partial (4/5 installed) |
| **Mnemosyne** | Primary agent memory layer. | live (dashboard down — runtime-state) |
| **GBrain** | Project substrate (in scope per J7 2026-07-09). | spec only (Phase P11) |
| **Honcho** | Semantic memory stack. | **decommission pending** (J7 2026-07-09: no combine-with-Mnemosyne needed; container still live, see `runtime-state.md` §2) |
| **AMB** | Agent Mesh Bus (Redis broker on `:6380`). **Phase 1A** = broker live + plain requirepass; **Phase 1C** = per-wolf ACL material finalized (current P8 scope). | Phase 1A live; Phase 1C partial |

## Supersedes

- The 2026-07-09 v1.1 canonicalization of `specs/starros-stack-spec.md` did not yet have this decision in place. v2.0 (this PR) implements the split.
