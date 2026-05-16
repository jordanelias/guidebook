## ot-cpg-built-environment

```yaml
slug: ot-cpg-built-environment
research_type: source-inventory  # NOT a parameter search; documents Co-2 tier source population for §1.5 Evidence Hierarchy
created: 2026-03-28 21:59
created_by_commit: 4915e9c6
last_updated: 2026-04-19
opus_synthesis: true
opus_synthesis_commit: 4de697dd  # 2026-03-29
status: COMPLETE

scope:
  description: >
    Inventory of confirmed OT professional body publications (Co-2 tier per §1.5)
    relevant to built environment and home modification. The Co-2 tier was defined
    (D-18 / project-standards.md) but had no source list; this inventory populates it.
  evidence_tier: Co-2
  population: ALL
  jurisdiction_scope: international  # RCOT (UK), AOTA (US), CAOT (CA), COTEC/WFOT (transnational)

research_inputs_used:
  - manual_canvass_of_OT_professional_bodies
  - bibliography_v9_cross_reference
  - dimensional_content_evaluation_per_source

native_aliases: N/A  # Source-inventory work; not a multilingual term search
multilingual_queries: N/A  # See note below
jurisdictions_searched: N/A  # Source-inventory, not jurisdictional comparison

provenance_notes: >
  This file is a metadata-only search-log. The actual research artifacts live in
  references/bpc/population-general/ot-cpg-built-environment.md (the BPC), authored
  in the same LOG operation (commit 4915e9c6, 2026-03-28). The 2026-03-26 search-log
  split migration (commits 27d0fbb1, e1dea9a7) created separate search-log files
  for parameter-search BPCs (e.g., mobility, visual, neurological) where there
  were genuine multilingual queries, jurisdictional sweeps, and native-alias work
  to capture. The ot-cpg-built-environment BPC, being a source-inventory rather
  than a parameter search, had no such content to split, and the corresponding
  search-log file was never created. Reconstructed 2026-05-15 in
  session_2026-05-15a-governance-reconciliation to close the validator co-existence
  check honestly — this file documents what the research actually was rather than
  fabricating multilingual scaffolding that never existed.

reconstruction:
  reconstructed: 2026-05-15
  reconstructed_in: session_2026-05-15a-governance-reconciliation
  reconstructed_reason: >
    Caller-sweep miss surfaced by validate_cross_refs.py after the
    references/search-logs → references/search-log path drift was fixed.
    Closes the BPC ↔ search-log 1:1 invariant for this slug.
```

### Research provenance

The Co-2 source inventory was produced 2026-03-28 (commit `4915e9c6`) via manual canvass of OT professional bodies (RCOT, AOTA, CAOT, COTEC/WFOT), cross-referencing each candidate against `bibliography-v9` and evaluating for dimensional content relevance to the built environment. Six sources confirmed as Co-2:

1. RCOT (2019) Housing Adaptations Without Delay
2. RCOT (2023) Living Well by Design
3. RCOT/Habinteg (2024) Inclusive Housing Design Guide
4. AOTA (2014) OT Practice Guidelines for Home Modifications
5. CAOT (2024) Home Assessment and Modifications Practice Document
6. COTEC/WFOT (2022) Position Statement on OT and Accessibility

The BPC (`references/bpc/population-general/ot-cpg-built-environment.md`) documents each entry's scope, dimensional-content judgement, and bibliography status. Opus synthesis applied 2026-03-29 (commit `4de697dd`). Migration under CO-0006 on 2026-04-19 (commit `d0b865c1`).

### No multilingual / jurisdictional research performed

Unlike parameter-search BPCs (e.g., `mobility-built-environment`, `room-acoustic-performance`), this BPC did not run a multilingual research pass — Co-2 tier population is a transnational professional-body inventory, not a per-jurisdiction comparison. The PI rule #9 nine-step cross-jurisdictional synthesis structure does not apply at this level; it applies to parameter BPCs whose specifications differ across jurisdictions.
