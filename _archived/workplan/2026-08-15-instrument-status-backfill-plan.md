# `jurisdictional_values` — instrument-status backfill plan (Q6 / A5 item 15)

**Status:** PROPOSAL. Nothing here is executed. The schema change is **D-SCHEMA, Change-Order gated**;
the classification policy in §4 is an owner call. Authority for the *dimension* itself is
ratification item A5 item 15 + DR-2026-07-13 H5(a), ratified 2026-07-13 and unimplemented since.

**Verified against the live DB 2026-08-15** — every number below is a query result, not a carried figure.

---

## 1. The problem, in the data

`jurisdictional_values`: **109 rows**, 20 distinct `item_code`, 12 jurisdictions
(DE 20 · GB 20 · US 20 · AU 18 · ISO 13 · FR 5 · NO 5 · EU 4 · CA/CH/JP/SG 1 each).

| Defect | Verified state |
|---|---|
| **D1 — no instrument dimension** | No `instrument_status` column exists. Nothing downstream can distinguish "the law requires X" from "a voluntary standard recommends X". |
| **D2 — `is_code_minimum` is empty** | `NULL` on **all 109 rows**. The ratification package described these rows as `is_code_minimum=1`; that was never true of the committed data. The one field that gestured at this dimension carries no signal at all. |
| **D3 — tier misgrade** | `evidence_tier = 6` on **all 109 rows** — a single value, so the column carries zero information. Tier 6 is *statutory codes*; but the set includes ISO 21542 (×9), BS 8300, DIN 18040, EN 81-70, AS/NZS, CSA B651, ANSI, IEC — which are **T4 international standards** under `tier-system.md`, not statutory codes. |
| **D4 — `jurisdiction` is unguarded, and has drifted two ways** | **(a)** 20 rows use **`GB`**; `schemas/enums.py JurisdictionCode` declares `UK = "UK"  # United Kingdom (project convention, not GB)` and the sibling `lang_jur_map` uses `UK`. Demonstrated: `jurisdictional_values JOIN lang_jur_map ON jurisdiction` matches **0 of the 20 GB rows** — the UK's code values are invisible to any jurisdiction-keyed join. **(b)** **`NZ` has 0 rows** despite being canonical and present in `lang_jur_map`, because the two joint AS/NZS standards that serve it are filed under `AU` (§4). Root cause of both: there is **no CHECK and no FK on `jurisdiction`** — the only FK is `item_code → items`. |

**D4 was not part of Q6 and is recorded here because it lives in the same table.** Fixing this table
twice would be worse than fixing it once; see §6.

## 2. Why D1 matters more than it looks

The project's whole posture is that code convergence is **not evidence** (`tier-system.md` §3/§8), and
that a regulatory-stratum claim may anchor best practice only at the flagged weak band. That
machinery assumes the regulatory stratum is one thing. It is not: a *statutory requirement* and a
*voluntary standard a designer may ignore* are different claims about the world, and the guidebook
currently renders both as "Tier 6". Every rendering surface carries a standing caveat because of it.

This is also a **symmetric-disclosure** problem (`project-standards.md` RULE 2026-07-25): the project
discounts code convergence loudly while its own code table cannot say what kind of instrument each
row is.

## 3. Proposed schema

One migration, additive, no data destroyed:

```sql
ALTER TABLE jurisdictional_values ADD COLUMN instrument_status TEXT
  CHECK (instrument_status IN (
    'statutory',              -- legally binding in this jurisdiction
    'statutory_referenced',   -- voluntary standard given legal force by reference from a code
    'voluntary_standard',     -- published standard, no legal force in this jurisdiction
    'guidance',               -- government/agency guidance, not a standard, not binding
    'unclassified'            -- not yet determined; the honest default
  ));
ALTER TABLE jurisdictional_values ADD COLUMN instrument_status_basis TEXT;
```

`instrument_status_basis` is **not optional decoration** — it is what stops this becoming folklore.
Every non-`unclassified` row records *why*, with a locator, in the same shape as the genealogy layer's
`root_classification_basis` (§4.5 of `evidence-architecture.md`).

**Deliberately not proposed:** rewriting `evidence_tier` in the same migration. See §5.

## 4. Classification method — and the line I will not cross unasked

Three bands, and the plan is explicit about which is which.

**Band A — mechanically defensible from the instrument's own identity (no jurisdiction research).**
An ISO/IEC/EN/DIN/AS-NZS/CSA/ANSI/BS number *is* a published voluntary standard by definition; that
is a fact about the document, not about any jurisdiction. These become `voluntary_standard` unless
Band B moves them. Similarly, ADA 2010, the NCC/BCA, TEK17, the French *Arrêté*, and Building
Regulations are statutory instruments by their own nature → `statutory`.

**Band B — requires per-jurisdiction legal knowledge, and is where errors would be invisible.**
Whether a voluntary standard is *referenced into force* is jurisdiction-specific and changes over
time: BS 8300 is cited by Approved Document M without being the law; DIN 18040 is an *eingeführte
technische Baubestimmung* in most but not all German Länder; EN 81-70 reaches force through national
adoption. Getting these wrong produces a page that tells a disabled reader the law requires something
it does not — the exact harm the non-authority posture exists to prevent.

**Band C — the honest residue.** Anything not settled by A or B stays `unclassified`. An
`unclassified` row is visible; a wrong one is not.

**My recommendation, and it is a recommendation:** execute Band A mechanically, leave Band B and C as
`unclassified`, and open a gap row per Band-B family so the debt is queryable rather than remembered.
That yields a column that is *true everywhere it speaks* on day one. The alternative — classifying
Band B now — is more useful and less honest, and it is not a call an implementer should make alone.

**Rows that must not be silently "improved":** **all 22 rows** whose `standard_name` joins two entities
in one string. **No organisation has a `/` in its name** — the delimiter always separates two things,
and the row cannot be classified until it is split. Two distinct decompositions are needed:

- **Instrument compounds (19)** — "BS 8300-2:2018 / Part M", "TEK17 / EN 81-70", "ADA / A117.1",
  "DIN 18040 / DVGW W 551", "DIN 18040 + DIN EN 81-41", "IBC 2024 / A117.1", "NFPA 72 / ADA §702" …
  Each pairs instruments of **different** status — typically a voluntary standard beside the code that
  references it — which is exactly the distinction `instrument_status` exists to record. Split into
  one row per instrument, same jurisdiction.
- **Joint-publication compounds (3)** — these are *not* single-organisation names:
  - `AS/NZS 2107:2016` and `AS/NZS 1428.4.1:2009` are **joint Australian/New Zealand standards**
    (Standards Australia **and** Standards New Zealand). Both are currently filed under `AU` alone.
    They split **by jurisdiction** → an `AU` row and an **`NZ`** row.
  - `ANSI/ASA S12.60-2010` names **two US bodies** (ANSI and **ASA**), one jurisdiction. It splits by
    publisher, not jurisdiction.

> **Correction, recorded because I nearly shipped the opposite instruction.** This paragraph first
> called those three rows *false positives* — asserting the slash sat "inside the publisher's name" —
> and warned an executor not to split them. That was wrong, and wrong in the worst direction: a
> warning that would have **prevented** correct work, written into a plan on pattern-matching
> intuition rather than a check. Corrected by the owner, 2026-08-15. The general lesson is the one
> this repo keeps re-learning: I asserted a distinction I had not verified, in a document whose whole
> premise is that every figure must be derived.

**A consequence worth stating on its own: `NZ` is a canonical jurisdiction with zero rows.**
`JurisdictionCode` declares `NZ`, `lang_jur_map` carries it, and `jurisdictional_values` has **0 NZ
rows** — because the two AS/NZS standards that serve New Zealand are filed under `AU`. So the table
does not merely mis-split a string; it renders one of the project's own jurisdictions invisible. This
sits alongside D4 (the `GB`/`UK` drift) as the same class of defect: `jurisdiction` is unguarded, and
what is unguarded has drifted.

## 5. The tier question is a separate decision, deliberately

D3 (every row at `evidence_tier=6`) is real, but correcting it means **moving evidence tiers on 109
rows**, which changes what the engine may anchor and at which strength band. That is a doctrine-
adjacent D-SCHEMA change with its own Change Order, and it should not ride along inside a backfill.

The sequencing that keeps both honest: land `instrument_status` first, populate Band A, **then** ask
whether `evidence_tier` should be re-derived *from* instrument status plus publisher class — at which
point the re-grading has a recorded basis per row instead of being a bulk `UPDATE`.

## 6. Sequencing, and the collision to avoid

`workplan/2026-08-14-remediation-workplan.md` §1 allocates migrations 058–066; 058–060 are used.
**This work should be batched with the Group 3 owner-decision round, not run beside it.** Group 3
already opens `specifications` (061/062); Q5's ratified H2 columns belong there too (raised in the
2026-08-15 register reconciliation). Opening `jurisdictional_values` in the same round means the
table is touched once for D1, D4 and the compound-name split, rather than three times.

**Blocked on owner input:** the Band-B policy (§4), the tier question (§5), the migration number, and
whether D4's `GB → UK` normalisation rides here or gets its own compensating migration.

## 7. Acceptance tests, written before the work

1. `instrument_status` CHECK refuses an invalid value on a scratch rebuild (shown firing, per
   `evidence-architecture.md` §10 — a check that has not been shown to fail proves nothing).
2. Every row with `instrument_status != 'unclassified'` has a non-empty `instrument_status_basis`.
3. Count of `unclassified` is **reported, not minimised** — the plan succeeds by being true, not by
   being complete.
4. `migrate_db.py --rebuild` reproduces the committed DB, shallow **and** `--deep`.
5. After D4(a): `jurisdictional_values JOIN lang_jur_map ON jurisdiction` matches the UK rows (0 → 20).
6. After D4(b) + the §4 joint-standard split: `NZ` has non-zero rows, and no canonical
   `JurisdictionCode` used by the table is absent from `lang_jur_map`.
7. A CHECK or FK now guards `jurisdiction`, shown refusing an out-of-enum value on a scratch
   rebuild — without it, D4 recurs the next time anyone writes this table.
8. `test_db_integrity` no worse than baseline; no new blocking failure.
