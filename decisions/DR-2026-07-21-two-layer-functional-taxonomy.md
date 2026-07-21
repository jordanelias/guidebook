# DR-2026-07-21 — Two-layer functional taxonomy: axes × profiles

- Status: **PROPOSED — pending owner ratification.** States and does not execute
  (posture per `DR-2026-07-21-product-posture-thinking-tool-not-authority.md`). No
  database row, item link, or skill file changes with this commit; the full doctrine
  and disposition tables live in `governance/functional-taxonomy.md`; ready-to-apply
  schema is staged at `working/taxonomy/staged_schema_functional_axes.sql` (outside the
  migration glob).
- Date: 2026-07-21
- Prepared by: Claude, from the owner-directed taxonomy interrogation of 2026-07-21
  (session on branch `claude/search-slugs-accessible-design-i9yxza`).
- Affects (if ratified): `populations` layer semantics; slug creation workflow
  (`serves_axes`); `functional-deficit-auditor_SKILL.md` §1–2 (regenerated from axis
  register); `evidence_population_match` population field; `db.py validate`.
- Related: `governance/conceptual-model.md` (entity model; note
  `DR-2026-07-21-entity-code-namespace-rename` — new tables here take no `E-##`/`ENT-##`
  codes until assigned under the post-rename namespace);
  `DR-2026-07-20-weighted-strength-anchor-model` (strength bands reused unchanged);
  `governance/co1-operational.md` (non-subordination reaffirmed at profile layer);
  GAP-277 (IntD existence question — answered by `AX-COG-L` if ratified).

## Context — why taxonomy is the curation gate

The population taxonomy decides what evidence is findable (an entity must name the
thing searched for) and where evidence attaches (an entity must exist to hold it). The
2026-07-21 audit found the current 22-population table fuses three ontologies —
functional axes, diagnoses, anthropometric archetypes — producing verified failures:
zero ICF `b`-codes corpus-wide; balance/vestibular function (`b235/b240/d415`)
unrepresented by any entity, slug, or search; PCS defined as two different conditions
in DB vs FDA skill; MS and MCAS parented etiologically rather than functionally; SENS
starved at 1 item link because it is an axis mislabeled as a population; the FDA skill
auditing against codes absent from the canonical table.

## Decision (proposed)

Adopt a two-layer taxonomy:

1. **Layer 1 — 17 functional axes** (`AX-*`), ICF `b`+`d` anchored,
   architect-actionable, canonical attachment for mechanism/threshold evidence and for
   item linkage. Six are new: five visible holes — `AX-BAL` balance/postural
   stability, `AX-COG-L` learning & information access, `AX-COM-E` expressive
   communication, `AX-ARO` arousal/stress regulation, `AX-CNT` continence & urgency —
   plus `AX-CHM` chemical/air-quality tolerance, which names the axis the existing
   air-quality slug already feeds.
2. **Layer 2 — profiles** (diagnostic, identity-cultural, demographic, anthropometric,
   compound, umbrella): weighted mappings onto axes **plus authored emergent content
   that is never reduced to axes** (the emergence guarantee; Co-1 non-subordination
   restated). Every existing population code is dispositioned (alias / profile /
   qualifier) per `governance/functional-taxonomy.md` §4 — including the PCS→
   `PCS-TBI`+`LCOV` split, MS/MCAS re-parenting, the VIS low-vision/non-visual split,
   DEAF's dual axis+cultural-profile disposition, and admission of CHD/LPA/EXH/BAR,
   `OLD` (older adults), and `VES` (vestibular disorders) as profiles.
3. **Curation rules** (§5): the selection principle (in-scope iff it bears on an axis,
   a profile, or an item), attachment rules per evidence kind, `serves_axes` slug
   discipline, and two standing zero-coverage gap queries.

## Alternatives considered and rejected

- **Status quo** — leaves the six axes invisible to search and curation; the audit
  showed absence of entity ⇒ absence of evidence, regardless of search effort.
- **ICD-organized taxonomy** — maximal interoperability, but formally encodes
  disability=disease against the corpus's own social-model lean, and cannot host
  identity-cultural profiles (Deaf, NDV) at all. ICD-11 is retained only as an optional
  per-profile anchor.
- **Flat function-only model (no profiles)** — cleanly §1.3-compliant but destroys
  non-decomposable corpora (DeafSpace, dementia design, ASPECTSS, age-friendly) and
  demotes Co-1 evidence to axis fragments; rejected on the emergence guarantee.
- **Full ICF including `e`-codes as item anchors** — retracted in-session: `e150/e155`
  granularity is far below item grain; ceremonial alignment only.

## Consequences if ratified

What information gets curated: evidence for six functional domains that currently
cannot be curated at all acquires attachment points; intellectual disability stops
being proxied (GAP-277); MH gets its actual axis (`b152/d240` un-scoped for the
architecturally actionable subset). How it is curated: mechanism evidence lands on
axes and becomes reachable from every profile sharing the axis (MS thermal evidence
serves SCI/POTS/OLD); profile and Co-1 evidence stays profile-anchored and
non-subordinated; slugs declare what they serve; coverage holes become queries instead
of unknowns.

Costs: one schema migration + seeds (staged, ~250 lines); FDA skill regeneration;
79-slug `serves_axes` backfill; item-link harvest from 87 existing FDA briefs (no new
research required for seeding). New research (3 proposed slug stubs) **queues behind
the language/jurisdiction debt** per the anti-displacement discipline — this DR adds
no search-execution obligations.

## Explicitly not decided here

Public-realm scope (needs its own scope DR) · any conflict-precedence rule (parity
display stands) · new search execution or reordering of the research queue · Part 2
prose restructure (Phase E rendering concern) · theoretical-genealogy note (separate,
smaller artifact if wanted).

## Ratification checklist (owner)

1. Ratify the 17-axis register (or amend membership) — §2.1.
2. Ratify the disposition table, esp. the three judgment calls flagged: DEAF dual
   disposition; EPI→`AX-SPR` situational; DBL de-privileged-to-compound-profile — §4.
3. Confirm PCS split into `PCS-TBI` + `LCOV` — §4.
4. Confirm admission of `OLD`, `VES`, and the four archetypes as profiles — §4.
5. Confirm the queue rule (taxonomy work does not displace language-debt execution) — §8.
6. On ratification: promote the staged SQL into `scripts/migrations/` and execute §9
   steps 1–7.
