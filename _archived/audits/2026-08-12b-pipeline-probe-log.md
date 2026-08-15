# Pipeline probe log — AGONIST full-direction probe
Generated 2026-08-12 08:35:27Z. Subject: atomic snapshot `probe.db` of the WORKING-TREE `data/guidebook.db`; repo HEAD `84cdac0+dirty` (the working tree carried uncommitted changes, so the DB read here is NOT the one at that commit; the repo received two data commits MID-SESSION — 7a7bebe evidence-stage clear, 6dd0cd3 source_locators recovery — so every sweep reads this one snapshot; the canonical file was only ever opened read-only, for copying).
Schema: 67 user tables (42 empty), 18 views, 0 triggers, PRAGMA user_version as committed.
Denominators (live-derived from the snapshot): **80 FK edges** (62 NOT NULL/PK, 18 nullable) · **128 CHECK clauses** · **268 non-PK NOT NULL columns** · **5 UNIQUE indexes** → rejectable-write surface = 481. (The independently verified pre-054 denominators were 80/127/267/5 = 479; migration 054 added source_locators: +1 CHECK, +1 NOT NULL.)

Verdict legend: `OK` correct behaviour · `ERROR` defect/unexpected failure · `ORPHAN` dangling rows/joints found · `BLOCKED` probe could not isolate the target (counts toward Examined, not toward Passed) · `FAILED-WRITE` a sanctioned write failed · **`SILENT-PASS`** a write that should have been rejected and was accepted.


---

## SWEEP A — schema connectivity, both directions

### A1 — full FK edge list (PRAGMA foreign_key_list per table)
| # | child table | child col | parent table | parent col | on_delete | child col nullable |
|---|---|---|---|---|---|---|
| 1 | `access_need_axis_map` | `axis_code` | `axes` | `axis_code` | NO ACTION | no |
| 2 | `access_need_axis_map` | `need_code` | `access_needs` | `need_code` | NO ACTION | no |
| 3 | `access_need_icf` | `need_code` | `access_needs` | `need_code` | NO ACTION | no |
| 4 | `bpc_metadata` | `slug` | `slugs` | `slug` | NO ACTION | no |
| 5 | `case_studies` | `slug` | `slugs` | `slug` | NO ACTION | no |
| 6 | `case_study_outcomes` | `case_study_id` | `case_studies` | `case_study_id` | NO ACTION | no |
| 7 | `case_study_populations` | `population_code` | `populations` | `population_code` | NO ACTION | no |
| 8 | `case_study_populations` | `case_study_id` | `case_studies` | `case_study_id` | NO ACTION | no |
| 9 | `case_study_specs` | `item_code` | `items` | `item_code` | NO ACTION | no |
| 10 | `case_study_specs` | `case_study_id` | `case_studies` | `case_study_id` | NO ACTION | no |
| 11 | `case_study_strategies` | `case_study_id` | `case_studies` | `case_study_id` | NO ACTION | no |
| 12 | `citation_mining` | `global_ref_id` | `evidence_sources` | `ref_id` | NO ACTION | YES — NULL-bypassable |
| 13 | `citation_mining` | `slug` | `slugs` | `slug` | NO ACTION | no |
| 14 | `citation_population_links` | `population_code` | `populations` | `population_code` | NO ACTION | no |
| 15 | `citation_population_links` | `citation_id` | `reasoning_doc_citations` | `citation_id` | NO ACTION | no |
| 16 | `conflicts` | `item_code` | `items` | `item_code` | NO ACTION | YES — NULL-bypassable |
| 17 | `connection_targets` | `con_id` | `connections` | `con_id` | NO ACTION | no |
| 18 | `economics_entries` | `ref_id` | `evidence_sources` | `ref_id` | NO ACTION | YES — NULL-bypassable |
| 19 | `economics_entry_populations` | `population_code` | `populations` | `population_code` | NO ACTION | no |
| 20 | `economics_entry_populations` | `entry_id` | `economics_entries` | `entry_id` | NO ACTION | no |
| 21 | `economics_entry_specs` | `item_code` | `items` | `item_code` | NO ACTION | no |
| 22 | `economics_entry_specs` | `entry_id` | `economics_entries` | `entry_id` | NO ACTION | no |
| 23 | `evidence_population_match` | `gap_id` | `gaps` | `gap_id` | NO ACTION | YES — NULL-bypassable |
| 24 | `evidence_population_match` | `ref_id` | `evidence_sources` | `ref_id` | NO ACTION | YES — NULL-bypassable |
| 25 | `evidence_source_authors` | `ref_id` | `evidence_sources` | `ref_id` | NO ACTION | no |
| 26 | `extraction_population_links` | `population_code` | `populations` | `population_code` | NO ACTION | no |
| 27 | `extraction_population_links` | `extraction_id` | `source_value_extractions` | `extraction_id` | NO ACTION | no |
| 28 | `gap_mining` | `gap_id` | `gaps` | `gap_id` | NO ACTION | no |
| 29 | `item_audit_runs` | `item_code` | `items` | `item_code` | NO ACTION | no |
| 30 | `item_axis_links` | `axis_code` | `axes` | `axis_code` | NO ACTION | no |
| 31 | `item_axis_links` | `item_code` | `items` | `item_code` | NO ACTION | no |
| 32 | `item_bpc_links` | `slug` | `slugs` | `slug` | NO ACTION | no |
| 33 | `item_bpc_links` | `item_code` | `items` | `item_code` | NO ACTION | no |
| 34 | `item_population_elaborations` | `evidence_ref_id` | `evidence_sources` | `ref_id` | NO ACTION | YES — NULL-bypassable |
| 35 | `item_population_elaborations` | `population_code` | `populations` | `population_code` | NO ACTION | no |
| 36 | `item_population_elaborations` | `item_code` | `items` | `item_code` | CASCADE | no |
| 37 | `item_population_links` | `item_code` | `items` | `item_code` | CASCADE | no |
| 38 | `item_population_links` | `population_code` | `populations` | `population_code` | NO ACTION | no |
| 39 | `items` | `bpc_source_slug` | `slugs` | `slug` | NO ACTION | YES — NULL-bypassable |
| 40 | `jurisdictional_values` | `item_code` | `items` | `item_code` | NO ACTION | no |
| 41 | `population_axis_map` | `axis_code` | `axes` | `axis_code` | NO ACTION | no |
| 42 | `population_axis_map` | `population_code` | `populations` | `population_code` | NO ACTION | no |
| 43 | `populations` | `parent_code` | `populations` | `population_code` | NO ACTION | YES — NULL-bypassable |
| 44 | `probe_population_links` | `population_code` | `populations` | `population_code` | NO ACTION | no |
| 45 | `probe_population_links` | `probe_id` | `spec_value_probes` | `probe_id` | NO ACTION | no |
| 46 | `reasoning_doc_citations` | `source_ref_id` | `evidence_sources` | `ref_id` | NO ACTION | no |
| 47 | `reasoning_doc_citations` | `reasoning_doc_slug` | `slugs` | `slug` | NO ACTION | no |
| 48 | `room_items` | `item_code` | `items` | `item_code` | NO ACTION | no |
| 49 | `room_items` | `room_code` | `rooms` | `room_code` | NO ACTION | no |
| 50 | `search_admissions` | `ref_id` | `evidence_sources` | `ref_id` | NO ACTION | no |
| 51 | `search_admissions` | `exec_id` | `search_executions` | `exec_id` | NO ACTION | no |
| 52 | `search_candidates` | `suggested_slug` | `slugs` | `slug` | NO ACTION | YES — NULL-bypassable |
| 53 | `search_candidates` | `found_under_slug` | `slugs` | `slug` | NO ACTION | no |
| 54 | `search_candidates` | `exec_id` | `search_executions` | `exec_id` | NO ACTION | YES — NULL-bypassable |
| 55 | `search_coverage` | `slug` | `slugs` | `slug` | NO ACTION | no |
| 56 | `search_executions` | `slug` | `slugs` | `slug` | NO ACTION | no |
| 57 | `search_languages` | `slug` | `slugs` | `slug` | NO ACTION | no |
| 58 | `slugs` | `merged_into` | `slugs` | `slug` | NO ACTION | YES — NULL-bypassable |
| 59 | `source_slug_links` | `slug` | `slugs` | `slug` | NO ACTION | no |
| 60 | `source_slug_links` | `ref_id` | `evidence_sources` | `ref_id` | NO ACTION | no |
| 61 | `source_value_extractions` | `promoted_to_rdc_id` | `reasoning_doc_citations` | `citation_id` | NO ACTION | YES — NULL-bypassable |
| 62 | `source_value_extractions` | `population_code` | `populations` | `population_code` | NO ACTION | YES — NULL-bypassable |
| 63 | `source_value_extractions` | `ref_id` | `evidence_sources` | `ref_id` | NO ACTION | no |
| 64 | `source_value_extractions` | `item_code` | `items` | `item_code` | NO ACTION | YES — NULL-bypassable |
| 65 | `source_value_extractions` | `root_ref_id` | `evidence_sources` | `ref_id` | NO ACTION | YES — NULL-bypassable |
| 66 | `source_value_extractions` | `slug` | `slugs` | `slug` | NO ACTION | no |
| 67 | `spec_value_probes` | `ref_id` | `evidence_sources` | `ref_id` | NO ACTION | YES — NULL-bypassable |
| 68 | `spec_value_probes` | `item_code` | `items` | `item_code` | NO ACTION | no |
| 69 | `spec_value_probes` | `slug` | `slugs` | `slug` | NO ACTION | no |
| 70 | `specification_source_links` | `ref_id` | `evidence_sources` | `ref_id` | NO ACTION | no |
| 71 | `specification_source_links` | `specification_id` | `specifications` | `specification_id` | NO ACTION | no |
| 72 | `specifications` | `gap_register_id` | `gaps` | `gap_id` | NO ACTION | YES — NULL-bypassable |
| 73 | `specifications` | `convergence_id` | `convergence_assessment` | `convergence_id` | NO ACTION | YES — NULL-bypassable |
| 74 | `specifications` | `population_code` | `populations` | `population_code` | NO ACTION | no |
| 75 | `specifications` | `item_code` | `items` | `item_code` | NO ACTION | no |
| 76 | `supersession_check` | `ref_id` | `evidence_sources` | `ref_id` | NO ACTION | no |
| 77 | `supersession_check` | `slug` | `slugs` | `slug` | NO ACTION | no |
| 78 | `term_aliases` | `term_id` | `terms` | `term_id` | NO ACTION | no |
| 79 | `term_item_links` | `item_code` | `items` | `item_code` | NO ACTION | no |
| 80 | `term_item_links` | `term_id` | `terms` | `term_id` | NO ACTION | no |

### [0001] A1 — all tables   `2026-08-12 08:35:27Z`
**Action:** Enumerate FK edges via PRAGMA foreign_key_list over 67 user tables
**Expected:** complete edge list
**Actual:** 80 FK edges, all single-column; 18 on NULLABLE columns (NULL-bypassable); DEFERRABLE clauses present in: []
**Verdict:** `OK`

### [0002] A2 — canonical DB   `2026-08-12 08:35:27Z`
**Action:** PRAGMA foreign_key_check (whole DB)
**Expected:** 0 violations
**Actual:** 0 violations
**Verdict:** `OK`

### [0003] A2 — scripts/migrate_db.py:161   `2026-08-12 08:35:27Z`
**Action:** compare the code comment '~18 pre-existing violations' against reality
**Expected:** comment matches the DB
**Actual:** comment claims '~18 violations' of production drift; PRAGMA foreign_key_check returns 0. The comment is STALE — the tolerance it justifies (only NEW violations fail an apply) remains in the code
**Verdict:** `ERROR`

### [0004] A2 — access_need_axis_map.axis_code → axes   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0005] A2 — access_need_axis_map.need_code → access_needs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0006] A2 — access_need_icf.need_code → access_needs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0007] A2 — bpc_metadata.slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0008] A2 — case_studies.slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0009] A2 — case_study_outcomes.case_study_id → case_studies   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0010] A2 — case_study_populations.population_code → populations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0011] A2 — case_study_populations.case_study_id → case_studies   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0012] A2 — case_study_specs.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0013] A2 — case_study_specs.case_study_id → case_studies   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0014] A2 — case_study_strategies.case_study_id → case_studies   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0015] A2 — citation_mining.global_ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0016] A2 — citation_mining.slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0017] A2 — citation_population_links.population_code → populations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0018] A2 — citation_population_links.citation_id → reasoning_doc_citations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0019] A2 — conflicts.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0020] A2 — connection_targets.con_id → connections   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0021] A2 — economics_entries.ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0022] A2 — economics_entry_populations.population_code → populations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0023] A2 — economics_entry_populations.entry_id → economics_entries   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0024] A2 — economics_entry_specs.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0025] A2 — economics_entry_specs.entry_id → economics_entries   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0026] A2 — evidence_population_match.gap_id → gaps   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0027] A2 — evidence_population_match.ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0028] A2 — evidence_source_authors.ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0029] A2 — extraction_population_links.population_code → populations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0030] A2 — extraction_population_links.extraction_id → source_value_extractions   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0031] A2 — gap_mining.gap_id → gaps   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0032] A2 — item_audit_runs.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0033] A2 — item_axis_links.axis_code → axes   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0034] A2 — item_axis_links.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0035] A2 — item_bpc_links.slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0036] A2 — item_bpc_links.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0037] A2 — item_population_elaborations.evidence_ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0038] A2 — item_population_elaborations.population_code → populations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0039] A2 — item_population_elaborations.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0040] A2 — item_population_links.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0041] A2 — item_population_links.population_code → populations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0042] A2 — items.bpc_source_slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0043] A2 — jurisdictional_values.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0044] A2 — population_axis_map.axis_code → axes   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0045] A2 — population_axis_map.population_code → populations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0046] A2 — populations.parent_code → populations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0047] A2 — probe_population_links.population_code → populations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0048] A2 — probe_population_links.probe_id → spec_value_probes   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0049] A2 — reasoning_doc_citations.source_ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0050] A2 — reasoning_doc_citations.reasoning_doc_slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0051] A2 — room_items.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0052] A2 — room_items.room_code → rooms   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0053] A2 — search_admissions.ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0054] A2 — search_admissions.exec_id → search_executions   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0055] A2 — search_candidates.suggested_slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0056] A2 — search_candidates.found_under_slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0057] A2 — search_candidates.exec_id → search_executions   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0058] A2 — search_coverage.slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0059] A2 — search_executions.slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0060] A2 — search_languages.slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0061] A2 — slugs.merged_into → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0062] A2 — source_slug_links.slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0063] A2 — source_slug_links.ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0064] A2 — source_value_extractions.promoted_to_rdc_id → reasoning_doc_citations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0065] A2 — source_value_extractions.population_code → populations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0066] A2 — source_value_extractions.ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0067] A2 — source_value_extractions.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0068] A2 — source_value_extractions.root_ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0069] A2 — source_value_extractions.slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0070] A2 — spec_value_probes.ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0071] A2 — spec_value_probes.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0072] A2 — spec_value_probes.slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0073] A2 — specification_source_links.ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0074] A2 — specification_source_links.specification_id → specifications   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0075] A2 — specifications.gap_register_id → gaps   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0076] A2 — specifications.convergence_id → convergence_assessment   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0077] A2 — specifications.population_code → populations   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0078] A2 — specifications.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0079] A2 — supersession_check.ref_id → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0080] A2 — supersession_check.slug → slugs   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0081] A2 — term_aliases.term_id → terms   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0082] A2 — term_item_links.item_code → items   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0083] A2 — term_item_links.term_id → terms   `2026-08-12 08:35:27Z`
**Action:** LEFT JOIN orphan query
**Expected:** 0 orphans
**Actual:** 0 orphans
**Verdict:** `OK`

### [0084] A2 — canonical DB — mid-session change of subject   `2026-08-12 08:35:27Z`
**Action:** compare row counts observed at session start against the current canonical
**Expected:** stable subject
**Actual:** TWO commits landed in the repo DURING this probe session: 7a7bebe ('clear all evidence-stage data; preserve schema for repopulation', 05:15Z) cleared item_population_elaborations (3 rows), pipeline_runs (6), url_verification_runs (5), items.pmp_* residue, 75 jurisdictional_values values and sqlite_sequence marks; 6dd0cd3 ('recover 835 document locators from the pre-reset corpus', 05:19Z) added the source_locators table (835 rows, user_version 53→54, +1 CHECK, +1 NOT NULL). This run's snapshot postdates both; all sweeps read the snapshot atomically
**Verdict:** `OK`

### [0085] A2 — item_population_elaborations.evidence_ref_id (live NULL-bypass)   `2026-08-12 08:35:27Z`
**Action:** check whether live data takes the NULL path around a declared FK
**Expected:** rows carry provenance
**Actual:** post-clear: 0 rows (0 NULL). PRE-clear (verified at session start, before commit 7a7bebe): 3 rows, ALL 3 with evidence_ref_id NULL against an EMPTY evidence_sources parent — live data had already taken the NULL-bypass path this sweep demonstrates synthetically in A3b. The clearing commit removed the rows; the structural hole remains (see A3b seq for this edge)
**Verdict:** `ORPHAN`

### [0086] A2 — evidence_population_match.source_ref →(undeclared) evidence_sources   `2026-08-12 08:35:27Z`
**Action:** orphan query on a reference column that has NO declared FK
**SQL:**
```sql
SELECT m.match_id, m.source_ref FROM evidence_population_match m LEFT JOIN evidence_sources s ON m.source_ref = s.ref_id WHERE m.source_ref IS NOT NULL AND s.ref_id IS NULL
```
**Expected:** 0 dangling
**Actual:** 0 dangling: []
**Verdict:** `OK`

### [0087] A2 — evidence_population_match.target_population →(undeclared) populations   `2026-08-12 08:35:27Z`
**Action:** orphan query on a reference column that has NO declared FK
**SQL:**
```sql
SELECT m.match_id, m.target_population FROM evidence_population_match m LEFT JOIN populations p ON m.target_population = p.population_code WHERE m.target_population IS NOT NULL AND p.population_code IS NULL
```
**Expected:** 0 dangling
**Actual:** 0 dangling: []
**Verdict:** `OK`

### [0088] A2 — source_value_extractions.echo_of →(undeclared) source_value_extractions   `2026-08-12 08:35:27Z`
**Action:** orphan query on a reference column that has NO declared FK
**SQL:**
```sql
SELECT e.extraction_id, e.echo_of FROM source_value_extractions e LEFT JOIN source_value_extractions p ON CAST(e.echo_of AS INTEGER) = p.extraction_id WHERE e.echo_of IS NOT NULL AND p.extraction_id IS NULL
```
**Expected:** 0 dangling
**Actual:** 0 dangling: []
**Verdict:** `OK`

### [0089] A2 — specifications.governing_refs (JSON) → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** every ref named in the JSON array must exist in evidence_sources (no FK can enforce a JSON payload)
**SQL:**
```sql
SELECT t.rowid, j.value FROM specifications t, json_each(t.governing_refs) j LEFT JOIN evidence_sources s ON j.value = s.ref_id WHERE t.governing_refs IS NOT NULL AND s.ref_id IS NULL
```
**Expected:** 0 dangling
**Actual:** 0 dangling ref(s): []
**Verdict:** `OK`

### [0090] A2 — search_executions.admitted_ref_ids (JSON) → evidence_sources   `2026-08-12 08:35:27Z`
**Action:** every ref named in the JSON array must exist in evidence_sources (no FK can enforce a JSON payload)
**SQL:**
```sql
SELECT t.rowid, j.value FROM search_executions t, json_each(t.admitted_ref_ids) j LEFT JOIN evidence_sources s ON j.value = s.ref_id WHERE t.admitted_ref_ids IS NOT NULL AND s.ref_id IS NULL
```
**Expected:** 0 dangling
**Actual:** 0 dangling ref(s): []
**Verdict:** `OK`

### A3 — bad-value FK probes, `PRAGMA foreign_keys=ON` (80/80 edges)

### [0091] A3 — access_need_axis_map.axis_code → axes.axis_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "access_need_axis_map" ("axis_code", "need_code", "relationship") VALUES (?, ?, ?)  -- {"axis_code": "PROBE-NO-SUCH-PARENT-1", "need_code": "A-AT", "relationship": "primary"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0092] A3 — access_need_axis_map.need_code → access_needs.need_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "access_need_axis_map" ("need_code", "axis_code", "relationship") VALUES (?, ?, ?)  -- {"need_code": "PROBE-NO-SUCH-PARENT-2", "axis_code": "AX-AMB", "relationship": "primary"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0093] A3 — access_need_icf.need_code → access_needs.need_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "access_need_icf" ("need_code", "icf_code", "icf_type", "confidence") VALUES (?, ?, ?, ?)  -- {"need_code": "PROBE-NO-SUCH-PARENT-3", "icf_code": "PROBE-ICF_CODE", "icf_type": "b", "confidence": "confirmed"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0094] A3 — bpc_metadata.slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-4", "population": "PROBE-POPULATION", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0095] A3 — case_studies.slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "case_studies" ("slug", "case_study_id", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-5", "case_study_id": "PROBE-CASE_STUDY_ID", "title": "PROBE-TITLE", "building_type": "PROBE-BUILDING_TYPE", "location": "PROBE-LOCATION", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0096] A3 — case_study_outcomes.case_study_id → case_studies.case_study_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "case_study_outcomes" ("case_study_id", "metric") VALUES (?, ?)  -- {"case_study_id": "PROBE-NO-SUCH-PARENT-6", "metric": "PROBE-METRIC"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0097] A3 — case_study_populations.population_code → populations.population_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "case_study_populations" ("population_code", "case_study_id") VALUES (?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-7", "case_study_id": "PROBE-CASE_STUDY_ID"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0098] A3 — case_study_populations.case_study_id → case_studies.case_study_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "case_study_populations" ("case_study_id", "population_code") VALUES (?, ?)  -- {"case_study_id": "PROBE-NO-SUCH-PARENT-8", "population_code": "ADHD"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0099] A3 — case_study_specs.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "case_study_specs" ("item_code", "case_study_id") VALUES (?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-9", "case_study_id": "PROBE-CASE_STUDY_ID"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0100] A3 — case_study_specs.case_study_id → case_studies.case_study_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "case_study_specs" ("case_study_id", "item_code") VALUES (?, ?)  -- {"case_study_id": "PROBE-NO-SUCH-PARENT-10", "item_code": "A-01"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0101] A3 — case_study_strategies.case_study_id → case_studies.case_study_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "case_study_strategies" ("case_study_id", "strategy") VALUES (?, ?)  -- {"case_study_id": "PROBE-NO-SUCH-PARENT-11", "strategy": "PROBE-STRATEGY"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0102] A3 — citation_mining.global_ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "citation_mining" ("global_ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"global_ref_id": "PROBE-NO-SUCH-PARENT-12", "slug": "aac-speech-production-environments", "local_ref_id": "PROBE-LOCAL_REF_ID", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0103] A3 — citation_mining.slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-13", "local_ref_id": "PROBE-LOCAL_REF_ID", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0104] A3 — citation_population_links.population_code → populations.population_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "citation_population_links" ("population_code", "citation_id") VALUES (?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-14", "citation_id": "PROBE-PK-15"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0105] A3 — citation_population_links.citation_id → reasoning_doc_citations.citation_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "citation_population_links" ("citation_id", "population_code") VALUES (?, ?)  -- {"citation_id": "PROBE-NO-SUCH-PARENT-17", "population_code": "ADHD"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0106] A3 — conflicts.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "conflicts" ("item_code", "conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-18", "conflict_id": "PROBE-PK-19", "domain": "PROBE-DOMAIN", "pop_a": "PROBE-POP_A", "pop_b": "PROBE-POP_B", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0107] A3 — connection_targets.con_id → connections.con_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "connection_targets" ("con_id", "target") VALUES (?, ?)  -- {"con_id": "PROBE-NO-SUCH-PARENT-20", "target": "PROBE-TARGET"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0108] A3 — economics_entries.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("ref_id", "entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-21", "entry_id": "PROBE-ENTRY_ID", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-SOURCE", "finding": "PROBE-FINDING", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0109] A3 — economics_entry_populations.population_code → populations.population_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entry_populations" ("population_code", "entry_id") VALUES (?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-22", "entry_id": "PROBE-ENTRY_ID"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0110] A3 — economics_entry_populations.entry_id → economics_entries.entry_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entry_populations" ("entry_id", "population_code") VALUES (?, ?)  -- {"entry_id": "PROBE-NO-SUCH-PARENT-23", "population_code": "ADHD"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0111] A3 — economics_entry_specs.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entry_specs" ("item_code", "entry_id") VALUES (?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-24", "entry_id": "PROBE-ENTRY_ID"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0112] A3 — economics_entry_specs.entry_id → economics_entries.entry_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entry_specs" ("entry_id", "item_code") VALUES (?, ?)  -- {"entry_id": "PROBE-NO-SUCH-PARENT-25", "item_code": "A-01"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0113] A3 — evidence_population_match.gap_id → gaps.gap_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("gap_id", "match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-NO-SUCH-PARENT-26", "match_id": "PROBE-PK-27", "source_ref": "PROBE-SOURCE_REF", "target_population": "PROBE-TARGET_POPULATION", "match_grade": "EXACT", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0114] A3 — evidence_population_match.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("ref_id", "match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-28", "match_id": "PROBE-PK-29", "source_ref": "PROBE-SOURCE_REF", "target_population": "PROBE-TARGET_POPULATION", "match_grade": "EXACT", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0115] A3 — evidence_source_authors.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_source_authors" ("ref_id", "position") VALUES (?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-30", "position": 1}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0116] A3 — extraction_population_links.population_code → populations.population_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "extraction_population_links" ("population_code", "extraction_id") VALUES (?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-31", "extraction_id": 1}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0117] A3 — extraction_population_links.extraction_id → source_value_extractions.extraction_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "extraction_population_links" ("extraction_id", "population_code") VALUES (?, ?)  -- {"extraction_id": 999999933, "population_code": "ADHD"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0118] A3 — gap_mining.gap_id → gaps.gap_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-NO-SUCH-PARENT-34", "attempt_at": "PROBE-ATTEMPT_AT", "attempted_by_session": "PROBE-ATTEMPTED_BY_SESSION", "search_strategy_record": "PROBE-SEARCH_STRATEGY_RECORD", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-DISCOVERIES_LOGGED"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0119] A3 — item_audit_runs.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("item_code", "run_id", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-35", "run_id": "PROBE-PK-36", "session": "PROBE-SESSION", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0120] A3 — item_axis_links.axis_code → axes.axis_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "item_axis_links" ("axis_code", "item_code") VALUES (?, ?)  -- {"axis_code": "PROBE-NO-SUCH-PARENT-37", "item_code": "A-01"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0121] A3 — item_axis_links.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "item_axis_links" ("item_code", "axis_code") VALUES (?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-38", "axis_code": "AX-AMB"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0122] A3 — item_bpc_links.slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "item_bpc_links" ("slug", "item_code", "link_type", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-39", "item_code": "A-01", "link_type": "primary", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0123] A3 — item_bpc_links.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "item_bpc_links" ("item_code", "slug", "link_type", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-40", "slug": "aac-speech-production-environments", "link_type": "primary", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0124] A3 — item_population_elaborations.evidence_ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("evidence_ref_id", "item_code", "population_code") VALUES (?, ?, ?)  -- {"evidence_ref_id": "PROBE-NO-SUCH-PARENT-41", "item_code": "A-01", "population_code": "ADHD"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0125] A3 — item_population_elaborations.population_code → populations.population_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("population_code", "item_code") VALUES (?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-42", "item_code": "A-01"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0126] A3 — item_population_elaborations.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("item_code", "population_code") VALUES (?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-43", "population_code": "ADHD"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0127] A3 — item_population_links.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "item_population_links" ("item_code", "population_code", "subtype") VALUES (?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-44", "population_code": "ADHD", "subtype": "PROBE-PK-45"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0128] A3 — item_population_links.population_code → populations.population_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "item_population_links" ("population_code", "item_code", "subtype") VALUES (?, ?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-46", "item_code": "A-01", "subtype": "PROBE-PK-47"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0129] A3 — items.bpc_source_slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "items" ("bpc_source_slug", "item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"bpc_source_slug": "PROBE-NO-SUCH-PARENT-48", "item_code": "PROBE-PK-49", "category": "A", "name": "PROBE-NAME", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0130] A3 — jurisdictional_values.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "jurisdictional_values" ("item_code", "jurisdiction") VALUES (?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-50", "jurisdiction": "PROBE-JURISDICTION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0131] A3 — population_axis_map.axis_code → axes.axis_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "population_axis_map" ("axis_code", "population_code", "role") VALUES (?, ?, ?)  -- {"axis_code": "PROBE-NO-SUCH-PARENT-51", "population_code": "ADHD", "role": "ALIAS"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0132] A3 — population_axis_map.population_code → populations.population_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "population_axis_map" ("population_code", "axis_code", "role") VALUES (?, ?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-52", "axis_code": "AX-AMB", "role": "ALIAS"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0133] A3 — populations.parent_code → populations.population_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "populations" ("parent_code", "population_code", "display_name") VALUES (?, ?, ?)  -- {"parent_code": "PROBE-NO-SUCH-PARENT-53", "population_code": "PROBE-PK-54", "display_name": "PROBE-DISPLAY_NAME"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0134] A3 — probe_population_links.population_code → populations.population_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "probe_population_links" ("population_code", "probe_id") VALUES (?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-55", "probe_id": "PROBE-PK-56"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0135] A3 — probe_population_links.probe_id → spec_value_probes.probe_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "probe_population_links" ("probe_id", "population_code") VALUES (?, ?)  -- {"probe_id": "PROBE-NO-SUCH-PARENT-57", "population_code": "ADHD"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0136] A3 — reasoning_doc_citations.source_ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("source_ref_id", "citation_id", "reasoning_doc_slug", "parameter", "claim_type", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"source_ref_id": "PROBE-NO-SUCH-PARENT-58", "citation_id": "PROBE-PK-59", "reasoning_doc_slug": "aac-speech-production-environments", "parameter": "PROBE-PARAMETER", "claim_type": "numerical_spec", "verified_at": "PROBE-VERIFIED_AT", "verified_by_session": "PROBE-VERIFIED_BY_SESSION", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-CLAIMED_VALUE", "claim_text": "PROBE-CLAIM_TEXT"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0137] A3 — reasoning_doc_citations.reasoning_doc_slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("reasoning_doc_slug", "citation_id", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"reasoning_doc_slug": "PROBE-NO-SUCH-PARENT-60", "citation_id": "PROBE-PK-61", "parameter": "PROBE-PARAMETER", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-62", "verified_at": "PROBE-VERIFIED_AT", "verified_by_session": "PROBE-VERIFIED_BY_SESSION", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-CLAIMED_VALUE", "claim_text": "PROBE-CLAIM_TEXT"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0138] A3 — room_items.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "room_items" ("item_code", "room_code") VALUES (?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-63", "room_code": "R-ASM"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0139] A3 — room_items.room_code → rooms.room_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "room_items" ("room_code", "item_code") VALUES (?, ?)  -- {"room_code": "PROBE-NO-SUCH-PARENT-64", "item_code": "A-01"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0140] A3 — search_admissions.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "search_admissions" ("ref_id", "exec_id") VALUES (?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-65", "exec_id": 1}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0141] A3 — search_admissions.exec_id → search_executions.exec_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "search_admissions" ("exec_id", "ref_id") VALUES (?, ?)  -- {"exec_id": 999999966, "ref_id": "PROBE-PK-67"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0142] A3 — search_candidates.suggested_slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("suggested_slug", "found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?, ?)  -- {"suggested_slug": "PROBE-NO-SUCH-PARENT-68", "found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": "PROBE-TITLE", "session": "PROBE-SESSION", "created_at": "PROBE-CREATED_AT"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0143] A3 — search_candidates.found_under_slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": "PROBE-NO-SUCH-PARENT-69", "disposition": "REHOME", "title": "PROBE-TITLE", "session": "PROBE-SESSION", "created_at": "PROBE-CREATED_AT"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0144] A3 — search_candidates.exec_id → search_executions.exec_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("exec_id", "found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?, ?)  -- {"exec_id": 999999970, "found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": "PROBE-TITLE", "session": "PROBE-SESSION", "created_at": "PROBE-CREATED_AT"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0145] A3 — search_coverage.slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-71", "jurisdiction": "PROBE-JURISDICTION", "status": "SEARCHED", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0146] A3 — search_executions.slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-72", "language": "PROBE-LANGUAGE", "query_text": "PROBE-QUERY_TEXT", "engine": "PROBE-ENGINE", "depth_method": "scoping", "session": "PROBE-SESSION", "executed_at": "PROBE-EXECUTED_AT"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0147] A3 — search_languages.slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-73", "language": "PROBE-LANGUAGE", "status": "SEARCHED", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0148] A3 — slugs.merged_into → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "slugs" ("merged_into", "slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"merged_into": "PROBE-NO-SUCH-PARENT-74", "slug": "PROBE-PK-75", "topic_directory": "PROBE-TOPIC_DIRECTORY", "sl_path": "PROBE-SL_PATH", "bpc_path": "PROBE-BPC_PATH", "status": "ACTIVE", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0149] A3 — source_slug_links.slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("slug", "ref_id", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-76", "ref_id": "PROBE-PK-77", "local_ref_id": "PROBE-LOCAL_REF_ID", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0150] A3 — source_slug_links.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-78", "slug": "aac-speech-production-environments", "local_ref_id": "PROBE-LOCAL_REF_ID", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0151] A3 — source_value_extractions.promoted_to_rdc_id → reasoning_doc_citations.citation_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("promoted_to_rdc_id", "ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"promoted_to_rdc_id": "PROBE-NO-SUCH-PARENT-79", "ref_id": "PROBE-PK-80", "slug": "aac-speech-production-environments", "parameter": "PROBE-PARAMETER", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-CREATED_AT", "updated_at": "PROBE-UPDATED_AT", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0152] A3 — source_value_extractions.population_code → populations.population_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("population_code", "ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-81", "ref_id": "PROBE-PK-82", "slug": "aac-speech-production-environments", "parameter": "PROBE-PARAMETER", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-CREATED_AT", "updated_at": "PROBE-UPDATED_AT", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0153] A3 — source_value_extractions.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-83", "slug": "aac-speech-production-environments", "parameter": "PROBE-PARAMETER", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-CREATED_AT", "updated_at": "PROBE-UPDATED_AT", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0154] A3 — source_value_extractions.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("item_code", "ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-84", "ref_id": "PROBE-PK-85", "slug": "aac-speech-production-environments", "parameter": "PROBE-PARAMETER", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-CREATED_AT", "updated_at": "PROBE-UPDATED_AT", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0155] A3 — source_value_extractions.root_ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("root_ref_id", "ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"root_ref_id": "PROBE-NO-SUCH-PARENT-86", "ref_id": "PROBE-PK-87", "slug": "aac-speech-production-environments", "parameter": "PROBE-PARAMETER", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-CREATED_AT", "updated_at": "PROBE-UPDATED_AT", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0156] A3 — source_value_extractions.slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("slug", "ref_id", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-88", "ref_id": "PROBE-PK-89", "parameter": "PROBE-PARAMETER", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-CREATED_AT", "updated_at": "PROBE-UPDATED_AT", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0157] A3 — spec_value_probes.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("ref_id", "probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-90", "probe_id": "PROBE-PK-91", "walk_id": "PROBE-WALK_ID", "slug": "aac-speech-production-environments", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-SPEC_UNIT", "direction": "up", "population": "PROBE-POPULATION", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-STEP_VALUE_UNIT", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0158] A3 — spec_value_probes.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("item_code", "probe_id", "walk_id", "slug", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-92", "probe_id": "PROBE-PK-93", "walk_id": "PROBE-WALK_ID", "slug": "aac-speech-production-environments", "spec_value_origin": 1.0, "spec_unit": "PROBE-SPEC_UNIT", "direction": "up", "population": "PROBE-POPULATION", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-STEP_VALUE_UNIT", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0159] A3 — spec_value_probes.slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("slug", "probe_id", "walk_id", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-94", "probe_id": "PROBE-PK-95", "walk_id": "PROBE-WALK_ID", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-SPEC_UNIT", "direction": "up", "population": "PROBE-POPULATION", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-STEP_VALUE_UNIT", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0160] A3 — specification_source_links.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "specification_source_links" ("ref_id", "specification_id") VALUES (?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-96", "specification_id": 1}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0161] A3 — specification_source_links.specification_id → specifications.specification_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "specification_source_links" ("specification_id", "ref_id") VALUES (?, ?)  -- {"specification_id": 999999997, "ref_id": "PROBE-PK-98"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0162] A3 — specifications.gap_register_id → gaps.gap_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("gap_register_id", "item_code", "population_code", "state") VALUES (?, ?, ?, ?)  -- {"gap_register_id": "PROBE-NO-SUCH-PARENT-99", "item_code": "A-01", "population_code": "ADHD", "state": "stated"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0163] A3 — specifications.convergence_id → convergence_assessment.convergence_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("convergence_id", "item_code", "population_code", "state") VALUES (?, ?, ?, ?)  -- {"convergence_id": 1000000000, "item_code": "A-01", "population_code": "ADHD", "state": "stated"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0164] A3 — specifications.population_code → populations.population_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("population_code", "item_code", "state") VALUES (?, ?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-101", "item_code": "A-01", "state": "stated"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0165] A3 — specifications.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state") VALUES (?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-102", "population_code": "ADHD", "state": "stated"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0166] A3 — supersession_check.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("ref_id", "check_id", "slug", "local_ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-103", "check_id": "PROBE-PK-104", "slug": "aac-speech-production-environments", "local_ref_id": "PROBE-LOCAL_REF_ID", "anchor_tier": 1, "anchor_evidence_type": "PROBE-ANCHOR_EVIDENCE_TYPE", "outcome": "current_best", "search_strategy_record": "PROBE-SEARCH_STRATEGY_RECORD", "checked_at": "PROBE-CHECKED_AT", "checked_by_session": "PROBE-CHECKED_BY_SESSION", "check_method": "pubmed_search"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0167] A3 — supersession_check.slug → slugs.slug   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("slug", "check_id", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-105", "check_id": "PROBE-PK-106", "local_ref_id": "PROBE-LOCAL_REF_ID", "ref_id": "PROBE-PK-107", "anchor_tier": 1, "anchor_evidence_type": "PROBE-ANCHOR_EVIDENCE_TYPE", "outcome": "current_best", "search_strategy_record": "PROBE-SEARCH_STRATEGY_RECORD", "checked_at": "PROBE-CHECKED_AT", "checked_by_session": "PROBE-CHECKED_BY_SESSION", "check_method": "pubmed_search"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0168] A3 — term_aliases.term_id → terms.term_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-NO-SUCH-PARENT-108", "alias": "PROBE-ALIAS", "language": "PROBE-PK-109", "alias_type": "SYNONYM", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0169] A3 — term_item_links.item_code → items.item_code   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "term_item_links" ("item_code", "term_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-110", "term_id": "TERM-001", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [0170] A3 — term_item_links.term_id → terms.term_id   `2026-08-12 08:35:27Z`
**Action:** insert child with nonexistent parent value (FK=ON)
**SQL:**
```sql
INSERT INTO "term_item_links" ("term_id", "item_code", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-NO-SUCH-PARENT-111", "item_code": "A-01", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** insert rejected with FOREIGN KEY constraint failed
**Actual:** rejected with FK error
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### A3b — NULL-path probes for the 18 nullable FK edges (FK never evaluated on NULL)

### [0171] A3b — citation_mining.global_ref_id → evidence_sources (NULL path)   `2026-08-12 08:35:27Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session", "global_ref_id") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "aac-speech-production-environments", "local_ref_id": "PROBE-112", "created_at": "PROBE-113", "created_by_session": "PROBE-114", "updated_at": "PROBE-115", "updated_by_session": "PROBE-116", "global_ref_id": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0172] A3b — conflicts.item_code → items (NULL path)   `2026-08-12 08:35:27Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "item_code") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-118", "domain": "PROBE-119", "pop_a": "PROBE-120", "pop_b": "PROBE-121", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-122", "created_by_session": "PROBE-123", "updated_at": "PROBE-124", "updated_by_session": "PROBE-125", "item_code": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0173] A3b — economics_entries.ref_id → evidence_sources (NULL path)   `2026-08-12 08:35:27Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session", "ref_id") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-126", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-127", "finding": "PROBE-128", "created_at": "PROBE-129", "created_by_session": "PROBE-130", "ref_id": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0174] A3b — evidence_population_match.gap_id → gaps (NULL path)   `2026-08-12 08:35:27Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session", "gap_id") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-132", "source_ref": "PROBE-133", "target_population": "PROBE-134", "match_grade": "EXACT", "created_at": "PROBE-135", "created_by_session": "PROBE-136", "gap_id": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0175] A3b — evidence_population_match.ref_id → evidence_sources (NULL path)   `2026-08-12 08:35:27Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session", "ref_id") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-137", "source_ref": "PROBE-138", "target_population": "PROBE-139", "match_grade": "EXACT", "created_at": "PROBE-140", "created_by_session": "PROBE-141", "ref_id": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0176] A3b — item_population_elaborations.evidence_ref_id → evidence_sources (NULL path)   `2026-08-12 08:35:27Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("item_code", "population_code", "evidence_ref_id") VALUES (?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "evidence_ref_id": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0177] A3b — items.bpc_source_slug → slugs (NULL path)   `2026-08-12 08:35:27Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session", "bpc_source_slug") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-143", "category": "A", "name": "PROBE-144", "created_at": "PROBE-145", "created_by_session": "PROBE-146", "updated_at": "PROBE-147", "updated_by_session": "PROBE-148", "bpc_source_slug": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0178] A3b — populations.parent_code → populations (NULL path)   `2026-08-12 08:35:27Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "populations" ("population_code", "display_name", "parent_code") VALUES (?, ?, ?)  -- {"population_code": "PROBE-150", "display_name": "PROBE-151", "parent_code": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0179] A3b — search_candidates.suggested_slug → slugs (NULL path)   `2026-08-12 08:35:28Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at", "suggested_slug") VALUES (?, ?, ?, ?, ?, ?)  -- {"found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": "PROBE-152", "session": "PROBE-153", "created_at": "PROBE-154", "suggested_slug": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0180] A3b — search_candidates.exec_id → search_executions (NULL path)   `2026-08-12 08:35:28Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at", "exec_id") VALUES (?, ?, ?, ?, ?, ?)  -- {"found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": "PROBE-155", "session": "PROBE-156", "created_at": "PROBE-157", "exec_id": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0181] A3b — slugs.merged_into → slugs (NULL path)   `2026-08-12 08:35:28Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "merged_into") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-159", "topic_directory": "PROBE-160", "sl_path": "PROBE-161", "bpc_path": "PROBE-162", "status": "ACTIVE", "created_at": "PROBE-163", "created_by_session": "PROBE-164", "updated_at": "PROBE-165", "updated_by_session": "PROBE-166", "merged_into": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0182] A3b — source_value_extractions.promoted_to_rdc_id → reasoning_doc_citations (NULL path)   `2026-08-12 08:35:28Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "promoted_to_rdc_id") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-168", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-169", "updated_at": "PROBE-170", "claimed_value": "PROBE-171", "promoted_to_rdc_id": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0183] A3b — source_value_extractions.population_code → populations (NULL path)   `2026-08-12 08:35:28Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "population_code") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-172", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-173", "updated_at": "PROBE-174", "claimed_value": "PROBE-175", "population_code": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0184] A3b — source_value_extractions.item_code → items (NULL path)   `2026-08-12 08:35:28Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "item_code") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-176", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-177", "updated_at": "PROBE-178", "claimed_value": "PROBE-179", "item_code": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0185] A3b — source_value_extractions.root_ref_id → evidence_sources (NULL path)   `2026-08-12 08:35:28Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "root_ref_id") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-180", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-181", "updated_at": "PROBE-182", "claimed_value": "PROBE-183", "root_ref_id": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0186] A3b — spec_value_probes.ref_id → evidence_sources (NULL path)   `2026-08-12 08:35:28Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session", "ref_id") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-185", "walk_id": "PROBE-186", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-187", "direction": "up", "population": "PROBE-188", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-189", "created_at": "PROBE-190", "created_by_session": "PROBE-191", "ref_id": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0187] A3b — specifications.gap_register_id → gaps (NULL path)   `2026-08-12 08:35:28Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "gap_register_id") VALUES (?, ?, ?, ?)  -- {"item_code": "G-07", "population_code": "MOB", "state": "stated", "gap_register_id": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0188] A3b — specifications.convergence_id → convergence_assessment (NULL path)   `2026-08-12 08:35:28Z`
**Action:** insert child row with the FK column explicitly NULL (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "convergence_id") VALUES (?, ?, ?, ?)  -- {"item_code": "A-11", "population_code": "MOB", "state": "stated", "convergence_id": null}
```
**Expected:** if the reference is semantically required, some constraint should reject it
**Actual:** row ACCEPTED with no parent linkage — SQL NULL-bypass: the FK exists but is never evaluated. Any writer can skip provenance on this edge
**Verdict:** **`SILENT-PASS`**

### [0189] A3c — evidence_population_match.source_ref vs ref_id (dual identity columns)   `2026-08-12 08:35:28Z`
**Action:** satisfy NOT NULL with free text in source_ref while leaving the FK'd ref_id NULL
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session", "ref_id") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-192", "source_ref": "PROBE-GARBAGE-NOT-A-REF", "target_population": "PROBE-193", "match_grade": "EXACT", "created_at": "PROBE-194", "created_by_session": "PROBE-195", "ref_id": null}
```
**Expected:** the row should be rejected — it claims a source that does not exist
**Actual:** ACCEPTED
**Verdict:** **`SILENT-PASS`**

### A4 — bad-value FK probes, `PRAGMA foreign_keys=OFF` (the migrate_db.py apply mode)

### [0190] A4 — access_need_axis_map.axis_code → axes.axis_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "access_need_axis_map" ("axis_code", "need_code", "relationship") VALUES (?, ?, ?)  -- {"axis_code": "PROBE-NO-SUCH-PARENT-196", "need_code": "A-AT", "relationship": "primary"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0191] A4 — access_need_axis_map.need_code → access_needs.need_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "access_need_axis_map" ("need_code", "axis_code", "relationship") VALUES (?, ?, ?)  -- {"need_code": "PROBE-NO-SUCH-PARENT-197", "axis_code": "AX-AMB", "relationship": "primary"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0192] A4 — access_need_icf.need_code → access_needs.need_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "access_need_icf" ("need_code", "icf_code", "icf_type", "confidence") VALUES (?, ?, ?, ?)  -- {"need_code": "PROBE-NO-SUCH-PARENT-198", "icf_code": "PROBE-ICF_CODE", "icf_type": "b", "confidence": "confirmed"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0193] A4 — bpc_metadata.slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-199", "population": "PROBE-POPULATION", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0194] A4 — case_studies.slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "case_studies" ("slug", "case_study_id", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-200", "case_study_id": "PROBE-CASE_STUDY_ID", "title": "PROBE-TITLE", "building_type": "PROBE-BUILDING_TYPE", "location": "PROBE-LOCATION", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0195] A4 — case_study_outcomes.case_study_id → case_studies.case_study_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "case_study_outcomes" ("case_study_id", "metric") VALUES (?, ?)  -- {"case_study_id": "PROBE-NO-SUCH-PARENT-201", "metric": "PROBE-METRIC"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0196] A4 — case_study_populations.population_code → populations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "case_study_populations" ("population_code", "case_study_id") VALUES (?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-202", "case_study_id": "PROBE-CASE_STUDY_ID"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0197] A4 — case_study_populations.case_study_id → case_studies.case_study_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "case_study_populations" ("case_study_id", "population_code") VALUES (?, ?)  -- {"case_study_id": "PROBE-NO-SUCH-PARENT-203", "population_code": "ADHD"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0198] A4 — case_study_specs.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "case_study_specs" ("item_code", "case_study_id") VALUES (?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-204", "case_study_id": "PROBE-CASE_STUDY_ID"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0199] A4 — case_study_specs.case_study_id → case_studies.case_study_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "case_study_specs" ("case_study_id", "item_code") VALUES (?, ?)  -- {"case_study_id": "PROBE-NO-SUCH-PARENT-205", "item_code": "A-01"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0200] A4 — case_study_strategies.case_study_id → case_studies.case_study_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "case_study_strategies" ("case_study_id", "strategy") VALUES (?, ?)  -- {"case_study_id": "PROBE-NO-SUCH-PARENT-206", "strategy": "PROBE-STRATEGY"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0201] A4 — citation_mining.global_ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "citation_mining" ("global_ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"global_ref_id": "PROBE-NO-SUCH-PARENT-207", "slug": "aac-speech-production-environments", "local_ref_id": "PROBE-LOCAL_REF_ID", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0202] A4 — citation_mining.slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-208", "local_ref_id": "PROBE-LOCAL_REF_ID", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0203] A4 — citation_population_links.population_code → populations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "citation_population_links" ("population_code", "citation_id") VALUES (?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-209", "citation_id": "PROBE-PK-210"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0204] A4 — citation_population_links.citation_id → reasoning_doc_citations.citation_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "citation_population_links" ("citation_id", "population_code") VALUES (?, ?)  -- {"citation_id": "PROBE-NO-SUCH-PARENT-212", "population_code": "ADHD"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0205] A4 — conflicts.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "conflicts" ("item_code", "conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-213", "conflict_id": "PROBE-PK-214", "domain": "PROBE-DOMAIN", "pop_a": "PROBE-POP_A", "pop_b": "PROBE-POP_B", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0206] A4 — connection_targets.con_id → connections.con_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "connection_targets" ("con_id", "target") VALUES (?, ?)  -- {"con_id": "PROBE-NO-SUCH-PARENT-215", "target": "PROBE-TARGET"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0207] A4 — economics_entries.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "economics_entries" ("ref_id", "entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-216", "entry_id": "PROBE-ENTRY_ID", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-SOURCE", "finding": "PROBE-FINDING", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0208] A4 — economics_entry_populations.population_code → populations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "economics_entry_populations" ("population_code", "entry_id") VALUES (?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-217", "entry_id": "PROBE-ENTRY_ID"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0209] A4 — economics_entry_populations.entry_id → economics_entries.entry_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "economics_entry_populations" ("entry_id", "population_code") VALUES (?, ?)  -- {"entry_id": "PROBE-NO-SUCH-PARENT-218", "population_code": "ADHD"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0210] A4 — economics_entry_specs.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "economics_entry_specs" ("item_code", "entry_id") VALUES (?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-219", "entry_id": "PROBE-ENTRY_ID"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0211] A4 — economics_entry_specs.entry_id → economics_entries.entry_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "economics_entry_specs" ("entry_id", "item_code") VALUES (?, ?)  -- {"entry_id": "PROBE-NO-SUCH-PARENT-220", "item_code": "A-01"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0212] A4 — evidence_population_match.gap_id → gaps.gap_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("gap_id", "match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-NO-SUCH-PARENT-221", "match_id": "PROBE-PK-222", "source_ref": "PROBE-SOURCE_REF", "target_population": "PROBE-TARGET_POPULATION", "match_grade": "EXACT", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0213] A4 — evidence_population_match.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("ref_id", "match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-223", "match_id": "PROBE-PK-224", "source_ref": "PROBE-SOURCE_REF", "target_population": "PROBE-TARGET_POPULATION", "match_grade": "EXACT", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0214] A4 — evidence_source_authors.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "evidence_source_authors" ("ref_id", "position") VALUES (?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-225", "position": 1}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0215] A4 — extraction_population_links.population_code → populations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "extraction_population_links" ("population_code", "extraction_id") VALUES (?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-226", "extraction_id": 1}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0216] A4 — extraction_population_links.extraction_id → source_value_extractions.extraction_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "extraction_population_links" ("extraction_id", "population_code") VALUES (?, ?)  -- {"extraction_id": 1000000127, "population_code": "ADHD"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0217] A4 — gap_mining.gap_id → gaps.gap_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-NO-SUCH-PARENT-228", "attempt_at": "PROBE-ATTEMPT_AT", "attempted_by_session": "PROBE-ATTEMPTED_BY_SESSION", "search_strategy_record": "PROBE-SEARCH_STRATEGY_RECORD", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-DISCOVERIES_LOGGED"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0218] A4 — item_audit_runs.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("item_code", "run_id", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-229", "run_id": "PROBE-PK-230", "session": "PROBE-SESSION", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0219] A4 — item_axis_links.axis_code → axes.axis_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "item_axis_links" ("axis_code", "item_code") VALUES (?, ?)  -- {"axis_code": "PROBE-NO-SUCH-PARENT-231", "item_code": "A-01"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0220] A4 — item_axis_links.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "item_axis_links" ("item_code", "axis_code") VALUES (?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-232", "axis_code": "AX-AMB"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0221] A4 — item_bpc_links.slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "item_bpc_links" ("slug", "item_code", "link_type", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-233", "item_code": "A-01", "link_type": "primary", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0222] A4 — item_bpc_links.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "item_bpc_links" ("item_code", "slug", "link_type", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-234", "slug": "aac-speech-production-environments", "link_type": "primary", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0223] A4 — item_population_elaborations.evidence_ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("evidence_ref_id", "item_code", "population_code") VALUES (?, ?, ?)  -- {"evidence_ref_id": "PROBE-NO-SUCH-PARENT-235", "item_code": "A-01", "population_code": "ADHD"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0224] A4 — item_population_elaborations.population_code → populations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("population_code", "item_code") VALUES (?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-236", "item_code": "A-01"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0225] A4 — item_population_elaborations.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("item_code", "population_code") VALUES (?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-237", "population_code": "ADHD"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0226] A4 — item_population_links.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "item_population_links" ("item_code", "population_code", "subtype") VALUES (?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-238", "population_code": "ADHD", "subtype": "PROBE-PK-239"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0227] A4 — item_population_links.population_code → populations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "item_population_links" ("population_code", "item_code", "subtype") VALUES (?, ?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-240", "item_code": "A-01", "subtype": "PROBE-PK-241"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0228] A4 — items.bpc_source_slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "items" ("bpc_source_slug", "item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"bpc_source_slug": "PROBE-NO-SUCH-PARENT-242", "item_code": "PROBE-PK-243", "category": "A", "name": "PROBE-NAME", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0229] A4 — jurisdictional_values.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "jurisdictional_values" ("item_code", "jurisdiction") VALUES (?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-244", "jurisdiction": "PROBE-JURISDICTION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0230] A4 — population_axis_map.axis_code → axes.axis_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "population_axis_map" ("axis_code", "population_code", "role") VALUES (?, ?, ?)  -- {"axis_code": "PROBE-NO-SUCH-PARENT-245", "population_code": "ADHD", "role": "ALIAS"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0231] A4 — population_axis_map.population_code → populations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "population_axis_map" ("population_code", "axis_code", "role") VALUES (?, ?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-246", "axis_code": "AX-AMB", "role": "ALIAS"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0232] A4 — populations.parent_code → populations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "populations" ("parent_code", "population_code", "display_name") VALUES (?, ?, ?)  -- {"parent_code": "PROBE-NO-SUCH-PARENT-247", "population_code": "PROBE-PK-248", "display_name": "PROBE-DISPLAY_NAME"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0233] A4 — probe_population_links.population_code → populations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "probe_population_links" ("population_code", "probe_id") VALUES (?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-249", "probe_id": "PROBE-PK-250"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0234] A4 — probe_population_links.probe_id → spec_value_probes.probe_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "probe_population_links" ("probe_id", "population_code") VALUES (?, ?)  -- {"probe_id": "PROBE-NO-SUCH-PARENT-251", "population_code": "ADHD"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0235] A4 — reasoning_doc_citations.source_ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("source_ref_id", "citation_id", "reasoning_doc_slug", "parameter", "claim_type", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"source_ref_id": "PROBE-NO-SUCH-PARENT-252", "citation_id": "PROBE-PK-253", "reasoning_doc_slug": "aac-speech-production-environments", "parameter": "PROBE-PARAMETER", "claim_type": "numerical_spec", "verified_at": "PROBE-VERIFIED_AT", "verified_by_session": "PROBE-VERIFIED_BY_SESSION", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-CLAIMED_VALUE", "claim_text": "PROBE-CLAIM_TEXT"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0236] A4 — reasoning_doc_citations.reasoning_doc_slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("reasoning_doc_slug", "citation_id", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"reasoning_doc_slug": "PROBE-NO-SUCH-PARENT-254", "citation_id": "PROBE-PK-255", "parameter": "PROBE-PARAMETER", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-211", "verified_at": "PROBE-VERIFIED_AT", "verified_by_session": "PROBE-VERIFIED_BY_SESSION", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-CLAIMED_VALUE", "claim_text": "PROBE-CLAIM_TEXT"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0237] A4 — room_items.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "room_items" ("item_code", "room_code") VALUES (?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-256", "room_code": "R-ASM"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0238] A4 — room_items.room_code → rooms.room_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "room_items" ("room_code", "item_code") VALUES (?, ?)  -- {"room_code": "PROBE-NO-SUCH-PARENT-257", "item_code": "A-01"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0239] A4 — search_admissions.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "search_admissions" ("ref_id", "exec_id") VALUES (?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-258", "exec_id": 1}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0240] A4 — search_admissions.exec_id → search_executions.exec_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "search_admissions" ("exec_id", "ref_id") VALUES (?, ?)  -- {"exec_id": 1000000159, "ref_id": "PROBE-PK-211"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0241] A4 — search_candidates.suggested_slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "search_candidates" ("suggested_slug", "found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?, ?)  -- {"suggested_slug": "PROBE-NO-SUCH-PARENT-260", "found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": "PROBE-TITLE", "session": "PROBE-SESSION", "created_at": "PROBE-CREATED_AT"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0242] A4 — search_candidates.found_under_slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": "PROBE-NO-SUCH-PARENT-261", "disposition": "REHOME", "title": "PROBE-TITLE", "session": "PROBE-SESSION", "created_at": "PROBE-CREATED_AT"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0243] A4 — search_candidates.exec_id → search_executions.exec_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "search_candidates" ("exec_id", "found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?, ?)  -- {"exec_id": 1000000162, "found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": "PROBE-TITLE", "session": "PROBE-SESSION", "created_at": "PROBE-CREATED_AT"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0244] A4 — search_coverage.slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-263", "jurisdiction": "PROBE-JURISDICTION", "status": "SEARCHED", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0245] A4 — search_executions.slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-264", "language": "PROBE-LANGUAGE", "query_text": "PROBE-QUERY_TEXT", "engine": "PROBE-ENGINE", "depth_method": "scoping", "session": "PROBE-SESSION", "executed_at": "PROBE-EXECUTED_AT"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0246] A4 — search_languages.slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-265", "language": "PROBE-LANGUAGE", "status": "SEARCHED", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0247] A4 — slugs.merged_into → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "slugs" ("merged_into", "slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"merged_into": "PROBE-NO-SUCH-PARENT-266", "slug": "PROBE-PK-267", "topic_directory": "PROBE-TOPIC_DIRECTORY", "sl_path": "PROBE-SL_PATH", "bpc_path": "PROBE-BPC_PATH", "status": "ACTIVE", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0248] A4 — source_slug_links.slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("slug", "ref_id", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-268", "ref_id": "PROBE-PK-211", "local_ref_id": "PROBE-LOCAL_REF_ID", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0249] A4 — source_slug_links.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-269", "slug": "PROBE-PK-267", "local_ref_id": "PROBE-LOCAL_REF_ID", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0250] A4 — source_value_extractions.promoted_to_rdc_id → reasoning_doc_citations.citation_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("promoted_to_rdc_id", "ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"promoted_to_rdc_id": "PROBE-NO-SUCH-PARENT-270", "ref_id": "PROBE-PK-211", "slug": "PROBE-PK-267", "parameter": "PROBE-PARAMETER", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-CREATED_AT", "updated_at": "PROBE-UPDATED_AT", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0251] A4 — source_value_extractions.population_code → populations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("population_code", "ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-271", "ref_id": "PROBE-PK-211", "slug": "PROBE-PK-267", "parameter": "PROBE-PARAMETER", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-CREATED_AT", "updated_at": "PROBE-UPDATED_AT", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0252] A4 — source_value_extractions.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-272", "slug": "PROBE-PK-267", "parameter": "PROBE-PARAMETER", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-CREATED_AT", "updated_at": "PROBE-UPDATED_AT", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0253] A4 — source_value_extractions.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("item_code", "ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-273", "ref_id": "PROBE-PK-211", "slug": "PROBE-PK-267", "parameter": "PROBE-PARAMETER", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-CREATED_AT", "updated_at": "PROBE-UPDATED_AT", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0254] A4 — source_value_extractions.root_ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("root_ref_id", "ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"root_ref_id": "PROBE-NO-SUCH-PARENT-274", "ref_id": "PROBE-PK-211", "slug": "PROBE-PK-267", "parameter": "PROBE-PARAMETER", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-CREATED_AT", "updated_at": "PROBE-UPDATED_AT", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0255] A4 — source_value_extractions.slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("slug", "ref_id", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-275", "ref_id": "PROBE-PK-211", "parameter": "PROBE-PARAMETER", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-CREATED_AT", "updated_at": "PROBE-UPDATED_AT", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0256] A4 — spec_value_probes.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("ref_id", "probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-276", "probe_id": "PROBE-PK-277", "walk_id": "PROBE-WALK_ID", "slug": "PROBE-PK-267", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-SPEC_UNIT", "direction": "up", "population": "PROBE-POPULATION", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-STEP_VALUE_UNIT", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0257] A4 — spec_value_probes.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("item_code", "probe_id", "walk_id", "slug", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-278", "probe_id": "PROBE-PK-279", "walk_id": "PROBE-WALK_ID", "slug": "PROBE-PK-267", "spec_value_origin": 1.0, "spec_unit": "PROBE-SPEC_UNIT", "direction": "up", "population": "PROBE-POPULATION", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-STEP_VALUE_UNIT", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0258] A4 — spec_value_probes.slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("slug", "probe_id", "walk_id", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-280", "probe_id": "PROBE-PK-281", "walk_id": "PROBE-WALK_ID", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-SPEC_UNIT", "direction": "up", "population": "PROBE-POPULATION", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-STEP_VALUE_UNIT", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0259] A4 — specification_source_links.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "specification_source_links" ("ref_id", "specification_id") VALUES (?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-282", "specification_id": 1}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0260] A4 — specification_source_links.specification_id → specifications.specification_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "specification_source_links" ("specification_id", "ref_id") VALUES (?, ?)  -- {"specification_id": 1000000183, "ref_id": "PROBE-PK-211"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0261] A4 — specifications.gap_register_id → gaps.gap_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "specifications" ("gap_register_id", "item_code", "population_code", "state") VALUES (?, ?, ?, ?)  -- {"gap_register_id": "PROBE-NO-SUCH-PARENT-284", "item_code": "A-17", "population_code": "LPA", "state": "stated"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0262] A4 — specifications.convergence_id → convergence_assessment.convergence_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "specifications" ("convergence_id", "item_code", "population_code", "state") VALUES (?, ?, ?, ?)  -- {"convergence_id": 1000000185, "item_code": "A-10", "population_code": "PROBE-PK-248", "state": "stated"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0263] A4 — specifications.population_code → populations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "specifications" ("population_code", "item_code", "state") VALUES (?, ?, ?)  -- {"population_code": "PROBE-NO-SUCH-PARENT-286", "item_code": "A-01", "state": "stated"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0264] A4 — specifications.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state") VALUES (?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-287", "population_code": "ADHD", "state": "stated"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0265] A4 — supersession_check.ref_id → evidence_sources.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "supersession_check" ("ref_id", "check_id", "slug", "local_ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-NO-SUCH-PARENT-288", "check_id": "PROBE-PK-289", "slug": "PROBE-PK-267", "local_ref_id": "PROBE-LOCAL_REF_ID", "anchor_tier": 1, "anchor_evidence_type": "PROBE-ANCHOR_EVIDENCE_TYPE", "outcome": "current_best", "search_strategy_record": "PROBE-SEARCH_STRATEGY_RECORD", "checked_at": "PROBE-CHECKED_AT", "checked_by_session": "PROBE-CHECKED_BY_SESSION", "check_method": "pubmed_search"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0266] A4 — supersession_check.slug → slugs.slug   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "supersession_check" ("slug", "check_id", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-NO-SUCH-PARENT-290", "check_id": "PROBE-PK-291", "local_ref_id": "PROBE-LOCAL_REF_ID", "ref_id": "PROBE-PK-211", "anchor_tier": 1, "anchor_evidence_type": "PROBE-ANCHOR_EVIDENCE_TYPE", "outcome": "current_best", "search_strategy_record": "PROBE-SEARCH_STRATEGY_RECORD", "checked_at": "PROBE-CHECKED_AT", "checked_by_session": "PROBE-CHECKED_BY_SESSION", "check_method": "pubmed_search"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0267] A4 — term_aliases.term_id → terms.term_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-NO-SUCH-PARENT-292", "alias": "PROBE-ALIAS", "language": "PROBE-PK-293", "alias_type": "SYNONYM", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0268] A4 — term_item_links.item_code → items.item_code   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "term_item_links" ("item_code", "term_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-NO-SUCH-PARENT-294", "term_id": "TERM-001", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0269] A4 — term_item_links.term_id → terms.term_id   `2026-08-12 08:35:28Z`
**Action:** insert child with nonexistent parent value (FK=OFF, migrate_db.py apply mode)
**SQL:**
```sql
INSERT INTO "term_item_links" ("term_id", "item_code", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-NO-SUCH-PARENT-295", "item_code": "A-01", "created_at": "PROBE-CREATED_AT", "created_by_session": "PROBE-CREATED_BY_SESSION", "updated_at": "PROBE-UPDATED_AT", "updated_by_session": "PROBE-UPDATED_BY_SESSION"}
```
**Expected:** would be rejected under FK=ON
**Actual:** insert COMMITTED — violation persists in the file
**Verdict:** **`SILENT-PASS`**

### [0270] A4 — probe-a-off.db   `2026-08-12 08:35:28Z`
**Action:** PRAGMA foreign_key_check after committing all FK=OFF probes
**Expected:** 80 violations visible
**Actual:** 80 violation rows persisted. migrate_db.py COMMITS the migration BEFORE running this check, tolerates any violation already in `pre_violations`, and skips the failure entirely when the migration body contains 'BOOTSTRAP' in its first 500 bytes — so every one of these edges is a committable write-path defect
**Verdict:** **`SILENT-PASS`**

### A5 — reverse-direction map
| table | rows | referenced by (inbound) | references (outbound) |
|---|---|---|---|
| `access_duration` | 3 | — | — |
| `access_need_axis_map` | 21 | — | access_needs, axes |
| `access_need_icf` | 43 | — | access_needs |
| `access_needs` | 17 | access_need_axis_map, access_need_icf | — |
| `access_stakes` | 3 | — | — |
| `axes` | 17 | access_need_axis_map, item_axis_links, population_axis_map | — |
| `bpc_metadata` | 0 | — | slugs |
| `case_studies` | 0 | case_study_outcomes, case_study_populations, case_study_specs, case_study_strategies | slugs |
| `case_study_outcomes` | 0 | — | case_studies |
| `case_study_populations` | 0 | — | case_studies, populations |
| `case_study_specs` | 0 | — | case_studies, items |
| `case_study_strategies` | 0 | — | case_studies |
| `citation_mining` | 0 | — | evidence_sources, slugs |
| `citation_population_links` | 0 | — | populations, reasoning_doc_citations |
| `conflicts` | 0 | — | items |
| `connection_targets` | 0 | — | connections |
| `connections` | 0 | connection_targets | — |
| `convergence_assessment` | 0 | specifications | — |
| `data_migrations` | 319 | — | — |
| `db_meta` | 2 | — | — |
| `decisions` | 158 | — | — |
| `economics_entries` | 0 | economics_entry_populations, economics_entry_specs | evidence_sources |
| `economics_entry_populations` | 0 | — | economics_entries, populations |
| `economics_entry_specs` | 0 | — | economics_entries, items |
| `evidence_population_match` | 0 | — | evidence_sources, gaps |
| `evidence_source_authors` | 0 | — | evidence_sources |
| `evidence_sources` | 0 | citation_mining, economics_entries, evidence_population_match, evidence_source_authors, item_population_elaborations, reasoning_doc_citations, search_admissions, source_slug_links, source_value_extractions, spec_value_probes, specification_source_links, supersession_check | — |
| `external_root_registry` | 0 | — | — |
| `extraction_population_links` | 0 | — | populations, source_value_extractions |
| `gap_mining` | 0 | — | gaps |
| `gaps` | 0 | evidence_population_match, gap_mining, specifications | — |
| `item_audit_runs` | 0 | — | items |
| `item_axis_links` | 158 | — | axes, items |
| `item_bpc_links` | 0 | — | items, slugs |
| `item_population_elaborations` | 0 | — | evidence_sources, items, populations |
| `item_population_links` | 372 | — | items, populations |
| `items` | 93 | case_study_specs, conflicts, economics_entry_specs, item_audit_runs, item_axis_links, item_bpc_links, item_population_elaborations, item_population_links, jurisdictional_values, room_items, source_value_extractions, spec_value_probes, specifications, term_item_links | slugs |
| `jurisdictional_values` | 109 | — | items |
| `lang_jur_map` | 70 | — | — |
| `life_stage_modifiers` | 2 | — | — |
| `pipeline_runs` | 0 | — | — |
| `population_axis_map` | 53 | — | axes, populations |
| `population_reclass` | 29 | — | — |
| `populations` | 23 | case_study_populations, citation_population_links, economics_entry_populations, extraction_population_links, item_population_elaborations, item_population_links, population_axis_map, populations, probe_population_links, source_value_extractions, specifications | populations |
| `probe_population_links` | 0 | — | populations, spec_value_probes |
| `reasoning_doc_citations` | 0 | citation_population_links, source_value_extractions | evidence_sources, slugs |
| `room_items` | 0 | — | items, rooms |
| `rooms` | 17 | room_items | — |
| `search_admissions` | 0 | — | evidence_sources, search_executions |
| `search_candidates` | 0 | — | search_executions, slugs |
| `search_coverage` | 0 | — | slugs |
| `search_executions` | 0 | search_admissions, search_candidates | slugs |
| `search_languages` | 0 | — | slugs |
| `situations` | 0 | — | — |
| `slugs` | 106 | bpc_metadata, case_studies, citation_mining, item_bpc_links, items, reasoning_doc_citations, search_candidates, search_coverage, search_executions, search_languages, slugs, source_slug_links, source_value_extractions, spec_value_probes, supersession_check | slugs |
| `source_locators` | 835 | — | — |
| `source_slug_links` | 0 | — | evidence_sources, slugs |
| `source_value_extractions` | 0 | extraction_population_links | evidence_sources, items, populations, reasoning_doc_citations, slugs |
| `spec_value_probes` | 0 | probe_population_links | evidence_sources, items, slugs |
| `specification_source_links` | 0 | — | evidence_sources, specifications |
| `specifications` | 0 | specification_source_links | convergence_assessment, gaps, items, populations |
| `supersession_check` | 0 | — | evidence_sources, slugs |
| `term_aliases` | 2382 | — | terms |
| `term_item_links` | 147 | — | items, terms |
| `terms` | 88 | term_aliases, term_item_links | — |
| `url_verification_runs` | 0 | — | — |
| `weighting_profile` | 5 | — | — |

### [0271] A5 — all tables   `2026-08-12 08:35:28Z`
**Action:** reverse-direction analysis: inbound edges, isolated tables, referenced-but-empty
**Expected:** connected schema
**Actual:** isolated (no inbound AND no outbound FK): ['access_duration', 'access_stakes', 'data_migrations', 'db_meta', 'decisions', 'external_root_registry', 'lang_jur_map', 'life_stage_modifiers', 'pipeline_runs', 'population_reclass', 'situations', 'source_locators', 'url_verification_runs', 'weighting_profile'] · referenced-but-EMPTY parent tables: ['case_studies', 'connections', 'convergence_assessment', 'economics_entries', 'evidence_sources', 'gaps', 'reasoning_doc_citations', 'search_executions', 'source_value_extractions', 'spec_value_probes', 'specifications'] · empty tables total: 42/66
**Verdict:** `ORPHAN`

### A6 — CHECK-constraint battery (127 clauses), FK=ON and FK=OFF

### [0272] A6/ON — access_duration CHECK(code IN ('permanent','temporary','situational'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (code outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "access_duration" ("code", "definition") VALUES (?, ?)  -- {"code": "PROBE-INVALID-ENUM", "definition": "PROBE-DEFINITION"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: code IN ('permanent','temporary','situational')`
**Verdict:** `OK`

### [0273] A6/ON — access_need_axis_map CHECK(relationship IN ('primary','partial','spans'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (relationship outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "access_need_axis_map" ("need_code", "axis_code", "relationship") VALUES (?, ?, ?)  -- {"need_code": "A-AT", "axis_code": "AX-AMB", "relationship": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: relationship IN ('primary','partial','spans')`
**Verdict:** `OK`

### [0274] A6/ON — access_need_icf CHECK(icf_type IN ('b','d','e','s'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (icf_type outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "access_need_icf" ("need_code", "icf_code", "icf_type", "confidence") VALUES (?, ?, ?, ?)  -- {"need_code": "A-AT", "icf_code": "PROBE-303", "icf_type": "PROBE-INVALID-ENUM", "confidence": "confirmed"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: icf_type IN ('b','d','e','s')`
**Verdict:** `OK`

### [0275] A6/ON — access_need_icf CHECK(confidence IN ('confirmed','proposed'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (confidence outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "access_need_icf" ("need_code", "icf_code", "icf_type", "confidence") VALUES (?, ?, ?, ?)  -- {"need_code": "A-AT", "icf_code": "PROBE-304", "icf_type": "b", "confidence": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: confidence IN ('confirmed','proposed')`
**Verdict:** `OK`

### [0276] A6/ON — access_needs CHECK(family IN ('perceiving','communicating','operating','pacing','environment_safety'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (family outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "access_needs" ("need_code", "family", "design_obligation") VALUES (?, ?, ?)  -- {"need_code": "PROBE-306", "family": "PROBE-INVALID-ENUM", "design_obligation": "PROBE-307"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: family IN
                    ('perceiving','communicating','operating','pacing','environment_safety')`
**Verdict:** `OK`

### [0277] A6/ON — access_needs CHECK(typical_stakes IN ('safety-critical','exclusion','friction'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (typical_stakes outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "access_needs" ("need_code", "family", "design_obligation", "typical_stakes") VALUES (?, ?, ?, ?)  -- {"need_code": "PROBE-308", "family": "perceiving", "design_obligation": "PROBE-309", "typical_stakes": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: typical_stakes IN ('safety-critical','exclusion','friction')`
**Verdict:** `OK`

### [0278] A6/ON — access_stakes CHECK(code IN ('safety-critical','exclusion','friction'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (code outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "access_stakes" ("code", "definition") VALUES (?, ?)  -- {"code": "PROBE-INVALID-ENUM", "definition": "PROBE-DEFINITION"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: code IN ('safety-critical','exclusion','friction')`
**Verdict:** `OK`

### [0279] A6/ON — axes CHECK(coverage_status IN ('ESTABLISHED','PARTIAL','STUB'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (coverage_status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "axes" ("axis_code", "name", "mechanism", "coverage_status", "falsification_condition") VALUES (?, ?, ?, ?, ?)  -- {"axis_code": "PROBE-318", "name": "PROBE-319", "mechanism": "PROBE-320", "coverage_status": "PROBE-INVALID-ENUM", "falsification_condition": "PROBE-321"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: coverage_status IN ('ESTABLISHED','PARTIAL','STUB')`
**Verdict:** `OK`

### [0280] A6/ON — bpc_metadata CHECK(pico_complete IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (pico_complete outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "pico_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-322", "created_at": "PROBE-323", "created_by_session": "PROBE-324", "updated_at": "PROBE-325", "updated_by_session": "PROBE-326", "pico_complete": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: pico_complete IN (0,1)`
**Verdict:** `OK`

### [0281] A6/ON — bpc_metadata CHECK(search_complete IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (search_complete outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "search_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-327", "created_at": "PROBE-328", "created_by_session": "PROBE-329", "updated_at": "PROBE-330", "updated_by_session": "PROBE-331", "search_complete": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: search_complete IN (0,1)`
**Verdict:** `OK`

### [0282] A6/ON — bpc_metadata CHECK(bpc_complete IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (bpc_complete outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "bpc_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-332", "created_at": "PROBE-333", "created_by_session": "PROBE-334", "updated_at": "PROBE-335", "updated_by_session": "PROBE-336", "bpc_complete": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: bpc_complete IN (0,1)`
**Verdict:** `OK`

### [0283] A6/ON — bpc_metadata CHECK(citation_mining_complete IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (citation_mining_complete outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "citation_mining_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-337", "created_at": "PROBE-338", "created_by_session": "PROBE-339", "updated_at": "PROBE-340", "updated_by_session": "PROBE-341", "citation_mining_complete": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: citation_mining_complete IN (0,1)`
**Verdict:** `OK`

### [0284] A6/ON — bpc_metadata CHECK(supersession_check_complete IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (supersession_check_complete outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "supersession_check_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-342", "created_at": "PROBE-343", "created_by_session": "PROBE-344", "updated_at": "PROBE-345", "updated_by_session": "PROBE-346", "supersession_check_complete": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: supersession_check_complete IN (0, 1)`
**Verdict:** `OK`

### [0285] A6/ON — bpc_metadata CHECK(closure_definition_version IS NULL OR closure_definition_version IN ('v1', 'v2'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (closure_definition_version outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "closure_definition_version") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-347", "created_at": "PROBE-348", "created_by_session": "PROBE-349", "updated_at": "PROBE-350", "updated_by_session": "PROBE-351", "closure_definition_version": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: closure_definition_version IS NULL OR closure_definition_version IN ('v1', 'v2')`
**Verdict:** `OK`

### [0286] A6/ON — case_studies CHECK(evidence_quality_tier IS NULL OR evidence_quality_tier BETWEEN 1 AND 3)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (evidence_quality_tier above range; FK=ON)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session", "evidence_quality_tier") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-352", "slug": "PROBE-PK-158", "title": "PROBE-353", "building_type": "PROBE-354", "location": "PROBE-355", "created_at": "PROBE-356", "created_by_session": "PROBE-357", "evidence_quality_tier": 4}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: evidence_quality_tier IS NULL
                                        OR evidence_quality_tier BETWEEN 1 AND 3`
**Verdict:** `OK`

### [0287] A6/ON — case_studies CHECK(cost_data_quality IS NULL OR cost_data_quality IN ('VERIFIED','PROVISIONAL','GREY'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (cost_data_quality outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session", "cost_data_quality") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-358", "slug": "PROBE-PK-158", "title": "PROBE-359", "building_type": "PROBE-360", "location": "PROBE-361", "created_at": "PROBE-362", "created_by_session": "PROBE-363", "cost_data_quality": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: cost_data_quality IS NULL OR cost_data_quality IN
                     ('VERIFIED','PROVISIONAL','GREY')`
**Verdict:** `OK`

### [0288] A6/ON — case_studies CHECK(harm_finding IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (harm_finding outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session", "harm_finding") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-364", "slug": "PROBE-PK-158", "title": "PROBE-365", "building_type": "PROBE-366", "location": "PROBE-367", "created_at": "PROBE-368", "created_by_session": "PROBE-369", "harm_finding": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: harm_finding IN (0,1)`
**Verdict:** `OK`

### [0289] A6/ON — case_study_outcomes CHECK(tier IS NULL OR tier BETWEEN 1 AND 3)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (tier above range; FK=ON)
**SQL:**
```sql
INSERT INTO "case_study_outcomes" ("case_study_id", "metric", "tier") VALUES (?, ?, ?)  -- {"case_study_id": "PROBE-CASE_STUDY_ID", "metric": "PROBE-370", "tier": 4}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: tier IS NULL OR tier BETWEEN 1 AND 3`
**Verdict:** `OK`

### [0290] A6/ON — citation_mining CHECK(backward IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (backward outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session", "backward") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "aac-speech-production-environments", "local_ref_id": "PROBE-371", "created_at": "PROBE-372", "created_by_session": "PROBE-373", "updated_at": "PROBE-374", "updated_by_session": "PROBE-375", "backward": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: backward IN (0,1)`
**Verdict:** `OK`

### [0291] A6/ON — citation_mining CHECK(forward IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (forward outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session", "forward") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "aac-speech-production-environments", "local_ref_id": "PROBE-376", "created_at": "PROBE-377", "created_by_session": "PROBE-378", "updated_at": "PROBE-379", "updated_by_session": "PROBE-380", "forward": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: forward IN (0,1)`
**Verdict:** `OK`

### [0292] A6/ON — conflicts CHECK(status IN ( 'RESOLVED-EVIDENCE', 'RESOLVED-CONSENSUS', 'RESOLUTION-PROPOSED', 'UNRESOLVED', 'MODE-S-ONLY' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-381", "domain": "PROBE-382", "pop_a": "PROBE-383", "pop_b": "PROBE-384", "status": "PROBE-INVALID-ENUM", "created_at": "PROBE-385", "created_by_session": "PROBE-386", "updated_at": "PROBE-387", "updated_by_session": "PROBE-388"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN (
                            'RESOLVED-EVIDENCE',
                            'RESOLVED-CONSENSUS',
                            'RESOLUTION-PROPOSED',
                            'UNRESOLVED',
                            'MODE-S-ONLY'
                        )`
**Verdict:** `OK`

### [0293] A6/ON — connections CHECK(status IN ( 'PENDING','CONSUMED','CONSUMED-DEFERRED','CLOSED' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-390", "status": "PROBE-INVALID-ENUM", "confidence": "HIGH", "filed_in": "PROBE-391", "created_at": "PROBE-392", "created_by_session": "PROBE-393", "updated_at": "PROBE-394", "updated_by_session": "PROBE-395"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN (
                            'PENDING','CONSUMED','CONSUMED-DEFERRED','CLOSED'
                        )`
**Verdict:** `OK`

### [0294] A6/ON — connections CHECK(confidence IN ('HIGH','MODERATE','SPECULATIVE'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (confidence outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-396", "status": "PENDING", "confidence": "PROBE-INVALID-ENUM", "filed_in": "PROBE-397", "created_at": "PROBE-398", "created_by_session": "PROBE-399", "updated_at": "PROBE-400", "updated_by_session": "PROBE-401"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: confidence IN ('HIGH','MODERATE','SPECULATIVE')`
**Verdict:** `OK`

### [0295] A6/ON — connections CHECK(connection_type IN ( 'CROSS-POPULATION','CROSS-ITEM', 'COMPOUND-INTERACTION','METHODOLOGY' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (connection_type outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session", "connection_type") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-402", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-403", "created_at": "PROBE-404", "created_by_session": "PROBE-405", "updated_at": "PROBE-406", "updated_by_session": "PROBE-407", "connection_type": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: connection_type IN (
                            'CROSS-POPULATION','CROSS-ITEM',
                            'COMPOUND-INTERACTION','METHODOLOGY'
                        )`
**Verdict:** `OK`

### [0296] A6/ON — connections CHECK(opus_reviewed IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (opus_reviewed outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session", "opus_reviewed") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-408", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-409", "created_at": "PROBE-410", "created_by_session": "PROBE-411", "updated_at": "PROBE-412", "updated_by_session": "PROBE-413", "opus_reviewed": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: opus_reviewed IN (0,1)`
**Verdict:** `OK`

### [0297] A6/ON — convergence_assessment CHECK(status IN ('convergent', 'divergent', 'single_axis', 'pending_assessment'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "convergence_assessment" ("status") VALUES (?)  -- {"status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('convergent', 'divergent',
                                              'single_axis', 'pending_assessment')`
**Verdict:** `OK`

### [0298] A6/ON — decisions CHECK(category IN ( 'D-DOCT','D-METH','D-SCHEMA','D-OP','D-PRES' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (category outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-415", "category": "PROBE-INVALID-ENUM", "delegation": "DG-NON", "summary": "PROBE-416", "outcome": "PROBE-417", "rationale": "PROBE-418", "decision_date": "PROBE-419", "decided_by": "PROBE-420", "model_routing": "PROBE-421", "effort_level": 1, "review_status": "PROBE-422", "created_at": "PROBE-423", "created_by_session": "PROBE-424", "updated_at": "PROBE-425", "updated_by_session": "PROBE-426"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: category IN (
                            'D-DOCT','D-METH','D-SCHEMA','D-OP','D-PRES'
                        )`
**Verdict:** `OK`

### [0299] A6/ON — decisions CHECK(delegation IN ('DG-NON','DG-REVIEW','DG-AUTO'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (delegation outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-427", "category": "D-DOCT", "delegation": "PROBE-INVALID-ENUM", "summary": "PROBE-428", "outcome": "PROBE-429", "rationale": "PROBE-430", "decision_date": "PROBE-431", "decided_by": "PROBE-432", "model_routing": "PROBE-433", "effort_level": 1, "review_status": "PROBE-434", "created_at": "PROBE-435", "created_by_session": "PROBE-436", "updated_at": "PROBE-437", "updated_by_session": "PROBE-438"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: delegation IN ('DG-NON','DG-REVIEW','DG-AUTO')`
**Verdict:** `OK`

### [0300] A6/ON — decisions CHECK(status IN ( 'ACTIVE','SUPERSEDED','WITHDRAWN','PROPOSED','PROVISIONAL' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-439", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-440", "outcome": "PROBE-441", "rationale": "PROBE-442", "decision_date": "PROBE-443", "decided_by": "PROBE-444", "model_routing": "PROBE-445", "effort_level": 1, "review_status": "PROBE-446", "created_at": "PROBE-447", "created_by_session": "PROBE-448", "updated_at": "PROBE-449", "updated_by_session": "PROBE-450", "status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN (
                            'ACTIVE','SUPERSEDED','WITHDRAWN','PROPOSED','PROVISIONAL'
                        )`
**Verdict:** `OK`

### [0301] A6/ON — economics_entries CHECK(pillar IN ('health','inaction','construction','market'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (pillar outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-451", "pillar": "PROBE-INVALID-ENUM", "entry_type": "cost_premium", "source": "PROBE-452", "finding": "PROBE-453", "created_at": "PROBE-454", "created_by_session": "PROBE-455"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: pillar IN ('health','inaction','construction','market')`
**Verdict:** `OK`

### [0302] A6/ON — economics_entries CHECK(entry_type IN ('cost_premium','retrofit_multiplier','grant_programme','health_outcome', 'market_value','housin)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (entry_type outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-456", "pillar": "health", "entry_type": "PROBE-INVALID-ENUM", "source": "PROBE-457", "finding": "PROBE-458", "created_at": "PROBE-459", "created_by_session": "PROBE-460"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: entry_type IN
                    ('cost_premium','retrofit_multiplier','grant_programme','health_outcome',
                     'market_value','housing_deficit','research_gap')`
**Verdict:** `OK`

### [0303] A6/ON — economics_entries CHECK(evidence_tier IS NULL OR evidence_tier BETWEEN 1 AND 6)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (evidence_tier above range; FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session", "evidence_tier") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-461", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-462", "finding": "PROBE-463", "created_at": "PROBE-464", "created_by_session": "PROBE-465", "evidence_tier": 7}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: evidence_tier IS NULL OR evidence_tier BETWEEN 1 AND 6`
**Verdict:** `OK`

### [0304] A6/ON — economics_entries CHECK(confidence IS NULL OR confidence IN ('HIGH','MODERATE','LOW'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (confidence outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session", "confidence") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-466", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-467", "finding": "PROBE-468", "created_at": "PROBE-469", "created_by_session": "PROBE-470", "confidence": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: confidence IS NULL OR confidence IN ('HIGH','MODERATE','LOW')`
**Verdict:** `OK`

### [0305] A6/ON — economics_entries CHECK(quant_status IS NULL OR quant_status IN ('VERIFIED-QUANT','UNVERIFIED-QUANT'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (quant_status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session", "quant_status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-471", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-472", "finding": "PROBE-473", "created_at": "PROBE-474", "created_by_session": "PROBE-475", "quant_status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: quant_status IS NULL OR quant_status IN
                    ('VERIFIED-QUANT','UNVERIFIED-QUANT')`
**Verdict:** `OK`

### [0306] A6/ON — evidence_population_match CHECK(match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (match_grade outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-476", "source_ref": "PROBE-477", "target_population": "PROBE-478", "match_grade": "PROBE-INVALID-ENUM", "created_at": "PROBE-479", "created_by_session": "PROBE-480"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH')`
**Verdict:** `OK`

### [0307] A6/ON — evidence_sources CHECK(scope IS NULL OR scope IN ( 'high_control', 'lower_control', 'national', 'international', 'intrinsic' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (scope outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "scope") VALUES (?, ?)  -- {"ref_id": "PROBE-482", "scope": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: scope IS NULL OR scope IN (
    'high_control', 'lower_control', 'national', 'international', 'intrinsic'
  )`
**Verdict:** `OK`

### [0308] A6/ON — evidence_sources CHECK(data_capture_status IN ('pending','captured','none-extractable','deferred'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (data_capture_status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "data_capture_status") VALUES (?, ?)  -- {"ref_id": "PROBE-483", "data_capture_status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: data_capture_status IN ('pending','captured','none-extractable','deferred')`
**Verdict:** `OK`

### [0309] A6/ON — evidence_sources CHECK(citation_mining_status IN ('pending','mined','deferred','not-applicable'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (citation_mining_status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "citation_mining_status") VALUES (?, ?)  -- {"ref_id": "PROBE-484", "citation_mining_status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: citation_mining_status IN ('pending','mined','deferred','not-applicable')`
**Verdict:** `OK`

### [0310] A6/ON — evidence_sources CHECK(processing_blocked_reason IS NULL OR processing_blocked_reason IN ( 'no-full-text', 'paywalled', 'no-doi', 'no)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (processing_blocked_reason outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "processing_blocked_reason") VALUES (?, ?)  -- {"ref_id": "PROBE-485", "processing_blocked_reason": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: processing_blocked_reason IS NULL OR processing_blocked_reason IN (
    'no-full-text',        -- full text could not be obtained
    'paywalled',           -- access blocked by paywall
    'no-doi',              -- no resolvable identifier for automated paths
    'not-indexed',         -- absent from the indexes the pipeline queries
    'language',            -- awaiting in-language reading capacity
    'no-quantified-claims',-- read; carries no extractable value
    'superseded',          -- superseded by another source
    'out-of-scope',        -- outside the corpus this project extracts from
    'tier-not-required'    -- tier does not oblige the work
  )`
**Verdict:** `OK`

### [0311] A6/ON — evidence_sources CHECK(verification_disposition IS NULL OR verification_disposition IN ('OPEN','CLOSED'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (verification_disposition outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "verification_disposition") VALUES (?, ?)  -- {"ref_id": "PROBE-486", "verification_disposition": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: verification_disposition IS NULL
         OR verification_disposition IN ('OPEN','CLOSED')`
**Verdict:** `OK`

### [0312] A6/ON — evidence_sources CHECK(verification_method IS NULL OR verification_method IN ( 'direct-render', 'co1-attestation', 'corroborated-not-)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (verification_method outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "verification_method") VALUES (?, ?)  -- {"ref_id": "PROBE-487", "verification_method": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: verification_method IS NULL OR verification_method IN (
    'direct-render',              -- the document was fetched and read
    'co1-attestation',            -- the attestation itself was obtained (DR 3.1)
    'corroborated-not-retrieved', -- >=2 independent retrievals agree; doc not obtained
    'citing-bibliography',        -- existence attested only by another work's references
    'tool'                        -- resolve_dois / verify_urls; verified_by_tool names which
  )`
**Verdict:** `OK`

### [0313] A6/ON — evidence_sources CHECK(verification_closure_reason IS NULL OR verification_closure_reason IN ( 'paywalled', 'print-only', 'access-den)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (verification_closure_reason outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "verification_closure_reason") VALUES (?, ?)  -- {"ref_id": "PROBE-488", "verification_closure_reason": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: verification_closure_reason IS NULL OR verification_closure_reason IN (
    'paywalled',
    'print-only',
    'access-denied-persistent',
    'withdrawn',
    'not-found-after-search',
    'disputed-existence'          -- owner ruling: there may be no resolution
  )`
**Verdict:** `OK`

### [0314] A6/ON — external_root_registry CHECK(root_type IN ( 'measurement_primary', 'participatory_finding', 'committee_assertion', 'derived_calculation', ')   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (root_type outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "external_root_registry" ("root_id", "description", "root_type") VALUES (?, ?, ?)  -- {"root_id": "PROBE-490", "description": "PROBE-491", "root_type": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: root_type IN (
                              'measurement_primary', 'participatory_finding',
                              'committee_assertion', 'derived_calculation',
                              'untraced')`
**Verdict:** `OK`

### [0315] A6/ON — gap_mining CHECK(outcome IN ( 'closure_evidence_found', 'partial_evidence_found', 'null_result', 'gap_recategorized', 'deferred)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-492", "attempt_at": "PROBE-493", "attempted_by_session": "PROBE-494", "search_strategy_record": "PROBE-495", "outcome": "PROBE-INVALID-ENUM", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-496"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: outcome IN (
        'closure_evidence_found',  -- enough to close the gap (rule #7 must fire)
        'partial_evidence_found',  -- some discoveries; gap stays OPEN with annotation
        'null_result',             -- searches ran clean, no relevant discoveries
        'gap_recategorized',       -- gap not mining-addressable after all
        'deferred'                 -- connectors unavailable / other blocker
    )`
**Verdict:** `OK`

### [0316] A6/ON — gap_mining CHECK(check_method IN ( 'pubmed_cluster', 'scholar_gateway_lived_experience', 'cochrane_direct', 'standards_body_dir)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (check_method outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-492", "attempt_at": "PROBE-497", "attempted_by_session": "PROBE-498", "search_strategy_record": "PROBE-499", "outcome": "closure_evidence_found", "check_method": "PROBE-INVALID-ENUM", "discoveries_logged": "PROBE-500"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: check_method IN (
        'pubmed_cluster',
        'scholar_gateway_lived_experience',
        'cochrane_direct',
        'standards_body_direct',
        'multilingual_research',
        'composite'
    )`
**Verdict:** `OK`

### [0317] A6/ON — gap_mining CHECK( outcome != 'closure_evidence_found' OR (discoveries_logged IS NOT NULL AND discoveries_logged != '[]') )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome='closure_evidence_found' with discoveries_logged NULL; FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-492", "attempt_at": "PROBE-501", "attempted_by_session": "PROBE-502", "search_strategy_record": "PROBE-503", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": null}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: outcome != 'closure_evidence_found'
        OR (discoveries_logged IS NOT NULL AND discoveries_logged != '[]')`
**Verdict:** `OK`

### [0318] A6/ON — gap_mining CHECK( outcome != 'gap_recategorized' OR (notes IS NOT NULL AND length(notes) >= 20) )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome='gap_recategorized' with notes NULL; FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged", "notes") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-492", "attempt_at": "PROBE-504", "attempted_by_session": "PROBE-505", "search_strategy_record": "PROBE-506", "outcome": "gap_recategorized", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-507", "notes": null}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: outcome != 'gap_recategorized'
        OR (notes IS NOT NULL AND length(notes) >= 20)`
**Verdict:** `OK`

### [0319] A6/ON — gap_mining CHECK( outcome != 'deferred' OR (notes IS NOT NULL AND length(notes) >= 10) )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome='deferred' with notes NULL; FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged", "notes") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-492", "attempt_at": "PROBE-508", "attempted_by_session": "PROBE-509", "search_strategy_record": "PROBE-510", "outcome": "deferred", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-511", "notes": null}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: outcome != 'deferred'
        OR (notes IS NOT NULL AND length(notes) >= 10)`
**Verdict:** `OK`

### [0320] A6/ON — gaps CHECK(category IN ( 'RP','SW','CR','ST','MX','CD','EC','EG', 'CI','DEC','CONF','AUDT' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (category outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-513", "category": "PROBE-INVALID-ENUM", "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-514", "created_at": "PROBE-515", "created_by_session": "PROBE-516", "updated_at": "PROBE-517", "updated_by_session": "PROBE-518"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: category IN (
                            'RP','SW','CR','ST','MX','CD','EC','EG',
                            'CI','DEC','CONF','AUDT'
                        )`
**Verdict:** `OK`

### [0321] A6/ON — gaps CHECK(priority IN ('P1','P2','P3'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (priority outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-519", "category": "RP", "priority": "PROBE-INVALID-ENUM", "status": "OPEN-PROBE", "description": "PROBE-520", "created_at": "PROBE-521", "created_by_session": "PROBE-522", "updated_at": "PROBE-523", "updated_by_session": "PROBE-524"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: priority IN ('P1','P2','P3')`
**Verdict:** `OK`

### [0322] A6/ON — gaps CHECK(status LIKE 'OPEN%' OR status LIKE 'CLOSED%')   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status fails LIKE; FK=ON)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-525", "category": "RP", "priority": "P1", "status": "PROBE-NOLIKE", "description": "PROBE-526", "created_at": "PROBE-527", "created_by_session": "PROBE-528", "updated_at": "PROBE-529", "updated_by_session": "PROBE-530"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status LIKE 'OPEN%' OR status LIKE 'CLOSED%'`
**Verdict:** `OK`

### [0323] A6/ON — gaps CHECK(mining_addressability IS NULL OR mining_addressability IN ( 'ADDRESSABLE', 'NOT-ADDRESSABLE', 'TRIAGE-NEEDED' )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (mining_addressability outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session", "mining_addressability") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-531", "category": "RP", "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-532", "created_at": "PROBE-533", "created_by_session": "PROBE-534", "updated_at": "PROBE-535", "updated_by_session": "PROBE-536", "mining_addressability": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: mining_addressability IS NULL OR mining_addressability IN (
        'ADDRESSABLE',
        'NOT-ADDRESSABLE',
        'TRIAGE-NEEDED'
    )`
**Verdict:** `OK`

### [0324] A6/ON — item_audit_runs CHECK(status IN ('IN-PROGRESS','COMPLETE','HANDED-OFF'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-538", "item_code": "A-01", "session": "PROBE-539", "created_at": "PROBE-540", "created_by_session": "PROBE-541", "updated_at": "PROBE-542", "updated_by_session": "PROBE-543", "status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('IN-PROGRESS','COMPLETE','HANDED-OFF')`
**Verdict:** `OK`

### [0325] A6/ON — item_axis_links CHECK(strength_band IN ('full','partial','weak'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (strength_band outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "item_axis_links" ("item_code", "axis_code", "strength_band") VALUES (?, ?, ?)  -- {"item_code": "A-01", "axis_code": "AX-AMB", "strength_band": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: strength_band IN ('full','partial','weak')`
**Verdict:** `OK`

### [0326] A6/ON — item_axis_links CHECK(use_mode IN ('independent','assisted','collective') OR use_mode IS NULL)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (use_mode outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "item_axis_links" ("item_code", "axis_code", "use_mode") VALUES (?, ?, ?)  -- {"item_code": "A-01", "axis_code": "AX-AMB", "use_mode": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: use_mode IN ('independent','assisted','collective') OR use_mode IS NULL`
**Verdict:** `OK`

### [0327] A6/ON — item_bpc_links CHECK(link_type IN ( 'primary','parameter','context','secondary' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (link_type outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "item_bpc_links" ("item_code", "slug", "link_type", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?)  -- {"item_code": "A-01", "slug": "PROBE-PK-158", "link_type": "PROBE-INVALID-ENUM", "created_at": "PROBE-544", "created_by_session": "PROBE-545"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: link_type IN (
        'primary','parameter','context','secondary'
    )`
**Verdict:** `OK`

### [0328] A6/ON — item_population_links CHECK(applicability IN ( 'applies', 'applies_strictly', 'applies_loosely', 'context_dependent', 'does_not_apply' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (applicability outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "item_population_links" ("item_code", "population_code", "subtype", "applicability") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "subtype": "PROBE-547", "applicability": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: applicability IN (
                        'applies', 'applies_strictly', 'applies_loosely',
                        'context_dependent', 'does_not_apply'
                      )`
**Verdict:** `OK`

### [0329] A6/ON — items CHECK(category IN ( 'A','B','C','D','E','F','G','H','I','J','K' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (category outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-548", "category": "PROBE-INVALID-ENUM", "name": "PROBE-549", "created_at": "PROBE-550", "created_by_session": "PROBE-551", "updated_at": "PROBE-552", "updated_by_session": "PROBE-553"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: category IN (
                            'A','B','C','D','E','F','G','H','I','J','K'
                        )`
**Verdict:** `OK`

### [0330] A6/ON — items CHECK(status IN ('draft','active','merged','retired'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-554", "category": "A", "name": "PROBE-555", "created_at": "PROBE-556", "created_by_session": "PROBE-557", "updated_at": "PROBE-558", "updated_by_session": "PROBE-559", "status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('draft','active','merged','retired')`
**Verdict:** `OK`

### [0331] A6/ON — jurisdictional_values CHECK(is_code_minimum IS NULL OR is_code_minimum IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (is_code_minimum outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "jurisdictional_values" ("item_code", "jurisdiction", "is_code_minimum") VALUES (?, ?, ?)  -- {"item_code": "A-01", "jurisdiction": "PROBE-560", "is_code_minimum": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: is_code_minimum IS NULL OR is_code_minimum IN (0, 1)`
**Verdict:** `OK`

### [0332] A6/ON — lang_jur_map CHECK(role IN ('PRIMARY', 'SECONDARY'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (role outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "lang_jur_map" ("language", "jurisdiction", "role") VALUES (?, ?, ?)  -- {"language": "PROBE-561", "jurisdiction": "PROBE-562", "role": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: role IN ('PRIMARY', 'SECONDARY')`
**Verdict:** `OK`

### [0333] A6/ON — life_stage_modifiers CHECK(code IN ('SEN','CHD'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (code outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "life_stage_modifiers" ("code", "label", "definition") VALUES (?, ?, ?)  -- {"code": "PROBE-INVALID-ENUM", "label": "PROBE-LABEL", "definition": "PROBE-DEFINITION"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: code IN ('SEN','CHD')`
**Verdict:** `OK`

### [0334] A6/ON — population_axis_map CHECK(role IN ('ALIAS','PRIMARY','SECONDARY','SITUATIONAL'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (role outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "population_axis_map" ("population_code", "axis_code", "role") VALUES (?, ?, ?)  -- {"population_code": "ADHD", "axis_code": "AX-AMB", "role": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: role IN ('ALIAS','PRIMARY','SECONDARY','SITUATIONAL')`
**Verdict:** `OK`

### [0335] A6/ON — population_reclass CHECK(row_kind IN ('EXISTING-POP','NEW-PROFILE'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (row_kind outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale") VALUES (?, ?, ?, ?)  -- {"population_code": "PROBE-571", "row_kind": "PROBE-INVALID-ENUM", "layer": "AXIS-ALIAS", "rationale": "PROBE-572"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: row_kind IN ('EXISTING-POP','NEW-PROFILE')`
**Verdict:** `OK`

### [0336] A6/ON — population_reclass CHECK(layer IN ('AXIS-ALIAS','PROFILE','QUALIFIER','SPLIT'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (layer outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale") VALUES (?, ?, ?, ?)  -- {"population_code": "PROBE-573", "row_kind": "EXISTING-POP", "layer": "PROBE-INVALID-ENUM", "rationale": "PROBE-574"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: layer IN ('AXIS-ALIAS','PROFILE','QUALIFIER','SPLIT')`
**Verdict:** `OK`

### [0337] A6/ON — population_reclass CHECK(profile_kind IN ('diagnostic','identity-cultural','demographic','anthropometric','compound','umbrella'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (profile_kind outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale", "profile_kind") VALUES (?, ?, ?, ?, ?)  -- {"population_code": "PROBE-575", "row_kind": "EXISTING-POP", "layer": "AXIS-ALIAS", "rationale": "PROBE-576", "profile_kind": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: profile_kind IN
                     ('diagnostic','identity-cultural','demographic','anthropometric','compound','umbrella')`
**Verdict:** `OK`

### [0338] A6/ON — population_reclass CHECK(mapping_confidence IN ('high','moderate','low','minimal','TO-ASSESS') OR mapping_confidence IS NULL)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (mapping_confidence outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale", "mapping_confidence") VALUES (?, ?, ?, ?, ?)  -- {"population_code": "PROBE-577", "row_kind": "EXISTING-POP", "layer": "AXIS-ALIAS", "rationale": "PROBE-578", "mapping_confidence": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: mapping_confidence IN
                     ('high','moderate','low','minimal','TO-ASSESS') OR mapping_confidence IS NULL`
**Verdict:** `OK`

### [0339] A6/ON — population_reclass CHECK(fluctuating IN ('yes','no') OR fluctuating IS NULL)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (fluctuating outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale", "fluctuating") VALUES (?, ?, ?, ?, ?)  -- {"population_code": "PROBE-579", "row_kind": "EXISTING-POP", "layer": "AXIS-ALIAS", "rationale": "PROBE-580", "fluctuating": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: fluctuating IN ('yes','no') OR fluctuating IS NULL`
**Verdict:** `OK`

### [0340] A6/ON — populations CHECK(category IN ( 'mobility', 'sensory', 'cognitive', 'mental_health', 'pain_fatigue', 'neurological', 'developmen)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (category outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "populations" ("population_code", "display_name", "category") VALUES (?, ?, ?)  -- {"population_code": "PROBE-581", "display_name": "PROBE-582", "category": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: category IN (
                        'mobility', 'sensory', 'cognitive', 'mental_health',
                        'pain_fatigue', 'neurological', 'developmental',
                        'general'
                      )`
**Verdict:** `OK`

### [0341] A6/ON — populations CHECK(is_compound IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (is_compound outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "populations" ("population_code", "display_name", "is_compound") VALUES (?, ?, ?)  -- {"population_code": "PROBE-583", "display_name": "PROBE-584", "is_compound": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: is_compound IN (0,1)`
**Verdict:** `OK`

### [0342] A6/ON — populations CHECK(status IN ('active', 'deprecated'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "populations" ("population_code", "display_name", "status") VALUES (?, ?, ?)  -- {"population_code": "PROBE-585", "display_name": "PROBE-586", "status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('active', 'deprecated')`
**Verdict:** `OK`

### [0343] A6/ON — reasoning_doc_citations CHECK(claim_type IN ( 'numerical_spec','jurisdiction_value','qualitative','definitional' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (claim_type outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-588", "reasoning_doc_slug": "PROBE-PK-158", "parameter": "PROBE-589", "claim_type": "PROBE-INVALID-ENUM", "source_ref_id": "PROBE-PK-167", "verified_at": "PROBE-590", "verified_by_session": "PROBE-591", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-592", "claim_text": "PROBE-593"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: claim_type IN (
        'numerical_spec','jurisdiction_value','qualitative','definitional'
    )`
**Verdict:** `OK`

### [0344] A6/ON — reasoning_doc_citations CHECK(value_match IN ( 'EXACT','WITHIN-TOLERANCE','DIFFERENT','NOT-FOUND','PAYWALL','SUPERSEDED' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (value_match outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-594", "reasoning_doc_slug": "PROBE-PK-158", "parameter": "PROBE-595", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-167", "verified_at": "PROBE-596", "verified_by_session": "PROBE-597", "value_match": "PROBE-INVALID-ENUM", "claim_match": "SUPPORTED", "claimed_value": "PROBE-598", "claim_text": "PROBE-599"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: value_match IN (
        'EXACT','WITHIN-TOLERANCE','DIFFERENT','NOT-FOUND','PAYWALL','SUPERSEDED'
    )`
**Verdict:** `OK`

### [0345] A6/ON — reasoning_doc_citations CHECK(claim_match IN ( 'SUPPORTED','PARTIAL','NOT-FOUND','PAYWALL','CONTRADICTED' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (claim_match outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-600", "reasoning_doc_slug": "PROBE-PK-158", "parameter": "PROBE-601", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-167", "verified_at": "PROBE-602", "verified_by_session": "PROBE-603", "value_match": "EXACT", "claim_match": "PROBE-INVALID-ENUM", "claimed_value": "PROBE-604", "claim_text": "PROBE-605"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: claim_match IN (
        'SUPPORTED','PARTIAL','NOT-FOUND','PAYWALL','CONTRADICTED'
    )`
**Verdict:** `OK`

### [0346] A6/ON — reasoning_doc_citations CHECK(paywall_purchase_candidate IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (paywall_purchase_candidate outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text", "paywall_purchase_candidate") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-606", "reasoning_doc_slug": "PROBE-PK-158", "parameter": "PROBE-607", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-167", "verified_at": "PROBE-608", "verified_by_session": "PROBE-609", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-610", "claim_text": "PROBE-611", "paywall_purchase_candidate": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: paywall_purchase_candidate IN (0,1)`
**Verdict:** `OK`

### [0347] A6/ON — reasoning_doc_citations CHECK( (claim_type IN ('numerical_spec','jurisdiction_value') AND claimed_value IS NOT NULL AND value_match IS NOT N)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (claim_type outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-612", "reasoning_doc_slug": "PROBE-PK-158", "parameter": "PROBE-613", "claim_type": "PROBE-INVALID-ENUM", "source_ref_id": "PROBE-PK-167", "verified_at": "PROBE-614", "verified_by_session": "PROBE-615", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-616", "claim_text": "PROBE-617"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: claim_type IN (
        'numerical_spec','jurisdiction_value','qualitative','definitional'
    )`
**Verdict:** `OK`

### [0348] A6/ON — room_items CHECK(applicability IN ('applies','conditional','not-applicable'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (applicability outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "room_items" ("room_code", "item_code", "applicability") VALUES (?, ?, ?)  -- {"room_code": "R-ASM", "item_code": "A-01", "applicability": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: applicability IN ('applies','conditional','not-applicable')`
**Verdict:** `OK`

### [0349] A6/ON — rooms CHECK(status IN ('active','draft','retired'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "rooms" ("room_code", "name", "status") VALUES (?, ?, ?)  -- {"room_code": "PROBE-619", "name": "PROBE-620", "status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('active','draft','retired')`
**Verdict:** `OK`

### [0350] A6/ON — search_candidates CHECK(disposition IN ('REHOME','MISCELLANEOUS','PENDING-VERIFICATION','OUT-OF-SCOPE','ADMITTED'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (disposition outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": "aac-speech-production-environments", "disposition": "PROBE-INVALID-ENUM", "title": "PROBE-621", "session": "PROBE-622", "created_at": "PROBE-623"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: disposition IN
                     ('REHOME','MISCELLANEOUS','PENDING-VERIFICATION','OUT-OF-SCOPE','ADMITTED')`
**Verdict:** `OK`

### [0351] A6/ON — search_candidates CHECK(locator_status IS NULL OR locator_status IN ('UNVERIFIED','RESOLVED','DEAD'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (locator_status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at", "locator_status") VALUES (?, ?, ?, ?, ?, ?)  -- {"found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": "PROBE-624", "session": "PROBE-625", "created_at": "PROBE-626", "locator_status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: locator_status IS NULL OR locator_status IN
                     ('UNVERIFIED','RESOLVED','DEAD')`
**Verdict:** `OK`

### [0352] A6/ON — search_candidates CHECK(tier_guess IS NULL OR tier_guess BETWEEN 1 AND 6)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (tier_guess above range; FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at", "tier_guess") VALUES (?, ?, ?, ?, ?, ?)  -- {"found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": "PROBE-627", "session": "PROBE-628", "created_at": "PROBE-629", "tier_guess": 7}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: tier_guess IS NULL OR tier_guess BETWEEN 1 AND 6`
**Verdict:** `OK`

### [0353] A6/ON — search_candidates CHECK(harm_finding IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (harm_finding outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at", "harm_finding") VALUES (?, ?, ?, ?, ?, ?)  -- {"found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": "PROBE-630", "session": "PROBE-631", "created_at": "PROBE-632", "harm_finding": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: harm_finding IN (0,1)`
**Verdict:** `OK`

### [0354] A6/ON — search_coverage CHECK(status IN ('SEARCHED','THIN','NO-DATA','NOT-RUN'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "jurisdiction": "PROBE-633", "status": "PROBE-INVALID-ENUM", "created_at": "PROBE-634", "created_by_session": "PROBE-635", "updated_at": "PROBE-636", "updated_by_session": "PROBE-637"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('SEARCHED','THIN','NO-DATA','NOT-RUN')`
**Verdict:** `OK`

### [0355] A6/ON — search_coverage CHECK(co1_attempted IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (co1_attempted outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "co1_attempted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "jurisdiction": "PROBE-638", "status": "SEARCHED", "created_at": "PROBE-639", "created_by_session": "PROBE-640", "updated_at": "PROBE-641", "updated_by_session": "PROBE-642", "co1_attempted": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: co1_attempted IN (0,1)`
**Verdict:** `OK`

### [0356] A6/ON — search_coverage CHECK(tier5_attempted IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (tier5_attempted outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "tier5_attempted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "jurisdiction": "PROBE-643", "status": "SEARCHED", "created_at": "PROBE-644", "created_by_session": "PROBE-645", "updated_at": "PROBE-646", "updated_by_session": "PROBE-647", "tier5_attempted": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: tier5_attempted IN (0,1)`
**Verdict:** `OK`

### [0357] A6/ON — search_coverage CHECK(tier6_attempted IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (tier6_attempted outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "tier6_attempted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "jurisdiction": "PROBE-648", "status": "SEARCHED", "created_at": "PROBE-649", "created_by_session": "PROBE-650", "updated_at": "PROBE-651", "updated_by_session": "PROBE-652", "tier6_attempted": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: tier6_attempted IN (0,1)`
**Verdict:** `OK`

### [0358] A6/ON — search_executions CHECK(target_tier IS NULL OR target_tier BETWEEN 1 AND 6)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (target_tier above range; FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "target_tier") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-653", "query_text": "PROBE-654", "engine": "PROBE-655", "depth_method": "scoping", "session": "PROBE-656", "executed_at": "PROBE-657", "target_tier": 7}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: target_tier IS NULL OR target_tier BETWEEN 1 AND 6`
**Verdict:** `OK`

### [0359] A6/ON — search_executions CHECK(target_evidence_type IS NULL OR target_evidence_type IN ('clinical','sr_meta','standard_eb','national_fw','cod)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (target_evidence_type outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "target_evidence_type") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-658", "query_text": "PROBE-659", "engine": "PROBE-660", "depth_method": "scoping", "session": "PROBE-661", "executed_at": "PROBE-662", "target_evidence_type": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: target_evidence_type IS NULL OR target_evidence_type IN
     ('clinical','sr_meta','standard_eb','national_fw','code','co1','co2','grey')`
**Verdict:** `OK`

### [0360] A6/ON — search_executions CHECK(target_scope IS NULL OR target_scope IN ('intrinsic','lower_control','high_control','national','international')   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (target_scope outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "target_scope") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-663", "query_text": "PROBE-664", "engine": "PROBE-665", "depth_method": "scoping", "session": "PROBE-666", "executed_at": "PROBE-667", "target_scope": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: target_scope IS NULL OR target_scope IN
     ('intrinsic','lower_control','high_control','national','international')`
**Verdict:** `OK`

### [0361] A6/ON — search_executions CHECK(depth_method IN ('scoping','systematic'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (depth_method outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-668", "query_text": "PROBE-669", "engine": "PROBE-670", "depth_method": "PROBE-INVALID-ENUM", "session": "PROBE-671", "executed_at": "PROBE-672"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: depth_method IN ('scoping','systematic')`
**Verdict:** `OK`

### [0362] A6/ON — search_executions CHECK(mining_direction IS NULL OR mining_direction IN ('none','backward','forward','both'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (mining_direction outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "mining_direction") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-673", "query_text": "PROBE-674", "engine": "PROBE-675", "depth_method": "scoping", "session": "PROBE-676", "executed_at": "PROBE-677", "mining_direction": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: mining_direction IS NULL OR mining_direction IN
     ('none','backward','forward','both')`
**Verdict:** `OK`

### [0363] A6/ON — search_executions CHECK(saturation_signal IS NULL OR saturation_signal IN ('none','partial','saturated'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (saturation_signal outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "saturation_signal") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-678", "query_text": "PROBE-679", "engine": "PROBE-680", "depth_method": "scoping", "session": "PROBE-681", "executed_at": "PROBE-682", "saturation_signal": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: saturation_signal IS NULL OR saturation_signal IN
     ('none','partial','saturated')`
**Verdict:** `OK`

### [0364] A6/ON — search_executions CHECK(backfill IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (backfill outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "backfill") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-683", "query_text": "PROBE-684", "engine": "PROBE-685", "depth_method": "scoping", "session": "PROBE-686", "executed_at": "PROBE-687", "backfill": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: backfill IN (0,1)`
**Verdict:** `OK`

### [0365] A6/ON — search_executions CHECK(terms_used IS NULL OR json_valid(terms_used))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (invalid JSON in terms_used; FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "terms_used") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-688", "query_text": "PROBE-689", "engine": "PROBE-690", "depth_method": "scoping", "session": "PROBE-691", "executed_at": "PROBE-692", "terms_used": "{not-json"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: terms_used IS NULL OR json_valid(terms_used)`
**Verdict:** `OK`

### [0366] A6/ON — search_executions CHECK(admitted_ref_ids IS NULL OR json_valid(admitted_ref_ids))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (invalid JSON in admitted_ref_ids; FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "admitted_ref_ids") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-693", "query_text": "PROBE-694", "engine": "PROBE-695", "depth_method": "scoping", "session": "PROBE-696", "executed_at": "PROBE-697", "admitted_ref_ids": "{not-json"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: admitted_ref_ids IS NULL OR json_valid(admitted_ref_ids)`
**Verdict:** `OK`

### [0367] A6/ON — search_languages CHECK(status IN ('SEARCHED','PARTIAL','NOT-RUN'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-698", "status": "PROBE-INVALID-ENUM", "created_at": "PROBE-699", "created_by_session": "PROBE-700", "updated_at": "PROBE-701", "updated_by_session": "PROBE-702"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('SEARCHED','PARTIAL','NOT-RUN')`
**Verdict:** `OK`

### [0368] A6/ON — situations CHECK(operational_access IN ('yes','no') OR operational_access IS NULL)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (operational_access outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "situations" ("situation_id", "title", "account_language", "account_text_ref", "operational_access") VALUES (?, ?, ?, ?, ?)  -- {"situation_id": "PROBE-704", "title": "PROBE-705", "account_language": "PROBE-706", "account_text_ref": "PROBE-707", "operational_access": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: operational_access IN ('yes','no') OR operational_access IS NULL`
**Verdict:** `OK`

### [0369] A6/ON — slugs CHECK(status IN ( 'ACTIVE','MERGED','STUB','PROVISIONAL' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-708", "topic_directory": "PROBE-709", "sl_path": "PROBE-710", "bpc_path": "PROBE-711", "status": "PROBE-INVALID-ENUM", "created_at": "PROBE-712", "created_by_session": "PROBE-713", "updated_at": "PROBE-714", "updated_by_session": "PROBE-715"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN (
                            'ACTIVE','MERGED','STUB','PROVISIONAL'
                        )`
**Verdict:** `OK`

### [0370] A6/ON — source_locators CHECK(doi IS NOT NULL OR url IS NOT NULL OR pmid IS NOT NULL OR pmcid IS NOT NULL OR isbn IS NOT NULL OR issn IS NOT)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (all of ['doi', 'url', 'pmid', 'pmcid', 'isbn', 'issn', 'standard_number'] NULL; FK=ON)
**SQL:**
```sql
INSERT INTO "source_locators" ("ref_id", "pmcid", "pmid", "url", "standard_number", "doi", "isbn", "issn") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-717", "pmcid": null, "pmid": null, "url": null, "standard_number": null, "doi": null, "isbn": null, "issn": null}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: doi IS NOT NULL OR url IS NOT NULL OR pmid IS NOT NULL
        OR pmcid IS NOT NULL OR isbn IS NOT NULL OR issn IS NOT NULL
        OR standard_number IS NOT NULL`
**Verdict:** `OK`

### [0371] A6/ON — source_value_extractions CHECK(claim_type IN ('numerical','range','qualitative','framework','absent'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (claim_type outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-718", "claim_type": "PROBE-INVALID-ENUM", "extraction_method": "skim", "created_at": "PROBE-719", "updated_at": "PROBE-720", "claimed_value": "PROBE-721"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: claim_type IN ('numerical','range','qualitative','framework','absent')`
**Verdict:** `OK`

### [0372] A6/ON — source_value_extractions CHECK(extraction_method IN ('skim','full-read','re-read','auto-mined'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (extraction_method outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-722", "claim_type": "numerical", "extraction_method": "PROBE-INVALID-ENUM", "created_at": "PROBE-723", "updated_at": "PROBE-724", "claimed_value": "PROBE-725"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: extraction_method IN ('skim','full-read','re-read','auto-mined')`
**Verdict:** `OK`

### [0373] A6/ON — source_value_extractions CHECK(extraction_status IN ('preliminary','reviewed','verified','contradicted','absent-confirmed'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (extraction_status outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "extraction_status") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-726", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-727", "updated_at": "PROBE-728", "claimed_value": "PROBE-729", "extraction_status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: extraction_status IN ('preliminary','reviewed','verified','contradicted','absent-confirmed')`
**Verdict:** `OK`

### [0374] A6/ON — source_value_extractions CHECK(root_type IN ( 'measurement_primary', 'participatory_finding', 'committee_assertion', 'derived_calculation', ')   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (root_type outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "root_type") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-730", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-731", "updated_at": "PROBE-732", "claimed_value": "PROBE-733", "root_type": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: root_type IN (
            'measurement_primary', 'participatory_finding',
            'committee_assertion', 'derived_calculation', 'untraced')`
**Verdict:** `OK`

### [0375] A6/ON — source_value_extractions CHECK(measurement_paradigm IN ( 'swept_path_dynamic', 'static_turning_circle', 'static_clearance', 'anthropometric_p)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (measurement_paradigm outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "measurement_paradigm") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-734", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-735", "updated_at": "PROBE-736", "claimed_value": "PROBE-737", "measurement_paradigm": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: measurement_paradigm IN (
            'swept_path_dynamic', 'static_turning_circle', 'static_clearance',
            'anthropometric_percentile', 'instrumented_physical_measurement',
            'route_metric', 'field_observation', 'participatory_spatial',
            'stated_unmeasured')`
**Verdict:** `OK`

### [0376] A6/ON — source_value_extractions CHECK(device_class IN ( 'manual_self_propelled', 'manual_attendant', 'power_chair', 'scooter', 'bariatric_manual', ')   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (device_class outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "device_class") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-738", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-739", "updated_at": "PROBE-740", "claimed_value": "PROBE-741", "device_class": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: device_class IN (
            'manual_self_propelled', 'manual_attendant', 'power_chair', 'scooter',
            'bariatric_manual', 'bariatric_power', 'walker_rollator',
            'mixed', 'not_device_scoped')`
**Verdict:** `OK`

### [0377] A6/ON — source_value_extractions CHECK(contested IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (contested outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "contested") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-742", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-743", "updated_at": "PROBE-744", "claimed_value": "PROBE-745", "contested": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: contested IN (0, 1)`
**Verdict:** `OK`

### [0378] A6/ON — source_value_extractions CHECK( (claim_type = 'absent' AND claimed_value IS NULL) OR (claim_type <> 'absent' AND claimed_value IS NOT NULL) )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (claim_type='absent' with claimed_value non-NULL; FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-746", "claim_type": "absent", "extraction_method": "skim", "created_at": "PROBE-747", "updated_at": "PROBE-748", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: (claim_type =  'absent' AND claimed_value IS NULL) OR
    (claim_type <> 'absent' AND claimed_value IS NOT NULL)`
**Verdict:** `OK`

### [0379] A6/ON — spec_value_probes CHECK(direction IN ('up','down'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (direction outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-749", "walk_id": "PROBE-750", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-751", "direction": "PROBE-INVALID-ENUM", "population": "PROBE-752", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-753", "created_at": "PROBE-754", "created_by_session": "PROBE-755"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: direction IN ('up','down')`
**Verdict:** `OK`

### [0380] A6/ON — spec_value_probes CHECK(claim_type IN ( 'minimum','maximum','target','range_low','range_high' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (claim_type outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-756", "walk_id": "PROBE-757", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-758", "direction": "up", "population": "PROBE-759", "claim_type": "PROBE-INVALID-ENUM", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-760", "created_at": "PROBE-761", "created_by_session": "PROBE-762"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: claim_type IN (
                            'minimum','maximum','target','range_low','range_high'
                        )`
**Verdict:** `OK`

### [0381] A6/ON — spec_value_probes CHECK(phase IN ( 'outer-pass-1st','outer-pass-2nd','outer-stop', 'refinement-pass-1st','refinement-pass-2nd','refine)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (phase outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-763", "walk_id": "PROBE-764", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-765", "direction": "up", "population": "PROBE-766", "claim_type": "minimum", "step_index": 1, "phase": "PROBE-INVALID-ENUM", "step_value": 1.0, "step_value_unit": "PROBE-767", "created_at": "PROBE-768", "created_by_session": "PROBE-769"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: phase IN (
                            'outer-pass-1st','outer-pass-2nd','outer-stop',
                            'refinement-pass-1st','refinement-pass-2nd','refinement-stop',
                            'final'
                        )`
**Verdict:** `OK`

### [0382] A6/ON — spec_value_probes CHECK(passes_strict IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (passes_strict outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session", "passes_strict") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-770", "walk_id": "PROBE-771", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-772", "direction": "up", "population": "PROBE-773", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-774", "created_at": "PROBE-775", "created_by_session": "PROBE-776", "passes_strict": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: passes_strict IN (0,1)`
**Verdict:** `OK`

### [0383] A6/ON — specification_source_links CHECK(role IN ('governing'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (role outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "specification_source_links" ("ref_id", "specification_id", "role") VALUES (?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "specification_id": 1, "role": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: role IN ('governing')`
**Verdict:** `OK`

### [0384] A6/ON — specifications CHECK(state IN ('stated', 'provisional', 'pending', 'not_applicable'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (state outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state") VALUES (?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: state IN ('stated', 'provisional',
                                                    'pending', 'not_applicable')`
**Verdict:** `OK`

### [0385] A6/ON — specifications CHECK(design_scale IN ('universal', 'population', 'person'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (design_scale outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "design_scale") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": "stated", "design_scale": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: design_scale IN ('universal', 'population', 'person')`
**Verdict:** `OK`

### [0386] A6/ON — specifications CHECK(governing_refs IS NULL OR json_valid(governing_refs))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (invalid JSON in governing_refs; FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "governing_refs") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": "stated", "governing_refs": "{not-json"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: governing_refs IS NULL OR json_valid(governing_refs)`
**Verdict:** `OK`

### [0387] A6/ON — specifications CHECK(code_floor_only IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (code_floor_only outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "code_floor_only") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": "stated", "code_floor_only": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: code_floor_only IN (0, 1)`
**Verdict:** `OK`

### [0388] A6/ON — specifications CHECK(has_unverified_sources IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (has_unverified_sources outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "has_unverified_sources") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": "stated", "has_unverified_sources": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: has_unverified_sources IN (0, 1)`
**Verdict:** `OK`

### [0389] A6/ON — specifications CHECK(all_sources_disqualified IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (all_sources_disqualified outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "all_sources_disqualified") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": "stated", "all_sources_disqualified": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: all_sources_disqualified IN (0, 1)`
**Verdict:** `OK`

### [0390] A6/ON — specifications CHECK(regulatory_stratum_only IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (regulatory_stratum_only outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "regulatory_stratum_only") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": "stated", "regulatory_stratum_only": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: regulatory_stratum_only IN (0, 1)`
**Verdict:** `OK`

### [0391] A6/ON — supersession_check CHECK(anchor_tier BETWEEN 1 AND 6)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (anchor_tier above range; FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-778", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-779", "ref_id": "PROBE-PK-167", "anchor_tier": 7, "anchor_evidence_type": "PROBE-780", "outcome": "current_best", "search_strategy_record": "PROBE-781", "checked_at": "PROBE-782", "checked_by_session": "PROBE-783", "check_method": "pubmed_search"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: anchor_tier BETWEEN 1 AND 6`
**Verdict:** `OK`

### [0392] A6/ON — supersession_check CHECK(outcome IN ( 'current_best', 'superseded_by', 'refined_by', 'divergent_no_supersession', 'co1_addition_logged')   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-784", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-785", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-786", "outcome": "PROBE-INVALID-ENUM", "search_strategy_record": "PROBE-787", "checked_at": "PROBE-788", "checked_by_session": "PROBE-789", "check_method": "pubmed_search"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: outcome IN (
        'current_best',
        'superseded_by',
        'refined_by',
        'divergent_no_supersession',
        'co1_addition_logged',
        'pending'  -- check started but not yet completed; should not appear on closed slug
    )`
**Verdict:** `OK`

### [0393] A6/ON — supersession_check CHECK(check_method IN ( 'pubmed_search', 'scholar_gateway', 'cochrane_direct', 'standards_body_direct', 'multilingua)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (check_method outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-790", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-791", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-792", "outcome": "current_best", "search_strategy_record": "PROBE-793", "checked_at": "PROBE-794", "checked_by_session": "PROBE-795", "check_method": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: check_method IN (
        'pubmed_search', 'scholar_gateway', 'cochrane_direct',
        'standards_body_direct', 'multilingual_research',
        'composite'
    )`
**Verdict:** `OK`

### [0394] A6/ON — supersession_check CHECK( (outcome IN ('superseded_by','refined_by','divergent_no_supersession') AND (superseding_ref_ids IS NOT NULL O)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-796", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-797", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-798", "outcome": "PROBE-INVALID-ENUM", "search_strategy_record": "PROBE-799", "checked_at": "PROBE-800", "checked_by_session": "PROBE-801", "check_method": "pubmed_search"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: outcome IN (
        'current_best',
        'superseded_by',
        'refined_by',
        'divergent_no_supersession',
        'co1_addition_logged',
        'pending'  -- check started but not yet completed; should not appear on closed slug
    )`
**Verdict:** `OK`

### [0395] A6/ON — supersession_check CHECK( outcome != 'refined_by' OR refinement_dimension IS NOT NULL )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome='refined_by' with refinement_dimension NULL; FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method", "refinement_dimension") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-802", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-803", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-804", "outcome": "refined_by", "search_strategy_record": "PROBE-805", "checked_at": "PROBE-806", "checked_by_session": "PROBE-807", "check_method": "pubmed_search", "refinement_dimension": null}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: -- superseded_by / refined_by / divergent_no_supersession require superseding refs
        (outcome IN ('superseded_by','refined_by','divergent_no_supersession')
         AND (superseding_ref_ids IS NOT NULL OR superseding_dois IS NOT NULL))
        OR
        outcome IN ('current_best','co1_addition_logged','pending')`
**Verdict:** `OK`

### [0396] A6/ON — supersession_check CHECK( outcome != 'divergent_no_supersession' OR divergence_notes IS NOT NULL )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome='divergent_no_supersession' with divergence_notes NULL; FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method", "divergence_notes") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-808", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-809", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-810", "outcome": "divergent_no_supersession", "search_strategy_record": "PROBE-811", "checked_at": "PROBE-812", "checked_by_session": "PROBE-813", "check_method": "pubmed_search", "divergence_notes": null}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: -- superseded_by / refined_by / divergent_no_supersession require superseding refs
        (outcome IN ('superseded_by','refined_by','divergent_no_supersession')
         AND (superseding_ref_ids IS NOT NULL OR superseding_dois IS NOT NULL))
        OR
        outcome IN ('current_best','co1_addition_logged','pending')`
**Verdict:** `OK`

### [0397] A6/ON — supersession_check CHECK( outcome != 'co1_addition_logged' OR anchor_evidence_type = 'co1' )   `2026-08-12 08:35:28Z`
**Action:** construct a violating row (FK=ON)
**Expected:** CHECK fires
**Actual:** no mechanical violation constructible for this expression (cross-column/complex predicate)
**Verdict:** `BLOCKED`

### [0398] A6/ON — term_aliases CHECK(alias_type IN ( 'SYNONYM','TRANSLATION','NARROWER', 'BROADER','DEPRECATED','DOMAIN' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (alias_type outside enum; FK=ON)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "alias": "PROBE-815", "language": "PROBE-816", "alias_type": "PROBE-INVALID-ENUM", "created_at": "PROBE-817", "created_by_session": "PROBE-818", "updated_at": "PROBE-819", "updated_by_session": "PROBE-820"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: alias_type IN (
                            'SYNONYM','TRANSLATION','NARROWER',
                            'BROADER','DEPRECATED','DOMAIN'
                        )`
**Verdict:** `OK`

### [0399] A6/ON — weighting_profile CHECK(json_valid(tier_weights))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (invalid JSON in tier_weights; FK=ON)
**SQL:**
```sql
INSERT INTO "weighting_profile" ("audience", "use_pattern", "tier_weights") VALUES (?, ?, ?)  -- {"audience": "PROBE-821", "use_pattern": "PROBE-822", "tier_weights": "{not-json"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: json_valid(tier_weights)`
**Verdict:** `OK`

### [0400] A6/OFF — access_duration CHECK(code IN ('permanent','temporary','situational'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (code outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "access_duration" ("code", "definition") VALUES (?, ?)  -- {"code": "PROBE-INVALID-ENUM", "definition": "PROBE-DEFINITION"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: code IN ('permanent','temporary','situational')`
**Verdict:** `OK`

### [0401] A6/OFF — access_need_axis_map CHECK(relationship IN ('primary','partial','spans'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (relationship outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "access_need_axis_map" ("need_code", "axis_code", "relationship") VALUES (?, ?, ?)  -- {"need_code": "A-AT", "axis_code": "AX-AMB", "relationship": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: relationship IN ('primary','partial','spans')`
**Verdict:** `OK`

### [0402] A6/OFF — access_need_icf CHECK(icf_type IN ('b','d','e','s'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (icf_type outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "access_need_icf" ("need_code", "icf_code", "icf_type", "confidence") VALUES (?, ?, ?, ?)  -- {"need_code": "A-AT", "icf_code": "PROBE-830", "icf_type": "PROBE-INVALID-ENUM", "confidence": "confirmed"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: icf_type IN ('b','d','e','s')`
**Verdict:** `OK`

### [0403] A6/OFF — access_need_icf CHECK(confidence IN ('confirmed','proposed'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (confidence outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "access_need_icf" ("need_code", "icf_code", "icf_type", "confidence") VALUES (?, ?, ?, ?)  -- {"need_code": "A-AT", "icf_code": "PROBE-831", "icf_type": "b", "confidence": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: confidence IN ('confirmed','proposed')`
**Verdict:** `OK`

### [0404] A6/OFF — access_needs CHECK(family IN ('perceiving','communicating','operating','pacing','environment_safety'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (family outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "access_needs" ("need_code", "family", "design_obligation") VALUES (?, ?, ?)  -- {"need_code": "PROBE-833", "family": "PROBE-INVALID-ENUM", "design_obligation": "PROBE-834"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: family IN
                    ('perceiving','communicating','operating','pacing','environment_safety')`
**Verdict:** `OK`

### [0405] A6/OFF — access_needs CHECK(typical_stakes IN ('safety-critical','exclusion','friction'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (typical_stakes outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "access_needs" ("need_code", "family", "design_obligation", "typical_stakes") VALUES (?, ?, ?, ?)  -- {"need_code": "PROBE-835", "family": "perceiving", "design_obligation": "PROBE-836", "typical_stakes": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: typical_stakes IN ('safety-critical','exclusion','friction')`
**Verdict:** `OK`

### [0406] A6/OFF — access_stakes CHECK(code IN ('safety-critical','exclusion','friction'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (code outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "access_stakes" ("code", "definition") VALUES (?, ?)  -- {"code": "PROBE-INVALID-ENUM", "definition": "PROBE-DEFINITION"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: code IN ('safety-critical','exclusion','friction')`
**Verdict:** `OK`

### [0407] A6/OFF — axes CHECK(coverage_status IN ('ESTABLISHED','PARTIAL','STUB'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (coverage_status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "axes" ("axis_code", "name", "mechanism", "coverage_status", "falsification_condition") VALUES (?, ?, ?, ?, ?)  -- {"axis_code": "PROBE-845", "name": "PROBE-846", "mechanism": "PROBE-847", "coverage_status": "PROBE-INVALID-ENUM", "falsification_condition": "PROBE-848"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: coverage_status IN ('ESTABLISHED','PARTIAL','STUB')`
**Verdict:** `OK`

### [0408] A6/OFF — bpc_metadata CHECK(pico_complete IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (pico_complete outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "pico_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-849", "created_at": "PROBE-850", "created_by_session": "PROBE-851", "updated_at": "PROBE-852", "updated_by_session": "PROBE-853", "pico_complete": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: pico_complete IN (0,1)`
**Verdict:** `OK`

### [0409] A6/OFF — bpc_metadata CHECK(search_complete IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (search_complete outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "search_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-854", "created_at": "PROBE-855", "created_by_session": "PROBE-856", "updated_at": "PROBE-857", "updated_by_session": "PROBE-858", "search_complete": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: search_complete IN (0,1)`
**Verdict:** `OK`

### [0410] A6/OFF — bpc_metadata CHECK(bpc_complete IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (bpc_complete outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "bpc_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-859", "created_at": "PROBE-860", "created_by_session": "PROBE-861", "updated_at": "PROBE-862", "updated_by_session": "PROBE-863", "bpc_complete": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: bpc_complete IN (0,1)`
**Verdict:** `OK`

### [0411] A6/OFF — bpc_metadata CHECK(citation_mining_complete IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (citation_mining_complete outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "citation_mining_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-864", "created_at": "PROBE-865", "created_by_session": "PROBE-866", "updated_at": "PROBE-867", "updated_by_session": "PROBE-868", "citation_mining_complete": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: citation_mining_complete IN (0,1)`
**Verdict:** `OK`

### [0412] A6/OFF — bpc_metadata CHECK(supersession_check_complete IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (supersession_check_complete outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "supersession_check_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-869", "created_at": "PROBE-870", "created_by_session": "PROBE-871", "updated_at": "PROBE-872", "updated_by_session": "PROBE-873", "supersession_check_complete": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: supersession_check_complete IN (0, 1)`
**Verdict:** `OK`

### [0413] A6/OFF — bpc_metadata CHECK(closure_definition_version IS NULL OR closure_definition_version IN ('v1', 'v2'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (closure_definition_version outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "closure_definition_version") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-874", "created_at": "PROBE-875", "created_by_session": "PROBE-876", "updated_at": "PROBE-877", "updated_by_session": "PROBE-878", "closure_definition_version": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: closure_definition_version IS NULL OR closure_definition_version IN ('v1', 'v2')`
**Verdict:** `OK`

### [0414] A6/OFF — case_studies CHECK(evidence_quality_tier IS NULL OR evidence_quality_tier BETWEEN 1 AND 3)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (evidence_quality_tier above range; FK=OFF)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session", "evidence_quality_tier") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-880", "slug": "PROBE-PK-267", "title": "PROBE-881", "building_type": "PROBE-882", "location": "PROBE-883", "created_at": "PROBE-884", "created_by_session": "PROBE-885", "evidence_quality_tier": 4}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: evidence_quality_tier IS NULL
                                        OR evidence_quality_tier BETWEEN 1 AND 3`
**Verdict:** `OK`

### [0415] A6/OFF — case_studies CHECK(cost_data_quality IS NULL OR cost_data_quality IN ('VERIFIED','PROVISIONAL','GREY'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (cost_data_quality outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session", "cost_data_quality") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-886", "slug": "PROBE-PK-267", "title": "PROBE-887", "building_type": "PROBE-888", "location": "PROBE-889", "created_at": "PROBE-890", "created_by_session": "PROBE-891", "cost_data_quality": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: cost_data_quality IS NULL OR cost_data_quality IN
                     ('VERIFIED','PROVISIONAL','GREY')`
**Verdict:** `OK`

### [0416] A6/OFF — case_studies CHECK(harm_finding IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (harm_finding outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session", "harm_finding") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-892", "slug": "PROBE-PK-267", "title": "PROBE-893", "building_type": "PROBE-894", "location": "PROBE-895", "created_at": "PROBE-896", "created_by_session": "PROBE-897", "harm_finding": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: harm_finding IN (0,1)`
**Verdict:** `OK`

### [0417] A6/OFF — case_study_outcomes CHECK(tier IS NULL OR tier BETWEEN 1 AND 3)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (tier above range; FK=OFF)
**SQL:**
```sql
INSERT INTO "case_study_outcomes" ("case_study_id", "metric", "tier") VALUES (?, ?, ?)  -- {"case_study_id": "PROBE-CASE_STUDY_ID", "metric": "PROBE-898", "tier": 4}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: tier IS NULL OR tier BETWEEN 1 AND 3`
**Verdict:** `OK`

### [0418] A6/OFF — citation_mining CHECK(backward IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (backward outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session", "backward") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "local_ref_id": "PROBE-899", "created_at": "PROBE-900", "created_by_session": "PROBE-901", "updated_at": "PROBE-902", "updated_by_session": "PROBE-903", "backward": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: backward IN (0,1)`
**Verdict:** `OK`

### [0419] A6/OFF — citation_mining CHECK(forward IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (forward outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session", "forward") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "local_ref_id": "PROBE-904", "created_at": "PROBE-905", "created_by_session": "PROBE-906", "updated_at": "PROBE-907", "updated_by_session": "PROBE-908", "forward": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: forward IN (0,1)`
**Verdict:** `OK`

### [0420] A6/OFF — conflicts CHECK(status IN ( 'RESOLVED-EVIDENCE', 'RESOLVED-CONSENSUS', 'RESOLUTION-PROPOSED', 'UNRESOLVED', 'MODE-S-ONLY' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-910", "domain": "PROBE-911", "pop_a": "PROBE-912", "pop_b": "PROBE-913", "status": "PROBE-INVALID-ENUM", "created_at": "PROBE-914", "created_by_session": "PROBE-915", "updated_at": "PROBE-916", "updated_by_session": "PROBE-917"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN (
                            'RESOLVED-EVIDENCE',
                            'RESOLVED-CONSENSUS',
                            'RESOLUTION-PROPOSED',
                            'UNRESOLVED',
                            'MODE-S-ONLY'
                        )`
**Verdict:** `OK`

### [0421] A6/OFF — connections CHECK(status IN ( 'PENDING','CONSUMED','CONSUMED-DEFERRED','CLOSED' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-919", "status": "PROBE-INVALID-ENUM", "confidence": "HIGH", "filed_in": "PROBE-920", "created_at": "PROBE-921", "created_by_session": "PROBE-922", "updated_at": "PROBE-923", "updated_by_session": "PROBE-924"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN (
                            'PENDING','CONSUMED','CONSUMED-DEFERRED','CLOSED'
                        )`
**Verdict:** `OK`

### [0422] A6/OFF — connections CHECK(confidence IN ('HIGH','MODERATE','SPECULATIVE'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (confidence outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-925", "status": "PENDING", "confidence": "PROBE-INVALID-ENUM", "filed_in": "PROBE-926", "created_at": "PROBE-927", "created_by_session": "PROBE-928", "updated_at": "PROBE-929", "updated_by_session": "PROBE-930"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: confidence IN ('HIGH','MODERATE','SPECULATIVE')`
**Verdict:** `OK`

### [0423] A6/OFF — connections CHECK(connection_type IN ( 'CROSS-POPULATION','CROSS-ITEM', 'COMPOUND-INTERACTION','METHODOLOGY' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (connection_type outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session", "connection_type") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-931", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-932", "created_at": "PROBE-933", "created_by_session": "PROBE-934", "updated_at": "PROBE-935", "updated_by_session": "PROBE-936", "connection_type": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: connection_type IN (
                            'CROSS-POPULATION','CROSS-ITEM',
                            'COMPOUND-INTERACTION','METHODOLOGY'
                        )`
**Verdict:** `OK`

### [0424] A6/OFF — connections CHECK(opus_reviewed IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (opus_reviewed outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session", "opus_reviewed") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-937", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-938", "created_at": "PROBE-939", "created_by_session": "PROBE-940", "updated_at": "PROBE-941", "updated_by_session": "PROBE-942", "opus_reviewed": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: opus_reviewed IN (0,1)`
**Verdict:** `OK`

### [0425] A6/OFF — convergence_assessment CHECK(status IN ('convergent', 'divergent', 'single_axis', 'pending_assessment'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "convergence_assessment" ("status") VALUES (?)  -- {"status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('convergent', 'divergent',
                                              'single_axis', 'pending_assessment')`
**Verdict:** `OK`

### [0426] A6/OFF — decisions CHECK(category IN ( 'D-DOCT','D-METH','D-SCHEMA','D-OP','D-PRES' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (category outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-944", "category": "PROBE-INVALID-ENUM", "delegation": "DG-NON", "summary": "PROBE-945", "outcome": "PROBE-946", "rationale": "PROBE-947", "decision_date": "PROBE-948", "decided_by": "PROBE-949", "model_routing": "PROBE-950", "effort_level": 1, "review_status": "PROBE-951", "created_at": "PROBE-952", "created_by_session": "PROBE-953", "updated_at": "PROBE-954", "updated_by_session": "PROBE-955"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: category IN (
                            'D-DOCT','D-METH','D-SCHEMA','D-OP','D-PRES'
                        )`
**Verdict:** `OK`

### [0427] A6/OFF — decisions CHECK(delegation IN ('DG-NON','DG-REVIEW','DG-AUTO'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (delegation outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-956", "category": "D-DOCT", "delegation": "PROBE-INVALID-ENUM", "summary": "PROBE-957", "outcome": "PROBE-958", "rationale": "PROBE-959", "decision_date": "PROBE-960", "decided_by": "PROBE-961", "model_routing": "PROBE-962", "effort_level": 1, "review_status": "PROBE-963", "created_at": "PROBE-964", "created_by_session": "PROBE-965", "updated_at": "PROBE-966", "updated_by_session": "PROBE-967"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: delegation IN ('DG-NON','DG-REVIEW','DG-AUTO')`
**Verdict:** `OK`

### [0428] A6/OFF — decisions CHECK(status IN ( 'ACTIVE','SUPERSEDED','WITHDRAWN','PROPOSED','PROVISIONAL' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-968", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-969", "outcome": "PROBE-970", "rationale": "PROBE-971", "decision_date": "PROBE-972", "decided_by": "PROBE-973", "model_routing": "PROBE-974", "effort_level": 1, "review_status": "PROBE-975", "created_at": "PROBE-976", "created_by_session": "PROBE-977", "updated_at": "PROBE-978", "updated_by_session": "PROBE-979", "status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN (
                            'ACTIVE','SUPERSEDED','WITHDRAWN','PROPOSED','PROVISIONAL'
                        )`
**Verdict:** `OK`

### [0429] A6/OFF — economics_entries CHECK(pillar IN ('health','inaction','construction','market'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (pillar outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-981", "pillar": "PROBE-INVALID-ENUM", "entry_type": "cost_premium", "source": "PROBE-982", "finding": "PROBE-983", "created_at": "PROBE-984", "created_by_session": "PROBE-985"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: pillar IN ('health','inaction','construction','market')`
**Verdict:** `OK`

### [0430] A6/OFF — economics_entries CHECK(entry_type IN ('cost_premium','retrofit_multiplier','grant_programme','health_outcome', 'market_value','housin)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (entry_type outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-986", "pillar": "health", "entry_type": "PROBE-INVALID-ENUM", "source": "PROBE-987", "finding": "PROBE-988", "created_at": "PROBE-989", "created_by_session": "PROBE-990"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: entry_type IN
                    ('cost_premium','retrofit_multiplier','grant_programme','health_outcome',
                     'market_value','housing_deficit','research_gap')`
**Verdict:** `OK`

### [0431] A6/OFF — economics_entries CHECK(evidence_tier IS NULL OR evidence_tier BETWEEN 1 AND 6)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (evidence_tier above range; FK=OFF)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session", "evidence_tier") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-991", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-992", "finding": "PROBE-993", "created_at": "PROBE-994", "created_by_session": "PROBE-995", "evidence_tier": 7}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: evidence_tier IS NULL OR evidence_tier BETWEEN 1 AND 6`
**Verdict:** `OK`

### [0432] A6/OFF — economics_entries CHECK(confidence IS NULL OR confidence IN ('HIGH','MODERATE','LOW'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (confidence outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session", "confidence") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-996", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-997", "finding": "PROBE-998", "created_at": "PROBE-999", "created_by_session": "PROBE-1000", "confidence": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: confidence IS NULL OR confidence IN ('HIGH','MODERATE','LOW')`
**Verdict:** `OK`

### [0433] A6/OFF — economics_entries CHECK(quant_status IS NULL OR quant_status IN ('VERIFIED-QUANT','UNVERIFIED-QUANT'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (quant_status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session", "quant_status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-1001", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-1002", "finding": "PROBE-1003", "created_at": "PROBE-1004", "created_by_session": "PROBE-1005", "quant_status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: quant_status IS NULL OR quant_status IN
                    ('VERIFIED-QUANT','UNVERIFIED-QUANT')`
**Verdict:** `OK`

### [0434] A6/OFF — evidence_population_match CHECK(match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (match_grade outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-1007", "source_ref": "PROBE-1008", "target_population": "PROBE-1009", "match_grade": "PROBE-INVALID-ENUM", "created_at": "PROBE-1010", "created_by_session": "PROBE-1011"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH')`
**Verdict:** `OK`

### [0435] A6/OFF — evidence_sources CHECK(scope IS NULL OR scope IN ( 'high_control', 'lower_control', 'national', 'international', 'intrinsic' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (scope outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "scope") VALUES (?, ?)  -- {"ref_id": "PROBE-1013", "scope": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: scope IS NULL OR scope IN (
    'high_control', 'lower_control', 'national', 'international', 'intrinsic'
  )`
**Verdict:** `OK`

### [0436] A6/OFF — evidence_sources CHECK(data_capture_status IN ('pending','captured','none-extractable','deferred'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (data_capture_status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "data_capture_status") VALUES (?, ?)  -- {"ref_id": "PROBE-1014", "data_capture_status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: data_capture_status IN ('pending','captured','none-extractable','deferred')`
**Verdict:** `OK`

### [0437] A6/OFF — evidence_sources CHECK(citation_mining_status IN ('pending','mined','deferred','not-applicable'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (citation_mining_status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "citation_mining_status") VALUES (?, ?)  -- {"ref_id": "PROBE-1015", "citation_mining_status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: citation_mining_status IN ('pending','mined','deferred','not-applicable')`
**Verdict:** `OK`

### [0438] A6/OFF — evidence_sources CHECK(processing_blocked_reason IS NULL OR processing_blocked_reason IN ( 'no-full-text', 'paywalled', 'no-doi', 'no)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (processing_blocked_reason outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "processing_blocked_reason") VALUES (?, ?)  -- {"ref_id": "PROBE-1016", "processing_blocked_reason": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: processing_blocked_reason IS NULL OR processing_blocked_reason IN (
    'no-full-text',        -- full text could not be obtained
    'paywalled',           -- access blocked by paywall
    'no-doi',              -- no resolvable identifier for automated paths
    'not-indexed',         -- absent from the indexes the pipeline queries
    'language',            -- awaiting in-language reading capacity
    'no-quantified-claims',-- read; carries no extractable value
    'superseded',          -- superseded by another source
    'out-of-scope',        -- outside the corpus this project extracts from
    'tier-not-required'    -- tier does not oblige the work
  )`
**Verdict:** `OK`

### [0439] A6/OFF — evidence_sources CHECK(verification_disposition IS NULL OR verification_disposition IN ('OPEN','CLOSED'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (verification_disposition outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "verification_disposition") VALUES (?, ?)  -- {"ref_id": "PROBE-1017", "verification_disposition": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: verification_disposition IS NULL
         OR verification_disposition IN ('OPEN','CLOSED')`
**Verdict:** `OK`

### [0440] A6/OFF — evidence_sources CHECK(verification_method IS NULL OR verification_method IN ( 'direct-render', 'co1-attestation', 'corroborated-not-)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (verification_method outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "verification_method") VALUES (?, ?)  -- {"ref_id": "PROBE-1018", "verification_method": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: verification_method IS NULL OR verification_method IN (
    'direct-render',              -- the document was fetched and read
    'co1-attestation',            -- the attestation itself was obtained (DR 3.1)
    'corroborated-not-retrieved', -- >=2 independent retrievals agree; doc not obtained
    'citing-bibliography',        -- existence attested only by another work's references
    'tool'                        -- resolve_dois / verify_urls; verified_by_tool names which
  )`
**Verdict:** `OK`

### [0441] A6/OFF — evidence_sources CHECK(verification_closure_reason IS NULL OR verification_closure_reason IN ( 'paywalled', 'print-only', 'access-den)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (verification_closure_reason outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "verification_closure_reason") VALUES (?, ?)  -- {"ref_id": "PROBE-1019", "verification_closure_reason": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: verification_closure_reason IS NULL OR verification_closure_reason IN (
    'paywalled',
    'print-only',
    'access-denied-persistent',
    'withdrawn',
    'not-found-after-search',
    'disputed-existence'          -- owner ruling: there may be no resolution
  )`
**Verdict:** `OK`

### [0442] A6/OFF — external_root_registry CHECK(root_type IN ( 'measurement_primary', 'participatory_finding', 'committee_assertion', 'derived_calculation', ')   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (root_type outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "external_root_registry" ("root_id", "description", "root_type") VALUES (?, ?, ?)  -- {"root_id": "PROBE-1021", "description": "PROBE-1022", "root_type": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: root_type IN (
                              'measurement_primary', 'participatory_finding',
                              'committee_assertion', 'derived_calculation',
                              'untraced')`
**Verdict:** `OK`

### [0443] A6/OFF — gap_mining CHECK(outcome IN ( 'closure_evidence_found', 'partial_evidence_found', 'null_result', 'gap_recategorized', 'deferred)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-1023", "attempt_at": "PROBE-1024", "attempted_by_session": "PROBE-1025", "search_strategy_record": "PROBE-1026", "outcome": "PROBE-INVALID-ENUM", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-1027"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: outcome IN (
        'closure_evidence_found',  -- enough to close the gap (rule #7 must fire)
        'partial_evidence_found',  -- some discoveries; gap stays OPEN with annotation
        'null_result',             -- searches ran clean, no relevant discoveries
        'gap_recategorized',       -- gap not mining-addressable after all
        'deferred'                 -- connectors unavailable / other blocker
    )`
**Verdict:** `OK`

### [0444] A6/OFF — gap_mining CHECK(check_method IN ( 'pubmed_cluster', 'scholar_gateway_lived_experience', 'cochrane_direct', 'standards_body_dir)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (check_method outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-1023", "attempt_at": "PROBE-1028", "attempted_by_session": "PROBE-1029", "search_strategy_record": "PROBE-1030", "outcome": "closure_evidence_found", "check_method": "PROBE-INVALID-ENUM", "discoveries_logged": "PROBE-1031"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: check_method IN (
        'pubmed_cluster',
        'scholar_gateway_lived_experience',
        'cochrane_direct',
        'standards_body_direct',
        'multilingual_research',
        'composite'
    )`
**Verdict:** `OK`

### [0445] A6/OFF — gap_mining CHECK( outcome != 'closure_evidence_found' OR (discoveries_logged IS NOT NULL AND discoveries_logged != '[]') )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome='closure_evidence_found' with discoveries_logged NULL; FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-1023", "attempt_at": "PROBE-1032", "attempted_by_session": "PROBE-1033", "search_strategy_record": "PROBE-1034", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": null}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: outcome != 'closure_evidence_found'
        OR (discoveries_logged IS NOT NULL AND discoveries_logged != '[]')`
**Verdict:** `OK`

### [0446] A6/OFF — gap_mining CHECK( outcome != 'gap_recategorized' OR (notes IS NOT NULL AND length(notes) >= 20) )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome='gap_recategorized' with notes NULL; FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged", "notes") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-1023", "attempt_at": "PROBE-1035", "attempted_by_session": "PROBE-1036", "search_strategy_record": "PROBE-1037", "outcome": "gap_recategorized", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-1038", "notes": null}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: outcome != 'gap_recategorized'
        OR (notes IS NOT NULL AND length(notes) >= 20)`
**Verdict:** `OK`

### [0447] A6/OFF — gap_mining CHECK( outcome != 'deferred' OR (notes IS NOT NULL AND length(notes) >= 10) )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome='deferred' with notes NULL; FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged", "notes") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-1023", "attempt_at": "PROBE-1039", "attempted_by_session": "PROBE-1040", "search_strategy_record": "PROBE-1041", "outcome": "deferred", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-1042", "notes": null}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: outcome != 'deferred'
        OR (notes IS NOT NULL AND length(notes) >= 10)`
**Verdict:** `OK`

### [0448] A6/OFF — gaps CHECK(category IN ( 'RP','SW','CR','ST','MX','CD','EC','EG', 'CI','DEC','CONF','AUDT' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (category outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-1044", "category": "PROBE-INVALID-ENUM", "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-1045", "created_at": "PROBE-1046", "created_by_session": "PROBE-1047", "updated_at": "PROBE-1048", "updated_by_session": "PROBE-1049"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: category IN (
                            'RP','SW','CR','ST','MX','CD','EC','EG',
                            'CI','DEC','CONF','AUDT'
                        )`
**Verdict:** `OK`

### [0449] A6/OFF — gaps CHECK(priority IN ('P1','P2','P3'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (priority outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-1050", "category": "RP", "priority": "PROBE-INVALID-ENUM", "status": "OPEN-PROBE", "description": "PROBE-1051", "created_at": "PROBE-1052", "created_by_session": "PROBE-1053", "updated_at": "PROBE-1054", "updated_by_session": "PROBE-1055"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: priority IN ('P1','P2','P3')`
**Verdict:** `OK`

### [0450] A6/OFF — gaps CHECK(status LIKE 'OPEN%' OR status LIKE 'CLOSED%')   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status fails LIKE; FK=OFF)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-1056", "category": "RP", "priority": "P1", "status": "PROBE-NOLIKE", "description": "PROBE-1057", "created_at": "PROBE-1058", "created_by_session": "PROBE-1059", "updated_at": "PROBE-1060", "updated_by_session": "PROBE-1061"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status LIKE 'OPEN%' OR status LIKE 'CLOSED%'`
**Verdict:** `OK`

### [0451] A6/OFF — gaps CHECK(mining_addressability IS NULL OR mining_addressability IN ( 'ADDRESSABLE', 'NOT-ADDRESSABLE', 'TRIAGE-NEEDED' )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (mining_addressability outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session", "mining_addressability") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-1062", "category": "RP", "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-1063", "created_at": "PROBE-1064", "created_by_session": "PROBE-1065", "updated_at": "PROBE-1066", "updated_by_session": "PROBE-1067", "mining_addressability": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: mining_addressability IS NULL OR mining_addressability IN (
        'ADDRESSABLE',
        'NOT-ADDRESSABLE',
        'TRIAGE-NEEDED'
    )`
**Verdict:** `OK`

### [0452] A6/OFF — item_audit_runs CHECK(status IN ('IN-PROGRESS','COMPLETE','HANDED-OFF'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-1069", "item_code": "A-01", "session": "PROBE-1070", "created_at": "PROBE-1071", "created_by_session": "PROBE-1072", "updated_at": "PROBE-1073", "updated_by_session": "PROBE-1074", "status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('IN-PROGRESS','COMPLETE','HANDED-OFF')`
**Verdict:** `OK`

### [0453] A6/OFF — item_axis_links CHECK(strength_band IN ('full','partial','weak'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (strength_band outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "item_axis_links" ("item_code", "axis_code", "strength_band") VALUES (?, ?, ?)  -- {"item_code": "A-01", "axis_code": "AX-AMB", "strength_band": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: strength_band IN ('full','partial','weak')`
**Verdict:** `OK`

### [0454] A6/OFF — item_axis_links CHECK(use_mode IN ('independent','assisted','collective') OR use_mode IS NULL)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (use_mode outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "item_axis_links" ("item_code", "axis_code", "use_mode") VALUES (?, ?, ?)  -- {"item_code": "A-01", "axis_code": "AX-AMB", "use_mode": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: use_mode IN ('independent','assisted','collective') OR use_mode IS NULL`
**Verdict:** `OK`

### [0455] A6/OFF — item_bpc_links CHECK(link_type IN ( 'primary','parameter','context','secondary' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (link_type outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "item_bpc_links" ("item_code", "slug", "link_type", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?)  -- {"item_code": "I-04", "slug": "PROBE-PK-267", "link_type": "PROBE-INVALID-ENUM", "created_at": "PROBE-1075", "created_by_session": "PROBE-1076"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: link_type IN (
        'primary','parameter','context','secondary'
    )`
**Verdict:** `OK`

### [0456] A6/OFF — item_population_links CHECK(applicability IN ( 'applies', 'applies_strictly', 'applies_loosely', 'context_dependent', 'does_not_apply' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (applicability outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "item_population_links" ("item_code", "population_code", "subtype", "applicability") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "subtype": "PROBE-1078", "applicability": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: applicability IN (
                        'applies', 'applies_strictly', 'applies_loosely',
                        'context_dependent', 'does_not_apply'
                      )`
**Verdict:** `OK`

### [0457] A6/OFF — items CHECK(category IN ( 'A','B','C','D','E','F','G','H','I','J','K' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (category outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-1080", "category": "PROBE-INVALID-ENUM", "name": "PROBE-1081", "created_at": "PROBE-1082", "created_by_session": "PROBE-1083", "updated_at": "PROBE-1084", "updated_by_session": "PROBE-1085"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: category IN (
                            'A','B','C','D','E','F','G','H','I','J','K'
                        )`
**Verdict:** `OK`

### [0458] A6/OFF — items CHECK(status IN ('draft','active','merged','retired'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-1086", "category": "A", "name": "PROBE-1087", "created_at": "PROBE-1088", "created_by_session": "PROBE-1089", "updated_at": "PROBE-1090", "updated_by_session": "PROBE-1091", "status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('draft','active','merged','retired')`
**Verdict:** `OK`

### [0459] A6/OFF — jurisdictional_values CHECK(is_code_minimum IS NULL OR is_code_minimum IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (is_code_minimum outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "jurisdictional_values" ("item_code", "jurisdiction", "is_code_minimum") VALUES (?, ?, ?)  -- {"item_code": "A-01", "jurisdiction": "PROBE-1092", "is_code_minimum": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: is_code_minimum IS NULL OR is_code_minimum IN (0, 1)`
**Verdict:** `OK`

### [0460] A6/OFF — lang_jur_map CHECK(role IN ('PRIMARY', 'SECONDARY'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (role outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "lang_jur_map" ("language", "jurisdiction", "role") VALUES (?, ?, ?)  -- {"language": "PROBE-1093", "jurisdiction": "PROBE-1094", "role": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: role IN ('PRIMARY', 'SECONDARY')`
**Verdict:** `OK`

### [0461] A6/OFF — life_stage_modifiers CHECK(code IN ('SEN','CHD'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (code outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "life_stage_modifiers" ("code", "label", "definition") VALUES (?, ?, ?)  -- {"code": "PROBE-INVALID-ENUM", "label": "PROBE-LABEL", "definition": "PROBE-DEFINITION"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: code IN ('SEN','CHD')`
**Verdict:** `OK`

### [0462] A6/OFF — population_axis_map CHECK(role IN ('ALIAS','PRIMARY','SECONDARY','SITUATIONAL'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (role outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "population_axis_map" ("population_code", "axis_code", "role") VALUES (?, ?, ?)  -- {"population_code": "ADHD", "axis_code": "AX-AMB", "role": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: role IN ('ALIAS','PRIMARY','SECONDARY','SITUATIONAL')`
**Verdict:** `OK`

### [0463] A6/OFF — population_reclass CHECK(row_kind IN ('EXISTING-POP','NEW-PROFILE'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (row_kind outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale") VALUES (?, ?, ?, ?)  -- {"population_code": "PROBE-1103", "row_kind": "PROBE-INVALID-ENUM", "layer": "AXIS-ALIAS", "rationale": "PROBE-1104"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: row_kind IN ('EXISTING-POP','NEW-PROFILE')`
**Verdict:** `OK`

### [0464] A6/OFF — population_reclass CHECK(layer IN ('AXIS-ALIAS','PROFILE','QUALIFIER','SPLIT'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (layer outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale") VALUES (?, ?, ?, ?)  -- {"population_code": "PROBE-1105", "row_kind": "EXISTING-POP", "layer": "PROBE-INVALID-ENUM", "rationale": "PROBE-1106"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: layer IN ('AXIS-ALIAS','PROFILE','QUALIFIER','SPLIT')`
**Verdict:** `OK`

### [0465] A6/OFF — population_reclass CHECK(profile_kind IN ('diagnostic','identity-cultural','demographic','anthropometric','compound','umbrella'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (profile_kind outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale", "profile_kind") VALUES (?, ?, ?, ?, ?)  -- {"population_code": "PROBE-1107", "row_kind": "EXISTING-POP", "layer": "AXIS-ALIAS", "rationale": "PROBE-1108", "profile_kind": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: profile_kind IN
                     ('diagnostic','identity-cultural','demographic','anthropometric','compound','umbrella')`
**Verdict:** `OK`

### [0466] A6/OFF — population_reclass CHECK(mapping_confidence IN ('high','moderate','low','minimal','TO-ASSESS') OR mapping_confidence IS NULL)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (mapping_confidence outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale", "mapping_confidence") VALUES (?, ?, ?, ?, ?)  -- {"population_code": "PROBE-1109", "row_kind": "EXISTING-POP", "layer": "AXIS-ALIAS", "rationale": "PROBE-1110", "mapping_confidence": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: mapping_confidence IN
                     ('high','moderate','low','minimal','TO-ASSESS') OR mapping_confidence IS NULL`
**Verdict:** `OK`

### [0467] A6/OFF — population_reclass CHECK(fluctuating IN ('yes','no') OR fluctuating IS NULL)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (fluctuating outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale", "fluctuating") VALUES (?, ?, ?, ?, ?)  -- {"population_code": "PROBE-1111", "row_kind": "EXISTING-POP", "layer": "AXIS-ALIAS", "rationale": "PROBE-1112", "fluctuating": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: fluctuating IN ('yes','no') OR fluctuating IS NULL`
**Verdict:** `OK`

### [0468] A6/OFF — populations CHECK(category IN ( 'mobility', 'sensory', 'cognitive', 'mental_health', 'pain_fatigue', 'neurological', 'developmen)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (category outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "populations" ("population_code", "display_name", "category") VALUES (?, ?, ?)  -- {"population_code": "PROBE-1114", "display_name": "PROBE-1115", "category": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: category IN (
                        'mobility', 'sensory', 'cognitive', 'mental_health',
                        'pain_fatigue', 'neurological', 'developmental',
                        'general'
                      )`
**Verdict:** `OK`

### [0469] A6/OFF — populations CHECK(is_compound IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (is_compound outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "populations" ("population_code", "display_name", "is_compound") VALUES (?, ?, ?)  -- {"population_code": "PROBE-1116", "display_name": "PROBE-1117", "is_compound": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: is_compound IN (0,1)`
**Verdict:** `OK`

### [0470] A6/OFF — populations CHECK(status IN ('active', 'deprecated'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "populations" ("population_code", "display_name", "status") VALUES (?, ?, ?)  -- {"population_code": "PROBE-1118", "display_name": "PROBE-1119", "status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('active', 'deprecated')`
**Verdict:** `OK`

### [0471] A6/OFF — reasoning_doc_citations CHECK(claim_type IN ( 'numerical_spec','jurisdiction_value','qualitative','definitional' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (claim_type outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-1121", "reasoning_doc_slug": "PROBE-PK-267", "parameter": "PROBE-1122", "claim_type": "PROBE-INVALID-ENUM", "source_ref_id": "PROBE-PK-1012", "verified_at": "PROBE-1123", "verified_by_session": "PROBE-1124", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-1125", "claim_text": "PROBE-1126"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: claim_type IN (
        'numerical_spec','jurisdiction_value','qualitative','definitional'
    )`
**Verdict:** `OK`

### [0472] A6/OFF — reasoning_doc_citations CHECK(value_match IN ( 'EXACT','WITHIN-TOLERANCE','DIFFERENT','NOT-FOUND','PAYWALL','SUPERSEDED' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (value_match outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-1127", "reasoning_doc_slug": "PROBE-PK-267", "parameter": "PROBE-1128", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-1012", "verified_at": "PROBE-1129", "verified_by_session": "PROBE-1130", "value_match": "PROBE-INVALID-ENUM", "claim_match": "SUPPORTED", "claimed_value": "PROBE-1131", "claim_text": "PROBE-1132"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: value_match IN (
        'EXACT','WITHIN-TOLERANCE','DIFFERENT','NOT-FOUND','PAYWALL','SUPERSEDED'
    )`
**Verdict:** `OK`

### [0473] A6/OFF — reasoning_doc_citations CHECK(claim_match IN ( 'SUPPORTED','PARTIAL','NOT-FOUND','PAYWALL','CONTRADICTED' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (claim_match outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-1133", "reasoning_doc_slug": "PROBE-PK-267", "parameter": "PROBE-1134", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-1012", "verified_at": "PROBE-1135", "verified_by_session": "PROBE-1136", "value_match": "EXACT", "claim_match": "PROBE-INVALID-ENUM", "claimed_value": "PROBE-1137", "claim_text": "PROBE-1138"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: claim_match IN (
        'SUPPORTED','PARTIAL','NOT-FOUND','PAYWALL','CONTRADICTED'
    )`
**Verdict:** `OK`

### [0474] A6/OFF — reasoning_doc_citations CHECK(paywall_purchase_candidate IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (paywall_purchase_candidate outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text", "paywall_purchase_candidate") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-1139", "reasoning_doc_slug": "PROBE-PK-267", "parameter": "PROBE-1140", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-1012", "verified_at": "PROBE-1141", "verified_by_session": "PROBE-1142", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-1143", "claim_text": "PROBE-1144", "paywall_purchase_candidate": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: paywall_purchase_candidate IN (0,1)`
**Verdict:** `OK`

### [0475] A6/OFF — reasoning_doc_citations CHECK( (claim_type IN ('numerical_spec','jurisdiction_value') AND claimed_value IS NOT NULL AND value_match IS NOT N)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (claim_type outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-1145", "reasoning_doc_slug": "PROBE-PK-267", "parameter": "PROBE-1146", "claim_type": "PROBE-INVALID-ENUM", "source_ref_id": "PROBE-PK-1012", "verified_at": "PROBE-1147", "verified_by_session": "PROBE-1148", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-1149", "claim_text": "PROBE-1150"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: claim_type IN (
        'numerical_spec','jurisdiction_value','qualitative','definitional'
    )`
**Verdict:** `OK`

### [0476] A6/OFF — room_items CHECK(applicability IN ('applies','conditional','not-applicable'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (applicability outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "room_items" ("room_code", "item_code", "applicability") VALUES (?, ?, ?)  -- {"room_code": "R-ASM", "item_code": "A-01", "applicability": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: applicability IN ('applies','conditional','not-applicable')`
**Verdict:** `OK`

### [0477] A6/OFF — rooms CHECK(status IN ('active','draft','retired'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "rooms" ("room_code", "name", "status") VALUES (?, ?, ?)  -- {"room_code": "PROBE-1152", "name": "PROBE-1153", "status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('active','draft','retired')`
**Verdict:** `OK`

### [0478] A6/OFF — search_candidates CHECK(disposition IN ('REHOME','MISCELLANEOUS','PENDING-VERIFICATION','OUT-OF-SCOPE','ADMITTED'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (disposition outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": "PROBE-PK-267", "disposition": "PROBE-INVALID-ENUM", "title": "PROBE-1154", "session": "PROBE-1155", "created_at": "PROBE-1156"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: disposition IN
                     ('REHOME','MISCELLANEOUS','PENDING-VERIFICATION','OUT-OF-SCOPE','ADMITTED')`
**Verdict:** `OK`

### [0479] A6/OFF — search_candidates CHECK(locator_status IS NULL OR locator_status IN ('UNVERIFIED','RESOLVED','DEAD'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (locator_status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at", "locator_status") VALUES (?, ?, ?, ?, ?, ?)  -- {"found_under_slug": "PROBE-PK-267", "disposition": "REHOME", "title": "PROBE-1157", "session": "PROBE-1158", "created_at": "PROBE-1159", "locator_status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: locator_status IS NULL OR locator_status IN
                     ('UNVERIFIED','RESOLVED','DEAD')`
**Verdict:** `OK`

### [0480] A6/OFF — search_candidates CHECK(tier_guess IS NULL OR tier_guess BETWEEN 1 AND 6)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (tier_guess above range; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at", "tier_guess") VALUES (?, ?, ?, ?, ?, ?)  -- {"found_under_slug": "PROBE-PK-267", "disposition": "REHOME", "title": "PROBE-1160", "session": "PROBE-1161", "created_at": "PROBE-1162", "tier_guess": 7}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: tier_guess IS NULL OR tier_guess BETWEEN 1 AND 6`
**Verdict:** `OK`

### [0481] A6/OFF — search_candidates CHECK(harm_finding IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (harm_finding outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at", "harm_finding") VALUES (?, ?, ?, ?, ?, ?)  -- {"found_under_slug": "PROBE-PK-267", "disposition": "REHOME", "title": "PROBE-1163", "session": "PROBE-1164", "created_at": "PROBE-1165", "harm_finding": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: harm_finding IN (0,1)`
**Verdict:** `OK`

### [0482] A6/OFF — search_coverage CHECK(status IN ('SEARCHED','THIN','NO-DATA','NOT-RUN'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "jurisdiction": "PROBE-1166", "status": "PROBE-INVALID-ENUM", "created_at": "PROBE-1167", "created_by_session": "PROBE-1168", "updated_at": "PROBE-1169", "updated_by_session": "PROBE-1170"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('SEARCHED','THIN','NO-DATA','NOT-RUN')`
**Verdict:** `OK`

### [0483] A6/OFF — search_coverage CHECK(co1_attempted IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (co1_attempted outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "co1_attempted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "jurisdiction": "PROBE-1171", "status": "SEARCHED", "created_at": "PROBE-1172", "created_by_session": "PROBE-1173", "updated_at": "PROBE-1174", "updated_by_session": "PROBE-1175", "co1_attempted": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: co1_attempted IN (0,1)`
**Verdict:** `OK`

### [0484] A6/OFF — search_coverage CHECK(tier5_attempted IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (tier5_attempted outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "tier5_attempted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "jurisdiction": "PROBE-1176", "status": "SEARCHED", "created_at": "PROBE-1177", "created_by_session": "PROBE-1178", "updated_at": "PROBE-1179", "updated_by_session": "PROBE-1180", "tier5_attempted": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: tier5_attempted IN (0,1)`
**Verdict:** `OK`

### [0485] A6/OFF — search_coverage CHECK(tier6_attempted IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (tier6_attempted outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "tier6_attempted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "jurisdiction": "PROBE-1181", "status": "SEARCHED", "created_at": "PROBE-1182", "created_by_session": "PROBE-1183", "updated_at": "PROBE-1184", "updated_by_session": "PROBE-1185", "tier6_attempted": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: tier6_attempted IN (0,1)`
**Verdict:** `OK`

### [0486] A6/OFF — search_executions CHECK(target_tier IS NULL OR target_tier BETWEEN 1 AND 6)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (target_tier above range; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "target_tier") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-1186", "query_text": "PROBE-1187", "engine": "PROBE-1188", "depth_method": "scoping", "session": "PROBE-1189", "executed_at": "PROBE-1190", "target_tier": 7}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: target_tier IS NULL OR target_tier BETWEEN 1 AND 6`
**Verdict:** `OK`

### [0487] A6/OFF — search_executions CHECK(target_evidence_type IS NULL OR target_evidence_type IN ('clinical','sr_meta','standard_eb','national_fw','cod)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (target_evidence_type outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "target_evidence_type") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-1191", "query_text": "PROBE-1192", "engine": "PROBE-1193", "depth_method": "scoping", "session": "PROBE-1194", "executed_at": "PROBE-1195", "target_evidence_type": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: target_evidence_type IS NULL OR target_evidence_type IN
     ('clinical','sr_meta','standard_eb','national_fw','code','co1','co2','grey')`
**Verdict:** `OK`

### [0488] A6/OFF — search_executions CHECK(target_scope IS NULL OR target_scope IN ('intrinsic','lower_control','high_control','national','international')   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (target_scope outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "target_scope") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-1196", "query_text": "PROBE-1197", "engine": "PROBE-1198", "depth_method": "scoping", "session": "PROBE-1199", "executed_at": "PROBE-1200", "target_scope": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: target_scope IS NULL OR target_scope IN
     ('intrinsic','lower_control','high_control','national','international')`
**Verdict:** `OK`

### [0489] A6/OFF — search_executions CHECK(depth_method IN ('scoping','systematic'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (depth_method outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-1201", "query_text": "PROBE-1202", "engine": "PROBE-1203", "depth_method": "PROBE-INVALID-ENUM", "session": "PROBE-1204", "executed_at": "PROBE-1205"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: depth_method IN ('scoping','systematic')`
**Verdict:** `OK`

### [0490] A6/OFF — search_executions CHECK(mining_direction IS NULL OR mining_direction IN ('none','backward','forward','both'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (mining_direction outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "mining_direction") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-1206", "query_text": "PROBE-1207", "engine": "PROBE-1208", "depth_method": "scoping", "session": "PROBE-1209", "executed_at": "PROBE-1210", "mining_direction": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: mining_direction IS NULL OR mining_direction IN
     ('none','backward','forward','both')`
**Verdict:** `OK`

### [0491] A6/OFF — search_executions CHECK(saturation_signal IS NULL OR saturation_signal IN ('none','partial','saturated'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (saturation_signal outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "saturation_signal") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-1211", "query_text": "PROBE-1212", "engine": "PROBE-1213", "depth_method": "scoping", "session": "PROBE-1214", "executed_at": "PROBE-1215", "saturation_signal": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: saturation_signal IS NULL OR saturation_signal IN
     ('none','partial','saturated')`
**Verdict:** `OK`

### [0492] A6/OFF — search_executions CHECK(backfill IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (backfill outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "backfill") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-1216", "query_text": "PROBE-1217", "engine": "PROBE-1218", "depth_method": "scoping", "session": "PROBE-1219", "executed_at": "PROBE-1220", "backfill": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: backfill IN (0,1)`
**Verdict:** `OK`

### [0493] A6/OFF — search_executions CHECK(terms_used IS NULL OR json_valid(terms_used))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (invalid JSON in terms_used; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "terms_used") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-1221", "query_text": "PROBE-1222", "engine": "PROBE-1223", "depth_method": "scoping", "session": "PROBE-1224", "executed_at": "PROBE-1225", "terms_used": "{not-json"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: terms_used IS NULL OR json_valid(terms_used)`
**Verdict:** `OK`

### [0494] A6/OFF — search_executions CHECK(admitted_ref_ids IS NULL OR json_valid(admitted_ref_ids))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (invalid JSON in admitted_ref_ids; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "admitted_ref_ids") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-1226", "query_text": "PROBE-1227", "engine": "PROBE-1228", "depth_method": "scoping", "session": "PROBE-1229", "executed_at": "PROBE-1230", "admitted_ref_ids": "{not-json"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: admitted_ref_ids IS NULL OR json_valid(admitted_ref_ids)`
**Verdict:** `OK`

### [0495] A6/OFF — search_languages CHECK(status IN ('SEARCHED','PARTIAL','NOT-RUN'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-1231", "status": "PROBE-INVALID-ENUM", "created_at": "PROBE-1232", "created_by_session": "PROBE-1233", "updated_at": "PROBE-1234", "updated_by_session": "PROBE-1235"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN ('SEARCHED','PARTIAL','NOT-RUN')`
**Verdict:** `OK`

### [0496] A6/OFF — situations CHECK(operational_access IN ('yes','no') OR operational_access IS NULL)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (operational_access outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "situations" ("situation_id", "title", "account_language", "account_text_ref", "operational_access") VALUES (?, ?, ?, ?, ?)  -- {"situation_id": "PROBE-1237", "title": "PROBE-1238", "account_language": "PROBE-1239", "account_text_ref": "PROBE-1240", "operational_access": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: operational_access IN ('yes','no') OR operational_access IS NULL`
**Verdict:** `OK`

### [0497] A6/OFF — slugs CHECK(status IN ( 'ACTIVE','MERGED','STUB','PROVISIONAL' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-1242", "topic_directory": "PROBE-1243", "sl_path": "PROBE-1244", "bpc_path": "PROBE-1245", "status": "PROBE-INVALID-ENUM", "created_at": "PROBE-1246", "created_by_session": "PROBE-1247", "updated_at": "PROBE-1248", "updated_by_session": "PROBE-1249"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: status IN (
                            'ACTIVE','MERGED','STUB','PROVISIONAL'
                        )`
**Verdict:** `OK`

### [0498] A6/OFF — source_locators CHECK(doi IS NOT NULL OR url IS NOT NULL OR pmid IS NOT NULL OR pmcid IS NOT NULL OR isbn IS NOT NULL OR issn IS NOT)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (all of ['doi', 'url', 'pmid', 'pmcid', 'isbn', 'issn', 'standard_number'] NULL; FK=OFF)
**SQL:**
```sql
INSERT INTO "source_locators" ("ref_id", "pmcid", "pmid", "url", "standard_number", "doi", "isbn", "issn") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-1251", "pmcid": null, "pmid": null, "url": null, "standard_number": null, "doi": null, "isbn": null, "issn": null}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: doi IS NOT NULL OR url IS NOT NULL OR pmid IS NOT NULL
        OR pmcid IS NOT NULL OR isbn IS NOT NULL OR issn IS NOT NULL
        OR standard_number IS NOT NULL`
**Verdict:** `OK`

### [0499] A6/OFF — source_value_extractions CHECK(claim_type IN ('numerical','range','qualitative','framework','absent'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (claim_type outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-1252", "claim_type": "PROBE-INVALID-ENUM", "extraction_method": "skim", "created_at": "PROBE-1253", "updated_at": "PROBE-1254", "claimed_value": "PROBE-1255"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: claim_type IN ('numerical','range','qualitative','framework','absent')`
**Verdict:** `OK`

### [0500] A6/OFF — source_value_extractions CHECK(extraction_method IN ('skim','full-read','re-read','auto-mined'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (extraction_method outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-1256", "claim_type": "numerical", "extraction_method": "PROBE-INVALID-ENUM", "created_at": "PROBE-1257", "updated_at": "PROBE-1258", "claimed_value": "PROBE-1259"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: extraction_method IN ('skim','full-read','re-read','auto-mined')`
**Verdict:** `OK`

### [0501] A6/OFF — source_value_extractions CHECK(extraction_status IN ('preliminary','reviewed','verified','contradicted','absent-confirmed'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (extraction_status outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "extraction_status") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-1260", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-1261", "updated_at": "PROBE-1262", "claimed_value": "PROBE-1263", "extraction_status": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: extraction_status IN ('preliminary','reviewed','verified','contradicted','absent-confirmed')`
**Verdict:** `OK`

### [0502] A6/OFF — source_value_extractions CHECK(root_type IN ( 'measurement_primary', 'participatory_finding', 'committee_assertion', 'derived_calculation', ')   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (root_type outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "root_type") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-1264", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-1265", "updated_at": "PROBE-1266", "claimed_value": "PROBE-1267", "root_type": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: root_type IN (
            'measurement_primary', 'participatory_finding',
            'committee_assertion', 'derived_calculation', 'untraced')`
**Verdict:** `OK`

### [0503] A6/OFF — source_value_extractions CHECK(measurement_paradigm IN ( 'swept_path_dynamic', 'static_turning_circle', 'static_clearance', 'anthropometric_p)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (measurement_paradigm outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "measurement_paradigm") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-1268", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-1269", "updated_at": "PROBE-1270", "claimed_value": "PROBE-1271", "measurement_paradigm": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: measurement_paradigm IN (
            'swept_path_dynamic', 'static_turning_circle', 'static_clearance',
            'anthropometric_percentile', 'instrumented_physical_measurement',
            'route_metric', 'field_observation', 'participatory_spatial',
            'stated_unmeasured')`
**Verdict:** `OK`

### [0504] A6/OFF — source_value_extractions CHECK(device_class IN ( 'manual_self_propelled', 'manual_attendant', 'power_chair', 'scooter', 'bariatric_manual', ')   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (device_class outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "device_class") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-1272", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-1273", "updated_at": "PROBE-1274", "claimed_value": "PROBE-1275", "device_class": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: device_class IN (
            'manual_self_propelled', 'manual_attendant', 'power_chair', 'scooter',
            'bariatric_manual', 'bariatric_power', 'walker_rollator',
            'mixed', 'not_device_scoped')`
**Verdict:** `OK`

### [0505] A6/OFF — source_value_extractions CHECK(contested IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (contested outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "contested") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-1276", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-1277", "updated_at": "PROBE-1278", "claimed_value": "PROBE-1279", "contested": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: contested IN (0, 1)`
**Verdict:** `OK`

### [0506] A6/OFF — source_value_extractions CHECK( (claim_type = 'absent' AND claimed_value IS NULL) OR (claim_type <> 'absent' AND claimed_value IS NOT NULL) )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (claim_type='absent' with claimed_value non-NULL; FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-1280", "claim_type": "absent", "extraction_method": "skim", "created_at": "PROBE-1281", "updated_at": "PROBE-1282", "claimed_value": "PROBE-CLAIMED_VALUE"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: (claim_type =  'absent' AND claimed_value IS NULL) OR
    (claim_type <> 'absent' AND claimed_value IS NOT NULL)`
**Verdict:** `OK`

### [0507] A6/OFF — spec_value_probes CHECK(direction IN ('up','down'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (direction outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-1284", "walk_id": "PROBE-1285", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-1286", "direction": "PROBE-INVALID-ENUM", "population": "PROBE-1287", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-1288", "created_at": "PROBE-1289", "created_by_session": "PROBE-1290"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: direction IN ('up','down')`
**Verdict:** `OK`

### [0508] A6/OFF — spec_value_probes CHECK(claim_type IN ( 'minimum','maximum','target','range_low','range_high' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (claim_type outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-1291", "walk_id": "PROBE-1292", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-1293", "direction": "up", "population": "PROBE-1294", "claim_type": "PROBE-INVALID-ENUM", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-1295", "created_at": "PROBE-1296", "created_by_session": "PROBE-1297"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: claim_type IN (
                            'minimum','maximum','target','range_low','range_high'
                        )`
**Verdict:** `OK`

### [0509] A6/OFF — spec_value_probes CHECK(phase IN ( 'outer-pass-1st','outer-pass-2nd','outer-stop', 'refinement-pass-1st','refinement-pass-2nd','refine)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (phase outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-1298", "walk_id": "PROBE-1299", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-1300", "direction": "up", "population": "PROBE-1301", "claim_type": "minimum", "step_index": 1, "phase": "PROBE-INVALID-ENUM", "step_value": 1.0, "step_value_unit": "PROBE-1302", "created_at": "PROBE-1303", "created_by_session": "PROBE-1304"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: phase IN (
                            'outer-pass-1st','outer-pass-2nd','outer-stop',
                            'refinement-pass-1st','refinement-pass-2nd','refinement-stop',
                            'final'
                        )`
**Verdict:** `OK`

### [0510] A6/OFF — spec_value_probes CHECK(passes_strict IN (0,1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (passes_strict outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session", "passes_strict") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-1305", "walk_id": "PROBE-1306", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-1307", "direction": "up", "population": "PROBE-1308", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-1309", "created_at": "PROBE-1310", "created_by_session": "PROBE-1311", "passes_strict": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: passes_strict IN (0,1)`
**Verdict:** `OK`

### [0511] A6/OFF — specification_source_links CHECK(role IN ('governing'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (role outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "specification_source_links" ("ref_id", "specification_id", "role") VALUES (?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "specification_id": 1, "role": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: role IN ('governing')`
**Verdict:** `OK`

### [0512] A6/OFF — specifications CHECK(state IN ('stated', 'provisional', 'pending', 'not_applicable'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (state outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state") VALUES (?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: state IN ('stated', 'provisional',
                                                    'pending', 'not_applicable')`
**Verdict:** `OK`

### [0513] A6/OFF — specifications CHECK(design_scale IN ('universal', 'population', 'person'))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (design_scale outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "design_scale") VALUES (?, ?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": "stated", "design_scale": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: design_scale IN ('universal', 'population', 'person')`
**Verdict:** `OK`

### [0514] A6/OFF — specifications CHECK(governing_refs IS NULL OR json_valid(governing_refs))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (invalid JSON in governing_refs; FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "governing_refs") VALUES (?, ?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": "stated", "governing_refs": "{not-json"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: governing_refs IS NULL OR json_valid(governing_refs)`
**Verdict:** `OK`

### [0515] A6/OFF — specifications CHECK(code_floor_only IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (code_floor_only outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "code_floor_only") VALUES (?, ?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": "stated", "code_floor_only": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: code_floor_only IN (0, 1)`
**Verdict:** `OK`

### [0516] A6/OFF — specifications CHECK(has_unverified_sources IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (has_unverified_sources outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "has_unverified_sources") VALUES (?, ?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": "stated", "has_unverified_sources": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: has_unverified_sources IN (0, 1)`
**Verdict:** `OK`

### [0517] A6/OFF — specifications CHECK(all_sources_disqualified IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (all_sources_disqualified outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "all_sources_disqualified") VALUES (?, ?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": "stated", "all_sources_disqualified": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: all_sources_disqualified IN (0, 1)`
**Verdict:** `OK`

### [0518] A6/OFF — specifications CHECK(regulatory_stratum_only IN (0, 1))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (regulatory_stratum_only outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "regulatory_stratum_only") VALUES (?, ?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": "stated", "regulatory_stratum_only": 987654321}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: regulatory_stratum_only IN (0, 1)`
**Verdict:** `OK`

### [0519] A6/OFF — supersession_check CHECK(anchor_tier BETWEEN 1 AND 6)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (anchor_tier above range; FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-1313", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-1314", "ref_id": "PROBE-PK-1012", "anchor_tier": 7, "anchor_evidence_type": "PROBE-1315", "outcome": "current_best", "search_strategy_record": "PROBE-1316", "checked_at": "PROBE-1317", "checked_by_session": "PROBE-1318", "check_method": "pubmed_search"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: anchor_tier BETWEEN 1 AND 6`
**Verdict:** `OK`

### [0520] A6/OFF — supersession_check CHECK(outcome IN ( 'current_best', 'superseded_by', 'refined_by', 'divergent_no_supersession', 'co1_addition_logged')   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-1319", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-1320", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-1321", "outcome": "PROBE-INVALID-ENUM", "search_strategy_record": "PROBE-1322", "checked_at": "PROBE-1323", "checked_by_session": "PROBE-1324", "check_method": "pubmed_search"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: outcome IN (
        'current_best',
        'superseded_by',
        'refined_by',
        'divergent_no_supersession',
        'co1_addition_logged',
        'pending'  -- check started but not yet completed; should not appear on closed slug
    )`
**Verdict:** `OK`

### [0521] A6/OFF — supersession_check CHECK(check_method IN ( 'pubmed_search', 'scholar_gateway', 'cochrane_direct', 'standards_body_direct', 'multilingua)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (check_method outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-1325", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-1326", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-1327", "outcome": "current_best", "search_strategy_record": "PROBE-1328", "checked_at": "PROBE-1329", "checked_by_session": "PROBE-1330", "check_method": "PROBE-INVALID-ENUM"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: check_method IN (
        'pubmed_search', 'scholar_gateway', 'cochrane_direct',
        'standards_body_direct', 'multilingual_research',
        'composite'
    )`
**Verdict:** `OK`

### [0522] A6/OFF — supersession_check CHECK( (outcome IN ('superseded_by','refined_by','divergent_no_supersession') AND (superseding_ref_ids IS NOT NULL O)   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-1331", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-1332", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-1333", "outcome": "PROBE-INVALID-ENUM", "search_strategy_record": "PROBE-1334", "checked_at": "PROBE-1335", "checked_by_session": "PROBE-1336", "check_method": "pubmed_search"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: outcome IN (
        'current_best',
        'superseded_by',
        'refined_by',
        'divergent_no_supersession',
        'co1_addition_logged',
        'pending'  -- check started but not yet completed; should not appear on closed slug
    )`
**Verdict:** `OK`

### [0523] A6/OFF — supersession_check CHECK( outcome != 'refined_by' OR refinement_dimension IS NOT NULL )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome='refined_by' with refinement_dimension NULL; FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method", "refinement_dimension") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-1337", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-1338", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-1339", "outcome": "refined_by", "search_strategy_record": "PROBE-1340", "checked_at": "PROBE-1341", "checked_by_session": "PROBE-1342", "check_method": "pubmed_search", "refinement_dimension": null}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: -- superseded_by / refined_by / divergent_no_supersession require superseding refs
        (outcome IN ('superseded_by','refined_by','divergent_no_supersession')
         AND (superseding_ref_ids IS NOT NULL OR superseding_dois IS NOT NULL))
        OR
        outcome IN ('current_best','co1_addition_logged','pending')`
**Verdict:** `OK`

### [0524] A6/OFF — supersession_check CHECK( outcome != 'divergent_no_supersession' OR divergence_notes IS NOT NULL )   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (outcome='divergent_no_supersession' with divergence_notes NULL; FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method", "divergence_notes") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-1343", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-1344", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-1345", "outcome": "divergent_no_supersession", "search_strategy_record": "PROBE-1346", "checked_at": "PROBE-1347", "checked_by_session": "PROBE-1348", "check_method": "pubmed_search", "divergence_notes": null}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: -- superseded_by / refined_by / divergent_no_supersession require superseding refs
        (outcome IN ('superseded_by','refined_by','divergent_no_supersession')
         AND (superseding_ref_ids IS NOT NULL OR superseding_dois IS NOT NULL))
        OR
        outcome IN ('current_best','co1_addition_logged','pending')`
**Verdict:** `OK`

### [0525] A6/OFF — supersession_check CHECK( outcome != 'co1_addition_logged' OR anchor_evidence_type = 'co1' )   `2026-08-12 08:35:28Z`
**Action:** construct a violating row (FK=OFF)
**Expected:** CHECK fires
**Actual:** no mechanical violation constructible for this expression (cross-column/complex predicate)
**Verdict:** `BLOCKED`

### [0526] A6/OFF — term_aliases CHECK(alias_type IN ( 'SYNONYM','TRANSLATION','NARROWER', 'BROADER','DEPRECATED','DOMAIN' ))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (alias_type outside enum; FK=OFF)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "alias": "PROBE-1350", "language": "PROBE-1351", "alias_type": "PROBE-INVALID-ENUM", "created_at": "PROBE-1352", "created_by_session": "PROBE-1353", "updated_at": "PROBE-1354", "updated_by_session": "PROBE-1355"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: alias_type IN (
                            'SYNONYM','TRANSLATION','NARROWER',
                            'BROADER','DEPRECATED','DOMAIN'
                        )`
**Verdict:** `OK`

### [0527] A6/OFF — weighting_profile CHECK(json_valid(tier_weights))   `2026-08-12 08:35:28Z`
**Action:** insert row violating the CHECK (invalid JSON in tier_weights; FK=OFF)
**SQL:**
```sql
INSERT INTO "weighting_profile" ("audience", "use_pattern", "tier_weights") VALUES (?, ?, ?)  -- {"audience": "PROBE-1356", "use_pattern": "PROBE-1357", "tier_weights": "{not-json"}
```
**Expected:** CHECK constraint failed
**Actual:** rejected by CHECK
**Exception:** `IntegrityError: CHECK constraint failed: json_valid(tier_weights)`
**Verdict:** `OK`

### A7 — NOT NULL battery (267 non-PK NOT NULL columns), FK=ON and FK=OFF

### [0528] A7/ON — access_duration.definition   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "access_duration" ("definition", "code") VALUES (?, ?)  -- {"definition": null, "code": "PROBE-PK-1358"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_duration.definition`
**Verdict:** `OK`

### [0529] A7/ON — access_need_axis_map.relationship   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "access_need_axis_map" ("need_code", "axis_code", "relationship") VALUES (?, ?, ?)  -- {"need_code": "A-AT", "axis_code": "AX-AMB", "relationship": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_need_axis_map.relationship`
**Verdict:** `OK`

### [0530] A7/ON — access_need_icf.icf_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "access_need_icf" ("need_code", "icf_code", "icf_type", "confidence") VALUES (?, ?, ?, ?)  -- {"need_code": "A-AT", "icf_code": "PROBE-1359", "icf_type": null, "confidence": "confirmed"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_need_icf.icf_type`
**Verdict:** `OK`

### [0531] A7/ON — access_need_icf.confidence   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "access_need_icf" ("need_code", "icf_code", "icf_type", "confidence") VALUES (?, ?, ?, ?)  -- {"need_code": "A-AT", "icf_code": "PROBE-1360", "icf_type": "b", "confidence": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_need_icf.confidence`
**Verdict:** `OK`

### [0532] A7/ON — access_needs.family   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "access_needs" ("need_code", "family", "design_obligation") VALUES (?, ?, ?)  -- {"need_code": "PROBE-1361", "family": null, "design_obligation": "PROBE-1362"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_needs.family`
**Verdict:** `OK`

### [0533] A7/ON — access_needs.design_obligation   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "access_needs" ("need_code", "family", "design_obligation") VALUES (?, ?, ?)  -- {"need_code": "PROBE-1363", "family": "perceiving", "design_obligation": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_needs.design_obligation`
**Verdict:** `OK`

### [0534] A7/ON — access_needs.source_version   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "access_needs" ("need_code", "family", "design_obligation", "source_version") VALUES (?, ?, ?, ?)  -- {"need_code": "PROBE-1364", "family": "perceiving", "design_obligation": "PROBE-1365", "source_version": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_needs.source_version`
**Verdict:** `OK`

### [0535] A7/ON — access_stakes.definition   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "access_stakes" ("definition", "code") VALUES (?, ?)  -- {"definition": null, "code": "PROBE-PK-1366"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_stakes.definition`
**Verdict:** `OK`

### [0536] A7/ON — axes.name   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "axes" ("axis_code", "name", "mechanism", "coverage_status", "falsification_condition") VALUES (?, ?, ?, ?, ?)  -- {"axis_code": "PROBE-1367", "name": null, "mechanism": "PROBE-1368", "coverage_status": "ESTABLISHED", "falsification_condition": "PROBE-1369"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: axes.name`
**Verdict:** `OK`

### [0537] A7/ON — axes.mechanism   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "axes" ("axis_code", "name", "mechanism", "coverage_status", "falsification_condition") VALUES (?, ?, ?, ?, ?)  -- {"axis_code": "PROBE-1370", "name": "PROBE-1371", "mechanism": null, "coverage_status": "ESTABLISHED", "falsification_condition": "PROBE-1372"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: axes.mechanism`
**Verdict:** `OK`

### [0538] A7/ON — axes.coverage_status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "axes" ("axis_code", "name", "mechanism", "coverage_status", "falsification_condition") VALUES (?, ?, ?, ?, ?)  -- {"axis_code": "PROBE-1373", "name": "PROBE-1374", "mechanism": "PROBE-1375", "coverage_status": null, "falsification_condition": "PROBE-1376"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: axes.coverage_status`
**Verdict:** `OK`

### [0539] A7/ON — axes.falsification_condition   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "axes" ("axis_code", "name", "mechanism", "coverage_status", "falsification_condition") VALUES (?, ?, ?, ?, ?)  -- {"axis_code": "PROBE-1377", "name": "PROBE-1378", "mechanism": "PROBE-1379", "coverage_status": "ESTABLISHED", "falsification_condition": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: axes.falsification_condition`
**Verdict:** `OK`

### [0540] A7/ON — bpc_metadata.population   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": null, "created_at": "PROBE-1380", "created_by_session": "PROBE-1381", "updated_at": "PROBE-1382", "updated_by_session": "PROBE-1383"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.population`
**Verdict:** `OK`

### [0541] A7/ON — bpc_metadata.pico_complete   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "pico_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-1384", "created_at": "PROBE-1385", "created_by_session": "PROBE-1386", "updated_at": "PROBE-1387", "updated_by_session": "PROBE-1388", "pico_complete": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.pico_complete`
**Verdict:** `OK`

### [0542] A7/ON — bpc_metadata.search_complete   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "search_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-1389", "created_at": "PROBE-1390", "created_by_session": "PROBE-1391", "updated_at": "PROBE-1392", "updated_by_session": "PROBE-1393", "search_complete": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.search_complete`
**Verdict:** `OK`

### [0543] A7/ON — bpc_metadata.bpc_complete   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "bpc_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-1394", "created_at": "PROBE-1395", "created_by_session": "PROBE-1396", "updated_at": "PROBE-1397", "updated_by_session": "PROBE-1398", "bpc_complete": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.bpc_complete`
**Verdict:** `OK`

### [0544] A7/ON — bpc_metadata.citation_mining_complete   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "citation_mining_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-1399", "created_at": "PROBE-1400", "created_by_session": "PROBE-1401", "updated_at": "PROBE-1402", "updated_by_session": "PROBE-1403", "citation_mining_complete": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.citation_mining_complete`
**Verdict:** `OK`

### [0545] A7/ON — bpc_metadata.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-1404", "created_at": null, "created_by_session": "PROBE-1405", "updated_at": "PROBE-1406", "updated_by_session": "PROBE-1407"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.created_at`
**Verdict:** `OK`

### [0546] A7/ON — bpc_metadata.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-1408", "created_at": "PROBE-1409", "created_by_session": null, "updated_at": "PROBE-1410", "updated_by_session": "PROBE-1411"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.created_by_session`
**Verdict:** `OK`

### [0547] A7/ON — bpc_metadata.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-1412", "created_at": "PROBE-1413", "created_by_session": "PROBE-1414", "updated_at": null, "updated_by_session": "PROBE-1415"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.updated_at`
**Verdict:** `OK`

### [0548] A7/ON — bpc_metadata.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-1416", "created_at": "PROBE-1417", "created_by_session": "PROBE-1418", "updated_at": "PROBE-1419", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.updated_by_session`
**Verdict:** `OK`

### [0549] A7/ON — bpc_metadata.supersession_check_complete   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "supersession_check_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "population": "PROBE-1420", "created_at": "PROBE-1421", "created_by_session": "PROBE-1422", "updated_at": "PROBE-1423", "updated_by_session": "PROBE-1424", "supersession_check_complete": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.supersession_check_complete`
**Verdict:** `OK`

### [0550] A7/ON — case_studies.slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-1425", "slug": null, "title": "PROBE-1426", "building_type": "PROBE-1427", "location": "PROBE-1428", "created_at": "PROBE-1429", "created_by_session": "PROBE-1430"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.slug`
**Verdict:** `OK`

### [0551] A7/ON — case_studies.title   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-1431", "slug": "PROBE-PK-158", "title": null, "building_type": "PROBE-1432", "location": "PROBE-1433", "created_at": "PROBE-1434", "created_by_session": "PROBE-1435"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.title`
**Verdict:** `OK`

### [0552] A7/ON — case_studies.building_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-1436", "slug": "PROBE-PK-158", "title": "PROBE-1437", "building_type": null, "location": "PROBE-1438", "created_at": "PROBE-1439", "created_by_session": "PROBE-1440"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.building_type`
**Verdict:** `OK`

### [0553] A7/ON — case_studies.location   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-1441", "slug": "PROBE-PK-158", "title": "PROBE-1442", "building_type": "PROBE-1443", "location": null, "created_at": "PROBE-1444", "created_by_session": "PROBE-1445"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.location`
**Verdict:** `OK`

### [0554] A7/ON — case_studies.harm_finding   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session", "harm_finding") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-1446", "slug": "PROBE-PK-158", "title": "PROBE-1447", "building_type": "PROBE-1448", "location": "PROBE-1449", "created_at": "PROBE-1450", "created_by_session": "PROBE-1451", "harm_finding": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.harm_finding`
**Verdict:** `OK`

### [0555] A7/ON — case_studies.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-1452", "slug": "PROBE-PK-158", "title": "PROBE-1453", "building_type": "PROBE-1454", "location": "PROBE-1455", "created_at": "PROBE-1456", "created_by_session": "PROBE-1457", "status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.status`
**Verdict:** `OK`

### [0556] A7/ON — case_studies.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-1458", "slug": "PROBE-PK-158", "title": "PROBE-1459", "building_type": "PROBE-1460", "location": "PROBE-1461", "created_at": null, "created_by_session": "PROBE-1462"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.created_at`
**Verdict:** `OK`

### [0557] A7/ON — case_studies.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-1463", "slug": "PROBE-PK-158", "title": "PROBE-1464", "building_type": "PROBE-1465", "location": "PROBE-1466", "created_at": "PROBE-1467", "created_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.created_by_session`
**Verdict:** `OK`

### [0558] A7/ON — case_study_outcomes.case_study_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "case_study_outcomes" ("case_study_id", "metric") VALUES (?, ?)  -- {"case_study_id": null, "metric": "PROBE-1468"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_study_outcomes.case_study_id`
**Verdict:** `OK`

### [0559] A7/ON — case_study_outcomes.metric   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "case_study_outcomes" ("case_study_id", "metric") VALUES (?, ?)  -- {"case_study_id": "PROBE-CASE_STUDY_ID", "metric": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_study_outcomes.metric`
**Verdict:** `OK`

### [0560] A7/ON — case_study_strategies.case_study_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "case_study_strategies" ("case_study_id", "strategy") VALUES (?, ?)  -- {"case_study_id": null, "strategy": "PROBE-1469"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_study_strategies.case_study_id`
**Verdict:** `OK`

### [0561] A7/ON — case_study_strategies.strategy   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "case_study_strategies" ("case_study_id", "strategy") VALUES (?, ?)  -- {"case_study_id": "PROBE-CASE_STUDY_ID", "strategy": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_study_strategies.strategy`
**Verdict:** `OK`

### [0562] A7/ON — citation_mining.backward   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session", "backward") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "aac-speech-production-environments", "local_ref_id": "PROBE-1470", "created_at": "PROBE-1471", "created_by_session": "PROBE-1472", "updated_at": "PROBE-1473", "updated_by_session": "PROBE-1474", "backward": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.backward`
**Verdict:** `OK`

### [0563] A7/ON — citation_mining.forward   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session", "forward") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "aac-speech-production-environments", "local_ref_id": "PROBE-1475", "created_at": "PROBE-1476", "created_by_session": "PROBE-1477", "updated_at": "PROBE-1478", "updated_by_session": "PROBE-1479", "forward": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.forward`
**Verdict:** `OK`

### [0564] A7/ON — citation_mining.connections_produced   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session", "connections_produced") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "aac-speech-production-environments", "local_ref_id": "PROBE-1480", "created_at": "PROBE-1481", "created_by_session": "PROBE-1482", "updated_at": "PROBE-1483", "updated_by_session": "PROBE-1484", "connections_produced": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.connections_produced`
**Verdict:** `OK`

### [0565] A7/ON — citation_mining.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "aac-speech-production-environments", "local_ref_id": "PROBE-1485", "created_at": null, "created_by_session": "PROBE-1486", "updated_at": "PROBE-1487", "updated_by_session": "PROBE-1488"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.created_at`
**Verdict:** `OK`

### [0566] A7/ON — citation_mining.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "aac-speech-production-environments", "local_ref_id": "PROBE-1489", "created_at": "PROBE-1490", "created_by_session": null, "updated_at": "PROBE-1491", "updated_by_session": "PROBE-1492"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.created_by_session`
**Verdict:** `OK`

### [0567] A7/ON — citation_mining.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "aac-speech-production-environments", "local_ref_id": "PROBE-1493", "created_at": "PROBE-1494", "created_by_session": "PROBE-1495", "updated_at": null, "updated_by_session": "PROBE-1496"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.updated_at`
**Verdict:** `OK`

### [0568] A7/ON — citation_mining.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "aac-speech-production-environments", "local_ref_id": "PROBE-1497", "created_at": "PROBE-1498", "created_by_session": "PROBE-1499", "updated_at": "PROBE-1500", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.updated_by_session`
**Verdict:** `OK`

### [0569] A7/ON — conflicts.domain   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-1501", "domain": null, "pop_a": "PROBE-1502", "pop_b": "PROBE-1503", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-1504", "created_by_session": "PROBE-1505", "updated_at": "PROBE-1506", "updated_by_session": "PROBE-1507"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.domain`
**Verdict:** `OK`

### [0570] A7/ON — conflicts.pop_a   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-1508", "domain": "PROBE-1509", "pop_a": null, "pop_b": "PROBE-1510", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-1511", "created_by_session": "PROBE-1512", "updated_at": "PROBE-1513", "updated_by_session": "PROBE-1514"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.pop_a`
**Verdict:** `OK`

### [0571] A7/ON — conflicts.pop_b   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-1515", "domain": "PROBE-1516", "pop_a": "PROBE-1517", "pop_b": null, "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-1518", "created_by_session": "PROBE-1519", "updated_at": "PROBE-1520", "updated_by_session": "PROBE-1521"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.pop_b`
**Verdict:** `OK`

### [0572] A7/ON — conflicts.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-1522", "domain": "PROBE-1523", "pop_a": "PROBE-1524", "pop_b": "PROBE-1525", "status": null, "created_at": "PROBE-1526", "created_by_session": "PROBE-1527", "updated_at": "PROBE-1528", "updated_by_session": "PROBE-1529"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.status`
**Verdict:** `OK`

### [0573] A7/ON — conflicts.source_skill   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "source_skill") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-1530", "domain": "PROBE-1531", "pop_a": "PROBE-1532", "pop_b": "PROBE-1533", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-1534", "created_by_session": "PROBE-1535", "updated_at": "PROBE-1536", "updated_by_session": "PROBE-1537", "source_skill": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.source_skill`
**Verdict:** `OK`

### [0574] A7/ON — conflicts.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-1538", "domain": "PROBE-1539", "pop_a": "PROBE-1540", "pop_b": "PROBE-1541", "status": "RESOLVED-EVIDENCE", "created_at": null, "created_by_session": "PROBE-1542", "updated_at": "PROBE-1543", "updated_by_session": "PROBE-1544"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.created_at`
**Verdict:** `OK`

### [0575] A7/ON — conflicts.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-1545", "domain": "PROBE-1546", "pop_a": "PROBE-1547", "pop_b": "PROBE-1548", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-1549", "created_by_session": null, "updated_at": "PROBE-1550", "updated_by_session": "PROBE-1551"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.created_by_session`
**Verdict:** `OK`

### [0576] A7/ON — conflicts.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-1552", "domain": "PROBE-1553", "pop_a": "PROBE-1554", "pop_b": "PROBE-1555", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-1556", "created_by_session": "PROBE-1557", "updated_at": null, "updated_by_session": "PROBE-1558"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.updated_at`
**Verdict:** `OK`

### [0577] A7/ON — conflicts.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-1559", "domain": "PROBE-1560", "pop_a": "PROBE-1561", "pop_b": "PROBE-1562", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-1563", "created_by_session": "PROBE-1564", "updated_at": "PROBE-1565", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.updated_by_session`
**Verdict:** `OK`

### [0578] A7/ON — connections.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-1566", "status": null, "confidence": "HIGH", "filed_in": "PROBE-1567", "created_at": "PROBE-1568", "created_by_session": "PROBE-1569", "updated_at": "PROBE-1570", "updated_by_session": "PROBE-1571"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.status`
**Verdict:** `OK`

### [0579] A7/ON — connections.confidence   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-1572", "status": "PENDING", "confidence": null, "filed_in": "PROBE-1573", "created_at": "PROBE-1574", "created_by_session": "PROBE-1575", "updated_at": "PROBE-1576", "updated_by_session": "PROBE-1577"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.confidence`
**Verdict:** `OK`

### [0580] A7/ON — connections.filed_in   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-1578", "status": "PENDING", "confidence": "HIGH", "filed_in": null, "created_at": "PROBE-1579", "created_by_session": "PROBE-1580", "updated_at": "PROBE-1581", "updated_by_session": "PROBE-1582"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.filed_in`
**Verdict:** `OK`

### [0581] A7/ON — connections.opus_reviewed   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session", "opus_reviewed") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-1583", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-1584", "created_at": "PROBE-1585", "created_by_session": "PROBE-1586", "updated_at": "PROBE-1587", "updated_by_session": "PROBE-1588", "opus_reviewed": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.opus_reviewed`
**Verdict:** `OK`

### [0582] A7/ON — connections.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-1589", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-1590", "created_at": null, "created_by_session": "PROBE-1591", "updated_at": "PROBE-1592", "updated_by_session": "PROBE-1593"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.created_at`
**Verdict:** `OK`

### [0583] A7/ON — connections.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-1594", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-1595", "created_at": "PROBE-1596", "created_by_session": null, "updated_at": "PROBE-1597", "updated_by_session": "PROBE-1598"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.created_by_session`
**Verdict:** `OK`

### [0584] A7/ON — connections.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-1599", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-1600", "created_at": "PROBE-1601", "created_by_session": "PROBE-1602", "updated_at": null, "updated_by_session": "PROBE-1603"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.updated_at`
**Verdict:** `OK`

### [0585] A7/ON — connections.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-1604", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-1605", "created_at": "PROBE-1606", "created_by_session": "PROBE-1607", "updated_at": "PROBE-1608", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.updated_by_session`
**Verdict:** `OK`

### [0586] A7/ON — convergence_assessment.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "convergence_assessment" ("status") VALUES (?)  -- {"status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: convergence_assessment.status`
**Verdict:** `OK`

### [0587] A7/ON — data_migrations.applied_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "data_migrations" ("migration_id", "applied_at", "content_sha") VALUES (?, ?, ?)  -- {"migration_id": "PROBE-1610", "applied_at": null, "content_sha": "PROBE-1611"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: data_migrations.applied_at`
**Verdict:** `OK`

### [0588] A7/ON — data_migrations.content_sha   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "data_migrations" ("migration_id", "applied_at", "content_sha") VALUES (?, ?, ?)  -- {"migration_id": "PROBE-1612", "applied_at": "PROBE-1613", "content_sha": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: data_migrations.content_sha`
**Verdict:** `OK`

### [0589] A7/ON — db_meta.value   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "db_meta" ("key", "value") VALUES (?, ?)  -- {"key": "PROBE-1615", "value": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: db_meta.value`
**Verdict:** `OK`

### [0590] A7/ON — decisions.category   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1616", "category": null, "delegation": "DG-NON", "summary": "PROBE-1617", "outcome": "PROBE-1618", "rationale": "PROBE-1619", "decision_date": "PROBE-1620", "decided_by": "PROBE-1621", "model_routing": "PROBE-1622", "effort_level": 1, "review_status": "PROBE-1623", "created_at": "PROBE-1624", "created_by_session": "PROBE-1625", "updated_at": "PROBE-1626", "updated_by_session": "PROBE-1627"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.category`
**Verdict:** `OK`

### [0591] A7/ON — decisions.delegation   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1628", "category": "D-DOCT", "delegation": null, "summary": "PROBE-1629", "outcome": "PROBE-1630", "rationale": "PROBE-1631", "decision_date": "PROBE-1632", "decided_by": "PROBE-1633", "model_routing": "PROBE-1634", "effort_level": 1, "review_status": "PROBE-1635", "created_at": "PROBE-1636", "created_by_session": "PROBE-1637", "updated_at": "PROBE-1638", "updated_by_session": "PROBE-1639"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.delegation`
**Verdict:** `OK`

### [0592] A7/ON — decisions.summary   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1640", "category": "D-DOCT", "delegation": "DG-NON", "summary": null, "outcome": "PROBE-1641", "rationale": "PROBE-1642", "decision_date": "PROBE-1643", "decided_by": "PROBE-1644", "model_routing": "PROBE-1645", "effort_level": 1, "review_status": "PROBE-1646", "created_at": "PROBE-1647", "created_by_session": "PROBE-1648", "updated_at": "PROBE-1649", "updated_by_session": "PROBE-1650"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.summary`
**Verdict:** `OK`

### [0593] A7/ON — decisions.outcome   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1651", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1652", "outcome": null, "rationale": "PROBE-1653", "decision_date": "PROBE-1654", "decided_by": "PROBE-1655", "model_routing": "PROBE-1656", "effort_level": 1, "review_status": "PROBE-1657", "created_at": "PROBE-1658", "created_by_session": "PROBE-1659", "updated_at": "PROBE-1660", "updated_by_session": "PROBE-1661"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.outcome`
**Verdict:** `OK`

### [0594] A7/ON — decisions.rationale   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1662", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1663", "outcome": "PROBE-1664", "rationale": null, "decision_date": "PROBE-1665", "decided_by": "PROBE-1666", "model_routing": "PROBE-1667", "effort_level": 1, "review_status": "PROBE-1668", "created_at": "PROBE-1669", "created_by_session": "PROBE-1670", "updated_at": "PROBE-1671", "updated_by_session": "PROBE-1672"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.rationale`
**Verdict:** `OK`

### [0595] A7/ON — decisions.decision_date   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1673", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1674", "outcome": "PROBE-1675", "rationale": "PROBE-1676", "decision_date": null, "decided_by": "PROBE-1677", "model_routing": "PROBE-1678", "effort_level": 1, "review_status": "PROBE-1679", "created_at": "PROBE-1680", "created_by_session": "PROBE-1681", "updated_at": "PROBE-1682", "updated_by_session": "PROBE-1683"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.decision_date`
**Verdict:** `OK`

### [0596] A7/ON — decisions.decided_by   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1684", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1685", "outcome": "PROBE-1686", "rationale": "PROBE-1687", "decision_date": "PROBE-1688", "decided_by": null, "model_routing": "PROBE-1689", "effort_level": 1, "review_status": "PROBE-1690", "created_at": "PROBE-1691", "created_by_session": "PROBE-1692", "updated_at": "PROBE-1693", "updated_by_session": "PROBE-1694"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.decided_by`
**Verdict:** `OK`

### [0597] A7/ON — decisions.model_routing   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1695", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1696", "outcome": "PROBE-1697", "rationale": "PROBE-1698", "decision_date": "PROBE-1699", "decided_by": "PROBE-1700", "model_routing": null, "effort_level": 1, "review_status": "PROBE-1701", "created_at": "PROBE-1702", "created_by_session": "PROBE-1703", "updated_at": "PROBE-1704", "updated_by_session": "PROBE-1705"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.model_routing`
**Verdict:** `OK`

### [0598] A7/ON — decisions.effort_level   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1706", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1707", "outcome": "PROBE-1708", "rationale": "PROBE-1709", "decision_date": "PROBE-1710", "decided_by": "PROBE-1711", "model_routing": "PROBE-1712", "effort_level": null, "review_status": "PROBE-1713", "created_at": "PROBE-1714", "created_by_session": "PROBE-1715", "updated_at": "PROBE-1716", "updated_by_session": "PROBE-1717"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.effort_level`
**Verdict:** `OK`

### [0599] A7/ON — decisions.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1718", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1719", "outcome": "PROBE-1720", "rationale": "PROBE-1721", "decision_date": "PROBE-1722", "decided_by": "PROBE-1723", "model_routing": "PROBE-1724", "effort_level": 1, "review_status": "PROBE-1725", "created_at": "PROBE-1726", "created_by_session": "PROBE-1727", "updated_at": "PROBE-1728", "updated_by_session": "PROBE-1729", "status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.status`
**Verdict:** `OK`

### [0600] A7/ON — decisions.review_status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1730", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1731", "outcome": "PROBE-1732", "rationale": "PROBE-1733", "decision_date": "PROBE-1734", "decided_by": "PROBE-1735", "model_routing": "PROBE-1736", "effort_level": 1, "review_status": null, "created_at": "PROBE-1737", "created_by_session": "PROBE-1738", "updated_at": "PROBE-1739", "updated_by_session": "PROBE-1740"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.review_status`
**Verdict:** `OK`

### [0601] A7/ON — decisions.supersedes   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session", "supersedes") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1741", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1742", "outcome": "PROBE-1743", "rationale": "PROBE-1744", "decision_date": "PROBE-1745", "decided_by": "PROBE-1746", "model_routing": "PROBE-1747", "effort_level": 1, "review_status": "PROBE-1748", "created_at": "PROBE-1749", "created_by_session": "PROBE-1750", "updated_at": "PROBE-1751", "updated_by_session": "PROBE-1752", "supersedes": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.supersedes`
**Verdict:** `OK`

### [0602] A7/ON — decisions.predecessors   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session", "predecessors") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1753", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1754", "outcome": "PROBE-1755", "rationale": "PROBE-1756", "decision_date": "PROBE-1757", "decided_by": "PROBE-1758", "model_routing": "PROBE-1759", "effort_level": 1, "review_status": "PROBE-1760", "created_at": "PROBE-1761", "created_by_session": "PROBE-1762", "updated_at": "PROBE-1763", "updated_by_session": "PROBE-1764", "predecessors": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.predecessors`
**Verdict:** `OK`

### [0603] A7/ON — decisions.decision_artifacts   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session", "decision_artifacts") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1765", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1766", "outcome": "PROBE-1767", "rationale": "PROBE-1768", "decision_date": "PROBE-1769", "decided_by": "PROBE-1770", "model_routing": "PROBE-1771", "effort_level": 1, "review_status": "PROBE-1772", "created_at": "PROBE-1773", "created_by_session": "PROBE-1774", "updated_at": "PROBE-1775", "updated_by_session": "PROBE-1776", "decision_artifacts": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.decision_artifacts`
**Verdict:** `OK`

### [0604] A7/ON — decisions.alternatives_considered   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session", "alternatives_considered") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1777", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1778", "outcome": "PROBE-1779", "rationale": "PROBE-1780", "decision_date": "PROBE-1781", "decided_by": "PROBE-1782", "model_routing": "PROBE-1783", "effort_level": 1, "review_status": "PROBE-1784", "created_at": "PROBE-1785", "created_by_session": "PROBE-1786", "updated_at": "PROBE-1787", "updated_by_session": "PROBE-1788", "alternatives_considered": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.alternatives_considered`
**Verdict:** `OK`

### [0605] A7/ON — decisions.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1789", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1790", "outcome": "PROBE-1791", "rationale": "PROBE-1792", "decision_date": "PROBE-1793", "decided_by": "PROBE-1794", "model_routing": "PROBE-1795", "effort_level": 1, "review_status": "PROBE-1796", "created_at": null, "created_by_session": "PROBE-1797", "updated_at": "PROBE-1798", "updated_by_session": "PROBE-1799"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.created_at`
**Verdict:** `OK`

### [0606] A7/ON — decisions.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1800", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1801", "outcome": "PROBE-1802", "rationale": "PROBE-1803", "decision_date": "PROBE-1804", "decided_by": "PROBE-1805", "model_routing": "PROBE-1806", "effort_level": 1, "review_status": "PROBE-1807", "created_at": "PROBE-1808", "created_by_session": null, "updated_at": "PROBE-1809", "updated_by_session": "PROBE-1810"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.created_by_session`
**Verdict:** `OK`

### [0607] A7/ON — decisions.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1811", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1812", "outcome": "PROBE-1813", "rationale": "PROBE-1814", "decision_date": "PROBE-1815", "decided_by": "PROBE-1816", "model_routing": "PROBE-1817", "effort_level": 1, "review_status": "PROBE-1818", "created_at": "PROBE-1819", "created_by_session": "PROBE-1820", "updated_at": null, "updated_by_session": "PROBE-1821"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.updated_at`
**Verdict:** `OK`

### [0608] A7/ON — decisions.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-1822", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-1823", "outcome": "PROBE-1824", "rationale": "PROBE-1825", "decision_date": "PROBE-1826", "decided_by": "PROBE-1827", "model_routing": "PROBE-1828", "effort_level": 1, "review_status": "PROBE-1829", "created_at": "PROBE-1830", "created_by_session": "PROBE-1831", "updated_at": "PROBE-1832", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.updated_by_session`
**Verdict:** `OK`

### [0609] A7/ON — economics_entries.pillar   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-1833", "pillar": null, "entry_type": "cost_premium", "source": "PROBE-1834", "finding": "PROBE-1835", "created_at": "PROBE-1836", "created_by_session": "PROBE-1837"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.pillar`
**Verdict:** `OK`

### [0610] A7/ON — economics_entries.entry_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-1838", "pillar": "health", "entry_type": null, "source": "PROBE-1839", "finding": "PROBE-1840", "created_at": "PROBE-1841", "created_by_session": "PROBE-1842"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.entry_type`
**Verdict:** `OK`

### [0611] A7/ON — economics_entries.source   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-1843", "pillar": "health", "entry_type": "cost_premium", "source": null, "finding": "PROBE-1844", "created_at": "PROBE-1845", "created_by_session": "PROBE-1846"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.source`
**Verdict:** `OK`

### [0612] A7/ON — economics_entries.finding   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-1847", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-1848", "finding": null, "created_at": "PROBE-1849", "created_by_session": "PROBE-1850"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.finding`
**Verdict:** `OK`

### [0613] A7/ON — economics_entries.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-1851", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-1852", "finding": "PROBE-1853", "created_at": "PROBE-1854", "created_by_session": "PROBE-1855", "status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.status`
**Verdict:** `OK`

### [0614] A7/ON — economics_entries.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-1856", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-1857", "finding": "PROBE-1858", "created_at": null, "created_by_session": "PROBE-1859"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.created_at`
**Verdict:** `OK`

### [0615] A7/ON — economics_entries.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-1860", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-1861", "finding": "PROBE-1862", "created_at": "PROBE-1863", "created_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.created_by_session`
**Verdict:** `OK`

### [0616] A7/ON — evidence_population_match.source_ref   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-1864", "source_ref": null, "target_population": "PROBE-1865", "match_grade": "EXACT", "created_at": "PROBE-1866", "created_by_session": "PROBE-1867"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_population_match.source_ref`
**Verdict:** `OK`

### [0617] A7/ON — evidence_population_match.target_population   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-1868", "source_ref": "PROBE-1869", "target_population": null, "match_grade": "EXACT", "created_at": "PROBE-1870", "created_by_session": "PROBE-1871"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_population_match.target_population`
**Verdict:** `OK`

### [0618] A7/ON — evidence_population_match.match_grade   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-1872", "source_ref": "PROBE-1873", "target_population": "PROBE-1874", "match_grade": null, "created_at": "PROBE-1875", "created_by_session": "PROBE-1876"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_population_match.match_grade`
**Verdict:** `OK`

### [0619] A7/ON — evidence_population_match.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-1877", "source_ref": "PROBE-1878", "target_population": "PROBE-1879", "match_grade": "EXACT", "created_at": null, "created_by_session": "PROBE-1880"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_population_match.created_at`
**Verdict:** `OK`

### [0620] A7/ON — evidence_population_match.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-1881", "source_ref": "PROBE-1882", "target_population": "PROBE-1883", "match_grade": "EXACT", "created_at": "PROBE-1884", "created_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_population_match.created_by_session`
**Verdict:** `OK`

### [0621] A7/ON — evidence_source_authors.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_source_authors" ("ref_id", "position") VALUES (?, ?)  -- {"ref_id": null, "position": 1}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_source_authors.ref_id`
**Verdict:** `OK`

### [0622] A7/ON — evidence_source_authors.position   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_source_authors" ("ref_id", "position") VALUES (?, ?)  -- {"ref_id": "PROBE-PK-167", "position": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_source_authors.position`
**Verdict:** `OK`

### [0623] A7/ON — evidence_source_authors.is_corporate   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_source_authors" ("ref_id", "position", "is_corporate") VALUES (?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "position": 1, "is_corporate": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_source_authors.is_corporate`
**Verdict:** `OK`

### [0624] A7/ON — evidence_source_authors.role   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_source_authors" ("ref_id", "position", "role") VALUES (?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "position": 1, "role": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_source_authors.role`
**Verdict:** `OK`

### [0625] A7/ON — evidence_sources.data_capture_status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "data_capture_status") VALUES (?, ?)  -- {"ref_id": "PROBE-1885", "data_capture_status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_sources.data_capture_status`
**Verdict:** `OK`

### [0626] A7/ON — evidence_sources.citation_mining_status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "citation_mining_status") VALUES (?, ?)  -- {"ref_id": "PROBE-1886", "citation_mining_status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_sources.citation_mining_status`
**Verdict:** `OK`

### [0627] A7/ON — external_root_registry.description   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "external_root_registry" ("root_id", "description") VALUES (?, ?)  -- {"root_id": "PROBE-1887", "description": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: external_root_registry.description`
**Verdict:** `OK`

### [0628] A7/ON — gap_mining.gap_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": null, "attempt_at": "PROBE-1888", "attempted_by_session": "PROBE-1889", "search_strategy_record": "PROBE-1890", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-1891"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.gap_id`
**Verdict:** `OK`

### [0629] A7/ON — gap_mining.attempt_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-492", "attempt_at": null, "attempted_by_session": "PROBE-1892", "search_strategy_record": "PROBE-1893", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-1894"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.attempt_at`
**Verdict:** `OK`

### [0630] A7/ON — gap_mining.attempted_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-492", "attempt_at": "PROBE-1895", "attempted_by_session": null, "search_strategy_record": "PROBE-1896", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-1897"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.attempted_by_session`
**Verdict:** `OK`

### [0631] A7/ON — gap_mining.search_strategy_record   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-492", "attempt_at": "PROBE-1898", "attempted_by_session": "PROBE-1899", "search_strategy_record": null, "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-1900"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.search_strategy_record`
**Verdict:** `OK`

### [0632] A7/ON — gap_mining.candidates_returned   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged", "candidates_returned") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-492", "attempt_at": "PROBE-1901", "attempted_by_session": "PROBE-1902", "search_strategy_record": "PROBE-1903", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-1904", "candidates_returned": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.candidates_returned`
**Verdict:** `OK`

### [0633] A7/ON — gap_mining.candidates_reviewed   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged", "candidates_reviewed") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-492", "attempt_at": "PROBE-1905", "attempted_by_session": "PROBE-1906", "search_strategy_record": "PROBE-1907", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-1908", "candidates_reviewed": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.candidates_reviewed`
**Verdict:** `OK`

### [0634] A7/ON — gap_mining.outcome   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-492", "attempt_at": "PROBE-1909", "attempted_by_session": "PROBE-1910", "search_strategy_record": "PROBE-1911", "outcome": null, "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-1912"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.outcome`
**Verdict:** `OK`

### [0635] A7/ON — gap_mining.check_method   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-492", "attempt_at": "PROBE-1913", "attempted_by_session": "PROBE-1914", "search_strategy_record": "PROBE-1915", "outcome": "closure_evidence_found", "check_method": null, "discoveries_logged": "PROBE-1916"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.check_method`
**Verdict:** `OK`

### [0636] A7/ON — gaps.category   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-1917", "category": null, "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-1918", "created_at": "PROBE-1919", "created_by_session": "PROBE-1920", "updated_at": "PROBE-1921", "updated_by_session": "PROBE-1922"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.category`
**Verdict:** `OK`

### [0637] A7/ON — gaps.priority   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-1923", "category": "RP", "priority": null, "status": "OPEN-PROBE", "description": "PROBE-1924", "created_at": "PROBE-1925", "created_by_session": "PROBE-1926", "updated_at": "PROBE-1927", "updated_by_session": "PROBE-1928"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.priority`
**Verdict:** `OK`

### [0638] A7/ON — gaps.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-1929", "category": "RP", "priority": "P1", "status": null, "description": "PROBE-1930", "created_at": "PROBE-1931", "created_by_session": "PROBE-1932", "updated_at": "PROBE-1933", "updated_by_session": "PROBE-1934"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.status`
**Verdict:** `OK`

### [0639] A7/ON — gaps.description   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-1935", "category": "RP", "priority": "P1", "status": "OPEN-PROBE", "description": null, "created_at": "PROBE-1936", "created_by_session": "PROBE-1937", "updated_at": "PROBE-1938", "updated_by_session": "PROBE-1939"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.description`
**Verdict:** `OK`

### [0640] A7/ON — gaps.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-1940", "category": "RP", "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-1941", "created_at": null, "created_by_session": "PROBE-1942", "updated_at": "PROBE-1943", "updated_by_session": "PROBE-1944"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.created_at`
**Verdict:** `OK`

### [0641] A7/ON — gaps.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-1945", "category": "RP", "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-1946", "created_at": "PROBE-1947", "created_by_session": null, "updated_at": "PROBE-1948", "updated_by_session": "PROBE-1949"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.created_by_session`
**Verdict:** `OK`

### [0642] A7/ON — gaps.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-1950", "category": "RP", "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-1951", "created_at": "PROBE-1952", "created_by_session": "PROBE-1953", "updated_at": null, "updated_by_session": "PROBE-1954"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.updated_at`
**Verdict:** `OK`

### [0643] A7/ON — gaps.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-1955", "category": "RP", "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-1956", "created_at": "PROBE-1957", "created_by_session": "PROBE-1958", "updated_at": "PROBE-1959", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.updated_by_session`
**Verdict:** `OK`

### [0644] A7/ON — item_audit_runs.item_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-1960", "item_code": null, "session": "PROBE-1961", "created_at": "PROBE-1962", "created_by_session": "PROBE-1963", "updated_at": "PROBE-1964", "updated_by_session": "PROBE-1965"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.item_code`
**Verdict:** `OK`

### [0645] A7/ON — item_audit_runs.session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-1966", "item_code": "A-01", "session": null, "created_at": "PROBE-1967", "created_by_session": "PROBE-1968", "updated_at": "PROBE-1969", "updated_by_session": "PROBE-1970"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.session`
**Verdict:** `OK`

### [0646] A7/ON — item_audit_runs.steps_complete   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session", "steps_complete") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-1971", "item_code": "A-01", "session": "PROBE-1972", "created_at": "PROBE-1973", "created_by_session": "PROBE-1974", "updated_at": "PROBE-1975", "updated_by_session": "PROBE-1976", "steps_complete": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.steps_complete`
**Verdict:** `OK`

### [0647] A7/ON — item_audit_runs.steps_started   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session", "steps_started") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-1977", "item_code": "A-01", "session": "PROBE-1978", "created_at": "PROBE-1979", "created_by_session": "PROBE-1980", "updated_at": "PROBE-1981", "updated_by_session": "PROBE-1982", "steps_started": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.steps_started`
**Verdict:** `OK`

### [0648] A7/ON — item_audit_runs.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-1983", "item_code": "A-01", "session": "PROBE-1984", "created_at": "PROBE-1985", "created_by_session": "PROBE-1986", "updated_at": "PROBE-1987", "updated_by_session": "PROBE-1988", "status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.status`
**Verdict:** `OK`

### [0649] A7/ON — item_audit_runs.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-1989", "item_code": "A-01", "session": "PROBE-1990", "created_at": null, "created_by_session": "PROBE-1991", "updated_at": "PROBE-1992", "updated_by_session": "PROBE-1993"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.created_at`
**Verdict:** `OK`

### [0650] A7/ON — item_audit_runs.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-1994", "item_code": "A-01", "session": "PROBE-1995", "created_at": "PROBE-1996", "created_by_session": null, "updated_at": "PROBE-1997", "updated_by_session": "PROBE-1998"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.created_by_session`
**Verdict:** `OK`

### [0651] A7/ON — item_audit_runs.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-1999", "item_code": "A-01", "session": "PROBE-2000", "created_at": "PROBE-2001", "created_by_session": "PROBE-2002", "updated_at": null, "updated_by_session": "PROBE-2003"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.updated_at`
**Verdict:** `OK`

### [0652] A7/ON — item_audit_runs.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-2004", "item_code": "A-01", "session": "PROBE-2005", "created_at": "PROBE-2006", "created_by_session": "PROBE-2007", "updated_at": "PROBE-2008", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.updated_by_session`
**Verdict:** `OK`

### [0653] A7/ON — item_bpc_links.link_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_bpc_links" ("item_code", "slug", "link_type", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?)  -- {"item_code": "A-01", "slug": "PROBE-PK-158", "link_type": null, "created_at": "PROBE-2009", "created_by_session": "PROBE-2010"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_bpc_links.link_type`
**Verdict:** `OK`

### [0654] A7/ON — item_bpc_links.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_bpc_links" ("item_code", "slug", "link_type", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?)  -- {"item_code": "A-01", "slug": "PROBE-PK-158", "link_type": "primary", "created_at": null, "created_by_session": "PROBE-2011"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_bpc_links.created_at`
**Verdict:** `OK`

### [0655] A7/ON — item_bpc_links.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_bpc_links" ("item_code", "slug", "link_type", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?)  -- {"item_code": "A-01", "slug": "PROBE-PK-158", "link_type": "primary", "created_at": "PROBE-2012", "created_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_bpc_links.created_by_session`
**Verdict:** `OK`

### [0656] A7/ON — item_population_elaborations.item_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("item_code", "population_code") VALUES (?, ?)  -- {"item_code": null, "population_code": "ADHD"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_population_elaborations.item_code`
**Verdict:** `OK`

### [0657] A7/ON — item_population_elaborations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("item_code", "population_code") VALUES (?, ?)  -- {"item_code": "A-01", "population_code": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_population_elaborations.population_code`
**Verdict:** `OK`

### [0658] A7/ON — item_population_links.applicability   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "item_population_links" ("item_code", "population_code", "subtype", "applicability") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "subtype": "PROBE-2013", "applicability": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_population_links.applicability`
**Verdict:** `OK`

### [0659] A7/ON — items.category   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-2014", "category": null, "name": "PROBE-2015", "created_at": "PROBE-2016", "created_by_session": "PROBE-2017", "updated_at": "PROBE-2018", "updated_by_session": "PROBE-2019"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.category`
**Verdict:** `OK`

### [0660] A7/ON — items.name   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-2020", "category": "A", "name": null, "created_at": "PROBE-2021", "created_by_session": "PROBE-2022", "updated_at": "PROBE-2023", "updated_by_session": "PROBE-2024"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.name`
**Verdict:** `OK`

### [0661] A7/ON — items.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-2025", "category": "A", "name": "PROBE-2026", "created_at": "PROBE-2027", "created_by_session": "PROBE-2028", "updated_at": "PROBE-2029", "updated_by_session": "PROBE-2030", "status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.status`
**Verdict:** `OK`

### [0662] A7/ON — items.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-2031", "category": "A", "name": "PROBE-2032", "created_at": null, "created_by_session": "PROBE-2033", "updated_at": "PROBE-2034", "updated_by_session": "PROBE-2035"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.created_at`
**Verdict:** `OK`

### [0663] A7/ON — items.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-2036", "category": "A", "name": "PROBE-2037", "created_at": "PROBE-2038", "created_by_session": null, "updated_at": "PROBE-2039", "updated_by_session": "PROBE-2040"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.created_by_session`
**Verdict:** `OK`

### [0664] A7/ON — items.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-2041", "category": "A", "name": "PROBE-2042", "created_at": "PROBE-2043", "created_by_session": "PROBE-2044", "updated_at": null, "updated_by_session": "PROBE-2045"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.updated_at`
**Verdict:** `OK`

### [0665] A7/ON — items.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-2046", "category": "A", "name": "PROBE-2047", "created_at": "PROBE-2048", "created_by_session": "PROBE-2049", "updated_at": "PROBE-2050", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.updated_by_session`
**Verdict:** `OK`

### [0666] A7/ON — jurisdictional_values.item_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "jurisdictional_values" ("item_code", "jurisdiction") VALUES (?, ?)  -- {"item_code": null, "jurisdiction": "PROBE-2051"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: jurisdictional_values.item_code`
**Verdict:** `OK`

### [0667] A7/ON — jurisdictional_values.jurisdiction   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "jurisdictional_values" ("item_code", "jurisdiction") VALUES (?, ?)  -- {"item_code": "A-01", "jurisdiction": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: jurisdictional_values.jurisdiction`
**Verdict:** `OK`

### [0668] A7/ON — jurisdictional_values.evidence_tier   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "jurisdictional_values" ("item_code", "jurisdiction", "evidence_tier") VALUES (?, ?, ?)  -- {"item_code": "A-01", "jurisdiction": "PROBE-2052", "evidence_tier": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: jurisdictional_values.evidence_tier`
**Verdict:** `OK`

### [0669] A7/ON — lang_jur_map.role   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "lang_jur_map" ("language", "jurisdiction", "role") VALUES (?, ?, ?)  -- {"language": "PROBE-2053", "jurisdiction": "PROBE-2054", "role": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: lang_jur_map.role`
**Verdict:** `OK`

### [0670] A7/ON — life_stage_modifiers.label   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "life_stage_modifiers" ("label", "code", "definition") VALUES (?, ?, ?)  -- {"label": null, "code": "PROBE-PK-2055", "definition": "PROBE-DEFINITION"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: life_stage_modifiers.label`
**Verdict:** `OK`

### [0671] A7/ON — life_stage_modifiers.definition   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "life_stage_modifiers" ("definition", "code", "label") VALUES (?, ?, ?)  -- {"definition": null, "code": "PROBE-PK-2056", "label": "PROBE-LABEL"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: life_stage_modifiers.definition`
**Verdict:** `OK`

### [0672] A7/ON — pipeline_runs.started_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "pipeline_runs" ("run_id", "started_at") VALUES (?, ?)  -- {"run_id": "PROBE-2058", "started_at": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: pipeline_runs.started_at`
**Verdict:** `OK`

### [0673] A7/ON — population_axis_map.role   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "population_axis_map" ("population_code", "axis_code", "role") VALUES (?, ?, ?)  -- {"population_code": "ADHD", "axis_code": "AX-AMB", "role": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: population_axis_map.role`
**Verdict:** `OK`

### [0674] A7/ON — population_reclass.row_kind   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale") VALUES (?, ?, ?, ?)  -- {"population_code": "PROBE-2059", "row_kind": null, "layer": "AXIS-ALIAS", "rationale": "PROBE-2060"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: population_reclass.row_kind`
**Verdict:** `OK`

### [0675] A7/ON — population_reclass.layer   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale") VALUES (?, ?, ?, ?)  -- {"population_code": "PROBE-2061", "row_kind": "EXISTING-POP", "layer": null, "rationale": "PROBE-2062"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: population_reclass.layer`
**Verdict:** `OK`

### [0676] A7/ON — population_reclass.rationale   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale") VALUES (?, ?, ?, ?)  -- {"population_code": "PROBE-2063", "row_kind": "EXISTING-POP", "layer": "AXIS-ALIAS", "rationale": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: population_reclass.rationale`
**Verdict:** `OK`

### [0677] A7/ON — populations.display_name   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "populations" ("population_code", "display_name") VALUES (?, ?)  -- {"population_code": "PROBE-2064", "display_name": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: populations.display_name`
**Verdict:** `OK`

### [0678] A7/ON — reasoning_doc_citations.reasoning_doc_slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-2065", "reasoning_doc_slug": null, "parameter": "PROBE-2066", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-167", "verified_at": "PROBE-2067", "verified_by_session": "PROBE-2068", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-2069", "claim_text": "PROBE-2070"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.reasoning_doc_slug`
**Verdict:** `OK`

### [0679] A7/ON — reasoning_doc_citations.parameter   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-2071", "reasoning_doc_slug": "PROBE-PK-158", "parameter": null, "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-167", "verified_at": "PROBE-2072", "verified_by_session": "PROBE-2073", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-2074", "claim_text": "PROBE-2075"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.parameter`
**Verdict:** `OK`

### [0680] A7/ON — reasoning_doc_citations.claim_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-2076", "reasoning_doc_slug": "PROBE-PK-158", "parameter": "PROBE-2077", "claim_type": null, "source_ref_id": "PROBE-PK-167", "verified_at": "PROBE-2078", "verified_by_session": "PROBE-2079", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-2080", "claim_text": "PROBE-2081"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.claim_type`
**Verdict:** `OK`

### [0681] A7/ON — reasoning_doc_citations.source_ref_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-2082", "reasoning_doc_slug": "PROBE-PK-158", "parameter": "PROBE-2083", "claim_type": "numerical_spec", "source_ref_id": null, "verified_at": "PROBE-2084", "verified_by_session": "PROBE-2085", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-2086", "claim_text": "PROBE-2087"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.source_ref_id`
**Verdict:** `OK`

### [0682] A7/ON — reasoning_doc_citations.verified_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-2088", "reasoning_doc_slug": "PROBE-PK-158", "parameter": "PROBE-2089", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-167", "verified_at": null, "verified_by_session": "PROBE-2090", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-2091", "claim_text": "PROBE-2092"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.verified_at`
**Verdict:** `OK`

### [0683] A7/ON — reasoning_doc_citations.verified_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-2093", "reasoning_doc_slug": "PROBE-PK-158", "parameter": "PROBE-2094", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-167", "verified_at": "PROBE-2095", "verified_by_session": null, "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-2096", "claim_text": "PROBE-2097"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.verified_by_session`
**Verdict:** `OK`

### [0684] A7/ON — reasoning_doc_citations.paywall_purchase_candidate   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text", "paywall_purchase_candidate") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-2098", "reasoning_doc_slug": "PROBE-PK-158", "parameter": "PROBE-2099", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-167", "verified_at": "PROBE-2100", "verified_by_session": "PROBE-2101", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-2102", "claim_text": "PROBE-2103", "paywall_purchase_candidate": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.paywall_purchase_candidate`
**Verdict:** `OK`

### [0685] A7/ON — room_items.applicability   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "room_items" ("room_code", "item_code", "applicability") VALUES (?, ?, ?)  -- {"room_code": "R-ASM", "item_code": "A-01", "applicability": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: room_items.applicability`
**Verdict:** `OK`

### [0686] A7/ON — rooms.name   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "rooms" ("room_code", "name") VALUES (?, ?)  -- {"room_code": "PROBE-2104", "name": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: rooms.name`
**Verdict:** `OK`

### [0687] A7/ON — rooms.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "rooms" ("room_code", "name", "status") VALUES (?, ?, ?)  -- {"room_code": "PROBE-2105", "name": "PROBE-2106", "status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: rooms.status`
**Verdict:** `OK`

### [0688] A7/ON — search_candidates.found_under_slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": null, "disposition": "REHOME", "title": "PROBE-2107", "session": "PROBE-2108", "created_at": "PROBE-2109"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_candidates.found_under_slug`
**Verdict:** `OK`

### [0689] A7/ON — search_candidates.disposition   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": "aac-speech-production-environments", "disposition": null, "title": "PROBE-2110", "session": "PROBE-2111", "created_at": "PROBE-2112"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_candidates.disposition`
**Verdict:** `OK`

### [0690] A7/ON — search_candidates.title   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": null, "session": "PROBE-2113", "created_at": "PROBE-2114"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_candidates.title`
**Verdict:** `OK`

### [0691] A7/ON — search_candidates.harm_finding   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at", "harm_finding") VALUES (?, ?, ?, ?, ?, ?)  -- {"found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": "PROBE-2115", "session": "PROBE-2116", "created_at": "PROBE-2117", "harm_finding": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_candidates.harm_finding`
**Verdict:** `OK`

### [0692] A7/ON — search_candidates.session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": "PROBE-2118", "session": null, "created_at": "PROBE-2119"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_candidates.session`
**Verdict:** `OK`

### [0693] A7/ON — search_candidates.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": "aac-speech-production-environments", "disposition": "REHOME", "title": "PROBE-2120", "session": "PROBE-2121", "created_at": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_candidates.created_at`
**Verdict:** `OK`

### [0694] A7/ON — search_coverage.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "jurisdiction": "PROBE-2122", "status": null, "created_at": "PROBE-2123", "created_by_session": "PROBE-2124", "updated_at": "PROBE-2125", "updated_by_session": "PROBE-2126"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.status`
**Verdict:** `OK`

### [0695] A7/ON — search_coverage.co1_attempted   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "co1_attempted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "jurisdiction": "PROBE-2127", "status": "SEARCHED", "created_at": "PROBE-2128", "created_by_session": "PROBE-2129", "updated_at": "PROBE-2130", "updated_by_session": "PROBE-2131", "co1_attempted": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.co1_attempted`
**Verdict:** `OK`

### [0696] A7/ON — search_coverage.tier5_attempted   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "tier5_attempted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "jurisdiction": "PROBE-2132", "status": "SEARCHED", "created_at": "PROBE-2133", "created_by_session": "PROBE-2134", "updated_at": "PROBE-2135", "updated_by_session": "PROBE-2136", "tier5_attempted": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.tier5_attempted`
**Verdict:** `OK`

### [0697] A7/ON — search_coverage.tier6_attempted   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "tier6_attempted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "jurisdiction": "PROBE-2137", "status": "SEARCHED", "created_at": "PROBE-2138", "created_by_session": "PROBE-2139", "updated_at": "PROBE-2140", "updated_by_session": "PROBE-2141", "tier6_attempted": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.tier6_attempted`
**Verdict:** `OK`

### [0698] A7/ON — search_coverage.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "jurisdiction": "PROBE-2142", "status": "SEARCHED", "created_at": null, "created_by_session": "PROBE-2143", "updated_at": "PROBE-2144", "updated_by_session": "PROBE-2145"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.created_at`
**Verdict:** `OK`

### [0699] A7/ON — search_coverage.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "jurisdiction": "PROBE-2146", "status": "SEARCHED", "created_at": "PROBE-2147", "created_by_session": null, "updated_at": "PROBE-2148", "updated_by_session": "PROBE-2149"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.created_by_session`
**Verdict:** `OK`

### [0700] A7/ON — search_coverage.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "jurisdiction": "PROBE-2150", "status": "SEARCHED", "created_at": "PROBE-2151", "created_by_session": "PROBE-2152", "updated_at": null, "updated_by_session": "PROBE-2153"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.updated_at`
**Verdict:** `OK`

### [0701] A7/ON — search_coverage.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "jurisdiction": "PROBE-2154", "status": "SEARCHED", "created_at": "PROBE-2155", "created_by_session": "PROBE-2156", "updated_at": "PROBE-2157", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.updated_by_session`
**Verdict:** `OK`

### [0702] A7/ON — search_executions.slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": null, "language": "PROBE-2158", "query_text": "PROBE-2159", "engine": "PROBE-2160", "depth_method": "scoping", "session": "PROBE-2161", "executed_at": "PROBE-2162"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.slug`
**Verdict:** `OK`

### [0703] A7/ON — search_executions.language   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": null, "query_text": "PROBE-2163", "engine": "PROBE-2164", "depth_method": "scoping", "session": "PROBE-2165", "executed_at": "PROBE-2166"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.language`
**Verdict:** `OK`

### [0704] A7/ON — search_executions.query_text   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2167", "query_text": null, "engine": "PROBE-2168", "depth_method": "scoping", "session": "PROBE-2169", "executed_at": "PROBE-2170"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.query_text`
**Verdict:** `OK`

### [0705] A7/ON — search_executions.engine   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2171", "query_text": "PROBE-2172", "engine": null, "depth_method": "scoping", "session": "PROBE-2173", "executed_at": "PROBE-2174"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.engine`
**Verdict:** `OK`

### [0706] A7/ON — search_executions.depth_method   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2175", "query_text": "PROBE-2176", "engine": "PROBE-2177", "depth_method": null, "session": "PROBE-2178", "executed_at": "PROBE-2179"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.depth_method`
**Verdict:** `OK`

### [0707] A7/ON — search_executions.results_found   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "results_found") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2180", "query_text": "PROBE-2181", "engine": "PROBE-2182", "depth_method": "scoping", "session": "PROBE-2183", "executed_at": "PROBE-2184", "results_found": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.results_found`
**Verdict:** `OK`

### [0708] A7/ON — search_executions.results_screened   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "results_screened") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2185", "query_text": "PROBE-2186", "engine": "PROBE-2187", "depth_method": "scoping", "session": "PROBE-2188", "executed_at": "PROBE-2189", "results_screened": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.results_screened`
**Verdict:** `OK`

### [0709] A7/ON — search_executions.results_admitted   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "results_admitted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2190", "query_text": "PROBE-2191", "engine": "PROBE-2192", "depth_method": "scoping", "session": "PROBE-2193", "executed_at": "PROBE-2194", "results_admitted": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.results_admitted`
**Verdict:** `OK`

### [0710] A7/ON — search_executions.backfill   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "backfill") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2195", "query_text": "PROBE-2196", "engine": "PROBE-2197", "depth_method": "scoping", "session": "PROBE-2198", "executed_at": "PROBE-2199", "backfill": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.backfill`
**Verdict:** `OK`

### [0711] A7/ON — search_executions.session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2200", "query_text": "PROBE-2201", "engine": "PROBE-2202", "depth_method": "scoping", "session": null, "executed_at": "PROBE-2203"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.session`
**Verdict:** `OK`

### [0712] A7/ON — search_executions.executed_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2204", "query_text": "PROBE-2205", "engine": "PROBE-2206", "depth_method": "scoping", "session": "PROBE-2207", "executed_at": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.executed_at`
**Verdict:** `OK`

### [0713] A7/ON — search_executions.harm_finding   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "harm_finding") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2208", "query_text": "PROBE-2209", "engine": "PROBE-2210", "depth_method": "scoping", "session": "PROBE-2211", "executed_at": "PROBE-2212", "harm_finding": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.harm_finding`
**Verdict:** `OK`

### [0714] A7/ON — search_languages.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2213", "status": null, "created_at": "PROBE-2214", "created_by_session": "PROBE-2215", "updated_at": "PROBE-2216", "updated_by_session": "PROBE-2217"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_languages.status`
**Verdict:** `OK`

### [0715] A7/ON — search_languages.results_count   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "results_count") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2218", "status": "SEARCHED", "created_at": "PROBE-2219", "created_by_session": "PROBE-2220", "updated_at": "PROBE-2221", "updated_by_session": "PROBE-2222", "results_count": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_languages.results_count`
**Verdict:** `OK`

### [0716] A7/ON — search_languages.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2223", "status": "SEARCHED", "created_at": null, "created_by_session": "PROBE-2224", "updated_at": "PROBE-2225", "updated_by_session": "PROBE-2226"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_languages.created_at`
**Verdict:** `OK`

### [0717] A7/ON — search_languages.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2227", "status": "SEARCHED", "created_at": "PROBE-2228", "created_by_session": null, "updated_at": "PROBE-2229", "updated_by_session": "PROBE-2230"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_languages.created_by_session`
**Verdict:** `OK`

### [0718] A7/ON — search_languages.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2231", "status": "SEARCHED", "created_at": "PROBE-2232", "created_by_session": "PROBE-2233", "updated_at": null, "updated_by_session": "PROBE-2234"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_languages.updated_at`
**Verdict:** `OK`

### [0719] A7/ON — search_languages.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-158", "language": "PROBE-2235", "status": "SEARCHED", "created_at": "PROBE-2236", "created_by_session": "PROBE-2237", "updated_at": "PROBE-2238", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_languages.updated_by_session`
**Verdict:** `OK`

### [0720] A7/ON — situations.title   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "situations" ("situation_id", "title", "account_language", "account_text_ref") VALUES (?, ?, ?, ?)  -- {"situation_id": "PROBE-2239", "title": null, "account_language": "PROBE-2240", "account_text_ref": "PROBE-2241"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: situations.title`
**Verdict:** `OK`

### [0721] A7/ON — situations.account_language   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "situations" ("situation_id", "title", "account_language", "account_text_ref") VALUES (?, ?, ?, ?)  -- {"situation_id": "PROBE-2242", "title": "PROBE-2243", "account_language": null, "account_text_ref": "PROBE-2244"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: situations.account_language`
**Verdict:** `OK`

### [0722] A7/ON — situations.account_text_ref   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "situations" ("situation_id", "title", "account_language", "account_text_ref") VALUES (?, ?, ?, ?)  -- {"situation_id": "PROBE-2245", "title": "PROBE-2246", "account_language": "PROBE-2247", "account_text_ref": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: situations.account_text_ref`
**Verdict:** `OK`

### [0723] A7/ON — slugs.topic_directory   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-2248", "topic_directory": null, "sl_path": "PROBE-2249", "bpc_path": "PROBE-2250", "status": "ACTIVE", "created_at": "PROBE-2251", "created_by_session": "PROBE-2252", "updated_at": "PROBE-2253", "updated_by_session": "PROBE-2254"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.topic_directory`
**Verdict:** `OK`

### [0724] A7/ON — slugs.sl_path   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-2255", "topic_directory": "PROBE-2256", "sl_path": null, "bpc_path": "PROBE-2257", "status": "ACTIVE", "created_at": "PROBE-2258", "created_by_session": "PROBE-2259", "updated_at": "PROBE-2260", "updated_by_session": "PROBE-2261"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.sl_path`
**Verdict:** `OK`

### [0725] A7/ON — slugs.bpc_path   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-2262", "topic_directory": "PROBE-2263", "sl_path": "PROBE-2264", "bpc_path": null, "status": "ACTIVE", "created_at": "PROBE-2265", "created_by_session": "PROBE-2266", "updated_at": "PROBE-2267", "updated_by_session": "PROBE-2268"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.bpc_path`
**Verdict:** `OK`

### [0726] A7/ON — slugs.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-2269", "topic_directory": "PROBE-2270", "sl_path": "PROBE-2271", "bpc_path": "PROBE-2272", "status": null, "created_at": "PROBE-2273", "created_by_session": "PROBE-2274", "updated_at": "PROBE-2275", "updated_by_session": "PROBE-2276"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.status`
**Verdict:** `OK`

### [0727] A7/ON — slugs.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-2277", "topic_directory": "PROBE-2278", "sl_path": "PROBE-2279", "bpc_path": "PROBE-2280", "status": "ACTIVE", "created_at": null, "created_by_session": "PROBE-2281", "updated_at": "PROBE-2282", "updated_by_session": "PROBE-2283"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.created_at`
**Verdict:** `OK`

### [0728] A7/ON — slugs.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-2284", "topic_directory": "PROBE-2285", "sl_path": "PROBE-2286", "bpc_path": "PROBE-2287", "status": "ACTIVE", "created_at": "PROBE-2288", "created_by_session": null, "updated_at": "PROBE-2289", "updated_by_session": "PROBE-2290"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.created_by_session`
**Verdict:** `OK`

### [0729] A7/ON — slugs.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-2291", "topic_directory": "PROBE-2292", "sl_path": "PROBE-2293", "bpc_path": "PROBE-2294", "status": "ACTIVE", "created_at": "PROBE-2295", "created_by_session": "PROBE-2296", "updated_at": null, "updated_by_session": "PROBE-2297"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.updated_at`
**Verdict:** `OK`

### [0730] A7/ON — slugs.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-2298", "topic_directory": "PROBE-2299", "sl_path": "PROBE-2300", "bpc_path": "PROBE-2301", "status": "ACTIVE", "created_at": "PROBE-2302", "created_by_session": "PROBE-2303", "updated_at": "PROBE-2304", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.updated_by_session`
**Verdict:** `OK`

### [0731] A7/ON — source_locators.recovered_from   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_locators" ("ref_id", "pmcid", "pmid", "url", "standard_number", "doi", "isbn", "issn", "recovered_from") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-2305", "pmcid": "PROBE-2306", "pmid": "PROBE-2307", "url": "PROBE-2308", "standard_number": "PROBE-2309", "doi": "PROBE-2310", "isbn": "PROBE-2311", "issn": "PROBE-2312", "recovered_from": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_locators.recovered_from`
**Verdict:** `OK`

### [0732] A7/ON — source_slug_links.local_ref_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "local_ref_id": null, "created_at": "PROBE-2313", "created_by_session": "PROBE-2314", "updated_at": "PROBE-2315", "updated_by_session": "PROBE-2316"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_slug_links.local_ref_id`
**Verdict:** `OK`

### [0733] A7/ON — source_slug_links.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2317", "created_at": null, "created_by_session": "PROBE-2318", "updated_at": "PROBE-2319", "updated_by_session": "PROBE-2320"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_slug_links.created_at`
**Verdict:** `OK`

### [0734] A7/ON — source_slug_links.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2321", "created_at": "PROBE-2322", "created_by_session": null, "updated_at": "PROBE-2323", "updated_by_session": "PROBE-2324"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_slug_links.created_by_session`
**Verdict:** `OK`

### [0735] A7/ON — source_slug_links.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2325", "created_at": "PROBE-2326", "created_by_session": "PROBE-2327", "updated_at": null, "updated_by_session": "PROBE-2328"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_slug_links.updated_at`
**Verdict:** `OK`

### [0736] A7/ON — source_slug_links.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2329", "created_at": "PROBE-2330", "created_by_session": "PROBE-2331", "updated_at": "PROBE-2332", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_slug_links.updated_by_session`
**Verdict:** `OK`

### [0737] A7/ON — source_value_extractions.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": null, "slug": "PROBE-PK-158", "parameter": "PROBE-2333", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-2334", "updated_at": "PROBE-2335", "claimed_value": "PROBE-2336"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.ref_id`
**Verdict:** `OK`

### [0738] A7/ON — source_value_extractions.slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": null, "parameter": "PROBE-2337", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-2338", "updated_at": "PROBE-2339", "claimed_value": "PROBE-2340"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.slug`
**Verdict:** `OK`

### [0739] A7/ON — source_value_extractions.parameter   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": null, "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-2341", "updated_at": "PROBE-2342", "claimed_value": "PROBE-2343"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.parameter`
**Verdict:** `OK`

### [0740] A7/ON — source_value_extractions.claim_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-2344", "claim_type": null, "extraction_method": "skim", "created_at": "PROBE-2345", "updated_at": "PROBE-2346", "claimed_value": "PROBE-2347"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.claim_type`
**Verdict:** `OK`

### [0741] A7/ON — source_value_extractions.extraction_method   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-2348", "claim_type": "numerical", "extraction_method": null, "created_at": "PROBE-2349", "updated_at": "PROBE-2350", "claimed_value": "PROBE-2351"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.extraction_method`
**Verdict:** `OK`

### [0742] A7/ON — source_value_extractions.extraction_status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "extraction_status") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-2352", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-2353", "updated_at": "PROBE-2354", "claimed_value": "PROBE-2355", "extraction_status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.extraction_status`
**Verdict:** `OK`

### [0743] A7/ON — source_value_extractions.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-2356", "claim_type": "numerical", "extraction_method": "skim", "created_at": null, "updated_at": "PROBE-2357", "claimed_value": "PROBE-2358"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.created_at`
**Verdict:** `OK`

### [0744] A7/ON — source_value_extractions.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-2359", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-2360", "updated_at": null, "claimed_value": "PROBE-2361"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.updated_at`
**Verdict:** `OK`

### [0745] A7/ON — source_value_extractions.contested   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "contested") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "slug": "PROBE-PK-158", "parameter": "PROBE-2362", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-2363", "updated_at": "PROBE-2364", "claimed_value": "PROBE-2365", "contested": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.contested`
**Verdict:** `OK`

### [0746] A7/ON — spec_value_probes.walk_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2366", "walk_id": null, "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-2367", "direction": "up", "population": "PROBE-2368", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-2369", "created_at": "PROBE-2370", "created_by_session": "PROBE-2371"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.walk_id`
**Verdict:** `OK`

### [0747] A7/ON — spec_value_probes.slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2372", "walk_id": "PROBE-2373", "slug": null, "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-2374", "direction": "up", "population": "PROBE-2375", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-2376", "created_at": "PROBE-2377", "created_by_session": "PROBE-2378"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.slug`
**Verdict:** `OK`

### [0748] A7/ON — spec_value_probes.item_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2379", "walk_id": "PROBE-2380", "slug": "PROBE-PK-158", "item_code": null, "spec_value_origin": 1.0, "spec_unit": "PROBE-2381", "direction": "up", "population": "PROBE-2382", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-2383", "created_at": "PROBE-2384", "created_by_session": "PROBE-2385"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.item_code`
**Verdict:** `OK`

### [0749] A7/ON — spec_value_probes.spec_value_origin   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2386", "walk_id": "PROBE-2387", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": null, "spec_unit": "PROBE-2388", "direction": "up", "population": "PROBE-2389", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-2390", "created_at": "PROBE-2391", "created_by_session": "PROBE-2392"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.spec_value_origin`
**Verdict:** `OK`

### [0750] A7/ON — spec_value_probes.spec_unit   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2393", "walk_id": "PROBE-2394", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": null, "direction": "up", "population": "PROBE-2395", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-2396", "created_at": "PROBE-2397", "created_by_session": "PROBE-2398"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.spec_unit`
**Verdict:** `OK`

### [0751] A7/ON — spec_value_probes.direction   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2399", "walk_id": "PROBE-2400", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-2401", "direction": null, "population": "PROBE-2402", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-2403", "created_at": "PROBE-2404", "created_by_session": "PROBE-2405"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.direction`
**Verdict:** `OK`

### [0752] A7/ON — spec_value_probes.population   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2406", "walk_id": "PROBE-2407", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-2408", "direction": "up", "population": null, "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-2409", "created_at": "PROBE-2410", "created_by_session": "PROBE-2411"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.population`
**Verdict:** `OK`

### [0753] A7/ON — spec_value_probes.claim_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2412", "walk_id": "PROBE-2413", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-2414", "direction": "up", "population": "PROBE-2415", "claim_type": null, "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-2416", "created_at": "PROBE-2417", "created_by_session": "PROBE-2418"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.claim_type`
**Verdict:** `OK`

### [0754] A7/ON — spec_value_probes.step_index   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2419", "walk_id": "PROBE-2420", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-2421", "direction": "up", "population": "PROBE-2422", "claim_type": "minimum", "step_index": null, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-2423", "created_at": "PROBE-2424", "created_by_session": "PROBE-2425"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.step_index`
**Verdict:** `OK`

### [0755] A7/ON — spec_value_probes.phase   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2426", "walk_id": "PROBE-2427", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-2428", "direction": "up", "population": "PROBE-2429", "claim_type": "minimum", "step_index": 1, "phase": null, "step_value": 1.0, "step_value_unit": "PROBE-2430", "created_at": "PROBE-2431", "created_by_session": "PROBE-2432"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.phase`
**Verdict:** `OK`

### [0756] A7/ON — spec_value_probes.step_value   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2433", "walk_id": "PROBE-2434", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-2435", "direction": "up", "population": "PROBE-2436", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": null, "step_value_unit": "PROBE-2437", "created_at": "PROBE-2438", "created_by_session": "PROBE-2439"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.step_value`
**Verdict:** `OK`

### [0757] A7/ON — spec_value_probes.step_value_unit   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2440", "walk_id": "PROBE-2441", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-2442", "direction": "up", "population": "PROBE-2443", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": null, "created_at": "PROBE-2444", "created_by_session": "PROBE-2445"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.step_value_unit`
**Verdict:** `OK`

### [0758] A7/ON — spec_value_probes.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2446", "walk_id": "PROBE-2447", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-2448", "direction": "up", "population": "PROBE-2449", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-2450", "created_at": null, "created_by_session": "PROBE-2451"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.created_at`
**Verdict:** `OK`

### [0759] A7/ON — spec_value_probes.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-2452", "walk_id": "PROBE-2453", "slug": "PROBE-PK-158", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-2454", "direction": "up", "population": "PROBE-2455", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-2456", "created_at": "PROBE-2457", "created_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.created_by_session`
**Verdict:** `OK`

### [0760] A7/ON — specification_source_links.role   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "specification_source_links" ("ref_id", "specification_id", "role") VALUES (?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "specification_id": 1, "role": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specification_source_links.role`
**Verdict:** `OK`

### [0761] A7/ON — specifications.item_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state") VALUES (?, ?, ?)  -- {"item_code": null, "population_code": "ADHD", "state": "stated"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.item_code`
**Verdict:** `OK`

### [0762] A7/ON — specifications.population_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state") VALUES (?, ?, ?)  -- {"item_code": "A-01", "population_code": null, "state": "stated"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.population_code`
**Verdict:** `OK`

### [0763] A7/ON — specifications.state   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state") VALUES (?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.state`
**Verdict:** `OK`

### [0764] A7/ON — specifications.code_floor_only   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "code_floor_only") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": "stated", "code_floor_only": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.code_floor_only`
**Verdict:** `OK`

### [0765] A7/ON — specifications.has_unverified_sources   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "has_unverified_sources") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": "stated", "has_unverified_sources": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.has_unverified_sources`
**Verdict:** `OK`

### [0766] A7/ON — specifications.all_sources_disqualified   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "all_sources_disqualified") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": "stated", "all_sources_disqualified": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.all_sources_disqualified`
**Verdict:** `OK`

### [0767] A7/ON — specifications.regulatory_stratum_only   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "regulatory_stratum_only") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": "stated", "regulatory_stratum_only": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.regulatory_stratum_only`
**Verdict:** `OK`

### [0768] A7/ON — supersession_check.slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-2458", "slug": null, "local_ref_id": "PROBE-2459", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-2460", "outcome": "current_best", "search_strategy_record": "PROBE-2461", "checked_at": "PROBE-2462", "checked_by_session": "PROBE-2463", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.slug`
**Verdict:** `OK`

### [0769] A7/ON — supersession_check.local_ref_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-2464", "slug": "PROBE-PK-158", "local_ref_id": null, "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-2465", "outcome": "current_best", "search_strategy_record": "PROBE-2466", "checked_at": "PROBE-2467", "checked_by_session": "PROBE-2468", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.local_ref_id`
**Verdict:** `OK`

### [0770] A7/ON — supersession_check.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-2469", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2470", "ref_id": null, "anchor_tier": 1, "anchor_evidence_type": "PROBE-2471", "outcome": "current_best", "search_strategy_record": "PROBE-2472", "checked_at": "PROBE-2473", "checked_by_session": "PROBE-2474", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.ref_id`
**Verdict:** `OK`

### [0771] A7/ON — supersession_check.anchor_tier   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-2475", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2476", "ref_id": "PROBE-PK-167", "anchor_tier": null, "anchor_evidence_type": "PROBE-2477", "outcome": "current_best", "search_strategy_record": "PROBE-2478", "checked_at": "PROBE-2479", "checked_by_session": "PROBE-2480", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.anchor_tier`
**Verdict:** `OK`

### [0772] A7/ON — supersession_check.anchor_evidence_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-2481", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2482", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": null, "outcome": "current_best", "search_strategy_record": "PROBE-2483", "checked_at": "PROBE-2484", "checked_by_session": "PROBE-2485", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.anchor_evidence_type`
**Verdict:** `OK`

### [0773] A7/ON — supersession_check.outcome   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-2486", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2487", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-2488", "outcome": null, "search_strategy_record": "PROBE-2489", "checked_at": "PROBE-2490", "checked_by_session": "PROBE-2491", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.outcome`
**Verdict:** `OK`

### [0774] A7/ON — supersession_check.search_strategy_record   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-2492", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2493", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-2494", "outcome": "current_best", "search_strategy_record": null, "checked_at": "PROBE-2495", "checked_by_session": "PROBE-2496", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.search_strategy_record`
**Verdict:** `OK`

### [0775] A7/ON — supersession_check.candidates_returned   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method", "candidates_returned") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-2497", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2498", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-2499", "outcome": "current_best", "search_strategy_record": "PROBE-2500", "checked_at": "PROBE-2501", "checked_by_session": "PROBE-2502", "check_method": "pubmed_search", "candidates_returned": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.candidates_returned`
**Verdict:** `OK`

### [0776] A7/ON — supersession_check.candidates_reviewed   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method", "candidates_reviewed") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-2503", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2504", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-2505", "outcome": "current_best", "search_strategy_record": "PROBE-2506", "checked_at": "PROBE-2507", "checked_by_session": "PROBE-2508", "check_method": "pubmed_search", "candidates_reviewed": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.candidates_reviewed`
**Verdict:** `OK`

### [0777] A7/ON — supersession_check.checked_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-2509", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2510", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-2511", "outcome": "current_best", "search_strategy_record": "PROBE-2512", "checked_at": null, "checked_by_session": "PROBE-2513", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.checked_at`
**Verdict:** `OK`

### [0778] A7/ON — supersession_check.checked_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-2514", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2515", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-2516", "outcome": "current_best", "search_strategy_record": "PROBE-2517", "checked_at": "PROBE-2518", "checked_by_session": null, "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.checked_by_session`
**Verdict:** `OK`

### [0779] A7/ON — supersession_check.check_method   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-2519", "slug": "PROBE-PK-158", "local_ref_id": "PROBE-2520", "ref_id": "PROBE-PK-167", "anchor_tier": 1, "anchor_evidence_type": "PROBE-2521", "outcome": "current_best", "search_strategy_record": "PROBE-2522", "checked_at": "PROBE-2523", "checked_by_session": "PROBE-2524", "check_method": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.check_method`
**Verdict:** `OK`

### [0780] A7/ON — term_aliases.alias_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "alias": "PROBE-2525", "language": "PROBE-2526", "alias_type": null, "created_at": "PROBE-2527", "created_by_session": "PROBE-2528", "updated_at": "PROBE-2529", "updated_by_session": "PROBE-2530"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_aliases.alias_type`
**Verdict:** `OK`

### [0781] A7/ON — term_aliases.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "alias": "PROBE-2531", "language": "PROBE-2532", "alias_type": "SYNONYM", "created_at": null, "created_by_session": "PROBE-2533", "updated_at": "PROBE-2534", "updated_by_session": "PROBE-2535"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_aliases.created_at`
**Verdict:** `OK`

### [0782] A7/ON — term_aliases.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "alias": "PROBE-2536", "language": "PROBE-2537", "alias_type": "SYNONYM", "created_at": "PROBE-2538", "created_by_session": null, "updated_at": "PROBE-2539", "updated_by_session": "PROBE-2540"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_aliases.created_by_session`
**Verdict:** `OK`

### [0783] A7/ON — term_aliases.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "alias": "PROBE-2541", "language": "PROBE-2542", "alias_type": "SYNONYM", "created_at": "PROBE-2543", "created_by_session": "PROBE-2544", "updated_at": null, "updated_by_session": "PROBE-2545"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_aliases.updated_at`
**Verdict:** `OK`

### [0784] A7/ON — term_aliases.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "alias": "PROBE-2546", "language": "PROBE-2547", "alias_type": "SYNONYM", "created_at": "PROBE-2548", "created_by_session": "PROBE-2549", "updated_at": "PROBE-2550", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_aliases.updated_by_session`
**Verdict:** `OK`

### [0785] A7/ON — term_item_links.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "term_item_links" ("term_id", "item_code", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "item_code": "A-01", "created_at": null, "created_by_session": "PROBE-2551", "updated_at": "PROBE-2552", "updated_by_session": "PROBE-2553"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_item_links.created_at`
**Verdict:** `OK`

### [0786] A7/ON — term_item_links.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "term_item_links" ("term_id", "item_code", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "item_code": "A-01", "created_at": "PROBE-2554", "created_by_session": null, "updated_at": "PROBE-2555", "updated_by_session": "PROBE-2556"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_item_links.created_by_session`
**Verdict:** `OK`

### [0787] A7/ON — term_item_links.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "term_item_links" ("term_id", "item_code", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "item_code": "A-01", "created_at": "PROBE-2557", "created_by_session": "PROBE-2558", "updated_at": null, "updated_by_session": "PROBE-2559"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_item_links.updated_at`
**Verdict:** `OK`

### [0788] A7/ON — term_item_links.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "term_item_links" ("term_id", "item_code", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "item_code": "A-01", "created_at": "PROBE-2560", "created_by_session": "PROBE-2561", "updated_at": "PROBE-2562", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_item_links.updated_by_session`
**Verdict:** `OK`

### [0789] A7/ON — terms.canonical_en   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "terms" ("term_id", "canonical_en", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-2564", "canonical_en": null, "created_at": "PROBE-2565", "created_by_session": "PROBE-2566", "updated_at": "PROBE-2567", "updated_by_session": "PROBE-2568"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: terms.canonical_en`
**Verdict:** `OK`

### [0790] A7/ON — terms.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "terms" ("term_id", "canonical_en", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-2569", "canonical_en": "PROBE-2570", "created_at": null, "created_by_session": "PROBE-2571", "updated_at": "PROBE-2572", "updated_by_session": "PROBE-2573"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: terms.created_at`
**Verdict:** `OK`

### [0791] A7/ON — terms.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "terms" ("term_id", "canonical_en", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-2574", "canonical_en": "PROBE-2575", "created_at": "PROBE-2576", "created_by_session": null, "updated_at": "PROBE-2577", "updated_by_session": "PROBE-2578"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: terms.created_by_session`
**Verdict:** `OK`

### [0792] A7/ON — terms.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "terms" ("term_id", "canonical_en", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-2579", "canonical_en": "PROBE-2580", "created_at": "PROBE-2581", "created_by_session": "PROBE-2582", "updated_at": null, "updated_by_session": "PROBE-2583"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: terms.updated_at`
**Verdict:** `OK`

### [0793] A7/ON — terms.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "terms" ("term_id", "canonical_en", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-2584", "canonical_en": "PROBE-2585", "created_at": "PROBE-2586", "created_by_session": "PROBE-2587", "updated_at": "PROBE-2588", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: terms.updated_by_session`
**Verdict:** `OK`

### [0794] A7/ON — url_verification_runs.started_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "url_verification_runs" ("run_id", "started_at") VALUES (?, ?)  -- {"run_id": "PROBE-2590", "started_at": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: url_verification_runs.started_at`
**Verdict:** `OK`

### [0795] A7/ON — weighting_profile.tier_weights   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=ON)
**SQL:**
```sql
INSERT INTO "weighting_profile" ("audience", "use_pattern", "tier_weights") VALUES (?, ?, ?)  -- {"audience": "PROBE-2591", "use_pattern": "PROBE-2592", "tier_weights": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: weighting_profile.tier_weights`
**Verdict:** `OK`

### [0796] A7/OFF — access_duration.definition   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "access_duration" ("definition", "code") VALUES (?, ?)  -- {"definition": null, "code": "PROBE-PK-2593"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_duration.definition`
**Verdict:** `OK`

### [0797] A7/OFF — access_need_axis_map.relationship   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "access_need_axis_map" ("need_code", "axis_code", "relationship") VALUES (?, ?, ?)  -- {"need_code": "A-AT", "axis_code": "AX-AMB", "relationship": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_need_axis_map.relationship`
**Verdict:** `OK`

### [0798] A7/OFF — access_need_icf.icf_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "access_need_icf" ("need_code", "icf_code", "icf_type", "confidence") VALUES (?, ?, ?, ?)  -- {"need_code": "A-AT", "icf_code": "PROBE-2594", "icf_type": null, "confidence": "confirmed"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_need_icf.icf_type`
**Verdict:** `OK`

### [0799] A7/OFF — access_need_icf.confidence   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "access_need_icf" ("need_code", "icf_code", "icf_type", "confidence") VALUES (?, ?, ?, ?)  -- {"need_code": "A-AT", "icf_code": "PROBE-2595", "icf_type": "b", "confidence": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_need_icf.confidence`
**Verdict:** `OK`

### [0800] A7/OFF — access_needs.family   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "access_needs" ("need_code", "family", "design_obligation") VALUES (?, ?, ?)  -- {"need_code": "PROBE-2596", "family": null, "design_obligation": "PROBE-2597"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_needs.family`
**Verdict:** `OK`

### [0801] A7/OFF — access_needs.design_obligation   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "access_needs" ("need_code", "family", "design_obligation") VALUES (?, ?, ?)  -- {"need_code": "PROBE-2598", "family": "perceiving", "design_obligation": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_needs.design_obligation`
**Verdict:** `OK`

### [0802] A7/OFF — access_needs.source_version   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "access_needs" ("need_code", "family", "design_obligation", "source_version") VALUES (?, ?, ?, ?)  -- {"need_code": "PROBE-2599", "family": "perceiving", "design_obligation": "PROBE-2600", "source_version": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_needs.source_version`
**Verdict:** `OK`

### [0803] A7/OFF — access_stakes.definition   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "access_stakes" ("definition", "code") VALUES (?, ?)  -- {"definition": null, "code": "PROBE-PK-2601"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: access_stakes.definition`
**Verdict:** `OK`

### [0804] A7/OFF — axes.name   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "axes" ("axis_code", "name", "mechanism", "coverage_status", "falsification_condition") VALUES (?, ?, ?, ?, ?)  -- {"axis_code": "PROBE-2602", "name": null, "mechanism": "PROBE-2603", "coverage_status": "ESTABLISHED", "falsification_condition": "PROBE-2604"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: axes.name`
**Verdict:** `OK`

### [0805] A7/OFF — axes.mechanism   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "axes" ("axis_code", "name", "mechanism", "coverage_status", "falsification_condition") VALUES (?, ?, ?, ?, ?)  -- {"axis_code": "PROBE-2605", "name": "PROBE-2606", "mechanism": null, "coverage_status": "ESTABLISHED", "falsification_condition": "PROBE-2607"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: axes.mechanism`
**Verdict:** `OK`

### [0806] A7/OFF — axes.coverage_status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "axes" ("axis_code", "name", "mechanism", "coverage_status", "falsification_condition") VALUES (?, ?, ?, ?, ?)  -- {"axis_code": "PROBE-2608", "name": "PROBE-2609", "mechanism": "PROBE-2610", "coverage_status": null, "falsification_condition": "PROBE-2611"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: axes.coverage_status`
**Verdict:** `OK`

### [0807] A7/OFF — axes.falsification_condition   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "axes" ("axis_code", "name", "mechanism", "coverage_status", "falsification_condition") VALUES (?, ?, ?, ?, ?)  -- {"axis_code": "PROBE-2612", "name": "PROBE-2613", "mechanism": "PROBE-2614", "coverage_status": "ESTABLISHED", "falsification_condition": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: axes.falsification_condition`
**Verdict:** `OK`

### [0808] A7/OFF — bpc_metadata.population   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": null, "created_at": "PROBE-2615", "created_by_session": "PROBE-2616", "updated_at": "PROBE-2617", "updated_by_session": "PROBE-2618"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.population`
**Verdict:** `OK`

### [0809] A7/OFF — bpc_metadata.pico_complete   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "pico_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-2619", "created_at": "PROBE-2620", "created_by_session": "PROBE-2621", "updated_at": "PROBE-2622", "updated_by_session": "PROBE-2623", "pico_complete": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.pico_complete`
**Verdict:** `OK`

### [0810] A7/OFF — bpc_metadata.search_complete   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "search_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-2624", "created_at": "PROBE-2625", "created_by_session": "PROBE-2626", "updated_at": "PROBE-2627", "updated_by_session": "PROBE-2628", "search_complete": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.search_complete`
**Verdict:** `OK`

### [0811] A7/OFF — bpc_metadata.bpc_complete   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "bpc_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-2629", "created_at": "PROBE-2630", "created_by_session": "PROBE-2631", "updated_at": "PROBE-2632", "updated_by_session": "PROBE-2633", "bpc_complete": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.bpc_complete`
**Verdict:** `OK`

### [0812] A7/OFF — bpc_metadata.citation_mining_complete   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "citation_mining_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-2634", "created_at": "PROBE-2635", "created_by_session": "PROBE-2636", "updated_at": "PROBE-2637", "updated_by_session": "PROBE-2638", "citation_mining_complete": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.citation_mining_complete`
**Verdict:** `OK`

### [0813] A7/OFF — bpc_metadata.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-2639", "created_at": null, "created_by_session": "PROBE-2640", "updated_at": "PROBE-2641", "updated_by_session": "PROBE-2642"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.created_at`
**Verdict:** `OK`

### [0814] A7/OFF — bpc_metadata.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-2643", "created_at": "PROBE-2644", "created_by_session": null, "updated_at": "PROBE-2645", "updated_by_session": "PROBE-2646"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.created_by_session`
**Verdict:** `OK`

### [0815] A7/OFF — bpc_metadata.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-2647", "created_at": "PROBE-2648", "created_by_session": "PROBE-2649", "updated_at": null, "updated_by_session": "PROBE-2650"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.updated_at`
**Verdict:** `OK`

### [0816] A7/OFF — bpc_metadata.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-2651", "created_at": "PROBE-2652", "created_by_session": "PROBE-2653", "updated_at": "PROBE-2654", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.updated_by_session`
**Verdict:** `OK`

### [0817] A7/OFF — bpc_metadata.supersession_check_complete   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "bpc_metadata" ("slug", "population", "created_at", "created_by_session", "updated_at", "updated_by_session", "supersession_check_complete") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "population": "PROBE-2655", "created_at": "PROBE-2656", "created_by_session": "PROBE-2657", "updated_at": "PROBE-2658", "updated_by_session": "PROBE-2659", "supersession_check_complete": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: bpc_metadata.supersession_check_complete`
**Verdict:** `OK`

### [0818] A7/OFF — case_studies.slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-2660", "slug": null, "title": "PROBE-2661", "building_type": "PROBE-2662", "location": "PROBE-2663", "created_at": "PROBE-2664", "created_by_session": "PROBE-2665"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.slug`
**Verdict:** `OK`

### [0819] A7/OFF — case_studies.title   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-2666", "slug": "PROBE-PK-267", "title": null, "building_type": "PROBE-2667", "location": "PROBE-2668", "created_at": "PROBE-2669", "created_by_session": "PROBE-2670"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.title`
**Verdict:** `OK`

### [0820] A7/OFF — case_studies.building_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-2671", "slug": "PROBE-PK-267", "title": "PROBE-2672", "building_type": null, "location": "PROBE-2673", "created_at": "PROBE-2674", "created_by_session": "PROBE-2675"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.building_type`
**Verdict:** `OK`

### [0821] A7/OFF — case_studies.location   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-2676", "slug": "PROBE-PK-267", "title": "PROBE-2677", "building_type": "PROBE-2678", "location": null, "created_at": "PROBE-2679", "created_by_session": "PROBE-2680"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.location`
**Verdict:** `OK`

### [0822] A7/OFF — case_studies.harm_finding   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session", "harm_finding") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-2681", "slug": "PROBE-PK-267", "title": "PROBE-2682", "building_type": "PROBE-2683", "location": "PROBE-2684", "created_at": "PROBE-2685", "created_by_session": "PROBE-2686", "harm_finding": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.harm_finding`
**Verdict:** `OK`

### [0823] A7/OFF — case_studies.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-2687", "slug": "PROBE-PK-267", "title": "PROBE-2688", "building_type": "PROBE-2689", "location": "PROBE-2690", "created_at": "PROBE-2691", "created_by_session": "PROBE-2692", "status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.status`
**Verdict:** `OK`

### [0824] A7/OFF — case_studies.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-2693", "slug": "PROBE-PK-267", "title": "PROBE-2694", "building_type": "PROBE-2695", "location": "PROBE-2696", "created_at": null, "created_by_session": "PROBE-2697"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.created_at`
**Verdict:** `OK`

### [0825] A7/OFF — case_studies.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "case_studies" ("case_study_id", "slug", "title", "building_type", "location", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"case_study_id": "PROBE-2698", "slug": "PROBE-PK-267", "title": "PROBE-2699", "building_type": "PROBE-2700", "location": "PROBE-2701", "created_at": "PROBE-2702", "created_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_studies.created_by_session`
**Verdict:** `OK`

### [0826] A7/OFF — case_study_outcomes.case_study_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "case_study_outcomes" ("case_study_id", "metric") VALUES (?, ?)  -- {"case_study_id": null, "metric": "PROBE-2703"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_study_outcomes.case_study_id`
**Verdict:** `OK`

### [0827] A7/OFF — case_study_outcomes.metric   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "case_study_outcomes" ("case_study_id", "metric") VALUES (?, ?)  -- {"case_study_id": "PROBE-CASE_STUDY_ID", "metric": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_study_outcomes.metric`
**Verdict:** `OK`

### [0828] A7/OFF — case_study_strategies.case_study_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "case_study_strategies" ("case_study_id", "strategy") VALUES (?, ?)  -- {"case_study_id": null, "strategy": "PROBE-2704"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_study_strategies.case_study_id`
**Verdict:** `OK`

### [0829] A7/OFF — case_study_strategies.strategy   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "case_study_strategies" ("case_study_id", "strategy") VALUES (?, ?)  -- {"case_study_id": "PROBE-CASE_STUDY_ID", "strategy": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: case_study_strategies.strategy`
**Verdict:** `OK`

### [0830] A7/OFF — citation_mining.backward   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session", "backward") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "local_ref_id": "PROBE-2705", "created_at": "PROBE-2706", "created_by_session": "PROBE-2707", "updated_at": "PROBE-2708", "updated_by_session": "PROBE-2709", "backward": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.backward`
**Verdict:** `OK`

### [0831] A7/OFF — citation_mining.forward   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session", "forward") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "local_ref_id": "PROBE-2710", "created_at": "PROBE-2711", "created_by_session": "PROBE-2712", "updated_at": "PROBE-2713", "updated_by_session": "PROBE-2714", "forward": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.forward`
**Verdict:** `OK`

### [0832] A7/OFF — citation_mining.connections_produced   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session", "connections_produced") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "local_ref_id": "PROBE-2715", "created_at": "PROBE-2716", "created_by_session": "PROBE-2717", "updated_at": "PROBE-2718", "updated_by_session": "PROBE-2719", "connections_produced": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.connections_produced`
**Verdict:** `OK`

### [0833] A7/OFF — citation_mining.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "local_ref_id": "PROBE-2720", "created_at": null, "created_by_session": "PROBE-2721", "updated_at": "PROBE-2722", "updated_by_session": "PROBE-2723"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.created_at`
**Verdict:** `OK`

### [0834] A7/OFF — citation_mining.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "local_ref_id": "PROBE-2724", "created_at": "PROBE-2725", "created_by_session": null, "updated_at": "PROBE-2726", "updated_by_session": "PROBE-2727"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.created_by_session`
**Verdict:** `OK`

### [0835] A7/OFF — citation_mining.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "local_ref_id": "PROBE-2728", "created_at": "PROBE-2729", "created_by_session": "PROBE-2730", "updated_at": null, "updated_by_session": "PROBE-2731"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.updated_at`
**Verdict:** `OK`

### [0836] A7/OFF — citation_mining.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "citation_mining" ("slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "local_ref_id": "PROBE-2732", "created_at": "PROBE-2733", "created_by_session": "PROBE-2734", "updated_at": "PROBE-2735", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: citation_mining.updated_by_session`
**Verdict:** `OK`

### [0837] A7/OFF — conflicts.domain   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-2736", "domain": null, "pop_a": "PROBE-2737", "pop_b": "PROBE-2738", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-2739", "created_by_session": "PROBE-2740", "updated_at": "PROBE-2741", "updated_by_session": "PROBE-2742"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.domain`
**Verdict:** `OK`

### [0838] A7/OFF — conflicts.pop_a   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-2743", "domain": "PROBE-2744", "pop_a": null, "pop_b": "PROBE-2745", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-2746", "created_by_session": "PROBE-2747", "updated_at": "PROBE-2748", "updated_by_session": "PROBE-2749"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.pop_a`
**Verdict:** `OK`

### [0839] A7/OFF — conflicts.pop_b   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-2750", "domain": "PROBE-2751", "pop_a": "PROBE-2752", "pop_b": null, "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-2753", "created_by_session": "PROBE-2754", "updated_at": "PROBE-2755", "updated_by_session": "PROBE-2756"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.pop_b`
**Verdict:** `OK`

### [0840] A7/OFF — conflicts.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-2757", "domain": "PROBE-2758", "pop_a": "PROBE-2759", "pop_b": "PROBE-2760", "status": null, "created_at": "PROBE-2761", "created_by_session": "PROBE-2762", "updated_at": "PROBE-2763", "updated_by_session": "PROBE-2764"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.status`
**Verdict:** `OK`

### [0841] A7/OFF — conflicts.source_skill   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "source_skill") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-2765", "domain": "PROBE-2766", "pop_a": "PROBE-2767", "pop_b": "PROBE-2768", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-2769", "created_by_session": "PROBE-2770", "updated_at": "PROBE-2771", "updated_by_session": "PROBE-2772", "source_skill": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.source_skill`
**Verdict:** `OK`

### [0842] A7/OFF — conflicts.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-2773", "domain": "PROBE-2774", "pop_a": "PROBE-2775", "pop_b": "PROBE-2776", "status": "RESOLVED-EVIDENCE", "created_at": null, "created_by_session": "PROBE-2777", "updated_at": "PROBE-2778", "updated_by_session": "PROBE-2779"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.created_at`
**Verdict:** `OK`

### [0843] A7/OFF — conflicts.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-2780", "domain": "PROBE-2781", "pop_a": "PROBE-2782", "pop_b": "PROBE-2783", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-2784", "created_by_session": null, "updated_at": "PROBE-2785", "updated_by_session": "PROBE-2786"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.created_by_session`
**Verdict:** `OK`

### [0844] A7/OFF — conflicts.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-2787", "domain": "PROBE-2788", "pop_a": "PROBE-2789", "pop_b": "PROBE-2790", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-2791", "created_by_session": "PROBE-2792", "updated_at": null, "updated_by_session": "PROBE-2793"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.updated_at`
**Verdict:** `OK`

### [0845] A7/OFF — conflicts.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "conflicts" ("conflict_id", "domain", "pop_a", "pop_b", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"conflict_id": "PROBE-2794", "domain": "PROBE-2795", "pop_a": "PROBE-2796", "pop_b": "PROBE-2797", "status": "RESOLVED-EVIDENCE", "created_at": "PROBE-2798", "created_by_session": "PROBE-2799", "updated_at": "PROBE-2800", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: conflicts.updated_by_session`
**Verdict:** `OK`

### [0846] A7/OFF — connections.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-2801", "status": null, "confidence": "HIGH", "filed_in": "PROBE-2802", "created_at": "PROBE-2803", "created_by_session": "PROBE-2804", "updated_at": "PROBE-2805", "updated_by_session": "PROBE-2806"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.status`
**Verdict:** `OK`

### [0847] A7/OFF — connections.confidence   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-2807", "status": "PENDING", "confidence": null, "filed_in": "PROBE-2808", "created_at": "PROBE-2809", "created_by_session": "PROBE-2810", "updated_at": "PROBE-2811", "updated_by_session": "PROBE-2812"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.confidence`
**Verdict:** `OK`

### [0848] A7/OFF — connections.filed_in   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-2813", "status": "PENDING", "confidence": "HIGH", "filed_in": null, "created_at": "PROBE-2814", "created_by_session": "PROBE-2815", "updated_at": "PROBE-2816", "updated_by_session": "PROBE-2817"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.filed_in`
**Verdict:** `OK`

### [0849] A7/OFF — connections.opus_reviewed   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session", "opus_reviewed") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-2818", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-2819", "created_at": "PROBE-2820", "created_by_session": "PROBE-2821", "updated_at": "PROBE-2822", "updated_by_session": "PROBE-2823", "opus_reviewed": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.opus_reviewed`
**Verdict:** `OK`

### [0850] A7/OFF — connections.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-2824", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-2825", "created_at": null, "created_by_session": "PROBE-2826", "updated_at": "PROBE-2827", "updated_by_session": "PROBE-2828"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.created_at`
**Verdict:** `OK`

### [0851] A7/OFF — connections.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-2829", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-2830", "created_at": "PROBE-2831", "created_by_session": null, "updated_at": "PROBE-2832", "updated_by_session": "PROBE-2833"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.created_by_session`
**Verdict:** `OK`

### [0852] A7/OFF — connections.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-2834", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-2835", "created_at": "PROBE-2836", "created_by_session": "PROBE-2837", "updated_at": null, "updated_by_session": "PROBE-2838"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.updated_at`
**Verdict:** `OK`

### [0853] A7/OFF — connections.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "connections" ("con_id", "status", "confidence", "filed_in", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"con_id": "PROBE-2839", "status": "PENDING", "confidence": "HIGH", "filed_in": "PROBE-2840", "created_at": "PROBE-2841", "created_by_session": "PROBE-2842", "updated_at": "PROBE-2843", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: connections.updated_by_session`
**Verdict:** `OK`

### [0854] A7/OFF — convergence_assessment.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "convergence_assessment" ("status") VALUES (?)  -- {"status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: convergence_assessment.status`
**Verdict:** `OK`

### [0855] A7/OFF — data_migrations.applied_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "data_migrations" ("migration_id", "applied_at", "content_sha") VALUES (?, ?, ?)  -- {"migration_id": "PROBE-2845", "applied_at": null, "content_sha": "PROBE-2846"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: data_migrations.applied_at`
**Verdict:** `OK`

### [0856] A7/OFF — data_migrations.content_sha   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "data_migrations" ("migration_id", "applied_at", "content_sha") VALUES (?, ?, ?)  -- {"migration_id": "PROBE-2847", "applied_at": "PROBE-2848", "content_sha": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: data_migrations.content_sha`
**Verdict:** `OK`

### [0857] A7/OFF — db_meta.value   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "db_meta" ("key", "value") VALUES (?, ?)  -- {"key": "PROBE-2850", "value": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: db_meta.value`
**Verdict:** `OK`

### [0858] A7/OFF — decisions.category   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2851", "category": null, "delegation": "DG-NON", "summary": "PROBE-2852", "outcome": "PROBE-2853", "rationale": "PROBE-2854", "decision_date": "PROBE-2855", "decided_by": "PROBE-2856", "model_routing": "PROBE-2857", "effort_level": 1, "review_status": "PROBE-2858", "created_at": "PROBE-2859", "created_by_session": "PROBE-2860", "updated_at": "PROBE-2861", "updated_by_session": "PROBE-2862"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.category`
**Verdict:** `OK`

### [0859] A7/OFF — decisions.delegation   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2863", "category": "D-DOCT", "delegation": null, "summary": "PROBE-2864", "outcome": "PROBE-2865", "rationale": "PROBE-2866", "decision_date": "PROBE-2867", "decided_by": "PROBE-2868", "model_routing": "PROBE-2869", "effort_level": 1, "review_status": "PROBE-2870", "created_at": "PROBE-2871", "created_by_session": "PROBE-2872", "updated_at": "PROBE-2873", "updated_by_session": "PROBE-2874"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.delegation`
**Verdict:** `OK`

### [0860] A7/OFF — decisions.summary   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2875", "category": "D-DOCT", "delegation": "DG-NON", "summary": null, "outcome": "PROBE-2876", "rationale": "PROBE-2877", "decision_date": "PROBE-2878", "decided_by": "PROBE-2879", "model_routing": "PROBE-2880", "effort_level": 1, "review_status": "PROBE-2881", "created_at": "PROBE-2882", "created_by_session": "PROBE-2883", "updated_at": "PROBE-2884", "updated_by_session": "PROBE-2885"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.summary`
**Verdict:** `OK`

### [0861] A7/OFF — decisions.outcome   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2886", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-2887", "outcome": null, "rationale": "PROBE-2888", "decision_date": "PROBE-2889", "decided_by": "PROBE-2890", "model_routing": "PROBE-2891", "effort_level": 1, "review_status": "PROBE-2892", "created_at": "PROBE-2893", "created_by_session": "PROBE-2894", "updated_at": "PROBE-2895", "updated_by_session": "PROBE-2896"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.outcome`
**Verdict:** `OK`

### [0862] A7/OFF — decisions.rationale   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2897", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-2898", "outcome": "PROBE-2899", "rationale": null, "decision_date": "PROBE-2900", "decided_by": "PROBE-2901", "model_routing": "PROBE-2902", "effort_level": 1, "review_status": "PROBE-2903", "created_at": "PROBE-2904", "created_by_session": "PROBE-2905", "updated_at": "PROBE-2906", "updated_by_session": "PROBE-2907"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.rationale`
**Verdict:** `OK`

### [0863] A7/OFF — decisions.decision_date   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2908", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-2909", "outcome": "PROBE-2910", "rationale": "PROBE-2911", "decision_date": null, "decided_by": "PROBE-2912", "model_routing": "PROBE-2913", "effort_level": 1, "review_status": "PROBE-2914", "created_at": "PROBE-2915", "created_by_session": "PROBE-2916", "updated_at": "PROBE-2917", "updated_by_session": "PROBE-2918"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.decision_date`
**Verdict:** `OK`

### [0864] A7/OFF — decisions.decided_by   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2919", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-2920", "outcome": "PROBE-2921", "rationale": "PROBE-2922", "decision_date": "PROBE-2923", "decided_by": null, "model_routing": "PROBE-2924", "effort_level": 1, "review_status": "PROBE-2925", "created_at": "PROBE-2926", "created_by_session": "PROBE-2927", "updated_at": "PROBE-2928", "updated_by_session": "PROBE-2929"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.decided_by`
**Verdict:** `OK`

### [0865] A7/OFF — decisions.model_routing   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2930", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-2931", "outcome": "PROBE-2932", "rationale": "PROBE-2933", "decision_date": "PROBE-2934", "decided_by": "PROBE-2935", "model_routing": null, "effort_level": 1, "review_status": "PROBE-2936", "created_at": "PROBE-2937", "created_by_session": "PROBE-2938", "updated_at": "PROBE-2939", "updated_by_session": "PROBE-2940"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.model_routing`
**Verdict:** `OK`

### [0866] A7/OFF — decisions.effort_level   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2941", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-2942", "outcome": "PROBE-2943", "rationale": "PROBE-2944", "decision_date": "PROBE-2945", "decided_by": "PROBE-2946", "model_routing": "PROBE-2947", "effort_level": null, "review_status": "PROBE-2948", "created_at": "PROBE-2949", "created_by_session": "PROBE-2950", "updated_at": "PROBE-2951", "updated_by_session": "PROBE-2952"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.effort_level`
**Verdict:** `OK`

### [0867] A7/OFF — decisions.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2953", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-2954", "outcome": "PROBE-2955", "rationale": "PROBE-2956", "decision_date": "PROBE-2957", "decided_by": "PROBE-2958", "model_routing": "PROBE-2959", "effort_level": 1, "review_status": "PROBE-2960", "created_at": "PROBE-2961", "created_by_session": "PROBE-2962", "updated_at": "PROBE-2963", "updated_by_session": "PROBE-2964", "status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.status`
**Verdict:** `OK`

### [0868] A7/OFF — decisions.review_status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2965", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-2966", "outcome": "PROBE-2967", "rationale": "PROBE-2968", "decision_date": "PROBE-2969", "decided_by": "PROBE-2970", "model_routing": "PROBE-2971", "effort_level": 1, "review_status": null, "created_at": "PROBE-2972", "created_by_session": "PROBE-2973", "updated_at": "PROBE-2974", "updated_by_session": "PROBE-2975"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.review_status`
**Verdict:** `OK`

### [0869] A7/OFF — decisions.supersedes   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session", "supersedes") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2976", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-2977", "outcome": "PROBE-2978", "rationale": "PROBE-2979", "decision_date": "PROBE-2980", "decided_by": "PROBE-2981", "model_routing": "PROBE-2982", "effort_level": 1, "review_status": "PROBE-2983", "created_at": "PROBE-2984", "created_by_session": "PROBE-2985", "updated_at": "PROBE-2986", "updated_by_session": "PROBE-2987", "supersedes": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.supersedes`
**Verdict:** `OK`

### [0870] A7/OFF — decisions.predecessors   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session", "predecessors") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-2988", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-2989", "outcome": "PROBE-2990", "rationale": "PROBE-2991", "decision_date": "PROBE-2992", "decided_by": "PROBE-2993", "model_routing": "PROBE-2994", "effort_level": 1, "review_status": "PROBE-2995", "created_at": "PROBE-2996", "created_by_session": "PROBE-2997", "updated_at": "PROBE-2998", "updated_by_session": "PROBE-2999", "predecessors": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.predecessors`
**Verdict:** `OK`

### [0871] A7/OFF — decisions.decision_artifacts   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session", "decision_artifacts") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-3000", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-3001", "outcome": "PROBE-3002", "rationale": "PROBE-3003", "decision_date": "PROBE-3004", "decided_by": "PROBE-3005", "model_routing": "PROBE-3006", "effort_level": 1, "review_status": "PROBE-3007", "created_at": "PROBE-3008", "created_by_session": "PROBE-3009", "updated_at": "PROBE-3010", "updated_by_session": "PROBE-3011", "decision_artifacts": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.decision_artifacts`
**Verdict:** `OK`

### [0872] A7/OFF — decisions.alternatives_considered   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session", "alternatives_considered") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-3012", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-3013", "outcome": "PROBE-3014", "rationale": "PROBE-3015", "decision_date": "PROBE-3016", "decided_by": "PROBE-3017", "model_routing": "PROBE-3018", "effort_level": 1, "review_status": "PROBE-3019", "created_at": "PROBE-3020", "created_by_session": "PROBE-3021", "updated_at": "PROBE-3022", "updated_by_session": "PROBE-3023", "alternatives_considered": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.alternatives_considered`
**Verdict:** `OK`

### [0873] A7/OFF — decisions.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-3024", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-3025", "outcome": "PROBE-3026", "rationale": "PROBE-3027", "decision_date": "PROBE-3028", "decided_by": "PROBE-3029", "model_routing": "PROBE-3030", "effort_level": 1, "review_status": "PROBE-3031", "created_at": null, "created_by_session": "PROBE-3032", "updated_at": "PROBE-3033", "updated_by_session": "PROBE-3034"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.created_at`
**Verdict:** `OK`

### [0874] A7/OFF — decisions.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-3035", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-3036", "outcome": "PROBE-3037", "rationale": "PROBE-3038", "decision_date": "PROBE-3039", "decided_by": "PROBE-3040", "model_routing": "PROBE-3041", "effort_level": 1, "review_status": "PROBE-3042", "created_at": "PROBE-3043", "created_by_session": null, "updated_at": "PROBE-3044", "updated_by_session": "PROBE-3045"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.created_by_session`
**Verdict:** `OK`

### [0875] A7/OFF — decisions.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-3046", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-3047", "outcome": "PROBE-3048", "rationale": "PROBE-3049", "decision_date": "PROBE-3050", "decided_by": "PROBE-3051", "model_routing": "PROBE-3052", "effort_level": 1, "review_status": "PROBE-3053", "created_at": "PROBE-3054", "created_by_session": "PROBE-3055", "updated_at": null, "updated_by_session": "PROBE-3056"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.updated_at`
**Verdict:** `OK`

### [0876] A7/OFF — decisions.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "decisions" ("decision_id", "category", "delegation", "summary", "outcome", "rationale", "decision_date", "decided_by", "model_routing", "effort_level", "review_status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"decision_id": "PROBE-3057", "category": "D-DOCT", "delegation": "DG-NON", "summary": "PROBE-3058", "outcome": "PROBE-3059", "rationale": "PROBE-3060", "decision_date": "PROBE-3061", "decided_by": "PROBE-3062", "model_routing": "PROBE-3063", "effort_level": 1, "review_status": "PROBE-3064", "created_at": "PROBE-3065", "created_by_session": "PROBE-3066", "updated_at": "PROBE-3067", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: decisions.updated_by_session`
**Verdict:** `OK`

### [0877] A7/OFF — economics_entries.pillar   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-3068", "pillar": null, "entry_type": "cost_premium", "source": "PROBE-3069", "finding": "PROBE-3070", "created_at": "PROBE-3071", "created_by_session": "PROBE-3072"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.pillar`
**Verdict:** `OK`

### [0878] A7/OFF — economics_entries.entry_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-3073", "pillar": "health", "entry_type": null, "source": "PROBE-3074", "finding": "PROBE-3075", "created_at": "PROBE-3076", "created_by_session": "PROBE-3077"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.entry_type`
**Verdict:** `OK`

### [0879] A7/OFF — economics_entries.source   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-3078", "pillar": "health", "entry_type": "cost_premium", "source": null, "finding": "PROBE-3079", "created_at": "PROBE-3080", "created_by_session": "PROBE-3081"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.source`
**Verdict:** `OK`

### [0880] A7/OFF — economics_entries.finding   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-3082", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-3083", "finding": null, "created_at": "PROBE-3084", "created_by_session": "PROBE-3085"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.finding`
**Verdict:** `OK`

### [0881] A7/OFF — economics_entries.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-3086", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-3087", "finding": "PROBE-3088", "created_at": "PROBE-3089", "created_by_session": "PROBE-3090", "status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.status`
**Verdict:** `OK`

### [0882] A7/OFF — economics_entries.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-3091", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-3092", "finding": "PROBE-3093", "created_at": null, "created_by_session": "PROBE-3094"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.created_at`
**Verdict:** `OK`

### [0883] A7/OFF — economics_entries.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "economics_entries" ("entry_id", "pillar", "entry_type", "source", "finding", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"entry_id": "PROBE-3095", "pillar": "health", "entry_type": "cost_premium", "source": "PROBE-3096", "finding": "PROBE-3097", "created_at": "PROBE-3098", "created_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: economics_entries.created_by_session`
**Verdict:** `OK`

### [0884] A7/OFF — evidence_population_match.source_ref   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-3099", "source_ref": null, "target_population": "PROBE-3100", "match_grade": "EXACT", "created_at": "PROBE-3101", "created_by_session": "PROBE-3102"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_population_match.source_ref`
**Verdict:** `OK`

### [0885] A7/OFF — evidence_population_match.target_population   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-3103", "source_ref": "PROBE-3104", "target_population": null, "match_grade": "EXACT", "created_at": "PROBE-3105", "created_by_session": "PROBE-3106"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_population_match.target_population`
**Verdict:** `OK`

### [0886] A7/OFF — evidence_population_match.match_grade   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-3107", "source_ref": "PROBE-3108", "target_population": "PROBE-3109", "match_grade": null, "created_at": "PROBE-3110", "created_by_session": "PROBE-3111"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_population_match.match_grade`
**Verdict:** `OK`

### [0887] A7/OFF — evidence_population_match.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-3112", "source_ref": "PROBE-3113", "target_population": "PROBE-3114", "match_grade": "EXACT", "created_at": null, "created_by_session": "PROBE-3115"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_population_match.created_at`
**Verdict:** `OK`

### [0888] A7/OFF — evidence_population_match.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_population_match" ("match_id", "source_ref", "target_population", "match_grade", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"match_id": "PROBE-3116", "source_ref": "PROBE-3117", "target_population": "PROBE-3118", "match_grade": "EXACT", "created_at": "PROBE-3119", "created_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_population_match.created_by_session`
**Verdict:** `OK`

### [0889] A7/OFF — evidence_source_authors.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_source_authors" ("ref_id", "position") VALUES (?, ?)  -- {"ref_id": null, "position": 1}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_source_authors.ref_id`
**Verdict:** `OK`

### [0890] A7/OFF — evidence_source_authors.position   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_source_authors" ("ref_id", "position") VALUES (?, ?)  -- {"ref_id": "PROBE-PK-1012", "position": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_source_authors.position`
**Verdict:** `OK`

### [0891] A7/OFF — evidence_source_authors.is_corporate   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_source_authors" ("ref_id", "position", "is_corporate") VALUES (?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "position": 1, "is_corporate": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_source_authors.is_corporate`
**Verdict:** `OK`

### [0892] A7/OFF — evidence_source_authors.role   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_source_authors" ("ref_id", "position", "role") VALUES (?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "position": 1, "role": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_source_authors.role`
**Verdict:** `OK`

### [0893] A7/OFF — evidence_sources.data_capture_status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "data_capture_status") VALUES (?, ?)  -- {"ref_id": "PROBE-3120", "data_capture_status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_sources.data_capture_status`
**Verdict:** `OK`

### [0894] A7/OFF — evidence_sources.citation_mining_status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_sources" ("ref_id", "citation_mining_status") VALUES (?, ?)  -- {"ref_id": "PROBE-3121", "citation_mining_status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: evidence_sources.citation_mining_status`
**Verdict:** `OK`

### [0895] A7/OFF — external_root_registry.description   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "external_root_registry" ("root_id", "description") VALUES (?, ?)  -- {"root_id": "PROBE-3122", "description": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: external_root_registry.description`
**Verdict:** `OK`

### [0896] A7/OFF — gap_mining.gap_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": null, "attempt_at": "PROBE-3123", "attempted_by_session": "PROBE-3124", "search_strategy_record": "PROBE-3125", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-3126"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.gap_id`
**Verdict:** `OK`

### [0897] A7/OFF — gap_mining.attempt_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-1023", "attempt_at": null, "attempted_by_session": "PROBE-3127", "search_strategy_record": "PROBE-3128", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-3129"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.attempt_at`
**Verdict:** `OK`

### [0898] A7/OFF — gap_mining.attempted_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-1023", "attempt_at": "PROBE-3130", "attempted_by_session": null, "search_strategy_record": "PROBE-3131", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-3132"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.attempted_by_session`
**Verdict:** `OK`

### [0899] A7/OFF — gap_mining.search_strategy_record   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-1023", "attempt_at": "PROBE-3133", "attempted_by_session": "PROBE-3134", "search_strategy_record": null, "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-3135"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.search_strategy_record`
**Verdict:** `OK`

### [0900] A7/OFF — gap_mining.candidates_returned   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged", "candidates_returned") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-1023", "attempt_at": "PROBE-3136", "attempted_by_session": "PROBE-3137", "search_strategy_record": "PROBE-3138", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-3139", "candidates_returned": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.candidates_returned`
**Verdict:** `OK`

### [0901] A7/OFF — gap_mining.candidates_reviewed   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged", "candidates_reviewed") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-1023", "attempt_at": "PROBE-3140", "attempted_by_session": "PROBE-3141", "search_strategy_record": "PROBE-3142", "outcome": "closure_evidence_found", "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-3143", "candidates_reviewed": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.candidates_reviewed`
**Verdict:** `OK`

### [0902] A7/OFF — gap_mining.outcome   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-1023", "attempt_at": "PROBE-3144", "attempted_by_session": "PROBE-3145", "search_strategy_record": "PROBE-3146", "outcome": null, "check_method": "pubmed_cluster", "discoveries_logged": "PROBE-3147"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.outcome`
**Verdict:** `OK`

### [0903] A7/OFF — gap_mining.check_method   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gap_mining" ("gap_id", "attempt_at", "attempted_by_session", "search_strategy_record", "outcome", "check_method", "discoveries_logged") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-PK-1023", "attempt_at": "PROBE-3148", "attempted_by_session": "PROBE-3149", "search_strategy_record": "PROBE-3150", "outcome": "closure_evidence_found", "check_method": null, "discoveries_logged": "PROBE-3151"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gap_mining.check_method`
**Verdict:** `OK`

### [0904] A7/OFF — gaps.category   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-3152", "category": null, "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-3153", "created_at": "PROBE-3154", "created_by_session": "PROBE-3155", "updated_at": "PROBE-3156", "updated_by_session": "PROBE-3157"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.category`
**Verdict:** `OK`

### [0905] A7/OFF — gaps.priority   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-3158", "category": "RP", "priority": null, "status": "OPEN-PROBE", "description": "PROBE-3159", "created_at": "PROBE-3160", "created_by_session": "PROBE-3161", "updated_at": "PROBE-3162", "updated_by_session": "PROBE-3163"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.priority`
**Verdict:** `OK`

### [0906] A7/OFF — gaps.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-3164", "category": "RP", "priority": "P1", "status": null, "description": "PROBE-3165", "created_at": "PROBE-3166", "created_by_session": "PROBE-3167", "updated_at": "PROBE-3168", "updated_by_session": "PROBE-3169"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.status`
**Verdict:** `OK`

### [0907] A7/OFF — gaps.description   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-3170", "category": "RP", "priority": "P1", "status": "OPEN-PROBE", "description": null, "created_at": "PROBE-3171", "created_by_session": "PROBE-3172", "updated_at": "PROBE-3173", "updated_by_session": "PROBE-3174"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.description`
**Verdict:** `OK`

### [0908] A7/OFF — gaps.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-3175", "category": "RP", "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-3176", "created_at": null, "created_by_session": "PROBE-3177", "updated_at": "PROBE-3178", "updated_by_session": "PROBE-3179"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.created_at`
**Verdict:** `OK`

### [0909] A7/OFF — gaps.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-3180", "category": "RP", "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-3181", "created_at": "PROBE-3182", "created_by_session": null, "updated_at": "PROBE-3183", "updated_by_session": "PROBE-3184"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.created_by_session`
**Verdict:** `OK`

### [0910] A7/OFF — gaps.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-3185", "category": "RP", "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-3186", "created_at": "PROBE-3187", "created_by_session": "PROBE-3188", "updated_at": null, "updated_by_session": "PROBE-3189"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.updated_at`
**Verdict:** `OK`

### [0911] A7/OFF — gaps.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "gaps" ("gap_id", "category", "priority", "status", "description", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"gap_id": "PROBE-3190", "category": "RP", "priority": "P1", "status": "OPEN-PROBE", "description": "PROBE-3191", "created_at": "PROBE-3192", "created_by_session": "PROBE-3193", "updated_at": "PROBE-3194", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: gaps.updated_by_session`
**Verdict:** `OK`

### [0912] A7/OFF — item_audit_runs.item_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-3195", "item_code": null, "session": "PROBE-3196", "created_at": "PROBE-3197", "created_by_session": "PROBE-3198", "updated_at": "PROBE-3199", "updated_by_session": "PROBE-3200"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.item_code`
**Verdict:** `OK`

### [0913] A7/OFF — item_audit_runs.session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-3201", "item_code": "A-01", "session": null, "created_at": "PROBE-3202", "created_by_session": "PROBE-3203", "updated_at": "PROBE-3204", "updated_by_session": "PROBE-3205"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.session`
**Verdict:** `OK`

### [0914] A7/OFF — item_audit_runs.steps_complete   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session", "steps_complete") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-3206", "item_code": "A-01", "session": "PROBE-3207", "created_at": "PROBE-3208", "created_by_session": "PROBE-3209", "updated_at": "PROBE-3210", "updated_by_session": "PROBE-3211", "steps_complete": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.steps_complete`
**Verdict:** `OK`

### [0915] A7/OFF — item_audit_runs.steps_started   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session", "steps_started") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-3212", "item_code": "A-01", "session": "PROBE-3213", "created_at": "PROBE-3214", "created_by_session": "PROBE-3215", "updated_at": "PROBE-3216", "updated_by_session": "PROBE-3217", "steps_started": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.steps_started`
**Verdict:** `OK`

### [0916] A7/OFF — item_audit_runs.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-3218", "item_code": "A-01", "session": "PROBE-3219", "created_at": "PROBE-3220", "created_by_session": "PROBE-3221", "updated_at": "PROBE-3222", "updated_by_session": "PROBE-3223", "status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.status`
**Verdict:** `OK`

### [0917] A7/OFF — item_audit_runs.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-3224", "item_code": "A-01", "session": "PROBE-3225", "created_at": null, "created_by_session": "PROBE-3226", "updated_at": "PROBE-3227", "updated_by_session": "PROBE-3228"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.created_at`
**Verdict:** `OK`

### [0918] A7/OFF — item_audit_runs.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-3229", "item_code": "A-01", "session": "PROBE-3230", "created_at": "PROBE-3231", "created_by_session": null, "updated_at": "PROBE-3232", "updated_by_session": "PROBE-3233"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.created_by_session`
**Verdict:** `OK`

### [0919] A7/OFF — item_audit_runs.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-3234", "item_code": "A-01", "session": "PROBE-3235", "created_at": "PROBE-3236", "created_by_session": "PROBE-3237", "updated_at": null, "updated_by_session": "PROBE-3238"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.updated_at`
**Verdict:** `OK`

### [0920] A7/OFF — item_audit_runs.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_audit_runs" ("run_id", "item_code", "session", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"run_id": "PROBE-3239", "item_code": "A-01", "session": "PROBE-3240", "created_at": "PROBE-3241", "created_by_session": "PROBE-3242", "updated_at": "PROBE-3243", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_audit_runs.updated_by_session`
**Verdict:** `OK`

### [0921] A7/OFF — item_bpc_links.link_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_bpc_links" ("item_code", "slug", "link_type", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?)  -- {"item_code": "I-04", "slug": "PROBE-PK-267", "link_type": null, "created_at": "PROBE-3244", "created_by_session": "PROBE-3245"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_bpc_links.link_type`
**Verdict:** `OK`

### [0922] A7/OFF — item_bpc_links.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_bpc_links" ("item_code", "slug", "link_type", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?)  -- {"item_code": "I-04", "slug": "PROBE-PK-267", "link_type": "primary", "created_at": null, "created_by_session": "PROBE-3246"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_bpc_links.created_at`
**Verdict:** `OK`

### [0923] A7/OFF — item_bpc_links.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_bpc_links" ("item_code", "slug", "link_type", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?)  -- {"item_code": "I-04", "slug": "PROBE-PK-267", "link_type": "primary", "created_at": "PROBE-3247", "created_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_bpc_links.created_by_session`
**Verdict:** `OK`

### [0924] A7/OFF — item_population_elaborations.item_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("item_code", "population_code") VALUES (?, ?)  -- {"item_code": null, "population_code": "ADHD"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_population_elaborations.item_code`
**Verdict:** `OK`

### [0925] A7/OFF — item_population_elaborations.population_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("item_code", "population_code") VALUES (?, ?)  -- {"item_code": "A-01", "population_code": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_population_elaborations.population_code`
**Verdict:** `OK`

### [0926] A7/OFF — item_population_links.applicability   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_population_links" ("item_code", "population_code", "subtype", "applicability") VALUES (?, ?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "subtype": "PROBE-3248", "applicability": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: item_population_links.applicability`
**Verdict:** `OK`

### [0927] A7/OFF — items.category   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-3249", "category": null, "name": "PROBE-3250", "created_at": "PROBE-3251", "created_by_session": "PROBE-3252", "updated_at": "PROBE-3253", "updated_by_session": "PROBE-3254"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.category`
**Verdict:** `OK`

### [0928] A7/OFF — items.name   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-3255", "category": "A", "name": null, "created_at": "PROBE-3256", "created_by_session": "PROBE-3257", "updated_at": "PROBE-3258", "updated_by_session": "PROBE-3259"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.name`
**Verdict:** `OK`

### [0929] A7/OFF — items.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session", "status") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-3260", "category": "A", "name": "PROBE-3261", "created_at": "PROBE-3262", "created_by_session": "PROBE-3263", "updated_at": "PROBE-3264", "updated_by_session": "PROBE-3265", "status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.status`
**Verdict:** `OK`

### [0930] A7/OFF — items.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-3266", "category": "A", "name": "PROBE-3267", "created_at": null, "created_by_session": "PROBE-3268", "updated_at": "PROBE-3269", "updated_by_session": "PROBE-3270"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.created_at`
**Verdict:** `OK`

### [0931] A7/OFF — items.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-3271", "category": "A", "name": "PROBE-3272", "created_at": "PROBE-3273", "created_by_session": null, "updated_at": "PROBE-3274", "updated_by_session": "PROBE-3275"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.created_by_session`
**Verdict:** `OK`

### [0932] A7/OFF — items.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-3276", "category": "A", "name": "PROBE-3277", "created_at": "PROBE-3278", "created_by_session": "PROBE-3279", "updated_at": null, "updated_by_session": "PROBE-3280"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.updated_at`
**Verdict:** `OK`

### [0933] A7/OFF — items.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-3281", "category": "A", "name": "PROBE-3282", "created_at": "PROBE-3283", "created_by_session": "PROBE-3284", "updated_at": "PROBE-3285", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: items.updated_by_session`
**Verdict:** `OK`

### [0934] A7/OFF — jurisdictional_values.item_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "jurisdictional_values" ("item_code", "jurisdiction") VALUES (?, ?)  -- {"item_code": null, "jurisdiction": "PROBE-3286"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: jurisdictional_values.item_code`
**Verdict:** `OK`

### [0935] A7/OFF — jurisdictional_values.jurisdiction   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "jurisdictional_values" ("item_code", "jurisdiction") VALUES (?, ?)  -- {"item_code": "A-01", "jurisdiction": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: jurisdictional_values.jurisdiction`
**Verdict:** `OK`

### [0936] A7/OFF — jurisdictional_values.evidence_tier   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "jurisdictional_values" ("item_code", "jurisdiction", "evidence_tier") VALUES (?, ?, ?)  -- {"item_code": "A-01", "jurisdiction": "PROBE-3287", "evidence_tier": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: jurisdictional_values.evidence_tier`
**Verdict:** `OK`

### [0937] A7/OFF — lang_jur_map.role   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "lang_jur_map" ("language", "jurisdiction", "role") VALUES (?, ?, ?)  -- {"language": "PROBE-3288", "jurisdiction": "PROBE-3289", "role": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: lang_jur_map.role`
**Verdict:** `OK`

### [0938] A7/OFF — life_stage_modifiers.label   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "life_stage_modifiers" ("label", "code", "definition") VALUES (?, ?, ?)  -- {"label": null, "code": "PROBE-PK-3290", "definition": "PROBE-DEFINITION"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: life_stage_modifiers.label`
**Verdict:** `OK`

### [0939] A7/OFF — life_stage_modifiers.definition   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "life_stage_modifiers" ("definition", "code", "label") VALUES (?, ?, ?)  -- {"definition": null, "code": "PROBE-PK-3291", "label": "PROBE-LABEL"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: life_stage_modifiers.definition`
**Verdict:** `OK`

### [0940] A7/OFF — pipeline_runs.started_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "pipeline_runs" ("run_id", "started_at") VALUES (?, ?)  -- {"run_id": "PROBE-3293", "started_at": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: pipeline_runs.started_at`
**Verdict:** `OK`

### [0941] A7/OFF — population_axis_map.role   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "population_axis_map" ("population_code", "axis_code", "role") VALUES (?, ?, ?)  -- {"population_code": "ADHD", "axis_code": "AX-AMB", "role": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: population_axis_map.role`
**Verdict:** `OK`

### [0942] A7/OFF — population_reclass.row_kind   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale") VALUES (?, ?, ?, ?)  -- {"population_code": "PROBE-3294", "row_kind": null, "layer": "AXIS-ALIAS", "rationale": "PROBE-3295"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: population_reclass.row_kind`
**Verdict:** `OK`

### [0943] A7/OFF — population_reclass.layer   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale") VALUES (?, ?, ?, ?)  -- {"population_code": "PROBE-3296", "row_kind": "EXISTING-POP", "layer": null, "rationale": "PROBE-3297"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: population_reclass.layer`
**Verdict:** `OK`

### [0944] A7/OFF — population_reclass.rationale   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "population_reclass" ("population_code", "row_kind", "layer", "rationale") VALUES (?, ?, ?, ?)  -- {"population_code": "PROBE-3298", "row_kind": "EXISTING-POP", "layer": "AXIS-ALIAS", "rationale": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: population_reclass.rationale`
**Verdict:** `OK`

### [0945] A7/OFF — populations.display_name   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "populations" ("population_code", "display_name") VALUES (?, ?)  -- {"population_code": "PROBE-3299", "display_name": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: populations.display_name`
**Verdict:** `OK`

### [0946] A7/OFF — reasoning_doc_citations.reasoning_doc_slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-3300", "reasoning_doc_slug": null, "parameter": "PROBE-3301", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-1012", "verified_at": "PROBE-3302", "verified_by_session": "PROBE-3303", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-3304", "claim_text": "PROBE-3305"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.reasoning_doc_slug`
**Verdict:** `OK`

### [0947] A7/OFF — reasoning_doc_citations.parameter   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-3306", "reasoning_doc_slug": "PROBE-PK-267", "parameter": null, "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-1012", "verified_at": "PROBE-3307", "verified_by_session": "PROBE-3308", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-3309", "claim_text": "PROBE-3310"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.parameter`
**Verdict:** `OK`

### [0948] A7/OFF — reasoning_doc_citations.claim_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-3311", "reasoning_doc_slug": "PROBE-PK-267", "parameter": "PROBE-3312", "claim_type": null, "source_ref_id": "PROBE-PK-1012", "verified_at": "PROBE-3313", "verified_by_session": "PROBE-3314", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-3315", "claim_text": "PROBE-3316"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.claim_type`
**Verdict:** `OK`

### [0949] A7/OFF — reasoning_doc_citations.source_ref_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-3317", "reasoning_doc_slug": "PROBE-PK-267", "parameter": "PROBE-3318", "claim_type": "numerical_spec", "source_ref_id": null, "verified_at": "PROBE-3319", "verified_by_session": "PROBE-3320", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-3321", "claim_text": "PROBE-3322"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.source_ref_id`
**Verdict:** `OK`

### [0950] A7/OFF — reasoning_doc_citations.verified_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-3323", "reasoning_doc_slug": "PROBE-PK-267", "parameter": "PROBE-3324", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-1012", "verified_at": null, "verified_by_session": "PROBE-3325", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-3326", "claim_text": "PROBE-3327"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.verified_at`
**Verdict:** `OK`

### [0951] A7/OFF — reasoning_doc_citations.verified_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-3328", "reasoning_doc_slug": "PROBE-PK-267", "parameter": "PROBE-3329", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-1012", "verified_at": "PROBE-3330", "verified_by_session": null, "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-3331", "claim_text": "PROBE-3332"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.verified_by_session`
**Verdict:** `OK`

### [0952] A7/OFF — reasoning_doc_citations.paywall_purchase_candidate   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "reasoning_doc_citations" ("citation_id", "reasoning_doc_slug", "parameter", "claim_type", "source_ref_id", "verified_at", "verified_by_session", "value_match", "claim_match", "claimed_value", "claim_text", "paywall_purchase_candidate") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"citation_id": "PROBE-3333", "reasoning_doc_slug": "PROBE-PK-267", "parameter": "PROBE-3334", "claim_type": "numerical_spec", "source_ref_id": "PROBE-PK-1012", "verified_at": "PROBE-3335", "verified_by_session": "PROBE-3336", "value_match": "EXACT", "claim_match": "SUPPORTED", "claimed_value": "PROBE-3337", "claim_text": "PROBE-3338", "paywall_purchase_candidate": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: reasoning_doc_citations.paywall_purchase_candidate`
**Verdict:** `OK`

### [0953] A7/OFF — room_items.applicability   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "room_items" ("room_code", "item_code", "applicability") VALUES (?, ?, ?)  -- {"room_code": "R-ASM", "item_code": "A-01", "applicability": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: room_items.applicability`
**Verdict:** `OK`

### [0954] A7/OFF — rooms.name   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "rooms" ("room_code", "name") VALUES (?, ?)  -- {"room_code": "PROBE-3339", "name": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: rooms.name`
**Verdict:** `OK`

### [0955] A7/OFF — rooms.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "rooms" ("room_code", "name", "status") VALUES (?, ?, ?)  -- {"room_code": "PROBE-3340", "name": "PROBE-3341", "status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: rooms.status`
**Verdict:** `OK`

### [0956] A7/OFF — search_candidates.found_under_slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": null, "disposition": "REHOME", "title": "PROBE-3342", "session": "PROBE-3343", "created_at": "PROBE-3344"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_candidates.found_under_slug`
**Verdict:** `OK`

### [0957] A7/OFF — search_candidates.disposition   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": "PROBE-PK-267", "disposition": null, "title": "PROBE-3345", "session": "PROBE-3346", "created_at": "PROBE-3347"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_candidates.disposition`
**Verdict:** `OK`

### [0958] A7/OFF — search_candidates.title   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": "PROBE-PK-267", "disposition": "REHOME", "title": null, "session": "PROBE-3348", "created_at": "PROBE-3349"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_candidates.title`
**Verdict:** `OK`

### [0959] A7/OFF — search_candidates.harm_finding   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at", "harm_finding") VALUES (?, ?, ?, ?, ?, ?)  -- {"found_under_slug": "PROBE-PK-267", "disposition": "REHOME", "title": "PROBE-3350", "session": "PROBE-3351", "created_at": "PROBE-3352", "harm_finding": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_candidates.harm_finding`
**Verdict:** `OK`

### [0960] A7/OFF — search_candidates.session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": "PROBE-PK-267", "disposition": "REHOME", "title": "PROBE-3353", "session": null, "created_at": "PROBE-3354"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_candidates.session`
**Verdict:** `OK`

### [0961] A7/OFF — search_candidates.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_candidates" ("found_under_slug", "disposition", "title", "session", "created_at") VALUES (?, ?, ?, ?, ?)  -- {"found_under_slug": "PROBE-PK-267", "disposition": "REHOME", "title": "PROBE-3355", "session": "PROBE-3356", "created_at": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_candidates.created_at`
**Verdict:** `OK`

### [0962] A7/OFF — search_coverage.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "jurisdiction": "PROBE-3357", "status": null, "created_at": "PROBE-3358", "created_by_session": "PROBE-3359", "updated_at": "PROBE-3360", "updated_by_session": "PROBE-3361"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.status`
**Verdict:** `OK`

### [0963] A7/OFF — search_coverage.co1_attempted   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "co1_attempted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "jurisdiction": "PROBE-3362", "status": "SEARCHED", "created_at": "PROBE-3363", "created_by_session": "PROBE-3364", "updated_at": "PROBE-3365", "updated_by_session": "PROBE-3366", "co1_attempted": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.co1_attempted`
**Verdict:** `OK`

### [0964] A7/OFF — search_coverage.tier5_attempted   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "tier5_attempted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "jurisdiction": "PROBE-3367", "status": "SEARCHED", "created_at": "PROBE-3368", "created_by_session": "PROBE-3369", "updated_at": "PROBE-3370", "updated_by_session": "PROBE-3371", "tier5_attempted": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.tier5_attempted`
**Verdict:** `OK`

### [0965] A7/OFF — search_coverage.tier6_attempted   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "tier6_attempted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "jurisdiction": "PROBE-3372", "status": "SEARCHED", "created_at": "PROBE-3373", "created_by_session": "PROBE-3374", "updated_at": "PROBE-3375", "updated_by_session": "PROBE-3376", "tier6_attempted": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.tier6_attempted`
**Verdict:** `OK`

### [0966] A7/OFF — search_coverage.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "jurisdiction": "PROBE-3377", "status": "SEARCHED", "created_at": null, "created_by_session": "PROBE-3378", "updated_at": "PROBE-3379", "updated_by_session": "PROBE-3380"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.created_at`
**Verdict:** `OK`

### [0967] A7/OFF — search_coverage.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "jurisdiction": "PROBE-3381", "status": "SEARCHED", "created_at": "PROBE-3382", "created_by_session": null, "updated_at": "PROBE-3383", "updated_by_session": "PROBE-3384"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.created_by_session`
**Verdict:** `OK`

### [0968] A7/OFF — search_coverage.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "jurisdiction": "PROBE-3385", "status": "SEARCHED", "created_at": "PROBE-3386", "created_by_session": "PROBE-3387", "updated_at": null, "updated_by_session": "PROBE-3388"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.updated_at`
**Verdict:** `OK`

### [0969] A7/OFF — search_coverage.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_coverage" ("slug", "jurisdiction", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "jurisdiction": "PROBE-3389", "status": "SEARCHED", "created_at": "PROBE-3390", "created_by_session": "PROBE-3391", "updated_at": "PROBE-3392", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_coverage.updated_by_session`
**Verdict:** `OK`

### [0970] A7/OFF — search_executions.slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": null, "language": "PROBE-3393", "query_text": "PROBE-3394", "engine": "PROBE-3395", "depth_method": "scoping", "session": "PROBE-3396", "executed_at": "PROBE-3397"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.slug`
**Verdict:** `OK`

### [0971] A7/OFF — search_executions.language   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": null, "query_text": "PROBE-3398", "engine": "PROBE-3399", "depth_method": "scoping", "session": "PROBE-3400", "executed_at": "PROBE-3401"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.language`
**Verdict:** `OK`

### [0972] A7/OFF — search_executions.query_text   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3402", "query_text": null, "engine": "PROBE-3403", "depth_method": "scoping", "session": "PROBE-3404", "executed_at": "PROBE-3405"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.query_text`
**Verdict:** `OK`

### [0973] A7/OFF — search_executions.engine   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3406", "query_text": "PROBE-3407", "engine": null, "depth_method": "scoping", "session": "PROBE-3408", "executed_at": "PROBE-3409"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.engine`
**Verdict:** `OK`

### [0974] A7/OFF — search_executions.depth_method   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3410", "query_text": "PROBE-3411", "engine": "PROBE-3412", "depth_method": null, "session": "PROBE-3413", "executed_at": "PROBE-3414"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.depth_method`
**Verdict:** `OK`

### [0975] A7/OFF — search_executions.results_found   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "results_found") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3415", "query_text": "PROBE-3416", "engine": "PROBE-3417", "depth_method": "scoping", "session": "PROBE-3418", "executed_at": "PROBE-3419", "results_found": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.results_found`
**Verdict:** `OK`

### [0976] A7/OFF — search_executions.results_screened   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "results_screened") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3420", "query_text": "PROBE-3421", "engine": "PROBE-3422", "depth_method": "scoping", "session": "PROBE-3423", "executed_at": "PROBE-3424", "results_screened": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.results_screened`
**Verdict:** `OK`

### [0977] A7/OFF — search_executions.results_admitted   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "results_admitted") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3425", "query_text": "PROBE-3426", "engine": "PROBE-3427", "depth_method": "scoping", "session": "PROBE-3428", "executed_at": "PROBE-3429", "results_admitted": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.results_admitted`
**Verdict:** `OK`

### [0978] A7/OFF — search_executions.backfill   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "backfill") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3430", "query_text": "PROBE-3431", "engine": "PROBE-3432", "depth_method": "scoping", "session": "PROBE-3433", "executed_at": "PROBE-3434", "backfill": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.backfill`
**Verdict:** `OK`

### [0979] A7/OFF — search_executions.session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3435", "query_text": "PROBE-3436", "engine": "PROBE-3437", "depth_method": "scoping", "session": null, "executed_at": "PROBE-3438"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.session`
**Verdict:** `OK`

### [0980] A7/OFF — search_executions.executed_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3439", "query_text": "PROBE-3440", "engine": "PROBE-3441", "depth_method": "scoping", "session": "PROBE-3442", "executed_at": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.executed_at`
**Verdict:** `OK`

### [0981] A7/OFF — search_executions.harm_finding   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_executions" ("slug", "language", "query_text", "engine", "depth_method", "session", "executed_at", "harm_finding") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3443", "query_text": "PROBE-3444", "engine": "PROBE-3445", "depth_method": "scoping", "session": "PROBE-3446", "executed_at": "PROBE-3447", "harm_finding": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_executions.harm_finding`
**Verdict:** `OK`

### [0982] A7/OFF — search_languages.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3448", "status": null, "created_at": "PROBE-3449", "created_by_session": "PROBE-3450", "updated_at": "PROBE-3451", "updated_by_session": "PROBE-3452"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_languages.status`
**Verdict:** `OK`

### [0983] A7/OFF — search_languages.results_count   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session", "results_count") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3453", "status": "SEARCHED", "created_at": "PROBE-3454", "created_by_session": "PROBE-3455", "updated_at": "PROBE-3456", "updated_by_session": "PROBE-3457", "results_count": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_languages.results_count`
**Verdict:** `OK`

### [0984] A7/OFF — search_languages.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3458", "status": "SEARCHED", "created_at": null, "created_by_session": "PROBE-3459", "updated_at": "PROBE-3460", "updated_by_session": "PROBE-3461"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_languages.created_at`
**Verdict:** `OK`

### [0985] A7/OFF — search_languages.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3462", "status": "SEARCHED", "created_at": "PROBE-3463", "created_by_session": null, "updated_at": "PROBE-3464", "updated_by_session": "PROBE-3465"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_languages.created_by_session`
**Verdict:** `OK`

### [0986] A7/OFF — search_languages.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3466", "status": "SEARCHED", "created_at": "PROBE-3467", "created_by_session": "PROBE-3468", "updated_at": null, "updated_by_session": "PROBE-3469"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_languages.updated_at`
**Verdict:** `OK`

### [0987] A7/OFF — search_languages.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "search_languages" ("slug", "language", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-PK-267", "language": "PROBE-3470", "status": "SEARCHED", "created_at": "PROBE-3471", "created_by_session": "PROBE-3472", "updated_at": "PROBE-3473", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: search_languages.updated_by_session`
**Verdict:** `OK`

### [0988] A7/OFF — situations.title   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "situations" ("situation_id", "title", "account_language", "account_text_ref") VALUES (?, ?, ?, ?)  -- {"situation_id": "PROBE-3474", "title": null, "account_language": "PROBE-3475", "account_text_ref": "PROBE-3476"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: situations.title`
**Verdict:** `OK`

### [0989] A7/OFF — situations.account_language   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "situations" ("situation_id", "title", "account_language", "account_text_ref") VALUES (?, ?, ?, ?)  -- {"situation_id": "PROBE-3477", "title": "PROBE-3478", "account_language": null, "account_text_ref": "PROBE-3479"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: situations.account_language`
**Verdict:** `OK`

### [0990] A7/OFF — situations.account_text_ref   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "situations" ("situation_id", "title", "account_language", "account_text_ref") VALUES (?, ?, ?, ?)  -- {"situation_id": "PROBE-3480", "title": "PROBE-3481", "account_language": "PROBE-3482", "account_text_ref": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: situations.account_text_ref`
**Verdict:** `OK`

### [0991] A7/OFF — slugs.topic_directory   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-3483", "topic_directory": null, "sl_path": "PROBE-3484", "bpc_path": "PROBE-3485", "status": "ACTIVE", "created_at": "PROBE-3486", "created_by_session": "PROBE-3487", "updated_at": "PROBE-3488", "updated_by_session": "PROBE-3489"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.topic_directory`
**Verdict:** `OK`

### [0992] A7/OFF — slugs.sl_path   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-3490", "topic_directory": "PROBE-3491", "sl_path": null, "bpc_path": "PROBE-3492", "status": "ACTIVE", "created_at": "PROBE-3493", "created_by_session": "PROBE-3494", "updated_at": "PROBE-3495", "updated_by_session": "PROBE-3496"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.sl_path`
**Verdict:** `OK`

### [0993] A7/OFF — slugs.bpc_path   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-3497", "topic_directory": "PROBE-3498", "sl_path": "PROBE-3499", "bpc_path": null, "status": "ACTIVE", "created_at": "PROBE-3500", "created_by_session": "PROBE-3501", "updated_at": "PROBE-3502", "updated_by_session": "PROBE-3503"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.bpc_path`
**Verdict:** `OK`

### [0994] A7/OFF — slugs.status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-3504", "topic_directory": "PROBE-3505", "sl_path": "PROBE-3506", "bpc_path": "PROBE-3507", "status": null, "created_at": "PROBE-3508", "created_by_session": "PROBE-3509", "updated_at": "PROBE-3510", "updated_by_session": "PROBE-3511"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.status`
**Verdict:** `OK`

### [0995] A7/OFF — slugs.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-3512", "topic_directory": "PROBE-3513", "sl_path": "PROBE-3514", "bpc_path": "PROBE-3515", "status": "ACTIVE", "created_at": null, "created_by_session": "PROBE-3516", "updated_at": "PROBE-3517", "updated_by_session": "PROBE-3518"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.created_at`
**Verdict:** `OK`

### [0996] A7/OFF — slugs.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-3519", "topic_directory": "PROBE-3520", "sl_path": "PROBE-3521", "bpc_path": "PROBE-3522", "status": "ACTIVE", "created_at": "PROBE-3523", "created_by_session": null, "updated_at": "PROBE-3524", "updated_by_session": "PROBE-3525"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.created_by_session`
**Verdict:** `OK`

### [0997] A7/OFF — slugs.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-3526", "topic_directory": "PROBE-3527", "sl_path": "PROBE-3528", "bpc_path": "PROBE-3529", "status": "ACTIVE", "created_at": "PROBE-3530", "created_by_session": "PROBE-3531", "updated_at": null, "updated_by_session": "PROBE-3532"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.updated_at`
**Verdict:** `OK`

### [0998] A7/OFF — slugs.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "slugs" ("slug", "topic_directory", "sl_path", "bpc_path", "status", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"slug": "PROBE-3533", "topic_directory": "PROBE-3534", "sl_path": "PROBE-3535", "bpc_path": "PROBE-3536", "status": "ACTIVE", "created_at": "PROBE-3537", "created_by_session": "PROBE-3538", "updated_at": "PROBE-3539", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: slugs.updated_by_session`
**Verdict:** `OK`

### [0999] A7/OFF — source_locators.recovered_from   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_locators" ("ref_id", "pmcid", "pmid", "url", "standard_number", "doi", "isbn", "issn", "recovered_from") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-3540", "pmcid": "PROBE-3541", "pmid": "PROBE-3542", "url": "PROBE-3543", "standard_number": "PROBE-3544", "doi": "PROBE-3545", "isbn": "PROBE-3546", "issn": "PROBE-3547", "recovered_from": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_locators.recovered_from`
**Verdict:** `OK`

### [1000] A7/OFF — source_slug_links.local_ref_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "local_ref_id": null, "created_at": "PROBE-3548", "created_by_session": "PROBE-3549", "updated_at": "PROBE-3550", "updated_by_session": "PROBE-3551"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_slug_links.local_ref_id`
**Verdict:** `OK`

### [1001] A7/OFF — source_slug_links.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3552", "created_at": null, "created_by_session": "PROBE-3553", "updated_at": "PROBE-3554", "updated_by_session": "PROBE-3555"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_slug_links.created_at`
**Verdict:** `OK`

### [1002] A7/OFF — source_slug_links.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3556", "created_at": "PROBE-3557", "created_by_session": null, "updated_at": "PROBE-3558", "updated_by_session": "PROBE-3559"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_slug_links.created_by_session`
**Verdict:** `OK`

### [1003] A7/OFF — source_slug_links.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3560", "created_at": "PROBE-3561", "created_by_session": "PROBE-3562", "updated_at": null, "updated_by_session": "PROBE-3563"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_slug_links.updated_at`
**Verdict:** `OK`

### [1004] A7/OFF — source_slug_links.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_slug_links" ("ref_id", "slug", "local_ref_id", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3564", "created_at": "PROBE-3565", "created_by_session": "PROBE-3566", "updated_at": "PROBE-3567", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_slug_links.updated_by_session`
**Verdict:** `OK`

### [1005] A7/OFF — source_value_extractions.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": null, "slug": "PROBE-PK-1241", "parameter": "PROBE-3568", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-3569", "updated_at": "PROBE-3570", "claimed_value": "PROBE-3571"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.ref_id`
**Verdict:** `OK`

### [1006] A7/OFF — source_value_extractions.slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": null, "parameter": "PROBE-3572", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-3573", "updated_at": "PROBE-3574", "claimed_value": "PROBE-3575"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.slug`
**Verdict:** `OK`

### [1007] A7/OFF — source_value_extractions.parameter   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": null, "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-3576", "updated_at": "PROBE-3577", "claimed_value": "PROBE-3578"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.parameter`
**Verdict:** `OK`

### [1008] A7/OFF — source_value_extractions.claim_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-3579", "claim_type": null, "extraction_method": "skim", "created_at": "PROBE-3580", "updated_at": "PROBE-3581", "claimed_value": "PROBE-3582"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.claim_type`
**Verdict:** `OK`

### [1009] A7/OFF — source_value_extractions.extraction_method   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-3583", "claim_type": "numerical", "extraction_method": null, "created_at": "PROBE-3584", "updated_at": "PROBE-3585", "claimed_value": "PROBE-3586"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.extraction_method`
**Verdict:** `OK`

### [1010] A7/OFF — source_value_extractions.extraction_status   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "extraction_status") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-3587", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-3588", "updated_at": "PROBE-3589", "claimed_value": "PROBE-3590", "extraction_status": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.extraction_status`
**Verdict:** `OK`

### [1011] A7/OFF — source_value_extractions.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-3591", "claim_type": "numerical", "extraction_method": "skim", "created_at": null, "updated_at": "PROBE-3592", "claimed_value": "PROBE-3593"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.created_at`
**Verdict:** `OK`

### [1012] A7/OFF — source_value_extractions.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-3594", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-3595", "updated_at": null, "claimed_value": "PROBE-3596"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.updated_at`
**Verdict:** `OK`

### [1013] A7/OFF — source_value_extractions.contested   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "source_value_extractions" ("ref_id", "slug", "parameter", "claim_type", "extraction_method", "created_at", "updated_at", "claimed_value", "contested") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "slug": "PROBE-PK-1241", "parameter": "PROBE-3597", "claim_type": "numerical", "extraction_method": "skim", "created_at": "PROBE-3598", "updated_at": "PROBE-3599", "claimed_value": "PROBE-3600", "contested": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: source_value_extractions.contested`
**Verdict:** `OK`

### [1014] A7/OFF — spec_value_probes.walk_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3601", "walk_id": null, "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-3602", "direction": "up", "population": "PROBE-3603", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-3604", "created_at": "PROBE-3605", "created_by_session": "PROBE-3606"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.walk_id`
**Verdict:** `OK`

### [1015] A7/OFF — spec_value_probes.slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3607", "walk_id": "PROBE-3608", "slug": null, "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-3609", "direction": "up", "population": "PROBE-3610", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-3611", "created_at": "PROBE-3612", "created_by_session": "PROBE-3613"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.slug`
**Verdict:** `OK`

### [1016] A7/OFF — spec_value_probes.item_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3614", "walk_id": "PROBE-3615", "slug": "PROBE-PK-1241", "item_code": null, "spec_value_origin": 1.0, "spec_unit": "PROBE-3616", "direction": "up", "population": "PROBE-3617", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-3618", "created_at": "PROBE-3619", "created_by_session": "PROBE-3620"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.item_code`
**Verdict:** `OK`

### [1017] A7/OFF — spec_value_probes.spec_value_origin   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3621", "walk_id": "PROBE-3622", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": null, "spec_unit": "PROBE-3623", "direction": "up", "population": "PROBE-3624", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-3625", "created_at": "PROBE-3626", "created_by_session": "PROBE-3627"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.spec_value_origin`
**Verdict:** `OK`

### [1018] A7/OFF — spec_value_probes.spec_unit   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3628", "walk_id": "PROBE-3629", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": null, "direction": "up", "population": "PROBE-3630", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-3631", "created_at": "PROBE-3632", "created_by_session": "PROBE-3633"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.spec_unit`
**Verdict:** `OK`

### [1019] A7/OFF — spec_value_probes.direction   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3634", "walk_id": "PROBE-3635", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-3636", "direction": null, "population": "PROBE-3637", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-3638", "created_at": "PROBE-3639", "created_by_session": "PROBE-3640"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.direction`
**Verdict:** `OK`

### [1020] A7/OFF — spec_value_probes.population   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3641", "walk_id": "PROBE-3642", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-3643", "direction": "up", "population": null, "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-3644", "created_at": "PROBE-3645", "created_by_session": "PROBE-3646"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.population`
**Verdict:** `OK`

### [1021] A7/OFF — spec_value_probes.claim_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3647", "walk_id": "PROBE-3648", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-3649", "direction": "up", "population": "PROBE-3650", "claim_type": null, "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-3651", "created_at": "PROBE-3652", "created_by_session": "PROBE-3653"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.claim_type`
**Verdict:** `OK`

### [1022] A7/OFF — spec_value_probes.step_index   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3654", "walk_id": "PROBE-3655", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-3656", "direction": "up", "population": "PROBE-3657", "claim_type": "minimum", "step_index": null, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-3658", "created_at": "PROBE-3659", "created_by_session": "PROBE-3660"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.step_index`
**Verdict:** `OK`

### [1023] A7/OFF — spec_value_probes.phase   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3661", "walk_id": "PROBE-3662", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-3663", "direction": "up", "population": "PROBE-3664", "claim_type": "minimum", "step_index": 1, "phase": null, "step_value": 1.0, "step_value_unit": "PROBE-3665", "created_at": "PROBE-3666", "created_by_session": "PROBE-3667"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.phase`
**Verdict:** `OK`

### [1024] A7/OFF — spec_value_probes.step_value   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3668", "walk_id": "PROBE-3669", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-3670", "direction": "up", "population": "PROBE-3671", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": null, "step_value_unit": "PROBE-3672", "created_at": "PROBE-3673", "created_by_session": "PROBE-3674"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.step_value`
**Verdict:** `OK`

### [1025] A7/OFF — spec_value_probes.step_value_unit   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3675", "walk_id": "PROBE-3676", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-3677", "direction": "up", "population": "PROBE-3678", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": null, "created_at": "PROBE-3679", "created_by_session": "PROBE-3680"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.step_value_unit`
**Verdict:** `OK`

### [1026] A7/OFF — spec_value_probes.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3681", "walk_id": "PROBE-3682", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-3683", "direction": "up", "population": "PROBE-3684", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-3685", "created_at": null, "created_by_session": "PROBE-3686"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.created_at`
**Verdict:** `OK`

### [1027] A7/OFF — spec_value_probes.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "spec_value_probes" ("probe_id", "walk_id", "slug", "item_code", "spec_value_origin", "spec_unit", "direction", "population", "claim_type", "step_index", "phase", "step_value", "step_value_unit", "created_at", "created_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"probe_id": "PROBE-3687", "walk_id": "PROBE-3688", "slug": "PROBE-PK-1241", "item_code": "A-01", "spec_value_origin": 1.0, "spec_unit": "PROBE-3689", "direction": "up", "population": "PROBE-3690", "claim_type": "minimum", "step_index": 1, "phase": "outer-pass-1st", "step_value": 1.0, "step_value_unit": "PROBE-3691", "created_at": "PROBE-3692", "created_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: spec_value_probes.created_by_session`
**Verdict:** `OK`

### [1028] A7/OFF — specification_source_links.role   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "specification_source_links" ("ref_id", "specification_id", "role") VALUES (?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "specification_id": 1, "role": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specification_source_links.role`
**Verdict:** `OK`

### [1029] A7/OFF — specifications.item_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state") VALUES (?, ?, ?)  -- {"item_code": null, "population_code": "BLIND", "state": "stated"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.item_code`
**Verdict:** `OK`

### [1030] A7/OFF — specifications.population_code   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state") VALUES (?, ?, ?)  -- {"item_code": "I-03", "population_code": null, "state": "stated"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.population_code`
**Verdict:** `OK`

### [1031] A7/OFF — specifications.state   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state") VALUES (?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.state`
**Verdict:** `OK`

### [1032] A7/OFF — specifications.code_floor_only   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "code_floor_only") VALUES (?, ?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": "stated", "code_floor_only": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.code_floor_only`
**Verdict:** `OK`

### [1033] A7/OFF — specifications.has_unverified_sources   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "has_unverified_sources") VALUES (?, ?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": "stated", "has_unverified_sources": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.has_unverified_sources`
**Verdict:** `OK`

### [1034] A7/OFF — specifications.all_sources_disqualified   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "all_sources_disqualified") VALUES (?, ?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": "stated", "all_sources_disqualified": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.all_sources_disqualified`
**Verdict:** `OK`

### [1035] A7/OFF — specifications.regulatory_stratum_only   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state", "regulatory_stratum_only") VALUES (?, ?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": "stated", "regulatory_stratum_only": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: specifications.regulatory_stratum_only`
**Verdict:** `OK`

### [1036] A7/OFF — supersession_check.slug   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-3693", "slug": null, "local_ref_id": "PROBE-3694", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-3695", "outcome": "current_best", "search_strategy_record": "PROBE-3696", "checked_at": "PROBE-3697", "checked_by_session": "PROBE-3698", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.slug`
**Verdict:** `OK`

### [1037] A7/OFF — supersession_check.local_ref_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-3699", "slug": "PROBE-PK-1241", "local_ref_id": null, "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-3700", "outcome": "current_best", "search_strategy_record": "PROBE-3701", "checked_at": "PROBE-3702", "checked_by_session": "PROBE-3703", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.local_ref_id`
**Verdict:** `OK`

### [1038] A7/OFF — supersession_check.ref_id   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-3704", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3705", "ref_id": null, "anchor_tier": 1, "anchor_evidence_type": "PROBE-3706", "outcome": "current_best", "search_strategy_record": "PROBE-3707", "checked_at": "PROBE-3708", "checked_by_session": "PROBE-3709", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.ref_id`
**Verdict:** `OK`

### [1039] A7/OFF — supersession_check.anchor_tier   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-3710", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3711", "ref_id": "PROBE-PK-1012", "anchor_tier": null, "anchor_evidence_type": "PROBE-3712", "outcome": "current_best", "search_strategy_record": "PROBE-3713", "checked_at": "PROBE-3714", "checked_by_session": "PROBE-3715", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.anchor_tier`
**Verdict:** `OK`

### [1040] A7/OFF — supersession_check.anchor_evidence_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-3716", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3717", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": null, "outcome": "current_best", "search_strategy_record": "PROBE-3718", "checked_at": "PROBE-3719", "checked_by_session": "PROBE-3720", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.anchor_evidence_type`
**Verdict:** `OK`

### [1041] A7/OFF — supersession_check.outcome   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-3721", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3722", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-3723", "outcome": null, "search_strategy_record": "PROBE-3724", "checked_at": "PROBE-3725", "checked_by_session": "PROBE-3726", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.outcome`
**Verdict:** `OK`

### [1042] A7/OFF — supersession_check.search_strategy_record   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-3727", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3728", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-3729", "outcome": "current_best", "search_strategy_record": null, "checked_at": "PROBE-3730", "checked_by_session": "PROBE-3731", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.search_strategy_record`
**Verdict:** `OK`

### [1043] A7/OFF — supersession_check.candidates_returned   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method", "candidates_returned") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-3732", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3733", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-3734", "outcome": "current_best", "search_strategy_record": "PROBE-3735", "checked_at": "PROBE-3736", "checked_by_session": "PROBE-3737", "check_method": "pubmed_search", "candidates_returned": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.candidates_returned`
**Verdict:** `OK`

### [1044] A7/OFF — supersession_check.candidates_reviewed   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method", "candidates_reviewed") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-3738", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3739", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-3740", "outcome": "current_best", "search_strategy_record": "PROBE-3741", "checked_at": "PROBE-3742", "checked_by_session": "PROBE-3743", "check_method": "pubmed_search", "candidates_reviewed": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.candidates_reviewed`
**Verdict:** `OK`

### [1045] A7/OFF — supersession_check.checked_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-3744", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3745", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-3746", "outcome": "current_best", "search_strategy_record": "PROBE-3747", "checked_at": null, "checked_by_session": "PROBE-3748", "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.checked_at`
**Verdict:** `OK`

### [1046] A7/OFF — supersession_check.checked_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-3749", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3750", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-3751", "outcome": "current_best", "search_strategy_record": "PROBE-3752", "checked_at": "PROBE-3753", "checked_by_session": null, "check_method": "pubmed_search"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.checked_by_session`
**Verdict:** `OK`

### [1047] A7/OFF — supersession_check.check_method   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "supersession_check" ("check_id", "slug", "local_ref_id", "ref_id", "anchor_tier", "anchor_evidence_type", "outcome", "search_strategy_record", "checked_at", "checked_by_session", "check_method") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  -- {"check_id": "PROBE-3754", "slug": "PROBE-PK-1241", "local_ref_id": "PROBE-3755", "ref_id": "PROBE-PK-1012", "anchor_tier": 1, "anchor_evidence_type": "PROBE-3756", "outcome": "current_best", "search_strategy_record": "PROBE-3757", "checked_at": "PROBE-3758", "checked_by_session": "PROBE-3759", "check_method": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: supersession_check.check_method`
**Verdict:** `OK`

### [1048] A7/OFF — term_aliases.alias_type   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "alias": "PROBE-3760", "language": "PROBE-3761", "alias_type": null, "created_at": "PROBE-3762", "created_by_session": "PROBE-3763", "updated_at": "PROBE-3764", "updated_by_session": "PROBE-3765"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_aliases.alias_type`
**Verdict:** `OK`

### [1049] A7/OFF — term_aliases.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "alias": "PROBE-3766", "language": "PROBE-3767", "alias_type": "SYNONYM", "created_at": null, "created_by_session": "PROBE-3768", "updated_at": "PROBE-3769", "updated_by_session": "PROBE-3770"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_aliases.created_at`
**Verdict:** `OK`

### [1050] A7/OFF — term_aliases.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "alias": "PROBE-3771", "language": "PROBE-3772", "alias_type": "SYNONYM", "created_at": "PROBE-3773", "created_by_session": null, "updated_at": "PROBE-3774", "updated_by_session": "PROBE-3775"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_aliases.created_by_session`
**Verdict:** `OK`

### [1051] A7/OFF — term_aliases.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "alias": "PROBE-3776", "language": "PROBE-3777", "alias_type": "SYNONYM", "created_at": "PROBE-3778", "created_by_session": "PROBE-3779", "updated_at": null, "updated_by_session": "PROBE-3780"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_aliases.updated_at`
**Verdict:** `OK`

### [1052] A7/OFF — term_aliases.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "term_aliases" ("term_id", "alias", "language", "alias_type", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "alias": "PROBE-3781", "language": "PROBE-3782", "alias_type": "SYNONYM", "created_at": "PROBE-3783", "created_by_session": "PROBE-3784", "updated_at": "PROBE-3785", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_aliases.updated_by_session`
**Verdict:** `OK`

### [1053] A7/OFF — term_item_links.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "term_item_links" ("term_id", "item_code", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "item_code": "A-01", "created_at": null, "created_by_session": "PROBE-3786", "updated_at": "PROBE-3787", "updated_by_session": "PROBE-3788"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_item_links.created_at`
**Verdict:** `OK`

### [1054] A7/OFF — term_item_links.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "term_item_links" ("term_id", "item_code", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "item_code": "A-01", "created_at": "PROBE-3789", "created_by_session": null, "updated_at": "PROBE-3790", "updated_by_session": "PROBE-3791"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_item_links.created_by_session`
**Verdict:** `OK`

### [1055] A7/OFF — term_item_links.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "term_item_links" ("term_id", "item_code", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "item_code": "A-01", "created_at": "PROBE-3792", "created_by_session": "PROBE-3793", "updated_at": null, "updated_by_session": "PROBE-3794"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_item_links.updated_at`
**Verdict:** `OK`

### [1056] A7/OFF — term_item_links.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "term_item_links" ("term_id", "item_code", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "TERM-001", "item_code": "A-01", "created_at": "PROBE-3795", "created_by_session": "PROBE-3796", "updated_at": "PROBE-3797", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: term_item_links.updated_by_session`
**Verdict:** `OK`

### [1057] A7/OFF — terms.canonical_en   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "terms" ("term_id", "canonical_en", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-3799", "canonical_en": null, "created_at": "PROBE-3800", "created_by_session": "PROBE-3801", "updated_at": "PROBE-3802", "updated_by_session": "PROBE-3803"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: terms.canonical_en`
**Verdict:** `OK`

### [1058] A7/OFF — terms.created_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "terms" ("term_id", "canonical_en", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-3804", "canonical_en": "PROBE-3805", "created_at": null, "created_by_session": "PROBE-3806", "updated_at": "PROBE-3807", "updated_by_session": "PROBE-3808"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: terms.created_at`
**Verdict:** `OK`

### [1059] A7/OFF — terms.created_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "terms" ("term_id", "canonical_en", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-3809", "canonical_en": "PROBE-3810", "created_at": "PROBE-3811", "created_by_session": null, "updated_at": "PROBE-3812", "updated_by_session": "PROBE-3813"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: terms.created_by_session`
**Verdict:** `OK`

### [1060] A7/OFF — terms.updated_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "terms" ("term_id", "canonical_en", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-3814", "canonical_en": "PROBE-3815", "created_at": "PROBE-3816", "created_by_session": "PROBE-3817", "updated_at": null, "updated_by_session": "PROBE-3818"}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: terms.updated_at`
**Verdict:** `OK`

### [1061] A7/OFF — terms.updated_by_session   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "terms" ("term_id", "canonical_en", "created_at", "created_by_session", "updated_at", "updated_by_session") VALUES (?, ?, ?, ?, ?, ?)  -- {"term_id": "PROBE-3819", "canonical_en": "PROBE-3820", "created_at": "PROBE-3821", "created_by_session": "PROBE-3822", "updated_at": "PROBE-3823", "updated_by_session": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: terms.updated_by_session`
**Verdict:** `OK`

### [1062] A7/OFF — url_verification_runs.started_at   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "url_verification_runs" ("run_id", "started_at") VALUES (?, ?)  -- {"run_id": "PROBE-3825", "started_at": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: url_verification_runs.started_at`
**Verdict:** `OK`

### [1063] A7/OFF — weighting_profile.tier_weights   `2026-08-12 08:35:28Z`
**Action:** insert explicit NULL into NOT NULL column (FK=OFF)
**SQL:**
```sql
INSERT INTO "weighting_profile" ("audience", "use_pattern", "tier_weights") VALUES (?, ?, ?)  -- {"audience": "PROBE-3826", "use_pattern": "PROBE-3827", "tier_weights": null}
```
**Expected:** NOT NULL constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: NOT NULL constraint failed: weighting_profile.tier_weights`
**Verdict:** `OK`

### A8 — UNIQUE battery (5 UNIQUE indexes), FK=ON and FK=OFF

### [1064] A8/ON — evidence_source_authors UNIQUE(ref_id, position, role)   `2026-08-12 08:35:28Z`
**Action:** insert second row duplicating the unique key (FK=ON)
**SQL:**
```sql
INSERT INTO "evidence_source_authors" ("ref_id", "position", "role") VALUES (?, ?, ?)  -- {"ref_id": "PROBE-PK-167", "position": 1, "role": "PROBE-UQ-3828"}
```
**Expected:** UNIQUE constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: UNIQUE constraint failed: evidence_source_authors.ref_id, evidence_source_authors.position, evidence_source_authors.role`
**Verdict:** `OK`

### [1065] A8/ON — item_population_elaborations UNIQUE(item_code, population_code, variant_distinction)   `2026-08-12 08:35:28Z`
**Action:** insert second row duplicating the unique key (FK=ON)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("item_code", "population_code", "variant_distinction") VALUES (?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "variant_distinction": "PROBE-UQ-3829"}
```
**Expected:** UNIQUE constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: UNIQUE constraint failed: item_population_elaborations.item_code, item_population_elaborations.population_code, item_population_elaborations.variant_distinction`
**Verdict:** `OK`

### [1066] A8/ON — items UNIQUE(item_id)   `2026-08-12 08:35:28Z`
**Action:** insert second row duplicating the unique key (FK=ON)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session", "item_id") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-3832", "category": "A", "name": "PROBE-3833", "created_at": "PROBE-3834", "created_by_session": "PROBE-3835", "updated_at": "PROBE-3836", "updated_by_session": "PROBE-3837", "item_id": "PROBE-UQ-3830"}
```
**Expected:** UNIQUE constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: UNIQUE constraint failed: items.item_id`
**Verdict:** `OK`

### [1067] A8/ON — jurisdictional_values UNIQUE(item_code, jurisdiction, standard_name)   `2026-08-12 08:35:28Z`
**Action:** insert second row duplicating the unique key (FK=ON)
**SQL:**
```sql
INSERT INTO "jurisdictional_values" ("item_code", "jurisdiction", "standard_name") VALUES (?, ?, ?)  -- {"item_code": "A-01", "jurisdiction": "PROBE-UQ-3838", "standard_name": "PROBE-UQ-3839"}
```
**Expected:** UNIQUE constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: UNIQUE constraint failed: jurisdictional_values.item_code, jurisdictional_values.jurisdiction, jurisdictional_values.standard_name`
**Verdict:** `OK`

### [1068] A8/ON — specifications UNIQUE(item_code, population_code)   `2026-08-12 08:35:28Z`
**Action:** insert second row duplicating the unique key (FK=ON)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state") VALUES (?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "state": "stated"}
```
**Expected:** UNIQUE constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: UNIQUE constraint failed: specifications.item_code, specifications.population_code`
**Verdict:** `OK`

### [1069] A8/OFF — evidence_source_authors UNIQUE(ref_id, position, role)   `2026-08-12 08:35:28Z`
**Action:** insert second row duplicating the unique key (FK=OFF)
**SQL:**
```sql
INSERT INTO "evidence_source_authors" ("ref_id", "position", "role") VALUES (?, ?, ?)  -- {"ref_id": "PROBE-PK-1012", "position": 1, "role": "PROBE-UQ-3840"}
```
**Expected:** UNIQUE constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: UNIQUE constraint failed: evidence_source_authors.ref_id, evidence_source_authors.position, evidence_source_authors.role`
**Verdict:** `OK`

### [1070] A8/OFF — item_population_elaborations UNIQUE(item_code, population_code, variant_distinction)   `2026-08-12 08:35:28Z`
**Action:** insert second row duplicating the unique key (FK=OFF)
**SQL:**
```sql
INSERT INTO "item_population_elaborations" ("item_code", "population_code", "variant_distinction") VALUES (?, ?, ?)  -- {"item_code": "A-01", "population_code": "ADHD", "variant_distinction": "PROBE-UQ-3841"}
```
**Expected:** UNIQUE constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: UNIQUE constraint failed: item_population_elaborations.item_code, item_population_elaborations.population_code, item_population_elaborations.variant_distinction`
**Verdict:** `OK`

### [1071] A8/OFF — items UNIQUE(item_id)   `2026-08-12 08:35:28Z`
**Action:** insert second row duplicating the unique key (FK=OFF)
**SQL:**
```sql
INSERT INTO "items" ("item_code", "category", "name", "created_at", "created_by_session", "updated_at", "updated_by_session", "item_id") VALUES (?, ?, ?, ?, ?, ?, ?, ?)  -- {"item_code": "PROBE-3844", "category": "A", "name": "PROBE-3845", "created_at": "PROBE-3846", "created_by_session": "PROBE-3847", "updated_at": "PROBE-3848", "updated_by_session": "PROBE-3849", "item_id": "PROBE-UQ-3842"}
```
**Expected:** UNIQUE constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: UNIQUE constraint failed: items.item_id`
**Verdict:** `OK`

### [1072] A8/OFF — jurisdictional_values UNIQUE(item_code, jurisdiction, standard_name)   `2026-08-12 08:35:28Z`
**Action:** insert second row duplicating the unique key (FK=OFF)
**SQL:**
```sql
INSERT INTO "jurisdictional_values" ("item_code", "jurisdiction", "standard_name") VALUES (?, ?, ?)  -- {"item_code": "A-01", "jurisdiction": "PROBE-UQ-3850", "standard_name": "PROBE-UQ-3851"}
```
**Expected:** UNIQUE constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: UNIQUE constraint failed: jurisdictional_values.item_code, jurisdictional_values.jurisdiction, jurisdictional_values.standard_name`
**Verdict:** `OK`

### [1073] A8/OFF — specifications UNIQUE(item_code, population_code)   `2026-08-12 08:35:28Z`
**Action:** insert second row duplicating the unique key (FK=OFF)
**SQL:**
```sql
INSERT INTO "specifications" ("item_code", "population_code", "state") VALUES (?, ?, ?)  -- {"item_code": "I-03", "population_code": "BLIND", "state": "stated"}
```
**Expected:** UNIQUE constraint failed
**Actual:** rejected
**Exception:** `IntegrityError: UNIQUE constraint failed: specifications.item_code, specifications.population_code`
**Verdict:** `OK`

**SWEEP A EXAMINED:** 80/80 edges enumerated · 89 orphan queries · FK bad-value ON 80/80 {'OK': 80, 'SILENT-PASS': 0, 'BLOCKED': 0} · NULL-path 18/18 {'SILENT-PASS': 18, 'BLOCKED': 0, 'OK': 0} · FK bad-value OFF 80/80 {'SILENT-PASS': 80, 'BLOCKED': 0, 'OK': 0} · CHECK ON 128/127 {'OK': 127, 'SILENT-PASS': 0, 'BLOCKED': 1} · CHECK OFF 128/127 {'OK': 127, 'SILENT-PASS': 0, 'BLOCKED': 1} · NOT NULL ON 268/267 {'OK': 268, 'SILENT-PASS': 0, 'BLOCKED': 0} · NOT NULL OFF 268/267 {'OK': 268, 'SILENT-PASS': 0, 'BLOCKED': 0} · UNIQUE ON 5/5 {'OK': 5, 'SILENT-PASS': 0, 'BLOCKED': 0} · UNIQUE OFF 5/5 {'OK': 5, 'SILENT-PASS': 0, 'BLOCKED': 0}


---

## SWEEP B — the pipeline spine, forward
Spine: slugs → search_executions → search_admissions → evidence_sources → (source_slug_links, source_value_extractions, evidence_population_match) → specifications → specification_source_links → render. Scratch copy `probe-spine.db`, foreign_keys=ON, synthetic rows PROBE-prefixed.

### [1074] B — search_executions (OUT OF ORDER)   `2026-08-12 08:35:28Z`
**Action:** insert execution for a slug that does not exist yet
**SQL:**
```sql
INSERT INTO search_executions (slug, language, query_text, engine, depth_method, session, executed_at) VALUES (?,?,?,?,?,?,?)  -- params: ["PROBE-slug-a", "en", "PROBE query", "manual", "scoping", "PROBE-session", "2026-08-12T00:00:00+00:00"]
```
**Expected:** rejected — slug FK
**Actual:** rejected
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [1075] B — slugs   `2026-08-12 08:35:28Z`
**Action:** create spine root PROBE-slug-a
**SQL:**
```sql
INSERT INTO slugs (slug, topic_directory, sl_path, bpc_path, status, created_at, created_by_session, updated_at, updated_by_session) VALUES (?,?,?,?,?,?,?,?,?)  -- params: ["PROBE-slug-a", "PROBE-topic", "PROBE/sl.md", "PROBE/bpc.md", "ACTIVE", "2026-08-12T00:00:00+00:00", "PROBE-session", "2026-08-12T00:00:00+00:00", "PROBE-session"]
```
**Expected:** accepted
**Actual:** accepted (rowid 107) — key carried forward: slug (TEXT). Nothing forces sl_path/bpc_path to exist on disk — dangling paths accepted silently
**Verdict:** `OK`

### [1076] B — search_executions   `2026-08-12 08:35:28Z`
**Action:** insert execution against PROBE-slug-a, admitted_ref_ids naming a ref that does not exist
**SQL:**
```sql
INSERT INTO search_executions (slug, language, query_text, engine, depth_method, results_found, results_screened, results_admitted, session, executed_at, admitted_ref_ids) VALUES (?,?,?,?,?,?,?,?,?,?,?)  -- params: ["PROBE-slug-a", "en", "PROBE query text", "manual", "scoping", 5, 5, 1, "PROBE-session", "2026-08-12T00:00:00+00:00", "[\"PROBE-REF-99901\"]"]
```
**Expected:** accepted
**Actual:** accepted (rowid 1) — key carried: exec_id (INTEGER PK). admitted_ref_ids is JSON — json_valid() is the only check; the dangling ref is accepted
**Verdict:** `OK`

### [1077] B — search_executions.admitted_ref_ids   `2026-08-12 08:35:28Z`
**Action:** verify the dangling JSON ref was accepted
**Expected:** a ref named in admitted_ref_ids should exist in evidence_sources
**Actual:** accepted with PROBE-REF-99901 not existing anywhere — the JSON leg of the dual store is unconstrained
**Verdict:** **`SILENT-PASS`**

### [1078] B — search_admissions (OUT OF ORDER)   `2026-08-12 08:35:28Z`
**Action:** admit a ref before the evidence source exists
**SQL:**
```sql
INSERT INTO search_admissions (exec_id, ref_id, created_at, created_by_session) VALUES (?,?,?,?)  -- params: [1, "PROBE-REF-99901", "2026-08-12T00:00:00+00:00", "PROBE-session"]
```
**Expected:** rejected — ref FK
**Actual:** rejected
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [1079] B — search_admissions (OUT OF ORDER)   `2026-08-12 08:35:28Z`
**Action:** admit under a nonexistent exec_id
**SQL:**
```sql
INSERT INTO search_admissions (exec_id, ref_id, created_at, created_by_session) VALUES (?,?,?,?)  -- params: [999999901, "PROBE-REF-99901", "2026-08-12T00:00:00+00:00", "PROBE-session"]
```
**Expected:** rejected — exec FK
**Actual:** rejected
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [1080] B — evidence_sources   `2026-08-12 08:35:28Z`
**Action:** create PROBE evidence source with NOTHING but a ref_id
**SQL:**
```sql
INSERT INTO evidence_sources (ref_id) VALUES (?)  -- params: ["PROBE-REF-99901"]
```
**Expected:** accepted
**Actual:** accepted (rowid 1) — every other column is nullable: no tier, no title, no verification_status, no type required. A source can enter the corpus completely empty — silently lost: everything about it
**Verdict:** `OK`

### [1081] B — evidence_sources   `2026-08-12 08:35:28Z`
**Action:** second source for the backward walk
**SQL:**
```sql
INSERT INTO evidence_sources (ref_id, tier, pub_title, verification_status) VALUES (?,?,?,?)  -- params: ["PROBE-REF-99902", 6, "PROBE Building Code", "verified"]
```
**Expected:** accepted
**Actual:** accepted (rowid 2)
**Verdict:** `OK`

### [1082] B — search_admissions   `2026-08-12 08:35:28Z`
**Action:** admit PROBE-REF-99901 under the real exec_id
**SQL:**
```sql
INSERT INTO search_admissions (exec_id, ref_id, created_at, created_by_session) VALUES (?,?,?,?)  -- params: [1, "PROBE-REF-99901", "2026-08-12T00:00:00+00:00", "PROBE-session"]
```
**Expected:** accepted
**Actual:** accepted (rowid 1) — key carried: (exec_id, ref_id). Nothing reconciles this table with search_executions.admitted_ref_ids / results_admitted
**Verdict:** `OK`

### [1083] B — search_executions ↔ search_admissions dual store   `2026-08-12 08:35:28Z`
**Action:** set results_admitted=0 while a search_admissions row exists for the same exec
**SQL:**
```sql
UPDATE search_executions SET results_admitted = 0 WHERE exec_id = ?
```
**Expected:** some constraint or trigger reconciles the count
**Actual:** accepted: results_admitted=0 while search_admissions holds 1 row(s). No trigger, no check — divergence is silent
**Verdict:** **`SILENT-PASS`**

### [1084] B — source_slug_links (OUT OF ORDER)   `2026-08-12 08:35:28Z`
**Action:** link a nonexistent ref to the slug
**SQL:**
```sql
INSERT INTO source_slug_links (ref_id, slug, local_ref_id, created_at, created_by_session, updated_at, updated_by_session) VALUES (?,?,?,?,?,?,?)  -- params: ["PROBE-REF-NOPE", "PROBE-slug-a", "L1", "2026-08-12T00:00:00+00:00", "PROBE-session", "2026-08-12T00:00:00+00:00", "PROBE-session"]
```
**Expected:** rejected
**Actual:** rejected
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [1085] B — source_slug_links   `2026-08-12 08:35:28Z`
**Action:** link PROBE-REF-99901 ↔ PROBE-slug-a
**SQL:**
```sql
INSERT INTO source_slug_links (ref_id, slug, local_ref_id, created_at, created_by_session, updated_at, updated_by_session) VALUES (?,?,?,?,?,?,?)  -- params: ["PROBE-REF-99901", "PROBE-slug-a", "L1", "2026-08-12T00:00:00+00:00", "PROBE-session", "2026-08-12T00:00:00+00:00", "PROBE-session"]
```
**Expected:** accepted
**Actual:** accepted (rowid 1) — key carried: ref_id + slug. An evidence source needs NO search_execution and NO admission to acquire links — the whole search stage is bypassable, silently
**Verdict:** `OK`

### [1086] B — source_value_extractions   `2026-08-12 08:35:28Z`
**Action:** extraction from PROBE-REF-99901 with full locator, item_code left NULL
**SQL:**
```sql
INSERT INTO source_value_extractions (ref_id, slug, parameter, claim_type, claimed_value, claim_text, source_section, extraction_method, extraction_status, created_at, updated_at, item_code, population_code, locator_scheme, loc_section, loc_clause) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)  -- params: ["PROBE-REF-99901", "PROBE-slug-a", "PROBE corridor width", "numerical", "1500", "PROBE claim text", "\u00a75.7", "skim", "preliminary", "2026-08-12T00:00:00+00:00", "2026-08-12T00:00:00+00:00", null, null, "din", "5", "5.7"]
```
**Expected:** accepted
**Actual:** accepted (rowid 1) — item_code and population_code are NULLABLE and left NULL — the extraction is now unreachable from any cell by structured join; only ref_id carries forward
**Verdict:** `OK`

### [1087] B — evidence_population_match   `2026-08-12 08:35:28Z`
**Action:** match row with source_ref garbage + ref_id NULL (dual identity)
**SQL:**
```sql
INSERT INTO evidence_population_match (match_id, source_ref, target_population, match_grade, created_at, created_by_session) VALUES (?,?,?,?,?,?)  -- params: ["PROBE-MATCH-1", "PROBE-TOTALLY-FAKE-REF", "PROBE-POP-X", "EXACT", "2026-08-12T00:00:00+00:00", "PROBE-session"]
```
**Expected:** should be rejected — source_ref AND target_population both dangle
**Actual:** accepted (rowid 1)
**Verdict:** **`SILENT-PASS`**

### [1088] B — specifications (OUT OF ORDER)   `2026-08-12 08:35:28Z`
**Action:** cell for an item that does not exist
**SQL:**
```sql
INSERT INTO specifications (item_code, population_code, state) VALUES (?,?,?)  -- params: ["PROBE-K-99", "PROBE-POP", "pending"]
```
**Expected:** rejected — item FK
**Actual:** rejected
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [1089] B — items   `2026-08-12 08:35:28Z`
**Action:** synthetic item K-99 (category K)
**SQL:**
```sql
INSERT INTO items (item_code, category, name, status, created_at, created_by_session, updated_at, updated_by_session) VALUES (?,?,?,?,?,?,?,?)  -- params: ["K-99", "K", "PROBE item", "draft", "2026-08-12T00:00:00+00:00", "PROBE-session", "2026-08-12T00:00:00+00:00", "PROBE-session"]
```
**Expected:** accepted
**Actual:** accepted (rowid 94)
**Verdict:** `OK`

### [1090] B — populations   `2026-08-12 08:35:28Z`
**Action:** synthetic population PROBE-POP
**SQL:**
```sql
INSERT INTO populations (population_code, display_name) VALUES (?,?)  -- params: ["PROBE-POP", "PROBE population"]
```
**Expected:** accepted
**Actual:** accepted (rowid 34) — category, parent_code, status all optional — a population can be created outside the taxonomy
**Verdict:** `OK`

### [1091] B — specifications   `2026-08-12 08:35:28Z`
**Action:** STATED cell with NULL governing_refs (doctrine: stated requires non-empty governing_refs)
**SQL:**
```sql
INSERT INTO specifications (item_code, population_code, state, governing_refs, created_at, created_by_session) VALUES (?,?,?,?,?,?)  -- params: ["K-99", "PROBE-POP", "stated", null, "2026-08-12T00:00:00+00:00", "PROBE-session"]
```
**Expected:** should be rejected per the evidence-state machine
**Actual:** accepted (rowid 1)
**Verdict:** **`SILENT-PASS`**

### [1092] B — specifications.governing_refs   `2026-08-12 08:35:28Z`
**Action:** point governing_refs at one PROBE ref and one dangling ref
**SQL:**
```sql
UPDATE specifications SET governing_refs = ? WHERE specification_id = ?  -- params: ["[\"PROBE-REF-99901\", \"REF-DANGLING-00000\"]", 1]
```
**Expected:** the dangling entry should be rejected
**Actual:** accepted (rowid 1)
**Verdict:** **`SILENT-PASS`**

### [1093] B — specification_source_links (OUT OF ORDER)   `2026-08-12 08:35:28Z`
**Action:** link a nonexistent cell
**SQL:**
```sql
INSERT INTO specification_source_links (specification_id, ref_id, role, created_at, created_by_session) VALUES (?,?,?,?,?)  -- params: [999999902, "PROBE-REF-99901", "governing", "2026-08-12T00:00:00+00:00", "PROBE-session"]
```
**Expected:** rejected — cell FK
**Actual:** rejected
**Exception:** `IntegrityError: FOREIGN KEY constraint failed`
**Verdict:** `OK`

### [1094] B — specification_source_links   `2026-08-12 08:35:28Z`
**Action:** governing link cell → PROBE-REF-99901
**SQL:**
```sql
INSERT INTO specification_source_links (specification_id, ref_id, role, created_at, created_by_session) VALUES (?,?,?,?,?)  -- params: [1, "PROBE-REF-99901", "governing", "2026-08-12T00:00:00+00:00", "PROBE-session"]
```
**Expected:** accepted
**Actual:** accepted (rowid 1) — key carried: specification_id + ref_id; role CHECK admits only 'governing'
**Verdict:** `OK`

### [1095] B — specification_source_links vs governing_refs   `2026-08-12 08:35:28Z`
**Action:** the JSON now names 2 refs while specification_source_links holds 1
**Expected:** the two representations should be forced equal
**Actual:** both writes accepted; the stores disagree and nothing reconciles them (compare Sweep C)
**Verdict:** **`SILENT-PASS`**

### [1096] B — render/build_site.py --only K-99   `2026-08-12 08:35:29Z`
**Action:** RENDER stage: python3 scripts/generate/build_site.py --only K-99
**Expected:** renders the PROBE item's spec page from the scratch DB
**Actual:** rc=0; output (trunc): Built 1 page(s) at DB fingerprint 20e7def9d212.
Pages citing at least one governing source: 1 of 1.
**Verdict:** `OK`

### [1097] B — render/build_site.py (full)   `2026-08-12 08:35:29Z`
**Action:** RENDER stage: python3 scripts/generate/build_site.py
**Expected:** renders all spec pages incl. the PROBE cell
**Actual:** rc=0; output (trunc): Built 94 page(s) at DB fingerprint 20e7def9d212.
Pages citing at least one governing source: 1 of 94.
**Verdict:** `OK`

### [1098] B — render/room_page.py R-BA   `2026-08-12 08:35:29Z`
**Action:** RENDER stage: python3 scripts/generate/room_page.py R-BA
**Expected:** expected to FAIL: queries phantom tables (room, room_item, …) — the live table is `rooms` keyed by room_code
**Actual:** rc=1; output (trunc): Traceback (most recent call last):
  File "/tmp/claude-0/-home-user-guidebook/1020731d-bba2-594c-9ca2-0d2b78825e52/scratchpad/probe2/tree/scripts/generate/room_page.py", line 282, in <module>
    main()
  File "/tmp/claude-0/-home-user-guidebook/1020731d-bba2-594c-9ca2-0d2b78825e52/scratchpad/probe2/tree/scripts/generate/room_page.py", line 278, in main
    generate(room_id, output_path)
  File "/tmp/claude-0/-home-user-guidebook/1020731d-bba2-594c-9ca2-0d2b78825e52/scratchpad/probe2/tree/scripts/generate/room_page.py", line 254, in generate
    room = query_room(conn, room_id)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/claude-0/-home-user-guidebook/1020731d-bba2-594c-9ca2-0d2b78825e52/scratchpad/probe2/tree/scripts/generate/room_page.py", line 26, in query_room
    room = conn.execute("SELECT * FROM room WHERE room_id = ?", (room_id,)).fetchone()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such table: room
**Exception:** `/tree/scripts/generate/room_page.py", line 254, in generate
    room = query_room(conn, room_id)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/claude-0/-home-user-guidebook/1020731d-bba2-594c-9ca2-0d2b78825e52/scratchpad/probe2/tree/scripts/generate/room_page.py", line 26, in query_room
    room = conn.execute("SELECT * FROM room WHERE room_id = ?", (room_id,)).fetchone()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such table: room`
**Verdict:** `ERROR`

### [1099] B — render/population_page.py ALL   `2026-08-12 08:35:29Z`
**Action:** RENDER stage: python3 scripts/generate/population_page.py ALL
**Expected:** population page for code ALL from scratch DB
**Actual:** rc=0; output (trunc): Generated: /tmp/claude-0/-home-user-guidebook/1020731d-bba2-594c-9ca2-0d2b78825e52/scratchpad/probe2/tree/site/populations/all.html (4753 bytes)
**Verdict:** `OK`

**SWEEP B EXAMINED: 26 handoff probes**


---

## SWEEP V — the 18 views (canonical AND PROBE-populated spine copy)

### [1100] V — v_best_practice   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** canonical: 0 rows; spine+PROBE: 1 rows; sample: [(1, 'K-99', 'PROBE-POP', 'stated', None, None, None, None, None, None, None, None, '["PROBE-REF-99901", "REF-DANGLING-00000"]', None, None, 0, None, None, None, None, 0, 0, '2026-08-12T00:00:00+00:00', 'PROBE-session', None, None, 0, 'anchored')]
**Verdict:** `OK`

### [1101] V — v_code_floor_only   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** EXECUTES-EMPTY on both — proves schema validity only; the view's semantics remain unverified (its base tables are empty even after the PROBE spine)
**Verdict:** `BLOCKED`

### [1102] V — v_coverage_branch   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** canonical: 0 rows; spine+PROBE: 1 rows; sample: [('PROBE-slug-a', None, None, None, None, 1, 0)]
**Verdict:** `OK`

### [1103] V — v_coverage_jurisdiction   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** canonical: 0 rows; spine+PROBE: 1 rows; sample: [('PROBE-slug-a', None, 1, 0, 0, None)]
**Verdict:** `OK`

### [1104] V — v_coverage_language   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** canonical: 0 rows; spine+PROBE: 1 rows; sample: [('PROBE-slug-a', 'en', 1, 0)]
**Verdict:** `OK`

### [1105] V — v_coverage_priority   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** canonical: 7210 rows; spine+PROBE: 7280 rows; sample: [('intellectual-disability-built-environment-design', 'AR', 'ES', 'PRIMARY', 5, 0), ('intellectual-disability-built-environment-design', 'AT', 'DE', 'PRIMARY', 5, 0)]
**Verdict:** `OK`

### [1106] V — v_divergence   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** EXECUTES-EMPTY on both — proves schema validity only; the view's semantics remain unverified (its base tables are empty even after the PROBE spine)
**Verdict:** `BLOCKED`

### [1107] V — v_item_extractions   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** EXECUTES-EMPTY on both — proves schema validity only; the view's semantics remain unverified (its base tables are empty even after the PROBE spine)
**Verdict:** `BLOCKED`

### [1108] V — v_item_provenance   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** canonical: 0 rows; spine+PROBE: 1 rows; sample: [('K-99', 'PROBE item', 'K', 1, 'PROBE-POP', 'stated', None, 0, 'governing', 'PROBE-REF-99901', None, None, None, None, None, None, None)]
**Verdict:** `OK`

### [1109] V — v_pending   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** EXECUTES-EMPTY on both — proves schema validity only; the view's semantics remain unverified (its base tables are empty even after the PROBE spine)
**Verdict:** `BLOCKED`

### [1110] V — v_pmp_latest_walk   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** EXECUTES-EMPTY on both — proves schema validity only; the view's semantics remain unverified (its base tables are empty even after the PROBE spine)
**Verdict:** `BLOCKED`

### [1111] V — v_registry_duplicate_descriptions   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** EXECUTES-EMPTY on both — proves schema validity only; the view's semantics remain unverified (its base tables are empty even after the PROBE spine)
**Verdict:** `BLOCKED`

### [1112] V — v_root_id_conflicts   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** EXECUTES-EMPTY on both — proves schema validity only; the view's semantics remain unverified (its base tables are empty even after the PROBE spine)
**Verdict:** `BLOCKED`

### [1113] V — v_source_admission   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** canonical: 0 rows; spine+PROBE: 1 rows; sample: [('PROBE-REF-99901', None, None, None, None, None, 1, 'PROBE-slug-a', 'PROBE query text', 'manual', 'en', None, 'scoping', None, None, 0, 'PROBE-session', '2026-08-12T00:00:00+00:00')]
**Verdict:** `OK`

### [1114] V — v_source_reach   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** canonical: 0 rows; spine+PROBE: 1 rows; sample: [('PROBE-REF-99901', None, None, None, 1, 'K-99', 'PROBE item', 'PROBE-POP', 'stated', 'PROBE-slug-a')]
**Verdict:** `OK`

### [1115] V — v_source_reach_all   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** canonical: 0 rows; spine+PROBE: 2 rows; sample: [('PROBE-REF-99901', None, None, None, 1, 1, 'K-99', 'PROBE item', 'PROBE-POP', 'stated', 'PROBE-slug-a'), ('PROBE-REF-99902', 'PROBE Building Code', 6, 'verified', 0, None, None, None, None, None, None)]
**Verdict:** `OK`

### [1116] V — v_unregistered_roots   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** EXECUTES-EMPTY on both — proves schema validity only; the view's semantics remain unverified (its base tables are empty even after the PROBE spine)
**Verdict:** `BLOCKED`

### [1117] V — v_value_independence   `2026-08-12 08:35:29Z`
**Action:** execute view on canonical and on the PROBE-populated spine copy
**Expected:** executes and returns rows
**Actual:** EXECUTES-EMPTY on both — proves schema validity only; the view's semantics remain unverified (its base tables are empty even after the PROBE spine)
**Verdict:** `BLOCKED`

**SWEEP V EXAMINED: 18/18 views executed**


---

## SWEEP C — the backward walk

### [1118] C — cell → specification_source_links   `2026-08-12 08:35:29Z`
**Action:** resolve links for PROBE cell 1
**Expected:** ≥1 governing ref
**Actual:** refs via csl: ['PROBE-REF-99901']
**Verdict:** `OK`

### [1119] C — specification_source_links → evidence_sources   `2026-08-12 08:35:29Z`
**Action:** resolve refs to sources
**Expected:** all resolve
**Actual:** [('PROBE-REF-99901', None, None)]
**Verdict:** `OK`

### [1120] C — evidence_sources → source_value_extractions (structured join on ref_id+item_code)   `2026-08-12 08:35:29Z`
**Action:** find the extraction backing this cell's value
**SQL:**
```sql
SELECT e.extraction_id, e.ref_id, e.item_code, e.population_code, e.loc_section, e.loc_clause FROM source_value_extractions e WHERE e.ref_id = ? AND e.item_code = ?
```
**Expected:** the extraction row
**Actual:** 0 rows — the extraction exists but its item_code is NULL, so the only structured join from cell to extraction returns nothing. BROKEN JOINT: no table links specifications to source_value_extractions; the join must be improvised on (ref_id, item_code) and item_code is nullable
**Verdict:** `ORPHAN`

### [1121] C — … fallback join on ref_id alone   `2026-08-12 08:35:29Z`
**Action:** extractions for the ref regardless of item
**Expected:** ≥1
**Actual:** [(1, '5', '5.7', '§5.7')] — reachable only by dropping the item join entirely
**Verdict:** `OK`

### [1122] C — source_value_extractions → loc_* → clause   `2026-08-12 08:35:29Z`
**Action:** read the decomposed locator
**Expected:** loc_section/loc_clause populated
**Actual:** loc_section='5', loc_clause='5.7' (set by the probe; live-data density below)
**Verdict:** `OK`

### [1123] C — cell → governing_refs (JSON dual store)   `2026-08-12 08:35:29Z`
**Action:** parse JSON and resolve to evidence_sources
**Expected:** all resolve, and match specification_source_links
**Actual:** JSON names ['PROBE-REF-99901', 'REF-DANGLING-00000']; resolved ['PROBE-REF-99901']; DANGLING ['REF-DANGLING-00000']; csl says ['PROBE-REF-99901'] — the two representations disagree and nothing reconciles them
**Verdict:** `ORPHAN`

### [1124] C — canonical: determined cells, dual-store agreement   `2026-08-12 08:35:29Z`
**Action:** compare sorted governing_refs JSON vs sorted specification_source_links per determined cell
**Expected:** 0 disagreements
**Actual:** determined cells: 0; with csl links: 0; with non-empty governing_refs: 0; cells where the two stores DISAGREE: 0
**Verdict:** `OK`

### [1125] C — canonical: backward funnel cell→ref→extraction→locator   `2026-08-12 08:35:29Z`
**Action:** count survivors at each joint of the backward walk
**Expected:** every determined cell walks back to a clause
**Actual:** governing refs on determined cells: 0 · of those refs, with ANY extraction: 0 · extractions joinable back to their cell via (ref_id,item_code): 0 · extractions with item_code set: 0/0 · extractions with ANY loc_* level populated: 0/0 · with legacy prose source_section: 0/0
**Verdict:** `ORPHAN`

### [1126] C — canonical: jurisdictional_values locator decomposition   `2026-08-12 08:35:29Z`
**Action:** how many rows have decomposed loc_* vs packed standard_name; does the table carry a ref FK at all
**Expected:** decomposed locators, ref-linked
**Actual:** rows: 109; with loc_section/clause: 0; ref_id column present: False (migration 053 notes the table 'has never had' the ref_id FK)
**Verdict:** `ORPHAN`

### [1127] C — renderers: which representation is read   `2026-08-12 08:35:29Z`
**Action:** static inspection (verified again by the Sweep D matrix)
**Expected:** one canonical representation
**Actual:** specification_source_links (role='governing') read by: scripts/generate/build_site.py, scripts/generate/spec_page.py; governing_refs JSON read by: scripts/generate/pilot_renderings.py (parses the JSON, recomputes derivation_sha, cross-counts csl); both read by: scripts/validate_evidence_state.py, scripts/tests/test_db_integrity.py, scripts/assess/assess_cell.py, tools/pipeline_completeness.py
**Verdict:** `OK`

**SWEEP C EXAMINED: 10 joints walked**


---

## SWEEP D — table × script matrix (AST scan + PREPARE verification)

### [1128] D — scan   `2026-08-12 08:35:32Z`
**Action:** AST-parsed 168/168 .py files under scripts/, tools/, schemas/ (+ 353 migration .sql files scanned for writers); 0 unparseable
**Expected:** all files parse
**Actual:** all parsed
**Verdict:** `OK`

### [1129] D — PREPARE verification   `2026-08-12 08:35:32Z`
**Action:** every complete SQL literal prepared (EXPLAIN) against the scratch schema: 1424 statements
**Expected:** all prepare
**Actual:** {'prepared_ok': 772, 'dynamic': 216, 'fragment': 210, 'no_such_table': 142, 'no_such_column': 3, 'other_error': 81, 'statements_total': 1424} · failures: scripts/assess/assess_cell.py:597 view v_best_practice already exists; scripts/audit/graph/extract_content.py:58 no such table: nodes; scripts/audit/graph/model.py:38 no such table: nodes; scripts/audit/graph/model.py:46 no such table: edges; scripts/audit/graph/model.py:53 no such table: edges; scripts/audit/graph/model.py:59 no such table: findings; scripts/audit/graph/model.py:67 no such table: build_meta; scripts/audit/graph/model.py:73 no such table: nodes; scripts/audit/graph/model.py:74 no such table: edges; scripts/audit/graph/model.py:75 no such table: edges; scripts/audit/graph/model.py:76 no such table: findings; scripts/audit/graph/topology.py:209 no such table: nodes; scripts/audit/graph/topology.py:219 no such table: edges; scripts/audit/graph/topology.py:265 no such table: nodes; scripts/audit/graph/topology.py:267 no such table: edges; scripts/audit/graph/topology.py:64 no such table: nodes; scripts/audit/graph/topology.py:80 no such table: edges; scripts/audit/graph/topology.py:94 no such table: edges; scripts/audit/graph/topology.py:124 no such table: edges; scripts/audit/graph/topology.py:149 no such table: edges; scripts/audit/graph/topology.py:168 no such table: edges; scripts/audit/graph/topology.py:187 no such table: nodes; scripts/audit/graph_audit.py:223 no such table: findings; scripts/audit/graph_audit.py:424 table connections already exists; scripts/audit/graph_audit.py:424 table connection_targets already exists; scripts/audit/graph_audit.py:424 table connections has 13 columns but 3 values were supplied; scripts/audit/graph_audit.py:128 no such table: findings; scripts/audit/graph_audit.py:145 no such table: build_meta; scripts/audit/graph_audit.py:181 no such table: findings; scripts/audit/graph_audit.py:190 no such table: findings; scripts/audit/graph_audit.py:342 no such table: zzz_phantom; scripts/audit/graph_audit.py:115 no such table: findings; scripts/audit/graph_audit.py:138 no such table: findings; scripts/audit/graph_audit.py:166 no such table: findings; scripts/audit/graph_audit.py:318 no such table: no_such_table; scripts/audit/graph_audit.py:163 no such table: findings; scripts/audit/graph_audit.py:285 no such table: findings; scripts/audit/graph_audit.py:368 no such table: findings; scripts/audit/graph_audit.py:369 no such table: findings; scripts/audit/jurisdictional_divergence.py:213 table jurisdictional_values already exists
**Verdict:** `ERROR`

### [1130] D — method blind spots (stated explicitly)   `2026-08-12 08:35:32Z`
**Action:** what this scan CANNOT see
**Expected:** n/a
**Actual:** (1) SQL assembled by string concatenation across variables or .join() of fragments; (2) table/column names arriving from runtime data (registry YAML, argv, config) — f-string statements are counted as DYNAMIC, not verified; (3) SQL embedded in non-Python (scripts/audit/render_audit.js, shell scripts); (4) executescript bodies — split naively on ';', quoted semicolons inside migrations could mis-split; (5) %-formatted SQL counted DYNAMIC; (6) columns consumed via SELECT * then dict access are invisible to the phantom-column check; (7) migration .sql files are scanned for writers but not PREPAREd (they demonstrably ran — the DB was rebuilt from them)
**Verdict:** `BLOCKED`

### D — table × script matrix (READ / WRITE)
| table | rows | readers (.py) | writers (.py) | migration writers |
|---|---|---|---|---|
| `access_duration` | 3 | — | — | 3 stmt-kind(s) |
| `access_need_axis_map` | 21 | scripts/validate_axes.py | — | 3 stmt-kind(s) |
| `access_need_icf` | 43 | — | — | 3 stmt-kind(s) |
| `access_needs` | 17 | — | — | 3 stmt-kind(s) |
| `access_stakes` | 3 | — | — | 3 stmt-kind(s) |
| `axes` | 17 | scripts/validate_axes.py | scripts/validate_axes.py (CREATE)<br>scripts/validate_axes.py (INSERT) | 4 stmt-kind(s) |
| `bpc_metadata` | 0 | scripts/audit/pre_rehab_banner_audit.py<br>scripts/db.py<br>scripts/generate/population_page.py<br>scripts/generate/spec_page.py<br>scripts/generate_parts.py<br>scripts/migrate/migrate_bpc_metadata.py<br>scripts/tests/test_db_integrity.py<br>tools/evidentiary_audit.py<br>tools/pipeline_completeness.py | scripts/db.py (INSERT)<br>scripts/db.py (UPDATE)<br>scripts/migrate/migrate_bpc_metadata.py (INSERT) | 27 stmt-kind(s) |
| `case_studies` | 0 | — | — | 4 stmt-kind(s) |
| `case_study_outcomes` | 0 | — | — | 2 stmt-kind(s) |
| `case_study_populations` | 0 | — | — | 2 stmt-kind(s) |
| `case_study_specs` | 0 | — | — | 2 stmt-kind(s) |
| `case_study_strategies` | 0 | — | — | 2 stmt-kind(s) |
| `citation_mining` | 0 | scripts/audit/citation_mining_completeness.py<br>scripts/audit/migration_reproducibility.py<br>scripts/audit/research_batch_dod.py<br>scripts/audit_consolidator.py<br>scripts/db.py<br>scripts/migrations/session_2026_05_11g_replay.py<br>scripts/tests/test_db_integrity.py<br>scripts/validate_db.py | scripts/db.py (INSERT)<br>scripts/db.py (UPDATE)<br>scripts/migrations/session_2026_05_11g_replay.py (INSERT) | 27 stmt-kind(s) |
| `citation_population_links` | 0 | tools/regenerate_vetting_surface.py | — | 5 stmt-kind(s) |
| `conflicts` | 0 | scripts/audit_consolidator.py<br>scripts/db.py<br>scripts/generate_parts.py<br>scripts/item_audit_pipeline.py<br>scripts/validate_conflicts.py | scripts/db.py (INSERT)<br>scripts/db.py (UPDATE)<br>scripts/item_audit_pipeline.py (DELETE) | 3 stmt-kind(s) |
| `connection_targets` | 0 | scripts/audit/graph/extract_db.py<br>scripts/audit_consolidator.py<br>scripts/db.py<br>scripts/item_audit_pipeline.py<br>scripts/migrate/migrate_connections.py<br>scripts/validate_db.py | scripts/audit/graph_audit.py (CREATE)<br>scripts/audit/graph_audit.py (INSERT)<br>scripts/db.py (DELETE)<br>scripts/db.py (INSERT)<br>scripts/item_audit_pipeline.py (DELETE)<br>scripts/migrate/migrate_connections.py (INSERT) | 5 stmt-kind(s) |
| `connections` | 0 | scripts/audit/graph_audit.py<br>scripts/audit/migration_reproducibility.py<br>scripts/audit_consolidator.py<br>scripts/db.py<br>scripts/generate_parts.py<br>scripts/item_audit_pipeline.py<br>scripts/migrate/migrate_connections.py<br>scripts/validate_cross_refs.py<br>scripts/validate_db.py | scripts/audit/graph_audit.py (CREATE)<br>scripts/audit/graph_audit.py (INSERT)<br>scripts/db.py (DELETE)<br>scripts/db.py (INSERT)<br>scripts/db.py (UPDATE)<br>scripts/item_audit_pipeline.py (DELETE)<br>scripts/migrate/_legacy_guard.py (INSERT)<br>scripts/migrate/migrate_connections.py (INSERT) | 6 stmt-kind(s) |
| `convergence_assessment` | 0 | scripts/audit/adjudication_integrity.py<br>scripts/audit/check_rendered_docs.py<br>scripts/generate/pilot_renderings.py<br>scripts/validate_evidence_state.py<br>tools/pipeline_completeness.py | scripts/assess/assess_cell.py (INSERT)<br>scripts/tests/test_evidence_cell_state_2_3.py (INSERT)<br>scripts/tests/test_validate_evidence_state_2_4.py (INSERT) | 7 stmt-kind(s) |
| `data_migrations` | 319 | scripts/migrate_db.py<br>scripts/tests/test_db_integrity.py<br>tools/pipeline_completeness.py | scripts/migrate_db.py (INSERT) | 13 stmt-kind(s) |
| `db_meta` | 2 | — | scripts/init_db.py (INSERT) | 10 stmt-kind(s) |
| `decisions` | 158 | scripts/migrate/migrate_decisions.py<br>scripts/tests/test_db_integrity.py | scripts/migrate/migrate_decisions.py (INSERT) | 6 stmt-kind(s) |
| `economics_entries` | 0 | scripts/audit/research_batch_dod.py<br>scripts/tests/test_db_integrity.py | — | 3 stmt-kind(s) |
| `economics_entry_populations` | 0 | — | — | 2 stmt-kind(s) |
| `economics_entry_specs` | 0 | — | — | 2 stmt-kind(s) |
| `evidence_population_match` | 0 | scripts/assess/assess_cell.py<br>scripts/audit/research_batch_dod.py<br>scripts/audit/research_protocol_audit.py<br>scripts/audit/table_connectivity.py<br>scripts/tests/probe_pipeline.py<br>scripts/tests/test_db_integrity.py<br>scripts/tests/test_directness_2_2.py | scripts/tests/probe_pipeline.py (INSERT)<br>scripts/tests/test_assess_cell_pilot.py (CREATE) | 21 stmt-kind(s) |
| `evidence_source_authors` | 0 | scripts/migrate_evidence_sources_v2.py<br>scripts/resolve_dois.py<br>scripts/tests/test_db_integrity.py<br>scripts/tests/test_verification_pipeline.py | scripts/migrate_evidence_sources_v2.py (CREATE)<br>scripts/migrate_evidence_sources_v2.py (INSERT)<br>scripts/resolve_dois.py (DELETE)<br>scripts/resolve_dois.py (INSERT)<br>scripts/tests/test_verification_pipeline.py (INSERT) | 28 stmt-kind(s) |
| `evidence_sources` | 0 | scripts/assess/assess_cell.py<br>scripts/audit/adjudication_integrity.py<br>scripts/audit/check_rendered_docs.py<br>scripts/audit/citation_mining_completeness.py<br>scripts/audit/code_currency_audit.py<br>scripts/audit/full_db_metadata_verification.py<br>scripts/audit/gap_mining_audit.py<br>scripts/audit/metadata_integrity_audit.py<br>scripts/audit/migration_reproducibility.py<br>scripts/audit/pmp_audit.py<br>scripts/audit/reasoning_doc_citations_audit.py<br>scripts/audit/register_integrity_check.py<br>scripts/audit/research_batch_dod.py<br>scripts/audit/research_protocol_audit.py<br>scripts/audit/source_slug_links_duplicates.py<br>scripts/audit/table_connectivity.py<br>scripts/audit_evidence_metadata.py<br>scripts/db.py<br>scripts/generate/pilot_renderings.py<br>scripts/generate/spec_page.py<br>scripts/generate_parts.py<br>scripts/migrate/migrate_evidence_sources.py<br>scripts/migrate_evidence_sources_v2.py<br>scripts/migrations/session_2026_05_11g_replay.py<br>scripts/probes/citation_mining_pipeline.py<br>scripts/resolve_dois.py<br>scripts/tests/probe_pipeline.py<br>scripts/tests/test_db_integrity.py<br>scripts/tests/test_url_verifier.py<br>scripts/tests/test_verification_pipeline.py<br>scripts/validate_db.py<br>scripts/validate_evidence_state.py<br>scripts/validate_verification_consistency.py<br>tools/evidentiary_audit.py<br>tools/pipeline_completeness.py<br>tools/regenerate_vetting_surface.py | scripts/audit/research_batch_dod.py (INSERT)<br>scripts/db.py (INSERT)<br>scripts/migrate/migrate_evidence_sources.py (INSERT)<br>scripts/migrations/session_2026_05_11g_replay.py (INSERT)<br>scripts/migrations/session_2026_05_11g_replay.py (UPDATE)<br>scripts/resolve_dois.py (UPDATE)<br>scripts/tests/probe_pipeline.py (INSERT)<br>scripts/tests/test_assess_cell_pilot.py (CREATE)<br>scripts/tests/test_assess_cell_pilot.py (INSERT)<br>scripts/tests/test_db_integrity.py (UPDATE)<br>scripts/tests/test_url_verifier.py (INSERT)<br>scripts/tests/test_verification_pipeline.py (INSERT)<br>scripts/validate_verification_consistency.py (CREATE)<br>scripts/validate_verification_consistency.py (INSERT) | 222 stmt-kind(s) |
| `external_root_registry` | 0 | — | — | 2 stmt-kind(s) |
| `extraction_population_links` | 0 | tools/regenerate_vetting_surface.py | — | 2 stmt-kind(s) |
| `gap_mining` | 0 | scripts/audit/gap_mining_audit.py<br>scripts/db.py | scripts/audit/graph_audit.py (DROP)<br>scripts/db.py (INSERT) | 2 stmt-kind(s) |
| `gaps` | 0 | scripts/assess/assess_cell.py<br>scripts/audit/gap_mining_audit.py<br>scripts/audit/migration_reproducibility.py<br>scripts/audit/research_protocol_audit.py<br>scripts/audit_consolidator.py<br>scripts/db.py<br>scripts/item_audit_pipeline.py<br>scripts/migrate/migrate_gaps.py<br>scripts/migrations/session_2026_05_11g_replay.py<br>scripts/tests/test_db_integrity.py<br>scripts/validate_conflicts.py<br>scripts/validate_db.py<br>scripts/validate_evidence_state.py<br>tools/pipeline_completeness.py | scripts/assess/assess_cell.py (INSERT)<br>scripts/db.py (INSERT)<br>scripts/db.py (UPDATE)<br>scripts/item_audit_pipeline.py (DELETE)<br>scripts/migrate/migrate_gaps.py (INSERT)<br>scripts/migrations/session_2026_05_11g_replay.py (INSERT)<br>scripts/migrations/session_2026_05_11g_replay.py (UPDATE)<br>scripts/tests/test_evidence_cell_state_2_3.py (CREATE)<br>scripts/tests/test_evidence_cell_state_2_3.py (INSERT)<br>scripts/tests/test_validate_evidence_state_2_4.py (CREATE)<br>scripts/tests/test_validate_evidence_state_2_4.py (INSERT) | 39 stmt-kind(s) |
| `item_audit_runs` | 0 | scripts/audit_consolidator.py<br>scripts/db.py<br>scripts/item_audit_pipeline.py<br>scripts/validate_audit_runs.py | scripts/audit_consolidator.py (UPDATE)<br>scripts/db.py (INSERT)<br>scripts/db.py (UPDATE)<br>scripts/item_audit_pipeline.py (INSERT)<br>scripts/item_audit_pipeline.py (UPDATE) | 5 stmt-kind(s) |
| `item_axis_links` | 158 | scripts/validate_axes.py | — | 9 stmt-kind(s) |
| `item_bpc_links` | 0 | scripts/generate/spec_page.py<br>scripts/tests/test_db_integrity.py<br>tools/pipeline_completeness.py | — | 4 stmt-kind(s) |
| `item_population_elaborations` | 0 | scripts/tests/probe_pipeline.py<br>scripts/tests/test_db_integrity.py | — | 8 stmt-kind(s) |
| `item_population_links` | 372 | scripts/audit/check_rendered_docs.py<br>scripts/audit/graph/extract_db.py<br>scripts/generate/population_page.py<br>scripts/generate/spec_page.py<br>scripts/item_audit_pipeline.py<br>scripts/tests/test_db_integrity.py<br>scripts/validate_items.py<br>tools/pipeline_completeness.py<br>tools/regenerate_vetting_surface.py | — | 7 stmt-kind(s) |
| `items` | 93 | scripts/audit/graph/extract_db.py<br>scripts/audit/graph_audit.py<br>scripts/audit/migration_reproducibility.py<br>scripts/audit/pmp_audit.py<br>scripts/audit/table_connectivity.py<br>scripts/audit_consolidator.py<br>scripts/db.py<br>scripts/generate/build_site.py<br>scripts/generate/pilot_renderings.py<br>scripts/generate/population_page.py<br>scripts/generate/spec_page.py<br>scripts/generate_parts.py<br>scripts/generate_search_queries.py<br>scripts/item_audit_pipeline.py<br>scripts/tests/test_db_integrity.py<br>scripts/validate_audit_runs.py<br>scripts/validate_db.py<br>scripts/validate_items.py<br>tools/evidentiary_audit.py<br>tools/pipeline_completeness.py<br>tools/regenerate_vetting_surface.py | scripts/audit/graph_audit.py (UPDATE)<br>scripts/audit/migration_reproducibility.py (INSERT)<br>scripts/db.py (INSERT)<br>scripts/migrate/migrate_items.py (INSERT)<br>scripts/tests/probe_pipeline.py (INSERT)<br>scripts/tests/test_evidence_cell_state_2_3.py (CREATE)<br>scripts/tests/test_evidence_cell_state_2_3.py (INSERT)<br>scripts/tests/test_validate_evidence_state_2_4.py (CREATE)<br>scripts/tests/test_validate_evidence_state_2_4.py (INSERT) | 10 stmt-kind(s) |
| `jurisdictional_values` | 109 | scripts/audit/jurisdictional_divergence.py<br>scripts/generate/pilot_renderings.py<br>scripts/tests/probe_pipeline.py<br>scripts/tests/test_db_integrity.py<br>scripts/validate_schema.py | scripts/audit/jurisdictional_divergence.py (CREATE)<br>scripts/audit/jurisdictional_divergence.py (INSERT) | 4 stmt-kind(s) |
| `lang_jur_map` | 70 | scripts/audit/alias_provenance_audit.py<br>scripts/db.py<br>scripts/generate_alias_chart.py<br>tools/pipeline_completeness.py | — | 4 stmt-kind(s) |
| `life_stage_modifiers` | 2 | — | — | 3 stmt-kind(s) |
| `pipeline_runs` | 0 | scripts/tests/test_db_integrity.py<br>scripts/tests/test_verification_pipeline.py | scripts/resolve_dois.py (CREATE)<br>scripts/resolve_dois.py (INSERT)<br>scripts/resolve_dois.py (REPLACE)<br>scripts/resolve_dois.py (UPDATE) | 3 stmt-kind(s) |
| `population_axis_map` | 53 | scripts/validate_axes.py | scripts/validate_axes.py (CREATE)<br>scripts/validate_axes.py (DELETE)<br>scripts/validate_axes.py (INSERT) | 7 stmt-kind(s) |
| `population_reclass` | 29 | — | — | 3 stmt-kind(s) |
| `populations` | 23 | scripts/assess/assess_cell.py<br>scripts/audit/graph/extract_db.py<br>scripts/audit/graph_audit.py<br>scripts/audit/population_integrity_audit.py<br>scripts/audit/table_connectivity.py<br>scripts/generate/population_page.py<br>scripts/generate/spec_page.py<br>scripts/generate_parts.py<br>scripts/tests/probe_pipeline.py<br>scripts/tests/test_db_integrity.py<br>scripts/validate_axes.py<br>scripts/validate_items.py<br>scripts/validate_population.py<br>tools/pipeline_completeness.py<br>tools/regenerate_vetting_surface.py | scripts/audit/graph_audit.py (UPDATE)<br>scripts/tests/probe_pipeline.py (INSERT)<br>scripts/tests/test_evidence_cell_state_2_3.py (CREATE)<br>scripts/tests/test_evidence_cell_state_2_3.py (INSERT)<br>scripts/tests/test_validate_evidence_state_2_4.py (CREATE)<br>scripts/tests/test_validate_evidence_state_2_4.py (INSERT)<br>scripts/validate_axes.py (CREATE)<br>scripts/validate_axes.py (INSERT) | 5 stmt-kind(s) |
| `probe_population_links` | 0 | tools/regenerate_vetting_surface.py | — | 5 stmt-kind(s) |
| `reasoning_doc_citations` | 0 | scripts/audit/adherence_log_audit.py<br>scripts/audit/reasoning_doc_citations_audit.py<br>scripts/tests/test_db_integrity.py<br>tools/pipeline_completeness.py<br>tools/regenerate_vetting_surface.py | — | 10 stmt-kind(s) |
| `room_items` | 0 | — | — | 1 stmt-kind(s) |
| `rooms` | 17 | — | — | 2 stmt-kind(s) |
| `search_admissions` | 0 | scripts/tests/probe_pipeline.py<br>scripts/tests/test_db_integrity.py | scripts/db.py (INSERT)<br>scripts/tests/probe_pipeline.py (INSERT) | 3 stmt-kind(s) |
| `search_candidates` | 0 | scripts/audit/research_batch_dod.py | — | 11 stmt-kind(s) |
| `search_coverage` | 0 | scripts/db.py<br>tools/evidentiary_audit.py | — | 9 stmt-kind(s) |
| `search_executions` | 0 | scripts/audit/research_batch_dod.py<br>scripts/db.py<br>scripts/tests/probe_pipeline.py<br>scripts/tests/test_db_integrity.py<br>tools/pipeline_completeness.py | scripts/audit/research_batch_dod.py (INSERT)<br>scripts/db.py (INSERT)<br>scripts/tests/probe_pipeline.py (INSERT)<br>scripts/tests/probe_pipeline.py (UPDATE) | 26 stmt-kind(s) |
| `search_languages` | 0 | scripts/audit/research_protocol_audit.py<br>scripts/db.py<br>tools/evidentiary_audit.py | — | 8 stmt-kind(s) |
| `situations` | 0 | — | — | 2 stmt-kind(s) |
| `slugs` | 106 | scripts/audit/graph/extract_db.py<br>scripts/audit/graph_audit.py<br>scripts/audit/table_connectivity.py<br>scripts/audit_evidence_metadata.py<br>scripts/generate_search_queries.py<br>scripts/migrate/migrate_bpc_metadata.py<br>scripts/migrate/migrate_evidence_sources.py<br>scripts/migrate/migrate_items.py<br>scripts/migrate/migrate_slugs.py<br>scripts/tests/test_db_integrity.py<br>scripts/validate_cross_refs.py<br>tools/evidentiary_audit.py<br>tools/pipeline_completeness.py | scripts/migrate/migrate_slugs.py (INSERT)<br>scripts/tests/probe_pipeline.py (INSERT) | 12 stmt-kind(s) |
| `source_locators` | 835 | — | — | 2 stmt-kind(s) |
| `source_slug_links` | 0 | scripts/assess/assess_cell.py<br>scripts/audit/citation_mining_completeness.py<br>scripts/audit/code_currency_audit.py<br>scripts/audit/migration_reproducibility.py<br>scripts/audit/source_slug_links_duplicates.py<br>scripts/audit/table_connectivity.py<br>scripts/audit_evidence_metadata.py<br>scripts/db.py<br>scripts/migrate/migrate_evidence_sources.py<br>scripts/migrations/session_2026_05_11g_replay.py<br>scripts/tests/test_db_integrity.py<br>scripts/validate_db.py<br>tools/evidentiary_audit.py<br>tools/regenerate_vetting_surface.py | scripts/db.py (INSERT)<br>scripts/migrate/migrate_evidence_sources.py (INSERT)<br>scripts/migrations/session_2026_05_11g_replay.py (DELETE)<br>scripts/migrations/session_2026_05_11g_replay.py (INSERT)<br>scripts/migrations/session_2026_05_11g_replay.py (UPDATE)<br>scripts/tests/probe_pipeline.py (INSERT)<br>scripts/tests/test_assess_cell_pilot.py (CREATE)<br>scripts/tests/test_assess_cell_pilot.py (INSERT) | 71 stmt-kind(s) |
| `source_value_extractions` | 0 | scripts/audit/adjudication_integrity.py<br>scripts/generate/pilot_renderings.py<br>scripts/tests/probe_pipeline.py<br>scripts/tests/test_db_integrity.py<br>tools/pipeline_completeness.py<br>tools/regenerate_vetting_surface.py | scripts/tests/probe_pipeline.py (INSERT) | 12 stmt-kind(s) |
| `spec_value_probes` | 0 | scripts/audit/adherence_log_audit.py<br>scripts/audit/gap_mining_audit.py<br>scripts/audit/pmp_audit.py<br>scripts/tests/test_db_integrity.py<br>tools/regenerate_vetting_surface.py | — | 13 stmt-kind(s) |
| `specification_source_links` | 0 | scripts/generate/build_site.py<br>scripts/generate/pilot_renderings.py<br>scripts/generate/spec_page.py<br>scripts/tests/probe_pipeline.py | scripts/tests/probe_pipeline.py (INSERT)<br>scripts/tests/test_validate_evidence_state_2_4.py (ALTER) | 1 stmt-kind(s) |
| `specifications` | 0 | scripts/assess/assess_cell.py<br>scripts/audit/adjudication_integrity.py<br>scripts/audit/check_rendered_docs.py<br>scripts/audit/jurisdictional_divergence.py<br>scripts/audit/register_integrity_check.py<br>scripts/audit/table_connectivity.py<br>scripts/generate/build_site.py<br>scripts/generate/pilot_renderings.py<br>scripts/generate/population_page.py<br>scripts/generate/spec_page.py<br>scripts/tests/probe_pipeline.py<br>scripts/tests/test_db_integrity.py<br>scripts/tests/test_evidence_cell_state_2_3.py<br>scripts/validate_evidence_state.py<br>scripts/validate_verification_consistency.py<br>tools/pipeline_completeness.py | scripts/assess/assess_cell.py (INSERT)<br>scripts/audit/jurisdictional_divergence.py (CREATE)<br>scripts/audit/jurisdictional_divergence.py (INSERT)<br>scripts/tests/probe_pipeline.py (INSERT)<br>scripts/tests/probe_pipeline.py (UPDATE)<br>scripts/tests/test_evidence_cell_state_2_3.py (ALTER)<br>scripts/tests/test_evidence_cell_state_2_3.py (INSERT)<br>scripts/tests/test_validate_evidence_state_2_4.py (ALTER)<br>scripts/tests/test_validate_evidence_state_2_4.py (INSERT)<br>scripts/validate_verification_consistency.py (CREATE)<br>scripts/validate_verification_consistency.py (DELETE)<br>scripts/validate_verification_consistency.py (INSERT) | 1 stmt-kind(s) |
| `supersession_check` | 0 | scripts/audit/code_currency_audit.py | scripts/db.py (INSERT) | 16 stmt-kind(s) |
| `term_aliases` | 2382 | scripts/audit/alias_provenance_audit.py<br>scripts/audit/graph/extract_db.py<br>scripts/audit/research_batch_dod.py<br>scripts/db.py<br>scripts/generate_alias_chart.py<br>scripts/generate_search_queries.py | scripts/audit/research_batch_dod.py (INSERT) | 13 stmt-kind(s) |
| `term_item_links` | 147 | scripts/audit/graph/extract_db.py<br>scripts/db.py<br>scripts/generate_alias_chart.py<br>scripts/generate_search_queries.py | — | 6 stmt-kind(s) |
| `terms` | 88 | scripts/db.py<br>scripts/generate_alias_chart.py<br>scripts/generate_parts.py<br>scripts/generate_search_queries.py | — | 8 stmt-kind(s) |
| `url_verification_runs` | 0 | scripts/tests/test_db_integrity.py | scripts/verify_urls.py (CREATE)<br>scripts/verify_urls.py (INSERT)<br>scripts/verify_urls.py (REPLACE)<br>scripts/verify_urls.py (UPDATE) | 3 stmt-kind(s) |
| `weighting_profile` | 5 | — | — | 2 stmt-kind(s) |

### [1131] D — unwritable outputs   `2026-08-12 08:35:32Z`
**Action:** tables read by code but with NO .py writer AND NO data-migration INSERT/UPDATE/DELETE
**Expected:** none
**Actual:** []
**Verdict:** `OK`

### [1132] D — unread inputs   `2026-08-12 08:35:32Z`
**Action:** tables written (py or migrations) but read by no scanned .py
**Expected:** none
**Actual:** ['access_duration', 'access_need_icf', 'access_needs', 'access_stakes', 'case_studies', 'case_study_outcomes', 'case_study_populations', 'case_study_specs', 'case_study_strategies', 'db_meta', 'economics_entry_populations', 'economics_entry_specs', 'external_root_registry', 'life_stage_modifiers', 'population_reclass', 'rooms', 'situations', 'source_locators', 'weighting_profile']
**Verdict:** `ERROR`

### [1133] D — phantom tables   `2026-08-12 08:35:32Z`
**Action:** table names referenced in code that do not exist in the schema
**Expected:** known set from room_page.py
**Actual:** cell_source_links ← [('scripts/tests/test_validate_evidence_state_2_4.py', 'ALTER')]; conflict ← [('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'READ'), ('scripts/db/migrate_all.py', 'REPLACE')]; connection_endpoint ← [('scripts/db/enrich_all_c_stage.py', 'INSERT'), ('scripts/db/enrich_all_c_stage.py', 'READ'), ('scripts/db/enrich_all_c_stage.py', 'REPLACE')]; doctrine ← [('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'REPLACE'), ('scripts/db/migrate_all.py', 'UPDATE')]; economics_entry ← [('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'REPLACE')]; evidence_cell_state ← [('scripts/tests/test_evidence_cell_state_2_3.py', 'ALTER'), ('scripts/tests/test_validate_evidence_state_2_4.py', 'ALTER')]; evidence_source ← [('scripts/db/enrich_all_c_stage.py', 'READ'), ('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'REPLACE')]; evidence_sources_v1_legacy ← [('scripts/tests/test_db_integrity.py', 'READ')]; jurisdictional_value ← [('scripts/db/enrich_all_c_stage.py', 'READ'), ('scripts/db/migrate_all.py', 'DELETE'), ('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'READ')]; measurement ← [('scripts/db/enrich_all_c_stage.py', 'READ'), ('scripts/db/migrate_all.py', 'INSERT')]; population ← [('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'READ'), ('scripts/db/migrate_all.py', 'REPLACE')]; room ← [('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'REPLACE'), ('scripts/db/migrate_all.py', 'UPDATE'), ('scripts/generate/room_page.py', 'READ')]; room_conflict ← [('scripts/db/enrich_all_c_stage.py', 'INSERT'), ('scripts/db/enrich_all_c_stage.py', 'READ'), ('scripts/db/enrich_all_c_stage.py', 'REPLACE'), ('scripts/db/migrate_all.py', 'INSERT'), ('scripts/generate/room_page.py', 'READ')]; room_dar_provision ← [('scripts/db/enrich_all_c_stage.py', 'INSERT'), ('scripts/db/enrich_all_c_stage.py', 'READ'), ('scripts/db/enrich_all_c_stage.py', 'REPLACE'), ('scripts/db/migrate_all.py', 'INSERT'), ('scripts/generate/room_page.py', 'READ')]; room_item ← [('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'REPLACE'), ('scripts/generate/room_page.py', 'READ')]; room_item_population ← [('scripts/db/enrich_all_c_stage.py', 'INSERT'), ('scripts/db/enrich_all_c_stage.py', 'READ'), ('scripts/db/enrich_all_c_stage.py', 'REPLACE'), ('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'REPLACE'), ('scripts/generate/room_page.py', 'READ')]; specialist ← [('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'REPLACE')]; specialist_population ← [('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'REPLACE')]; specialist_trigger ← [('scripts/db/migrate_all.py', 'INSERT')]; specification ← [('scripts/db/enrich_all_c_stage.py', 'READ'), ('scripts/db/enrich_all_c_stage.py', 'UPDATE'), ('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'READ'), ('scripts/db/migrate_all.py', 'REPLACE'), ('scripts/db/migrate_all.py', 'UPDATE'), ('scripts/generate/room_page.py', 'READ')]; specification_population ← [('scripts/db/enrich_all_c_stage.py', 'READ'), ('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'READ'), ('scripts/db/migrate_all.py', 'REPLACE')]; specification_source ← [('scripts/db/enrich_all_c_stage.py', 'INSERT'), ('scripts/db/enrich_all_c_stage.py', 'READ'), ('scripts/db/enrich_all_c_stage.py', 'REPLACE')]; t ← [('scripts/audit/readonly_db_open_audit.py', 'INSERT')]; throughline ← [('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'REPLACE')]; throughline_specification ← [('scripts/db/migrate_all.py', 'INSERT'), ('scripts/db/migrate_all.py', 'REPLACE')]
**Verdict:** `ERROR`

### [1134] D — separate-DB tables (graph audit module)   `2026-08-12 08:35:32Z`
**Action:** table names used by scripts/audit/graph/* + graph_audit.py — these target a STANDALONE graph database file, not data/guidebook.db
**Expected:** classified separately, not as guidebook phantoms
**Actual:** __DYN__ ← ['scripts/audit/graph/model.py', 'scripts/audit/graph_audit.py']; build_meta ← ['scripts/audit/graph/model.py', 'scripts/audit/graph_audit.py']; edges ← ['scripts/audit/graph/model.py', 'scripts/audit/graph/topology.py']; findings ← ['scripts/audit/graph/model.py', 'scripts/audit/graph_audit.py']; no_such_table ← ['scripts/audit/graph_audit.py']; nodes ← ['scripts/audit/graph/extract_content.py', 'scripts/audit/graph/model.py', 'scripts/audit/graph/topology.py']; real_table ← ['scripts/audit/graph/extract_code.py']; zzz_phantom ← ['scripts/audit/graph_audit.py']
**Verdict:** `OK`

### [1135] D — phantom columns (static)   `2026-08-12 08:35:32Z`
**Action:** columns referenced in SQL that do not exist on their (real) table
**Expected:** none
**Actual:** scripts/audit/migration_reproducibility.py:440 items.id [INSERT column list]; scripts/migrate/migrate_evidence_sources.py:307 evidence_sources.authors [INSERT column list]; scripts/migrate/migrate_evidence_sources.py:307 evidence_sources.year [INSERT column list]; scripts/migrate/migrate_evidence_sources.py:307 evidence_sources.title [INSERT column list]; scripts/migrate/migrate_evidence_sources.py:307 evidence_sources.doi_less_key [INSERT column list]; scripts/migrate/migrate_items.py:158 items.applicable_groups [INSERT column list]
**Verdict:** `ERROR`

### [1136] D — legacy scripts   `2026-08-12 08:35:32Z`
**Action:** scripts under scripts/db, scripts/migrate, scripts/convert — marked, not excluded
**Expected:** marked
**Actual:** 29 legacy scripts included in the matrix: ['scripts/convert/convert_bpc_metadata.py', 'scripts/convert/convert_conflicts.py', 'scripts/convert/convert_connections.py', 'scripts/convert/convert_doctrines.py', 'scripts/convert/convert_gaps.py', 'scripts/convert/convert_jurisdictions.py', 'scripts/convert/convert_populations.py', 'scripts/convert/convert_rooms.py', 'scripts/convert/convert_slugs.py', 'scripts/convert/convert_sources.py', 'scripts/convert/convert_spec_db.py', 'scripts/convert/convert_specialists.py', 'scripts/convert/version_retrofit.py', 'scripts/db.py', 'scripts/db/enrich_all_c_stage.py', 'scripts/db/init_db.py', 'scripts/db/migrate_all.py', 'scripts/migrate/_legacy_guard.py', 'scripts/migrate/init_database.py', 'scripts/migrate/migrate_bpc_metadata.py', 'scripts/migrate/migrate_connections.py', 'scripts/migrate/migrate_decisions.py', 'scripts/migrate/migrate_evidence_sources.py', 'scripts/migrate/migrate_gaps.py', 'scripts/migrate/migrate_items.py', 'scripts/migrate/migrate_slugs.py', 'scripts/migrate/phase_jv_appendix_a.py', 'scripts/migrate_db.py', 'scripts/migrate_evidence_sources_v2.py']
**Verdict:** `OK`

**SWEEP D EXAMINED: 168/168 scripts AST-parsed · 1424 SQL statements PREPARE-checked (772 prepared, 216 dynamic, 210 fragments) · 67 tables in matrix · 25 phantom tables · 6 phantom column refs**


---

## EXECUTIVE SUMMARY
- Rejectable-write surface probed (FK=ON): **481/481** (80 FK bad-value + 128 CHECK + 268 NOT NULL + 5 UNIQUE); same surface re-probed under FK=OFF; plus 18/18 NULL-path probes and 1 dual-identity probe.
- Sweep A: edges 80/80 · orphan queries 89 · reverse map 66/66 tables; isolated=['access_duration', 'access_stakes', 'data_migrations', 'db_meta', 'decisions', 'external_root_registry', 'lang_jur_map', 'life_stage_modifiers', 'pipeline_runs', 'population_reclass', 'situations', 'source_locators', 'url_verification_runs', 'weighting_profile']; referenced-but-empty=['case_studies', 'connections', 'convergence_assessment', 'economics_entries', 'evidence_sources', 'gaps', 'reasoning_doc_citations', 'search_executions', 'source_value_extractions', 'spec_value_probes', 'specifications']
- Sweep B: 26 handoff probes · Sweep V: 18/18 views · Sweep C: 10 joints
- Sweep D: 168/168 scripts; 1424 statements prepared; unwritable=[]; unread=['access_duration', 'access_need_icf', 'access_needs', 'access_stakes', 'case_studies', 'case_study_outcomes', 'case_study_populations', 'case_study_specs', 'case_study_strategies', 'db_meta', 'economics_entry_populations', 'economics_entry_specs', 'external_root_registry', 'life_stage_modifiers', 'population_reclass', 'rooms', 'situations', 'source_locators', 'weighting_profile']; phantom tables=['cell_source_links', 'conflict', 'connection_endpoint', 'doctrine', 'economics_entry', 'evidence_cell_state', 'evidence_source', 'evidence_sources_v1_legacy', 'jurisdictional_value', 'measurement', 'population', 'room', 'room_conflict', 'room_dar_provision', 'room_item', 'room_item_population', 'specialist', 'specialist_population', 'specialist_trigger', 'specification', 'specification_population', 'specification_source', 't', 'throughline', 'throughline_specification']; phantom column refs=6

**SILENT-PASS total: 106** — seqs [171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 1077, 1083, 1087, 1091, 1092, 1095]
**ORPHAN total: 6** — seqs [85, 271, 1120, 1123, 1125, 1126]
**ERROR/FAILED-WRITE total: 6** — seqs [3, 1098, 1129, 1132, 1133, 1135]
**BLOCKED total: 12** — seqs [397, 525, 1101, 1106, 1107, 1109, 1110, 1111, 1112, 1116, 1117, 1130]
