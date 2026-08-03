#!/usr/bin/env python3
"""Audit evidence metadata against PI v10.8 standing rule #10.

Standing rule #10 (evidence verification gate):
  No BPC synthesis claim may cite a source with metadata_quality = AUTHOR-TITLE-ONLY
  or verification_status = NULL. Required minimum: metadata_quality IN (COMPLETE, COMPLETE-STATUTORY) per DR-2026-05-18
  AND verification_status IN ('VERIFIED', 'UNVERIFIED-1').

This script enforces that gate by reporting:
  1. Overall evidence-base health (cross-tab of metadata_quality × verification_status)
  2. Per-BPC eligibility for Phase E (counts of eligible vs ineligible sources)
  3. BPCs ready to begin Phase E synthesis (have ≥N eligible sources per tier)
  4. BPCs blocked, with specifically what blocks them
  5. High-impact source rehabilitations (sources cited by many BPCs)

Usage:
  python scripts/audit_evidence_metadata.py                # full report
  python scripts/audit_evidence_metadata.py --slug X       # one BPC
  python scripts/audit_evidence_metadata.py --ready        # only ready-for-Phase-E
  python scripts/audit_evidence_metadata.py --blocked      # only blocked BPCs
  python scripts/audit_evidence_metadata.py --json         # machine-readable
  python scripts/audit_evidence_metadata.py --strict       # exit 1 if no BPCs ready

Eligibility thresholds (configurable via --min-eligible / --min-tiers):
  --min-eligible: minimum eligible-source count to consider a BPC ready (default 3)
  --min-tiers:    minimum number of tier categories represented (default 2)

Exit codes:
  0 — audit ran cleanly
  1 — --strict was set and no BPCs are ready
  2 — invocation error
"""

import argparse
import json
import os
import sqlite3
import sys
from collections import defaultdict, Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = os.environ.get("GUIDEBOOK_DB_PATH", str(REPO_ROOT / "data" / "guidebook.db"))

# Rule #10 eligibility — required minimum for a source to be cited in synthesis
ELIGIBLE_METADATA = {"COMPLETE", "COMPLETE-STATUTORY"}
ELIGIBLE_VERIFICATION = {"VERIFIED", "UNVERIFIED-1"}
EXCLUDED_VERIFICATION = {"UNVERIFIED-CLOSED", "CLOSED-DELETED"}


def is_eligible(metadata_quality: str | None, verification_status: str | None) -> bool:
    """Implement the standing rule #10 eligibility test."""
    return (
        metadata_quality in ELIGIBLE_METADATA
        and verification_status in ELIGIBLE_VERIFICATION
    )


def is_excluded(verification_status: str | None) -> bool:
    """Sources explicitly excluded from any synthesis citation."""
    return verification_status in EXCLUDED_VERIFICATION


# ── Audit pieces ────────────────────────────────────────────────────────────

def overall_health(conn) -> dict:
    """Cross-tab of metadata_quality × verification_status."""
    rows = conn.execute("""
        SELECT COALESCE(metadata_quality, 'NULL') as mq,
               COALESCE(verification_status, 'NULL') as vs,
               COUNT(*) as n
        FROM evidence_sources
        GROUP BY metadata_quality, verification_status
        ORDER BY n DESC
    """).fetchall()

    total = conn.execute("SELECT COUNT(*) FROM evidence_sources").fetchone()[0]
    eligible = conn.execute(f"""
        SELECT COUNT(*) FROM evidence_sources
        WHERE metadata_quality IN ({','.join(['?'] * len(ELIGIBLE_METADATA))})
        AND verification_status IN ({','.join(['?'] * len(ELIGIBLE_VERIFICATION))})
    """, (*ELIGIBLE_METADATA, *ELIGIBLE_VERIFICATION)).fetchone()[0]
    excluded = conn.execute(f"""
        SELECT COUNT(*) FROM evidence_sources
        WHERE verification_status IN ({','.join(['?'] * len(EXCLUDED_VERIFICATION))})
    """, tuple(EXCLUDED_VERIFICATION)).fetchone()[0]

    return {
        "total_sources": total,
        "eligible_for_synthesis": eligible,
        "excluded_from_synthesis": excluded,
        "ineligible_pending_rehab": total - eligible - excluded,
        "eligible_pct": round(100 * eligible / total, 1) if total else 0,
        "cross_tab": [dict(r) for r in rows],
    }


def per_slug_eligibility(conn, min_eligible: int, min_tiers: int) -> list:
    """For each slug, count eligible vs ineligible sources, broken out by tier."""
    rows = conn.execute("""
        SELECT s.slug,
               COUNT(DISTINCT sl.ref_id) as total_sources,
               COUNT(DISTINCT CASE
                 WHEN es.metadata_quality IN ('COMPLETE','COMPLETE-STATUTORY')
                 AND es.verification_status IN ('VERIFIED', 'UNVERIFIED-1')
                 THEN sl.ref_id END) as eligible_sources,
               COUNT(DISTINCT CASE
                 WHEN es.verification_status IN ('UNVERIFIED-CLOSED', 'CLOSED-DELETED')
                 THEN sl.ref_id END) as excluded_sources
        FROM slugs s
        LEFT JOIN source_slug_links sl ON s.slug = sl.slug
        LEFT JOIN evidence_sources es ON sl.ref_id = es.ref_id
        GROUP BY s.slug
    """).fetchall()

    slug_data = []
    for r in rows:
        slug = r["slug"]
        if r["total_sources"] == 0:
            slug_data.append({
                "slug": slug, "total_sources": 0, "eligible_sources": 0,
                "excluded_sources": 0, "tiers_with_eligible": [],
                "ready": False, "reason": "no linked sources",
            })
            continue

        # Tier breakdown of eligible sources for this slug
        tier_rows = conn.execute("""
            SELECT es.tier, COUNT(DISTINCT sl.ref_id) as n
            FROM source_slug_links sl
            JOIN evidence_sources es ON sl.ref_id = es.ref_id
            WHERE sl.slug = ?
            AND es.metadata_quality IN ('COMPLETE','COMPLETE-STATUTORY')
            AND es.verification_status IN ('VERIFIED', 'UNVERIFIED-1')
            GROUP BY es.tier
        """, (slug,)).fetchall()
        tiers_with_eligible = sorted([
            tr["tier"] for tr in tier_rows
            if tr["tier"] is not None and tr["n"] > 0
        ])

        ready = (
            r["eligible_sources"] >= min_eligible
            and len(tiers_with_eligible) >= min_tiers
        )
        reason = None
        if not ready:
            if r["eligible_sources"] < min_eligible:
                reason = (
                    f"only {r['eligible_sources']} eligible source"
                    f"{'s' if r['eligible_sources'] != 1 else ''} "
                    f"(need ≥{min_eligible})"
                )
            elif len(tiers_with_eligible) < min_tiers:
                reason = (
                    f"only {len(tiers_with_eligible)} tier"
                    f"{'s' if len(tiers_with_eligible) != 1 else ''} represented "
                    f"in eligible set (need ≥{min_tiers})"
                )

        slug_data.append({
            "slug": slug,
            "total_sources": r["total_sources"],
            "eligible_sources": r["eligible_sources"],
            "excluded_sources": r["excluded_sources"],
            "tiers_with_eligible": tiers_with_eligible,
            "ready": ready,
            "reason": reason,
        })

    return slug_data


def quick_wins(conn, top_n: int = 20) -> dict:
    """Sources that, if rehabilitated, would unblock the most BPCs.

    Two categories:
      - COMPLETE-but-unverified: just need verification (fastest unblock)
      - VERIFIED-but-incomplete-metadata: need metadata completion (DOI/CrossRef etc.)
    """
    complete_but_unverified = conn.execute("""
        SELECT es.ref_id, es.first_author_last, es.pub_year, es.pub_title,
               COUNT(DISTINCT sl.slug) as bpc_uses
        FROM evidence_sources es
        LEFT JOIN source_slug_links sl ON es.ref_id = sl.ref_id
        WHERE es.metadata_quality IN ('COMPLETE','COMPLETE-STATUTORY')
        AND (es.verification_status IS NULL OR es.verification_status NOT IN ('VERIFIED', 'UNVERIFIED-1', 'UNVERIFIED-CLOSED', 'CLOSED-DELETED'))
        GROUP BY es.ref_id
        ORDER BY bpc_uses DESC, es.ref_id
        LIMIT ?
    """, (top_n,)).fetchall()

    verified_but_thin = conn.execute("""
        SELECT es.ref_id, es.first_author_last, es.pub_year, es.pub_title,
               es.metadata_quality, COUNT(DISTINCT sl.slug) as bpc_uses
        FROM evidence_sources es
        LEFT JOIN source_slug_links sl ON es.ref_id = sl.ref_id
        WHERE es.verification_status IN ('VERIFIED', 'UNVERIFIED-1')
        AND (es.metadata_quality NOT IN ('COMPLETE','COMPLETE-STATUTORY') OR es.metadata_quality IS NULL)
        GROUP BY es.ref_id
        ORDER BY bpc_uses DESC, es.ref_id
        LIMIT ?
    """, (top_n,)).fetchall()

    return {
        "complete_but_unverified": [dict(r) for r in complete_but_unverified],
        "verified_but_thin": [dict(r) for r in verified_but_thin],
    }


def render_report(health: dict, slugs: list, qw: dict, args) -> None:
    """Human-readable text report."""
    print("=" * 76)
    print("EVIDENCE METADATA AUDIT — PI v10.8 standing rule #10")
    print("=" * 76)
    print(f"DB: {DB_PATH}")
    print()

    # Overall health
    print("OVERALL EVIDENCE-BASE HEALTH")
    print("-" * 76)
    print(f"  Total sources:                 {health['total_sources']}")
    print(f"  Eligible for synthesis:        {health['eligible_for_synthesis']} "
          f"({health['eligible_pct']}%)")
    print(f"  Excluded from synthesis:       {health['excluded_from_synthesis']}")
    print(f"  Pending rehabilitation:        {health['ineligible_pending_rehab']}")
    print()
    print("  Distribution (metadata_quality × verification_status):")
    for r in health["cross_tab"][:8]:
        print(f"    {r['mq']:<22} × {r['vs']:<22} {r['n']:>4}")

    # Per-BPC eligibility
    ready = [s for s in slugs if s["ready"]]
    blocked = [s for s in slugs if not s["ready"] and s["total_sources"] > 0]
    empty = [s for s in slugs if s["total_sources"] == 0]

    print()
    print(f"PHASE E READINESS (thresholds: ≥{args.min_eligible} eligible sources, ≥{args.min_tiers} tier categories)")
    print("-" * 76)
    print(f"  Total slugs:                   {len(slugs)}")
    print(f"  READY for Phase E:             {len(ready)}")
    print(f"  BLOCKED (have sources but insufficient eligible): {len(blocked)}")
    print(f"  EMPTY (no linked sources):     {len(empty)}")

    if not args.blocked_only:
        print()
        print("READY BPCs (can begin Phase E now):")
        if not ready:
            print("  (none — every BPC blocked by evidence base)")
        else:
            for s in sorted(ready, key=lambda x: -x["eligible_sources"]):
                tiers = ",".join(str(t) for t in s["tiers_with_eligible"])
                print(f"  {s['slug'][:55]:<55} "
                      f"{s['eligible_sources']:>3}/{s['total_sources']:<3} eligible · tiers [{tiers}]")

    if not args.ready_only:
        print()
        print(f"TOP BLOCKED BPCs (closest to ready — showing top 15):")
        # Order by eligible_sources DESC (closest to threshold), then total_sources DESC
        blocked_sorted = sorted(blocked, key=lambda x: (-x["eligible_sources"], -x["total_sources"]))
        for s in blocked_sorted[:15]:
            tiers = ",".join(str(t) for t in s["tiers_with_eligible"]) or "—"
            print(f"  {s['slug'][:55]:<55} "
                  f"{s['eligible_sources']:>3}/{s['total_sources']:<3} eligible · "
                  f"tiers [{tiers}] · {s['reason']}")

    # Quick wins
    if not (args.ready_only or args.blocked_only):
        print()
        print("HIGH-IMPACT REHABILITATION TARGETS")
        print("-" * 76)
        cbu = qw["complete_but_unverified"]
        if cbu:
            print(f"\n  COMPLETE metadata but unverified ({len(cbu)} shown — fastest unblock):")
            print(f"    These need only a verification pass to become synthesis-eligible.")
            for s in cbu[:10]:
                title = (s['pub_title'] or '')[:50]
                print(f"    {s['ref_id']:<14} {(s['first_author_last'] or '?')[:18]:<18} "
                      f"({s['pub_year']})  used by {s['bpc_uses']} BPC{'s' if s['bpc_uses'] != 1 else ''}")
                print(f"       {title}")
        vbt = qw["verified_but_thin"]
        if vbt:
            print(f"\n  VERIFIED but incomplete metadata ({len(vbt)} shown):")
            print(f"    These need DOI/title/journal completion (Action will help over time).")
            for s in vbt[:10]:
                title = (s['pub_title'] or '')[:50]
                print(f"    {s['ref_id']:<14} {(s['first_author_last'] or '?')[:18]:<18} "
                      f"({s['pub_year']})  used by {s['bpc_uses']} BPC{'s' if s['bpc_uses'] != 1 else ''} · "
                      f"[{s['metadata_quality'] or 'NULL'}]")
                print(f"       {title}")

    print()
    print("=" * 76)
    if not ready:
        print("AUDIT VERDICT: Phase E is blocked everywhere — no BPC has ≥"
              f"{args.min_eligible} eligible sources across ≥{args.min_tiers} tiers.")
        print("  Recommended: Phase B (evidence rehabilitation) must continue before Phase E starts.")
    else:
        print(f"AUDIT VERDICT: {len(ready)} BPC{'s' if len(ready) != 1 else ''} can begin Phase E synthesis.")
    print("=" * 76)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--slug", help="Audit one BPC by slug")
    ap.add_argument("--ready", "--ready-only", action="store_true", dest="ready_only",
                    help="Show only BPCs ready for Phase E")
    ap.add_argument("--blocked", "--blocked-only", action="store_true", dest="blocked_only",
                    help="Show only blocked BPCs")
    ap.add_argument("--min-eligible", type=int, default=3,
                    help="Minimum eligible sources to count a BPC as ready (default 3)")
    ap.add_argument("--min-tiers", type=int, default=2,
                    help="Minimum tier categories represented (default 2)")
    ap.add_argument("--json", action="store_true",
                    help="Machine-readable JSON output")
    ap.add_argument("--strict", action="store_true",
                    help="Exit 1 if no BPCs are ready")
    args = ap.parse_args()

    if not os.path.exists(DB_PATH):
        print(f"ERROR: DB not found at {DB_PATH}", file=sys.stderr)
        return 2

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    health = overall_health(conn)
    slugs = per_slug_eligibility(conn, args.min_eligible, args.min_tiers)
    qw = quick_wins(conn)

    if args.slug:
        match = [s for s in slugs if s["slug"] == args.slug]
        if not match:
            print(f"ERROR: slug '{args.slug}' not found", file=sys.stderr)
            return 2
        slugs = match

    if args.json:
        print(json.dumps({
            "health": health,
            "slugs": slugs,
            "quick_wins": qw,
            "thresholds": {
                "min_eligible": args.min_eligible,
                "min_tiers": args.min_tiers,
            },
        }, indent=2, default=str))
    else:
        render_report(health, slugs, qw, args)

    conn.close()

    if args.strict:
        ready_count = sum(1 for s in slugs if s["ready"])
        if ready_count == 0:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
