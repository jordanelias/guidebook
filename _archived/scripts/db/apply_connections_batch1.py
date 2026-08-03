#!/usr/bin/env python3
"""
scripts/db/apply_connections_batch1.py — Apply connection scout findings to database.

Applies measurement updates, new connection endpoints, and specification
enrichment from CON-0189 through CON-0239 (connection scout session 2026-05-04).

Priority: safety-critical and strong-convergence findings first.
"""

import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = REPO_ROOT / "data" / "db" / "guidebook.db"


def apply(conn):
    """Apply connection scout findings."""

    # === SAFETY-CRITICAL MEASUREMENT UPDATES ===

    # CON-0207: Rest seat height ≥480mm replaces 420mm (Tier 1 convergence)
    # Affects: E-10, I-03, G-02, G-07
    for item in ["E-10", "I-03", "G-02", "G-07"]:
        spec_id = conn.execute(
            "SELECT spec_id FROM specification WHERE item_code=? LIMIT 1", (item,)
        ).fetchone()
        if spec_id:
            conn.execute("""
                INSERT OR REPLACE INTO measurement 
                (spec_id, design_mode, population_code, value_min, value_max, unit, unit_display, notes)
                VALUES (?, 'universal', NULL, 480, NULL, 'mm', '≥480 mm seat height',
                'CON-0207: Triple convergence OFS (Roxburgh 2024 Tier 1) + MOB/NEU (STS biomechanics) + DEM (STS difficulty). Replaces 420 mm.')
            """, (spec_id[0],))

    # CON-0237: Corridor ≥1200mm metabolic normalisation (Koontz 2012)
    spec_a02 = conn.execute(
        "SELECT spec_id FROM specification WHERE item_code='A-02' LIMIT 1"
    ).fetchone()
    if spec_a02:
        conn.execute("""
            INSERT OR REPLACE INTO measurement
            (spec_id, design_mode, population_code, value_min, value_max, unit, unit_display, notes)
            VALUES (?, 'population_based', 'MOB', 1200, NULL, 'mm', '≥1200 mm primary circulation',
            'CON-0237: Koontz 2012 — below 900 mm metabolic cost increases 30-45%%. At 1200 mm normalises. Primary wheelchair routes must be ≥1200 mm for metabolic efficiency, not just access.')
        """, (spec_a02[0],))

    # CON-0210: Bathroom power WC + OFS requires ≥2200×2500mm
    spec_g04 = conn.execute(
        "SELECT spec_id FROM specification WHERE item_code='G-04' LIMIT 1"
    ).fetchone()
    if spec_g04:
        conn.execute("""
            INSERT OR REPLACE INTO measurement
            (spec_id, design_mode, population_code, value_min, value_max, unit, unit_display, notes)
            VALUES (?, 'population_based', 'MOB', 2500, NULL, 'mm', '≥2500 mm (power WC + OFS)',
            'CON-0210: Power WC turning (ø1800) + bilateral grab bars + OFS staged rising (≥500 mm forward) exceeds 2200 mm. Requires ≥2200×2500 mm.')
        """, (spec_g04[0],))

    # === CONNECTION ENDPOINTS ===
    # Resolve spec_ids for target items
    def get_spec(item_code):
        r = conn.execute("SELECT spec_id FROM specification WHERE item_code=? LIMIT 1", (item_code,)).fetchone()
        return r[0] if r else f"STUB-{item_code}"

    con_endpoints = [
        # (con_id, source_item, target_item, conn_type, desc)
        ("CON-0216", "G-04", "G-03", "cross-reference",
         "SAFETY-CRITICAL: Continuous horizontal grab rail 850-900 mm AFF linking WC → basin → door."),
        ("CON-0200", "E-07", "A-09", "conflict-domain",
         "FLOOR-SPECIFICATION-SYSTEM: 13th conflict domain. Zoned resolution required."),
        ("CON-0213", "G-09", "H-05", "cross-reference",
         "Emergency call multi-position reach envelope: 6 positions."),
        ("CON-0217", "A-16", "B-10", "cross-reference",
         "Sequenced multi-modal alarm replacing simultaneous."),
        ("CON-0198", "H-01", "H-01", "cross-reference",
         "Induction-only: triple convergence MS+VIS+DEM. Universal Mode candidate."),
        ("CON-0206", "D-06", "D-08", "cross-reference",
         "Dual-height signage: DEM ≤1220 mm + VIS 1400-1600 mm."),
        ("CON-0202", "H-02", "H-02", "cross-reference",
         "Control hierarchy: Voice→Switch→Rocker→Lever→Touchscreen LAST."),
        ("CON-0221", "F-01", "F-01", "cross-reference",
         "Sensory gradient is TOPOLOGY not linear."),
        ("CON-0231", "D-02", "D-02", "cross-reference",
         "Wayfinding format hierarchy: landmark→sequential→map LAST."),
        ("CON-0235", "D-02", "D-08", "cross-reference",
         "Layout > signage UNIVERSAL for all wayfinding-impaired populations."),
        ("CON-0223", "C-04", "C-03", "cross-reference",
         "Floor contrast partitioning: floor-floor ≤10 LRV; floor-wall ≥30 LRV."),
        ("CON-0222", "A-16", "A-16", "cross-reference",
         "A-16 within 20 m of accessible WC."),
        ("CON-0224", "F-07", "F-07", "cross-reference",
         "OFS ≤21°C vs DEM 24.9°C. Ambient 18-20°C + local warmth."),
        ("CON-0233", "K-05", "K-05", "cross-reference",
         "SCI thermal perception absent. Objective monitoring required."),
        ("CON-0229", "A-02", "A-07", "cross-reference",
         "Sawatzky: wheelchair injury prevention, not just access."),
        ("CON-0228", "G-03", "G-03", "cross-reference",
         "OT delivery prerequisite: Clemson Cochrane 38% vs non-significant."),
    ]

    for con_id, src_item, tgt_item, conn_type, desc in con_endpoints:
        src_spec = get_spec(src_item)
        conn.execute("""
            INSERT OR REPLACE INTO connection_endpoint
            (connection_id, spec_id, target_spec_id, target_item_code, connection_type, description)
            VALUES (?, ?, NULL, ?, ?, ?)
        """, (con_id, src_spec, tgt_item, conn_type, desc))

    # === NEW CONFLICT DOMAIN ===
    conn.execute("""
        INSERT OR REPLACE INTO conflict
        (conflict_id, conflict_label, domain, population_a, population_b,
         governing_principle, resolution_status, resolution_description,
         specifications_involved, notes)
        VALUES (
            'FLOOR-SPEC-SYS',
            'Floor Specification System',
            'FLOOR-SPECIFICATION-SYSTEM',
            'NEU/spasticity + DEAF',
            'PAIN',
            'Harm-asymmetry: spasticity fall risk (involuntary, destabilizing) > pain exacerbation (reversible)',
            'resolved',
            'Zoned resolution: primary path firm/non-compliant/PTV ≥36/plain; TWSI lane within path; cushioned mat at rest points ONLY; acoustic via ceiling+wall not floor.',
            'A-09, E-07, C-04, E-08',
            'CON-0200: 13th conflict domain. Corridor floor carries 9+ simultaneous specifications.'
        )
    """)

    conn.commit()

    # === Verify ===
    print("=== Connection Scout Application Report ===")
    meas = conn.execute("SELECT COUNT(*) FROM measurement").fetchone()[0]
    ce = conn.execute("SELECT COUNT(*) FROM connection_endpoint").fetchone()[0]
    conf = conn.execute("SELECT COUNT(*) FROM conflict").fetchone()[0]
    print(f"  measurements: {meas}")
    print(f"  connection_endpoints: {ce}")
    print(f"  conflicts: {conf}")

    # Items with updated measurements
    updated = conn.execute("""
        SELECT DISTINCT s.item_code FROM specification s
        JOIN measurement m ON s.spec_id = m.spec_id
        WHERE m.notes LIKE '%CON-%'
    """).fetchall()
    print(f"  items with CON- measurements: {', '.join(r[0] for r in updated)}")


def main():
    conn = sqlite3.connect(str(DB_PATH))
    apply(conn)
    conn.close()
    print("\nConnection scout findings applied.")


if __name__ == "__main__":
    main()
