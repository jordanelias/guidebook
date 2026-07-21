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
| G1 | Co-1 review gate (pre-launch form): adversarial passes + published-Co-1 checks per disposition | gate | **PARTIAL** | Two 2026-07-21 adversarial passes done (stand as the form); per-disposition published-Co-1 checks not yet run. Full discharge needs post-launch consultation (may never exist) — taxonomy is operative-but-provisional meanwhile |
| G2 | Non-English concept validation: 17 axes vs `term_aliases` + searched JA/DE/ZH/KO/ES/FR strata | gate | **PENDING** | Real work; doable this repo. Must precede axis-register freeze |
| E1 | Promote staged SQL → `scripts/migrations/` (timestamped) + apply to `data/guidebook.db` + record in `data_migrations` | DB mutation | **BLOCKED** | Gated behind G1+G2. Irreversible on canonical DB — run as a distinct, confirmed, validated stage. Do NOT promote early (arms CI rebuild) |
| E2 | Backfill `slugs.serves_axes` (79 slugs) | DB mutation | **BLOCKED** | After E1. ~60 mechanical, remainder judgment |
| E3 | Harvest `item_axis_links` from 87 FDA briefs (`references/audit-briefs/*_brief.md`); then re-derive `item_population_links` | DB mutation (large) | **BLOCKED** | After E1. Largest item; likely multi-session; correctness-critical |
| E4 | Regenerate `functional-deficit-auditor_SKILL.md` §§1–2 from the axis register | skill regen | **BLOCKED** | After E3 (depends on harvested links); ends FDA↔DB↔canon drift |
| E5 | Normalise `evidence_population_match.target_population` → codes + elaboration; define non-DOI intake fields | DB mutation | **BLOCKED** | After E1 |
| E6 | Extend `db.py validate`: zero-coverage axis queries + profile-layer containment rules | tooling | **READY** | Non-DB; can proceed independently of the gates |
| E7 | Close GAP-277 (IntD info-access → AX-COG-L); open STUB-axis evidence-debt gaps | gap register | **BLOCKED** | After E1 (gap rows are DB) |
| E8 | Enum change (`PopulationCode`) per `population-taxonomy.md` §5 process | governance+schema | **BLOCKED** | After E1; follows canonical change process |

## Sequence

Gates first (**G1 partial, G2 pending**) → **E1** apply (confirmed, validated stage)
→ E2/E3/E5/E7/E8 (DB) and E4 (skill) → E6 may run any time. Research execution against
the new STUB axes remains queued behind the language/jurisdiction debt (ratified queue
rule), so no new search work is in this register.

## Next action

G2 (non-English validation) and E6 (validator extension) are the two stages runnable
now without touching the canonical DB. Recommend running G2 next (it gates E1 and is
the ratified pre-freeze check), then returning to the owner to confirm the E1 apply as
a distinct stage.
