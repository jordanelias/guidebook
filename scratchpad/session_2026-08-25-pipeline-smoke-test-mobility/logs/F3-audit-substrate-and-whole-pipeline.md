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
