# Session record: 2026-05-19 → 2026-05-20 — V2-manual verification pilot + CI restoration + governance drift

**Session ID:** `session_2026-05-19-deployment-state-reconciliation`
**Span:** 2026-05-19 ~18:00 UTC → 2026-05-20 ~07:00 UTC (single conversation, multi-stage; persistence compaction at ~05:30)
**Bootstrap version:** PI v10.13 + architecture v2.3 + userPreferences v6.3
**Pilot artifact:** DR-2026-05-19 Channel-2 manual verification protocol — proposed, 5 amendments, 6 pilot batches executed
**Outcome:** V2-manual NULL-verification COMPLETE-STATUTORY queue drained 41→0; rule #10 eligible pool 221→236 (33.0%→35.2%); both CI workflows restored to fully green after long-standing pre-session breakage; 4 governance drifts surfaced (1 fixed, 1 documented forward).

---

## Headline outcomes

| Metric | Pre-session | Post-session | Δ |
|---|---|---|---|
| Eligible (rule #10, COMPLETE+COMPLETE-STATUTORY×VERIFIED+UNVERIFIED-1) | 221 (33.0%) | 236 (35.2%) | +15 |
| V2-manual NULL queue (COMPLETE-STATUTORY × NULL verification_status) | 41 | 0 | -41 |
| IS-PAYWALL owner-purchase queue | 0 | 18 | +18 |
| NEEDS-HUMAN owner-different-IP queue | 0 | 2 | +2 |
| DEFERRED-V2-AUTOMATED queue (V2-scraper priority) | 0 | 19 | +19 |
| Both CI workflows green on HEAD | ✗ (failing pre-session debt) | ✓ (`777bdbf`) | restored |

Net: 41 rows moved from `NULL` to explicit-cause states; 15 of those joined the eligible pool (either via fresh VERIFIED probe or via standard-number-inheritance from a VERIFIED canonical).

---

## Commits in chronological order

1. `29ea3bf` — governance: snapshot PI v10.13 to repo (`governance/project-instructions-v10_13.md`)
2. `9e2b986` — governance: reconcile PI deployment queue (v10.11/12/13 all live, snapshotted) **[DOCTRINE]**
3. `d641e42` — governance: propose DR-2026-05-19 channel-2 manual verification protocol **[DOCTRINE]**
4. `671be9b` — manual-statutory-verification: V2-manual pilot batch 1 (AU/NO/US/NZ): 3 VERIFIED + 1 UNVERIFIED-1
5. `1290f2d` — governance: DR-2026-05-19 batch 1 findings + routing-table refinements **[DOCTRINE]**
6. `662af85` — governance: DR-2026-05-19 batch 2 findings + IS-PAYWALL/DEFERRED-V2-AUTOMATED state-machine extension **[DOCTRINE]**
7. `6a388e5` — manual-statutory-verification: V2-manual pilot batch 2 (hard-case CN/JP/NL/BR/JA): 0 VERIFIED, 3 IS-PAYWALL, 2 DEFERRED-V2-AUTOMATED
8. `27083b2` — manual-statutory-verification: extend B01/B02 enum allowlists for new states; strip data_migrations INSERTs to unblock --rebuild
9. `6e6c35d` — manual-statutory-verification: DB-integrity CI restoration (v1_legacy sync C05/D02, Bettarello dedup REF-00047→REF-00561 D01, author backfill G02); 35/35 checks pass
10. `fb08405` — governance: DR-2026-05-19 batch 3 findings + B01 V1-§4 enum sync **[DOCTRINE]**
11. `0941a03` — manual-statutory-verification: V2-manual pilot batch 3 (middle-cohort SE/CA/SG/INT): 1 VERIFIED + 1 IS-PAYWALL + 2 NEEDS-HUMAN + 1 DEFERRED-V2-AUTOMATED
12. `5b1dc42` — manual-statutory-verification: retroactive search-log stubs for economics-sources + government-grant-programmes (rule #4 audit-trail parity restored)
13. `ba6d11e` — manual-statutory-verification: remove orphan threshold CI step per CO-0009 (long-standing CI bug since 2026-05-04 — script archived, CI invocation never cleaned up)
14. `478683f` — governance: DR-2026-05-19 batch 4 amendment — standard-number-inheritance mechanic **[DOCTRINE]**
15. `ff9f1ac` — manual-statutory-verification: V2-manual pilot batch 4 inheritance (21 rows × 7 standards): +9 VERIFIED, +1 UNVERIFIED-1, +6 IS-PAYWALL, +5 DEFERRED-V2-AUTOMATED
16. `56e823d` — manual-statutory-verification: rename attestations to `decisions_` prefix per audit-script naming convention
17. `4df63ca` — manual-statutory-verification: V2-manual pilot batch 5 (8 probed + 6 inherited): +1 VERIFIED + 9 IS-PAYWALL + 4 DEFERRED-V2-AUTOMATED
18. `2a9fad3` — governance: DR-2026-05-19 batch 6 amendment — jurisdiction-pattern routing mechanic **[DOCTRINE]**
19. `777bdbf` — manual-statutory-verification: V2-manual pilot batch 6 (jurisdiction-pattern routing): 6 CN/JP rows DEFERRED-V2-AUTOMATED; NULL queue drained 6→0

---

## DR-2026-05-19 protocol evolution

The DR was authored as the formal specification of a manual-verification track running parallel to the (still unbuilt) V2-automated track. It evolved through 5 amendments responding to observed pilot outcomes:

| Amendment | Trigger | New mechanic / refinement |
|---|---|---|
| Original (d641e42) | Sonnet authoring | §3 four-criterion VERIFIED predicate; §3.4 15-jurisdiction routing table; §3.5 7-state machine |
| 1 (1290f2d) | Batch 1 findings | Routing-table refinements (NO year-encoded IDs, NFPA JSON-in-HTML pattern, NZ SPA route confirmed as UNVERIFIED-1) |
| 2 (662af85) | Batch 2 owner-direction "I can't help with 403s if they're not in English or paywall" | Added IS-PAYWALL and DEFERRED-V2-AUTOMATED as 6th/7th state-machine values; refined NEEDS-HUMAN scope |
| 3 (fb08405) | Batch 3 yield | Cumulative-yield projections refined; B01 enum allowlist sync to V1 §4 spec (NO-MATCH, NEEDS-HUMAN, SUPERSEDED, REVERTED) |
| 4 (478683f) | Inheritance opportunity recognized in batch 4 | Standard-number-inheritance mechanic: exact-string match propagates verification status across same-standard rows; tool suffix `-inherited` |
| 5 (2a9fad3) | Last 6 NULL rows queued and protocol-blocked | Jurisdiction-pattern routing mechanic: ≥3 establishing canonicals per pattern; constrained to non-VERIFIED states only; tool suffix `-pattern` |

---

## Routing matrix (operative, final form)

| Block type | language | paywalled? | Status | Owner can help? |
|---|---|---|---|---|
| Cloudflare/bot 403 | EN | n/a | NEEDS-HUMAN | yes (different-IP) |
| SPA catalog | EN | yes | IS-PAYWALL | yes (purchase) |
| SPA catalog | non-EN covered (19-lang) | yes | IS-PAYWALL | yes (purchase) |
| SPA catalog | EN | no | UNVERIFIED-1 | n/a (cleared gate) |
| SPA catalog | non-EN | no | DEFERRED-V2-AUTOMATED | no |
| 403 / DNS / blocked | non-EN | no | DEFERRED-V2-AUTOMATED | no |
| URL-guess fails | any | no | DEFERRED-V2-AUTOMATED | no |
| Static portal | EN | no | VERIFIED | n/a (cleared gate) |

Three routing mechanics (chronological introduction): (1) per-row probe — DR §3 original; (2) standard-number-inheritance — amendment 4, exact `standard_number` match across rows; (3) jurisdiction-pattern routing — amendment 5, non-VERIFIED only, requires ≥3 establishing canonicals.


## Pilot yield analysis

**Batch-level outcomes:**

| Batch | type | rows | VERIFIED | UNVERIFIED-1 | IS-PAYWALL | NEEDS-HUMAN | DEFERRED |
|---|---|---|---|---|---|---|---|
| 1 | probed (easy-case) | 4 | 3 | 1 | 0 | 0 | 0 |
| 2 | probed (hard-case) | 5 | 0 | 0 | 3 | 0 | 2 |
| 3 | probed (middle-cohort) | 5 | 1 | 0 | 1 | 2 | 1 |
| 4 | inherited | 21 | 9 | 1 | 6 | 0 | 5 |
| 5 | probed + inherited | 14 | 1 | 0 | 9 | 0 | 4 |
| 6 | pattern-routed | 6 | 0 | 0 | 0 | 0 | 6 |
| **Total** | — | **55** | **14** | **2** | **19** | **2** | **18** |

Counts include the Bettarello dedup absorption: probed batch 4 inheritance contributed +9 VERIFIED, but REF-00047 dedup (-1 from eligible pool) means the net eligibility delta is +15 not +16.

**Yield ratios:**
- Gate-clear (VERIFIED + UNVERIFIED-1): 16/55 = **29%**
- Owner-actionable (IS-PAYWALL + NEEDS-HUMAN): 21/55 = **38%**
- V2-scraper-priority (DEFERRED-V2-AUTOMATED): 18/55 = **33%**

The pattern routing in batch 6 (6 rows, 0 gate-clears) pulls the gate-clear ratio down. Restricting to probed+inherited rows only: 16/49 = **33%** gate-clear — close to the batch-2 amendment projection of 25–40%.

**Mechanic contribution to eligibility delta:**
- Per-row probes: +5 VERIFIED + 1 UNVERIFIED-1 = +6
- Inheritance (batch 4 + batch 5): +9 VERIFIED + 1 UNVERIFIED-1 = +10
- Dedup absorption: -1
- **Net: +15 to eligible pool**

Inheritance was the highest-yield mechanic by raw count (10 of 15 eligibility gains), but only because of the existence of multi-citation same-standard rows from prior session ingest. The mechanic is not generative — it cannot add eligibility beyond what same-standard groupings allow.

---

## Pre-session debt resolved

Four CI-blocking issues that predated this session and had been silently failing every push:

1. **Orphan `Check file thresholds` CI step** (`.github/workflows/ci.yml`) — referenced `scripts/check_thresholds.py` which was archived to `_archived/` per CO-0009 on 2026-05-04. The CO explicitly said "no longer called by any skill or CI" but the CI invocation was never removed. **Failing on every push for 15 days.** Fixed in `ba6d11e`.

2. **B01 enum allowlist drift** (`scripts/tests/test_db_integrity.py`) — `VALID_VSTATUS` did not include `COMPLETE-STATUTORY` (introduced by DR-2026-05-18 7 days earlier) nor the new V2-manual states. Extended in `27083b2` (initial: COMPLETE-STATUTORY + IS-PAYWALL + DEFERRED-V2-AUTOMATED) and `fb08405` (full V1 §4 sync: NO-MATCH, NEEDS-HUMAN, SUPERSEDED, REVERTED).

3. **v1_legacy parity** (C05/D02) — REF-00726 and REF-00727 added to `evidence_sources` on 2026-05-17 without parallel inserts into `evidence_sources_v1_legacy`. Per the 2026-05-15 sync-precedent established by `data_20260515210000`, v1_legacy is a synced shadow (not an archaeological freeze). Sync migration `data_20260519055000` resolved.

4. **Bettarello 2021 duplicate DOI** (D01) — DOI `10.3390/app11093942` shared between REF-00047 (legacy ghost with wrong title field) and REF-00561 (canonical, verified 2026-05-16, named in DR-2026-05-13 §4 as the "Bettarello precedent"). Dedup migration `data_20260519060000` repointed REF-00047's single source_slug_link to REF-00561 and deleted REF-00047 from both `evidence_sources` and `evidence_sources_v1_legacy`.

5. **Two missing-search-log BPCs** (cross-refs CI) — `economics-sources` and `government-grant-programmes` BPCs authored 2026-05-03 without corresponding search-log entries (rule #4 violation by the original session). Retroactive search-log stubs authored in `5b1dc42`, explicitly flagged as `retroactive_backfill: true` with original-session-record honestly missing.

6. **Author-row coverage gap** (G02) — 2 COMPLETE non-corporate rows missing author rows (REF-00726, REF-00727), plus 1 partial-coverage row (REF-00561 had 1 of 4 authors). All 3 backfilled in `data_20260519061000` (9 total author rows added).

After these were fixed, `35/35` db_integrity checks passed locally and on CI for the first time this session.

---

## Surfaced drift (forward-only documentation)

### Drift 1: Commit-msg format vs DOCTRINE-token placement

**Issue.** `scripts/ci_helpers/check_commit_msg.py` requires the regex pattern `^[a-z][a-z0-9_-]+:\s+.+\s+\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\]$` — i.e., the `[YYYY-MM-DD HH:MM]` timestamp must be **the last bracket** on the commit line. The doctrine-SHA token introduced by rule #11 / PI v10.13 is independently validated by `audit.yml`'s grep-based check, which does not care about position. Six governance commits this session wrote the doctrine token AFTER the timestamp (`... [2026-05-20 06:37] [DOCTRINE: 61c7f95]`), which puts the timestamp in the middle of the line and fails the commit-msg format check.

**Affected commits:** `9e2b986`, `d641e42`, `1290f2d`, `662af85`, `478683f`, `2a9fad3`. All flagged commit-msg job as `failure`; overall `Guidebook CI` run reported `failure` despite all five other jobs passing.

**Resolution.** Going forward, governance commits with doctrine token use order: `{skill}: {action} [DOCTRINE: SHA] [YYYY-MM-DD HH:MM]`. Token first, timestamp last. (PI v10.13 rule #11 sub-(a) text does not specify token placement; this is a CI-format vs documentation-convention mismatch. A v10.14 micro-patch could state the order explicitly. Pre-existing governance commits show the same pattern, so this is not session-introduced — I propagated it.)

**Not fixed historically.** Rewriting old commit messages requires force-push of `main`, which the project's CI gate on `main` discourages. The 6 commits remain with their original (failing-cm-format) messages; future commits will use the correct order.

### Drift 2: Attestation naming convention

**Issue.** `scripts/audit/adherence_log_audit.py::_attestation_path_for` produces `attestations/{prefix}_{stem}.json`, where `prefix` is the first path component of the synthesis file (e.g., `decisions` for files under `decisions/`). Initial session commits wrote attestations as `attestations/DR-2026-05-19-channel-2-manual-verification.json` (no prefix) and `attestations/PI-update-needed.json` (no prefix). The CI `check_0_presence` check passed on most commits because the same commit also included the attestation file (lit by the "OR rel in changed" branch of the check), but commit `478683f` triggered a presence failure because of a transient interaction with the diff scope.

**Resolution.** Renamed both files via `git mv` in `56e823d`. Going forward, `decisions/<name>.md` → `attestations/decisions_<name>.json`.

### Drift 3: PI numerator references stale `/661`

**Issue.** PI v10.13 rule #10 prose ("`metadata_quality = AUTHOR-TITLE-ONLY` ... / 661") and bootstrap status block lines use `/661` as the denominator. Actual evidence_sources count fluctuates: was 671 at session start, is 670 post-dedup.

**Resolution.** Not fixed this session — minor cosmetic drift that doesn't affect any gate. Candidate for a v10.14 micro-patch alongside the DOCTRINE-ordering note above.

### Drift 4: Bootstrap status grep matches wrong header shape

**Issue.** Bootstrap line `grep -E "session_close|next_action|blockers" /tmp/session.md` matches against expected session-record headers, but the current session-record format (this file included) doesn't use those exact keywords. Bootstrap quietly returns no lines on this grep but doesn't halt.

**Resolution.** Not fixed this session — would require either renaming session-record sections to match the grep or amending bootstrap to match the actual format. Candidate for v10.14.

---

## Migrations committed (sequence of 8)

1. `scripts/migrations/data_20260519020000_v2_manual_verification_pilot_batch_1.sql` — 4 batch-1 probe writes
2. `scripts/migrations/data_20260519050000_v2_manual_verification_pilot_batch_2.sql` — 5 batch-2 probe writes
3. `scripts/migrations/data_20260519055000_v1_legacy_sync_marzi_2024_2025.sql` — C05/D02 parity restore
4. `scripts/migrations/data_20260519060000_dedup_bettarello_2021_app11093942.sql` — D01 fix
5. `scripts/migrations/data_20260519061000_author_backfill_bettarello_2021_marzi_2024_2025.sql` — G02 fix
6. `scripts/migrations/data_20260519063000_v2_manual_verification_pilot_batch_3.sql` — 5 batch-3 probe writes
7. `scripts/migrations/data_20260519064500_v2_manual_verification_pilot_batch_4_inheritance.sql` — 21 inherited writes
8. `scripts/migrations/data_20260519070000_v2_manual_verification_pilot_batch_5.sql` — 14 writes (8 probed + 6 inherited)
9. `scripts/migrations/data_20260519073000_v2_manual_verification_pilot_batch_6_pattern.sql` — 6 pattern-routed writes

All migrations applied via direct Python execution and recorded in `data_migrations` table with filename-stem `migration_id` (avoiding the pre-session `migrate_db.py --rebuild` UNIQUE-constraint bug with custom IDs).

Migration reproducibility verified at each commit: `python3 scripts/migrate_db.py --rebuild /tmp/r.db` replays all 20 active data migrations + 2 schema migrations cleanly. CI rebuild-parity check passes invariant comparisons across 7 tables.

---

## Rule traceability (what fired where)

| Rule | Mechanism | This session's instance |
|---|---|---|
| #1 source discipline | text rule | Every batch's verification_note records actual probe URLs, HTTP codes, byte sizes, body-token matches. Where probes failed, all attempted URLs are listed with their outcomes. Honest eligibility-delta accounting recorded in DR amendments rather than papered over. |
| #2 best-practice-synthesis-routing | text rule | Not fired — no synthesis content authored. |
| #3 structural change | text rule + Change Order | Not fired — no TOC/item-code/cross-reference changes. CI workflow file edit (`ba6d11e`) is mechanical-script-change scope, not structural. |
| #4 research-log discipline | text rule | Retroactive search-log stubs for economics-sources and government-grant-programmes (`5b1dc42`) restore rule-#4 audit-trail parity for 2 BPCs that predated the rule's enforcement. |
| #5 connector posture | text rule | No MCP connectors used. |
| #6 canonical workplan | text rule | Session is operating under BPC-rewrite-workplan-2026-05-11 §V2-verification track — manual verification fits into Phase B-verification of the workplan even though the DR is independent. |
| #7 adversarial-research | scripts/audit/research_protocol_audit.py | Not fired — no gap closures. |
| #8 progressive-measurement | scripts/audit/pmp_audit.py | Not fired — no numerical specification writes. |
| #9 9-step synthesis | scripts/validate_reasoning.py | Not fired — no reasoning-doc authoring. |
| #10 evidence-verification | scripts/audit_evidence_metadata.py | DR-2026-05-19 entire purpose is to move sources from NULL to VERIFIED/UNVERIFIED-1 (existence gate) under the rule. +15 to eligible pool. |
| #11 adherence-logging | scripts/audit/adherence_log_audit.py | 6 attestation file states (initial 3 + 3 amendments). check_0_presence interaction documented above (drift 2). |

---

## Known broken / pending work

### Owner-purchase queue (18 rows)
Standards behind commercial paywalls; owner action required to close DR §6 step 5 (third skill-promotion gate).

By publisher:
- **NEN** (Dutch commercial): NEN 9120:2025 — REF-00071, REF-00433, REF-00466 (3 rows)
- **ABNT** (Brazilian commercial): NBR 9050:2020 — REF-00077, REF-00208, REF-00414, REF-00435, REF-00456 (5 rows)
- **JSA** (Japanese commercial): JIS T 9251:2006 — REF-00017 (1 row)
- **BSI/DIN/ISO** (European commercial): BS EN ISO 10535:2021 — REF-00116 (1 row)
- **ANSI/ASA** (American commercial): S12.60-2010 etc. — REF-00326, REF-00335, REF-00563, REF-00604 (4 rows)
- **IEC** (international commercial): TR 63079:2017 — REF-00334 (1 row)
- **IES** (American commercial): RP-46-23 — REF-00559 (1 row)
- **CIE** (international commercial): TN 015:2023 — REF-00560 (1 row)
- **SBi/AAU** (Danish, historically commercial): SBi-anvisning 218 — REF-00575 (1 row)

Most likely first purchase: NEN 9120:2025 (Dutch covered in 19-language coverage; smallest publisher to engage with).

### Owner-different-IP queue (2 rows)
EN sources behind Cloudflare/bot blocks. Owner can probably fetch from residential IP and forward content/URL.

- REF-00074 — Singapore BCA Code on Accessibility 2025 (bca.gov.sg 403)
- REF-00491 — ASPECTSS 2.0 Mostafa (archnet.org 429, dcu.ie 404, emerald 403)

### V2-automated scraper priority queue (19 rows)
Awaits per-body scrapers; no manual action available. By target portal:

- **MLIT JP** (`mlit.go.jp`): 4 rows
- **MEXT JA** (`mext.go.jp`): 1 row
- **openstd / MOHURD CN** (`openstd.samr.gov.cn`, `mohurd.gov.cn`): 6 rows
- **Boverket SE** (`boverket.se`): 5 rows
- **NL/JP/SE/INT misc**: 3 rows

### DR §6 step 5 promotion-to-skill gate

| Requirement | Status |
|---|---|
| ≥3 jurisdictions validated | ✓ (13: AU, NO, US, NZ, CN, JP, NL, BR, JA, SE, CA, SG, INT, DA) |
| Reproducibility under different session conditions | ✓ (6 batches, 3 routing mechanics introduced incrementally, persistence-compaction-survived) |
| ≥1 IS-PAYWALL purchase cycle closed | ✗ (queue established; no end-to-end cycle demonstrated) |

Skill promotion blocked on the third requirement. Owner action: complete one purchase and re-verify (likely NEN candidate) before authoring `skills/manual-statutory-verification_SKILL.md` and the corresponding level-2 audit script.

### `scripts/migrate_db.py` runner bug (pre-session)
12 historical data migrations were recorded in `data_migrations` with custom `migration_id` values (not matching filename stem). On `--rebuild`, the runner INSERTs with filename-stem ID, which collides with the historical custom-ID rows for the same SQL. This blocks full historical rebuild from scratch but does NOT block CI's invariant comparison (it only checks counts, which match). Out of scope for this session. Architecturally suggests rewriting historical migrations to remove their custom-ID INSERT and let the runner manage all data_migrations rows — but this is forward-only data, so a compensating migration would be the right move when prioritized.

---

## Next-action handoff

1. **Owner**: pick one IS-PAYWALL row and complete purchase → re-verify → close DR §6 step 5 third requirement → promote protocol to `skills/manual-statutory-verification_SKILL.md`.
2. **PI v10.14 candidate**: combine (a) doctrine-token-position note, (b) `/661` → `/670` numerator update, (c) bootstrap header grep update. Single micro-patch.
3. **NULL queue scope**: 203 NULL-verification rows remain but all are now OUT of V2-manual scope (their metadata_quality is AUTHOR-TITLE-ONLY, GREY, or COMPLETE-but-not-statutory — different verification tracks). The V2-manual queue specifically is drained.
4. **V2-automated scrapers**: the DEFERRED-V2-AUTOMATED queue (19 rows) now has a sufficient size and target-portal diversity to inform scraper-priority sequencing. By-portal counts above.

session_close marker: this session ends here. Next session bootstrap should fetch `sessions/LATEST` → `session_2026-05-19-deployment-state-reconciliation.md` and resume from one of the four next-action items.
