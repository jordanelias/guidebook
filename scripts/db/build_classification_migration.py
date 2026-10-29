#!/usr/bin/env python3
"""
scripts/db/build_classification_migration.py — emit the data-migration SQL that seeds the
classification vocabularies (migration 026) and tags every evidence source.

Reads the DB READ-ONLY and prints SQL to stdout; pipe it to scripts/emit_data_migration.py:

    python3 scripts/db/build_classification_migration.py | \\
        python3 scripts/emit_data_migration.py \\
            --session session_2026-10-29-classification-codes.md \\
            --summary "seed ICF/access-need vocabularies; tag evidence_sources by population/ICF/need"

Tagging is layered, and every row records its method + confidence + review_status:

  manual-read              hand-assigned after reading the abstract (MANUAL below). Still UNREVIEWED
                           until the owner reviews; confidence reflects what the abstract states.
  population-match-record  from evidence_population_match.target/study_population text.
  title-keyword            explicit disability/population term in the source title (regex rules).
  slug-item-link           'cited-for': populations of the Guidebook items the source's BPC slug supports.
  derived-from-population-map   ICF / access-need tags inferred from 'subject' population tags via the
                           PROVISIONAL maps below. Never independent classification.

Nothing here is verified by a human reviewer: all rows are UNREVIEWED. The vocabularies and maps are
PROVISIONAL (owner / functional-deficit review required). Population 'ALL' is the universal design scale.
"""

import os
import re
import sqlite3
import sys
from pathlib import Path

DB = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))
SESSION = "session_2026-10-29-classification-codes"
NOW = "2026-10-29 12:00"

ICF = {  # WHO ICF categories (b = body functions, d = activities/participation, e = environment)
    "b110": "Consciousness functions", "b114": "Orientation functions", "b117": "Intellectual functions",
    "b1300": "Energy level", "b134": "Sleep functions", "b140": "Attention functions",
    "b144": "Memory functions", "b152": "Emotional functions", "b156": "Perceptual functions",
    "b210": "Seeing functions", "b230": "Hearing functions",
    "b270": "Sensory functions related to temperature and other stimuli", "b280": "Sensation of pain",
    "b420": "Blood pressure functions", "b435": "Immunological system functions",
    "b455": "Exercise tolerance functions", "b4552": "Fatiguability",
    "b710": "Mobility of joint functions", "b730": "Muscle power functions", "b735": "Muscle tone functions",
    "b760": "Control of voluntary movement functions", "b765": "Involuntary movement functions",
    "b770": "Gait pattern functions",
    "d115": "Listening", "d160": "Focusing attention", "d240": "Handling stress and other psychological demands",
    "d410": "Changing basic body position", "d420": "Transferring oneself", "d440": "Fine hand use",
    "d445": "Hand and arm use", "d450": "Walking", "d455": "Moving around",
    "d460": "Moving around in different locations", "d465": "Moving around using equipment",
    "e120": "Products and technology for personal indoor and outdoor mobility and transportation",
    "e150": "Design, construction and building products and technology of buildings for public use",
    "e155": "Design, construction and building products and technology of buildings for private use",
}

NEEDS = {
    "AN-01": ("Step-free route", "A continuous route without steps or abrupt level changes."),
    "AN-02": ("Low-effort movement", "Routes and features that limit the strength, stamina or energy needed to move."),
    "AN-03": ("Rest and recovery opportunities", "Places to stop, sit or recover along routes."),
    "AN-04": ("Space to manoeuvre, turn and pass", "Room for wheeled mobility, mobility aids and passing."),
    "AN-05": ("Stable footing and handrail support", "Slip-resistant, even surfaces and graspable support."),
    "AN-06": ("Reachable and operable controls", "Controls and hardware usable with limited reach, grip or dexterity."),
    "AN-07": ("Clear visual information", "Contrast, lighting and legible signage."),
    "AN-08": ("Clear auditory environment", "Controlled noise and reverberation; hearing-support systems."),
    "AN-09": ("Predictable, calm sensory environment", "Limited and controllable sensory load (sound, light, pattern)."),
    "AN-10": ("Simple orientation and wayfinding", "Legible layout and cognitive support for finding the way."),
    "AN-11": ("Thermal comfort and temperature control", "Stable, controllable temperature."),
    "AN-12": ("Control, privacy and psychological safety", "Predictability, retreat and a sense of safety and control."),
    "AN-13": ("Pain-minimising surfaces and postures", "Features that avoid provoking pain (hard surfaces, vibration, awkward postures)."),
    "AN-14": ("Clean air and low chemical exposure", "Low pollutant, allergen and chemical load."),
}

# population -> (primary ICF codes, secondary ICF codes). PROVISIONAL.
POP_ICF = {
    "ADHD": (["b140", "d160"], []),
    "AUT": (["b156", "b152", "d240"], []),
    "NDV": (["b140", "b156", "d240"], []),
    "SENS": (["b156", "d240"], ["b270"]),
    "PCS": (["b140", "b144"], ["b156", "b280"]),
    "MH": (["b152", "b134", "d240"], []),
    "DEM": (["b114", "b144", "b117"], []),
    "EPI": (["b110", "b765"], []),
    "MS": (["b4552", "b730", "b735", "b770"], ["b270"]),
    "NEU": (["b760", "b770"], ["b735"]),
    "CFS": (["b1300", "b4552", "b455"], ["b280"]),
    "OFS": (["b4552", "b455", "b420"], []),
    "POTS": (["b420", "b455", "b4552"], []),
    "MCAS": (["b435"], []),
    "PAIN": (["b280"], ["d450"]),
    "MOB": (["d450", "d455", "d465", "b770", "b730"], ["b710"]),
    "SCI": (["b730", "b735", "d465", "d420", "d410"], ["b420"]),
    "UPL": (["b710", "b730", "d445", "d440"], []),
    "VIS": (["b210"], ["d460"]),
    "DEAF": (["b230"], ["d115"]),
    "DBL": (["b210", "b230"], ["d460"]),
}

POP_NEED = {
    "MOB": ["AN-01", "AN-02", "AN-04", "AN-05"], "SCI": ["AN-01", "AN-02", "AN-04", "AN-11"],
    "UPL": ["AN-02", "AN-05", "AN-06"], "OFS": ["AN-02", "AN-03", "AN-11"],
    "CFS": ["AN-02", "AN-03", "AN-09"], "POTS": ["AN-02", "AN-03", "AN-11"],
    "MS": ["AN-01", "AN-02", "AN-03", "AN-11"], "NEU": ["AN-01", "AN-02", "AN-05"],
    "PAIN": ["AN-02", "AN-03", "AN-05", "AN-13"], "VIS": ["AN-05", "AN-07", "AN-10"],
    "DEAF": ["AN-07", "AN-08"], "DBL": ["AN-05", "AN-07", "AN-08", "AN-10"],
    "DEM": ["AN-09", "AN-10", "AN-12"], "AUT": ["AN-09", "AN-10", "AN-12"],
    "NDV": ["AN-09", "AN-10"], "ADHD": ["AN-09", "AN-10"], "SENS": ["AN-09", "AN-11"],
    "PCS": ["AN-07", "AN-08", "AN-09"], "MH": ["AN-09", "AN-12"], "EPI": ["AN-05", "AN-09"],
    "MCAS": ["AN-11", "AN-14"],
}

# (population, regex over lower-cased title, confidence). Evaluated on title text.
RULES = [
    ("DBL", r"deaf-?\s?blind", "medium"),
    ("DEAF", r"\bdeaf\b|hearing (loss|impair|aid)|cochlear|hard of hearing|\bhoh\b", "medium"),
    ("VIS", r"visual(ly)? impair|vision impair|low vision|\bblind|sight loss|visually", "medium"),
    ("VIS", r"tactile (walking )?surface|tactile paving|\btwsi\b|\btgsi\b", "low"),
    ("SCI", r"spinal cord|tetraplegi|quadriplegi|paraplegi", "medium"),
    ("MOB", r"wheelchair|wheeled mobility|mobility (impair|limit|aid|device)|walking aid|rollator|ambulant|manual chair", "medium"),
    ("MOB", r"\bscooter", "low"),
    ("UPL", r"upper[- ]limb|upper extremity|\bgrip\b|dexterity|hand function", "medium"),
    ("DEM", r"dementia|alzheimer", "medium"),
    ("AUT", r"autis", "medium"),
    ("AUT", r"\basd\b", "low"),
    ("ADHD", r"adhd|attention[- ]deficit", "medium"),
    ("NDV", r"neurodiver|neurodevelopment|neurodivergen", "medium"),
    ("MH", r"mental health|psychiatr|depress|anxiety|ptsd|trauma-informed", "medium"),
    ("MS", r"multiple sclerosis", "medium"),
    ("EPI", r"epilep|seizure", "medium"),
    ("CFS", r"chronic fatigue|myalgic|me/cfs", "medium"),
    ("POTS", r"postural.{0,20}tachycardia|\bpots\b", "medium"),
    ("MCAS", r"mast cell", "medium"),
    ("PAIN", r"chronic pain|fibromyalgia|arthritis", "medium"),
    ("PAIN", r"\bpain\b", "low"),
    ("OFS", r"orthostatic", "medium"),
    ("OFS", r"fatigue", "low"),
    ("PCS", r"concussion", "medium"),
    ("SENS", r"sensory (processing|sensitiv|integration)|snoezelen|sensory room", "low"),
    ("NEU", r"neurolog|stroke|parkinson|cerebral palsy", "medium"),
]
MATCH_ONLY_RULES = [("ALL", r"healthy adults|general population|able-bodied|normal subjects", "low")]
CODE_TOKEN = re.compile(r"\b(NDV|AUT|DEAF|MS|SCI|UPL|PAIN|DEM|MOB|VIS|OFS|ADHD|DBL|CFS|POTS|PCS|MH|EPI|SENS|NEU)\b")

# Hand-assigned after reading the abstract (evidence/s14-abstracts-manual-read.txt).
# (ref_ids, population, role, confidence, basis)
MANUAL_POP = [
    (["REF-00388"], "SCI", "subject", "high", "Abstract (Yang et al. 2012): 36 manual wheelchair users with SCI T8-L2; level vs 3-degree slope."),
    (["REF-00388"], "MOB", "subject", "high", "Abstract: manual wheelchair propulsion kinematics/kinetics, level vs 3-degree slope."),
    (["REF-00037", "REF-VERIFIED-003"], "MOB", "subject", "high", "Abstract (Rouvier 2022 PLoS One): systematic review, 34 studies of manual wheelchair users crossing slope/cross-slope/curb/ground; study-population mix not stated in abstract."),
    (["REF-00037", "REF-VERIFIED-003"], "UPL", "subject", "medium", "Abstract: outcome focus is upper-limb stress and fatigue during manual wheelchair propulsion."),
    (["REF-00385"], "ALL", "subject", "high", "Abstract (Waters & Mulroy 1988): 260 normal subjects aged 6-80; normative walking-energy tables; not a disability population."),
    (["REF-00025"], "ALL", "subject", "high", "Abstract (Lawati 2017): 214 able-bodied students learning a manual-wheelchair threshold skill; proxy (non-wheelchair-user) population."),
    (["REF-00070"], "SCI", "subject", "high", "Abstract (Sawatzky 2015): consensus update of clinical guidelines for upper-extremity preservation in spinal cord injury."),
    (["REF-00070"], "UPL", "subject", "medium", "Abstract: upper-extremity preservation guidance."),
]
MANUAL_ICF = [
    (["REF-00388", "REF-00037", "REF-VERIFIED-003"], "d465", "high", "Manual wheelchair propulsion = moving around using equipment."),
    (["REF-00388", "REF-00037", "REF-VERIFIED-003", "REF-00386", "REF-00030"], "e150", "medium", "Studies a slope/ramp environmental barrier; e150 is the nearest ICF environment code (ICF has no ramp-specific code)."),
    (["REF-00385"], "b455", "medium", "Energy expenditure of walking (exercise tolerance functions)."),
]
MANUAL_NEED = [
    (["REF-00388", "REF-00037", "REF-VERIFIED-003", "REF-00386", "REF-00030"], "AN-02", "medium", "Studies propulsion force/effort on slopes."),
    (["REF-00037", "REF-VERIFIED-003", "REF-00386", "REF-00030"], "AN-01", "medium", "Slope/ramp as the step-free route."),
    (["REF-00385"], "AN-02", "medium", "Normative energy cost of walking."),
]


def q(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


def insert(table, cols, rows):
    if not rows:
        return ""
    out = []
    for i in range(0, len(rows), 200):
        chunk = rows[i:i + 200]
        vals = ",\n  ".join("(" + ", ".join(q(str(v)) if v is not None else "NULL" for v in r) + ")" for r in chunk)
        out.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES\n  {vals};")
    return "\n".join(out) + "\n"


def main():
    db = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    pops = {r[0] for r in db.execute("SELECT population_code FROM populations")}
    refs = {r[0] for r in db.execute("SELECT ref_id FROM evidence_sources")}
    title = {r[0]: " ".join(x or "" for x in r[1:]).lower() for r in db.execute(
        "SELECT ref_id, pub_title, pub_subtitle, book_title FROM evidence_sources")}

    tags = {}  # (ref, pop, role, method) -> (confidence, basis)

    def add(ref, pop, role, method, conf, basis):
        assert ref in refs, ref
        assert pop in pops, pop
        tags.setdefault((ref, pop, role, method), (conf, basis))

    # manual-read
    for ref_ids, pop, role, conf, basis in MANUAL_POP:
        for ref in ref_ids:
            add(ref, pop, role, "manual-read", conf, basis)

    # population-match-record
    for mid, ref, tp, sp in db.execute("SELECT match_id, ref_id, target_population, study_population FROM evidence_population_match WHERE ref_id IS NOT NULL"):
        text = f"{tp or ''} {sp or ''}"
        found = {m for m in CODE_TOKEN.findall(text)}
        low = text.lower()
        for pop, rx, conf in RULES + MATCH_ONLY_RULES:
            if re.search(rx, low):
                found.add(pop)
        if "DBL" in found:
            found -= {"DEAF", "VIS"}
        for pop in sorted(found):
            add(ref, pop, "subject", "population-match-record", "medium",
                f"evidence_population_match {mid}: target={(tp or '')[:80]!r}; study={(sp or '')[:80]!r}")

    # title-keyword
    for ref, t in title.items():
        found = {}
        for pop, rx, conf in RULES:
            if re.search(rx, t) and (pop not in found or conf == "medium"):
                found[pop] = conf
        if "DBL" in found:
            found.pop("DEAF", None)
            found.pop("VIS", None)
        if "CFS" in found:
            found.pop("OFS", None)
        for pop, conf in sorted(found.items()):
            add(ref, pop, "subject", "title-keyword", conf, "Explicit term in source title (rule-based; abstract not read).")

    # slug-item-link (cited-for)
    cited = {}
    for ref, slug, pop, item in db.execute("""
        SELECT ssl.ref_id, ssl.slug, ipl.population_code, i.item_code
        FROM source_slug_links ssl
        JOIN items i ON i.bpc_source_slug = ssl.slug
        JOIN item_population_links ipl ON ipl.item_code = i.item_code
        WHERE ssl.ref_id IN (SELECT ref_id FROM evidence_sources)"""):
        cited.setdefault((ref, pop), set()).add((slug, item))
    for (ref, pop), si in sorted(cited.items()):
        slugs = sorted({s for s, _ in si})
        items = sorted({i for _, i in si})
        add(ref, pop, "cited-for", "slug-item-link", "low",
            f"Cited under {', '.join(slugs)}, which supports item(s) {', '.join(items)} for this population.")

    # ICF / need tags
    icf_tags, need_tags = {}, {}
    for (ref, pop, role, method), (conf, basis) in tags.items():
        if role != "subject":
            continue
        for rel, codes in (("primary", POP_ICF.get(pop, ([], []))[0]),):
            for code in codes:
                icf_tags.setdefault((ref, code, "derived-from-population-map"), set()).add(pop)
        for code in POP_NEED.get(pop, []):
            need_tags.setdefault((ref, code, "derived-from-population-map"), set()).add(pop)
    icf_rows, need_rows = [], []
    for (ref, code, method), ps in sorted(icf_tags.items()):
        icf_rows.append((ref, code, method, "low", "UNREVIEWED",
                         f"Derived from subject population(s) {', '.join(sorted(ps))} via population_icf_map (provisional)."))
    for ref_ids, code, conf, basis in MANUAL_ICF:
        for ref in ref_ids:
            assert ref in refs and code in ICF
            icf_rows.append((ref, code, "manual-read", conf, "UNREVIEWED", basis))
    for (ref, code, method), ps in sorted(need_tags.items()):
        need_rows.append((ref, code, method, "low", "UNREVIEWED",
                          f"Derived from subject population(s) {', '.join(sorted(ps))} via population_access_need_map (provisional)."))
    for ref_ids, code, conf, basis in MANUAL_NEED:
        for ref in ref_ids:
            assert ref in refs and code in NEEDS
            need_rows.append((ref, code, "manual-read", conf, "UNREVIEWED", basis))

    sql = ["-- Seed ICF / access-need vocabularies and tag evidence_sources. Generated by",
           "-- scripts/db/build_classification_migration.py (deterministic; read the script for rules).",
           "-- All tags UNREVIEWED; vocabularies and maps PROVISIONAL.", ""]
    sql.append(insert("icf_codes", ["icf_code", "chapter", "title", "created_at", "created_by_session"],
                      [(c, c[0], t, NOW, SESSION) for c, t in sorted(ICF.items())]))
    sql.append(insert("access_needs", ["need_code", "label", "description", "status", "created_at", "created_by_session"],
                      [(c, l, d, "PROVISIONAL", NOW, SESSION) for c, (l, d) in sorted(NEEDS.items())]))
    basis_icf = "Provisional: ICF domain most associated with this population's design-relevant impairment; owner/functional-deficit review required."
    sql.append(insert("population_icf_map", ["population_code", "icf_code", "relation", "basis", "review_status", "created_at", "created_by_session"],
                      [(p, c, rel, basis_icf, "PROVISIONAL", NOW, SESSION)
                       for p, (prim, sec) in sorted(POP_ICF.items()) for rel, cs in (("primary", prim), ("secondary", sec)) for c in cs]))
    basis_need = "Provisional: access need commonly associated with this population in the Guidebook's evidence; owner review required."
    sql.append(insert("population_access_need_map", ["population_code", "need_code", "basis", "review_status", "created_at", "created_by_session"],
                      [(p, n, basis_need, "PROVISIONAL", NOW, SESSION) for p, ns in sorted(POP_NEED.items()) for n in ns]))
    sql.append(insert("source_population_tags",
                      ["ref_id", "population_code", "role", "method", "confidence", "review_status", "basis", "created_at", "created_by_session"],
                      [(r, p, ro, m, c, "UNREVIEWED", b, NOW, SESSION) for (r, p, ro, m), (c, b) in sorted(tags.items())]))
    sql.append(insert("source_icf_tags", ["ref_id", "icf_code", "method", "confidence", "review_status", "basis", "created_at", "created_by_session"],
                      [r + (NOW, SESSION) for r in icf_rows]))
    sql.append(insert("source_need_tags", ["ref_id", "need_code", "method", "confidence", "review_status", "basis", "created_at", "created_by_session"],
                      [r + (NOW, SESSION) for r in need_rows]))
    print("\n".join(sql))

    by_method = {}
    for (_, _, _, m) in tags:
        by_method[m] = by_method.get(m, 0) + 1
    sources_tagged_subject = len({r for (r, p, ro, m) in tags if ro == "subject"})
    sources_any = len({r for (r, *_x) in tags})
    print(f"-- STATS population tags={len(tags)} by_method={by_method}; sources with subject tag={sources_tagged_subject}/{len(refs)}; "
          f"with any tag={sources_any}/{len(refs)}; icf rows={len(icf_rows)}; need rows={len(need_rows)}", file=sys.stderr)


if __name__ == "__main__":
    main()
