-- 083_one_icf_layer_in_base.sql
--
-- ONE ICF LAYER IN BASE, UNDER THE NAMES THE OWNER ALREADY RULED.
--
-- OWNER, 2026-09-16, three statements in sequence: "Please rename to icf / icf_codes",
-- then "why are we duplicating something if it's in base", then "do whatever makes sense
-- for all the ICF stuff".
--
-- THE MIDDLE ONE IS THE FINDING, AND THE ANSWER IS THAT I DUPLICATED IT. D-0169 (owner
-- selections, 2026-08-27, `references/project-standards.md`) already ruled the ICF naming
-- family, including `axes` -> `base_taxonomy_icf` and `axis_code` -> `icf_code`. On
-- 2026-09-13, executing the "give the ICF lens real ICF codes" ruling, I created a new
-- registry and called it `base_icf` -- a name I invented, for a role that was already
-- named. Two tables then stood in base for the ICF layer. That is rule 5's central
-- prohibition, committed by the session whose whole subject was the ICF lens, because the
-- search stopped before reaching D-0169. CLAUDE.md section 6 already records this exact
-- failure mode in its own words: "A ruling can be in the repository, in the file section 9
-- sends you to, and still fail to bind if the search stops at the first answer it finds."
--
-- ============================================================================
-- 1. THE CODE REGISTRY TAKES ITS RULED NAME
-- ============================================================================
--
-- `base_icf` holds the 72 real ICF b/d/e codes and is what the pipeline actually reads --
-- `assess_cell.derivation_handshake()`, `db.py`'s writers, `derivation_handshake_integrity`.
-- It is the ICF taxonomy, so it takes the ruled name and joins its siblings:
-- `base_taxonomy_medical` already exists under that grammar.
--
-- The column is already `icf_code`, which is what D-0169 ruled, so it does not move. Six
-- foreign keys point here; SQLite rewrites every one of them on RENAME, which is the
-- behaviour this migration wants (unlike 081, where a rename ASIDE silently re-pointed
-- children at a table about to be dropped).

ALTER TABLE base_icf RENAME TO base_taxonomy_icf;

-- D-0169's last row, and the owner's stated reason: `access_need_icf` maps `need_code` to
-- ICF **e**-codes, and a name one word from the taxonomy itself "would recreate the `items`
-- ambiguity deliberately". Naming it for what it holds settles it.

ALTER TABLE access_need_icf RENAME TO access_need_icf_codes;

-- ============================================================================
-- 2. THE GROUPING LAYER STOPS CALLING ITSELF AN AXIS -- AND STOPS LOOKING LIKE A
--    SECOND CODE REGISTRY
-- ============================================================================
--
-- `axes` is NOT the ICF code registry. Its 17 rows are curated GROUPINGS over ICF codes:
-- each carries a name, a mechanism, a falsification condition, a coverage status, and the
-- b/d codes it spans. D-0169 ruled it `base_taxonomy_icf` when it was the only candidate
-- for that name; it no longer is, and today's "why are we duplicating" is the ruling that
-- settles which table gets it.
--
-- So it takes a name that satisfies every constraint at once: no "axis" (owner, four times
-- over, most recently 2026-09-15 -- "axis is a term used to describe information"); inside
-- the `icf_*` family D-0169 ruled; and unmistakably not the code registry.
--
-- WHY IT IS RENAMED AND NOT RETIRED, stated because retiring it is the obvious next thought
-- and it is wrong today. Nothing in the pipeline reads it -- the only live consumer is its
-- own validator -- and its content is also rendered in `governance/functional-taxonomy.md`,
-- so it looks like dead scaffolding. But its two maps carry 74 curated assignments covering
-- 20 populations, where the direct `population_icf_links` covers 12. Retiring it loses that
-- coverage, and the obvious repair -- expanding each grouping row into one row per ICF code
-- it spans -- MANUFACTURES PRECISION THE SOURCE NEVER STATED: "MOB is an ALIAS of the
-- ambulant-movement grouping" is one recorded judgment, and expanding it to five claims
-- that MOB has a deficit in b770, b730, d450, d455 and d460 individually asserts five. That
-- is the fabrication class CLAUDE.md 5(c) names, arrived at by arithmetic instead of memory.
-- 53 population rows would have become 198, and 21 access-need rows 81.
--
-- So: renamed, kept whole, and its status recorded for the owner to rule on.

ALTER TABLE axes RENAME TO base_icf_groupings;
ALTER TABLE base_icf_groupings RENAME COLUMN axis_code TO grouping_code;

ALTER TABLE population_axis_map RENAME TO population_icf_grouping_map;
ALTER TABLE population_icf_grouping_map RENAME COLUMN axis_code TO grouping_code;

ALTER TABLE access_need_axis_map RENAME TO access_need_icf_grouping_map;
ALTER TABLE access_need_icf_grouping_map RENAME COLUMN axis_code TO grouping_code;

-- The two JSON columns that name groupings. D-0169 ruled `serves_icf` / `attaches_icf`;
-- they become `serves_icf_groupings` / `attaches_icf_groupings` for the same reason the
-- table did -- under the ruled names they would read as lists of ICF CODES, which is not
-- what they hold.

ALTER TABLE slugs RENAME COLUMN serves_axes TO serves_icf_groupings;
ALTER TABLE situations RENAME COLUMN attaches_axes TO attaches_icf_groupings;

-- ============================================================================
-- 3. WHAT THIS MIGRATION DOES NOT DO
-- ============================================================================
--
-- No row is added, changed or deleted. Every rename above is an identifier change, and
-- `migration_reproducibility` compares row counts for exactly this reason: a rename that
-- quietly moved data would show up there, and nothing here moves any.
--
-- `item_axis_links` is in D-0169's ruled table and does NOT exist in this schema -- the
-- item layer was emptied on 2026-09-01 and its junction is `item_taxonomy_links`, whose
-- `icf_code` migration 081 already re-pointed at the code registry. Naming it here would
-- have been a rename of nothing, which is how a caller sweep comes to report success over
-- an object that was never there.

PRAGMA user_version = 83;
