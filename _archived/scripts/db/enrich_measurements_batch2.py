#!/usr/bin/env python3
"""Batch 2 measurement enrichment — remaining 43 items."""

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

    # === ACOUSTIC ===
    add("A-04", "universal", None, None, None, None, None, "", "Graduated zoning from arrival to occupancy",
        "CON-0221: Topology not linear. Calm spine + utility branches. See F-01.")
    add("A-08", "universal", None, None, None, None, 25, "NC", "NC-25 maximum in sensitive spaces",
        "HVAC noise control. BB93 + PAS 6463. Applies to A-16, hearing loop spaces, NDV-primary.")
    add("A-09", "universal", None, None, None, None, 36, "PTV", "PTV ≥36 wet",
        "CON-0200: FLOOR-SPECIFICATION-SYSTEM. Zoned resolution — primary path firm/non-compliant.")
    add("A-09", "population_based", "NEU", None, None, None, None, "", "FIRM non-compliant (spasticity)",
        "CON-0200: NEU/spasticity requires firm floor. Foam/soft triggers extensor spasm.")
    add("A-13", "universal", None, None, None, None, None, "dB", "No sound masking in NEU environments",
        "Sound masking contraindicated: NEU auditory processing sensitivity. Remove, do not add noise.")
    add("A-15", "universal", None, None, None, None, None, "", "Acoustic differentiation between spaces",
        "VIS navigation cue: acoustic contrast between adjacent spaces aids orientation.")

    # === LIGHTING ===
    add("B-02", "universal", None, 300, None, None, None, "lux", "≥300 lux diffuse for lip reading",
        "Shadow-free illumination. CCT ≥4000K for sign language visibility. DEAF BPC.")
    add("B-03", "universal", None, None, None, None, None, "Hz", "No fluorescent overhead lighting",
        "Eliminate stroboscopic flicker. NDV/NEU/epilepsy trigger. LED drivers ≥25 kHz PWM or DC.")
    add("B-05", "universal", None, 5, None, None, None, "m", "≥5 m gradual lighting transition",
        "Transition zones at all major illumination boundaries. NDV sensory load management.")
    add("B-07", "universal", None, None, None, None, None, "lux", "Indirect/cove lighting in sensitive spaces",
        "No direct downlight in NDV/MH spaces. Indirect reduces glare and visual stress.")
    add("B-08", "universal", None, None, None, None, 30, "GU", "≤30 gloss units (matte floor)",
        "Low-reflectance floor finish. Reduces glare for VIS, reduces visual noise for NDV.")
    add("B-09", "universal", None, None, None, None, None, "", "Maximise natural light",
        "Clerestory, light wells, rooflights. CON-0232: Al Khatib 2024 biophilic SR — daylight is single most replicated intervention.")
    add("B-11", "universal", None, None, None, None, 2700, "K", "≤2700K after 19:00",
        "Warm CCT evening. Circadian: reduce melanopic stimulation. CON-0214: independent of B-12 sensor.")

    # === VISUAL / COLOUR ===
    add("C-02", "universal", None, None, None, None, None, "", "Distinct warm colour per wing/zone",
        "Colour-coded wayfinding. DEM/IntD primary. Maximum 5-7 zones per building.")
    add("C-05", "universal", None, None, None, None, 10, "LRV", "≤10 LRV differential (DEM inverse)",
        "CON-0223: Adjacent floor materials ≤10 LRV. Prevents step-misperception. DSDC evidence.")

    # === WAYFINDING ===
    add("D-02", "universal", None, None, None, None, None, "", "Layout > signage (CON-0235)",
        "CON-0231/0235: Sequential wayfinding. Landmark-first, map-last. Universal for all wayfinding impairment.")
    add("D-03", "universal", None, None, None, None, None, "m", "Toilet visible from primary seating",
        "DEM: no navigation required. Marquardt 2011. CON-0018/0130. Glazed panel or direct sightline.")
    add("D-05", "universal", None, 6, None, None, None, "m²", "≥6 m² focus room/breakout alcove",
        "Enclosed low-stimulation. NDV/MH primary. CON-0238: branch off calm spine.")
    add("D-06", "universal", None, None, None, None, 1200, "mm", "Memory box at ≥1200 mm AFF",
        "DEM room identification. Personalisation aids wayfinding. CON-0208: DEM bedroom coordination.")
    add("D-07", "universal", None, None, None, None, None, "", "No blind corners — curved or mirrored",
        "VIS cane collision prevention. DEM spatial disorientation at hidden junctions.")
    add("D-09", "universal", None, None, None, None, None, "", "No rearrangement without user consent",
        "DEM/NEU: consistent layout is a cognitive accessibility provision. FDR-DEM-01.")
    add("D-10", "universal", None, None, None, None, None, "", "Glazed panels in internal partitions",
        "DEM: visible destinations. VIS: visual connection. DEAF: sign language sightline.")
    add("D-11", "universal", None, None, None, None, None, "m", "Loop path, secured perimeter, seating",
        "DEM safe garden. Dementia Australia 2022. Rest seating per CON-0190 intervals.")

    # === CIRCULATION ===
    add("E-02", "universal", None, 1100, 1400, None, None, "mm", "1100×1400 mm platform (min)",
        "Platform lift. BS 8300: 1100×1400 preferred. Power wheelchair: ≥1400×1600.")
    add("E-03", "universal", None, None, None, None, None, "", "≤1:20 gradient",
        "CON ramp. Waters 1985: above 1:12 → shoulder injury. Best practice 1:20. MS fatigue.")
    add("E-03", "population_based", "MOB", None, None, None, 50, "mm/m", "1:20 (50 mm/m) max gradient",
        "Sawatzky 2015: upper limb preservation. CON-0229.")
    add("E-04", "universal", None, 3600, None, None, None, "mm", "≥3600 mm bay width",
        "Accessible parking. Covered. Closest to entry. Transfer zone each side.")
    add("E-05", "universal", None, 3000, 2000, None, None, "mm", "≥3000×2000 mm canopy",
        "Weather protection at entry. Covered canopy minimum.")
    add("E-06", "universal", None, None, None, None, 0, "mm", "Zero step (0 mm threshold)",
        "Level entry. All accessible entrances. BS 8300, AS 1428.1, DIN 18040-1.")
    add("E-07", "universal", None, None, None, None, 36, "PTV", "PTV ≥36 wet",
        "Slip resistance throughout. BS 7976-2 pendulum test.")
    add("E-08", "universal", None, 1200, None, None, None, "mm", "≥1200 mm clear width primary routes",
        "CON-0237: Koontz metabolic normalisation at 1200 mm. 900 mm = 30-45% metabolic penalty.")
    add("E-09", "universal", None, None, None, None, None, "", "ISO 23599:2019 TWSI",
        "CON-0197: PD gait cues use FLAT bands; TWSI uses raised ≥4 mm profile. Differentiation required.")
    add("E-11", "universal", None, 900, None, None, None, "mm", "≥900 mm clear opening",
        "Automatic sliding doors. Sensor activation zone ≥1500 mm from door face.")
    add("E-12", "universal", None, 1800, None, None, None, "mm", "ø1800 mm turning at landing",
        "Entrance landing for power wheelchair. BS 8300 Annex G.")
    add("E-13", "universal", None, None, None, None, None, "", "Cognitive legibility at entrance",
        "CON-0218: arrival-as-system. Entrance must be identifiable without prior knowledge of building.")
    add("E-15", "universal", None, None, None, None, None, "m²", "Height-adjustable bench + overhead hoist",
        "Changing Places. BS 8300. Adult-sized bench + ceiling track hoist + peninsular WC.")

    # === ENVIRONMENT ===
    add("F-02", "universal", None, None, None, None, None, "", "Fragrance-free zones in sensitive areas",
        "NDV/MH/OFS chemical sensitivity. Scent-free cleaning products required.")
    add("F-04", "universal", None, None, None, None, 13, "MERV", "MERV 13+ filtration",
        "Air quality. Low-VOC specification. OFS/MCAS mast cell trigger avoidance.")
    add("F-06", "universal", None, None, None, None, None, "", "Whole-building fragrance-free policy",
        "Operational standard. Extends F-02 to all areas. Scented products prohibited.")
    add("F-08", "universal", None, None, None, None, None, "min", "HVAC response ≤15 min to setpoint",
        "Thermal transition speed. CON-0191: bathroom pre-heating for ≤5°C inter-room differential.")

    # === CONTROLS ===
    add("H-03", "universal", None, None, None, None, None, "", "Visual paging + real-time captioning",
        "DEAF/DBL assembly provision. Screen-based announcements + CART/AI captioning.")
    add("H-04", "universal", None, 1000, 1200, None, None, "mm", "1000-1200 mm AFF intercom height",
        "Accessible intercom with visual+tactile. Video door entry. CON-0233: SCI requires visual temp display.")

    # === CEILING HOIST ===
    add("I-04", "universal", None, None, None, None, 200, "kg", "≥200 kg SWL ceiling hoist",
        "Ceiling track provision. CON-0103: structural blocking at construction. DAR provision.")

    conn.executemany("""
        INSERT OR REPLACE INTO measurement
        (spec_id, design_mode, population_code, value_min, value_max, value_median, value_fixed, unit, unit_display, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, measurements)

    conn.commit()

    print(f"=== Batch 2 Measurement Enrichment ===")
    print(f"  Inserted: {len(measurements)} measurements")
    total = conn.execute("SELECT COUNT(*) FROM measurement").fetchone()[0]
    print(f"  Total measurements: {total}")
    items_with = conn.execute("""
        SELECT COUNT(DISTINCT s.item_code) FROM specification s
        JOIN measurement m ON s.spec_id = m.spec_id
    """).fetchone()[0]
    items_total = conn.execute("SELECT COUNT(DISTINCT item_code) FROM specification").fetchone()[0]
    print(f"  Items with measurements: {items_with}/{items_total}")

    # Show remaining gaps
    remaining = conn.execute("""
        SELECT s.item_code FROM specification s
        LEFT JOIN measurement m ON s.spec_id = m.spec_id
        GROUP BY s.item_code HAVING COUNT(m.measurement_id) = 0
        ORDER BY s.item_code
    """).fetchall()
    if remaining:
        print(f"  Remaining without: {', '.join(r[0] for r in remaining)}")
    else:
        print(f"  ALL ITEMS HAVE MEASUREMENTS")


def main():
    conn = sqlite3.connect(str(DB_PATH))
    enrich(conn)
    conn.close()


if __name__ == "__main__":
    main()
