"""
schemas/extraction_relation.py — the comparator junction, migration 075.

Mirrors `extraction_relations`, added 2026-09-13 alongside two nullable columns on
`source_value_extractions` (`figure_role`, `comparator` — added directly to
`schemas/source_value_extraction.py`, not duplicated here). No ruling created this
table; it closes a measured gap: a figure this project extracts is routinely stated
RELATIVE to something — a run-length limit a slope only holds under, a code's own
number a T1 study tested subjects against rather than measured independently, a
baseline a source states an increment over — and before this table there was no
column anywhere that could name what the "something" was. `db.py add-extraction`
requires `--claim-text` so every row carries the source's own words; nothing before
this table required the row to say what its number was measured or stated against.

    source_value_extractions (the figure)
       ↓ from_extraction_id, NOT NULL, no UNIQUE — one figure may carry SEVERAL
       │  comparator edges (a slope is both condition_on a run limit AND
       │  audited_against a code's stated maximum)
    extraction_relations (this model — the comparator edge)
       ↓ to_extraction_id (a row this project holds) — OR — to_label (prose naming
         a referent this project has not captured as its own row)

THE REFERENT IS A ROW OR A LABEL, NEVER BOTH AND NEVER NEITHER. `exactly_one_referent`
below mirrors the table's own CHECK; see that method's docstring for why a
row-and-a-label together would be as wrong as neither. Rule 5 ("point, do not
copy") is why a row referent is preferred wherever one exists — `to_label` exists
only because the project cannot always point at a row it has not captured.

VOCABULARIES ARE PLAIN str HERE, NOT Enums, on purpose. CLAUDE.md section 4: "vocabularies
come from the schema, not a list in code" — `dbcore.check_values()` reads each column's
own CHECK, and `db.py`'s writer (once one exists) refuses against that same declaration.
An Enum class would be a second, independent home for these six vocabularies that could
silently drift from the migration's CHECK the first time it changes; `schemas/
source_value_extraction.py`'s own docstring records exactly this reasoning for why
`root_type` / `measurement_paradigm` / `device_class` are deliberately NOT enums, and
calls the three that still are "predating that rule". This file is written after the
rule, not before it, so none of its six vocabulary columns are enums. The shape rules
below (which fields may or must accompany which) ARE validated here, because a shape
rule spans several columns and no single CHECK-per-column reading could express it —
that is a different kind of fact from "which strings are members of this vocabulary."
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator

# The eight `relation` values, one line of meaning each — copied from the CHECK this
# migration wrote, not the other way round (CLAUDE.md section 4).
#   tested_at        subjects were physically measured at/against this referent.
#   audited_against  tested whether subjects fit within the referent's own stated
#                    limit, rather than measuring an independent value.
#   confirms         an independent measurement agrees with the referent's value.
#   insufficient     the source asserts the referent's value is NOT ENOUGH.
#   exceeds          the source asserts the referent's value is more than needed.
#   delta_over       a stated increment over a baseline, not an absolute figure.
#   condition_on     holds only given a second figure this project also holds as a row.
#   derived_from     computed from the referent; pairs with input_role.
RELATION_MEANINGS = {
    "tested_at": "subjects were physically measured at/against this referent",
    "audited_against": "tested whether subjects fit the referent's own stated limit",
    "confirms": "an independent measurement agrees with the referent's value",
    "insufficient": "the source asserts the referent's value is not enough",
    "exceeds": "the source asserts the referent's value is more than needed",
    "delta_over": "a stated increment over a baseline, not an absolute figure",
    "condition_on": "holds only given a second figure this project also holds as a row",
    "derived_from": "computed from the referent; pairs with input_role",
}


class ExtractionRelation(BaseModel):
    """One comparator edge: what a figure is stated relative to, and how.

    Many of these may point FROM the same extraction (a slope is both
    condition_on a run limit and audited_against a code's stated maximum), which
    is why there is no UNIQUE constraint on from_extraction_id alone — only on the
    full edge identity (idx_xr_identity), which forbids writing the same edge
    twice, not writing several different edges from one figure.
    """

    relation_id: Optional[int] = None  # autoincrement PK

    from_extraction_id: int = Field(
        ...,
        description="FK source_value_extractions.extraction_id — THE FIGURE this "
                    "edge qualifies.",
    )
    relation: str  # live vocabulary: RELATION_MEANINGS keys / the table's own CHECK

    # ── The referent: a row, or a label — never both, never neither ──────────
    to_extraction_id: Optional[int] = Field(
        None, description="FK source_value_extractions.extraction_id — a referent "
                          "this project already holds as its own row."
    )
    to_label: Optional[str] = Field(
        None, description="Prose naming the referent when it is not a row this "
                          "project has captured — a code clause, a source's own "
                          "sample, or a referent the source itself never names."
    )
    to_kind: Optional[str] = None  # 'standard'/'own_sample'/'prior_source'/'unnamed';
                                   # meaningful only when to_label is set

    stated: str      # 'named'/'unnamed'/'inferred' — the column's own CHECK
    input_role: Optional[str] = None  # 'base'/'delta'/'factor'; set iff relation=='derived_from'

    quote: str = Field(
        ..., description="The source's own words for the comparison, verbatim. "
                         "Mirrors the verbatim floor db.py add-extraction already "
                         "puts on --claim-text and observed_terms.context_quote."
    )
    notes: Optional[str] = None

    created_at: Optional[datetime] = None
    created_by_session: Optional[str] = None

    # --- Validators: SHAPE rules spanning several columns, mirroring the table's
    #     own table-level CHECKs one-for-one. Per-column vocabulary membership is
    #     deliberately NOT re-validated here — see the module docstring.

    @model_validator(mode="after")
    def no_self_reference(self) -> "ExtractionRelation":
        """An edge cannot compare a figure to itself."""
        if self.to_extraction_id is not None and self.to_extraction_id == self.from_extraction_id:
            raise ValueError(
                "to_extraction_id must not equal from_extraction_id: a figure "
                "cannot be its own comparator."
            )
        return self

    @model_validator(mode="after")
    def exactly_one_referent(self) -> "ExtractionRelation":
        """The referent is a row or a label, never both and never neither.

        Two representations of one fact (rule 5): if a row exists, point at it;
        if it does not, describe it in words. Carrying both would be a row AND a
        restated copy of what the row already says; carrying neither would leave
        the edge pointing at nothing.
        """
        has_row = self.to_extraction_id is not None
        has_label = self.to_label is not None
        if has_row == has_label:
            raise ValueError(
                "exactly one of to_extraction_id / to_label must be set — the "
                "referent is a row this project holds, or a label describing one "
                "it does not, never both and never neither."
            )
        return self

    @model_validator(mode="after")
    def row_required_for_condition_and_derivation(self) -> "ExtractionRelation":
        """You cannot be conditioned by, or computed from, a figure that does not
        exist as a row."""
        if self.relation in ("condition_on", "derived_from") and self.to_extraction_id is None:
            raise ValueError(
                f"relation={self.relation!r} requires to_extraction_id: a "
                f"condition or a derivation must name a figure this project "
                f"actually holds as a row, not only a label."
            )
        return self

    @model_validator(mode="after")
    def input_role_iff_derived_from(self) -> "ExtractionRelation":
        """input_role names which side of a derivation this edge is, so it is
        meaningless outside relation='derived_from' and mandatory inside it."""
        is_derivation = self.relation == "derived_from"
        has_role = self.input_role is not None
        if is_derivation != has_role:
            raise ValueError(
                "input_role must be set if and only if relation='derived_from' "
                f"(relation={self.relation!r}, input_role={self.input_role!r})."
            )
        return self

    @model_validator(mode="after")
    def unnamed_is_never_a_row(self) -> "ExtractionRelation":
        """An unnamed referent cannot simultaneously be one specific known row:
        if the source does not say what it is, this project cannot have
        resolved it to a row either."""
        if self.stated == "unnamed" and self.to_extraction_id is not None:
            raise ValueError(
                "stated='unnamed' cannot carry a row referent — an unnamed "
                "referent has, by definition, nothing to point at."
            )
        return self

    @model_validator(mode="after")
    def to_kind_unnamed_matches_stated(self) -> "ExtractionRelation":
        """Calling the referent's kind 'unnamed' is a claim about how the source
        stated it, so it must agree with `stated` rather than disagree with it."""
        if self.to_kind == "unnamed" and self.stated != "unnamed":
            raise ValueError(
                "to_kind='unnamed' requires stated='unnamed' — the two describe "
                "the same fact from two columns and must not disagree."
            )
        return self
