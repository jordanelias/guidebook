#!/usr/bin/env python3
"""Append a reattestation entry to DR-2026-08-19's attestation for the 2026-09-26 AMENDED note.

One attestation per artifact path, updated through its reattestation log (the convention its
own 2026-09-10 entry records). Preserves the file's existing JSON escaping and indentation.
Run from the worktree root.
"""
import json

P = "attestations/decisions_DR-2026-08-19-research-restart-operative-instrument.json"
with open(P, encoding="utf-8") as f:
    raw = f.read()
a = json.loads(raw)
sha = a["doctrine_sha"]
a.setdefault("reattestation", []).append({
    "prior_doctrine_sha": sha,
    "new_doctrine_sha": sha,
    "delta_ref": "scripts/migrations/096_candidate_disposition_exhausted.sql",
    "materiality": "IMMATERIAL",
    "verdict_change": "none",
    "reason": (
        "ANNOTATED 2026-09-26, NOT RE-GROUNDED: doctrine did not move. Step 4 of section 12.1 "
        "states the search_candidates disposition list as REHOME|MISCELLANEOUS|"
        "PENDING-VERIFICATION|OUT-OF-SCOPE|ADMITTED; schema migration 096 (owner ruling "
        "2026-09-25) added EXHAUSTED. An AMENDED callout was appended beneath the step, in the "
        "instrument's own appended-not-edited style, pointing at the column's CHECK as the "
        "vocabulary's only home and noting the REHOME destination rule added the same day. Section "
        "12.1 was already superseded in full on 2026-09-10; the text of the step is unchanged."),
})
with open(P, "w", encoding="utf-8") as f:
    f.write(json.dumps(a, indent=2, ensure_ascii="\\u00" in raw)
            + ("\n" if raw.endswith("\n") else ""))
print("appended; entries:", len(a["reattestation"]))
