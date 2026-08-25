# F3 — READ-ONLY DOCTRINAL AUDIT: SUBSTRATE, CROSS-STAGE CONTRACT, AND THE PIPELINE AS A WHOLE

Agent: F3 (substrate + whole-pipeline auditor). Date: 2026-08-25.
Method: full read of CLAUDE.md, DR-2026-08-19 (instrument, incl. §12), pipeline-contract.yaml,
pipeline-map.yaml, mission/decision-protocol, PROTOCOL.md, and all seven logs (S1–S6,
OPUS-runbook-drift); independent re-derivation of every prioritised claim against the live repo,
read-only (`file:data/guidebook.db?mode=ro`). No file modified except this one.
sha256(data/guidebook.db) at audit time: 30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf
(matches every agent's recorded start/end hash).

---

## A. SUBSTRATE CONSEQUENCE ANALYSIS

CLAUDE.md's map is explicit: substrate is not a stage; it is the layer all five stages point into.
A substrate defect is therefore a five-stage defect. Element by element, with the mobility batch as
the test case:

**`items` (93 rows).** FOR: the design-parameter registry; one axis of every judgment cell; the
render key (93 `site/specs/` pages key on it). POINTED INTO BY: research (frame pull, instrument
§12.1 step 2), evidence (via `items.bpc_source_slug`), judgment (`specifications.item_code`),
render (spec_page, index.html, parts). WRONG ⇒ everywhere: a missing item means evidence has
nowhere to file, no cell can exist, no page can render — and a determination-bearing NAME (42/93
per instrument §1.1) contaminates research anchoring. MOBILITY STATE: all 11 named items exist and
are active (S1 §1.1, S6 §9a, independently agree); **no handrail item exists** (verified: 0 rows
matching `%handrail%`); `items.bpc_source_slug @ 'B-08'` is NULL.

**`populations` (23 rows).** FOR: the cell's second axis; FK target of
`evidence_population_match.target_population` and `specifications`. WRONG ⇒ the only judgment
engine crashes — proven live by S3 entry 4 (`PILOT_CELLS` code `NEU` not in table → ValueError).
MOBILITY: MOB/SCI/MS/LMB/MOVE all present; but 0 of the 25 live match rows target any of them.

**`slugs` (106).** FOR: research's unit of work; evidence attaches via `source_slug_links`;
synthesis keys `bpc_metadata` on slug×population. WRONG ⇒ evidence files to nowhere. MOBILITY:
5 of 6 needed slugs exist and are ACTIVE; there is no corridor-specific slug (S4 2h: no
`%corridor%` slug — E-08 rides `accessible-circulation-geometry`); B-08 has no slug at all.
`source_slug_links` covers exactly **1 of 106 slugs** (verified: COUNT(DISTINCT slug)=1).

**`terms` / `term_aliases` / `term_item_links` (88 / 2,382 / partial).** FOR: query design (R4)
and multilingual coverage (R11). WRONG ⇒ searches framed without the project's own vocabulary,
untraceably — BRK-12 stands (terms_used NULL in all live search rows; S1's own logged searches
did not populate it either, so the batch will repeat this unless instructed). MOBILITY: E-11 and
B-08 carry **zero** term links (S6 §9b) — the door-threshold searches start with no vocabulary;
BRK-11 (alias case mismatch vs `lang_jur_map`) still silently empties the runbook's own
`synonyms --language DE` form.

**`access_needs` + crossing maps (`access_need_icf`, `access_need_axis_map`, `item_axis_links`).**
FOR: the mandated ICF/access-need frame (CLAUDE.md §6). S1 §1.2 walked the full chain for all 11
items: it resolves, codes AND names. **This is the one substrate layer fully ready for the batch.**
Weak point: AX-BAL (balance — the handrail axis) is the only STUB among 9 axes touched.
`population_axis_map` remains quarantined scaffolding (owner D-1, BRK-20): it must never supply
applicability.

**`lang_jur_map` (70).** FOR: coverage denominators (`db.py coverage` derives 48 jurisdictions /
19 languages from it — correctly, S1 §3.6) and language targeting. MOBILITY: UN and ISO have 0
rows — 2 of bucket 1's 10 members have no language-authority record (S6 §9c).

**`jurisdictional_values` (109, REFERENCE-ONLY).** FOR: lead pointers to code documents, keyed to
items. UPSTREAM WRONG ⇒ research pulls leads for the wrong jurisdiction; DOWNSTREAM ⇒ a `UK`
query silently misses the 20 `GB` rows (verified: COUNT=20) and rendered jurisdiction comparisons
inherit the split. Its `jurisdiction` column is enforced by NOTHING (see B.2). GOOD: 29 rows
already sit on mobility items (E-01×7, E-03×8, E-08×7, G-04×7 — OPUS PART 2), doctrinally clean
(value columns 0/109 non-null).

**`decisions` (163, register stops at D-0163) + 61 DR files.** FOR: authority and supersession.
S6 #29: 51 of 61 DRs have no register row — the authority layer is majority-unindexed, which is
how paperwork gets argued against rulings (CLAUDE.md §0). MOBILITY-RELEVANT OPEN: OD-A/B/C gate
ANY determination (instrument §3 step 4a: "Nothing in step 5 can be authored until OD-A, OD-B and
OD-C are answered"); OD-G gates the GB fix; OD-2 (bucket ratification) is not visibly signed.

**`data_migrations` + the write path.** FOR: the only lawful mutation channel. STATE: proven
end-to-end on a mobility-shaped batch (S6 §2: add-locator → add-jurisdictional-value →
emit_batch_sql → emit_data_migration → migrate_db on a throwaway; reproducibility 7/7 shallow —
re-run by me, PASS — and 66/66 deep with the 2 DR-exempt tables). This is the healthiest thing in
the repository. Its one mechanical hole is D-14 (is_canonical unwired — see B.8), which is a hole
in the *guarantee*, not in the path.

**`schemas/enums.py`.** FOR: the canonical vocabulary home. `JurisdictionCode` is missing
UN, ES, PT, FI (verified: 27 members) — and nothing on the write path consumes it, so it fails
OPEN, not closed. The substrate defect that is most literally a five-stage defect: a mis-coded
jurisdiction written today propagates into search logs (R12), `jurisdictional_values`, synthesis
prose and rendered comparison tables, and no gate at any stage reads the value.

---

## B. VERIFICATION VERDICTS (each independently re-derived)

1. **`JurisdictionCode` omits UN/ES/PT/FI — CONFIRMED.** Ran the enum: 27 members; all four
   absent. `schemas/enums.py:140-178`. ADDENDUM, against OPUS D-5: its consequence clause — "the
   write would be refused (or, worse, coerced) at the point of admission" — is **REFUTED**. No code
   path connects this enum to any writer (B.2): `add-jurisdictional-value --jurisdiction ES`
   succeeds silently (S6 §2f/8a proved it on scratch). The blocker is not a refusal; it is a silent
   mis-write. Worse than D-5 says, and differently.
2. **`insert_jurisdictional_value` makes zero vocab calls on `jurisdiction`; 20 live GB rows;
   `validate_jurisdiction.py` never opens the DB — CONFIRMED.** Read `scripts/db.py:2363-2400`
   in full: existence check on item_code, tier band, R3 — no jurisdiction check. All `check_vocab`
   call sites in db.py: 2284, 2287, 2325, 2412, 2414, 2505 — none for this column.
   `SELECT COUNT(*) ... WHERE jurisdiction='GB'` = 20. `grep sqlite3|connect|guidebook.db
   scripts/validate_jurisdiction.py` = zero hits. OPUS D-6's "EXAMINED: 111 of the wrong subject"
   framing is exact and is the sharpest formulation in the seven logs.
3. **Write path works on scratch; emit captures UPDATEs and refuses DELETE; deep reproducibility
   66/66 — CONFIRMED.** Code: `emit_batch_sql.py:124-151` (column-level UPDATE diff; missing-row
   `sys.exit` refusal, never a DELETE). S6 §2e exercised all three branches empirically. I re-ran
   the shallow reproducibility audit: PASS; S6 recorded `--deep` EXAMINED: 66 with
   `evidence_source_authors`/`pipeline_runs` EXEMPT per DR-2026-05-28.
4. **`--changed-from` does not run the selftest; `preflight.sh` does — CONFIRMED.**
   `run_checks.py:395-396` (`if args.selftest: return selftest(reg)`) vs `:432` (`elif
   args.changed_from`) — disjoint branches; `preflight.sh:80-81` runs `--selftest || exit 1` first.
5. **`doctrine_recheck --cross-ref` never runs the drift pass — CONFIRMED.**
   `doctrine_recheck.py:332-338`: passes 2.4 (drift) and 2.5 (register) run only when
   `--cross-ref` is ABSENT; the registered form (`check-registry.yaml:800`) passes it. The 3
   vanished governance docs (co1-operational, evidence-methodology, population-taxonomy) are S6
   §7a's live run of bare mode; I verified the code path, not the run (bare mode may write a
   snapshot; out of read-only bounds). The registered check structurally cannot see the loss class
   its own name promises to catch.
6. **`pipeline_contract_audit` under-reports by one; honest map 13 V / 6 I / 0 B — CONFIRMED.**
   I ran both tools in parallel: the audit prints 14 VERIFIABLE / 5 INCOMPLETE / 0 BROKEN;
   `run_checks --selftest` C7 prints 5 unclaimed criteria including
   `cross_stage/attestation-doctrine-binding`, which the audit counts VERIFIABLE (file-granularity
   blind spot its own registry comment at `check-registry.yaml:942` admits). Union of uncovered = 6
   (discovery-provenance, derivation-handshake, convergence-independence, opus-routing,
   render-freshness, attestation-doctrine-binding); intersection-verifiable = 13. Caveat, stated:
   "13" requires demanding BOTH a registered file AND a live `basis:` claim — the correct standard.
7. **Attestation free text is never read for meaning — CONFIRMED.**
   `adherence_log_audit.py:342-378` (SequenceMatcher near-duplicate ratio on bias_direction /
   counterclaim), `:458-480` (verdict↔structure consistency); schema enforces minLength 30/20/10.
   Nothing parses content for truth. S6 §10c and S4 7e agree; code settles it.
8. **D-14 `is_canonical()` — CONFIRMED in every particular.** Callers: `dbcore.py:438-439`
   (its own selftest) and nothing else (grep). `connect()` (`dbcore.py:83+`) never calls it;
   `db_path()` (`:51-59`) defaults to the canonical file when GUIDEBOOK_DB_PATH is unset.
   Skills instructing the canonical path on WRITE commands: `connection-auditor_SKILL.md:185,192`
   (update-connection), `:199` (add-gap); `connection-discovery_SKILL.md:219` (add-connection).
   The instrument's own failure-mode #1 (§12.4) names this exact sequence and offers discipline
   plus a post-hoc checksum where a written-and-unwired mechanical refusal exists.

**B-list extras.** Attestation gate caught this session's own omission — CONFIRMED (S6 §1c:
blocking FAIL naming the missing `attestations/sessions_session_2026-08-25-...json`; OPUS PART 4:
CI red on `d4042e6`; the attestation now exists and validates, S6 §10b). `db.py log-search`
count-mismatch refusal — CONFIRMED in code (`db.py:370-382`, `:1025` repeatable
`--admitted-ref-id`).

**OPUS-runbook-drift, audited adversarially (the log I was told to attack):**
- **D-1 CONFIRMED.** `scripts/audit/table_connectivity.py` absent; deleted in `80a34d1` (the
  2026-08-20 cull); instrument line 794 still commands it as Step 0's fifth command, unannotated.
- **D-2 CONFIRMED.** `db.py:394-396` ("admitted_ref_ids intentionally NOT written — …owner ruling
  2026-08-24"); `test_db_integrity.py:996-998` ("H03/H04 DELETED 2026-08-24"); `log-search` takes
  repeatable `--admitted-ref-id` with count/duplicate refusals. Instrument §12.1 step 7 (lines
  856-864) still instructs the abolished dual write and cites the two deleted checks as blocking.
- **D-3 CONFIRMED** (instrument line 830 "No CLI; scratch SQL" vs the live `add-candidate`, S1
  §4.2-4.4). **D-4 CONFIRMED** (no `update-search`/`update-execution` subcommand exists; R8's
  log-before-screen then update-counts flow has no sanctioned writer).
- **D-5: core CONFIRMED, consequence clause REFUTED** (see B.1). Note the OPUS/S6 disagreement on
  governance weight: decision-protocol.md:73-77 item 4 makes jurisdiction inclusion always DG-NON,
  so S6's "nowhere near doctrine-weight" UNDERSTATES it and OPUS's classification is right — but
  the owner's own live statement ("our first two defined research buckets") arguably already made
  the decision; the correct act under CLAUDE.md §0.0 is to record that supersession, not to reopen
  the question.
- **D-8 CONFIRMED exactly** (my re-derivation: 138 mined DOIs, 4 in `source_locators`, 134
  stranded). **D-10 CONFIRMED exactly** (272 distinct mobility DOIs in the two B11 artifacts, 16 in
  the clue store, 0 admitted, 256 NEW).
- **D-9 CONFIRMED textually and empirically.** §2.2 froze "until … at least one admitted source
  with a complete walk"; §5 released "the moment evidence_sources is non-empty"; §2.5's correction
  records the enforcer implementing the weaker clause. Live: evidence_sources=10;
  specifications, source_value_extractions, bpc_metadata, item_bpc_links, convergence_assessment
  all 0. Ten sources, zero complete walks. The freeze released on a row count §4 was written to
  reject.
- **D-11 mechanism CONFIRMED** (adherence_log_audit default `base="HEAD~1"`; registry cmd passes no
  base; S4 7d independently proved `--changed-from HEAD~10` changes nothing). The three-species
  vacuity taxonomy (empty subject / wrong subject / wrong window) is the best analytical
  contribution in the seven logs and should outlive this session.
- **D-12: the withdrawal is sound and properly done.** `directness.py:225` (`in (POP_EXACT, None)`)
  is a real latent hazard; `assess_cell.py:191-195` G2 does neutralise it; the surviving finding —
  `anchoring()` at `assess_cell.py:248-250` admits COND_DOWN_WEIGHTED, so never-assessed and
  assessed-partial anchor identically — is CONFIRMED and correctly classified as DG-NON doctrine.
- **D-16 CONFIRMED by recount:** 11 distinct REF-ids; 3 admitted (00325/00561/00578); **8**
  lead-only (00335/00571/00576/00577/00580/00589/00726/00727). OPUS's correction of S4 is right;
  S4's prose said "7 of 11" while S4's own table already showed 8 — an internal inconsistency in
  S4, caught properly.
- **Residual criticism of OPUS:** (i) D-5's refusal claim (above); (ii) PART 3's "highest-value
  pre-batch action" (promote 256 leads) is stated without pricing the OD-5 writer-half interaction
  it itself names in D-15 — promoting leads BEFORE fixing `add-source`'s single-table dedup
  *increases* the duplicate-identity risk 25-fold; ordering matters and PART 6 knows it, PART 3
  doesn't say it; (iii) OPUS never cites `references/project-standards.md:638-641`, the standing
  rule that governs whether this whole exercise was lawful — the most consequential omission in
  its own remit (see C4).

---

## C. THE WHOLE-PIPELINE READING

### C1. Where the walk actually stops — and empty data vs unbuilt wiring, per stage

Read across all six traces, a unit of mobility work proceeds like this on the scratch: frame pull
(works, S1 §1) → `log-search` (works) → `add-candidate` screen/stage with R15 (works) →
`add-source` admission + slug link + authors (works; S2 admitted a real ramp-slope T1 source) →
`add-population-match` (works, cross-session dissent works) → `log-mining` (works). The first
friction is that the honest admission immediately fails the blocking gate `test_db_integrity` I1
(`verification_disposition` unsettable) and `adjudication_integrity` tier derivation (`scope`
unsettable) — wiring, two missing flags. **The hard stop is the evidence→judgment hinge:**
`source_value_extractions` (5 readers, 0 writers — S2 PART 10) and `specifications` (no CLI, and
the only engine, `assess_cell.py`, is hardcoded to 7 pilot cells and crashes twice against the
live DB — S3 entries 1-5). Nothing downstream of population grading can be reached through any
sanctioned instrument. Table:

| Stage | Blocked by | Verdict with PERFECT upstream data |
|---|---|---|
| research | works today; convenience wiring absent (lead selector, mining client, R8 count-update path) | runs |
| evidence-collection | **wiring, small**: `--scope`, `--verification-disposition`, `--evidence-type choices=`, Co-1 provenance flags, OD-5 writer-half dedup | admission lands but **fails its own blocking gate** — fails |
| judgment | **wiring, structural**: no writer for `specifications`/`source_value_extractions`/`specification_source_links`; engine broken (gap-id format, dead population code) + empty data (`source_slug_links` = 1 slug, 0 mobility) | **still fails** — no instrument can target the cell |
| synthesis | **wiring, structural**: `update-bpc` INSERT branch crashes on every first row (no `--population`); no `reasoning_doc_citations` writer; the contract's anchor table `best_practice_synthesis` does not exist in the schema | **still fails** — first write crashes |
| render | **empty data** (honest "not yet computed" banner; `generate_parts --mode full` refuses correctly) + one wiring defect that fires exactly when data arrives: `specification_source_links` has no writer, so a determination renders with zero citations (S3 entry 23) | renders — but citation-less, and parts//index.html stay stale (no regenerator covers them) |
| substrate | works (write path + reproducibility proven); gaps are CONTENT: handrail item, B-08 slug, 4 enum codes, UN/ISO lang rows, 20 GB rows — plus one small wiring gap (no jurisdiction vocab call in the writer) | runs |

The single most decision-relevant sentence: **evidence-collection's blockers are flag-sized;
judgment's and synthesis's are structural; render's are data-shaped except the citation join.**
"Run the batch" fixes none of the wiring column; building the wiring column fixes nothing in the
data column. Both claims are proven in the traces, not asserted.

### C2. Re-entrancy

The 2026-08-21 finding holds, and the traces split it: **the artefact layer is re-entrant, the
process layer is single-pass.** Re-entrant by design: `emit_batch_sql` diffs UPDATEs against
canonical (a batch may revisit rows it already shipped — S6 §2e proved it); an admitted source
lawfully writes substrate (jurisdictional refs, terms); mining re-enters admission. Single-pass in
fact: `sessions/LATEST` updates only at close-out, so this very session misfiled 664 command-log
lines into the 2026-08-23 session's directory (S6 §6c — the staleness bug was relocated, not
fixed); the attestation gate's window is one commit regardless of the range under review (D-11);
`assess_cell` hardcodes its cells; CLAUDE.md's §5 numbers went stale within the same day (36
commits, S6 §1c); the freeze cannot re-arm (D-9). A second mobility batch six weeks later finds:
its opening commands filed under THIS session; parts/ and index.html further stale with no gate;
the OD-5 writer half still minting duplicate identities against a clue store 25× larger; the
runbook still teaching the abolished dual write unless the D-1..D-4 edits land; three vanished
governance docs still undetected because the registered doctrine check still cannot look; and 51
of 61 DRs still unindexed. The pipeline can be re-entered; the *instrumentation* assumes it never is.

### C3. The apparatus/deliverable ratio — derived live, per CLAUDE.md §1

```
63 checks; 4 quarantined            (governance/check-registry.yaml)
30,494 executable LOC               (scripts/ + tools/, .py+.sh, ex-__pycache__)
 5,837 of those LOC generate output (scripts/generate/* + generate_parts.py + tools/*.py ≈ 19%)
Deliverable: 10 evidence_sources · 0 specifications · 875 leads · 1 reasoning doc · §4 criterion UNMET
```
≈3,000 executable LOC per admitted source; apparatus-per-determination is division by zero.

Which pattern dominates? **Split by layer, not globally.** The write-time refusal layer earned its
keep in these traces: attestation_presence caught this session's real omission (blocking, then CI);
emit_batch_sql refused a DELETE; log-search refuses count mismatches; R15/R3/R9 vocab and FK
refusals fired correctly dozens of times across S1/S2/S6; validate_evidence_state fired 7/7
injected violations; pmp_audit caught 3/3; test_db_integrity caught 4/4 including the organic I1.
The post-hoc audit layer is where wrong-subject/vacuous concentrates: validate_jurisdiction
(blocking, 111 wrong subjects), doctrine_recheck --cross-ref (registered form skips its own drift
pass), 8 NOTHING-IN-SCOPE of 63 with 4 blocking-and-vacuous, register_integrity's misleading
"(DB cross-check on)" label, validate_reasoning's exit-0-on-missing-doc, the contract audit's
false-VERIFIABLE, reasoning_doc_citations_audit's phantom CHECK 8.

REMOVE, with evidence (deleting is as cheap as adding; removal needs evidence, not permission):
1. `scripts/generate/room_page.py` — queries two nonexistent tables, unwired from registry, CI and
   `regenerate_derived.sh`; crash-on-contact (S5 e8, S4 8d). Git is the archive. Delete.
2. `requirements.txt` — a disagreeing second home for the dependency list the registry owns
   (S6 §1b; CLAUDE.md §5 already documents the drift). Delete or reduce to a pointer.
3. The `--cross-ref` flag in `check-registry.yaml:800` — one-token removal makes the registered
   doctrine check run the drift pass that, run bare, found 3 vanished governance docs. (Removal of
   a flag, not addition of a check.)
4. `assess_cell.py`'s PILOT_CELLS engine — self-described one-time pilot, broken two ways against
   the live DB, cannot target any mobility cell; keeping it misleads. Delete when (not before) the
   general judgment writer replaces it.
5. The quarantine limbo — 4 registered-never-selected entries; `code_currency_audit` passes clean
   standalone (S6 #32) while `adjudication_integrity` — quarantined — caught two of this smoke
   test's real defects. Re-register the second, delete the rest. An unregistered check is the
   defect class §1 names.
6. `validate_jurisdiction`'s BLOCKING status under its current name — not deletion but rescoping:
   its real subject is a markdown registry; the DB half belongs in the writer (one `check_vocab`
   call). A blocking check whose name promises the DB and whose subject is prose is apparatus that
   examines the wrong thing at the project's most doctrinally sensitive column.

### C4. Is this smoke test itself the pathology? Ruled on, both halves, unsoftened.

**Does it violate the freeze? No — the freeze is spent.** §2.2's freeze expired by §5's own terms
at `evidence_sources ≥ 1` (live: 10); `meta_work_freeze` was retired SPENT the same day it fired.
D-9's finding stands and matters: it expired on the *weaker* of the instrument's own two release
conditions, so its expiry proves nothing about readiness — but expired is expired.

**Does it violate operative doctrine? In letter, yes.** `references/project-standards.md:638-641`
is a standing owner-directed RULE, not a freeze clause: *"An adversarial pass may be commissioned
ONLY against a diff that (a) wrote rows to the research tables … or (b) authored or amended a
synthesis artifact. Plans, critiques, censuses, handoffs, registers, session records, Decision
Records and this ledger are not adversarial-pass subjects… If it fails, decline in one line of the
session log; no critique document may be written… Budget: at most one adversarial pass per
research batch. A pass on a pass is forbidden."* This session's subject is the apparatus, not a
data or synthesis diff; it wrote seven critique documents plus three audits of the critiques —
and this F3 document, an audit of OPUS's audit, is literally the forbidden pass-on-a-pass. **The
only thing that makes the session lawful is CLAUDE.md §0.0:** the owner commissioned it (the
session record, committed before the run, states its purpose and deliverable), and a live owner
statement supersedes the standing rule on contact. The correct act — which none of the seven logs
performed, because none of them cites project-standards:638 at all — is to RECORD that
supersession once, in the session record, rather than leave a ratified rule silently contradicted
by the owner's own commissioned work. That record is owed and cheap.

**Separately: is it worth it? Yes — once, narrowly, and only if it is spent.** The honest
accounting: ~6,400 lines of audit, zero determinations, zero canonical rows, §4's acceptance
criterion untouched. Against that: it found, before the batch could, the four first-write crashes
on the DOCUMENTED path (`--scope`, I1 disposition, `update-bpc` population, `--dry-run --slug`),
the structural absence of the entire judgment hinge, the unwired canonical-DB guard, and a
ratified runbook that still commands a deleted script and an abolished dual write. Every one of
those, hit mid-batch, produces exactly the hand-SQL workaround that CLAUDE.md §4 names as the
2026-08-19 fabrication's entry point — the repository has already run the counterfactual once, and
it produced invented co-authors past six green gates. The value is real and it is fully captured
by one code PR plus one owner sitting. **A second smoke test would be the loop wearing a lab
coat.** And the instrument's deeper lesson stands against the test's own genre: batches 1–2 ran
and the walks are still incomplete (D-9) — neither audits NOR row counts satisfy §4; only a
rendered, readable answered question does, and this session did not move that criterion by one
line.

### C5. What must happen before the mobility batch, in order

**(ii) FIRST — one owner sitting (DG-NON, gates everything below):**
1. OD-A / OD-B / OD-C — instrument §3 step 4a says in bold that nothing in step 5 (a
   determination) can be authored until these are answered. They are the true head of the queue.
2. OD-G (GB→UK, 20 rows) — fix rows and wire the enforcer in the same change, per §3 item 6c.
3. Jurisdiction set: confirm buckets 1–2 as ratified (OD-2) and the four enum members
   (UN/ES/PT/FI) — DG-NON per decision-protocol §2.4(4); the owner's bucket statement likely
   already decides it; record, do not relitigate.
4. Handrail item + slug; B-08 slug — topic/work-product inclusion (§1.4: slug authored from the
   ICF frame, item list consulted for coverage only).
5. D-12's doctrine question: may a source whose population applicability was never assessed anchor
   a `stated` cell? (assess_cell.py:248-250 currently says yes, silently.)
6. Scope ruling for batch 1: does it END at admission+grading+mining, or reach a determination?
   If the latter, item (i).6 below stops being optional.

**(i) THEN — one code PR, no permission needed (evidence = these seven logs):**
1. `add-source`: add `--scope`, `--verification-disposition` (default CLOSED when VERIFIED),
   `--evidence-type choices=` (copy `db.py:1223`), `--co1-provenance`/`--co1-source-type`; make
   its DOI dedup query both ref_id homes (mirror `add-locator`, `db.py:2513-2521`); fix the
   `--dry-run --slug` crash. (S2 blockers 1-5, 8.)
2. `update-bpc --population` (fix the INSERT branch, S4 2h).
3. Wire `is_canonical()` into `dbcore.connect()` as a write-refusal; fix
   `connection-auditor_SKILL.md:185,192,199` and `connection-discovery_SKILL.md:219`. (D-14.)
4. `insert_jurisdictional_value`: `check_vocab` against `JurisdictionCode` (after sitting item 3).
5. Instrument edits at lines 794, 830, 856-864 (+ record D-4); give R8's two-phase flow a writer
   (extend `log-search` or add `update-search`). The registry one-token `--cross-ref` removal and
   the D-11 base-threading (one registry line) ride along — both already bit this session.
6. IF the owner rules batch 1 reaches a determination: minimal judgment writers —
   `add-extraction` (`source_value_extractions`), a general `specifications` writer with
   `specification_source_links`, replacing the pilot engine. This is the largest item and the only
   one that is genuinely new construction; it is also what §4's acceptance criterion requires.
7. The promotion migration: 256 mobility leads → `source_locators` (DOI/year/first-author only,
   title NULL pending R10) — AFTER (i).1's dedup fix lands, never before (the ordering PART 3
   omits and PART 6 proves).

**(iii) DEFERRED until after batch 1 — ruthlessly:** all three comparative-analysis tools (S4
Q1-Q3); `opus_reviewed` enforcement and the build_part05 filter; conflicts→judgment wiring;
freshness gates for parts//index.html/populations/rooms (regenerate by hand once, post-batch);
`pipeline_contract_audit` granularity fix; `next_gap_id` scheme fix; `deferred_reason ''`
coercion; the clue-store read CLI (reads may be ad-hoc SQL — only writes are gated); the
Crossref/OpenAlex/Semantic-Scholar mining clients (batch 1 mines by hand through
`retrieval_log.fetch()` exactly as batches 1–2 did — one instruction line, not code); UN/ISO
`lang_jur_map` rows unless a UN/ISO search is actually in batch 1's plan; every skill-prose
cleanup not named in (i). Each of these fails CLAUDE.md §1's test — no wrong thing reaches the
GUIDEBOOK in batch 1 if they do not exist.

### C6. The strongest objection to the smoke test's own conclusions — made forcefully

*"This is the ten adversarial passes of July–August again, wearing instrumentation. Six agents and
~6,400 lines examined apparatus and produced zero rows; the standing rule at
project-standards:638 forbids the exercise outright; half the 'blockers' are first-use artifacts
any system exhibits before first use; the instrument's own §3 proved the method — 'running the
batch first is what made the later schema work safe' — so the batch, not the audit, is the test;
and the surest prediction available is that these seven logs will now spawn apparatus commits,
which is the disease presenting as the diagnosis."*

**Ruling: it holds on form, and on roughly half the substance — and it collapses exactly where
the audit's own distinction lands.** It holds: the session is out-of-form under the standing rule
(C4); the (iii) list above exists because the logs do over-propose; nobody derived the §1 ratio or
priced their ABSENT-lists against §1's burden of proof. It collapses: "the batch is the test" was
already run — batch 1 (2026-08-19) hit the write-path gaps mid-flight and the workaround produced
five fabricated author lists past six green gates; the wiring-column defects found here
(update-bpc crash, scope/I1, no judgment writer) are precisely the class the batch does NOT fix
but routes around, by hand-SQL, at the moment of maximum pressure. For the empty-data column the
objection is right and the deferral list honours it. For the unbuilt-wiring column it is wrong,
and the empty-data/unbuilt-wiring split in C1 is the audit's answer to its own strongest critic.

---

## D. WHAT ALL SEVEN LOGS MISSED, COLLECTIVELY

1. **Nobody asked whether any blocking check is actually REQUIRED on the merge path.** OD-9
   ("Required-check set on `main`… wire AFTER the batch — approved in principle") is recorded and,
   as far as any log shows, unwired. Unverifiable from this container (no `gh`), but the question
   was never even raised — and if no check is required on `main`, every "blocking" verdict in all
   seven logs describes preflight discipline, not enforcement. The repo's entire real access
   control (OD-9's own words) went unexamined by an exercise devoted to gates.
2. **Concurrency and the committed binary blob.** Six agents raced one worktree (S6 §3d watched
   HEAD move mid-run) and nobody asked what two research sessions do to `data/guidebook.db` — an
   unmergeable binary whose every batch moves the sha — or to migration filename/number
   allocation, whose "sole allocator" (instrument §B) is a prose table in a superseded workplan.
   The smoke test WAS the experiment and never read its own result. Batch scale-out (OD-2's whole
   subject) hits this first.
3. **Nobody read the rule that governs the session itself.** `references/project-standards.md:638`
   (adversarial passes bound to data/synthesis diffs; pass-on-a-pass forbidden) is uncited by all
   seven logs including OPUS's freeze analysis — the sharpest available instance of the
   repository's signature failure (a ruling in the record, invisible to the search), reproduced by
   the very exercise built to catch that class. Corollary miss: no log priced its own ABSENT-list
   against CLAUDE.md §1's burden of proof, and none derived the §1 ratio this audit derives in C3.

Minor collective gaps, recorded without elaboration: `terms_used` was left NULL by S1's own logged
searches (BRK-12 will recur in batch 1 unless the runbook's `--terms-used` is made a habit); no
log tested `generate_parts --mode full`'s boundary predicate with exactly one `specifications`
row (S5 flagged this itself); and no one checked whether the 96 schema-valid attestations include
any whose free text is wrong — the one reader that could, per S6 §10c, is a human, and none of the
seven agents was tasked to be it.

— End of F3 audit. sha256(data/guidebook.db) re-verified unchanged at close:
30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf
