#!/usr/bin/env python3
"""
scripts/audit/source_slug_links_duplicates.py

Audit source_slug_links for duplicate (slug, local_ref_id) pairs.

Per GAP-285, source_slug_links lacks a UNIQUE(slug, local_ref_id) constraint, and
duplicates have accumulated:
  - accessibility-feature-market-value-uplift-framing: all 19 local_ref_ids (01-19) duplicated
  - school-environment-autism: SEA-01 maps to multiple ref_ids
  - others: per audit output

This script categorises each duplicate set so the owner can decide per-set whether
the duplicate is:
  (a) a true duplicate evidence_sources row (merge ref_ids), or
  (b) distinct sources that accidentally collided on local_ref_id (renumber)

Output sections:
  1. Per-slug duplicate (slug, local_ref_id) sets
  2. Heuristic classification (looks at evidence_sources fields per ref_id in the set)
  3. Cleanup recommendation per set

Usage:
    python3 scripts/audit/source_slug_links_duplicates.py
    python3 scripts/audit/source_slug_links_duplicates.py --slug some-slug
    python3 scripts/audit/source_slug_links_duplicates.py --json

Author: written 2026-05-11 in session_2026-05-11g-citation-mining.md per GAP-285 P2.
"""
import argparse, json, os, sqlite3, sys
from collections import defaultdict

DEFAULT_DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")

def audit(db_path, slug_filter=None, output_json=False):
    if not os.path.exists(db_path):
        print(f"ERROR: DB not found at {db_path}", file=sys.stderr)
        return 2

    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row

    where = "WHERE slug = ?" if slug_filter else ""
    params = (slug_filter,) if slug_filter else ()

    dup_sets = con.execute(f"""
        SELECT slug, local_ref_id, COUNT(*) as n
        FROM source_slug_links
        {where}
        GROUP BY slug, local_ref_id
        HAVING COUNT(*) > 1
        ORDER BY n DESC, slug, local_ref_id
    """, params).fetchall()

    results = []
    for ds in dup_sets:
        members = con.execute("""
            SELECT ssl.ref_id, ssl.local_ref_id, ssl.created_at, ssl.created_by_session,
                   es.tier, es.verification_status, es.authors, es.year, es.title, es.doi
            FROM source_slug_links ssl
            LEFT JOIN evidence_sources es ON ssl.ref_id = es.ref_id
            WHERE ssl.slug = ? AND ssl.local_ref_id = ?
            ORDER BY ssl.created_at
        """, (ds["slug"], ds["local_ref_id"])).fetchall()

        # Heuristic classification
        unique_authors = set((m["authors"] or "").lower().strip()[:40] for m in members)
        unique_years = set(m["year"] for m in members if m["year"])
        unique_dois = set(m["doi"] for m in members if m["doi"])

        if len(unique_dois) > 1:
            classification = "DISTINCT-SOURCES (different DOIs) — RENUMBER local_ref_id"
        elif len(unique_authors) > 1 and len(unique_years) > 1:
            classification = "LIKELY-DISTINCT (different authors and years) — RENUMBER local_ref_id"
        elif len(unique_authors) == 1 and len(unique_years) <= 1:
            classification = "LIKELY-DUPLICATE (same authors and year) — MERGE ref_ids"
        else:
            classification = "AMBIGUOUS — manual review"

        results.append({
            "slug": ds["slug"],
            "local_ref_id": ds["local_ref_id"],
            "count": ds["n"],
            "classification": classification,
            "members": [dict(m) for m in members],
        })

    # Summary stats
    total_duplicates = sum(r["count"] - 1 for r in results)  # excess rows
    by_slug = defaultdict(int)
    for r in results:
        by_slug[r["slug"]] += r["count"] - 1

    if output_json:
        print(json.dumps({
            "db_path": db_path,
            "total_duplicate_sets": len(results),
            "total_excess_rows": total_duplicates,
            "duplicates_by_slug": dict(by_slug),
            "results": results,
        }, indent=2, default=str))
    else:
        print(f"=== source_slug_links duplicate audit ===")
        print(f"  DB: {db_path}")
        print(f"  Slug filter: {slug_filter or '(all)'}")
        print(f"  Total duplicate (slug, local_ref_id) sets: {len(results)}")
        print(f"  Total excess rows: {total_duplicates}")
        print()
        if by_slug:
            print(f"  Duplicates by slug:")
            for s, n in sorted(by_slug.items(), key=lambda x: -x[1]):
                print(f"    {s}: {n} excess rows")
            print()

        for r in results[:20]:  # cap output
            print(f"  {r['slug']} / {r['local_ref_id']}  (n={r['count']})")
            print(f"    classification: {r['classification']}")
            for m in r["members"]:
                t = f"T{m['tier']}" if m['tier'] else "T?"
                vs = m["verification_status"] or "(null)"
                auth = (m["authors"] or "(unknown)")[:30]
                yr = m["year"] or "?"
                doi = m["doi"] or "-"
                print(f"      {m['ref_id']}  {t}  {vs:12}  {auth}  ({yr})  doi={doi[:40]}")
            print()
        if len(results) > 20:
            print(f"  ... and {len(results) - 20} more (use --json for full list)")

        if total_duplicates:
            print()
            print(f"  Per GAP-285: UNIQUE(slug, local_ref_id) constraint cannot be applied until")
            print(f"  these duplicates are resolved per-set.")

    return 0 if total_duplicates == 0 else 1

def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument("--db", default=DEFAULT_DB)
    p.add_argument("--slug", help="Scope to a single slug")
    p.add_argument("--json", action="store_true", dest="output_json")
    args = p.parse_args()
    sys.exit(audit(args.db, slug_filter=args.slug, output_json=args.output_json))

if __name__ == "__main__":
    main()
