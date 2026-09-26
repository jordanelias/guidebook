#!/usr/bin/env python3
"""Batch 20 -- fourth fix-forward: repair GAP-050 and record GAP-051 as ruled.

Owner rulings relayed 2026-09-26 (recorded on contact, CLAUDE.md rule 0):
  (1) GAP-050: fix now, before merge -- backfill a logged search for each real discovery
      path, reattribute the candidates, unlink the proxy edges, link the true ones
      (batch 17's candidates 107/108 are the precedent).
  (2) GAP-051: the raise-only rule for results_admitted IS the answer, not a stopgap.

Every fact about batch 19 below was checked before this was written, against:
  * batch 19's manifest line 'M1 REF-01006 backward mining' (2026-09-20T03:23:42Z,
    artefact 9a51a98c7235d28f.json, 28 references, reference-count agrees) and its
    citation_mining row for REF-01006 (backward=1, 03:25), which names Pinto and Garg;
  * candidates 123/124 created 03:24, both on exec 91;
  * the batch-19 adversarial subagent's transcript
    (transcripts/harness_ca1ae452/subagents/2026-09-20T03-41-13_other_aaddd48c.jsonl,
    03:48:15Z) and the batch-19 main transcript (03:58:44Z), which hold the Internet
    Archive lookup verbatim and its result (numFound 3); batch 19's manifest has no
    record of it.
Run from the worktree root, against the SCRATCH db. Exec ids are read from log-search's
own JSON output, never derived by a second query.
"""
import json
import os
import subprocess
import sys

SCRATCH = "/tmp/claude-0/-home-user-guidebook/34e8c762-53ff-5f39-b746-3f5298058fcb/scratchpad/b20e.db"
S = "session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa"
B19 = "session_2026-09-20-research-batch-19-pre1990-chain-steinfeld-walter-templer"
ENV = dict(os.environ, GUIDEBOOK_DB_PATH=SCRATCH)
DRY = "--dry-run" in sys.argv
RULING1 = ("Owner ruling 2026-09-26, recorded on contact (CLAUDE.md rule 0): fix GAP-050 before "
           "merge, following batch 17's candidates 107/108.")


def db(*args):
    cmd = ["python3", "scripts/db.py", *args, "--session", S] + (["--dry-run"] if DRY else [])
    r = subprocess.run(cmd, capture_output=True, text=True, env=ENV)
    if r.returncode != 0:
        sys.exit(f"FAILED: {args[:4]}\n{r.stderr[-2000:]}{r.stdout[-800:]}")
    out = r.stdout.strip()
    return json.loads(out[out.index("{"):])


def step(label, out):
    print(f"{label}: {json.dumps(out)[:180]}")


BACKFILL_PRIOR = (
    "BACKFILL, AND THE PRIOR IS THE ABSENCE OF ONE -- recorded as such rather than "
    "reconstructed, as batch 17's exec 77 did. This step RAN in batch 19 and was NEVER LOGGED "
    "as a search; batch 20's independent review found the gap (GAP-050), and the owner ruled "
    "on 2026-09-26 that it be logged now. No prior was written before it ran, and writing one "
    "today would be the rationalisation DR-2026-05-09 forbids.")

# ---- 1. the REF-01006 backward pass (candidates 123 and 124) --------------------------
exec_a = db("log-search", "--slug", "accessible-circulation-geometry", "--language", "EN",
            "--engine", "crossref-deposit", "--depth-method", "scoping",
            "--mining-direction", "backward", "--backfill", "1",
            "--results-found", "28", "--results-screened", "28", "--harm-finding", "1",
            "--query-text",
            "BACKFILL (logged 2026-09-26 by batch 20 for a step batch 19 ran and never logged). "
            "BACKWARD MINING PASS over REF-01006 (Raghuram et al. 2026, doi "
            "10.1016/j.dialog.2026.100342): its publisher-deposited Crossref reference list, 28 "
            "references (reference-count agrees), fetched by batch 19 at 2026-09-20T03:23:42Z and "
            f"persisted as retrieval-log/{B19}/9a51a98c7235d28f.json (manifest purpose 'M1 "
            "REF-01006 backward mining'). Batch 19 recorded the pass in citation_mining (REF-01006, "
            "backward) and staged candidates 123 (Garg 2024) and 124 (Pinto 2021) from it, but "
            "wrote no search_executions row -- so both were filed on exec 91, the Co-1 search that "
            "admitted REF-01006, which never returned either of them.",
            "--prior-expectation", BACKFILL_PRIOR,
            "--findings-note",
            "WHAT THE PASS FOUND lives where batch 19 wrote it -- the citation_mining note for "
            "REF-01006 -- and is pointed at, not copied (rule 5). DERIVE THE SCREEN YIELD: python3 "
            "scripts/research/mining_screen.py --ref REF-01006 --compare. results_screened 28 is "
            "the screen run over every deposited title; which titles a person then read is not "
            "recorded. harm_finding 1 because both staged candidates carry it (each title asks "
            "whether disabled people are denied a right). Candidates 123 and 124 are moved here "
            "from exec 91 with reattribute-candidate; REF-01007 (candidate 124) is linked here and "
            "unlinked from exec 91.")["exec_id"]
step("exec A (REF-01006 backward pass)", exec_a)

# ---- 2. the ad hoc Internet Archive lookup (candidate 125) ----------------------------
exec_b = db("log-search", "--slug", "accessible-circulation-geometry", "--language", "EN",
            "--engine", "internet-archive", "--depth-method", "scoping",
            "--mining-direction", "none", "--backfill", "1",
            "--results-found", "3", "--results-screened", "3",
            "--query-text",
            "BACKFILL (logged 2026-09-26 by batch 20 for a lookup batch 19 ran and never logged). "
            "NOT A DESIGNED RESEARCH QUERY: an ad hoc catalogue lookup run by batch 19's "
            "independent adversarial pass while it checked that batch's claim that John A. "
            "Templer had no ramp research. Verbatim: "
            "https://archive.org/advancedsearch.php?q=creator%3ATempler+AND+%28pedestrian+OR+ramp"
            "+OR+handicapped%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&fl%5B%5D=creator"
            "&rows=20&output=json -- run at 2026-09-20T03:48:15Z (transcripts/harness_ca1ae452/"
            "subagents/2026-09-20T03-41-13_other_aaddd48c.jsonl), then re-run by the batch-19 "
            "session at 03:58:44Z to verify before staging candidate 125 "
            "(transcripts/harness_ca1ae452/main.jsonl). numFound 3: provisionsforeld00temp, "
            "_0 and _1, 'Provisions for elderly and handicapped pedestrians : final report', "
            "Templer, John, 1979. WHERE THE TITLE CAME FROM IS NOT RECORDED: a Crossref query in "
            "the same command, run just before it, already used the report's title words "
            "('Templer provisions elderly handicapped pedestrians'), so this lookup confirmed a "
            "copy existed rather than discovering the title from nothing. Neither response was "
            "persisted in batch 19's retrieval log; the transcripts are the record.",
            "--prior-expectation", BACKFILL_PRIOR,
            "--findings-note",
            "Candidate 125 (Templer, FHWA-RD-79-1/-2/-3) came from this lookup, not from exec 90, "
            "whose seven logged routes (ERIC, OpenAlex, Crossref, TRID) never queried Internet "
            "Archive; exec 90's own 2026-09-20 correction records the find. Moved here with "
            "reattribute-candidate; REF-01008 (Volume 3, provisionsforeld00temp_0) is linked "
            "here and unlinked from exec 90.")["exec_id"]
step("exec B (Internet Archive lookup)", exec_b)

# ---- 3. candidates to the searches that actually surfaced them -------------------------
for cid, ex, why in (
        (123, exec_a, "surfaced by batch 19's backward pass over REF-01006's deposited "
                      "reference list, not by exec 91's queries"),
        (124, exec_a, "surfaced by batch 19's backward pass over REF-01006's deposited "
                      "reference list, not by exec 91's queries"),
        (125, exec_b, "surfaced by batch 19's adversarial pass's Internet Archive lookup; "
                      "exec 90's logged routes never queried Internet Archive")):
    step(f"reattribute {cid}", db(
        "reattribute-candidate", "--candidate-id", str(cid), "--exec-id", str(ex),
        "--reason", f"{RULING1} This candidate was {why}. That step was never logged, so it "
                    f"was filed on the nearest logged search; exec {ex} is the step, logged as "
                    f"a backfill (GAP-050)."))

# ---- 4. the proxy edges out, the true edges in -----------------------------------------
for ex, ref in ((91, "REF-01007"), (90, "REF-01008")):
    step(f"unlink {ex}->{ref}", db(
        "unlink-admission", "--exec-id", str(ex), "--ref-id", ref, "--reason",
        f"{RULING1} This edge copied a proxy attribution: the candidate that became {ref} was "
        f"filed on this search because the step that surfaced it was never logged. It is moved "
        f"to that step, now logged as a backfill (GAP-050)."))
for ex, ref, cand in ((exec_a, "REF-01007", 124), (exec_b, "REF-01008", 125)):
    step(f"link {ex}->{ref}", db(
        "link-admission", "--exec-id", str(ex), "--ref-id", ref, "--reason",
        f"{RULING1} Candidate {cand}, admitted as {ref} in batch 20, was surfaced by this step; "
        f"the edge moves here from the search it had been filed on. The attribution rests on "
        f"batch 19's own records named in this search's query_text, not on S01, which cannot "
        f"fail on an edge this verb writes."))

# ---- 5. GAP-050 closed with the chain; GAP-051 recorded as ruled -----------------------
step("GAP-050", db("amend-gap", "--gap-id", "GAP-050", "--append-note",
     f"FIXED 2026-09-26 BY OWNER RULING (fix before merge; batch 17's 107/108 precedent). THE "
     f"CORRECTED CHAIN: (1) exec {exec_a}, a backfill search row for batch 19's backward pass "
     f"over REF-01006's Crossref deposit (28 references; retrieval-log artefact "
     f"9a51a98c7235d28f.json; citation_mining REF-01006) -> candidates 123 and 124 reattributed "
     f"there from exec 91 -> edge (91, REF-01007) unlinked, (exec {exec_a}, REF-01007) linked. "
     f"(2) exec {exec_b}, a backfill search row for batch 19's adversarial pass's ad hoc "
     f"Internet Archive lookup (creator:Templer AND (pedestrian OR ramp OR handicapped), "
     f"numFound 3; recorded only in the batch-19 transcripts) -> candidate 125 reattributed "
     f"there from exec 90 -> edge (90, REF-01008) unlinked, (exec {exec_b}, REF-01008) linked. "
     f"results_admitted: execs {exec_a} and {exec_b} raised 0 -> 1 by link-admission; exec 91 "
     f"stays 1 (its REF-01006 edge remains) and exec 90 stays 0. research_protocol_audit now "
     f"names REF-01007 and REF-01008 as admitted only by a BACKFILLED search, which is true "
     f"and is the honest residue: the step ran, and it was not logged when it ran. Derive the "
     f"chain: select candidate_id, exec_id, resolved_ref_id from search_candidates where "
     f"candidate_id in (123,124,125); select * from search_admissions where ref_id in "
     f"('REF-01007','REF-01008'); select exec_id, backfill, engine, results_admitted from "
     f"search_executions where exec_id in (90,91,{exec_a},{exec_b})."))
step("close GAP-050", db("close-gap", "--gap-id", "GAP-050", "--status", "CLOSED-FIXED"))

step("GAP-051", db("amend-gap", "--gap-id", "GAP-051", "--append-note",
     "RESOLVED BY OWNER RULING 2026-09-26, recorded on contact (CLAUDE.md rule 0; recorded in "
     "references/project-standards.md). The raise-only rule described above IS THE ANSWER, not "
     "a session's stopgap awaiting a choice: results_admitted is set at insert from the "
     "search's edges; a later admission edge written on that search raises it to "
     "max(count, edges); removing a wrong edge lowers it by one, never below the edges that "
     "remain; and it is NEVER lowered to force agreement with the edges. This supersedes, for "
     "post-insert writes, both DR-2026-08-19 step 7's 'must agree exactly' and the 2026-09-02 "
     "repair's 'nothing updates it thereafter'. The restored historical counts above their "
     "edges stay as they are, by design. Code: _results_admitted_after in scripts/db.py; "
     "cases: scripts/tests/test_db_amend_writers.py (L03, L06, U03)."))
step("close GAP-051", db("close-gap", "--gap-id", "GAP-051", "--status", "CLOSED-DECIDED"))

print("DONE", "(dry run)" if DRY else "", "exec_a", exec_a, "exec_b", exec_b)
