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
    2 — DB error, or --session names no resolvable session

Every run reports an `Examined` count and one of three verdicts: OUTSTANDING,
CLEAN, or NOTHING-IN-SCOPE. The third exists because "no violations found" and
"no subjects to find violations in" both used to print `Outstanding: 0` and exit
0, which made the pass carry no information — the gate could not say whether it
had done its job or merely been pointed somewhere empty.

Author: written 2026-05-11 in session_2026-05-11g-citation-mining.md per GAP-283 P1.
"""
import argparse
import json
import os
import sqlite3
import sys

DEFAULT_DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")

def _latest_hint():
    """What the session pointers currently name — for the mis-scoped-session error.

    Reports BOTH pointers since the W4 split. This gate is fed LATEST-RESEARCH;
    quoting LATEST alone in its error would send the reader to the wrong file.
    """
    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out = []
    for name in ("LATEST-RESEARCH", "LATEST"):
        try:
            with open(os.path.join(repo, "sessions", name)) as f:
                out.append(f"sessions/{name}={f.read().strip().splitlines()[0]!r}")
        except Exception:
            out.append(f"sessions/{name}=unreadable")
    return "; ".join(out)


def session_keys(session):
    """Both spellings of a session name, because the DB holds both.

    `evidence_sources.created_by_session` stores the bare stem on 32 of its 33
    distinct values and `...11g-citation-mining.md` on the 33rd. The pointer
    files under sessions/ hold the FILENAME, with the extension. So the scoping
    predicate `created_by_session = :session` compared a name ending in `.md`
    against values that do not, and selected nothing — for every session, under
    either pointer.

    That is the mechanism behind the vacuous pass this gate was cited for. It
    was read as a pointer-staleness problem (CLAUDE.md §2(a); pointer corrected
    2026-08-22, was §10) and the W4.1 pointer
    split was expected to fix it; the split is correct and necessary, but on its
    own it moved the gate from one name that matched nothing to another name
    that matched nothing. Normalising here is what actually puts rows in scope.
    """
    stem = session[:-3] if session.endswith(".md") else session
    return stem, stem + ".md"


def audit(db_path, session=None, tier_max=2, output_json=False):
    if not os.path.exists(db_path):
        print(f"ERROR: DB not found at {db_path}", file=sys.stderr)
        return 2, None

    try:
        con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        con.row_factory = sqlite3.Row
    except Exception as e:
        print(f"ERROR: cannot open DB: {e}", file=sys.stderr)
        return 2, None

    # A --session naming a session that does not EXIST must ERROR, not report
    # compliance.
    #
    # This gate is BLOCKING, and scoped to a session it reports "Outstanding: 0"
    # whenever the scope selects nothing. Demonstrated 2026-08-04: `--session
    # no-such-session-xyz.md` printed "Total with citation_mining row: 9 (4.7%) /
    # Outstanding: 0" and exited 0 — a typo was indistinguishable from compliance.
    # This closes that: an unresolvable session name is an operator error (exit 2),
    # distinct from the backlog the gate exists to report (exit 1).
    #
    # This validates that the session RECORD exists, not that the scope selects
    # rows. A scope selecting nothing is reported instead of refused — see the
    # `examined` count and the NOTHING-IN-SCOPE verdict below, added by W4 on
    # 2026-08-06. An earlier draft made the empty scope an error and was reverted:
    # a session that legitimately logged only Tier 3 sources has nothing this gate
    # is entitled to demand, and failing it would redden main for doing nothing
    # wrong. Naming the empty scope is what the situation needed; punishing it was
    # not. The `.md` normalisation landed in the same pass — see session_keys().
    # A session is RESOLVABLE if it has a record OR it logged rows. Requiring a
    # `.md` file alone was wrong and was caught by the compliance check before it
    # could bite: 22 of the 33 distinct `created_by_session` values in
    # evidence_sources have no file under sessions/ — including every
    # `session_2026-07-19-*` citation-mining batch, i.e. exactly the research
    # sessions this gate exists to audit. File-only resolution is latent today
    # (the registered check is fed sessions/LATEST, which is a real file) and
    # would have turned this blocking gate red with a spurious "operator error"
    # the moment W4.1 pointed it at a research session.
    if session:
        repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        sdir = os.path.join(repo, "sessions")
        stem, stem_md = session_keys(session)
        known = set()
        for root, _dirs, files in os.walk(sdir):
            for fn in files:
                if fn.endswith(".md"):
                    known.add(fn)
                    known.add(fn[:-3])
        logged = con.execute(
            "SELECT EXISTS (SELECT 1 FROM evidence_sources "
            "WHERE created_by_session IN (?, ?))", (stem, stem_md)).fetchone()[0]
        if not logged and known and stem not in known and session not in known:
            print(f"ERROR: --session {session!r} names no session record under "
                  f"sessions/. A scope that selects nothing reports 'Outstanding: 0' "
                  f"and passes, which is indistinguishable from compliance — so an "
                  f"unresolvable name is refused rather than answered. "
                  f"Pointers: {_latest_hint()}.",
                  file=sys.stderr)
            return 2, None

    # Outstanding = Tier 1..tier_max source in evidence_sources, linked to some slug,
    # with no citation_mining row referencing its ref_id, and (if --session given)
    # was added in that session.
    skey, skey_md = session_keys(session) if session else (None, None)
    where_session = ("AND es.created_by_session IN (:session, :session_md)"
                     if session else "")
    params = {"session": skey, "session_md": skey_md, "tier_max": tier_max}
    rows = con.execute(f"""
        SELECT DISTINCT es.ref_id, es.tier, va.author_display AS authors, es.pub_year AS year, es.pub_title AS title, es.doi,
                        es.created_by_session, es.verification_status,
                        GROUP_CONCAT(DISTINCT ssl.slug) as slugs
        FROM evidence_sources es
        JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
        -- POINTER, NOT COPY (migration 063): the author list has one home,
        -- evidence_source_authors, and v_evidence_authors renders it.
        LEFT JOIN v_evidence_authors va ON va.ref_id = es.ref_id
        -- Resolve a mining row to its source the way citation_mining's own
        -- primary key does: global_ref_id when present, otherwise
        -- (slug, local_ref_id) through source_slug_links. global_ref_id is NULL
        -- on 146 of 183 rows, so joining on it alone reported 48 of 168
        -- Tier 1-2 sources as unmined when a mining row for them exists.
        -- This gate is BLOCKING, so those were 48 false positives at session
        -- close. Same defect as data_20260802215744, found by the adversarial
        -- pass over that fix; corrected here rather than in a second column.
        LEFT JOIN citation_mining cm
               ON cm.global_ref_id = es.ref_id
        -- cm2 IS A LEGACY FALLBACK AND IS CURRENTLY DORMANT: measured 2026-08-24,
        -- 0 of 10 citation_mining rows have a NULL global_ref_id, so this join reaches
        -- nothing. It is KEPT rather than deleted because its reason is specific and
        -- its failure direction is safe: a row that only (slug, local_ref_id) can reach
        -- would otherwise report UNMINED, which is the 48-false-positive bug described
        -- above. `log_mining` now always writes global_ref_id, so the only way it fires
        -- again is a legacy import. Delete it once no such row can exist.
        LEFT JOIN citation_mining cm2
               ON cm2.slug = ssl.slug AND cm2.local_ref_id = ssl.local_ref_id
        WHERE es.tier BETWEEN 1 AND :tier_max
          AND cm.global_ref_id IS NULL
          AND cm2.slug IS NULL
          {where_session}
        GROUP BY es.ref_id
        ORDER BY es.tier, es.ref_id
    """, params).fetchall()

    # EXAMINED — the denominator the "Outstanding" count is a fraction of.
    #
    # Same shape as the query above minus the two mining joins: slug-linked
    # sources inside the tier scope, inside the session scope if one was given.
    # Without this the gate could print "Outstanding: 0" over a scope holding
    # nothing and there was no line in the output to tell the two apart. That is
    # the vacuity CLAUDE.md §2(a) names (pointer corrected 2026-08-22, was §10):
    # passing on merits and passing for want of
    # subjects render identically, so the pass carries no information either way.
    examined = con.execute(f"""
        SELECT COUNT(DISTINCT es.ref_id)
        FROM evidence_sources es
        JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
        WHERE es.tier BETWEEN 1 AND :tier_max
          {where_session}
    """, params).fetchone()[0]

    # A second query stood here, disabled with `if False else []` and annotated
    # "^ disabled the convoluted query — keep simple, do it in Python below". It was
    # dead on every path. Removed 2026-08-24 with the author-copy sweep; git is the
    # archive for code (CLAUDE.md §1). The Python scan below is the live version.
    # Simpler: scan cm rows where both directions are 0 and no defer reason
    bad_cm = []
    for cm in con.execute("""
        SELECT cm.global_ref_id, cm.slug, cm.local_ref_id, cm.backward, cm.forward,
               cm.deferred_reason, es.tier, va.author_display AS authors, es.pub_year AS year,
               es.created_by_session as es_session, cm.created_by_session as cm_session
        FROM citation_mining cm
        JOIN evidence_sources es ON cm.global_ref_id = es.ref_id
        LEFT JOIN v_evidence_authors va ON va.ref_id = es.ref_id
        WHERE es.tier BETWEEN 1 AND ?
          AND cm.backward = 0 AND cm.forward = 0
          AND (cm.deferred_reason IS NULL OR cm.deferred_reason = '')
    """, (tier_max,)).fetchall():
        if session and not ({cm["es_session"], cm["cm_session"]} & {skey, skey_md}):
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

    # A session-scoped run that selects no subjects is CLEAN in the sense that it
    # found no violation, and empty in the sense that it looked at nothing. It
    # gets its own word so the two never share one.
    verdict = ("OUTSTANDING" if (rows or bad_cm)
               else "NOTHING-IN-SCOPE" if examined == 0
               else "CLEAN")

    result = {
        "db_path": db_path,
        "session_scope": session,
        "tier_max": tier_max,
        "examined": examined,
        "verdict": verdict,
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
        print(f"  Examined (slug-linked T1-{tier_max} sources in scope): {examined}")
        print(f"  Outstanding (no citation_mining row): {len(rows)}")
        print(f"  VERDICT: {verdict}")
        if session:
            # Repo-wide, and labelled as such. These used to be printed under a
            # session-scoped run as "Total in scope" / a coverage percentage,
            # which read as though the session had been measured — the run that
            # examined zero of its own sources still reported "9 (4.7%)".
            print(f"  (repo-wide, not this session: {total_with_cm}/{total_t12} "
                  f"T1-{tier_max} sources mined, {coverage_pct:.1f}%)")
        else:
            print(f"  Total in scope: {total_t12}")
            print(f"  Total with citation_mining row: {total_with_cm} ({coverage_pct:.1f}%)")
        if verdict == "NOTHING-IN-SCOPE":
            print()
            print(f"  Nothing was checked. {session!r} logged no slug-linked "
                  f"Tier 1-{tier_max} sources, so this run found no violation by "
                  f"having no subject — which is not the same as compliance. If "
                  f"that session did research, the scope or the pointer is wrong.")
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
