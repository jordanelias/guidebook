---
name: connection-scout
status: DEPRECATED
deprecated_date: 2026-05-05
superseded_by: connection-discovery
decision: D-0146
---

# DEPRECATED — Use connection-discovery instead

connection-scout has been merged into connection-discovery (D-0146, 2026-05-05).

**Migration:**
- `--mode evidence` replaces connection-scout internal mode (BPC + gap register scan)
- `--mode external` replaces connection-scout external mode (forward citations)
- SPECULATIVE→gap rule preserved: now routes to category CR (not CONN, which was never valid)

All new connection scans use `skills/connection-discovery_SKILL.md`.
