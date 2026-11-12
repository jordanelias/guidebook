# 12 — `db.py` verb matrix (the CLI write path)

_Generated 2026-11-12 02:01 UTC at commit e73b588, schema user_version 125. Every figure here is computed by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_dossier.py`; re-run it, do not trust this text (CLAUDE.md rule 7a)._


72 verbs. Reads/writes derived from the handler block plus up to 3 levels of called helpers; names a table wherever its name appears in the code, so a read column can over-report (it cannot under-report a literal table name).

| verb | stage(s) written | tables written | tables read (≤12 shown) | help |
|---|---|---|---|---|
| add-alias | base | term_aliases | evidence_sources, observed_terms, term_adjudications, terms | Record a SOURCE-ATTESTED alias from an adjudicated |
| add-candidate | research | search_candidates | search_executions, slugs | Stage a screened candidate (search_candidates |
| add-case-study | evidence | case_studies | evidence_sources, slugs | Record a Part-12 case study |
| add-code-lead | research | research_code_leads | source_locators | Record a code/standard lead (research_code_leads |
| add-conflict | synthesis | conflicts | base_parameters, base_taxonomy_identity, decisions | Insert a conflict record |
| add-connection | synthesis | connection_targets, connections | base_parameters | Insert a new connection record |
| add-economics-entry | evidence | economics_entries | evidence_sources | Record a Part-13 economics finding |
| add-extraction | judgment | extraction_relations, source_value_extractions | base_parameters, base_taxonomy_medical, evidence_sources, external_root_registry, source_scans, source_slug_links, v_derived_figure_check, v_scan_ledger | Record what one source asserts for one parameter |
| add-gap | synthesis | gaps |  | Insert a new gap record |
| add-gap-mining | research | gap_mining |  | Record a gap-driven mining attempt (DR-2026-05-26 |
| add-icf-code | base | base_icf |  | Mint one ICF code into base_icf — the registry the ICF lens points at |
| add-locator | research | source_locators | evidence_sources | Write a lead into the clue store |
| add-medical | base | base_taxonomy_medical, icf_medical_map, identity_medical_map | base_icf, base_taxonomy_identity, specifications, terms | Mint a medical-lens row and at least one crossing |
| add-parameter | base | base_parameters | parameter_declinations, specifications, term_adjudications, terms | Promote an adjudicated term into base_parameters |
| add-population-icf-link | base | identity_icf_map | base_icf, base_taxonomy_identity | Map a population to an ICF activity it has a functional deficit in (H3 |
| add-population-match | judgment | evidence_population_match | base_taxonomy_identity, evidence_sources | Grade population-of-study vs population-served (R13 |
| add-source | evidence | evidence_source_authors, evidence_sources, source_slug_links | base_parameters, citation_mining, observed_terms, slugs, source_locators, term_adjudications, terms, v_evidence_authors, v_scan_ledger | Insert an evidence source |
| add-supersession-check | synthesis | supersession_check |  | Record a per-anchor-source supersession outcome (DR-2026-05-24 |
| add-term | base+judgment | term_adjudications, terms | observed_terms, term_aliases | Mint a term for a NEW concept and adjudicate it NAMES-NEW |
| adjudicate-term | judgment | term_adjudications | evidence_population_match, observed_terms, terms | Decide whether an observed phrase names our concept |
| amend-extraction | judgment | source_value_extractions | evidence_sources, extraction_relations, source_scans, v_scan_ledger | Change figure_role or comparator on an existing |
| amend-gap | synthesis | gaps |  | APPEND a dated correction to a gap's description |
| amend-population-match | judgment | evidence_population_match |  | Re-grade an R13 match in place (a ruling, not a dissent -- |
| amend-search | research | search_execution_artefacts, search_executions | adversarial_passes, evidence_sources, v_coverage_branch | APPEND a dated correction to a logged search's findings_note |
| amend-source | evidence | evidence_sources |  | Correct a JUDGEMENT field on an evidence row, recording what was replaced |
| amend-term | base | terms | term_aliases | Replace a term's definition or scope_note, recording the |
| annotate-parameter | base | base_parameters | terms | Append a dated, attributed line to a parameter's notes |
| close-adversarial-pass | infrastructure | adversarial_passes | adversarial_findings | Close a pass once every lens is covered and at least one row SURVIVED (RC4 |
| close-gap | synthesis | gaps |  | Close a gap record |
| conflicts | — | — | conflicts | Query conflict records |
| connections | — | — | connection_targets, connections | Query connections |
| correct-source | evidence | evidence_source_authors, evidence_sources |  | Rewrite bibliographic fields FROM THE LOGGED PAYLOAD |
| coverage | — | — | lang_jur_map, search_executions, slugs, v_coverage_priority, v_research_scope | Check search coverage |
| decline-parameter | base | parameter_declinations | base_parameters, terms | Record that a term is NOT a design parameter, and why |
| delete-connection | synthesis | connection_targets, connections |  | Hard-delete a connection by CON-ID (data corrections only |
| derive-extraction | judgment | extraction_relations, source_value_extractions | base_parameters, base_taxonomy_medical, evidence_sources, external_root_registry, source_scans, source_slug_links, v_derived_figure_check, v_scan_ledger | Write a computed (base+delta) extraction and the |
| dispose-adversarial-finding | infrastructure | adversarial_findings |  | Set an adversarial finding's disposition (RC4 |
| gaps | — | — | gaps | Query gaps |
| is-mined | — | — | citation_mining, evidence_sources, source_locators | Check mining status |
| link-admission | research | search_admissions, search_executions | evidence_sources, search_candidates, v_coverage_language | Record that an EXISTING search admitted a source -- only |
| link-source-slug | evidence | source_slug_links | evidence_sources, slugs | Cross-file an ADMITTED source to an ADDITIONAL slug (R9 |
| log-mining | evidence+research | citation_mining, evidence_sources | connections, search_candidates, search_executions, source_locators, source_slug_links | Log citation mining |
| log-search | research | search_admissions, search_execution_artefacts, search_executions | adversarial_passes, base_parameters, evidence_sources, lang_jur_map, slugs, v_coverage_branch, v_research_scope | Append one row to search_executions |
| merge-parameter | base | base_parameters | determination_gates, specifications, terms | Fold one parameter into another: status merged, |
| migrate | — | — |  | Run pending schema migrations |
| mint-term-from-catalogue | base | terms | term_aliases | Mint a term from a PERMITTED catalogue, pointing at the |
| next-id | — | — | conflicts, connections, gaps, terms | Get next available ID |
| observe-term | evidence | observed_terms | evidence_sources | Record that a source USES a phrase (evidence stage, D-0173 |
| raise-determination-gate | specification | determination_gates | base_parameters, base_taxonomy_identity, evidence_sources | Raise an H4 gate: cap a cell at provisional until it is resolved |
| raise-follow-up | judgment | extraction_follow_ups | source_value_extractions | Tag an extraction for a reviewer to re-check |
| reattribute-candidate | research | search_candidates | search_executions, terms | Repoint a candidate at the search that surfaced it |
| record-adversarial-pass | infrastructure | adversarial_findings, adversarial_passes |  | Record a completed antagonist pass and its findings block (RC4 |
| record-scan | evidence | source_scans | base_parameters, evidence_sources, v_scan_ledger | Record one READING of a source against the parameter list (source_scans); |
| relate-extraction | judgment | extraction_relations | source_value_extractions | Add a comparator edge to an existing extraction row, |
| rename-term | base | term_aliases, terms | observed_terms, term_adjudications | Correct a term's canonical name from an observation or an |
| resolve-candidate | research | search_candidates | evidence_sources, slugs | Close a staged candidate, re-describing it from the source (R15 |
| resolve-determination-gate | specification | determination_gates |  | Close an H4 gate by the named path, with the rationale the schema requires |
| resolve-follow-up | judgment | extraction_follow_ups |  | Close an open extraction follow-up with what the re-check |
| retire-parameter | base | base_parameters | determination_gates, source_value_extractions, specifications, terms, v_scan_ledger, v_value_independence | Retire a parameter IN PLACE (status retired; reason |
| retire-specification | specification | specifications |  | Retire a determination in place so its cell can be determined again |
| revoke-declination | base | parameter_declinations | decisions | Revoke a parameter declination (recorded on the row, |
| set-icf-title | base | base_icf |  | Name a seeded ICF code (GAP-ICF-TITLES); refuses to overwrite a title |
| set-parameter-direction | base | base_parameters | evidence_sources, source_value_extractions, terms | Record which way is better for a disabled person on this parameter |
| supersede-source | evidence | evidence_sources | v_convergence_sources, v_determination_provenance, v_evidence_authors, v_item_provenance, v_source_admission, v_source_reach_all | Mark an admitted source SUPERSEDED BY another (a mirror, a DOI-less |
| unlink-admission | research | search_admissions, search_executions | search_candidates, v_coverage_language | Remove a WRONG admission edge (the corrective half of |
| unmined | — | — | citation_mining, evidence_sources, slugs, source_slug_links | List unmined Tier 1-N sources |
| unmined-gaps | — | — | gap_mining, gaps | Query gaps eligible for gap-driven mining |
| update-code-lead | research | research_code_leads |  | Move a code lead's status or clause, APPENDING a dated note |
| update-conflict | synthesis | conflicts |  | Update a conflict record |
| update-connection | synthesis | connections |  | Update connection status |
| update-gap-addressability | synthesis | gaps |  | Set gaps.mining_addressability per DR-2026-05-26 |
| update-locator | research | source_locators | evidence_sources | Move a lead's status in the clue store |


## Tables no `db.py` verb writes (derived)

| table | stage | rows |
|---|---|---|
| access_duration | base | 3 |
| access_need_icf | base | 43 |
| access_needs | base | 17 |
| access_stakes | base | 3 |
| base_taxonomy_identity | base | 23 |
| convergence_assessment | synthesis | 5 |
| convergence_sources | synthesis | 69 |
| data_migrations | infrastructure | 476 |
| decisions | infrastructure | 188 |
| external_root_registry | evidence | 0 |
| lang_jur_map | base | 70 |
| life_stage_modifiers | base | 2 |
| reasoning_doc_citations | synthesis | 0 |
| rooms | base | 17 |
| slugs | base | 106 |
| specification_extraction_links | specification | 151 |
| specification_source_links | specification | 38 |
| weighting_profile | render | 5 |