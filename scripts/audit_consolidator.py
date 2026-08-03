"""
scripts/audit_consolidator.py — Implementation of audit-consolidator skill.

Usage:
    python3 scripts/audit_consolidator.py --item I-01 --session SESSION_NAME
    python3 scripts/audit_consolidator.py --item I-01 --session SESSION_NAME --dry-run

Produces: references/audit-briefs/{item_code}_brief.md
Updates:  item_audit_runs status → COMPLETE
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DB_PATH   = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))

# Gap category → routing skill
RESEARCH_CATS  = {"RP", "EC", "EG", "CONF", "MX"}
AUTHORING_CATS = {"AUDT", "SW", "CR", "CD"}
INFRA_CATS     = {"CI", "DEC", "ST"}

CATEGORY_SKILL = {
    "RP":   "functional-deficit-researcher / multilingual-research",
    "EC":   "economics-researcher",
    "EG":   "evidence-auditor → FDR",
    "CONF": "cross-population-conflict-mapper (resolution evidence run)",
    "MX":   "multilingual-research",
    "AUDT": "item-specification-writer",
    "SW":   "item-specification-writer",
    "CR":   "connection-discovery → ISW",
    "CD":   "item-specification-writer",
    "CI":   "technical",
    "DEC":  "workplan-orchestrator",
    "ST":   "structure-auditor",
}


def load_data(conn, item_code):
    gaps = conn.execute(
        "SELECT * FROM gaps WHERE section=? AND status LIKE 'OPEN%' ORDER BY priority, category",
        (item_code,)
    ).fetchall()

    conflicts = conn.execute(
        "SELECT * FROM conflicts WHERE item_code=? ORDER BY status, domain",
        (item_code,)
    ).fetchall()

    connections = conn.execute("""
        SELECT c.con_id, c.confidence, c.connection_type, c.description, c.status
        FROM connections c
        JOIN connection_targets ct ON c.con_id = ct.con_id
        WHERE ct.target LIKE ? AND c.status='PENDING'
        ORDER BY c.confidence DESC, c.con_id
    """, (f"%{item_code}%",)).fetchall()

    deferred = conn.execute(
        "SELECT slug, local_ref_id, deferred_reason, created_by_session "
        "FROM citation_mining WHERE deferred_reason IS NOT NULL "
        "ORDER BY created_by_session"
    ).fetchall()

    item = conn.execute(
        "SELECT * FROM items WHERE item_code=?", (item_code,)
    ).fetchone()

    run = conn.execute(
        "SELECT * FROM item_audit_runs WHERE item_code=? ORDER BY created_at DESC LIMIT 1",
        (item_code,)
    ).fetchone()

    return gaps, conflicts, connections, deferred, item, run


def check_integrity(conn, conflicts):
    warnings = []
    for c in conflicts:
        gid = c["gap_id"]
        if gid:
            gap = conn.execute("SELECT gap_id, status FROM gaps WHERE gap_id=?", (gid,)).fetchone()
            if not gap:
                warnings.append(f"[DATA-INTEGRITY: {c['conflict_id']} references deleted gap {gid}]")
            elif "CLOSED" in (gap["status"] or ""):
                warnings.append(f"[DATA-INTEGRITY: {c['conflict_id']} references closed gap {gid} — review]")
    return warnings


def build_brief(item_code, item, run, gaps, conflicts, connections, deferred,
                integrity_warnings, session):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

    item_name = item["name"] if item else item_code
    run_id    = run["run_id"] if run else "N/A"
    steps_c   = json.loads(run["steps_complete"])  if run else []
    steps_s   = json.loads(run["steps_started"])   if run else []
    incomplete = list(set(steps_s) - set(steps_c))

    # Partition gaps
    research  = [g for g in gaps if g["category"] in RESEARCH_CATS]
    authoring = [g for g in gaps if g["category"] in AUTHORING_CATS]
    infra     = [g for g in gaps if g["category"] in INFRA_CATS]

    # Priority counts
    p_counts = {"P1": 0, "P2": 0, "P3": 0}
    for g in gaps:
        p_counts[g["priority"]] = p_counts.get(g["priority"], 0) + 1

    # Triggers
    fdr_trigger  = any(
        "FDR-TRIGGER" in (g["description"] or "").upper() or
        "FDR trigger" in (g["description"] or "")
        for g in research
    )
    econ_trigger = any(g["category"] == "EC" and g["priority"] in ("P1", "P2") for g in research)

    lines = []
    lines.append(f"# Audit Brief — {item_code}: {item_name}")
    lines.append(f"**Date:** {ts} UTC")
    lines.append(f"**Session:** {session}")
    lines.append(f"**Run ID:** {run_id}")
    lines.append(f"**Pipeline steps complete:** {', '.join(steps_c) if steps_c else 'None'}")
    if incomplete:
        lines.append(f"**Mid-step failures (started, not complete):** {', '.join(sorted(incomplete))}")

    if integrity_warnings:
        lines.append("")
        for w in integrity_warnings:
            lines.append(f"> ⚠️ {w}")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Research Actions
    lines.append("## Research Actions")
    lines.append("")
    if research:
        lines.append("| Gap ID | Category | Priority | Routing skill | Description |")
        lines.append("|---|---|---|---|---|")
        for g in sorted(research, key=lambda x: (x["priority"], x["gap_id"])):
            skill = CATEGORY_SKILL.get(g["category"], "—")
            desc  = (g["description"] or "")[:120].replace("|", "·")
            lines.append(f"| {g['gap_id']} | {g['category']} | {g['priority']} | {skill} | {desc} |")
    else:
        lines.append("*(No research actions)*")

    lines.append("")
    lines.append("## Authoring Corrections")
    lines.append("")
    if authoring:
        lines.append("| Gap ID | Category | Priority | Routing skill | Description |")
        lines.append("|---|---|---|---|---|")
        for g in sorted(authoring, key=lambda x: (x["priority"], x["gap_id"])):
            skill = CATEGORY_SKILL.get(g["category"], "—")
            desc  = (g["description"] or "")[:120].replace("|", "·")
            lines.append(f"| {g['gap_id']} | {g['category']} | {g['priority']} | {skill} | {desc} |")
    else:
        lines.append("*(No authoring corrections)*")

    if infra:
        lines.append("")
        lines.append("## Infrastructure")
        lines.append("")
        lines.append("| Gap ID | Category | Priority | Routing skill | Description |")
        lines.append("|---|---|---|---|---|")
        for g in sorted(infra, key=lambda x: x["gap_id"]):
            skill = CATEGORY_SKILL.get(g["category"], "—")
            desc  = (g["description"] or "")[:120].replace("|", "·")
            lines.append(f"| {g['gap_id']} | {g['category']} | {g['priority']} | {skill} | {desc} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Conflicts
    lines.append("## Active Conflicts")
    lines.append("")
    resolved_c   = [c for c in conflicts if c["status"] not in ("UNRESOLVED", "MODE-S-ONLY")]
    unresolved_c = [c for c in conflicts if c["status"] in ("UNRESOLVED", "MODE-S-ONLY")]
    if conflicts:
        lines.append("| Conflict ID | Domain | Pop A | Pop B | Status | Gap ID |")
        lines.append("|---|---|---|---|---|---|")
        for c in sorted(conflicts, key=lambda x: x["conflict_id"]):
            lines.append(
                f"| {c['conflict_id']} | {c['domain']} | {c['pop_a']} | {c['pop_b']} "
                f"| {c['status']} | {c['gap_id'] or '—'} |"
            )
    else:
        lines.append("*(No conflicts logged for this item)*")

    lines.append("")
    lines.append("## Pending Connections")
    lines.append("")
    if connections:
        lines.append("| CON-ID | Confidence | Type | Description |")
        lines.append("|---|---|---|---|")
        for c in connections:
            desc = (c["description"] or "")[:100].replace("|", "·")
            lines.append(f"| {c['con_id']} | {c['confidence']} | {c['connection_type'] or '—'} | {desc} |")
    else:
        lines.append("*(No pending connections)*")

    lines.append("")
    lines.append("## Deferred Citations")
    lines.append("")
    if deferred:
        lines.append("| Source slug | Local ref | Deferred reason | Session |")
        lines.append("|---|---|---|---|")
        for d in deferred:
            lines.append(f"| {d['slug']} | {d['local_ref_id']} | {d['deferred_reason']} | {d['created_by_session']} |")
    else:
        lines.append("*(No deferred citations)*")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"**Gaps logged:** {len(gaps)} total (P1: {p_counts.get('P1',0)} · P2: {p_counts.get('P2',0)} · P3: {p_counts.get('P3',0)})")
    lines.append(f"**Research actions:** {len(research)}")
    lines.append(f"**Authoring corrections:** {len(authoring)}")
    lines.append(f"**Infrastructure:** {len(infra)}")
    lines.append(f"**Conflicts:** {len(conflicts)} (resolved: {len(resolved_c)} · unresolved: {len(unresolved_c)})")
    lines.append(f"**Pending connections:** {len(connections)}")
    lines.append(f"**Deferred citations:** {len(deferred)}")
    lines.append(f"**Economics-researcher trigger:** {'YES (P2 EC gap present)' if econ_trigger else 'NO'}")
    lines.append(f"**FDR trigger:** {'YES (RP gap with FDR-TRIGGER scenario)' if fdr_trigger else 'NO'}")

    return "\n".join(lines)


def run(item_code, session, dry_run=False):
    if not DB_PATH.exists():
        print(f"ERROR: DB not found at {DB_PATH}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    gaps, conflicts, connections, deferred, item, run_rec = load_data(conn, item_code)
    integrity_warnings = check_integrity(conn, conflicts)

    brief = build_brief(
        item_code, item, run_rec, gaps, conflicts, connections,
        deferred, integrity_warnings, session
    )

    brief_dir  = REPO_ROOT / "references" / "audit-briefs"
    brief_path = brief_dir / f"{item_code}_brief.md"

    if not dry_run:
        brief_dir.mkdir(parents=True, exist_ok=True)
        brief_path.write_text(brief, encoding="utf-8")
        print(f"Brief written: {brief_path}")

        # Update audit run record
        if run_rec:
            conn.execute("""
                UPDATE item_audit_runs
                SET status='COMPLETE', brief_path=?, updated_at=?, updated_by_session=?
                WHERE run_id=?
            """, (
                f"references/audit-briefs/{item_code}_brief.md",
                datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
                session,
                run_rec["run_id"],
            ))
            conn.commit()
            print(f"item_audit_runs updated: {run_rec['run_id']} → COMPLETE")
    else:
        print("[DRY-RUN] Brief would be written to:", brief_path)
        print("[DRY-RUN] item_audit_runs would be updated to COMPLETE")
        print()
        print(brief[:500] + "...(truncated for dry-run)")

    conn.close()
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit consolidator for item audit pipeline")
    parser.add_argument("--item", required=True, help="Item code (e.g. I-01)")
    parser.add_argument("--session", required=True, help="Session name")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    sys.exit(run(args.item, args.session, args.dry_run))
