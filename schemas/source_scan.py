"""
schemas/source_scan.py — one READING of one source against the parameter list.

Mirrors `source_scans` (migration 103, tooling T1, owner approval D8 2026-10-09;
catalogue-plan-v2 section 3.8). A reading records which source was read, which saved
file (by sha256), how much of its text, against which catalogue version, and whether
the open pass for quantities the catalogue lacks was done. `v_scan_ledger` derives,
from these rows and the extractions, a status for every (source, active parameter)
pair: EXTRACTED / STATED-ABSENT / READ-NOTHING-FOUND / READ-PARTIAL / NOT-READ.

COMPUTED, NOT TYPED (CLAUDE.md rule 8). `catalogue_version` is the highest
parameter_id when the reading was recorded; `pages_read`/`pages_total` come from the
page markers of the file read. `db.py record-scan` computes all three and refuses a
typed catalogue version, so this model carries them as plain fields to be filled, not
values an author chooses.

VOCABULARIES ARE PLAIN str, NOT Enums: `mode`, `text_scope` and `method` are owned by
the table's own CHECKs and read by `dbcore.check_values()`; an Enum here would be a
second home free to drift (the reasoning recorded in schemas/extraction_relation.py).
The cross-column shape rules ARE mirrored, because no single CHECK-per-column reading
can express them.

WHAT READS THIS MODEL: scripts/audit/validate_pydantic_schemas.py, which compares its
fields with the live table. The writer is `db.py record-scan`; the table is captured
through `dbcore.writable_tables()`.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator


class SourceScan(BaseModel):
    """One reading of one admitted source. Mirrors `source_scans` (migration 103)."""

    model_config = ConfigDict(extra="forbid")

    scan_id: Optional[int] = None          # AUTOINCREMENT; never reissued
    ref_id: str
    mode: str                              # CHECK: catalogue | targeted
    catalogue_version: int                 # computed by the writer, never typed
    target_parameter_id: Optional[int] = None
    text_scope: str                        # CHECK: full | partial | fragment | abstract
    pages_read: Optional[int] = None       # computed from the file's page markers
    pages_total: Optional[int] = None
    file_sha256: str
    open_pass_done: int = 0
    method: str                            # CHECK: full-read | pre-screen
    notes: Optional[str] = None

    created_at: Optional[str] = None
    created_by_session: Optional[str] = None
    updated_at: Optional[str] = None
    updated_by_session: Optional[str] = None

    @model_validator(mode="after")
    def shape(self) -> "SourceScan":
        """Mirrors the table's three cross-column CHECKs."""
        if (self.mode == "targeted") != (self.target_parameter_id is not None):
            raise ValueError("a targeted reading names exactly one parameter; a "
                             "catalogue reading names none")
        if (self.pages_read is not None and self.pages_total is not None
                and self.pages_read > self.pages_total):
            raise ValueError("pages_read exceeds pages_total")
        if (self.text_scope == "full" and self.pages_read is not None
                and self.pages_read != self.pages_total):
            raise ValueError("a full reading of a paged text covers every page; "
                             "fewer pages is a partial reading")
        if len(self.file_sha256) != 64:
            raise ValueError("file_sha256 is the manifest's full sha256 (64 hex chars)")
        return self
