# bootstrap.sh — DB-derive Phase E/D denominators (staged)

**Type:** *executed* (repo edit, staged for `main`). Per PI v10.14 `bootstrap.sh` ships by ordinary commit — no PI bump, no owner paste.

## Change (`bootstrap-denominators.diff`, +5/−2)
The session status block had hardcoded `/ 95` (Phase E) and `/ 245` (Phase D) denominators — the stale "95 filesystem BPCs" phantom and the authoring-time connection count. Replaced both with runtime DB queries, matching the existing `ES_TOTAL` pattern:
- `REASONING_BPC_TARGET = SELECT COUNT(*) FROM slugs WHERE status='ACTIVE'` → **82** (the workplan's "ACTIVE slugs only" Phase-E target; the 14 frozen aggregates are correctly excluded).
- `REASONING_CON_TARGET = SELECT COUNT(*) FROM connections` → **273** (was 245 at authoring).

Both vars default to `?` so a failed DB fetch degrades gracefully, consistent with the other state queries. Comment block updated to record that the denominators are now DB-derived.

## Verified
`bash -n` clean; queries resolve to 82 / 273 against the committed DB; diff is surgical.

## Commit (passes check_commit_msg.py)
`bootstrap: DB-derive Phase E/D denominators, retiring stale /95 and /245 [2026-06-09 02:00]`

## Not touched (out of scope; flagged earlier)
- `/ 675` (Track 1 versioning denominator) — still hardcoded; same drift class. Left as-is per your scoping; say the word and I'll DB-derive it too.
- `references/specification-database.json` (ALL-ENV / -stub spec slugs) — inert under DB-as-truth (read only by the historical convert/migrate import pipeline); flagged for the spec-layer cleanup.
- Stale doc references (`native-alias-verification.md`, `co1-operational.md` DEAF.md example) — non-gating.
