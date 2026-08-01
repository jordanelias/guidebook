# Retired workflows

Origin path for every file here: `.github/workflows/`.

Retired on **2026-08-01** by the ecosystem-tooling consolidation. Preserved rather
than deleted, per CLAUDE.md §9 guardrail 2 (*retire to `_archived/`, mirroring the
origin path — don't delete*). A workflow cannot be redirect-stubbed the way a
document can, because a stub left in `.github/workflows/` would still be executed
by GitHub; moving it here is the equivalent act.

None of this is lost capability. Every check these workflows ran is now declared in
`governance/check-registry.yaml` and invoked by `scripts/run_checks.py`.

| File | Absorbed into | Why |
|---|---|---|
| `audit.yml` | `.github/workflows/ci.yml` (`data`, `attestation` batteries) | Its four jobs duplicated ci.yml's checkout + install and kept a second, separately-maintained list of checks. Its migration-reproducibility heredoc became `scripts/audit/migration_reproducibility.py`. |
| `research-contract.yml` | `.github/workflows/ci.yml` (`research` battery) | Same shape again: a third checkout, a third install, a third check list. Every check it ran is registered, at the same enforcement level it had here. |
| `regenerate-vetting-surface.yml` | `.github/workflows/regenerate-derived.yml` (matrix leg `vetting-surface`) | The three regenerate workflows were byte-for-byte identical apart from generator, staged outputs, commit prefix and trigger paths. |
| `regenerate-evidentiary-audit.yml` | `.github/workflows/regenerate-derived.yml` (matrix leg `evidentiary-audit`) | As above. Its PR-side `check` job moved to ci.yml's `render` battery. |
| `regenerate-pipeline-completeness.yml` | `.github/workflows/regenerate-derived.yml` (matrix leg `pipeline-completeness`) | As above. Its PR-side `check` job moved to ci.yml's `render` battery. |

## What was deliberately NOT consolidated

`resolve-dois.yml` and `verify-urls.yml` stay separate and live. They are the two
channels of the source-verification pipeline: different schedules (weekly vs
bi-weekly), different concurrency groups, different network profiles, different
state tables (`pipeline_runs` vs `url_verification_runs`), and both are the
authoritative writers of tables the reproducibility gate deliberately exempts.
Merging them would mean routing a cron to a specific job via
`github.event.schedule` conditionals — more fragility than the saved duplication
is worth, since they share almost no logic.
