#!/usr/bin/env python3
"""
scripts/audit/scan_debt.py — which (source, parameter) pairs nobody has read in full?

WHY THIS EXISTS (tooling T1, 2026-10-09; catalogue-plan-v2 sections 3.8 and 8.2). The
owner's requirement: "Ensure that we can add and expand parameter catalogue as required
based on new information we come across." A parameter promoted in month three is owed a
look in month one's sources, and nothing showed that debt: the catalogue could imply "no
code sets a requirement" where nobody read the code for that quantity, while every gate
read green -- how GAP-061's figures were lost. `v_scan_ledger` (migration 103) derives a
status for every unsuperseded source x active parameter from the extractions and the
reading record (source_scans); this counts the pairs still owed.

DEBT = NOT-READ + READ-PARTIAL pairs. EXTRACTED, STATED-ABSENT and READ-NOTHING-FOUND are
accounted for. READ-PARTIAL is debt because a partial, fragment or abstract reading cannot
say a quantity is absent from the pages it did not see.

NO DEBT BASELINE, deliberately (the "no floor" this check was asked for). Debt RISES
legitimately -- every parameter promoted and every source admitted adds pairs -- so a
ratchet-down baseline would turn red on correct work. It is advisory and red whenever
debt > 0: the honest state of a catalogue that has not been read. Its readers: the next
cohort's worklist (the pairs printed below), the catalogue's evidence-state line, and the
Release 0 acceptance test (plan section 12, Q12), which will scope it to that source set.

EXAMINED is the number of ledger pairs. Zero pairs means no unsuperseded source or no
active parameter -- a corpus clear, which this project has done once (2026-09-13) -- and
the registry floor (min_items: 1) makes that visible rather than a silent pass.

THE RE-READ FLAG, `--reread` (T-031; OD-23, the owner 2026-11-12: "we can still read a source more than once--we
just want to minimize duplicate reads ... We can flag a source to be read again for later parameters"). Derived, never
stored, so it cannot drift from the scans: each owed pair takes the first route that reaches it, in this order --
`inventory` (a clause of the source's inventory, source_clauses, holds a form of the parameter's term: its label or
an alias that names the concept itself, NARROWER and BROADER left out as v_term_names leaves them out; matched by
retrieval_log.normalise_quote, the project's one matching rule), `retained-text` (the file the source's latest full
scan read is on disk and still hashes to its sha256: sweep it), else `reread` (THE FLAG: owed, no clause matches, and
no retained text). A flag is cleared by recording the reading (record-scan --mode targeted, or catalogue). A judgment
that the inventory missed a clause is an open typed gap on the pair, not a second flag. Readers: this mode, and
`db.py cell-status` (evidence, owed, reread_flagged).

Usage:
    python3 scripts/audit/scan_debt.py [--limit N] [--reread]
Exit 0 no debt (with --reread: no pair flagged); 1 debt (a pair flagged); 2 cannot run (no database, or a pre-103
schema).
"""
import argparse
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))
DEBT = ("NOT-READ", "READ-PARTIAL")
# BLOCKED (migration 124): no full reading covers the pair and the source carries a
# processing_blocked_reason the ledger classes as an obstacle to the text (no full text,
# paywalled, language), so the pair is not debt while the obstacle stands. A partial, fragment
# or abstract reading may cover a BLOCKED pair (it does not prove the full text obtainable);
# the ledger row still names it, and it is printed here by scope so "blocked, abstract read" is
# visible and not mistaken for "blocked, nothing read". A full reading outranks the block
# (READ-NOTHING-FOUND). Nothing clears the column: the ledger alone says whether a pair is
# still blocked. A reason the ledger does not class as an obstacle leaves the pair NOT-READ.


def _retained_text(conn, retrieval_log, ref_id):
    """`session/artefact` of the file the source's latest FULL scan read, when it is on disk and still hashes to the
    scan's file_sha256; else None."""
    import hashlib
    scan = conn.execute("SELECT file_sha256 FROM source_scans WHERE ref_id = ? AND text_scope = 'full' "
                        "ORDER BY scan_id DESC LIMIT 1", (ref_id,)).fetchone()
    if scan is None:
        return None
    url = conn.execute("SELECT url FROM evidence_sources WHERE ref_id = ?", (ref_id,)).fetchone()
    for h in retrieval_log.artefacts_for_source(ref_id, url[0] if url else None):
        if ((h["sha256"] or "").lower() == scan[0] and h["exists"]
                and hashlib.sha256(h["path"].read_bytes()).hexdigest() == scan[0]):
            return f"{h['session']}/{h['artefact']}"
    return None


def reread_routes(conn, retrieval_log, parameter_id=None):
    """Every owed pair (DEBT in v_scan_ledger), optionally of one parameter, with the route that reaches it: a dict of
    ref_id, parameter_id, status, route (`inventory`, `retained-text` or `reread`) and what the route reads (`clauses`
    or `file`). The one home of the re-read flag (module docstring); read-only."""
    norm = retrieval_log.normalise_quote
    sql, args = (f"SELECT ref_id, parameter_id, status FROM v_scan_ledger WHERE status IN "
                 f"({','.join('?' * len(DEBT))})", list(DEBT))
    if parameter_id is not None:
        sql, args = sql + " AND parameter_id = ?", args + [parameter_id]
    owed = conn.execute(sql + " ORDER BY parameter_id, ref_id", args).fetchall()
    forms, clauses, retained, out = {}, {}, {}, []
    for ref, pid, status in owed:
        if pid not in forms:
            forms[pid] = {f for (n,) in conn.execute(
                "SELECT t.canonical_en FROM base_parameters p JOIN terms t ON t.term_id = p.term_id "
                "WHERE p.parameter_id = ? UNION SELECT a.alias FROM base_parameters p JOIN term_aliases a "
                "ON a.term_id = p.term_id WHERE p.parameter_id = ? AND a.alias_type NOT IN ('NARROWER', 'BROADER')",
                (pid, pid)) for f in [norm(n)] if f}
        if ref not in clauses:
            clauses[ref] = [(cid, norm(text)) for cid, text in conn.execute(
                "SELECT c.clause_id, c.clause_text FROM source_clauses c JOIN source_scans s ON s.scan_id = c.scan_id "
                "WHERE s.ref_id = ? ORDER BY c.clause_id", (ref,))]
        pair = {"ref_id": ref, "parameter_id": pid, "status": status}
        hit = [cid for cid, body in clauses[ref] if any(f in body for f in forms[pid])]
        if hit:
            out.append({**pair, "route": "inventory", "clauses": hit})
            continue
        if ref not in retained:
            retained[ref] = _retained_text(conn, retrieval_log, ref)
        out.append({**pair, "route": "retained-text", "file": retained[ref]} if retained[ref]
                   else {**pair, "route": "reread"})
    return out


def _reread(conn, limit):
    sys.path.insert(0, str(REPO / "scripts" / "research"))
    import retrieval_log                                              # noqa: E402
    routes = reread_routes(conn, retrieval_log)
    print("scan_debt --reread — the route each owed (source x parameter) pair takes: inventory, retained text, "
          "or a re-read")
    print(f"EXAMINED: {len(routes)}")
    for route in ("inventory", "retained-text", "reread"):
        mine = [r for r in routes if r["route"] == route]
        print(f"  {route:<14} {len(mine)}")
        for r in mine[:limit]:
            via = (f" clauses {r['clauses']}" if route == "inventory" else
                   f" sweep {r['file']}" if route == "retained-text" else "")
            print(f"    {r['ref_id']} x parameter {r['parameter_id']} ({r['status']}){via}")
        if len(mine) > limit:
            print(f"    ... {len(mine) - limit} more")
    flagged = sum(r["route"] == "reread" for r in routes)
    if not flagged:
        print("PASS: no owed pair needs the source read again")
        return 0
    print(f"REREAD: {flagged} pair(s) flagged: no clause of the inventory matches and no retained text is on disk. "
          f"Read once for every pair owed by the source (record-scan --mode catalogue), or --mode targeted when "
          f"exactly one is owed.")
    return 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--limit", type=int, default=20,
                    help="how many owed pairs to list per parameter (default 20)")
    ap.add_argument("--reread", action="store_true",
                    help="list each owed pair's route (inventory, retained text, re-read) and the pairs flagged "
                         "to be read again")
    args = ap.parse_args()
    if not DB_PATH.exists():
        print(f"scan_debt: no database at {DB_PATH}", file=sys.stderr)
        return 2
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        if not conn.execute("SELECT 1 FROM sqlite_master WHERE name='v_scan_ledger'"
                            ).fetchone():
            print("scan_debt: v_scan_ledger is absent (pre-103 schema)", file=sys.stderr)
            return 2
        if args.reread:
            return _reread(conn, args.limit)
        status = dict(conn.execute("SELECT status, COUNT(*) FROM v_scan_ledger "
                                   "GROUP BY status").fetchall())
        per_param = conn.execute(
            "SELECT l.parameter_id, t.canonical_en, "
            "SUM(l.status = 'NOT-READ'), SUM(l.status = 'READ-PARTIAL') "
            "FROM v_scan_ledger l JOIN base_parameters p USING (parameter_id) "
            "JOIN terms t ON t.term_id = p.term_id "
            "GROUP BY l.parameter_id ORDER BY l.parameter_id").fetchall()
        blocked = conn.execute(
            "SELECT COALESCE(text_scope, 'no reading'), COUNT(*) FROM v_scan_ledger "
            "WHERE status = 'BLOCKED' GROUP BY 1 ORDER BY 1").fetchall()
        # An operator's claim, named: a 'full' reading with no page count nothing verified.
        uncounted = conn.execute("SELECT COUNT(*) FROM source_scans WHERE text_scope = 'full' "
                                 "AND pages_read IS NULL").fetchone()[0]
        owed = conn.execute(
            "SELECT parameter_id, ref_id, status FROM v_scan_ledger WHERE status IN (?, ?) "
            "ORDER BY parameter_id, ref_id", DEBT).fetchall()
    finally:
        conn.close()

    total = sum(status.values())
    debt = sum(status.get(s, 0) for s in DEBT)
    print("scan_debt — (source x active parameter) pairs not yet read in full")
    print(f"EXAMINED: {total}")
    for s in ("EXTRACTED", "STATED-ABSENT", "BLOCKED", "READ-NOTHING-FOUND", "READ-PARTIAL",
              "NOT-READ"):
        print(f"  {s:<19} {status.get(s, 0)}")
    if status.get("BLOCKED"):
        print(f"  ({status['BLOCKED']} BLOCKED pair(s) are not debt: no full reading covers "
              f"them and the source carries a processing_blocked_reason the ledger classes as "
              f"an obstacle to the text. By the strongest covering reading: "
              + ", ".join(f"{scope} {n}" for scope, n in blocked) + ")")
    print(f"  full readings nothing counted (text_scope 'full', pages_read NULL): {uncounted} "
          f"-- the operator's claim, not a count")
    if not debt:
        print("PASS: every pair is extracted, stated absent, blocked, or read in full")
        return 0
    for pid, name, not_read, partial in per_param:
        if not_read or partial:
            refs = [r for p, r, _s in owed if p == pid]
            print(f"  parameter {pid} ({name}): {not_read} not read, {partial} read only "
                  f"partially -- {', '.join(refs[:args.limit])}"
                  + (" ..." if len(refs) > args.limit else ""))
    print(f"DEBT: {debt} pair(s). Read each source against the whole list and record it "
          f"(db.py record-scan; scripts/research/full_text.py derives a held PDF's text), or "
          f"a targeted reading for one new parameter (record-scan --mode targeted).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
