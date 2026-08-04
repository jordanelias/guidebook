#!/usr/bin/env python3
"""
scripts/generate/build_site.py — build the spec pages, and prove they match the DB.

SCOPE, STATED PLAINLY: this drives `site/specs/` only. `site/populations/` (11
files) and `site/rooms/` (17 files) have generators — population_page.py and
room_page.py — that it does NOT drive; room_page.py additionally crashes
against the live schema (no `rooms` table). Naming this "build every page"
would be false for 28 of ~121 files.

The per-page generators (spec_page.py, population_page.py, room_page.py) each
render ONE page from argv and have never had a driver. The 87 files under
site/specs/ were produced by an ad-hoc loop at some point and have not been
regenerated since; six items added later have no page at all, including A-18,
which holds one of only two `primary` item_bpc_links. This is that driver.

SCOPE, AND WHAT THIS DELIBERATELY IS NOT
An earlier version of this driver also wrote a `render_manifest` table
recording each build event. That table was dropped by migration 046: the owner
has stated the target architecture is dynamic rendering on the site, and under
dynamic rendering there is no per-page build event to record. Static per-page
HTML continues to be generated as an explicit stopgap, not as the destination.

So this driver stays deliberately thin. It answers "is this page stale?" by
comparing the file on disk against a fresh render — which needs no stored
state, and keeps working unchanged when the static stopgap is retired.

DETERMINISM IS THE CONTRACT
Per the owner directive of 2026-08-04, the site must not depend on an expiring
CI artifact. What makes the output trustworthy is that the same DB and the same
generators reproduce it exactly, so this driver iterates in a stable order
(item_code) and never depends on set or dict ordering.

USAGE
  python3 scripts/generate/build_site.py                  # build everything
  python3 scripts/generate/build_site.py --only E-08      # one item
  python3 scripts/generate/build_site.py --dry-run        # render, write nothing
  python3 scripts/generate/build_site.py --check          # fail if any page is stale

--check is the piece with value beyond the build: it detects hand-edited
generated output, which CLAUDE.md forbids and nothing currently catches.

Exit codes: 0 success; 1 a generator failed, or --check found staleness.
"""

import argparse
import hashlib
import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts" / "generate"))

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO_ROOT / "data" / "guidebook.db"))
SITE_DIR = REPO_ROOT / "site"

# Same shape as scripts/generate_parts.py:83 so the two derived surfaces agree
# on what "the DB state" means. Its known weakness, restated rather than
# inherited quietly: this hashes COUNTS, so it cannot see an UPDATE — the same
# blindness that lets the blocking migration_reproducibility gate pass while
# enrichment columns diverge. It is a cheap label for a build, not evidence
# that two builds are equivalent. The sha256 of the output is that.
FP_TABLES = (
    "items", "populations", "evidence_cell_state", "cell_source_links",
    "evidence_sources", "item_bpc_links", "item_population_links",
)


def fingerprint(conn):
    parts = []
    for t in FP_TABLES:
        try:
            n = conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        except sqlite3.Error:
            n = "NA"
        parts.append(f"{t}={n}")
    uv = conn.execute("PRAGMA user_version").fetchone()[0]
    parts.append(f"user_version={uv}")
    blob = ";".join(parts)
    return hashlib.sha256(blob.encode()).hexdigest()[:12]


def governing_refs(conn, item_code):
    """The sources this item's cells rest on — reported, not stored.

    Used only to tell the operator how many pages actually show evidence. The
    durable answer to "what justifies this page?" belongs in the provenance
    views over cell_source_links, which work identically under static or
    dynamic rendering.
    """
    # role='governing' matches spec_page.py's own filter. Without it the two
    # definitions agree only while 'governing' is the sole role in the table,
    # and diverge silently the day a second one exists.
    return [r[0] for r in conn.execute(
        "SELECT DISTINCT csl.ref_id FROM cell_source_links csl "
        "JOIN evidence_cell_state ecs USING (cell_id) "
        "WHERE ecs.item_code = ? AND csl.role = 'governing' "
        "ORDER BY csl.ref_id", (item_code,))]


def orphan_pages(conn):
    """Files in site/specs/ with no matching row in `items`.

    A page whose item was deleted keeps serving a specification the project no
    longer holds. Nothing else looks for these, and re-rendering cannot find
    them: the build walks `items`, so a file with no item is never visited.
    """
    live = {r[0].lower() for r in conn.execute("SELECT item_code FROM items")}
    specs = SITE_DIR / "specs"
    if not specs.is_dir():
        return []
    return sorted(
        str(p.relative_to(REPO_ROOT))
        for p in specs.glob("*.html") if p.stem.lower() not in live
    )


def build_specs(conn, only=None, dry_run=False, want_refs=True):
    import spec_page  # noqa: E402  (path injected above)

    fp = fingerprint(conn)
    items = [r[0] for r in conn.execute(
        "SELECT item_code FROM items ORDER BY item_code")]
    if only:
        items = [i for i in items if i == only]
        if not items:
            print(f"ERROR: item '{only}' not found in items.", file=sys.stderr)
            return None

    rows, failures = [], []
    for item_code in items:
        out_path = SITE_DIR / "specs" / f"{item_code.lower()}.html"
        try:
            item = spec_page.query_item(conn, item_code)
            if not item:
                failures.append((item_code, "not found by query_item"))
                continue
            html = spec_page.render_html(item)
        except Exception as e:  # a generator crash must fail the build, not be skipped
            failures.append((item_code, f"{type(e).__name__}: {e}"))
            continue

        if not dry_run:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(html, encoding="utf-8")

        rows.append({
            "page_path": str(out_path.relative_to(REPO_ROOT)),
            "item_code": item_code,
            "db_fingerprint": fp,
            "output_sha256": hashlib.sha256(html.encode("utf-8")).hexdigest(),
            "governing_refs": governing_refs(conn, item_code) if want_refs else [],
        })

    if failures:
        for code, why in failures:
            print(f"ERROR: {code}: {why}", file=sys.stderr)
        return None
    return rows


def check_stale(rows):
    """Compare what is on disk against what the generators now produce.

    Catches two things: generated output that has drifted from its source
    (nobody regenerated after a DB change), and generated output that was
    hand-edited, which CLAUDE.md forbids and nothing currently detects.
    """
    stale = []
    for r in rows:
        disk = REPO_ROOT / r["page_path"]
        if disk.exists():
            got = hashlib.sha256(disk.read_bytes()).hexdigest()
            if got != r["output_sha256"]:
                stale.append((r["page_path"], "file on disk differs from fresh render"))
        else:
            stale.append((r["page_path"], "file missing on disk"))
    return stale


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="build a single item_code")
    ap.add_argument("--dry-run", action="store_true",
                    help="render and report, write no files")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any page differs from a fresh render")
    args = ap.parse_args()

    # Read-only: this process renders and compares, it never writes the DB.
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)

    rows = build_specs(conn, only=args.only,
                       dry_run=args.dry_run or args.check,
                       want_refs=not args.check)
    if rows is None:
        conn.close()
        sys.exit(1)

    if args.check:
        stale = check_stale(rows)
        if not args.only:
            stale += [(p, "orphan: no such item in `items`") for p in orphan_pages(conn)]
        conn.close()
        if stale:
            for path, why in stale:
                print(f"STALE: {path} — {why}", file=sys.stderr)
            print(f"\n{len(stale)} staleness finding(s). "
                  f"Run: python3 scripts/generate/build_site.py", file=sys.stderr)
            sys.exit(1)
        print(f"FRESH: {len(rows)} page(s) match a fresh render.")
        return

    if args.dry_run:
        print(f"DRY RUN: {len(rows)} page(s) would be written; nothing changed on disk.")
        conn.close()
        return

    fp = rows[0]["db_fingerprint"] if rows else "-"
    cited = sum(1 for r in rows if r["governing_refs"])
    conn.close()
    print(f"Built {len(rows)} page(s) at DB fingerprint {fp}.")
    print(f"Pages citing at least one governing source: {cited} of {len(rows)}.")


if __name__ == "__main__":
    main()
