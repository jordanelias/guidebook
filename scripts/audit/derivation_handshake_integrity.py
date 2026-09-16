#!/usr/bin/env python3
"""scripts/audit/derivation_handshake_integrity.py — the handshake, checked on the rows.

WHAT WRONG THING REACHES THE *GUIDEBOOK* IF THIS DOES NOT EXIST (CLAUDE.md §8's bar,
which is about the book and not the apparatus):

  1. A `stated` determination sitting under an OPEN, BINDING gate. The book asserts a
     best-practice value while an audit has already said its population links are wrong,
     or that a source of equal-or-greater strength contradicts it. H4's whole content is
     that such a cell reads `provisional` "until resolved"; a cap that fails silently is
     indistinguishable from a cap that was never applied.
  2. A CULTURAL CLAIM ANCHOR THAT ANCHORS NOTHING — and this is the one the schema
     cannot catch. Migration 080's CHECK lets a `population_only` row skip the named-path
     rationale if `cultural_claim_anchor` is non-NULL, and it can only test that the value
     is valid JSON. A row carrying `["REF-00123"]` where REF-00123 is a code document
     satisfies that CHECK, skips the rationale, and inherits the dignity exemption BY
     ASSERTION. The ratified boundary criterion exists precisely to stop that: "the
     protection is anchored, not self-declared… a `population_only` claim WITHOUT such an
     anchor is simply a single-path claim owing the standard named-path rationale; it
     gains no cultural exemption by assertion." Nothing but this check enforces it.
  3. A single-path determination owing a rationale and carrying none. The CHECK refuses
     it at write time; this is the backstop for rows arriving by another route (a
     hand-written migration, a replay) — the same division of labour
     `medical_lens_integrity` has with `db.py add-medical`.
  4. `functional_basis` disagreeing with `population_icf_links`. The column is a JSON
     snapshot of rows that live in a table, which is a second home (rule 5) and is
     tolerated only because it records what the engine READ at determination time. The
     moment it names a mapping the table does not hold, the determination is justified by
     a functional basis nobody can reach.
  5. A gate whose stored `trigger_tier` no longer matches its own source. The
     ladder-inversion guard reads `trigger_tier`; if the source has since been re-tiered,
     the guard is deciding on a stale number — a grey-tier trigger can come to pin a
     T1-anchored cell, or a T1 trigger can stop binding, and neither is visible from the
     gate row. The same snapshot-versus-live shape as K02 in test_db_integrity.

ADVISORY, WITH THE RATCHET NAMED. House norm: a newly-wired check starts advisory. It is
also vacuous today — `specifications` holds 0 rows, because no parameter has been minted
since the 2026-09-13 circulation clear — and adding a SIXTH blocking-and-vacuous gate to
the list `run_checks.py` already prints as a defect would make the battery worse, not
safer. Ratchet to `blocking` with `min_items: 1` in the same change that writes the first
determination; determinations are never deleted, so the floor holds once set.
"""
import json
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# G3's predicate, IMPORTED AND NEVER RETYPED (rule 5). `grain_for()` is the one home of
# "which Co-1 provenance is population-grain community knowledge", and
# assess_cell.derivation_handshake() decides the anchor with the same call. A copy here
# would be a second implementation of a ratified rule, which is the finding that made
# grain_for() the single home in the first place.
from schemas.directness import GRAIN_AGGREGATE, grain_for      # noqa: E402

# HONOURS GUIDEBOOK_DB_PATH — the blocking db_path_env_audit requires it, and its reason
# is the one that matters here: a script that ignores the variable reads the committed
# database while a test believes it is reading a scratch copy, which would make this
# check's own fault injection unreliable.
DB = Path(os.environ.get("GUIDEBOOK_DB_PATH",
                         Path(__file__).resolve().parents[2] / "data" / "guidebook.db"))

VALUE_PATHS = ("dual", "population_only", "function_only")


def _table(con, name):
    return con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
                       (name,)).fetchone() is not None


def main(argv=None):
    # --db EXISTS SO THIS CHECK CAN BE FAULT-INJECTED. A gate nobody has seen go red is a
    # gate nobody has tested, and every subject below is unreachable on today's corpus.
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--db", default=str(DB), help="database to read (default: canonical)")
    args = ap.parse_args(argv)
    con = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row

    fails, notes = [], []
    specs = [dict(r) for r in con.execute(
        "SELECT * FROM specifications WHERE retired_at IS NULL ORDER BY specification_id")] if _table(con, "specifications") else []
    gates = [dict(r) for r in con.execute(
        "SELECT * FROM determination_gates ORDER BY gate_id")] if _table(con, "determination_gates") else []
    links = set()
    if _table(con, "population_icf_links"):
        links = {(r[0], r[1]) for r in con.execute(
            "SELECT population_code, icf_code FROM population_icf_links")}

    # --- 1 + 5. THE H4 CAP, AND THE LADDER GUARD IT DEPENDS ON ----------------------
    open_by_param = {}
    for g in gates:
        if g["resolved_at"] is None:
            open_by_param.setdefault(g["parameter_id"], []).append(g)
        if g["trigger_ref_id"]:
            src = con.execute(
                "SELECT tier, evidence_type FROM evidence_sources WHERE ref_id=?",
                (g["trigger_ref_id"],)).fetchone()
            if src is None:
                fails.append(
                    f"gate {g['gate_id']}: trigger_ref_id {g['trigger_ref_id']} is not a "
                    f"live source, so the strength this gate claims cannot be checked "
                    f"against anything")
            elif (src["tier"], src["evidence_type"]) != (g["trigger_tier"],
                                                        g["trigger_evidence_type"]):
                fails.append(
                    f"gate {g['gate_id']}: stored trigger is T{g['trigger_tier']}/"
                    f"{g['trigger_evidence_type']} but {g['trigger_ref_id']} is now "
                    f"T{src['tier']}/{src['evidence_type']}. The ladder-inversion guard "
                    f"reads the STORED value, so it is deciding on a stale strength.")

    for s in specs:
        sid, pid = s["specification_id"], s["parameter_id"]
        # The cell's best anchor, read the way derivation_handshake() reads it: the
        # strongest tier among the sources the determination actually governs on.
        govern = json.loads(s["governing_refs"]) if s.get("governing_refs") else []
        best = 6
        if govern:
            q = ",".join("?" * len(govern))
            row = con.execute(
                f"SELECT MIN(tier) FROM evidence_sources WHERE ref_id IN ({q}) "
                f"AND tier IS NOT NULL", govern).fetchone()
            if row and row[0] is not None:
                best = row[0]
        for g in open_by_param.get(pid, []):
            if g["identity_code"] and s["identity_code"] and \
                    g["identity_code"] != s["identity_code"]:
                continue
            if g["trigger_tier"] > best:
                continue                       # correctly non-binding: see the guard above
            if s["state"] == "stated":
                fails.append(
                    f"specification {sid}: `stated` under open gate {g['gate_id']} "
                    f"({g['verdict']}, T{g['trigger_tier']}) against a T{best} anchor. H4 "
                    f"caps such a cell at `provisional` until the gate is resolved by the "
                    f"named path; the book is asserting a value an audit has already "
                    f"contested.")

        # --- 2 + 3. THE SINGLE-PATH OBLIGATION, AND THE ANCHOR THAT MUST ANCHOR ------
        paths = s.get("derivation_paths")
        if paths is None:
            notes.append(f"specification {sid}: no derivation_paths recorded — written "
                         f"before migration 080, or by a route that skips the engine")
        elif paths not in VALUE_PATHS:
            fails.append(f"specification {sid}: derivation_paths={paths!r} is outside the "
                         f"ruled vocabulary {VALUE_PATHS}")
        anchor_raw = s.get("cultural_claim_anchor")
        if anchor_raw:
            try:
                anchor = json.loads(anchor_raw)
            except ValueError:
                anchor = None
                fails.append(f"specification {sid}: cultural_claim_anchor is not JSON")
            if isinstance(anchor, list):
                if not anchor:
                    fails.append(
                        f"specification {sid}: cultural_claim_anchor is an EMPTY list. An "
                        f"empty anchor still satisfies the schema's json_valid CHECK and "
                        f"still excuses the rationale, which is the exemption-by-assertion "
                        f"the boundary criterion forbids.")
                for ref in anchor:
                    src = con.execute(
                        "SELECT tier, evidence_type, co1_source_type FROM evidence_sources "
                        "WHERE ref_id=?", (ref,)).fetchone()
                    if src is None:
                        fails.append(
                            f"specification {sid}: cultural_claim_anchor names {ref}, "
                            f"which is not a live source. A protection anchored to nothing "
                            f"is self-declared.")
                        continue
                    if src["evidence_type"] != "co1" or grain_for(
                            "co1", src["tier"], src["co1_source_type"])[0] != GRAIN_AGGREGATE:
                        fails.append(
                            f"specification {sid}: cultural_claim_anchor names {ref}, which "
                            f"is evidence_type={src['evidence_type']!r} "
                            f"co1_source_type={src['co1_source_type']!r} — not "
                            f"population-grain community provenance under G3. The dignity "
                            f"protection is ANCHORED, NOT SELF-DECLARED: without a real "
                            f"anchor this cell owes the standard named-path rationale.")
            if paths != "population_only":
                notes.append(
                    f"specification {sid}: cultural_claim_anchor set on a {paths!r} "
                    f"determination. Harmless, but the protection only ever excuses the "
                    f"rationale a population_only row owes.")
        if paths in ("population_only", "function_only") and not s.get("derivation_rationale") \
                and not anchor_raw:
            fails.append(
                f"specification {sid}: {paths} with neither a named-path rationale nor a "
                f"cultural anchor. Migration 080's CHECK refuses this at write time, so "
                f"this row arrived by a route that bypassed it.")

        # --- 4. THE SNAPSHOT AGAINST THE TABLE --------------------------------------
        if s.get("functional_basis"):
            try:
                fb = json.loads(s["functional_basis"])
            except ValueError:
                fb = None
                fails.append(f"specification {sid}: functional_basis is not JSON")
            if isinstance(fb, list) and s["identity_code"]:
                missing = sorted({e.get("icf_code") for e in fb
                                  if isinstance(e, dict)
                                  and (s["identity_code"], e.get("icf_code")) not in links})
                if missing:
                    fails.append(
                        f"specification {sid}: functional_basis names "
                        f"{', '.join(map(str, missing))} for {s['identity_code']}, which "
                        f"population_icf_links does not hold. The determination is "
                        f"justified by a functional basis a reader cannot reach.")
            if not fb and s.get("derivation_paths") in ("dual", "function_only"):
                fails.append(
                    f"specification {sid}: derivation_paths={s['derivation_paths']!r} "
                    f"claims a function path, but functional_basis is empty.")
        elif s.get("derivation_paths") in ("dual", "function_only"):
            fails.append(
                f"specification {sid}: derivation_paths={s['derivation_paths']!r} claims a "
                f"function path with no functional_basis recorded at all.")

    print("=" * 70)
    print("derivation_handshake_integrity")
    print("=" * 70)
    for f in fails:
        print(f"  [FAIL] {f}")
    for n in notes:
        print(f"  [NOTE] {n}")

    unresolved = sum(1 for g in gates if g["resolved_at"] is None)
    if not specs:
        print("  specifications holds 0 rows.")
        print("  NOT a check with nothing to say: it is the corpus state. `specifications`")
        print("  cannot accept a row until a parameter is minted (CLAUDE.md §4), and none")
        print("  has been since the 2026-09-13 circulation clear. Every subject here is")
        print("  therefore unreachable today — which is why this check is advisory and why")
        print("  its own failure paths are exercised by fault injection against a scratch")
        print("  copy rather than by the live corpus.")
    print(f"\n  determinations: {len(specs)}  "
          f"gates: {len(gates)} ({unresolved} open)  "
          f"distinct (population, ICF code) pairs: {len(links)}")
    print(f"EXAMINED: {len(specs) + len(gates)}")
    print("VERDICT: " + ("FAIL" if fails else "CLEAN"))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
