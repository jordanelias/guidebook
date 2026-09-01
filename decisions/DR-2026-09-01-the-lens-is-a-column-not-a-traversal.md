# DR-2026-09-01-the-lens-is-a-column-not-a-traversal — The lens is a COLUMN, not a traversal: one item×taxonomy link table with four nullable lens pointers. item_axis_links is folded in; base_taxonomy_medical is created.

**Status:** **ADOPTED, REVIEW PENDING** — a `DG-REVIEW` decision taken by a session under
`CLAUDE.md` §1, which places code and tables outside the owner gate. It is landed and live; the
review it awaits is the owner's, and `review_status` in the register is `PENDING` until then.

**Register row:** `D-0184` · category `D-SCHEMA` · delegation `DG-REVIEW` ·
decided by `session_2026-09-01-lens-architecture` on 2026-09-01 19:20 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED and landed as migration 065. item_population_links (372) and item_axis_links (158)
become item_taxonomy_links (530), carrying identity_code, icf_code, needs_code and medical_code.
base_taxonomy_medical is created empty.

## Rationale

Executes D-0170's four lenses and D-0182's cardinality against the owner's stated goal of a
dynamically rendering site with a multimodal lens and filters. The alternative -- store a fact
in one lens and cross to the others at render through population_axis_map / access_need_axis_map
-- was measured on 2026-09-01 and fails twice. (1) THE CROSSINGS ARE INCOMPLETE: identity→ICF 20
of 23, ICF→identity 16 of 17, needs→ICF 15 of 17, ICF→needs 15 of 17, and identity↔needs has no
direct map at all; every gap is a silently empty page rather than a "no results" page. (2)
TRAVERSAL MANUFACTURES INFERENCE AND CHANGES THE ANSWER: the identity lens asked for DEAF
returns 20 items, while the ICF lens asked for AX-AUD -- the axis DEAF crosses to -- returns 38
rows, because DEAFBLIND crosses to AX-AUD too. Only the first is a recorded fact. D-0174
reserves applicability to synthesis, so a render layer that crosses is adjudicating where
nothing reviews it and no attestation covers it. With the lens as a column the render is WHERE
<lens>_code = ?, one query shape for four lenses, and no UNION anywhere -- a UNION is only
forced when the taxonomies live in separate link tables, which is the state this ends.

## Alternatives considered

- Keep item_axis_links and add lens columns only to item_population_links -- rejected: the ICF
  lens keeps two homes (rule 5) and every lens-neutral render query needs a UNION over two
  shapes.
- Change only rationale_ref's type now and reshape later -- rejected: it rebuilds the same table
  twice and sweeps its callers twice, which is the failure CLAUDE.md §0.4 describes.
- Merge strength_band into applicability -- rejected: they are different qualifiers and merging
  them is a doctrinal judgement, not a schema migration. Both columns survive.

## Notes, and what remains owed

TWO THINGS GIVEN UP, STATED RATHER THAN BURIED. (1) UNIQUENESS IS WEAKER. The old primary keys
were (item_code, population_code, subtype) and (item_code, axis_code); the wide form must permit
A-18×DEAF×AX-AUD beside A-18×DEAF×AX-SPR, which are two mechanisms and not a duplicate.
idx_itl_row_identity keeps every full lens tuple unique, but an identity-only row is no longer
structurally prevented from sitting beside a wide row already carrying that identity. That
residual dual-home risk is an audit's job, not a constraint's, and the audit is OWED. (2)
APPLICABILITY IS NULLABLE NOW. It was NOT NULL DEFAULT 'applies'; the 158 folded axis rows never
carried it, and defaulting them would assert a judgement nobody made -- exactly the inference
D-0174 reserves to synthesis. NULL means not adjudicated. ALSO OWED: the graph extractor draws
only the identity lens, because `axes` is absent from its PRIMARY node registry and emitting the
ICF edge would fire ref.dangling_structural on all 158 rows; registering `axes` is the one-line
fix and it changes audit output, so it was not smuggled into a rename sweep. Coverage is
unchanged either way -- item_axis_links was never extracted. base_taxonomy_medical is created
EMPTY and no row can reference it until it is populated, which is content (DG-NON) and the
owner's alone; it is created now because SQLite cannot add a table-level CHECK by ALTER, so a
medical_code bolted on later would sit outside the at-least-one rule.

## Delegation

Schema shape, not doctrine. CLAUDE.md §1 places code and tables outside the owner gate and puts
the burden of proof on ADDING apparatus; this removes a table rather than adding one. It is DG-
REVIEW rather than DG-AUTO because it changes the shape the render layer will be built against,
which the owner is entitled to see before the site is written.

## Artifacts

- `scripts/migrations/065_one_link_table_four_lenses.sql`
- `scratchpad/session_2026-09-01-lens-architecture/LENS-ARCHITECTURE.md`
- `scratchpad/session_2026-09-01-lens-architecture/insurance/`
