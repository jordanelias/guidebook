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

WHERE THE CONTRACT LIVES. governance/research-contract.yaml is the CANONICAL text of the research
contract (DR-2026-08-01-research-contract-single-source). Until then it existed as two hand-transcribed
copies — this docstring and the SessionStart hook in .claude/settings.json — with no comparator,
and they had drifted on R1, R2 and R3; two of those changed what the contract obliges. The hook
is now GENERATED from the contract, and `research_contract_sync` cross-references the rule ids
here against it, so a rule defined in one place and absent from the other fails a check.

The table below is documentation of what this script implements. It is not the contract. If it
and governance/research-contract.yaml ever disagree, the contract governs and this table is the
thing to correct — and note that R1's pass is Co-1 / **Tier 2** / Co-2, and R2's scope is
confirmed **Tier 1-2** (not T1-T3), both corrected at the contract on 2026-08-01.

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

  R4  COMBINATORIAL dimension.  Cells are (parameter x lens); populations/access_needs/ICF/axes
      are first-class. Observed violation: 0 of 52 queries crossed a population, access need,
      ICF code or axis — coverage was one-dimensional.

  R5  NON-ENGLISH WORK NOT DOWN-TIERED.  A peer-reviewed journal or professional-body standard is
      academic/professional literature in its own right; non-indexation in PubMed/Scopus is an
      INDEXING fact, not an evidence-quality fact.  Observed violation: ES/JA searches targeted
      evidence_type='clinical' while ID searches were targeted 'grey'.  Since 2026-10-02 the
      subject is the batch's non-English ADMISSIONS, not its search targets: one filed 'grey'
      that is a journal article, names a journal or carries a DOI fails.

  R6  FINDINGS NOT SMUGGLED INTO deferred_reason.  deferred_reason means "deliberately NOT
      searched" and coverage views filter on it. Observed violation: 6 SEARCHED cells carried
      findings in deferred_reason and were counted as deferred.

  R7  FAILURE / HARM / INADEQUACY captured.  Mission is "get people to ask the right questions";
      evidence that the built environment FAILS people is first-class, not a by-product.
      Requires: harm findings flagged (search_executions.harm_finding / search_candidates), and
      off-slug or unverified material registered in search_candidates rather than left in prose.
      Asserted here since 2026-10-02: count integrity only (screened <= found, admitted <=
      screened). The candidate floor is gone; RC1 (provenance_artefact_audit) and adversarial
      standing subject 1 enforce the substance.

  R8  EMPTIES AND DEFERRALS KEPT.  "It's okay if nothing surfaces so long as we know that we
      tried hard to find something to surface." A zero-yield logged search is a COMPLETED unit of
      work. Requires: zero-yield searches are retained, never deleted or back-filled. NOT
      tested: that a search's prior was written before it ran (no timestamp can witness it).

  R9  NO DUPLICATE-DOI ADMISSION.  DOI pre-check before creating a source; cross-file the existing
      ref_id instead. Observed violation: a duplicate slipped through and tripped D01.

  R10 LOCATOR RE-RETRIEVAL before admission.  No admission without a real re-retrieval; a
      doi.org 302 to the publisher, or a PubMed/Crossref hit, counts as resolved. When a
      publisher blocks, LADDER (Crossref -> PubMed -> publisher page -> repository) rather than
      treating the block as terminal.

  --- Added 2026-09-10, from workplan/2026-09-10-road-to-batch-06.md B3. ---

  R10b NO SILENTLY-NULL VERIFICATION STATUS ON A URL-BEARING ADMISSION.  R10 above examines
      VERIFIED sources only, so it cannot see the one condition that wakes the scheduled
      verify-urls cron: a source with a URL and verification_status left NULL. That is exactly
      what `add-source` permits and exactly the pool verify_urls.py polls; the cron's next fire
      writes a url_verification_runs row (not exempt from migration_reproducibility) straight to
      main and reddens migration_reproducibility for every open DB-touching PR.

  R11 VOCABULARY PROVENANCE.  CO-0005 / DR-2026-05-09: no machine back-translation; every alias
      must carry its authoritative in-language source basis, else [UNVERIFIED-TERMS].

  R12 STRUCTURED HOMES USED.  Case-study, economics and jurisdictional VALUE data belong in
      case_studies / economics_entries / research_code_leads — not in prose notes.

  --- Added 2026-07-25, derived from the remediation pass itself. ---

  R13 POPULATION-OF-STUDY vs POPULATION-SERVED.  Every tier-1..3 admission carries a graded
      population match. An admission with no match row silently asserts that the population
      STUDIED is the population SERVED. Observed: a chamber emissions test with no human
      participants filed against chemical sensitivity; a general-population autistic-TRAITS
      sample filed against autistic people; a general-population CHILDREN sample used for
      neurodivergent adults. All three are usable as PROXY and misleading as anything else.

  R14 A ZERO-YIELD SEARCH MUST SAY WHY.  An empty result is evidence of ABSENCE only if the
      query was well-formed. Observed: four PubMed queries returned 0 purely because
      descriptive multi-concept phrasings AND-chain — a METHOD failure. Keep the empty (R8),
      but distinguish query-shape failure / wrong index / genuine absence. Only the last counts.

  R15 A RESOLVED CANDIDATE IS RE-DESCRIBED FROM THE SOURCE.  A staged candidate's description
      is a HYPOTHESIS. Observed: a lead staged as "the direct built-environment claim" resolved
      to an SEM mechanism study in a general-population trait sample supplying no design
      parameter. Unchecked, that description would have hardened into fact in the register.

  --- Added 2026-10-02, GAP-061 (process-gap remediation plan WP11). ---

  R16-adjudicate EVERY OBSERVATION ON THE BATCH'S ADMISSIONS IS ADJUDICATED.  R11-harvest asserts
      that each admission carries an observed phrase; nothing asserted that judgment ever
      answered one. Observed: batch 23 passed R11-harvest with not one of its observations
      adjudicated. An answer that names no term counts; silence does not.

  R16 EVERY CONCEPT A SOURCE STATES A FIGURE FOR IS DISPOSED OF.  Every term an adjudication of
      those observations names is a parameter (base_parameters) or is declined with its reason
      (parameter_declinations). Observed: nothing promoted a harvested term to a parameter, so
      every extraction in the database was filed under the one parameter that existed, and
      what sources state for any other concept was lost. Both R16 predicates are scoped to the
      batch's ADMISSIONS, as R11-harvest is, not to the session's writes.

DESIGN RULES for anyone extending this gate (learned by attacking it on 2026-07-24, when eight
of eight attacks succeeded):
  * Prefer STRUCTURAL evidence over TEXT evidence. Substring checks false-pass: "lived
    experience" appearing in a query proved nothing; population codes matched inside ordinary
    words because SQLite LIKE is case-insensitive ("COM" in "accommodate").
  * Thresholds of "> 0" are gameable forever by one row. Make them proportionate.
  * A check that can never fail is decorative. R8 passed while every empty row was deleted.
  * Baseline numbers may only RATCHET DOWN. Raising one to make a batch pass defeats the gate.
  * The selftest must clone the LIVE schema and fail loudly; a silently-rotted guard is worse
    than no guard, because it manufactures confidence.

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
sys.path.insert(0, str(REPO / "scripts"))
import dbcore                                                        # noqa: E402
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", str(REPO / "data" / "guidebook.db")))
BASELINE_PATH = REPO / "governance" / "research-contract-baseline.json"

# Populations / axes / ICF vocabulary used to detect a combinatorial query (R4).
COMBINATORIAL_HINTS = (
    "icf", "wheelchair", "blind", "low vision", "deaf", "autis", "dementia", "vestibul",
    "chronic pain", "fatigue", "ambulant", "neurodiver", "cognitive", "intellectual",
    "hard of hearing", "population", "disabilit",
)
CO1_HINTS = ("lived experience", "co-production", "co-design", "participatory", "dpo",
             "disabled people's organisation", "user-led", "peer research", "nothing about us")

# ---------------------------------------------------------------------------------------------
# TUNABLE THRESHOLDS — collected here ON PURPOSE, for review.
#
# These numbers were chosen by the agent whose work this gate judges, which is a conflict of
# interest, not a neutral act: the FIRST version of R1 accepted a substring and duly passed a run
# with zero Co-1 sources. They are gathered in one block instead of buried in the checks so a
# reviewer can audit every discretionary number in under a minute and change one without reading
# the logic. Each records what it is and why it is where it is.
#
# STATUS: PROVISIONAL pending independent review (DR-2026-07-25 §6.4). Raising any of these makes
# the gate weaker; do that deliberately and say so in the PR, never to make a batch pass.
# ---------------------------------------------------------------------------------------------

# R2 — citation_mining rows expected per admitted tier-1..3 anchor.
# 1/4 = "mine a meaningful minority of anchors per batch", not "mine everything" (which would
# stall batches) and not ">0" (which one stub row satisfies forever). Deliberately weak-ish: it is
# a floor against doing NOTHING, not a definition of systematic mining.
R2_MINING_PER_ANCHORS = 4

# R7's threshold (registered candidates per screened result) was DELETED 2026-10-02, process-gap
# remediation plan WP12. That weakens R7, and per this block's header the PR says so: the party
# being judged typed both terms of the ratio, and batch 23 met the floor by recording rather than
# by searching. R7 now asserts count integrity only; see its block for what enforces the rest.


def _rows(cx, sql, args=()):
    return cx.execute(sql, args).fetchall()


def check_baseline(ref="origin/main"):
    """Fail if the committed baseline forgives more debt than REF's did.

    The baseline exists so inherited debt does not hold this gate permanently red
    — a red-forever gate is ignored, which is the failure this whole script is
    against. That amnesty was self-administered: `--write-baseline` ratchets
    numbers down only, but nothing checked the FILE, and the file is editable.
    Raising `R13: 494` to `R13: 600` in a text editor forgives 106 fresh
    violations and leaves a green gate and no trace, which is a more thorough
    defeat of the check than deleting it — deleting it is at least visible.

    The ratchet needs a witness outside the file. Git is that witness: the
    baseline at REF is what the branch inherited, and a count above it is new
    amnesty being claimed in this diff. Lowering is always allowed, that is debt
    being paid. Dropping a code entirely is refused too — a removed key forgives
    the rule outright and reads, in a diff, like tidying.

    Exit 0 when the file only ratchets down, 1 on any increase or removal, 2 when
    REF cannot be read (unknown ref, shallow clone) — absent is not innocent.
    """
    import json
    import subprocess

    rel = BASELINE_PATH.relative_to(REPO)

    def _show(spec):
        p = subprocess.run(["git", "show", f"{spec}:{rel.as_posix()}"], cwd=REPO,
                           capture_output=True, text=True)
        return p.stdout if p.returncode == 0 else None

    # CI checks out at depth 1, so `origin/main` is simply ABSENT on a PR — the
    # one context where this ratchet means anything. Shipped without this, the
    # check exited 2 on every pull request: a blocking gate that could not pass,
    # which is the mirror image of the gate-that-cannot-fail this repo keeps
    # finding. Fetch the base ref before concluding it is unreachable.
    prior_raw = _show(ref)
    if prior_raw is None:
        remote_ref = ref.split("/", 1)[1] if ref.startswith("origin/") else ref
        subprocess.run(["git", "fetch", "--quiet", "--depth", "1",
                        "origin", remote_ref], cwd=REPO, capture_output=True)
        prior_raw = _show(ref) or _show("FETCH_HEAD")
    if prior_raw is None:
        print(f"ERROR: cannot read {rel} at {ref}, and fetching it failed. The "
              f"ratchet has no witness without it, and passing on an unreadable "
              f"baseline would be exactly the amnesty this check closes. In CI "
              f"this means the job needs `fetch-depth: 0` or network access to "
              f"origin.", file=sys.stderr)
        return 2

    if not BASELINE_PATH.exists():
        print(f"ERROR: {rel} exists at {ref} but not here — removing the baseline "
              f"forgives every rule in it.", file=sys.stderr)
        return 1

    prior = json.loads(prior_raw).get("counts", {})
    now = json.loads(BASELINE_PATH.read_text()).get("counts", {})

    raised = [(c, prior[c], now[c]) for c in prior if c in now and now[c] > prior[c]]
    dropped = sorted(set(prior) - set(now))
    lowered = [(c, prior[c], now[c]) for c in prior if c in now and now[c] < prior[c]]
    added = sorted(set(now) - set(prior))

    # EXAMINED must carry exactly ONE number — run_checks.py's EXAMINED_RE
    # takes only the first \d+ after the prefix, and the two-number form
    # printed here (`len(prior)` first, `len(now)` second) meant a genuinely
    # populated "here" count was silently reported as `len(prior)`. On a fresh
    # branch with no prior baseline entries (len(prior)==0, e.g. before the
    # file existed at origin/main) this check — BLOCKING with min_items:1 —
    # read as EXAMINED: 0 and failed vacuity, even though the comparison below
    # is real and covers every rule code either snapshot names. Report the
    # union of codes actually compared as the single honest whole-check count,
    # and put the prior/now breakdown in separate prose that does not start
    # with "EXAMINED:".
    all_codes = sorted(set(prior) | set(now))
    print(f"research-contract baseline ratchet — {rel} vs {ref}")
    print(f"  EXAMINED: {len(all_codes)}")
    print(f"  ({len(prior)} baselined rule(s) at {ref}, {len(now)} here)")
    for c, b, n in lowered:
        print(f"  ok      {c}: {b} -> {n} (debt paid down)")
    for c in added:
        # New keys are allowed: a rule can start failing for reasons that predate
        # this branch, and refusing them would mean the baseline could never
        # record a newly-discovered inheritance. They are printed, not passed
        # over, because "new inherited debt" and "debt I just created" look the
        # same in a file and differ only in the PR that carries them.
        print(f"  NEW     {c}: {now[c]} — newly baselined; confirm this is inherited, "
              f"not introduced by this branch")
    for c, b, n in raised:
        print(f"  FAIL    {c}: {b} -> {n} — {n - b} additional violation(s) forgiven")
    for c in dropped:
        print(f"  FAIL    {c}: removed (was {prior[c]}) — the rule is forgiven outright")

    if raised or dropped:
        print(f"\n{len(raised) + len(dropped)} baseline entr(ies) forgive more than "
              f"{ref} did. Remediate the violations, or say in the PR why the "
              f"amnesty is correct and have it reviewed — do not raise a number to "
              f"make a batch pass.")
        return 1
    print(f"\nRESULTS: baseline ratchets down only ({len(lowered)} lowered, "
          f"{len(added)} newly recorded)")
    return 0


def audit(session=None, allmode=False, capture=None, use_baseline=True):
    cx = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    scope = "" if allmode else " AND created_by_session = ?"
    sargs = () if allmode else (session,)
    issues, notes = [], []

    def fail(code, msg, count=1):
        issues.append((code, msg, count))

    def ok(code, msg):
        notes.append(f"{code}: PASS — {msg}")

    # --- R1 Co-1 / Co-2 lived-experience pass -------------------------------------------
    # HARDENED (adversarial pass 2026-07-24): the original accepted a SUBSTRING match in
    # query_text as proof of a Co-1 pass. It therefore PASSED a run with 0 co1/co2-targeted
    # searches and 0 co1/co2 sources admitted, because one unrelated query happened to contain
    # the words "lived experience". The project's most important doctrinal commitment had the
    # weakest check. Structural evidence is now REQUIRED; the phrase match is a hint only.
    co1 = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE target_evidence_type IN "
                    f"('co1','co2'){scope}", sargs)[0][0]
    co1_src = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE evidence_type IN "
                        f"('co1','co2'){scope}",
                    sargs)[0][0]
    co1_waiver = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE "
                           f"COALESCE(findings_note,'') LIKE '%CO1-NOT-APPLICABLE%'{scope}",
                       sargs)[0][0]
    co1_txt = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE ("
                        + " OR ".join(["LOWER(query_text) LIKE ?"] * len(CO1_HINTS))
                        + f"){scope}", tuple(f"%{h}%" for h in CO1_HINTS) + sargs)[0][0]
    if co1 == 0 and co1_src == 0 and co1_waiver == 0:
        fail("R1", f"NO Co-1/Co-2 pass: 0 searches targeted co1/co2 and 0 co1/co2 sources "
                   f"admitted ({co1_txt} query text merely MENTIONS lived experience — that is "
                   f"not a Co-1 pass). Co-1 is CO-PRIMARY with T1 (CRPD Art 4.3); "
                   f"multilingual-research Step 1 is 'first; no exceptions'. Run a DPO/"
                   f"lived-experience retrieval, or record 'CO1-NOT-APPLICABLE: <reason>' in "
                   f"findings_note.")
    else:
        ok("R1", f"{co1} co1/co2-targeted searches, {co1_src} co1/co2 sources, "
                 f"{co1_waiver} reasoned waivers")

    # --- R2 citation mining on admitted anchors -----------------------------------------
    # HARDENED: the original was satisfied by a single stub row with mining_direction<>'none'
    # and never consulted citation_mining at all — "did you mine?" did not look at the mining
    # table. Now requires actual citation_mining rows, proportionate to admitted anchors.
    admitted = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE tier BETWEEN 1 AND 3"
                         f"{scope}", sargs)[0][0]
    mined_rows = _rows(cx, f"SELECT COUNT(*) FROM citation_mining WHERE 1=1"
                           f"{scope}", sargs)[0][0]
    mined_dir = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE mining_direction IS NOT "
                          f"NULL AND mining_direction <> 'none'{scope}", sargs)[0][0]
    if admitted > 0 and mined_rows == 0:
        fail("R2", f"{admitted} tier-1..3 anchors admitted but ZERO citation_mining rows "
                   f"(mining_direction<>'none' on {mined_dir} search rows is NOT evidence of "
                   f"mining — the mining register is the evidence). Mine backward AND forward, "
                   f"depth 2-3, per citation-miner.")
    elif admitted > 0 and mined_rows < max(1, admitted // R2_MINING_PER_ANCHORS):
        fail("R2", f"only {mined_rows} citation_mining rows for {admitted} anchors — mining is "
                   f"token rather than systematic (expect >= {max(1, admitted // R2_MINING_PER_ANCHORS)}).")
    else:
        ok("R2", f"{mined_rows} citation_mining rows for {admitted} anchors")

    # --- R3 clause citation on quantified regulatory values -----------------------------
    uncited = _rows(cx, f"SELECT ref_id FROM evidence_sources WHERE tier >= 4 AND "
                        f"(article_number IS NULL OR article_number='') AND "
                        f"(pages IS NULL OR pages='') AND "
                        f"COALESCE(notes,'') NOT LIKE '%UNVERIFIED-QUANT%'"
                        f"{scope}", sargs)
    if uncited:
        fail("R3", f"{len(uncited)} regulatory-stratum source(s) carry values with no clause/"
                   f"section/page AND no [UNVERIFIED-QUANT] flag: "
                   f"{', '.join(r[0] for r in uncited[:5])}", len(uncited))
    else:
        ok("R3", "all regulatory sources clause-cited or flagged [UNVERIFIED-QUANT]")

    # --- R4 combinatorial dimension ------------------------------------------------------
    # HARDENED: the original counted a query containing the substring "disabilit" as
    # "combinatorial". On the run that motivated this script that scored 21/52 PASS while ZERO
    # queries had actually crossed a population code, access need, ICF code or axis. Word
    # presence is not study design. Now requires a REAL crossing: either an explicit population/
    # ICF/axis identifier in the query, or a population linkage produced by the batch.
    total = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE 1=1{scope}", sargs)[0][0]
    # HARDENED TWICE. v1 counted the substring "disabilit" as combinatorial. v2 matched population
    # codes in query_text — also unsound, because SQLite LIKE is case-INSENSITIVE and the codes are
    # short ASCII: 'COM' matches "accommodate", 'AUT' matches "autistic", 'BAR' matches
    # "bariatric", 'ID' matches almost anything. Text can never prove a crossing. v3 therefore
    # requires STRUCTURAL evidence: a population linkage actually produced by the batch.
    linked = 0
    if _rows(cx, "SELECT COUNT(*) FROM sqlite_master WHERE name='evidence_population_match'"
             )[0][0]:
        linked = _rows(cx, f"SELECT COUNT(*) FROM evidence_population_match WHERE 1=1"
                           f"{scope}", sargs)[0][0]
    # A LINKAGE REQUIRES SOMETHING TO LINK. `evidence_population_match` keys on an admitted
    # source, so a batch that admitted nothing cannot produce one -- and until 2026-09-17 R4
    # read that as "ZERO population linkages" and failed it. The subject of this rule is
    # ADMITTED EVIDENCE, not searches; a zero-yield batch has no subject, which is different
    # from having one and failing to cross it. Counted here rather than reusing the R9 block's
    # figure because that is computed further down.
    n_admitted = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE 1=1"
                           f"{scope}", sargs)[0][0]
    if total and linked == 0 and n_admitted:
        fail("R4", f"{total} searches produced ZERO population linkages "
                   f"(evidence_population_match) over {n_admitted} admitted source(s). Cells are "
                   f"(parameter x lens) since migration 071 — NOT (item x population), the "
                   f"traversal D-0184 rejected: a search that merely mentions a population in "
                   f"prose is not a crossing — link admitted evidence to the population(s)/axis "
                   f"it actually speaks to.", total)
    elif total and linked == 0:
        ok("R4", f"NOTHING TO CROSS: {total} search(es) logged and 0 sources admitted, so there "
                 f"is no admitted evidence to link to a population. A zero-yield batch fails to "
                 f"cross nothing (R14)")
    else:
        ok("R4", f"{linked} population linkages produced across {total} searches")

    # --- R5 non-English not down-tiered --------------------------------------------------
    # MOVED FROM SEARCH TARGETS TO ADMISSIONS 2026-10-02 (process-gap remediation plan WP12,
    # I4). Until then this read search_executions and failed a non-English search whose
    # target_evidence_type was 'grey'. That tested a proxy -- what a search SOUGHT -- and not
    # the harm the rule names, which happens when a source is FILED: a non-English journal
    # article filed evidence_type='grey' renders ○ where it is owed ● (governance/
    # tier-system.md). The proxy was wrong both ways. It never saw a journal article filed
    # grey from an untargeted or English-targeted search, and it pushed batch 23 to retarget
    # two searches that genuinely sought grey material to 'co1' to clear the gate (session
    # record §2.5), falsifying the column it read.
    #
    # The subject is the batch's non-English ADMISSIONS. One fails when it is filed grey AND
    # carries a mark of journal publication: source_type 'journal_article' (a member of the
    # column's own CHECK, asserted against dbcore.check_values below rather than trusted from
    # this line), a journal_name, or a DOI. Language is read from lang_detected, then the
    # older `language` column, the order db.py's own sort uses; case-insensitively, as the
    # 2026-07-25 fix to the search form of this rule established ('EN' and 'en' both occur).
    #
    # WHAT THIS CANNOT TELL, stated so the PASS line is not strengthened. A DOI or a journal
    # name marks publication, not peer review: a non-English grey report or thesis carrying a
    # repository DOI, or a letter printed in a journal, fails here although grey may be right.
    # The payload settles that and this gate cannot, so the FAIL names the waiver beside the
    # correction. An admission with no language recorded at all is read as English and NOT
    # examined; it is counted and REPORTED rather than passed over in silence.
    # The search-target count survives as a REPORTED line only: a target classifies what was
    # sought, and a non-English search may honestly seek grey material.
    if "journal_article" not in dbcore.check_values(cx, "evidence_sources", "source_type"):
        raise SystemExit("R5: 'journal_article' is no longer in evidence_sources.source_type's "
                         "CHECK. This rule is a caller of that vocabulary (CLAUDE.md rule 4); "
                         "re-derive the journal-publication mark before trusting R5 again.")
    lang = "upper(COALESCE(lang_detected, language, 'EN'))"
    n_non_en = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE {lang} <> 'EN'"
                         f"{scope}", sargs)[0][0]
    n_no_lang = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE "
                          f"lang_detected IS NULL AND language IS NULL{scope}", sargs)[0][0]
    downtiered = _rows(cx, f"SELECT ref_id, {lang}, COALESCE(source_type, '-') "
                           f"FROM evidence_sources WHERE {lang} <> 'EN' "
                           f"AND evidence_type = 'grey' AND (source_type = 'journal_article' "
                           f"OR COALESCE(journal_name, '') <> '' OR COALESCE(doi, '') <> '')"
                           f"{scope} ORDER BY ref_id", sargs)
    grey_sought = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE "
                            f"upper(language) <> 'EN' AND target_evidence_type = 'grey'{scope}",
                        sargs)[0][0]
    r5_reported = (f"REPORTED, not asserted: {grey_sought} non-English search(es) targeted "
                   f"'grey' (a target is what was sought, not how a source was filed); "
                   f"{n_no_lang} admission(s) with no language recorded, read as English and "
                   f"not examined")
    if downtiered:
        fail("R5", f"{len(downtiered)} of {n_non_en} non-English admission(s) filed "
                   f"evidence_type 'grey' while carrying a mark of journal publication "
                   f"(source_type journal_article, a journal name or a DOI): "
                   + ", ".join(f"{r} ({lg}, {st})" for r, lg, st in downtiered[:8])
                   + ". Non-indexation in PubMed/Scopus is an INDEXING fact, not a quality "
                     "fact: re-file a peer-reviewed article with db.py amend-source --field "
                     "evidence_type. If the source genuinely is grey (a report with a "
                     "repository DOI, a letter), record that as a reasoned waiver in the PR. "
                   + r5_reported, len(downtiered))
    else:
        ok("R5", (f"EXAMINED: {n_non_en} non-English admission(s); none filed grey with a "
                  f"journal_article type, a journal name or a DOI" if n_non_en else
                  "EXAMINED: 0 non-English admissions, so this asserts nothing")
                 + ". " + r5_reported)

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
    # FLOOR REMOVED 2026-10-02 (process-gap remediation plan WP12, I3); COUNT INTEGRITY KEPT.
    # This asserted one registered candidate per 25 screened results. Both terms of that ratio
    # are typed by the party being judged, and batch 23 showed the floor gamed in both
    # directions in one session (session record §2.3-2.4): results_screened was set equal to
    # results_found on every web search, inflating the denominator, and the floor was then met
    # by staging seven more already-screened documents after the gate reported short. A floor
    # that is cleared by recording rather than by searching certifies nothing about whether
    # material stayed in prose.
    #
    # R7'S SUBSTANTIVE ENFORCERS ARE ELSEWHERE, and this rule no longer pretends otherwise:
    #   * RC1, provenance_artefact_audit (blocking): a candidate is checked against the bytes
    #     its search actually returned, so a staged candidate is rooted in a payload;
    #   * adversarial standing subject 1, "Harm findings against the rows that claim them"
    #     (skills/adversarial-research_SKILL.md, "Standing subjects of every adversarial
    #     pass"): whether harm and off-slug material REACHED a flagged row or a candidate is
    #     not machine-decidable, and that pass is where it is decided.
    #
    # What stays asserted is the arithmetic the search log must obey whoever typed it: no
    # search screened more results than it found, and none admitted more than it screened.
    # One known route to the second: link-admission raises results_admitted on an existing
    # row (raise-only, owner ruling 2026-09-26) and no verb amends results_screened, so a
    # search whose screened count was under-logged fails here with no correction path: the
    # PR states which count is wrong, and `--all` carries it as baselined debt. That is a
    # true inconsistency in the record, not a false alarm.
    #
    # REPORTED, NEVER ASSERTED: the candidate and harm counts. Printing a number the check
    # never tested is CLAUDE.md §5(a) at message level -- it is how the exec-32 filing gap
    # stayed invisible while this line read PASS (softened deliberately 2026-09-03). Do NOT
    # restore a confident wording, or a floor, without a predicate behind it that the party
    # being judged cannot satisfy by typing.
    harm = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE harm_finding=1{scope}",
                 sargs)[0][0]
    cand = _rows(cx, f"SELECT COUNT(*) FROM search_candidates WHERE 1=1{scope}", sargs)[0][0]
    screened = _rows(cx, f"SELECT COALESCE(SUM(results_screened),0) FROM search_executions "
                         f"WHERE 1=1{scope}", sargs)[0][0]
    miscounted = _rows(cx, f"SELECT exec_id, results_found, results_screened, results_admitted "
                           f"FROM search_executions WHERE (results_screened > results_found "
                           f"OR results_admitted > results_screened){scope} ORDER BY exec_id",
                       sargs)
    r7_reported = (f"REPORTED, not asserted: {cand} candidate(s) registered for {screened} "
                   f"screened; {harm} row(s) carry harm_finding=1. Whether harm and off-slug "
                   f"material reached a row is adversarial standing subject 1")
    if miscounted:
        fail("R7", f"{len(miscounted)} of {total} search(es) carry counts that contradict "
                   f"each other (results_screened > results_found, or results_admitted > "
                   f"results_screened): "
                   + ", ".join(f"exec {e} (found {f}, screened {s}, admitted {a})"
                               for e, f, s, a in miscounted[:8])
                   + ". A search cannot screen more than it found or admit more than it "
                     "screened; the log is append-only, so say in the PR which count is "
                     "wrong and why. " + r7_reported, len(miscounted))
    else:
        ok("R7", (f"EXAMINED: {total} search(es); every one screened no more than it found "
                  f"and admitted no more than it screened" if total else
                  "EXAMINED: 0 searches, so this asserts nothing")
                 + ". " + r7_reported)

    # --- R8 empties kept + APPEND-ONLY integrity -------------------------------------------
    # HARDENED: the original could never fail — it printed a count and passed. Deleting the
    # ENTIRE zero-yield record (destroying the honesty evidence) still returned PASS. The log is
    # append-only by design, so deletion is detectable as gaps between max(exec_id) and COUNT(*).
    empties = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE results_found = 0 AND "
                        f"deferred_reason IS NULL{scope}", sargs)[0][0]
    mx, cnt = _rows(cx, "SELECT COALESCE(MAX(exec_id),0), COUNT(*) FROM search_executions")[0]
    if mx > cnt:
        fail("R8", f"search_executions is APPEND-ONLY but max(exec_id)={mx} exceeds COUNT={cnt}: "
                   f"{mx - cnt} row(s) were DELETED. Zero-yield and deferred searches are the "
                   f"honesty record — 'we tried hard and nothing surfaced' — and must never be "
                   f"removed or back-filled.")
    else:
        # STATED HONESTLY 2026-10-02 (process-gap remediation plan WP12, I2). R8's hook text
        # obliges a prior written BEFORE the search runs, and that stays an instruction. Nothing
        # here, or anywhere in the database, can witness it: log-search writes the prior in the
        # same row and the same call as the results, so the row exists only after the search
        # did, and dbcore.now() stamps to the minute. Batch 23 wrote its whole log in one pass
        # after admission (session record §2.3), and this line read PASS. The adversarial pass
        # and the session transcript are the only witnesses, joined by the tool-call ledger
        # (plan WP14) for a search it records; a two-phase log (plan WP15) is what would let a
        # predicate here read precedence. Do not let this line claim it until one does.
        ok("R8", f"{empties} zero-yield searches retained; log intact (no deleted rows). "
                 f"NOT TESTED: that each prior preceded its search -- log-search writes the "
                 f"prior with the results, after the search ran, and dbcore.now() is "
                 f"minute-precision; the adversarial pass and the transcript (and the "
                 f"tool-call ledger, for a search it records) are its only witnesses")

    # --- R9 duplicate DOI ------------------------------------------------------------------
    # Scoped to THIS batch: did this batch introduce a duplicate? (Corpus-wide duplicate debt is
    # test_db_integrity D01's job; a gate that is permanently red for inherited reasons trains
    # people to ignore it — which is the exact failure mode this script exists to prevent.)
    dupes = _rows(cx, f"SELECT e.doi, COUNT(*) c FROM evidence_sources e WHERE e.doi IS NOT NULL "
                      f"AND e.doi <> '' AND e.doi IN (SELECT doi FROM evidence_sources WHERE "
                      f"doi IS NOT NULL AND doi <> ''"
                      f"{scope}) "
                      f"GROUP BY e.doi HAVING c > 1", sargs)
    if dupes:
        fail("R9", f"{len(dupes)} DOI(s) admitted by THIS batch already exist in the corpus — "
                   f"pre-check DOIs and cross-file the existing ref_id (`db.py "
                   f"link-source-slug`) instead of creating a "
                   f"second row: {', '.join(str(d[0]) for d in dupes[:5])}", len(dupes))
    else:
        ok("R9", "this batch introduced no duplicate DOIs")

    # --- R9a / R9b: the stash R9 could not see (OD-5) --------------------------------------
    # R9 above compares evidence_sources against ITSELF. source_locators -- 835 held
    # identifiers, 441 of them DOIs -- was invisible to it, so the gate certified "no
    # duplicate" against about 2% of what this project actually holds. That is OD-5, and
    # CLAUDE.md 4 records it as a known live defect.
    #
    # The NAIVE widening is wrong and was rejected on evidence 2026-08-23: every DOI then
    # held in both tables (4 of them) carried the SAME ref_id in each, because promoting a
    # stash lead into the corpus under its held id is the pipeline WORKING. A check that
    # failed on mere overlap would have failed all four correct promotions, and would fail
    # the next batch's promotion of REF-00327/576/577/579 as well.
    #
    # The real defect is one source wearing two identities, and it runs in both directions:
    #   R9a  this batch admitted DOI D as ref_id Y, but the stash already holds D as X != Y
    #   R9b  this batch admitted ref_id R, but the stash holds R against a DIFFERENT DOI
    # R9b is not hypothetical: there is no next_ref_id allocator (CLAUDE.md 4), so a batch
    # that mints below the stash high-water mark collides with a held identifier in silence.
    escope = "" if allmode else " AND e.created_by_session = ?"

    # SUBJECT COUNT FIRST. Adversarial pass 2026-08-23 found R9a/R9b printing a bare
    # "PASS" for a session that admitted nothing -- CLAUDE.md 2(a), a gate that passes
    # having examined nothing, reproduced inside the fix written for a gate that examined
    # the WRONG set. Both rules now carry their subject count, and say so when it is zero.
    # WIDENED TO URL 2026-09-17. The subject was DOI-bearing admissions ALONE, so a batch
    # whose sources legitimately have no DOI -- every Co-1, DPO, grey and regulatory source
    # there is -- fell into the zero-branch below and was told it had admitted nothing and
    # was "missing its locators". Both halves were false for batch 09, which admitted two
    # sources each carrying a URL. The stash holds 402 URLs against 465 DOIs (derive it:
    # SELECT COUNT(*) FROM source_locators WHERE COALESCE(url,'') <> ''), so the check
    # could be performed and simply was not. This is R9b's own 2026-08-23 widening applied
    # to R9a: CLAUDE.md §4's warning is not DOI-conditional, and neither is identity.
    n_doi = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources e WHERE COALESCE(e.doi,'') <> ''"
                      f"{escope}", sargs)[0][0]
    n_url = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources e WHERE COALESCE(e.doi,'') = '' "
                      f"AND COALESCE(e.url,'') <> ''{escope}", sargs)[0][0]
    n_adm = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources e WHERE 1=1{escope}", sargs)[0][0]
    # DID THIS SESSION LOOK? The difference between "admitted nothing AFTER SEARCHING" and
    # "did nothing" is the whole of the zero-yield question, and the search log is what
    # settles it -- derived, not a sentinel row anyone has to remember to write. R14 is
    # explicit that a zero-yield search is "a COMPLETED unit of work", so a batch that
    # searched honestly and admitted nothing is COMPLIANT doctrine; before 2026-09-17 it was
    # non-compliant machinery, and once research_dod_session became blocking that combination
    # would have stopped CI for a batch that did exactly what the contract asks.
    n_search = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE 1=1"
                         f"{' AND created_by_session = ?' if not allmode else ''}", sargs)[0][0]

    # RETIRED STASH ROWS ARE NOT A HELD IDENTITY, AND EXCLUDING THEM IS THE WHOLE POINT
    # OF THE TOMBSTONE. Migration 076 retains the thirteen refs the 2026-09-13 clear deleted
    # as `source_locators` rows with status RETIRED, precisely so their ref_ids are never
    # reissued. R9a's remedy -- "cross-file the held id instead of minting a second" -- is
    # therefore IMPOSSIBLE against one: cross-filing to REF-00973 would reuse a retired
    # identifier, which is the one thing 076 exists to prevent. Without this clause the two
    # requirements contradict each other for exactly the set the clear produced, and the
    # re-run the same ruling ordered cannot admit a single cleared source by any route.
    # Found by batch 08, whose cell (TERM-001 ramp gradient) has REF-00979 and REF-00980 --
    # the two most on-point ramp-slope papers in the prior corpus -- among the tombstones.
    # R9b IS DELIBERATELY NOT CHANGED. It joins on ref_id, not DOI, and a tombstone blocking
    # a batch from minting a ref_id the stash still holds is that rule working as intended.
    split = _rows(cx, f"SELECT e.ref_id, sl.ref_id, e.doi FROM evidence_sources e "
                      f"JOIN source_locators sl ON LOWER(TRIM(sl.doi)) = LOWER(TRIM(e.doi)) "
                      f"WHERE COALESCE(e.doi,'') <> '' AND COALESCE(sl.doi,'') <> '' "
                      f"AND COALESCE(sl.status,'') <> 'RETIRED' "
                      f"AND sl.ref_id <> e.ref_id{escope}", sargs)

    # A URL IS A HELD IDENTITY ONLY WHEN IT IDENTIFIES EXACTLY ONE SOURCE, and that
    # restriction is the whole design rather than a refinement of it. Measured 2026-09-17
    # before this was written: the BSI catalogue page for BS 8300 is held against SEVEN
    # different ref_ids, the ISO and DIN catalogue pages and the ADA standards page against
    # five each. Those are LANDING PAGES -- one web address serving a whole standards family
    # -- and sharing one is correct, not a defect. A naive url join would have fired on every
    # one of them and told the operator to "cross-file the held id", which for two genuinely
    # different standards is wrong advice that destroys an identity rather than repairing one.
    # So the set is derived, never assumed: a url the stash resolves to a single ref_id is an
    # identity; a url it resolves to several is a catalogue, and proves nothing either way.
    # Derive the split rather than trusting this comment:
    #   SELECT LOWER(TRIM(url)), COUNT(DISTINCT ref_id) n FROM source_locators
    #   WHERE COALESCE(url,'') <> '' GROUP BY 1 HAVING n > 1;
    urlnorm = "RTRIM(LOWER(TRIM({}.url)), '/')"
    singleton = (f"SELECT {urlnorm.format('s2')} FROM source_locators s2 "
                 f"WHERE COALESCE(s2.url,'') <> '' AND COALESCE(s2.status,'') <> 'RETIRED' "
                 f"GROUP BY 1 HAVING COUNT(DISTINCT s2.ref_id) = 1")
    usplit = _rows(cx, f"SELECT e.ref_id, sl.ref_id, e.url FROM evidence_sources e "
                       f"JOIN source_locators sl ON {urlnorm.format('sl')} = {urlnorm.format('e')} "
                       f"WHERE COALESCE(e.url,'') <> '' AND COALESCE(sl.url,'') <> '' "
                       f"AND COALESCE(sl.status,'') <> 'RETIRED' "
                       f"AND sl.ref_id <> e.ref_id "
                       f"AND {urlnorm.format('sl')} IN ({singleton}){escope}", sargs)

    if split or usplit:
        both = [(a, b, d, "DOI") for a, b, d in split] + [(a, b, u, "URL") for a, b, u in usplit]
        fail("R9a", f"{len(both)} source(s) admitted under a ref_id that DIFFERS from the one "
                    f"the identifier stash already holds for the same identifier — one source, "
                    f"two identities. Cross-file the held id instead of minting a second: "
                    + "; ".join(f"{a} vs stash {b} ({k} {d})" for a, b, d, k in both[:5]),
             len(both))
    elif n_doi == 0 and n_url == 0:
        # THE TWO STATES THIS BRANCH USED TO CONFLATE. "Admitted nothing" and "admitted
        # sources that carry no comparable identifier" are different facts and only the
        # first is vacuity; the old message asserted the second was the first, and told a
        # batch with two well-located sources that it was "missing its locators".
        if n_adm:
            fail("R9a", f"NOTHING IN SCOPE — {n_adm} source(s) admitted and not one carries a "
                        f"DOI or a URL, so no identifier exists to cross-check against the "
                        f"stash. That is not a locator problem to be waived: a source with no "
                        f"resolvable identifier at all cannot be cross-filed, deduplicated or "
                        f"re-retrieved by anyone. Give each admission its locator (R10).")
        elif n_search:
            # THE ZERO-YIELD BATCH, and it is a legitimate outcome rather than a hole.
            # The session ran searches and admitted nothing, which R14 calls a completed
            # unit of work. There is genuinely no identifier to cross-check, and saying so
            # is not the vacuity this rule guards against -- the guard is preserved by the
            # branch below, which still fires when NOTHING was logged either.
            ok("R9a", f"NOTHING TO CROSS-CHECK, and that is an honest result: {n_search} "
                      f"search(es) logged, 0 admissions. A zero-yield batch has no identifier "
                      f"to collide with the stash (R14: a zero-yield search is a completed "
                      f"unit of work)")
        else:
            fail("R9a", "NOTHING IN SCOPE — this batch admitted no sources AND logged no "
                        "searches, so nothing was examined and nothing was attempted. That is "
                        "an untouched or misnamed session, not a zero-yield one: check the "
                        "session id is the bare stem the DB stores (CLAUDE.md §7).")
    else:
        ok("R9a", f"{n_doi} admitted DOI(s) and {n_url} URL-only admission(s) checked against "
                  f"the stash; none held under a different ref_id")

    # R9b WIDENED 2026-08-23. It compared DOIs only, so it reached 441 of 835 stash rows and
    # was blind to the other 394 -- yet CLAUDE.md 4's warning ("mint above the high-water mark
    # or you will collide with a held identifier") is not DOI-conditional. Comparing every
    # identifier the stash carries reaches 751 of 835. A row with NO identifier at all (84)
    # cannot be adjudicated either way and is deliberately out of reach, not silently included.
    ID_COLS = ("doi", "pmid", "pmcid", "isbn", "issn", "standard_number")
    conflict = " OR ".join(
        f"(COALESCE(e.{c},'') <> '' AND COALESCE(sl.{c},'') <> '' "
        f"AND LOWER(TRIM(sl.{c})) <> LOWER(TRIM(e.{c})))" for c in ID_COLS)
    collide = _rows(cx, f"SELECT e.ref_id, COALESCE(e.doi, e.pmid, e.isbn, e.issn, "
                        f"e.standard_number), COALESCE(sl.doi, sl.pmid, sl.isbn, sl.issn, "
                        f"sl.standard_number) FROM evidence_sources e "
                        f"JOIN source_locators sl ON sl.ref_id = e.ref_id "
                        f"WHERE ({conflict}){escope}", sargs)
    if collide:
        fail("R9b", f"{len(collide)} ref_id(s) admitted by this batch collide with a HELD "
                    f"identifier in source_locators that identifies a DIFFERENT source — mint "
                    f"above `db.py next-id ref`, which computes the high-water mark "
                    f"as the UNION of every table holding a ref_id -- NOT the stash alone: "
                    + "; ".join(f"{r} admitted {a}, stash holds {b}" for r, a, b in collide[:5]),
             len(collide))
    elif n_adm == 0 and n_search:
        ok("R9b", f"NOTHING TO COLLIDE, and that is an honest result: {n_search} search(es) "
                  f"logged, 0 admissions. A zero-yield batch mints no ref_id, so none can "
                  f"collide with a held identifier (R14)")
    elif n_adm == 0:
        fail("R9b", "NOTHING IN SCOPE — this batch admitted no sources AND logged no searches, "
                    "so the identifier collision check examined nothing and nothing was "
                    "attempted. An untouched or misnamed session, not a zero-yield one.")
    else:
        ok("R9b", f"{n_adm} admitted ref_id(s) checked against the stash across "
                  f"{len(ID_COLS)} identifier types; no collision")

    # --- R10 locator re-retrieval ----------------------------------------------------------
    # HARDENED: the original accepted ANY non-empty locator field and never checked whether the
    # locator actually RESOLVED — 77 VERIFIED sources with unresolved DOIs passed silently.
    unver = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE verification_status='VERIFIED'"
                      f" AND COALESCE(doi,'')='' AND COALESCE(url,'')='' AND COALESCE(pmid,'')=''"
                      f" AND COALESCE(verified_by_tool,'')=''"
                      f"{scope}", sargs)[0][0]
    unresolved = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE "
                           f"verification_status='VERIFIED' AND COALESCE(doi,'') <> '' AND "
                           f"COALESCE(doi_resolution_outcome,'') NOT IN ('RESOLVED','NO-MATCH')"
                           f"{scope}", sargs)[0][0]
    if unver:
        fail("R10", f"{unver} VERIFIED source(s) with no locator or verifying tool. Ladder "
                    f"DOI -> Crossref/PubMed -> publisher -> repository; a publisher block is "
                    f"not a terminal answer.", unver)
    elif unresolved:
        fail("R10", f"{unresolved} VERIFIED source(s) carry a DOI whose resolution was never "
                    f"recorded (doi_resolution_outcome unset). Holding a DOI string is not "
                    f"re-retrieval — resolve it and record the outcome.")
    else:
        ok("R10", "every VERIFIED source has a locator AND a recorded resolution outcome")

    # --- R10b unverified-status admission carrying a URL -----------------------------------
    # R10 above examines VERIFIED sources ONLY (its own comment, above). That is blind to the
    # condition that actually wakes the scheduled verify-urls cron: verify_urls.py:447-470
    # pools any source with `url<>'' AND verification_status IS NULL` and, for a non-empty
    # candidate set, writes a url_verification_runs row — a table NOT in
    # migration_reproducibility.EXEMPT_TABLES — then `.github/workflows/verify-urls.yml`
    # commits data/guidebook.db straight to main on its own schedule (cron: 0 06 1,15 * *).
    # `add-source` accepts a NULL --verification-status (db.py branches only on VERIFIED), so a
    # batch can admit exactly this row and pass every other rule. The next 1st/15th 06:00 UTC
    # fire then pushes a blob to main and reddens migration_reproducibility for every OPEN
    # DB-touching PR (2026-09-07 did this to PR #128; workplan/2026-09-10-road-to-batch-06.md
    # B3). Block the admission itself — the cron is owner decision #5 and is not this fix's to
    # edit (same workplan, STOP CONDITIONS #1).
    unverified_url = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE "
                               f"COALESCE(url,'') <> '' AND verification_status IS NULL"
                               f"{scope}", sargs)[0][0]
    # The subject: URL-bearing admissions. Without this the pass could not say whether it
    # had looked at anything, which is the whole of §5(a).
    n_url_bearing = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE "
                              f"COALESCE(url,'') <> ''"
                              f"{scope}", sargs)[0][0]
    if unverified_url:
        fail("R10b", f"{unverified_url} admitted source(s) carry a URL with verification_status "
                     f"left NULL. This is exactly the pool verify_urls.py's scheduled cron "
                     f"claims: the next 1st/15th 06:00 UTC fire will write a "
                     f"url_verification_runs row (not exempt from migration_reproducibility) "
                     f"and push a DB blob to main, reddening migration_reproducibility for "
                     f"every open DB-touching PR. Set --verification-status on add-source (even "
                     f"UNVERIFIED is a real value) before merge.", unverified_url)
    else:
        # SUBJECT COUNT, per this file's own DESIGN RULES and the R9a/R9b hardening
        # directly above: a bare PASS on a session that admitted nothing is CLAUDE.md
        # §5(a), and R10b shipped with exactly that on 2026-09-10.
        if not n_url_bearing:
            ok("R10b", "NOTHING IN SCOPE — this batch admitted no source carrying a URL, "
                       "so the cron's pool cannot have grown. EXAMINED: 0")
        else:
            ok("R10b", f"EXAMINED: {n_url_bearing} admitted source(s) carrying a URL; "
                       f"none left verification_status NULL")

    # --- R11 vocabulary provenance ---------------------------------------------------------
    noprov_scope = _rows(cx, f"SELECT COUNT(*) FROM term_aliases WHERE 1=1"
                       f"{scope}", sargs)[0][0]
    noprov = _rows(cx, f"SELECT COUNT(*) FROM term_aliases WHERE COALESCE(notes,'')=''"
                       f"{scope}", sargs)[0][0]
    if noprov:
        fail("R11", f"{noprov} alias(es) with no sourcing note. No back-translation: every alias "
                    f"needs its authoritative in-language basis or [UNVERIFIED-TERMS].", noprov)
    else:
        # EXAMINED, per CLAUDE.md §2(a). This printed "all vocabulary carries
        # in-language sourcing provenance" over ZERO aliases for batch 05 -- and
        # corpus-wide 856 of 2382 aliases have no note, so the sentence was not merely
        # uninformative, it was the opposite of the corpus truth. A scoped count must
        # state its scope.
        ok("R11", f"{noprov_scope} alias(es) written by this batch; all carry "
                  f"in-language sourcing provenance" if noprov_scope else
                  "EXAMINED: 0 aliases. This batch wrote none, so this asserts "
                  "nothing about the corpus")

    # R11's second half, added 2026-09-03: the D-0173 concept-vocabulary harvest.
    # The subject is THIS BATCH'S ADMISSIONS, not this session's writes — a later
    # session harvesting batch 05's nine sources satisfies the requirement, and
    # scoping on observed_terms.created_by_session would have called that a miss.
    # What this asserts is ONLY that every source the batch admitted carries at
    # least one observation. Whether the phrases harvested are the RIGHT ones is
    # not machine-decidable and is not claimed here; judgment adjudicates them
    # through term_adjudications, and the adversarial pass is where coverage is
    # argued. Do not "strengthen" this message: the weaker sentence is the true one.
    #
    # Why it exists at all, against §1's burden of proof: migration 068 shipped the
    # table, the writer AND a contract line ordering agents to harvest as they go,
    # and batch 05 admitted nine sources and harvested nothing. Nobody noticed until
    # someone counted the rows by hand a day later. Without this line the harvest is
    # a rule with no reader, which §1 calls the same defect as an unread field.
    unharvested = _rows(cx,
        "SELECT e.ref_id FROM evidence_sources e WHERE NOT EXISTS ("
        "SELECT 1 FROM observed_terms o WHERE o.ref_id = e.ref_id)" + escope, sargs)
    harvested = _rows(cx,
        "SELECT COUNT(*) FROM observed_terms o WHERE EXISTS ("
        "SELECT 1 FROM evidence_sources e WHERE e.ref_id = o.ref_id" + escope + ")",
        sargs)[0][0]
    if unharvested:
        fail("R11-harvest",
             "%d admitted source(s) with no observed_terms row: %s. D-0173 harvests the "
             "concept vocabulary AT EVIDENCE, in the source's own words: "
             "db.py observe-term --ref-id ... --surface-form ..." % (
                 len(unharvested), ", ".join(r[0] for r in unharvested[:8])),
             len(unharvested))
    else:
        ok("R11-harvest",
           "%d concept observation(s) across this batch's admissions; every admitted "
           "source carries at least one. Whether they are the RIGHT phrases is NOT "
           "tested here — judgment adjudicates them" % harvested if harvested else
           "EXAMINED: 0 sources. This batch admitted none, so this asserts nothing")

    # --- R16 / R16-adjudicate: every concept a source states a figure for is disposed of ---
    # Added 2026-10-02 for GAP-061 (plan: scratchpad/session_2026-10-01-research-batch-23/
    # process-gap-remediation-plan.md, WP11). R11-harvest above asserts that each admission
    # carries an observation and stops there, and so did the loop: nothing promoted a
    # harvested term to a parameter, every extraction was filed under the one parameter that
    # existed, and batch 23 passed this gate with not one of its observations adjudicated.
    #
    # SCOPE IS THE BATCH'S ADMISSIONS (escope), as in R11-harvest, never this session's
    # writes: a later session adjudicating batch 23's phrases discharges batch 23's debt,
    # and a judgement-only pilot is gated through the batch whose sources it re-reads. The
    # converse is the known gap: a session that adjudicates ANOTHER batch's observations is
    # not gated here on the terms it names. `--all` and the baseline ratchet see that.
    #
    # R16-adjudicate: an observation with NO term_adjudications row. Any row answers it --
    # one that names no term included. Divergent second rows are deliberate (adjudicate_term)
    # and change nothing here.
    whose = "the corpus's" if allmode else "this batch's"   # subject phrase, per scope
    unadjudicated = _rows(cx,
        "SELECT o.observation_id FROM observed_terms o "
        "JOIN evidence_sources e ON e.ref_id = o.ref_id "
        "WHERE NOT EXISTS (SELECT 1 FROM term_adjudications a "
        "WHERE a.observation_id = o.observation_id)" + escope
        + " ORDER BY o.observation_id", sargs)
    if unadjudicated:
        fail("R16-adjudicate",
             "%d of %d observation(s) on %s admissions carry no term_adjudications "
             "row: observation_id %s. A harvested phrase is not yet judged. Answer each with "
             "db.py adjudicate-term --observation-id N --outcome ... (an outcome that names "
             "no term is an answer), or db.py add-term --from-observation N for a concept "
             "new to the vocabulary" % (
                 len(unadjudicated), harvested, whose,
                 ", ".join(str(r[0]) for r in unadjudicated[:8])),
             len(unadjudicated))
    else:
        ok("R16-adjudicate",
           "EXAMINED: %d observation(s) on %s admissions; every one adjudicated"
           % (harvested, whose) if harvested else
           "EXAMINED: 0 observations on %s admissions, so this asserts nothing (an "
           "admission with no observation is R11-harvest's to fail)" % whose)

    # R16: a term NAMED by an adjudication of those observations that holds neither a
    # parameter (base_parameters, any status: a merged or retired parameter is a recorded
    # decision about the term) nor a declination (parameter_declinations, migration 101).
    # `a.term_id IS NOT NULL` is the schema's own pairing CHECK for the outcomes that name a
    # term, so the outcome vocabulary stays out of this file (CLAUDE.md rule 8) and
    # NAMES-EXISTING counts as well as NAMES-NEW: a phrase naming a term we already hold is
    # still a concept the source states a figure for. Every named term can be disposed of by
    # one call, add-parameter or decline-parameter, and neither refuses for want of anything
    # this batch must first do, so the rule does not hold red a batch that did its judging.
    # ONE EXCEPTION, stated rather than discovered: add-parameter refuses a term whose
    # canonical_en carries a value (db.py _VALUE_BEARING) and canonical_en has no amend
    # path, so such a term could be disposed of only by a declination that would be untrue.
    # add-term refuses those names, and no live term carries one; re-derive by matching
    # `select canonical_en from terms` against _VALUE_BEARING. Meeting one is a GAP to file.
    # THE PREDICATE IS WIDER THAN THE RULE'S TITLE. Nothing here can tell whether a source
    # states a figure for a named concept, so every named term must be disposed of, figure
    # or none. A disposition is per term and corpus-wide, so that costs one call per term
    # once, not one per batch.
    # WHAT THIS DOES NOT TEST, stated so the PASS line is not "strengthened": a figure stated
    # for a concept no observation records leaves no row here, and whether a parameter goes
    # on to carry an extraction is not read either.
    adj_join = ("FROM term_adjudications a "
                "JOIN observed_terms o ON o.observation_id = a.observation_id "
                "JOIN evidence_sources e ON e.ref_id = o.ref_id ")
    undisposed = _rows(cx,
        "SELECT DISTINCT a.term_id " + adj_join +
        "WHERE a.term_id IS NOT NULL "
        "AND NOT EXISTS (SELECT 1 FROM base_parameters p WHERE p.term_id = a.term_id) "
        "AND NOT EXISTS (SELECT 1 FROM parameter_declinations d WHERE d.term_id = a.term_id)"
        + escope + " ORDER BY a.term_id", sargs)
    n_named = _rows(cx, "SELECT COUNT(DISTINCT a.term_id) " + adj_join +
                    "WHERE a.term_id IS NOT NULL" + escope, sargs)[0][0]
    # The outcomes that name no term, grouped from the rows rather than listed here.
    unnamed = _rows(cx, "SELECT a.outcome, COUNT(*) " + adj_join +
                    "WHERE a.term_id IS NULL" + escope + " GROUP BY a.outcome "
                    "ORDER BY a.outcome", sargs)
    unnamed_txt = ("%d adjudication(s) name no term (%s)" % (
        sum(n for _o, n in unnamed), ", ".join("%s %d" % (o, n) for o, n in unnamed))
        if unnamed else "0 adjudications name no term")
    if undisposed:
        fail("R16",
             "%d of %d term(s) named by adjudications of %s observations hold "
             "neither a parameter nor a declination: %s. A concept a source states a figure "
             "for is filed against a parameter (db.py add-parameter --term-id T) or, if it is "
             "not a quantity under determination (an element, a lens term, a method), "
             "declined with its reason (db.py decline-parameter --term-id T --reason ...)" % (
                 len(undisposed), n_named, whose,
                 ", ".join(r[0] for r in undisposed[:8])),
             len(undisposed))
    else:
        ok("R16",
           ("EXAMINED: %d term(s) named by adjudications of %s observations; "
            "every one is a parameter or declined" % (n_named, whose) if n_named else
            "EXAMINED: 0 terms named by adjudications of %s observations, so "
            "this asserts nothing" % whose)
           + ". REPORTED, not asserted: %s. A figure stated for a concept never observed "
             "is NOT tested here — adversarial standing subject 4" % unnamed_txt)


    # --- R12 structured homes used ----------------------------------------------------------
    econ_words = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE ("
                           f"LOWER(COALESCE(findings_note,'')) LIKE '%cost%' OR "
                           f"LOWER(COALESCE(findings_note,'')) LIKE '%grant%' OR "
                           f"LOWER(COALESCE(findings_note,'')) LIKE '%bcr%'){scope}", sargs)[0][0]
    # HARDENED: threshold was "table is empty", so ONE row satisfied it permanently while any
    # amount of economic data stayed in prose. Now proportionate to the prose findings observed.
    econ_rows = _rows(cx, "SELECT COUNT(*) FROM economics_entries")[0][0]
    if econ_words and econ_rows < econ_words:
        fail("R12", f"{econ_words} search(es) carry economic findings in prose but only "
                    f"{econ_rows} economics_entries row(s) exist. Economic/case-study/value data "
                    f"belongs in economics_entries / case_studies / research_code_leads, not "
                    f"in prose notes.", econ_words)
    else:
        ok("R12", f"structured homes used (economics_entries={econ_rows} for {econ_words} "
                  f"prose findings)")

    # --- R13 POPULATION-OF-STUDY vs POPULATION-SERVED ---------------------------------------
    # LESSON (2026-07-25): the highest-frequency silent error in this session was admitting a
    # source for a population it did not study. Twice caught only because linkage was done by
    # hand: Jinno 2007 is a CHAMBER EMISSIONS test with no human participants, filed against COM;
    # Amos 2019 is a GENERAL-POPULATION autistic-TRAITS sample, filed against AUT. Both are
    # legitimate as PROXY evidence and dangerous as anything else. An admission with no population
    # match asserts, silently, that study population == served population.
    anchors = _rows(cx, f"SELECT ref_id FROM evidence_sources WHERE tier BETWEEN 1 AND 3"
                        f"{scope}", sargs)
    unmatched = [r[0] for r in anchors
                 if not _rows(cx, "SELECT 1 FROM evidence_population_match WHERE ref_id=?",
                              (r[0],))]
    if unmatched:
        fail("R13", f"{len(unmatched)} tier-1..3 source(s) admitted with NO population match row "
                    f"— silently asserting that the population studied is the population served: "
                    f"{', '.join(unmatched[:5])}. Grade each EXACT/PARTIAL/PROXY and write the "
                    f"mismatch note.", len(unmatched))
    else:
        # Whether a mismatch_note is TRUE against the payload it describes is standing
        # subject 2 of the adversarial pass -- skills/adversarial-research_SKILL.md,
        # "Standing subjects of every adversarial pass". Named here so the gate points
        # at a home that exists; the phrase was in this file's R7 comment for a day
        # while no such section did.
        ok("R13", f"all {len(anchors)} tier-1..3 admissions carry a population match "
                  f"ROW -- presence only. Nothing here reads match_grade or "
                  f"mismatch_note, so 'graded' was an overclaim and is gone")

    # --- R14 ZERO-YIELD MUST SAY WHY ---------------------------------------------------------
    # LESSON: a zero-yield search is only evidence of ABSENCE if the query was well-formed. Twice
    # this session an over-conjunctive PubMed query returned 0 and the honest reading was "wrong
    # query shape", not "no evidence exists" — PubMed AND-chains every term, so descriptive
    # multi-concept phrasings return nothing. Recording the empty without that distinction
    # silently converts a method failure into a finding of absence.
    bare_empty = _rows(cx, f"SELECT COUNT(*) FROM search_executions WHERE results_found = 0 AND "
                           f"deferred_reason IS NULL AND COALESCE(findings_note,'') = ''{scope}",
                       sargs)[0][0]
    if bare_empty:
        fail("R14", f"{bare_empty} zero-yield search(es) carry no findings_note. Keep the empty "
                    f"(R8) but say WHICH it is: query-shape failure, wrong index, or genuine "
                    f"absence. Only the last is evidence.", bare_empty)
    else:
        ok("R14", "every zero-yield search records why it was empty")

    # --- R15 A RESOLVED CANDIDATE MUST BE RE-DESCRIBED FROM THE SOURCE ------------------------
    # LESSON: a staged candidate's description is a HYPOTHESIS, not a finding. This session staged
    # "Amos et al. — sensory input as a barrier to autistic adults engaging in public and
    # occupational spaces — the direct built-environment claim". Resolving it showed that was
    # over-claimed: it is an SEM mechanism study in a general-population trait sample supplying no
    # design parameter. Unresolved, that description would have hardened into fact in the register.
    admitted_cands = _rows(cx, f"SELECT candidate_id, title FROM search_candidates WHERE "
                               f"disposition = 'ADMITTED' AND COALESCE(notes,'') NOT LIKE "
                               f"'%RESOLVED%'{scope}", sargs)
    if admitted_cands:
        fail("R15", f"{len(admitted_cands)} candidate(s) marked ADMITTED without a RESOLVED note "
                    f"re-describing them from the actual source. A candidate description is a "
                    f"hypothesis until the source is read; confirm or correct it on resolution.",
             len(admitted_cands))
    else:
        ok("R15", "resolved candidates are re-described from the source")

    # ---- baseline: legacy debt must not hold the gate permanently red ----------------------
    # A gate that is always red teaches people to ignore it — the precise failure this script
    # exists to prevent. In --all mode, pre-existing debt recorded in the baseline is reported
    # as INHERITED and does not fail the run; any INCREASE over baseline does.
    inherited = []
    if allmode and use_baseline and BASELINE_PATH.exists():
        import json
        base = json.loads(BASELINE_PATH.read_text()).get("counts", {})
        kept = []
        for code, msg, count in issues:
            b = base.get(code)
            if b is not None and count <= b:
                inherited.append(f"{code}: {count} (baseline {b}) — INHERITED DEBT, not a regression")
            else:
                kept.append((code, msg, count))
        issues = kept

    # ---- report ----------------------------------------------------------------------------
    scope_txt = "ALL SESSIONS" if allmode else f"session={session}"
    print("=" * 78)
    print(f"research_batch_dod — RESEARCH DEFINITION-OF-DONE — {scope_txt}")
    print("=" * 78)
    for n in notes:
        print(f"  {n}")
    for i in inherited:
        print(f"  ~ {i}")
    if issues:
        print("-" * 78)
        for code, msg, _c in issues:
            print(f"  ✗ {code}: {msg}")
        print("-" * 78)
        print(f"  NON-COMPLIANT: {len(issues)} rule(s) unmet.")
        print("  Per owner directive 2026-07-24: RESEARCH IS INVALID IF IT IS NOT COMPLIANT WITH")
        print("  OUR GOVERNANCE AND VERIFICATION TOOLS AND RULES AND ETHOS.")
        print("  Remediate, or record an explicit reasoned waiver in the PR before merge.")
        print("=" * 78)
        if capture is not None:
            capture.update({c: n for c, _m, n in issues})
        return 1
    print("-" * 78)
    print("  COMPLIANT — all research definition-of-done rules met.")
    print("=" * 78)
    return 0


def selftest():
    """Prove the checks fire.

    The synthetic corpus is built by CLONING THE LIVE SCHEMA (sqlite_master DDL) rather than
    hand-writing CREATE statements. v1 hand-wrote them, drifted the moment the checks were
    hardened, and the selftest began CRASHING instead of testing — the guard against the gate
    rotting had itself rotted, and only a manual re-run caught it. Cloning removes that class of
    failure entirely.
    """
    import tempfile
    global DB_PATH
    if not DB_PATH.exists():
        print("SELFTEST: SKIP — no live DB to clone schema from")
        return 0
    live = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    ddl = [r[0] for r in live.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL")]
    live.close()

    fd = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    cx = sqlite3.connect(fd.name)
    for stmt in ddl:
        try:
            cx.execute(stmt)
        except sqlite3.Error:
            pass  # skip anything with unmet deps; the gate degrades gracefully on missing tables
    T = "SELFTEST-SESSION"
    # A corpus that violates: R1 (no co1), R2 (no mining), R3 (uncited tier-6 value),
    # R4 (no population linkage), R6 (findings in deferred_reason), R8 (deleted row -> id
    # gap), R10 (VERIFIED, no locator), R11 (alias w/o provenance). Exec 1 below is a
    # non-English search targeted 'grey'; since 2026-10-02 that is R5's REPORTED line, not
    # its subject, and the R5 fixture further down asserts that it no longer counts.
    cx.execute("INSERT INTO search_executions (exec_id,slug,jurisdiction,language,"
               "target_evidence_type,query_text,engine,depth_method,mining_direction,"
               "results_found,results_screened,results_admitted,deferred_reason,backfill,"
               "created_by_session,created_at) VALUES (1,'s','ID','id','grey','q','web','scoping','none',"
               "5,5,0,'found things',0,?,'t')", (T,))
    cx.execute("INSERT INTO search_executions (exec_id,slug,language,query_text,engine,"
               "depth_method,mining_direction,results_found,results_screened,results_admitted,"
               "backfill,created_by_session,created_at) VALUES (3,'s','en','q','web','scoping','none',"
               "0,0,0,0,?,'t')", (T,))   # exec_id 2 absent => append-only violation for R8
    cx.execute("INSERT INTO evidence_sources (ref_id,tier,evidence_type,verification_status,"
               "notes,created_by_session) VALUES ('REF-ST1',6,'code','VERIFIED','250 lbf',?)", (T,))
    # A tier-1..3 anchor, so that "zero citation_mining rows" is actually an R2
    # VIOLATION. Added 2026-08-04: the corpus previously seeded only the tier-6
    # row above, so R2's `admitted > 0` precondition was never met and the rule
    # reported OK on a corpus its own comment claimed violated it. The old
    # `rc == 1`-only assertion could not see the difference; the per-rule
    # assertion added in the same commit surfaced it on the first run.
    cx.execute("INSERT INTO evidence_sources (ref_id,tier,evidence_type,verification_status,"
               "notes,created_by_session) VALUES ('REF-ST2',2,'sr_meta','VERIFIED','anchor',?)", (T,))
    cx.execute("INSERT INTO term_aliases (term_id,alias,language,alias_type,notes,created_at,"
               "created_by_session,updated_at,updated_by_session) "
               "VALUES ('TERM-001','x','id','TRANSLATION','','t',?,'t',?)", (T, T))
    # --- R9, R12, R15: implemented since inception, never once OBSERVED to fire -------------
    # (DR-2026-08-19 §12.0, F9.) Three of fifteen rules were asserted by nobody: the selftest
    # certified twelve and the corpus exercised twelve, so detection for these three could have
    # rotted to a no-op and every run would still have printed PASS. That is this repository's
    # signature failure -- a green gate that examined nothing -- reproduced inside the very
    # script written to prevent it. Each seed below is shaped to fire ONE rule and to leave the
    # others' arithmetic untouched.
    #
    # R9: two rows sharing a DOI, one from a PRIOR session, so the rule's batch-scoped subquery
    # finds this batch's row and the corpus-wide count reaches 2. Tier 6 keeps them out of R13
    # (tier 1..3 only); article_number keeps them out of R3 (tier >= 4 needs a clause cite);
    # verification_status left NULL keeps them out of R10 (VERIFIED only).
    cx.execute("INSERT INTO evidence_sources (ref_id,tier,evidence_type,doi,article_number,"
               "created_by_session) VALUES ('REF-ST3',6,'code','10.9999/dup','§5.2',?)", (T,))
    cx.execute("INSERT INTO evidence_sources (ref_id,tier,evidence_type,doi,article_number,"
               "created_by_session) VALUES ('REF-ST4',6,'code','10.9999/dup','§5.2',"
               "'PRIOR-SESSION')")
    # R9a: the stash holds this DOI under a DIFFERENT ref_id, so the batch has minted a
    # second identity for a source the project already had a lead on. Distinct DOI from
    # REF-ST3/ST4 so the original R9 does not also fire on it.
    cx.execute("INSERT INTO evidence_sources (ref_id,tier,evidence_type,doi,article_number,"
               "created_by_session) VALUES ('REF-ST5',6,'code','10.9999/split','§5.2',?)", (T,))
    cx.execute("INSERT INTO source_locators (ref_id,doi) VALUES "
               "('REF-STASH-A','10.9999/split')")
    # R9a NEGATIVE CASE: the same shape against a RETIRED tombstone must NOT fire. A rule
    # that cannot be shown to stay silent when it should is half-tested; the assertion is
    # on R9a's COUNT below, not merely on whether it fired, because firing once for the
    # live stash row above would otherwise mask firing twice.
    cx.execute("INSERT INTO evidence_sources (ref_id,tier,evidence_type,doi,article_number,"
               "created_by_session) VALUES ('REF-ST5R',6,'code','10.9999/retired-split',"
               "'§5.2',?)", (T,))
    cx.execute("INSERT INTO source_locators (ref_id,doi,status) VALUES "
               "('REF-STASH-R','10.9999/retired-split','RETIRED')")
    # R9b: the mirror -- the batch minted a ref_id the stash already holds against a
    # different DOI. Joins on ref_id, not DOI, so it cannot cross-fire with R9a.
    cx.execute("INSERT INTO evidence_sources (ref_id,tier,evidence_type,doi,article_number,"
               "created_by_session) VALUES ('REF-ST6',6,'code','10.9999/minted','§5.2',?)", (T,))
    cx.execute("INSERT INTO source_locators (ref_id,doi) VALUES "
               "('REF-ST6','10.9999/already-held')")
    # R10b: a URL-bearing admission with verification_status left NULL -- exactly the pool
    # verify_urls.py's scheduled cron polls (workplan/2026-09-10-road-to-batch-06.md B3). No doi
    # keeps this row out of R9/R9a/R9b; verification_status NULL (never 'VERIFIED') keeps it out
    # of R10 above, which is the whole point -- R10 cannot see this condition, R10b must.
    cx.execute("INSERT INTO evidence_sources (ref_id,tier,evidence_type,url,"
               "created_by_session) VALUES ('REF-ST7',6,'code','https://example.org/doc',?)", (T,))
    # R12: an economic finding left in prose with economics_entries empty. findings_note is the
    # correct channel (R6 forbids using deferred_reason for it), and results_found > 0 keeps it
    # out of R14's zero-yield check. exec_id 4 preserves the exec_id-2 gap that R8 detects.
    cx.execute("INSERT INTO search_executions (exec_id,slug,language,query_text,engine,"
               "depth_method,mining_direction,results_found,results_screened,results_admitted,"
               "findings_note,backfill,created_by_session,created_at) VALUES (4,'s','en','q','web',"
               "'scoping','none',50,50,0,'lifetime cost of retrofit vs new build',0,?,'t')", (T,))
    # R15: a candidate marked ADMITTED whose description was never re-checked against the source.
    cx.execute("INSERT INTO search_candidates (candidate_id,found_under_slug,disposition,title,"
               "created_by_session,created_at) VALUES (1,'s','ADMITTED','a staged hypothesis',?,'t')", (T,))
    # R16 / R16-adjudicate (2026-10-02, GAP-061). Observations on REF-ST2, this batch's
    # tier-2 anchor, and on REF-ST4, a PRIOR session's admission. Each row is shaped so
    # that one defect in either predicate moves an asserted COUNT off 1, so the assertion
    # below is on the counts, as R9a's is, not merely on firing:
    #   obs 1  REF-ST2  NAMES-EXISTING -> TERM-ST-U, no parameter, no declination  R16 counts it
    #   obs 2  REF-ST2  NAMES-NEW      -> TERM-ST-D, declined                      must not count
    #   obs 3  REF-ST2  NAMES-EXISTING -> TERM-ST-P, holds a parameter             must not count
    #   obs 4  REF-ST2  NOT-OURS, no term                                          neither counts
    #   obs 5  REF-ST2  unadjudicated                       R16-adjudicate counts it
    #   obs 6  REF-ST4  unadjudicated                       out of scope, must not count
    #   obs 7  REF-ST4  NAMES-EXISTING -> TERM-ST-X, undisposed   out of scope, must not count
    # What each catches: an outcome filter that keeps only NAMES-NEW silences R16 (obs 1 is
    # NAMES-EXISTING, and obs 2's term is declined); a lost declination or parameter clause
    # takes R16 to 2; a lost escope takes either rule to 2; testing for "no NAMING
    # adjudication" instead of "no adjudication" takes R16-adjudicate to 2 (obs 4).
    # Observations on REF-ST2 take it out of R11-harvest's subject; R11-harvest still fires
    # on this session's other admissions (REF-ST1, ST3, ST5, ST5R, ST6, ST7), none of which
    # carries an observation. REF-ST4's observations are a prior session's, outside it.
    for tid in ("TERM-ST-U", "TERM-ST-D", "TERM-ST-P", "TERM-ST-X"):
        cx.execute("INSERT INTO terms (term_id,canonical_en,created_at,created_by_session,"
                   "updated_at,updated_by_session) VALUES (?,?,'t',?,'t',?)",
                   (tid, tid.lower(), T, T))
    cx.execute("INSERT INTO parameter_declinations (term_id,reason,created_at,"
               "created_by_session) VALUES ('TERM-ST-D','an element, not a quantity','t',?)",
               (T,))
    cx.execute("INSERT INTO base_parameters (term_id,created_at,created_by_session) "
               "VALUES ('TERM-ST-P','t',?)", (T,))
    for oid, ref in ((1, "REF-ST2"), (2, "REF-ST2"), (3, "REF-ST2"), (4, "REF-ST2"),
                     (5, "REF-ST2"), (6, "REF-ST4"), (7, "REF-ST4")):
        cx.execute("INSERT INTO observed_terms (observation_id,ref_id,surface_form,language,"
                   "created_at,created_by_session) VALUES (?,?,?,'EN','t',?)",
                   (oid, ref, f"phrase {oid}", T))
    for oid, outcome, tid in ((1, "NAMES-EXISTING", "TERM-ST-U"), (2, "NAMES-NEW", "TERM-ST-D"),
                              (3, "NAMES-EXISTING", "TERM-ST-P"), (4, "NOT-OURS", None),
                              (7, "NAMES-EXISTING", "TERM-ST-X")):
        cx.execute("INSERT INTO term_adjudications (observation_id,outcome,term_id,rationale,"
                   "created_at,created_by_session) VALUES (?,?,?,'fixture','t',?)",
                   (oid, outcome, tid, T))
    # R5 (2026-10-02, plan WP12): the subject is non-English ADMISSIONS. Seven rows, each
    # shaped so that one defect in the predicate moves the asserted COUNT off 3:
    #   REF-ST8   id  grey      journal_article                  counts (journal_article)
    #   REF-ST9   NL  grey      report, names a journal          counts (journal_name; upper case)
    #   REF-ST10  sv  grey      report, carries a DOI            counts (doi)
    #   REF-ST11  es  grey      report, no journal, no DOI       must not count (a grey report)
    #   REF-ST12  en  grey      journal_article                  must not count (English)
    #   REF-ST13  pt  clinical  journal_article                  must not count (not filed grey)
    #   REF-ST14  de  grey      journal_article, PRIOR session   must not count (out of scope)
    # THE NEGATIVE CASE THE MOVE IS ABOUT: exec 1 above is a non-English search targeted 'grey'
    # and must not count. The old search-target predicate fires once on it alone (count 1);
    # keeping it beside the new one gives 4. Dropping any one disjunct gives 2; dropping the
    # language, grey or upper() clause, or the scope, gives 4. Tier is NULL on every row so
    # none enters R2's, R3's or R13's tier-banded arithmetic; REF-ST10's DOI is held by no
    # stash row and no other source, so R9, R9a and R9b do not see it.
    for ref, lg, et, st, jn, doi, sess in (
            ("REF-ST8", "id", "grey", "journal_article", None, None, T),
            ("REF-ST9", "NL", "grey", "report", "Tijdschrift voor fixtures", None, T),
            ("REF-ST10", "sv", "grey", "report", None, "10.9999/st10-sv", T),
            ("REF-ST11", "es", "grey", "report", None, None, T),
            ("REF-ST12", "en", "grey", "journal_article", None, None, T),
            ("REF-ST13", "pt", "clinical", "journal_article", None, None, T),
            ("REF-ST14", "de", "grey", "journal_article", None, None, "PRIOR-SESSION")):
        cx.execute("INSERT INTO evidence_sources (ref_id,lang_detected,evidence_type,"
                   "source_type,journal_name,doi,created_by_session) VALUES (?,?,?,?,?,?,?)",
                   (ref, lg, et, st, jn, doi, sess))
    # R7 (2026-10-02, plan WP12): the candidate floor is gone and count integrity is the
    # predicate. Exec 5 screened more than it found and exec 6 admitted more than it screened,
    # one per clause, so the asserted count is 2; exec 7 has exec 5's defect in a PRIOR
    # session and must not count. Execs 1, 3 and 4 above are consistent and must not count.
    # The old floor fired once here (1 candidate for 58 screened, expected 2), so the old
    # code's count is 1. Exec ids continue past 4, keeping the exec-2 gap R8 detects.
    for eid, found, scr, adm, sess in ((5, 1, 2, 0, T), (6, 3, 1, 2, T),
                                       (7, 1, 2, 0, "PRIOR-SESSION")):
        cx.execute("INSERT INTO search_executions (exec_id,slug,language,query_text,engine,"
                   "depth_method,mining_direction,results_found,results_screened,"
                   "results_admitted,backfill,created_by_session,created_at) "
                   "VALUES (?,'s','en','q','web','scoping','none',?,?,?,0,?,'t')",
                   (eid, found, scr, adm, sess))
    cx.commit(); cx.close()
    # NOTE: inserts above are deliberately NOT wrapped in try/except. If the live schema changes
    # such that this corpus can no longer be built, the selftest must CRASH LOUDLY rather than
    # quietly stop testing — silent rot is the exact failure this guard exists to catch.

    # Capture WHICH rules fired, not just that something did.
    #
    # Until 2026-08-04 this asserted `rc == 1` alone. `expected` was built, printed
    # in the success line, and never compared — so the selftest certified nine
    # rules while proving one. If detection for R2..R11 had all rotted, R1 alone
    # kept it green, and this check is BLOCKING. The capture hook already existed
    # in audit(); it simply was not used here.
    caught = {}
    real, DB_PATH = DB_PATH, Path(fd.name)
    try:
        rc = audit(session=T, capture=caught)
    finally:
        DB_PATH = real
        os.unlink(fd.name)
    # Every rule the corpus PROVABLY fires must be asserted, not just the nine the
    # original comment named. R7, R13 and R14 were fired by this corpus all along
    # and went unasserted — the same blind spot this selftest was hardened to
    # close, left open for three rules that were already being exercised. R13
    # fires because of REF-ST2 ("no population match row"), so it arrived with the
    # R2 fix in the same commit. If a rule here stops firing, that is either
    # detection rot or a corpus change; both need a human, so both fail.
    # R11-harvest added 2026-09-03 with the rule. The corpus seeds evidence rows
    # and no observed_terms, so it fires without any new fixture — but it is listed
    # HERE because a rule that is not in `expected` is a rule this selftest does not
    # protect, which is the exact hole the 2026-08-04 note above describes closing.
    # R16 and R16-adjudicate added 2026-10-02 with the rule, with the R9a-style count
    # assertion below: each is seeded to fire exactly once beside rows that must not count.
    expected = {"R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8",
                "R9", "R9a", "R9b", "R10", "R10b", "R11", "R11-harvest",
                "R12", "R13", "R14", "R15", "R16", "R16-adjudicate"}
    fired = {c for c, n in caught.items() if n}
    missed = expected - fired
    print()
    for rule in sorted(expected):
        print(f"  {'FIRED' if rule in fired else '**SILENT — RULE NOT DETECTED**'}: {rule}")
    # NEGATIVE ASSERTION (2026-09-16). R9a is seeded with two same-DOI/different-ref_id
    # pairs: one live stash row, which must fire, and one RETIRED tombstone, which must not.
    # A count of 2 means the status clause has been dropped and the corpus re-run is blocked
    # again; a count of 1 is the fix holding.
    r9a_n = caught.get("R9a", 0)
    r9a_bad = r9a_n != 1
    if r9a_bad:
        print(f"  **R9a COUNT {r9a_n}, EXPECTED 1** — a RETIRED tombstone is being read as a "
              f"held identity again; see the status clause in R9a.")
    # NEGATIVE ASSERTIONS (2026-10-02). See the R16 fixture comment for what a count
    # other than 1 means in each predicate.
    count_bad = False
    for rule in ("R16", "R16-adjudicate"):
        n = caught.get(rule, 0)
        if n != 1:
            count_bad = True
            print(f"  **{rule} COUNT {n}, EXPECTED 1** — a clause of the predicate has been "
                  f"dropped or narrowed; see the R16 fixture comment in selftest().")
    # COUNT ASSERTIONS (2026-10-02, plan WP12). R5 and R7 changed subject; a count of 1 is
    # what the OLD predicates produce on this corpus (each fired once, with no count), so
    # firing alone would have passed the code these replace. See the R5 and R7 fixture
    # comments for what each other count means.
    for rule, want in (("R5", 3), ("R7", 2)):
        n = caught.get(rule, 0)
        if n != want:
            count_bad = True
            print(f"  **{rule} COUNT {n}, EXPECTED {want}** — the predicate is not the one "
                  f"this selftest was written against; see the {rule} fixture comment in "
                  f"selftest().")
    if rc == 1 and not missed and not r9a_bad and not count_bad:
        print(f"SELFTEST: PASS — gate rejected the corpus AND all {len(expected)} "
              f"seeded rules fired")
        return 0
    if rc != 1:
        print("SELFTEST: FAIL — gate did NOT reject a knowingly-violating corpus")
    if missed:
        print(f"SELFTEST: FAIL — the gate rejected the corpus, but {len(missed)} seeded "
              f"rule(s) did not fire: {sorted(missed)}. Detection for those rules has "
              f"rotted; exit 1 alone would have hidden it.")
    if r9a_bad or count_bad:
        print("SELFTEST: FAIL — a seeded rule fired with the wrong count (see the ** lines "
              "above): firing alone does not prove the predicate kept its clauses.")
    return 1


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Research batch definition-of-done gate")
    p.add_argument("--session", metavar="ID",
                   help="session id to gate. EITHER FORM IS ACCEPTED: the bare stem the DB "
                        "stores, or the same id with '.md' as the pointer files and "
                        "emit_data_migration carry it. A trailing '.md' is stripped before "
                        "any query runs -- see the normalisation below for why that is a "
                        "refusal of a trap rather than a convenience.")
    p.add_argument("--all", action="store_true", help="whole-corpus posture")
    p.add_argument("--selftest", action="store_true", help="prove the checks fire")
    p.add_argument("--write-baseline", action="store_true",
                   help="snapshot current INHERITED debt so the gate fails only on regressions")
    p.add_argument("--check-baseline", metavar="REF", nargs="?", const="origin/main",
                   help="fail if the committed baseline raises any count above REF "
                        "(default origin/main). Closes the hand-edit amnesty.")
    a = p.parse_args()
    # THE TWO-FORM SESSION ID, AND WHY THIS IS NOT A CONVENIENCE. CLAUDE.md §7: the DB
    # stores the BARE STEM, while `sessions/LATEST-RESEARCH`, `emit_data_migration
    # --session` and `citation_mining_completeness --session` all take the id WITH '.md'.
    # `--session` here is interpolated straight into `WHERE session = ?` against columns
    # holding the stem, so the '.md' form matches ZERO ROWS -- and every rule then reports
    # PASS over an empty subject. That is §7's named failure verbatim: "Wrong form scopes a
    # gate to nothing and it passes green."
    #
    # It stopped being hypothetical the moment this gate was registered to run in CI, which
    # substitutes @SESSION@ from a pointer file, and pointer files carry '.md'. Registering
    # it without this line would have installed a gate that runs on every PR, examines
    # nothing, and reports the contract satisfied.
    if a.session:
        a.session = a.session[:-3] if a.session.endswith(".md") else a.session
    if a.selftest:
        sys.exit(selftest())
    if a.check_baseline:
        sys.exit(check_baseline(a.check_baseline))
    if a.write_baseline:
        import json, datetime
        caught = {}
        # Run WITHOUT baseline filtering: capture must see every failing rule, otherwise
        # already-baselined entries are filtered out before capture and would be DELETED from
        # the baseline on rewrite (observed and fixed 2026-07-25).
        audit(allmode=True, capture=caught, use_baseline=False)
        # MERGE, ratchet-down-only: an existing entry may fall (debt remediated) but never rise,
        # and is never dropped. Raising a threshold to make a batch pass would defeat the gate.
        prior = {}
        if BASELINE_PATH.exists():
            prior = json.loads(BASELINE_PATH.read_text()).get("counts", {})
        merged = dict(prior)
        raised = []
        for code, n in caught.items():
            if code in merged:
                if n > merged[code]:
                    raised.append(f"{code}: {merged[code]} -> {n}")
                merged[code] = min(merged[code], n)   # ratchet DOWN only
            else:
                merged[code] = n
        caught = merged
        BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
        BASELINE_PATH.write_text(json.dumps({
            "_comment": "Inherited research-contract debt at baseline. The gate fails only on "
                        "counts EXCEEDING these — a permanently-red gate teaches people to "
                        "ignore it. Lower these numbers as debt is remediated; never raise them "
                        "to make a batch pass. Enforced by `--check-baseline`, which compares "
                        "this file against origin/main and fails on any increase or removal: "
                        "the ratchet lives in git, not in this comment.",
            "captured_at": datetime.date.today().isoformat(),
            "counts": caught,
        }, indent=2) + "\n")
        print(f"\nwrote baseline: {BASELINE_PATH} -> {caught}")
        if raised:
            # Exit NONZERO. This printed the regression and exited 0, so the one
            # line that says "your debt grew" scrolled past inside a successful
            # command. The ratchet held — the numbers were not raised — but the
            # operator was told nothing they had to act on.
            print("\nREGRESSION (baseline NOT raised; remediate instead): "
                  + "; ".join(raised))
            sys.exit(1)
        sys.exit(0)
    if not a.session and not a.all:
        p.error("give --session <id> or --all")
    sys.exit(audit(session=a.session, allmode=a.all))
