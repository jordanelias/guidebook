# Handoff — structural integrity audit complete, remediation not started

**Repo:** `jordanelias/guidebook`
**Branch:** `claude/status-check-12728x` · **PR:** #91 (open)
**HEAD at handoff:** `331f59a`
**Last session record:** `sessions/session_2026-08-11-structural-integrity-audit.md`
**Latest PI in repo:** `governance/project-instructions-v10_14.md` (the repo PI legitimately lags — the owner pastes it into claude.ai)
**Doctrine SHA:** `0f2f525`
**The plan to work from:** `workplan/2026-08-11-remediation-and-pipeline-anatomy.md`

> **The header fields above are checked** by `validate_cross_refs` (blocking) for the named
> record and plan, and reported by `test_db_integrity` L04 for pointer drift. Note that
> `session_pointer_resolvable` — named in CLAUDE.md §10 and in the previous handoff as a
> registered blocking check — **does not exist**, in the registry or in code. The audit it named
> was deliberately deleted on 2026-08-06 and its function redistributed; pointer honesty is
> genuinely enforced, by three other mechanisms, verified by execution. CLAUDE.md §10 needs
> correcting on this and still describes the *fixed* SKIP hazard as current.

---

## Start here

**Read `workplan/2026-08-11-remediation-and-pipeline-anatomy.md` §0.2 first** — eleven of that
document's own first-draft proposals were corrected or killed by its adversarial passes, and the
correction log tells you which conclusions are load-bearing and which were withdrawn. Then §1.6,
the sequencing, which exists because `tooling-register.md` §6 already withdrew as unwise the
exact bundle the first draft proposed.

**Then run the environment setup, because the documented one fails:**

```
pip install --ignore-installed pydantic jsonschema      # NOT `pip install -r requirements.txt`
```

`requirements.txt` pins `PyYAML==6.0.3` against a container-installed 6.0.1 that pip cannot
uninstall, and omits `jsonschema` while asserting in its header that only two dependencies
exist. Without these, five *blocking* checks fail with `ModuleNotFoundError` and the repo looks
broken when it is not.

## Where things stand

**The apparatus is green and the green is not load-bearing.** `run_checks.py --all` reports
`PASS — 55 green, 9 advisory`; `test_db_integrity` reports 70/70. Meanwhile a fabricated
corridor width passes every blocking gate, at least eleven representations are measurably out of
agreement, and 7 of the last 30 `ci.yml` runs on `main` were red and merged.

**The structural question is answered.** A synthetic topic traversed all twelve stages with no
break point — so the structure *can* carry content. That is the problem, not the reassurance:
`tier=99` reached the published bibliography as a fabricated band "T99", and the determined
value never rendered at all.

**Nothing has been executed.** The register proposes; it does not act.

## Do these first — no decision required

1. **Guard the three unguarded direct writers.** `scripts/migrations/session_2026_05_11g_replay.py`,
   `scripts/migrate/init_database.py`, `scripts/migrate/phase_jv_appendix_a.py` — import
   `_legacy_guard` as their seven siblings already do. The first takes no arguments, defaults to
   the canonical DB, has its 64-row payload committed and present, and would leave no
   `data_migrations` record. **This is the one item that can undo the clean-room reset.**
2. **Wire the registry's existing `deps:` field.** `governance/check-registry.yaml` declares
   per-battery dependencies; `grep -n "deps" scripts/run_checks.py` returns nothing. Two entries
   are also wrong: `tests: {deps: []}` is false, and the `governance` entry at line 174 is
   malformed YAML — unquoted commas in a flow mapping produce two junk keys and a truncated
   description, which `check_yaml` passes because it is valid YAML.
3. **Fix the `test_graph_audit` crash.** `graph_audit.py:277` dereferences `None` on an empty
   `connections` table, hiding every assertion behind it.

## The owner decisions that unblock the rest

| # | Decision | Why it is first |
|---|---|---|
| **D2** | The migration exemption list — `url_verification_runs` and `evidence_sources`-by-DOI are legitimate out-of-migration writers that are not exempt | Blocks the deep-gate promotion *and* the binary-retirement question |
| **Deep gate** | Promote `migration_reproducibility_deep` to blocking | One word; it passes today (63 of 66 tables identical); closes the fabrication hole. Must land with D2 or the next fortnightly bot run reddens it |
| **D1** | Branch protection on `main` | Without it every `blocking` level is decorative. Alone, in its own window — never bundled with check promotions |
| **Binary DB** | Stop committing `data/guidebook.db`; make it a build artifact | The 345 SQL migrations are the reviewable form and rebuild it in 15 s. Gated on D2 |

## Two migrations that are free today and never will be again

DR-2026-08-06 §1 promises a walk back to values, sources, **the population served**, and **the
doctrine that governed the judgement**. Two of those four cannot be recorded at all:
`evidence_population_match.target_population` has no FK, and no doctrine column exists anywhere
in the database. **No quantity of rows fixes either.** With every table empty, both migrations
are trivial now.

## Working rules that bit during this session

- **Use a heredoc written to a file for commit messages, and substitute the timestamp before
  writing.** A quoted heredoc (`<<'EOF'`) does not expand `$TS`, and a commit landed with the
  literal string `[TIMESTAMP]`, failing the format check until amended.
- **Re-derive a causal claim, not just a count.** Three times this session a pass reported a real
  defect with a false mechanism. A right conclusion with a wrong cause produces the wrong fix.
- **Check that a check had a subject.** Five of 28 blocking checks declare a vacuity floor.
- **`min_items` is not the remedy for a subject that is empty by ratified decision** — the repo
  adjudicated that on 2026-08-06 and retired a floor it had just added. Use a warranted,
  self-lifting suppression in the shape of `scripts/audit/graph/known_debt.yaml`.

## Outstanding from this session

- A doctrine-lens antagonist pass on pipeline stages 4–6 and 10–12 (logged as a deviation in
  the attestation).
- The migration emitter was never exercised end to end; the sanctioned write path remains
  untested.
- `governance/context-map.yaml` is new — regenerate it, never edit it
  (`python3 scripts/generate/context_map.py`).
