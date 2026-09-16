-- 084_retire_icf_grouping_layer.sql
--
-- THE ICF GROUPING LAYER IS DELETED.
--
-- OWNER RULING 2026-09-16: "Delete." — answering the question put at the end of migration
-- 083's record: whether the grouping layer earns its keep at all.
--
-- WHAT IT WAS. Seventeen coined groupings over ICF codes -- `DM-AMB` ambulant movement,
-- `DM-WHM` wheeled movement, and so on -- each carrying a name, the ICF b/d codes it
-- spans, a mechanism, a coverage status and a falsification condition; plus two maps
-- assigning populations (53 rows) and access needs (21 rows) to them.
--
-- WHY IT GOES, which is evidence and not preference (CLAUDE.md section 8: removing carries
-- no burden of proof, but it does require a reason):
--
--   * NOTHING DOWNSTREAM READ IT. The determination engine, the writers and the checks all
--     go through the ICF code registry and `population_icf_links`. The grouping layer's
--     only live consumer was `validate_icf_groupings.py` -- its own validator. A check
--     whose entire subject is a table nobody else reads is measuring its own scaffolding.
--   * IT WAS A SECOND HOME. The seventeen groupings are also rendered in full in
--     `governance/functional-taxonomy.md` -- code, name, ICF anchors, mechanism, coverage
--     -- which is where the doctrine actually lives and is maintained. Rule 5.
--   * ITS CODES WERE THE `AX-` PREFIX'S LAST HOME. The owner ruled that prefix out four
--     times before migration 082 struck it; the codes were re-minted `DM-*`, a prefix
--     derived from `icf_demands.demand_code` -- a family D-0169 had already REJECTED. So
--     the layer's identifiers were wrong twice in three days, in a table nobody read.
--
-- ============================================================================
-- WHAT IS LOST, STATED PLAINLY RATHER THAN IMPLIED
-- ============================================================================
--
-- 53 POPULATION ASSIGNMENTS COVERING 20 POPULATIONS. `population_icf_links` -- the direct
-- population-to-ICF-code map the pipeline actually reads -- covers 12. So eight populations
-- keep no ICF relation of any kind after this migration. That consequence was put to the
-- owner in those terms before the ruling, and the ruling was "Delete."
--
-- THE REPAIR IS NOT AN EXPANSION, and this is why the rows are dropped rather than
-- converted. Turning "MOB is an ALIAS of the ambulant-movement grouping" into five rows
-- claiming MOB has a deficit in b770, b730, d450, d455 and d460 individually asserts five
-- judgments where one was recorded -- CLAUDE.md 5(c)'s fabrication class, reached by
-- arithmetic instead of by memory. The eight uncovered populations get real rows when a
-- source states them, through `db.py add-population-icf-link`, which requires a provenance.
--
-- EVERY DELETED ROW REMAINS RECOVERABLE. All three tables were populated by
-- `scripts/migrations/057_baseline_2026-08-12.sql`, which is committed and immutable under
-- rule 3. That file is the archive; this comment is the pointer to it. Nothing here is
-- copied into `_archived/`, because section 8 is explicit that git history is the archive
-- and a copy would be a third home for data that already has two.
--
-- ============================================================================
-- THE DROPS
-- ============================================================================
--
-- Children before parent: both maps carry a foreign key into the registry, and dropping
-- the parent first would leave two tables pointing at nothing until their own DROP landed.
-- Nothing else references any of the three -- no view, no index, no other foreign key,
-- verified against `sqlite_master` and `PRAGMA foreign_key_list` before this was written.

DROP TABLE population_icf_grouping_map;

DROP TABLE access_need_icf_grouping_map;

DROP TABLE base_icf_groupings;

-- The two columns that named groupings from the other side. `slugs.serves_icf_groupings`
-- holds exactly one non-empty value -- `vestibular-balance-built-environment` serving
-- `["DM-BAL"]` -- and that fact is already stated in the slug's own reasoning document,
-- `references/bpc/health-and-symptom-management/vestibular-balance-built-environment.md`,
-- which names the balance demand in its opening line. `situations.attaches_icf_groupings`
-- holds none at all.
--
-- The columns go rather than being left NULL: an empty column that nothing can populate is
-- the unread field section 8 calls the same defect as an unregistered check.

ALTER TABLE slugs DROP COLUMN serves_icf_groupings;

ALTER TABLE situations DROP COLUMN attaches_icf_groupings;

PRAGMA user_version = 84;
