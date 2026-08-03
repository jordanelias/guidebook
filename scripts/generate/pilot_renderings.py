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
- No fabricated values. source_value_extractions is empty, so no evidence-anchored
  numeric value exists for any pilot cell; renderings say so instead of inventing
  numbers (the corridor 2440mm figure in tier-system.md §3 is doctrine prose, not
  an extracted determination value — it is cited as context, never as this cell's
  computed value).
- Regulatory floors shown are real jurisdictional_values rows (is_code_minimum=1).
- The solo-authorship Co-1 limit is declared on Co-1-governed renderings
  (mission-and-epistemics §Operational reality).
"""
import argparse
import html
import json
import os
import sqlite3
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO_ROOT)

RULE_VERSION = "pilot-1"

ROLES = ["designer", "ot", "policymaker", "disabled_person", "carer", "advocacy_brief"]
REGISTERS = {"designer": "technical", "ot": "clinical", "policymaker": "policy",
             "disabled_person": "plain", "carer": "plain-care", "advocacy_brief": "plain-rights"}

# ---------------------------------------------------------------------------
# THE CLAIM-STRENGTH REGISTER MAP (evidence-architecture.md §6, versioned with
# rule_version). Keyed by tuple-class; one language cell per register. Renderers
# MUST draw claim-strength language from here and nowhere else (I4/I5).
# ---------------------------------------------------------------------------
def tuple_class(state, tier_basis, conv_status, rso):
    if state == "pending":
        return "pending"
    if rso:
        return "regulatory_stratum_only"
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
        "disabled_person": "Research and disabled people's own published experience both "
                           "address this. This is an evidence-based recommendation, not just "
                           "a building rule.",
        "carer": "Research and disabled people's published experience both support attention "
                 "to this feature. It is an evidence-based recommendation, not just a rule.",
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
    "regulatory_stratum_only": {
        "designer": "Regulatory-stratum value [◐]: standards/codes converge ({basis}); "
                    "no anchoring evidence (T1/Co-1/T2/Co-2) exists for this cell.",
        "ot": "Regulatory-stratum value only ({basis}): no clinical, lived-experience, or "
              "CPG anchor exists; treat the value as a compliance floor, not a clinical target.",
        "policymaker": "Standards converge ({basis}). Convergence is not evidence: no "
                       "T1/Co-1/T2/Co-2 anchor exists. Treat this value as floor, not target — "
                       "the jurisdictions could all be wrong together.",
        "disabled_person": "Building rules in several countries agree on this, but there's no "
                           "research or lived-experience evidence yet showing it's what "
                           "actually works best. You can ask for better than the rule.",
        "carer": "Building rules agree on this, but no research or lived-experience evidence "
                 "yet shows it's what works best.",
        "advocacy_brief": "The law sets a floor here, and NO evidence yet shows that floor is "
                          "enough. That gap is itself an advocacy point: demand the research.",
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
    q = ("SELECT cell_id,item_code,population_code,state,design_scale,convergence_id,"
         "tier_basis,governing_refs,rule_version,derivation_sha,code_floor_only,"
         "confidence_synthesis_basis,gap_register_id,falsification_condition "
         "FROM evidence_cell_state ORDER BY cell_id")
    for r in conn.execute(q):
        c = dict(zip(("cell_id", "item_code", "population", "state", "design_scale",
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
        cells.append(c)
    return cells


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
        parts.append("Evidence-anchored value range: not yet extracted "
                     "(source_value_extractions empty) — no number is invented here.")
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
                          "ANCHOR: none — no anchoring evidence (T1/Co-1/T2/Co-2) exists for "
                          "this cell; the floor is the only defensible value claim.")
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
        tc = tuple_class(c["state"], c["tier_basis"], c["conv_status"], c["rso"])
        basis = c["tier_basis"] or "no basis"
        blocks = []
        for role in ROLES:
            claim = REGISTER_MAP[tc][role].format(basis=basis)
            body = "".join(f"<p class='emphasis'>{html.escape(p)}</p>"
                           for p in role_body(c, role))
            blocks.append(
                f"<div class='rendering' data-cell='{c['item_code']}×{c['population']}' "
                f"data-role='{role}' data-register='{REGISTERS[role]}' "
                f"data-state='{c['state']}' data-tier-basis='{html.escape(basis)}' "
                f"data-conv='{c['conv_status'] or ''}' data-rso='{c['rso']}' "
                f"data-cfo='{c['code_floor_only']}' data-sha='{c['derivation_sha']}' "
                f"data-rule-version='{c['rule_version']}' data-tuple-class='{tc}'>"
                f"<h4>{role.replace('_', ' ')} · {REGISTERS[role]}</h4>"
                f"<p class='claim-strength'>{html.escape(claim)}</p>{body}</div>")
        rows.append(
            f"<section class='cell' id='{c['item_code']}-{c['population']}'>"
            f"<h2>{html.escape(c['item_name'])} × {c['population']}</h2>"
            f"<p class='tuple'>tuple: state={c['state']} · basis={html.escape(basis)} · "
            f"convergence={c['conv_status']} · rso={c['rso']} · cfo={c['code_floor_only']} "
            f"· sha={c['derivation_sha'][:16]}… · {c['rule_version']}</p>"
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
           "regulatory-stratum-only cells carry no best-practice language in any register "
           "(I3); the policymaker view always pairs floor with anchor (I2).</p>"
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
