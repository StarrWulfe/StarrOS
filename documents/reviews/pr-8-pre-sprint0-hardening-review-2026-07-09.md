## 🛡️ JIGO REVIEW — PR #8 (pre-Sprint-0 hardening)

**Verdict:** Ready with minor fixes
**Run-this-now:** Sprint-0 blockers (A4 Ishii ack) before merge; rest of Lane A + B1 can land.

---

### Top issues (ranked by impact)

1. **A4 — Ishii signoff missing on AMB row + Phase 1A/1C labels.**
   `kanban/backlog.md:48` lists A4 author = Ishii and the brief (q4) confirms
   Ishii hasn't seen the wording. The labels touch security posture (per-wolf
   ACL material in Phase 1C, `:6380` plain requirepass during Phase 1A). No
   policy change of that weight should ship on San's solo authorship. **Block
   on this one card**; the rest of the PR can land on a separate ship without
   A4 if Ishii ack is delayed.

2. **`docs/persistence-boundaries.md:35` — anchor remap lands on the wrong
   target.** The new text says "see `docs/runtime-state.md` §2 (Honcho API
   row) and §3 (decommission pending item)." §3 line 60 is the Mnemosyne
   item; the Honcho item is the §2 row at line 41 with the
   DECOMMISSION-PENDING note inline. "Decommission pending item" doesn't
   appear as a §3 Top-5 entry — it lives in §2 only. The cross-ref is
   mislabeled; should read "§2 (Honcho API row, see decommission-pending
   note)."

3. **`kanban/board-schema.md`, `README.md`, `packets/examples/*.md` — no
   trailing newline at EOF.** `\ No newline at end of file` on all four.
   POSIX minor; tools that consume `cat | sha256sum` will hash differently
   than tools that read line-by-line. Add a final `\n`.

4. **Mnemosyne restart procedure `[NEEDS-KOHROKU]` (`docs/runtime-state.md:60`)
   is honest triage, not a fix.** The wording is acceptable for merge;
   Sprint 0 is gated on a Kohroku ping. Carry this as E3-T16-bis or a
   sibling card in E5 so it doesn't drift past Sprint 0 opening.

5. **The "unanimous Phase 1A" labeling across spec / runtime / glossary
   reads consistent but is only consistent at the row level.** The ADR-0003
   glossary (`decisions/0003-canonical-spec-boundaries.md:42`) defines
   "Phase 1A = broker live + plain requirepass," but no doc actually
   asserts or checks that the live `:6380` broker IS using plain
   requirepass (or that "plain requirepass" is the intended interim auth
   posture). This is acceptable to defer to Sprint 0 work (P8 ACL
   finalization) but should be flagged as an open question worth a single
   sentence in `docs/architecture/open-questions.md` if that file exists.

6. **Dossier issue #8 (skill-vs-prompt mismatch) is moot in this branch.**
   No `prompts/skills/...` reference exists anywhere except as the brief's
   quote of its own description (`prompts/jigo-review-pre-sprint0.md:70`).
   San was right to skip it. But the underlying class — three runtime
   skills (`jigo-review`, `nixos-host-operations`, `j7-homelab-environment`)
   cited by canonical docs with no in-repo one-paragraph stub
   (`documents/audits/claude-shakedown-2026-07-09.md:83`) — is the real
   gap, and Sprint 0 will trip on it. Suggest opening E5 for a follow-up
   hardening lane: "in-repo one-paragraph stub for every canonical skill."

7. **`kanban/backlog.md:27` E2-T1 dedup is correct but slightly under-
   documented.** "DEDUP — see E3-T12; same deliverable" is unambiguous, but
   a reader scanning Epic E2 (data + orchestration) won't see why an E2-row
   is pointing at an E3-card. Add a one-line rationale ("subsumed by E3-T12
   after Phase P11 was added; kept visible for E0 audit trail"). Trivial.

### Safe to ignore (≤5)

- `TREE.txt` deletion is correct; remaining greps are all "history of
  finding" / "delete it" — no live canonical claim remains.
- `specs/gbrain-substrate.md:16` still says "GBrain is referenced in
  `kanban/backlog.md` E2-T1 (OKF/GBrain substrate)" — looks stale but it's
  preserved as the etymology of the legacy `OKF/` typo per spec L16 itself.
  Not worth chasing.
- Honcho status word is normalized on the three ADR-0003/runtime-state/
  spec surfaces that mattered (`decisions/0003-canonical-spec-boundaries.md:42`,
  `docs/runtime-state.md:41`, `specs/starros-stack-spec.md:61`).
- Sprint-0 gating on the hardening PR is correct; the README status block
  captures it (`README.md:13–17`).
- E3-T16 (Outpost Traefik re-sequence) is well-scoped: peer-host
  discipline (Outpost admin path), named owners (Ishii + Toki), J7-signoff
  gate for risky change windows, one-line sed + HUP per
  `docs/runtime-state.md:60`.

### Final answer

**Ship the PR as soon as A4 gets Ishii ack.** The other six are minor and
either fix-in-line or carry into Sprint 0 (Kohroku ping on Mnemosyne,
follow-up E5 for skill stubs). The schema fields, the legal-transition
table, the GBrain dedup, the spec §13/§14 cleanup, and the cross-reference
sweep all hit their marks against the dossier. No rollback needed; no
re-surfacing of completed E2-T1 work; Lane B + B1 + E0 all gate-correctly.
The `done` terminus now requires J7, the externals now require Jigo, the
schema/policy gap is closed. Sprint 0 can open against this substrate.

---

**Reviewer:** 🛡️ Jigo
**Date:** 2026-07-09
**Branch reviewed:** `docs/pre-sprint0-hardening` (commit `f7c46c4`,
                   12 files, +176/-45 vs `main`)
**Memo path:** /nas/hdd/agent-shared/reviews/pr-8-pre-sprint0-hardening-review-2026-07-09.md
**Mode:** repository-side review per `prompts/jigo-review-pre-sprint0.md` (San-authored brief, branch `docs/pre-sprint0-hardening` @ `f7c46c4`); local Mononoke review workspace at `/nas/hdd/agent-shared/WORKSPACES/starros-v1/repo/`
