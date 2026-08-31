# DR-2026-08-27 — base_sources is a registry of research TARGETS -- prompts for where to look. It is neither evidence nor research

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0172` · category `D-SCHEMA` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-08-27 13:52 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-08-27, correcting an agent finding that had called it a duplication
defect.

## Rationale

The owner: "academic publishing institutions, research journals, university publications, books
and articles, etc are all sources for finding evidence sources. so too are countries, codes and
standards, professional organizations, clinical bodies, and advocacy groups. none of these are
evidence, and none of these are research. they are all prompts for research to target such that
they can find evidence." Both bullets of the architecture note are one coherent member and
neither is the corpus; the agent error came from reading "sources" as this project's
evidence_sources. It is a third input to the research matrix alongside the clue store. Measured:
no target registry exists, and the nearest thing is search_executions.engine -- free text, no
vocabulary, no table, no CHECK -- so target coverage is not a derivable fact and a body nobody
thought to search is invisible to every gate.

## Alternatives considered

- Treat the two bullets as a source-type taxonomy plus the academic corpus -- refuted by the
owner; neither is the corpus.

## Notes, and what remains owed

Nomenclature hazard flagged at ratification: "sources" would then do two jobs -- base_sources is
where to look, evidence_sources is what we found. That is the class the owner retired `items`
for. Resolve the name before the table exists.

## Delegation

Owner ruling. The pipeline shape, the project vocabulary and the research methodology are
judgements about the book, which governance/decision-protocol.md places in the DG-NON class and
CLAUDE.md rule 0 makes non-delegable.

## Artifacts

- `references/project-standards.md (entries dated 2026-08-27)`
- `references/owner-notes/2026-08-27-architecture-note.md`
