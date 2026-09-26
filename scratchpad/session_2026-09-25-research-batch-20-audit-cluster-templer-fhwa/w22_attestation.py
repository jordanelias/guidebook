#!/usr/bin/env python3
"""Update batch 20's attestation after the fourth fix-forward (owner rulings 2026-09-26).
Run from the worktree root."""
import json

P = "attestations/sessions_session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa.json"
with open(P, encoding="utf-8") as f:
    a = json.load(f)
integ = a.setdefault("per_rule_status", {}).setdefault("integrity-protocol", {})
integ["reason"] = integ.get("reason", "") + (
    " A fourth fix-forward (2026-09-26, owner rulings) repaired GAP-050 through the CLI alone: "
    "two backfill search rows for the real discovery steps (execs 99, 100), "
    "reattribute-candidate, unlink-admission, link-admission (w21_gap050_repair.py). Its "
    "DELETEs could not be captured by the additive-only emit path, so emit_batch_sql.py gained "
    "an opt-in --allow-delete, limited to tables a sanctioned writer deletes from "
    "(dbcore.deletable_tables, derived); a rebuild replays the deletes and reproduces every row.")
for d in a.get("deviations", []):
    if d.get("rule") == "integrity-protocol" and "GAP-050" in d.get("reason", ""):
        d["reason"] += (
            " REPAIRED 2026-09-26 by owner ruling: the real steps are logged as backfills, the "
            "candidates and edges moved to them, GAP-050 closed as fixed. The deviation stays "
            "recorded because the batch shipped the proxy edges as a repair before an "
            "independent review caught them.")
with open(P, "w", encoding="utf-8") as f:
    f.write(json.dumps(a, indent=2, ensure_ascii=False) + "\n")
print("ok")
