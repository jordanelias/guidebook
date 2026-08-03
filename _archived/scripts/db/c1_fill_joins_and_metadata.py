#!/usr/bin/env python3
"""
C1 migration consolidation: fills join tables, performance criteria, 
conflict domains, summaries, BPC metadata, slugs, and connections.

Run after migrate_all.py and enrich_all_c_stage.py.
Idempotent (INSERT OR REPLACE / INSERT OR IGNORE).

Usage:
    cd /path/to/guidebook
    python3 scripts/db/c1_fill_joins_and_metadata.py
"""
import sqlite3, json, os, re, glob, yaml
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
WEB_DB = REPO / "data" / "db" / "guidebook.db"
TRACK_DB = REPO / "data" / "guidebook.db"
SESSION = "c1-migration-script"


def fill_website_db():
    db = sqlite3.connect(str(WEB_DB))
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')

    # 1. Summaries from why_md first sentence
    missing = db.execute(
        "SELECT spec_id, why_md FROM specification WHERE (summary IS NULL OR summary='') AND why_md IS NOT NULL"
    ).fetchall()
    for sid, why in missing:
        first = why.split('.')[0].strip() + '.' if '.' in why else why[:150]
        if len(first) > 20:
            db.execute("UPDATE specification SET summary=? WHERE spec_id=?", (first, sid))
    db.commit()

    # 2. Question headings from YAML
    qh_path = REPO / "data" / "question-headings.yaml"
    if qh_path.exists():
        with open(qh_path) as f:
            qh = yaml.safe_load(f)
        for ic, entry in qh.items():
            h = entry.get('question_heading')
            if h:
                db.execute(
                    "UPDATE specification SET question_heading=? WHERE item_code=? AND (question_heading IS NULL OR question_heading='')",
                    (h, ic))
        db.commit()

    # 3. Doctrine-specification joins
    docs = db.execute("SELECT doctrine_id, doctrine_group, title FROM doctrine").fetchall()
    items = db.execute("SELECT DISTINCT item_code, ot_evidence_basis FROM specification").fetchall()
    all_ic = [ic for ic, _ in items]
    fw_map = {
        'DOC-0008': ['biomechanical'], 'DOC-0009': ['sensory', 'dunn'],
        'DOC-0010': ['ecology', 'ehp'], 'DOC-0011': ['compensatory'],
        'DOC-0012': ['cognitive', 'allen'], 'DOC-0013': ['peop'],
        'DOC-0014': ['affordance'], 'DOC-0015': ['competence-press'],
        'DOC-0016': ['attention restoration', 'stress recovery'],
    }
    for did, dg, dt in docs:
        if dg in ('core', 'evidence', 'ethics'):
            for ic in all_ic:
                db.execute("INSERT OR IGNORE INTO doctrine_specification VALUES (?,?)", (did, ic))
        elif did in fw_map:
            for ic, ot in items:
                if ot and any(kw in ot.lower() for kw in fw_map[did]):
                    db.execute("INSERT OR IGNORE INTO doctrine_specification VALUES (?,?)", (did, ic))
    db.commit()

    # 4. Specialist-specification joins
    sp_pops = {}
    for r in db.execute("SELECT specialist_id, population_code FROM specialist_population"):
        sp_pops.setdefault(r[0], set()).add(r[1])
    spec_pops = {}
    for r in db.execute("SELECT s.item_code, spp.population_code FROM specification s JOIN specification_population spp ON s.spec_id=spp.spec_id"):
        spec_pops.setdefault(r[0], set()).add(r[1])
    for sp_id, sp_set in sp_pops.items():
        for ic, ic_set in spec_pops.items():
            if sp_set & ic_set:
                db.execute("INSERT OR IGNORE INTO specialist_specification VALUES (?,?)", (sp_id, ic))
    db.commit()

    # 5. Specialist stage scope
    stages = [('BRIEF','brief'),('CONCEPT','concept'),('DD','design development'),
              ('TENDER','tender'),('CONSTRUCTION','construction'),('HANDOVER','handover'),
              ('POST_OCC','post-occupancy')]
    for sp_id, role in db.execute("SELECT specialist_id, role FROM specialist"):
        for stage, text in stages:
            db.execute("INSERT OR IGNORE INTO specialist_stage_scope (specialist_id, stage, scope_text) VALUES (?,?,?)",
                       (sp_id, stage, f"{role}: {text}"))
    db.commit()

    # 6. Performance criteria from measurements
    seen = set()
    for row in db.execute("""
        SELECT m.spec_id, s.title, s.parameter, m.value_min, m.value_max, m.value_fixed, m.unit, m.notes
        FROM measurement m JOIN specification s ON m.spec_id=s.spec_id ORDER BY m.spec_id
    """):
        sid, title, param, vmin, vmax, vfixed, unit, notes = row
        u = unit or ''
        if vfixed: desc, thresh = f"{param or title}: {vfixed} {u}", f"{vfixed} {u}"
        elif vmin and vmax and vmin == vmax: desc, thresh = f"{param or title}: {vmin} {u}", f"{vmin} {u}"
        elif vmin and vmax: desc, thresh = f"{param or title}: {vmin}–{vmax} {u}", f"{vmin}–{vmax} {u}"
        elif vmin: desc, thresh = f"{param or title}: ≥{vmin} {u}", f"≥{vmin} {u}"
        elif vmax: desc, thresh = f"{param or title}: ≤{vmax} {u}", f"≤{vmax} {u}"
        else: continue
        key = (sid, desc.strip())
        if key in seen: continue
        seen.add(key)
        db.execute("INSERT OR IGNORE INTO performance_criterion (spec_id, description, test_method, pass_threshold, notes) VALUES (?,?,?,?,?)",
                   (sid, desc.strip(), f"Measure and verify", thresh.strip(), notes))
    db.commit()

    # Summary
    for t in ['doctrine_specification','specialist_specification','specialist_stage_scope','performance_criterion']:
        c = db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  website.{t}: {c}")
    db.close()


def fill_tracking_db():
    db = sqlite3.connect(str(TRACK_DB))
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')

    # BPC metadata from local files
    bpc_files = glob.glob(str(REPO / 'references/bpc/**/*.md'), recursive=True)
    bpc_files = [f for f in bpc_files if '/' in f.replace(str(REPO / 'references/bpc/'), '')]
    for fpath in bpc_files:
        slug = os.path.splitext(os.path.basename(fpath))[0]
        with open(fpath) as f:
            text = f.read()
        pop_m = re.search(r'for (MOB|VIS|DEAF|DEM|NDV|AUT|SCI|OFS|PAIN|NEU|UPL|ABI|MH|IntD)', text)
        pop = pop_m.group(1) if pop_m else 'MULTI'
        upd = re.search(r'\*\*Updated:\*\*\s*(\d{4}-\d{2}-\d{2})', text)
        opus = 1 if '[OPUS-SYNTHESIS]' in text else 0
        search = 1 if re.search(r'[Oo]riginal search:', text) else 0
        co1_m = re.search(r'Co-1\s+(\d+)/(\d+)', text)
        co1 = int(co1_m.group(1)) if co1_m else 0
        st_m = re.search(r'\*\*STATUS:\s*(PROVISIONAL|COMPLETE|DRAFT)', text)
        db.execute("""INSERT OR REPLACE INTO bpc_metadata
            (slug, population, last_updated, jurisdictions_searched, co1_pass_count, evidence_state,
             pico_complete, search_complete, bpc_complete, citation_mining_complete,
             created_at, created_by_session, updated_at, updated_by_session)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (slug, pop, upd.group(1) if upd else None, 0, co1,
             st_m.group(1) if st_m else None, 0, search, opus, 0,
             now, SESSION, now, SESSION))
    db.commit()
    print(f"  tracking.bpc_metadata: {db.execute('SELECT COUNT(*) FROM bpc_metadata').fetchone()[0]}")
    db.close()


if __name__ == '__main__':
    print("=== Website DB ===")
    fill_website_db()
    print("\n=== Tracking DB ===")
    fill_tracking_db()
    print("\nDone.")
