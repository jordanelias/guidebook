# Evidentiary-audit remediation — Batch A (WS0, data-hygiene prep)

*Executes Batch A of `workplan/evidentiary-base-research-plan-2026-07-19.md`, the plan derived from
`audits/evidentiary-base-audit.md` (data as of 2026-07-19). WS0 = the fast, no-new-research data-hygiene
pass that resets an honest measurement baseline before any sourcing work. 2026-07-19.*

---

## What this batch changed

**Migration:** `scripts/migrations/data_20260719231100_2026-07-19-evidentiary-audit-ws0-jurisdiction-hygiene.sql`
(applied; `data_migrations` 208 → 209; `PRAGMA foreign_key_check` / `integrity_check` clean).

Moved the **4 mis-filed language codes** out of `evidence_sources.jurisdiction` into their true
jurisdiction — audit finding 6 / §3.3. Every value was recovered from the row's **own** `publisher` /
`standard_number` metadata; no new research, no fabrication surface:

| ref_id | was `jurisdiction` | → | why |
|---|---|---|---|
| REF-00195 | `ZH` | **CN** | GB/T 建标156-2011, PRC MoE/MOHURD/NDRC national school standard (lang already `zh`, batch 8) |
| REF-00196 | `ZH` | **CN** | Beijing Special Education School Guidelines, PRC ministries (lang already `zh`, batch 8) |
| REF-00197 | `ZH` | **CN** | DB3303/T 084-2025, **Zhejiang provincial** standard; also `lang_detected` `en`→`zh` |
| REF-00575 | `DA` | **DK** | SBi-anvisning 218, Danish Building Research Institute (build.dk); also `lang_detected` `en`→`da` |

For REF-00197/00575 the leaked `jurisdiction` value *was* the true source language, so `lang_detected` is
corrected in the same step. This finishes what batch 8 started (batch 8 fixed the `zh` language mislabel on
REF-00195/196 but left `ZH` sitting in the jurisdiction column).

**Verification (regenerated, not asserted):** re-running `python3 tools/evidentiary_audit.py` now reports
**0 language codes mis-filed in the jurisdiction column** (was `DA`×1 + `ZH`×3 = 4). Finding 6 is resolved.
One slice moved **E→D** (grades A6·B17·C19·D15·E12·F13 → A6·B17·C19·D16·E11·F13) — the honest effect of the
previously-excluded mis-filed codes now counting as real CN/DK true-jurisdictions in the breadth component.
`DE`/`ES`/`FR` remain (correctly) — those are the **countries** Germany/Spain/France, not language codes;
the audit only ever flagged `DA`/`ZH` because those two language codes map to different country codes
(`DK`/`CN`).

## What this batch deliberately did NOT change (carefulness > completeness)

The plan's WS0 also names two other data-hygiene items. On inspection, the honest action for both is *not* a
blind mutation:

- **18–19 NULL-jurisdiction instances — confirmed intentional, left NULL.** Read row-by-row, these are
  almost entirely **trans-national primary research** (journal articles: *Lymphatic Research & Biology*,
  *OTJR*, AOTA Press, Frontiers, Wiley, *Rheumatology International*, *Health & Place*, …) with no single
  national home. Backfilling a jurisdiction onto a clinical study would **misrepresent** it. The audit itself
  treats these as legitimately excluded from jurisdiction denominators (§3.5). No migration; determination
  recorded here.
- **24 orphan sources (linked to no active slug) — inventoried, deferred to the slice batches.** Linking an
  orphan to a slug is evidence-*curation* (which claim does it back?), not mechanical hygiene, and several
  carry a `REF-VERIFIED-*` prefix suggesting a deliberate verified-source set. Rather than bulk-link blind,
  each is routed into the WS1/WS2 batch for the slug it naturally supports. Inventory below.

### Orphan inventory (24) — route into the relevant slice batch

- **School acoustics (ANSI/ASA S12.60):** REF-00326, REF-00335, REF-00604 → `deaf-classroom-reverberation-time` / `room-acoustic-performance`
- **Assistive listening (IEC 60118-4, ISO 23599, Auracast):** REF-VERIFIED-005, REF-VERIFIED-006, REF-VERIFIED-008 → `assistive-listening-systems` / `deaf-*`
- **Wheelchair biomechanics/propulsion:** REF-VERIFIED-003, REF-VERIFIED-002 → `stair-ramp-threshold-biomechanics-accessibility` / `mobility-built-environment`
- **Thermal/MS sensitivity:** REF-VERIFIED-010, REF-VERIFIED-012 → `ms-thermal-temperature-conflict-resolution` / `thermoregulation-built-environment`
- **Neurodiversity design (PAS 6463):** REF-00094 → `neurodivergent-built-environment` / sensory slices
- **Economics (cost of accessible buildings / extra costs of disability):** REF-VERIFIED-001, REF-00734 → `accessible-design-economics-cost-premium` / `case-study-economics-financial-data`
- **Dementia/psychiatric/aging-in-place clinical:** REF-00729, REF-00730, REF-00731, REF-00735, REF-00728, REF-00571, REF-00732 → respective population/health slices
- **RA disability assessment / speech reception:** REF-VERIFIED-004, REF-VERIFIED-009, REF-VERIFIED-011 → `upper-limb-impairment-*` / `deaf-acoustic-*`

## Next

Batch B–D (WS1 †): anchor the 9 supporting-only slices — highest ROI, since they already hold confirmed
T3-clinical evidence and need only a T1/Co-1/T2/Co-2 anchor. Consult
`working/evidence-migration/slug-language-tracking-matrix.md` first, and confirm retrieval-tool
reachability (`curl "$HTTPS_PROXY/__agentproxy/status"`) before any sourcing batch.
