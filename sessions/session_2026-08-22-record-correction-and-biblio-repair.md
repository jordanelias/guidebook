# session_2026-08-22-record-correction-and-biblio-repair

**Span.** 2026-08-22. **Branch.** `claude/provenance-walk-review-dyw1xk`, PR #113.
**Form.** DR-2026-08-19 §7 — agonist/antagonist. Acts 0–3 of
`workplan/2026-08-22-agonist-antagonist-execution-plan.md`, which this session executed.

**Purpose.** Execute the plan's unblocked acts: correct the record, land two code fixes, repair the
bibliography from payloads held on disk. Stop at the owner gate — acts 4–6 need OD-A…OD-G.

**Not a research session.** No search logged, no source admitted, no synthesis authored.
`search_executions` 9 at open and at close; `evidence_sources` 5; `specifications` 0.
**`sessions/LATEST-RESEARCH` is deliberately NOT moved** — it points at
`session_2026-08-19-research-batch-01-room-acoustic-performance`, which has subjects, and `L04`
passes because of that. This session repaired existing rows; it did not create research subjects.

**The canonical DB changed.** `f70c48d7…03c2c` at open → `3a8828f6…c4716` at close.
Two data migrations, both through `emit_batch_sql` → `emit_data_migration` → `migrate_db`:
`data_20260822012151` (the bibliographic repair) and `data_20260822012400` (the tier-derivation
scope). `user_version` 60 throughout. Rebuild + `migration_reproducibility --deep` PASS;
`test_db_integrity` **72/72**.

---

## 1. What the DB now says that it did not say this morning

**The bibliography is true as stored.** `volume`, `issue`, `pages_start`, `pages_end`,
`article_number`, `issn` and `pub_month` were NULL on all five sources while the Crossref payloads
retrieved on 2026-08-19 supplied every one of them, and all five rows were stamped
`metadata_quality='COMPLETE'`. Every value written was derived **in code from the payload bytes**,
never typed: the script reads `retrieval-log/…/manifest.jsonl`, opens the artefact, and takes the
field. All five artefact sha256s were verified against the manifest first.

**Two mis-filed article numbers moved.** `REF-00968.pages='2645738'` and
`REF-00607.pages='23312165241273399'` were article numbers sitting in a page-range column. The
2026-08-20 record called REF-00968's value one "no payload asserts" — **it is asserted**, as
`article-number`, with `page` null. The repair is a field move, not a deletion, and REF-00968 was
not the only instance. `REF-00965` and `REF-00967` are **not** instances: their payloads assert
`page` as well as `article-number`, so their `pages` values stand.

**Two titles are payload-exact again.** `REF-00968` had lost the possessive apostrophe in
`students’`; `REF-00966` had straight quotes where the payload has typographic ones.

**Nine ORCIDs.** Held in the payloads, NULL in the DB. An ORCID is the most durable identifier a
person has in this record.

**Emily's name is now defended in the row itself.** `evidence_source_authors.corporate_name_note`
on REF-00966 position 3 says, in the table, that `andsensory` is the surname and `Emily` the given
name, that she publishes as **@21andsensory**, that the correct rendering is **Emily
(@21andsensory)**, and that these co-authors were deleted once already on 2026-08-19 from the paper
whose entire Co-1 warrant *is* their co-authorship. Per D-2, that reasoning belongs in a table
column, on the same surface as the data — not in prose.

**The Co-1 warrant fields are closed, and the tier question is not.** `co1_provenance` and
`co1_source_type` were NULL on all three Co-1 rows — a tier asserted with its warrant columns
empty. Both are now populated with the values the *retrieved record* supports and nothing more:
`published_corpus` (the closed enum's pre-launch value — how the citation reached us, not a
judgement) and `peer_reviewed_literature` (the payload types each `journal-article`; it is also the
value that claims the least, since `assess_cell.source_grain()` treats it as specific rather than
aggregate grain). The `notes` on each row say explicitly that this **does not settle the tier**, and
name **OD-D**.

## 2. The finding this session did not go looking for

`adjudication_integrity.py` is quarantined, so `run_checks.py` never selects it and no CI run has
executed it in weeks. The plan said to **delete** it — kept in the 2026-08-20 cull on a claim that is
demonstrably false (`test_adjudication_integrity` is not a registered check; the id appears in
`check-registry.yaml` exactly once, inside another entry's prose).

Running it before deleting it is what changed the answer:

> `FAIL: 5 tier-derivation inconsistency(ies) of 5 checked` — every one *underivable*, because
> **`scope` was NULL on all five sources** and `schemas/tier_derivation.py` keys the ratified tier
> table on `(evidence_type, scope)`.

**Every stored tier was asserted with its own derivation input missing.** Same defect class as
`co1_provenance` being NULL, one layer deeper, and invisible to all 63 registered checks because the
only gate that looks is the one nothing selects.

Four were repaired: `co1` and `sr_meta` admit exactly **one** valid scope (`intrinsic`), so the value
is *determined by the ratified table, not judged*, and the derived tier equals the tier already
stored — **no tier changed**. The fifth, REF-00967, was deliberately left NULL: `clinical` admits
`high_control` → Tier 1 and `lower_control` → Tier 3, the stored tier is 1, and writing
`high_control` would harden by a clerical act exactly the tier the 2026-08-20 antagonist disputes.
That is **OD-E**. The gate still reports one inconsistency, and it should: it is pointing at a real
open question, which is what a gate is for.

**The plan's recommendation is withdrawn in the plan, with the reason.** F-23a was right that the
keep-rationale was false; the recommendation then inherited the cull plan's *other* claim — measured
PASS/0 on 2026-08-18 — without re-running it. That claim was true when made and false three days
later, because the 2026-08-19 batch landed five sources in between. A correct finding about a false
premise produced a wrong recommendation, and only running the thing caught it.

## 3. Code: two fixes, and one widening that was not planned as one

**`retrieval_log.py` names artefacts for what they contain** (defect B5-f, deferred once). Every
artefact was written `<sha16>.json` regardless of content, so a full-text attempt returning HTML
landed as unparseable JSON and the **blocking** `check_json` gate went red. That was repaired *in
data only* on 2026-08-20 by hand-renaming files; the cause stayed live, and the next full-text fetch
would have re-reddened CI. Now the extension is sniffed from the body — and verified by running the
new logic over **all 22 held artefacts**, where it reproduces the hand-corrections exactly, 22/22.

**BRK-26 is fixed: `assess_cell.py` no longer rewrites `v_best_practice`.** It DROPped and re-CREATEd
the view mid-determination and shipped that DDL inside the emitted replayable SQL. Verified after the
change: the engine's emitted SQL contains no DDL, the view in a probe DB is byte-identical to
canonical, and `test_assess_cell_pilot` passes.

**BRK-25 is refuted, not fixed.** The handoff said to "do BRK-25 in the same pass". Doing so would
have **reverted ratified doctrine**: `_archived/scripts/migrations/029` implements DR-2026-07-21, in
which a regulatory-stratum-only cell *is* best practice at the **weak** band — flagged, never
suppressed — and it deliberately dropped the two migration-027 guards BRK-25 asks for. BRK-25 quoted
CLAUDE.md's *"walled off"* without *"from full-strength anchoring"*, and cited neither the DR nor the
migration. Recorded in the map as `REFUTED`, severity `high` → `informational`.

**`verify_authors` now checks bibliographic fidelity too**, and this replaces the new check the plan
proposed. The plan wanted a check to stop Emily's name being deleted again; `author_fidelity`
**already does that** — it diffs stored surnames against the payload — so adding one would have been
apparatus for a job already done. What was actually missing was field coverage: the verifier examined
authors only, which is *why it printed CLEAN* over five rows whose bibliography was empty and
mis-filed. Widened, it **fails on the pre-repair DB** (`rc=1`, 2 mis-files, 11 gaps) and is **CLEAN
after** — reproduce, then fix, then show the same check passing. `author_fidelity` stays **advisory**:
its registry entry sets promotion after the second research batch, and there has not been one.

**`emit_batch_sql.py` now captures `evidence_source_authors`.** Its absence was not neutral — that
table is where the 2026-08-19 fabrication happened, and because the capture path could not see it,
the repair had to be hand-written, through the same channel the fabrication entered by. Selftest 9/9,
and the change earned itself immediately: 10 of this session's 15 captured updates are author rows.

## 4. The caller sweep CLAUDE.md owed its own rule

CLAUDE.md was rewritten 2026-08-19 to §0–§8. **28+ live references still pointed at §9 and §10**, and
two of them cited *guardrail 4* — "retirement is owner-gated" — which §1 did not renumber but
**inverted**. That is worse than a broken pointer: an obsolete rule cited as live authority, and it
was load-bearing, since it is part of what kept 220 LOC alive in the cull.

Swept, with a visible `[pointer corrected]` marker on each: `references/` (3), `skills/` (4),
`governance/retired-vocabulary.yaml` (6), `governance/check-registry.yaml` (3), `scripts/` (5),
`.ignore` (2), and two ratified DRs where the citation was factual rather than doctrinal.

**Deliberately not swept:** `scripts/migrations/*.sql` and `data/decisions/decision_register.yaml`
(committed migrations are immutable by rule 3, and a decision's recorded rationale is what it was),
and `_archived/`, `workplan/`, `attestations/`, `audits/` (frozen records — 31 files). `.ignore`
**entries** were proven unchanged by diffing the non-comment lines against HEAD; only comments moved,
because changing the scope of that file is owner-gated on its own footing.

Also corrected: CLAUDE.md §1's hardcoded *"~35k executable LOC"*, stale since the cull removed 6,716
of them, replaced with the command that derives it.

## 5. Records corrected rather than absorbed

| Where | Was | Is |
|---|---|---|
| provenance-walk attestation | `doctrine_sha: 8366c28`, and a reason built on "the doctrine SHA moved" | `0f2f525`. It did not move; `8366c28` is the 2026-07-25 merge of PR #71. The conclusion survives its broken premise |
| same, deviation 1 | "the plan's own section 9 forbids" the sha moving | §9's eight forbids contain no such clause; §4.5 explicitly permits it |
| same, counterclaim | "400-line", "thirty-one commits" | 791 lines, 33 commits — both understated the charge |
| session record §7 act 4 | "an article number no payload asserts" | supported but mis-filed; REF-00607 is a second instance |
| `check-registry.yaml:253` | "RED on main (63/69 as of 2026-08-04)" | **72/72**, re-measured. Scheduled and skipped by three prior plans |
| `adjudication_integrity` reason | "RED — 274 tier inconsistencies" | 1 of 5, and it is OD-E. The 274 predates a reset that deleted the corpus producing it |
| `pipeline-map.yaml` | 6 defects | BRK-25 refuted; BRK-26 `guard:` line inverted the meaning of the code it cited; BRK-24's "11" → 17; a phantom list cross-reference; a false grep result *inside the paragraph about grep discipline*; `unclassified_paths` re-derived to **1,232 of 2,174 (57%)**, and it named `README.md`, which does not exist |
| `record-command.py` | "is_error is what it actually carries" | measured false. The payload carries `interrupted, isImage, noOutputExpected, stderr, stdout` — no `exit_code`, no `is_error` |

## 6. Provenance, measured instead of assumed

The command-log hook asserted in a comment that the harness payload carries `is_error`. Its own log
falsified that — 354 real events with both fields null — so the hook now records `response_keys`, and
one turn of that measurement gave the real answer above. Acting on it: **`stderr` was being thrown
away**, which is why the log could not tell a gate that passed from one that raised. It now records
`stderr_bytes`, `stderr_sha256` and `interrupted`.

The always-null fields are **kept, not deleted** — the log is append-only and 356 lines already carry
that schema — with an instruction in the code that no gate, session record or attestation may cite a
line in this file as evidence a command *succeeded*. It proves a command was **issued**.

`.claude/session` was stale, pointing at the previous session, so the 2026-08-21 digestion session's
commands were filed under it. Repointed before any other work this session.

**Still open and outside this repo:** `/root/.claude/stop-hook-git-check.sh` carries no exclusion for
the tracked command log, so the livelock the last session diagnosed is armed again on every fresh
container. The durable fix is in the owner's own `~/.claude/`:
`git diff --quiet -- ':(exclude)scratchpad/*/commands.jsonl'` and
`git ls-files --others --exclude-standard -- ':!scratchpad'`. **Note the tension nobody has recorded:**
that same dirty-tree complaint is currently the *only* thing prompting anyone to commit the log, so
installing the exclusion naively turns "saved always" into "saved when an agent remembers".

## 7. My own errors

| error | how it was caught |
|---|---|
| Wrote "eleven days" for the interval a stale DR line stood | Arithmetic against the dates in the same sentence — the DR is 2026-08-19 and today is 2026-08-22. Three days |
| Planned to delete `adjudication_integrity.py` as vacuous | Running it: FAIL, 5 of 5, on a defect nothing else can see (§2) |
| Accepted a `grep` that failed on a missing file as proof no DDL remained | The grep printed an error and the `||` branch printed "none — clean". A non-existent file is not an absent string. Re-run after installing pydantic so the artefact actually existed |
| Corrected "400-line" in one place and left the same figure in the next sentence | Re-grepping the file for `400` after the edit |
| A pointer-correction edit that split a sentence across a comment | Reading the patched lines back |
| **Wrote a placeholder sha256 (`2d5f4e10…`) into this record's own header**, next to the words "derive it; do not read it here" | Deriving it. The real value is `3a8828f6…c4716`. This is §2(b) committed inside the session record correcting other people's §2(b) failures, and it would have been indistinguishable from a real hash to every reader and every gate |

The generalisable one is the third. **A tool that could not have seen the thing is not evidence of
absence** — the failure family the previous session recorded five times in its §6, reproduced here
under a different disguise: not a stale grep, but a grep whose *subject did not exist*.

---

## 8. HANDOFF — the next act is the owner's

**Read:** `decisions/DR-2026-08-19-…` (amended §3), then
`workplan/2026-08-22-agonist-antagonist-execution-plan.md` §2.

**Acts 0–3 are done. Acts 4–6 are blocked, and not on work — on seven decisions.**

- **OD-A** — are `item_population_links` substrate or scaffolding? All **372** carry `rationale_ref`
  NULL. If scaffolding, D-1 quarantines them and **no cell is determinable anywhere**. If substrate,
  A-18's absence is a gap to fill. *Recommendation: substrate, provisionally, with any edge a
  determination relies on re-derived and given a `rationale_ref` in that determination's own migration.*
- **OD-B** — do deaf and hard-of-hearing people belong on `room-acoustic-performance`? `DEAF` holds
  16 links, **none on this slug**, while the only Tier-1-anchored value on the parameter is theirs.
- **OD-C** — A-18's applicability set. *Recommendation: DEAF, AUT, NDV, DEM.*
- **OD-D** — REF-00965 / REF-00968 Co-1 → T3? Needs full texts this environment cannot reach.
- **OD-E** — REF-00967 T1 → T3? **Now blocking a live gate**: its `scope` cannot be written until
  this is answered, and `adjudication_integrity` reports the inconsistency until it is.
- **OD-F** — ratify or refuse the adversarial-subject waiver.
- **OD-G** — strike DR §12.1 Step 10's `jurisdictional_values` clause. An interim **STOP** notice is
  in place at that step; the deletion is the owner's.

**State at handoff.** `user_version` 60 · `evidence_sources` 5 · `specifications` 0 ·
`search_executions` 9 · `data_migrations` 335 · registry 63 checks / 4 quarantined ·
`test_db_integrity` 72/72 · reproducibility PASS (`--deep` too) · preflight **PASS**, 50 green,
9 nothing-in-scope, 4 advisory failures — **all four measured identical on `origin/main`** in a
worktree (`validate_pydantic_schemas` 246 findings both sides; `validate_reasoning` errors on a
pilot-era reasoning doc this branch never touched; `retired_vocabulary`; `test_verification_pipeline`).

**Do not** author a determination as the next act, and now for a second, independent reason: A-18 has
no lawful applicability edge (BRK-20) **and** no engine can address it — `assess_cell.py` carries
seven hardcoded pilot cells, none on this slug, stamps a July 2026 session id on every row it writes,
and **crashes on today's data** before emitting anything (`next_gap_id()` returns `GAP-1` because it
parses `GAP-B01-001` as non-numeric, which fails the `GAP-NNN` validator). Verified identical on
`origin/main`, so it is not this branch's doing. Not fixed here: nothing uses it, and repairing it
would make a dead pilot engine look usable. Act 5 authors by hand SQL, as DR §12.5 requires.
