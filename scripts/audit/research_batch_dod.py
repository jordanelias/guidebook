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

WHERE THE CONTRACT LIVES. governance/research-contract.yaml is the CANONICAL text of R1-R15
(DR-2026-08-01-research-contract-single-source). Until then it existed as two hand-transcribed
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

# R7 — screened results per registered candidate.
# 1 candidate per 25 screened results. Rationale: most screened hits are correctly discarded; this
# asserts only that a batch which screened hundreds of results found SOMETHING worth staging.
R7_SCREENED_PER_CANDIDATE = 25


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
    scope = "" if allmode else " AND session = ?"
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
                        f"('co1','co2'){scope.replace('session','created_by_session')}",
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
                         f"{scope.replace('session','created_by_session')}", sargs)[0][0]
    mined_rows = _rows(cx, f"SELECT COUNT(*) FROM citation_mining WHERE 1=1"
                           f"{scope.replace('session','created_by_session')}", sargs)[0][0]
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
                        f"{scope.replace('session','created_by_session')}", sargs)
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
                           f"{scope.replace('session','created_by_session')}", sargs)[0][0]
    if total and linked == 0:
        fail("R4", f"{total} searches produced ZERO population linkages "
                   f"(evidence_population_match). Cells are (item x population): a search that "
                   f"merely mentions a population in prose is not a crossing — link admitted "
                   f"evidence to the population(s)/axis it actually speaks to.", total)
    else:
        ok("R4", f"{linked} population linkages produced across {total} searches")

    # --- R5 non-English not down-tiered --------------------------------------------------
    # CASE BUG FIXED 2026-07-25: this compared `language <> 'en'` against a column that carries
    # ISO codes in UPPERCASE in lang_jur_map and search_languages. SQLite '=' / '<>' on TEXT is
    # case-sensitive, so every English-language row written as 'EN' was read as non-English and
    # any English grey-targeted search failed R5 spuriously — while a genuinely non-English grey
    # search written lowercase would still be caught only by luck of the writer's casing. Compare
    # case-insensitively so the check tests the language, not the keystroke.
    downtiered = _rows(cx, f"SELECT exec_id, language FROM search_executions WHERE "
                           f"upper(language) <> 'EN' AND target_evidence_type = 'grey'{scope}",
                       sargs)
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
    # HARDENED: threshold was "> 0", so ONE candidate satisfied it forever no matter how much
    # material stayed in prose. Now proportionate to the yield actually screened.
    cand = _rows(cx, f"SELECT COUNT(*) FROM search_candidates WHERE 1=1{scope}", sargs)[0][0]
    screened = _rows(cx, f"SELECT COALESCE(SUM(results_screened),0) FROM search_executions "
                         f"WHERE 1=1{scope}", sargs)[0][0]
    expected = max(1, screened // R7_SCREENED_PER_CANDIDATE) if screened else 0
    if total and cand < expected:
        fail("R7", f"only {cand} candidates registered for {screened} screened results "
                   f"(expect >= {expected}). Off-slug / unverified material must land in "
                   f"search_candidates, not in prose that evaporates.")
    else:
        # ASSERTED: cand >= max(1, screened//25). REPORTED, NEVER ASSERTED: the harm
        # count. `harm` appears in this string and in no predicate anywhere in this
        # file, and printing a number the check never tested is CLAUDE.md §2(a) at
        # message level -- it is how the exec-32 filing gap stayed invisible while this
        # line read PASS. Softened deliberately 2026-09-03. Do NOT restore the confident
        # wording without putting a predicate behind it, and do not add one that merely
        # counts rows: whether a batch's harm findings actually REACHED the flagged rows
        # is not machine-decidable, which is why it is a standing subject of the
        # adversarial pass instead.
        ok("R7", f"{cand} candidates for {screened} screened "
                 f"(asserted: >= 1 per 25 screened). {harm} row(s) carry "
                 f"harm_finding=1 -- REPORTED, not asserted")

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
        ok("R8", f"{empties} zero-yield searches retained; log intact (no deleted rows)")

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
    n_doi = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources e WHERE COALESCE(e.doi,'') <> ''"
                      f"{escope}", sargs)[0][0]
    n_adm = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources e WHERE 1=1{escope}", sargs)[0][0]

    split = _rows(cx, f"SELECT e.ref_id, sl.ref_id, e.doi FROM evidence_sources e "
                      f"JOIN source_locators sl ON LOWER(TRIM(sl.doi)) = LOWER(TRIM(e.doi)) "
                      f"WHERE COALESCE(e.doi,'') <> '' AND COALESCE(sl.doi,'') <> '' "
                      f"AND sl.ref_id <> e.ref_id{escope}", sargs)
    if split:
        fail("R9a", f"{len(split)} source(s) admitted under a ref_id that DIFFERS from the one "
                    f"the identifier stash already holds for the same DOI — one source, two "
                    f"identities. Cross-file the held id instead of minting a second: "
                    + "; ".join(f"{a} vs stash {b} ({d})" for a, b, d in split[:5]), len(split))
    elif n_doi == 0:
        fail("R9a", "NOTHING IN SCOPE — this batch admitted no source carrying a DOI, so the "
                    "stash cross-check examined nothing. A pass here would assert nothing. "
                    "If the batch admitted sources, they are missing their locators (see R10).")
    else:
        ok("R9a", f"{n_doi} admitted DOI(s) checked against the stash; none held under a "
                  f"different ref_id")

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
                    f"above the stash high-water mark: "
                    + "; ".join(f"{r} admitted {a}, stash holds {b}" for r, a, b in collide[:5]),
             len(collide))
    elif n_adm == 0:
        fail("R9b", "NOTHING IN SCOPE — this batch admitted no sources, so the identifier "
                    "collision check examined nothing.")
    else:
        ok("R9b", f"{n_adm} admitted ref_id(s) checked against the stash across "
                  f"{len(ID_COLS)} identifier types; no collision")

    # --- R10 locator re-retrieval ----------------------------------------------------------
    # HARDENED: the original accepted ANY non-empty locator field and never checked whether the
    # locator actually RESOLVED — 77 VERIFIED sources with unresolved DOIs passed silently.
    unver = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE verification_status='VERIFIED'"
                      f" AND COALESCE(doi,'')='' AND COALESCE(url,'')='' AND COALESCE(pmid,'')=''"
                      f" AND COALESCE(verified_by_tool,'')=''"
                      f"{scope.replace('session','created_by_session')}", sargs)[0][0]
    unresolved = _rows(cx, f"SELECT COUNT(*) FROM evidence_sources WHERE "
                           f"verification_status='VERIFIED' AND COALESCE(doi,'') <> '' AND "
                           f"COALESCE(doi_resolution_outcome,'') NOT IN ('RESOLVED','NO-MATCH')"
                           f"{scope.replace('session','created_by_session')}", sargs)[0][0]
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

    # --- R11 vocabulary provenance ---------------------------------------------------------
    noprov_scope = _rows(cx, f"SELECT COUNT(*) FROM term_aliases WHERE 1=1"
                       f"{scope.replace('session','created_by_session')}", sargs)[0][0]
    noprov = _rows(cx, f"SELECT COUNT(*) FROM term_aliases WHERE COALESCE(notes,'')=''"
                       f"{scope.replace('session','created_by_session')}", sargs)[0][0]
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
                        f"{scope.replace('session','created_by_session')}", sargs)
    unmatched = [r[0] for r in anchors
                 if not _rows(cx, "SELECT 1 FROM evidence_population_match WHERE ref_id=?",
                              (r[0],))]
    if unmatched:
        fail("R13", f"{len(unmatched)} tier-1..3 source(s) admitted with NO population match row "
                    f"— silently asserting that the population studied is the population served: "
                    f"{', '.join(unmatched[:5])}. Grade each EXACT/PARTIAL/PROXY and write the "
                    f"mismatch note.", len(unmatched))
    else:
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
    # R4 (no population linkage), R5 (non-EN targeted grey), R6 (findings in deferred_reason),
    # R8 (deleted row -> id gap), R10 (VERIFIED, no locator), R11 (alias w/o provenance).
    cx.execute("INSERT INTO search_executions (exec_id,slug,jurisdiction,language,"
               "target_evidence_type,query_text,engine,depth_method,mining_direction,"
               "results_found,results_screened,results_admitted,deferred_reason,backfill,"
               "session,executed_at) VALUES (1,'s','ID','id','grey','q','web','scoping','none',"
               "5,5,0,'found things',0,?,'t')", (T,))
    cx.execute("INSERT INTO search_executions (exec_id,slug,language,query_text,engine,"
               "depth_method,mining_direction,results_found,results_screened,results_admitted,"
               "backfill,session,executed_at) VALUES (3,'s','en','q','web','scoping','none',"
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
    # R9b: the mirror -- the batch minted a ref_id the stash already holds against a
    # different DOI. Joins on ref_id, not DOI, so it cannot cross-fire with R9a.
    cx.execute("INSERT INTO evidence_sources (ref_id,tier,evidence_type,doi,article_number,"
               "created_by_session) VALUES ('REF-ST6',6,'code','10.9999/minted','§5.2',?)", (T,))
    cx.execute("INSERT INTO source_locators (ref_id,doi) VALUES "
               "('REF-ST6','10.9999/already-held')")
    # R12: an economic finding left in prose with economics_entries empty. findings_note is the
    # correct channel (R6 forbids using deferred_reason for it), and results_found > 0 keeps it
    # out of R14's zero-yield check. exec_id 4 preserves the exec_id-2 gap that R8 detects.
    cx.execute("INSERT INTO search_executions (exec_id,slug,language,query_text,engine,"
               "depth_method,mining_direction,results_found,results_screened,results_admitted,"
               "findings_note,backfill,session,executed_at) VALUES (4,'s','en','q','web',"
               "'scoping','none',50,50,0,'lifetime cost of retrofit vs new build',0,?,'t')", (T,))
    # R15: a candidate marked ADMITTED whose description was never re-checked against the source.
    cx.execute("INSERT INTO search_candidates (candidate_id,found_under_slug,disposition,title,"
               "session,created_at) VALUES (1,'s','ADMITTED','a staged hypothesis',?,'t')", (T,))
    #
    # R7 INTERACTION, stated rather than discovered: the R15 candidate raises `cand` to 1, and R7
    # fires only while cand < max(1, screened // 25). The R12 fixture takes total screened from 5
    # to 55, so expected becomes 2 and 1 < 2 -- R7 still fires. Lower that fixture below 50 and
    # expected falls to 1, R7 goes silent, and this selftest fails on the missing rule. That is
    # the correct outcome: the arithmetic is load-bearing and must not be edited casually.
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
    expected = {"R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8",
                "R9", "R9a", "R9b", "R10", "R11", "R12", "R13", "R14", "R15"}
    fired = {c for c, n in caught.items() if n}
    missed = expected - fired
    print()
    for rule in sorted(expected):
        print(f"  {'FIRED' if rule in fired else '**SILENT — RULE NOT DETECTED**'}: {rule}")
    if rc == 1 and not missed:
        print(f"SELFTEST: PASS — gate rejected the corpus AND all {len(expected)} "
              f"seeded rules fired")
        return 0
    if rc != 1:
        print("SELFTEST: FAIL — gate did NOT reject a knowingly-violating corpus")
    if missed:
        print(f"SELFTEST: FAIL — the gate rejected the corpus, but {len(missed)} seeded "
              f"rule(s) did not fire: {sorted(missed)}. Detection for those rules has "
              f"rotted; exit 1 alone would have hidden it.")
    return 1


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Research batch definition-of-done gate")
    p.add_argument("--session", help="session id to gate")
    p.add_argument("--all", action="store_true", help="whole-corpus posture")
    p.add_argument("--selftest", action="store_true", help="prove the checks fire")
    p.add_argument("--write-baseline", action="store_true",
                   help="snapshot current INHERITED debt so the gate fails only on regressions")
    p.add_argument("--check-baseline", metavar="REF", nargs="?", const="origin/main",
                   help="fail if the committed baseline raises any count above REF "
                        "(default origin/main). Closes the hand-edit amnesty.")
    a = p.parse_args()
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
