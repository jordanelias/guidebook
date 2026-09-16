# Executable surface map — scripts/ and .claude/hooks/

Generation date: 2026-09-16. Hand-assembled by a read-only pass; every claim below is
followed by the exact command that produced it. Per rule 7/8, treat any count here as
stale the moment the tree changes again — re-run the commands, don't quote this file.

**Scope:** every `.py` / `.sh` / `.js` file under `scripts/` (98 files) plus the two
`.claude/hooks/*` files (2 files) = 100 files. `scripts/migrations/*.sql` and
`scripts/audit/graph/{known_debt.yaml,schema.sql}` are data/config, not executable, and
are excluded. `tools/*.py` (evidentiary_audit.py, pipeline_completeness.py,
regenerate_vetting_surface.py) are out of scope (not under `scripts/`) but are cited
where a `scripts/` file's caller lives there.

**Method, exactly:**
- File inventory: `find scripts -type f \( -name '*.py' -o -name '*.sh' -o -name '*.js' \) | grep -v __pycache__`
- Registry ground truth: `python3 scripts/run_checks.py --list` (ran clean; pydantic/jsonschema
  already present in this container) plus a structural parse of `governance/check-registry.yaml`'s
  `cmd:` lists (script → check id, including `status: quarantined/retired` entries).
- Caller sweep for "is X uncalled": **`git grep -n "<name>" -- .`** (bypasses `.ignore`,
  per the CRITICAL TRAP) for every candidate, then manually classified each hit as
  live code (import/subprocess), a workflow step, a skill runbook step, or historical
  prose (decisions/ sessions/ scratchpad/ transcripts/ workplan/\_superseded-equivalent —
  i.e. a record of something that WAS run, not an instruction to run it going forward).
  **"No matches outside historical prose" is stated only where the git grep in this
  session actually returned that** — never inferred.
- Two prior architecture documents already ran a materially similar sweep on 2026-09-10:
  `architecture/conformance-schema-findings.md` and `architecture/meta-scripts-spec.md`.
  Their findings are cited where independently re-confirmed in this session (grep run
  again, dates re-checked) — never taken on trust alone. Where re-confirmed, both the
  doc's claim and this session's independent command are given.
- Dates: `git log -1 --format=%ad --date=short -- <path>` for every file (run as one
  batched loop; see raw output above in this session's transcript).

---

## 1. Registered checks — invoked ONLY by `run_checks.py` (58 files, 63 active + 4 quarantined + 1 retired-archived check ids)

`run_checks.py` is confirmed the sole caller of every id below: `.github/workflows/ci.yml`'s
battery jobs all read `python3 scripts/run_checks.py --battery <name> ...`, and
`scripts/preflight.sh` is `cat scripts/preflight.sh` — a thin wrapper calling the same
entry point. No other file was found (git grep, see §4) invoking these scripts directly
except the two exceptions named in §3.

| Script | Check id(s) | Battery | Level | Last touched |
|---|---|---|---|---|
| scripts/ci_helpers/check_utf8_md.py | check_utf8_md | syntax | blocking | 2026-08-11 |
| scripts/ci_helpers/check_json.py | check_json | syntax | blocking | 2026-08-11 |
| scripts/ci_helpers/check_yaml.py | check_yaml | syntax | blocking | 2026-08-11 |
| scripts/validate_bpc.py | validate_bpc | structure | blocking | 2026-08-14 |
| scripts/validate_cross_refs.py | validate_cross_refs | structure | blocking | 2026-08-14 |
| scripts/tests/test_db_integrity.py | test_db_integrity | db_integrity | blocking | 2026-09-13 |
| scripts/audit/migration_reproducibility.py | migration_reproducibility, migration_reproducibility_deep | data | blocking/advisory | 2026-08-28 |
| scripts/audit/source_slug_links_duplicates.py | source_slug_links_duplicates | data | blocking | 2026-08-24 |
| scripts/validate_parameters.py | validate_parameters | data | advisory | 2026-09-10 |
| scripts/audit/readonly_db_open_audit.py | readonly_db_open_audit | data | advisory | 2026-08-14 |
| scripts/audit/db_path_env_audit.py | db_path_env_audit | data | blocking | 2026-08-15 |
| scripts/audit/alias_provenance_audit.py | alias_provenance_audit | data | blocking | 2026-08-21 |
| scripts/audit/citation_mining_completeness.py | citation_mining_session, citation_mining_backlog_t2 | data | blocking/informational | 2026-08-24 |
| scripts/audit/claude_md_spine.py | claude_md_spine | governance | blocking | 2026-09-09 |
| scripts/audit/schema_reference_audit.py | schema_reference_audit | schema | blocking | 2026-08-28 |
| scripts/validate_schema.py | validate_schema_cross_check | schema | advisory | 2026-09-02 |
| scripts/validate_evidence_state.py | validate_evidence_state | schema | blocking | 2026-09-10 |
| scripts/validate_population.py | validate_population | schema | advisory | 2026-08-22 |
| scripts/validate_jurisdiction.py | validate_jurisdiction | schema | blocking | 2026-08-14 |
| scripts/validate_axes.py | validate_axes | schema | blocking | 2026-09-01 |
| scripts/validate_verification_consistency.py | validate_verification_consistency | schema | blocking | 2026-09-10 |
| scripts/audit_evidence_metadata.py | audit_evidence_metadata | schema | advisory | 2026-08-24 |
| scripts/audit/validate_pydantic_schemas.py | validate_pydantic_schemas | schema | advisory (RED, 243 findings per registry text) | 2026-09-13 |
| scripts/audit_adversarial_use.py | audit_adversarial_use | governance | blocking | 2026-08-14 |
| scripts/research/retrieval_log.py | author_fidelity | research | advisory | 2026-09-13 |
| scripts/decision_capture.py | decision_capture | governance | blocking | 2026-08-11 |
| scripts/doctrine_recheck.py | doctrine_recheck | governance | blocking | 2026-08-21 |
| scripts/audit/retired_vocabulary_audit.py | retired_vocabulary | governance | advisory | 2026-09-11 |
| scripts/audit/matrix_consistency.py | matrix_consistency | governance | advisory | 2026-08-14 |
| scripts/audit/pipeline_contract_audit.py | pipeline_contract_audit | governance | advisory | 2026-08-21 |
| scripts/audit/claims_docket.py | claims_docket | governance | advisory | 2026-08-14 |
| scripts/audit/adherence_log_audit.py | attestation_presence, attestation_schema, attestation_evidence, attestation_verdict | attestation | blocking×2/advisory/informational | 2026-09-11 |
| scripts/audit/research_batch_dod.py | research_contract_baseline_ratchet, research_dod_selftest, research_dod | research | blocking×2/advisory | 2026-09-16 — **also invoked directly, see §3** |
| scripts/generate/research_contract_hook.py | research_contract_sync | research | blocking | 2026-09-10 |
| scripts/audit/research_protocol_audit.py | research_protocol_audit | research | advisory | 2026-09-03 |
| scripts/audit/metadata_integrity_audit.py | metadata_integrity_audit | research | advisory | 2026-08-14 |
| scripts/audit/gap_mining_audit.py | gap_mining_audit | research | advisory | 2026-08-14 |
| scripts/audit/population_integrity_audit.py | population_integrity_audit | research | advisory | 2026-09-10 |
| scripts/audit/graph_audit.py | graph_audit | research | advisory | 2026-09-01 |
| scripts/validate_reasoning.py | validate_reasoning | research | advisory | 2026-08-14 |
| scripts/audit/pmp_audit.py | pmp_audit | research | advisory | 2026-08-14 |
| scripts/audit/reasoning_doc_citations_audit.py | reasoning_doc_citations_audit | research | advisory | 2026-08-14 |
| scripts/tests/test_graph_audit.py | test_graph_audit | tests | advisory | 2026-08-11 |
| scripts/tests/test_pipeline_contract.py | test_pipeline_contract | tests | advisory | 2026-08-11 |
| scripts/tests/test_record_command_session.py | test_record_command_session | tests | advisory | 2026-09-03 |
| scripts/tests/test_url_verifier.py | test_url_verifier | tests | advisory | 2026-08-11 |
| scripts/tests/test_verification_pipeline.py | test_verification_pipeline | tests | advisory | 2026-08-24 |
| scripts/tests/test_assess_cell_pilot.py | test_assess_cell_pilot | tests | advisory | 2026-09-13 |
| scripts/tests/test_evidence_cell_state_2_3.py | test_evidence_cell_state_2_3 | tests | advisory | 2026-09-13 |
| scripts/tests/test_validate_evidence_state_2_4.py | test_validate_evidence_state_2_4 | tests | advisory | 2026-09-13 |
| scripts/tests/test_directness_2_2.py | test_directness_2_2 | tests | advisory | 2026-09-10 |
| scripts/generate/context_map.py | context_map_fresh | render | advisory | 2026-08-19 |
| scripts/generate/build_site.py | site_pages_fresh | render | advisory | 2026-09-11 |
| scripts/audit/render_audit.js | render_audit_browser | render | advisory (node) | 2026-08-14 |
| scripts/audit/judgment_handoff_shape.py | judgment_handoff_shape | schema | blocking | 2026-08-27 |
| scripts/audit/extraction_relations_integrity.py | extraction_relations_integrity | db_integrity | blocking | 2026-09-13 |
| scripts/audit/derived_not_curated_audit.py | derived_not_curated_audit | schema | blocking | 2026-09-13 |
| scripts/audit/identifier_floor_audit.py | identifier_floor_audit | db_integrity | blocking | 2026-09-13 |
| scripts/audit/source_locators_integrity.py | source_locators_integrity | data | advisory | 2026-09-11 |
| scripts/audit/derivation_handshake_integrity.py | derivation_handshake_integrity | schema | advisory | 2026-09-13 |
| scripts/audit/medical_lens_integrity.py | medical_lens_integrity | schema | advisory | 2026-09-11 |

**Quarantined / retired** (registered but `run_checks.py --list` confirms they are
**never selected** by `--all`/`--battery`/`--changed-from` — the registry's own text for
each says so, e.g. adjudication_integrity's entry: *"Still quarantined: run_checks.py
never selects it, so it does not gate anything"*):

| Script | Check id | Status | Last touched |
|---|---|---|---|
| scripts/audit/register_integrity_check.py | register_integrity_check | quarantined 2026-09-11, "RED BY CONSTRUCTION" | 2026-09-10 |
| scripts/audit/adjudication_integrity.py | adjudication_integrity | quarantined (re-measured PASS 2026-09-12; promotion is owner-gated on OD-E) | 2026-08-12 |
| scripts/audit/code_currency_audit.py | code_currency_audit | quarantined, "RED" | 2026-08-24 |
| scripts/audit/pre_rehab_banner_audit.py | pre_rehab_banner_audit | quarantined, 6-slug drift | 2026-08-11 |
| _archived/scripts/validate_db.py | validate_db | **retired** 2026-08-15, script physically moved to `_archived/` — not part of the 98-file `scripts/` inventory at all | — |

---

## 2. Shared library modules — imported by other scripts/checks, not run directly

Confirmed live by `git grep -n "^import <mod>\|^from <mod> import"` against the whole tree.

| Module | Imported by | Evidence |
|---|---|---|
| scripts/ci_helpers/repo_files.py | check_json.py, check_utf8_md.py, check_yaml.py | `grep -n repo_files scripts/ci_helpers/check_*.py` — all three import it |
| scripts/ci_helpers/commit_gate.py | check_commit_msg.py:55 | `from commit_gate import is_bot, is_merge` |
| scripts/dbcore.py | 7 files under scripts/ (db.py + 6 audit/validate scripts) | `grep -rn "import dbcore\|from dbcore" scripts/*.py scripts/**/*.py \| wc -l` → 7 |
| scripts/db.py | scripts/audit/medical_lens_integrity.py:39, scripts/validate_parameters.py:57 | `from db import _VALUE_BEARING, _MD_CODE` / `from db import _VALUE_BEARING` |
| scripts/audit/graph/{model,build,extract_db,extract_code,extract_content,extract_contract,topology}.py | scripts/audit/graph_audit.py:50 (`import build as gbuild`, then `gbuild.build()`); the extract_*/topology modules are imported inside build.py:14-19 | Independently confirmed — `graph_audit.py` (a live, registered check) is the driver for the whole `graph/` package. `scripts/audit/graph/__init__.py` is a 3-line comment-only marker; nothing imports the directory as a package (`git grep -n "audit.graph\|from scripts.audit.graph"` → no hits) — harmless but functionally decorative |
| scripts/tests/_baseline_ddl.py | test_evidence_cell_state_2_3.py, test_validate_evidence_state_2_4.py | both `import _baseline_ddl`-style fixtures per registry note |

---

## 3. Direct-invocation defects — a workflow (or hook) calling a check outside `run_checks.py`

CLAUDE.md §8: *"Adding a check means editing `governance/check-registry.yaml` — never a
workflow."* Two live violations of the spirit of that rule found (git grep on every
registered script's basename across `.github/`, `.claude/`, confirmed against the
current file, not the doc's dates):

| Site | What it calls | Why it's a defect |
|---|---|---|
| `.github/workflows/ci.yml:266` — `run: python3 scripts/ci_helpers/check_commit_msg.py` | A commit-format check | `check_commit_msg.py` **is not in `governance/check-registry.yaml` at all** (`grep -n check_commit_msg governance/check-registry.yaml` → no output). CLAUDE.md rule 1 itself documents this as the enforcement mechanism ("Enforced by check_commit_msg.py, push events only (ci.yml:257)") — i.e. the repo's own doctrine ratifies the bypass rather than treating it as a defect, but per §8's literal rule this is exactly "editing a workflow" instead of the registry. **Also stale as cited**: CLAUDE.md says `ci.yml:257`; the job is at line 266 today (`wc -l .github/workflows/ci.yml` → 267 lines total) — a 9-line drift, itself an instance of rule 7 (uncited volatile fact). |
| `.claude/settings.json` `Stop` hook — `python3 scripts/audit/research_batch_dod.py --all` | Three registered check ids' own script, run with `--all` outside `run_checks.py` | This is the harness's own definition-of-done gate, deliberately **non-blocking by design** per the hook's own inline comment ("non-blocking by design, but this session closed non-compliant"). Same shape as the ci.yml case — a registry script invoked from outside `run_checks.py` — but here it's intentional and documented at the point of use, not silent. `architecture/meta-scripts-spec.md` §4.2 L0.1 flags the same site independently ("`.claude/settings.json:68` invoking `scripts/audit/research_batch_dod.py` ... is the one that is genuinely un-gated") — re-confirmed this session against the live `.claude/settings.json` `Stop` block (not `SessionStart` as that doc's line-68 pointer implies; the doc's own line number is stale, the mechanism is real). |

`scripts/resolve_dois.py` (`.github/workflows/resolve-dois.yml`) and `scripts/verify_urls.py`
(`.github/workflows/verify-urls.yml`) are called directly by their workflows too, but these
are **not checks** — they are scheduled DB-writing pipelines (Channel 1/Channel 2 source
verification), never registered, and CLAUDE.md rule 3's own text names this exact
mechanism as the timer that breaks rule 3 on `pipeline_runs`. Not a §8 violation; a
different, already-documented rule-3 exposure.

---

## 4. Confirmed UNCALLED — examined, zero live callers found

For each, `git grep -n "<name>"` was run against the **whole tree** (not `-- scripts/`),
so `.ignore`-hidden dirs (`_archived/`, `sessions/`, `transcripts/`, `workplan/`, etc.)
were searched. Every hit is listed by directory class; "historical prose only" means every
hit without exception falls in `decisions/`, `attestations/`, `sessions/`, `scratchpad/`,
`transcripts/`, `workplan/` (dated before today, describing a session that already
happened) or self-referential (the file mentioning itself).

| Script | Hits outside historical prose | Verdict |
|---|---|---|
| **scripts/audit/rename_insurance.py** | None. `git grep -ln rename_insurance -- .` returns only `architecture/*.md` (doctrine describing the defect), `attestations/decisions_DR-2026-09-01-*.json` (a past session's evidence), `sessions/session_2026-09-01-lens-architecture.md`, and `scratchpad/session_2026-08-27-*` (the session that built it). **No workflow, no skill, no registry entry, no `import`.** | **UNCALLED.** Confirms `architecture/conformance-schema-findings.md` defect #7, independently re-verified this session. |
| **scripts/tests/test_adjudication_integrity.py** | None current. Only hit outside itself: `governance/check-registry.yaml`, and that hit is the registry's **own prose disowning it** — the `adjudication_integrity` entry states verbatim: *"That cull kept this script and its wrapper on the ground that 'test_adjudication_integrity is a LIVE registered check'. It is not, and never was: that id appears in this file only inside this prose."* The repo has **no pytest convention** (`scripts/tests/test_graph_audit.py:7`: "Matches the repo's standalone-script test convention (no pytest)"), so nothing picks this file up implicitly either. Remaining hits are five `workplan/2026-08-{02,11,18,20,22}-*.md` files, all dated before this file's own last commit (2026-08-11) or shortly after — historical planning docs, not live instructions. | **UNCALLED**, and the registry disowns it in its own text. |
| **scripts/generate/room_page.py** | None as a caller. `git grep -ln room_page` hits are: `governance/schema-reference-exemptions.yaml` (an exemption entry, not an invocation), `scripts/generate/build_site.py`'s own docstring (see below), `scripts/audit/graph/extract_code.py` (a selftest fixture example, not a call), and workplan/decision docs. | **UNCALLED, and independently confirmed BROKEN.** `build_site.py`'s own docstring (lines 5-9): *"room_page.py still exists (owner-parked on decision 8) and crashes against the live schema (no `rooms` table)"* — re-confirmed via `governance/schema-reference-exemptions.yaml:24-29`: *"scripts/generate/room_page.py is KNOWN-BROKEN and owner-gated, not a rename casualty... It queries four tables that have never existed in this schema; the live tables are `rooms` and `room_items`... Exempted rather than fixed because fixing it means deciding what the room stratum IS."* **Not silent detritus — the owner already knows and has parked it pending decision 8** — but it has zero callers today and its target tables (plural, phantom) do not exist. |
| **scripts/generate/pilot_renderings.py** | Its symbols (`REGISTER_MAP`, `ROLES`, `tuple_class`) are imported by exactly one file: `scripts/audit/register_integrity_check.py:34`. That check is **quarantined** (§1) — `run_checks.py` never runs it. `governance/check-registry.yaml:1720` independently confirms the same import. No other script, workflow, or skill imports or subprocess-calls `pilot_renderings.py`. | **Called only by dead code.** Its only executable caller is a check that is registered but never selected. If `working/pilot/pilot-renderings.html` (the file `judgment_handoff_shape.py` — a *live, blocking* check — reads) is meant to be kept current, nothing in the automated surface regenerates it: `judgment_handoff_shape.py` was grepped directly for `pilot_renderings` and returned **no hits** — it reads the static HTML, not the generator. |

---

## 5. Called, but the target is gone — a live caller, a dead subject

| Script | Caller | Target that no longer exists | Evidence |
|---|---|---|---|
| **scripts/audit_consolidator.py** | `skills/audit-consolidator_SKILL.md:254` (`python3 scripts/audit_consolidator.py ...` — a real runbook step, Step 8 of `skills/item-audit-pipeline_SKILL.md` per its own frontmatter) | Both skills key everything on `item_code` against the `items` table and `item_audit_runs`. **`items` holds 0 rows and `item_audit_runs` holds 0 rows** (`select count(*) from items` / `from item_audit_runs` against `data/guidebook.db?mode=ro`, this session). CLAUDE.md's own trap section states the item layer was deleted from the DB. `scripts/audit_consolidator.py:70` runs `SELECT * FROM items WHERE item_code=?` — always empty today; `:74` the same against `item_audit_runs`. | Nominally "called" (a skill instructs running it), but every code path through it degenerates: no item row, no run row, and the brief it builds would cite nothing. This is `architecture/conformance-schema-findings.md`'s "N5" plus a second, independent defect (skills pointed at a deleted layer) — the skill files themselves (`skills/audit-consolidator_SKILL.md`, `skills/item-audit-pipeline_SKILL.md`) were last touched 2026-08-15 and 2026-09-13 respectively but never updated for the 2026-09-01 item-layer deletion. |
| **scripts/audit_consolidator.py** (same file, separate finding) | — | Rule 3 (never write `guidebook.db` directly; migrations only) | Independently re-read (not just cited from the doc): `scripts/audit_consolidator.py:248` opens `conn = sqlite3.connect(str(DB_PATH))` — **read-write, not `mode=ro`** — and `:268-272` executes `UPDATE item_audit_runs SET status='COMPLETE', ... WHERE run_id=?` directly, bypassing the sanctioned scratch-copy → `db.py` → `emit_batch_sql.py` → `emit_data_migration.py` → `migrate_db.py` path entirely. Currently inert only because `item_audit_runs` is empty so `run_rec` is always `None` and the `UPDATE` branch never fires — the moment that table gets a row again (e.g. if the item-audit pipeline is revived), this becomes a live rule-3 violation with no refusal in front of it. |
| **scripts/assess/assess_cell.py** | `scripts/tests/test_assess_cell_pilot.py:30` (`from assess_cell import determine`) — its only executable caller | The rule it implements is duplicated, not shared, by the real write path | `scripts/db.py` never imports `assess_cell` (`git grep "^import assess_cell\|from assess_cell import"` finds only the test file). Instead `db.py` re-implements the same G2/G3/G6 grain-classification logic inline, and says so in its own comments: `scripts/db.py:2472` "assess_cell.classify() compares against lowercase literals..."; `:4376` "Mirrors assess_cell.LENS_COLUMNS deliberately"; `:4814,4828` describe a real production incident ("a blank skipped validation") that `assess_cell.validate_parameter()` already handles but `db.py`'s own copy did not. This is rule 5 ("never write the same fact into a second table... point, do not copy") applied to *logic* rather than data — two homes for one rule, one of them (the canonical one, per `architecture/meta-scripts-spec.md` L1.5) reachable only through a test. |

---

## 6. Sanctioned manual CLI tools — no automated caller, and that's correct

These are documented, human/agent-run steps in CLAUDE.md's own write path or governance
process. Absence of an automated caller is the intended design, not detritus — evidenced
by recency of use (fresh migrations landing through 2026-09-13).

| Script | Role | Evidence of live use |
|---|---|---|
| scripts/db.py | Primary write CLI (also a library — see §2) | Data migrations through `data_20260913060346_...sql` |
| scripts/migrate_db.py | Sole writer of `data/guidebook.db`; explicitly allow-listed in `.claude/settings.json` `permissions.allow` | Same |
| scripts/emit_data_migration.py | Write-path step 4/5 | `CLAUDE.md:196` names it; no script imports/subprocesses it (prose-only caller, but it's the documented CLI, not orphaned code) |
| scripts/research/emit_batch_sql.py | Write-path step 3/5 | Same profile as `rename_insurance.py`/`audit_consolidator.py` by caller-count (**zero code callers** — only prose in CLAUDE.md, `.claude/settings.json`'s comment, and three other scripts' *comments*, never an `import`) — but distinguished from §4 because it is the officially named step in an actively-exercised pipeline (batch migrations dated through 2026-09-13 exist that could only have been produced this way), not a retired one-off. Flagged here rather than in §4 for that reason, but the caller-sweep evidence is identical in shape to the confirmed-dead scripts, so treat "manual sanctioned tool" as an assertion resting on CLAUDE.md doctrine, not on a discovered caller. |
| scripts/preflight.sh | Local mirror of CI | `cat scripts/preflight.sh` confirms it is a thin wrapper calling `scripts/run_checks.py`, not a second check list |
| scripts/regenerate_derived.sh | Local mirror of `regenerate-derived.yml` | `.github/workflows/regenerate-derived.yml` does **not** call this script — its `regenerate` job matrix calls `tools/pipeline_completeness.py`, `tools/evidentiary_audit.py`, `tools/regenerate_vetting_surface.py` directly, duplicating (not calling) the same three-tool sequence `regenerate_derived.sh:15-17` runs locally. Low-severity duplication: the shell script's own header says it exists to "mirror CI regenerate-*.yml" for local use, so this looks like intentional parity rather than drift, but it is two hand-kept copies of one sequence and a change to one won't fail CI against the other. |
| scripts/audit/rename_insurance.py, scripts/workflows/anchor-correctness-sweep.js | One-off / on-demand tools | `rename_insurance.py` is genuinely dead (§4). `anchor-correctness-sweep.js` is a **Workflow-tool script** (`export const meta = {...}` — the shape documented by the `workflow-authoring` skill), run on demand through the agent harness's own Workflow tool rather than through git-tracked automation; it produced `audits/anchor-correctness-sweep-2026-07-20.md` and `sessions/session_2026-07-20-anchor-correctness-sweep.md` on its one recorded run. Not found in any `.github/workflows/*.yml` (confirmed — it is not that kind of "workflow" despite the directory name `scripts/workflows/`). No current caller found, but this file's whole invocation model is "run me by hand via the Workflow tool when doing an anchor-correctness sweep," so absence of a git-tracked caller does not mean the same thing here as it does for `rename_insurance.py`. |
| scripts/bootstrap.sh | PAT-gated onboarding for the claude.ai surface | CLAUDE.md §7 explicitly: "Don't run `scripts/bootstrap.sh`." No workflow/script/hook calls it (`git grep -ln bootstrap.sh` → only `CLAUDE.md`, `decisions/PI-update-needed.md`, `governance/project-instructions-v10_14.md`, `governance/retired-vocabulary.yaml`, two `workplan/` files — all prose). Uncalled by design, for a different product surface, not this repo's automation. |
| scripts/preserve_transcripts.py | `.claude/settings.json` `SubagentStop` hook | `python3 "${CLAUDE_PROJECT_DIR:-.}/scripts/preserve_transcripts.py"` — confirmed live hook caller |

---

## 7. Render-surface generators — one gated, one not (coverage gap, not duplication)

| Script | Output | Freshness check registered? |
|---|---|---|
| scripts/generate/build_site.py (imports scripts/generate/spec_page.py) | `site/specs/*.html` (partial — `build_site.py`'s own docstring: drives `site/specs/` only, **not** `site/populations/` 11 files or `site/rooms/` 17 files) | Yes — `site_pages_fresh` (§1) |
| scripts/generate/context_map.py | `governance/context-map.yaml` | Yes — `context_map_fresh` (§1) |
| **scripts/generate_parts.py** | `parts/v10/*.md` — a declared render surface (`governance/check-registry.yaml` `kinds.render.paths` includes `parts/**`) | **No.** Not in the registry under any id, not called by any workflow. `git log -1 --date=short` on the script (2026-08-14) is *after* `parts/v10/part00.md`'s own last commit (2026-08-12) — i.e. the generator changed after its declared output was last regenerated, and nothing would have caught that drift the way `site_pages_fresh` catches `site/` drift. Not a duplicate of `build_site.py` (different surface, markdown book vs. per-page HTML) but the same "DB → rendered book content" job, gated asymmetrically. |

---

## 8. Everything else — imported, tested, or otherwise plainly live

`scripts/dbcore.py`, `scripts/db.py` (§2), the `scripts/audit/graph/*.py` package (§2),
`scripts/ci_helpers/{repo_files,commit_gate}.py` (§2), and every file in §1's two tables
are accounted for. That totals:

- §1 active-check table: 58 distinct scripts
- §1 quarantined table: 4 distinct scripts (the 5th, `validate_db.py`, lives in `_archived/`, outside the 98-file inventory)
- §2: 3 files not already counted (`db.py` and the `graph/` package are already in §1 as
  a registered check's dependency; `repo_files.py` and `commit_gate.py` are net-new)
- §3: `check_commit_msg.py` (net-new)
- §4: 4 files (`rename_insurance.py`, `test_adjudication_integrity.py`, `room_page.py`, `pilot_renderings.py`)
- §5: `audit_consolidator.py`, `assess_cell.py` (net-new; `assess_cell.py`'s test wrapper `test_assess_cell_pilot.py` already counted in §1)
- §6: `migrate_db.py`, `emit_data_migration.py`, `emit_batch_sql.py`, `preflight.sh`, `regenerate_derived.sh`, `anchor-correctness-sweep.js`, `bootstrap.sh`, `preserve_transcripts.py` (net-new)
- §7: `generate_parts.py` (net-new); `build_site.py`, `context_map.py`, `spec_page.py` already counted (§1/§2)
- `resolve_dois.py`, `verify_urls.py` (§3, net-new — scheduled pipelines, tested by `test_verification_pipeline.py`/`test_url_verifier.py` already in §1)
- `.claude/hooks/ensure-deps.sh` — `.claude/settings.json` `SessionStart`, confirmed
- `.claude/hooks/record-command.py` — `.claude/settings.json` `PostToolUse`, confirmed

58 + 4 + 3 + 1 + 4 + 2 + 8 + 1 + 2 + 2 = 85 distinct files positively classified with a
named caller (or named absence of one). The remainder (`spec_page.py` imported by
`build_site.py`; `_baseline_ddl.py` imported by two tests; `research_contract_hook.py`
double-counted between §1 and the SessionStart-hook-index trap check below) fold into
the counts above — **re-derive the exact 98/100 reconciliation with a script before
citing a total in any document that outlives this session**, per rule 7.

---

## 9. Traps specifically checked and found NOT currently violated

- **SessionStart hook index** (CLAUDE.md §7): `.claude/settings.json`'s `SessionStart`
  array has one entry whose `hooks` list is `[printf-contract, ensure-deps.sh]`.
  `scripts/generate/research_contract_hook.py:90,175` reads/writes exactly
  `settings["hooks"]["SessionStart"][0]["hooks"][0]["command"]`, which today is the
  printf block, not `ensure-deps.sh` — i.e. nothing has inserted at index 0 ahead of it.
  Compliant as of this read.
- **`.ignore` blindness**: this report's every "uncalled" claim in §4 was produced with
  `git grep`, not the Grep tool, and each table names the actual hits found in
  `.ignore`-hidden directories rather than asserting silence.

---

## Appendix — full per-file caller/date table (all 98 `scripts/` files + 2 hooks)

Legend: **REG**=registered check (run_checks.py only) · **QUAR**=registered, quarantined
(never selected) · **LIB**=imported module, no independent registry id · **HOOK**=`.claude/settings.json` hook · **WF**=`.github/workflows/*.yml` direct call · **SKILL**=invoked from a `skills/*_SKILL.md` runbook step · **MANUAL**=documented human/agent CLI step, no code caller · **DEAD**=no caller found · **GEN**=render generator (see §7).

| File | Class | Caller | Last touched |
|---|---|---|---|
| scripts/assess/assess_cell.py | LIB/DEAD-in-prod | only scripts/tests/test_assess_cell_pilot.py | 2026-09-13 |
| scripts/audit/adherence_log_audit.py | REG | attestation_* ×4 | 2026-09-11 |
| scripts/audit/adjudication_integrity.py | QUAR | run_checks.py never selects | 2026-08-12 |
| scripts/audit/alias_provenance_audit.py | REG | alias_provenance_audit | 2026-08-21 |
| scripts/audit/citation_mining_completeness.py | REG | citation_mining_session, _backlog_t2 | 2026-08-24 |
| scripts/audit/claims_docket.py | REG | claims_docket | 2026-08-14 |
| scripts/audit/claude_md_spine.py | REG | claude_md_spine | 2026-09-09 |
| scripts/audit/code_currency_audit.py | QUAR | run_checks.py never selects | 2026-08-24 |
| scripts/audit/db_path_env_audit.py | REG | db_path_env_audit | 2026-08-15 |
| scripts/audit/derivation_handshake_integrity.py | REG | derivation_handshake_integrity | 2026-09-13 |
| scripts/audit/derived_not_curated_audit.py | REG | derived_not_curated_audit | 2026-09-13 |
| scripts/audit/extraction_relations_integrity.py | REG | extraction_relations_integrity | 2026-09-13 |
| scripts/audit/gap_mining_audit.py | REG | gap_mining_audit | 2026-08-14 |
| scripts/audit/graph/__init__.py | LIB (decorative) | nothing imports the package form | 2026-08-11 |
| scripts/audit/graph/build.py | LIB | scripts/audit/graph_audit.py:50 | 2026-08-11 |
| scripts/audit/graph/extract_code.py | LIB | scripts/audit/graph/build.py:16 | 2026-08-21 |
| scripts/audit/graph/extract_content.py | LIB | scripts/audit/graph/build.py:17 | 2026-08-14 |
| scripts/audit/graph/extract_contract.py | LIB | scripts/audit/graph/build.py:18 | 2026-08-11 |
| scripts/audit/graph/extract_db.py | LIB | scripts/audit/graph/build.py:15 | 2026-09-01 |
| scripts/audit/graph/model.py | LIB | build.py + all extract_*.py | 2026-08-11 |
| scripts/audit/graph/topology.py | LIB | scripts/audit/graph/build.py:19 | 2026-09-01 |
| scripts/audit/graph_audit.py | REG | graph_audit | 2026-09-01 |
| scripts/audit/identifier_floor_audit.py | REG | identifier_floor_audit | 2026-09-13 |
| scripts/audit/judgment_handoff_shape.py | REG | judgment_handoff_shape | 2026-08-27 |
| scripts/audit/matrix_consistency.py | REG | matrix_consistency | 2026-08-14 |
| scripts/audit/medical_lens_integrity.py | REG | medical_lens_integrity | 2026-09-11 |
| scripts/audit/metadata_integrity_audit.py | REG | metadata_integrity_audit | 2026-08-14 |
| scripts/audit/migration_reproducibility.py | REG | migration_reproducibility, _deep | 2026-08-28 |
| scripts/audit/pipeline_contract_audit.py | REG | pipeline_contract_audit | 2026-08-21 |
| scripts/audit/pmp_audit.py | REG | pmp_audit | 2026-08-14 |
| scripts/audit/population_integrity_audit.py | REG | population_integrity_audit | 2026-09-10 |
| scripts/audit/pre_rehab_banner_audit.py | QUAR | run_checks.py never selects | 2026-08-11 |
| scripts/audit/readonly_db_open_audit.py | REG | readonly_db_open_audit | 2026-08-14 |
| scripts/audit/reasoning_doc_citations_audit.py | REG | reasoning_doc_citations_audit | 2026-08-14 |
| scripts/audit/register_integrity_check.py | QUAR | run_checks.py never selects | 2026-09-10 |
| scripts/audit/rename_insurance.py | **DEAD** | none — see §4 | 2026-08-28 |
| scripts/audit/render_audit.js | REG | render_audit_browser (node) | 2026-08-14 |
| scripts/audit/research_batch_dod.py | REG + HOOK | research_dod*, and `.claude/settings.json` Stop hook directly | 2026-09-16 |
| scripts/audit/research_protocol_audit.py | REG | research_protocol_audit | 2026-09-03 |
| scripts/audit/retired_vocabulary_audit.py | REG | retired_vocabulary | 2026-09-11 |
| scripts/audit/schema_reference_audit.py | REG | schema_reference_audit | 2026-08-28 |
| scripts/audit/source_locators_integrity.py | REG | source_locators_integrity | 2026-09-11 |
| scripts/audit/source_slug_links_duplicates.py | REG | source_slug_links_duplicates | 2026-08-24 |
| scripts/audit/validate_pydantic_schemas.py | REG | validate_pydantic_schemas | 2026-09-13 |
| scripts/audit_adversarial_use.py | REG | audit_adversarial_use | 2026-08-14 |
| scripts/audit_consolidator.py | SKILL/dead-target | skills/audit-consolidator_SKILL.md:254, item-audit-pipeline step 8 — see §5 | 2026-08-15 |
| scripts/audit_evidence_metadata.py | REG | audit_evidence_metadata | 2026-08-24 |
| scripts/bootstrap.sh | MANUAL (do-not-run) | none; CLAUDE.md says don't | 2026-08-11 |
| scripts/ci_helpers/check_commit_msg.py | WF-direct (§3 defect) | .github/workflows/ci.yml:266 | 2026-08-19 |
| scripts/ci_helpers/check_json.py | REG | check_json | 2026-08-11 |
| scripts/ci_helpers/check_utf8_md.py | REG | check_utf8_md | 2026-08-11 |
| scripts/ci_helpers/check_yaml.py | REG | check_yaml | 2026-08-11 |
| scripts/ci_helpers/commit_gate.py | LIB | check_commit_msg.py:55 | 2026-08-11 |
| scripts/ci_helpers/repo_files.py | LIB | check_json/check_utf8_md/check_yaml.py | 2026-08-11 |
| scripts/db.py | MANUAL + LIB | human/skill CLI; imported by medical_lens_integrity.py, validate_parameters.py | 2026-09-16 |
| scripts/dbcore.py | LIB | 7 files under scripts/ | 2026-09-13 |
| scripts/decision_capture.py | REG | decision_capture | 2026-08-11 |
| scripts/doctrine_recheck.py | REG | doctrine_recheck | 2026-08-21 |
| scripts/emit_data_migration.py | MANUAL | write-path step, prose-only callers | 2026-08-19 |
| scripts/generate/build_site.py | REG (GEN) | site_pages_fresh | 2026-09-11 |
| scripts/generate/context_map.py | REG (GEN) | context_map_fresh | 2026-08-19 |
| scripts/generate/pilot_renderings.py | **DEAD (called only by dead code)** | scripts/audit/register_integrity_check.py (quarantined) — see §4 | 2026-09-10 |
| scripts/generate/research_contract_hook.py | REG | research_contract_sync | 2026-09-10 |
| scripts/generate/room_page.py | **DEAD + BROKEN** | none; owner-parked on decision 8 — see §4 | 2026-08-11 |
| scripts/generate/spec_page.py | LIB (GEN) | scripts/generate/build_site.py:122 | 2026-09-01 |
| scripts/generate_parts.py | MANUAL (GEN, ungated) | none automated — see §7 | 2026-08-14 |
| scripts/migrate_db.py | MANUAL | sanctioned DB writer, settings.json allow-list | 2026-08-19 |
| scripts/preflight.sh | MANUAL | wraps run_checks.py | 2026-08-14 |
| scripts/preserve_transcripts.py | HOOK | .claude/settings.json SubagentStop | 2026-09-09 |
| scripts/regenerate_derived.sh | MANUAL | local mirror; workflow duplicates instead of calling it — see §6 | 2026-08-11 |
| scripts/research/emit_batch_sql.py | MANUAL | write-path step 3, prose-only callers | 2026-09-13 |
| scripts/research/retrieval_log.py | REG | author_fidelity | 2026-09-13 |
| scripts/resolve_dois.py | WF-direct (pipeline, not a check) | .github/workflows/resolve-dois.yml | 2026-08-24 |
| scripts/run_checks.py | WF + MANUAL | .github/workflows/ci.yml (all batteries), scripts/preflight.sh | 2026-08-22 |
| scripts/tests/_baseline_ddl.py | LIB | test_evidence_cell_state_2_3.py, test_validate_evidence_state_2_4.py | 2026-09-10 |
| scripts/tests/test_adjudication_integrity.py | **DEAD** | none; registry's own text disowns it — see §4 | 2026-08-11 |
| scripts/tests/test_assess_cell_pilot.py | REG | test_assess_cell_pilot | 2026-09-13 |
| scripts/tests/test_db_integrity.py | REG | test_db_integrity | 2026-09-13 |
| scripts/tests/test_directness_2_2.py | REG | test_directness_2_2 | 2026-09-10 |
| scripts/tests/test_evidence_cell_state_2_3.py | REG | test_evidence_cell_state_2_3 | 2026-09-13 |
| scripts/tests/test_graph_audit.py | REG | test_graph_audit | 2026-08-11 |
| scripts/tests/test_pipeline_contract.py | REG | test_pipeline_contract | 2026-08-11 |
| scripts/tests/test_record_command_session.py | REG | test_record_command_session | 2026-09-03 |
| scripts/tests/test_url_verifier.py | REG | test_url_verifier | 2026-08-11 |
| scripts/tests/test_validate_evidence_state_2_4.py | REG | test_validate_evidence_state_2_4 | 2026-09-13 |
| scripts/tests/test_verification_pipeline.py | REG | test_verification_pipeline | 2026-08-24 |
| scripts/validate_axes.py | REG | validate_axes | 2026-09-01 |
| scripts/validate_bpc.py | REG | validate_bpc | 2026-08-14 |
| scripts/validate_cross_refs.py | REG | validate_cross_refs | 2026-08-14 |
| scripts/validate_evidence_state.py | REG | validate_evidence_state | 2026-09-10 |
| scripts/validate_jurisdiction.py | REG | validate_jurisdiction | 2026-08-14 |
| scripts/validate_parameters.py | REG | validate_parameters | 2026-09-10 |
| scripts/validate_population.py | REG | validate_population | 2026-08-22 |
| scripts/validate_reasoning.py | REG | validate_reasoning | 2026-08-14 |
| scripts/validate_schema.py | REG | validate_schema_cross_check | 2026-09-02 |
| scripts/validate_verification_consistency.py | REG | validate_verification_consistency | 2026-09-10 |
| scripts/verify_urls.py | WF-direct (pipeline, not a check) | .github/workflows/verify-urls.yml | 2026-08-14 |
| scripts/workflows/anchor-correctness-sweep.js | MANUAL (Workflow-tool script) | Claude Code Workflow tool, on demand — not git-tracked automation | 2026-08-11 |
| .claude/hooks/ensure-deps.sh | HOOK | .claude/settings.json SessionStart | 2026-08-25 |
| .claude/hooks/record-command.py | HOOK | .claude/settings.json PostToolUse | 2026-09-03 |

---

## Did-not-examine (be honest about scope)

- `tools/*.py` and `tools/*.html` were read only where a `scripts/` file's caller pointed
  there (regenerate-derived.yml, regenerate_derived.sh). Not independently audited.
- Content/correctness of what each script does when run (e.g. whether `spec_page.py`
  produces anything meaningful given `items`=0 rows) is a currency question, not a
  caller question — flagged where it surfaced (§5, §7) but not exhaustively re-derived
  for every registered check.
- `architecture/meta-scripts-spec.md`'s proposed `scripts/meta/l0.py` / `l1.py` do not
  exist (`find . -name 'l0.py' -o -name 'l1.py'` → nothing under `scripts/`) — that
  document is a spec, not shipped code; not counted anywhere above.
