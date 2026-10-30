#!/usr/bin/env python3
"""
scripts/db/build_ramp_batch_2_migration.py

Second SQL emitter for the 2026-10-29 ramp-slope batch: records two studies that
the E-03 page had been carrying outside the database (Sanford 1997, Rooney 2021).
Evidence is binary: if it is relied on, it is recorded. Same conventions as
build_ramp_batch_migration.py (abstract-level read, UNVERIFIED-1, UNREVIEWED tags).

    python -X utf8 scripts/db/build_ramp_batch_2_migration.py | \
      python scripts/emit_data_migration.py \
        --session session_2026-10-29-ramp-slopes-research-batch-2.md \
        --summary "record Sanford 1997 and Rooney 2021 as evidence_sources with tags"
"""
import sys

SESSION = "session_2026-10-29-ramp-slopes-research-batch-2"
NOW = "2026-10-29 21:00"


def q(v):
    if v is None:
        return "NULL"
    if isinstance(v, int):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


NOTE = ("Recorded 2026-10-29 from a search result and the E-03 staging data; abstract-level only, full text not read; "
        "DOI as stated in the staging data where present. Tier is provisional.")

# ref, last, first, display, year, title, journal, doi, source_type, evidence_type, tier, count, complete, extra note
SOURCES = [
    ("REF-00752", "Sanford", "J. A.", "Sanford JA, Story M, & Jones M", 1997,
     "An analysis of the effects of ramp slope on people with mobility impairments", "Assistive Technology",
     "10.1080/10400435.1997.10132293", "journal_article", "clinical", 3, 3, 1,
     "171 participants, slopes 1:8 to 1:20 over a 30 ft ramp; few manual wheelchair users could not ascend, even at 1:8."),
    ("REF-00753", "Rooney", "S.", "Rooney S et al.", 2021,
     "Oxygen cost of walking in people with multiple sclerosis and its association with fatigue", "International Journal of MS Care",
     None, "journal_article", "sr_meta", 2, 1, 0,
     "Meta-analysis of 9 studies; DOI not yet resolved."),
]
POP = [("REF-00752", "MOB", "high", "Participants were people with mobility impairments, including manual wheelchair users."),
       ("REF-00753", "MS", "high", "People with multiple sclerosis.")]
ICF = [("REF-00752", "d465", "high"), ("REF-00752", "d455", "medium"),
       ("REF-00753", "d450", "high"), ("REF-00753", "b455", "high"), ("REF-00753", "b4552", "medium")]
NEED = [("REF-00752", "AN-02", "medium"), ("REF-00753", "AN-02", "medium"), ("REF-00753", "AN-03", "medium")]


def main():
    out = ["-- Ramp-slope batch 2: record two studies relied on by the E-03 page.", ""]
    cols = ("ref_id, source_type, author_count, author_count_is_complete, first_author_last, first_author_first, "
            "is_corporate_primary, author_display, pub_year, pub_title, lang_detected, translation_method, "
            "journal_name, doi, tier, evidence_type, jurisdiction, metadata_quality, verification_status, grey_flag, "
            "notes, created_at, created_by_session, verification_attempt_count, scope")
    rows = []
    for ref, last, first, disp, yr, title, jour, doi, st, et, tier, n, comp, extra in SOURCES:
        mq = "AUTHOR-TITLE-ONLY" if not doi else "COMPLETE"
        rows.append("  (" + ", ".join(q(v) for v in (
            ref, st, n, comp, last, first, 0, disp, yr, title, "en", "native_english", jour, doi, tier, et, "INT",
            mq, "UNVERIFIED-1", 0, NOTE + " " + extra, NOW, SESSION, 0, "lower_control")) + ")")
    out.append(f"INSERT INTO evidence_sources ({cols}) VALUES\n" + ",\n".join(rows) + ";\n")

    def emit(table, cols, items, fmt):
        out.append(f"INSERT INTO {table} ({cols}, review_status, created_at, created_by_session) VALUES")
        out.append(",\n".join("  (" + ", ".join(q(v) for v in fmt(it)) + f", 'UNREVIEWED', {q(NOW)}, {q(SESSION)})" for it in items) + ";\n")

    emit("source_population_tags", "ref_id, population_code, role, method, confidence, basis", POP,
         lambda t: (t[0], t[1], "subject", "manual-read", t[2], "Abstract read: " + t[3]))
    emit("source_icf_tags", "ref_id, icf_code, method, confidence, basis", ICF,
         lambda t: (t[0], t[1], "manual-read", t[2], "Function studied, from abstract."))
    emit("source_need_tags", "ref_id, need_code, method, confidence, basis", NEED,
         lambda t: (t[0], t[1], "manual-read", t[2], "Access need addressed, from abstract (provisional vocabulary)."))
    print("\n".join(out))
    print(f"[stats] sources={len(SOURCES)} pop={len(POP)} icf={len(ICF)} need={len(NEED)}", file=sys.stderr)


if __name__ == "__main__":
    main()
