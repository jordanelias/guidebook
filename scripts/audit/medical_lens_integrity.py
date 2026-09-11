#!/usr/bin/env python3
"""scripts/audit/medical_lens_integrity.py — the fourth lens cannot become the frame.

WHAT WRONG THING REACHES THE *GUIDEBOOK* IF THIS DOES NOT EXIST (CLAUDE.md §8's bar for
adding a check, which is about the book and not the apparatus):

  1. A determination whose only lens is a DIAGNOSIS. That renders as "this is what disabled
     people with condition X need", which is the medical model as the project's frame. D-0170
     adopted the medical lens as a READER'S CHOICE — "we give our users the choice of what
     model they want to use to browse the site" — and its rationale turns entirely on the
     lens being offered rather than adopted. A medical-only cell reverses that on the page.
  2. A medical row whose display_name states its answer — the item-layer defect the owner
     deleted a whole table to escape, rebuilt one lens over.
  3. A medical row nothing crosses to. The reader selects the medical lens, finds the row,
     and cannot get from it to the evidence, because the crossings are what carry them.
  4. An ICD-11 anchor asserted from memory. Reported rather than failed, because with no WHO
     credentials in the environment the honest state is unverified — but a count nobody
     prints is a count nobody acts on.

`db.py add-medical` refuses 1-3 at write time. This is the backstop for rows that arrive by
any other route (a hand-written migration, a replay, a future writer), which is the same
division of labour `validate_parameters` has with `add-term`.

ADVISORY UNTIL ANCHORS VERIFY. Blocking on unverified anchors today would redden every run
for a reason no session can fix from this container; that is a check red by construction,
which CLAUDE.md rule 6 says teaches its reader to ignore it.
"""
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db import _VALUE_BEARING, _MD_CODE          # noqa: E402  — imported, never retyped (rule 5)

# HONOURS GUIDEBOOK_DB_PATH, because the blocking db_path_env_audit caught the first draft
# hardcoding this and it was right to. Its own reason is the one that matters: a script that
# ignores the variable "will silently read the committed database while a test believes it is
# reading a scratch copy" — which would have made this check's own fault injection unreliable
# in any configuration that sets it.
DB = Path(os.environ.get("GUIDEBOOK_DB_PATH",
                         Path(__file__).resolve().parents[2] / "data" / "guidebook.db"))


def main(argv=None):
    # --db EXISTS SO THIS CHECK CAN BE FAULT-INJECTED. A gate nobody has seen go red is a
    # gate nobody has tested; pointing it at a scratch copy with a deliberately bad row is
    # how its failure path gets exercised without touching the committed blob.
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--db", default=str(DB), help="database to read (default: canonical)")
    args = ap.parse_args(argv)
    con = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute("SELECT * FROM base_taxonomy_medical ORDER BY medical_code")]
    fails, notes = [], []

    crossed = {r[0] for r in con.execute("SELECT medical_code FROM identity_medical_map")} | \
              {r[0] for r in con.execute("SELECT medical_code FROM icf_medical_map")}

    for r in rows:
        code = r["medical_code"]
        if not _MD_CODE.match(code):
            fails.append(f"{code}: code does not match ^MD-[A-Z]+(-[A-Z]+)*$ — a digit here "
                         f"collides with the prior-version [A-Z]-NN item shape")
        for col in ("display_name", "description"):
            if r.get(col) and _VALUE_BEARING.search(r[col]):
                fails.append(f"{code}: {col} states a determination in its own name — "
                             f"{r[col]!r}")
        if code not in crossed:
            fails.append(f"{code}: no crossing in identity_medical_map or icf_medical_map — "
                         f"a reader selecting the medical lens cannot reach the evidence "
                         f"from it (D-0170)")
        if not r.get("icd11_verified_at"):
            notes.append(f"{code}: icd11_anchors={r.get('icd11_anchors')!r} NOT verified "
                         f"against a retrieved payload")

    # THE FRAME TEST. A cell keyed on a diagnosis alone is the medical model as the project's
    # frame. assess_cell.py should never emit one; this catches any that arrive otherwise.
    medical_only = [r[0] for r in con.execute(
        "SELECT specification_id FROM specifications "
        "WHERE medical_code IS NOT NULL AND identity_code IS NULL "
        "AND icf_code IS NULL AND needs_code IS NULL")]
    for sid in medical_only:
        fails.append(f"specification {sid}: medical_code is its ONLY lens. A determination "
                     f"keyed on a diagnosis alone renders the medical model as the "
                     f"project's frame, which D-0170 offers as a choice and does not adopt.")

    print("=" * 70)
    print("medical_lens_integrity")
    print("=" * 70)
    for f in fails:
        print(f"  [FAIL] {f}")
    for n in notes:
        print(f"  [NOTE] {n}")
    if not rows:
        print("  base_taxonomy_medical holds 0 rows.")
        print("  NOT an unexecuted ruling: D-0170 adopted the lens 2026-08-27 and the")
        print("  vocabulary's CONTENT is blocked on licensing (DG-NON item 7) — see")
        print("  scratchpad/pr-134-repository-orientation/MEDICAL-LENS-LICENSING-STOP.md.")
    print(f"\n  unverified anchors: {len(notes)} of {len(rows)}")
    print(f"EXAMINED: {len(rows)}")
    print("VERDICT: " + ("FAIL" if fails else "CLEAN"))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
