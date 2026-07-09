# ADR-0004: Multiplex target is per-wolf gateways, not a single canonical gateway

**Status:** Accepted
**Date:** 2026-07-09
**Deciders:** J7

## Context

`specs/starros-stack-spec.md` §2 item 3 (v1.1/v2.0 canonicalization) asserted two
contradictory targets in the same sentence: a single canonical
`hermes-gateway.service` handling all wolf traffic, versus "one gateway per
active wolf" as the canonical default. This was flagged as issue #1 in the
2026-07-09 external Claude shakedown audit (`documents/audits/claude-shakedown-2026-07-09.md`
§4.3) as blocking Phase P0's definition of done, since P0 ("Stabilize
multiplex + fix Ashitaka port 8643") cannot be marked complete without knowing
which target it's stabilizing toward.

Multiplexing was attempted and did not reach a working state. A multiplex
process does exist and run (`docs/runtime-state.md` §2: PID 490006 on
`:8642`), but with `multiplex_profiles: false` — it is not performing
per-wolf profile routing, and getting it there was not achieved.

Meanwhile, 9 of 10 wolves are already running successfully as independent
per-wolf gateway units on `:8644`–`:8652`. Only Ashitaka's unit is broken:
process alive (PID 20888) but unbound to `:8643`.

## Decision

**Per-wolf gateways are the canonical target**, matching what is already
deployed. The single-canonical-gateway sentence in spec §2 item 3 is struck.

Multiplexing is not adopted for wolf traffic routing at this time. The
existing multiplex process on `:8642` may continue running for whatever
non-wolf-routing purpose it currently serves, but it is not the target
architecture and should not be extended toward `multiplex_profiles: true`
without a future ADR reopening this decision.

Phase P0's scope narrows to: **fix Ashitaka's `:8643` binding** so it joins
the other 9 wolves as a per-wolf unit. No multiplex-adoption work is in
scope for P0.

## Consequences

- `specs/starros-stack-spec.md` §2 item 3 is corrected to state the per-wolf
  target only, with a cross-reference to this ADR.
- `kanban/backlog.md` E3-T1 is retitled to reflect the narrowed P0 scope
  (multiplex-adoption language removed).
- If port sprawl (10+ per-wolf listeners) later becomes a real operational
  problem, multiplexing may be revisited — but as a new ADR with its own
  named blocker analysis, not a silent re-reading of the old spec sentence.
- No runtime change required by this ADR alone; Ashitaka's binding fix is
  tracked as the (retitled) E3-T1 card, owner Ishii.

## Alternatives considered

- **Debug and complete multiplexing now.** Rejected for lack of a known path
  to `multiplex_profiles: true` — the attempt already failed once, and P0 is
  blocked in the meantime. Can be revisited later per Consequences above.
- **Leave the spec sentence ambiguous and let San's Sprint-0 work resolve it
  implicitly.** Rejected — this is exactly the failure mode the shakedown
  audit flagged; an implicit resolution wouldn't be recorded anywhere.
