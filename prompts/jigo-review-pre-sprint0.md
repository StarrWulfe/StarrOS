# Jigo review brief — PR #8 (pre-Sprint-0 hardening)

## Context

San just opened PR #8 (`docs/pre-sprint0-hardening`, commit `c514274`,
11 files, +85/-45) batching the Lane A + Lane B hardening work that
gates Sprint 0. This is the verifier pass before we open Phase P0
(Ashitaka gateway `:8643` re-bind).

PR: https://code.starrwulfe.xyz/j7/StarrOS/pulls/8
Diff: https://code.starrwulfe.xyz/j7/StarrOS/pulls/8/files
Repo path: `/nas/hdd/agent-shared/WORKSPACES/starros-v1/repo/`
Branch: `docs/pre-sprint0-hardening` (from `main`, mergeable, no conflicts)

## Scope to verify

Seven cards landed in one PR (Lane A1-A6 + Lane B1):

- **A1** `kanban/board-schema.md` — added `forbidden_paths` and
  `report_back_channel` required fields + legal-transition table.
  Dossier issues #3, #4.
- **A2** `kanban/backlog.md` + `specs/gbrain-substrate.md` +
  `docs/persistence-boundaries.md` — GBrain card dedup (E2-T1 merged
  into E3-T12), E1-T5 → E1-T3 mis-citation fixed. Dossier issue #5.
- **A3** `README.md` + `specs/starros-stack-spec.md` + dangling
  anchors in 3 files + obsolete tree-listing file deleted + Mnemosyne restart
  procedure unified. Dossier issues #7, #10, fact #10.
- **A4** `specs/starros-stack-spec.md` §3 + `docs/runtime-state.md`
  §2 + `decisions/0003-canonical-spec-boundaries.md` glossary —
  AMB-Redis broker row added, `:6380` port registered, Phase 1A/1C
  labels defined. Dossier issue #6.
- **A5** `packets/examples/*.md` — both Mission-Control-targeting
  examples stamped `[HISTORICAL — Mission Control paused]`; added
  Report-back channel metadata line. Dossier issue #9.
- **A6** `docs/persistence-boundaries.md` (profile.yaml template/instance
  note) + `decisions/0003-canonical-spec-boundaries.md` (hermes-workspace-src
  glossary clause). Dossier §4.5 items 2, 4.
- **B1** `kanban/backlog.md` E3-T16 added — re-sequences E3-T11 (Outpost
  Traefik 404 fix) ahead of Sprint 0. Rec #6.

## What I want you to check

1. **Did San actually fix the thing the dossier cited, or did he
   rationalize around it?** Especially A3 (cross-ref sweep) — this is
   the largest scope and the most prone to "looks plausible, misses
   the actual line."
2. **Are the new schema fields (`forbidden_paths`, `report_back_channel`,
   legal-transition table) enforceable?** Or did San add prose that
   reads nice but the dispatcher can't actually check?
3. **Did the GBrain dedup create a new contradiction** (e.g. now E3-T12
   has too many responsibilities, or E1-T3's dep on E1-T5 is broken)?
4. **AMB row + Phase 1A/1C labels** — confirm Ishii would sign off on
   the wording. (He hasn't seen this yet.)
5. **The Mnemosyne restart procedure** — San tagged this `[NEEDS-KOHROKU]`
   because the canonical helper script (`bsm-secret-fetch-for-environmentfile.sh`)
   was chosen from the dossier, not from Kohroku. Is the placeholder
   wording good enough for the repo to merge, or should we block on
   Kohroku first?
6. **Obsolete tree-listing file deletion** — is anything still referencing
   the deleted file as a source-of-truth? A repo-wide grep should return
   nothing post-commit; San claims it does — verify.
7. **Anything in the diff that smells like "this will bite us in
   Sprint 0."** San tends to over-document in hardening passes; flag
   if the added prose is heavy enough to need pruning.

## One open question (your call, not blocking)

Dossier issue #8 (jigo-review.md repo-vs-skill mismatch — file at
`prompts/jigo-review.md` exists, 313 bytes, but `prompts/san-execute-shakedown.md`
references it as if it were a skill at `prompts/skills/jigo-review.md`)
was **not** in Lane A or B. San flagged it but didn't fix it. Should it:

  (a) be added as A7 in this PR (cheap, but enlarges scope), or
  (b) wait for a follow-up PR (cleaner separation), or
  (c) is it actually fine as-is and we're overthinking it?

## Verdict format (your standard)

Verdict (Ready / Ready with minor fixes / Blocked)
+ Top issues (≤7, ranked by impact)
+ Safe to ignore (≤5, things San flagged but you accept)
+ Final answer (1-3 sentences)
≤500 words. No tables. No full-file rewrites — just `path:line` refs
the way you usually do.

Branch in repo:
```
cd /nas/hdd/agent-shared/WORKSPACES/starros-v1/repo/
git fetch
git checkout docs/pre-sprint0-hardening
```
