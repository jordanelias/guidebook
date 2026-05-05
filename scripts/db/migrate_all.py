#!/usr/bin/env python3
"""
scripts/db/migrate_all.py — Bulk migration of all content into SQLite.

Reinitializes the database and migrates:
1. Specifications (73 records from specification-database.json)
2. Populations (11 records from populations.json)
3. Conflicts (14 records from conflicts.json)
4. Doctrines (16 records from convert_doctrines.py definitions)
5. Specialists (6 records from convert_specialists.py definitions)
6. Rooms (17 records from convert_rooms.py definitions)
7. Throughlines (parsed from throughline-analysis.md)
8. Economics (parsed from economics.json)

Usage:
    python3 scripts/db/migrate_all.py
    python3 scripts/db/migrate_all.py --verify-only
"""

import json
import os
import re
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = REPO_ROOT / "data" / "db" / "guidebook.db"

# Add repo root for imports
sys.path.insert(0, str(REPO_ROOT))


def _parse_evidence_tier(tier_val):
    """Parse evidence tier from various formats to integer 1-6."""
    if tier_val is None:
        return None
    if isinstance(tier_val, int):
        return tier_val if 1 <= tier_val <= 6 else None
    s = str(tier_val)
    if s.isdigit():
        v = int(s)
        return v if 1 <= v <= 6 else None
    import re as _re
    nums = _re.findall(r"\d+", s)
    if nums:
        v = int(nums[0])  # lowest = most conservative
        return v if 1 <= v <= 6 else None
    return None


def migrate_specifications(conn):
    """Migrate all specifications from specification-database.json."""
    with open(REPO_ROOT / "references" / "specification-database.json", "r") as f:
        db = json.load(f)

    specs = db["specifications"]
    count = 0

    for s in specs:
        # Map JSON fields to SQLite columns
        conflict_domains = json.dumps(s.get("conflict_domains")) if s.get("conflict_domains") else None
        populations = s.get("populations", [])

        conn.execute("""
            INSERT OR REPLACE INTO specification (
                spec_id, item_code, title, parameter, value_type,
                recommendation_strength, evidence_tier,
                universal_value, population_value, person_specific_note,
                question_heading, summary, evidence_summary,
                dar_relevant, structural_backing_required,
                retrofit_category, ot_evidence_basis, curation_status,
                conflict_domains, bpc_source_slug, notes, context_note,
                percentile_basis, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
        """, (
            s["spec_id"], s["item_code"], s.get("slug", s["item_code"]),
            s.get("parameter"), s.get("value_type"),
            s.get("recommendation_strength", "UNSET"), _parse_evidence_tier(s.get("evidence_tier")),
            None,  # universal_value — populated from measurements
            json.dumps({"min": s.get("value_min"), "max": s.get("value_max"),
                        "median": s.get("value_median"), "unit": s.get("unit")})
            if s.get("value_min") is not None else None,
            s.get("person_specific_note"),
            s.get("question_heading"), s.get("summary"), s.get("evidence_summary"),
            1 if s.get("dar_relevant") else 0,
            1 if s.get("structural_backing_required") else 0,
            s.get("retrofit_category"), s.get("ot_evidence_basis"),
            s.get("curation_status", "automated"),
            conflict_domains, s.get("bpc_source_slug"),
            s.get("notes"), s.get("context_note"), s.get("percentile_basis"),
        ))

        # Specification-population joins
        for pop_code in populations:
            conn.execute(
                "INSERT OR REPLACE INTO specification_population (spec_id, population_code, role) VALUES (?, ?, 'primary')",
                (s["spec_id"], pop_code),
            )

        # Measurements from value fields
        if s.get("value_min") is not None or s.get("value_max") is not None:
            conn.execute("""
                INSERT INTO measurement (spec_id, design_mode, value_min, value_max, value_median, unit, unit_display)
                VALUES (?, 'population_based', ?, ?, ?, ?, ?)
            """, (
                s["spec_id"], s.get("value_min"), s.get("value_max"),
                s.get("value_median"), s.get("unit"),
                f'{s.get("value_min","?")}–{s.get("value_max","?")} {s.get("unit","")}'.strip(),
            ))

        # Jurisdictional values (plain codes — detail extraction is C-stage)
        for jcode in s.get("jurisdictions_supporting", []):
            if isinstance(jcode, str):
                conn.execute("""
                    INSERT INTO jurisdictional_value (spec_id, jurisdiction, notes)
                    VALUES (?, ?, 'supporting')
                """, (s["spec_id"], jcode))
            elif isinstance(jcode, dict):
                conn.execute("""
                    INSERT INTO jurisdictional_value (spec_id, jurisdiction, standard_name, clause_ref, value_text, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    s["spec_id"], jcode.get("jurisdiction"), jcode.get("standard"),
                    jcode.get("clause"), jcode.get("value"), jcode.get("notes"),
                ))

        for jcode in s.get("jurisdictions_divergent", []):
            if isinstance(jcode, str):
                conn.execute("""
                    INSERT INTO jurisdictional_value (spec_id, jurisdiction, notes)
                    VALUES (?, ?, 'divergent')
                """, (s["spec_id"], jcode))

        count += 1

    conn.commit()
    return count


def migrate_populations(conn):
    """Migrate all populations from populations.json."""
    with open(REPO_ROOT / "references" / "website" / "data" / "populations.json", "r") as f:
        data = json.load(f)

    count = 0
    for p in data["populations"]:
        conn.execute("""
            INSERT OR REPLACE INTO population (
                code, label, functional_profile,
                co1_status, co1_gap_note, evidence_confidence,
                co_occurrence_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            p["population_id"], p["label"], p.get("functional_profile"),
            p.get("co1_status"), p.get("co1_gap_note"),
            p.get("evidence_confidence"), p.get("co_occurrence_notes"),
        ))
        count += 1

    # Sub-code populations referenced in spec_population joins
    sub_pops = [
        ("ALL", "Universal (All Populations)", "Population-agnostic provisions applicable regardless of functional capacity.", None, None, None),
        ("MOB/AMB", "Mobility — Ambulant", "Walking with or without aids. Reduced balance, endurance, or gait pattern.", None, None, "MODERATE"),
        ("NDV/AUT", "Neurodivergence — Autism", "Autism spectrum. Sensory processing differences per Dunn model.", None, None, "MODERATE"),
        ("IntD", "Intellectual Disability", "Cognitive impairment affecting environmental comprehension and wayfinding.", None, None, "LOW"),
    ]
    for code, label, profile, co1, gap, conf in sub_pops:
        conn.execute(
            "INSERT OR REPLACE INTO population (code, label, functional_profile, co1_status, co1_gap_note, evidence_confidence) VALUES (?, ?, ?, ?, ?, ?)",
            (code, label, profile, co1, gap, conf),
        )
        count += 1

    conn.commit()
    return count


def migrate_conflicts(conn):
    """Migrate all conflicts from conflicts.json."""
    with open(REPO_ROOT / "references" / "website" / "data" / "conflicts.json", "r") as f:
        data = json.load(f)

    count = 0

    for c in data.get("resolved_conflicts", []):
        pop_a = c.get("population_a", {})
        pop_b = c.get("population_b", {})
        resolution = c.get("resolution", {})

        conn.execute("""
            INSERT OR REPLACE INTO conflict (
                conflict_id, conflict_label, domain,
                population_a, population_b,
                governing_principle, resolution_status, resolution_description,
                strategy_codes, decision_tree, unresolvable_residual,
                specifications_involved, citations
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["conflict_id"], c.get("conflict_label"), c.get("domain"),
            json.dumps(pop_a), json.dumps(pop_b),
            c.get("governing_principle"),
            "RESOLVED-EVIDENCE",
            resolution.get("description") if isinstance(resolution, dict) else str(resolution),
            json.dumps(resolution.get("strategy_codes", [])) if isinstance(resolution, dict) else None,
            json.dumps(c.get("decision_tree")),
            c.get("unresolvable_residual"),
            json.dumps(c.get("specifications_involved", [])),
            json.dumps(c.get("citations", [])),
        ))
        count += 1

    for c in data.get("unresolvable_conflicts", []):
        conn.execute("""
            INSERT OR REPLACE INTO conflict (
                conflict_id, conflict_label, domain,
                resolution_status, resolution_description,
                mode_s_trigger, mitigation,
                specifications_involved
            ) VALUES (?, ?, ?, 'UNRESOLVABLE-MODE-S', ?, ?, ?, ?)
        """, (
            c["conflict_id"], c.get("conflict_label"), c.get("domain"),
            json.dumps(c.get("resolution")) if c.get("resolution") else None,
            c.get("trigger"), c.get("mitigation"),
            json.dumps([c.get("related_conflict")]) if c.get("related_conflict") else None,
        ))
        count += 1

    conn.commit()
    return count


def migrate_doctrines(conn):
    """Migrate doctrines from converter definitions."""
    from scripts.convert.convert_doctrines import DOCTRINES

    count = 0
    for d in DOCTRINES:
        conn.execute("""
            INSERT OR REPLACE INTO doctrine (
                doctrine_id, slug, title, doctrine_group, statement,
                implications, part_section, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active')
        """, (
            d["doctrine_id"], d["slug"], d["title"], d["group"],
            d["statement"], d.get("implications"), d.get("part_section"),
        ))
        count += 1

    conn.commit()
    return count


def migrate_specialists(conn):
    """Migrate specialists from converter definitions."""
    from scripts.convert.convert_specialists import SPECIALISTS

    count = 0
    for s in SPECIALISTS:
        conn.execute("""
            INSERT OR REPLACE INTO specialist (
                specialist_id, role, role_label, part_section,
                role_description, co_design_notes, guidebook_relationship, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active')
        """, (
            s["specialist_id"], s["role"], s["role_label"], s.get("part_section"),
            s["role_description"], s.get("co_design_notes"), s.get("guidebook_relationship"),
        ))

        # Triggers
        for trigger in s.get("appointment_triggers", []):
            conn.execute(
                "INSERT INTO specialist_trigger (specialist_id, trigger_text) VALUES (?, ?)",
                (s["specialist_id"], trigger),
            )

        # Population joins
        for pop in s.get("population_codes", []):
            conn.execute(
                "INSERT OR REPLACE INTO specialist_population (specialist_id, population_code) VALUES (?, ?)",
                (s["specialist_id"], pop),
            )

        count += 1

    conn.commit()
    return count


def migrate_rooms(conn):
    """Migrate rooms from converter definitions."""
    from scripts.convert.convert_rooms import RESIDENTIAL_ROOMS, NON_RESIDENTIAL_ROOMS

    count = 0
    for room_list, btype, part in [(RESIDENTIAL_ROOMS, "residential", 6), (NON_RESIDENTIAL_ROOMS, "non-residential", 7)]:
        for r in room_list:
            conn.execute("""
                INSERT OR REPLACE INTO room (
                    room_id, room_label, building_type, part_source, section,
                    evidence_density, status
                ) VALUES (?, ?, ?, ?, ?, ?, 'active')
            """, (
                r["room_id"], r["room_label"], btype, part,
                r.get("section"), r.get("evidence_density"),
            ))
            count += 1

    conn.commit()
    return count


def migrate_throughlines(conn):
    """Migrate throughlines from throughline-analysis.md."""
    input_path = REPO_ROOT / "references" / "throughline-analysis.md"
    if not input_path.exists():
        return 0

    with open(input_path, "r") as f:
        content = f.read()

    sections = re.split(r"(?=^### T-\d{2}\.)", content, flags=re.MULTILINE)
    count = 0

    for section in sections:
        m = re.match(r"^### (T-\d{2})\.\s*(.+)$", section, re.MULTILINE)
        if not m:
            continue

        tid = m.group(1)
        title = m.group(2).strip()

        lines = section.split("\n")
        desc_lines = []
        in_desc = False
        for line in lines[1:]:
            stripped = line.strip()
            if not in_desc and stripped:
                in_desc = True
            if in_desc:
                if not stripped and desc_lines:
                    break
                desc_lines.append(stripped)

        description = " ".join(desc_lines).strip()[:500]
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

        spec_refs = sorted(set(re.findall(r"\b([A-K]-\d{2})\b", section)))

        conn.execute("""
            INSERT OR REPLACE INTO throughline (
                throughline_id, title, slug, description, status
            ) VALUES (?, ?, ?, ?, 'active')
        """, (tid, title, slug, description))

        for ref in spec_refs:
            conn.execute(
                "INSERT OR REPLACE INTO throughline_specification (throughline_id, item_code) VALUES (?, ?)",
                (tid, ref),
            )

        count += 1

    conn.commit()
    return count


def migrate_economics(conn):
    """Migrate economics from economics.json."""
    input_path = REPO_ROOT / "references" / "website" / "data" / "economics.json"
    if not input_path.exists():
        return 0

    with open(input_path, "r") as f:
        data = json.load(f)

    SECTION_MAP = {
        "cost_premiums": ("construction", "cost_premium"),
        "retrofit_multipliers": ("construction", "retrofit_multiplier"),
        "grant_programmes": ("inaction", "grant_programme"),
        "health_outcomes": ("health", "health_outcome"),
        "housing_deficit": ("inaction", "housing_deficit"),
        "research_gaps": ("health", "research_gap"),
    }

    count = 0
    counter = 1

    for section_key, (pillar, entry_type) in SECTION_MAP.items():
        section_data = data.get(section_key, [])
        if not isinstance(section_data, list):
            continue

        for item in section_data:
            entry_id = f"ECON-{counter:04d}"
            source = item.get("source", item.get("programme_name", "Unknown"))
            finding = item.get("finding", item.get("description", ""))

            value_numeric = None
            for num_field in ["premium_percent_min", "multiplier", "max_funding", "accessible_pct", "gap_units"]:
                if num_field in item and item[num_field] is not None:
                    try:
                        value_numeric = float(item[num_field])
                    except (ValueError, TypeError):
                        pass
                    break

            conn.execute("""
                INSERT OR REPLACE INTO economics_entry (
                    entry_id, pillar, entry_type, source, jurisdiction,
                    finding, study_design, value_numeric, currency, bcr, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
            """, (
                entry_id, pillar, entry_type, source,
                item.get("jurisdiction"), finding,
                item.get("study_design") or item.get("design"),
                value_numeric, item.get("currency"), item.get("bcr"),
            ))
            counter += 1
            count += 1

    # Market value entries
    mv = data.get("market_value", {})
    if isinstance(mv, dict):
        for key, val in mv.items():
            if isinstance(val, list):
                for item in val:
                    entry_id = f"ECON-{counter:04d}"
                    conn.execute("""
                        INSERT OR REPLACE INTO economics_entry (
                            entry_id, pillar, entry_type, source, jurisdiction,
                            finding, status
                        ) VALUES (?, 'market', 'market_value', ?, ?, ?, 'active')
                    """, (
                        entry_id, item.get("source", key),
                        item.get("jurisdiction"), item.get("finding", ""),
                    ))
                    counter += 1
                    count += 1

    conn.commit()
    return count


def create_item_stubs(conn):
    """Create stub specs for Part 4 items not yet in specification table."""
    import yaml

    existing = set(r[0] for r in conn.execute(
        "SELECT DISTINCT item_code FROM specification"
    ).fetchall())

    with open(REPO_ROOT / "parts" / "v10" / "part04.md", "r") as f:
        part4_lines = f.readlines()

    with open(REPO_ROOT / "references" / "part04-item-index.md", "r") as f:
        index_content = f.read()

    items = {}
    for line in index_content.split("\n"):
        m = re.match(r"\|\s*([A-K]-\d{2})\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", line)
        if m:
            code, title = m.group(1), m.group(2).strip()
            start, end = int(m.group(3)), int(m.group(4))
            if "MERGED" not in title.upper() and "ABSORBED" not in title.upper():
                items[code] = {"title": title, "start": start, "end": end}

    with open(REPO_ROOT / "data" / "question-headings.yaml", "r") as f:
        qh = yaml.safe_load(f)

    count = 0
    for code in sorted(items):
        if code in existing:
            continue

        item = items[code]
        content = "".join(part4_lines[item["start"] - 1 : item["end"]])

        # Extract populations
        pop_match = re.search(r"\*\*Applicable Groups:\*\*\s*(.+)", content)
        populations = []
        if pop_match:
            populations = re.findall(
                r"\b(MOB|VIS|DEAF|NEU|DEM|NDV|PAIN|DBL|OFS|IntD|ALL"
                r"|MOB/UPL|NDV/AUT|NDV/ADHD|NDV/SENS|NDV/MH"
                r"|NEU/PCS|OFS/ME|OFS/POTS|OFS/MCAS)\b",
                pop_match.group(1),
            )

        # Evidence tier from grade_confidence
        tier = None
        tier_match = re.search(r"grade_confidence:\s*(HIGH|MODERATE|LOW)", content)
        if tier_match:
            tier = {"HIGH": 2, "MODERATE": 3, "LOW": 4}.get(tier_match.group(1), 4)

        # Retrofit category
        retrofit = None
        retro_match = re.search(r"Retrofit penalty:\s*(LOW|MODERATE|HIGH|STRUCTURAL)", content, re.IGNORECASE)
        if retro_match:
            retrofit = retro_match.group(1).upper()

        # Question heading
        qh_entry = qh.get(code, {})
        question = qh_entry.get("question_heading") if isinstance(qh_entry, dict) else None

        # DAR and structural
        dar = 1 if "dar" in content.lower() or "structural blocking" in content.lower() else 0
        structural = 1 if re.search(r"structural.{0,20}backing|structural.{0,20}blocking|STRUCTURAL", content) else 0

        spec_id = f"SPEC-{code.replace('-', '')}-001"
        conn.execute("""
            INSERT OR REPLACE INTO specification (
                spec_id, item_code, title, parameter,
                evidence_tier, question_heading,
                dar_relevant, structural_backing_required,
                retrofit_category, curation_status, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'automated', 'active')
        """, (spec_id, code, item["title"], item["title"], tier, question, dar, structural, retrofit))

        for pop in populations:
            conn.execute(
                "INSERT OR REPLACE INTO specification_population (spec_id, population_code, role) VALUES (?, ?, 'primary')",
                (spec_id, pop),
            )

        count += 1

    # Backfill question headings for specs that have them in YAML but not in DB
    for code, entry in qh.items():
        if isinstance(entry, dict) and "question_heading" in entry:
            conn.execute(
                'UPDATE specification SET question_heading = ? WHERE item_code = ? AND question_heading IS NULL',
                (entry["question_heading"], code),
            )

    conn.commit()
    return count


def verify(conn):
    """Print verification report."""
    tables = [
        "specification", "population", "specification_population",
        "measurement", "jurisdictional_value", "conflict",
        "doctrine", "specialist", "specialist_trigger", "specialist_population",
        "room", "room_item", "room_item_population",
        "room_dar_provision", "room_conflict",
        "throughline", "throughline_specification",
        "economics_entry", "evidence_source",
    ]

    print("\n=== Migration Verification ===")
    total = 0
    for table in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        total += count
        print(f"  {table:30s} {count:5d} rows")
    print(f"  {'TOTAL':30s} {total:5d} rows")

    # Check spec coverage
    spec_codes = conn.execute(
        "SELECT DISTINCT item_code FROM specification WHERE item_code NOT LIKE '[%'"
    ).fetchall()
    print(f"\n  Unique item codes: {len(spec_codes)}")

    # Check population coverage
    pop_count = conn.execute("SELECT COUNT(*) FROM population").fetchone()[0]
    print(f"  Populations: {pop_count}")

    # Check jurisdiction coverage
    jv_count = conn.execute("SELECT COUNT(DISTINCT jurisdiction) FROM jurisdictional_value").fetchone()[0]
    print(f"  Distinct jurisdictions: {jv_count}")

    # Check conflicts
    resolved = conn.execute("SELECT COUNT(*) FROM conflict WHERE resolution_status = 'RESOLVED-EVIDENCE'").fetchone()[0]
    unresolvable = conn.execute("SELECT COUNT(*) FROM conflict WHERE resolution_status = 'UNRESOLVABLE-MODE-S'").fetchone()[0]
    print(f"  Conflicts: {resolved} resolved + {unresolvable} unresolvable")


def migrate_evidence_sources(conn):
    """C7: Migrate evidence sources from global-reference-registry.md."""
    registry_path = REPO_ROOT / "references" / "global-reference-registry.md"
    if not registry_path.exists():
        return 0

    with open(registry_path, "r") as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        line = line.strip()
        if not line.startswith("| REF-"):
            continue

        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 8:
            continue

        ref_id = cells[0]
        authors = cells[1] or None
        year_str = cells[2]
        title = cells[3] or None
        doi = cells[4] if cells[4] else None
        pmid = cells[5] if len(cells) > 5 and cells[5] else None
        tier_str = cells[6] if len(cells) > 6 else None
        jurisdiction = cells[7] if len(cells) > 7 and cells[7] else None
        used_in = cells[8] if len(cells) > 8 else None

        year = None
        if year_str:
            m = re.search(r"(\d{4})", year_str)
            if m:
                year = int(m.group(1))

        tier = None
        if tier_str:
            m = re.search(r"(\d)", tier_str)
            if m:
                tier = int(m.group(1))

        if doi and not doi.startswith("10."):
            doi_match = re.search(r"(10\.\S+)", doi)
            doi = doi_match.group(1) if doi_match else None

        conn.execute("""
            INSERT OR REPLACE INTO evidence_source (
                ref_id, authors, year, title, doi, evidence_tier, jurisdiction, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (ref_id, authors, year, title, doi, tier, jurisdiction, used_in))
        count += 1

    conn.commit()
    return count


def extract_room_matrices(conn):
    """C5: Extract room item matrices from Part 6."""
    part6_path = REPO_ROOT / "parts" / "v10" / "part06.md"
    if not part6_path.exists():
        return 0

    with open(part6_path, "r") as f:
        content = f.read()

    POP_CODES = ["MOB", "VIS", "DEAF", "DEM", "NDV", "OFS", "DBL", "PAIN", "NEU"]
    ROOM_MAP = {
        "§6.1": "R-ENT", "§6.2": "R-GAR", "§6.3": "R-LAU",
        "§6.4": "R-BED", "§6.5": "R-BA", "§6.6": "R-LIV",
        "§6.7": "R-KIT", "§6.8": "R-HAL", "§6.9": "R-STA",
    }

    sections = re.split(r"(?=^### §\d+\.\d+)", content, flags=re.MULTILINE)
    total_items = 0

    for section in sections:
        header_match = re.match(r"^### (§\d+\.\d+\w?)", section)
        if not header_match:
            continue

        section_id = header_match.group(1)
        room_id = ROOM_MAP.get(section_id)
        if not room_id:
            continue

        # Update criticality note
        crit_match = re.search(
            r"\*\*Room criticality:\*\*\s*(.+?)(?=\n\n|\n\*\*Item)", section, re.DOTALL
        )
        if crit_match:
            conn.execute(
                "UPDATE room SET criticality_note = ? WHERE room_id = ?",
                (crit_match.group(1).strip()[:500], room_id),
            )

        # Find item application table
        table_idx = section.find("Item application table")
        if table_idx < 0:
            continue

        table_block = section[table_idx:]
        lines = table_block.split("\n")

        header_line = None
        data_lines = []
        in_data = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("| Item"):
                header_line = stripped
                continue
            if stripped.startswith("| ---"):
                in_data = True
                continue
            if in_data:
                clean = stripped
                if clean.startswith("**"):
                    clean = clean[2:]
                if clean.endswith("**"):
                    clean = clean[:-2]
                clean = clean.replace("\\*\\*", "").strip()
                if not clean or (not clean.startswith("|")):
                    break
                if clean.startswith("| *●") or "---" in clean:
                    continue
                data_lines.append(clean)

        if not header_line:
            continue

        headers = [h.strip() for h in header_line.split("|")[1:-1]]
        pop_cols = {}
        for i, h in enumerate(headers):
            for pop in POP_CODES:
                if h.strip() == pop:
                    pop_cols[i] = pop

        stage_col = None
        for i, h in enumerate(headers):
            if "design" in h.lower() and "stage" in h.lower():
                stage_col = i

        for line in data_lines:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) < 3:
                continue

            cell0 = re.sub(r"R-[A-Z]+-\d+\w?\s*", "", cells[0])
            code_match = re.search(r"([A-K]-\d{2})", cell0)
            if not code_match:
                continue

            item_code = code_match.group(1)
            stage = cells[stage_col].strip().replace("\\*\\*", "") if stage_col and len(cells) > stage_col else None

            pop_app = {}
            for col_idx, pop_code in pop_cols.items():
                if col_idx < len(cells):
                    val = cells[col_idx].strip()
                    if "●" in val:
                        pop_app[pop_code] = "primary"
                    elif "○" in val:
                        pop_app[pop_code] = "secondary"

            conn.execute(
                "INSERT OR REPLACE INTO room_item (room_id, item_code, design_stage) VALUES (?, ?, ?)",
                (room_id, item_code, stage),
            )

            for pop, role in pop_app.items():
                conn.execute(
                    "INSERT OR REPLACE INTO room_item_population (room_id, item_code, population_code, applicability) VALUES (?, ?, ?, ?)",
                    (room_id, item_code, pop, role),
                )

            total_items += 1

        # DAR provisions
        dar_match = re.search(
            r"\*\*DAR provisions.*?\n\n\|.+\n\|[-| ]+\n((?:\|.+\n)+)", section, re.DOTALL
        )
        if dar_match:
            for row in dar_match.group(1).strip().split("\n"):
                cells = [c.strip() for c in row.split("|")[1:-1]]
                if len(cells) >= 2 and cells[0] and not cells[0].startswith("*"):
                    conn.execute(
                        "INSERT INTO room_dar_provision (room_id, description, notes) VALUES (?, ?, ?)",
                        (room_id, cells[0], cells[1] if len(cells) > 1 else None),
                    )

        # Conflict register
        conf_match = re.search(
            r"\*\*Conflict register.*?\n\n\|.+\n\|[-| ]+\n((?:\|.+\n)+)", section, re.DOTALL
        )
        if conf_match:
            for row in conf_match.group(1).strip().split("\n"):
                cells = [c.strip() for c in row.split("|")[1:-1]]
                if len(cells) >= 2 and cells[0] and not cells[0].startswith("*"):
                    conn.execute(
                        "INSERT INTO room_conflict (room_id, description, resolution) VALUES (?, ?, ?)",
                        (room_id, cells[0], cells[2] if len(cells) > 2 else None),
                    )

    conn.commit()
    return total_items


def extract_part4_content(conn):
    """C3: Extract specification content fields from Part 4 prose."""
    import yaml

    with open(REPO_ROOT / "parts" / "v10" / "part04.md", "r") as f:
        part4_lines = f.readlines()

    with open(REPO_ROOT / "references" / "part04-item-index.md", "r") as f:
        index_content = f.read()

    items = {}
    for line in index_content.split("\n"):
        m = re.match(r"\|\s*([A-K]-\d{2})\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", line)
        if m:
            code = m.group(1)
            if "MERGED" not in m.group(2).upper() and "ABSORBED" not in m.group(2).upper():
                items[code] = {"start": int(m.group(3)), "end": int(m.group(4))}

    count = 0
    for code, item in sorted(items.items()):
        content = "".join(part4_lines[item["start"] - 1 : item["end"]])
        updates = {}

        # schedule_md
        spec_match = re.search(
            r"\*\*Specifications:\*\*\s*\n(.*?)(?=\n\*\*[A-Z]|\n##|\Z)", content, re.DOTALL
        )
        if spec_match:
            schedule = spec_match.group(1).strip()
            if schedule and len(schedule) > 10:
                updates["schedule_md"] = schedule

        # retrofit_category
        retro_match = re.search(r"Retrofit penalty:\s*(LOW|MODERATE|HIGH|STRUCTURAL)", content, re.IGNORECASE)
        if retro_match:
            cat = retro_match.group(1).upper()
            full = re.search(r"Retrofit penalty:\s*(.+?)(?:\.|$)", content, re.IGNORECASE)
            if full and "STRUCTURAL" in full.group(1).upper():
                cat = "STRUCTURAL"
            updates["retrofit_category"] = cat

        # ot_evidence_basis
        ot_match = re.search(r"\*\*Evidence basis \(OT\):\*\*\s*(.+?)(?=\n\n|\n\*\*|\Z)", content, re.DOTALL)
        if ot_match and len(ot_match.group(1).strip()) > 5:
            updates["ot_evidence_basis"] = ot_match.group(1).strip()[:500]

        # dar_note
        dar_mentions = re.findall(r"(?:DAR|structural blocking|structural backing|design.for.adaptab).*", content, re.IGNORECASE)
        if dar_mentions and len(dar_mentions[0].strip()) > 10:
            updates["dar_note"] = dar_mentions[0].strip()[:300]

        # evidence_tier
        tier_match = re.search(r"grade_confidence:\s*(HIGH|MODERATE|LOW)", content)
        if tier_match:
            updates["evidence_tier"] = {"HIGH": 2, "MODERATE": 3, "LOW": 4}[tier_match.group(1)]

        # summary — from Description first sentence
        desc_match = re.search(r"\*\*Description:\*\*\s*(.+?)(?=\n\n|\n\*\*)", content, re.DOTALL)
        if desc_match:
            desc = desc_match.group(1).strip()
            first_sent = re.split(r"(?<=[.!?])\s", desc)[0]
            if len(first_sent) > 10:
                updates["summary"] = first_sent[:300]

        # evidence_summary
        cite_match = re.search(r"\*\*Key citations:\*\*\s*(.+?)(?=\n\n|\n\*\*|\Z)", content, re.DOTALL)
        if cite_match and len(cite_match.group(1).strip()) > 5:
            updates["evidence_summary"] = cite_match.group(1).strip()[:500]

        # why_md — from Description full
        if desc_match and len(desc_match.group(1).strip()) > 30:
            updates["why_md"] = desc_match.group(1).strip()

        # Apply (only fill nulls)
        for field, value in updates.items():
            conn.execute(
                f'UPDATE specification SET {field} = ? WHERE item_code = ? AND ({field} IS NULL OR {field} = "")',
                (value, code),
            )

        if updates:
            count += 1

    conn.commit()
    return count




def main():
    verify_only = "--verify-only" in sys.argv

    if verify_only:
        conn = sqlite3.connect(str(DB_PATH))
        verify(conn)
        conn.close()
        return

    # Reinitialize database
    print("Reinitializing database...")
    if DB_PATH.exists():
        DB_PATH.unlink()

    from scripts.db.init_db import init_db
    init_db(DB_PATH)

    conn = sqlite3.connect(str(DB_PATH))

    print("\nMigrating populations...")
    pop_count = migrate_populations(conn)
    print(f"  → {pop_count} populations")

    print("Migrating specifications...")
    spec_count = migrate_specifications(conn)
    print(f"  → {spec_count} specifications")

    print("Migrating conflicts...")
    conflict_count = migrate_conflicts(conn)
    print(f"  → {conflict_count} conflicts")

    print("Migrating doctrines...")
    doc_count = migrate_doctrines(conn)
    print(f"  → {doc_count} doctrines")

    print("Migrating specialists...")
    specialist_count = migrate_specialists(conn)
    print(f"  → {specialist_count} specialists")

    print("Migrating rooms...")
    room_count = migrate_rooms(conn)
    print(f"  → {room_count} rooms")

    print("Migrating throughlines...")
    tl_count = migrate_throughlines(conn)
    print(f"  → {tl_count} throughlines")

    print("Migrating economics...")
    econ_count = migrate_economics(conn)
    print(f"  → {econ_count} economics entries")

    print("Migrating evidence sources...")
    evidence_count = migrate_evidence_sources(conn)
    print(f"  → {evidence_count} evidence sources")

    print("Extracting room matrices from Part 6...")
    room_count = extract_room_matrices(conn)
    print(f"  → {room_count} room items")

    print("Creating item stubs from Part 4...")
    stub_count = create_item_stubs(conn)
    print(f"  → {stub_count} item stubs")

    print("Extracting Part 4 content...")
    extract_count = extract_part4_content(conn)
    print(f"  → {extract_count} items enriched")

    verify(conn)
    conn.close()

    print("\nBulk migration complete.")


if __name__ == "__main__":
    main()
