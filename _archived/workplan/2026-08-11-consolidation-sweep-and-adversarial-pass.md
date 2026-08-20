# 2026-08-11 — Consolidation sweep, and the adversarial pass on it

**Status:** FINDINGS — nothing in this document has been executed. It proposes; it does not act.
No file was moved, no register edited, no migration emitted. The only change this session makes
to the repository is this document.
**Subject:** the whole repository at `1f15381`, read against the week's commits (81 since
2026-08-04) and against the live database.
**Method:** Part 1 is the sweep — read the repo as a system, not as a grep target. Part 2 turns
the adversarial protocol from `workplan/2026-08-11-remediation-and-pipeline-anatomy.md` §3 back
on Part 1's own findings, default verdict REFUTED, CONFIRMED only on personal reproduction.
**Doctrine SHA:** `0f2f525`. **Environment:** `pydantic==2.13.3`, `PyYAML`, `jsonschema` installed.

> **Read §0.2 before §1.** Four of this sweep's own findings were killed or materially changed by
> the adversarial pass, and one reversed its recommendation entirely. The corrections are in the
> body, not an appendix.

---

## Part 0 — What this found, in one page

### 0.1 The governing fact

Everything below descends from one event. **DR-2026-08-06 reset the evidence corpus** — 11,849
rows across 38 tables — and preserved the file surfaces "as reference." The decision was right
and its execution was clean. What was not done, and could not have been done in the same
commit, is the consequence: **the repository's prose still describes, cites, indexes, plans over
and asserts a corpus that no longer exists, and almost none of it is marked.**

The live database holds **0 evidence sources**. 39 of its 67 tables are empty. Against that:

| Surface | Volume | Marked as reference? |
|---|---|---|
| `references/bpc/` synthesis | 102 files, 12,730 lines | 70 of 102 carry a banner naming a **superseded** event; 16 per-slug files carry none |
| `references/connections/` | 28 files, 10,294 lines | no |
| `site/` (generated) | 124 files, 11,601 lines | no |
| `specs/`, `parts/` | 5,794 lines | no |
| `references/global-reference-registry.{md,json}` | 531 REF-IDs, dual-stored | no — and it declares *itself* authoritative |
| `working/` | 39 files, ~1.1 MB, wholly corpus-derived | no |
| `workplan/` planning over the reset corpus | 32 of 66 files, 9,879 lines | no |

**176 distinct `REF-NNNNN` identifiers are cited across the frozen surfaces. All 176 resolved
before the reset. None resolves now.** A further 1,233 citation instances sit in `references/`
files outside the reset's declared boundary.

### 0.2 The four things the adversarial pass changed

| # | The sweep proposed | Verdict | What replaced it |
|---|---|---|---|
| **X1** | "Retire the `governance/armature_*` series — 2,059 lines of self-declared *pre-decision, NOT decision-quality, Sonnet-drafted* material sitting in the doctrine directory, cited by no code." | **REVERSED** | `governance/functional-taxonomy.md` — CANONICAL — derives its two-layer architecture from `armature_v4` §§4.2–4.3 and cites it as authority thirteen times. It cannot be retired. The real finding is the opposite of pruning: **canonical doctrine rests on a document that disclaims decision-quality.** The fix is promotion or restatement, not removal (§1.5). |
| **X2** | "All 12 deprecated skills are still named in `references/skill-registry.md` as if live." | **REFUTED — my error** | The registry has a `## Deprecated skills` section listing each with a retirement reason. This is the repo doing it right. Only the inverse holds: 2 *active* skills are absent from the registry (§1.7). |
| **X3** | "`governance/tier-system.md`, `time-model.md` and `mission-and-epistemics.md` carry superseded/provisional status lines." | **REFUTED — my error** | My grep caught `**Supersedes:**` and read it as `SUPERSEDED`. `tier-system.md` is OPERATIVE, `mission-and-epistemics.md` is CANONICAL. Only `population-taxonomy.md` genuinely carries `Status: SUPERSEDED`, and it carries a loud banner (§1.5). |
| **X4** | "The attestation audit degrades silently when `jsonschema` is absent — a live vacuity." | **REFUTED** | `adherence_log_audit.py:214-216` appends an issue on `ImportError`, and `audit()` returns 1 if any issue exists. It fails loudly. CI installs `jsonschema` in both jobs that need it. The narrower `requirements.txt` defect survives (§1.8). |

Four corrections against roughly twenty claims. Two were my own pattern-matching — the failure
mode this sweep was explicitly asked to avoid — and both were caught by reading the file instead
of the match. That ratio is the argument for Part 2 existing at all.

---

## Part 1 — The sweep

Ordered by consequence, not by size. Every number below was produced by a command run on
2026-08-11 against `1f15381`; where a claim has no command behind it, it says so.

### 1.1 One concept — "frozen" — expressed in three registers that agree on one entry

The repository has three mechanisms for saying "this text is preserved, not current." They were
each built for a good reason, and they have **almost disjoint membership**:

| Register | Question it answers | Members |
|---|---|---|
| `.ignore` | hidden from agent search | `_archived/`, `workplan/_superseded/`, `audits/`, `references/audits/`, `sessions/**`, `references/search-log/`, `versions/` |
| `validate_cross_refs.REFERENCE_ONLY` | excluded from DB cross-ref resolution | `parts/`, `references/bpc/`, `references/bpc-reasoning/`, `references/connections/`, `references/connection-reasoning/`, `specs/`, `site/`, `_archived/` |
| `retired-vocabulary.yaml` `exempt_paths` | retired vocabulary licensed here | 69 entries, superset of `.ignore` |

**The two operative lists intersect in exactly one entry: `_archived/`.**

The consequence is not symmetric, and that asymmetry is the finding. `.ignore` states its own
rationale precisely: *"Every directory below holds FROZEN RECORDS: text that was true on its date
and is preserved unedited on purpose. A hit from one answers a current question wrongly."* That
rationale describes `references/bpc/` — 102 files of retracted synthesis carrying 133 distinct
dimensional values — at least as well as it describes anything it actually covers. And
`references/bpc/` is not covered.

**Demonstration, not assertion.** `rg -l "grab bar"` returns **122 files**. Classified:

- **39** in the frozen reference corpus (reset out of the DB five days ago)
- **7** dated records, **2** superseded governance docs
- **74** in neither register — including `references/global-reference-registry.md`,
  `references/fdr/`, `references/systematic-reviews/`, `references/cost-data/`,
  `references/claim-reference-join.{md,json}`, `references/tier1-verified-sources.json`,
  `references/conflict-matrices/`, `references/website/data/*.json`, and `working/`

The live database returns **zero rows** for the same question. A session that greps for a
grab-bar figure today gets 122 files and no signal about which, if any, is current. This is
CLAUDE.md §9 guardrail 1 — the stale anchor that caused a real error — reproduced at scale.

**Proposal (D-OP, owner-gated).** Not a fourth register. One declaration —
`governance/frozen-surfaces.yaml` — carrying every frozen path once, with its date, its
governing decision, and per-path flags for the three questions above. `.ignore` and
`REFERENCE_ONLY` become generated from it. `REFERENCE_ONLY` in particular should not live as a
tuple inside one validator: it is the operative boundary of the most recent governing decision
in the repository, and it is currently a local constant.

### 1.2 A rival source of truth, dual-stored, backed by nothing

`references/global-reference-registry.md` line 6: *"Single source of truth for all references
cited anywhere in the guidebook."* Line 601: *"**Authority:** This registry is the single source
of truth. If a BPC Key sources table and this registry conflict, the registry governs."*

This directly contradicts the layer model (CLAUDE.md §2, `architecture/project-architecture-guidebook-v2.3.md`):
the DB is canonical and every other store is the thing to reconcile. Measured:

| | |
|---|---|
| REF-IDs in the registry | **531** |
| identical set in `references/global-reference-registry.json` | **531** — same IDs, byte-different store |
| of the 531, present in the **live** DB | **0** |
| of the 531, present in the **pre-reset** DB | 496 |
| **cited by the registry but absent from the DB even before the reset** | **35** |
| in the pre-reset DB but absent from the registry | **367** |

The last two rows matter independently of the reset. The registry claiming to govern over the DB
was already wrong in both directions in July: 35 identifiers it asserts never existed as sources,
and it was missing 43% of the corpus it claims to be complete for. It was generated on 2026-04-19
and never reconciled.

It is read by two scripts, both legacy one-shot importers (`scripts/convert/convert_sources.py`,
`scripts/db/migrate_all.py`), and cited in prose by `governance/conceptual-model.md` and
`decisions/DR-2026-07-12-evidence-architecture-unification.md`.

**Proposal.** Retire both files to `_archived/references/`, leaving a redirect stub naming the DB
and the archive branch (CLAUDE.md §9 guardrail 2). The authority sentences must go regardless of
where the file lives — a live file asserting supremacy over the canonical store is a doctrinal
defect, not a housekeeping one. Owner-gated: retirement (guardrail 4).

### 1.3 The retraction banners name a superseded event, and 16 files have none

70 of 102 `references/bpc/` files carry:

> `**SYNTHESIS VALIDITY:** PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION`
> `(See PI rule #10; cohort defined by DR-2026-05-23 …Claims requiring Phase E.2g reverification.)`

That banner was correct on 2026-05-23. It is now **understated in a specific and misleading
direction**: it says *retracted pending reverification*, which reads as recoverable by a
verification pass. DR-2026-08-06 says the corpus is reference and the project proceeds as though
no research was performed. A reader following the banner would go looking for Phase E.2g.

Of the 32 without a banner, 16 are `bpc/` root files (the frozen flat aggregates, `_template`,
`index`) and are accounted for. **The other 16 are per-slug synthesis files carrying no validity
marking at all**, including:

- `seating-and-rest/energy-conservation-rest-points-seating.md` — 249 lines, 13 dimensional
  values. This is the slug named by `sessions/LATEST-RESEARCH`, the subject of a *blocking* gate.
- `frameworks-and-methodology/residential-accessible-home-case-studies.md` — 477 lines
- `frameworks-and-methodology/manoeuvring-footprint-vs-turning-radius-methodology.md` — 175
  lines, `Status: OPERATIVE`, "cited by dimension-specifying BPCs across the corpus"

That last one also records an unfinished repair in its own text: *"**Still open:** the closure
text of GAP-272 carries the same uncorrected 'Vergara 2023' attribution and needs the identical
repair."* `gaps` is now empty, so the repair target no longer exists — the note is now
unactionable and should be resolved to a statement of fact rather than left as an open task.

**Proposal.** One banner, one wording, one governing DR, on all 85 per-slug BPC files, generated
and checked rather than hand-applied — the check being an extension of the existing
`pre_rehab_banner_audit.py` (currently quarantined, RED on 6 slugs) rather than a new script
(guardrail 3).

### 1.4 `workplan/` — 66 documents, 28,347 lines, no index, 6 aware of the reset

| | |
|---|---|
| active workplan documents | **66** (plus 20 `_superseded/`, 16 `deprecated/`) |
| total lines | **28,347** |
| documents that mention the clean-room reset | **6** |
| documents naming reset corpus tables or Phases B/E and never mentioning the reset | **32** (9,879 lines) |
| a date-sorted index | **none** — `ls workplan/ \| grep -i index` returns nothing |

The 32 figure is a keyword measurement and I want its limits stated: some of those documents are
*methodology* (`research-protocol-adversarial.md`, `best-practices-assessment-system.md`) which an
empty corpus does not invalidate. The measurement is exactly what it says — they name the reset
corpus and do not name the reset — not a claim that all 32 are dead.

The prior remediation plan already adjudicated the obvious move: its **K3** killed the 57-file
rename as FATAL (278 files cite those filenames, including 9 immutable migrations and 8
forward-only attestations) and replaced it with **D9 — generate a date-sorted index instead.**
**D9 has not been built.** That remains the correct, cheap, non-destructive action, and it is the
one this sweep endorses without qualification.

Two things D9 should carry that the original proposal did not: a **reset-relative status column**
(pre-reset / reset-aware / reset-neutral), and generation from the files rather than hand
maintenance, registered in the check registry so it cannot rot — the pattern
`context_map_fresh` already established on 2026-08-11.

### 1.5 Doctrine resting on documents that disclaim being doctrine

This is X1 after the adversarial pass reversed it.

`governance/armature_v4.md` — 486 lines — states: *"**Status:** PRE-DECISION DRAFT — captured
intent for Stage A formalization. **NOT decision-quality.** Sonnet-drafted; flagged for Opus
synthesis at A7 / A12."* The full v1→v4 lineage sits in `governance/` (5 files, 2,059 lines,
168 KB), none of it referenced by any script, workflow or registry.

The pruning reading is wrong. `governance/functional-taxonomy.md` — live, canonical, the
governing document for the "work from axes, not umbrellas" rule (CLAUDE.md §10) — cites the
armature as authority **thirteen times**, including for its foundational two-layer architecture
(§§4.2–4.3) and for open ratification items R6 and R7. Migration `030_two_layer_functional_taxonomy.sql`
carries `armature §5` reasoning in eight committed rows.

So the finding is a provenance defect, not a volume one: **a canonical taxonomy derives its
architecture from a Sonnet-drafted document that says it is not decision-quality, and the
promotion that was supposed to happen at A7/A12 never did.** The synthesis-routing floor (PI rule
#2, DR-2026-06-10) exists precisely to prevent below-floor authorship becoming doctrine, and this
is that, by inheritance rather than by direct write.

Adjacent, and smaller: `governance/population-taxonomy.md` carries `Status: SUPERSEDED (population
code set)` with a clear banner and 32 inbound references. The banner works; the file is correctly
retained for its structural detail. No action beyond eventual rewrite.

**Proposal (D-DOCT, DG-NON — owner decides).** Either restate the load-bearing armature sections
inside `functional-taxonomy.md` at doctrine quality and retire the lineage to `_archived/`, or
promote `armature_v4` explicitly with an Opus-authored ratification note. What should not persist
is the current state, where the status line and the citations contradict each other.

### 1.6 The quarantine list is four different dispositions under one word

16 checks are quarantined, holding **3,590 lines** of maintained-but-never-run code. The entries
are unusually well written — each carries a reason, several carry corrections of earlier wrong
reasons. The defect is that one label covers four incompatible situations, so "quarantined" tells
a reader nothing about what to do:

| Disposition | Count | Members | What it actually needs |
|---|---|---|---|
| **Not a gate by nature** | 4 | `table_connectivity`, `jurisdictional_divergence`, `contamination_sampler`, `check_phase_a_complete` | a report venue, never promotion |
| **Green but vacuous** | 5 | `validate_conflicts`, `validate_item`, `validate_db`, `validate_audit_runs`, `validate_temporal` | a populated subject, or deletion |
| **Red with real findings** | 6 | `validate_conflict`, `schema_reference_drift_audit`, `adjudication_integrity`, `code_currency_audit`, `pre_rehab_banner_audit`, `validate_commits` | owner adjudication of a backlog |
| **Wrong venue** | 1 | `full_db_metadata_verification` (~298s, network-bound) | move to the scheduled workflows |

`validate_temporal` is the sharpest case: it reads `data/temporal/`, **a directory that does not
exist**, and was `blocking` while examining zero records until 2026-08-04. Its subject was never
built. That is not a quarantine; it is a deletion or a project.

**Proposal.** Add one field — `disposition:` — to the quarantine schema, with those four values,
and require `exit_condition:` on the two dispositions that can ever be promoted. This is a
registry edit, not a new mechanism (guardrail 3), and it makes the list answerable: today a reader
must parse sixteen paragraphs of prose to learn that only six of them describe anything a person
could act on.

### 1.7 Smaller, verified, cheap

**a. Two live validator generations share a namespace.** `validate_item.py` (239L) and
`validate_conflict.py` (200L) are the pre-DB YAML/markdown generation, both quarantined.
`validate_items.py` (128L) and `validate_conflicts.py` (86L) are the live DB generation, both
registered. The names differ by one character. A session reaching for the live check has a
coin-flip chance of running the retired one and reading its output as current. Rename the retired
pair with a `legacy_` prefix, or retire them.

**b. Three database initialisers.** `scripts/init_db.py` (106L, unregistered), `scripts/db/init_db.py`
(432L), `scripts/migrate/init_database.py` (417L). CLAUDE.md §10 already warns against the first.
`scripts/db/**` targets `data/db/guidebook.db` — **a path that does not exist on disk** — and
`scripts/db/` holds 3 files totalling 99 KB reachable from ten prose documents.

**c. `references/methodology/` holds an un-finished split.** `economics-research-methodology-v1.9-archived.md`
(26,651 shingles) contains `perceptual-value-crossover.md` at 98% containment,
`economics-methodology-core.md` at 91%, `throughline-cost-of-inaction.md` at 92% and
`throughline-market-value.md` at 83%. The monolith was split into four and then kept, in the live
directory, with `-archived` in its filename but not in `_archived/`.

**d. Two active skills are absent from `references/skill-registry.md`:** `integrity-protocol`,
`supersession-audit`. The registry is the identifier source that attestations bind to; the repo's
own stated principle is that an unlisted item re-opens the hole on principle.

**e. `references/search-log/` and `references/bpc/` each carry 14 flat uppercase aggregates**
(`MOB.md`, `DEAF.md`, …) whose first line reads *"FROZEN — Do not read or write… Any skill reading
this file is in error."* `validate_bpc.py:80-83` correctly skips them. They are self-declaring and
code-respected — but they sit in the live corpus directory rather than `_archived/`, which is what
guardrail 2 prescribes. The `search-log` copies are at least covered by `.ignore`; the `bpc` copies
are fully greppable, which is how `references/bpc/MOB.md` appeared in the 122-file result in §1.1.

**f. `working/` — 39 files, ~1.1 MB — is entirely corpus-derived and entirely unmarked.** Every
file under `working/evidence-migration/` and `working/pilot/` cites REF-IDs that resolve only in
the archived pre-reset database. It is in no register.

### 1.8 Two live defects the week's commits documented and did not fix

Both were confirmed by the 2026-08-11 adversarial review (its F6, F10). Both are still present at
`1f15381`, and `check-registry.yaml` was modified 14 times in the last seven days.

**a. `governance/check-registry.yaml:174` is malformed YAML.**

```yaml
governance:  {deps: [pydantic], description: Decision protocol, doctrine recheck, adversarial-use.}
```

Unquoted commas inside a flow mapping. It parses to
`{'deps': ['pydantic'], 'description': 'Decision protocol', 'doctrine recheck': None, 'adversarial-use.': None}`
— two junk keys and a description truncated to a third of its text. `run_checks.py` reads neither
`description` nor battery-level `deps`, so present impact is cosmetic; the hazard is that a
registry that parses successfully into the wrong shape is the exact thing `--selftest` exists to
catch and does not. Quoting the string is a one-character-class fix.

**b. `requirements.txt` is both un-installable here and factually wrong.** Its header states:
*"All scripts under `scripts/` and the `schemas/` package depend only on these two."* They do not
— `scripts/audit/adherence_log_audit.py` needs `jsonschema`, which `ci.yml` works around by
hand-listing it in the `attestation` and `research` jobs. Separately, `pip install -r requirements.txt`
fails in this container (`Cannot uninstall PyYAML 6.0.1, RECORD file not found` — Debian-managed
PyYAML); `--ignore-installed PyYAML` succeeds. Two independent environments have now hit this.

### 1.9 Where CLAUDE.md has drifted

CLAUDE.md is the most-read file in the repository and states plainly that it is a derived map. It
was modified 5 times this week. Checked mechanically:

| Claim | Verdict |
|---|---|
| §7 "Ten of the twelve [tests] are registered… two unregistered are `test_adjudication_integrity` and `test_generate_parts_4_2`" | **CONFIRMED**, exactly |
| §7 "four [workflows], since the 2026-08-01 consolidation" | **CONFIRMED** — `ci.yml`, `regenerate-derived.yml`, `resolve-dois.yml`, `verify-urls.yml` |
| §4 exempt tables `evidence_source_authors`, `pipeline_runs` | consistent with DR-2026-05-28; no contradicting code found |
| §10 "**`session_pointer_resolvable` (blocking)** now fails if either pointer dangles… and reports drift when `LATEST-RESEARCH` falls behind the DB" | **WRONG — no such check exists**, in the registry or in code |

The §10 error deserves its mechanism stated, because the underlying work was done well and only
the documentation is wrong. Commit `4fc6304` — *"delete the watcher, fix the dispatcher it was
watching"* — deleted `scripts/audit/session_pointer_audit.py` and instead fixed `run_checks.py:217-229`
so that **a blocking check with no subject FAILS rather than SKIPs**. That is the better fix and it
is live. But two things follow. The protection is real under a different name and mechanism, so a
session searching for `session_pointer_resolvable` finds nothing and may conclude, wrongly, that
nothing guards it. And the *second* capability CLAUDE.md attributes to it — reporting drift when
`LATEST-RESEARCH` falls behind the DB — lived in the deleted watcher and **has no replacement**.
Post-reset it would report nothing anyway (`evidence_sources` is empty), which is exactly how a
dropped capability stays invisible until content resumes.

`sessions/LATEST-RESEARCH` currently names a 2026-07-26 session — sixteen days behind `LATEST`.

---

## Part 2 — The adversarial pass

Protocol: the audited document's own (§3 of `2026-08-11-remediation-and-pipeline-anatomy.md`).
Lens-separated. Default verdict **REFUTED**. **CONFIRMED** only where I re-derived the claim
myself, from the file or the database, on 2026-08-11.

### 2.1 Accuracy lens — every load-bearing number, re-derived

| # | Claim | Verdict | Command / evidence |
|---|---|---|---|
| A1 | Live DB: `user_version` 53, 67 tables, 18 views, 39 tables empty, 0 evidence sources | **CONFIRMED** | `PRAGMA user_version`; `COUNT(*)` per table over `sqlite_master` |
| A2 | 176 REF-IDs cited on frozen surfaces; 0 in live DB; **176 of 176** in the pre-reset DB | **CONFIRMED, both directions** | regex over `references/bpc`, `bpc-reasoning`, `site`, `specs`, `parts` ∩ both databases. The reverse test matters: it proves the citations were *valid and were reset out from under*, not that the prose was ever fabricated |
| A3 | `global-reference-registry`: 531 IDs, `.md` and `.json` sets **identical**, 0 live, 496 pre-reset, 35 never in the DB, 367 DB sources missing from it | **CONFIRMED** | set arithmetic against both databases |
| A4 | `.ignore` ∩ `REFERENCE_ONLY` = `{_archived/}` | **CONFIRMED** | parsed both, intersected |
| A5 | `rg -l "grab bar"` → 122 files; 39 frozen-reference, 74 in no register | **CONFIRMED — after a false start** | see §2.3 M1 |
| A6 | 70 of 102 BPC files banner DR-2026-05-23; 16 per-slug files unbannered | **CONFIRMED** | banner scan, root vs nested separated |
| A7 | 66 active workplans, 28,347 lines, no index | **CONFIRMED** | `ls`, `cat \| wc -l`, index search |
| A8 | 16 quarantined checks, 3,590 lines | **CONFIRMED** | registry parse + `wc -l` per resolved path |
| A9 | `check-registry.yaml:174` parses to two junk keys | **CONFIRMED, precisely** | `yaml.safe_load` output reproduced verbatim |
| A10 | `session_pointer_resolvable` exists nowhere | **CONFIRMED** | zero hits across `governance/`, `scripts/`, `.github/` |
| A11 | `run_checks.py --all` → PASS, 55 green, 10 advisory, 0 blocking | **CONFIRMED with a caveat** | reproduced twice. The 2026-08-11 review recorded "56 green, 9 advisory". One check moved between buckets in five days; **neither number should be written down anywhere**, which is the point CLAUDE.md makes about volatile facts and which this table is now demonstrating against itself |
| A12 | `data/db/guidebook.db` does not exist | **CONFIRMED** | `ls data/db/` → No such directory. 20 files still name the path |

### 2.2 Method lens — is the sweep's method sound where it claims to be?

**M1 — my own measurement contradicted itself, and I nearly reported the wrong number. CORRECTED.**
The first classification of the "grab bar" grep, run through `subprocess.run(['rg', ...])` inside
a heredoc, returned **0 files**. A direct shell `rg` returned **122**. I did not report either
until the discrepancy was resolved: the shell result reproduces at 122 across three invocations
and is the one used throughout. The subprocess path returned empty stdout without raising, and I
did not check its return code — a silent-empty-result bug in my own instrument, which is
precisely the class of defect §1.6 and the repo's own history are about. **A check reporting zero
may have examined zero, and that applies to the auditor's tooling too.**

**M2 — the "unmarked frozen surface" finding does not depend on the grep. CONFIRMED.**
Set arithmetic against two databases (A2, A3) establishes it independently of any search
behaviour. The grep demonstrates *reader impact*; the set arithmetic establishes *fact*. Had the
grep been unavailable the finding would stand unchanged.

**M3 — "32 workplans plan over the reset corpus" is a keyword heuristic and is stated as one.
OVERSTATED if read as 32 dead documents.** It measures co-occurrence of reset-corpus vocabulary
with absence of reset vocabulary. Methodology documents in that set survive an empty corpus fine.
§1.4 states this limit inline rather than in a footnote, and the recommendation (build the index,
add a status column) does not depend on the count being exact — which is the property a
heuristic-backed recommendation should have.

**M4 — the near-duplicate detection surfaced mostly template boilerplate, and I discarded it.
CONFIRMED as a limitation.** Shingle containment over 932 markdown files produced 778 pairs above
0.35. Inspection showed the great majority are `references/search-log/` files sharing a YAML
template — ~500 shared shingles between structurally identical, factually distinct logs. Only
three families survived reading: the flat/nested duplication (§1.7e), the economics methodology
split (§1.7c), and the `global-reference-registry` `.md`/`.json` pair (§1.2). **A high similarity
score is a candidate, not a finding**, and 775 of 778 candidates were not findings.

**M5 — I ran the checks in a broken environment first and would have reported five false
blocking failures. CORRECTED before reporting.** The first `run_checks.py --all` reported 5
blocking failures — `validate_schema`, `validate_evidence_state`, `audit_adversarial_use`,
`decision_capture`, `doctrine_recheck` — every one a `ModuleNotFoundError: pydantic`, because
`pip install -r requirements.txt` had failed (§1.8b) and I had not verified it succeeded. With
dependencies installed, all five pass. **A red result whose cause is the harness is not a
finding**, and the fact that the documented install command is what produced it is why §1.8b is
in the report at all.

### 2.3 Logic lens — do the recommendations follow from the findings?

**L1 — "consolidate the three frozen registers" does not follow from "they differ." REFINED.**
Three registers answering three different questions may legitimately have different membership;
difference alone proves nothing. The finding is narrower and does follow: `.ignore` states a
rationale — *a hit from a frozen record answers a current question wrongly* — and that rationale
applies to `references/bpc/` by its own terms, while `references/bpc/` is excluded. The defect is
**a stated rule not applied to a case it names**, not mere divergence. The single-declaration
proposal is a means; the necessary part is that the reference corpus be registered somewhere a
reader will look.

**L2 — retiring the global registry does not follow from it being stale. CONFIRMED anyway, on a
different ground.** Staleness alone would argue for regeneration. The authority sentence at line
601 is what forces the issue: it instructs a reader to prefer a markdown file over the canonical
database, contradicting the layer model. That is true independently of the reset, and would have
been true in July when the registry was already wrong in both directions.

**L3 — the banner fix must not become a vacuous green. CARRIED FORWARD from K2.** The prior
plan's K2 killed a proposal that would have turned a red `validate_reasoning` into a green one by
moving its only subject out of scope. The §1.3 proposal is exposed to the same failure: a banner
check that passes because it finds no files, or because banners are present but wrong, is worse
than no check. Any implementation must declare a subject count and fail when the subject is empty
— the `min_items` / `EXAMINED: <n>` convention that already exists.

**L4 — §1.5 reverses its own recommendation, and the reversal is the finding. CONFIRMED.**
The sweep's first pass proposed retiring the armature series on volume and status grounds without
checking inbound citations. Reading `functional-taxonomy.md` inverted it. Recorded here rather
than silently corrected, because the near-miss is instructive: **status lines and citation graphs
are independent, and a document can be simultaneously self-disclaimed and load-bearing.** Any
future retirement proposal in this repository should require the citation graph before the status
line — which is what `<migration_and_growth>` already says about renames and removals, applied to
retirement.

**L5 — the nothing-was-executed posture is correct here. CONFIRMED.** Every substantive proposal
above lands on an owner-gated class: retirements (§1.2, §1.7c, §1.7e), doctrine promotion (§1.5),
and `.ignore` scope (§1.1) are guardrail-4 and DG-NON territory. The three that are *not*
owner-gated and could be executed by a session today are the YAML quote (§1.8a), the
`requirements.txt` correction (§1.8b), the CLAUDE.md §10 correction (§1.9), and the D9 index
(§1.4). Those four are the recommended next session; they are also the four with no reversibility
cost.

### 2.4 Impact lens — what does fixing each actually buy?

| Finding | If fixed | If not |
|---|---|---|
| §1.1 frozen registers | a grep answers with one current source instead of 122 mixed ones | the failure mode that already caused one recorded error stays live, and grows as content resumes |
| §1.2 rival registry | the layer model holds without exception | a live file instructs readers to prefer it over the canonical DB |
| §1.3 banners | 85 files say the same true thing | 16 substantive files assert unbanner-ed values; 70 point at a superseded remedy |
| §1.4 workplan index | one command answers "what is the current plan" | 28,347 lines, 66 candidates, `sessions/handoff-next-session.md` known-stale |
| §1.5 armature | canonical taxonomy has doctrine-quality provenance | the synthesis floor is satisfied in letter and breached by inheritance |
| §1.6 quarantine | 6 actionable items separate from 10 that are not | 3,590 lines of code with a label that does not distinguish "broken" from "not a gate" |
| §1.8a YAML | the registry parses to its intended shape | a successfully-parsing wrong shape that `--selftest` does not catch |
| §1.8b requirements | the documented install command works | the documented command produces five false blocking failures — which it did to me |
| §1.9 CLAUDE.md | the map matches the territory on its own most-cited section | the most-read file names a blocking gate that does not exist |

**The honest summary of impact.** None of this is content, and none of it makes the guidebook more
true about the built environment. What it buys is that the *next* content session gets one answer
per question instead of several, which is the condition DR-2026-08-06 reset the corpus to create
and which the file surfaces have not yet been brought into line with. The reset removed the wrong
answers from the database. It did not remove them from the prose, and the prose is what a session
reads first.

---

## Part 3 — Recommended sequence

Nothing here is executed. Ordered so that each step is reversible and none blocks on an owner
decision that a later step would invalidate.

**Executable now, no owner gate, no reversibility cost:**

1. Quote the `governance` battery description — `check-registry.yaml:174` (§1.8a).
2. Add `jsonschema` to `requirements.txt` and correct its header claim (§1.8b).
3. Correct CLAUDE.md §10: name the dispatcher-level guarantee at `run_checks.py:217-229`, delete
   `session_pointer_resolvable`, and record the dropped drift-reporting capability as a known gap
   rather than a live feature (§1.9).
4. Build D9 — the generated, date-sorted, reset-relative `workplan/INDEX.md`, registered for
   freshness like `context_map_fresh` (§1.4).

**Proposals requiring owner sign-off, in dependency order:**

5. `governance/frozen-surfaces.yaml` as the single declaration; `.ignore` and `REFERENCE_ONLY`
   generated from it (§1.1). Everything else depends on this existing.
6. Re-banner the 85 per-slug BPC files against DR-2026-08-06, with a subject-count floor (§1.3, L3).
7. Retire `global-reference-registry.{md,json}` to `_archived/references/` with a redirect stub;
   remove the authority sentences regardless of outcome (§1.2).
8. Adjudicate the armature: restate-and-retire, or promote (§1.5). D-DOCT / DG-NON.
9. Add `disposition:` to the quarantine schema and classify the 16 (§1.6).
10. The small set: `legacy_` prefix on the two retired validators, the `references/methodology/`
    split completion, the two missing skill-registry entries, `working/` registration (§1.7).

**Not recommended:** any bulk rename, any deletion, and any promotion of a check to blocking in
the same window as branch protection — all three were adjudicated and refused in prior work
(K3, K4, `tooling-register.md` §6), and nothing in this sweep changes those rulings.

---

*Every count in this document was derived on 2026-08-11 against `1f15381` by the command named
beside it. Counts of the live database, the check suite, and CI status are volatile by
construction — §2.1 A11 is a worked example of one going stale inside five days. Re-derive before
relying on any of them.*
