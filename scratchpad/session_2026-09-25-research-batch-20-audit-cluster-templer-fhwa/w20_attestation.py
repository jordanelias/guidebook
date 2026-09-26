#!/usr/bin/env python3
"""Update batch 20's attestation after the 2026-09-26 code-review round. Run from the worktree root."""
import json

P = "attestations/sessions_session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa.json"
with open(P, encoding="utf-8") as f:
    a = json.load(f)
prs = a.setdefault("per_rule_status", {})
integ = prs.setdefault("integrity-protocol", {})
integ["reason"] = integ.get("reason", "") + (
    " A 2026-09-26 code-review round added a fourth data migration (the record half: three OPEN "
    "gaps GAP-050/051/052, corrections to GAP-045/046/047 and to execs 90 and 91), driven by "
    "scratchpad/<session>/w18_code_review_round.py; the code half repaired the batch-20 writers "
    "and added scripts/tests/test_db_amend_writers.py. The rebuild again reproduces every row "
    "with only the bot's pre-existing drift.")
devs = a.setdefault("deviations", [])
devs.append({
    "rule": "integrity-protocol",
    "reason": (
        "Batch 20 wrote two admission edges with its own new verb and called them repaired, and "
        "a gate (S01) went green over them. S01 cannot fail on an edge link-admission writes, "
        "because the edge copies the column S01 compares; checked against batch 19's own record "
        "on 2026-09-26, both edges copy PROXY attributions -- candidate 124 came from REF-01006's "
        "reference list, candidate 125 from an Internet Archive search exec 90 never logged. Not "
        "repaired in this PR (it reconstructs batch 19's unlogged work, and the PR is on hold): "
        "filed as GAP-050, with results_admitted on execs 90 and 91 deliberately not raised to "
        "meet the proxy edges."),
})
devs.append({
    "rule": "adherence-logging-and-attestation",
    "reason": (
        "The batch's driver scripts masked db.py refusals with `| grep ... || true`, so five "
        "refused writes in w07/w08 ran past `set -e` silently. No data is wrong -- each refused "
        "write was redone in the next script and the final rows were checked -- but the committed "
        "scripts did not replay as they ran. Repaired 2026-09-26: dead attempts removed with a "
        "note of what ran, the mask narrowed so pipefail fails loud on a refusal."),
})
with open(P, "w", encoding="utf-8") as f:
    f.write(json.dumps(a, indent=2, ensure_ascii=False) + "\n")
print("ok; deviations:", len(devs))
