# Repair plan — adversarial critique of session 2026-09-01, batch 04

**Critique.** Two Fable 5 read-only passes, run blind and partitioned: critic A on data and code,
critic B on claims and process. 10 + 32 findings; both also recorded what they CLEARED, which is
where most of the value is — see §5.

**Verification.** I re-derived every finding below myself before accepting it. Findings I could not
reproduce are not in this plan. Two of critic B's own numbers were wrong and are corrected in §5.

**The headline.** The migration is mechanically sound — FK-clean, reproducible, correct ledger,
0 blocking gate failures, and every table count in every commit message is exact. The damage is
elsewhere: the retraction created a **ref_id collision hazard**, it **rewrote a research-stage
record** it claimed not to touch, and the session **misread the instrument it invoked** — then
described its own breach of that instrument as a discovery.

---

## 1. What I got wrong, stated plainly

### 1.1 I breached DR-2026-08-19 §1.4 and called it the instrument's failure (B-09, B-10)

I wrote, in a commit message and in the PR body:

> *"DR-2026-08-19 §1.4 wrote a quarantine for exactly this and never ran it — measured today, all 93
> items were status=active and slugs.status=PROVISIONAL held zero rows. A rhetorical demotion left
> the containers standing."*

**§1.4 does not say that.** It is six CONDUCT rules for future sessions. It never prescribes a
change to `items.status`. Its rule 3 applies `PROVISIONAL` to *item-derived slugs* and records
*"zero rows currently use it"* as its own stated BASELINE. Zero PROVISIONAL rows is therefore
consistent with the protocol having been OBEYED — no item-derived slug was ever created.

And two of its rules bind the session that invokes it:

> **Rule 1.** *"A slug is authored from the ICF/access-need frame first; the item list may then be
> consulted to check coverage — never to supply one."*
> **Rule 2.** *"No value crosses. No numeric, dimension, threshold, range, or prescriptive clause
> from an item name … may appear in a `search_executions` row, a `search_candidates` row, an
> admitted source's fields, or a determination."*

`FRAME.md` was derived from `items`. Item values were carried into both agonist briefs and reached
their queries — agonist-1 #8 `"…22 newtons…"` (I-01's "≤22 N"), agonist-2 #6 `"pendulum test value
slip resistance…"` (E-07's "PTV ≥36"). **The rule was live and I broke it.** The mitigating fact is
real but smaller than the breach: §12.1 step 2 of the SAME instrument tells a session to run
`db.py items --category A`, so the instrument is self-contradictory. That is a defect to record,
not a defence.

**Repair.** Correct the record (§3.1). The instrument's internal contradiction — §1.4 rule 1 vs
§12.1 step 2 — goes to the owner as its own question (§4.3).

### 1.2 "147 preserved DOI leads" is false (A-02, B-25)
147 *entries* in `citation_mining.connections_produced`; **138 distinct**; **134 not already held
in `source_locators`**. Stated in a commit message, the migration header (immutable) and the PR body.
This is CLAUDE.md §2(b) — prose contradicting the database — in exactly the class this repository
names as one of its three real failure modes.

### 1.3 `RULINGS.md` says the migration was never applied; it was (B-06)
`RULINGS.md:102` still reads *"It cannot be applied until that command is approved. No workaround
was attempted."* `data_migrations` holds it applied at `2026-09-01T20:56:54`. True for under a
minute, never updated, and committed. Same failure mode as 1.2.

### 1.4 I introduced a bug while fixing one (A-06)
`scripts/validate_schema.py` — my empty-registry `return 0` fires BEFORE `run_cross_checks()`, so
`validate_schema_cross_check` is now **structurally unreachable**. Its comment also asserts that the
registry's `min_items` guard escalates the empty scope; my own next commit replaced `min_items`
with `no_floor`, making that inert. The comment is false about the state I left.

### 1.5 "The item layer is gone" is materially incomplete (B-11)
The ROW layer is gone. The rendered determinations are not: `index.html` (E-08 ×2, "1200" ×1),
`parts/v10/part04.md`, `versions/current/…v9-0…md` — none touched by this PR. DR-2026-08-19 §1.2
warned of precisely this: *"Archiving the `items` rows quarantines none of this. A researcher who
greps the repository for their slug will meet the old answer before they have logged their first
search."*

### 1.6 Smaller false or loose claims
| # | Claim | Truth |
|---|---|---|
| B-01 | "one [DOI] under five" ref_ids | **two** are under five |
| B-03 | the 08-31 command log "the prior session left untracked" | every line carries THIS session's id; it was misfiled by this session |
| B-04 | PR: "41 green … 9 advisory" | **42 green, 15 nothing-in-scope, 8 advisory** |
| B-05 | REF-00037 carries "a third, different DOI" | a **second** |
| B-07 | `empty-by-decision` "used by three checks" | **eleven** on main, 13 at HEAD |
| B-24 | "applying five owner rulings" | **four**; R-05 is recorded, not executed |
| B-26 | "27 author rows in byline order" | NFBUK has no byline; `Bates\|David M` is credited **Editor** in the payload |
| B-27 | "38,720 ED visits" | *"an **estimated** 38,720 ED weighted visits"* (NEISS national estimate) |
| B-13/B-14 | "eight admissions", "~30 logged queries" | 8 `evidence_sources` + 27 author rows + 8 slug links; **zero `search_executions`, zero `search_admissions`**. The queries exist in markdown only |

---

## 2. Data repair — ONE compensating migration

Append-only: the applied migration is immutable, so every correction is a new forward migration
(CLAUDE.md rule 3). Order within the file matters; FK-parent rows first.

### 2.1 A-01 (P1) — restore the ref_id high-water mark **before any future `add-source`**
`dbcore.next_ref_id()` returns **`REF-00965`**. Deleting `evidence_sources` dropped the union
high-water from 970 to 964, because REF-00965–970 had no `source_locators` rows. Meanwhile 26
surviving research rows still name them: `search_candidates.notes` ×12, `.why_not_admitted` ×10,
`search_executions.findings_note` ×3, `gaps.GAP-B02-001` ×1 — plus two retrieval-log manifests,
which are the §2(c) verification artefact.

**Fix.** INSERT REF-00965…REF-00970 into `source_locators` with their DOI, title, year,
`status='REFERENCE-ONLY'`, `recovered_from='retracted-2026-09-01-owner-ruling'`. This restores the
mark to 970, keeps the six identities as research-stage LEADS (which R-04 explicitly permits),
and keeps R9's cross-file pre-check functional. **Do not touch the allocator** — it is correct;
its inputs were removed.

**This is the one item that must land before the branch is used for more research.**

### 2.2 A-02 — make `citation_mining` identify what it mined
All ten rows now have `global_ref_id` NULL, `doi` NULL, and a `local_ref_id` that resolved through
the emptied `source_slug_links`. They are records of mining against nothing, and `db.py log_mining`
will now **crash** (NOT NULL on a lookup that returns NULL) rather than duplicate.

**Fix.** `UPDATE citation_mining SET doi = <anchor DOI>` per `(slug, local_ref_id)`, from the six
identities recovered in 2.1. The `doi` column is now the ONLY home for that fact, so this is not a
rule-5 copy. Correct the "147" figure in the new migration's header.

### 2.3 A-03 — restore the research record, and retire the invariant that forced the lie
`UPDATE search_executions SET results_admitted = 0` rewrote 7 rows (Σ was 10). `v_coverage_*` now
report that 25 searches on `room-acoustic-performance` yielded nothing. That is false: the searches
did admit; the retraction happened downstream.

**Coupled decision — these cannot be separated.** Restoring the values breaks **H05**
(`results_admitted` == `COUNT(search_admissions)`), which would go red at 10 ≠ 0. `test_db_integrity`
itself calls `results_admitted` *"a third store of the same fact"*, and CLAUDE.md rule 5 says
*"A parity check is not a fix — it makes a dual home survivable, therefore permanent."*

**Fix.** Restore the 7 values AND retire H05 in the same change, writer-retiring `results_admitted`
the way `admitted_ref_ids` was retired on 2026-08-24. `v_coverage_*` then compute current yield from
`search_admissions` (honestly 0) while the execution row keeps its history.

### 2.4 A-04 — a candidate cannot be ADMITTED to nothing
`search_candidates` #1 is `disposition='ADMITTED'`, notes *"Admitted as REF-00968"* — which no longer
exists. R15 passes only because its predicate is `notes LIKE '%RESOLVED%'`.

**Fix.** Re-disposition to `PENDING-VERIFICATION` with a note recording the retraction. **Do not**
add a new check for `ADMITTED ⇒ EXISTS evidence_sources` in this pass — CLAUDE.md §1 puts the burden
of proof on adding apparatus. Propose it separately (§4.4).

---

## 3. Record and code repair — no migration needed

### 3.1 Corrections (all of §1)
- Append to `RULINGS.md` a dated correction: applied at 20:56:54 in `befaa29` (1.3).
- Write the **session record** `sessions/session_2026-09-01-research-batch-04-accessible-circulation.md`
  carrying: the §1.4 breach and misreading (1.1); the 147→138/134 correction; the item-value
  crossings, which rule 4 says must be *"recorded, not hidden"*; and the corrections table in 1.6.
  The migration ledger already NAMES this record and it does not exist (A-08, B-20).
- **Attestation is NOT owed** — critic B confirmed this PR touches no `decisions/`, `sessions/`,
  `references/bpc-reasoning/` or `references/connection-reasoning/` path, so CLAUDE.md rule 2 never
  triggered. *Writing the session record will trigger it*, so the attestation lands with it.
- Update `sessions/LATEST`. **Do NOT update `LATEST-RESEARCH`** — no research was logged to the DB
  (B-13/B-14), so pointing the citation-mining gate here would scope it to nothing and pass green,
  which is §7 trap 2 exactly.
- Update the PR body: 42/15/8; name the 8 advisory failures; state that 8 BLOCKING gates are now
  vacuous (B-22); replace "the item layer is gone" with the row-vs-rendered distinction (1.5);
  correct "admissions" and "logged queries" (B-13/B-14); drop "This retracts batches 01–03" for
  "retracts their evidence; their 28/60/10/5 research rows remain, 7 modified" (B-31).

### 3.2 A-06 — fix `validate_schema` properly
Move the empty-registry branch AFTER the `--cross-check` dispatch so `run_cross_checks()` is
reachable; delete the false comment; correct the stale `data/specifications` docstring.

### 3.3 A-07 / B-12 — finish the caller sweep
- `governance/pipeline-contract.yaml:7` spine still reads `… -> Item (ENT-08) -> render`; criterion
  `base-parameter-vocabulary` still points at `scripts/validate_items.py`.
- `governance/research-contract.yaml` R12 still orders *"Code values → jurisdictional_values"*, and
  `db.py:2383` refuses every such write now that `items` is empty — the contract instructs an
  impossible act. Regenerate the SessionStart hook after editing.
- Registry notes for `validate_items` and `site_pages_fresh` assert *"not a corpus that legitimately
  empties"*; both now fail their vacuity floors.
- **R-03 residue (B-12):** item codes still sit in `terms.scope_note` ×7, `axes.design_domains` ×17,
  `search_candidates.title` ×13, `search_executions.findings_note` ×1. The ruling said the retained
  base should be *pared* of item codes. Disclose and register as owed; the text edits are a
  content judgement (§4.2).
- A-09: `test_db_integrity` L02 now vanishes silently when the YAML dir is absent; add the
  `else: record(..., subject=0)` branch so the skip is stated, per the file's own C05 convention.

---

## 4. Owner decisions — NOT a session's to make

### 4.1 `jurisdictional_values` was deleted on an over-read (B-19) — **the most serious open item**
Neither quoted ruling names the table. `item_code` is `NOT NULL REFERENCES items`, so it could not
take the null-the-pointer treatment R-04 gave `citation_mining` without a re-key. And two records
say this was owed its own decision:
- **DR-2026-08-19 §1.5** demands the `jurisdictional_values` consequence be decided *"as its own
  decision, before `items` is touched… It must not be collateral damage."*
- **D-0181 (2026-08-31, one day old)** treats the rows as research: *"jurisdictional_values holds 109
  rows and is renamed research_code_leads by the parked migration 065."*

`RULINGS.md` records neither. CLAUDE.md rule 0 requires a supersession be RECORDED. **Question:**
confirm the deletion supersedes D-0181 and §1.5 — or restore the 109 rows re-keyed off `item_code`
as `research_code_leads`, which is what D-0181 anticipated.

### 4.2 The rendered determinations (1.5, A-05)
`site/populations/*` still publishes **172 links across 79 item codes**; `site/index.html` and root
`index.html` carry 12 more into the deleted directory; `site/assets/e-08-jurisdictions.json` is an
orphaned copy of an archived YAML record. `index.html`, `parts/`, `versions/` still state the
determinations. `validate_cross_refs` treats `site/` as REFERENCE_ONLY, so no gate fires.
**Question:** is `site/` a frozen reference surface (restore `site/specs/`, stop) or a live one
(finish the sweep to `_archived/` and fix the links)? Mission and work-product inclusion is DG-NON.

### 4.3 The instrument contradicts itself (1.1)
§1.4 rule 1 forbids taking the frame from items; §12.1 step 2 instructs `db.py items --category A`.
One must be amended.

### 4.4 Re-running the batch
The research survives as material. Re-admitting it needs: the §2.1 fix landed, a frame derived from
ICF/access-needs rather than items, D'Souza's tier re-argued (B-17 — T1 was asserted on a test the
same brief used to put Chang & Drury at T3), the RNIB Co-1 hedge carried through (B-16), the
entrance-vs-kerb inference dropped or evidenced (B-18), and `co1_provenance` reachable through the
CLI at all — a coverage bug not currently registered.

---

## 5. What the critics CLEARED, so nobody re-derives it

- **Every table count** in every commit message: exact, both directions, against `origin/main` and HEAD.
- **No FK orphans** on either side; `integrity_check` ok; all 18 views enumerated — only the three
  `v_coverage_*` changed meaningfully (that is 2.3, not a separate defect).
- **Every item-keyed table** other than the four deleted was ALREADY zero on `origin/main`.
- **Migration mechanics**: `content_sha` correct, rebuild-identical, guards cannot fire, ledger sound.
- **`graph_audit` fixture**: provably never touches canonical, cannot collide, still measures what it claims.
- **No live code path** reads the archived YAML.
- **Bibliographic fidelity: no invented authors.** All 19 Crossref payloads match the briefs. The
  Bennett 2009 duplicated author list is real in the payload. Geoerg 2019 is 4 authors in Crossref,
  Semantic Scholar and DOAJ. NFBUK §2.8/2.9 and RNIB's 60 mm line are verbatim in the extracted text.
- **Attestation was not owed** (see 3.1).
- **Canonical sha256 unmoved** until `migrate_db`, as required.

**Two of critic B's own claims were wrong**, and are corrected rather than carried:
- B-13 says *"the only `log-search` invocations are `--help`"*. One non-help invocation appears in the
  command log. It does not change the finding — zero `search_executions` rows exist — but the
  absolute phrasing is not supported.
- B's paraphrase *"8.3% of a 338-person sample"* misread the brief; the brief's own wording
  (*"8.3% of men in a sample of 338"*) is correct. B caught its own error and said so.

---

## 6. Sequence

| # | Act | Gate |
|---|---|---|
| 1 | Compensating migration: §2.1 + §2.2 + §2.4 | `next_ref_id` → REF-00971; `citation_mining.doi` 10/10; FK check 0 |
| 2 | §2.3 restore + retire H05 (coupled) | `test_db_integrity` green with H05 gone; `v_coverage_*` honest |
| 3 | §3.2 `validate_schema` fix | `--cross-check` actually executes |
| 4 | §3.3 caller sweep + hook regen | `--selftest` PASS; R12 no longer orders an impossible write |
| 5 | §3.1 session record + attestation + pointers + PR body | attestation schema-valid; `LATEST` moved, `LATEST-RESEARCH` NOT |
| 6 | §4 to the owner | — |

Acts 1–5 are mine. Act 6 is not, and **§4.1 should be answered before act 1**, because restoring
`jurisdictional_values` would change what the compensating migration must contain.

---

## 7. §4.1 ANSWERED — measured 2026-09-01, after the plan above was written

The owner asked what serves long-term integrity and how much of `jurisdictional_values` can safely
move to another phase. Measured rather than argued.

### 7.1 What the 109 archived records actually contain
Exactly **three** columns carry data — `item_code`, `jurisdiction`, `standard_name`, each 109/109.
`value_text`, `value_numeric`, `unit`, `is_code_minimum`, `spec_id`, `source_section`,
`evidence_tier`, `notes` are **0 non-null of 109**, cleared by the 2026-08-12 REFERENCE-ONLY ruling.

| measure | value |
|---|---|
| records | 109 |
| distinct `(jurisdiction, standard_name)` | **83** |
| rows that are pure item-crossing duplication | **26** |
| distinct `item_code` | 20 |
| jurisdictions | 12, all valid codes: AU CA CH DE EU FR GB ISO JP NO SG US |

**100% of the surviving information is item-independent.** The only item-dependent column is
`item_code`, which the ruling removes. Relocation therefore loses nothing but the duplication.

### 7.2 CORRECTION to my own first measurement
A first pass matched archived standard names against `source_locators` with
`standard_number LIKE '%key%' OR title LIKE '%key%'` and reported **"81 of 83 already held."**
**That is wrong.** The loose pattern was matching a corrupted column. Matched strictly against
`source_locators.standard_number`, the overlap is **11 of 83**. So ~72 of the 83 exist nowhere else
in the project and are lost with the archive if not relocated. Recorded because the wrong figure
would have argued the opposite conclusion — that relocation was mostly duplication.

### 7.3 Why `source_locators` is the wrong destination, measured
- **24 rows carry BOTH a `standard_number` and a `doi`.** A standard has no DOI. This is the
  signature of two identifier classes with different shapes forced into one row format — the same
  defect as `REF-00037`, and the cause of today's false R9a block on Rouvier.
- **`jurisdiction` is no longer a jurisdiction column.** ~200 distinct values, including full URLs
  (`https://www.ada.gov/...`), prose findings (`Descent fall risk 3x ascent`), slug names,
  quantified claims (`2cm threshold defeats 45.8%`), and warnings
  (`KfW "Altersgerecht Umbauen" grant SUSPENDED Dec 2021`). Roughly nine values are real codes.
- The 83 code leads are, by contrast, the **cleanest structured data in the project**: uniform,
  complete, no nulls in any populated column. Merging the cleanest data into the dirtiest store
  destroys the ability to tell them apart afterwards.

### 7.4 Recommendation
Restore the 83 as a **research-stage table with a constraint surface `source_locators` cannot
have**: `jurisdiction` NOT NULL against a controlled list, `standard_name` NOT NULL, and **no DOI
column at all** — which makes the 24-row collision structurally impossible rather than merely
discouraged. This is what D-0181 already named `research_code_leads`.

**Not a rule-5 breach.** Rule 5 forbids the same FACT in two tables; after the move a code lead
lives in exactly one place. The 11 overlaps are reconciled, not duplicated.

**Do not carry `item_code`.** It is a coverage hint — "this standard was consulted for corridor
width" — and under the owner's frame that is the presupposition to avoid. It is not lost: the
archived filenames encode it (`a-3_e08.yaml` -> E-08), so it stays auditable in `_archived/` while
being absent from the live frame.

**So §4.1 is not a supersession of D-0181 — it is its EXECUTION.** D-0181 called these rows
research; the retraction deleted them instead of moving them.

### 7.5 A defect found while answering
D-0181's note reads *"renamed research_code_leads by the parked migration 065"*. **Migration 065 is
`065_one_link_table_four_lenses.sql`** — the lens work of 2026-09-01 consumed the reserved slot. The
rename has no migration number, and a session reading D-0181 would look for one that does not exist.
Class DOC-DRIFT, P3; the fix is a corrected note on the register row, not a renumbering.

### 7.6 Explicitly OUT of scope
`source_locators` needs its own repair pass — 32 duplicate DOIs, the misaligned `doi`/bibliography
columns, and the `jurisdiction` junk drawer. That is a larger job than this one and must not ride
along on it.
