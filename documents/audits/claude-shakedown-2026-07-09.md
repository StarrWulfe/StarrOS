# Claude Shakedown Dossier — 2026-07-09

> **Auditor:** external Claude (Anthropic), per `prompts/claude-shakedown.md`.
> **Repo state audited:** `main` @ `524fbfe` ("Merge pull request 'prompts: claude-shakedown.md …' (#4)").
> **Intended location:** `documents/audits/claude-shakedown-2026-07-09.md` (ephemeral until promoted).
> **Access:** repo read-only. No SSH to Mononoke/Outpost/Yoseba, no runtime logs, no Hermes Kanban DB, no `~/.hermes/cron/output/` dossiers (§3 item 12 of the shakedown prompt was unreachable from the repo). Claims requiring those are marked `[UNKNOWN]`.

---

## 4.1 Verified facts vs inferred assumptions

| # | Claim | Status | Evidence |
|---|---|---|---|
| 1 | All 22 canonical `.md` files listed in the shakedown reading list exist in the repo | Verified | `find` over working tree at `524fbfe` |
| 2 | `TREE.txt` is stale: it omits `decisions/0003`, `docs/runtime-state.md`, `docs/persistence-boundaries.md`, `docs/external-workers.md`, `specs/gbrain-substrate.md`, `prompts/claude-shakedown.md` | Verified | `TREE.txt` vs working tree |
| 3 | Spec provenance v1.0 sha `908aae4a4b…` is a **blob**, not a commit | Verified | `git cat-file -t 908aae4a4b` → `blob`; `[starros-stack-spec.md §14 line 220]` says "commit sha" |
| 4 | Spec §14 marks PR #1 "open"; PR #1 is merged | Verified | merge commit `99b5b49` on `main`; `[starros-stack-spec.md §14 line 221]` |
| 5 | Honcho is de-scoped **and still running** bound to `0.0.0.0:8000` | Verified (as documented) | `[runtime-state.md §2 line 40]` "OK; **de-scoped**" |
| 6 | Ashitaka `:8643` unbound; 9 wolves OK on `:8644–:8652` | Verified (as documented) | `[runtime-state.md §2 lines 45–46, §3 line 60]` — port table internally consistent |
| 7 | `board-schema.md` required fields omit `forbidden_paths` and `report_back_channel`, both mandated by `external-workers.md` §4 | Verified | `[board-schema.md lines 16–29]` vs `[external-workers.md §4 lines 41–42]` |
| 8 | `gbrain-substrate.md` cites backlog card **E1-T5**, but E1-T5 is the external-workers doc; the GBrain authoring card is **E1-T3** | Verified | `[gbrain-substrate.md line 3]` vs `[backlog.md lines 18, 20]`; same wrong ID propagated to `[persistence-boundaries.md line 16]` example column |
| 9 | Four cross-references point at runtime-state section anchors that do not exist: §"Mission Control — paused", §"Multiplex", §"De-scoped", and Nextcloud "empty — see runtime-state" | Verified | `[starros-stack-spec.md §2 line 33, §2 line 34, §3 line 49]`, `[persistence-boundaries.md line 34]` vs the actual headings of `runtime-state.md` (§0–§7) |
| 10 | `runtime-state.md` gives two different Mnemosyne restart procedures | Verified | `[runtime-state.md §2 line 47]` ("`nixos-host-operations` skill") vs `[§3 line 59]` ("`bsm-secret-fetch-for-environmentfile.sh` helper") |
| 11 | AMB (Redis `:6380`) appears in the ADR-0003 glossary and Phase P8, but is absent from both the spec §3 component table and the runtime-state §2 port map | Verified | `[decisions/0003 line 47]`, `[starros-stack-spec.md §11 line 195]` vs `[§3 lines 41–59]`, `[runtime-state.md §2 lines 30–51]` |
| 12 | `kanban/README.md` and `backlog.md` reference a `sprints/` directory that does not exist | Verified | `[kanban/README.md line 9]`, `[backlog.md line 4]` vs working tree |
| 13 | `specs/aionui-addendum.md` is a 3-line placeholder in the canonical `specs/` tree | Verified | `[aionui-addendum.md lines 1–3]` |
| 14 | Jigo punch-list card `t_377762_b187` and the "9 open questions" PR-2 body exist as described | `[UNKNOWN]` | Kanban SQLite and Forgejo PR bodies are not in the repo; taken on trust from `[claude-shakedown.md §4.4–4.5]` |
| 15 | The Mission Control pause / Honcho removal / Hermes-Workspace kill are J7 directives dated 2026-07-09 | Verified (as documented) | `[decisions/0003 §Glossary lines 39–46]`; the directive text itself is not in the repo `[INFERRED]` that it was verbal/chat |
| 16 | Nextcloud is on `gatewood.xyz` while everything else is `starrwulfe.xyz` | Verified as written; **intent** `[UNKNOWN]` | `[persistence-boundaries.md line 19]` `cloud.gatewood.xyz`, `[runtime-state.md §4 line 67]` `talk.gatewood.xyz` — possibly a second real domain, possibly stale paste |
| 17 | "Heroes are 12, not 13" refers to a component count nowhere defined in the repo | `[INFERRED]` | `[persistence-boundaries.md line 34]` — no doc enumerates "the 13 heroes"; unverifiable in-repo |
| 18 | `wolfpack-dashboard-data-contract.md` (cited twice as canonical) is not in the repo | Verified absent | `[starros-stack-spec.md §7 line 113, §10 line 175]` |
| 19 | The two San audit dossiers (Round 1/Round 2) predate canonicalization | `[UNKNOWN]` | live at `~/.hermes/cron/output/`; unreachable from repo |
| 20 | External-worker slack tolerances and review gates contain no approval-bypass path for ADRs/spec/secrets | Verified (doc-level) | `[external-workers.md §3 lines 29–34, §5 lines 47–53]`, `[starros-stack-spec.md §4.1 lines 75–82]` |

---

## 4.2 Audit by section

### 4.2.1 `decisions/0001-repo-is-source-of-truth.md`

**Coherence:** Tight. The runtime-state weekly-rewrite exception (line 16) is well-drawn and correctly mirrored in `[runtime-state.md §0]` and `[persistence-boundaries.md line 10]`. **Cross-doc consistency:** Consistent everywhere it is cited. **Gaps:** ADR-0001 declares the repo authoritative, but the repo carries visible self-drift: stale `TREE.txt` (fact 2), stale `README.md` milestones (all five "first milestones" are done per E0 checkboxes `[backlog.md lines 8–12]` yet the README still frames them as pending), and stale spec provenance (facts 3–4). None is individually serious `[BROKEN]`-level, but in a repo whose constitutional claim is "if it matters, it's committed and correct here," visible rot in the top-level files erodes the claim fastest. **Risk hotspots:** none.

### 4.2.2 `decisions/0002-human-authors-playbook-v0.md`

**Coherence:** Fine; two-line ADR doing one job. **Consistency:** Matches `[README.md]` workflow and `[docs/workflow.md]`. **Gaps:** Status is "Accepted" with no sunset — E0-T1/E0-T4 are checked done, so ADR-0002's phase ("first handoff is review-and-kanbanization") has arguably completed. Nothing says what San's authority is *after* v0. Minor, but San-facing prompts will keep loading a constraint whose trigger condition has passed. **Risk hotspots:** none.

### 4.2.3 `docs/runtime-state.md`

**Coherence:** `[PARTIAL]`. The §0 boundary table is excellent and should be the template for the rest of the repo. Two internal defects: (a) the Mnemosyne restart procedure is given twice with different answers (fact 10) — an on-call wolf at 3am should not have to guess which is current; (b) the port table has a duplicate cosmetic row (`[§2 line 51]`, "11080/11081 — see Nextcloud above"). **Consistency:** The port table, Top-5 list, and drift sections agree with each other and with the shakedown prompt's §2.5 — except the shakedown prompt says "Restart per `nixos-host-operations` skill" for Mnemosyne, inheriting side (a)'s ambiguity. **Gaps:** AMB Redis `:6380` is missing from the Mononoke service map (fact 11) despite Phase P8 actively touching its ACLs — the live map of "what listens on this box" omits a live broker. Honcho's row says "OK; de-scoped": a de-scoped service still bound to `0.0.0.0` is a standing decision nobody has made (stop it? keep it warm? until when?), and the port map is the only place that tension is visible. **Risk hotspots:** anyone using §2 as a firewall/ACL baseline will miss `:6380`; anyone reclaiming `:8000` "because Honcho is removed" will kill a running service without a decision record.

### 4.2.4 `docs/persistence-boundaries.md`

**Coherence:** Strong; the concern→store→writer→reader table is the most operationally useful doc in the repo. **Consistency:** `[PARTIAL]`. Three defects: (a) the GBrain row's example cites "E1-T5 GBrain spec drafted" — wrong card ID (fact 8); (b) the Notes cite a runtime-state "§De-scoped historical note" that doesn't exist (fact 9); (c) "Heroes are 12, not 13" is an in-joke with no in-repo referent (fact 17) — charming, but a canonical doc should not require oral tradition to parse. **Gaps:** the per-wolf identity row (line 11) names both `~/.hermes/profiles/<wolf>/` files *and* implies `wolfpack.nix` seeds them, while `[runtime-state.md §6 line 81]` says the sibling `wolf-souls/` tree is "staging." The template/instance/staging triangle for `profile.yaml` is exactly Jigo minor #2 — see §4.5. **Risk hotspots:** the Nextcloud row's `cloud.gatewood.xyz` (fact 16): if that's a typo, every wolf pointed at persistence-boundaries for "where do long-form docs go" gets a wrong hostname.

### 4.2.5 `docs/external-workers.md`

**Coherence:** The strongest policy doc in the repo. The named-responsible vs fixed-operator (Okkoto) distinction in §2/§5 is clearly drawn; §3's never-list and §8's anti-patterns close the obvious loopholes. One wry note: §7 forbids the term "external workers" while the file is named `external-workers.md` — harmless, but it means every compliant citation of the file violates its own naming table on sight. **Consistency:** `[PARTIAL]` — the §4 hard requirements (`forbidden_paths` non-empty, `report_back_channel` set) are **not** enforceable by `kanban/board-schema.md`, which lacks both fields (fact 7). Policy says "a card may not be marked `in-external-implementation` unless…" but the card schema cannot represent two of the three preconditions. That's a Jigo-grade loophole: a schema-valid card can be policy-invalid, and nothing structural catches it. **Gaps:** §2 cites "`jigo-review` skill §0.5 config-first mandate," but the repo's `prompts/jigo-review.md` is 11 lines with no §0.5 and no config-first language. Either the skill (runtime, canonical) and the prompt (repo, canonical) are two different artifacts with one name, or the repo copy is a stub of the real thing. ADR-0001 says repo is truth; the citation says the skill is. Pick one. **Risk hotspots:** none beyond the schema gap.

### 4.2.6 `specs/starros-stack-spec.md`

**Coherence:** `[PARTIAL]`. §2 item 3 contradicts itself in one sentence: "a **single canonical `hermes-gateway.service`** … holds the API server. Per-wolf units are an on-demand option; the canonical default is **one gateway per active wolf**" `[§2 line 33]`. Those are opposite targets. Since Phase P0 ("Stabilize multiplex + fix Ashitaka :8643") is *in progress right now* and P0's success criterion depends on which target is true — collapse everything into `:8642`, or fix `:8643` and run 10 per-wolf units — this is the single most consequential sentence-level defect in the repo. Everything else in the spec is coherent. **Consistency:** the dangling anchors (fact 9), the "Nextcloud yes (empty — see runtime-state)" claim that runtime-state never substantiates, the missing AMB row in §3 (fact 11), and the two cited-but-absent artifacts (`wolfpack-dashboard-data-contract.md`, fact 18). §13's first recommendation ("add runtime-state + persistence-boundaries to san-handoff reading list") is already implemented — `[san-handoff.md lines 8–9]` — so the spec is carrying a completed to-do as an open one. **Gaps:** two phase-numbering systems coexist: the P0–P13 rollout and an "AMB Phase 1A / Phase 1C" scheme (`[decisions/0003 line 47]`, `[§11 line 195]` "Phase 1C ACL finalization (Phase P8)"). A reader cannot tell whether "Phase 1C" is a sub-phase of P8, a legacy AMB-internal label, or a third plan. **Risk hotspots:** §2.4/§3 correctly flag Mission Control paused — the spec does *not* invite the classic mistake. Good. But §7's Mission Control target section still names a data contract file that isn't in the repo; anyone starting P2 work from the spec alone would begin by hunting a ghost.

### 4.2.7 `specs/gbrain-substrate.md`

**Coherence:** Good draft discipline — confirmed facts vs assumptions-to-validate are explicitly separated (§2/§3), and §5's "does NOT store" list correctly fences GBrain off from Mnemosyne, `wolfpack.db`, Forgejo, and runtime-state, which was the biggest duplication risk. **Consistency:** the E1-T5 mis-citation (fact 8); otherwise aligned with `[persistence-boundaries.md line 16]` and `[starros-stack-spec.md §8 line 121]`. **Gaps:** §7 proposes `/var/lib/gbrain/<slug>.db` while §9's hosting recommendation proposes daily backup to `/nas/hdd/agent-shared/gbrain/` — fine, but neither path appears in persistence-boundaries' table, whose GBrain row still says "TBD." Once J7 accepts §7, persistence-boundaries must be updated in the same PR or the "single answer to where do I write this" claim breaks. §8's "every card state transition emits a GBrain event" quietly creates a hard runtime dependency from Hermes Kanban → GBrain that no kanban doc mentions. **Risk hotspots:** the Matrix-bot surface (§7) touches Synapse on **Outpost** — per shakedown §2.1, that's a peer-host sequencing hazard, and the spec doesn't flag it. Recommendation "API-only in v1, bot in v2" (§9) conveniently defers the hazard; make that explicit as the *reason*.

### 4.2.8 `kanban/board-schema.md` + `kanban/backlog.md`

**Coherence:** schema is minimal and clean; state list matches every state name used elsewhere (`ready-for-implementation`, `in-external-implementation`, `changes-requested` all resolve). **Consistency:** `[PARTIAL]` — the two missing card fields (fact 7) and the GBrain double-card: E2-T1 "GBrain substrate definition" and E3-T12 "GBrain substrate spec (Phase P11)" describe the same deliverable with different owners implied by context (`[backlog.md lines 27, 45]`). This is Jigo minor #1 and it's live ammunition: San's handoff explicitly instructs kanbanization from this file, so the duplicate will become two runtime cards on day one. **Gaps:** `sprints/` referenced, absent (fact 12); no transition rules despite `[kanban/README.md line 8]` promising "transition rules" in board-schema — the schema lists states and fields, but zero legal-transition or authority mapping (who may move a card from `awaiting-wolf-review` to `ready-to-merge`?). The spec's §4.1 slack tolerances say "kanban card moves — wolf solo," which combined with no transition rules means any wolf can move any card to `done` solo. That is almost certainly not intended. **Risk hotspots:** E3 cards inherit phase statuses from spec §11; if the multiplex contradiction (§4.2.6) is resolved toward single-gateway, E3-T1's title ("Multiplex + Ashitaka :8643") is the wrong work.

### 4.2.9 `packets/leaf-card-template.md` (+ examples)

**Coherence:** Complete against external-workers §4's checklist — every required section exists, including the PR-3-added `report_back_channel`. **Consistency:** the two worked examples (`backend-kanban-adapter.md`, `ui-preview-panel.md`) both target **Mission Control** app paths (`apps/mission-control-api/**`, `apps/mission-control/src/panels/preview/**`) — i.e., the repo's only two example packets exercise the one component that is paused by J7 directive. They also omit the `Report-back channel` metadata line the template now requires, so the examples fail the current template. **Gaps:** template has no `dependencies` or `spec_paths` echo even though board-schema requires those card fields; packet and card will drift. **Risk hotspots:** a wolf copying an example packet verbatim would open externally-implemented work against a paused component — precisely the shakedown §2.4 pitfall, embedded in the training examples.

### 4.2.10 `prompts/san-handoff.md`, `prompts/fable-global.md`, `prompts/jigo-review.md`

**san-handoff:** `[WORKING]`. Reading list is complete and correctly ordered relative to ADR-0003 (spec then runtime-state — note it inverts the shakedown's own "runtime-state first" ordering; for San's kanbanization job the spec-first order is defensible, but the two prompts should agree on *why* their orders differ or one should change). Tasks 1–5 and the output format match ADR-0002's mandate.
**fable-global:** `[WORKING]`. Paused-components banner is prominent and correct; constraints match external-workers and ADR-0001.
**jigo-review:** `[PARTIAL]` — 11 lines, no config-first mandate, no §0.5, while external-workers §2 cites "jigo-review skill §0.5" as binding. Also reviews only "playbook, backlog, and packet template" — Jigo's actual demonstrated remit (doc-canon PR review, E1-T8) is the whole canonical surface. The repo prompt undersells the runtime skill; under ADR-0001 the repo copy is the canonical one, which means the canonical Jigo is weaker than the operating Jigo.

### 4.2.11 `docs/playbook.md`, `docs/workflow.md`

**Coherence:** both fine; playbook's required-sections list is a good SOP contract. **Consistency:** workflow step 9 ("after merge, the spec and runtime-state are updated in the same PR") is contradicted in practice by the spec's own stale §13/§14 (facts 3–4, §4.2.6) — the rule exists, the habit doesn't yet. **Gaps:** playbook cites `system/j7-homelab-environment` skill for destructive-op discipline; like `jigo-review` and `nixos-host-operations`, this is a runtime skill invisible to the repo. Three load-bearing skills are cited by canonical docs and none has even a one-paragraph summary in-repo. **Risk hotspots:** none.

### 4.2.12 Optional context (San dossiers Round 1/2)

Unreachable from the repo (`~/.hermes/cron/output/`). Noted for completeness; nothing in this dossier depends on them.

---

## 4.3 Top issues (ranked)

**1. The multiplex target contradiction blocks P0.** *Problem:* `[starros-stack-spec.md §2 line 33]` simultaneously declares a single canonical gateway and per-wolf gateways as the canonical default. *Why it matters:* Phase P0 is in progress right now and its definition of done depends on which sentence-half is true. *Fix direction:* J7 picks the target (one line in the spec, plus an ADR if the choice is architectural), then retitle E3-T1 to match.

**2. Honcho is "removed" on paper and running on the box.** *Problem:* three different status words (removed / de-scoped / OK) across `[starros-stack-spec.md §3 line 61]`, `[decisions/0003 line 46]`, `[runtime-state.md §2 line 40]`, with the service still bound `0.0.0.0:8000`. *Why it matters:* a de-scoped-but-live service is unowned attack surface and an ambiguity about whether `:8000` can be reclaimed. *Fix direction:* one J7 decision — stop-and-archive vs keep-warm-until-date — recorded in runtime-state, with the glossary and spec normalized to one status word.

**3. The board schema cannot enforce the external-worker policy.** *Problem:* `board-schema.md` lacks `forbidden_paths` and `report_back_channel`, both mandatory per `[external-workers.md §4 lines 41–42]`. *Why it matters:* a schema-valid card can be policy-invalid, so the strongest safety policy in the repo has no structural teeth. *Fix direction:* add both fields to the required-fields list; two lines.

**4. No kanban transition rules despite "wolf solo" move authority.** *Problem:* `[kanban/README.md line 8]` promises transition rules in board-schema; none exist, while `[starros-stack-spec.md §4.1 line 78]` grants wolves solo card-move authority. *Why it matters:* as written, any wolf can solo-move any card to `done`, bypassing Jigo/Ishii gates that live only in prose. *Fix direction:* add a minimal legal-transition table (state → allowed next states → authority) to board-schema.

**5. GBrain is double-carded and mis-cited.** *Problem:* E2-T1 and E3-T12 are the same deliverable `[backlog.md lines 27, 45]`; `[gbrain-substrate.md line 3]` and `[persistence-boundaries.md line 16]` both cite E1-T5, which is the external-workers card. *Why it matters:* San's handoff will mechanically mint duplicate runtime cards and a wrong provenance trail on day one. *Fix direction:* delete or merge E2-T1 into E3-T12; fix both E1-T5 citations to E1-T3.

**6. AMB is invisible to both maps.** *Problem:* the Redis broker on `:6380` is in the glossary and Phase P8 but absent from the spec §3 component table and the runtime-state §2 port map. *Why it matters:* P8 is in progress against a component neither canonical map acknowledges; ACL work on an unmapped listener is how firewall baselines go wrong. *Fix direction:* add an AMB row to both tables; reconcile "Phase 1A/1C" labels to the P-numbering or define them once.

**7. The dangling-anchor cluster.** *Problem:* four cross-references point at runtime-state sections that don't exist (fact 9), plus two docs cite absent artifacts (`wolfpack-dashboard-data-contract.md`; the divergent Mnemosyne restart procedures, fact 10). *Why it matters:* the whole doc-canon design is "follow the pointer"; dead pointers train wolves to stop following pointers. *Fix direction:* one sweep PR fixing anchors to real headings, plus a decision on the single Mnemosyne restart procedure.

**8. `jigo-review.md` (repo) ≠ `jigo-review` (skill).** *Problem:* external-workers §2 binds review to a skill section (§0.5 config-first) that the canonical repo prompt doesn't contain. *Why it matters:* under ADR-0001 the repo copy is authoritative, so the binding review standard is formally undefined. *Fix direction:* either sync the skill's operative sections into `prompts/jigo-review.md`, or add a one-line pointer declaring the skill canonical for review procedure (and note the ADR-0001 exception).

**9. The example packets model the forbidden move.** *Problem:* both worked examples target paused Mission Control paths and omit the now-required `Report-back channel` field. *Why it matters:* examples are what wolves copy; these teach opening external-worker cards against a paused component with an incomplete packet. *Fix direction:* replace with one live-component example (e.g., a P9 agent-card task) or stamp both `HISTORICAL — Mission Control paused` and add the missing field.

**10. Truth-repo hygiene rot.** *Problem:* stale `TREE.txt`, stale README milestones, spec §14 calling a blob a commit and PR #1 "open," and spec §13 carrying an already-implemented recommendation. *Why it matters:* individually cosmetic; collectively they contradict ADR-0001's core promise and normalize drift. *Fix direction:* one hygiene PR; optionally delete `TREE.txt` (git *is* the tree) rather than maintain it.

---

## 4.4 The 9 open questions from PR #2

1. **GBrain owner.** Answerable-with-recommendation from docs: `[gbrain-substrate.md §9 line 75]` recommends Ashitaka primary / Okkoto implementation, and that split matches the charters in `[claude-shakedown.md §2.2]` (Ashitaka = integrator, Okkoto = builder). Mokku fits taxonomy consulting only. **Needs J7 ratification, but the docs converge on Ashitaka/Okkoto.**
2. **GBrain hosting.** Docs answer: Mononoke-only v1 with NAS backup `[gbrain-substrate.md §9 line 76]`, and the shakedown's own peer-host warning (§2.1) independently argues against Outpost in v1 — the only Outpost-facing piece (Matrix bot) is already deferred to v2. **Effectively answered; J7 rubber-stamp.**
3. **P11 deliverable — spec only vs spec + skeleton.** Docs answer: spec only `[gbrain-substrate.md §9 line 79]`, and note the spec *already exists*, so P11's status "not started" in `[starros-stack-spec.md §11 line 198]` is arguably wrong — P11-as-spec is done pending acceptance. **Needs J7 to accept the spec and re-status P11; the skeleton becomes a new card.**
4. **Per-project granularity.** Docs answer: one substrate per J7-named project `[gbrain-substrate.md §9 line 77]`, consistent with the per-board kanban SQLite pattern `[persistence-boundaries.md line 20]`. **Effectively answered.**
5. **6th external tool.** Docs answer: **no** — `[external-workers.md §1 line 17]` requires an ADR for a 6th, no candidate is named anywhere, and the 5th (Claude Code) isn't even installed yet (P6). Finish P6 before widening.
6. **Mission Control revival trigger.** **Not answerable from docs** — no doc defines a re-evaluation trigger; fable-global says only "re-evaluate at Phase P2," which is circular (P2 *is* the revival). Needs a J7 decision naming a concrete trigger (e.g., "after P0+P1+P4 close" or a date).
7. **Hermes Workspace flake input — keep or remove from `flake.nix`.** **Not answerable from docs** — `flake.nix` is not in this repo, and the glossary only records the kill. Given "intentionally killed," removal is the hygiene-consistent move, but it touches `/etc/nixos` and is therefore **Ishii + J7** territory per `[external-workers.md §3 line 30]`.
8. **AionUI addendum timing.** **Not answerable** — the placeholder `[aionui-addendum.md]` has no owner or date. Since it's Mission-Control-adjacent UX and Mission Control is paused, the honest answer is: either park it explicitly ("blocked-on P2 revival") or delete the placeholder from canonical `specs/` until content exists. Needs J7/Nago.
9. **PR-2 review lane — who reviews canonical-doc PRs.** Answerable by precedent: E1-T8 shows Jigo reviewed the doc-canon PR pair `[backlog.md line 23]`, and the spec's slack table puts ADR/schema/template changes at "San + Jigo + J7" `[starros-stack-spec.md §4.1 line 82]`. **Answer: Jigo is the reviewer wolf; San preflights; J7 gates.** The real gap is that `prompts/jigo-review.md` doesn't yet describe doc-canon review (issue #8).

---

## 4.5 The 4 deferred Jigo minors

1. **GBrain card dedup (E2-T1 vs spec).** Reconstruction: Jigo flagged that E2-T1 ("was OKF/GBrain") and the Phase-P11 card describe one deliverable, risking double-carding. Verified live: E2-T1 and E3-T12 duplicates plus the E1-T5 mis-citations (fact 8). **Land pre-Sprint 0** — San kanbanizes from this exact file; the dedup is a 3-line edit that prevents runtime duplicate cards. Deferring it converts a doc minor into a board defect.
2. **`profile.yaml` canonical location.** Reconstruction: Jigo flagged that readers can't tell whether `~/.hermes/wolf-souls/_profile-template.yaml` (staging/template) or `~/.hermes/profiles/<wolf>/profile.yaml` (instance) is canonical, since `[persistence-boundaries.md line 11]` names the profiles tree and `[runtime-state.md §6 line 81]` calls wolf-souls "staging" without mentioning the template file at all. **Land pre-Sprint 0 as a one-sentence note** in persistence-boundaries ("template lives in staging tree; instances in profiles tree are canonical") — cheap, and P9 (agent cards) plus P1 (wolfpack.nix seeding) both touch this boundary soon.
3. **Honcho row wording (spec §3 vs 0003 glossary).** Reconstruction: "removed" vs "de-scoped" inconsistency. Verified, and escalated by this audit to issue #2 because the service is still *running* — the wording drift is masking an unmade operational decision. **Land pre-Sprint 0**, and pair the wording fix with the stop/keep decision so the words finally mean something.
4. **Mission Control source-dir pointer.** Reconstruction: Jigo flagged that "Hermes Workspace" (killed flake input, per glossary) and `hermes-workspace-src/` (the *kept* source dir for *paused* Mission Control, `[starros-stack-spec.md §10 line 166]`, `[runtime-state.md §3 line 62]`) share a name across a live/killed boundary, and the paths disagree in absoluteness. **Genuinely can wait** — Mission Control is paused and nothing in Sprint 0 touches the dir — *provided* the glossary gains one clause now: "the `hermes-workspace-src/` directory holds paused Mission Control source and is unrelated to the killed flake input." One clause now, full cleanup at P2 revival.

---

## 4.6 Concrete recommendations (ranked)

1. **Resolve the multiplex target sentence.** *Where:* `specs/starros-stack-spec.md` §2 item 3 (line 33); new ADR-0004 if the choice is single-gateway. *Who:* J7 (decision) + Ishii (feasibility). *Risk:* low (doc edit) but the decision itself is medium. *Effort:* small. Unblocks P0's definition of done.
2. **Add `forbidden_paths` + `report_back_channel` to board-schema and a minimal transition-authority table.** *Where:* `kanban/board-schema.md` lines 16–29 (fields) and a new §Transitions. *Who:* San (author) + Jigo (review). *Risk:* low. *Effort:* small. Closes issues #3 and #4 in one PR.
3. **Decide Honcho's runtime fate and normalize the status word.** *Where:* `docs/runtime-state.md` §2 line 40 + §3; `specs/starros-stack-spec.md` §3 line 61; `decisions/0003` line 46. *Who:* J7 (decision) + Toki (execution if stopping) + Ishii if the podman unit is Nix-managed. *Risk:* medium (touches a running service). *Effort:* small.
4. **One cross-reference sweep PR.** Fix the four dangling anchors, the two E1-T5→E1-T3 citations, the E2-T1/E3-T12 dedup, the duplicate Mnemosyne restart procedure (pick one), the stale spec §13/§14 provenance, README milestones, and delete or regenerate `TREE.txt`. *Where:* per §4.2/§4.3 citations above. *Who:* San (author) + Jigo (review). *Risk:* low. *Effort:* medium (breadth, not depth).
5. **Add AMB to both canonical maps and unify phase labels.** *Where:* `specs/starros-stack-spec.md` §3 table + `docs/runtime-state.md` §2 port map (`:6380` row); define or retire "Phase 1A/1C" in `decisions/0003` glossary. *Who:* Ishii (owns P8) + San. *Risk:* low. *Effort:* small.
6. **Re-sequence the Outpost Traefik fix ahead of Sprint 0.** The public-404 fix is documented as a one-line sed + HUP `[runtime-state.md §3 line 61]` yet sits at P10; a source-of-truth repo that 404s publicly undermines every workflow that fetches it by URL. Keep the peer-host discipline (it's Outpost's Traefik, so it's **Toki/Ishii on Outpost's admin path**, not a Mononoke change). *Where:* `kanban/backlog.md` E3-T11 ordering; `specs/starros-stack-spec.md` §11. *Who:* J7 (re-sequence) + Ishii/Toki (execute). *Risk:* low-medium (peer host). *Effort:* small.
7. **Fix or retire the two example packets.** Replace with one live-component example (P9 agent-card authoring is ideal: bounded, real, non-paused) or stamp both as historical; add the missing `Report-back channel` line either way. *Where:* `packets/examples/*.md`. *Who:* Okkoto (owner of external-worker policy) + Jigo. *Risk:* low. *Effort:* small.

---

## 4.7 What I did NOT find

Stated per shakedown §4.7, because false negatives are the dangerous failure mode:

- **No approval-bypass lanes.** I went looking for a path by which an external coder worker, or a wolf acting solo under §4.1 slack tolerances, could touch ADRs, `specs/`, NixOS modules, or secrets without a human/Jigo/Ishii gate. The prose gates are complete and mutually consistent (`[external-workers.md §3, §5]`, `[starros-stack-spec.md §4.1]`, `[docs/playbook.md]`). The only structural weakness is enforcement (issues #3–#4), not policy.
- **No secrets in the repo.** I checked for committed credential material. The BSM project UUID and the `BWS_ACCESS_TOKEN` *pointer* in `[starros-stack-spec.md §6 line 101]` are identifiers/paths, not secrets; Matrix room IDs are partially elided. Nothing resembling a token, key, or password is committed.
- **No second control plane.** No doc proposes Notion/Confluence/alternate boards; Nextcloud Deck is explicitly demoted `[starros-stack-spec.md §5 line 95]`; GBrain is carefully fenced as pointers-not-content `[gbrain-substrate.md §5, §8]`. ADR-0001 discipline held everywhere I checked.
- **No paused-component resource allocation.** Outside the two stale example packets (issue #9), no live plan, card, or phase quietly allocates Sprint-0 work to Mission Control, Honcho, or the Hermes Workspace flake input. The pause discipline is well-propagated (fable-global banner, glossary, spec §3, runtime-state Top-5).
- **No Megapack bleed-through.** The single Megapack reference in StarrOS canon (`[starros-stack-spec.md §7 line 112]`) carries its explicit cross-reference, exactly as the shakedown demands. Persistence-boundaries' Nextcloud/CryptPad *examples* mention Megapack paths, but examples are illustrative, not scope claims.
- **No wolf-charter contradictions.** Owner assignments across spec §3, §10, backlog E3, and external-workers are mutually consistent with the ten charters (Ishii on all NixOS, Jigo on all review, Okkoto as fixed operator, etc.). I found zero cases of a card owned by a wolf outside its charter.
- **No inconsistency in the Top-5 broken list.** Shakedown §2.5, runtime-state §3, and spec §11 phase statuses tell the same story about what hurts today (with the single exception of the Mnemosyne restart-procedure duplication, fact 10, already ranked).
- **Categories I could not audit at all** (not "clean," just invisible from the repo): the actual SOUL.md contents, `wolfpack.nix` and any `/etc/nixos` module, the Hermes Kanban DB and card `t_377762_b187`, the PR bodies, `flake.nix`, the three cited runtime skills, and live port truth. Every runtime claim above is "as documented," not "as observed."

---

## References

- `decisions/0001-repo-is-source-of-truth.md`
- `decisions/0002-human-authors-playbook-v0.md`
- `decisions/0003-canonical-spec-boundaries.md`
- `docs/runtime-state.md`
- `docs/persistence-boundaries.md`
- `docs/external-workers.md`
- `docs/playbook.md`
- `docs/workflow.md`
- `specs/starros-stack-spec.md`
- `specs/gbrain-substrate.md`
- `specs/aionui-addendum.md`
- `kanban/README.md`
- `kanban/board-schema.md`
- `kanban/backlog.md`
- `packets/leaf-card-template.md`
- `packets/examples/backend-kanban-adapter.md`
- `packets/examples/ui-preview-panel.md`
- `prompts/san-handoff.md`
- `prompts/jigo-review.md`
- `prompts/fable-global.md`
- `prompts/claude-shakedown.md`
- `README.md`, `TREE.txt`
- git history: commits `524fbfe`, `99b5b49`, `21dee6d`, `cdaaa02`; blob `908aae4a4b`
