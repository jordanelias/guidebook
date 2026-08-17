# 2026-08-17 — Consolidated action plan

**Provenance.** A read-only audit and consolidation pass (Fable 5) over (a) the two artifacts produced
on 2026-08-16 — `workplan/2026-08-16-adversarial-critique-and-execution-plan.md` and
`sessions/session_2026-08-16-pr103-adversarial-pass.md` — and (b) every commit from 2026-08-10 to
2026-08-17, PRs #91 through the current branch. Written out here by Opus 5.

**This document supersedes the five-wave plan in `workplan/2026-08-16-adversarial-critique-and-
execution-plan.md` §Part 3.** That plan was written before the audit and before five further findings
existed. Its findings stand (all ten survived attack); its *sequencing* is replaced by §6 below.

**Status of every figure here.** Every number was live on **2026-08-17**. This repository's own
registers are the standing proof that such figures rot. §7 lists the ones that must be re-derived at
execution time rather than carried from this page.

---

## 0. What the audit changed about the previous two documents

### 0.1 Corrections to my own work, stated plainly

Four errors in the 2026-08-16 artifacts, all mine, all now verified:

**E1 — HIGH. The PR #103 pass broke a check, and its commit body claimed the opposite.**
`attestations/sessions_session_2026-08-16-pr103-adversarial-pass.json` cites the rule identifier
`integrity-protocol`. That identifier is not registered, so `attestation_evidence` now fails:

```
CHECK 3: attestations/sessions_session_2026-08-16-pr103-adversarial-pass.json
         unknown rule identifiers: ['integrity-protocol']
```

Commit `b17163f` states *"3 advisory, all pre-existing."* The true count at that tree is **4**, and the
fourth is new and self-caused. Re-measured this session: advisory set = `retired_vocabulary`,
**`attestation_evidence`**, `research_dod`, `validate_reasoning`.

The mechanics are almost certainly benign — checks run, then attestation authored, then commit — but
the mechanism does not matter. The claim is false on the record, and the failure is this repo's named
pattern: *final state not re-measured before the claim was written.* It occurred inside the artifact
whose subject was obligations that go unverified.

**E2 — the root cause is not mine, and is worse than the symptom.** `skills/integrity-protocol_SKILL.md`
reads *"Status: ACTIVE — ratified by owner directive 2026-07-13"*, and the 2026-07-13 register records
that flip as EXECUTED item 1. But `integrity-protocol` appears in **neither** the "All active skills"
block of `references/skill-registry.md` (lines 64–83) **nor** `EXTRA_RULE_IDS` in
`scripts/audit/adherence_log_audit.py` (lines 84–112) — both verified absent this session. That is
**34 days of registry drift against an owner-ratified skill**, and it is precisely the defect class
`DR-2026-07-13-attestation-rule-identifier-registry-gap` (Q23) was ratified to close. It surfaced only
because an attestation happened to cite it.

**E3 — MEDIUM. C3 overstated its executor scenario.** The critique said *"an executor applying the rule
as written misses it"* of `jv 38` (`DIN 18040 + DIN EN 81-41`). The rule misses it; the plan's **own
example list names it** (`2026-08-15-instrument-status-backfill-plan.md:90`). Also: **the headline
count 22 is correct.** What fails to reproduce is the stated *rule*, not the number. C3's remedy —
enumerate by `jv_id` — is unchanged and still right, and the `jv 84` trap is unaffected and is the
part that matters.

**E4 — LOW. C4 mis-ranked ISO.** I called it "the third-largest jurisdiction in the table." Live: DE 20,
GB 20, US 20, AU 18, **ISO 13** — fifth. The substantive claim (ISO carries 13 rows and has no
`lang_jur_map` entry, so acceptance test 6 cannot pass) is unaffected.

**E5 — the pass under-sold the DR, in the direction that flattered its own finding.** P1 said H1 *"says
only 'three anti-gaming disciplines (adversarial-review hardening)'"*. In fact
`DR-2026-07-13-value-genealogy-and-derivation-handshake:21` spells out all three disciplines' content
nearly verbatim. What §4.5 actually added is the *enforcement-strength characterization* —
"structural rather than editorial" — which is what P1 attacks, so **the finding stands and its
severity is unchanged**; the characterization of the DR was unfair and is corrected here.

**E6 — MEDIUM. The brief was marked DISCHARGED with roughly half its checklist unaudited.** Brief §3
lists eight author claims. The pass records no verdict on **claims 2, 5, 6, 7 and 8** (re-run `--all`;
write *different* matcher probes; re-measure "33 occurrences"; test the DR-2026-07-22 merge-ratification
reading against the merge rule's four limits; third verification of the `schema-spec.md` currency
fill), and never weighed the A2 design call the brief handed forward. Attack surfaces A1, A3, A4 are
genuinely discharged; the §3 claim list is not. `DISCHARGED` is the wrong single word for that state.

### 0.2 What survived the audit

All ten critique findings (C1–C10) and all six pass findings (P1–P6) survive as substantively correct,
with the nuances above. Independently re-derived by the auditor: C1's zero-flag conclusion, traced
through `iter_text_files()` at `scripts/audit/retired_vocabulary_audit.py:167–186` rather than
inferred; C9's dead exemptions, traced through the compiled `glob_to_re()` output; P1's DDL and
`git grep -l` results; P3's four live locations and the PR #103 diff line; P4's single-file grep
result; P5's three escape lines. The recorded near-miss was real and its retraction correct.

One time-bound caveat: the critique's claim *"the 2026-08-16 baseline reproduces exactly"* was true at
`a251fb6` and is **no longer true at HEAD** — because of E1.

### 0.3 Five findings neither 2026-08-16 artifact reached

**N1** = E1/E2 above. **N2, N3, N4** below; N5 = E4.

**N2 — MEDIUM. The remedy P4 proposed cannot reach two of the four targets P3 found.**
P4 proposed registering the repealed Person-Mode formulations in `governance/retired-vocabulary.yaml`.
But `references/project-standards.md` is **globally exempt** (`retired-vocabulary.yaml:92`) as the
append-only ledger. So the tripwire can never flag `:14` (the ledger's *definition* of Person Mode) or
`:202` (the mandated *format string*) — the two most consequential of P3's four hits. A session that
adds the entries, sees green, and declares the semantic debt closed would be wrong.

The correct mechanism exists and is different: the 2026-08-14 remediation workplan §4 established, by
verification rather than assumption, that **amend-in-place on the append-only ledger is licensed**
(four ledger rules already carry dated in-place reconciliation clauses citing their DRs). Neither
2026-08-16 artifact connected these two facts.

**N3 — MEDIUM. Vacuity has two polarities and only one is instrumented.** The 2026-08-14 work fixed and
instrumented *green-on-zero*. Live today, uninstrumented, is *red-on-zero*:

- `test_directness_2_2`'s live-smoke leg asserts `n > 0` (`scripts/tests/test_directness_2_2.py:114`)
  against `evidence_population_match`, which is 0 rows post-reset.
- `test_verification_pipeline` G01–G03 assert thresholds ≥50 / ≥30 / ≥100 against the deliberately
  emptied corpus.

And `governance/check-registry.yaml:1220` **mis-describes** the first: it claims the live-smoke leg
"SKIPs when `/tmp/work14.db` is absent (it is, in CI)". False — `scripts/run_checks.py:446` does
`env.setdefault("GUIDEBOOK_DB_PATH", "data/guidebook.db")`, so under the runner the leg always runs
against the canonical DB and fails deterministically.

Why this matters beyond tidiness: it makes the advisory-failure count an **ambient constant**. Sessions
verify "same six" as a *number* rather than as a *set* — which is exactly how E1's new, seventh failure
entered unremarked. The two polarities are one throughline (T4), and the red one is the one that just
cost us.

**N4 — the migration-054 renumbering note and five other obligations live only in commit messages or
closed register sections.** Enumerated as G4–G11 in §5.

---

## 1. Throughlines

Five root patterns account for nearly every outstanding item. This is the consolidation the plan is
built on: **~45 tracked items reduce to five causes.**

### T1 — Ratification produces prose, not mechanics; and the fix for that is itself stuck in prose.

Every ratified-but-unimplemented item shares one mechanism: ratification writes an obligation into a DR
or a register, and nothing converts it into a check, a registry row, or a gated artifact. Instances
outstanding: Q5-H2/H3/H4, Q6, E10 (ratified 2026-07-13, unbuilt), DR-2026-07-14's "tracked second
pass", Q21's re-statement, F6, the migration-054 renumber note, the Universal/Population tension.

The designed cure already exists on paper — **remediation Track B commit H**: `decision-protocol.md`
gains a §3.5 requiring a superseding DR to carry a Ratification Sweep section, repealed formulations
join the retired-vocabulary apparatus, and `ratification_sweep_audit.py` enforces the coupling. It is
deferred to the owner track and unexecuted. **So the cure for T1 is currently an instance of T1.**
That is the single highest-leverage observation in this document.

### T2 — Enforcement is token-level; the expensive drift is proposition-level.

The tripwire can police *spellings*. The repo's costly drifts are *meanings*: "position within range"
surviving under corrected vocabulary (P3); three skills teaching the superseded evidence ladder in
current words (Q3); "Tier 2" as a design-mode name inside a mandated format string. Every sweep that
moved words and left semantics is an instance — and N2 is the corollary: the exemption architecture
protects precisely the surface where semantic drift is most expensive.

### T3 — Volatile facts are derived correctly at measurement time and then violated at citation time.

`CLAUDE.md`'s own header rule says to derive volatile facts live. Sessions do. Then those figures get
*cited* from prose weeks later: Q19's four stale numbers; the register's "executable without owner
input" line; the remediation numbering table; `supersedes` reported as populated when it is `'[]'` on
all 162 rows; the brief's F1 premise; `CLAUDE.md` §7's "two blocking gates are red on `main` today"
(0 blocking, measured); `tooling-register.md` §4's "`test_db_integrity` STILL RED 26/35" (72/72 today);
and the "46/6" baseline. **The registers are the worst offenders because they are what sessions orient
from.**

### T4 — Vacuity has two polarities; one is fixed, the other is live and just cost us.

See N3. Green-on-zero: named, counted four times, instrumented 2026-08-14. Red-on-zero: live, unnamed,
mis-documented in the registry, and the direct enabling condition for E1.

### T5 — The independence budget is real, but the gate that spends it is advisory in fact.

Three sessions correctly treated cold context as consumable — two self-disqualified, one declared per
surface. Yet the P3 gate demanding the pass was **merged past** (C7); the pass that discharged it left
half its checklist silent (E6); and the discharge status was written into the brief *by the pass
itself*. A gate whose satisfaction is self-certified, in blocking language, is the process-layer twin
of T4.

### Recurrence counts, 2026-08-10 → 2026-08-17

| Failure mode | Count this week |
|---|---|
| Claim asserted rather than derived, caught later | **≥7** — the cull list; `supersedes` `'[]'`; two Mode-S facts in one attestation; F1's probe read backwards; C1's premise written into the brief; **E1's "3 advisory, all pre-existing"**; the register's "executable without owner input" line |
| Gate green on zero subjects (instrumented) | **5 blocking checks vacuous at every run** |
| Gate **red** on zero subjects (uninstrumented) | **2** — N3 |
| Obligation parked in prose, no mechanical tracker | **≥6** |
| Sweep does vocabulary, leaves semantics / one layer of N | **≥4** |
| Ratified decision whose named step never ran | **4 standing, 2 discharged late this week** |

Two incidents from the week deserve naming because they are worked examples the plan is built to avoid:

- **The SUPERSEDED round-trip.** An implementer retired the `SUPERSEDED` status on a reading the owner
  had not made, justified by `supersedes != ''` — which is the string `'[]'` on all 162 rows. String
  emptiness was queried; array population was reported. Overturned by the owner within hours; restored
  by migration 060. The ledger now permanently carries the round-trip.
- **`6d0f663`.** A re-derivation broke two claims in already-pushed, already-green commits. No gate
  caught either.

---

## 2. Conflicts — where two live sources disagree

Each carries a verdict and the evidence. These are not opinions; each was measured.

| # | Conflict | Verdict |
|---|---|---|
| **K1** | `workplan/ratification-execution-register-2026-07-13.md:268-270` lists Q5-H2/H3/H4, Q6 and E10 under **"Executable without owner input"**. `sessions/session_2026-08-16-ladder-and-vocabulary-sweeps.md:154-155` lists the same items as D-SCHEMA and untouchable. The instrument plan's first line says D-SCHEMA. The register contradicts **itself** at `:244-247`. | **The register line is wrong.** It is also the single most dangerous line in the repo: it is the sentence a next session reads to decide what it may author. |
| **K2** | `CLAUDE.md` §7: "two blocking gates are red on `main` today". Measured: **0 blocking failures**, `test_db_integrity` **72/72**. | **CLAUDE.md stale.** The 2026-08-14 batch corrected `preflight.sh` (`1ae54fd`, one file) and missed this — a one-layer-of-N sweep, T2. |
| **K3** | `references/tooling-register.md` §4: "`test_db_integrity` … STILL RED. 26/35". Measured 72/72. | **Register stale (dated 2026-08-01).** Consequential: its §6.7 recommendation *"do not require the DB-integrity job until its backlog clears"* is cited by `CLAUDE.md` and gates owner decision #10 — **and the backlog is clear.** The recommendation must be re-derived before #10 is decided. |
| **K4** | `governance/check-registry.yaml:1220` vs `scripts/run_checks.py:446`. | **Registry note wrong** (N3). |
| **K5** | Commit `b17163f` body: "3 advisory, all pre-existing". Its own tree: 4, one new. | **Commit wrong** (E1). |
| **K6** | `workplan/2026-08-15-adversarial-brief-pr103.md:30-33` vs `governance/retired-vocabulary.yaml:87`. | **Brief wrong** (C1), and **still live at HEAD** — `b17163f` edited the same file's status block and left the false premise standing. |
| **K7** | `skills/integrity-protocol_SKILL.md` header (ACTIVE, ratified) vs `references/skill-registry.md:64-83`. | **Registry block wrong** (E2). |
| **K8** | Ladder session: "four of the six findings are in no register", then lists six. F3 was tracked as remediation decision #9 *and* firing as RV-012. | **At most three were unregistered.** Both the commit's "four" and my critique's objection to it are off. |
| **K9** | E-register rows E2/E6/E12 read "authorized/owed"; the register's own closing line says done 2026-07-24. `slugs.serves_axes` exists (verified). | **Resolved in favour of "done"**; the rows still mislead a fast reader. Micro-discrepancy: E3 records 157 `item_axis_links`; live is **158**. Cause unattributed — plausibly F-07, unverified. |
| **K10** | Q19 row vs live taxonomy. | **Row wrong on all four numbers** (C6). |

---

## 3. Gaps — obligations that exist in no register at all

| # | Gap | How it was findable |
|---|---|---|
| **G1** | `integrity-protocol` missing from the active-skills block — 34 days of drift against an owner-ratified skill (E2) | Only because an attestation cited it |
| **G2** | Inverse-vacuity reds (N3); no register row, and the one registry note about them is false | Reading the runner's env handling against the registry's claim |
| **G3** | The exemption blindspot (N2) — the planned repealed-formulation tripwire structurally cannot police the ledger | Cross-reading a proposed remedy against the exemption list |
| **G4** | DR-2026-07-14's "tracked second pass" — found by P4, still tracked nowhere | `git grep` |
| **G5** | The Q21/B5 gate re-statement obligation | In-row concession, no tracker |
| **G6** | The **Universal/Population doctrine tension** — "as available as reasonably possible" vs "co-extensive with code compliance, the floor". Flagged OPEN inside the 2026-07-13 register at `:159`, follow-up 3. **Never given a Q-number; absent from every later plan.** | Only by reading a *closed* section of a 274-line register |
| **G7** | F6's fourth vocabulary ("Mode-6 / Tier-7") | Session finding only |
| **G8** | C1–C9 and P1–P6 themselves — no register row points at any of them | This document is the fix |
| **G9** | `validate_pydantic_schemas`' 246-finding accept/reject policy, "separate future work" since Q25 closed — a permanently red advisory with no owner queue entry | Running it |
| **G10** | The brief's five unaudited §3 claims, concealed by the DISCHARGED status (E6) | Reading the brief against the pass |
| **G11** | The migration-054 renumbering note (`6dd0cd3` body: "`locator_schemes` … should re-derive its number") | Commit message only |

**G6 is the most consequential.** It is a doctrine-level tension about what Universal Mode *is*, raised
by the owner's own articulation, flagged as open, and then lost inside a section marked closed. It is
DG-NON and has been invisible for five weeks.

---

## 4. Master inventory

45 items, deduplicated across both ratification registers, four workplans, three session records and
the two 2026-08-16 artifacts.

**Gate legend:** `FREE` no owner input, no schema change · `COLD` needs uncontaminated context ·
`D-SCHEMA` Change-Order gated (owner decision #4 batch) · `OWNER` owner decision · `DG-NON` owner-only
by doctrine, propose never decide · `RESEARCH` evidence work, not a sweep.

| id | Item | Gate | Blocks / blocked by |
|---|---|---|---|
| **I-01** | Strike the false F1 premise from the brief (K6); record the A2 design call as resolved | FREE | blocks I-10 |
| **I-02** | Register `:268-270` — move Q5/Q6/E10 out of "executable without owner input" (K1) | FREE | blocks safe orientation of every next session |
| **I-03** | Re-derive the Q19 row: 23 populations / 17 without a page / 93 items / **0** without a page | FREE | page *generation* remains a step-5 scope decision |
| **I-04** | Instrument plan §4 — replace the delimiter rule with the 22 enumerated `jv_id`s, add the third class (`jv 13`, `jv 15`), name `jv 38` and `jv 84` explicitly; §7 — name `ISO` in test 6, add `lang_jur_map` drift as D5 | FREE | precondition for I-20 |
| **I-05** | Forward-notes on ladder-session F1 (premise false) and F3 (already firing as RV-012, tracked as decision #9) | FREE | — |
| **I-06** | `CLAUDE.md` §3 — add the `working/` map line | FREE | interim for I-33 |
| **I-07** | Add `Mode-P`/`Mode-S` to RV-025/026; delete the two dead per-entry exemptions | FREE (CODEOWNERS review) | — |
| **I-08** | **Resolve `integrity-protocol`** — add to the skill-registry active block or extend `EXTRA_RULE_IDS` via the Q23 precedent (E2) | FREE-with-review | **blocks a green `attestation_evidence`; do first** |
| **I-09** | Correct `check-registry.yaml:1220` (K4) **and** decide the vacuity semantics for data-dependent live-smoke legs | FREE (note) / design call (semantics) | removes the ambient-red noise that hid E1 |
| **I-10** | Complete the pass residue: brief §3 claims 2, 5, 6, 7, 8 + the A2 design call — or record a scoped deviation and restate DISCHARGED honestly (E6) | COLD, or OWNER accepts partial | blocked by I-01 |
| **I-11** | P5's three line adjudications — `page-templates.md:262` heading rename, `navigation-modes.md:184`, `:320` | FREE | — |
| **I-12** | Tracker row for the Q21/B5 re-statement | FREE (row) / RESEARCH (substance) | blocked by corpus repopulation |
| **I-13** | Tracker row for DR-2026-07-14's second pass; seed repealed-formulation RV entries — **with the N2 caveat welded on** | FREE (monotone) | ledger targets need I-14 |
| **I-14** | Amend-in-place the ledger's Person-Mode semantics — `project-standards.md:14`, `:170`, `:202`; retire `:202`'s "Tier 2"-as-mode usage | OWNER-adjacent (mechanism licensed; meaning is doctrine — **propose**) | N2: unreachable by tripwire |
| **I-15** | `skills/item-specification-writer_SKILL.md:129` semantics | FREE | — |
| **I-16** | P1 hardening — FK or CHECK `root_id`→`external_root_registry`, CHECK coupling `untraced`→NULL `root_id`; P2 — re-word §4.5 to describe the live view | D-SCHEMA (constraints) / FREE-with-review (doctrine wording; `evidence-architecture.md` is **not** the SHA anchor, so no cascade) | cheap while `source_value_extractions` = 0 |
| **I-17** | Re-prototype the six Track-C migrations at 061–066 | FREE (prep) → D-SCHEMA | precondition for #4 |
| **I-18** | **Owner decision #4** — ratify the Group-3 batch | OWNER | unblocks I-16, I-19, I-20, I-21 |
| **I-19** | Q5-H2 (`functional_basis`, `derivation_paths`) + H3 `population_icf_links` + H4 gate | D-SCHEMA | cheap while `specifications` = 0 |
| **I-20** | Q6 `instrument_status` + `_basis` + D4/D5 guard + GB→UK + compound split | D-SCHEMA + OWNER (Band-B policy, #1, GB→UK ride-along) | blocked by I-04, I-18 |
| **I-21** | E10 ICCT `cross_test_pairs` + view + gate | D-SCHEMA | join the batch |
| **I-22** | **Owner decision #1** — `jurisdictional_values.evidence_tier` nullable vs NOT NULL + CHECK | OWNER | gates what 062 writes |
| **I-23** | **Owner decision #2** — retire `data/decisions/decision_register.yaml` | OWNER | — |
| **I-24** | **Owner decision #5** — durable third-write-path answer (bridge landed; `url_verification_runs` = 0 verified) | OWNER | — |
| **I-25** | **Owner decision #6** — jurisdiction scope, now **four** numbers: 46 skill / 24(+2) canonical / 27 enum / **48 in `lang_jur_map`, 22 outside the enum** | DG-NON | — |
| **I-26** | **Owner decision #7** — "cross-population" | OWNER | — |
| **I-27** | **Track B commits A–C, G, H** — doctrine batch + SHA rotation + ledger amendments + **the ratification-sweep apparatus** | OWNER | **H is the structural cure for T1** |
| **I-28** | **Owner decision #9** — PI v10.15 (fixes F3's dead gate; RV-003 ×5 and RV-012 ×2 live in v10_14) | OWNER (PI not API-writable) | conditional on #6 |
| **I-29** | **Owner decision #10** — required-check set | OWNER | **re-derive §6.7 first** (K3) |
| **I-30** | Track D Tier-2 (7 packages) + HOLD (5) + re-derive the Tier-1 row against shipped 059 | OWNER (#8 remainder) | — |
| **I-31** | The pre-reset verification record — **63 of 70** RV occurrences (RV-016 38, RV-012 16, RV-014 9) are one unasked question | OWNER + RESEARCH | — |
| **I-32** | `mission-PROVISIONAL.md` retire or stub (F5) | OWNER | — |
| **I-33** | `working/` disposition (C8) | OWNER | I-06 interim |
| **I-34** | F6's fourth vocabulary — decide the retiring entry | FREE (propose) | — |
| **I-35** | Q13 external-mining queue | RESEARCH | feeds the first genealogy cycle |
| **I-36** | Q4 directness promotion — **not re-derived by any pass since 2026-07-13** | re-derive first | — |
| **I-37** | Q15 — owner-external (Actions enforcement, scholarly connector, `lang_jur_map` jurisdictions) | OWNER | — |
| **I-38** | E9 pipeline stage-ids | OWNER (needs deployed `<audit_trail>`) | — |
| **I-39** | E11 product-posture doctrine edit | OWNER (SHA cascade) | run with I-27 commit A |
| **I-40** | `mode_s_trigger` column rename | D-SCHEMA (own Change-Order + caller sweep) | clears the RV-025/026 exemption debt |
| **I-41** | `validate_pydantic_schemas` 246-drift accept/reject policy (G9) | OWNER, untracked | keeps an advisory permanently red |
| **I-42** | Stale red-gate claims — `CLAUDE.md` §7 (K2), `tooling-register.md` §4 (K3) | FREE | K3 gates I-29 |
| **I-43** | `schema-reconciliation.md` currency `[OWNER-TO-DETERMINE]` | OWNER | — |
| **I-44** | §5 of DR-2026-07-25 | DG-NON | — |
| **I-45** | **The Universal/Population doctrine tension** (G6) | DG-NON | invisible five weeks |

---

## 5. Migration-number allocation — stated once, here, and nowhere else

Every prior allocation table is superseded by this one. Two live plans currently allocate the same
numbers; this reconciles them.

| Slot | Contents | Status |
|---|---|---|
| 054 | locator recovery | **consumed** |
| 055–057 | specification rename, baseline | **consumed** |
| 058 | `status_vocabulary_ratification` (D-0161) | **consumed** |
| 059 | `tier1_retirements` (D-0162) | **consumed** |
| 060 | `restore_superseded_status` (D-0163) | **consumed** |
| **061–066** | Track C's six, renumbered from 058–063 — **re-prototype owed (I-17)** | allocated |
| **067** | ratification trigger (writer plan Phase 0) | allocated |
| **068** | Tier-1 retirement **residue only, after re-derivation against shipped 059** | allocated |
| **069** | Tier-2 retirements | allocated |
| **070+** | anything that cannot join the 061–066 batch | reserve |

**I-19 (Q5-H2/H3), I-20 (Q6), I-21 (E10) and I-16's constraints join *inside* 061–066** where their
target tables coincide, rather than taking new numbers. `specifications` and `jurisdictional_values`
should each be opened **once**.

**No other live plan may allocate migration numbers.** The remediation workplan already carries a
staleness banner; **Wave 0 must add the same one-line pointer to `2026-08-15-instrument-status-backfill-
plan.md` §6**, which still reasons from the old allocation. G11's migration-054 note is discharged by
this table.

---

## 6. The plan

Six waves. Ordering is dependency-driven, not thematic.

### Wave 0 — Correct the record before anyone acts on it

**Gate: FREE.** One PR. No DB write, no migration, no doctrine SHA motion.

**Items, in execution order:**

1. **I-08 first.** Resolving `integrity-protocol` flips `attestation_evidence` green, which makes every
   subsequent acceptance test in this plan readable. Doing it last would mean every wave measures
   against a red it caused.
2. Then the document corrections: **I-01, I-02, I-03, I-04, I-05, I-06, I-42**, plus **I-09's registry
   note**, **I-11**, and register rows for **G4–G8, G10, G11**, and **G6 given a Q-number at last**.
3. Then **I-12** and **I-13** as tracker rows only — substance deferred.

**Acceptance, written before the work:**

- `python3 scripts/run_checks.py --changed-from origin/main` → 0 blocking, and the advisory set is
  exactly `{retired_vocabulary, research_dod, validate_reasoning}` — i.e. **`attestation_evidence`
  green again**. Verify by *name*, never by count. That is the direct lesson of E1.
- `--all` advisory count ≤ 7 with **no new names**.
- `PRAGMA user_version` = 60.
- `git diff --stat` touches nothing under `data/` or `scripts/migrations/`.

**Blast radius:** documents plus one registry list. The only behavioural change is one check returning
to green.

**Flag for the owner:** I-08 has two admissible forms — add `integrity-protocol` to the skill-registry
active block, or extend `EXTRA_RULE_IDS`. If the owner reads skill-registry's identifier-stability
section as governing the active-list block, this needs a DR on the Q23 precedent. **Propose both forms
in the PR body; do not pick unilaterally.**

### Wave 1 — Monotone tripwire edits

**Gate: FREE, CODEOWNERS review on `governance/`.**

Items: **I-07**; **I-13's** three repealed-formulation entries (`position within .* range`,
`resolves position`, `determines position within`) **carrying the N2 caveat in the entry note itself**;
**I-15**.

**Acceptance:**

- `retired_vocabulary_audit.py` total stays **exactly 70**, RV-025/026 stay at **1 each**. If either
  moves, revert — this is the critique's own pre-written test, re-validated by the audit.
- Each new repealed-formulation entry **fires on at least one known live line** before I-15 lands
  (`skills/item-specification-writer_SKILL.md:129` is the mutation test) and on **zero** lines outside
  the ledger after.
- The entry note states in terms that `references/project-standards.md` is globally exempt, so a future
  session cannot read green as "semantic debt closed".

### Wave 2 — The pass residue

**Gate: COLD, or an owner-scoped closure.**

Item **I-10**, now **materially narrower** than when the critique proposed it: surfaces A1, A3 and A4
are genuinely discharged. What remains is brief §3 claims 2, 5, 6, 7, 8 and the A2 design call.
Precondition: **Wave 0's I-01**, or the pass again reasons from the false premise.

Three admissible dispositions, unchanged: a fresh session; an authorized cold subagent; or a recorded
deviation accepting partial discharge. **This is an owner call.**

**Acceptance:** every §3 claim carries a recorded verdict *or* a recorded skip-with-reason, and the
brief's status line names exactly what was and was not audited. `DISCHARGED` unqualified is not an
acceptable end state given E6.

### Wave 3 — The Group-3 schema batch

**Gate: D-SCHEMA, owner decision #4. Propose; do not execute until ratified.**

Contents: 061–066 re-prototyped (**I-17**) + 067 trigger, with **I-19**, **I-20**, **I-21** and
**I-16's constraints** joining inside.

**Preconditions, every one before authoring a line of SQL:**

1. **I-17** — the six prototypes re-run at their new numbers. They were tested at 058–063 and the
   remediation banner states they have **not** been re-prototyped since renumbering.
2. **Owner decision #1 (I-22)** — it changes what 062 writes.
3. The **22 compound rows hand-classified by `jv_id`** per corrected I-04. Not by delimiter rule.
4. The **Band-B policy** decided (§4 of the instrument plan). Recommendation stands: execute Band A
   mechanically, leave Band B and C `unclassified`, open a gap row per Band-B family.
5. The **`ISO` scoping call** for acceptance test 6 — add to `lang_jur_map`, or scope the test to
   country codes.
6. Whether **GB→UK** rides in 062 or takes its own compensating migration.

**Acceptance:**

- The instrument plan §7's eight tests **as amended by I-04** — ISO named, D5 added.
- **Every new CHECK shown *firing*** on a scratch rebuild. A check never shown to fail proves nothing
  (`evidence-architecture.md` §10).
- `migrate_db.py --rebuild` reproduces the committed DB **shallow and `--deep`**.
- `test_db_integrity` ≥ 72/72.
- The `unclassified` count **reported, not minimised**. The migration succeeds by being true.

### Wave 4 — Owner tracks

**Gate: OWNER. Propose only.**

**I-27** is the priority within this wave, and specifically **commit H** — it is the structural cure for
T1, and every week it stays deferred, T1 produces more instances. Two execution-time requirements:
re-verify the "zero of 82 attestations" claim with `adherence_log_audit --check window` **at execution
time, not from the plan**; and land the D-0161 register entry as a **YAML append paired with a data
migration**, since writing only the YAML is what produced the live `delegation_rationale` divergence.

Then: **I-28** (#9, folds F3 and the live RV-003/RV-012 PI hits), **I-29** (#10 — **but re-derive the
§6.7 recommendation against today's green `test_db_integrity` first**, K3), **I-30**, **I-23**, **I-24**,
**I-14** (ride with Track B's licensed amend-in-place), **I-32**, **I-33**, **I-41**, **I-43**.

**DG-NON — propose, never decide:** **I-25** (#6, present all four numbers including the 48), **I-26**
(#7), **I-44**, and **I-45** (G6, five weeks invisible).

### Wave 5 — Research-shaped

**Gate: RESEARCH. These are not sweeps and must not be executed as sweeps.**

**I-31** — the pre-reset verification record. 63 of the 70 live retired-vocabulary occurrences are one
unasked question, and `evidence_sources` is 0 rows, so the prose is the **only** surviving record of
those gradings. Rewriting it mechanically would destroy the record and manufacture new gradings in one
move. This deserves its own owner decision.

**I-35** (Q13), **I-12's substance**, **I-36** (Q4, after re-derivation — untouched since 2026-07-13).

**One linkage to record in I-09's registry note so nobody "fixes" it wrongly:** corpus repopulation is
what naturally clears N3's two inverse-vacuity reds. Nobody should weaken those tests to get green.

---

## 7. Figures that must be re-derived at execution time

Never carried from this page. Every one was live 2026-08-17 and every one is the kind this repo
demonstrates rots:

the tripwire's 70/1/1 acceptance figures · the advisory-failure **set** (by name, not count) · "zero of
82 attestations" · the 22 `jv_id` list · all `site/` page counts · the 23/93 taxonomy counts ·
`user_version` · the doctrine SHA · `test_db_integrity`'s pass ratio · the `item_axis_links` count
(157 recorded, 158 live, cause unattributed).

## 8. What the audit could not verify

Stated rather than rounded up:

- **PRs #91–#97 at diff level.** Commit bodies were read and their load-bearing end-states verified;
  the fold-or-cut ledger, the resolution-plan revisions and the six-agent audit's internal claims were
  not re-derived.
- **Whether the 2026-08-15/16 "46/6" baselines included `test_directness_2_2` among their six.** No
  session enumerates the six by name. The reconstruction — their 6 = today's 7 minus
  `attestation_evidence` — is consistent and explains everything, but it is inference.
- **GitHub-side state** — branch protection's required-check set and live Actions results. The
  `merged_at` claim for PR #103 was verified from the local merge commit instead.
- **The instrument plan's Band-A/B domain assertions** — which standards are statutory in which
  jurisdiction, e.g. DIN 18040's Länder-by-Länder status. Outside a read-only session's reach, and
  exactly why Band B is owner-gated.
- **Historical counts** "101 → 70" and "33 → 2" — only the end states were re-derived.
- **Whether `run_checks` was executed before or after the attestation was authored** in E1. The
  committed claim is false at the committed tree either way; only the intent differs.

## 9. Contested — flagged rather than settled

1. Whether "in no register" fairly describes F3. The commit's "four" is defensible as {F3, F4, F5, F6};
   with F3 shown pre-tracked the true count is at most three. Both framings are off.
2. Whether P4 exceeded the brief. The audit's view — and mine on reflection — is that **P3 is squarely
   in scope**, because brief A3 asks in terms whether any *behavioural* rule keyed on the old phrasing,
   and `project-standards.md:202` is exactly that. P4 is a justified extension. **The attestation's
   counterclaim over-concedes and should be read with that correction.**
3. Whether the ladder session's sweep of three dated-but-live records was right. Its author left it
   explicitly arguable; it remains so.
4. Whether E1's mechanics matter. They do not for the record — the claim is false either way — but they
   bear on how I-08 is framed.
