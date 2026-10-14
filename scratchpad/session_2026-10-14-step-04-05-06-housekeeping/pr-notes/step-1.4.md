# PR body notes, step 1.4 (axes retired as one act) -- branch stack/1.4-axes-retired (stacked on 1.3)
Migration drop_axes (AFTER_DATA: 20260920060857, R3 marker in header): drops axes (17 rows), access_need_axis_map (21), population_axis_map (53), situations (0), slugs.serves_axes (1 value ["AX-BAL"]).
Verified: --rebuild of the step-1.1 tree reproduces all rows; no data migration writes the objects; only inbound FKs are the two maps into axes.
validate_axes.py + base-demand-vocabulary criterion deleted; FK-to-base_icf replacement derived (5 icf_code columns with real FKs to base_icf).
Instrument: C-017 closed (R35 declares axes-live sentences stale); atoms ENT-105, ENT-156, OPI-049, DRS-199, DRS-006, DRS-023 SUPERSEDED by R35; ENT-076 flagged.
Owner items: D-0170, D-0184, functional-taxonomy sentences stale per R35 (not edited); schemas/slug.py serves_axes goes with R5; AX- strings in references/ -> 1.6(c).
Contract: criterion base-demand-vocabulary removed (owner merge).
Gates: preflight PASS; rebuild parity; pipeline_contract_audit verifiable 30 -> 29; build_graph --check 0.

## After the adversarial pass (ab52a1b on stack/1.4; 1.3's C-020 closed in 4f90739)
F1/F2 repaired as text: migration 109's header and RULINGS R3 now say population_icf_links is a PARTIAL re-derivation (map: 20 populations; links: 12; ADHD, DEAFBLIND, EPI, MS, VES have map rows and no link row).
OWNER ITEMS: re-derive population-to-ICF links for ADHD, DEAFBLIND, EPI, MS, VES; the 2026-09-11 medical-lens ruling's ACTION still says "from populations and axes" (axes is gone; no supersession recorded);
documents D-0170, D-0184, functional-taxonomy (R35 stale) remain unedited. F3 message restored. F4 C-017 restored narrowed. F5 atoms fixed. F6 E07 foreign_key_check test added (red on planted violation).
F7 (C-020) closed in 1.3. F8 partial.
