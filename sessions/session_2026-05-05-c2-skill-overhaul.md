# Session: C2-Skill-Overhaul
**Date:** 2026-05-05
**session_close:** 2026-05-05 03:30
**Model:** Sonnet 4.6 (overhaul execution)

## Summary
C2 skill ecosystem overhaul — SQLite integration, citation mining pipeline, db.py CLI expansion, Phase 1-D/E completion.

## Deliverables

### Skills deprecated (→ skills/deprecated/)
chunk-assembler, file-splitter, fix-linebreaks, haiku-chunker, vol2-item-formatter,
volii-validator, bulk-renumber, evidence-marker + stray evidence_auditor_validate.py

### Skills rewritten (SQLite-first)
- citation-miner: inline+batch modes, depth-1, is-mined/log-mining/unmined/update-bpc/add-source CLI
- research-log-manager: upsert-coverage/upsert-language/add-source CLI
- connection-scout: add-connection/update-connection CLI, correct target column
- bibliography-compiler: evidence_sources schema corrected (authors/tier not surname/evidence_tier)
- item-specification-writer: SQLite-first sourcing, bpc_metadata corrected
- workplan-orchestrator: SQLite session-start note
- session-consolidator: SQLite register queries note

### New skills created
- question-author: question_heading atom authoring
- cell-curator: spec×population evidence state classification
- doctrine-recheck: periodic alignment audit

### Skills patched (register references)
multilingual-research, functional-deficit-researcher, economics-researcher,
literature-review-planner, content-gap-analyzer, relational-integrity-checker

### db.py expanded (scripts/db.py)
9 new CLI subcommands: add-gap, close-gap, add-connection, update-connection,
unmined, upsert-coverage, upsert-language, update-bpc, add-source
4 new Python functions: update_bpc_metadata, insert_evidence_source,
insert_source_slug_link, get_unmined_for_all_slugs
Total: 837 lines (was 549)

### Schema errors corrected
- evidence_sources: surname→authors, evidence_tier→tier, no language/journal columns
- connection_targets: target_type+target_id→single target column
- log-mining --connections: JSON array not comma-delimited
- is-mined: named flags --slug --ref not positional
- bpc_metadata: opus_synthesis→bpc_complete

### Phase 1-D complete
validate_cross_refs.py: loads slugs + CON-IDs from SQLite instead of markdown files

### Phase 1-E complete
Archive headers added to: gap_register.md, references/connections/_index.md, references/slug-registry.md

## Commits
- ac1df4ad: deprecate 8 skills + stray .py
- a2ef66be: rewrite 5 + create 3 new skills
- a56ba734: patch 8 skills for SQLite migration
- 677a16fb: fix schema errors in 6 skills
- d82c5672: add 9 CLI subcommands to db.py + sync 3 skills
- a878c4bf: fix research-log-manager corruption
- (this commit): Phase 1-D/E + LATEST update

## next_action
- Run multilingual-research passes on P2 gap items (131 open, all RES category)
- Begin systematic citation mining batch on 607 unmined Tier 1-3 sources
- C3: spec page content authoring for 67 stub items

## blockers
[]
