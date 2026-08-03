#!/usr/bin/env python3
"""
scripts/db/seed_e08_pilot.py — Seed E-08 Corridor Clear Width pilot data.

Populates all relevant tables for the E-08 specification, demonstrating
the complete pipeline from SQLite atoms to rendered page.

Usage:
    python3 scripts/db/seed_e08_pilot.py
"""

import json
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = REPO_ROOT / "data" / "db" / "guidebook.db"


def seed(conn: sqlite3.Connection):
    """Seed E-08 pilot data."""

    # --- 1. Populations ---
    populations = [
        ("MOB", "Mobility — Wheelchair Users", "Uses manual or powered wheelchair for primary mobility. Functional capacity ranges from independent community mobility to requiring full-time attendant assistance.", "COMPLETE", None, "HIGH"),
        ("VIS", "Vision — Blind and Low Vision", "Navigates using cane, guide dog, or residual vision. Functional range from total blindness to moderate low vision with contrast sensitivity loss.", "COMPLETE", None, "HIGH"),
        ("DEM", "Dementia", "Cognitive impairment affecting wayfinding, spatial orientation, and environmental interpretation. Allen CDM levels 3-5 for residential; levels 4-5 for community.", "COMPLETE", None, "MODERATE"),
        ("DEAF", "Deaf and Hard of Hearing", "Communicates via sign language and/or uses hearing aids/cochlear implants. DeafSpace principles apply to spatial layout, lighting, and sightlines.", "COMPLETE", None, "HIGH"),
        ("DBL", "Deafblind", "Combined hearing and vision loss requiring tactile communication and intervenor support. Requires companion space in all circulation.", "PARTIAL", "Co-1 gap: no DBO-specific built environment research found", "LOW"),
        ("ALL", "Universal (All Populations)", "Population-agnostic provisions that apply regardless of functional capacity.", None, None, None),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO population (code, label, functional_profile, co1_status, co1_gap_note, evidence_confidence) VALUES (?, ?, ?, ?, ?, ?)",
        populations,
    )

    # --- 2. Specification ---
    conn.execute("""
        INSERT OR REPLACE INTO specification (
            spec_id, item_code, title, parameter, value_type, design_mode,
            recommendation_strength, evidence_tier,
            universal_value, population_value, person_specific_note,
            question_heading, summary, evidence_summary,
            why_md, schedule_md,
            dar_relevant, dar_note, structural_backing_required,
            retrofit_category, ot_evidence_basis, curation_status,
            conflict_domains, bpc_source_slug, status
        ) VALUES (
            'SPEC-E08-001', 'E-08',
            'Corridor Clear Width (≥1200 mm Minimum on All Primary Routes)',
            'Clear width on primary accessible routes',
            'RANGE', 'population_based',
            'CONDITIONAL_POPULATION', 3,
            '≥1200 mm (code minimum exceeded)',
            '{"min": 1200, "max": 1800, "median": 1500, "unit": "mm"}',
            'OT assessment resolves position within range based on wheelchair type, companion requirement, and route frequency',
            'Can two power wheelchairs pass each other?',
            'Primary accessible routes require 1200 mm clear width minimum, exceeding the 1000 mm code minimum in most jurisdictions. Two-way routes require 1800 mm.',
            'Tier 3 — BS 8300; ADA; DIN 18040; Koontz 2010 PMID:20434614 (wheelchair propulsion biomechanics)',
            'Corridors narrower than 1200 mm force manual wheelchair users into compensatory shoulder movements that increase joint loading and reduce propulsion efficiency. For power wheelchair users, corridors below 1500 mm eliminate independent passing. For Deaf users communicating in sign language, corridors below 2440 mm prevent side-by-side signed conversation. The corridor width directly determines whether a person can move through a building independently or must wait, reverse, or be assisted.',
            'Corridor clear width: ≥1200 mm on all primary accessible routes. Where continuous 1200 mm not achievable: passing bay ≥1500×1500 mm at ≤10 m intervals. Two-way primary routes: ≥1800 mm. No furniture, equipment, or signage projecting into corridor clear width.',
            1, 'Corridor width is a DAR priority: widening an existing corridor requires structural intervention. Build to 1200 mm minimum (1500 mm preferred) at construction.',
            1,
            'STRUCTURAL', 'Biomechanical FOR — wheelchair propulsion biomechanics (Koontz 2010)',
            'automated',
            '["SPATIAL-OPEN"]',
            'accessible-circulation-geometry',
            'active'
        )
    """)

    # --- 3. Specification-Population joins ---
    spec_pops = [
        ("SPEC-E08-001", "MOB", "primary"),
        ("SPEC-E08-001", "VIS", "secondary"),
        ("SPEC-E08-001", "DEM", "secondary"),
        ("SPEC-E08-001", "DEAF", "secondary"),
        ("SPEC-E08-001", "DBL", "secondary"),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO specification_population (spec_id, population_code, role) VALUES (?, ?, ?)",
        spec_pops,
    )

    # --- 4. Measurements ---
    measurements = [
        ("SPEC-E08-001", "universal", None, 1200, None, None, 1200, "mm", "≥1200 mm", "Code minimum exceeded — most jurisdictions require 1000 mm"),
        ("SPEC-E08-001", "population_based", "MOB", 1200, 1800, 1500, None, "mm", "1200–1800 mm (median 1500 mm)", "Single passage 1200mm; two-way 1800mm"),
        ("SPEC-E08-001", "population_based", "DEAF", 1800, 2440, 2100, None, "mm", "1800–2440 mm (median 2100 mm)", "DeafSpace signed-conversation width"),
        ("SPEC-E08-001", "population_based", "DBL", 1500, 1800, 1650, None, "mm", "1500–1800 mm (median 1650 mm)", "Intervenor companion width"),
        ("SPEC-E08-001", "person_specific", None, None, None, None, None, "mm", "OT assessment", "Resolves within population range based on wheelchair dimensions"),
    ]
    conn.executemany(
        "INSERT INTO measurement (spec_id, design_mode, population_code, value_min, value_max, value_median, value_fixed, unit, unit_display, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        measurements,
    )

    # --- 5. Jurisdictional values ---
    jurisdictions = [
        ("SPEC-E08-001", "US", "ADA 2010", "§403", "915 mm", 915, "mm", "Narrowest minimum"),
        ("SPEC-E08-001", "UK", "BS 8300-2:2018", "§7", "1200 mm (1800 mm two-way)", 1200, "mm", "Guidebook aligns"),
        ("SPEC-E08-001", "DE", "DIN 18040-1", "§4.3", "1500 mm (1800 mm two-way)", 1500, "mm", "Widest minimum"),
        ("SPEC-E08-001", "AU", "AS 1428.1:2021", "§7", "1000 mm (1800 mm passing)", 1000, "mm", "Between US and UK"),
        ("SPEC-E08-001", "NO", "TEK17", "§12-6", "1500 mm", 1500, "mm", "Same as DE"),
        ("SPEC-E08-001", "ISO", "ISO 21542:2021", "—", "1200 mm (1800 mm passing)", 1200, "mm", "Matches UK/guidebook"),
    ]
    conn.executemany(
        "INSERT INTO jurisdictional_value (spec_id, jurisdiction, standard_name, clause_ref, value_text, value_numeric, unit, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        jurisdictions,
    )

    # --- 6. Performance criteria ---
    criteria = [
        ("SPEC-E08-001", "No furniture, equipment, or signage projecting into corridor clear width", "Visual inspection", "0 mm projection into clear width"),
        ("SPEC-E08-001", "Passing bay at ≤10 m intervals where continuous 1200 mm not achievable", "Measurement", "≥1500×1500 mm bay at ≤10 m"),
    ]
    conn.executemany(
        "INSERT INTO performance_criterion (spec_id, description, test_method, pass_threshold) VALUES (?, ?, ?, ?)",
        criteria,
    )

    # --- 7. Evidence sources ---
    sources = [
        ("ACG-02", "BSI", 2018, "BS 8300-2:2018 — Design of an accessible and inclusive built environment", None, None, "https://www.bsigroup.com/en-GB/standards/bs-8300/", 5, "UK"),
        ("ACG-03", "DIN", 2010, "DIN 18040-1:2010 — Barrierefreies Bauen Pt 1", None, None, "https://www.din.de/", 6, "DE"),
        ("ACG-06", "US Access Board", 2010, "2010 ADA Standards for Accessible Design §407", None, None, "https://www.ada.gov/", 6, "US"),
        ("ACG-07", "Standards Australia", 2021, "AS 1428.1:2021 — Design for access and mobility", None, None, "https://www.standards.org.au/", 6, "AU"),
        ("KOONTZ-2010", "Koontz AM et al.", 2010, "Wheelchair propulsion biomechanics in corridors of varying width", "J Rehabil Res Dev", "10.1682/JRRD.2009.07.0091", None, 3, "US"),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO evidence_source (ref_id, authors, year, title, journal, doi, url, evidence_tier, jurisdiction) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        sources,
    )

    # --- 8. Specification-source joins ---
    spec_sources = [
        ("SPEC-E08-001", "ACG-02", "supporting"),
        ("SPEC-E08-001", "ACG-03", "supporting"),
        ("SPEC-E08-001", "ACG-06", "supporting"),
        ("SPEC-E08-001", "ACG-07", "supporting"),
        ("SPEC-E08-001", "KOONTZ-2010", "primary"),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO specification_source (spec_id, ref_id, role) VALUES (?, ?, ?)",
        spec_sources,
    )

    # --- 9. Connection endpoints ---
    connections = [
        ("CON-E08-E01", "SPEC-E08-001", None, "E-01", "cross-reference", "Lift car width — same corridor width applies to lift lobby approach"),
        ("CON-E08-E10", "SPEC-E08-001", None, "E-10", "cross-reference", "Rest seating — seating alcoves must not project into corridor clear width"),
        ("CON-E08-E11", "SPEC-E08-001", None, "E-11", "cross-reference", "Door clear width — corridor doors must maintain clear width continuity"),
        ("CON-E08-D04", "SPEC-E08-001", None, "D-04", "cross-reference", "Landmarks at decision points — landmark placement must not project into clear width"),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO connection_endpoint (connection_id, spec_id, target_spec_id, target_item_code, connection_type, description) VALUES (?, ?, ?, ?, ?, ?)",
        connections,
    )

    conn.commit()

    # --- Verify ---
    tables = [
        "population", "specification", "specification_population",
        "measurement", "jurisdictional_value", "performance_criterion",
        "evidence_source", "specification_source", "connection_endpoint",
    ]
    print("=== E-08 Pilot Seed Report ===")
    for table in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")


def main():
    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}. Run init_db.py first.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    seed(conn)
    conn.close()
    print("\nE-08 pilot data seeded successfully.")


if __name__ == "__main__":
    main()
