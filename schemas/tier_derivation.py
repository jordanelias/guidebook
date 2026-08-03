"""
schemas/tier_derivation.py — derive evidence tier from (evidence_type, scope).

Per the ratified evidence hierarchy (governance/tier-system.md, doctrine SHA
373255e; decisions D-A, D-D, D-E) and governance/evidence-methodology.md §1.1.

Closes R6 ("tier hand-set, not derivable"): tier becomes a function of
evidence_type and a `scope` discriminator rather than a free integer.

`scope` only does disambiguation work for the two evidence types that span
more than one tier:

  - clinical:     high_control  -> Tier 1   intervention / RCT / biomechanical /
                                            sensory-threshold studies. Per D-E,
                                            directly-relevant high-control non-OT
                                            primary research is admitted at T1,
                                            not demoted.
                  lower_control -> Tier 3   cross-sectional, observational,
                                            qualitative, single-centre.

  - standard_eb:  national      -> Tier 2   named-organisation / national
                                            evidence-based standard (DPO /
                                            professional-body stream).
                  international  -> Tier 4   international standard with an
                                            evidence basis (ISO / IEC / EN).

For the remaining six evidence types tier is fixed by evidence_type alone, and
scope carries the sentinel 'intrinsic':

  co1 -> 1 (Co-1)   co2 -> 2 (Co-2)   sr_meta -> 2 (D-A)   grey -> 3
  national_fw -> 5   code -> 6
"""

from typing import Optional

# --- Scope discriminator values ---
SCOPE_HIGH_CONTROL = "high_control"
SCOPE_LOWER_CONTROL = "lower_control"
SCOPE_NATIONAL = "national"
SCOPE_INTERNATIONAL = "international"
SCOPE_INTRINSIC = "intrinsic"

ALL_SCOPES = frozenset({
    SCOPE_HIGH_CONTROL,
    SCOPE_LOWER_CONTROL,
    SCOPE_NATIONAL,
    SCOPE_INTERNATIONAL,
    SCOPE_INTRINSIC,
})

# --- (evidence_type, scope) -> tier : the ratified ladder as a total function
#     over the valid pairs. ---
TIER_MAP = {
    ("clinical", SCOPE_HIGH_CONTROL): 1,
    ("clinical", SCOPE_LOWER_CONTROL): 3,
    ("co1", SCOPE_INTRINSIC): 1,
    ("sr_meta", SCOPE_INTRINSIC): 2,
    ("standard_eb", SCOPE_NATIONAL): 2,
    ("standard_eb", SCOPE_INTERNATIONAL): 4,
    ("co2", SCOPE_INTRINSIC): 2,
    ("grey", SCOPE_INTRINSIC): 3,
    ("national_fw", SCOPE_INTRINSIC): 5,
    ("code", SCOPE_INTRINSIC): 6,
}

# Admissible scope values per evidence_type (for validation / CHECK parity).
VALID_SCOPES_BY_TYPE = {
    "clinical": frozenset({SCOPE_HIGH_CONTROL, SCOPE_LOWER_CONTROL}),
    "standard_eb": frozenset({SCOPE_NATIONAL, SCOPE_INTERNATIONAL}),
    "co1": frozenset({SCOPE_INTRINSIC}),
    "co2": frozenset({SCOPE_INTRINSIC}),
    "sr_meta": frozenset({SCOPE_INTRINSIC}),
    "grey": frozenset({SCOPE_INTRINSIC}),
    "national_fw": frozenset({SCOPE_INTRINSIC}),
    "code": frozenset({SCOPE_INTRINSIC}),
}


class TierDerivationError(ValueError):
    """Raised when (evidence_type, scope) has no ratified tier."""


def derive_tier(evidence_type: str, scope: Optional[str]) -> int:
    """Return the canonical tier for (evidence_type, scope), else raise.

    Raises TierDerivationError when the pair is not in the ratified map:
    an unknown evidence_type, or a missing / invalid scope for a multi-tier
    type. Callers that want a soft check should use check_tier_consistency.
    """
    key = (evidence_type, scope)
    if key in TIER_MAP:
        return TIER_MAP[key]
    valid = sorted(VALID_SCOPES_BY_TYPE.get(evidence_type, set()))
    raise TierDerivationError(
        f"no ratified tier for (evidence_type={evidence_type!r}, scope={scope!r}); "
        f"valid scopes for this type: {valid or 'UNKNOWN evidence_type'}"
    )


def expected_scope_from_tier(evidence_type: str, tier: int) -> Optional[str]:
    """Inverse helper: the scope implied by a (evidence_type, tier) pair when
    exactly one scope maps there, else None.

    Used ONLY to backfill `scope` from an already-consistent stored tier during
    migration 022's companion data migration. This is a bootstrap convenience,
    NOT independent ground truth: it asserts only that the stored tier and the
    backfilled scope agree, not that either matches the source's actual study
    design / standard level. Independent validation of scope against source
    content is deferred to the evidence-base passes (Phase B / E).
    """
    candidates = [s for (t, s), tt in TIER_MAP.items() if t == evidence_type and tt == tier]
    return candidates[0] if len(candidates) == 1 else None


def check_tier_consistency(evidence_type: str, scope: Optional[str], stored_tier: int) -> bool:
    """True iff stored_tier equals the tier derived from (evidence_type, scope).

    Rows for which this returns False — including rows whose (type, scope) pair
    raises TierDerivationError — are exactly the Stage 2.5 tier-consistency
    sweep targets.
    """
    try:
        return derive_tier(evidence_type, scope) == stored_tier
    except TierDerivationError:
        return False
