"""
schemas/source_value_extraction.py — the JUDGMENT item.

Mirrors the `source_value_extractions` SQLite table as migration 073 re-keyed it.

WHICH STAGE THIS IS, because the file said the wrong one for four months. D-0168
(2026-08-27, RATIFIED ON CONTACT): *"The evidence item is the SOURCE; the judgment
item is the extracted, tiered, categorised value. Evidence to judgment is 1:N."*
So this table is at JUDGMENT, not evidence collection. The owner's worked example
is the one to hold in mind: one code document (Canada's NBC 3.8) yields MANY rows
here, one per clause. The old docstring drew this model as a link in an
"evidence-curation chain" between `source_slug_links` and `reasoning_doc_citations`
and ended at `items.pmp_*`; that chain's last two links are prior-version content
(the owner emptied the item layer 2026-09-01) and its stage assignment is the one
D-0168 overturned.

    evidence_sources (the evidence item — one row per source)
       ↓  1:N   — ruled, and pinned by scripts/audit/judgment_handoff_shape.py
    source_value_extractions (the judgment item — one row per extracted value) ← this model
       ↓
    specifications (the determination — keyed on the SAME parameter_id and the
                    SAME four lenses, so the hand-off needs no translation)

CELL IDENTITY — THE SAME TWO HALVES `specifications` CARRIES, AND FOR THE SAME REASONS.

The SUBJECT is `parameter_id` into `base_parameters` (owner 2026-08-26; built by
migration 071, made mandatory here). It is the pointer rule 5 requires: the
parameter's NAME lives in `terms.canonical_en`, reached through
`base_parameters.term_id`, and is never copied onto an extraction row.

The LENS is the four browsing taxonomies (owner 2026-08-28, CHECK relaxed by
D-0182 to "at least one"): identity / ICF / access-need / medical. That ruling names
this table in its own evidence and its ACTION says `population_code` is retired in
favour of the four.

THREE COLUMNS THIS MODEL NO LONGER DECLARES, and none of them is an omission:
`parameter` and `parameter_canonical` (retired by 073 — the verbatim source phrase
lives in `observed_terms.surface_form`, which is where R11/D-0173 put it, with a live
writer and 33 live rows), and `population_code` / `population_label` / `item_code`
(retired by 073 under the 2026-08-28 and 2026-08-26 rulings respectively).

SCOPE — THIS IS NOW A COMPLETE MIRROR, which it deliberately was not before.
It declared 22 of the table's columns and carried a paragraph explaining that the
value-genealogy layer (root_id, root_type, root_ref_id, root_population_note,
root_classification_basis, echo_of, measurement_paradigm, device_class, contested,
file_anchor, setting) was "real work with its own review surface, tracked as F5".
CLAUDE.md §7 calls that drift a bug, not a convention, and
`scripts/audit/validate_pydantic_schemas.py` reported all eleven as DB-only every
run. They are declared below. Field count is checked against the live table by that
audit; do not state it here (CLAUDE.md rule 7).

VOCABULARIES, AND A DELIBERATE ASYMMETRY WORTH NAMING SO IT READS AS A DECISION.
`root_type`, `measurement_paradigm` and `device_class` are declared `Optional[str]`
and NOT as Python enums, even though each has a closed CHECK. CLAUDE.md §4:
"Vocabularies come from the schema, not a list in code" — `dbcore.check_values()`
reads the column's own CHECK and that is what `db.py add-extraction` refuses on, so a
Python copy would be a second home that drifts the first time a migration changes the
list. The three enums that ARE here (ClaimType, ExtractionMethod, ExtractionStatus)
predate that rule; `ClaimType` is load-bearing for `_value_consistency` below, which
mirrors the table's own claim/value CHECK. Retiring the other two is a separate change
with its own sweep, not a side effect of this one.

Lens CODES are likewise not validated here — a code's vocabulary is its own base
registry, reached by a real typed FK (populations / axes / access_needs /
base_taxonomy_medical). `at_least_one_lens` below validates the SHAPE, which the
database also states, and nothing else.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class ClaimType(str, Enum):
    NUMERICAL = "numerical"
    RANGE = "range"
    QUALITATIVE = "qualitative"
    FRAMEWORK = "framework"
    ABSENT = "absent"  # source linked to topic/parameter but asserts no value


class ExtractionMethod(str, Enum):
    SKIM = "skim"
    FULL_READ = "full-read"
    RE_READ = "re-read"
    AUTO_MINED = "auto-mined"


class ExtractionStatus(str, Enum):
    PRELIMINARY = "preliminary"
    REVIEWED = "reviewed"
    VERIFIED = "verified"
    CONTRADICTED = "contradicted"
    ABSENT_CONFIRMED = "absent-confirmed"


class SourceValueExtraction(BaseModel):
    """One judgment item: what ONE source asserts, for ONE parameter, under ONE
    or more lenses, at ONE place in the document.

    Many of these may point at the same `ref_id`, and many may point at the same
    (`ref_id`, `parameter_id`) pair. Both fan-outs are ruled, not tolerated —
    D-0168's clause-level example, and the DR-2026-08-19 §7 dissent contest where
    a divergent adversarial grade lands as a second row and the divergence reads
    as a contest rather than overwriting the first grade.
    """

    extraction_id: Optional[int] = None  # autoincrement PK

    # ── The hand-off key (D-0168) ────────────────────────────────────────────
    ref_id: str = Field(..., description="FK evidence_sources.ref_id — the EVIDENCE item")
    slug: str = Field(
        ...,
        description="the slug this extraction was mined under. Not a copy of "
                    "source_slug_links: that junction says the source is admitted to "
                    "the slug, this says the reading happened there, and "
                    "evidence_sources has no slug column to point at.",
    )

    # ── The subject (owner 2026-08-26; mandatory since migration 073) ────────
    parameter_id: int = Field(
        ...,
        description="FK base_parameters.parameter_id — THE SUBJECT. Mandatory: an "
                    "extraction whose parameter is unknown cannot reach the "
                    "determination it exists to support, and `db.py add-extraction` "
                    "mints the row and its subject together.",
    )

    # ── The four lenses (owner 2026-08-28; CHECK relaxed by D-0182) ──────────
    # Each is a code in its own base registry, reached by a real typed FK. The codes
    # are NOT validated here — the registry is the vocabulary (CLAUDE.md §4).
    identity_code: Optional[str] = None   # populations.population_code
    icf_code: Optional[str] = None        # axes.axis_code
    needs_code: Optional[str] = None      # access_needs.need_code
    medical_code: Optional[str] = None    # base_taxonomy_medical.medical_code

    jurisdiction: Optional[str] = None  # "UK","US","Multi", or None for clinical
    setting: Optional[str] = None

    # ── The asserted claim ───────────────────────────────────────────────────
    claim_type: ClaimType
    claimed_value: Optional[str] = None
    claimed_unit: Optional[str] = None
    claim_text: Optional[str] = None  # exact source phrasing — clause-level verbatim
    source_section: Optional[str] = None  # "Table 6, p.33"

    # ── Value genealogy / independence substrate (DR-2026-07-13 H1) ──────────
    # v_value_independence counts DISTINCT COALESCE(root_ref_id, root_id) over the
    # measurement/participatory/derived root types. Vocabularies live in the columns'
    # own CHECKs; see the module docstring for why they are not enums here.
    root_id: Optional[str] = None
    root_type: Optional[str] = None
    root_ref_id: Optional[str] = None  # FK evidence_sources.ref_id — the root SOURCE
    echo_of: Optional[str] = None
    measurement_paradigm: Optional[str] = None
    device_class: Optional[str] = None
    root_population_note: Optional[str] = None
    root_classification_basis: Optional[str] = None
    contested: int = 0  # 0/1; SQLite has no boolean and the column is INTEGER
    file_anchor: Optional[str] = None

    # ── Pinpoint locator (schema 053) ────────────────────────────────────────
    # A code or standard is cited at a hierarchical position inside it. These mirror
    # the DB columns 1:1; most are NULL on most rows, because a level a document does
    # not have is not missing data. `locator_scheme` records which family's naming
    # applies (ISO's top numbered level is a CLAUSE, ADA's is a SECTION), so a reader
    # knows whether to render '§404.2' or 'clause 12.3'. The `_end` companions carry
    # spans -- 'ADA 2010 §604-608' is live data. Under D-0168 these are also what
    # makes the 1:N fan-out legible: NBC 3.8's clauses are many rows, and these tell
    # them apart.
    locator_scheme: Optional[str] = None
    loc_division: Optional[str] = None
    loc_part: Optional[str] = None
    loc_section: Optional[str] = None
    loc_subsection: Optional[str] = None
    loc_paragraph: Optional[str] = None
    loc_clause: Optional[str] = None
    loc_subclause: Optional[str] = None
    loc_division_end: Optional[str] = None
    loc_part_end: Optional[str] = None
    loc_section_end: Optional[str] = None
    loc_subsection_end: Optional[str] = None
    loc_paragraph_end: Optional[str] = None
    loc_clause_end: Optional[str] = None
    loc_subclause_end: Optional[str] = None
    loc_note: Optional[str] = None

    # ── Provenance of the extraction itself ──────────────────────────────────
    extraction_method: ExtractionMethod
    extraction_status: ExtractionStatus = ExtractionStatus.PRELIMINARY

    # Bridge to synthesis layer
    promoted_to_rdc_id: Optional[str] = None  # FK reasoning_doc_citations.citation_id

    notes: Optional[str] = None

    # Audit
    created_at: Optional[datetime] = None
    created_by_session: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by_session: Optional[str] = None

    # --- Validators ---

    @model_validator(mode="after")
    def _value_consistency(self):
        # Mirror the SQL CHECK: claim_type='absent' ↔ claimed_value IS NULL
        if self.claim_type == ClaimType.ABSENT and self.claimed_value is not None:
            raise ValueError("claim_type='absent' requires claimed_value to be None")
        if self.claim_type != ClaimType.ABSENT and self.claimed_value is None:
            raise ValueError(
                f"claim_type='{self.claim_type.value}' requires claimed_value to be set"
            )
        return self

    @model_validator(mode="after")
    def at_least_one_lens(self) -> "SourceValueExtraction":
        """D-0182, mechanised: absence in a lens is fine, absence in ALL is not.

        This is the Python side of the live table's
        `CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code)
        IS NOT NULL)`, and is word-for-word the same guard `schemas/evidence_state.py`
        puts on the determination. It was "exactly one" under the 2026-08-28 ruling and
        D-0182 relaxed it; stating a value in several lenses at once is the ideal, not a
        violation.

        The determination and the extraction it rests on carry the SAME shape on
        purpose: a judgment row that could not name a lens would hand the determination
        a value about nobody.
        """
        if (
            self.identity_code is None
            and self.icf_code is None
            and self.needs_code is None
            and self.medical_code is None
        ):
            raise ValueError(
                "An extraction must be stated in at least one lens: set one or more of "
                "identity_code / icf_code / needs_code / medical_code (D-0182). A value "
                "attached to no lens is a value about nobody."
            )
        return self
