# Sweep list: what the critics found and did not repair, and why (owner instruction 2026-11-15, "sweep … forward and backward")

Derive every count; none is typed here. One section per task; a finding is repaired in the commit named, or is the owner's / a design question with the file that would change.

## T-020 (commit d1bfc280; critic repairs in the next commit on the branch)

Repaired in the repair commit: order of the new refusals now held by T020-09 (red when the kind block is moved ahead of the earlier refusals); T020-08 splits the id-shape probes so each rule fails alone and re-reads the refusal to see the fixture kind listed (red when the id pattern admits a digit); `insert_parameter` refuses a non-string `--quantity-kind` instead of raising AttributeError; the skill sentence that counted the verbs taking `--approval-ref` now derives them by a grep.

Not repaired:
1. **The warrant's digit test admits a quote whose only digit is not a value** (a year, a clause number, "Class 1"). It conforms to T-020 section 4 item 1a(iii) as written; section 3 promises "an observation of a source stating a value of the quantity". Tightening it (a digit adjacent to a unit, or an adjudicated extraction) would add what section 4 does not name. A design question for the file `tasks/T-020-quantity-kind.md` (section 4, 1a(iii)) and for T-109, which assigns the live parameters their kind. Today the warrant is recorded and contestable, not proven.
2. **`insert_parameter` records the judgment under a blank session** (`session='  '`). Pre-existing (not a weakening); `insert_quantity_kind` refuses it. A small refusal in `insert_parameter` would close it; it is not named by T-020, so it is left for a task that names it.
3. **Migration 143 line 2 types "six-kind seed"** (rule 7a). The migration is committed and immutable (rule 3); the sentence is a comment and cannot be edited. The commit message of d1bfc280 carries two typed counts for the same reason and is history.
4. **`STATE-GRAPH.md` and `graph.json` lack T-020's guard and `add-quantity-kind`.** They are generated; regenerated in the end-of-batch sweep (owner instruction 2026-11-15, item 4), not per task.

## T-022 (commit 1ca23587; critic repairs in the commit after it)

Repaired: both B12 edges removed (the owner's statement of 2026-11-06 (seventh) supersedes the route for base vocabulary: rule 0; the executor had entered them on its own reading, which the task file did not state); the B11 edges no longer say "until the owner answers OD-10" (answered 2026-11-12) and now state what the carrier selects (every skim, not only a skim under a determination); the B7 edge no longer claims "T1-T2" (the carrier is any mined source); the audit refuses an edge id held twice (T022-09); T022-10 holds the stage EARLIER than the carrying stage (the `<=` to `==` mutant now fails); `test_pipeline_contract` fails when no return is ruled at all (deleting every `re_entry` block no longer passes). Each guard was run red on a seeded defect and the file restored byte for byte. The task file carries both corrections.

Not repaired (a design or owner question, or data):
1. **Three of the six carriers carry nothing today** (derive: `gaps.parameter_id` populated rows, `term_aliases.source_url` populated rows, `extraction_follow_ups` rows). The audit holds that a carrier exists and its value is in the column's CHECK, not that it is used; "never used" is a fact of the data, which later research fills.
2. **B10 cannot name "open" as a carrier value**: `gaps.status` is a LIKE check, so `dbcore.check_values` returns no set. The edge names the column only. A real CHECK on `gaps.status` would be a schema change this task does not name.
3. **B13 names `source_url` only**; the boundary table says URL, page and line. `term_aliases` also has `source_page` and `source_line`; a second carrier per edge is not what the schema of `ReEntry` allows, and the owner's statement says page and line are "if need be".
4. **B11 and the two skim edges share one carrier**, so the edge cannot tell an evidence-origin return from a judgment-origin one. They are two edges because the boundary table has two re-entry stages; whether a single edge with two target stages is better is a design question for `governance/pipeline-contract.yaml`.
5. **The graph ingest ignores `re_entry`** (`scripts/audit/graph/extract_contract.py` renders stages and criteria only), so the ruled returns are absent from the state graph. A later task that renders them owns it; the end-of-batch sweep regenerates the derived files.
6. **B9 and B14 are not entered**: the boundary table marks them "ledger" and "inferred", not "ruled".

## T-049 (commit 3818ed33; critic repairs in the commit after it)

Stopped once: the executor's section 3 flag `--source-row-key` ended in a secret word (`key`), and `dbcore._secret_flag` redacts such a flag's value in the refusal recorder (T-088, case T088-05b). Renamed the FLAG to `--source-row-id` (the column stays `source_row_key`); exempting it would weaken a T-088 guard. The task file records the rename.

Repaired: the definition of "current" had three homes (the view, `_current_translation`, the audit); the verbs and the audit now read `v_translations_current`; four refusals no test held now have a case each, each run red on a seeded defect (T049-87 own-language request, T049-88 blank session, T049-89 unknown target language, T049-90 translator kind outside the CHECK, which names the kinds the CHECK holds); T-037's task file now states that the renderer must hash-check a translation before showing it.

Not repaired (the spec's own wording, a design or owner question):
1. **OD-30 is recorded, not enforced, at the read surface.** The view admits `translated` rows (T-049 item 2) and the reader gate is T-037's (item 8). The commit message of 3818ed33 says the registry entries check that no translation is shown unreviewed; they check pointer, hash and numbers. The claim is history; this note corrects it.
2. **The reviewer check is a case-insensitive name compare** (item 8). A near-identical name, the same session and a non-Opus model all pass; the database cannot verify a model class. Whether the review's session must differ from the translator's is a rule the file does not state (task file, design question (b)).
3. **A translation equal to its original is accepted**: no flag carries the original, but the text a translator supplies is not compared with it (design question (c)).
4. **The number rule refuses `1 200 mm` to `1,200 mm`, and passes a reordered pair, a changed unit and a flipped comparator** (item 5; design question (a)). A change to item 5 and T-008's reader.
5. **A stale translation stays in the view** after its original changes; the verbs refuse it and the advisory audit reports it, and T-037 must check the hash (now stated in its file). A stale `requested` row has no verb that closes it.
6. **The joined-cells census examines no translation column** while the table holds no row (it counts columns with data). Re-run it after the first translation is written.
7. **`translations` rows and other tables' keys are translatable cells** (`translations.translated_text`, `evidence_sources.ref_id`): the file lists no translatable tables, by design.
