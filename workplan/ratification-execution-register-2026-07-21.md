# Ratification execution register — 2026-07-21

Tracks execution of the DR-2026-07-21-two-layer-functional-taxonomy §9 steps
authorized by owner directive "Ratify all" (see
`decisions/RATIFICATION-RECORD-2026-07-21.md`). Nothing here is left implicit; each
stage is staged, committed, and — per the project's execution discipline — receives
the mechanical battery and an independent adversarial pass on completion. Canonical
`data/guidebook.db` is **not** mutated until the gates pass and the apply stage is
confirmed.

| # | Stage | Kind | Status | Blocker / note |
|---|---|---|---|---|
| G1 | ~~Co-1 review gate~~ → **DISSOLVED** (not a completeness gate) | n/a | **DISSOLVED 2026-07-21** | Owner directive: lived-experience *vetting* would require an infinite surface (every cross-cut × context per §0.5/T9), so it cannot gate. Reframed as standing openness (continuous, per-person correction via Person Mode + situations); taxonomy ships as the floor and stays revisable. See `functional-taxonomy.md` §9.1 |
| G2 | Non-English concept validation (quick pass 2026-07-21) | gate | **DONE (pass 1)** | `term_aliases` (880 rows) carries no aliases yet for the new axis stems (vestibular/balance/continence/arousal/ambulation = 0; thermo = 7) — expected for new entities. Finding: native-language alias population for the 17 axes is a follow-up (E12), not a blocker; the schema apply creates the entities that alias work annotates |
| E1 | Apply schema migration `030_two_layer_functional_taxonomy.sql` to `data/guidebook.db` | DB mutation | **DONE 2026-07-21** | Applied via `db.py migrate` → user_version 30; axes 17 / population_reclass 29 / population_axis_map 69 / item_axis_links 0 / situations 0. **Rebuild-reproducibility verified** (all 5 tables byte-identical committed vs `--rebuild`); no new integrity failures (the 9 pre-exist on main) |
| G2 | Non-English concept validation: 17 axes vs `term_aliases` + searched JA/DE/ZH/KO/ES/FR strata | gate | **PENDING** | Real work; doable this repo. Must precede axis-register freeze |
| E1 | Promote staged SQL → `scripts/migrations/` (timestamped) + apply to `data/guidebook.db` + record in `data_migrations` | DB mutation | **BLOCKED** | Gated behind G1+G2. Irreversible on canonical DB — run as a distinct, confirmed, validated stage. Do NOT promote early (arms CI rebuild) |
| E2 | Backfill `slugs.serves_axes` (79 slugs) | DB mutation | **BLOCKED** | After E1. ~60 mechanical, remainder judgment |
| E3 | Harvest `item_axis_links` from 87 FDA briefs (`references/audit-briefs/*_brief.md`); then re-derive `item_population_links` | DB mutation (large) | **BLOCKED** | After E1. Largest item; likely multi-session; correctness-critical |
| E4 | Regenerate `functional-deficit-auditor_SKILL.md` §§1–2 from the axis register | skill regen | **BLOCKED** | After E3 (depends on harvested links); ends FDA↔DB↔canon drift |
| E5 | Normalise `evidence_population_match.target_population` → codes + elaboration; define non-DOI intake fields | DB mutation | **BLOCKED** | After E1 |
| E6 | Extend `db.py validate`: zero-coverage axis queries + profile-layer containment rules | tooling | **READY** | Non-DB; can proceed independently of the gates |
| E7 | Close GAP-277 (IntD info-access → AX-COG-L); open STUB-axis evidence-debt gaps | gap register | **BLOCKED** | After E1 (gap rows are DB) |
| E8 | Enum change (`PopulationCode`) per `population-taxonomy.md` §5 process | governance+schema | **BLOCKED** | After E1; follows canonical change process |

## Addendum items — from "Yes, ratify ALL recent work" (three further DRs)

| # | Stage | Kind | Status | Blocker / note |
|---|---|---|---|---|
| E9 | Pipeline-contract: reconcile stage ids vs the deployed `<audit_trail>`; resolve the blob-vs-commit `doctrine_sha` convention + `ci.yml` doctrine-gate mismatch | owner action + tooling | **BLOCKED (owner)** | Ratification precondition per DR-2026-07-13; only the owner has the deployed list. `pipeline-contract.yaml` is accepted as the Level-2 index meanwhile; the sha-convention fix also affects how every attestation's `doctrine_sha` is checked |
| E10 | ICCT: `cross_test_pairs` table + `v_cross_test_open` view (migration); `connection-discovery` `--mode category-crosstest`; `assess_cell.py` ICCT gate in the `stated` predicate (new `rule_version`); methodology doc | DB + tooling (large) | **READY (non-canonical)** | Migration is additive/read-oriented; can be authored+staged without touching determinations. The `stated`-predicate gate change is behaviour-affecting — stage under a new rule_version and adversarial-pass it |
| E11 | Product-posture: apply the `mission-and-epistemics.md` language edit (adjudicate-vs-dictate disambiguation at §doctrine) | doctrine edit (SHA cascade) | **BLOCKED (careful)** | Changes doctrine blob `0f2f525` → triggers re-attestation materiality (DR-2026-07-21-re-attestation-materiality-and-window). Run deliberately with the materiality triage, not as a casual edit |

| E12 | Native-language alias population for the 17 axes (`term_aliases`) | data | **READY** | Surfaced by G2 pass 1; enables the deeper non-English concept-carving check. Not a blocker for the schema (already applied) |

## Sequence

**G1 dissolved · G2 pass-1 done · E1 DONE (migration 030 applied + reproducibility-verified).**
Remaining: **E3** (harvest `item_axis_links` from 87 FDA briefs — the substantive next
step that makes items reference axes) and **E2** (`slugs.serves_axes`) are the bridges
that turn the now-created scaffolding into a connected graph; then **E4** (FDA skill
regen), **E5/E7/E8** (DB), **E6/E10** (tooling), **E12** (aliases). **E9** (pipeline
stage-id reconciliation) and **E11** (product-posture mission edit — doctrine-sha
cascade) remain owner-gated. All canonical-DB writes go through migration files (never
direct `db.py` writes — those bypass the reproducibility gate). Research execution
against the STUB axes stays queued behind the language/jurisdiction debt.

## Next action

The taxonomy scaffolding is live in the canonical DB. The highest-value next step is
**E3** — harvesting `item_axis_links` from the 87 FDA audit briefs — because it is what
connects the 93 items to the 17 axes and makes the two-layer model queryable end-to-end.
It is large and correctness-critical (a data migration, adversarial-passed), so it is
its own focused stage rather than part of this one.

---

## 2026-07-24 reconciliation (under RULE "merge implies ratification")

The standing rule recorded 2026-07-24 (`project-standards.md`; owner: "always assume I Ratify
if I merge it") retires the "BLOCKED — pending ratification" state for everything here: these
items are **authorized and owed**, not un-authorized. Verified against DB truth this date, and
cross-reconciled with the later **DR-2026-07-23-population-schema-replace** (which superseded the
two-layer DR's *population code scheme* but RETAINED the axes layer):

| # | Item | DB-verified status 2026-07-24 | Disposition |
|---|---|---|---|
| E1 | migration 030 (axes/scaffolding) | axes=17, access_needs=17 (031 added) — **DONE** | closed |
| E8 | `PopulationCode` enum change | **DONE differently** — replaced with the flat 23-code set by DR-2026-07-23 (`schemas/enums.py`) | closed (superseding path) |
| E5/E7 | population junctions / gap rows | **SUPERSEDED in part** by the 2026-07-23 population re-key | reconcile under new scheme, not old |
| **E3** | `item_axis_links` from 87 FDA briefs | **DONE 2026-07-24 — 157 links, 93 items → 17/17 axes** (adversarially validated, ~139/150 first-pass sound; fixes applied) | closed — see caveat |
| **E2** | `slugs.serves_axes` backfill | **column does not exist — UNBUILT** | authorized/owed (schema + data) |
| **E10** | ICCT intra-category cross-test (owner-directed 2026-07-20) | **`cross_test_pairs` table missing — UNBUILT** | authorized/owed |
| E6 | `db.py validate` axis/containment extensions | tooling — not built | authorized/owed (non-DB) |
| E12 | native-language aliases for 17 axes | not built | authorized/owed (non-blocking) |
| **E9** | pipeline-contract stage-id reconciliation | **still OWNER-INPUT** — needs the deployed `<audit_trail>` list only the owner has | remains owner-gated (rule limit 2) |
| **E11** | product-posture `mission-and-epistemics.md` edit | not applied — **doctrine-SHA cascade** | authorized but run with materiality triage (rule limit 2) |

**Bottom line:** ratification backlog clear. Done this session: **E2 (column unblocked), E6, E12, E3**.
Remaining: **E10** buildable; **E9/E11** owner-gated. (Rows above for E2/E6/E12 predate their build; see PR #63.)

**E3 epistemic caveat (owner-flagged 2026-07-24).** `item_axis_links` is a **structural / research-targeting
map, not derived content.** It was authored by mapping item *names/function* onto axis semantics — the same
knowledge that named the items — so it re-expresses, it does not discover. It was validated for *internal
consistency* against the FDA briefs (thin — gap tables only), **not** against evidence: the underlying item
set is **~0.7% researched** (15 of 2,139 item×population evidence cells exist; 11 of 93 items have any cell).
Legitimate use: show where the *current item list* is thin (e.g. AX-COG-L has items but zero population
mappings) so research can be targeted — never a substitute for the research, and not a claim about what
accessible design requires.
