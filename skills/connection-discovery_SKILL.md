---
name: connection-discovery
description: >
  Find relationships between design parameters, populations and methods that no single
  extraction states, and log them as typed rows. Cross-parameter links (a wheelchair's swept path
  constrains turning space, corridor width and door approach), cross-population effects on one physical
  parameter, compound interactions, and methodology findings. Modes: parameter (a determination or its
  extractions), evidence (new extractions, gaps, pending connections), external (forward citations via
  Scholar Gateway / PubMed), category-crosstest (every pair of parameters in a named cluster). Use after
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
(`base_taxonomy_identity`), extractions, or a methodology, **one kind per column** (migration 120). Four of
the five are foreign keys; `--methodology` names a methodological principle and is the one target kind with
no table, so it is free text. The connection id is computed by the writer, never typed.

## Two homes, and which holds what
- **A typed edge between two extractions** is the strongest link: `extraction_relations` (`condition_on`,
  `derived_from`, `delta_over`, `insufficient`, …) points from one figure to another row and can cross
  parameters; across two *sources* it needs `--cross-source <reason>` or the writer refuses. When one parameter's figure is computed from or conditioned on another's, file the edge
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
| `category-crosstest` | a named cluster (parameters sharing a physical element, an envelope or a population; what a letter-category was) | every unordered pair in the cluster |

`category-crosstest` is the exhaustive pass (`decisions/DR-2026-07-20-intra-category-cross-test.md`, ACCEPTED
2026-07-21; "category" is now a named cluster of parameters): the other modes follow what an author thought to
cross-reference, this one enumerates all pairs so none is skipped. A cluster has no table: name it in the GAP
and in each connection's description. Per pair (per program) give one verdict, in words, because no column
holds a verdict: the two are independent; one subsumes the other; they interact; they share a physical element
under distinct programs; they are one variable conflated under two names; or they are in genuine conflict.
Compare only within a measurement paradigm and device class (`measurement_paradigm`, `device_class`); a
cross-paradigm pairing is a derivation, never an identity, and never a genuine conflict. Flag
**cross-partition leakage** where a shared element or population links parameters across a cluster boundary.
**Not built, and said so:** the DR's pair table (X6) and its hard gate on `stated` (X5). Until they exist a
verdict has no typed home: "interact" and "shared element, distinct programs" are `connections` rows, a genuine
conflict goes to `cross-population-conflict-mapper`, and the verdicts with no row (independent, subsumes,
conflated) are named in a GAP for the cluster so the pass is not lost.

---

## Step 0 — Scope and dedup
State the scope (a parameter, a slug or a cluster), what identifies it, and the mode. Load existing connections
for the scope (`python3 scripts/db.py connections --status PENDING`, then join `connection_targets` on
`parameter_id` or `slug` in a read-only query). A new connection with the same targets and `connection_type` as
an existing one is a duplicate: `add-connection` refuses it, naming the existing id.

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

Confidence is `connections.confidence`, read from the column's own CHECK (`HIGH`: direct evidence links the
targets and the source says so; `MODERATE`: implied by reasoning or an evidence gap). A plausible relationship
with no direct evidence is not a connection and the CHECK admits no value for it (migration 122): file it as a
gap (`add-gap --category CR --priority P3 --description "speculative: …" --skill connection-discovery`).

Route first: a relationship at MODERATE or above is a connection; an evidence or scope gap is a gap (`RP`,
`AUDT` or `CONF`); a population conflict goes to `cross-population-conflict-mapper`; anything else is discarded.
There is no connection-shaped gap category.

## Step 3 — Log
```bash
GUIDEBOOK_DB_PATH="$SCRATCH/guidebook.db" python3 scripts/db.py add-connection \
  --confidence HIGH --connection-type CROSS-PARAMETER \
  --filed-in <slug> --source-skill connection-discovery \
  --description "<one sentence: the relationship, its mechanism, why it matters to a determination>" \
  --parameter 3 --parameter 12 --session <session>
```
The id is computed by the writer (omit `--con-id`; a typed one must equal `next-id connections`). `--filed-in`
is a topic slug (`slugs.slug`, a foreign key). Targets are flags, each repeatable and each validated against
its table: `--parameter`, `--target-slug`, `--identity`, `--extraction`, `--methodology`. The type sets the
arity the writer holds: `CROSS-PARAMETER` and `COMPOUND-INTERACTION` need two or more `--parameter` targets,
`CROSS-POPULATION` two or more `--identity` targets, `METHODOLOGY` one `--methodology`; a type the CHECK
admits for which the writer holds no arity rule is refused by name, never filed unchecked; a parameter target
must be `active` (a merged or retired one is refused). Description bar: usable by the determination run
without further lookup.
Bad: "turning space and chair length are related". Good: "REF-xxxxx Table 2 gives a 1.35 m swept path for a
powered chair; that exceeds the 1.2 m the turning-space figure assumes, so the turning figure needs its own row for
that chair class."

## Step 4 — Verify and hand on
Count before and after: `python3 scripts/db.py connections --status PENDING` lists the rows (`--summary`
groups them by confidence only), and the list should have grown by the number logged. Consumption: when a
determination uses a connection, `db.py update-connection --con-id CON-NNNN --status CONSUMED --session …`
(`--status` is `connections.status`, from the CHECK). A connection that reveals a conflict goes to
`cross-population-conflict-mapper`; do not log the conflict here. `connections.opus_reviewed` exists and no
verb sets it; do not claim a review that no row records.

## Rules
1. Never type a connection id: the writer computes it.
2. HIGH confidence connections feed the determination run (`scripts/assess/assess_cell.py` stage).
3. A relationship with no direct evidence is a CR gap, never a connection.
4. No `[A-Z]-NN` target and no prefixed free-text target: use the typed flags.
5. Use the CLI only; the archived registers (`gap_register.md`, `connection-register-active.md`, per-topic
   `connections.md`) are not read or written.
6. Feeds `cross-population-conflict-mapper`.
