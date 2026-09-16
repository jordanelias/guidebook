# Are we safe to research? — derived 2026-09-16, branch `claude/research-safety-ny8pl0`

Every figure below was derived from the live repo on the date in the heading, with the command that
produced it. Re-derive before relying on any of it (`CLAUDE.md` rule 7). This answer supersedes
`scratchpad/research-capability-status/STATUS.md` (2026-09-12), which was written before the corpus
was cleared and whose figures are all stale.

## VERDICT

**Yes — the research and evidence stages are clear, and nothing blocks starting a batch today.** One
ruled thing is missing from the engine and it sits further down the same walk, at judgment:
**the derived-figure band function is unimplemented**. It bites the first time a re-run meets a source
that states an increment rather than a width — which is exactly what `REF-00976` (AIJ 2004, ">30 cm
enlargement") did the last time this slug was worked.

## What changed since the last answer

The 2026-09-12 answer described a live corpus of 13 sources and two determinations. On 2026-09-13 the
owner ruled the whole circulation corpus untrusted and it was cleared — 229 rows across every stage
(`references/project-standards.md`, entry "the whole circulation corpus is untrusted";
`scripts/migrations/data_20260913040739_2026-09-13-clear-circulation-corpus.sql`). `evidence_sources`,
`source_value_extractions`, `specifications` and `base_parameters` all hold 0 rows today. The clear
followed five owner rulings the same day on how figures are graded and weighed, so the honest reading
is that the doctrine grading the corpus changed under it, not that a specific row was found false.

## The preconditions, each derived

| | State | Derived by |
|---|---|---|
| dependencies | `pydantic` 2.13.5, `jsonschema` 4.26.0 present | `bash .claude/hooks/ensure-deps.sh` |
| governance battery | **RESULT: PASS** — no blocking failure; 10 advisory failures | `python3 scripts/run_checks.py --all` |
| registry coherence | **SELFTEST: PASS** | `python3 scripts/run_checks.py --selftest` |
| `ref_id` minting floor | `next_ref_id` → **REF-00983**; high-water 982 | `dbcore.next_ref_id(conn)` |
| parameter writer | `add-parameter --term-id TERM-002` accepted, `parameter_id` 3, provenance `base-vocabulary` | rehearsed `--dry-run` on a scratch copy |
| search writer | `log-search` accepted | rehearsed `--dry-run` on a scratch copy |
| retrieval reachable | PubMed eutils **200**; Crossref answered (404 on a DOI that does not exist) | `curl` against both |
| quote attribution | `quote_in_artefacts` reports SCOPED vs UNSCOPED rather than claiming a corpus hit proves attribution | `scripts/research/retrieval_log.py:470` |
| ICF lens | `base_icf` 72 codes; all six `icf_code` columns FK into it | migration 081 |
| cron window | next DB-touching scheduled run **Mon 2026-09-21 06:00 UTC** (`resolve-dois`) | `.github/workflows/*.yml` |

**The identifier hazard the clear created is closed.** The clearing ruling's own ACTION was "settle
the `ref_id` minting floor BEFORE admitting the first source, so retired identifiers are not
reissued." `next_ref_id` returns REF-00983, not REF-00971, and `identifier_floor_audit` is green.

**The "a determination has no NUMBER" finding is closed.** `compose_value()`
(`scripts/assess/assess_cell.py:574`) now resolves `value_min`/`value_max`/`value_unit`/`value_note`;
the 2026-09-12 answer recorded them hardcoded `None` and read by nothing.

## Gaps, worst first

1. **The derived-figure band function is unimplemented.** Ruled 2026-09-13: `floor(mean(ordinal(input
   bands)))`, ordinals `●`=3 `◐`=2 `○`=1, inputs equally weighted, with five acceptance rows. No
   ordinal encoding exists: `grep -rn 'ordinal' scripts/ schemas/ governance/` returns only two prose
   hits in `governance/armature_v4*.md`. `db.py derive-extraction` computes the derived row's *value*
   (base + delta) and nothing computes its *band*. The ruling's own implementer note says the encoding
   "has to be introduced with the engine rule, not assumed to be present."
2. **43 of 72 `base_icf` codes carry no title.** `CLAUDE.md` §6 requires ICF codes **and** names.
   Logged as `GAP-ICF-TITLES`; closes by retrieval and persisted bytes, never by recall.
3. **`source_locators_integrity` FAILS: of the 48 `source_locators` titles that embed a DOI, 31 do not
   match the row's own DOI and 17 are unprovable** (550 title-bearing rows examined). Repair is blocked on a
   missing writer — `db.py` cannot set `source_locators.title`. That is the table R9's duplicate-DOI
   pre-check reads, so a re-run cross-files against a register with 31 known-bad titles. The DOI path
   is unaffected.
4. **Seven blocking checks are vacuous and `research_dod` is NON-COMPLIANT for want of a subject.**
   Both are the empty corpus, not a defect: the first source landing gives them something to gate.
   `sessions/LATEST-RESEARCH` still names batch 06, whose rows no longer exist, so
   `citation_mining_session` scopes to a cleared session.
5. **DR-2026-08-19 clause (c) is recorded, not adjudicated.** Its freeze exit was discharged on
   `evidence_sources >= 1`; that count is 0 again and the gate that observed it was deleted. The DR
   says the freeze ended by its own terms — this is not a claim that it revives.
6. **Two owner questions stay open and neither blocks a first batch:** what happens when a determined
   cell meets new evidence (supersession), and whether the medical lens survives the 2026-09-13
   statement "access needs, ICF codes, disability identities".

## The order a re-run has to follow

`base_parameters` is empty, so `specifications.parameter_id` and `source_value_extractions.parameter_id`
— both `NOT NULL` into it — are unwritable until a parameter is minted. `add-parameter --term-id
TERM-002` mints one without needing an adjudication, because TERM-002 is base vocabulary (rehearsed
above). So the batch-07 runbook's step 1 still stands, and the walk is:

    add-parameter -> log-search -> add-source -> observe-term -> add-population-match
      -> add-extraction -> assess_cell

Derive the unwritable set before planning any write (`CLAUDE.md` §4) rather than trusting this list.

**One piece of drift found on the way, small but in the path of this exact question.**
`db.py add-parameter --help` says `--term-id` "must carry a NAMES-NEW/NAMES-EXISTING adjudication".
`insert_parameter` deliberately does not refuse one — its own docstring: *"DELIBERATELY NOT REFUSED: a
term with no adjudication"*, because `term_adjudications` holds 0 rows and the 88 live terms were
seeded months before observe/adjudicate existed. Read literally, the help text says the parameter
layer cannot bootstrap, and it can: the rehearsal above minted `parameter_id` 3 from TERM-002.
