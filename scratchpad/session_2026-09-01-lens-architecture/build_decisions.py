#!/usr/bin/env python3
"""Build D-0182..D-0184 into BOTH homes from one source.

The YAML register (which `decision_capture` reads) and the `decisions` table are
separate homes with no sync script -- a rule-5 dual home recorded in the ledger on
2026-08-27. Until it is culled, ratification needs both writes, and the only defence
against them disagreeing is to derive both from one literal. That is what this file is.

  python3 build_decisions.py --yaml    append the three entries to the register
  python3 build_decisions.py --sql     print the INSERTs for a data migration
"""
import argparse, json, sys, yaml

WHEN = "2026-09-01 19:20"
SESSION = "session_2026-09-01-lens-architecture"

OWNER_RATIONALE = (
    "Owner ruling. The lens taxonomy and how a reader browses the book are doctrine -- "
    "mission, audience and population taxonomy sit in governance/decision-protocol.md's "
    "DG-NON class, and CLAUDE.md rule 0 makes a live owner statement non-delegable and "
    "superseding on contact."
)

DECISIONS = [
  dict(
    decision_id="D-0182", category="D-SCHEMA", delegation="DG-NON",
    delegation_rationale=OWNER_RATIONALE,
    summary=("A taxonomy link may be ABSENT from a lens, MUST tie to at least one, and "
             "IDEALLY ties into many."),
    outcome="ADOPTED by owner ruling 2026-09-01.",
    rationale=(
        "Given in three messages during the lens-architecture investigation: \"it is OKAY "
        "for a link to be absent in a related taxonomy column\", \"but a link MUST be tied "
        "to at least one\", \"and ideally it ties into many\". Together they are a "
        "cardinality rule over the four lenses of D-0170, and they settle a question the "
        "schema could not: whether a link row states ONE taxonomy or several. It states as "
        "many as are known, and at least one. The owner's own example -- an evidence row "
        "concerning ICF codes for assistive mobility devices that also concerns wheelchair "
        "identity and also paraplegia medically -- is one fact, so it is one row. Measured "
        "2026-09-01: the rule is expressible in SQLite as a table-level "
        "CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL), "
        "which admits the four-lens row, admits a single-lens row with three NULLs, and "
        "refuses a row that states no lens at all. All three were tested against the live "
        "shape before this was recorded."
    ),
    alternatives_considered=[
        "Exactly one lens per row (CHECK (...) = 1) -- this was the parked design in the "
        "migration 065 generator, and the ruling reverses it: it forbids the owner's own "
        "wheelchair example, which is one fact stating three lenses.",
        "No constraint at all -- rejected by the ruling's second clause; a link tied to no "
        "taxonomy is unreachable from every lens and renders nowhere.",
    ],
    decision_date=WHEN, decided_by="jordanelias",
    model_routing="human/none/none", effort_level="0",
    decision_artifacts=[
        "decisions/DR-2026-09-01-a-link-states-at-least-one-lens-ideally-many.md",
        "scripts/migrations/065_one_link_table_four_lenses.sql",
        "scratchpad/session_2026-09-01-lens-architecture/LENS-ARCHITECTURE.md",
    ],
    predecessors=["D-0170"], supersedes=[], status="ACTIVE", review_status="NA",
    notes=(
        "The ideally-many clause is an AUTHORING aim, not a constraint, and is deliberately "
        "not mechanised: a CHECK demanding two lenses would refuse the 372 identity-only "
        "rows that already exist and every honest single-lens fact after them. What the "
        "crossing maps become is the aid to it -- when an identity link is recorded they "
        "suggest the ICF and needs codes that probably belong on the same row, for a human "
        "or a synthesis step to confirm. They stop being render machinery."
    ),
  ),
  dict(
    decision_id="D-0183", category="D-SCHEMA", delegation="DG-NON",
    delegation_rationale=OWNER_RATIONALE,
    summary=("rationale_ref points at the DECISION that authorises the edge -- "
             "decisions.decision_id, a typed foreign key."),
    outcome="ADOPTED by owner ruling 2026-09-01.",
    rationale=(
        "D-0175 (OD-A) rules these links substrate provisionally: any edge a determination "
        "relies on must be re-derived and carry a rationale_ref in that determination's own "
        "migration. Measured 2026-08-31, that obligation was unenforceable -- rationale_ref "
        "was an unconstrained INTEGER with no foreign key, so it referenced nothing and ANY "
        "integer satisfied \"carries a rationale_ref\". Asked what it should point at, the "
        "owner ruled: the decision that authorises it. That makes the column TEXT REFERENCES "
        "decisions(decision_id), so a fabricated warrant is refused by the database rather "
        "than by attention."
    ),
    alternatives_considered=[
        "Point at evidence_sources.ref_id -- rejected by the ruling; an edge is authorised by "
        "a decision, and the evidence behind that decision is reached through it by pointer.",
        "Leave it untyped and enforce by check -- rejected: a check reads what a constraint "
        "could have refused, and every one of the 372 rows proved the column inert.",
    ],
    decision_date=WHEN, decided_by="jordanelias",
    model_routing="human/none/none", effort_level="0",
    decision_artifacts=[
        "decisions/DR-2026-09-01-rationale-ref-points-at-the-decision.md",
        "scripts/migrations/065_one_link_table_four_lenses.sql",
    ],
    predecessors=["D-0175"], supersedes=[], status="ACTIVE", review_status="NA",
    notes=(
        "The column stays NULLABLE and all 530 existing rows keep NULL. OD-A's debt is paid "
        "where an edge is USED, and making it NOT NULL would either forge 530 warrants or "
        "block the table entirely. This also discharges the correction D-0175's own notes "
        "demanded: the parked 065 generator DROPPED rationale_ref on the grounds that it was "
        "0 of 372 populated, and OD-A makes it the column where the debt is paid. It is kept."
    ),
  ),
  dict(
    decision_id="D-0184", category="D-SCHEMA", delegation="DG-REVIEW",
    delegation_rationale=(
        "Schema shape, not doctrine. CLAUDE.md §1 places code and tables outside the "
        "owner gate and puts the burden of proof on ADDING apparatus; this removes a table "
        "rather than adding one. It is DG-REVIEW rather than DG-AUTO because it changes the "
        "shape the render layer will be built against, which the owner is entitled to see "
        "before the site is written."
    ),
    summary=("The lens is a COLUMN, not a traversal: one item×taxonomy link table with "
             "four nullable lens pointers. item_axis_links is folded in; "
             "base_taxonomy_medical is created."),
    outcome=(
        "ADOPTED and landed as migration 065. item_population_links (372) and "
        "item_axis_links (158) become item_taxonomy_links (530), carrying identity_code, "
        "icf_code, needs_code and medical_code. base_taxonomy_medical is created empty."
    ),
    rationale=(
        "Executes D-0170's four lenses and D-0182's cardinality against the owner's stated "
        "goal of a dynamically rendering site with a multimodal lens and filters. The "
        "alternative -- store a fact in one lens and cross to the others at render through "
        "population_axis_map / access_need_axis_map -- was measured on 2026-09-01 and fails "
        "twice. (1) THE CROSSINGS ARE INCOMPLETE: identity→ICF 20 of 23, ICF→identity "
        "16 of 17, needs→ICF 15 of 17, ICF→needs 15 of 17, and identity↔needs has "
        "no direct map at all; every gap is a silently empty page rather than a \"no results\" "
        "page. (2) TRAVERSAL MANUFACTURES INFERENCE AND CHANGES THE ANSWER: the identity lens "
        "asked for DEAF returns 20 items, while the ICF lens asked for AX-AUD -- the axis DEAF "
        "crosses to -- returns 38 rows, because DEAFBLIND crosses to AX-AUD too. Only the "
        "first is a recorded fact. D-0174 reserves applicability to synthesis, so a render "
        "layer that crosses is adjudicating where nothing reviews it and no attestation "
        "covers it. With the lens as a column the render is WHERE <lens>_code = ?, one query "
        "shape for four lenses, and no UNION anywhere -- a UNION is only forced when the "
        "taxonomies live in separate link tables, which is the state this ends."
    ),
    alternatives_considered=[
        "Keep item_axis_links and add lens columns only to item_population_links -- rejected: "
        "the ICF lens keeps two homes (rule 5) and every lens-neutral render query needs a "
        "UNION over two shapes.",
        "Change only rationale_ref's type now and reshape later -- rejected: it rebuilds the "
        "same table twice and sweeps its callers twice, which is the failure CLAUDE.md §0.4 "
        "describes.",
        "Merge strength_band into applicability -- rejected: they are different qualifiers and "
        "merging them is a doctrinal judgement, not a schema migration. Both columns survive.",
    ],
    decision_date=WHEN, decided_by=SESSION,
    model_routing="opus/200/synth", effort_level="200",
    decision_artifacts=[
        "decisions/DR-2026-09-01-the-lens-is-a-column-not-a-traversal.md",
        "scripts/migrations/065_one_link_table_four_lenses.sql",
        "scratchpad/session_2026-09-01-lens-architecture/LENS-ARCHITECTURE.md",
        "scratchpad/session_2026-09-01-lens-architecture/insurance/",
    ],
    predecessors=["D-0170", "D-0175", "D-0182", "D-0183"], supersedes=[],
    status="ACTIVE", review_status="PENDING",
    notes=(
        "TWO THINGS GIVEN UP, STATED RATHER THAN BURIED. (1) UNIQUENESS IS WEAKER. The old "
        "primary keys were (item_code, population_code, subtype) and (item_code, axis_code); "
        "the wide form must permit A-18×DEAF×AX-AUD beside A-18×DEAF×AX-SPR, "
        "which are two mechanisms and not a duplicate. idx_itl_row_identity keeps every full "
        "lens tuple unique, but an identity-only row is no longer structurally prevented from "
        "sitting beside a wide row already carrying that identity. That residual dual-home "
        "risk is an audit's job, not a constraint's, and the audit is OWED. (2) APPLICABILITY "
        "IS NULLABLE NOW. It was NOT NULL DEFAULT 'applies'; the 158 folded axis rows never "
        "carried it, and defaulting them would assert a judgement nobody made -- exactly the "
        "inference D-0174 reserves to synthesis. NULL means not adjudicated. ALSO OWED: the "
        "graph extractor draws only the identity lens, because `axes` is absent from its "
        "PRIMARY node registry and emitting the ICF edge would fire ref.dangling_structural "
        "on all 158 rows; registering `axes` is the one-line fix and it changes audit output, "
        "so it was not smuggled into a rename sweep. Coverage is unchanged either way -- "
        "item_axis_links was never extracted. base_taxonomy_medical is created EMPTY and no "
        "row can reference it until it is populated, which is content (DG-NON) and the "
        "owner's alone; it is created now because SQLite cannot add a table-level CHECK by "
        "ALTER, so a medical_code bolted on later would sit outside the at-least-one rule."
    ),
  ),
]

COLS = ["decision_id","category","delegation","delegation_rationale","summary","outcome",
        "rationale","decision_date","decided_by","model_routing","effort_level","status",
        "review_status","supersedes","predecessors","decision_artifacts",
        "alternatives_considered","notes"]
JSON_COLS = {"supersedes","predecessors","decision_artifacts","alternatives_considered"}

def sql_lit(v):
    return "'" + str(v).replace("'", "''") + "'"

def emit_sql():
    out = []
    for d in DECISIONS:
        vals = []
        for c in COLS:
            v = d[c]
            vals.append(sql_lit(json.dumps(v) if c in JSON_COLS else v))
        vals += [sql_lit(WHEN), sql_lit(SESSION), sql_lit(WHEN), sql_lit(SESSION)]
        cols = ", ".join(COLS + ["created_at","created_by_session","updated_at","updated_by_session"])
        out.append(f"INSERT INTO decisions ({cols}) VALUES ({', '.join(vals)});")
    return "\n".join(out)

def emit_yaml():
    reg = yaml.safe_load(open("data/decisions/decision_register.yaml"))
    have = {d["decision_id"] for d in reg["decisions"]}
    for d in DECISIONS:
        if d["decision_id"] in have:
            sys.exit(f"{d['decision_id']} already in the register -- refusing to double-write")
        e = {c: d[c] for c in COLS}
        e["effort_level"] = str(e["effort_level"])
        reg["decisions"].append(e)
    reg["last_updated"] = WHEN
    with open("data/decisions/decision_register.yaml", "w") as f:
        yaml.safe_dump(reg, f, sort_keys=False, width=110, allow_unicode=True,
                       default_flow_style=False)
    print(f"appended {len(DECISIONS)} decisions; last_updated={WHEN}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--yaml", action="store_true"); ap.add_argument("--sql", action="store_true")
    a = ap.parse_args()
    if a.sql: print(emit_sql())
    elif a.yaml: emit_yaml()
    else: ap.error("need --yaml or --sql")
