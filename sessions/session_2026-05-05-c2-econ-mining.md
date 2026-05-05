# Session: C2-Skill-Overhaul + Economics Citation Mining (Depth-3)
**Date:** 2026-05-05
**session_close:** 2026-05-05 05:59
**Model:** Sonnet 4.6

## Work completed

### C2 Skill overhaul (Phase 1-C through 1-E complete)

**Skills deprecated (8 + stray .py):**
chunk-assembler, file-splitter, fix-linebreaks, haiku-chunker, vol2-item-formatter,
volii-validator, bulk-renumber, evidence-marker → skills/deprecated/

**Skills rewritten (SQLite-first):**
- citation-miner — inline/batch modes, depth-1 rule, correct CLI signatures
- research-log-manager — clean rewrite, upsert-coverage/language/add-source CLI
- connection-scout — add-connection/update-connection CLI, target column corrected
- bibliography-compiler — evidence_sources schema corrected
- item-specification-writer — SQLite-first sourcing, bpc_metadata corrected

**New skills:**
- question-author, cell-curator, doctrine-recheck

**Skills patched (SQLite register migration):**
multilingual-research, functional-deficit-researcher, economics-researcher,
literature-review-planner, content-gap-analyzer, relational-integrity-checker,
session-consolidator, workplan-orchestrator

**db.py expanded — 9 new CLI subcommands:**
add-gap, close-gap, add-connection, update-connection, unmined,
upsert-coverage, upsert-language, update-bpc, add-source
**4 new Python functions:**
update_bpc_metadata, insert_evidence_source, insert_source_slug_link, get_unmined_for_all_slugs

**Schema errors corrected (bottom-up audit):**
- evidence_sources: surname→authors, evidence_tier→tier, no language/journal cols
- connection_targets: target_type+target_id→single target column
- log-mining --connections: JSON array not comma-delimited string
- is-mined: named flags --slug --ref not positional
- bpc_metadata: opus_synthesis→bpc_complete
- upsert-coverage: no CLI → added to db.py
- upsert-language: no CLI → added to db.py

**Phase 1-D:** validate_cross_refs.py rewritten — loads slugs + CON-IDs from SQLite

**Phase 1-E:** Archive headers added to gap_register.md, connections/_index.md, slug-registry.md

### Economics citation mining (depth-3 authorised override)

**Slugs mined:** economics-sources.md, construction-cost-data.md
**Sources added:** 15 (D1: 7, D2: 6, D3: 2)

**Key new sources:**
- Cockayne 2021 OTIS RCT (PMID 34254934) — COUNTER-FINDING: OT home mod not cost-effective in general 'at-risk' population (UK, NHS HTA)
- Campbell 2005 VIP trial (PMID 16183652) — home safety effective/cost-effective for VIS population specifically (NZ, BMJ)
- Smith & Widiatmoko 1998 (PMID 9659769) — foundational cost model; $172/person/year; cost-saving at 10 years (AU)
- Szanton 2011 CAPABLE pilot (PMID 22091738) — effect sizes confirmed; correct PMID established
- Gathercole 2021 ATTILA (PMID 33755548) — COUNTER-FINDING: full AT package not superior for DEM independent living (UK)
- Robertson 2001 ×2 (PMID 11264206, 11264207) — NZD $155–1,803/fall prevented depending on framing
- Logan 2022 FinCH (PMID 35125131) — £190.62/fall averted; £4,543/QALY care homes (UK)
- Robertson 2001 JECH (PMID 11449021) — NZD $314/fall prevented at 1 year foundational

**Pattern finding:** Counter-findings consistent — home modification economics population-specific.
General 'at-risk' (OTIS) and general DEM AT (ATTILA) show no benefit. High-risk targeted
populations (HAPPI/NZ, VIP, CAPABLE/Medicaid) show strong returns. Supports Mode P / Mode S.

**Erratum:** PMC3157760 cited as Gitlin ABLE RCT is WRONG — resolves to 1985 spinal paper.
Correct Gitlin ABLE citation needs resolution next session.

## Commits this session
- ac1df4ad: deprecate 8 assembly-pipeline skills
- a2ef66be: rewrite 5 + create 3 new skills
- a56ba734: patch 8 skills for SQLite migration
- 677a16fb: fix schema errors in 6 skills (bottom-up audit)
- d82c5672: add 9 CLI subcommands to db.py + sync 3 skills
- a878c4bf: fix research-log-manager corruption
- 34a55841: Phase 1-D/E + LATEST + session file
- 95e0ce2b: economics depth-3 mining — 15 sources + erratum

## next_action
1. Resolve Gitlin ABLE RCT correct PMID/DOI (PubMed query: "Gitlin ABLE functional difficulties home intervention 2006")
2. Mine Ielegems 2024 Belgium cost study reference list (architecture literature — use Scholar Gateway, not PubMed)
3. Mine TERRAGON/DStGB 2017 bibliography (German regulatory source)
4. 131 P2 gaps open — all RES category, multilingual-research passes
5. C3: spec page authoring for stub items (67 items without BPC content)

## blockers
[]

## gaps_status
- OPEN P1: 0
- OPEN P2: 131 (all RES — multilingual-research queued)
- OPEN P3: ~37
