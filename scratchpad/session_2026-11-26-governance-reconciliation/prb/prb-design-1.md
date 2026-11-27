# PR B, part 1: design (agonist's case)

Agonist report, 2026-11-27. Branch head `ee815a82`, schema `user_version` 167. Method: DR-2026-08-19 section 7
(agonist-antagonist). This file designs the change and implements nothing. The repository and `data/guidebook.db` were
read only. The canonical sha256 was `3d419efb…68edb9` before the probes and unchanged after them.

The engine was run on scratch copies in
`/tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/prb1/`.
"After" behaviour was simulated in memory on a read-only connection. Nothing was written to the repository.

Rule 7a: every figure here is a reading taken today, and the command that produced it sits beside it. Re-run the
command rather than trusting the figure.

Scope: three parts of one tooling pull request (CLAUDE.md rule 10).
- (I) T-117, the marker table.
- (II) The selection slice of T-059.
- (III) T-056 item 3a.

They change one engine function (`determine`), so they ship together: one `RULE_VERSION` bump and one migration.
PROXY-grade "thin" is an open owner input (Q3) and is not decided here.

---

## 0. The probe: what reaches the book today

All four commands below ran from `/home/user/guidebook`. `$S` is the scratch directory above.

```
cp data/guidebook.db $S/r3.db
python3 scripts/assess/assess_cell.py --db $S/r3.db --emit-sql $S/r3.sql --parameter-id 3 \
  --slug accessible-circulation-geometry --identity MOB --session session_prb1-probe \
  --stamp "2026-01-01 00:00" --report-json $S/r3.json        # the same with 12 for r12
GUIDEBOOK_DB_PATH=$S/r3.db python3 scripts/tests/test_db_integrity.py   # the same with r12.db
```

**Engine output (quoted):**
```
param 3×MOB  provisional  basis=T4-6-only-threshold+CO1+T2-direction(proxy_inference) scale=universal  refs=27 sources=31 extractions_in_lens=116 outside_lens=6 nonanchor=0 rso=0 marker=○
param 12×MOB provisional  basis=T4-6-only(regulatory_stratum_only) scale=universal  refs=10 sources=10 extractions_in_lens=20 outside_lens=1 nonanchor=0 rso=1 marker=○
```

**Integrity test.** It exits with `rc=1` on both copies, failing on
`[✗] C10: no published cell rests on an unverified or disputed source (1 examined)`.
- In the 3×MOB row, six governing sources are not verified: REF-00994 (T4), REF-00997 (T5), REF-01013, REF-01014,
  REF-01016 and REF-01026.
- In the 12×MOB row, one is not verified: REF-01016 (T6).
- Command: `select j.ref_id,e.tier,e.verification_status from specification_source_links j join evidence_sources e using(ref_id) where j.specification_id=9 and e.verification_status<>'VERIFIED'`, run on each copy.

**The CHECK.** On an in-memory copy of `r3.db`, `update specifications set marker='⚠' where specification_id=9` is
refused with `CHECK constraint failed: marker IS NULL OR (marker IN ('●', '◐', '○') AND (regulatory_stratum_only = 0 OR marker = '○'))`.
On `r12.db` (where `regulatory_stratum_only` is 1), `◐` is refused as well.

**The governing list (3×MOB).** Four sources are in the engine's `source_records` but are neither governing nor
supporting: REF-01005, REF-01008, REF-01025 and REF-01029, all T3 grey and all VERIFIED.
- Nine of their rows are excluded with the sentence "*supplies a value, but REF-… is not in the governing set: it was
  disqualified on tier, verification or supersession*".
- REF-01025 states 1:20, which is the headline value.
- Command: on `$S/r3.db`, `select … from specification_extraction_links … where specification_id=9 and role='excluded'`.
  The full query is in the transcript.

**Synthetic cases.** These run today's engine on the test file's own fixture builder (`synth_db`), in memory. Each
line is a wrong thing the code produces today (output quoted, abridged):

| fixture | today | the owner's rule gives |
|---|---|---|
| T1 states 1:12; three T6 codes state 1:20; `lower_is_better` | `stated`, value 8.33 % (1:12), governing 1 | 5 % (1:20): the code value wins when no harm is stated (ledger 7177) |
| one T4 standard only | marker `○`, `scale=universal` | `◐` ("T4 only half circle", 7195); `population` (OD-48) |
| T3 clinical only | marker `●` | `◐` (OD-57, 7303 and 7327) |
| T2 sr_meta UNVERIFIED only | `stated`, marker `○` | ⚠ if it has a route; otherwise it anchors nothing (§1.2 below) |
| three T6 at 1:12 plus T3 grey at 1:20 | value 1:12, marker `○`, grey not governing | 1:20 marked ⚠ (U1 at 7870; OD-64 at 7424) |
| T1 UNVERIFIED states 1:20; T3 clinical states 1:16 | marker `○` | ⚠ for a value whose only source is unverified (7053) |
| Co-2, keyed on ICF `d450` only | `scale=population` | `universal`: no identity code (OD-48, 7995) |

The values of live cells do not change. Every lens cell of parameters 3 and 12 was run before and after the slice. It
added governing sources only to 3×MOB, and no cell's headline moved:
- 3×MOB stays 5 %.
- 12×MOB stays 6000 mm.
- The other five cells are `pending` before and after.
- Command: the in-memory loop in the transcript over `extraction_lens_links` for parameters 3 and 12.

---

## 1. (I) T-117: the marker table in code

### 1.1 The wrong thing that reaches the guidebook today
1. **The stored glyph is right only by accident.**
   - For 12×MOB: the value's own source is REF-00988 (T5, VERIFIED). The engine writes `○`, but only because of the
     regulatory-only override (`assess_cell.py`, `if regulatory_stratum_only: source_bands = []`). `band(5, …)` still
     returns PARTIAL (`schemas/tier_derivation.py`, `if tier in (4, 5)`).
   - For 3×MOB: the marker comes from `_confirmed_bands`, under the 2026-10-21 rule that an unconfirmed code row is
     weak, and not from the value's own source.
   - A different corpus gives a wrong glyph with nothing going red. The synthetic table above shows T4-only `○`,
     T3 clinical `●`, and an unverified sole source `○`.
2. **A published cell cannot exist.**
   - C10 refuses any live row with a non-VERIFIED governing source. That is both probe rows (rc=1, quoted above).
   - The CHECK refuses ⚠, so a value that rests only on an unverified or grey source cannot be stored with the
     owner's glyph.

### 1.2 The rulings applied (line numbers in `references/project-standards.md`)
- OD-57 at 7303 ("od57 yes"), recorded at 7327–7328. The circle table is ● for T1, T2, Co-1 and Co-2; ◐ for T3 and T4;
  ○ for T5 and T6.
- 7195: "T4 only half circle". 7071: "thin too".
- 7053: "no, triangle instead if the value is coming from grey or unverified". The correction entry begins at 7049.
- 7039: "except use the Unicode one", meaning U+26A0 with no U+FE0F.
- 7005: "let's return to keeping them but they get a triangle warning".
- OD-64 at 7401 ("2 triangle for all"), recorded at 7424–7425. Every grey basis takes ⚠, T3 grey included.
- OD-59, registered at 7273 and recorded at 7333–7334. The showcased value carries the grade of its own source, with ⚠
  only where that value's own basis is grey, unverified or thin.
- OR-22b at 6183: a floor claim that a verified study confirms by absence takes "the study's own band", and
  "migration 116's regulation-only rule (○) does not apply to it".
- OR-23 at 4725 ("only when the source is properly cited in an academic context") and OR-23b at 6186 ("for T4 to T6 …
  cited by jurisdiction, standard number and clause").
- `governance/tier-system.md:77`: "with one it carries ⚠; without one it anchors nothing".
- Thin: the owner's definition is at 7087. The project's own inferences are thin (7119). A mixed value is thin (7159).
  Not thin: a vetted clinical judgment (7101) and a clinician's or academic's derivation (7137).
- What is not ruled: whether "any PROXY grade makes a value thin" (the entry at 7083, "What it does not decide"; and
  `tier-system.md:80`). The ACTION at 7096 says "derive thin from the population match and the proxy-inference
  record", but it does not say which state of either record is thin.

**What C10 must become (my reading).** The owner's words give three rules:
- "Keeping them" plus "triangle instead": an unverified source is kept, and a value that comes from it carries ⚠.
- OD-59: the triangle belongs to the value, not to the cell's whole governing set.
- OR-23 and OR-23b, as reconciled in `tier-system.md:77`: an unverified source anchors only with a route.

So C10 stops refusing a source merely for being unverified. It refuses a source that is unverified **and** has no route.
The engine gives the triangle per value. T-117 item 4a ("not VERIFIED … unless its marker is ⚠") contradicts OD-59 once
the governing set spans tiers, because it would force ⚠ on every cell that holds any unverified source. It also ignores
OR-23 and OR-23b.

### 1.3 The smallest code change
1. **`schemas/tier_derivation.py` `band()`.** Reads `(tier, evidence_type)` as today.
   - Before: `if tier == 3: return FULL if evidence_type == "clinical" else WEAK`, and `if tier in (4, 5): PARTIAL`.
   - After: tier 1 or 2 → FULL; tier 3 or 4 → PARTIAL; tier 5 or 6 → WEAK.
   - The docstring says a grey basis is shown as ⚠ by the engine, never by a circle (OD-64), and cites the ledger
     headings. The T3 type split goes: `band()` no longer reads `evidence_type` for T3.
   - Co-1 and Co-2 are tiers 1 and 2 in `TIER_MAP`, so no list is typed.
2. **`schemas/enums.py` `EvidenceMarker`.** Add `WARNING = "⚠"`.
   - `ordinal` counts the circles only: `circles=[m for m in EvidenceMarker if m is not EvidenceMarker.WARNING]`.
     This keeps ● 3, ◐ 2, ○ 1 (`tier-system.md:78`). `WARNING.ordinal` raises.
   - `floor_mean` iterates the circles only.
   - Read by: `determine`, the `EvidenceStateRecord.marker` field, the CHECK-parity test
     (`test_assess_cell_pilot.py`, "MARKER vocabulary"), and render (T-037).
3. **`scripts/assess/assess_cell.py` `determine`, the marker block.** It reads `recs`, `governing`, `confirmed` and the
   stating rows from item 4. Before:
   ```
   if regulatory_stratum_only: source_bands = []
   else: … verified governing … _confirmed_bands … band(...)
   marker = floor_mean(source_bands or [EvidenceMarker.WEAK]).value
   ```
   After, in outline:
   ```
   confirmed = _confirmed_bands(conn, parameter_id, links, confirmer_anchors, lens, by_ref)   # every cell (OR-22b), not only proxy
   def own(ref):   # a source's own marker, tier-system §5
       r = by_ref[ref]
       if r["evidence_type"] == EvidenceType.GREY.value or not _verified(r): return EvidenceMarker.WARNING
       return confirmed.get(ref) or band(r["tier"], r["evidence_type"])
   basis = stating_refs or governing          # OD-59: the value's own sources; with no value, the cell's set (R7)
   marks = [own(g) for g in basis]; circles = [m for m in marks if m is not EvidenceMarker.WARNING]
   if not circles:                      marker = WARNING
   elif stating_refs and set(marks) != {circles[0]}: raise Refusal(<Q-B2: several sources state the value with different markers; nothing written>)
   else:                                marker = floor_mean(circles)   # one circle when a value is shown; R7's floor mean when none is
   ```
   Thin is not computed (§1.8, Q3). The hook for it is the `own()` predicate: a ruling adds one condition there.
4. **`_compose_headline` and `compose_value` return the stating extraction ids** as a sixth element: the headline rows
   whose bound equals the selected `vmin` or `vmax`.
   - Kept as a list parallel to `bounds`, so the existing `for b, _u in bounds` loops are untouched.
   - Read by: the marker block only.
   - Callers to update: `determine`, and `scripts/tests/test_scan_contract.py:1019`, which unpacks five values.
5. **`_confirmed_bands`.** An unconfirmed row takes its source's own band, not WEAK. The 2026-10-21 "weak" premise was
   "a value read off the regulatory stratum is weak", which "T4 only half circle" replaced. The per-source floor mean
   ("one confirmed clause does not confirm the code") is kept.
   - It now runs for every stated or provisional cell (OR-22b), not only proxy cells.
   - On today's data this changes nothing: all three `confirms` edges have label referents (`select … from extraction_relations where relation='confirms'`).
6. **Delete the regulatory-only override** and correct its comment block, which still says "Option A section 2.3 …
   weak".
7. **The route gate (OR-23 and OR-23b).** One predicate, `dbcore.route_shown(conn, ref_id, parameter_id)`:
   - For a source at or above `dbcore.REGULATORY_FROM_TIER`: `jurisdiction` and `standard_number` are both non-NULL,
     and every live value-supplying row of the source for the parameter carries a locator (`clause_id` or any `loc_*`
     column, with the names read by PRAGMA, not typed).
   - For T1 to T3: no recorded academic route exists (Q-B4), so the predicate returns not shown.
   - The engine drops a non-VERIFIED source with no shown route before `classify`. It is still counted in
     `has_unverified_sources`, and its rows are listed as excluded with the reason.
   - Read by: `determine` and C10.
   - Today `standard_number` is NULL on all eight unverified sources
     (`select ref_id,standard_number from evidence_sources where verification_status<>'VERIFIED'`), and
     `source_locators` holds no row for the six that govern 3×MOB.
8. **`scripts/tests/test_db_integrity.py` C10.** Its subject stays the published cells. It fails when either holds:
   - a non-VERIFIED governing source for which `dbcore.route_shown` is false; or
   - a cell whose governing sources are all non-VERIFIED and whose marker is not ⚠.

   Exact "value's own source" correctness stays with the engine's unit tests and with
   `derivation_handshake_integrity` item 6 (advisory). Re-deriving the selection inside C10 would be a second home.

### 1.4 Red tests (write first)
In `scripts/tests/test_assess_cell_pilot.py`. The prefix is free (`git grep -c 'T117-' scripts/tests/` prints 0
today). Fixtures use the file's `synth_db`.

- **T117-01.** `synth_db([{"tier":4,"evidence_type":"standard_eb","claimed_value":"1:12","claimed_unit":R,"comparator":"<="}], direction="lower_is_better")` at `MOB`. Assert marker `◐`. Red: `○` (quoted above).
- **T117-02.** A unit test on the function: `band(5,"national_fw") == WEAK`. Red: PARTIAL.
  - Defect in the T-117 file: its T117-02 says a T5-only cell is red at engine level ("◐ before"). It is not. The
    override masks it, and the engine writes `○` today (synthetic "T5-only (US, CA)" → `○`).
- **T117-03.** `band(3,"clinical") == PARTIAL` (red: FULL). The grey case: three T6 at 1:12 plus T3 grey at 1:20,
  `lower_is_better`. Assert value 5 %, marker `"⚠"` and `"️" not in marker`. Red: value 8.33 %, marker `○`.
- **T117-04.** A T4 source that is UNVERIFIED and has `jurisdiction`, `standard_number` and a locator states the
  selected value alone. Assert ⚠. Red: today it is left out of the marker and gives `○`.
  - The same source without `standard_number`: assert it is excluded and the reason names OR-23b. Red: today it
    governs.
  - A Co-2 control: `●`, green before and after.
- **T117-05.** Runs against the live DDL, through the existing `try_row` helper. A live row with marker ⚠ is accepted;
  `◐` with `regulatory_stratum_only=1` is accepted. Red: both refused.
  - Deliberately not asserted, unlike the T-117 file: "● with rso=1 refused" (see §1.6).
- **T117-06** (OD-59). T1 states 1:20 and T3 clinical states 1:16. Assert `●`.
  - This is green before (T1 is the only governing source today). It kills the mutation "floor mean over all governing
    sources", which gives `◐`.
  - The same fixture with T1 UNVERIFIED: today `○` with T1 anchoring. After: T1 is excluded (no route, Q-B4), and the
    value is 1:16 from T3 clinical, marked `◐`. That is red.
- **T117-07** (C10). Copy the live database to a temporary file and insert one `stated` cell plus its source links.
  Assert C10's result from the importable `run_checks(db_path)`. The accessor for that result is [UNVERIFIED]: read
  `record()` first.
  - (a) An unverified governing source with a route, not stating the value, under a circle: passes. Red: fails today.
  - (b) An unverified governing source without a route: fails.
  - (c) All governing sources unverified, under a circle: fails.
- **T117-08** (Q-B2). Two sources state the selected value, one verified T6 and one T4 with a route but unverified.
  Assert `Refusal` naming Q-B2. Red: today `○`.
- Existing assertions that flip; each is a caller, edited in the PR:
  - "T3-clinical alone … still full", line ~730, becomes ◐.
  - "a stated cell resting on an unverified source is not full", line ~812: the cell becomes `pending` (no route).
  - "a source with no recorded verification …", line ~806: it becomes `pending`.
  - Case 3d's "the row's CHECK pins … weak": the value is still WEAK (T5 is ○), but the reason text is false and is
    reworded.
  - The `_proxy_cell` cases with T4 or T5 codes, if any: find them with `grep -n -E '"tier": (4|5)' scripts/tests/test_assess_cell_pilot.py`.
- **After-test.** The whole file is green, plus seeded defects, each killed:
  - `band()` T4 → WEAK (kills T117-01).
  - The override restored (kills T117-01).
  - ⚠ written with U+FE0F (kills T117-03).
  - The `own()` predicate replaced by a floor mean over governing (kills T117-06).

### 1.5 Schema migration
`scripts/migrations/168_marker_table_and_harm_relation.sql` sets `PRAGMA user_version = 168`. It holds both rebuilds of
this PR; the second is in §2.5.

**The CHECK.** It becomes `marker IS NULL OR marker IN ('●','◐','○','⚠')`. The second CHECK (live ⇔ marker) is
unchanged.

**SQLite needs a rebuild.** A column CHECK cannot be altered (migration 116 added this one with `ADD COLUMN`). The
recipe is migration 114's, generated from the live DDL with one substitution:
1. Capture `sqlite_sequence`.
2. Drop the view closure. This is derived, not typed: views whose SQL names `specifications`, transitively. Today that
   is `v_best_practice`, `v_determination_provenance`, `v_divergence`, `v_gap_subject`, `v_item_provenance`,
   `v_pending` and `v_source_reach_all`.
3. `CREATE TABLE "_168_new_specifications"`, then `INSERT … SELECT` by column name, `DROP`, `RENAME`.
4. Recreate `idx_spec_row_identity`, `idx_spec_retired`, the trigger `trg_spec_retire_needs_reason` and the views from
   their stored SQL.
5. Restore the sequence as a maximum.
6. The inbound keys need no rebuild, because the rename keeps the name: `specification_source_links`,
   `specification_extraction_links`, `determination_gates` and the self-reference. `migrate_db.py` turns foreign keys
   off outside the transaction, so run `PRAGMA foreign_key_check` after.

**Replay order.** No new `-- AFTER_DATA:` marker is needed. This corrects the T-117 file, which says it is "required".
- The CHECK only widens: old ⊆ new. No column is renamed or dropped.
- The last committed data migration that writes `specifications` is `data_20260918201549…`. The loop in the
  transcript greps `INSERT INTO|UPDATE|DELETE FROM "specifications"` across `data_*.sql`.
- The existing marker chain (131 and 146, `-- AFTER_DATA: 20261106053823`) already replays 168 after it.
- No data migration later than that cutoff writes `specifications` or `extraction_relations`.

**Rule 3 and rule 5.** Committed data migrations are untouched (they are immutable). No column is dropped.
`migration_reproducibility` compares row counts, and a rebuild preserves them. Prove the rebuild with
`migrate_db.py --rebuild` and `migration_reproducibility.py --deep`, which compares every row. Then run the CLAUDE.md §4
UNWRITABLE derivation; it must print no new line.

**Retired rows.** All eight existing rows are retired, with marker NULL (`select specification_id,marker,retired_at is not null from specifications`).

### 1.6 Where this deliberately departs from the T-117 file
- **No `regulatory_stratum_only = 0 OR marker <> '●'` clause.** OR-22b (6183) lets a regulatory-only cell whose claim a
  verified study confirms take that study's band, and confirmers are anchoring tiers, so that band is ●. The clause
  would refuse an owner-ruled state.
- **No `population_match` parent extension.** Nothing reads it until Q3 rules that PROXY makes a value thin
  (CLAUDE.md §8).
- **C10 as in §1.2 above, not item 4a.**
- **`rests_on_proxy_inference` is not a thin cause** (§1.8).

### 1.7 Callers to sweep (rule 4)
Commands (re-run them):
- `git grep -n -E 'EvidenceMarker|floor_mean|\bband\(' -- scripts schemas`
- `git grep -l -w marker -- scripts/tests`
- `sqlite_master like '%marker%'`
- the registry sweep in T-117 §5

What they found today:
- **Code:** `schemas/enums.py`, `schemas/evidence_state.py:179`, `schemas/tier_derivation.py`, `assess_cell.py`
  (`band`, `floor_mean`, `_confirmed_bands`, marker block, `STORED_ANSWER`).
- **Tests:** `test_assess_cell_pilot.py` (the "MARKER vocabulary" parity, about 15 marker assertions, `BAND` at ~1393),
  `test_db_amend_writers.py:117`, `test_evidence_cell_state_2_3.py:52`, `test_run_pipeline_refusals.py:2339`,
  `test_validate_evidence_state_2_4.py:27`, `test_scan_contract.py:1019`. The last is the 6-tuple caller; the others
  insert WEAK or FULL and stay true.
- **Views and triggers:** none read `marker`. `v_item_provenance` names `regulatory_stratum_only` and is recreated
  verbatim.
- **Registry:** the hits on `marker` (`skill_vocabulary_audit`, `code_value_identity_audit`) are "scope marker", which
  is a mention. `test_assess_cell_pilot` is a caller. `test_db_integrity` (blocking) holds C10.
- **Prose:**
  - `governance/tier-system.md:81` ("Until T-117 lands … earlier table") becomes false on merge, so delete it in this
    PR. Editing `governance/` needs no attestation.
  - The ○ gloss "grey, thin or unverified" survives in `governance/owner-browser.yaml:111,807` and in
    `skills/evidence-auditor_SKILL.md:47`. These belong to T-120. List them, do not edit them.
  - The comment in `schemas/enums.py:94` repeats the gloss and is corrected here.

### 1.8 Open owner inputs for (I) (never decided here)
- **Q3.** Does a PROXY grade make a value thin?
  - Q3b: does `rests_on_proxy_inference` make it thin?
  - Evidence against reading Q3b as already ruled:
    - The 3×MOB value (5 %) is stated verbatim by REF-00992 and REF-00995 (extractions 25 and 30). It is no new value
      the project proposed (7159).
    - Read as thin, it would mark a code-only cell ⚠ only when research findings also exist. More evidence would then
      lower the marker, which the engine's own R39 comment refuses.
- **Q-B2 (new).** When several sources state the selected value, whose marker does the value carry?
  - (a) Mixed: some warned (grey or unverified), some not.
  - (b) Different circles.
  - OD-59 (7273) answered "its own source" for a value with one source. F5 of antagonist-4 found the plural case
    unruled.
  - Until it is answered, the engine refuses (T117-08). It does not fire on 3×MOB or 12×MOB after the route gate (§3).
    It would fire on 3 if REF-00994 gained a route.
- **Q-B4 (new).** How is OR-23's "academic route" recorded for an unretrievable T1 to T3 source?
  - Until it is answered, such a source anchors nothing: "without one it anchors nothing" (`tier-system.md:77`).
  - Live effect: none on parameters 3 and 12. The one unverified T1 source, REF-01002, is not in the 3×MOB gathered
    set (re-run the source list query of §0).

---

## 2. (II) The T-059 selection slice

### 2.1 The wrong thing that reaches the guidebook today
- The cascade in `determine` picks one stratum as the governing set:
  - anchors (T1, Co-1, T2, Co-2) if any;
  - else T3 clinical;
  - else T4 to T6, with T3 grey never governing (`elif b["t3g"]: state = "pending"`).
- `compose_value` then picks the most accommodating value inside that stratum only. The resulting wrong things:
  - **The value.** A more accommodating code value is hidden behind a research value with no harm statement. The
    synthetic H1 case states 1:12 where the owner's test gives 1:20.
  - **The source list.** On 3×MOB, four eligible T3 grey sources, one of which states the headline, are excluded with a
    false reason ("disqualified on tier").
  - **The prose.** The proxy branch writes "not a best-practice claim" and "only T1/Co-1/T2/Co-2 evidence can do that"
    into stored columns. U6 (7875) says "if the only values are from code then code determines the ideal/best".

### 2.2 The rulings applied
- The harm test, owner answer at 7173 and 7177.
- U1 at 7870. Its "tier sets the marker … not eligibility" is an [ASSUMPTION] of the recorder, but it rests on the
  owner's "if no, code wins".
- U6 at 7875.
- OD-58 at 7330–7331: a research publication or a clinical guideline states that a person with a disability struggles
  more at the more accommodating value than at the value it proposes. A statement is enough; it is never a code and
  never the project.
- The ACTION at 7343 (3).
- OD-65 at 7427: every code value carries a lens.

### 2.3 The smallest code change (`scripts/assess/assess_cell.py`)
1. **Eligibility is the union of today's per-stratum filters, with no filter changed.** This runs after the route gate
   of §1.3 item 7:
   ```
   eligible = anchoring(b["t1"]+b["co1"]+b["t2"]+b["co2"]+b["t3c"]+b["t3g"]) + b["t45"] + b["t6"]
   if state in ("stated", "provisional"): governing = sorted({r["ref_id"] for r in eligible})
   ```
   - The cascade still sets `state`, `tier_basis`, `conv`, `conf` and the gap. No state rule changes (§2.6).
   - `anchoring()` keeps excluding research that is MISMATCHed or fails B5a. The regulatory sets stay unfiltered, as
     today, which leaves the documented B5a question on codes open.
   - `tier_basis` now names the strata that set the state. Its comment "describes the GOVERNING set only" is corrected.
   - `supporting = sorted(set(supporting) - set(governing))`.
2. **`regulatory_stratum_only` and `code_floor_only` are read from the final governing set**, not set inside the G1
   branch.
   - rso = 1 iff every governing ref is in `b["t45"] + b["t6"]`, and the cell is not proxy.
   - cfo = 1 iff every governing ref is in `b["t6"]`.
   - Without this, a T3 grey source in a G1 cell would leave rso = 1, which is false.
   - Read by: `validate_evidence_state` ("stated but rso/cfo"), `register_integrity_check`, the CHECK, render.
3. **The harm test (displacement).** In `_compose_headline`, after the selection:
   - Collect `worse_at` edges (§2.5) whose from-row is in the cell's lens, from a live source of a counting kind, and
     whose referent row's bound equals the selected bound.
   - If any exist, the value becomes the most accommodating of the from-rows' own bounds ("the value that source
     proposes"). Repeat while that value is itself displaced, bounded by the number of bounds.
   - The kind rule:
     - A from-source in the regulatory stratum (`tier >= dbcore.REGULATORY_FROM_TIER`) never counts. The writer
       refuses it (§2.5).
     - Co-1, T3 grey and T2 `standard_eb` (national) are Q-B3 (open). If one of them would displace, the engine refuses
       the cell, naming Q-B3.
     - `clinical`, `sr_meta` and `co2` count: "research publication or clinical guideline".
   - Both values stay shown: the displaced row stays `governing` in the links.
4. **Reword the four stale prose strings** of the proxy and floor branches (the D-43 count `assess_cell.py:3`) to state
   the basis without a tier verdict.
   - The exclusion sentence for a value row outside the governing set becomes: "superseded, closed-unverified,
     unretrievable without a route (OR-23/OR-23b), population MISMATCH, or a stored tier not derivable (B5a)". Today's
     "disqualified on tier" becomes false.
   - Per-row precision is T-059 step 1, not this slice.
5. **`RULE_VERSION`** goes from `pilot-8` to `pilot-9`, with one comment line. The sha payload format is unchanged, so
   K01 in `test_db_integrity.py` needs no edit (its own comment at line 47).

### 2.4 Red tests
In `test_assess_cell_pilot.py`, using the T-059 numbering:
- **T059-H1.** T1 at 1:12, three T6 at 1:20, `lower_is_better`. Assert 5 %. Red: 8.33 % (quoted).
- **T059-H2.** H1 plus a `worse_at` edge from the T1 row to a T6 row, carrying a quote. Assert 8.33 %, with the T6 rows
  still `governing`. Red: the relation value does not exist, so the fixture insert fails.
- **T059-H3.** H2, with the T1 row linked to `DEAF` only. Assert 5 %.
- **T059-H5.** H2 from a T4 source. The writer refuses it. Inserted directly in the fixture, the engine ignores it:
  assert 5 %.
- **T059-H6.** H2 with the T1 row as a `claim`. Assert 8.33 %, with no measured outcome needed.
- **T059-H7.** H1 with direction NULL. Assert no value; green before, as a guard.
- **T059-H8 (new).** H2 from a T3 grey source. Assert a `Refusal` naming Q-B3.
- **T059-G1 (new).** Three T6 at 1:12 plus T3 grey at 1:20. Assert the grey ref is governing and the value is 5 %.
  Red: grey is excluded and the value is 8.33 %.
- **After-test.** Seeded defect: remove the lens filter from the harm reader. H3 must kill it.

### 2.5 Schema migration for the harm record (the second rebuild in 168)
Why existing records cannot hold an OD-58 statement:
- `harm_finding` is allowed only on `finding` rows and needs an `insufficient` edge.
- `insufficient` means "NOT ENOUGH", which is the opposite direction.
- `exceeds` means "more than needed", which carries no difficulty.

These are the definitions in the `extraction_relations` DDL. T-059 §4 item 6 reaches the same finding.

The change, in one migration:
- `relation` gains the value `worse_at`, with this meaning: "the source states that people struggle more at the
  referent's value than at this row's value". The from-row is the value the source proposes; the referent is the more
  accommodating value.
- A new CHECK: `relation <> 'worse_at' OR (to_extraction_id IS NOT NULL AND stated = 'named')`. That is, a row referent
  that the source itself names, never `inferred` (never the project's inference). It deliberately does not go into the
  `condition_on`/`derived_from` CHECK, because `_row_only_relations` (db.py:10926) reads that CHECK, and "leans on"
  is not this edge's meaning.
- The rebuild: the 114 recipe again. Closure: `v_derived_figure_check`. Indexes: `idx_xr_identity`, `idx_xr_to`.
  AUTOINCREMENT floor captured. Derived by the same closure query.
- **Writer (`scripts/db.py` `_write_relation_edge`), three refusals:**
  - the from-source is in the regulatory stratum (`dbcore.REGULATORY_FROM_TIER`);
  - the from-row is not in `dbcore.VALUE_SUPPLYING_ROLES`;
  - the new CHECK, restated as a sentence.
- No new verb is needed. `relate-extraction --relation` reads its choices from the CHECK (db.py:2991).
- Read by: the displacement in `_compose_headline`.

### 2.6 Deliberately not done
- The state rules for a grey-only cell (`pending`; DR-2026-07-12 item 2, whose premise was T3 grey's old ○) and for a
  code-only cell below §2.3 richness (`pending`). U1 and U6 question both, but they are state rules. No current
  identity cell is grey-only (query in the transcript), and both probe cells are rich. This is Q-B5.
- T-059 steps 1, 2 and 4 (exclusion causes per row, divergence, fragility note), its item 7 (flip to blocking:
  apparatus) and its T-128 dependency (withdrawn by OD-87).
- T-125's skill paragraph. In the parameter 3 corpus, every `insufficient` edge is on the steep side, and the one harm
  sentence (extraction 77) is from a T4 code, which does not count. So no harm statement waits to be recorded.

### 2.7 Callers
- **Code:** the cascade and G1 branch of `determine`; `compose_value` (6-tuple); `test_scan_contract.py:1019`; db.py
  `_write_relation_edge`.
- **Registry:** `extraction_relations_integrity` (blocking) reads `relation`. Run it before and after.
- **Tests:** the pilot's "NO-PROXY: tier_basis keeps the rso marker", line ~709, and the PROXY tier_basis cases are
  re-run; they should stay green.
- **Prose:** `governance/evidence-architecture.md:122` ("most-accommodating floor selection") and
  `governance/jurisdiction-philosophy.md:74` ("A code value does NOT establish best practice") are T-120's. List them.

---

## 3. (III) T-056 item 3a: design_scale states whom the determination is for

### 3.1 Wrong thing today
Both probe rows store `design_scale = universal`, keyed to `MOB`, because the G1 branch writes it from the stratum
(`assess_cell.py:1489`, `design_scale = SCALE_UNIVERSAL`). A wheelchair user's cell then says it is for everyone. The
reverse case also occurs: a Co-2 cell keyed only on `d450` stores `population` (synthetic, quoted).

### 3.2 Ruling
OD-48 at 7995–7996: "whom it is for", which is option (a) of T-056 item 3a: `universal` when the determination has no
identity code, `population` otherwise.

### 3.3 Change
- One line before the cascade: `design_scale = SCALE_POPULATION if identity else SCALE_UNIVERSAL`.
- Delete line 1489.
- Correct the G1 header comment (`assess_cell.py:86`) and the `schemas/directness.py:51` comment ("universal /
  code-compliant").
- "Rests on codes" is already `regulatory_stratum_only`. No reader read it from `design_scale`:
  `git grep -n -E 'design_scale|SCALE_UNIVERSAL' -- scripts schemas` shows only the vocabulary validators, the graph
  extractor and the tests.

### 3.4 Tests
- **T056-01.** A G1 cell at `MOB`: assert `population`. Red.
- The existing assertion "T6-only => design_scale universal" (line 248) is a caller and flips.
- **T056-02.** Anchored, `d450` only: assert `universal`. Red.
- **T056-03.** G1, `d450` only: `universal` (guard).
- **T056-04.** Anchored at `MOB`: `population` (guard).
- No migration: the CHECK already holds both values.

---

## 4. Expected live result after the PR (the live-data comparison, on a copy)
Only the fields named below may change. Any other change is a stop.

- **3×MOB.**
  - Governing: the 27 refs, plus the four T3 grey, minus the six unverified with no route, which makes 25.
  - The value stays 5 %. The stating rows are 25 and 30 (REF-00992 and REF-00995, T6, VERIFIED), so the marker is
    `○`. Extraction 28 (REF-00994) stated 5 % too, but now has no route.
  - `design_scale` becomes `population`. C10 passes.
- **12×MOB.**
  - Governing: 10 minus REF-01016, which makes 9.
  - The value stays 6000 mm, stated by REF-00988 (T5, VERIFIED), so the marker is `○`. `population`. C10 passes.
- Simulation commands: the in-memory runs in the transcript. The route-gate step is reasoned from the
  `standard_number` query, not executed: [UNVERIFIED] until built.
- Research consequence (for PR R1 and T-104): recording `standard_number` for REF-01016 (stated in its title,
  "NZS 4121:2001") brings it back as a ⚠ source. Whether `correct-source` accepts that for an unretrievable source
  without a payload is [UNVERIFIED].

## 5. What becomes dead (deleted in the PR)
- The regulatory-only marker override.
- The `if rests_on_proxy_inference:` guard on `_confirmed_bands`.
- The WEAK default for an unconfirmed row.
- The G1 `design_scale` line.
- The T3 type split in `band()`.
- C10's VERIFIED-only clause.
- The CHECK's second clause.
- `tier-system.md:81`.
- `floor_mean` stays. It is still read for a cell with no value (R7), inside `_confirmed_bands`, and by the
  derived-figure rule (`tier-system.md:78`).

## 6. Stop conditions
- The OD-57, OD-59, OD-64, OD-58 or OD-48 gate prints CLOSED.
- The live-data comparison shows a value or state change on any cell other than through the route gate as listed in §4.
- `migrate_db.py --rebuild` or the deep reproducibility check differs.
- The UNWRITABLE derivation prints a new line.
- A check green before is red after.
- Deriving a cause would need a list kept beside a column (rule 8). The exception is the Q-B3 open list, which is an
  owner question with a ledger pointer, deleted when answered.
- The owner answers Q3, Q-B2 or Q-B4 differently from how a test asserts. Then rebuild to the answer, and do not keep
  the test.

## 7. Size (reasoned, not measured)
`git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'`, estimated part by part:

| file | estimate | what it covers |
|---|---|---|
| `assess_cell.py` | about +90/−45 | marker block +20/−14; eligibility, rso and cfo +12/−6; harm reader +35; 6-tuple +6/−3; refusals +10; strings and comments ±15; design_scale +1/−1; RULE_VERSION +3 |
| `tier_derivation.py` | about +10/−10 | |
| `enums.py` | about +6/−2 | |
| `dbcore.py` | about +20 | `route_shown` |
| `db.py` | about +15 | refusals |
| `test_db_integrity.py` | about +25/−15 | C10 |
| `test_scan_contract.py` | ±1 | |
| new tests | about +170 | |
| flipped assertions | ±15 | |

- Total: about +350/−90.
- The migration file, outside the measure, is about 400 to 500 generated lines (two rebuilds and eight views).
- Without the harm record and reader, the PR shrinks by about 35 engine lines, 15 db.py lines and one rebuild. That
  would break "keep the harm test".

## 8. Open owner inputs, collected (ask before building)
- **Q3.** PROXY grade → thin? Q3b: `rests_on_proxy_inference` → thin?
- **Q-B2.** Several stating sources with different markers (mixed warned, or different circles).
- **Q-B3.** Do Co-1, T3 grey and T2 national evidence-based standards count as a "research publication or clinical
  guideline" under OD-58?
- **Q-B4.** How is OR-23's academic route recorded for an unretrievable T1 to T3 source?
- **Q-B5.** Does a grey-only or a below-richness code-only cell reach `provisional` under U1 and U6?
- **Coordinator, not the owner.**
  - Drop T-117's T-068 and T-120 dependencies.
  - Record the T-117 file defects: T117-02, T117-05's ● clause, item 4a, the "required" AFTER_DATA claim, and the
    unruled `rests_on_proxy_inference`-as-thin.

---

## 9. The agonist's case (for the antagonist to break)

**Claim 1.** For 3×MOB and 12×MOB, `○` is the right glyph under the owner's ruled table, once the route gate excludes
route-less unverified sources. The "wrong marker, ⚠" of the path-finder is not derivable from ruled text. What is wrong
today is how the marker is derived and the two gates (C10 and the CHECK), not the glyph.
- [CONFIDENCE: high for 12; medium for 3.] For 3 it depends on the route gate and on Q-B2.
- **Evidence:**
  - The stating rows are 25 and 30 (T6, VERIFIED, both `○` by band) and 28 (REF-00994, T4, UNVERIFIED, no
    `standard_number`).
  - For 12 the stating row is 116 (REF-00988, T5, VERIFIED, `○`).
  - PROXY grades exist on REF-00994 and REF-00995 only, and Q3 is unruled.
- **Falsified if:** a ledger line in the owner's words rules that a PROXY grade or a proxy inference makes a value thin;
  or that a value stated jointly by verified and unverified sources takes ⚠; or `standard_number` is found recorded for
  REF-00994 in another table.

**Claim 2.** T-117 item 5's CHECK clause `regulatory_stratum_only = 0 OR marker <> '●'` contradicts OR-22b. The CHECK
should only widen to four glyphs.
- [CONFIDENCE: high.]
- **Evidence:** OR-22b (6183) and `tier-system.md:76`. Confirmers come from `_anchors_of`, so they are FULL-tier.
- **Falsified if:** OR-22b was withdrawn after 2026-11-13; or a confirmed claim cannot occur in a cell with
  `regulatory_stratum_only = 1` once confirmation runs in every cell.

**Claim 3.** The rule requires route-gated eligibility, not T-117 item 4a's "⚠ makes an unverified source pass". C10
must refuse an unverified source with no route, and the triangle belongs to the value's own sources (OD-59). Item 4a
would force ⚠ on every cross-tier cell that holds any unverified source, and would admit route-less citations.
- [CONFIDENCE: medium.] The route gate is the most contestable addition. "Keeping them" (7005, 2026-11-14) is later
  than OR-23b (2026-11-13).
- **Evidence:** 4725, 6186, `tier-system.md:77`, 7053, 7273. The owner queue states that OR-23b "blocks: The engine
  change for the empty-circle rule" (`governance/owner-browser.yaml`, OR-23b), which names the engine as the route
  rule's home.
- **Falsified if:** the owner reads "keeping them … triangle" as superseding the route condition; or reads "triangle
  instead" as covering any unverified source among those that state the value.

**Claim 4.** The selection slice changes no live headline on parameters 3 or 12. It adds four T3 grey governing sources
to 3×MOB, one of which states the headline. It makes the H1 fixture state the code value. The OD-58 harm test cannot be
recorded in any existing column, so a typed relation value is the smallest home.
- [CONFIDENCE: high for the measured effects; medium that `worse_at` on `extraction_relations` beats a new small table.]
- **Evidence:** the before-and-after loop over all lens cells of parameters 3 and 12 (§0); the `extraction_relations`
  DDL definitions; `harm_finding`'s CHECK; T-059's own analysis.
- **Falsified if:** a stored record already carries "people struggle more at the more accommodating value" with a lens
  and accepts a `claim` row; or a live cell's value moves under the union.

**Claim 5.** The design_scale fix is one line. It changes both probe rows from `universal` to `population`, and no
reader takes `universal` to mean "rests on codes".
- [CONFIDENCE: high.]
- **Evidence:** `git grep -n -E 'design_scale|SCALE_UNIVERSAL' -- scripts schemas`; `sqlite_master` holds no view
  reading `design_scale`; OD-48 at 7995.
- **Falsified if:** a reader (code, view, render contract, or `governance/pipeline-contract.yaml:322` "ready to present
  per audience") reads `universal` as the regulatory-only basis.

[UNVERIFIED] items:
- The exact `run_checks` result accessor for T117-07.
- Whether `correct-source` will write `standard_number` for an unretrievable source.
- The after-state of the route gate, which was reasoned, not executed.
- The size figures, which are reasoned.

## Summary
PR B part 1 is one engine function, one migration and the C10 rewrite.

**(I)** `band()` follows the owner's table, and the regulatory override goes. The value carries its own sources' marker
(OD-59), with ⚠ for grey or unverified, and the CHECK widens to four glyphs. T-117's ● clause contradicts OR-22b and is
dropped. C10 refuses only an unverified source with no route (OR-23, OR-23b); the engine excludes those sources.

**(II)** Every tier is eligible, and a `worse_at` relation keeps the OD-58 harm test.

**(III)** `design_scale` is `population` whenever an identity is keyed.

On scratch copies today, both probe rows fail C10, and the CHECK refuses ⚠. After the change, the simulation and
reasoning give 3×MOB and 12×MOB keeping their values, marked `○`, with C10 passing. Thin is not decided (Q3). Four new
owner questions remain (Q-B2 to Q-B5).

File: /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/prb-design-1.md
