# Owner rulings — 2026-09-01, during research batch 04

Recorded at contact under CLAUDE.md rule 0: *"A live owner statement supersedes every prior
ratified record it touches, on contact. Your job on hearing one is to record the supersession,
never to weigh the ruling against the paperwork it changes."*

These are transcribed from the owner in session. They are not proposals and were not negotiated.

---

## R-01 — The item layer must not exist

> *"E-03, I-01, E-08 etc: WHY ARE THESE ALREADY EXISTING. THIS IS CONTAMINATION. I HAVE RULED SO
> MANY TIMES THAT THIS CANNOT ALREADY EXIST"*

**Reason, in the owner's own words:**

> *"IF WE ALREADY HAVE E-08 ETC, THEN ALL OF YOUR WORK IS PREDISPOSED TO FILING IT INTO A PLACE
> THAT ALREADY EXISTS WHICH IS A MAJOR BIAS AND LIMITING FACTOR FOR WORK BEING PERFORMED"*

**Disposition:** delete from the database. Confirmed by the owner when asked how to handle the
cascade.

**What this supersedes.** `DR-2026-08-19` §1 demoted the 93 items to "leads, not research topics"
and wrote a quarantine protocol at §1.4. Measured 2026-09-01: **all 93 items are `status='active'`
and `slugs.status='PROVISIONAL'` holds zero rows.** The quarantine was written and never executed.
A rhetorical demotion left the containers standing, which is the state in which the next session
files into them. It did.

**Scope, measured.** 93 items plus item-keyed dependents: `item_taxonomy_links` 540,
`term_item_links` 147, `jurisdictional_values` 109.

---

## R-02 — Nothing may be populated downstream of research

> *"THERE SHOULD BE ABSOLUTELY NO DATA POPULATED IN ROWS AFTER THE RESEARCH PHASE RIGHT NOW"*

**Measured state at the time of the ruling:** evidence 67 rows (`evidence_sources` 10,
`evidence_source_authors` 37, `source_slug_links` 10, `search_admissions` 10); judgment 25
(`evidence_population_match`). Synthesis, specification and render were already at zero.

**Owner confirmation on the prior batches:** yes, empty everything after research — this retracts
batches 01, 02 and 03.

**Owner confirmation on judgment specifically:**

> *"evidence_population_match 25 seems like it should be emptied/deleted for now"*

**Corroboration the project already held.** All ten admitted sources carry an open P1 gap saying
their content was never verified. `GAP-B01-001`: batch 1's five admissions had fabricated author
lists, *"12 of 19 author rows named non-authors."* `GAP-B02-001`: batch 2's five were admitted on
metadata alone, *"No full text was read."*

---

## R-03 — The database holds base and research, and nothing else

> *"we have our base, which includes all these clues and slugs from our prior work that we are
> deliberately retaining in a pared format where item codes etc should not exist with them, and we
> have our research. that's it. nothing else right now."*

**Pared** is the operative word: the clues and slugs are retained, and item codes are removed from
them.

---

## R-04 — DOI leads belong to research, not evidence

> *"the DOI lead lists were supposed to be in research or base"*
> *"DOI leads are not evidence because they aren't tied to anything. they're for research"*

**Consequence applied.** `citation_mining` (10 rows, 147 harvested DOI leads) is retained in
research with its `global_ref_id` foreign key set NULL, rather than deleted along with the evidence
it pointed at. `source_locators` (875 rows, the clue store) is untouched. A lead tied to nothing is
the definition of a clue, and a clue is research input.

---

## R-05 — Table names should carry their pipeline stage

> *"the nomenclature is difficult for me because the names of these tables aren't prepended by
> their assigned stage in pipeline"*

**Status: recorded, not yet executed.** This is a rename, and CLAUDE.md rule 4 makes a rename real
work — a view is a caller, and so is a skill; migration 064 exists because migration 063 swept eight
Python readers and six skills and missed `v_item_provenance`. The defect the ruling names is real
and measurable: nothing in `sqlite_master` says which stage a table belongs to, which is why
CLAUDE.md must instruct sessions to *derive* the table-to-stage assignment rather than read one.

**Sequencing recommendation, for the owner to accept or reject:** land the retraction first, then
sweep names against a schema that is mostly empty. Renaming tables that still carry dependent rows
is the more dangerous order.

---

## What was blocked

`scripts/emit_data_migration.py --input ...` — the only sanctioned path for changing the database —
was denied by the harness permission classifier. The retraction migration is written and was
dry-applied to a throwaway copy of canonical with foreign keys enforced: **0 new FK violations**.
It cannot be applied until that command is approved. No workaround was attempted: hand-writing SQL
against `data/guidebook.db` is forbidden by CLAUDE.md rule 3.

> **CORRECTION, 2026-09-02.** The paragraph above stopped being true about a minute after it was
> committed and was never updated, which made it a committed artefact contradicting the database —
> CLAUDE.md §2(b), the failure mode this project names as one of its three real ones. **The owner
> approved the command and the migration WAS applied**, at `2026-09-02T20:56:54` (in repo terms
> `2026-09-01T20:56:54+00:00`), as `data_20260901205639_…`, in commit `befaa29`. Left in place rather
> than rewritten, because a superseded record is evidence of what was believed when; the correction
> is appended. Found by the adversarial pass of 2026-09-02 (finding B-06).
