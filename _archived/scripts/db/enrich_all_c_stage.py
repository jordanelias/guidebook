#!/usr/bin/env python3
"""
C-stage comprehensive enrichment:
1. C3: Prose fields (why_md, schedule_md, evidence_summary)
2. C7: specification_source joins
3. C5: Room DAR, conflicts, population mappings
4. Remaining connection endpoints
"""

import sqlite3, re
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "db" / "guidebook.db"


def get_spec(conn, item_code):
    r = conn.execute("SELECT spec_id FROM specification WHERE item_code=? LIMIT 1", (item_code,)).fetchone()
    return r[0] if r else None


def enrich_prose(conn):
    """C3: Fill empty prose fields using existing database content."""
    
    specs = conn.execute("""
        SELECT spec_id, item_code, title, summary, evidence_summary, why_md, schedule_md,
               evidence_tier, recommendation_strength, dar_relevant, dar_note,
               ot_evidence_basis, bpc_source_slug
        FROM specification
    """).fetchall()
    
    updated = 0
    for s in specs:
        spec_id, item, title, summary, ev_sum, why, sched, tier, rec, dar, dar_note, ot, bpc = s
        
        # Get populations for this spec
        pops = conn.execute(
            "SELECT population_code, role FROM specification_population WHERE spec_id=? ORDER BY role, population_code",
            (spec_id,)
        ).fetchall()
        primary = [p[0] for p in pops if p[1] == "primary"]
        secondary = [p[0] for p in pops if p[1] == "secondary"]
        
        # Get measurements
        meas = conn.execute(
            "SELECT design_mode, population_code, value_min, value_max, value_fixed, unit, unit_display, notes FROM measurement WHERE spec_id=?",
            (spec_id,)
        ).fetchall()
        
        # Get jurisdictional values
        jvs = conn.execute(
            "SELECT jurisdiction, standard_name, clause_ref, value_text FROM jurisdictional_value WHERE spec_id=? ORDER BY jurisdiction",
            (spec_id,)
        ).fetchall()
        
        changes = {}
        
        # --- why_md ---
        if not why or len(why) < 50:
            parts = []
            if summary:
                parts.append(summary)
            if primary:
                parts.append(f"Primary populations: {', '.join(primary)}.")
            if secondary:
                parts.append(f"Secondary populations: {', '.join(secondary)}.")
            if meas:
                meas_desc = []
                for m in meas:
                    if m[6]:  # unit_display
                        meas_desc.append(m[6])
                if meas_desc:
                    parts.append("Key specifications: " + "; ".join(meas_desc[:3]) + ".")
            if dar and dar_note:
                parts.append(f"DAR: {dar_note}")
            if ot:
                parts.append(f"OT basis: {ot}")
            if parts:
                changes["why_md"] = " ".join(parts)
        
        # --- schedule_md ---
        if not sched or len(sched) < 20:
            sched_parts = []
            if meas:
                for m in meas:
                    if m[6] and m[7]:  # unit_display + notes
                        sched_parts.append(f"{m[6]}: {m[7][:100]}")
            if jvs:
                jv_summary = "; ".join(f"{j[0]} ({j[1]}): {j[3]}" for j in jvs[:4])
                sched_parts.append(f"Jurisdictional values: {jv_summary}")
            if sched_parts:
                changes["schedule_md"] = " | ".join(sched_parts[:5])
        
        # --- evidence_summary ---
        if not ev_sum or len(ev_sum) < 20:
            ev_parts = []
            if tier:
                ev_parts.append(f"Evidence tier: {tier}")
            if rec:
                ev_parts.append(f"Recommendation: {rec}")
            if bpc:
                ev_parts.append(f"BPC source: {bpc}")
            if meas:
                for m in meas:
                    if m[7] and 'CON-' in str(m[7]):  # notes with connection references
                        ev_parts.append(m[7][:150])
            if ev_parts:
                changes["evidence_summary"] = ". ".join(ev_parts)
        
        # Apply changes
        if changes:
            sets = ", ".join(f"{k} = ?" for k in changes)
            vals = list(changes.values()) + [spec_id]
            conn.execute(f"UPDATE specification SET {sets} WHERE spec_id = ?", vals)
            updated += 1
    
    conn.commit()
    
    # Report
    empty_why = conn.execute("SELECT COUNT(*) FROM specification WHERE why_md IS NULL OR why_md = '' OR length(why_md) < 50").fetchone()[0]
    empty_sched = conn.execute("SELECT COUNT(*) FROM specification WHERE schedule_md IS NULL OR schedule_md = '' OR length(schedule_md) < 20").fetchone()[0]
    empty_ev = conn.execute("SELECT COUNT(*) FROM specification WHERE evidence_summary IS NULL OR evidence_summary = '' OR length(evidence_summary) < 20").fetchone()[0]
    print(f"  C3 Prose: {updated} specs updated. Remaining empty: why={empty_why}, sched={empty_sched}, ev={empty_ev}")


def enrich_spec_sources(conn):
    """C7: Link evidence_source records to specifications by keyword matching."""
    
    # Get all specs with their titles and BPC slugs
    specs = conn.execute("""
        SELECT spec_id, item_code, title, bpc_source_slug, why_md, evidence_summary
        FROM specification
    """).fetchall()
    
    # Get all evidence sources
    sources = conn.execute("""
        SELECT ref_id, authors, title, evidence_tier
        FROM evidence_source
    """).fetchall()
    
    # Build keyword index from source titles
    import re
    source_keywords = {}
    for src in sources:
        ref_id, authors, title, tier = src
        words = set(re.findall(r'\b[a-z]{4,}\b', (title or '').lower()))
        source_keywords[ref_id] = (words, authors or '', title or '', tier)
    
    # Topic keywords per item category
    category_keywords = {
        'A': {'acoustic', 'noise', 'sound', 'reverberation', 'hearing', 'loop', 'speech'},
        'B': {'light', 'lighting', 'circadian', 'visual', 'alarm', 'fire', 'sensor'},
        'C': {'contrast', 'colour', 'color', 'pattern', 'luminance'},
        'D': {'wayfinding', 'signage', 'navigation', 'spatial', 'orientation', 'cognitive'},
        'E': {'door', 'ramp', 'threshold', 'corridor', 'circulation', 'stair', 'entry', 'slip', 'parking', 'tactile'},
        'F': {'thermal', 'temperature', 'ventilation', 'fragrance', 'olfactory', 'sensory'},
        'G': {'grab', 'bathroom', 'shower', 'toilet', 'counter', 'storage', 'hoist', 'bedroom', 'reception'},
        'H': {'control', 'intercom', 'switch', 'emergency', 'call', 'captioning', 'paging'},
        'I': {'seating', 'rest', 'hoist', 'ceiling'},
        'K': {'acoustic', 'thermal', 'comfort'},
    }
    
    joins = []
    for spec in specs:
        spec_id, item, title, bpc_slug, why, ev_sum = spec
        category = item[0] if item else ''
        cat_kw = category_keywords.get(category, set())
        
        # Extract keywords from spec title
        spec_words = set(re.findall(r'\b[a-z]{4,}\b', (title or '').lower()))
        search_words = spec_words | cat_kw
        
        # Find matching sources (require ≥2 keyword overlap)
        matches = []
        for ref_id, (src_words, authors, src_title, tier) in source_keywords.items():
            overlap = search_words & src_words
            if len(overlap) >= 2:
                matches.append((ref_id, len(overlap)))
        
        # Take top 5 matches by overlap score
        matches.sort(key=lambda x: -x[1])
        for ref_id, score in matches[:5]:
            joins.append((spec_id, ref_id, "keyword_match"))
    
    if joins:
        conn.executemany(
            "INSERT OR REPLACE INTO specification_source (spec_id, ref_id, role) VALUES (?, ?, ?)",
            joins
        )
    conn.commit()
    
    total = conn.execute("SELECT COUNT(*) FROM specification_source").fetchone()[0]
    unique_specs = conn.execute("SELECT COUNT(DISTINCT spec_id) FROM specification_source").fetchone()[0]
    unique_sources = conn.execute("SELECT COUNT(DISTINCT ref_id) FROM specification_source").fetchone()[0]
    print(f"  C7 Sources: {len(joins)} joins. {unique_specs} specs linked to {unique_sources} sources. Total: {total}")


def enrich_rooms(conn):
    """C5: Room DAR provisions, conflicts, and population mappings."""
    
    # DAR provisions per room type
    dar_provisions = [
        # R-BA Bathroom
        ("R-BA", "Structural blocking in walls at all grab bar positions (bilateral + vertical)", "CD", "Wall backing plan"),
        ("R-BA", "Drainage fall in structural floor for future wet room conversion", "CD", "Structural floor plan"),
        ("R-BA", "Electrical conduit for future ceiling hoist track", "CD", "Reflected ceiling plan"),
        ("R-BA", "Door frame sized for 900 mm clear opening (future automatic door)", "SD", "Floor plan"),
        ("R-BA", "Pre-heating system capacity for ≤5°C inter-room differential (CON-0191)", "DD", "Mechanical plan"),
        
        # R-BED Bedroom
        ("R-BED", "Structural blocking for bilateral grab bars at bed head", "CD", "Wall backing plan"),
        ("R-BED", "Ceiling hoist track structural mount points (≥200 kg)", "CD", "Reflected ceiling plan"),
        ("R-BED", "Conduit for future environmental control system", "CD", "Reflected ceiling plan"),
        ("R-BED", "Door frame 900 mm clear (future automatic)", "SD", "Floor plan"),
        ("R-BED", "Emergency call wiring to bed head position (CON-0213)", "CD", "Electrical plan"),
        
        # R-KIT Kitchen
        ("R-KIT", "Worktop height adjustment mechanism space (650-900 mm range)", "DD", "Section"),
        ("R-KIT", "Induction cooktop electrical supply (32A dedicated circuit)", "CD", "Electrical plan"),
        ("R-KIT", "Under-counter knee clearance (≥700 mm AFF clear)", "SD", "Section"),
        ("R-KIT", "Pull-out base unit runners (full extension, soft close)", "DD", "Elevation"),
        
        # R-LIV Living Room
        ("R-LIV", "Ceiling hoist track structural mount points", "CD", "Reflected ceiling plan"),
        ("R-LIV", "Environmental control conduit (lighting, thermal, acoustic)", "CD", "Reflected ceiling plan"),
        
        # R-ENT Entry
        ("R-ENT", "Automatic door operator power and conduit", "CD", "Floor plan; elevation"),
        ("R-ENT", "Level threshold detail (≤3 mm weather sealed)", "SD", "Section"),
        ("R-ENT", "Video intercom conduit and backing", "CD", "Elevation"),
        
        # R-HAL Hallway
        ("R-HAL", "Rest seating alcove recess (≥200 mm × ≥900 mm) at intervals (CON-0204)", "SD", "Floor plan"),
        ("R-HAL", "Overnight sensor lighting circuit independent of circadian (CON-0214)", "CD", "Reflected ceiling plan"),
        
        # R-LAU Laundry
        ("R-LAU", "Front-loader appliance plinth (raised 300-400 mm for seated access)", "DD", "Elevation"),
        ("R-LAU", "Anti-vibration floor treatment under appliances", "DD", "Floor plan"),
        
        # R-GAR Garage
        ("R-GAR", "Level access from vehicle transfer zone to dwelling entry", "SD", "Floor plan; section"),
        
        # R-STA Staircase
        ("R-STA", "Platform lift shaft space reservation", "SD", "Floor plan; section"),
        ("R-STA", "Continuous handrail structural fixings both sides", "CD", "Section"),
        
        # Non-residential
        # R-REC Reception
        ("R-REC", "Counter hearing loop infrastructure (conduit + power)", "CD", "Floor plan"),
        ("R-REC", "Accessible counter section (760-860 mm height zone)", "SD", "Elevation"),
        
        # R-COR Corridor
        ("R-COR", "Rest seating alcoves at ≤20 m intervals (CON-0190)", "SD", "Floor plan"),
        ("R-COR", "TWSI installation zone in floor finish (CON-0197)", "DD", "Floor plan"),
        ("R-COR", "Acoustic treatment mounting points (ceiling + walls)", "DD", "Reflected ceiling plan"),
        
        # R-MTG Meeting Room
        ("R-MTG", "Hearing loop infrastructure (perimeter + portable backup)", "CD", "Floor plan"),
        ("R-MTG", "Acoustic partition STC ≥50 (CON-0211)", "CD", "Wall section"),
        ("R-MTG", "Captioning display mounting and power", "DD", "Elevation"),
        
        # R-OFC Office
        ("R-OFC", "A-16 quiet room within 20 m of primary workspace (CON-0222)", "SD", "Floor plan"),
        ("R-OFC", "Height-adjustable desk power (sit-stand, 650-1200 mm)", "DD", "Floor plan"),
        
        # R-ASM Assembly
        ("R-ASM", "Hearing loop full room + portable backup", "CD", "Floor plan"),
        ("R-ASM", "Changing Places facility adjacent", "SD", "Floor plan"),
        ("R-ASM", "VAD fire alarm synchronised at 0.5 Hz (CON-0217)", "DD", "Reflected ceiling plan"),
        
        # R-CAN Canteen
        ("R-CAN", "Accessible counter section", "SD", "Elevation"),
        ("R-CAN", "Hearing loop at service counter", "CD", "Floor plan"),
        
        # R-CHW Changing Places
        ("R-CHW", "Ceiling hoist track ≥200 kg SWL", "CD", "Reflected ceiling plan"),
        ("R-CHW", "Height-adjustable changing bench structural mount", "CD", "Floor plan"),
        ("R-CHW", "Peninsular WC with bilateral transfer space", "SD", "Floor plan"),
        
        # R-WC Accessible WC
        ("R-WC", "Bilateral grab bar structural blocking", "CD", "Wall backing plan"),
        ("R-WC", "Emergency call pull cord + push pad at floor level", "SD", "Floor plan; elevation"),
    ]
    
    conn.executemany(
        "INSERT OR REPLACE INTO room_dar_provision (room_id, description, construction_stage, drawing_reference) VALUES (?, ?, ?, ?)",
        dar_provisions
    )
    
    # Room conflicts
    room_conflicts = [
        ("R-BA", "Grab bar diameter: MOB 32 mm vs PAIN/OFS 35 mm", "Mode P median 33 mm; Mode S OT resolves", "GRAB-BAR-DIA"),
        ("R-BA", "Floor: firm (NEU spasticity) vs cushioned (PAIN)", "Firm floor default; cushioned mat at fixed standing positions only (CON-0200)", "FLOOR-SPECIFICATION-SYSTEM"),
        ("R-KIT", "Palette: VIS high-contrast safety vs NDV muted calm", "Dual palette: muted background + high-contrast functional elements (CON-0219)", "KITCHEN-PALETTE"),
        ("R-COR", "Floor: 9+ simultaneous specifications", "Zoned resolution: firm path + TWSI lane + cushioned alcoves (CON-0200)", "FLOOR-SPECIFICATION-SYSTEM"),
        ("R-BED", "Mirror: DEM disorientation vs VIS need for mirror", "Cabinet-door mirrors (controllable exposure) for DEM/NDV/MH (CON-0201)", "MIRROR-PLACEMENT"),
        ("R-MTG", "Acoustic: RT60 ≤0.3s (DEAF/NDV) vs cost of treatment", "RT60 ≤0.3s governs — life-safety for DEAF speech intelligibility", "ACOUSTIC-TREATMENT"),
        ("R-LIV", "Thermal: OFS ≤21°C vs DEM ~24.9°C neutral", "Ambient 18-20°C + local warmth for DEM (heated seating pad) (CON-0224)", "THERMAL-RANGE"),
    ]
    
    conn.executemany(
        "INSERT OR REPLACE INTO room_conflict (room_id, description, resolution, conflict_domain) VALUES (?, ?, ?, ?)",
        room_conflicts
    )
    
    # Room-item-population mappings
    # Primary population mappings for key items in each room
    rip_data = []
    
    # Helper: add population mappings for common items across rooms
    room_pop_map = {
        "R-BA": [
            ("G-03", "MOB", "primary"), ("G-03", "PAIN", "primary"), ("G-03", "OFS", "secondary"),
            ("G-04", "MOB", "primary"), ("G-04", "DEM", "secondary"), ("G-04", "PAIN", "secondary"), ("G-04", "OFS", "secondary"), ("G-04", "NEU", "secondary"),
            ("E-07", "MOB", "primary"), ("E-07", "DEM", "primary"), ("E-07", "VIS", "secondary"),
            ("H-01", "MOB", "primary"), ("H-01", "NDV", "secondary"),
            ("G-09", "MOB", "primary"), ("G-09", "OFS", "secondary"), ("G-09", "NEU", "secondary"),
            ("H-05", "MOB", "primary"), ("H-05", "OFS", "secondary"),
            ("B-12", "DEM", "primary"), ("B-12", "MOB", "secondary"), ("B-12", "OFS", "secondary"),
            ("C-04", "VIS", "primary"), ("C-04", "DEM", "secondary"),
        ],
        "R-BED": [
            ("G-08", "MOB", "primary"), ("G-08", "DEM", "secondary"),
            ("B-12", "DEM", "primary"), ("B-12", "OFS", "secondary"),
            ("H-05", "MOB", "primary"), ("H-05", "OFS", "secondary"),
            ("G-09", "MOB", "primary"), ("G-09", "NEU", "secondary"),
            ("D-06", "DEM", "primary"), ("D-06", "IntD", "secondary"),
            ("I-04", "MOB", "primary"),
            ("H-02", "NDV", "primary"), ("H-02", "MOB", "secondary"),
        ],
        "R-KIT": [
            ("H-01", "MOB", "primary"), ("H-01", "OFS", "secondary"), ("H-01", "PAIN", "secondary"),
            ("G-05", "MOB", "primary"), ("G-05", "OFS", "secondary"),
            ("E-07", "MOB", "primary"), ("E-07", "VIS", "secondary"),
            ("C-04", "VIS", "primary"), ("C-04", "DEM", "secondary"),
        ],
        "R-COR": [
            ("E-08", "MOB", "primary"), ("E-08", "VIS", "secondary"),
            ("A-09", "MOB", "primary"), ("A-09", "NEU", "secondary"), ("A-09", "PAIN", "secondary"),
            ("E-09", "VIS", "primary"), ("E-09", "DBL", "primary"),
            ("E-10", "OFS", "primary"), ("E-10", "PAIN", "primary"), ("E-10", "DEM", "secondary"), ("E-10", "MOB", "secondary"),
            ("I-03", "OFS", "primary"), ("I-03", "PAIN", "primary"), ("I-03", "MOB", "secondary"),
            ("D-02", "DEM", "primary"), ("D-02", "VIS", "primary"), ("D-02", "IntD", "secondary"),
            ("D-08", "DEM", "primary"), ("D-08", "VIS", "primary"), ("D-08", "IntD", "secondary"),
            ("B-10", "DEAF", "primary"), ("B-10", "NDV", "secondary"),
            ("C-04", "VIS", "primary"), ("C-04", "DEM", "secondary"),
        ],
        "R-ENT": [
            ("E-06", "MOB", "primary"), ("E-06", "VIS", "secondary"),
            ("E-11", "MOB", "primary"), ("E-11", "DEM", "secondary"),
            ("E-13", "DEM", "primary"), ("E-13", "IntD", "secondary"), ("E-13", "VIS", "secondary"),
            ("H-04", "DEAF", "primary"), ("H-04", "VIS", "secondary"),
            ("E-05", "MOB", "primary"), ("E-05", "OFS", "secondary"),
        ],
        "R-REC": [
            ("G-06", "MOB", "primary"), ("G-06", "VIS", "secondary"),
            ("A-10", "DEAF", "primary"), ("A-10", "DBL", "secondary"),
            ("D-02", "DEM", "primary"), ("D-02", "VIS", "primary"),
            ("D-08", "DEM", "primary"), ("D-08", "VIS", "primary"),
            ("H-04", "DEAF", "primary"),
        ],
        "R-MTG": [
            ("A-11", "DEAF", "primary"), ("A-11", "DBL", "secondary"),
            ("K-01", "DEAF", "primary"), ("K-01", "NDV", "secondary"),
            ("H-03", "DEAF", "primary"), ("H-03", "DBL", "secondary"),
            ("H-02", "NDV", "primary"), ("H-02", "MOB", "secondary"),
            ("A-14", "NDV", "primary"), ("A-14", "DEAF", "secondary"),
        ],
        "R-OFC": [
            ("G-05", "MOB", "primary"), ("G-05", "OFS", "secondary"),
            ("A-16", "NDV", "primary"), ("A-16", "OFS", "secondary"), ("A-16", "DEM", "secondary"),
            ("D-05", "NDV", "primary"), ("D-05", "OFS", "secondary"),
            ("H-02", "NDV", "primary"), ("H-02", "MOB", "secondary"),
        ],
        "R-ASM": [
            ("A-11", "DEAF", "primary"), ("A-11", "DBL", "secondary"),
            ("B-10", "DEAF", "primary"), ("B-10", "NDV", "secondary"),
            ("H-03", "DEAF", "primary"),
            ("E-15", "MOB", "primary"),
        ],
        "R-WC": [
            ("G-03", "MOB", "primary"), ("G-03", "PAIN", "secondary"),
            ("G-04", "MOB", "primary"), ("G-04", "DEM", "secondary"),
            ("E-07", "MOB", "primary"), ("E-07", "VIS", "secondary"),
            ("H-05", "MOB", "primary"), ("H-05", "OFS", "secondary"),
            ("C-04", "VIS", "primary"),
        ],
        "R-CHW": [
            ("E-15", "MOB", "primary"),
            ("G-03", "MOB", "primary"),
            ("G-04", "MOB", "primary"),
            ("I-04", "MOB", "primary"),
            ("H-05", "MOB", "primary"),
        ],
    }
    
    for room_id, mappings in room_pop_map.items():
        for item, pop, role in mappings:
            rip_data.append((room_id, item, pop, role))
    
    conn.executemany(
        "INSERT OR REPLACE INTO room_item_population (room_id, item_code, population_code, applicability) VALUES (?, ?, ?, ?)",
        rip_data
    )
    
    conn.commit()
    
    dar_count = conn.execute("SELECT COUNT(*) FROM room_dar_provision").fetchone()[0]
    conf_count = conn.execute("SELECT COUNT(*) FROM room_conflict").fetchone()[0]
    rip_count = conn.execute("SELECT COUNT(*) FROM room_item_population").fetchone()[0]
    print(f"  C5 Rooms: {dar_count} DAR provisions, {conf_count} conflicts, {rip_count} population mappings")


def apply_remaining_connections(conn):
    """Apply remaining 35 PENDING connections as endpoints."""
    
    def get_spec(item_code):
        r = conn.execute("SELECT spec_id FROM specification WHERE item_code=? LIMIT 1", (item_code,)).fetchone()
        return r[0] if r else f"STUB-{item_code}"
    
    remaining = [
        # CON-0189 NEU sub-typing → DEM staging
        ("CON-0189", "D-02", "D-04", "cross-reference", "NEU navigation sub-typing → DEM wayfinding staging (Claessen & van der Ham 2017)."),
        # CON-0190 Rest interval harmonization
        ("CON-0190", "E-10", "I-03", "cross-reference", "Rest seating interval: DEM ≤20m, OFS ≤25m, MOB ≤50m. Governing = most restrictive."),
        # CON-0191 Inter-room temp
        ("CON-0191", "G-04", "F-07", "cross-reference", "Inter-room ≤5°C differential. Japan heat shock 6,073 deaths/year."),
        # CON-0192 MOB zero-conflict
        ("CON-0192", "A-02", "A-02", "methodology", "MOB zero-conflict status → Universal Mode base layer."),
        # CON-0193 IT/DK/KR framework
        ("CON-0193", "D-02", "D-02", "methodology", "IT DM 236/89 + DK SBi-230 + KR 2024 → Design Mode structural precedents."),
        # CON-0194 VIS+OFS compound
        ("CON-0194", "I-03", "D-02", "compound", "VIS+OFS compound: rest seating tactile-indicated + recline at ≤20m."),
        # CON-0195 Stage-aware specification
        ("CON-0195", "D-02", "D-02", "methodology", "Stage-aware specification principle for DEM and NEU."),
        # CON-0196 Overnight path lighting
        ("CON-0196", "B-12", "D-05", "cross-reference", "Overnight path lighting Universal Mode — 5+ populations, no conflict."),
        # CON-0197 PD strips vs TWSI
        ("CON-0197", "C-04", "E-09", "cross-reference", "PD gait cues (flat) vs TWSI (raised ≥4mm) differentiation protocol."),
        # CON-0198 already applied
        # CON-0199 MS+OFS clustering
        ("CON-0199", "H-01", "H-01", "cross-reference", "MS+OFS activity clustering ≤2m. Kitchen assumes fatigued user."),
        # CON-0200 already applied
        # CON-0201 DEM mirror
        ("CON-0201", "G-04", "G-04", "cross-reference", "Cabinet-door mirrors (not fixed wall) for DEM/NDV/MH bathrooms."),
        # CON-0202 already applied
        # CON-0203 G-03 three-SR
        ("CON-0203", "G-03", "G-03", "methodology", "Three-SR evidence: Clemson 2023 + Crosby 2026 + Kim 2025. GRADE HIGH."),
        # CON-0204 Alcove geometry
        ("CON-0204", "I-03", "E-10", "cross-reference", "Rest alcove ≥200mm recess + ≥900mm width + ≥450mm depth. Universal Mode."),
        # CON-0205 Overhead cane gap
        ("CON-0205", "E-08", "A-02", "cross-reference", "Overhead obstacle base-detectability ≤300mm AFF for VIS/DEM/NDV."),
        # CON-0206 already applied
        # CON-0207 already applied (measurement)
        # CON-0208 DEM bedroom
        ("CON-0208", "G-08", "D-06", "cross-reference", "DEM bedroom: 14 coordinated specifications across 10 items."),
        # CON-0209 Kitchen cabinet DEM+MOB
        ("CON-0209", "H-01", "H-01", "compound", "DEM+MOB kitchen: cabinet base ≤1200mm or eliminate overheads."),
        # CON-0210 already applied (measurement)
        # CON-0211 Acoustic zoning
        ("CON-0211", "K-01", "A-14", "cross-reference", "Building acoustic zoning matrix: STC varies by zone adjacency."),
        # CON-0212 Seat height cascade
        ("CON-0212", "E-10", "G-02", "cross-reference", "Consistent ≥480mm across all rest seating. Height transitions trigger spasticity."),
        # CON-0213 already applied
        # CON-0214 already applied
        # CON-0215 Bathroom beacon
        ("CON-0215", "G-04", "B-12", "cross-reference", "Bathroom nocturnal beacon ≤2 lux always-on through glazed panel."),
        # CON-0216 already applied
        # CON-0217 already applied
        # CON-0218 already applied
        # CON-0219 already applied
        # CON-0220 A-16 approach
        ("CON-0220", "A-16", "F-01", "cross-reference", "A-16 approach decompression: 10m reduced lighting + no through-traffic."),
        # CON-0221 already applied
        # CON-0222 already applied
        # CON-0223 already applied
        # CON-0224 already applied
        # CON-0225 Keall cost-benefit
        ("CON-0225", "G-03", "G-03", "methodology", "Keall 2017 cost-benefit: RCT-derived ROI for home modifications."),
        # CON-0226 IntD layout>signage
        ("CON-0226", "D-02", "D-02", "cross-reference", "IntD governed by layout>signage principle (Marquardt transfer)."),
        # CON-0227 PAS 6463 dual-rationale
        ("CON-0227", "D-05", "C-04", "cross-reference", "Multi-sensory zone: VIS compensatory redundancy + NDV graduated management."),
        # CON-0228 already applied
        # CON-0229 already applied
        # CON-0230 Crosby hospital admission
        ("CON-0230", "G-03", "G-03", "methodology", "Crosby 2026: grab bars reduce hospital admissions (economics)."),
        # CON-0231 already applied
        # CON-0232 Biophilic economics
        ("CON-0232", "B-09", "B-09", "methodology", "Al Khatib 2024: biophilic design reduces hospitalisation. Part 11 economics."),
        # CON-0233 already applied
        # CON-0234 HAwD process
        ("CON-0234", "G-03", "G-03", "methodology", "RCOT HAwD 6-stage process → Part 9 reference adaptation pathway."),
        # CON-0235 already applied
        # CON-0236 Passini decision theory
        ("CON-0236", "D-02", "D-02", "methodology", "Passini 1984 decision theory → Part 1 wayfinding foundation."),
        # CON-0237 already applied
        # CON-0238 already applied
        # CON-0239 Habinteg cross-population
        ("CON-0239", "H-02", "H-02", "methodology", "Habinteg 2024: cross-population OT practice bridge. Part 1/Part 9."),
    ]
    
    for con_id, src_item, tgt_item, conn_type, desc in remaining:
        src_spec = get_spec(src_item)
        conn.execute("""
            INSERT OR REPLACE INTO connection_endpoint
            (connection_id, spec_id, target_spec_id, target_item_code, connection_type, description)
            VALUES (?, ?, NULL, ?, ?, ?)
        """, (con_id, src_spec, tgt_item, conn_type, desc))
    
    conn.commit()
    
    total = conn.execute("SELECT COUNT(*) FROM connection_endpoint").fetchone()[0]
    print(f"  Connections: {len(remaining)} endpoints added. Total: {total}")


def main():
    conn = sqlite3.connect(str(DB_PATH))
    
    print("=== C-Stage Comprehensive Enrichment ===")
    enrich_prose(conn)
    enrich_spec_sources(conn)
    enrich_rooms(conn)
    apply_remaining_connections(conn)
    
    # Final report
    print(f"\n=== Final Database State ===")
    for table in ["specification", "population", "specification_population", "measurement",
                   "jurisdictional_value", "conflict", "connection_endpoint", "specification_source",
                   "room", "room_item", "room_dar_provision", "room_conflict", "room_item_population",
                   "evidence_source", "economics_entry"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count}")
    
    conn.close()
    print("\nC-stage enrichment complete.")


if __name__ == "__main__":
    main()
