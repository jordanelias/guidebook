# CLAUDE.md compliance (orchestrator, 2026-09-23)
Verdict: mechanically sound (spine, cited checks, .ignore lines, ci.yml:257, archived paths, hook index all resolve) but breaks its own rules.
1. §6 says specifications unwritable via parameter_id into "still-empty base_parameters"; live: base_parameters 1 row, specifications 8 (all retired per architecture audit). Contradicts §4.
2. §4 "dbcore.WRITABLE_TABLES keeps going blind" — constant deleted (scripts/dbcore.py:783); rule 8 says derived.
3. §4 locator scripts/db.py:3978-3999 stale; refusal at db.py:7063-7076.
4. §7 "four dashboards ~579KB" — 7 files, 4.1M (du -ch tools/*.html).
5. Brief says "process, workflow and rules only"; carries 10 correction histories (grep -c 'until 20' CLAUDE.md); 34.6KB/4,972 words loaded every turn.
6. Never names .claude/agents (antagonist, db-census, repo-sweep) nor workflow skills (orient, batch-done, session-open, adversarial): grep count 0.
7. §7 stop-hook remedy scripts/fix_stop_hook_loop.sh is blocked for the agent by the auto-mode classifier (self-modification) — not executable by the agent.
8. Unanchored "this session's nine defects", "four separate times".
Gate run observations: attestation_presence/attestation_schema BLOCKING+vacuous on a non-synthesis diff; 3 advisory checks red on untouched main (retired_vocabulary, context_map_fresh, source_locators_integrity); 22/76 checks have no stated authority.
Owner instruction 2026-09-23: stop running suites so frequently; interrogate their merits.
