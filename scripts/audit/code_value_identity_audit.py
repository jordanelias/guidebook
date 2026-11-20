#!/usr/bin/env python3
"""
scripts/audit/code_value_identity_audit.py -- a code value whose codes the maps tie to a group, with no identity written, is listed.

WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT IT (T-126): a code value silently absent from every cell of a group it
serves. The writer's warning (`db.py add-extraction` / `add-lens-link`: "WARNING: maps propose ...") is seen once, by
the session that wrote the row; the engine reaches a cell only through the lens links written on a figure (D-0184,
OR-1), so a stored code value whose recorder left out every group its codes propose is otherwise invisible. Subject
and findings are derived from the live tables on each run; the proposals are the writer's own query
(`db.identity_proposals`).

Prints `EXAMINED: <n>`, the live figures of sources of tier 4 or above (the regulatory stratum) with any live lens
link; a derived line, never a failure, counting those that carry no identity link that is judged (not `carried`) and
not `ALL` (the queue the one-time pass over stored code values, T-127, works); then
  (i)   by extraction id, every such figure with live ICF or access-need links, no live identity link and at least
        one proposal, with its proposals (`ALL` is not an identity, OD-31); a figure whose every live link has basis `heading` is left out (OD-31: a
        heading that names no group gives no identity). A figure whose recorder judged that no proposed group is served
        stays here (OD-47, still the owner's, decides whether such a judgment needs a row of its own);
  (ii)  for information, every live identity (the scope marker aside) no live map row proposes;
  (iii) for information, every such figure for which a map row (or the access_need_icf row it is reached through)
        created after the figure's newest live lens link proposes an identity the figure does not carry: the figures
        recorded before the base could propose a group, for a later lens pass. It clears when the session writes a
        link (a live link newer than the map row);
  (iv)  for information, the figures with no ICF or need link: those whose only identity is the scope marker (they
        reach no group cell: the harm this audit names) and those reached only through carried, unjudged identity
        links, each counted and listed by id.

Usage:  python3 scripts/audit/code_value_identity_audit.py
Exit 0 list (i) is empty; 1 it is not; 2 cannot run. Lists (ii) to (iv) and the queue line never set the exit code. The registry level,
not the exit code, makes it advisory.
"""
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import db                                                              # noqa: E402
import dbcore                                                          # noqa: E402

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))


def main():
    if not DB_PATH.exists():
        print(f"code_value_identity_audit: no database at {DB_PATH}", file=sys.stderr)
        return 2
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        figs = conn.execute(
            "SELECT DISTINCT k.extraction_id, MAX(datetime(k.created_at)) OVER (PARTITION BY k.extraction_id) "
            "FROM v_live_lens_links k JOIN source_value_extractions x ON x.extraction_id = k.extraction_id "
            "JOIN evidence_sources e ON e.ref_id = x.ref_id WHERE e.tier >= ? ORDER BY k.extraction_id", (dbcore.REGULATORY_FROM_TIER,)).fetchall()
        marker = dbcore.SCOPE_MARKER_IDENTITY                              # not a group (OD-31)
        omitted, late, queue, only_marker, only_carried = [], [], 0, [], []
        for eid, newest in figs:
            links = conn.execute("SELECT identity_code, icf_code, needs_code, basis FROM v_live_lens_links "
                                 "WHERE extraction_id=?", (eid,)).fetchall()
            ids = {r[0] for r in links if r[0] and r[0] != marker}
            queue += not any(r[0] and r[0] != marker and r[3] != "carried" for r in links)
            icf, needs = [r[1] for r in links if r[1]], [r[2] for r in links if r[2]]
            if not icf and not needs:                     # reached only through its identity links, if at all
                if not ids:
                    only_marker.append(eid)
                elif all(r[3] == "carried" for r in links):
                    only_carried.append(eid)
            props = db.identity_proposals(conn, icf, needs)
            if not ids and (icf or needs) and props and any(r[3] != "heading" for r in links):
                omitted.append((eid, props))
            fresh = sorted({p["identity_code"] for p in props if p["identity_code"] not in ids and any(
                t and conn.execute("SELECT datetime(?) > ?", (t, newest)).fetchone()[0]
                for t in (p["map_created_at"], p["need_row_created_at"]))})
            if fresh:
                late.append((eid, fresh))
        unproposed = [c for (c,) in conn.execute(
            "SELECT identity_code FROM base_taxonomy_identity WHERE status='active' AND identity_code <> ? AND "
            "identity_code NOT IN (SELECT identity_code FROM identity_icf_map WHERE retired_at IS NULL) "
            "ORDER BY identity_code", (marker,))]
    finally:
        conn.close()
    print("code_value_identity_audit -- a code value whose codes the maps tie to a group, with no identity written, is listed")
    print(f"EXAMINED: {len(figs)}")
    print(f"queue (derived, not a failure): {queue} of these figures carry no identity link that is judged (basis other "
          f"than carried) and not {marker}; the one-time lens pass over stored code values (T-127) works this queue")
    print(f"(i) figures with ICF or need links, no identity link but the scope marker, and a proposal: {len(omitted)}")
    for eid, props in omitted:
        print(f"  extraction {eid}: maps propose " + ", ".join(
            f"{p['identity_code']} (via {p['icf_code']}; {p['mapping_confidence']}, {p['provenance']})" for p in props))
    print(f"(ii) live identities no map row proposes (information): {', '.join(unproposed) or 'none'}")
    print(f"(iii) figures a map row newer than their newest live link proposes a group for (information): {len(late)}")
    for eid, codes in late:
        print(f"  extraction {eid}: {', '.join(codes)}")
    print(f"(iv) figures with no ICF or need link (information, the lens passes' queue): {len(only_marker)} carry no "
          f"identity but {marker}, so reach no group cell: {', '.join(map(str, only_marker)) or 'none'}; "
          f"{len(only_carried)} are reached only through carried (unjudged) identity links: "
          f"{', '.join(map(str, only_carried)) or 'none'}")
    return 1 if omitted else 0


if __name__ == "__main__":
    sys.exit(main())
