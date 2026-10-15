# PR body notes, step 1.1 (render apparatus, RULINGS R1) -- branch stack/1.1-render-apparatus

Gates (diff-scoped): preflight PASS; run_checks --selftest PASS; build_graph --check 0 failures, --selftest 18/18.
Removed registry checks (derived by diffing check ids vs origin/main): evidentiary_audit_fresh, pipeline_completeness_fresh,
pipeline_walk_fresh, render_audit_browser, schema_walkability_fresh, site_pages_fresh.
Net-negative measure (CLAUDE.md §8): `git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'`
-> 23 files, +51 / -2422. Whole diff: 97 files, +3654 / -21453. (tools/ is outside the measure.)

Antagonist (Fable 5.1, read-only, isolated worktree): F1-F8, each reproduced then repaired in d6c2008 (see commit body).

Owner items:
- DR-2026-09-26 line 615 (RC-156) still tells the reader to regenerate tools/*.html with scripts/regenerate_derived.sh; decisions/ is ratified text, not edited here.
- research_contract_sync registry note now describes its shape as a derived-artifact gate modelled on context_map_fresh --check.
- stage-map completeness (a table missing from governance/stage-map.yaml) is now enforced only by the unregistered
  `build_graph.py --check` until plan step 4.4 registers it; by review until then.
- preflight (diff-scoped) and `--all` select different check counts; counts are derived, run `run_checks.py --list`.
- register_integrity_check cannot start (imports deleted pilot_renderings); quarantine reason says so; plan 1.6(a) deletes it.
- GAP-036 and GAP-066 stay open; closing them is a data row (rule 10).
Not in this PR: any data row, migration, or the item-layer work (1.2).
