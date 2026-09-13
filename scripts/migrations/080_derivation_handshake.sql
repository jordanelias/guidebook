-- 080_derivation_handshake.sql
--
-- H2/H3/H4 — the derivation handshake, the population<->function map, and the gate.
-- Ratified 2026-07-13 (DR-2026-07-13-value-genealogy-and-derivation-handshake); stated in
-- `governance/evidence-architecture.md` section 5.5 and carrying an
-- `[ENGINE-LAG 2026-08-15]` marker ever since, whose own text names exactly what is
-- missing: "`specifications` carries neither `functional_basis` nor `derivation_paths`;
-- `population_icf_links` does not exist; `assess_cell.py` implements no H4 gate."
--
-- WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT IT. The corpus derives values along two
-- paths that have never been required to meet: TOP-DOWN from population and community
-- (BPCs, Co-1, every population join) and BOTTOM-UP from function (the ICF-indexed
-- `references/fdr/` corpus, population-blind at collection). Nothing requires them to
-- agree before a value ships, and -- the marker's closing sentence -- "a `population_only`
-- determination cannot be distinguished by query from an unexamined one". The same
-- absence-versus-finding collision this session has now closed at the identifier, the
-- extraction and the value.
--
-- ============================================================================
-- H2. THE HANDSHAKE, ON THE DETERMINATION
-- ============================================================================
--
-- `derivation_paths` is the ruled vocabulary: dual / population_only / function_only.
-- Dual-path convergence is recorded as itself evidence -- doctrine #3 (convergence across
-- independent axes) extended from evidence axes to derivation paths.

ALTER TABLE specifications ADD COLUMN functional_basis TEXT;

ALTER TABLE specifications ADD COLUMN derivation_rationale TEXT;

-- THE CULTURAL/DIGNITY PROTECTION, AS A COLUMN RATHER THAN AN INFERENCE.
--
-- Ratified as a NAMED COMMITMENT 2026-07-13, and quoted here because the schema is where
-- it becomes checkable: claims whose normative force is community-rooted remain FULLY
-- ASSERTABLE as `population_only`; the handshake makes a derivation explicit, it never
-- requires a mechanism where the claim is cultural, and NO FUNCTIONAL DERIVATION MAY
-- FLATTEN, REDUCE OR OVERRIDE A COMMUNITY CLAIM. There is no bottom-up override of Co-1.
-- "A signing-space corridor width is not a wheelchair-envelope calculation that came out
-- wrong; it is a different claim, held by the community whose language it serves."
--
-- THE BOUNDARY CRITERION IS WHY THIS IS A REF LIST AND NOT A FLAG. The protection is
-- ANCHORED, not self-declared: "community-rooted" means anchored by Co-1/participatory
-- provenance per `co1_source_type`, or an equivalent documented community process. A
-- `population_only` claim WITHOUT such an anchor is simply a single-path claim owing the
-- standard named-path rationale; it gains no cultural exemption by assertion. A boolean
-- could be set by anyone; a JSON array of the ref_ids that anchor it can be checked
-- against those sources' own `co1_source_type`, which is what stops the protection
-- becoming a route around the mechanism requirement.
ALTER TABLE specifications ADD COLUMN cultural_claim_anchor TEXT
    CHECK (cultural_claim_anchor IS NULL OR json_valid(cultural_claim_anchor));

-- THE RULE, MECHANISED. A single-path determination owes a named-path rationale UNLESS it
-- is population_only and culturally anchored. Expressible as a sibling-referencing column
-- CHECK, which is the one form ALTER TABLE admits -- so the dignity line stops being
-- "doctrine binding on authors" (the marker's own words) and becomes a state the database
-- refuses to hold wrongly.
ALTER TABLE specifications ADD COLUMN derivation_paths TEXT
    CHECK (derivation_paths IS NULL
        OR (derivation_paths = 'dual')
        OR (derivation_paths = 'function_only' AND derivation_rationale IS NOT NULL)
        OR (derivation_paths = 'population_only'
            AND (derivation_rationale IS NOT NULL OR cultural_claim_anchor IS NOT NULL)));

-- ============================================================================
-- H3. THE POPULATION<->FUNCTION MAP IS DATA, NOT SKILL PROSE
-- ============================================================================
--
-- "One table: population code x ICF d-code x mechanism x confidence x provenance,
-- promoting the FDA mapping and the armature's mapping-confidence classifications out of
-- prose into provenance-bearing rows." Until now that mapping lived only in
-- `skills/functional-deficit-auditor_SKILL.md` as a markdown table -- unvalidated prose
-- that no FK could check and no query could read.
--
-- SIMULTANEOUSLY THE FORWARD MAP AND THE SUBSTRATE FOR REVERSE-MAPPING, which is the point:
-- reverse-mapping "is what would have flagged DEAF's absence from the corridor item's
-- population links MECHANICALLY rather than by eye".
--
-- `icf_code` IS FREE TEXT, DELIBERATELY, and this is a real divergence from the project's
-- usual FK discipline. The FDA mapping states ranges ("d310-d329", "d710-d729") and the
-- live `axes` table holds 17 AX- codes, not ICF d-codes: there is no table here to point
-- at. A fabricated FK into `axes` would assert a crossing nobody ruled. The ICF is an
-- external published vocabulary; when a d-code registry lands, this column gets its FK and
-- this comment gets deleted.
CREATE TABLE population_icf_links (
    link_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    population_code     TEXT NOT NULL REFERENCES populations(population_code),
    icf_code            TEXT NOT NULL,
    mechanism           TEXT NOT NULL,
    mapping_confidence  TEXT NOT NULL
                        CHECK (mapping_confidence IN ('high_predictive',
                                                      'moderate_contextual',
                                                      'low_indicative')),
    -- WHERE THIS ROW CAME FROM. A mapping with no provenance is the skill prose again,
    -- in a table. 'fda-skill-2026-09-13' is the promotion of the audited markdown; a
    -- later row derived from a study names its ref_id.
    provenance          TEXT NOT NULL,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    -- One row per (population, code, mechanism): the same population may reach one ICF
    -- code by two different mechanisms (SCI is "biomechanical + autonomic"), and both are
    -- real. Collapsing them would lose the distinction the mechanism column exists for.
    UNIQUE (population_code, icf_code, mechanism)
);

CREATE INDEX idx_picf_icf ON population_icf_links(icf_code);

-- ============================================================================
-- H4. THE ADVISORY CHECKS BECOME GATES, WITH DEADLOCK DISCIPLINE
-- ============================================================================
--
-- "FDA verdicts UNLINKED / MISLINKED / UNDER-CONSERVATIVE and FDR delta-classification
-- CONTRADICTS force the affected cell to `provisional` -- never `stated` -- until resolved."
--
-- THREE DISCIPLINES, each a column here:
--
--   * "The gate binds ONLY WHERE A CHECK HAS ACTUALLY RUN: no silent pretence of coverage."
--     So the gate is a table of rows a check wrote, not a flag on the determination. Zero
--     rows means zero cells gated, which is the correct reading of "no check has run" --
--     and it is why this table being empty today is the doctrine working rather than a gap.
--
--   * "Gate rows carry the tier and type of the triggering source, so a grey-tier
--     CONTRADICTS cannot pin a T1-anchored cell indefinitely and thereby INVERT THE LADDER."
--     Hence trigger_tier / trigger_evidence_type, NOT NULL: a gate row that cannot say how
--     strong its trigger was is a gate that can invert the ladder by omission.
--
--   * "Resolution is a NAMED PATH -- evidence-auditor adjudication recorded on the cell
--     together with its rationale -- so no cell sits at `provisional` with no owner of
--     resolution." Hence resolved_by_session + resolution_rationale, and a CHECK that one
--     cannot arrive without the other.
CREATE TABLE determination_gates (
    gate_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    parameter_id        INTEGER NOT NULL REFERENCES base_parameters(parameter_id),
    -- The lens the finding applies to, NULL meaning every lens on this parameter. Not an
    -- FK set like specifications' four, because a gate is raised against a parameter by an
    -- audit that may not know which cells exist yet.
    identity_code       TEXT REFERENCES populations(population_code),
    verdict             TEXT NOT NULL
                        CHECK (verdict IN ('UNLINKED', 'MISLINKED',
                                           'UNDER-CONSERVATIVE', 'CONTRADICTS')),
    -- The ladder-inversion guard: how strong the thing raising the gate actually is.
    trigger_ref_id      TEXT REFERENCES evidence_sources(ref_id),
    trigger_tier        INTEGER NOT NULL CHECK (trigger_tier BETWEEN 1 AND 6),
    trigger_evidence_type TEXT NOT NULL,
    detail              TEXT NOT NULL,
    raised_at           TEXT NOT NULL,
    raised_by_session   TEXT NOT NULL,
    resolved_at         TEXT,
    resolved_by_session TEXT,
    resolution_rationale TEXT,
    CHECK ((resolved_at IS NULL AND resolved_by_session IS NULL
            AND resolution_rationale IS NULL)
        OR (resolved_at IS NOT NULL AND resolved_by_session IS NOT NULL
            AND resolution_rationale IS NOT NULL))
);

CREATE INDEX idx_gates_open ON determination_gates(parameter_id, resolved_at);

-- The open gates a determination must read, with the strength of what raised them. A
-- cross-stage view: specification reads it, judgment/evidence raise it.
CREATE VIEW v_open_determination_gates AS
SELECT g.gate_id, g.parameter_id, g.identity_code, g.verdict,
       g.trigger_ref_id, g.trigger_tier, g.trigger_evidence_type, g.detail,
       g.raised_at, g.raised_by_session
  FROM determination_gates g
 WHERE g.resolved_at IS NULL;

PRAGMA user_version = 80;
