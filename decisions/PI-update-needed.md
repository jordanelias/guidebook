# PI v10.6 Update Required

**Pending owner action.** The DR adopted protocol requires PI update to add standing rule #7.

Current PI is v10.5 in claude.ai project knowledge. Cannot be modified via repo commit.

**To apply:**
1. Owner edits Project Instructions in claude.ai
2. Adds the standing rule below
3. Bumps version to v10.6
4. Updates changelog


## Proposed addition to PI v10.6 (next revision)

### Standing rule #7: Adversarial research protocol
All research-generating gap closures must populate four protocol fields:
- `gaps.confidence_interval` (numerical range, e.g., "60-75%")
- `gaps.shift_conditions` (what would shift CI up/down)
- `gaps.named_dissenter` (specific contrary view OR "NONE FOUND" with logged queries)
- `gaps.falsification_condition` (specific finding that would invalidate)

Population matches must be logged to `evidence_population_match` with rubric grade (EXACT/PARTIAL/PROXY/MISMATCH).

Audit query: `scripts/audit/research_protocol_audit.py` (run before session close).

Rationale: Claude's research mode defaults to consensus confirmation. Protocol forces specific, falsifiable artifacts that humans can spot-check. See `decisions/DR-2026-05-09-adversarial-research-protocol.md`.

Enforcement level: 2 (audit query). Promotion to 3 (pre-commit hook) deferred until Phase 1 hooks ship.
