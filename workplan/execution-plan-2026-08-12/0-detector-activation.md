# Wave 0 — Activate the detector that already works

**Read `00-holistic-execution-plan.md` first.** **Precondition: L1 exists.**

**Three items, minutes each.** Every other wave needs code or a decision. This needs a registry
entry for a script that already works and already knows about wrong rows — after one line of it
is fixed.

**Owner gates: none.** All three are session-executable once L1 exists.

**Ordering inside the wave: W0.3 → W0.1 → W0.2. Not W0.1 first.** Wiring a detector whose row
filter is anti-correlated with its own defect class produces a green that means nothing.

---

## W0.3 — Unblind the detector before trusting its all-clear

### Objective
Add a sixth finding class, `numeric_without_unit`, so the detector can see the eight rows its
current row filter excludes by construction.

### The defect, re-derived at `fd4c09d`

`scripts/audit/jurisdictional_divergence.py:66-73`, the `_rows()` helper:

```python
def _rows(conn):
    return conn.execute(
        "SELECT item_code, jurisdiction, unit, value_numeric, is_code_minimum, "
        "       COALESCE(standard_name,'') AS standard_name, evidence_tier "
        "FROM jurisdictional_values "
        "WHERE value_numeric IS NOT NULL AND unit IS NOT NULL AND jurisdiction IS NOT NULL "
        "ORDER BY item_code, unit, jurisdiction"
    ).fetchall()
```

The `WHERE` clause is at **`:70`** (the plan cites `:69`; corrected). **Every row with a
numeric and no unit is excluded from every finding class** — and the extractor failure that
manufactures class ordinals, years and edition numbers is precisely the failure that leaves
`unit` NULL. The filter is anti-correlated with the defect class the script exists to catch.

**Proof at HEAD.** Run unmodified, the detector exits `0` and surfaces 26 findings — and
**neither `E-07` nor `E-15` appears anywhere in its output**, although between them they hold
four of the repository's worst values.

### Correction to the resolution plan

W0.1's falsifier reads *"its output appears in CI and names no defect."* **That is far too
weak and would mislead the session that ran it.** At HEAD the detector names:

| Class | Count | Verdict | Named |
|---|---|---|---|
| `within_jurisdiction_divergence` | 2 | WARN | E-06/DE (10 vs 20 mm), G-04/DE (4.7 vs 5.3 m²) |
| `candidate_conflation_or_error` | 3 | WARN | B-10 (2.0–54.0 Hz, ×27), E-12 (81.0–1400.0 mm, ×17), G-04 (4.2–1500.0 m², ×357) |
| `cross_jurisdiction_divergence` | 9 | INFO | D-08, E-01, E-03, E-06, E-08, H-01, I-01, I-02, I-03 |
| `unadjudicated_divergence` | 12 | WARN | all diverging items — "no `specifications` determination exists to adjudicate (judgment stage unbuilt)" |
| `convergence_not_evidence` | 0 | INFO | — |

**The true statement is: it names 26 findings and cannot name the 8 that matter most.**

### The eight invisible rows — and the distinction the plan does not draw

**This is the most important correction in Wave 0.** The eight NULL-unit rows are **not one
class**. Four are genuine dimensionless quantities that are correct as they stand:

| jv | item / juris | numeric | source text | verdict |
|---|---|---|---|---|
| 14 | E-07 / US | 0.42 | `Threshold: ≥0.42` (ANSI A326.3) | **CORRECT** — DCOF is dimensionless |
| 15 | E-07 / GB | 36.0 | `PTV ≥36 wet` (BS 7976-2/HSE) | **CORRECT** — PTV is dimensionless |
| 96 | A-10 / US | 50.0 | `≥50 occupants` (ADA §219) | **CORRECT** — a count threshold |
| 100 | A-10 / FR | 50.0 | `≥50 seats` (Arrêté 2017) | **CORRECT** — a count threshold |
| 16 | E-07 / DE | 9.0 | `R9–R13` (DIN 51130) | **DEFECT** — a slip-class ordinal |
| 17 | E-07 / AU | 3.0 | `P3–P5` (AS 4586:2013) | **DEFECT** — a slip-class ordinal |
| 106 | E-15 / GB | 2021.0 | `Building Regs 2021` | **DEFECT** — a year; the row's real quantity is `Min Area: ≥12m²` |
| 107 | E-15 / US | 1.0 | `Supplement 1 (2024)` | **DEFECT** — an edition ordinal |

**A blanket "numeric without unit is a defect" rule would corrupt four correct rows.** The new
finding class must therefore *list and require adjudication*, not assert a defect.

### The second blind spot, which this item does NOT close

Wave 5's whole-table sweep found a **ninth** false value that `numeric_without_unit` will not
catch either: **`jv 52` — E-03 / NO, `1.0 ratio`, extracted from the "1" in "1:12"**, where
sibling rows encode the same gradient as `8.3`.

It evades both blind spots at once: it **has** a unit, and its in-item spread (1.0–8.3 = ×8.3)
falls **below the ×10 conflation threshold at `jurisdictional_divergence.py:141`**, so it
surfaces only as INFO-level "legitimate jurisdictional divergence."

**State this limit in the finding class's own rubric.** After W0.3 the detector still cannot see
a false value that carries a unit and sits inside a plausible spread. Closing that would need a
`value_text`-vs-`value_numeric` consistency check, which is a different and larger tool — do not
build it here, and do not let the post-W0.3 all-clear be read as "the table is clean."

### Ordered steps

1. Write the ledger entry (`plan_item: W0.3`) before editing.
2. Add a second row-fetch helper beside `_rows()` — **do not widen `_rows()` itself**, which
   would silently feed unitless numerics into the divergence-spread arithmetic and manufacture
   nonsense spreads:
   ```python
   def _unitless_rows(conn):
       return conn.execute(
           "SELECT jv_id, item_code, jurisdiction, value_numeric, "
           "       COALESCE(standard_name,'') AS standard_name, "
           "       COALESCE(value_text,'')    AS value_text "
           "FROM jurisdictional_values "
           "WHERE value_numeric IS NOT NULL AND unit IS NULL "
           "ORDER BY item_code, jurisdiction"
       ).fetchall()
   ```
3. Add the finding class `numeric_without_unit`, emitted at **WARN**, one line per row, printing
   `jv_id`, `item_code`, `jurisdiction`, `value_numeric`, `standard_name` and a truncated
   `value_text`, with the fixed rubric: *"a numeric with no unit is either a dimensionless
   quantity (correct) or an ordinal/year/edition captured by the extractor (defect) — adjudicate
   against `value_text`."*
4. Add its count to the `SURFACED:` summary line.
5. Print an `EXAMINED: <n>` count for the class — per the repository's own named failure mode, a
   gate reporting zero must be able to prove it had a subject.

### Verification
`python3 scripts/audit/jurisdictional_divergence.py` must now print
`[numeric_without_unit] 8 (WARN)` naming jv 14, 15, 16, 17, 96, 100, 106, 107, and
`EXAMINED: 8`. After W5.1 lands, the count falls to **4** (the four correct dimensionless rows
remain listed; the four defects are corrected to NULL or to their real figure).

### Falsifier
If the detector at HEAD already names E-07 or E-15, the blind spot does not exist and this item
does not execute. *(Checked: it does not name them.)*

### Risks
Widening `_rows()` instead of adding `_unitless_rows()` would inject unitless numerics into the
`×N range` arithmetic — the exact class of error the detector exists to report.

---

## W0.1 — Wire the detector into the registry at `informational`

### Objective
Move `jurisdictional_divergence` from the quarantine list into `checks:` at the level that
already exists for a check whose exit code carries no verdict.

### Preconditions
**W0.3 must land first.** L1 must exist.

### The quarantine entry is honest — and that is the point

At `governance/check-registry.yaml:1304-1310`:

```yaml
  - id: jurisdictional_divergence
    cmd: [python3, scripts/audit/jurisdictional_divergence.py]
    status: quarantined
    reason: >-
      Green, but it is a SURFACING tool ("SURFACED: 2 candidate contradictions"),
      not a pass/fail gate. Its exit code carries no verdict. Belongs in a report,
      not a gate.
```

**The reasoning is correct and was never the problem. "Not a gate" was simply read as "not
run."** The registry has a level for exactly this — `informational` — and 2 of the 65 active
checks already use it.

Note also: the quarantine reason quotes `"SURFACED: 2 candidate contradictions"`, which is
**stale** — the current output line reads `SURFACED: 2 within-jurisdiction candidate
contradiction(s), 3 candidate conflation/error(s), 9 cross-jurisdiction divergence(s), 12
unadjudicated`. Do not carry the quotation forward.

### The §6.5 collision, resolved
`references/tooling-register.md` §6 item 5 makes quarantine terminal **for retirement**, not for
activation. De-quarantine to active is an established move performed five times, recorded in the
registry's own comments. The precedent's exact form is at `check-registry.yaml:1312-1313`:

```yaml
  # validate_pydantic_schemas was de-quarantined 2026-08-01 with --strict; it is
  # now an active advisory check in the schema battery above.
```

### Ordered steps

1. Ledger entry (`plan_item: W0.1`), written first.
2. **Delete** `check-registry.yaml:1304-1310` (the seven-line quarantine entry).
3. **Insert in its place** a comment in the established form:
   ```yaml
   # jurisdictional_divergence was de-quarantined 2026-08-12 at informational; its
   # exit code still carries no verdict, which is what informational means. Its
   # NULL-unit blind spot was fixed first (W0.3). It is now an active check in the
   # data battery above.
   ```
   The comment is required, not decorative: `run_checks.py --selftest` C1b fails an id present
   in both `checks:` and `quarantine:`, so the entry cannot simply be moved.
4. **Add to `checks:`**, in the `data` battery, matching the house entry shape exactly:
   ```yaml
     - id: jurisdictional_divergence
       cmd: [python3, scripts/audit/jurisdictional_divergence.py]
       battery: data
       kinds: [data]
       level: informational
       basis: unattributed
       cost: fast
   ```
5. Note in the entry's `note:` that its verdict is advisory-by-construction and that
   `EXAMINED:` counts are its real output.

### Verification
- `python3 scripts/run_checks.py --selftest` → exits 0 (C1b would fail on a double-listed id).
- `python3 scripts/run_checks.py --list` → shows `jurisdictional_divergence` as active,
  quarantine membership drops **16 → 15** (15 `quarantined` + 1 `vacuous` → 14 + 1).
- `python3 scripts/run_checks.py --kinds data --battery data` → runs it and reports its findings
  without failing the run.

### Falsifier
If `informational` results were found to fail a run, the level is wrong and the item stops.
*(Checked: `run_checks.py` exits non-zero only when a `blocking` check fails.)*

### Sequencing note
W7.10 must be re-derived after this lands — quarantine membership changes from 16 entries to 15.

---

## W0.2 — File the rows the detector names as W5.1 defects

### Objective
Route the detector's output into the corpus-defect wave rather than leaving it as console text.

### Ordered steps
1. Ledger entry (`plan_item: W0.2`).
2. Take the detector's `candidate_conflation_or_error` rows (B-10, E-12, G-04) and W0.3's
   `numeric_without_unit` defects (jv16, jv17, jv106, jv107) and confirm each against
   `5-corpus-defects.md`'s enumeration.
3. **File nothing new.** W5.1 already carries all eight. This item is a reconciliation: if the
   detector names a row W5.1 does not, W5.1's enumeration was incomplete and must be extended
   before it ships.

### Verification
The detector's defect-bearing output is a subset of W5.1's enumerated rows. Any row in the
former and not the latter is a finding.

### Falsifier
If the detector names no row outside W5.1's list and W5.1's list is complete, this item is a
no-op — record that in the ledger and close it.

---

## Re-derivation notes

| Plan claim | Status | Evidence |
|---|---|---|
| Detector prints `[candidate_conflation_or_error] 3 (WARN)` naming B-10, E-12, G-04, exits 0 | **CONFIRMED** | ran at `fd4c09d` |
| "Its output appears in CI and names no defect" (W0.1 falsifier) | **REVISED** | it names 26 findings; the correct claim is that it cannot name the 8 that matter |
| Row filter at `:69` | **CORRECTED** | `_rows()` spans `:66-73`; the `WHERE` is at `:70` |
| 8 NULL-unit rows today, 4 after W5.1 | **CONFIRMED** on count | but see next row |
| The 8 are one defect class | **REFUTED** | 4 are genuine dimensionless quantities (jv14, 15, 96, 100); only 4 are defects |
| G-04 headline is ×357 | **CONFIRMED** | vs E-15's in-item spread, invisible to the detector |
| `test_jurisdictional_divergence` is registered, active, advisory | **CONFIRMED** | `check-registry.yaml:931-937`, `tests` battery |
| Quarantine list holds 16 entries | **CONFIRMED** | 15 `quarantined` + 1 `vacuous` |
| De-quarantine is an established move | **CONFIRMED** | precedent comment at `:1312-1313` |
