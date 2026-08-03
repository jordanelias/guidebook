"""
schemas/directness.py — consolidated rule-based directness model (Stage 2.2).

Per governance/evidence-methodology.md §1.4 (scale-conditioned weighting),
§1.6 (mode-asymmetry), and §1.7 (directness as a conditioning layer —
grain-matching); doctrine SHA 373255e; decision D-D. §1.7 names this build:
"The scattered directness primitives currently recorded across the schema
(match_grade, value_match, passes_strict, relevance notes) are consolidated
into one rule-based directness model at Stage 2.2."

MODEL
-----
Directness is a CONDITIONING LAYER over the single population-anchored ladder
(schemas/tier_derivation.py) — not a separate hierarchy per scale (D-D). A source
is weighted by how well its GRAIN matches the GRAIN OF THE CLAIM, bidirectionally
(GRADE directness). The project REJECTS a "most-specific-to-least-specific"
gradient: grain-match is the axis, not specificity (§1.7).

Three structured dimensions replace the free-text notes:

  1. population-directness  <- evidence_population_match.match_grade
  2. value-directness       <- reasoning_doc_citations.value_match
                               (+ spec_value_probes.passes_strict corroboration;
                                home substrate: source_value_extractions, DR-2026-05-28-b)
  3. scale-directness       <- NEW in 2.2: grain-match between the evidence's grain
                               and the claim's design scale, mode-asymmetric (§1.6).

EXCLUDED AS A GHOST
-------------------
room_item_population.applicability is NOT consolidated: that table is absent from
the canonical migration-built DB, and scripts/db/ is not referenced by any CI
workflow (legacy build path superseded by scripts/migrate_db.py). Consolidating it
would consolidate a ghost.

BOUNDARY
--------
This module is the model. Storage of the consolidated directness — including a
scale_directness column — is Stage 2.3's evidence_cell_state / convergence_assessment
tables; they apply this model. The conditioning is CATEGORICAL, not a number
(no false-precision confidence score; cf. the convergence assessment, §convergence).
"""

from typing import Optional


# ---------------------------------------------------------------------------
# Design scales (the CLAIM's grain) — Design Hierarchy, §1.4
# ---------------------------------------------------------------------------
SCALE_UNIVERSAL = "universal"    # universal / code-compliant   (Universal Mode)
SCALE_POPULATION = "population"  # population-informed range+median (Population scale)
SCALE_PERSON = "person"          # person-specific, OT-resolved  (Person scale)

ALL_SCALES = frozenset({SCALE_UNIVERSAL, SCALE_POPULATION, SCALE_PERSON})

# Existing encoding in schemas/enums.py RecommendationStrength <-> design scale.
# Kept as a mapping (not a redefinition) so the two stay reconciled.
SCALE_FROM_RECOMMENDATION = {
    "STRONG_UNIVERSAL": SCALE_UNIVERSAL,
    "CONDITIONAL_POPULATION": SCALE_POPULATION,
    "CONDITIONAL": SCALE_PERSON,
}


# ---------------------------------------------------------------------------
# Evidence grain (the SOURCE's grain) — §1.7
# ---------------------------------------------------------------------------
GRAIN_AGGREGATE = "aggregate"  # population-level synthesis (SR / meta-analysis; co-2)
GRAIN_SPECIFIC = "specific"    # parameter/individual-level primary study (clinical; Co-1; grey)
GRAIN_CODE = "code"            # standards / code floor (standard_eb / national_fw / code)

ALL_GRAINS = frozenset({GRAIN_AGGREGATE, GRAIN_SPECIFIC, GRAIN_CODE})

# Default grain by evidence_type (the 8-value enum from tier_derivation.py).
# Grain is, in principle, per-source; this is the common-case default a caller
# may override when a specific source's grain differs from its type's default.
GRAIN_FROM_EVIDENCE_TYPE = {
    "sr_meta": GRAIN_AGGREGATE,
    "co2": GRAIN_AGGREGATE,
    "clinical": GRAIN_SPECIFIC,
    "co1": GRAIN_SPECIFIC,
    "grey": GRAIN_SPECIFIC,
    "standard_eb": GRAIN_CODE,
    "national_fw": GRAIN_CODE,
    "code": GRAIN_CODE,
}


# ---------------------------------------------------------------------------
# Dimension 1 — population-directness  (<- evidence_population_match.match_grade)
# match_grade is already a structured grade; this is identity-with-validation,
# bringing it under the consolidated model.
# ---------------------------------------------------------------------------
POP_EXACT = "EXACT"
POP_PARTIAL = "PARTIAL"
POP_PROXY = "PROXY"
POP_MISMATCH = "MISMATCH"

ALL_POP_DIRECTNESS = frozenset({POP_EXACT, POP_PARTIAL, POP_PROXY, POP_MISMATCH})


def population_directness_from_match_grade(match_grade: Optional[str]) -> Optional[str]:
    """Map evidence_population_match.match_grade -> population-directness grade."""
    if match_grade is None or match_grade == "":
        return None
    g = match_grade.strip().upper()
    if g not in ALL_POP_DIRECTNESS:
        raise ValueError(f"unknown match_grade {match_grade!r}; expected one of {sorted(ALL_POP_DIRECTNESS)}")
    return g


# ---------------------------------------------------------------------------
# Dimension 2 — value-directness  (<- reasoning_doc_citations.value_match
#                                    + spec_value_probes.passes_strict)
# value_match vocab: EXACT / WITHIN-TOLERANCE / PAYWALL / CONTRADICTED / NOT-FOUND.
# PAYWALL is a verification state, not a directness grade -> None (ungradeable).
# ---------------------------------------------------------------------------
VAL_EXACT = "EXACT"
VAL_WITHIN = "WITHIN-TOLERANCE"
VAL_NOT_FOUND = "NOT-FOUND"
VAL_CONTRADICTED = "CONTRADICTED"

ALL_VAL_DIRECTNESS = frozenset({VAL_EXACT, VAL_WITHIN, VAL_NOT_FOUND, VAL_CONTRADICTED})
_VALUE_MATCH_UNGRADEABLE = frozenset({"PAYWALL"})


def value_directness(value_match: Optional[str]) -> Optional[str]:
    """Map reasoning_doc_citations.value_match -> value-directness grade.
    PAYWALL (unverifiable) and NULL return None — no directness can be asserted."""
    if value_match is None or value_match == "":
        return None
    g = value_match.strip().upper()
    if g in _VALUE_MATCH_UNGRADEABLE:
        return None
    if g not in ALL_VAL_DIRECTNESS:
        raise ValueError(f"unknown value_match {value_match!r}; expected one of "
                         f"{sorted(ALL_VAL_DIRECTNESS)} (or PAYWALL/NULL -> None)")
    return g


def value_corroborated_by_strict(passes_strict) -> bool:
    """spec_value_probes.passes_strict (rule #8 strict termination) corroborates a
    value-directness grade. 1 -> corroborated; 0/None -> not."""
    return passes_strict == 1 or passes_strict == "1"


# ---------------------------------------------------------------------------
# Dimension 3 — scale-directness  (NEW in 2.2)
# Bidirectional grain-match per §1.7, mode-asymmetric per §1.6.
# ---------------------------------------------------------------------------
SD_DIRECT = "DIRECT"               # grain matches the claim's scale
SD_ADJACENT = "ADJACENT"           # one scale off; supportive, not anchoring at full weight
SD_DOWN_WEIGHTED = "DOWN-WEIGHTED"  # grain mismatch — too coarse / over-generalized for the claim
SD_NON_ANCHORING = "NON-ANCHORING"  # code-grain outside Universal: convergence-not-evidence (§1.6/§3)

ALL_SCALE_DIRECTNESS = frozenset({SD_DIRECT, SD_ADJACENT, SD_DOWN_WEIGHTED, SD_NON_ANCHORING})


def scale_directness(evidence_grain: str, claim_scale: str,
                     generalizes_beyond_measured: bool = False) -> str:
    """Grain-match between a source's grain and a claim's design scale.

    Encodes §1.7's two named cases bidirectionally and §1.6's mode-asymmetry:

      - AGGREGATE (population grain): DIRECT for a population claim; DOWN-WEIGHTED
        for a person-specific claim (grain too coarse for the individual);
        ADJACENT at Universal (can support raising the code floor).
      - SPECIFIC (parameter/individual grain): DIRECT for a person claim; at the
        population scale DIRECT unless it generalizes beyond what it measured
        (then DOWN-WEIGHTED); ADJACENT at Universal.
      - CODE (standards/code grain): DIRECT only at Universal (it IS the floor);
        NON-ANCHORING at Population/Person (convergence-not-evidence, §1.6/§3).
    """
    if evidence_grain not in ALL_GRAINS:
        raise ValueError(f"unknown evidence_grain {evidence_grain!r}; expected one of {sorted(ALL_GRAINS)}")
    if claim_scale not in ALL_SCALES:
        raise ValueError(f"unknown claim_scale {claim_scale!r}; expected one of {sorted(ALL_SCALES)}")

    if evidence_grain == GRAIN_CODE:
        return SD_DIRECT if claim_scale == SCALE_UNIVERSAL else SD_NON_ANCHORING

    if evidence_grain == GRAIN_AGGREGATE:
        if claim_scale == SCALE_POPULATION:
            return SD_DIRECT
        if claim_scale == SCALE_PERSON:
            return SD_DOWN_WEIGHTED
        return SD_ADJACENT  # universal

    # GRAIN_SPECIFIC
    if claim_scale == SCALE_PERSON:
        return SD_DIRECT
    if claim_scale == SCALE_POPULATION:
        return SD_DOWN_WEIGHTED if generalizes_beyond_measured else SD_DIRECT
    return SD_ADJACENT  # universal


# ---------------------------------------------------------------------------
# Consolidation — the conditioning layer over the tier (categorical, not a number)
# ---------------------------------------------------------------------------
COND_DIRECT = "DIRECT"               # full tier weight for this claim
COND_DOWN_WEIGHTED = "DOWN-WEIGHTED"  # tier weight reduced by grain mismatch on >=1 dimension
COND_DISCOUNTED = "DISCOUNTED"        # cannot anchor: population MISMATCH or value CONTRADICTED
COND_NON_ANCHORING = "NON-ANCHORING"  # code-grain outside Universal (convergence-not-evidence)

ALL_CONDITIONING = frozenset({COND_DIRECT, COND_DOWN_WEIGHTED, COND_DISCOUNTED, COND_NON_ANCHORING})


def consolidate(population_directness: Optional[str],
                value_directness_grade: Optional[str],
                scale_directness_grade: Optional[str],
                value_corroborated: bool = False) -> Optional[str]:
    """Combine the three dimension grades into one conditioning grade.

    A dimension passed as None is "not applicable to this claim" and does not
    block. Rule order (most-restrictive first):
      1. scale NON-ANCHORING            -> NON-ANCHORING (code-grain off Universal)
      2. population MISMATCH / value CONTRADICTED -> DISCOUNTED (cannot anchor)
      3. every applicable dimension at full grain-match -> DIRECT
      4. otherwise (>=1 partial/proxy/within/adjacent/down-weighted) -> DOWN-WEIGHTED
    """
    if scale_directness_grade == SD_NON_ANCHORING:
        return COND_NON_ANCHORING
    if population_directness == POP_MISMATCH or value_directness_grade == VAL_CONTRADICTED:
        return COND_DISCOUNTED

    pop_full = population_directness in (POP_EXACT, None)
    val_full = (value_directness_grade in (VAL_EXACT, None)
                or (value_directness_grade == VAL_WITHIN and value_corroborated))
    scale_full = scale_directness_grade in (SD_DIRECT, None)

    if scale_directness_grade is None and population_directness is None and value_directness_grade is None:
        return None  # nothing to condition on
    if pop_full and val_full and scale_full:
        return COND_DIRECT
    return COND_DOWN_WEIGHTED


def directness_from_primitives(match_grade: Optional[str] = None,
                               value_match: Optional[str] = None,
                               passes_strict=None,
                               evidence_type: Optional[str] = None,
                               claim_scale: Optional[str] = None,
                               evidence_grain: Optional[str] = None,
                               generalizes_beyond_measured: bool = False) -> dict:
    """Single consolidation entry point: the scattered DB primitives + the new
    scale dimension -> one structured directness record. This is the
    consolidation §1.7 names. Returns the per-dimension grades and the
    overall conditioning; storage of this record is Stage 2.3."""
    pop = population_directness_from_match_grade(match_grade)
    val = value_directness(value_match)
    corrob = value_corroborated_by_strict(passes_strict)

    grain = evidence_grain
    if grain is None and evidence_type is not None:
        grain = GRAIN_FROM_EVIDENCE_TYPE.get(evidence_type)
    if grain is not None and grain not in ALL_GRAINS:
        raise ValueError(f"unknown evidence_grain {grain!r}")

    scale = None
    if grain is not None and claim_scale is not None:
        scale = scale_directness(grain, claim_scale, generalizes_beyond_measured)

    conditioning = consolidate(pop, val, scale, corrob)
    return {
        "population_directness": pop,
        "value_directness": val,
        "value_corroborated": corrob,
        "evidence_grain": grain,
        "scale_directness": scale,
        "conditioning": conditioning,
    }


def check_directness_record(rec: dict) -> list:
    """Return a list of vocabulary violations in a directness record (empty = clean).
    Mirrors tier_derivation.check_tier_consistency's role for audit use."""
    problems = []
    if rec.get("population_directness") not in (None,) and rec["population_directness"] not in ALL_POP_DIRECTNESS:
        problems.append(f"population_directness {rec['population_directness']!r} not in vocab")
    if rec.get("value_directness") not in (None,) and rec["value_directness"] not in ALL_VAL_DIRECTNESS:
        problems.append(f"value_directness {rec['value_directness']!r} not in vocab")
    if rec.get("evidence_grain") not in (None,) and rec["evidence_grain"] not in ALL_GRAINS:
        problems.append(f"evidence_grain {rec['evidence_grain']!r} not in vocab")
    if rec.get("scale_directness") not in (None,) and rec["scale_directness"] not in ALL_SCALE_DIRECTNESS:
        problems.append(f"scale_directness {rec['scale_directness']!r} not in vocab")
    if rec.get("conditioning") not in (None,) and rec["conditioning"] not in ALL_CONDITIONING:
        problems.append(f"conditioning {rec['conditioning']!r} not in vocab")
    return problems
