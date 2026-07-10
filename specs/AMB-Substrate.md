---
title: AMB Substrate — Agent Mesh Bus (canonical integration spec)
status: DRAFT for San/Jigo review — folds a2a-amb-kanban-prexx-20260630 into StarrOS
date: 2026-07-10
author: external reviewer (Claude), reconciled from wolfpack artifacts 1–9
supersedes: the ADR-0003 glossary one-liner for AMB; closes shakedown audit issue #6
---

# AMB Substrate

## 0. What belongs here vs. the canonical spec vs. runtime-state

This spec is the **design contract** for inter-agent communication: the bus, the
envelope, the channel topology, the gateway handler contract, and the loop-safety
rules. It is the single home for "how do wolves signal each other."

- **Live runtime facts** (what's bound on `:6380` right now, ACL user list, stream
  entry counts) live in `docs/runtime-state.md` §2 and are referenced here, not
  duplicated.
- **Task/handoff state** lives on the Kanban blackboard (`kanban/`) and in the wiki/
  Mnemosyne. The bus carries *signals about* state; it does not carry state.
- **A2A protocol compliance** is addressed in §8 as a position, not a claim.

The governing principle, stated once: **signals on the bus, state on the
blackboard.** A wolf finishing work writes the result to the Kanban card (state),
emits exactly one event on the bus (signal), and stops. The next wolf reads the
card for content, not the message. No wolf ever conversationally replies to
another wolf. There is no conversation to loop.

## 1. What AMB is

AMB (Agent Mesh Bus) is a **Redis-Streams message bus** on `:6380` (Mononoke,
`127.0.0.1`-bound) that wolves use to signal each other and to wake on inbound
work. It is Hermes-internal and wolfpack-specific. It is **not** an A2A-protocol
endpoint (see §8), and it is **not** a chat medium — human↔agent chat stays on
Telegram/Matrix/email; agent↔agent coordination is AMB-only.

**Current reality (2026-07-10):** the broker is live, 12 ACL users are wired,
`amb:pack.broadcast` has ~41 real entries — but **every wolf is read-only** and
**no consumer has registered a group** (`groups: 0` on every stream). The bus is
built and proven on the wire; it is not yet carrying end-to-end traffic. Closing
that gap is the near-term charter (§9).

## 2. Broker & transport

**Primitive: Redis Streams, exclusively.** `XADD` to publish, `XREADGROUP … BLOCK 0
STREAMS <topic> >` to consume, `XACK` to acknowledge, `XAUTOCLAIM` for stuck-message
recovery. No `PUBLISH`/`SUBSCRIBE` anywhere — pub/sub loses messages on disconnect
and Streams do not, which is the correct choice and is canonical.

**Deployment:** `services.redis.servers.amb` via `/etc/nixos/nix/services/amb-redis.nix`
(Phase 1A, deployed). `appendOnly = true`, `appendfsync = everysec`,
`maxmemory-policy = noeviction`. NO_EVICTION is load-bearing: under memory pressure
Redis must block, never silently drop stream entries a slow consumer hasn't read.

**Delivery guarantee: at-least-once.** AOF + NO_EVICTION + ACK-after-process means a
broker restart or slow consumer replays rather than drops. Exactly-once is **not**
provided; duplicate delivery on retry is expected and must be absorbed by consumer-
side idempotency (§6, rule 4). This is the right guarantee for an agent bus; do not
try to make it exactly-once.

**Auth:** agenix-managed passwords (one per wolf + admin + default) + Redis ACL. The
`aclfile` directive supersedes `requirepass` under Redis 8; the default user's hash
is the sole legacy auth path and should be treated as an operator backdoor, not a
wolf identity.

## 3. Channel topology (canonical)

There is a live gulf between the **deployed ACL** (dotted, legacy:
`amb:wolf.<w>.event`) and the **A2 channel registry** (colon-separated, current:
`amb:<wolf>:dispatch`). This spec resolves it.

**Canonical form is colon-separated** per A2 naming rules (`amb:` prefix, `:`
separator, no dots, underscore over hyphen). The dotted `amb:wolf.<w>.*` channels are
**legacy — migrate and retire.** The ACL must be re-rendered to grant the colon
channels; until then, code targeting `amb:<wolf>:dispatch` writes to a channel no ACL
permits, which is the root of the "read-only wolves" gulf.

**Canonical channel set:**

| Channel | Kind | Writer | Readers | Purpose |
|---|---|---|---|---|
| `amb:<wolf>:dispatch` | inbox | San + any wolf | owner wolf | point-to-point work handoff |
| `amb:<wolf>:status` | outbox | owner wolf | San + interested wolves | progress/result signals |
| `amb:<wolf>:handoff` | inbox | any wolf | owner wolf | context transfer |
| `amb:<wolf>:escalation:c{4,5}` | inbox | risk-triager dim | owner wolf + San | severity-gated escalation |
| `amb:pack.broadcast` | broadcast | **San only** | all wolves | pack-wide, **non-respondable** |
| `amb:kanban:task:{created,completed,blocked}` | signal | kanban watcher | San + dispatch rules | state→signal fan-out (§7) |
| `amb:system.heartbeat` | signal | consumer daemons | San/observability | liveness, **non-respondable** |
| `amb:circuit:{open,closed}` | signal | circuit breaker | all wolves | storm-guard state (§6) |
| `amb:stuck` | signal | broker/daemon | San | N-of-M stuck escalation |

**Write-side ACL (the current blocker).** Each wolf needs `+xadd` on its own
`amb:<wolf>:status`/`:dispatch` outbound channels and on the peer inbox channels it
must hand off to — **not** blanket `+@write`. `amb:pack.broadcast` is **San-write-only**;
enforce "producers must be San" at the ACL, not just by convention (today any wolf
could publish to broadcast — a loop amplifier). Broadcast and all `signal`-kind
channels are **non-respondable by rule** (§6).

## 4. Message envelope

The shipped `hermes_amb.Envelope` (v1.0) is canonical, with three corrections:

**(a) Pin the stream field key.** Live entries appear under both `e` (legacy) and
`data` (current) — drift between Phase 1A and 1B publishers. Canonical is **`data`**;
consumers must tolerate `e` during migration, and publishers must stop emitting `e`.

**(b) Promote two IDs to first-class header fields.** Today `task_id` is
payload-only and there is no thread/context grouping. Add:
- **`context_id`** (required for any multi-step interaction) — groups related
  envelopes into one logical thread. This is not A2A-decoration; it is the anchor
  the turn-budget loop guard counts against (§6, rule 3). Without it you cannot
  detect a runaway chain.
- **`task_id`** (optional header, when the envelope relates to a Kanban card) —
  promoted out of payload so the state↔signal wiring (§7) and audit trail key on a
  header field, not free-form payload.

**(c) Populate `message_id` post-XADD.** The broker-assigned entry id must be written
back via `with_message_id(entry_id)`; null `message_id` on the wire (as seen in the
2026-07-07 smoke tests) breaks dedup and audit correlation.

**Canonical required header (9):** `amb_version`, `timestamp`, `kind`
(`event`|`command`), `source_wolf`, `origin_dimension_id`, `target_topic`, `payload`,
`context_id`, `message_id` (post-publish). **Optional:** `task_id`, `recipient`,
`dispatch_hint`, `signature`, `sequence_id`, `escalation_class`, `severity`.

## 5. Gateway handler contract (the anti-loop core)

**This is the single most important section and the design is already mostly built
in B2.** The rule is: **classify first, invoke on demand — never auto-invoke.**

Every inbound envelope, at every wolf's gateway, passes through the B2 decision tree
(`Handlers.envelope_received` → `Disposition`) **before** any LLM turn. B2 is a pure
router; it emits an action set, not a response. The gateway executes that action set.
The LLM is woken **only** when `needs_llm_turn == True`.

Canonical action semantics (from B2's matrix):
- `llm_turn` → wake the wolf with the envelope as context (the only path that costs a
  model call)
- `kanban_comment` / `kanban_block` → mutate the blackboard, no turn
- `escalate` → Matrix/Telegram ping to J7, no turn
- `local_state_update` → scratchpad/handoff update, no turn
- `log_only` → log + `XACK`, no turn (this is the default for heartbeats, events,
  and anything not addressed to this wolf as actionable work)

**Terminal-by-default.** A woken wolf completes its turn, writes results to the
Kanban card, emits **at most one** outbound envelope (a `:status` signal), and stops.
It does not react to its own emission. The gateway default is **not** "wake me on
everything"; it is "classify everything, wake me on work." Ratify option (B) from
artifact 7 as canonical, with per-wolf operator override (option C) as the only
escape hatch. Option (A) auto-invoke is **prohibited** — it is the loop generator.

## 6. Anti-loop rules

Belt-and-suspenders, enforced at gateway middleware so they hold even when a wolf
misbehaves. Current status noted per rule.

1. **Classify-first / terminal-by-default** (§5). *Status: built in B2, needs to be
   the wired gateway default.*
2. **Signals are never answered.** Every `signal`-kind and `broadcast` channel is
   non-respondable by construction; an event/FYI terminates. *Status: falls out of
   B2 `log_only`; make it a hard middleware rule, not a matrix row.*
3. **`context_id` + turn budget.** Every multi-step interaction carries a `context_id`;
   the gateway drops auto-messages once a context exceeds a turn budget (default 6)
   and escalates to San/J7. *Status: `context_id` MISSING (§4 adds it); turn budget
   MISSING — highest-priority new work.*
4. **Dedup / idempotency.** Reprocessing a `message_id` is a no-op. *Status: MISSING —
   `hermes_amb.dedup.DedupHelper` referenced but not implemented; at-least-once makes
   this mandatory, not optional.*
5. **Self-echo suppression.** A wolf ignores envelopes bearing its own `source_wolf`.
   *Status: PARTIAL — exists only on the Matrix-fallback path (C6 gate); extend to the
   AMB broadcast/dispatch path.*
6. **Point-to-point inboxes; broadcast non-respondable + San-only** (§3). *Status:
   topology supports it; ACL enforcement of San-only broadcast is MISSING.*

**Storm backstop.** Ishii's CircuitBreaker spec (`mnemosyne-boundary-crossings.md`
§4: N=3, `T_dwell=300s`, per-wolf, one-shot per incident) is the coarse safety net
beneath rules 1–6 — when the fine-grained guards fail, the breaker trips a wolf's
outbound path and emits `amb:circuit:open`. *Status: spec is binding for Phase 1E;
no `CircuitBreaker` class shipped.* The 2026-06-29 heartbeat→seen→witness storm
(~50 events/60s) is the incident this backstops; note it happened on the **hermes
gateway path with no AMB involvement**, which confirms the loop is a property of the
handler contract (§5), not the transport.

## 7. State↔signal wiring (fixes the founding incident)

The incident J7 cited as the reason for building AMB: card T11 (`t_a637df43`) should
have auto-dispatched Okkoto on completion of T8 and didn't — there is no code path
from `kanban.task.completed` to dispatching the next assignee. The notify-only
`kanban_watchers.py:113` poller observes but never re-enters the dispatcher.

**Canonical chain (loop-safe):**
1. Card transitions to `done` → `kanban_watchers.py` publishes **one** event to
   `amb:kanban:task:completed` carrying `task_id` + `context_id` (the ~45 LOC sibling
   row-diff branch from architecture §3.4).
2. San's consumer (or a dispatch rule) reads the event, and if the card defines a
   next assignee, creates the next card and writes to `amb:<next-wolf>:dispatch`.
3. The next wolf's gateway classifies (§5), does the work, updates the card, emits one
   `:status` signal, and stops.

**Why this cannot loop:** the completion event is a signal (rule 2 — not answered);
the chain advances only by explicit, idempotent card-state transitions (rule 4); each
step shares a `context_id` so the turn budget (rule 3) caps any runaway. This is the
exact point where the missing-signal problem (the founding incident) and the
cascading-signal problem (chat-looping) are solved by one mechanism.

Reverse direction (AMB event → Kanban mutation, architecture §3.3) uses the same
`task_id` key. AMB→wiki is out of scope until a concrete need exists — do not build
it speculatively.

## 8. A2A alignment — position, not claim

**The wolfpack is not A2A-compliant, and should not chase full wire-compliance now.**
The self-assessment in artifact 6 is accurate: internal agent cards (wrong schema,
unserved), no task object/state machine, Redis Streams instead of JSON-RPC-2.0-over-
HTTP, no SSE, no webhook, no `contextId`. That verdict is correct.

**The reason not to chase it:** A2A's transport is fundamentally different (JSON-RPC/
HTTP/SSE) from what you built (Redis Streams). Full compliance means either replacing
Streams — throwing away persistence, at-least-once, and ACLs you've earned — or
building an A2A-facade gateway that translates. The facade is the right *eventual*
move, but it only earns its keep when you talk to **external** agents. For an internal
11-wolf pack you control end to end, it is premature.

**What to adopt from A2A now, because these are loop-safety primitives regardless of
wire format:**
- **The task lifecycle model.** A2A's eight states (submitted, working,
  input_required, auth_required, completed, failed, canceled, rejected) include the
  terminal and interrupt states your Kanban set (`todo/in_progress/done/blocked/
  archived`) lacks. Terminal states are what make an interaction *end*. Map your
  Kanban states onto this model and treat a task as terminating — adopt the model,
  not the wire.
- **`contextId`** (§4). Load-bearing for the turn budget; not optional decoration.

**Defer:** `role`+`parts[]` message shape, `/.well-known/agent-card.json` serving,
JSON-RPC transport, SSE/webhook. **Keep parked:** Phase 1D `a2a_tool.py`, correctly
gated on the first compatible upstream `a2a-sdk` release (Q7 = WAIT).

**Where you only *look* compliant (flag these so nobody over-claims):** the internal
"agent cards" share almost no schema with A2A `AgentCard` and aren't served anywhere;
`payload.task_id` looks like A2A's `taskId` but is payload-level with no task object
behind it; the `amb:req.<from>.<to>:<uuid>` convention looks like `contextId` but is a
per-request-pair pattern, documented-not-wired, and does not durably thread a
conversation.

## 9. Current-state gulf & migration

Honest inventory of what stands between "built" and "carrying traffic":

1. **Wolves are read-only.** The live ACL emits `+@read` only; any wolf publish fails
   `NOPERM`. Write-side ACL wiring (§3) is the top blocker. *(Phase 1C/2, Ishii.)*
2. **No consumer has registered a group** (`groups: 0`). The B1 daemon template
   exists but no per-wolf consumer is running. *(Phase 2, B3 — module written,
   deploy deferred.)*
3. **Two deploys are gated on a pre-existing flake-hygiene blocker** (dirty
   `flake.lock`, NAR hash mismatch on `path:/home/san/.hermes/hermes-agent`) — **not**
   an AMB defect. A3 and B3 activation wait on it. *(Owner: San, flake hygiene.)*
4. **Loop guards 3–4 unbuilt** (`context_id`, turn budget, dedup). These are new work,
   not migration.
5. **Dimension channels (C8) are spec-only** — registry + `channels.py` constants
   exist; no ACL, no producer. Fine to leave dormant until a dimension actually needs
   its own channel.

## 10. Open decisions for J7

- **D-AMB-1:** Ratify classify-first (§5 option B) as the canonical gateway default,
  prohibiting auto-invoke. *(Recommended: yes — it's your loop fix and it's built.)*
- **D-AMB-2:** Adopt the A2A task-state model + `context_id` now; defer wire-
  compliance until external federation. *(Recommended: yes.)*
- **D-AMB-3:** Confirm `amb:pack.broadcast` is San-write-only at the ACL, not just by
  convention. *(Recommended: yes.)*
- **D-AMB-4:** Sequence the write-side ACL + first consumer group ahead of the loop-
  guard work, so the bus carries real traffic before it carries complex traffic.

## Sources

Reconciled from `a2a-amb-kanban-prexx-20260630` artifacts 1–9 (INVENTORY +
Artifacts 2–9), the live `:6380` broker probes (2026-07-10), `hermes_amb/`
(`envelope.py`, `client.py`, `dispatch.py`, `channels.py`, `matrix_fallback.py`),
`documents/a2-deliverable.md`, `documents/b2-deliverable.md`,
`documents/prexx-part2-architecture.md` §3, `documents/mnemosyne-boundary-crossings.md`
§4, and the A2A protocol specification (a2a-protocol.org, task lifecycle) for the
alignment position in §8.