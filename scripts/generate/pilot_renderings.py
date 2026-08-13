#!/usr/bin/env python3
"""
scripts/generate/pilot_renderings.py — render pilot determinations in every register.

Demonstrates governance/evidence-architecture.md §6: the SAME determination tuple
rendered for five roles (armature_v4.md §4.5) plus the advocacy-brief use-pattern
(G5), with claim-strength language drawn ONLY from REGISTER_MAP — the finite,
versioned lookup that makes "role changes register, never data" testable.

Integrity invariants I1–I5 are asserted by scripts/audit/register_integrity_check.py,
which imports REGISTER_MAP from this module (single source of truth).

Honesty rules baked in:
- No fabricated values. No evidence-anchored numeric value has been promoted to a
  determination for any pilot cell, so renderings say so instead of inventing
  numbers (the corridor 2440mm figure in tier-system.md §3 is doctrine prose, not
  an extracted determination value — it is cited as context, never as this cell's
  computed value). This used to read "source_value_extractions is empty"; the
  table now holds 8 rows and two pilot cells reach one each, so the claim is made
  per cell rather than about the table.
- Regulatory floors shown are real jurisdictional_values rows (is_code_minimum=1).
- The solo-authorship Co-1 limit is declared on Co-1-governed renderings
  (mission-and-epistemics §Operational reality).
"""
import argparse
import hashlib
import html
import json
import os
import sqlite3
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO_ROOT)

# The register map is versioned, which is what evidence-architecture §6 means by
# "versioned with rule_version". This constant was `RULE_VERSION = "pilot-1"` and
# was dead — nothing read it, and the engine's real RULE_VERSION lives in
# assess_cell.py (currently "pilot-2"), so the name invited exactly the confusion
# of reading a renderer constant as a determination version. map-2 is the
# DR-2026-07-21 Option A revision: weak-band split, G8 disclosure in the plain
# registers, amended-I3 header.
REGISTER_MAP_VERSION = "map-2"

ROLES = ["designer", "ot", "policymaker", "disabled_person", "carer", "advocacy_brief"]
REGISTERS = {"designer": "technical", "ot": "clinical", "policymaker": "policy",
             "disabled_person": "plain", "carer": "plain-care", "advocacy_brief": "plain-rights"}

# ---------------------------------------------------------------------------
# THE CLAIM-STRENGTH REGISTER MAP (evidence-architecture.md §6, versioned with
# rule_version). Keyed by tuple-class; one language cell per register. Renderers
# MUST draw claim-strength language from here and nowhere else (I4/I5).
# ---------------------------------------------------------------------------
def tuple_class(state, tier_basis, conv_status, rso, n_reg_refs=0, n_reg_jur=0):
    """Map a determination tuple to its register-map key.

    The regulatory-stratum branch splits in two as of the DR-2026-07-21 Option A
    rework. One shared row previously served cell 9005 (15 instruments, 12
    jurisdictions) and cells 9012/9013 (one instrument, one jurisdiction), and
    it asserted convergence — which made it false for the singles. Collapsing to
    a convergence-free text fixed the falsehood but silenced what is true and
    worth saying about 9005. The split says each accurately.

    Note what the broad row may and may not claim. E-06's recorded code minimums
    are 5, 10, 13 and 20 mm across AU/DE/FR/US — they do NOT agree on a value.
    So the honest claim for 9005 was never value convergence; it is BREADTH:
    many instruments, many jurisdictions, regulating this parameter, with a
    visible spread. A value-convergence row is not pre-built here because no
    cell occupies that state (043's lesson); it becomes assertable when
    direction-aware most-accommodating selection lands (DR §5.2) or the floors
    actually agree.
    """
    if state == "pending":
        return "pending"
    if rso:
        return "rso_weak_broad" if (n_reg_refs >= 2 and n_reg_jur >= 2) else "rso_weak_single"
    if state == "provisional":
        return "provisional_t3"
    if conv_status == "pending_assessment":
        return "stated_multi_axis"
    return "stated_single_axis"


REGISTER_MAP = {
    "stated_multi_axis": {
        "designer": "Best practice [●]: anchored by multiple independent evidence axes "
                    "({basis}). Value-level convergence assessment pending extraction.",
        "ot": "Best practice [●]: multi-axis anchor ({basis}). Population-Mode range "
              "for Person-Mode resolution; value extraction pending.",
        "policymaker": "Evidence-anchored best practice exists ({basis}); multiple independent "
                       "evidence axes. Its relation to the recorded code minimums is pending "
                       "value extraction — no delta is asserted before the values are.",
        # G8 (RATIFIED 2026-07-13) requires the value-convergence-pending
        # disclosure in EVERY register. The four technical registers carried it;
        # these two plain registers did not, so cells 9001–9003 rendered without
        # it. The disclosure lives in the claim-strength row, not role_body, so
        # I4/I5 equality enforces it mechanically. Plain language, no jargon —
        # "value-level convergence" must not appear in a plain register.
        "disabled_person": "Research and disabled people's own published experience both "
                           "address this. This is an evidence-based recommendation, not just "
                           "a building rule. One check is still in progress: whether the "
                           "different kinds of evidence agree on the same measurements. "
                           "Until that check is done, this page gives no number.",
        "carer": "Research and disabled people's published experience both support attention "
                 "to this feature. It is an evidence-based recommendation, not just a rule. "
                 "Whether the different evidence sources agree on exact measurements is still "
                 "being checked, so no number is given yet.",
        "advocacy_brief": "You can cite independent research AND community evidence for this "
                          "({basis}). How the evidence-based value compares to the legal "
                          "minimum is pending extraction — cite the evidence itself; "
                          "accuracy protects credibility.",
    },
    "stated_single_axis": {
        "designer": "Best practice [●]: anchored by a single evidence axis ({basis}); "
                    "basis disclosed, no independent corroborating axis yet.",
        "ot": "Best practice [●] on a single axis ({basis}); treat corroboration as open.",
        "policymaker": "Evidence-anchored best practice on a single axis ({basis}); no "
                       "independent second axis yet.",
        "disabled_person": "There is solid evidence for this from one kind of source ({basis}). "
                           "Other kinds of evidence haven't weighed in yet.",
        "carer": "There is solid evidence for this from one kind of source ({basis}).",
        "advocacy_brief": "Citable evidence exists for this ({basis}) — one strong evidence "
                          "stream; name it accurately when advocating.",
    },
    "provisional_t3": {
        "designer": "Provisional [◐]: supporting clinical research only ({basis}) — "
                    "'rarely the sole basis' (tier-system §1); not a settled best practice.",
        "ot": "Provisional [◐]: lower-control clinical evidence only ({basis}); "
              "clinical judgment carries more weight here than the literature.",
        "policymaker": "Provisional ({basis}): supporting-tier clinical evidence only; "
                       "not yet an anchored best-practice claim.",
        "disabled_person": "Early research supports this, but it isn't settled yet. "
                           "It's a reasonable ask, honestly labelled as provisional.",
        "carer": "Early research supports this, but it isn't settled yet.",
        "advocacy_brief": "Early research supports this ask; label it as provisional evidence "
                          "when citing it — accuracy protects credibility.",
    },
    # ── The weak band (DR-2026-07-21 Option A) ─────────────────────────────
    # Under Option A a code-consensus claim CAN anchor best practice, but only
    # at the flagged weak band (○) — "best practice as currently known" —
    # rendered flagged in every register and never suppressed. Rendered
    # unflagged, or at ●/◐, it is in error. These rows carry [○] and not [◐]:
    # tier-system §8 puts the determination-level band for any regulatory-
    # stratum cell at ○, and the previous row printed [◐], which was a band
    # error under DR-2026-07-21 §2.3.
    #
    # Two rows, not one. A single row served both cell 9005 and cells
    # 9012/9013 and asserted convergence, which was false for the singles;
    # collapsing it to convergence-free text fixed that and silenced what is
    # true of 9005. The split states each accurately, with the counts drawn per
    # cell from the DB rather than written into prose.
    "rso_weak_broad": {
        "designer": "Best practice as currently known [○ weak, code-derived] ({basis}): "
                    "{n_refs} regulatory instruments across {n_jur} jurisdictions address "
                    "this parameter, and their required values differ — see the recorded "
                    "spread. No anchoring evidence (T1/Co-1/T2/Co-2) exists for this cell; "
                    "code agreement is not evidence, and the value stands only because "
                    "nothing stronger says otherwise.",
        "ot": "Best practice as currently known [○ weak, code-derived] ({basis}): regulatory "
              "instruments only ({n_refs} across {n_jur} jurisdictions); no clinical, "
              "lived-experience, or CPG anchor. Treat this as the current regulatory answer, "
              "not a clinically adjudicated target.",
        "policymaker": "Best available given current regulation, NOT academically adjudicated "
                       "[○ weak, code-derived]: {n_refs} instruments across {n_jur} "
                       "jurisdictions regulate this parameter ({basis}). Convergence is not "
                       "evidence — no T1/Co-1/T2/Co-2 anchor exists; the jurisdictions could "
                       "all be wrong together, or all be copying one unevidenced ancestor. "
                       "This stands as weak-band best practice only because nothing stronger "
                       "says otherwise.",
        "disabled_person": "Building rules and standards in {n_jur} countries or standards "
                           "bodies cover this. That's a rules answer, not a research answer: "
                           "no research and no lived-experience evidence yet shows what "
                           "actually works best. It's the best answer anyone has right now, "
                           "it could change when real evidence arrives, and you can ask for "
                           "better than the rule.",
        "carer": "This comes from building rules in {n_jur} countries or standards bodies, "
                 "not from research or lived experience. It's the best answer available right "
                 "now, and it could change when real evidence arrives.",
        "advocacy_brief": "The only basis here is regulation — {n_refs} instruments across "
                          "{n_jur} jurisdictions — and NO research or lived-experience "
                          "evidence yet shows it is enough. Cite it as the current regulatory "
                          "answer, never as proven best practice; the missing evidence is "
                          "itself an advocacy point: demand the research.",
    },
    "rso_weak_single": {
        "designer": "Best practice as currently known [○ weak, code-derived] ({basis}): the "
                    "entire basis is a single regulatory instrument in a single jurisdiction. "
                    "No anchoring evidence (T1/Co-1/T2/Co-2) exists for this cell; one "
                    "instrument is not convergence, code is not evidence, and the value "
                    "stands only because nothing stronger says otherwise.",
        "ot": "Best practice as currently known [○ weak, code-derived] ({basis}): one "
              "regulatory instrument, no clinical, lived-experience, or CPG anchor. Treat "
              "this as the current regulatory answer, not a clinically adjudicated target.",
        "policymaker": "Best available given current regulation, NOT academically adjudicated "
                       "[○ weak, code-derived] ({basis}): a single instrument in a single "
                       "jurisdiction. Where only one instrument speaks there is not even "
                       "convergence — no T1/Co-1/T2/Co-2 anchor exists, and the one "
                       "instrument could simply be wrong. This stands as weak-band best "
                       "practice only because nothing stronger says otherwise.",
        "disabled_person": "This comes from one set of building rules in one country. That's "
                           "a rules answer, not a research answer: no research and no "
                           "lived-experience evidence yet shows what actually works best. "
                           "It's the best answer anyone has right now, it could change when "
                           "real evidence arrives, and you can ask for better than the rule.",
        "carer": "This comes from one set of building rules in one country, not from research "
                 "or lived experience. It's the best answer available right now, and it could "
                 "change when real evidence arrives.",
        "advocacy_brief": "The basis here is one regulatory instrument in one jurisdiction, "
                          "and NO research or lived-experience evidence yet shows it is "
                          "enough. Cite it as exactly that; the missing evidence is itself an "
                          "advocacy point: demand the research.",
    },
    "pending": {
        "designer": "[BEST-PRACTICE-PENDING] — evidence gap logged (→ gap register). "
                    "No synthesis is offered.",
        "ot": "[BEST-PRACTICE-PENDING] — no usable evidence found; gap logged.",
        "policymaker": "[BEST-PRACTICE-PENDING] — evidence gap logged; absence of evidence "
                       "recorded, not concealed.",
        "disabled_person": "We don't know yet. This is an open gap we are tracking — "
                           "not a settled answer, and not a 'no'.",
        "carer": "We don't know yet. This is an open, tracked gap.",
        "advocacy_brief": "No evidence exists yet — a tracked gap. 'Unknown' can be an "
                          "advocacy point: ask who is funding the answer.",
    },
}

CO1_LIMIT = ("Co-1 engagement is at evidence level (published corpus), not participation "
             "level: CRPD Art. 4.3 is honored in partial form pre-launch "
             "(mission-and-epistemics §Operational reality).")


def fetch_cells(conn):
    cells = []
    q = ("SELECT specification_id,item_code,population_code,state,design_scale,convergence_id,"
         "tier_basis,governing_refs,rule_version,derivation_sha,code_floor_only,"
         "confidence_synthesis_basis,gap_register_id,falsification_condition "
         "FROM specifications ORDER BY specification_id")
    for r in conn.execute(q):
        c = dict(zip(("specification_id", "item_code", "population", "state", "design_scale",
                      "convergence_id", "tier_basis", "governing_refs", "rule_version",
                      "derivation_sha", "code_floor_only", "synthesis_basis",
                      "gap_id", "falsification"), r))
        c["item_name"] = conn.execute("SELECT name FROM items WHERE item_code=?",
                                      (c["item_code"],)).fetchone()[0]
        c["refs"] = json.loads(c["governing_refs"]) if c["governing_refs"] else []
        conv = conn.execute("SELECT status, rationale FROM convergence_assessment "
                            "WHERE convergence_id=?", (c["convergence_id"],)).fetchone() \
            if c["convergence_id"] else None
        c["conv_status"] = conv[0] if conv else None
        c["conv_rationale"] = conv[1] if conv else None
        c["rso"] = 1 if (c["tier_basis"] or "").endswith("(regulatory_stratum_only)") else 0
        c["floors"] = conn.execute(
            "SELECT jurisdiction, standard_name, value_numeric, unit FROM jurisdictional_values "
            "WHERE item_code=? AND is_code_minimum=1 AND value_numeric IS NOT NULL "
            "ORDER BY jurisdiction", (c["item_code"],)).fetchall()
        c["has_co1"] = "CO1" in (c["tier_basis"] or "")
        # Per-source extracted values reaching THIS cell: a governing source of
        # this cell whose extraction is for this cell's item. The item match is
        # what migration 052 made possible and is not optional — joining on
        # ref_id alone attributes four RT60-in-seconds extractions to cells for
        # A-02 (NRC) and A-08 (NC), parameters in different units entirely.
        # role='governing' is filtered explicitly rather than relied on: it is
        # the only value specification_source_links admits today, and a second role
        # arriving must not silently widen what this counts.
        # Breadth of the regulatory basis, for the weak-band split. Drawn from
        # evidence_sources.jurisdiction over the governing set — the fact is
        # already there and needs no column.
        #
        # Two signals were rejected. convergence_assessment.status records
        # single_axis for all three RSO cells: that counts EVIDENCE AXES, not
        # jurisdictions, and overloading it would corrupt its meaning.
        # jurisdictional_values is wrong the other way — cells 9012/9013 have
        # zero rows there while having a real single-instrument basis, so it
        # would read "no basis" where a basis exists. COUNT(DISTINCT ...) skips
        # NULL jurisdictions, which errs toward calling a basis narrow.
        c["n_reg_refs"] = len(c["refs"]) if c["rso"] else 0
        if c["rso"] and c["refs"]:
            qs = ",".join("?" * len(c["refs"]))
            c["n_reg_jur"] = conn.execute(
                f"SELECT COUNT(DISTINCT jurisdiction) FROM evidence_sources "
                f"WHERE ref_id IN ({qs})", c["refs"]).fetchone()[0]
        else:
            c["n_reg_jur"] = 0
        # Does the recorded derivation_sha still verify against this row? The
        # engine's own function (assess_cell.sha) hashes
        # item|population|sorted(governing_refs)::rule_version, so a sha that no
        # longer recomputes means the row moved after the determination was
        # recorded. Two of the seven non-NULL shas fail this today: 9007's
        # attests population NEU (renamed to BRAIN without restamping) and
        # 9003's attests a six-ref governing set that was narrowed to four.
        # Rendering a stale hash unremarked would present a broken attestation
        # as a working one — worse than the NULLs, which at least admit they
        # attest nothing.
        if c["derivation_sha"] and c["rule_version"]:
            refs_for_sha = sorted(json.loads(c["governing_refs"] or "[]"))
            payload = (f"{c['item_code']}|{c['population']}|" + "|".join(refs_for_sha)
                       + "::" + c["rule_version"])
            c["sha_stale"] = hashlib.sha256(payload.encode()).hexdigest() != c["derivation_sha"]
        else:
            c["sha_stale"] = False
        c["extractions"] = conn.execute(
            "SELECT COUNT(*) FROM specification_source_links l "
            "JOIN source_value_extractions x "
            "  ON x.ref_id = l.ref_id AND x.item_code = ? "
            "WHERE l.specification_id = ? AND l.role = 'governing'",
            (c["item_code"], c["specification_id"])).fetchone()[0]
        cells.append(c)
    return cells


def _sha_label(sha):
    """Human-readable derivation sha, tolerant of the 8 cells that have none.

    This function exists because `derivation_sha[:16]` raised TypeError and made
    the whole generator unrunnable: 8 of the 15 determination rows (9008–9015)
    carry a NULL sha, so the crash arrived the moment the second batch of cells
    was added and nobody could regenerate this document afterwards. The committed
    HTML is therefore frozen at the 7-cell era.

    "not recorded" is the honest rendering. Whether those 8 rows SHOULD carry a
    sha is a data question — a derivation hash is a claim about how a
    determination was computed, and inventing one here would be fabricating that
    claim. The render says what is true and leaves the backfill to whoever
    adjudicates it.

    NOTE — the `data-sha` HTML attribute is deliberately NOT routed through this,
    and neither is `data-rule-version`. register_integrity_check.py cross-checks
    both against `str(row[...])`, which is the literal string 'None' for a NULL,
    so a corrected attribute would fail the cross-check. Between them that repr
    is published 8 + 12 = 20 times (cells 9008–9015 have no sha; 9014–9015 also
    have no rule_version). Both are real warts and both are named here rather
    than only the first — an earlier version of this note documented `data-sha`
    alone, which made the disclosure look complete when it was half.

    Fixing them means None-normalising the checker in lockstep. That is a
    two-line change and the coupling is by design (the checker imports
    REGISTER_MAP, ROLES and tuple_class from this module as single source of
    truth), so the reluctance is narrower than "don't touch it": the checker is
    quarantined pending the DR-2026-07-21 Option A rework of the I3 lexicon, and
    the None-normalisation belongs in that same pass rather than arriving alone
    into a check the registry cannot yet run.
    """
    return f"{sha[:16]}…" if sha else "not recorded"


FLOOR_STATUS_CAVEAT = ("Instrument status varies: jurisdictional_values stores statutory codes "
                       "and referenced/voluntary standards together (e.g. BS 8300-2 is voluntary "
                       "guidance, not GB law) — verify legal status per jurisdiction before "
                       "citing any of these as a legal requirement.")


def role_body(c, role):
    """Role-specific EMPHASIS content (what is foregrounded) — never claim strength."""
    parts = []
    floors = c["floors"]
    # ALL floors rendered — silent truncation misleads (adversarial finding 7).
    floor_line = "; ".join(f"{j}: {v:g} {u} ({s})" for j, s, v, u in floors)
    if role == "designer":
        parts.append(f"Evidence basis: {c['tier_basis'] or 'none'} · governing refs: "
                     f"{len(c['refs'])} · scale: {c['design_scale']}")
        if floors:
            parts.append(f"Recorded code minimums, per jurisdiction: {floor_line}. "
                         + FLOOR_STATUS_CAVEAT)
        # This sentence used to assert "source_value_extractions empty" for every
        # cell. That was true when written and is now false for two of the
        # fifteen — a false statement in published output, the same class of
        # defect as a stale audit gate. It is now read per cell.
        if c["extractions"]:
            # "reaching this cell", not "for this item" — the count is
            # cell-scoped (governing sources of THIS cell), and 8 extractions
            # exist for item A-18 while only 1 reaches cell 9008. Naming the
            # wrong denominator would overstate the cell's evidence.
            parts.append(f"Evidence-anchored value range: not yet synthesised. "
                         f"{c['extractions']} per-source extracted value(s) reach this cell "
                         f"through its governing sources; none has been promoted to a cell "
                         f"determination, so no number is stated here.")
        else:
            parts.append("Evidence-anchored value range: not yet extracted for this cell "
                         "— no number is invented here.")
    elif role == "ot":
        parts.append(f"Anchor: {c['tier_basis'] or 'none'}. Person-Mode resolution happens "
                     "within the Population-Mode range once extracted; the population "
                     "evidence conditions the assessment process, never the assessed answer.")
    elif role == "policymaker":
        if floors:
            parts.append(f"FLOOR (recorded code minimums; instrument status varies — see note): "
                         f"{floor_line}. " + FLOOR_STATUS_CAVEAT)
            anchor_txt = ("ANCHOR: evidence-anchored best practice exists "
                          f"({c['tier_basis']}); extracted delta pending value extraction."
                          if c["state"] == "stated" and not c["rso"] else
                          # "the floor is the only defensible value claim" stated
                          # I3's repealed absolute form: under Option A the
                          # determination above IS a claim, at the flagged weak
                          # band. The floor is its basis, not its replacement.
                          "ANCHOR: none — no anchoring evidence (T1/Co-1/T2/Co-2) exists for "
                          "this cell; the determination above is weak-band and code-derived, "
                          "and the recorded floors are its entire basis.")
            parts.append(anchor_txt)
        parts.append(f"Citation chain: {', '.join(c['refs'][:6])}{'…' if len(c['refs']) > 6 else ''}"
                     if c["refs"] else "Citation chain: none (see gap register).")
    elif role == "disabled_person":
        parts.append(f"What this is about: {c['item_name']}.")
        if c["has_co1"]:
            parts.append("Disabled people's own published research and positions are part of "
                         "the evidence base here — cited as evidence, alongside (not beneath) "
                         "clinical research.")
        parts.append("Questions to raise with your architect or OT are generated from the "
                     "Person-Mode handoff for this item.")
    elif role == "carer":
        parts.append(f"What this is about: {c['item_name']}. The carer view is its own view — "
                     "it never substitutes for the disabled person's own decisions "
                     "(CRPD Art. 12, supported not substituted).")
    elif role == "advocacy_brief":
        if floors:
            parts.append(f"Recorded minimums today: {floor_line}. Before citing any of these "
                         "as 'the law', check which are statutory codes and which are "
                         "voluntary standards in your jurisdiction — a wrongly-cited "
                         "'legal minimum' hands the other side an easy rebuttal.")
        if c["state"] == "stated" and not c["rso"]:
            parts.append(f"The evidence base to cite: {c['tier_basis']} "
                         f"({len(c['refs'])} sources, listed in the citation chain).")
        if c["gap_id"]:
            parts.append(f"Tracked gap: {c['gap_id']} — citable as an unmet research need.")
    # The solo-authorship Co-1 limit is declared in EVERY register of a
    # Co-1-governed determination (evidence-architecture §9: "limits are
    # rendered"), not only the disabled-person view (adversarial finding 18e).
    if c["has_co1"]:
        parts.append(CO1_LIMIT)
    return parts


def render(cells, out_path):
    rows = []
    for c in cells:
        tc = tuple_class(c["state"], c["tier_basis"], c["conv_status"], c["rso"],
                         c["n_reg_refs"], c["n_reg_jur"])
        basis = c["tier_basis"] or "no basis"
        blocks = []
        for role in ROLES:
            # n_refs/n_jur are surplus kwargs for every row but the two weak-band
            # ones; str.format ignores what a template does not reference.
            claim = REGISTER_MAP[tc][role].format(
                basis=basis, n_refs=c["n_reg_refs"], n_jur=c["n_reg_jur"])
            body = "".join(f"<p class='emphasis'>{html.escape(p)}</p>"
                           for p in role_body(c, role))
            blocks.append(
                f"<div class='rendering' data-cell='{c['item_code']}×{c['population']}' "
                f"data-role='{role}' data-register='{REGISTERS[role]}' "
                f"data-state='{c['state']}' data-tier-basis='{html.escape(basis)}' "
                f"data-conv='{c['conv_status'] or ''}' data-rso='{c['rso']}' "
                f"data-cfo='{c['code_floor_only']}' "
                f"data-reg-refs='{c['n_reg_refs']}' data-reg-jur='{c['n_reg_jur']}' "
                f"data-sha='{c['derivation_sha'] or ''}' "
                f"data-rule-version='{c['rule_version'] or ''}' data-tuple-class='{tc}'>"
                f"<h4>{role.replace('_', ' ')} · {REGISTERS[role]}</h4>"
                f"<p class='claim-strength'>{html.escape(claim)}</p>{body}</div>")
        rows.append(
            f"<section class='cell' id='{c['item_code']}-{c['population']}'>"
            f"<h2>{html.escape(c['item_name'])} × {c['population']}</h2>"
            f"<p class='tuple'>tuple: state={c['state']} · basis={html.escape(basis)} · "
            f"convergence={c['conv_status'] or 'none recorded'} · rso={c['rso']} "
            f"· cfo={c['code_floor_only']} "
            f"· sha={_sha_label(c['derivation_sha'])} · {c['rule_version'] or 'not recorded'}</p>"
            + (f"<p class='sha-warning'>Derivation sha does not verify against this row's "
               f"own governing set and rule version — the determination was recorded, then "
               f"the row changed without restamping. Treat the sha as stale, not as "
               f"attesting this state.</p>" if c["sha_stale"] else "")
            + (f"<p class='falsification'>Falsification: {html.escape(c['falsification'])}</p>"
               if c["falsification"] else "")
            + "<div class='roles'>" + "".join(blocks) + "</div></section>")
    doc = ("<!doctype html><meta charset='utf-8'><title>Pilot renderings — evidence architecture</title>"
           "<style>body{font-family:system-ui;max-width:1200px;margin:2rem auto;padding:0 1rem}"
           ".roles{display:grid;grid-template-columns:repeat(3,1fr);gap:.6rem}"
           ".rendering{border:1px solid #999;border-radius:6px;padding:.6rem;font-size:.85rem}"
           ".claim-strength{font-weight:600}.tuple{font-family:monospace;font-size:.8rem}"
           ".falsification{font-size:.8rem;color:#444}h4{margin:.1rem 0}</style>"
           "<h1>Same determination, six registers — pilot demonstration</h1>"
           "<p>Every rendering of a cell carries the identical determination tuple "
           "(I1); claim-strength language is drawn only from REGISTER_MAP (I4/I5); "
           "regulatory-stratum-only cells render only as flagged weak-band (○, code-derived) "
           "best practice with the code-is-not-evidence caveat — never unflagged, never above "
           "the weak band (I3 as amended by DR-2026-07-21 Option A); the policymaker view "
           f"always pairs floor with anchor (I2). Register map: {REGISTER_MAP_VERSION}.</p>"
           + "".join(rows))
    with open(out_path, "w") as f:
        f.write(doc)
    return len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    conn = sqlite3.connect(args.db)
    n = render(fetch_cells(conn), args.out)
    print(f"{n} cells rendered × {len(ROLES)} roles -> {args.out}")


if __name__ == "__main__":
    main()
