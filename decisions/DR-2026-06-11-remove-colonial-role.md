# DR-2026-06-11: Remove COLONIAL from the lang_jur_map role taxonomy

- Status: ACCEPTED
- Date: 2026-06-11
- Decider: owner (jordanelias); executed by session_2026-06-11-stage-4.3-gate-closure
- Affects: workplan A.3 (line 218), schema migration 023 CHECK, data migration data_20260611224657

## Context

`lang_jur_map.role` was specified in workplan A.3 (`audits/bpc-rewrite-workplan-2026-05-11.md`, line 218) as `role in {PRIMARY, SECONDARY, COLONIAL}`. The COLONIAL value:

- was never defined anywhere. A.3 lists the role set and gives PRIMARY/SECONDARY examples but states no criterion distinguishing COLONIAL from SECONDARY.
- is contradicted by A.3's own examples, which mark colonial-legacy English as SECONDARY: `(EN, IN, SECONDARY), (EN, ZA, SECONDARY)`.

The value traces to the workplan commits `ce26611` and `e8a8350` (2026-05-10/11), authored under the jordanelias git identity, then transcribed into the schema CHECK by migration 023 (2026-06-09). It was not an AI invention lacking spec basis; an earlier characterization to that effect during this session was wrong and is corrected below.

During Stage 4.3 gate G5, this session populated `lang_jur_map` (data migration `data_20260611224657`) with 49 rows including 9 COLONIAL rows. That population was premature: migration 023 had explicitly deferred population pending owner role definitions, and the COLONIAL assignments contradicted A.3's examples. The owner then directed removal of all instances of COLONIAL.

## Decision

Remove COLONIAL from every operative location:

1. Workplan A.3 role set: `{PRIMARY, SECONDARY, COLONIAL}` becomes `{PRIMARY, SECONDARY}`.
2. Schema CHECK: migration 025 rebuilds `lang_jur_map` with `role IN ('PRIMARY', 'SECONDARY')`.
3. Data: the premature G5 population is reverted; `lang_jur_map` is reset to empty.

Because CI rebuilds all schema migrations before all data migrations, tightening the CHECK while data migration `data_20260611224657` replays its COLONIAL inserts is impossible (the inserts violate the tightened CHECK on rebuild). The erroneous, same-day G5 data migration is therefore withdrawn: its file is deleted and its `data_migrations` ledger row is removed (within migration 025) so that the committed DB equals a fresh rebuild. This is a deliberate, scoped exception to the forward-only / append-only migration convention, justified because the migration is same-day, erroneous, and depended on by nothing.

Historical migration 023 retains COLONIAL in its CREATE statement as an immutable audit record; it is superseded by migration 025 at the live-schema level.

## Consequences

- `lang_jur_map` is empty with CHECK `('PRIMARY', 'SECONDARY')`; `user_version` is 25.
- The table must be repopulated later under owner-defined PRIMARY/SECONDARY criteria. A.3's deferred role definitions remain outstanding. Five jurisdictions whose only candidate mapping was colonial-legacy English (NG, GH, ZA, PH, SG) are unmapped until those definitions exist.
- Rebuild reproducibility verified: the 7 invariants and `user_version` reproduce; ledger count 187 equals 187 between committed and rebuilt.

## Provenance correction

An earlier statement this session, that COLONIAL was "an AI invention with no spec basis," was incorrect. COLONIAL was in the adopted workplan A.3, committed under the owner's git identity. The only Claude-authored step in its lineage was migration 023 transcribing it into the schema. This record corrects that error.
