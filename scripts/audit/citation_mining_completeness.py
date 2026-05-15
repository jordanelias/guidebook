#!/usr/bin/env python3
"""
scripts/audit/citation_mining_completeness.py

Audit citation_mining completeness. Surfaces the GAP-283 protocol-violation pattern:
research sessions adding Tier 1-2 evidence_sources rows without corresponding
citation_mining rows (per standards RULE 124, mandatory mining for confirmed Tier 1-2;
per skill citation-miner §0 and research-log-manager LOG step 6+7).

Usage:
    python3 scripts/audit/citation_mining_completeness.py
        Audit all Tier 1-2 sources in the DB. Report any without a citation_mining row.

    python3 scripts/audit/citation_mining_completeness.py --session SESSION_FILENAME
        Scope to sources added in the named session. Returns nonzero exit code if any
        Tier 1-2 source from that session lacks a citation_mining row. Intended as a
        session-close blocker.

    python3 scripts/audit/citation_mining_completeness.py --tier-max 3
        Include Tier 3 in the audit (default is 1-2 only — Tier 3 is not mandatory
        per RULE 124, but partial-coverage tracking can be useful).

    python3 scripts/audit/citation_mining_completeness.py --json
        Machine-readable output (for hook integration when hooks/ ships).

Exit codes:
    0 — clean (no outstanding sources, or warnings only)
    1 — outstanding sources found (use as session-close blocker)
    2 — DB error / unable to read

Author: written 2026-05-11 in session_2026-05-11g-citation-mining.md per GAP-283 P1.
"""
import argparse
import json
import os
import sqlite3
import sys

DEFAULT_DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")

def audit(db_path, session=None, tier_max=2, output_json=False):
    if not os.path.exists(db_path):
        print(f"ERROR: DB not found at {db_path}", file=sys.stderr)
        return 2, None

    try:
        con = sqlite3.connect(db_path)
        con.row_factory = sqlite3.Row
    except Exception as e:
        print(f"ERROR: cannot open DB: {e}", file=sys.stderr)
        return 2, None

    # Outstanding = Tier 1..tier_max source in evidence_sources, linked to some slug,
    # with no citation_mining row referencing its ref_id, and (if --session given)
    # was added in that session.
    where_session = "AND es.created_by_session = :session" if session else ""
    rows = con.execute(f"""
        SELECT DISTINCT es.ref_id, es.tier, es.author_display AS authors, es.pub_year AS year, es.pub_title AS title, es.doi,
                        es.created_by_session, es.verification_status,
                        GROUP_CONCAT(DISTINCT ssl.slug) as slugs
        FROM evidence_sources es
        JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
        LEFT JOIN citation_mining cm ON cm.global_ref_id = es.ref_id
        WHERE es.tier BETWEEN 1 AND :tier_max
          AND cm.global_ref_id IS NULL
          {where_session}
        GROUP BY es.ref_id
        ORDER BY es.tier, es.ref_id
    """, {"session": session, "tier_max": tier_max}).fetchall()

    # Also report rows where cm exists but both backward=0 AND forward=0 AND no deferred_reason
    bad_cm = con.execute(f"""
        SELECT cm.global_ref_id, cm.slug, cm.local_ref_id, cm.backward, cm.forward,
               cm.deferred_reason, es.tier, es.author_display AS authors, es.pub_year AS year, es.created_by_session
        FROM citation_mining cm
        JOIN evidence_sources es ON cm.global_ref_id = es.ref_id
        WHERE es.tier BETWEEN 1 AND :tier_max
          AND cm.backward = 0 AND cm.forward = 0
          AND (cm.deferred_reason IS NULL OR cm.deferred_reason = '')
          {("AND es.created_by_session = :session" if session else "").replace("es.", "cm.created_by_session = :session OR es.")}
        ORDER BY cm.global_ref_id
    """, {"session": session, "tier_max": tier_max}).fetchall() if False else []
    # ^ disabled the convoluted query — keep simple, do it in Python below

    # Simpler: scan cm rows where both directions are 0 and no defer reason
    bad_cm = []
    for cm in con.execute("""
        SELECT cm.global_ref_id, cm.slug, cm.local_ref_id, cm.backward, cm.forward,
               cm.deferred_reason, es.tier, es.author_display AS authors, es.pub_year AS year,
               es.created_by_session as es_session, cm.created_by_session as cm_session
        FROM citation_mining cm
        JOIN evidence_sources es ON cm.global_ref_id = es.ref_id
        WHERE es.tier BETWEEN 1 AND ?
          AND cm.backward = 0 AND cm.forward = 0
          AND (cm.deferred_reason IS NULL OR cm.deferred_reason = '')
    """, (tier_max,)).fetchall():
        if session and (cm["es_session"] != session and cm["cm_session"] != session):
            continue
        bad_cm.append(dict(cm))

    # Stats
    total_t12 = con.execute(
        "SELECT COUNT(*) FROM evidence_sources WHERE tier BETWEEN 1 AND ?",
        (tier_max,)
    ).fetchone()[0]
    total_with_cm = con.execute("""
        SELECT COUNT(DISTINCT es.ref_id) FROM evidence_sources es
        JOIN citation_mining cm ON cm.global_ref_id = es.ref_id
        WHERE es.tier BETWEEN 1 AND ?
    """, (tier_max,)).fetchone()[0]
    coverage_pct = (total_with_cm / total_t12 * 100) if total_t12 else 0.0

    result = {
        "db_path": db_path,
        "session_scope": session,
        "tier_max": tier_max,
        "total_tier_in_scope": total_t12,
        "total_with_citation_mining": total_with_cm,
        "coverage_pct": round(coverage_pct, 1),
        "outstanding_count": len(rows),
        "outstanding": [dict(r) for r in rows],
        "stub_cm_rows": bad_cm,  # rows that exist but say nothing happened — also a violation
        "stub_cm_count": len(bad_cm),
    }

    if output_json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"=== Citation-mining completeness audit ===")
        print(f"  DB: {db_path}")
        print(f"  Session scope: {session or '(all)'}")
        print(f"  Tier scope: 1..{tier_max}")
        print(f"  Total in scope: {total_t12}")
        print(f"  Total with citation_mining row: {total_with_cm} ({coverage_pct:.1f}%)")
        print(f"  Outstanding (no citation_mining row): {len(rows)}")
        if rows:
            print()
            print(f"  {'REF-ID':12} {'T':2} {'SESS':40} {'STATUS':12} {'AUTHORS':30} {'YEAR':6}")
            for r in rows:
                sess = (r["created_by_session"] or "(unknown)")[:38]
                auth = (r["authors"] or "(unknown)")[:28]
                yr = r["year"] or "?"
                vs = r["verification_status"] or "(null)"
                print(f"  {r['ref_id']:12} T{r['tier']} {sess:40} {vs:12} {auth:30} {yr:6}")
        if bad_cm:
            print(f"\n  Stub citation_mining rows (both directions=0, no deferred_reason): {len(bad_cm)}")
            for r in bad_cm:
                print(f"    {r['global_ref_id']} ({r['slug']}/{r['local_ref_id']}) — protocol violation")
        if rows or bad_cm:
            print()
            print(f"  PROTOCOL VIOLATION per GAP-283. RULE 124 mandates mining for confirmed Tier 1-2 sources.")
            print(f"  Remediate: invoke citation-miner skill INLINE for each REF-ID above, OR")
            print(f"  write a citation_mining row with deferred_reason set if mining is legitimately blocked.")

    # Exit code: 1 if any outstanding, 0 if clean
    exit_code = 1 if (rows or bad_cm) else 0
    return exit_code, result

def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument("--db", default=DEFAULT_DB, help=f"DB path (default: {DEFAULT_DB})")
    p.add_argument("--session", default=None, help="Scope to a session filename")
    p.add_argument("--tier-max", type=int, default=2, choices=[1, 2, 3],
                   help="Maximum tier to include (default 2 = mandatory only)")
    p.add_argument("--json", action="store_true", dest="output_json", help="JSON output")
    args = p.parse_args()

    code, _ = audit(args.db, session=args.session, tier_max=args.tier_max, output_json=args.output_json)
    sys.exit(code)

if __name__ == "__main__":
    main()
