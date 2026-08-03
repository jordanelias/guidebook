#!/usr/bin/env python3
"""Enrich specifications with measurements from BPC/FDR data."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "db" / "guidebook.db"


def get_spec(conn, item_code):
    r = conn.execute("SELECT spec_id FROM specification WHERE item_code=? LIMIT 1", (item_code,)).fetchone()
    return r[0] if r else None


def enrich(conn):
    measurements = []

    def add(item, mode, pop, vmin, vmax, vmed, vfix, unit, disp, notes):
        sid = get_spec(conn, item)
        if sid:
            measurements.append((sid, mode, pop, vmin, vmax, vmed, vfix, unit, disp, notes))

    # === ACOUSTIC (A-03, A-05, A-06, A-07, A-14) ===
    add("A-03", "universal", None, 35, None, None, None, "STC", "STC ≥35", "Acoustic door at sensitive space boundaries. BS 8300, PAS 6463.")
    add("A-05", "universal", None, None, None, None, 0.25, "NRC", "NRC ≥0.25 (carpet)", "Carpet NRC contribution. Conflict: DEAF vibration needs hard floor. See CON-0200.")
    add("A-06", "universal", None, None, None, None, 0.70, "NRC", "NRC ≥0.70 (wall panels)", "Fabric wall panels at acoustic reflection points.")
    add("A-07", "universal", None, None, None, None, None, "mm", "No parallel hard surfaces within 4 m", "Flutter echo elimination. Splay ≥5° or absorptive treatment.")
    add("A-14", "universal", None, 50, None, None, None, "STC", "STC ≥50", "Double-leaf partition for sensitive adjacencies. CON-0211: varies by zone pairing.")

    # === ACOUSTIC HEARING LOOPS (A-10, A-11) ===
    add("A-10", "universal", None, None, None, None, None, "dB", "IEC 60118-4:2014", "Counter hearing loop. Field strength per IEC 60118-4.")
    add("A-11", "universal", None, None, None, None, None, "dB", "IEC 60118-4:2014", "Room perimeter loop. RT60 ≤0.4s in looped spaces.")

    # === LIGHTING (B-01, B-06, B-10, B-12) ===
    add("B-01", "universal", None, 150, 250, None, None, "melanopic EDI", "≥150-250 melanopic EDI daytime", "Circadian lighting. CIE S 026:2023. CON-0214: isolate from B-12 sensor circuit.")
    add("B-06", "universal", None, 0, 300, None, None, "lux", "0-300 lux continuous dimming", "Individual dimming control. CCT 2700-4000K adjustable.")
    add("B-10", "universal", None, None, None, None, 0.5, "Hz", "VAD 0.5 Hz synchronised", "CON-0217: sequenced multi-modal alarm. EN 54-23:2010. VAD sync prevents seizure.")
    add("B-12", "universal", None, None, None, None, 5, "lux", "≥5 lux at 300-400 mm AFF", "CON-0196/0214: sensor overnight lighting. 2700-3000K. Independent of B-01 circadian.")

    # === CONTRAST AND PATTERN (C-03, C-04) ===
    add("C-03", "universal", None, None, None, None, 10, "LRV", "≤10 LRV inter-zone differential", "CON-0223: DEM floor-to-floor ≤10 LRV. No patterned flooring. DSDC evidence.")
    add("C-04", "universal", None, 30, None, None, None, "LRV", "≥30 LRV at boundaries", "CON-0223: VIS floor-to-wall/fixture ≥30 LRV. BS 8300, AS 1428.1.")
    add("C-04", "population_based", "VIS", 50, None, None, None, "LRV", "≥50 LRV best practice", "Severe VIS needs ~75 LRV (65% Michelson). 50 LRV as intermediate target.")

    # === WAYFINDING (D-02, D-05, D-06, D-08) ===
    add("D-08", "population_based", "DEM", None, 1220, None, None, "mm", "DEM signage ≤1220 mm AFF", "CON-0206: DEM downward visual scan (Benbow 2013). Dual-height with VIS zone.")
    add("D-08", "population_based", "VIS", 1400, 1600, None, None, "mm", "VIS braille 1400-1600 mm AFF", "CON-0206: ISO 21542, BS 8300. Tactile zone above DEM zone.")

    # === THERMAL (F-07) ===
    add("F-07", "population_based", "MOB", 18, 22, None, None, "°C", "18-22°C (SCI/MS max)", "CON-0224: SCI poikilothermia + MS Uhthoff's. Ceiling 22°C (Griggs 2019).")
    add("F-07", "population_based", "DEM", 18, 26, None, 25, "°C", "18-26°C (DEM neutral ~24.9°C)", "CON-0224: DEM older adult neutral 24.9°C. Local warmth, not ambient increase.")

    # === BATHROOM (G-05, G-06, G-08, G-09) ===
    add("G-05", "universal", None, 650, 870, None, None, "mm", "650-870 mm AFF adjustable", "Adjustable-height work surface. MOB seated: 760 mm.")
    add("G-06", "universal", None, 760, 860, None, None, "mm", "760-860 mm AFF (accessible section)", "Reception counter accessible height section.")
    add("G-08", "universal", None, 380, 1220, None, None, "mm", "380-1220 mm AFF (reach range)", "Universal reach range for storage. NIOSH + OT energy conservation.")
    add("G-09", "universal", None, 400, 500, None, None, "mm", "400-500 mm AFF (floor-level pull)", "Bedroom emergency call. CON-0213: 6-position reach envelope. Also ≤500 mm from bed head.")

    # === CONTROLS (H-02, H-05) ===
    add("H-02", "universal", None, None, None, None, None, "", "Voice → Switch → Rocker → Lever → Touchscreen", "CON-0202: population-prioritised hierarchy. Voice primary for severe motor impairment.")
    add("H-05", "universal", None, 400, 500, None, None, "mm", "400-500 mm AFF (floor reach)", "CON-0213: multi-position emergency call. 6 positions from different body postures.")

    # === SENSORY QUIET ROOM (A-16) ===
    add("A-16", "universal", None, 8, None, None, None, "m²", "≥8 m² clear floor area", "PAS 6463:2022 §14.1. CON-0222: within 20 m of accessible WC.")

    # === SEATING INTERVAL ===
    add("E-10", "population_based", "DEM", None, None, None, 20, "m", "≤20 m (DEM governs)", "CON-0190: DEM interval governs in mixed-population settings.")
    add("E-10", "population_based", "OFS", None, None, None, 25, "m", "≤25 m (OFS/PAIN)", "CON-0190: Roxburgh 2024 Tier 1. OFS fatigue threshold.")
    add("E-10", "population_based", "MOB", None, None, None, 50, "m", "≤50 m (MOB)", "CON-0190: AS 1428.1. Manual propulsion endurance.")

    # === BUILDING APPROACH ===
    add("F-03", "universal", None, 3, None, None, None, "m", "≥3 m decompression zone", "Exit decompression from A-16. CON-0220: approach decompression 10 m also needed.")

    # Insert all
    conn.executemany("""
        INSERT OR REPLACE INTO measurement
        (spec_id, design_mode, population_code, value_min, value_max, value_median, value_fixed, unit, unit_display, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, measurements)

    conn.commit()

    print(f"=== Measurement Enrichment Report ===")
    print(f"  Inserted: {len(measurements)} measurements")
    total = conn.execute("SELECT COUNT(*) FROM measurement").fetchone()[0]
    print(f"  Total measurements: {total}")
    items_with = conn.execute("""
        SELECT COUNT(DISTINCT s.item_code) FROM specification s
        JOIN measurement m ON s.spec_id = m.spec_id
    """).fetchone()[0]
    items_total = conn.execute("SELECT COUNT(DISTINCT item_code) FROM specification").fetchone()[0]
    print(f"  Items with measurements: {items_with}/{items_total}")


def main():
    conn = sqlite3.connect(str(DB_PATH))
    enrich(conn)
    conn.close()


if __name__ == "__main__":
    main()
