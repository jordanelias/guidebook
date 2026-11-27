# impl-prb-iv: `amend-search --set-deferred-reason` (PR B, piece IV), tests first

Implementer log, 2026-11-27. Branch ccr-64231823-gqy3xr at 807e7c8c. Tooling only (rule 10): no row, no migration,
nothing run on the canonical database. `sha256sum data/guidebook.db` was 3d419efb…edb9 at start and at end.
Nothing committed, staged or stashed.

## 0. Facts re-verified before any edit (canonical, read-only)

- `python3 scripts/db.py amend-search --help | grep -c deferred` printed 0: no deferred-reason flag.
- Rows 87, 133, 138, 191: slug accessible-circulation-geometry, results_found 0, absence_class NULL, deferred_reason NULL.
- `PRAGMA table_info(search_executions)`: `deferred_reason TEXT`, nullable, no default; no trigger names the table
  (`select count(*) from sqlite_master where type='trigger' and sql like '%search_executions%'` gave 0). No migration needed.
- `--set-absence-class genuine_absence` on exec 9 (deferred) on a scratch copy: rc 0, row after `(9, 0, 'genuine_absence', 1)`.
- No zero-result row has a search_admissions edge today (count 0), so D9's case is built by HAND in the test.

## 1. RED (tests written first; full output: scratchpad/impl-iv-red.txt)

New section T081A-01..04 in scripts/tests/test_run_pipeline_refusals.py, placed after T080. Rows are chosen by query
on scratch copies; the admission edge is HAND / TASK-FIXTURE. T081A-01/02 are gated by a signature probe (red by name);
T081A-03 is not gated and calls the existing flag, so it fails on the real defect.

```
Section T081A: a search logged as run whose request returned no result list is amended to deferred (OD-45)
  [✗] T081A-01: amend-search --set-deferred-reason sets the reason and moves the row from examined_empty to deferred
      feature absent: amend_search(set_deferred_reason=...)
  [✗] T081A-02: --set-deferred-reason refuses a blank reason, a found, classed, already-deferred or admitting row, and both flags in one call, writing nothing
      feature absent: amend_search(set_deferred_reason=...)
  [✗] T081A-03: --set-absence-class refuses a row already deferred (it says the search was not run) and writes nothing
      (None, ('DELIBERATELY NOT SEARCHED this batch. AX-PAI (ICF b280, sensation of pain) carries 2 of the 13 items on this slug, and its axis mechanism is impact, vibration, pressure and cold - a structure-borne and tactile demand, not an airborne room-acoustic one. Searching it under this slug would have imported the wrong mechanism. It needs its own frame and belongs with a vibration/structure-borne 
  [✗] T081A-04: through the CLI, amend-search --help lists --set-deferred-reason and a blank reason is refused with the REFUSING prefix
      (2, 'ined,log-search,add-source,add-conflict,update-conflict,conflicts,delete-connection,add-supersession-check,add-gap-mining,update-gap-addressability,unmined-gaps,request-translation,record-translation,review-translation,translations} ...\ndb.py: error: unrecognized arguments: --set-deferred-reason   \n')
Section T073: a fixture retrieval root leaves out a folder filed under an id the database has not minted
EXAMINED: 604 cases
SKIPPED-NO-FIXTURE: 1
FAILED: 4
```
T081A-03's detail line was truncated at 400 characters before it reached `absence_class`; I changed its detail to print
`absence_class after the call` and proved the defect separately on a scratch copy (exec 9: rc 0, `(9, 0, 'genuine_absence', 1)`).

## 2. Implementation (scripts/db.py only)

- `amend_search`: new parameter `set_deferred_reason`; SELECT reads `deferred_reason`; `any_setter` counts it.
- Converse refusal in the `--set-absence-class` block: refused when the row is deferred or `--set-deferred-reason` is in
  the same call.
- New block: refuses blank; already deferred (write-once); results_found > 0 or any search_admissions edge (D9; retired
  edges included, since a retired admission still means the search ran); an absence class. Writes the column and a
  `|| CORRECTED <date>: deferred_reason set …` trail; returns `deferred_reason` in the result.
- argparse `--set-deferred-reason`; dispatch; `p_am` help and the docstring now say the verb sets typed columns;
  `--set-absence-class` help says "or is deferred".
- Stale `log_search` comment ("amend-search writes only findings_note and harm_finding") now says what its argument
  needs: amend-search cannot write prior_expectation.
- What reads it: T-081's research batch writes it; cell_status, v_deferred_acts, coverage --slug, the v_coverage_* views
  and research_batch_dod R8/R14 read the column. Nothing became dead.

`git diff --stat` (tooling files only):
```
 scripts/db.py                                      | 66 ++++++++++++++---
 scripts/tests/test_run_pipeline_refusals.py        | 84 ++++++++++++++++++++++
 skills/research-log-manager_SKILL.md               |  5 ++
 skills/run-pipeline_SKILL.md                       |  5 +-
 .../tasks/T-081-classify-zero-result-searches.md   | 10 +--
 5 files changed, 153 insertions(+), 17 deletions(-)
```

The db.py diff:
```diff
diff --git a/scripts/db.py b/scripts/db.py
index b630e4e0..9c6c3900 100644
--- a/scripts/db.py
+++ b/scripts/db.py
@@ -904,8 +904,8 @@ def log_search(slug: str, language: str, query_text: str, engine: str,
     # R8 says log every query WITH the prior written before you run it. A flag that
     # is merely available is not that rule: batch 05 logged 43 searches and CHECK 7
     # reports 9 verified citations with no prior, permanently, because
-    # search_executions is append-only (R8) and `amend-search` writes only
-    # findings_note and harm_finding -- so those nine can never be cleared by any
+    # search_executions is append-only (R8) and `amend-search` cannot write
+    # prior_expectation -- so those nine can never be cleared by any
     # sanctioned path. The check went red forever, and a check that is red forever
     # is one its reader learns to skip: exactly the cry-wolf failure this session
     # fixed in the fidelity checker and then rebuilt here. Refusing at the writer is
@@ -1905,7 +1905,8 @@ def main():
     p_cs.add_argument("--dry-run", action="store_true")
 
     p_am = sub.add_parser("amend-search",
-                          help="APPEND a dated correction to a logged search's findings_note")
+                          help="APPEND a dated correction to a logged search's findings_note, and "
+                               "set the typed columns its flags name")
     p_am.add_argument("--exec-id", required=True, type=int)
     p_am.add_argument("--append-note", required=True, dest="append_note",
                       help="Appended after a '|| CORRECTED <date>:' marker. The existing "
@@ -1934,7 +1935,12 @@ def main():
     p_am.add_argument("--set-absence-class",
                       choices=dbcore.schema_choices("search_executions", "absence_class"),
                       help="R14: classify a zero-yield search (query-shape failure / wrong index / "
-                           "genuine absence). Write-once; refused when the search found anything.")
+                           "genuine absence). Write-once; refused when the search found anything or is deferred.")
+    p_am.add_argument("--set-deferred-reason",
+                      help="OD-45: a search logged as run whose request returned no result list (blocked, "
+                           "rate-limited, reset, a stub page) was not run. Records the failure in deferred_reason "
+                           "(free text; the column has no CHECK). Write-once; refused when the search found or "
+                           "admitted anything or carries an absence class.")
     p_am.add_argument("--set-harm-finding", action="store_true",
                       help="Raise harm_finding 0 -> 1. R7 makes harm first-class, so a "
                            "search logged with the flag down that did surface harm has an "
@@ -3917,7 +3923,8 @@ def main():
                            set_origin_pass_id=args.set_origin_pass_id,
                            add_result_artefacts=args.add_result_artefacts,
                            clear_target=args.clear_target,
-                           set_absence_class=args.set_absence_class))
+                           set_absence_class=args.set_absence_class,
+                           set_deferred_reason=args.set_deferred_reason))
 
     elif args.command == "amend-gap":
         # _emit, not a bare assignment: until 2026-09-25 both of these assigned the
@@ -5280,8 +5287,15 @@ def amend_search(exec_id: int, note: str, session: str, dry_run: bool = False,
                  set_target_evidence_type: str = None,
                  set_origin: str = None, set_mined_ref_id: str = None,
                  set_origin_pass_id: int = None, add_result_artefacts=None,
-                 clear_target: bool = False, set_absence_class: str = None):
-    """APPEND a correction to a logged search's findings_note. Never rewrite it.
+                 clear_target: bool = False, set_absence_class: str = None,
+                 set_deferred_reason: str = None):
+    """APPEND a correction to a logged search's findings_note, and set the typed columns its flags name. Never
+    rewrite the note.
+
+    --set-deferred-reason (OD-45 ACTION (1), (2) and (4)). A search logged as run whose request returned no result
+    list (a block, a rate limit, a reset, a stub page) was not run, and every zero-result reader counts it as a search
+    that found nothing until deferred_reason says otherwise. Write-once, and refused on a row that ran: one with
+    results, an admission edge or an absence class. The re-run it is owed is a new row (R8).
 
     --clear-target (2026-09-27, exec 77 / DR-2026-09-26 5.2d). --set-origin's own
     refusal below requires target_tier/target_evidence_type/target_scope to be NULL
@@ -5318,15 +5332,16 @@ def amend_search(exec_id: int, note: str, session: str, dry_run: bool = False,
         row = conn.execute("SELECT exec_id, findings_note, harm_finding, "
                            "target_evidence_type, mining_direction, origin, "
                            "mined_ref_id, origin_pass_id, query_text, "
-                           "target_tier, target_scope, results_found, absence_class "
-                           "FROM search_executions WHERE exec_id=?", [exec_id]).fetchone()
+                           "target_tier, target_scope, results_found, absence_class, "
+                           "deferred_reason FROM search_executions WHERE exec_id=?", [exec_id]).fetchone()
         if row is None:
             raise Refusal(f"exec {exec_id}: no such search execution.")
         stamp = audit(session)
         marker = f" || CORRECTED {stamp['created_at'][:10]}: "
         any_setter = (set_harm_finding or set_target_evidence_type or set_origin
                      or set_mined_ref_id or set_origin_pass_id is not None
-                     or add_result_artefacts or clear_target or set_absence_class)
+                     or add_result_artefacts or clear_target or set_absence_class
+                     or set_deferred_reason is not None)
         duplicate = note in (row["findings_note"] or "")
         if duplicate and not any_setter:
             return {"exec_id": exec_id, "appended": False,
@@ -5505,10 +5520,39 @@ def amend_search(exec_id: int, note: str, session: str, dry_run: bool = False,
             if row["absence_class"]:
                 raise Refusal(f"exec {exec_id}: absence_class is already {row['absence_class']!r}. "
                               f"It is write-once.")
+            if row["deferred_reason"] or set_deferred_reason is not None:
+                raise Refusal(f"exec {exec_id}: deferred_reason says this search was not run, and an absence class says "
+                              f"it ran and found nothing. A row cannot assert both (OD-45): pass the one that is true, "
+                              f"and log a re-run as a new row with log-search. Nothing was written.")
             conn.execute("UPDATE search_executions SET absence_class=? WHERE exec_id=?",
                          [set_absence_class, exec_id])
             absence_set = set_absence_class
 
+        deferral_set = None
+        if set_deferred_reason is not None:
+            reason = set_deferred_reason.strip()
+            if not reason:
+                raise Refusal(f"exec {exec_id}: a blank --set-deferred-reason states no cause. Name the failure the "
+                              f"request met (a 403, a 429, a reset, a stub page). Nothing was written.")
+            if row["deferred_reason"]:
+                raise Refusal(f"exec {exec_id}: deferred_reason is already set. It is write-once; log the re-run as a "
+                              f"new row with log-search. Nothing was written.")
+            admitted = [r[0] for r in conn.execute(
+                "SELECT ref_id FROM search_admissions WHERE exec_id=? ORDER BY ref_id", [exec_id])]
+            if row["results_found"] != 0 or admitted:
+                raise Refusal(f"exec {exec_id}: results_found={row['results_found']}, search_admissions "
+                              f"{admitted or 'none'}: this search ran. deferred_reason means not run, never a findings "
+                              f"channel (R6); correct what it found with --append-note. Nothing was written.")
+            if row["absence_class"]:
+                raise Refusal(f"exec {exec_id}: absence_class is {row['absence_class']!r}: the row says it ran and found "
+                              f"nothing. A row cannot assert both (OD-45); the class is write-once, so a wrong one is "
+                              f"corrected by a compensating migration. Nothing was written.")
+            conn.execute("UPDATE search_executions SET deferred_reason=? WHERE exec_id=?", [reason, exec_id])
+            trail = f"{marker}deferred_reason set: the request returned no result list, so the search was not run (OD-45)"
+            merged = (merged or "").rstrip() + trail
+            conn.execute("UPDATE search_executions SET findings_note=? WHERE exec_id=?", [merged, exec_id])
+            deferral_set = reason
+
         raised = False
         if set_harm_finding:
             # MONOTONIC, 0 -> 1 ONLY. R7 makes failure, harm and inadequacy first-class
@@ -5536,7 +5580,7 @@ def amend_search(exec_id: int, note: str, session: str, dry_run: bool = False,
                 "origin": origin_set, "mined_ref_id": mined_ref_set,
                 "origin_pass_id": origin_pass_set, "cleared_target": cleared,
                 "result_artefacts_added": len(add_result_artefacts or []),
-                "absence_class": absence_set}
+                "absence_class": absence_set, "deferred_reason": deferral_set}
 
 
 def amend_gap(gap_id: str, note: str, session: str, dry_run: bool = False):
```

## 3. GREEN (full output: scratchpad/impl-iv-green.txt)

```
Section T081A: a search logged as run whose request returned no result list is amended to deferred (OD-45)
  [✓] T081A-01: amend-search --set-deferred-reason sets the reason and moves the row from examined_empty to deferred
  [✓] T081A-02: --set-deferred-reason refuses a blank reason, a found, classed, already-deferred or admitting row, and both flags in one call, writing nothing
  [✓] T081A-03: --set-absence-class refuses a row already deferred (it says the search was not run) and writes nothing
  [✓] T081A-04: through the CLI, amend-search --help lists --set-deferred-reason and a blank reason is refused with the REFUSING prefix
Section T073: a fixture retrieval root leaves out a folder filed under an id the database has not minted
EXAMINED: 604 cases
SKIPPED-NO-FIXTURE: 1
PASS: all 604 cases
  [-] T054-02: SKIPPED-NO-FIXTURE: fewer than three codes without live carriers
```
The one skip (T054-02) is the same in the red run, so it predates this change; the other 600 cases pass in both runs.

test_db_integrity.py: run on the working tree and on a clean `git archive HEAD` extraction (scratchpad/iv/base);
outputs identical (`diff` empty), rc 0 both, "EXAMINED: 4339 subject-inspections across 47 instrumented check(s) of 57"
(re-run rather than trust), with the same ten PASSED-HAVING-EXAMINED-NOTHING checks in both.

build_graph.py --check: rc 1 on both trees, "4 failure(s), 5 warning(s), 112 moved" in both; the only difference is
the order of two WARN lines. Pre-existing, unrelated (EVI-055/058 quotes in tier-system.md).

## 4. Prose callers swept (git grep)

- skills/run-pipeline_SKILL.md ~135-137: adds the amend path for a row already written as run.
- skills/research-log-manager_SKILL.md step 3: one paragraph for the same case.
- T-081 task file: §2 (flag added as a precondition, with its check), §4 item 1 third bullet (write the deferral with the
  flag instead of "the row is not amended here"), §6 (deferred rows leave the command's output), §8 (precondition),
  §9 (the deferral's refusals named as expected refusals).
- NOT edited: skills/citation-miner_SKILL.md:120. It is about `log-mining` (citation_mining.deferred_reason), not
  search_executions, and quotes R6 word for word ("DELIBERATELY NOT SEARCHED"). This flag does not change what it says;
  rewording it alone would make the skill disagree with the contract sentence it quotes. It should change with R6.
  research-log-manager l.170 and research_batch_dod.py:546, db.py:611/1753 carry the same phrase (same reasoning).
- Checked still true: research_protocol_audit.py:113/241 and db.py:924 ("amend-search cannot touch/write" prior_expectation).
  architecture/meta-scripts-spec.md:59 only lists the verb.
- `git grep -i -E 'no deferred.reason flag|cannot become a deferral|amend-search\` writes only'` outside transcripts and
  scratchpad: no hits left.

## 5. governance/research-contract.yaml R6 (not edited)

Hook text: "Findings go in findings_note. deferred_reason means DELIBERATELY NOT SEARCHED." The first half still holds
(the flag refuses any row that found or admitted anything, so no finding enters the column). The second half is now
visibly narrower than the practice: since OD-45 (log-search, T-080) and now this flag, deferred_reason also holds
"a request that returned no result list" (a 429, a 403, a reset), which is not deliberate. It is the same inaccuracy
log-search already had; this change widens its reach to amendments. To make it true, the word "DELIBERATELY" would
change to something like "NOT RUN (declined, or the request returned no result list; OD-45)". That edit touches the
blocking research_contract_sync check and the SessionStart hook injection, and the same phrase is repeated in
citation-miner l.120, research-log-manager l.170, research_batch_dod.py:546 (R6 message), db.py:611 and the
--deferred-reason help at db.py:1753, plus the DDL comment "non-NULL => deliberate no-search" (schema migration).
Left for the coordinator / owner.

## 6. The write path on a scratch copy (scratchpad/iv/s6.db, s7.db)

- One row (exec 87, s7.db): `emit_batch_sql.py` → "0 insert(s), 1 update(s), 0 delete(s)"; the UPDATE sets
  deferred_reason, findings_note and the updated_* stamp in one statement.
- All four (s6.db): "0 insert(s), 4 update(s), 0 delete(s)".
- cell_status(3) research: 87, 133, 138, 191 leave examined_empty and form never_examined.deferred_searches
  `[87, 133, 138, 191]`; owed.pairs_in_scope `[]` before and after (the antagonist's D7 holds: no pair returns to owed).
- `coverage --slug accessible-circulation-geometry` diff: only `searches_outside_scope` 68 → 67 and
  `searches_deferred_with_reason` 0 → 4. As the antagonist measured.
- Converse on the same copy: `--set-absence-class genuine_absence` on exec 9 → `REFUSING: … A row cannot assert both
  (OD-45) … Nothing was written.` rc 1.

## 7. Surprises

- cell_status's `examined_empty` is "results_admitted = 0", not "results_found = 0": it lists many searches that found
  results but admitted none (e.g. most of exec 29..196). Its docstring says "looked at and found nothing". Not in scope;
  noted for the T-037 page, which would print those as empty.
- The refusal for a row that found results and one with an admission edge is one message naming both facts (one
  check, smallest code); the test asserts each case separately.
- The test file takes about 100 s per run (604 cases), so I ran it twice (red, green) and no mutation runs; each
  T081A-02 case is a distinct state whose refusal is the only thing stopping a write, so removing any one refusal turns
  the case red.

## 8. What I did not do

No commit/add/push/stash/checkout; no edit of research-contract.yaml, the DDL comment or citation-miner l.120; no
database row or migration; no run of the flag on data/guidebook.db; no run_checks.py / preflight (the coordinator gates
the whole PR); no re-run of the four searches (OD-45 ACTION (3), research).
