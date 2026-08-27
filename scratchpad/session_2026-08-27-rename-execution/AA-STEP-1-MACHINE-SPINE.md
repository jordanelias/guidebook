# Step 1 — the seven-stage spine into the machine, argued both ways

**Owner instruction:** *"Please perform next steps carefully and thoroughly in agonist-antagonist."*
Method as established: agonist states the case, antagonist attacks it, **the resolution binds to a
measurement.** Where no measurement reaches, the item is declared owner-owed rather than settled.

---

## C-0 · Is step 1 even first? — **one of my own work items dissolves**

**AGONIST (my stated order).** Seven stages first, then P0.1/P0.2, then *"three vacuous-gate
sweeps"*, then the rename. I argued the sweeps matter because *"they'd certify a broken rename
green."*

**ANTAGONIST.** Measured: the registry **already carries a reasoned `no_floor` for every one of the
four**, and none is a defect.

| gate | recorded reason |
|---|---|
| `validate_evidence_state` | *empty-by-decision* — instrumented, examining 0 because the corpus was emptied |
| `validate_verification_consistency` | *empty-by-decision* — same |
| `attestation_presence` | *changeset-scoped* — examines the synthesis files in the changeset, by design |
| `check_rendered_docs` | *examines-none-by-policy* |

Two are the ordained pre-synthesis state (`CLAUDE.md` rule 4: empty is unproven, **not** dead). One
is changeset-scoped **by design** — and that design is exactly what made CI catch my attestation
defect when the local invocation did not, because the two use different changesets. One declines by
policy.

**RESOLUTION — the work item is withdrawn.** There is nothing to sweep. `run_checks.py` already
reports them as NOTHING-IN-SCOPE precisely so nobody banks them as evidence, and the registry carries
why. **I invented this item**, and the §2(a) machinery it was meant to protect is the machinery that
refuted it.

---

## C-1 · Adding `base` to the contract — does it invent apparatus?

**AGONIST.** `pipeline-contract.yaml` is, in `CLAUDE.md`'s own words, *"the single home of the stage
ids."* The ledger, `CLAUDE.md` and eight ratified Decision Records all say seven stages; the contract
says five. **The declared single home disagrees with everything that cites it.**

**ANTAGONIST — the schema demands more than a name.** Every stage requires `anchor`, `entry` and
`criteria`, and every criterion requires `id`, `kind`, `criterion`, `references` and a `check`.
**What are `base`'s criteria?** Inventing them to satisfy a schema shape is §1's burden unpaid in its
purest form — apparatus added because a structure demands it, not because something wrong reaches the
guidebook without it. And `base` is the vocabulary layer: what integrity property does a vocabulary
even have that a check enforces?

**Measured — the criteria already exist, unattributed, and five of them are BLOCKING.**

```bash
python3 -c "import yaml;d=yaml.safe_load(open('governance/check-registry.yaml'));
print(len([c for c in d['checks'] if c.get('basis')=='unattributed']))"   # -> 30
```

Of those 30, eleven are base-shaped, and these have a clean one-to-one with a criterion:

| existing check | level | becomes the enforcer for |
|---|---|---|
| `validate_schema`, `validate_schema_cross_check` | **blocking** / advisory | `base/base-schema-validates` |
| `validate_population`, `population_integrity_audit` | advisory | `base/base-population-vocabulary` |
| `validate_axes` | **blocking** | `base/base-demand-vocabulary` |
| `validate_jurisdiction` | **blocking** | `base/base-jurisdiction-vocabulary` |
| `validate_items` | advisory | `base/base-parameter-vocabulary` |
| `retired_vocabulary` | advisory | `base/base-retired-vocabulary-not-taught` |

> **RESOLUTION — nothing is invented. `base` gets a contract entry that gives a home to eight checks
> that already run and have never had a stage to belong to.** The reason they were "unattributed" is
> that the contract had no stage for them. That is the §1 burden paid in the strongest available
> form: the apparatus exists, it enforces, and the record was the thing missing.

**Deliberately left unattributed:** `test_db_integrity`, `source_slug_links_duplicates`,
`validate_pydantic_schemas` — cross-cutting, not base-specific. Attributing them to `base` to reduce
a count would be the invention this contest exists to prevent.

---

## C-2 · Moving four criteria from `judgment` to `specification`

**AGONIST.** M-6, established earlier this session: four of judgment's criteria are enforced by
`scripts/validate_evidence_state.py` **against the `specifications` table**. They are specification
criteria mis-filed under judgment.

**ANTAGONIST.** A criterion's home should follow the *stage that must satisfy it*, not the table its
enforcer happens to read. Judgment produces the inputs a specification rests on; if judgment stops
being answerable for governing-refs, does anything check them earlier?

**Measured.** `validate_evidence_state.py` names `specifications` **8 times**, and the four criteria
—`governing-refs-nonempty`, `no-regulatory-stratum-stated`, `tier3-alone-threshold`,
`derivation-handshake` — are each stated over a determination, which under D-0168 is the
specification stage's object, not judgment's. Judgment's own object is the extracted, tiered,
categorised value.

**RESOLUTION — move the four.** Judgment keeps `handoff-fanout-preserved` (which guards the
evidence→judgment fan-out this session ruled) and `convergence-independence` (which counts
independent evidence axes — a judgment act). **The antagonist's concern is real and is answered by
what stays**, not by leaving the four mis-filed.

---

## C-3 · Rename the stage id `evidence-collection` → `evidence`?

**AGONIST.** The ruled spine is *"Base Research Evidence Judgment Synthesis Specifications Render."*
The owner wrote **Evidence**. Leaving `evidence-collection` reproduces in miniature the exact defect
this step exists to fix: the machine holding a name doctrine has moved past.

**ANTAGONIST.** It is a stage-id rename, and stage ids are load-bearing — `basis:` refs are
stage-qualified, and `stage_label()` derives display from the id. This is precisely the surface that
broke `--selftest` on the last stage rename (2026-08-25, C7).

**Measured — the caller set is small and fully enumerable:**

```
CLAUDE.md · governance/check-registry.yaml · governance/pipeline-contract.yaml
references/project-standards.md · tools/pipeline_completeness.py          (5 live)
audits/…2026-07-12.md · workplan/2026-08-22-master-execution-plan.md      (2 frozen/superseded)
```

**RESOLUTION — rename, and run `--selftest`, not just `--changed-from`.** Five live callers is a
sweep I can complete and verify in one pass, and C7 is the check that proves it. The frozen two are
historical records and are left alone.

---

## What this step does NOT do

- **It does not touch the database.** No migration, no `user_version` bump. The spine is a contract
  and a stage list; the table renames are step 4 and are separately blocked.
- **It does not resolve `base_building`'s shape.** Still owner-owed.
- **It does not promote any gate.** `decision_capture` stays advisory per the owner's selection.
