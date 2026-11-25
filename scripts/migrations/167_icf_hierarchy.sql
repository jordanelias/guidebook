-- 167: the ICF lens gets a hierarchy (OD-74, OD-75; owner statements 2026-11-22: "ICF codes/classifications (e.g.
-- Neuromusculoskeletal and movement-related functions, Movement functions b750-789)").
--
-- `base_icf.parent_code` points a code at the code or block above it, so a browsing reader or a cell keyed on an umbrella
-- reaches the codes beneath it by the one rule the identity lens already uses (`base_taxonomy_identity.parent_code`,
-- T-055). A block is a row whose `icf_code` is its span (`b750–b789`), as the stored ranges `d310–d329` already are; the
-- existing CHECK admits it, so no other column changes. The component (b, d, e, s) is the level above the blocks and
-- stays `component`. Nothing is written here: the column is NULL on every row until a data batch sets it from the
-- persisted WHO payload (`db.py import-icf-tree`), which is a research pull request of its own (CLAUDE.md rule 10).
--
-- What reads it: `dbcore.family_sql('icf_code')` (the engine's gather, `db.py cell-status`, the derivation-handshake
-- audit) and `db.py icf-glossary`. Without it a cell keyed on b750–b789 gathers nothing from a figure linked to b765.

ALTER TABLE base_icf ADD COLUMN parent_code TEXT REFERENCES base_icf(icf_code);

PRAGMA user_version = 167;
