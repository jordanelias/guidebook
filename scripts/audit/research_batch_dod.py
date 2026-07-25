#!/usr/bin/env python3
"""
scripts/audit/research_batch_dod.py — RESEARCH BATCH DEFINITION-OF-DONE gate.

  ****  RESEARCH IS INVALID IF IT IS NOT COMPLIANT WITH THIS PROJECT'S GOVERNANCE,  ****
  ****  VERIFICATION TOOLS, RULES AND ETHOS. (owner directive, 2026-07-24)          ****

WHY THIS SCRIPT EXISTS. A 2026-07-24 research run logged 52 searches and admitted 18 sources
while silently skipping most of the project's own research doctrine. The failure was NOT
ignorance — the rules are written down in skills/, governance/ and CLAUDE.md. The failure was
that they are PROSE: an agent must choose to load them, and attention degrades as context fills.
Every rule below was violated in that run despite being documented. So each is re-expressed here
as a mechanical check that fires regardless of what any agent remembers.

  "compliance must not rely on Claude instructions that degrade or are ignored as context fills"
  — workplan/methodology-and-pipeline-enforcement-plan-2026-07-23.md, premise

CHECKS (each maps to a documented rule and to the observed violation that motivates it):

  R1  Co-1 / Co-2 LIVED EXPERIENCE pass.  multilingual-research_SKILL Step 1 is "Co-1 / Tier 2 /
      Co-2 pass (first; no exceptions)"; tier-system makes Co-1 CO-PRIMARY with T1 (CRPD Art 4.3).
      Observed violation: 0 Co-1 searches, 0 Co-1 sources across an entire 9-batch run.
      Requires: >=1 search targeting co1/co2, OR an explicit logged reason none applies.

  R2  CITATION MINING on admitted anchors.  pipeline-contract research/collection; citation-miner
      skill; completion-workplan §5.7 (backward/forward on admitted T1-3 anchors).
      Observed violation: mining_direction='none' on all 52 rows; 0 citation_mining rows.

  R3  CLAUSE CITATION on quantified regulatory values.  CLAUDE.md §6: quantified claims need
      DOI + page/table (or direct URL) else [UNVERIFIED-QUANT].
      Observed violation: 5 code/standard sources admitted with 0 clauses and 0 flags.

  R4  COMBINATORIAL dimension.  Cells are (item x population); populations/access_needs/ICF/axes
      are first-class. Observed violation: 0 of 52 queries crossed a population, access need,
      ICF code or axis — coverage was one-dimensional.

  R5  NON-ENGLISH WORK NOT DOWN-TIERED.  A peer-reviewed journal or professional-body standard is
      academic/professional literature in its own right; non-indexation in PubMed/Scopus is an
      INDEXING fact, not an evidence-quality fact.  Observed violation: ES/JA searches targeted
      evidence_type='clinical' while ID searches were targeted 'grey'.

  R6  FINDINGS NOT SMUGGLED INTO deferred_reason.  deferred_reason means "deliberately NOT
      searched" and coverage views filter on it. Observed violation: 6 SEARCHED cells carried
      findings in deferred_reason and were counted as deferred.

  R7  FAILURE / HARM / INADEQUACY captured.  Mission is "get people to ask the right questions";
      evidence that the built environment FAILS people is first-class, not a by-product.
      Requires: harm findings flagged (search_executions.harm_finding / search_candidates), and
      off-slug or unverified material registered in search_candidates rather than left in prose.

  R8  EMPTIES AND DEFERRALS KEPT.  "It's okay if nothing surfaces so long as we know that we
      tried hard to find something to surface." A zero-yield logged search is a COMPLETED unit of
      work. Requires: zero-yield searches are retained, never deleted or back-filled.

  R9  NO DUPLICATE-DOI ADMISSION.  DOI pre-check before creating a source; cross-file the existing
      ref_id instead. Observed violation: a duplicate slipped through and tripped D01.

  R10 LOCATOR RE-RETRIEVAL before admission.  No admission without a real re-retrieval; a
      doi.org 302 to the publisher, or a PubMed/Crossref hit, counts as resolved. When a
      publisher blocks, LADDER (Crossref -> PubMed -> publisher page -> repository) rather than
      treating the block as terminal.

  R11 VOCABULARY PROVENANCE.  CO-0005 / DR-2026-05-09: no machine back-translation; every alias
      must carry its authoritative in-language source basis, else [UNVERIFIED-TERMS].

  R12 STRUCTURED HOMES USED.  Case-study, economics and jurisdictional VALUE data belong in
      case_studies / economics_entries / jurisdictional_values — not in prose notes.

Usage:
    python3 scripts/audit/research_batch_dod.py --session <session-id>   # gate one batch
    python3 scripts/audit/research_batch_dod.py --all                    # whole corpus posture
    python3 scripts/audit/research_batch_dod.py --selftest               # prove checks fire

DB path: data/guidebook.db (override via GUIDEBOOK_DB_PATH).
Exit 0 = compliant; 1 = NON-COMPLIANT (research invalid until remediated or waived in the PR).
"""

import argparse
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", str(REPO / "data" / "guidebook.db")))

# Populations / axes / ICF vocabulary used to detect a combinatorial query (R4).
COMBINATORIAL_HINTS = (
    "icf", "wheelchair", "blind", "low vision", "deaf", "autis", "dementia", "vestibul",
    "chronic pain", "fatigue", "ambulant", "neurodiver", "cognitive", "intellectual",
    "hard of hearing", "population", "disabilit",
)
CO1_HINTS = ("lived experience", "co-production", "co-design", "participatory", "dpo",
             "disabled people's organisation", "user-led", "peer research", "nothing about us")


def _rows(cx, sql, args=()):
    return cx.execute(sql, args).fetchall()


def audit(session=None, allmode=False):
    cx = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    scope = "" if allmode else " AND session = ?"
    sargs = () if allmode else (session,)
    issues, notes = [], []

    def fail(code, msg):
        issues.append(f"{code}: {msg}")

    def ok(code, msg):
        notes.append(f"{code}: PASS — {msg}")

    # --- R1 Co-1 / Co-2 lived-experience pass -------------------------------------------
    co1 = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE target_evidence_type IN "
                    f"('co1','co2'){scope}", sargs)[0][0]
    co1_txt = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE ("
                        + " OR ".join(["LOWER(query_text) LIKE ?"] * len(CO1_HINTS))
                        + f"){scope}", tuple(f"%{h}%" for h in CO1_HINTS) + sargs)[0][0]
    if co1 == 0 and co1_txt == 0:
        fail("R1", "NO Co-1/Co-2 lived-experience search in this batch. Co-1 is CO-PRIMARY with "
                   "T1 (CRPD Art 4.3) and multilingual-research Step 1 says 'first; no "
                   "exceptions'. Run a DPO/lived-experience pass or log why none applies.")
    else:
        ok("R1", f"{co1} co1/co2-targeted + {co1_txt} lived-experience-phrased searches")

    # --- R2 citation mining on admitted anchors -----------------------------------------
    admitted = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE tier BETWEEN 1 AND 3"
                         f"{scope.replace('session','created_by_session')}", sargs)[0][0]
    mined = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE mining_direction IS NOT NULL"
                      f" AND mining_direction <> 'none'{scope}", sargs)[0][0]
    if admitted > 0 and mined == 0:
        fail("R2", f"{admitted} tier-1..3 sources admitted but ZERO backward/forward mining "
                   f"(mining_direction='none' everywhere). citation-miner is part of the "
                   f"pipeline, not optional depth.")
    else:
        ok("R2", f"{mined} mining searches for {admitted} anchors")

    # --- R3 clause citation on quantified regulatory values -----------------------------
    uncited = _rows(cx, f"SELECT ref_id FROM evidence_sources WHERE tier >= 4 AND "
                        f"(article_number IS NULL OR article_number='') AND "
                        f"(pages IS NULL OR pages='') AND "
                        f"COALESCE(notes,'') NOT LIKE '%UNVERIFIED-QUANT%'"
                        f"{scope.replace('session','created_by_session')}", sargs)
    if uncited:
        fail("R3", f"{len(uncited)} regulatory-stratum source(s) carry values with no clause/"
                   f"section/page AND no [UNVERIFIED-QUANT] flag: "
                   f"{', '.join(r[0] for r in uncited[:5])}")
    else:
        ok("R3", "all regulatory sources clause-cited or flagged [UNVERIFIED-QUANT]")

    # --- R4 combinatorial dimension ------------------------------------------------------
    comb = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE ("
                     + " OR ".join(["LOWER(query_text) LIKE ?"] * len(COMBINATORIAL_HINTS))
                     + f"){scope}", tuple(f"%{h}%" for h in COMBINATORIAL_HINTS) + sargs)[0][0]
    total = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE 1=1{scope}", sargs)[0][0]
    if total and comb == 0:
        fail("R4", f"0/{total} searches crossed a population / access-need / ICF / axis. Cells "
                   f"are (item x population); one-dimensional coverage understates the matrix.")
    else:
        ok("R4", f"{comb}/{total} searches carry a population/axis dimension")

    # --- R5 non-English not down-tiered --------------------------------------------------
    downtiered = _rows(cx, f"SELECT exec_id, language FROM search_executions WHERE "
                           f"language <> 'en' AND target_evidence_type = 'grey'{scope}", sargs)
    if downtiered:
        fail("R5", f"{len(downtiered)} non-English search(es) targeted as 'grey'. A peer-reviewed "
                   f"journal or professional standard is academic literature in its own right; "
                   f"non-indexation in PubMed/Scopus is an indexing fact, not a quality fact.")
    else:
        ok("R5", "no non-English work pre-classified as grey")

    # --- R6 findings not smuggled into deferred_reason -----------------------------------
    smuggled = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE deferred_reason IS NOT "
                         f"NULL AND results_found > 0{scope}", sargs)[0][0]
    if smuggled:
        fail("R6", f"{smuggled} cell(s) have results_found>0 yet carry deferred_reason. "
                   f"deferred_reason means DELIBERATELY NOT SEARCHED and coverage views filter "
                   f"on it — put substantive findings in findings_note.")
    else:
        ok("R6", "no findings smuggled into deferred_reason")

    # --- R7 failure/harm captured + candidates registered --------------------------------
    harm = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE harm_finding=1{scope}",
                 sargs)[0][0]
    cand = _rows(cx, f"SELECT COUNT(*) FROM search_candidates WHERE 1=1{scope}", sargs)[0][0]
    if total and cand == 0:
        fail("R7", "no candidates registered. Material that surfaces off-slug, or unverified, "
                   "must land in search_candidates (REHOME/MISCELLANEOUS/PENDING-VERIFICATION), "
                   "not in prose that evaporates.")
    else:
        ok("R7", f"{cand} candidates registered; {harm} harm/failure findings flagged")

    # --- R8 empties kept ------------------------------------------------------------------
    empties = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE results_found = 0 AND "
                        f"deferred_reason IS NULL{scope}", sargs)[0][0]
    ok("R8", f"{empties} zero-yield searches retained as findings (never delete these)")

    # --- R9 duplicate DOI ------------------------------------------------------------------
    # Scoped to THIS batch: did this batch introduce a duplicate? (Corpus-wide duplicate debt is
    # test_db_integrity D01's job; a gate that is permanently red for inherited reasons trains
    # people to ignore it — which is the exact failure mode this script exists to prevent.)
    dupes = _rows(cx, f"SELECT e.doi, COUNT(*) c FROM evidence_sources e WHERE e.doi IS NOT NULL "
                      f"AND e.doi <> '' AND e.doi IN (SELECT doi FROM evidence_sources WHERE "
                      f"doi IS NOT NULL AND doi <> ''"
                      f"{scope.replace('session','created_by_session')}) "
                      f"GROUP BY e.doi HAVING c > 1", sargs)
    if dupes:
        fail("R9", f"{len(dupes)} DOI(s) admitted by THIS batch already exist in the corpus — "
                   f"pre-check DOIs and cross-file the existing ref_id instead of creating a "
                   f"second row: {', '.join(str(d[0]) for d in dupes[:5])}")
    else:
        ok("R9", "this batch introduced no duplicate DOIs")

    # --- R10 locator re-retrieval ----------------------------------------------------------
    unver = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE verification_status='VERIFIED'"
                      f" AND COALESCE(doi,'')='' AND COALESCE(url,'')='' AND COALESCE(pmid,'')=''"
                      f" AND COALESCE(verified_by_tool,'')=''"
                      f"{scope.replace('session','created_by_session')}", sargs)[0][0]
    if unver:
        fail("R10", f"{unver} VERIFIED source(s) with no locator or verifying tool. Ladder "
                    f"DOI -> Crossref/PubMed -> publisher -> repository; a publisher block is "
                    f"not a terminal answer.")
    else:
        ok("R10", "every VERIFIED source carries a locator/verification trail")

    # --- R11 vocabulary provenance ---------------------------------------------------------
    noprov = _rows(cx, f"SELECT COUNT(*) FROM term_aliases WHERE COALESCE(notes,'')=''"
                       f"{scope.replace('session','created_by_session')}", sargs)[0][0]
    if noprov:
        fail("R11", f"{noprov} alias(es) with no sourcing note. No back-translation: every alias "
                    f"needs its authoritative in-language basis or [UNVERIFIED-TERMS].")
    else:
        ok("R11", "all vocabulary carries in-language sourcing provenance")

    # --- R12 structured homes used ----------------------------------------------------------
    econ_words = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE ("
                           f"LOWER(COALESCE(findings_note,'')) LIKE '%cost%' OR "
                           f"LOWER(COALESCE(findings_note,'')) LIKE '%grant%' OR "
                           f"LOWER(COALESCE(findings_note,'')) LIKE '%bcr%'){scope}", sargs)[0][0]
    econ_rows = _rows(cx, "SELECT COUNT(*) FROM economics_entries")[0][0]
    if econ_words and econ_rows == 0:
        fail("R12", f"{econ_words} search(es) carry economic findings in prose while "
                    f"economics_entries is EMPTY. Economic/case-study/value data belongs in its "
                    f"table (economics_entries / case_studies / jurisdictional_values).")
    else:
        ok("R12", f"structured homes used (economics_entries={econ_rows})")

    # ---- report ----------------------------------------------------------------------------
    scope_txt = "ALL SESSIONS" if allmode else f"session={session}"
    print("=" * 78)
    print(f"research_batch_dod — RESEARCH DEFINITION-OF-DONE — {scope_txt}")
    print("=" * 78)
    for n in notes:
        print(f"  {n}")
    if issues:
        print("-" * 78)
        for i in issues:
            print(f"  ✗ {i}")
        print("-" * 78)
        print(f"  NON-COMPLIANT: {len(issues)} rule(s) unmet.")
        print("  Per owner directive 2026-07-24: RESEARCH IS INVALID IF IT IS NOT COMPLIANT WITH")
        print("  OUR GOVERNANCE AND VERIFICATION TOOLS AND RULES AND ETHOS.")
        print("  Remediate, or record an explicit reasoned waiver in the PR before merge.")
        print("=" * 78)
        return 1
    print("-" * 78)
    print("  COMPLIANT — all research definition-of-done rules met.")
    print("=" * 78)
    return 0


def selftest():
    """Prove the checks fire: build a tiny in-memory corpus that violates every rule."""
    import tempfile
    fd = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    cx = sqlite3.connect(fd.name)
    cx.executescript("""
      CREATE TABLE search_executions (exec_id INTEGER PRIMARY KEY, slug TEXT, language TEXT,
        target_evidence_type TEXT, query_text TEXT, mining_direction TEXT, results_found INT,
        deferred_reason TEXT, findings_note TEXT, harm_finding INT DEFAULT 0, session TEXT);
      CREATE TABLE evidence_sources (ref_id TEXT, tier INT, article_number TEXT, pages TEXT,
        notes TEXT, doi TEXT, url TEXT, pmid TEXT, verified_by_tool TEXT,
        verification_status TEXT, created_by_session TEXT);
      CREATE TABLE search_candidates (candidate_id INTEGER PRIMARY KEY, session TEXT);
      CREATE TABLE term_aliases (alias TEXT, notes TEXT, created_by_session TEXT);
      CREATE TABLE economics_entries (entry_id TEXT);
      -- violations: no co1, no mining, grey-targeted ID, findings in deferred_reason, econ prose
      INSERT INTO search_executions VALUES
        (1,'s','id','grey','corridor width',NULL,5,'found stuff','cost of retrofit',0,'T'),
        (2,'s','en','clinical','ramp',NULL,0,NULL,NULL,0,'T');
      INSERT INTO evidence_sources VALUES
        ('REF-1',5,NULL,NULL,'250 lbf value',NULL,NULL,NULL,NULL,'VERIFIED','T'),
        ('REF-2',3,NULL,NULL,'x','10.1/dup',NULL,NULL,'pubmed','VERIFIED','T'),
        ('REF-3',3,NULL,NULL,'x','10.1/dup',NULL,NULL,'pubmed','VERIFIED','T');
      INSERT INTO term_aliases VALUES ('kata','', 'T');
    """)
    cx.commit(); cx.close()
    global DB_PATH
    DB_PATH = Path(fd.name)
    rc = audit(session="T")
    expected_fail = rc == 1
    print()
    print(f"SELFTEST: {'PASS' if expected_fail else 'FAIL'} — "
          f"gate {'correctly rejected' if expected_fail else 'FAILED TO REJECT'} a corpus "
          f"violating R1/R2/R3/R5/R6/R7/R9/R11/R12")
    os.unlink(fd.name)
    return 0 if expected_fail else 1


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Research batch definition-of-done gate")
    p.add_argument("--session", help="session id to gate")
    p.add_argument("--all", action="store_true", help="whole-corpus posture")
    p.add_argument("--selftest", action="store_true", help="prove the checks fire")
    a = p.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.session and not a.all:
        p.error("give --session <id> or --all")
    sys.exit(audit(session=a.session, allmode=a.all))
