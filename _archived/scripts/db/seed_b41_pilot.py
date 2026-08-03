#!/usr/bin/env python3
"""
scripts/db/seed_b41_pilot.py — Seed B4.1 pilot data.

Seeds G-04 (Bathroom), R-BA (Bathroom room), and MOB population
with full relational data for the pilot track.

Usage:
    python3 scripts/db/seed_b41_pilot.py
"""

import json
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = REPO_ROOT / "data" / "db" / "guidebook.db"


def seed(conn):
    """Seed B4.1 pilot data."""

    # --- 1. Additional populations ---
    new_pops = [
        ("PAIN", "Chronic Pain and Fibromyalgia", "Persistent pain affecting grip, reach, endurance, and posture tolerance. Functional range from mild intermittent pain to constant severe pain requiring pacing strategies.", "PARTIAL", None, "MODERATE"),
        ("OFS", "Orthostatic and Fatigue Spectrum", "Conditions including ME/CFS, POTS, MCAS causing exercise intolerance, orthostatic intolerance, and cognitive fatigue. Requires rest access and reduced exertion environments.", "PARTIAL", "Co-1 gap: limited built environment research specific to OFS", "LOW"),
        ("NEU", "Neurological and Acquired Brain Injury", "Acquired neurological conditions (stroke, TBI, MS, Parkinson's) affecting motor control, balance, cognition, and sensory processing. Functional range highly variable.", "COMPLETE", None, "MODERATE"),
        ("NDV", "Neurodivergence", "Autism, ADHD, sensory processing differences, dyspraxia. Sensory environment (acoustic, lighting, texture) significantly affects function. Four sensory profiles per Dunn model.", "COMPLETE", None, "MODERATE"),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO population (code, label, functional_profile, co1_status, co1_gap_note, evidence_confidence) VALUES (?, ?, ?, ?, ?, ?)",
        new_pops,
    )

    # --- 2. G-04 Specification ---
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
            'SPEC-G04-001', 'G-04',
            'Accessible Bathroom (Wet Room Configuration — Zero Threshold)',
            'Shower area configuration and threshold',
            'SPECIFICATION', 'population_based',
            'CONDITIONAL_POPULATION', 3,
            'Zero threshold (≤3 mm); floor slope ≤1:80 to drain',
            '{"shower_area_min": "900×900 mm", "shower_area_preferred": "1200×900 mm", "slip_resistance_ptv": 36, "unit": "mm"}',
            'OT assessment resolves bathroom layout, grab bar positions, and equipment selection based on transfer type (standing pivot, seated, lateral, hoist)',
            'Can someone who uses a shower wheelchair roll from the bedroom into the shower without encountering a lip, ledge, or change of level?',
            'Wet room configuration eliminates the shower threshold — the single most common fall hazard in residential bathrooms for mobility, neurological, and pain populations.',
            'Tier 3 — BS 8300; DIN 18040-2; AS 1428.1; Koontz et al. (transfer biomechanics)',
            'A shower tray threshold of even 15 mm is an absolute barrier to a shower wheelchair user and a significant fall hazard for anyone with reduced balance, lower limb weakness, or pain-limited stepping. The wet room eliminates this barrier entirely: continuous floor from bathroom to shower, with integrated drainage fall. For dementia users, the absence of a visible threshold reduces spatial confusion and step-refusal behaviour. For pain and fatigue populations, the zero-threshold allows shower access without the exertion of stepping over a barrier that can trigger symptom flares.',
            'Shower area: wet room configuration with zero threshold (≤3 mm). Continuous floor from bathroom to shower. Floor slope ≤1:80 to drain. Linear drain at wall or tiled trench. Drain within 1200 mm of all shower area points. Shower clear area ≥900×900 mm; ≥1200×900 mm preferred. Slip resistance PTV ≥36 wet throughout shower area.',
            1, 'Wet room floor is a DAR priority: the drainage fall and waterproof tanking must be built into the structural floor. Retrofit requires full bathroom strip-out and floor reconstruction.',
            1,
            'STRUCTURAL', 'EHP Framework (create strategy) + Biomechanical FOR (transfer mechanics, fall prevention)',
            'automated',
            '["GRAB-BAR-DIA"]',
            'accessible-bathroom-and-grab-bar',
            'active'
        )
    """)

    # --- 3. G-04 populations ---
    g04_pops = [
        ("SPEC-G04-001", "MOB", "primary"),
        ("SPEC-G04-001", "DEM", "secondary"),
        ("SPEC-G04-001", "PAIN", "secondary"),
        ("SPEC-G04-001", "OFS", "secondary"),
        ("SPEC-G04-001", "NEU", "secondary"),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO specification_population (spec_id, population_code, role) VALUES (?, ?, ?)",
        g04_pops,
    )

    # --- 4. G-04 measurements ---
    g04_meas = [
        ("SPEC-G04-001", "universal", None, None, None, None, 3, "mm", "≤3 mm threshold", "Zero threshold specification"),
        ("SPEC-G04-001", "population_based", "MOB", 900, 1200, None, None, "mm", "900–1200 mm shower clear width", "Wheelchair shower: 1200×900 preferred"),
        ("SPEC-G04-001", "population_based", "ALL", None, None, None, 36, "PTV", "PTV ≥36 wet", "Slip resistance floor specification"),
        ("SPEC-G04-001", "person_specific", None, None, None, None, None, "mm", "OT assessment", "Layout, grab bars, and equipment per transfer type"),
    ]
    conn.executemany(
        "INSERT INTO measurement (spec_id, design_mode, population_code, value_min, value_max, value_median, value_fixed, unit, unit_display, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        g04_meas,
    )

    # --- 5. G-04 jurisdictional values ---
    g04_jv = [
        ("SPEC-G04-001", "US", "ADA 2010", "§604", "≤13 mm threshold", 13, "mm", None),
        ("SPEC-G04-001", "UK", "BS 8300-2:2018", "§18", "Level access (Doc M)", 0, "mm", "Guidebook aligns"),
        ("SPEC-G04-001", "AU", "AS 1428.1:2021", "§15", "Zero threshold", 0, "mm", "Matches guidebook"),
        ("SPEC-G04-001", "DE", "DIN 18040-1", "§4.3.6", "Zero threshold", 0, "mm", "Matches guidebook"),
        ("SPEC-G04-001", "ISO", "ISO 21542:2021", "§20", "Level access", 0, "mm", None),
    ]
    conn.executemany(
        "INSERT INTO jurisdictional_value (spec_id, jurisdiction, standard_name, clause_ref, value_text, value_numeric, unit, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        g04_jv,
    )

    # --- 6. G-04 performance criteria ---
    g04_criteria = [
        ("SPEC-G04-001", "Slip resistance PTV ≥36 wet throughout shower area", "Pendulum test (BS 7976-2)", "PTV ≥36"),
        ("SPEC-G04-001", "Zero threshold: no step, tray, or lip >3 mm", "Measurement", "≤3 mm"),
        ("SPEC-G04-001", "Drain within 1200 mm of all shower area points", "Measurement", "≤1200 mm"),
    ]
    conn.executemany(
        "INSERT INTO performance_criterion (spec_id, description, test_method, pass_threshold) VALUES (?, ?, ?, ?)",
        g04_criteria,
    )

    # --- 7. G-04 connections ---
    g04_conns = [
        ("CON-G04-G03", "SPEC-G04-001", None, "G-03", "cross-reference", "Grab bar positions — grab bar placement is integral to bathroom safety"),
        ("CON-G04-E07", "SPEC-G04-001", None, "E-07", "cross-reference", "Slip resistance — floor finish specification"),
        ("CON-G04-F07", "SPEC-G04-001", None, "F-07", "cross-reference", "Heated bathroom floor — Japan heat shock prevention"),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO connection_endpoint (connection_id, spec_id, target_spec_id, target_item_code, connection_type, description) VALUES (?, ?, ?, ?, ?, ?)",
        g04_conns,
    )

    # --- 8. Room: R-BA (Bathroom) ---
    conn.execute("""
        INSERT OR REPLACE INTO room (
            room_id, room_label, building_type, part_source, section,
            criticality_note, evidence_density, status
        ) VALUES (
            'R-BA', 'Bathroom', 'residential', 6, '§6.7',
            'Highest fall-risk space in residential buildings. Wet surfaces, transfers, and confined space create compounding hazards. Most bathroom falls occur during transfers (toilet, shower, bath).',
            '■ Rich',
            'active'
        )
    """)

    # R-BA item matrix
    ba_items = [
        ("R-BA", "G-03", "SD", "Floor plan; elevation"),
        ("R-BA", "G-04", "SD", "Floor plan; section"),
        ("R-BA", "E-07", "DD", "Floor plan (finish schedule)"),
        ("R-BA", "H-01", "DD", "Elevation"),
        ("R-BA", "F-07", "DD", "Floor plan"),
        ("R-BA", "B-01", "DD", "Reflected ceiling plan"),
        ("R-BA", "K-01", "CD", "Elevation"),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO room_item (room_id, item_code, design_stage, must_appear_on) VALUES (?, ?, ?, ?)",
        ba_items,
    )

    # R-BA DAR provisions
    ba_dar = [
        ("R-BA", "Structural blocking in walls at all grab bar positions (bilateral + vertical)", "CD", "Wall backing plan"),
        ("R-BA", "Drainage fall in structural floor for future wet room conversion", "CD", "Structural floor plan"),
        ("R-BA", "Electrical conduit for future ceiling hoist track", "CD", "Reflected ceiling plan"),
        ("R-BA", "Door frame sized for 900 mm clear opening (future automatic door)", "SD", "Floor plan"),
    ]
    conn.executemany(
        "INSERT INTO room_dar_provision (room_id, description, construction_stage, drawing_reference) VALUES (?, ?, ?, ?)",
        ba_dar,
    )

    # R-BA conflicts
    ba_conflicts = [
        ("R-BA", "Grab bar diameter: MOB prefers 32 mm; PAIN/OFS prefers 35 mm (reduced grip force)", "GRAB-BAR-DIA: Mode P median 33 mm; Mode S OT resolves", "GRAB-BAR-DIA"),
    ]
    conn.executemany(
        "INSERT INTO room_conflict (room_id, description, resolution, conflict_domain) VALUES (?, ?, ?, ?)",
        ba_conflicts,
    )

    # R-BA population applicability
    ba_pops = [
        ("R-BA", "G-03", "MOB", "primary"),
        ("R-BA", "G-03", "PAIN", "primary"),
        ("R-BA", "G-04", "MOB", "primary"),
        ("R-BA", "G-04", "DEM", "secondary"),
        ("R-BA", "E-07", "MOB", "primary"),
        ("R-BA", "E-07", "DEM", "primary"),
        ("R-BA", "H-01", "MOB", "primary"),
        ("R-BA", "H-01", "NDV", "secondary"),
        ("R-BA", "F-07", "DEM", "primary"),
        ("R-BA", "B-01", "VIS", "primary"),
        ("R-BA", "B-01", "DEM", "secondary"),
        ("R-BA", "K-01", "DEAF", "primary"),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO room_item_population (room_id, item_code, population_code, applicability) VALUES (?, ?, ?, ?)",
        ba_pops,
    )

    conn.commit()

    # --- Verify ---
    print("=== B4.1 Pilot Seed Report ===")
    for table in ["population", "specification", "measurement", "jurisdictional_value",
                   "room", "room_item", "room_dar_provision", "room_conflict", "room_item_population"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")


def main():
    conn = sqlite3.connect(str(DB_PATH))
    seed(conn)
    conn.close()
    print("\nB4.1 pilot data seeded.")


if __name__ == "__main__":
    main()
