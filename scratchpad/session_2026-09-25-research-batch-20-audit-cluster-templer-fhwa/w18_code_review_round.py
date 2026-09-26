#!/usr/bin/env python3
"""Batch 20 -- third fix-forward: the record half of the 2026-09-26 code-review round.

The code half (db.py / dbcore.py / the new test) is in the same commit. This script writes
only what the record must now say, through db.py, to the SCRATCH db. New gap ids are read
from db.py's output, never computed here. Every claim about batch 19 below was checked
against batch 19's own session record (section 13), exec 90's logged query_text, and
GAP-037's 2026-09-20 text before this was run.
"""
import json
import os
import subprocess
import sys

SCRATCH = "/tmp/claude-0/-home-user-guidebook/34e8c762-53ff-5f39-b746-3f5298058fcb/scratchpad/b20d.db"
S = "session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa"
B19 = "sessions/session_2026-09-20-research-batch-19-pre1990-chain-steinfeld-walter-templer.md"
ENV = dict(os.environ, GUIDEBOOK_DB_PATH=SCRATCH)
DRY = "--dry-run" in sys.argv


def db(*args):
    cmd = ["python3", "scripts/db.py", *args, "--session", S] + (["--dry-run"] if DRY else [])
    r = subprocess.run(cmd, capture_output=True, text=True, env=ENV)
    if r.returncode != 0:
        sys.exit(f"FAILED: {args[:4]}\n{r.stderr[-2000:]}{r.stdout[-800:]}")
    out = r.stdout.strip()
    return json.loads(out[out.index("{"):])


def step(label, out):
    print(f"{label}: {json.dumps(out)[:170]}")


# ---- new gaps -------------------------------------------------------------------------
g_prov = db("add-gap", "--category", "RP", "--priority", "P2", "--skill", "governance",
            "--description",
            "THE TWO ADMISSION EDGES BATCH 20 WROTE WITH link-admission COPY PROXY ATTRIBUTIONS, AND "
            "NO GATE CAN SAY SO. link-admission writes (exec, source) only when a candidate row "
            "records both, and it copies that row's exec_id -- so integrity check S01 cannot fail on "
            "these edges, and it did not. What decides whether they are TRUE is whether the search "
            "named on the candidate actually surfaced it, and batch 19's own record says it did not "
            "in either case. (1) Candidate 124 (Pinto 2021, now REF-01007) sits on exec 91, batch "
            "19's Co-1 pass; batch 19's session record, section 13, says 'REF-01006's references hold "
            "at least five audits of real health facilities -- Pinto 2021 ... Candidates 123 and 124 "
            "stage the two strongest'. They came from reading the REFERENCE LIST of the source exec 91 "
            "admitted, a backward step R2 says to log as its own search row, and batch 19 logged "
            "none (its only backward exec is 88, over REF-01005). Candidate 123 (Garg 2024) is in the "
            "same state. (2) Candidate 125 (Templer FHWA-RD-79-3, now REF-01008) sits on exec 90, "
            "whose logged query names seven routes -- ERIC, OpenAlex, Crossref, TRID -- and not "
            "Internet Archive, where batch 19's adversarial pass found the report ('the endpoint this "
            "same batch used for Walter an hour earlier and never pointed at Templer', GAP-037's "
            "2026-09-20 text; exec 90's own note was later amended to say 'Candidate 125 stages "
            "it'). CONSEQUENCE: search_admissions now says a Co-1-targeted search admitted a T3 "
            "facility census, and a Templer-identification query admitted a report it never "
            "queried. THE PRECEDENT FOR THE FIX is batch 17's candidates 107/108: log the unlogged "
            "search with log-search --backfill 1 and a prior that states its own absence, move the "
            "candidates with reattribute-candidate, then unlink-admission the proxy edge and "
            "link-admission the true one. NOT DONE HERE: it reconstructs another batch's unlogged "
            "work, and the batch-20 PR is on hold for review. Until it is done, results_admitted on "
            "execs 90 and 91 is deliberately NOT raised to meet these edges -- raising it would "
            "carry the proxy into v_coverage_branch's Co-1 count. Derive the state: select "
            "candidate_id, exec_id, resolved_ref_id from search_candidates where candidate_id in "
            "(123,124,125); select * from search_admissions where ref_id in "
            "('REF-01007','REF-01008').")["gap_id"]
step("gap provenance", g_prov)

g_count = db("add-gap", "--category", "DEC", "--priority", "P3", "--skill", "governance",
             "--description",
             "WHAT results_admitted MEANS AFTER A SEARCH IS LOGGED IS UNSETTLED, AND TWO RECORDS "
             "DISAGREE. DR-2026-08-19 step 7 (the operative instrument) prescribes updating "
             "search_executions.results_admitted in the same transaction as the admission edge. The "
             "2026-09-02 repair (session_2026-09-02-owed-repairs; the H05 comment in "
             "scripts/tests/test_db_integrity.py) deleted invariant H05 after enforcing it had "
             "rewritten seven searches' counts to 0, and declared the column writer-retired: set at "
             "insert, 'nothing updates it thereafter'. The views v_coverage_language, "
             "_jurisdiction and _branch SUM it as 'admitted'. Batch 20's link-admission was the first "
             "writer of an edge on an existing search and left the count behind (a 2026-09-26 "
             "review measured exec 90 at 0 with 1 edge, exec 91 at 1 with 2). db.py now reconciles "
             "the two: link-admission raises the count to max(count, edges), unlink-admission "
             "lowers it by one but never below the edges left -- so the restored historical counts "
             "(count above edges, by design) are never touched. That is a reconciliation made by a "
             "session, not a ruling, and the owner may prefer either pure form (always sync, or "
             "never move after insert, with the views reading COUNT(search_admissions)). The "
             "reasoning and the one place to change it: _results_admitted_after in scripts/db.py. "
             "Derive the rows where count and edges differ: select e.exec_id, e.results_admitted, "
             "(select count(*) from search_admissions a where a.exec_id=e.exec_id) edges from "
             "search_executions e where results_admitted <> edges.")["gap_id"]
step("gap results_admitted", g_count)

g_rehome = db("add-gap", "--category", "RP", "--priority", "P3", "--skill", "governance",
              "--description",
              "LEGACY REHOME CANDIDATES THAT NAME NO DESTINATION. From 2026-09-26 both writers that "
              "can set REHOME -- add-candidate and resolve-candidate -- refuse one without a "
              "filable --suggested-slug other than the slug it was found under "
              "(_check_rehome_destination in scripts/db.py). Rows written before that still sit "
              "in the refused state. They are not filled mechanically here: a destination is a "
              "judgment about each candidate, made by reading it, and the writer now refuses the "
              "guess a blanket fill would be. Derive them rather than trusting a count: select "
              "candidate_id, found_under_slug, suggested_slug, title from search_candidates where "
              "disposition='REHOME' and (suggested_slug is null or suggested_slug = "
              "found_under_slug). Each is repaired with resolve-candidate --disposition REHOME "
              "--suggested-slug <slug>, or moved to another disposition if no slug fits.")["gap_id"]
step("gap legacy REHOME", g_rehome)

# ---- corrections to the three gaps batch 20 closed -----------------------------------
step("GAP-045", db("amend-gap", "--gap-id", "GAP-045", "--append-note",
     "THE FIRST FIX WAS INCOMPLETE, FOUND BY A 2026-09-26 CODE REVIEW THAT RAN IT. --suggested-slug "
     "was OPTIONAL and checked only for existence, so a REHOME could still name no destination, "
     "point back at its own origin, or name a MERGED slug -- the states the flag existed to end. "
     "NOW: REHOME REQUIRES a destination; one equal to found_under_slug is refused; the slug must "
     "pass _check_slug_filable (MERGED refused, as everywhere else in db.py); the same rule guards "
     "add-candidate, the other writer that can set REHOME; and --clear-suggested-slug empties a "
     "stale value on a non-REHOME resolution (the UPDATE cannot write NULL through a COALESCE). "
     "Every refusal has a case in scripts/tests/test_db_amend_writers.py. The code gap stays "
     "closed; the rows written before the rule are " + g_rehome + "."))

step("GAP-046", db("amend-gap", "--gap-id", "GAP-046", "--append-note",
     "CORRECTED 2026-09-26 AFTER A CODE REVIEW THAT RAN THE VERB. (1) AN OVERCLAIM, WITHDRAWN: this "
     "gap said link-admission 'restates a recorded fact and cannot attribute a source to an "
     "arbitrary search', and batch 20's notes said the edges were written 'as S01 requires'. The "
     "precise statement: the refusal stops an attribution NOBODY recorded; it does not establish "
     "that the recorded one is TRUE. The edge copies the candidate's exec_id, so S01, which compares "
     "exactly those two columns, cannot fail on it -- a green S01 there is two tables agreeing about "
     "one fact, not verification. And the two edges written from this gap turn out to copy proxy "
     "attributions: " + g_prov + ". (2) A REFUSAL REMOVED: link-admission refused a source another "
     "exec already admitted; log-search permits that, a source surfaced by two searches is "
     "ordinary, and the refusal pointed at reattribute-candidate, which would have falsified the "
     "surfacing search. (3) A CORRECTIVE VERB ADDED: db.py had no DELETE or UPDATE on "
     "search_admissions, so a wrong edge could not be removed by any sanctioned path; "
     "unlink-admission does it, keeping the removed edge in the search's findings_note. (4) "
     "results_admitted now moves with an edge link-admission adds or unlink-admission removes, "
     "never lowered to meet the edges; the disagreement between the operative instrument and the "
     "2026-09-02 retirement of that column is " + g_count + ". The code gap stays closed."))

step("GAP-047", db("amend-gap", "--gap-id", "GAP-047", "--append-note",
     "CORRECTED 2026-09-26 AFTER A CODE REVIEW THAT RAN THE VERB. amend-term's no-op check compared "
     "the stored scope_note with the replacement, but the stored value carries earlier audit lines, "
     "so an identical second call never matched -- and it quoted the whole old column inside the new "
     "line, nesting one audit line inside the next. Now: no-op detection for `definition` only; a "
     "scope_note amendment replaces the body, keeps the earlier AMENDED lines, and adds one, so a "
     "repeated identical amendment is a second dated line. amend-term also gained the "
     "fk_declared/check_declared gates amend-source and amend-extraction apply to every amendable "
     "field, and its stamp comes from dbcore.upd. The trailer and the --reason guard of all four "
     "batch-20 writers are now dbcore.append_dated_note and dbcore.require_reason. Cases: "
     "scripts/tests/test_db_amend_writers.py."))

# ---- the two searches' own notes ---------------------------------------------------------
step("exec 91", db("amend-search", "--exec-id", "91", "--append-note",
     "BATCH 20's ADMISSION LINE ABOVE OVERSTATES THE PROVENANCE. It says 'Candidate 124 was surfaced "
     "by this search'. Batch 19's own record (" + B19 + ", section 13) says Pinto 2021 -- and Garg "
     "2024, candidate 123 -- were found in REF-01006's REFERENCE LIST, the source this search "
     "admitted, not in this search's results; that backward step was never logged as a search. "
     "Candidates 123 and 124 were filed on this exec as the nearest logged search. The edge (91, "
     "REF-01007) copies that filing and is not independent evidence of it; results_admitted here is "
     "deliberately NOT raised to meet it. See " + g_prov + "."))
step("exec 90", db("amend-search", "--exec-id", "90", "--append-note",
     "BATCH 20's ADMISSION LINE ABOVE OVERSTATES THE PROVENANCE. It says 'Candidate 125 was surfaced "
     "by this search'. This search's logged query names seven routes (ERIC, OpenAlex, Crossref, "
     "TRID) and not Internet Archive, where batch 19's adversarial pass found the FHWA report "
     "(GAP-037's 2026-09-20 text; the correction above on this note records the find). The edge "
     "(90, REF-01008) copies the candidate's filing on this exec and is not independent evidence of "
     "it; results_admitted here is deliberately NOT raised to meet it. See " + g_prov + "."))

print("DONE", "(dry run)" if DRY else "")
