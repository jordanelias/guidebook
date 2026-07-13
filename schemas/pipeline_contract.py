"""
schemas/pipeline_contract.py — Pydantic model for governance/pipeline-contract.yaml.

Validates the machine-checkable stage contract (the PROPOSED pipeline handshake
spec, DR-2026-07-13-pipeline-contract). Plain pydantic v2 BaseModel with
extra='forbid', matching the repo's config-schema style. No DB coupling.
"""
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict


class Criterion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    kind: Literal["integrity", "completeness"]
    criterion: str
    references: str
    check: Optional[str] = None   # repo-relative enforcer path, or None = declared-but-unenforced


class Stage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    anchor: str
    entry: List[str]
    criteria: List[Criterion]


class CrossStageGate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    criterion: str
    references: str
    check: Optional[str] = None


class PipelineContract(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: int
    status: str
    ratified: bool
    authored_by: str
    dr: str
    enforcement_level: int
    spine: str
    stages: List[Stage]
    cross_stage: List[CrossStageGate]

    def all_checks(self):
        """Yield (location, criterion_id, check_path_or_None) across the whole contract."""
        for st in self.stages:
            for c in st.criteria:
                yield (f"stage:{st.id}", c.id, c.check)
        for g in self.cross_stage:
            yield ("cross_stage", g.id, g.check)

    @classmethod
    def load(cls, path):
        import yaml
        from pathlib import Path
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        return cls.model_validate(data)
