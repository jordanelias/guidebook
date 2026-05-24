# Session record: 2026-05-23 — BPC rewrite workplan Phase B.0 closure (pre-rehab banner cohort)

**Session ID:** `session_2026-05-23-bpc-rewrite-phase-b-closure`
**Span:** 2026-05-23 ~23:00 UTC → 2026-05-23 ~23:50 UTC
**Bootstrap version:** PI v10.14 + architecture v2.3 + userPreferences v6.3
**Headline outcome:** B.0 closed — 68 unique slugs / 70 BPC files carry the `SYNTHESIS VALIDITY: PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION` banner; `bpc_metadata.evidence_state = 'RETRACTED-PRE-REHAB'` for the 68 slugs. New DR (DR-2026-05-23) defines the cohort; new audit script (Level 2) verifies four invariants. v10.15 PI queue entry briefly proposed then withdrawn per owner directive (no PI bump unless critical armature) — the DR + audit + DB state are sufficient armature. B.10/B.8 trivial gap closed: REF-00734 Tibble 2005 `synthesis_attribution_required` flag backfilled; 30/30 co1 rows now flagged. **B.11 batch 1 completed (backward + forward) for 5 Tier-1 sources in `room-acoustic-performance`** via CrossRef (backward) and OpenAlex `cites:` API (forward); B=1/F=1 on all 5 rows; 173 backward + 69 forward = 242 NEW candidate references surfaced for next-session triage. (Turn 4's initial DEFERRED forward state was corrected in turn 5 once owner pushback prompted investigation of alternatives — Scholar Gateway unavailability does not mean ALL forward sources unavailable; OpenAlex provides free programmatic cited-by lookup matching skill §2's spirit.)

---

## Headline outcomes

| Metric | Pre-session | Post-session | Δ |
|---|---|---|---|
| bpc_metadata rows with `evidence_state = 'RETRACTED-PRE-REHAB'` | 0 | 68 | +68 |
| BPC md files carrying SYNTHESIS VALIDITY banner | 0 | 70 | +70 |
| Active workplan §B.0 status | OPEN, target ~30 BPCs | CLOSED, applied to 70 files / 68 slugs | closed |
| co1 rows with `synthesis_attribution_required = 1` (B.10) | 29/30 | 30/30 | +1 |
| Co-1 six-field set (B.8) | 29/30 | 30/30 | +1 |
| citation_mining backward=1 rows (B.11) | 2 (school-environment-autism) | 7 (+ 5 room-acoustic-performance) | +5 |
| citation_mining forward=1 rows (B.11) | 0 | 5 (room-acoustic-performance) | +5 |
| B.11 unmined T1-3 sources for room-acoustic-performance | 22 | 17 | -5 |
| Backward discovery surface (NEW candidate refs) | n/a | 173 | new |
| Forward discovery surface (NEW candidate refs) | n/a | 69 | new |
| Phase B substantive items remaining | 3 (B.0, B.11, B.9) + 2 trivial (B.8, B.10) | 2 (B.11 in progress, B.9) | -3 |
| Eligible evidence pool (rule #10) | 638/638 (100%) | 638/638 (100%) | unchanged |
| pre_rehab_banner_audit invariants | n/a (script didn't exist) | 4/4 PASS | new audit |
| Pending data migrations on b0a4a25 | 114 (pre-existing drift) | 118 | +4 |

---

## Cohort vs handoff target

Handoff sized B.0 at ~30 BPCs. The actual cohort is 2.3× larger (70 files / 68 unique slugs). The discrepancy was surfaced in turn 1 as `[GAP: handoff-target-mismatch — ~30 stated, ≥70 found]`, three cohort-definition options were enumerated (A literal PI #10, B full pre-rehab, C unknown narrower subset), Option B was recommended, the owner replied "proceed" which was interpreted as approving B per `<intent_resolution>` first-reasonable-read commit. DR-2026-05-23 documents the decision; the v10.15 queue entry in `decisions/PI-update-needed.md` proposes a literal rule #10 text patch to reflect the broader cohort definition.

A narrower interpretation (e.g., A) would re-bound the cohort to ~65 files (only the bare `[OPUS-SYNTHESIS]` tag with `Updated: 2026-03-29` headers, excluding the April-round 14 and the 4 provisional variants). The DB migration is forward-reversible — specific slugs can be transitioned out of `RETRACTED-PRE-REHAB` without retracting the DR if the owner narrows the cohort.

---

## Commits

(To be appended by the commit itself; see below.)

---

## Artifacts touched

| Path | Action | Banner / new content |
|---|---|---|
| `decisions/DR-2026-05-23-pre-rehab-banner-cohort-definition.md` | NEW | DR documenting cohort definition + Phase E.2g overwrite predicate |
| `decisions/DR-2026-05-23-cohort-manifest.json` | NEW | Frozen cohort enumeration (70 files, 68 slugs) at HEAD b0a4a25 |
| `decisions/PI-update-needed.md` | MODIFIED | v10.15 queue entry: rule #10 final-paragraph cohort wording patch |
| `scripts/migrations/data_20260523230900_pre_rehab_banner_evidence_state.sql` | NEW | Data migration updating 68 unique slugs to `evidence_state = 'RETRACTED-PRE-REHAB'` |
| `scripts/audit/pre_rehab_banner_audit.py` | NEW | Level 2 audit verifying 4 invariants (cohort↔banner, cohort↔DB, no over-banner, no over-DB) |
| 70 files under `references/bpc/**.md` | MODIFIED | `SYNTHESIS VALIDITY: PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION` banner inserted after the existing `Opus synthesis:` / `Opus synthesis complete` anchor line |
| `data/guidebook.db` | UPDATED | 68 rows in `bpc_metadata` set to `evidence_state = 'RETRACTED-PRE-REHAB'`; new row in `data_migrations` for `data_20260523230900_pre_rehab_banner_evidence_state` |
| `attestations/decisions_DR-2026-05-23-pre-rehab-banner-cohort-definition.json` | NEW | Per-rule status for the new DR |
| `attestations/decisions_PI-update-needed.json` | MODIFIED | Re-attested for this session's PI-update-needed edit |
| `attestations/sessions_session_2026-05-23-bpc-rewrite-phase-b-closure.json` | NEW | Per-rule status for this session record |
| `sessions/LATEST` | UPDATED | Pointer → `session_2026-05-23-bpc-rewrite-phase-b-closure.md` |
| `decisions/PI-update-needed.md` | RE-MODIFIED (later in session) | v10.15 queue entry withdrawn per owner directive; replaced with "considered and rejected" note citing architecture v2.3 state-vs-rule clause |
| `decisions/DR-2026-05-23-pre-rehab-banner-cohort-definition.md` | RE-MODIFIED (later in session) | Companion-to-PI-update-needed line removed; new "Why no PI amendment is needed" section added |
| `scripts/migrations/data_20260524011500_b11_room_acoustic_mining_batch1.sql` | NEW | B.11 batch 1 BACKWARD migration — CrossRef-sourced ref lists for 5 Tier-1 sources |
| `scripts/migrations/data_20260524063500_b11_room_acoustic_forward_mining.sql` | NEW | B.11 batch 1 FORWARD migration via OpenAlex `cites:` API — supersedes turn-4 DEFERRED state |
| `sessions/artifacts/2026-05-23-b11-room-acoustic-mining-discoveries.json` | NEW | BACKWARD discovery surface — 5 sources × 173 NEW candidate refs |
| `sessions/artifacts/2026-05-23-b11-room-acoustic-forward-discoveries.json` | NEW | FORWARD discovery surface — 5 sources × 69 NEW candidate refs (OpenAlex citers) |
| `data/guidebook.db` (B.11 update) | RE-UPDATED | 5 citation_mining rows (B=1, F=1, deferred_reason cleared) + 1 GAP row (GAP-292) + 3 data_migrations entries |

---

## Known broken / pending work

1. **Data-migrations tracking drift (pre-existing).** `data_migrations` table is ~92 rows behind the migration-file count (38 applied per table, 130 files present, 114 reported as pending by the dry-run, of which most are already mechanically applied to `data/guidebook.db` but not recorded in the tracking table). This session's migration was applied directly + recorded manually to avoid touching the broader drift. Recommend: a dedicated cleanup pass (probably a DR + reconciliation script) before the next regular migration session.
2. **Two duplicate-slug files surfaced in the cohort.** `thermoregulation-built-environment` and `cross-population-conflict-resolutions` each have two markdown copies in different directories. Both copies received the banner this session. Duplicate-file resolution is a Phase E.2g triage task per the DR; not in scope this session.
3. **Markdown citation drift from 40 excised ref-ids.** BPC reasoning docs still contain textual citations to the 40 ref-ids excised on 2026-05-23. Source_slug_links rows cascade-deleted on the DB side, but raw markdown readers see dangling pointers. Separate cleanup pass — not started in this session, not started in the prior either.
4. **`bpc-rewrite-workplan-2026-05-11.md` §B.0 status update.** The workplan still lists B.0 as "Target: ~30 BPCs; Current: 0 applied." That document should be updated to reflect the closure (with the corrected cohort size of 70 files / 68 unique slugs). Not done this session; queued.
5. **PI rule #10 cohort wording — no amendment.** The live PI in claude.ai (v10.14) reads "from the 2026-03-30 round." Per owner directive 2026-05-23, this is not amended — the DR + audit script + DB state are the operational armature for the broader cohort. Architecture v2.3 `<migration_and_growth>` explicitly places state of this kind out of PI. The `[ASSUMPTION: applying broader cohort per DR-2026-05-23]` tag that briefly stood for the v10.15-queued period is retired; the DR is the standing reference.
6. **GAP-292 (logged this session): REF-00571 misclassification.** Kotloski 2020 rat-kindling/TBI-seizure paper (DOI `10.3389/fneur.2019.01286`) is linked to slug `room-acoustic-performance` as RAP-13 but is unrelated to acoustic performance. Surfaced during B.11 backward mining. Owner action: reclassify or retire the `source_slug_links` row. P2 priority.

---

## Next-action handoff

**Phase B continuation:**

- **B.11 citation mining.** ~58 slugs / ~80+ sources remaining. **Batch 1 of room-acoustic-performance complete (5/22 Tier-1 sources mined backward + forward; 17 remaining in this slug).** Skill: `citation-miner`. Per-slug effort: ~30 min per 5-source batch using the CrossRef (backward) + OpenAlex `cites:` (forward) pattern validated this session.
  - **Discovery triage queue:** 173 backward + 69 forward = 242 NEW candidate refs in `sessions/artifacts/2026-05-23-b11-room-acoustic-*-discoveries.json` need per-row tier classification + verification + INSERT before they can support synthesis. Workflow option A: process discoveries before moving to next batch (preserves mining momentum within slug). Workflow option B: rotate to other slug batches and bulk-triage discoveries periodically (preserves discovery depth across slugs).
  - **Forward mining via OpenAlex** is the validated path. Skill §0 names Scholar Gateway as "preferred for forward"; when Scholar Gateway's `cites` endpoint is unavailable, OpenAlex's free `filter=cites:{work_id}` endpoint provides equivalent citation-relationship data and matches skill §2 spirit ("Scholar Gateway forward citations or Google Scholar 'cited by'"). The skill text could be amended to name OpenAlex explicitly as an accepted forward source; that is a skill-file edit not a PI bump.
- **B.9 derivation_chain.** 14/638 populated; ~186 cited sources remaining at ~10 min each. Can run in parallel with B.11.
- ~~B.8 Co-1 six fields.~~ **CLOSED this session** — 30/30 via REF-00734 backfill.
- ~~B.10 synthesis_attribution_required.~~ **CLOSED this session** — 30/30 co1 rows flagged.
- **B.12 Tier 2 jurisdictional instruments.** Partial across rehab batches; needs an inventory pass.

**After all of Phase B closure:**

- Phase E.1 pilot per PI rule #10 Track 3 mandate: single BPC under `reasoning_doc_citations` workflow with inline review before scaling. Candidate: any of the 68 RETRACTED-PRE-REHAB slugs — recommend choosing one that already has good citation-mining + derivation_chain coverage so Phase E.1 is bounded to the reasoning-doc-citations protocol itself and isn't blocked on B.11/B.9 backfill.

**Owner action queue:**

- Optionally: review DR-2026-05-23 cohort definition — if `~30` was the intended scope, narrow back via a follow-up migration transitioning specific slugs out of `RETRACTED-PRE-REHAB`.
- The pre-existing data_migrations tracking drift is owner-visible but not yet on a queue; consider whether to address before the next migration session.
