# DR-2026-08-27 — Relevance is an adjudication made at evidence collection, against a topic; applicability remains a synthesis judgement

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0174` · category `D-METH` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-08-27 13:52 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-08-27: "evidence states relevant items, and relevancy is something
that must be adjudicated against a topic/category/concept."

## Rationale

Relevance is not a property a document carries but a relation, so evidence collection judges --
it simply judges a different question from judgment. This refutes an agent finding that the
evidence stage was a "pure log" and that R1 (phase before-admitting) therefore conflicted with
it; there is no conflict. The distinction from applicability must be protected: DR-2026-08-24
§2.4 defers applicability and says nothing about relevance, and cannot, since relevance must be
settled at collection or nothing can be admitted. Conflating them breaks both ways. Measured
defect: source_slug_links.relevance_note exists and is populated in 0 of 10 rows, and
search_admissions records no grounds at all -- the adjudication is made every time and recorded
never. Under the harvest ruling (D-0173) the grounds become derivable rather than hand-written.

## Alternatives considered

- Treat evidence collection as a pure log with all judgement deferred -- refuted by the owner:
"relevant" is itself an adjudication.

## Notes, and what remains owed

Granularity gap measured: the owner names topic/category/concept, but slugs is flat -- no
parent, category, group or level column, 106 leaves. A source relevant at the category level can
only be copied across every leaf (rule 5) or lost. The owner has ruled parent columns are
needed.

## Delegation

Owner ruling. The pipeline shape, the project vocabulary and the research methodology are
judgements about the book, which governance/decision-protocol.md places in the DG-NON class and
CLAUDE.md rule 0 makes non-delegable.

## Artifacts

- `references/project-standards.md (entries dated 2026-08-27)`
