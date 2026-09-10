"""
schemas/base_parameter.py — the design parameter under determination, at base.

WHAT THIS IS. `base_parameters` is THE SUBJECT of a determination (owner ruling
2026-08-26, `references/project-standards.md`: "The judgment object is the
**canonical parameter**, and `items` is the render rollup the entity model already
calls it"). Migration 071 built it at base and re-keyed `specifications` onto it.

WHY IT IS AT BASE. Base holds the vocabularies and registries every other stage
points into. A parameter is one of those: research mines phrases, evidence records
them verbatim and unjudged (`db.py observe-term`, R11/D-0173), judgment adjudicates
a phrase onto a canonical parameter, and specification keys its determination on
that parameter. Nothing downstream may hold the parameter's NAME — the name lives
in `terms`, reached by `term_id`. That is rule 5, "point, do not copy".

WHY IT IS NOT `items`. The owner emptied the item layer on 2026-09-01 precisely
because a pre-authored container whose name states its answer — `E-08 Corridor
Clear Width (>=1200 mm Minimum on All Primary Routes)` — predisposes every finding
to file into it. A parameter is minted from an observed term through
`db.py add-term`, which refuses a value-bearing name for the same reason.

WHAT READS THIS MODEL. `scripts/audit/validate_pydantic_schemas.py` compares it
field-for-column against the live table; CLAUDE.md §4 makes the mirror part of the
schema-change protocol. It is not a writer — `scripts/db.py` is, through
`dbcore.WRITABLE_TABLES`.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator


class BaseParameter(BaseModel):
    """One canonical design parameter. Mirrors `base_parameters` (migration 071)."""

    model_config = ConfigDict(extra="forbid")

    parameter_id: Optional[int] = None  # INTEGER PRIMARY KEY; assigned by SQLite

    # The pointer, and the whole of rule 5's discipline in one column: UNIQUE, so a
    # second parameter for the same term is refused rather than becoming a dual home.
    term_id: str

    # Lifecycle. The vocabulary is NOT restated here: the column's own CHECK owns it
    # ('active' | 'merged' | 'retired'), and dbcore.check_values() reads that CHECK.
    # A list in Python would be a second home for a vocabulary — the same defect the
    # model exists to catch (CLAUDE.md §4).
    status: str = "active"
    merged_into: Optional[int] = None

    notes: Optional[str] = None

    created_at: Optional[str] = None
    created_by_session: Optional[str] = None
    updated_at: Optional[str] = None
    updated_by_session: Optional[str] = None

    @model_validator(mode="after")
    def merged_into_iff_merged(self) -> "BaseParameter":
        """Mirrors the table's structural CHECK.

        `merged_into` is meaningful only for a merged row and required for one.
        This is a relationship between two columns, not a vocabulary, so unlike
        `status` it belongs in the model as well as the schema.
        """
        if self.status == "merged" and self.merged_into is None:
            raise ValueError(
                "status 'merged' requires merged_into — a merge that names no "
                "survivor loses the parameter it merged."
            )
        if self.status != "merged" and self.merged_into is not None:
            raise ValueError(
                f"merged_into is set but status is {self.status!r}; only a merged "
                "row points at a survivor."
            )
        return self
