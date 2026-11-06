---
name: connection-discovery
description: >
  Find relationships between design parameters, populations and methods that no single
  extraction states, and log them as typed rows. Cross-parameter links (a wheelchair's swept path
  constrains turning space, corridor width and door approach), cross-population effects on one physical
  parameter, compound interactions, and methodology findings. Modes: parameter (a determination or its
  extractions), evidence (new extractions, gaps, pending connections), external (forward citations via
  Scholar Gateway / PubMed), cluster-crosstest (every pair of parameters in a named cluster). Use after
  citation mining, after a new or revised determination, or when a source bears on several parameters.
  Do NOT use to audit existing connections. Absorbs connection-scout (D-0146).
---

# Connection Discovery

**Model:** Opus-class or above (synthesis across dispersed evidence).
**Output:** `connections` + `connection_targets` via `python3 scripts/db.py add-connection`, and typed edges
between extractions via `relate-extraction` / `derive-extraction`.

**Keyed on the parameter, not on a container.** The subject of a determination is a `base_parameters` row
(owner 2026-08-26); the item layer is deleted (CLAUDE.md §7). Treat any `[A-Z]-NN` code you meet as prior-version
content, never as a target. A connection points at parameters, slugs, identity-lens codes
(`base_taxonomy_identity`), extractions, or a methodology, **one kind per column, each a real foreign key**
(migration 120); there is no free-text target.

## Two homes, and which holds what
- **A typed edge between two extractions** is the strongest link: `extraction_relations` (`condition_on`,
  `derived_from`, `delta_over`, `insufficient`, …) points from one figure to another row and can cross
  parameters. When one parameter's figure is computed from or conditioned on another's, file the edge
  (`derive-extraction`, `relate-extraction`); a `connections` row alone cannot be joined.
- **A `connections` row** is the narrative index of a relationship. Its targets are typed rows in
  `connection_targets` (`parameter_id`, `slug`, `identity_code`, `extraction_id`, `methodology`; exactly one set per
  row), so a renamed or merged parameter cannot orphan a link and every target joins.

## Modes
| Mode | Trigger | Reads |
|---|---|---|
| `parameter` (default) | a determination written or revised | the parameter's live `specifications` row and its extractions |
| `evidence` | new extractions, gap update | `source_value_extractions`, `gaps`, PENDING connections |
| `external` | citation mining finished for a slug | T1–T2 forward citations in `evidence_sources` |
| `cluster-crosstest` | a named cluster (parameters sharing a physical element, an envelope or a population) | every unordered pair in the cluster |

`cluster-crosstest` is the exhaustive pass (`decisions/DR-2026-07-20-intra-category-cross-test.md`, PROPOSED):
the other modes follow what an author thought to cross-reference, this one enumerates all pairs so none is skipped.
Per pair give one verdict: `INDEPENDENT`, `SUBSUMES`/`SUBSUMED_BY`, `INTERACTS`, `SHARED_ELEMENT_DISTINCT_PROGRAM`,
`CONFLATED_VARIABLE`, `GENUINE_CONFLICT`. Compare only within a measurement paradigm and device class
(`measurement_paradigm`, `device_class`); a cross-paradigm pairing is a derivation, never an identity, and never
`GENUINE_CONFLICT`. Flag **cross-partition leakage** where a shared element or population links parameters across a
cluster boundary. Only `GENUINE_CONFLICT` goes to `cross-population-conflict-mapper`; the others are typed
`connections` rows; log unexamined pairs as gaps.

## Step 0 — Scope and dedup
`scope_type: parameter | slug | cluster`, `scope_id`, `mode`. Load existing connections for the scope
(`python3 scripts/db.py connections --status PENDING`, then join `connection_targets` on `parameter_id` or `slug` in
a read-only query). A new connection with the same targets and `connection_type` as an existing one is a duplicate:
skip it.

## Step 1 — Read, by mode
Read the live determination and every extraction for the parameter in full; for `evidence`, also open gaps
(`db.py gaps --status OPEN`) and PENDING connections. For each extraction note its lens columns, so a population effect
on a shared parameter is visible. For `external`, take T1–T2 sources from `evidence_sources`, follow forward citations,
log mining with `db.py log-mining`; a cross-slug citation is a cross-parameter candidate.

## Step 2 — Identify connections
For each finding ask: does it imply a design relationship between two parameters, populations or methodological
principles not already recorded?

| Type (stored value) | Test |
|---|---|
| `CROSS-PARAMETER` | does evidence for parameter X constrain parameter Y? |
| `CROSS-POPULATION` | does a finding for population A conflict with or reinforce one for B on the same parameter? |
| `COMPOUND-INTERACTION` | would applying specifications X and Y to one person together give a non-additive result? |
| `METHODOLOGY` | does it affect the guidebook's method? |

Confidence: `HIGH` direct evidence links the targets and the source says so; `MODERATE` implied by reasoning or an
evidence gap; `SPECULATIVE` plausible, no direct evidence.

Route first: a relationship at MODERATE or above is a connection; a SPECULATIVE one is a gap
(`add-gap --category CR --priority P3 --description "SPECULATIVE: …" --skill connection-discovery`, never a
connection); an evidence or scope gap is a gap (`RP`, `AUDT` or `CONF`); a population conflict goes to
`cross-population-conflict-mapper`; anything else is discarded. `CONN` is not a gap category.

## Step 3 — Log
```bash
python3 scripts/db.py next-id connections      # never increment by hand
GUIDEBOOK_DB_PATH="$SCRATCH/guidebook.db" python3 scripts/db.py add-connection \
  --con-id CON-XXXX --confidence HIGH --connection-type CROSS-PARAMETER \
  --filed-in <slug> --source-skill connection-discovery \
  --description "<one sentence: the relationship, its mechanism, why it matters to a determination>" \
  --parameter 3 --parameter 12 --session <session>
```
`--filed-in` is a topic slug (`slugs.slug`, a foreign key). Targets are flags, each repeatable and each validated
against its table: `--parameter`, `--target-slug`, `--identity`, `--extraction`, `--methodology`; at least one is
required. Description bar: usable by the determination run without further lookup.
Bad: "turning space and chair length are related". Good: "REF-xxxxx Table 2 gives a 1.35 m swept path for a
powered chair; that exceeds the 1.2 m the turning-space figure assumes, so the turning figure needs its own row for
that chair class."

## Step 4 — Verify and hand on
`db.py connections --status PENDING --summary` should have grown by the number logged. Consumption: when a
determination uses a connection, `db.py update-connection --con-id CON-XXXX --status CONSUMED --session …`. A
connection that reveals a conflict goes to `cross-population-conflict-mapper`; do not log the conflict here.
`connections.opus_reviewed` exists and no verb sets it; do not claim a review that no row records.

## Rules
1. `next-id connections` for every CON-ID.
2. HIGH confidence connections feed the determination run (`scripts/assess/assess_cell.py` stage).
3. SPECULATIVE is a CR gap, never a connection.
4. No `[A-Z]-NN` target, no `--item-code`, no prefixed free-text target: use the typed flags.
5. Use the CLI only; the archived registers (`gap_register.md`, `connection-register-active.md`, per-topic
   `connections.md`) are not read or written.
6. Feeds `cross-population-conflict-mapper`.
