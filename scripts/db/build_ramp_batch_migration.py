#!/usr/bin/env python3
"""
scripts/db/build_ramp_batch_migration.py

Emit the SQL for the 2026-10-29 ramp-slope research batch (E-03): 12 literature
sources plus the current Irish and Singapore code editions, with population /
ICF / access-need tags. Prints SQL on stdout; pipe into emit_data_migration.py:

    python -X utf8 scripts/db/build_ramp_batch_migration.py | \
      python scripts/emit_data_migration.py \
        --session session_2026-10-29-ramp-slopes-research-batch.md \
        --summary "add 12 ramp-slope studies and current IE/SG code rows with classification tags"

Provenance of every row: audits/research-batch-ramp-slopes-2026-10-29/findings.md.
Literature was read at abstract level only (Consensus search results, no DOI
supplied), so those rows are UNVERIFIED-1 / AUTHOR-TITLE-ONLY and DOI is left
NULL. Nothing here invents a DOI.
"""

SESSION = "session_2026-10-29-ramp-slopes-research-batch"
NOW = "2026-10-29 19:30"
ABS_NOTE = ("Abstract-level read via Consensus search 2026-10-29 (ramp-slopes research batch); "
            "no DOI supplied by the search, DOI not yet resolved; full text not read. Tier is provisional.")


def q(v):
    if v is None:
        return "NULL"
    if isinstance(v, int):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


# (ref_id, last, first, authors_display, year, title, journal, pops, icfs, needs, proxy_note)
# pops: (code, confidence, basis); icfs/needs: (code, confidence)
LIT = [
    ("REF-00738", "Chow", "J.", "Chow J et al.", 2009,
     "Kinematic and electromyographic analysis of wheelchair propulsion on ramps of different slopes for young men with paraplegia",
     "Archives of Physical Medicine and Rehabilitation",
     [("MOB", "high", "Manual wheelchair users (10 men with paraplegia)."),
      ("SCI", "medium", "Paraplegia; abstract does not state spinal cord injury explicitly.")],
     [("d465", "high"), ("b730", "medium")], [("AN-02", "medium")], None),
    ("REF-00739", "Hashizume", "T.", "Hashizume T et al.", 2015,
     "Biomechanics and Physiology for Propelling Wheelchair Uphill Slope",
     "Studies in Health Technology and Informatics",
     [("SCI", "high", "Five wheelchair users with cervical cord injury tested at 5-12.5 % slopes."),
      ("MOB", "high", "Manual wheelchair users.")],
     [("d465", "high"), ("b455", "medium")], [("AN-02", "medium")], None),
    ("REF-00740", "Bertocci", "G.", "Bertocci G et al.", 2018,
     "Manual wheelchair propulsion on ramp slopes encountered when boarding public transit buses",
     "Disability and Rehabilitation: Assistive Technology",
     [], [("d465", "medium")], [("AN-02", "medium")],
     "Proxy sample: seven able-bodied adults with no propulsion experience; not tagged to a population."),
    ("REF-00741", "Choi", "Y.-O.", "Choi Y-O et al.", 2015,
     "Effects of ramp slope on physiological characteristic and performance time of healthy adults propelling and pushing wheelchairs",
     "Journal of Physical Therapy Science",
     [], [("d465", "medium"), ("b455", "low")], [("AN-02", "medium")],
     "Proxy sample: 24 healthy adults; not tagged to a population."),
    ("REF-00742", "Lenker", "J.", "Lenker J et al.", 2016,
     "Usability evaluation of access ramps in transit buses: Preliminary findings",
     "Journal of Public Transportation",
     [("MOB", "high", "27 adults: manual and power wheelchair users."),
      ("VIS", "high", "Includes people with vision impairment using a cane or service animal.")],
     [("d465", "high"), ("d455", "medium"), ("b730", "low")], [("AN-02", "medium"), ("AN-05", "medium")], None),
    ("REF-00743", "Pierret", "B.", "Pierret B et al.", 2014,
     "Cardio-respiratory and subjective strains sustained by paraplegic subjects, when travelling on a cross slope in a manual wheelchair (MWC)",
     "Applied Ergonomics",
     [("MOB", "high", "25 paraplegic manual wheelchair users."),
      ("SCI", "medium", "Paraplegia; abstract does not state spinal cord injury explicitly.")],
     [("d465", "high"), ("b455", "medium")], [("AN-02", "medium")],
     "Cross-slope study: belongs with the cross-slope item, not E-03 running slope."),
    ("REF-00744", "Flemmer", "C.", "Flemmer C et al.", 2026,
     "Analysis of the effect of path cross slope on manual wheelchair propulsion",
     "Disability and Rehabilitation: Assistive Technology",
     [("MOB", "medium", "Mechanical model of manual wheelchair propulsion; no participants.")],
     [("d465", "medium")], [("AN-02", "medium")],
     "Cross-slope mechanical model: belongs with the cross-slope item, not E-03 running slope."),
    ("REF-00745", "Har-Nir", "I.", "Har-Nir I et al.", 2022,
     "Energy expenditure and perceived effort during uphill and downhill walking in people with multiple sclerosis",
     "European Journal of Physical and Rehabilitation Medicine",
     [("MS", "high", "18 ambulatory people with multiple sclerosis (mean EDSS 2.9).")],
     [("d455", "high"), ("b455", "medium")], [("AN-02", "medium")], None),
    ("REF-00746", "Liu", "H.", "Liu H et al.", 2023,
     "Comparison of gait between walking up and down an incline with a walking device in older adults",
     "Geriatric Nursing",
     [("MOB", "medium", "26 older adults walking with a cane or rolling walker; no older-adult population code exists.")],
     [("d455", "medium"), ("d465", "medium"), ("b770", "medium")], [("AN-05", "medium")], None),
    ("REF-00747", "Leone", "C.", "Leone C et al.", 2016,
     "Prevalence of Walking-Related Motor Fatigue in Persons With Multiple Sclerosis",
     "Neurorehabilitation and Neural Repair",
     [("MS", "high", "208 people with multiple sclerosis, EDSS up to 6.5.")],
     [("b4552", "high"), ("d450", "medium")], [("AN-03", "medium")],
     "Context for endurance limits; walking test on level ground, not a slope study."),
    ("REF-00748", "Lay", "A. N.", "Lay AN et al.", 2005,
     "The effects of sloped surfaces on locomotion: a kinematic and kinetic analysis",
     "Journal of Biomechanics",
     [], [("b770", "medium"), ("d450", "low")], [],
     "Proxy sample: nine healthy volunteers; not tagged to a population."),
    ("REF-00749", "Jahanian", "O.", "Jahanian O et al.", 2022,
     "Hand-rim biomechanics during geared manual wheelchair propulsion over different ground conditions in individuals with spinal cord injury",
     "Journal of Biomechanics",
     [("SCI", "high", "Seven manual wheelchair users with spinal cord injury."),
      ("MOB", "high", "Manual wheelchair users.")],
     [("d465", "high"), ("b730", "low")], [("AN-02", "medium")],
     "Intervention (geared wheels) on one ramp; not a slope-threshold study."),
]

CODE_ROWS = [
    dict(
        ref="REF-00750", last=None, display="Department of Housing, Local Government and Heritage (Ireland)",
        year=2022,
        title="Building Regulations Technical Guidance Document M: Access and Use (2022) - ramped access routes (1.1.3.4, Table 2)",
        publisher="Department of Housing, Local Government and Heritage (Ireland)",
        std="TGD M (2022)", jur="IE",
        url="https://assets.gov.ie/static/documents/technical-guidance-document-m-access-and-use-2022.pdf",
        note="Primary text read 2026-10-29 via pdftotext (clauses 1.1.3.4, 2.1.3.4, Table 2). Current edition per gov.ie listing; legal in-force date not separately confirmed.",
    ),
    dict(
        ref="REF-00751", last=None, display="Building and Construction Authority (Singapore)",
        year=2025,
        title="Code on Accessibility in the Built Environment 2025 (v1.1) - changes in level and ramps (4.5-4.6)",
        publisher="Building and Construction Authority (Singapore)",
        std="Code on Accessibility in the Built Environment 2025 v1.1", jur="SG",
        url="https://file.go.gov.sg/bca-coa2025.pdf",
        note="Primary text read 2026-10-29 via pdftotext (Tables 4 and 5, clauses 4.5-4.6). Version 1.1 revision dated 1 March 2026; in-force date not read.",
    ),
]


def main():
    out = ["-- Ramp-slope research batch, 2026-10-29. See audits/research-batch-ramp-slopes-2026-10-29/findings.md.", ""]

    cols = ("ref_id, source_type, author_count, author_count_is_complete, first_author_last, first_author_first, "
            "is_corporate_primary, author_display, pub_year, pub_title, lang_detected, translation_method, "
            "journal_name, tier, evidence_type, jurisdiction, metadata_quality, verification_status, grey_flag, "
            "notes, created_at, created_by_session, verification_attempt_count, scope")
    out.append(f"INSERT INTO evidence_sources ({cols}) VALUES")
    rows = []
    for ref, last, first, disp, yr, title, jour, pops, icfs, needs, note in LIT:
        notes = ABS_NOTE + (" " + note if note else "")
        rows.append("  (" + ", ".join(q(v) for v in (
            ref, "journal_article", 1, 0, last, first, 0, disp, yr, title, "en", "native_english",
            jour, 3, "clinical", "INT", "AUTHOR-TITLE-ONLY", "UNVERIFIED-1", 0,
            notes, NOW, SESSION, 0, "lower_control")) + ")")
    out.append(",\n".join(rows) + ";")
    out.append("")

    ccols = ("ref_id, source_type, author_count, author_count_is_complete, is_corporate_primary, author_display, "
             "pub_year, pub_title, lang_detected, translation_method, publisher, standard_number, url, url_accessed, "
             "tier, evidence_type, jurisdiction, metadata_quality, verification_status, verified_by_tool, "
             "last_verified_at, grey_flag, notes, created_at, created_by_session, verification_attempt_count, scope")
    out.append(f"INSERT INTO evidence_sources ({ccols}) VALUES")
    rows = []
    for r in CODE_ROWS:
        rows.append("  (" + ", ".join(q(v) for v in (
            r["ref"], "standard", 1, 1, 1, r["display"], r["year"], r["title"], "en", "native_english",
            r["publisher"], r["std"], r["url"], "2026-10-29", 6, "code", r["jur"], "COMPLETE-STATUTORY",
            "VERIFIED", "web-fetch+pdftotext", "2026-10-29T19:30:00Z", 0, r["note"], NOW, SESSION, 1,
            "national")) + ")")
    out.append(",\n".join(rows) + ";")
    out.append("")

    pop, icf, need = [], [], []
    for ref, _l, _f, _d, _y, _t, _j, pops, icfs, needs, _n in LIT:
        for code, conf, basis in pops:
            pop.append((ref, code, "subject", "manual-read", conf, "Abstract read: " + basis))
        for code, conf in icfs:
            icf.append((ref, code, "manual-read", conf, "Function studied, from abstract."))
        for code, conf in needs:
            need.append((ref, code, "manual-read", conf, "Access need addressed, from abstract (provisional vocabulary)."))

    def emit(table, cols, items):
        if not items:
            return
        out.append(f"INSERT INTO {table} ({cols}, review_status, created_at, created_by_session) VALUES")
        out.append(",\n".join("  (" + ", ".join(q(v) for v in it) + f", 'UNREVIEWED', {q(NOW)}, {q(SESSION)})" for it in items) + ";")
        out.append("")

    emit("source_population_tags", "ref_id, population_code, role, method, confidence, basis", pop)
    emit("source_icf_tags", "ref_id, icf_code, method, confidence, basis", icf)
    emit("source_need_tags", "ref_id, need_code, method, confidence, basis", need)

    print("\n".join(out))
    import sys
    print(f"[stats] sources={len(LIT) + len(CODE_ROWS)} pop_tags={len(pop)} icf_tags={len(icf)} need_tags={len(need)}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
