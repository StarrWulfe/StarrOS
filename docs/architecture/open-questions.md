# Architecture Open Questions — StarrOS

> **Purpose:** Live architectural questions whose answer is not yet known, not yet committed to a spec, or pending a Phase transition. Each entry is one question with the current evidence snapshot, the transition criteria that close it, and the destination card/decision where the answer lands. Re-audited when phases advance; entries that resolve should be moved to `decisions/0004-*.md` or rolled into `specs/starros-stack-spec.md` and removed from this file.
>
> **Owner:** San (writer) + Ishii (Phase 1A/1C ACL authority) + Jigo (verification on close).

---

## OQ-1 — Is "plain requirepass" on `:6380` the intended interim posture, and what proves the Phase 1A → 1C transition is complete?

**Source / trigger.** Jigo minor #5 from the PR #8 pre-Sprint-0 review (2026-07-09). Row-level labels for Phase 1A / Phase 1C are consistent across `specs/starros-stack-spec.md` §3 line 60 ("Phase 1A live, Phase 1C partial"), `docs/runtime-state.md` §2 line 40 ("Phase 1A live; Phase 1C ACL finalization in progress (P8)"), and `decisions/0003-canonical-spec-boundaries.md` glossary line 47 ("Phase 1A = broker live + plain requirepass; Phase 1C = per-wolf ACL material finalized"), but **no doc asserted that the live `:6380` AMB broker was actually running plain requirepass**, and the "plain requirepass" interim posture was not explicitly named as the intended Phase 1A security shape.

**Verification (live, 2026-07-10, by ishii@run-13 on Mononoke).** Read the rendered `/run/redis-amb/nixos.conf` that the upstream `redis-amb-prep-conf` writes for the broker. It contains exactly two effective directives:

```
include "/nix/store/avy38wgs8xjskssak0xnwbx124077974-redis.conf"
requirepass Bie0sYHP9TYLv9IvNUNXkGJpemCD5XKjk3u426HA
```

`redis-cli -h 127.0.0.1 -p 6380 PING` returns `NOAUTH Authentication required.` with no credentials, confirming the broker enforces authentication on every connection. **No `aclfile` directive is emitted** — despite `settings.aclfile = toString config.services.amb-redis.acl.aclFile;` being declared in `/etc/nixos/nix/services/amb-redis.nix` line 102, the upstream NixOS redis module's prep-conf only writes `requirepass`, not `aclfile` (the rendered ACL file at `/nix/store/*-amb-redis-acl-on.conf` exists in the nix store but is never loaded by the broker). So the live broker is exactly **plain requirepass Phase 1A** as the spec / runtime / glossary claim.

**Implication for "is plain requirepass the intended interim posture?"** Yes — by NixOS-module source-of-truth and by broker runtime, this is the intended Phase 1A security shape: a single shared `requirepass` (the agenix-decrypted `amb-redis-password` materialised at `/run/agenix/amb-redis-password`), no per-wolf ACL isolation, all wolfpack AMB clients share one credential. This is the "transition posture" — adequate for AMB wire-up (Phase 1B spike `t_b9c3a8a5`) and Pack communication, but not the target posture.

**Phase 1A → Phase 1C transition criteria** (the answer that closes this open question; tracked on E3-T9):

1. **ACL file is loaded by the broker.** Render `/run/redis-amb/nixos.conf` (or equivalent) contains `aclfile /nix/store/...-amb-redis-acl-on.conf`. Today this directive is declared in the module but not emitted — this is the live gap.
2. **All 11 per-wolf users authenticate via their agenix secret** (`/run/agenix/amb-redis-<wolf>-password`) rather than the shared requirepass. Verified by `redis-cli --user <wolf> --pass-file /run/agenix/amb-redis-<wolf>-password -p 6380 ACL WHOAMI` returning `<wolf>` and `<wolf>`'s permissions.
3. **Default user's permissions are narrowed** to operator-only (`+@all -@dangerous` or similar) once `aclfile` supersedes `requirepass`, so that the operator backdoor does not silently grant full admin.
4. **`requirePassFile` is either removed or demoted to a comment** in `amb-redis.nix`, because once `aclfile` loads, redis 8 IGNORES `requirepass`. Leaving it set is misleading (suggests it's authoritative when it isn't).
5. **Cross-wolf stream isolation is enforced**, not just declared. `redis-cli ACL LIST` shows each wolf's `~amb:wolf.<self>.*` key pattern with NO `~amb:wolf.<other>.*` patterns. A test from wolf A trying `PUBLISH amb:wolf.B.<x> <msg>` must be denied.
6. **The spec / runtime / glossary row-level wording is updated** from "Phase 1C partial / in progress" to "Phase 1C live", and this open question is closed (moved to `decisions/0004-amb-phase1c-completion.md`).

**Out of scope here.** E3-T18 (this entry) only verifies Phase 1A is current and documents the transition. E3-T9 owns the Phase 1C ACL finalization itself (the open code-level work to make the upstream redis module honor `settings.aclfile`, plus the ACL narrowing pass). The two should not be merged.

**Do NOT.** Do not change `requirepass` value or any ACL outside E3-T9. Both are destructive on the shared broker and require J7 sign-off via the standard Phase 1C ruling path.

---

## OQ-7 — When does the wolfpack adopt A2A-protocol wire compliance? (Q-status: WAIT)

**Source / trigger.** `specs/AMB-Substrate.md` §8 (A2A alignment — position, not claim). J7 asked the external reviewer to surface this as an explicit `open-question` rather than a parked card.

**Position today.** The wolfpack is **not** A2A-compliant, and should not chase full wire-compliance now:
- Internal "agent cards" share almost no schema with A2A `AgentCard` and aren't served anywhere.
- `payload.task_id` looks like A2A's `taskId` but is payload-level with no task object behind it.
- AMB transport is Redis Streams, not JSON-RPC-2.0-over-HTTP — full compliance means either replacing Streams (throwing away persistence, at-least-once, ACLs) or building an A2A-facade gateway that translates.
- For an internal 11-wolf pack under end-to-end control, A2A wire-compliance is premature. The facade is the right *eventual* move but only earns its keep when talking to **external** agents.

**What we adopt now, regardless of wire format** (load-bearing for loop safety, not optional decoration):
- A2A's task lifecycle model (submitted, working, input_required, auth_required, completed, failed, canceled, rejected) — the terminal/interrupt states. Map the Kanban state set (`todo/in_progress/done/blocked/archived`) onto this model and treat a task as terminating. Spec source: §8 of `specs/AMB-Substrate.md`; see `kanban/backlog.md` L2-1 for the card-format envelope bump that makes this enforceable on every emit.
- `contextId` promoted to required header — drives the turn-budget loop guard (L2-3).

**Defer** until the first compatible upstream release:
- `role` + `parts[]` message shape
- `/.well-known/agent-card.json` serving
- JSON-RPC transport
- SSE / webhook
- `a2a_tool.py` and the Phase 1D external-agent-facing path

**Gating trigger** (re-evaluation):
- First compatible upstream `a2a-sdk` release that is actually usable from Python 3.12 with `redis-py 8.0.1` (the current AMB client) AND provides an internal-wolfpack-shaped `AgentCard` schema we can serve without rewriting our plumbing.
- OR a concrete inbound request from an external agent that needs to consume AMB messages (e.g. a J7-initiated cross-agent collaboration with a non-wolfpack system).

When that trigger fires, this entry becomes `decisions/000N-a2a-adoption-decision.md` and the work opens as a new epic (current estimate: ≤ 6 weeks work + 1 week migration + 1 week shadow-validation against AMB-fed traffic). Until then, keep parked.

**Do NOT.** Do not start a `a2a_tool.py` module, do not add JSON-RPC endpoints, do not serve `/.well-known/agent-card.json` until the trigger fires. Speculative adoption is exactly the failure mode this entry exists to prevent.