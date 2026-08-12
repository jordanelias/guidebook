# 2026-08-12 — Resolution plan for everything the trials, the sweep and the audits found

**Status:** PROPOSED. Nothing below is executed. Three items are marked DONE because the sessions
that found them fixed them while fixing their own defects; everything else is a proposal with a
gate.
**Provenance.** Rewrite in place of the plan authored in PR #93 (merged `bc81070`), retaining its
wave structure and its sequencing rule. Rewritten in place again at revision 5.
**Revision 5** (this one) changes the plan's *shape*, not most of its content. Revisions 1–4
argued about which items are true. Revision 5 asks a different question — **what kind of
mechanism can carry each item** — and the answer reorders everything: the majority of this plan's
invariants are currently defended by *checks that run after a write*, and most of them can be
defended by *constraints that make the write impossible*. Parts I–VII are new. Waves L and H and
0–9 are retained below, each with a disposition (Part VII), because they remain the evidence
base and the loss-audit obligation (W6.9) forbids dropping them.
**Subject:** `fd4c09d` (the PR #95 merge). **Doctrine SHA:** `0f2f525`.

> **The finding that governs revision 5.** The repository's compliance model is *detect-then-
> report*: 65 registered checks, 28 blocking, run after the fact against a database that has
> **zero triggers** and whose sanctioned write path **turns foreign keys off** (`migrate_db.py:161`),
> **commits before it checks** (`:171` precedes `:174`), **rolls back nothing** in its own
> `except` (`:183-184`), and **disables enforcement on a prose substring** (`:176`, duplicated at
> `:261`). Every failure this plan catalogues is a failure of that model: the detector that was
> blind to its own defect class (W0.3), the check that examined nothing four separate times, the
> attestation corpus validated by nothing, the item names that state answers the pipeline never
> derived. **A constraint cannot be blind to what it forbids; a detector can.** Revision 5's
> central move is to migrate every invariant that is expressible in DDL out of the check layer
> and into the row — and to do it in the window the clean-room reset opened, because SQLite has
> no `ADD CONSTRAINT` and 39 of 67 tables are empty *today*.

> **The finding that governed revision 4, retained.** Revisions 1–3 each corrected their
> predecessor's *arithmetic* while inheriting its *facts*. Revision 4 re-ran the facts: `main` is
> **already branch-protected**, `test_db_integrity` is **70/70 green**, the attestation defect
> W5.4 describes was fixed by an ancestor of revision 3's own declared subject, and the
> write-path fix W1.1 specifies **cannot work** because migration bodies commit themselves.
> Thirty-one claims did not survive. That method is now a standing rule (W6.11), and revision 5
> applied it to revision 4 — see Appendix E, where **four more claims did not survive, two of
> them in recommendations this revision was drafted to adopt.**

---

## 0.0 Method of revision 5, and its four corrections

Revision 5 was derived by two independent read-only reasoning passes over the same repository at
`fd4c09d` — one asking *what makes an untraceable row impossible to write*, one asking *what is
the critical path and what should be cut* — followed by a verification pass that re-ran every
load-bearing claim either pass produced. **Four did not survive, and two of them were headline
recommendations:**

| # | Claim | Verdict at HEAD |
|---|---|---|
| **AE-1** | *"Add `CHECK (value_numeric IS NULL OR unit IS NOT NULL)` to `jurisdictional_values` — one line kills the W5.1 defect class at the write."* | **REFUTED, and it would destroy live data.** Eight rows are numeric-with-NULL-unit, and **four of them are legitimate**: `jv 14` E-07/US `0.42` (wet DCOF), `jv 15` E-07/GB `36.0` (PTV), `jv 96` A-10/US and `jv 100` A-10/FR `50.0` (occupant trigger counts). DCOF and PTV are **dimensionless indices**; the constraint as proposed forbids the correct rows along with the garbage. Corrected specification at Part I §I.4 — the invariant is *numeric implies a declared quantity kind*, not *numeric implies a unit*, and it requires a backfill migration before it can be added. |
| **AE-2** | *"The 109 `jurisdictional_values` rows already show `UK`(88)/`GB`(5)/`GB-SCT`(1) drift."* | **REFUTED as stated; the underlying finding is real and stronger.** `jurisdictional_values` contains **zero** `UK` rows (it uses `GB`, 20). The drift is **cross-table**: `UK` appears 1× in `lang_jur_map` and 7× in `term_aliases` while `jurisdictional_values` uses `GB`. Three tables hold `jurisdiction` as free text with **52 distinct values** across them (12 / 48 / 17, partial overlap), no canonical table, `ISO` and `EU` — standards bodies, not jurisdictions — in the same column, and the literal string **`colloquial`** sitting in `term_aliases.jurisdiction`. W9.2 is upgraded from *ratified-but-omitted* to *now-or-never*. |
| **AE-3** | *"Only 14 of 65 checks declare `min_items`."* | **REFUTED — it is 6 of 65.** The vacuity guard covers **9%** of the register, not 22%. The argument for inverting the default (Part III) is correspondingly stronger, not weaker. |
| **AE-4** | *"The stage-7 hole is a false premise — the migration path is the universal writer, so nine of the fourteen unwritable outputs need no code."* | **UPHELD IN PART, and it is the single most useful structural claim in either pass.** The migration path *is* a writer for any table. But it is the write path this plan's Wave 1 exists to fix, and `pipeline-contract.yaml` R12 instructs sessions to write tables no tool serves — so the reframing is only safe *after* Part II lands. Adopted as sequenced: declare-then-serve, not build-nine-importers. See Part V M4. |

**Standing caveat, per W6.6 and W6.11.** The two passes were reasoning passes; their conclusions
are candidate findings until run. Every figure in Parts I–VII was re-derived by this revision
against `fd4c09d` by executing the command beside it. Re-derive again before acting.

---

## 0. The organising claim

Five statements, and the plan follows from their order:

1. **Hard-coding has entered the frame the reset preserved.** 28 of 93 item names carry
   determined numeric values; `evidence_cell_state` holds 0 determinations. The vocabulary states
   the answers the pipeline has not derived. **Owner ruling, 2026-08-11: this should not be the
   case; hard-coding undermines the entire project.** (§0.1, Wave H.)
2. **The write path is not safe to use** — and the fix everyone specified does not work. A
   foreign-key violation commits; a prose word disables enforcement; one failed migration voids
   every migration behind it; and reordering the FK check cannot undo any of it (W1.1).
3. **The pipeline determines a state, never a number.** Twelve stages carry evidence to a
   judgement about *how well evidenced* a cell is, then the value is written by hand. That may be
   correct — but it is undeclared, and every Wave 4 operation is downstream of ruling on it.
4. **Green does not mean examined.** The repository contains a working detector for a
   data-corruption class; it is quarantined; **CI runs the *test* of that detector and never the
   detector** (W0.1). And the detector is blind to half the class it exists to catch (W0.3).
5. **The hole is not diffuse — it is stage 7.** 14 tables are *unwritable outputs* — the pipeline
   reads them, no code can fill them — and **nine are in stage 7**, with stages 8 and 9
   inheriting the gap. Stages 1–5 work. **Evidence can be gathered and cannot become a value.**

**Sequencing rule, unchanged from PR #93:** fix the substrate, then rule on the boundary, then
build. Wave 3 writes rows, and rows are what make Wave 1 expensive.

**One rule added ahead of all of them (owner requirement, 2026-08-11):** *nothing executes
without a ledger entry written first.* Wave L. Every finding in this plan that was lost,
inherited, or silently reversed between generations was lost because the act that changed
something recorded the change and not its consequences.

**Four rules added by rewriting:**
- *Before building a detector, check whether one exists.* W0.1 and `db.py` are the same lesson.
- *Consolidation without a loss-audit is how findings die.* Every supersession lists what it
  dropped (W6.9).
- *A correction that does not propagate is not a correction.* (W6.10.)
- **New in revision 4:** *Re-derive facts, not only arithmetic.* A successor that recomputes its
  predecessor's sums while inheriting its observations inherits its errors with a clean audit
  trail (W6.11).

### 0.1 The owner ruling that reorders this plan

During revision 4's re-derivation the owner examined the `items` table and ruled:

> *"We aren't supposed to have any specifications/coded items like E-02."*
> *"This is bonkers and should not be the case."*
> *"Hard-coding undermines the entire project."*

**What was put to the owner, verbatim from the query:**

| | |
|---|---|
| item names containing a digit | **28 of 93** |
| item names carrying a prescriptive condition clause | **23 of 93** |
| `evidence_cell_state` rows (determinations) | **0** |
| `evidence_sources` rows | **0** |

Examples: `E-08 Corridor Clear Width (≥1200 mm Minimum on All Primary Routes)` ·
`E-07 Slip Resistance (PTV ≥36 Wet Throughout All Circulation and Entry)` ·
`E-01 Accessible Lift (1400×1100 mm Car, All Floors Served)` ·
`A-02 Acoustic Ceiling Panels (NRC ≥0.85) in Occupied Spaces` ·
`B-01 Circadian Lighting (≥150 EML Minimum at Eye Level in Daytime Spaces)` ·
`B-11 Warm Colour Temperature for Evening (≤2700 K After 19:00)` ·
`E-02 Platform Lift (Where Full Passenger Lift Not Achievable)`.

**Why this is a doctrine breach and not a naming preference.** Three separate grounds, each
independently sufficient:

1. **It exceeds what the reset authorised.** `DR-2026-08-06-clean-room-evidence-reset.md:25`
   grants the frame *"the design-parameter **categories** (`items`)."* "Corridor Clear Width" is
   a category. "≥1200 mm Minimum on All Primary Routes" is a determination. The DR's §1
   indictment — *"not one cell could [walk backwards to its evidence]"* — is reproduced inside
   the layer the reset preserved.
2. **The values contradict the evidence the repository actually holds.** E-08's recorded
   jurisdictional values are US 915 mm (ADA 2010 §403), AU 1000 mm (AS 1428.1:2021), GB 1200 mm,
   ISO 1200 mm, DE 1500 mm (DIN 18040-1), NO 1500 mm (TEK17 §12-6). The name asserts ≥1200 as
   *the* minimum, with **two jurisdictions below it and two above.** It adopts GB/ISO and
   promotes it to universal identity — the **T4–T6 regulatory-stratum wall breached at the
   vocabulary layer**, where `governance/tier-system.md` walls code convergence off from
   full-strength anchoring. E-07 is worse in kind: "PTV ≥36" adopts *Britain's metric*, under
   which the US (DCOF 0.42), German (R-class) and Australian (P-class) values are
   unrepresentable. E-04's "3600 mm Width" has **zero** jurisdictional values behind it.
3. **It contradicts the project's stated posture.** `CLAUDE.md` §1: a thinking tool, *"not a
   prescription manual."* `E-02 Platform Lift (Where Full Passenger Lift Not Achievable)` names a
   provision and a condition of use.

**And the fix is cheap, which is the one piece of good news.** `items.name` **is not a key.** All
14 inbound foreign keys target `item_code` (`case_study_specs`, `conflicts`,
`economics_entry_specs`, `evidence_cell_state`, `item_audit_runs`, `item_axis_links`,
`item_bpc_links`, `item_population_elaborations`, `item_population_links`,
`jurisdictional_values`, `room_items`, `source_value_extractions`, `spec_value_probes`,
`term_item_links`). This is **not** K3's FATAL 278-file rename. See Wave H.

### 0.3 Changes from the PR #93 original

Unchanged from revision 3. Retained: new Wave 0; W5.1 expanded and swept; W1.4's fix changed to
"import `db.py`'s function"; W3.2 contested and replaced; W5.4 widened; Wave 3 given a target
order; new Wave 7; net line/file accounting; D-B recorded as ratified-with-zero-presence.

**Ported here by W8.2 — the R↔W cross-map, the only Rosetta stone joining the two ID systems:**

| Register ID | Wave ID | Note |
|---|---|---|
| R-02 | **W1.1** | same finding; #93 added the fix spec — **which revision 4 refutes** |
| R-03 | **W1.2** | same; #93 added the `--allow-fk-violations` remedy |
| R-04 | **W1.3** | same; #93 added `--skip <id>` + "N not attempted" |
| R-01 / R-05 | W1 "also in this wave" / W7.1 | **R-05 recalibrated in revision 4 — see AC-16** |
| R-11 / R-12 / R-13 | W1 "also in this wave" | same |
| R-06 | **W5.1** | same row; #93 additionally called for the sweep |
| R-24 | **W5.4** | **both framings superseded — see AC-19** |
| R-17 | **W6.4** | same |
| R-17b | **W5.6** | **its owner gate was dropped in transit — see W9.1** |
| R-21 | **W5.7** | **now re-derived and CONFIRMED — see AC-22** |

### 0.4 Revision 2 — nine findings restored, four errors fixed

Restored: W1.5, W1.6, W5.6, D-C, W5.7, W5.8, W3.9, W6.8, W7.11. Arithmetic fixed: W7.3 −8→−6;
net 66→58; W5.1 "5 rows across 3 items"→6 across 4 (**now 8 across 5 — §0.7**); workplan lines
~34,000→31,189 (**now 31,338 — the figure went stale inside revision 3**).

### 0.5 Revision 3 — what revision 2 left undone

Added Wave 8 with per-document correction specs; Appendix A; W7.2's quarantine collision
resolved; W8.4; three guardrail breaches; §0.6's loss-audit.

### 0.6 Revision 3's loss-audit

Carried forward, not encoded: the occurrence-matrix statistics; the lower-effort W7.12 variant
(keep the ledger as a fifth document with a banner); the confound in W6.8's evidence.

### 0.7 Revision 4 — the re-derivation, and what it overturned

Seven independent read-only passes re-ran the evidence commands behind every wave. Results:

| # | Added or overturned in revision 4 | Consequence |
|---|---|---|
| 1 | **Wave H** — the hard-coding ruling (§0.1) | New first wave; outranks W0.1 |
| 2 | **W1.1's fix specification is refuted** | The four-line reorder cannot work; replaced |
| 3 | **D-C's premise is dead — `main` is already protected** | Wave 2 becomes a configuration audit |
| 4 | **W5.1 is 8 rows across 5 items**, not 6 across 4 | Two new false values at E-15 |
| 5 | **W0.3 added** — the detector is blind to NULL-unit rows | It cannot see half the class |
| 6 | **W5.4's numbers were stale at revision 3's own subject** | 4 of 76, 8 ids, `integrity-protocol` cited by **zero** |
| 7 | **W5.7/R-21 re-derived and CONFIRMED** | The one entry the register never verified |
| 8 | **W9 added** — the dropped inheritance | Two ratified obligations no wave carried |
| 9 | **W7.14 is impossible as written** | The artifacts never existed in the repository |
| 10 | **Twenty-two further corrections** | Appendix C |
| 11 | **Wave L** — the execution ledger, with five standing interrogations (owner requirement) | Gates every other wave; nothing executes without an entry written first |

**Revision 4's own loss-audit** — carried forward but deliberately **not** encoded as items:

- **The 914 repo-wide dangling `REF-NNNNN` identifiers** (327 `GAP-`, 291 `CON-`), of which most
  are legitimate immutable migration history. The genuinely novel part — **81 REF-IDs and 27
  GAP-IDs cited in `decisions/` and `attestations/`**, which are forward-only and cannot be
  rewritten — is folded into W7.5's scope note rather than given its own item, because it has no
  clean fix: the frozen-surfaces declaration must carry "cited-as-of-date" semantics for the
  governance layer, not a resolution guarantee.
- **The 82-file / 22,111-line "unreferenced" candidate list** produced by revision 4's own
  connectivity matrix. It is inflated by `schemas/` (32 files, dynamically resolved) and
  top-level entry points. The ledger's adjudicated **26 files / 7,330 lines** stands. Recorded
  because it is this revision's own instance of W6.6.
- **`workplan/deprecated/` (16 files) sits outside `.ignore`**, unlike `_superseded/`. Noted for
  W7.8's index and a future owner ruling; not an item.
- **The `db.py` deletion branch carries a 12-file caller sweep** (CLAUDE.md + 11
  `skills/*_SKILL.md`). Folded into W7.4's framing rather than itemised.

---

## PART I — The constraint architecture: move the invariant into the row

### I.1 The argument

This repository's compliance model is **detect-then-report**, and its entire catalogue of
failures is that model failing in the four ways it can fail:

| Failure mode | Instances in this plan |
|---|---|
| The detector was never run | W0.1 — `jurisdictional_divergence` quarantined 11 days while CI ran its *unit test* green |
| The detector ran and examined nothing | four separate incidents (CLAUDE.md §10); `citation_mining_completeness`'s `.md` predicate; `test_directness_2_2` |
| The detector ran, examined rows, and was blind to the defect class | W0.3 — `jurisdictional_divergence.py:69` filters `WHERE value_numeric IS NOT NULL AND unit IS NOT NULL`, and the extractor failure it exists to catch is *precisely* the one that leaves `unit` NULL |
| The detector ran, found the defect, and nothing was gated on it | 34 advisory checks; the nine standing advisory failures (W5.8) |

A constraint has none of these failure modes. It cannot be un-run, cannot examine nothing, cannot
filter out its own subject, and cannot be advisory. **Every invariant moved from the check layer
into the DDL is one fewer check that can be vacuous** — which is the argument that connects
Part I to Part III, and the argument no previous revision made.

### I.2 What survives the write path — the mechanism selection

Four declarative mechanisms are available in SQLite. They are **not** equally durable here,
because of a fact no prior revision stated crisply:

| Mechanism | Survives `PRAGMA foreign_keys=OFF`? | Survives `executescript()` of an arbitrary migration? | Survives `--rebuild`? |
|---|---|---|---|
| `FOREIGN KEY` | **NO** | yes when on | yes when on |
| `CHECK` | **YES** | **YES** | **YES** |
| `NOT NULL` | **YES** | **YES** | **YES** |
| `TRIGGER` | **YES** | **YES** | **YES** |

`migrate_db.py:161` executes `PRAGMA foreign_keys = OFF` before every migration body, and
`:250` does the same in the rebuild path. **So the repository's schema leans almost entirely on
the one mechanism its own writer disables**, checks after commit, and downgrades to a warning on
a substring. Verified at HEAD: the canonical database contains **0 triggers**
(`SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'`), and `evidence_cell_state` carries
only enum CHECKs and one `json_valid` — not one of its state-machine implications.

The constraint architecture below therefore uses **CHECK and TRIGGER as the primary carriers**
and FK as reinforcement, which is the inverse of the current schema's weighting.

### I.3 The state machine, promoted from prose to DDL

`governance/mission-and-epistemics.md:109-120` defines a four-state machine whose implications are
in-row and whose columns already exist. Not one is constrained. Each line below is a *doctrine
sentence* that becomes unwritable-when-false:

```sql
-- evidence_cell_state, added by table rebuild (SQLite has no ADD CONSTRAINT).
-- Free at 0 rows. Permanently expensive after the first content batch.

CHECK (state <> 'pending'         OR gap_register_id IS NOT NULL)
-- doctrine: a pending cell carries a gap-register entry. Today: validator-only.

CHECK (state <> 'not_applicable'  OR not_applicable_rationale IS NOT NULL)
-- doctrine: not_applicable is a judgement, and a judgement states its ground.

CHECK (NOT (state = 'stated' AND (code_floor_only = 1 OR regulatory_stratum_only = 1)))
-- doctrine: the T4-T6 regulatory stratum never anchors a `stated` cell.
-- This is `no-regulatory-stratum-stated` from pipeline-contract.yaml:79-82, which is
-- DECLARED-BUT-UNENFORCED (`check: null`). One CHECK makes it real.

CHECK ((value_min IS NULL AND value_max IS NULL) OR value_unit IS NOT NULL)
CHECK (value_min IS NULL OR value_max IS NULL OR value_min <= value_max)
-- D-A's acceptance conditions, promoted from a contract sentence to a row property.

CHECK (doctrine_sha IS NULL OR (length(doctrine_sha) = 7 AND doctrine_sha GLOB '[0-9a-f]*'))
-- W3.3, leg 4 of DR-2026-08-06's four-leg promise. NOT NULL once the writer stamps it.
```

**Note the ordering trap this creates and how to avoid it.** `CHECK (state <> 'pending' OR
gap_register_id IS NOT NULL)` combined with `gap_register_id REFERENCES gaps(gap_id)` means a
pending cell cannot be written before its gap row. That is correct and it is *also* why W1.4's
`GAP-1` bug becomes fatal rather than cosmetic: with the constraint in place, a malformed gap id
stops the determination instead of decorating it. **W1.4 is therefore a prerequisite of I.3, not
an independent hygiene item.**

### I.4 The quantity constraints — corrected against live data (AE-1)

The tempting one-liner is `CHECK (value_numeric IS NULL OR unit IS NOT NULL)`. **Do not ship it.**
Re-derived at HEAD, eight `jurisdictional_values` rows are numeric-with-NULL-unit, and **four are
correct data**:

| jv | item | jur | numeric | reading |
|---|---|---|---|---|
| 14 | E-07 | US | 0.42 | **legitimate** — wet DCOF, a dimensionless index |
| 15 | E-07 | GB | 36.0 | **legitimate** — PTV, a dimensionless index |
| 96 | A-10 | US | 50.0 | **legitimate** — occupant trigger count |
| 100 | A-10 | FR | 50.0 | **legitimate** — seat trigger count |
| 16 | E-07 | DE | 9.0 | garbage — the `9` in "R9–R13" |
| 17 | E-07 | AU | 3.0 | garbage — the `3` in "P3–P5" |
| 106 | E-15 | GB | 2021.0 | garbage — the **year** in "Building Regs 2021" |
| 107 | E-15 | US | 1.0 | garbage — the edition ordinal in "Supplement 1 (2024)" |

The naive constraint forbids rows 14, 15, 96 and 100 — real values that happen to be
dimensionless — and the repository would then "fix" them by inventing units, which is the same
failure as inventing the numbers. **The invariant is not *numeric implies unit*; it is *numeric
implies a declared quantity kind*.** Specification:

1. **Backfill migration first.** Correct the four garbage rows per W5.1 (`value_numeric = NULL`,
   the text states no quantity), and give the four legitimate rows an explicit dimensionless
   token — `unit = 'DCOF'`, `'PTV'`, `'persons'`, `'persons'` — so that "no unit" and "a
   dimensionless index" stop being the same state.
2. **Then** rebuild with `CHECK (value_numeric IS NULL OR unit IS NOT NULL)`, which is now true
   of every row and false of every future extractor artifact.
3. **And keep the detector.** W0.3's sixth finding class (`numeric_without_unit`) becomes a
   *zero-by-construction* check — it should report `EXAMINED: n, FAILURES: 0` forever, and if it
   ever reports otherwise, the constraint was dropped in a rebuild. A detector that guards a
   constraint is not redundant; it guards the constraint's continued existence.

**Second-order consequence, and the reason this matters beyond eight rows:** the same
column-pair pattern (`value_numeric`/`unit`) exists in `source_value_extractions` and
`spec_value_probes`, both empty. Constrain them **now**, in the same migration, where it costs
nothing and no backfill is required.

### I.5 The Co-1 constraint — doctrine's most distinctive commitment, defended by nothing

`governance/tier-system.md` makes lived experience (Co-1) **co-primary with T1** under CRPD Art.
4.3. `evidence_sources` has 97 columns including `evidence_type`, `tier`, `co1_provenance` and
`co1_source_type`. The relationship between them is enforced by **`validate_source_co1_fields()`
at `validate_evidence_state.py:76-121`, which scans `data/sources/*.yaml` — a directory that does
not exist.** Doctrine's signature commitment is defended by a function that reads nothing.

```sql
CHECK (evidence_type <> 'co1' OR tier = 1)
CHECK (evidence_type <> 'co1' OR co1_provenance IS NOT NULL)
```

`evidence_sources` is empty (0 rows), so this is a free rebuild today. **Verify against the
archived pre-reset DB first** (`archive/pre-reset-corpus-2026-08-06` at `4fc6304`): if historical
Co-1 rows violate it, that is a finding about the corpus, not a reason to weaken the constraint.

### I.6 The two triggers — the walkback edge itself

The constitutive claim ("any published best practice walks backwards to its evidence") is a
**cross-row** implication, so CHECK cannot express it. It needs the mechanism this database has
zero of.

The insertion-order objection — `cell_source_links.cell_id` references `evidence_cell_state`, so
the cell must exist before its links — has a clean resolution that is *also* the epistemically
honest shape: **cells are born `pending`, and promotion is a separate act.**

```sql
CREATE TRIGGER trg_cell_birth_pending
BEFORE INSERT ON evidence_cell_state
WHEN NEW.state IN ('stated','provisional')
BEGIN
  SELECT RAISE(ABORT,
    'a cell is created pending; promote it after attaching evidence via cell_source_links');
END;

CREATE TRIGGER trg_cell_promotion_requires_evidence
BEFORE UPDATE OF state ON evidence_cell_state
WHEN NEW.state IN ('stated','provisional')
 AND NOT EXISTS (SELECT 1 FROM cell_source_links WHERE cell_id = NEW.cell_id)
BEGIN
  SELECT RAISE(ABORT,
    'stated/provisional requires at least one row in cell_source_links');
END;
```

This is the strongest guarantee available in this stack: it fires under `foreign_keys = OFF`,
under `executescript()` of a hand-written migration, under `--rebuild`, and for a session that has
never read CLAUDE.md. **It converts DR-2026-08-06 §1's indictment — *"not one cell could walk
backwards"* — from a property the repository audits into a property the repository cannot violate.**

### I.7 The one demotion — `governing_refs` is the structural root cause

This is the item no wave addresses head-on, and it is where the untraceable row actually comes
from. Verified DDL:

```
governing_refs  TEXT CHECK (governing_refs IS NULL OR json_valid(governing_refs))
```

**A reference list living in a JSON blob that no foreign key can reach.** It is the operative
carrier today: `validate_evidence_state.py:275-277` validates the blob, and the corridor-walk
trial produced a determination with **7 governing refs and 0 junction rows** — after which
`spec_page.py:217-223` correctly rendered *"records no governing sources … treat it as
unevidenced."* The honesty mechanism reported the cell as unevidenced **because the evidence was
in a string.**

W3.5 as written adds a `cell_source_links` write *beside* the blob. That leaves two truths, which
is the dual-store class Wave 7 exists to clear and guardrail 5 exists to forbid. **Specification:**

1. `cell_source_links` becomes the **sole** carrier of the cell→source edge.
2. `governing_refs` becomes **derived** — regenerated from the junction by the writer, or dropped
   entirely and replaced by a `v_cell_governing_refs` view. Prefer dropping: a cache with no
   invalidation rule is how the two diverge again.
3. `validate_evidence_state.py` reads the junction, not the blob.
4. The I.6 trigger then means what it says. With the blob still operative it does not: a cell
   could satisfy the trigger with one junction row while asserting seven refs in JSON.

### I.8 What stays in the check layer, honestly

The constraint architecture is not a claim that checks are obsolete. Four classes cannot move,
and saying so precisely is what keeps the register from re-inflating:

| Class | Example | Why it stays a check |
|---|---|---|
| **Fuzzy predicates** | H4's "no determination in an item name, except standard designations like `ISO 23599:2019`" | The permitted set is judgment; a CHECK would need an unbounded exception list |
| **Cross-store agreement** | DB ↔ entity YAML ↔ markdown ↔ rendered site | The constraint engine sees one store |
| **Judgment adequacy** | verification-adequacy classes (DR-2026-08-06 §3); tier grading | Not mechanically decidable |
| **File-surface facts** | banners, pointers, doc freshness, commit format | Not rows |

**Scope statement, stated so it cannot be overclaimed later:** Part I guarantees *DB-side*
traceability only. That is the right scope, because DR-2026-08-06 §1's indictment is a DB-side
indictment.

### I.9 Cost, and why the window is closing

| Item | Cost | Cost after first content batch |
|---|---|---|
| ~10 CHECKs across 4 tables | table rebuild at 0 rows (or 109 for `jv`, post-backfill) | rebuild + data remediation + invalidated determinations |
| 2 triggers | 20 lines of DDL | same DDL, but retrofitting onto populated-but-unlinked cells **re-runs the reset's own §1 indictment** |
| `doctrine_sha` column | one migration | one migration + backfill of unknowable historical SHAs |
| `governing_refs` demotion | free (0 rows) | a dual-store reconciliation of exactly the kind Wave 7 exists to clear |

**SQLite has no `ADD CONSTRAINT`.** Every item above is a table rebuild, and a table rebuild is
free at zero rows and a migration-with-remediation afterwards. The clean-room reset bought a
one-time window in which "untraceable is unwritable" costs one migration. **The window closes at
the first content batch, and nothing else in this plan has that property to the same degree.**

---

## PART II — The write path: the one choke-point that is real

### II.1 Why this is Part II and not a wave item

`scripts/db.py` is 1,889 lines and 43 functions with **zero importers and zero subprocess
callers**, while 80 scripts open SQLite directly across four idioms. That is the repository's own
proof that **a library choke-point is a discipline, and disciplines here fail.** The only real
choke-point is `executescript()` inside `migrate_db.py`. Part I's constraints work *because* they
sit below that choke-point rather than beside it; Part II makes the choke-point itself sound.

### II.2 The specification (supersedes W1.1–W1.3 as one edit)

Verified at HEAD, `migrate_db.py:158-186`, the apply loop does this:

```
pre_violations = foreign_key_check()      # :160
PRAGMA foreign_keys = OFF                 # :161
executescript(sql)                        # :163   <- migration body contains its own COMMIT
INSERT INTO data_migrations …             # :164
conn.commit()                             # :171   <- durable here
PRAGMA foreign_keys = ON                  # :173
post_violations = foreign_key_check()     # :174   <- checked after durability
is_bootstrap = "BOOTSTRAP" in body[:500]  # :176   <- prose disables enforcement
raise IntegrityError                      # :182   <- too late
except: conn.rollback()                   # :183-184 <- rolls back nothing
```

`emit_data_migration.py:201` wraps every emitted body in `BEGIN TRANSACTION; … COMMIT;`, and
`executescript()` issues an implicit COMMIT before running. **Nothing inside this connection can
be atomic**, which is why the four-line reorder four documents agreed on cannot meet its own exit
condition. Replacement:

1. `conn.backup()` to a tempfile snapshot.
2. Apply the migration **to the snapshot**.
3. `PRAGMA foreign_key_check` on the snapshot; diff against the pre-set.
4. **Clean → apply to the real database. Dirty → discard the snapshot, write nothing, exit non-zero.**
5. Delete both `is_bootstrap` tests (`:176` and the undocumented duplicate at `:261`).
6. On failure, move the file to `scripts/migrations/failed/` (invisible to the non-recursive
   `glob("*.sql")` in both the apply and rebuild paths) and print `N migration(s) not attempted`.

**Exit condition, unchanged from Wave 1 and now actually reachable:** the corridor walk's stage-4a
ordering probe is rejected **with nothing written** — no data row, no `data_migrations` row.

### II.3 The interaction with Part I that must not be missed

`PRAGMA foreign_keys = OFF` at `:161` remains necessary for bulk load ordering, and Part I's
CHECKs and triggers are **unaffected by it** — that is precisely why they were chosen. But a
migration body that violates a CHECK now fails inside `executescript()` on the *snapshot*, which
is the behaviour the exit condition names. **Part I without Part II gives loud failures after
durability; Part II without Part I gives a clean snapshot check over an unconstrained schema.
They are one deliverable.**

---

## PART III — The verdict layer: closing the vacuity class permanently

### III.1 What the guard is and what it covers

`run_checks.py:272-301` is well built: it FAILs (not SKIPs) when a check declaring `min_items`
prints no `EXAMINED: <n>` line, with an anchored regex, and its own comment records the
false-positive it already caused. The defect is coverage. Re-derived at HEAD: **6 of 65 checks
declare `min_items` — 9% of the register** (revision 5 corrects a claim of 14, AE-3). All four
historical incidents were checks that had not opted in. **An opt-in guard protects exactly the
authors who already suspected themselves.**

### III.2 The four sub-species and the instrument for each

| # | Sub-species | Instance | Instrument |
|---|---|---|---|
| 1 | **Non-declaration** | 59 of 65 checks | **Invert the default.** A `run_checks.py --selftest` assertion (C8) that every `active` check declares either `min_items` or an explicit `vacuity_exempt: <reason>`. Ratchetable, mechanical, one assertion |
| 2 | **Self-reported subjecthood** | `citation_mining_completeness` printed a count from a predicate matching nothing | **EXAMINED-delta tracking** — persist `(commit, check_id, verdict, examined_n)` per gated run; a green check whose `examined_n` fell across a commit is the repo's named failure mode, detectable by the runner with no hand-authoring |
| 3 | **The filtered detector** | `jurisdictional_divergence.py:69` | **Not closable by any output-side guard** — the filter is invisible from the output. Closed only by Part I: a constraint has no filter |
| 4 | **Registry-level absence** | CI runs `test_jurisdictional_divergence`, never the detector | **Two selftest assertions:** every `scripts/audit/*.py` appears in `checks:` or `quarantine:`; and W7.10's `disposition:` / `exit_condition:` fields on every quarantine entry |

### III.3 The `basis:` correction

"All 65 checks carry a `basis:` field" is true and **half-empty: 32 of 65 are `unattributed`**
(re-derived at HEAD; next largest is `hygiene` at 16). The field exists; the authority half does
not. The registry's own header is honest about the ratchet; **any summary citing basis-coverage
as an achieved guarantee is reporting the field, not the property.** Add a selftest assertion
that the `unattributed` count is non-increasing, which is the only version of this that is cheap
and cannot rot.

---

## PART IV — The ledger, mechanically derived (this supersedes Wave L's specification)

### IV.1 The owner requirement, restated

> *An active logging of all work performed, complete with specific notes about where any
> lines/values were changed, such that we have an active trail for future work and auditing — and
> the logging must involve active interrogation of interdependencies, tracing, orphaning, breaks,
> and deduplication/culling candidacy.*

**The requirement is adopted in full. Wave L's *specification* of it is rejected**, and Part IV
is the replacement. This is a proposal about mechanism, not scope: nothing the owner asked for is
dropped.

### IV.2 Why the six-block hand-authored form is the wrong instrument

Wave L proposes six mandatory hand-authored YAML blocks per atomic change, gating every other
wave. Four arguments against, three of which are the repository's own recorded history:

1. **`emit_data_migration.py:59-63` already ruled on this**, in its own comment: the same wrong
   value was written twice in one day *after* being recorded in a session file, a PR body **and**
   an attestation deviation — *"and prose did not prevent the repeat a few hours later. The fix
   belongs at the point of writing."* Wave L is prose at the point of writing.
2. **The attestation system is Wave L's predecessor**: per-change, hand-authored, mandatory
   blocks, minimum lengths (`bias_direction` ≥30 chars), forward-only corrections. Outcome after
   76 artifacts: 4 failing their own resolution check, 8 unresolvable rule identifiers, and
   corpus validity established by nothing because every attestation check is diff-scoped
   (`adherence_log_audit.py:551`). A second such system firing *more often* converges on
   boilerplate *faster*.
3. **Wave L claims descent from `walk_harness.py` to satisfy guardrail 3, and the descent is
   backwards.** The harness's 105-action log was **captured by instrumentation**. Wave L
   generalises its *output format* while discarding its *mechanism*.
4. **Wave L concedes its own unenforceability at L5**: whether `unswept_and_unexplained` is truly
   empty "is not mechanically checkable." A gate whose central field is unverifiable is a
   declaration, and Part III §III.3 is about what declarations are worth.

### IV.3 The derived ledger — specification

**Principle: automatic capture by default, hand annotation by exception.** One `work_log` table,
one generated `workplan/WORK-LOG.md` view, and the five interrogations answered by *queries* over
facts that cannot be wrong.

| Block | Wave L | Revision 5 | Source of truth |
|---|---|---|---|
| **Identity** (commit, session, timestamps) | hand | **derived** | git |
| **Locus** (path, target, line, before/after, mechanism, migration_id) | hand | **derived** | `git diff` + `data_migrations` |
| **I1 interdependency** (readers, writers, caller sweep) | hand | **derived + 1 exception field** | the sweep command is already mechanical; only `deliberately_not_swept` *reasons* are authored |
| **I2 tracing** (walkback intact) | hand | **enforced, not recorded** | Part I §I.6 — the trigger makes an untraceable cell unwritable, so the field is redundant where it matters and unverifiable where it does not |
| **I3 orphaning** (dangling REF-/GAP-/CON- ids, unreferenced objects) | hand | **derived** | `validate_cross_refs` + the connectivity matrix, differenced across commits |
| **I4 breaks** (what changed verdict) | hand | **derived — and this is the highest-value block** | `run_checks.py` already captures every check's status and output; persist it. `verdict_changes`, `examined_changes`, `newly_vacuous` become queries. **This simultaneously delivers Part III §III.2 sub-species 2** |
| **I5 dedup/culling candidacy** | hand | **hand — the one genuine judgment** | authored, one line, and the only block a session must write |
| **Intent** | hand, pre-registered | **hand, pre-registered, one line** | the intent-vs-derived-actuals delta survives at ~5% of the authoring cost |

**Net:** Wave L's +1 table and +1 generated file are retained. Its four hand-authored blocks
become **two one-line fields**. The five interrogations go from five prose sections that can be
written falsely to **four queries that cannot be and one judgment that is explicitly a judgment.**

### IV.4 Honest limitation

A derived ledger records what *happened*, not what was *intended and abandoned*. That is exactly
what the pre-registered intent line preserves, and it is why the intent field survives the cull
while the other four do not. **If a loss recurs that the derived ledger would not have caught,
grow the schema then — with the instance as its evidence.**

---

## PART V — The execution sequence

Seven moves. Each has an exit condition that is a command, not a judgement. **The sequencing rule
from PR #93 is retained and sharpened:** fix the substrate, rule on the boundary, then build —
because rows are what make substrate fixes expensive, and Part I §I.9 quantifies exactly how
expensive.

### M0 — The owner memo. Blocks M3, M4, M6. (Part VI)

Five questions, one sitting, four with drafted recommendations. Nothing else in this plan asks
for owner attention until M7.

### M1 — The write path and its prerequisites. No decision required.

- Part II §II.2 as **one edit** to `migrate_db.py:158-186` (subsumes W1.1, W1.2, W1.3).
- **W1.4 via `db.py`** — give `db.py:next_gap_id` an optional `conn` parameter *first*, then
  import it. A literal import silently opens `GUIDEBOOK_DB_PATH` while `assess_cell.py:490-491`
  refuses the canonical DB, and `assess_cell.py` is exempt from `db_path_env_audit`, so nothing
  would catch it. **This is a prerequisite of Part I §I.3, not hygiene** — under the pending-gap
  CHECK a malformed gap id stops the determination.
- **W1.5** — `requirements.txt` (`PyYAML>=6.0,<7`, add `jsonschema`); the documented setup command
  currently fails in a clean container.
- **R-01 interim** — `assert_not_canonical` + required `--db` on the replay script, the only real
  unguarded writer. *Not* the full W7.1 retirement (deferred, reversible).
- **R-11/R-12/R-13** — read the registry's `deps:` field and abort with exit 2; quote
  `check-registry.yaml:174`; guard `graph_audit.py:277`'s selftest leg.

**Exit:** stage-4a probe rejected with nothing written; `assess_cell.py` completes; a clean
container runs `pip install -r requirements.txt` successfully.

### M2 — The numeric substrate, cleaned then constrained.

Order matters and is not negotiable: **W0.3 → W0.1 → W9.1 → W5.1 + W5.6 → Part I §I.4.**

- **W0.3 first.** Wiring a detector whose row filter is anti-correlated with its own defect class
  produces a green that means nothing.
- **W9.1's one-line exemption DR** (`url_verification_runs` joins DR-2026-05-28's exempt list)
  ships *with* W5.6, or the widened blocking gate goes permanently red the next time the
  bi-weekly cron writes.
- **W5.1 widened to twelve rows** (AE-1): the eight known defects **plus** the four legitimate
  dimensionless rows that need an explicit unit token before the constraint can exist.
- Reconcile the five shadow YAMLs in the same PR.

**Exit:** `numeric_without_unit` reports `EXAMINED: 109, FAILURES: 0`; the reproducibility gate
covers 99.9% of rows instead of 2.2%; the CHECK is in the DDL.

### M3 — Wave H, the hard-coding ruling. Owner-ruled; execution shape in M0 Q2.

**H3 first and read-only** — classify all 28 stripped values into (a) already held in
`jurisdictional_values` or (b) held nowhere, *in the migration's own comment block*. Then H1/H2 as
one data migration on `items.name` (**not a key** — all 14 inbound FKs target `item_code`), then
regenerate `parts/` and `site/`, then H4 advisory, then H5 (the same method run over `populations`,
`axes`, `access_needs`, `slugs`, `rooms`).

**Exit:** `SELECT COUNT(*) FROM items WHERE name GLOB '*[0-9]*'` returns only the permitted
standard-designation set; the 51 rendered files regenerate clean.

### M4 — The boundary, and the reshapes that are now-or-never.

- **D-A declared** ("human, declared" — M0 Q1) in `pipeline-contract.yaml`, with the input
  contract Part I §I.3 now *enforces* rather than declares.
- **AE-4 adopted as sequenced:** the migration path is the writer for stage-7 outputs. Declare it
  in the contract for five of six; build only **W3.5** (the one real code writer — `assess_cell.py`
  must insert `cell_source_links` after line 573), and fold Part I §I.7's demotion into the same
  change so the junction is the *sole* carrier, not a second one.
- **W3.2** — split `target_population` into code + note **before any rows**; 22 of 30 pre-reset
  values were prose, so a bare FK would forbid the majority of the column's historical use.
- **W9.2 — upgraded to now-or-never (AE-2).** Canonical `jurisdictions` and `languages` tables,
  FK'd from `jurisdictional_values`, `lang_jur_map` and `term_aliases`. Live evidence: **52
  distinct free-text values across three tables**, `GB` vs `UK` disagreement *between* tables,
  standards bodies (`ISO`, `EU`) in a jurisdiction column, and the literal string `colloquial` in
  `term_aliases.jurisdiction`. DR-2026-08-06 §4.4 already calls this "the first frame work after
  this reset."
- **W3.9 Candidate B** — shared locator *definition* in place, plus the `locator_schemes`
  registry sized for ~24 families. Re-derived: `locator_scheme` is **NULL on all 109 rows**, so
  the entire 16-column block is unpopulated and free to reshape today.
- **Part I §I.3, §I.5, §I.6 land here** — the table rebuilds, in one migration, while empty.
- **Part IV's `work_log`** table + generated view + the two registered checks.

**Exit:** inserting a `stated` cell with no `cell_source_links` row raises; inserting a `pending`
cell with no gap raises; `governing_refs` no longer exists as an independent carrier.

### M5 — Stop the repository lying to its next session. Minutes, no gate.

**W8.7** (seven one-line supersession banners) + **W8.8** (`sessions/handoff-next-session.md`,
five merges stale and hidden from grep by `.ignore`) + **W7.8** (`workplan/INDEX.md`, generated,
registered for freshness) + one `.ignore` line for `workplan/deprecated/`.

**And the corrections this revision owes to CLAUDE.md**, which is the file every session reads
first: §0 and §7 assert `main` is unprotected (**it is protected**); §7 asserts two blocking gates
are red (**zero are; `test_db_integrity` is 70/70**); §4's `--rebuild` docstring and
`migrate_db.py:27-30` both still describe the reproducibility gate as catching direct writes.

**Cut from Wave 8: W8.1–W8.6's line-number corrections.** Correcting figures inside documents
whose banner already says *"figures superseded, reasoning stands"* is analysis-about-analysis on
documents being retired. The porting obligation is discharged by §0.3–§0.7 and Appendices A/C/E.
**W7.13's ID renames are deferred** for the same reason: on bannered documents the C1/C4/D2
collisions are inert, and the INDEX's dual-ID column resolves them.

### M6 — Content.

Drop `case_studies`' rival prose columns, load the two bounded corpora already identified (the
56 KB case-study compendium, `references/economics/`), resume research under `db.py log-search`
per DR-2026-08-06 §4.1. **This is the terminal state every move above is measured against**, and
its absence from revision 4's dependency graph — which terminates in more apparatus (Wave 4) — is
the single most important structural correction revision 5 makes.

### M7 — Everything else, after content flows.

W7.1 (19 files / 6,074 lines — reversible, `_archived/`), W7.2, Wave 4 (gated on D-A **and** on
content existing), W5.8's nine advisories, the frozen-corpus declarations (W7.5–W7.7), the
view rulings, both Part-3 cuts, W7.12, W7.13, and the second owner memo.

---

## PART VI — The owner memo: five questions, one sitting

Revision 4 scatters ~20 owner gates across ten waves, serialising the scarcest resource in the
project. Batched, most-unblocking first. **Four of the five carry drafted recommendations and
should be read as consent items.**

| # | Question | Recommendation | Unblocks |
|---|---|---|---|
| **Q1** | **D-A — is value determination a machine stage or a human one?** `assess_cell.py:559` writes `None, None, None` for `value_min/max/unit` unconditionally; no code path runs from N extracted values to one value | **Human, declared** in `pipeline-contract.yaml`, with the input contract and acceptance conditions Part I §I.3 enforces in DDL | The stage-7 reframing (AE-4), W3.6, all of Wave 4, and the definition of content production itself. **One yes converts fourteen "unwritable outputs" into a contract sentence plus one code writer** |
| **Q2** | **Wave H execution shape** (the principle is already ruled) | Sign the 28-name mapping; rule on H4's permitted set (standard designations like `ISO 23599:2019` stay); rule H6's three dispositions (`rooms` → register as frame; `item_population_elaborations` → reset) | M3, W5.2, W5.3 |
| **Q3** | **First content batch authorisation** (DG-NON: work-product inclusion) | The case-study compendium + `references/economics/` as the first population | **M6 — the terminal state** |
| **Q4** | **W9.1 exemption DR** — one line adding `url_verification_runs` to DR-2026-05-28's exempt list | Adopt. Without it, W5.6's widened blocking gate goes permanently red on a legitimate cron write | The whole M2 chain shipping safely |
| **Q5** | **`scripts/db.py` — adopt or delete?** 1,889 lines, 43 functions, zero callers | **Adopt, narrowly.** Deleting strands a ratified discipline (DR-2026-08-06 §4.1 names `db.py log-search`), requires a 12-file caller sweep, and **deletes the correct `next_gap_id` that W1.4's live bug re-implemented wrongly**. "Adopt" does **not** mean converting 80 scripts — it means the id-allocator and `connect()` seams, each shipping with a registered check, applied to scripts as they are touched. `repo_root()` never: no correctness argument | W1.4's clean fix; the seams |

**Deferred to a second memo, explicitly scheduled after M6:** W7.1, W7.5–W7.7, W7.9, W7.12, the
view and `weighting_profile` rulings, W9.3's five deferred items, R-25. No owner attention is
spent on retirement hygiene while content production is still blocked.

---

## PART VII — Disposition of every prior item (the loss audit)

Discharges **W6.9**: every supersession publishes what it dropped. Nothing below is deleted; each
item is placed.

| Item | Disposition |
|---|---|
| **L1–L5** | **Superseded by Part IV.** Requirement adopted in full; six-block hand-authored form rejected; `work_log` table and generated view retained; I4 upgraded to the highest-value block and made mechanical |
| **H1–H6** | **On path — M3.** Unchanged. H3 remains the first action of the wave |
| **W0.1, W0.2, W0.3** | **On path — M2**, in that order, W0.3 first |
| **W1.1, W1.2, W1.3** | **Superseded by Part II §II.2** as one edit. Revision 4's snapshot-verify approach is adopted and specified against the verified line numbers |
| **W1.4** | **On path — M1, and promoted**: a prerequisite of Part I §I.3, not hygiene |
| **W1.5, W1.6** | **On path — M1** (W1.6 is documentation: name the dispatcher guarantee and L04's dormancy) |
| **D-A** | **On path — M0 Q1**, with the recommendation carried verbatim |
| **D-B** (triangle marker) | **Deferred to M7.** No derived value can exist before content; the DR should still be written when W3.1 lands |
| **D-C** (branch protection) | **Premise dead — `main` is protected.** Reduced to the configuration audit in M5's CLAUDE.md corrections + a note that the "no promotions during the protection window" rule is live |
| **W3.1** | **Deferred to M7** with D-B |
| **W3.2** | **On path — M4.** Now-or-never |
| **W3.3** | **Absorbed into Part I §I.3** as the `doctrine_sha` CHECK |
| **W3.4** | **Absorbed into Part I §I.5**, widened with the `co1_provenance` companion CHECK |
| **W3.5** | **On path — M4, and corrected**: the junction must be the *sole* carrier (Part I §I.7), not a second one beside `governing_refs` |
| **W3.6** | **Deferred to M7** — depends on W3.1 and D-A |
| **W3.7** | **Deferred to M7** — 16 judgment acts needing owner review; second memo |
| **W3.8** | **Superseded by AE-4 + M4**: declare five of six in the contract; build only W3.5 |
| **W3.9** | **On path — M4, Candidate B**, strengthened: `locator_scheme` is NULL on all 109 rows |
| **W4.1–W4.5** | **Deferred to M7.** Gated on D-A *and* on content existing |
| **W5.1** | **On path — M2, widened from 8 rows to 12** (AE-1) |
| **W5.2, W5.3** | **Deferred** — both explicitly wait on Wave H (M3) |
| **W5.4** | **Split.** (c) — the `--corpus` flag and `attestation_corpus` check — is **on path at M5**, because it is the instrument that makes the 76-artifact corpus checkable at all. (a) and (b) are second-memo items |
| **W5.5** | **Second memo**, paired with the 11 unread views. Revision 5's position: **views are the most reversible object class in the database** — the definition survives in migration history forever — so retire by default and recreate when a reader exists, rather than spending owner attention ruling on each |
| **W5.6** | **On path — M2**, shipping with W9.1 |
| **W5.7** | **Deferred to M7** — latent, fires on the first partial determination, which cannot occur before M6 |
| **W5.8** | **Deferred to M7.** Do not clear by silencing |
| **W6.1–W6.3** | DONE, retained as record |
| **W6.4** | Folds into W5.4(c) — **on path at M5** |
| **W6.5** | Retained as method note |
| **W6.6–W6.11** | **On path — land in `references/project-standards.md`** in its `RULE:`/`CONDITION:`/`ACTION:`/`DATE:` format with the paired Decision record. **Revision 5 adds W6.12** (below). They must not land in a workplan document again — three of them already lived there and died |
| **W7.1** | **Deferred to M7.** Reversible (retire to `_archived/`); its one dangerous member gets the M1 interim guard |
| **W7.2** | **Deferred to M7.** Drop entirely if it starts to feel like `db.py` again |
| **W7.3, W7.3-G5, W7.9** | **Second memo.** Revision 5 recommends **not** taking the Part-3 cuts: `situations` is the native Co-1 entity, named in five governance documents including a ratification record — DG-NON exposure for a two-table prize. An empty table costs nothing |
| **W7.4** | **On path — M0 Q5.** Adopt narrowly |
| **W7.5–W7.7** | **Deferred to M7** — honesty work, not production-blocking |
| **W7.8** | **On path — M5** |
| **W7.10** | **Absorbed into Part III §III.2** sub-species 4 |
| **W7.11** | **Second memo** |
| **W7.12** | **Deferred** — fully reversible once M5's banners are up |
| **W7.13** | **Cut from the critical path.** Inert on bannered documents; the INDEX's dual-ID column resolves the collisions |
| **W7.14** | **Dropped as written** (the artifacts never existed); the re-derivation from the anatomy document is an M7 item |
| **W8.1–W8.6** | **Cut** (except where an item is separately on path). Analysis-about-analysis on documents being retired |
| **W8.7, W8.8** | **On path — M5** |
| **W9.1** | **On path — M2**, shipping with W5.6 |
| **W9.2** | **On path — M4, upgraded to now-or-never** (AE-2) |
| **W9.3** | **Split by its own members**: (1)→W9.1 on path; (2) promote `migration_reproducibility_deep`→ absorbed into M2's widening; (3)→W5.6 on path; (4) DONE; (5)–(8) second memo |
| **W9.4** | **Second memo** — the 23 ledger-only migrations and the hand-maintained `BASELINE_DATA_CUTOFF_TS` are a dual representation inside the mechanism proposed as sole source of truth |
| **W9.5** | **Deferred to M7** — PMP exists, is unrun, is unwired; it is a content act |
| **W9.6** | **On path — M0**, as a line item in the memo (the archive tag was never created; the archive branch is unprotected) |

### W6.12 — the new method rule revision 5 adds

> **RULE:** A rule that can be a constraint must not be shipped as a check.
> **CONDITION:** An invariant is expressible as `CHECK`, `NOT NULL`, `FOREIGN KEY` or `TRIGGER`
> over the canonical schema.
> **ACTION:** Ship it in the DDL. A check may *additionally* guard the constraint's continued
> existence, but must not be the primary carrier. Where the invariant is not so expressible,
> record which of Part I §I.8's four classes it falls into.
> **DATE:** 2026-08-12

**And the anti-recursion rule, which is not a wave item and governs all of them:**

> **RULE:** No new analysis document until the previous plan's next move has a merged PR.
> **CONDITION:** A session proposes a workplan file whose subject is the apparatus rather than
> the content.
> **ACTION:** Extend the live plan in place, or write a registry check, a DB row, or a DR.
> Findings live in enforced stores, never in prose registers.
> **DATE:** 2026-08-12

The evidence for it is this plan's own history: nine analysis documents in two days, ~13,500
lines, four plan revisions, **zero items executed**, and an error-generation rate of 31 killed
claims in one revision — including a register written to end ID collisions that was followed by
two documents minting new colliding series. The primary deliverable — reasoning docs — stands at
**one**. The next 31,000 lines this repository produces should be evidence rows.

---

## Wave L — The execution ledger. Before any wave executes, including Wave H.

> **SUPERSEDED BY PART IV (revision 5).** The owner requirement is adopted in full; the
> six-block hand-authored specification below is rejected as the instrument, on the evidence in
> Part IV §IV.2. The `work_log` table, the generated view and the five interrogations survive —
> four of them as queries. **The text below is retained as the requirement's record and as the
> source of the block definitions Part IV derives.**

**Owner requirement, 2026-08-11:** *an active logging of all work performed, complete with
specific notes about where any lines/values were changed, such that we have an active trail for
future work and auditing — and the logging must involve active interrogation of
interdependencies, tracing, orphaning, breaks, and deduplication/culling candidacy.*

**This is not a fifth register (guardrail 3).** It extends the mechanism the repository already
built and already ratified: `walk_harness.py`, whose 105-action verbatim log is what made the
corridor-walk trial auditable and whose absence from the review beside it is finding **W6.1**.
Wave L generalises the harness from one trial to every change, and it discharges W6.9 (every
supersession publishes a loss-audit) and W6.10 (a correction that does not propagate is not a
correction) by making both mechanical rather than remembered.

**The governing rule: no change executes without a ledger entry, and the entry is written before
the change, not after.** An entry authored afterwards records what a session remembers; an entry
authored before records what it intended, and the delta between them is the finding.

### L1 — The record shape

One entry per atomic change. **Six mandatory blocks; an entry missing any block is invalid.**

```yaml
- entry_id: WL-0001
  # ── 1. IDENTITY ────────────────────────────────────────────────────────────
  plan_item: H1                      # the wave item this discharges; NEVER null
  session: session_2026-08-12-...    # matches sessions/ and created_by_session
  commit: <sha, filled after>        # forward-only; never rewritten
  intent_written_at: <ISO>           # before the change
  executed_at: <ISO>                 # after; a large gap is itself a signal

  # ── 2. LOCUS — where, exactly ──────────────────────────────────────────────
  changes:
    - path: data/guidebook.db        # or a file path
      target: items.name WHERE item_code='E-08'
      line: null                     # file changes MUST carry line numbers
      before: "Corridor Clear Width (≥1200 mm Minimum on All Primary Routes)"
      after:  "Corridor Clear Width"
      mechanism: data_migration      # | schema_migration | direct_edit |
                                     #   registry_entry | regeneration | owner_decision
      migration_id: data_2026...     # joins to data_migrations; null if not a migration

  # ── 3. INTERDEPENDENCY — what depends on what changed ──────────────────────
  interdependency:
    readers: []                      # every non-archived reader, enumerated, not counted
    writers: []
    caller_sweep_command: "git grep -n '<exact string>' -- ':!_archived'"
    caller_sweep_result: 51          # and the classification below
    swept: []                        # fixed in this change
    deliberately_not_swept: []       # with a reason EACH: generated / frozen / immutable
    unswept_and_unexplained: []      # MUST be empty for the entry to be valid

  # ── 4. TRACING — can the result still be walked backwards? ─────────────────
  tracing:
    walkback: "E-08 ≥1200 → jurisdictional_values jv 72 (GB, BS 8300-2:2018) and jv 77 (ISO)"
    walkback_intact: true            # false REQUIRES a gap row or a written reason
    doctrine_sha: 0f2f525
    evidence_locator: "clause/section per R3, or DOI+page per R3, or [UNVERIFIED-QUANT]"

  # ── 5. ORPHANING AND BREAKS — what this left dangling or altered ───────────
  orphaning:
    identifiers_orphaned: []         # REF-/GAP-/CON- ids now resolving to nothing
    objects_orphaned: []             # views/columns/tables/files with no remaining reader
    prose_orphaned: []               # documents whose claim this change falsifies
  breaks:
    checks_before: {}                # check id -> verdict + EXAMINED count, BEFORE
    checks_after: {}                 # same, AFTER
    verdict_changes: []              # every check that moved, with a one-line cause
    examined_changes: []             # every check whose SUBJECT COUNT moved — a check
                                     # that stayed green while its EXAMINED fell is the
                                     # repository's named failure mode; flag it here
    newly_vacuous: []                # green-with-zero-subjects introduced by this change

  # ── 6. DEDUPLICATION AND CULLING CANDIDACY — what this change made redundant ─
  culling:
    made_redundant: []               # now-duplicate stores, columns, files, prose
    duplicate_of: null               # if this change re-implemented something extant
    detector_checked: true           # W6.7: was an existing tool searched for first?
    detector_search_command: "grep -n <concept> governance/check-registry.yaml scripts/"
    cull_candidates_raised: []       # candidates, NOT findings (W6.6)
    cull_candidates_adjudicated: []  # which were confirmed, by what command
```

### L2 — The five standing interrogations

Every entry answers these. **They are questions, not fields to fill with "n/a" — an entry whose
answers are all empty is either trivial or unexamined, and the ledger should make that visible.**

| # | Interrogation | Answered wrong when | Worked example from this plan |
|---|---|---|---|
| **I1** | **Interdependency.** What reads this, what writes it, and did the caller sweep enumerate them or merely count them? | A count is recorded and the members are not. `CLAUDE.md` §0 rule 5 makes a rename incomplete until every caller is fixed — a count cannot discharge that | W7.4's delete branch: "−1 file" until the sweep found **CLAUDE.md §4:169 plus 11 `skills/*_SKILL.md`** |
| **I2** | **Tracing.** After this change, can the affected value still be walked back to its source, population and governing doctrine? | The walkback is asserted rather than run. DR-2026-08-06 §1 reset the corpus precisely because *"not one cell could do that"* | Wave H's **H3**: every stripped number is classified (a) already in `jurisdictional_values` or (b) held nowhere — and (b) is the finding |
| **I3** | **Orphaning.** What now points at nothing? | Orphans are counted on the surface that changed and not on the surfaces that cited it | The reset orphaned **914 `REF-NNNNN`, 327 `GAP-`, 291 `CON-`** repo-wide, including **81 REF-IDs in `decisions/` and 42 in `attestations/`** — forward-only, unrewritable, and counted by no document |
| **I4** | **Breaks.** Which checks changed verdict, and — separately — which changed **subject count**? | Only verdicts are recorded. *A gate reporting zero may have examined zero*, and this repository has produced that failure four times | `pre_rehab_banner_audit` went from "RED on 6 slugs" to **RED on 68** without anyone noticing, because the reset emptied `bpc_metadata` under it |
| **I5** | **Deduplication / culling candidacy.** What did this change make redundant, and did it re-implement something that already existed? | A new tool is written beside an existing one. **This is W6.7, and the repository has paid twice** | `next_gap_id` re-implemented `db.py:149` and got the schema wrong; `jurisdictional_divergence` sat quarantined while its defect class was re-reported as new |

### L3 — Where the ledger lives, and how it is kept honest

- **Canonical store: a `work_log` table in `data/guidebook.db`**, per CLAUDE.md §2 — the DB is
  authoritative and markdown derives. Schema migration; joins to `data_migrations.migration_id`
  and to `sessions`. **Fallback if the owner prefers not to add a table:**
  `workplan/work-log/WL-<session>.yaml`, one file per session, validated against a schema in
  `schemas/`. The fallback is materially worse — it re-creates the dual-store class this plan
  spends Wave 7 removing — and is recorded only so the choice is explicit.
- **Generated, not transcribed, wherever the fact already exists.** `commit`, `migration_id`,
  `executed_at` and the `changes[].path` set come from git and `data_migrations`; only the four
  interrogation blocks are hand-authored. A ledger that asks a session to retype what git already
  knows will be filled in wrongly and then trusted.
- **A generated `workplan/WORK-LOG.md`** — reverse-chronological, one row per entry, linking
  plan item → commit → migration → checks moved. This is the artefact a future session reads;
  the table is what a query reads.
- **Registered, so it cannot rot.** Two checks, both `advisory` on arrival:
  `work_log_complete` (every commit touching `data/`, `scripts/`, `governance/` or `schemas/`
  since the ledger's epoch has an entry whose `plan_item` resolves to a wave item, and whose
  `unswept_and_unexplained` is empty) and `work_log_fresh` (the generated markdown matches the
  table, on the `context_map_fresh` pattern).
- **Forward-only.** An entry is never rewritten. A correction is a **new** entry with
  `supersedes: WL-NNNN` and a `loss_audit:` block naming what the superseded entry got wrong —
  which is W6.9 made mechanical, and W6.11's answer: a successor that re-derives arithmetic
  while inheriting facts leaves a visible trail of exactly that.

### L4 — Retrofit, bounded

**Do not backfill the repository's history.** The epoch is the first Wave-L commit. But three
existing bodies of work already carry ledger-shaped evidence and should be imported as entries so
the trail starts non-empty rather than pristine-and-useless:

1. The corridor-walk trial's **105-action log** (`walk_harness.py` output) — already the right
   shape; import as entries with `plan_item: W6.1`.
2. The **eight W5.1 corrections**, when they land — the single best worked example of all five
   interrogations firing at once (I1: five shadow YAMLs; I2: value-vs-text walkback; I3: none;
   I4: the detector's WARN clearing *and* its EXAMINED count; I5: the YAMLs become redundant).
3. **Wave H itself** — 28 names, each with its (a)/(b) classification from H3, is the reference
   entry for I2.

### L5 — What the ledger is not

- **Not a substitute for attestations.** Attestations bind an *artifact* to doctrine; the ledger
  binds a *change* to its consequences. Synthesis-path commits still owe both.
- **Not a place for volatile totals.** Per R-17, `EXAMINED` counts and per-check verdicts are
  recorded **with the diff they were measured against**; suite totals are never recorded at all.
- **Not a gate on its own honesty.** `work_log_complete` can only check that entries exist and
  are structurally complete. Whether `unswept_and_unexplained` is truly empty, or merely
  asserted empty, is not mechanically checkable — which is why the block exists as a named field
  rather than an unstated assumption. State that limit in the check's registry `note:`.

---

## Wave H — The hard-coding ruling. First among the substantive waves.

**Owner-ruled 2026-08-11 (§0.1).** DG-NON — work-product inclusion/exclusion and trajectory are
owner-only, and the owner has ruled. What remains is execution shape, which is proposed here.

| # | Action | Evidence | Falsified if |
|---|---|---|---|
| **H1** | **Strip the determinations from the 28 value-bearing item names.** `E-08 Corridor Clear Width (≥1200 mm Minimum on All Primary Routes)` → `Corridor Clear Width`; `E-07 Slip Resistance (PTV ≥36 Wet Throughout All Circulation and Entry)` → `Slip Resistance`; `A-02 Acoustic Ceiling Panels (NRC ≥0.85) in Occupied Spaces` → `Acoustic Absorption at Ceiling`; and so through the list. A name states **what parameter is being determined**, never **what it was determined to be** | 28 of 93 names contain a digit; `evidence_cell_state` = 0 rows | An item name is shown to be the only carrier of a value nothing else records — then the value moves to a cell or a gap first, and the rename follows |
| **H2** | **Strip the prescriptive condition clauses from the 23 that carry them.** `E-02 Platform Lift (Where Full Passenger Lift Not Achievable)` → `Platform Lift`; `A-05 Carpet in Corridors and Occupied Spaces (Where VIS Navigation Maintained)` → `Floor Covering: Carpet`. A condition of use is a determination about *when* the provision applies — a cell's judgement, not a parameter's identity | `CLAUDE.md` §1: "not a prescription manual" | The owner rules that scope clauses are part of a parameter's identity |
| **H3** | **Record every stripped value before it is stripped.** Each of the 28 numbers is either (a) already in `jurisdictional_values` under its jurisdiction — E-08's ≥1200 is GB/ISO, already rows 72 and 77 — in which case the name was a duplicate of a correctly-held value and stripping loses nothing; or (b) **held nowhere else**, in which case it is an unevidenced assertion and its removal is the point. Classify all 28 into (a)/(b) **in the migration's own comment block**, so the act is auditable | E-04's "3600 mm" has zero backing rows — an instance of (b) | Any value is found to be (c): correctly evidenced, and held only in the name |
| **H4** | **Add the standing gate.** A registered check asserting no `items.name` matches `\d` outside a permitted set (ISO/EN/DIN standard designations in a name like `E-09 Tactile Walking Surface Indicators (ISO 23599:2019)` are a citation, not a determination — decide whether they stay). Level `advisory` on arrival, per house norm | The defect entered because nothing looked | The check cannot express the permitted set without an unbounded exception list |
| **H5** | **Audit the other seeded vocabularies for the same defect.** `populations`, `axes`, `access_needs`, `slugs`, `rooms` — does any name carry a determination? This is H1's method run twice, which is the lesson W5.1 taught at the cost of two missed rows | The extractor class was found once and stopped once (§W5.1) | No other vocabulary carries values in its names |

**Mechanism.** One data migration via `scripts/emit_data_migration.py` updating `items.name`;
mirrored regeneration of `parts/` and `site/` (both generated — regenerate, do not hand-edit);
one hand edit each to `index.html` (the hand-authored mockup) and `data/question-headings.yaml`.

**Blast radius, measured.** The full name strings appear in 51 rendered files (`parts/`, `site/`,
`index.html` — all generated except the mockup), 20 `references/` files (frozen corpus per
DR-2026-08-06 — leave, they are reference), **4 immutable migrations (must NOT be edited —
forward-only; the correction is a new migration)**, 1 code file, and 13 live files total outside
the generated and frozen sets.

**Why this is ahead of W0.1 and W5.1.** Same defect class — a number asserted without evidence —
but 28 instances instead of 8, and unlike the eight, **these are on the rendered surface**: E-08's
name ships in `parts/v10/part04.md:92` and across `site/populations/*.html`.

**H6 — the three off-frame populated tables.** DR-2026-08-06's frame enumeration authorises 18 of
the 27 populated tables; 6 more are infrastructure. Three are neither:

| Table | Rows | Disposition |
|---|---|---|
| `rooms` | 17 | Frame-adjacent typology the DR does not name. Owner ruling: register as frame, or reset |
| `weighting_profile` | 5 | Already W5.5 — five rows no code touches |
| `item_population_elaborations` | 3 | Columns `variant_distinction`, `spec_variant_a`, `spec_variant_b` — **synthesis output**, the class the reset existed to clear. Reset it |

---

## Wave 0 — Before anything else in the tooling layer. Three items, minutes each.

| # | Action | Evidence | Falsified if |
|---|---|---|---|
| **W0.1** | **Wire `scripts/audit/jurisdictional_divergence.py` into the registry at `informational`** — the level that already exists for a check whose exit code carries no verdict, which is the correct and honest reason it was quarantined on 2026-08-01 | Run unmodified at HEAD it prints `[candidate_conflation_or_error] 3 (WARN)` naming B-10, E-12, G-04, and exits 0. `test_jurisdictional_divergence` is meanwhile **registered, active and passing** in the `tests` battery | Its output appears in CI and names no defect |
| **W0.2** | **File the rows it names as W5.1 defects** — now **eight rows across five items** | see W5.1 | — |
| **W0.3** | **NEW — fix the detector's blind spot before trusting its all-clear.** `scripts/audit/jurisdictional_divergence.py:69` filters `WHERE value_numeric IS NOT NULL AND unit IS NOT NULL`. **Every NULL-unit row is excluded from analysis — and the extractor failure that manufactures class ordinals and years is precisely the failure that leaves `unit` NULL.** The detector's row filter is anti-correlated with the defect class it exists to catch. Add a sixth finding class `numeric_without_unit` listing all such rows (8 today, 4 after W5.1) | E-15's in-item spread is ×2021 — six times wider than the ×357 G-04 headline the detector *does* report — and invisible to it | The detector at HEAD names E-07 or E-15 (it does not) |

**Why Wave 0.** Every other item needs code or a decision. This needs a registry entry for a
script that already works and already knows about wrong rows. **The quarantine entry is
well-reasoned and honest; "not a gate" was simply read as "not run."** W0.3 is new because
clearing a WARN with a blind detector is how the next E-15 survives.

**The §6.5 collision, resolved.** `references/tooling-register.md` §6 item 5 makes quarantine
terminal *for retirement*, not for activation. De-quarantine to active is an established move
performed five times already, recorded in the registry's own comments (`claims_docket`,
`pmp_audit`, `reasoning_doc_citations_audit`, `validate_pydantic_schemas`,
`register_integrity_check`). The quarantine block is **removed and replaced by a comment** —
`run_checks.py --selftest` C1b fails an id present in both `checks:` and `quarantine:`.

---

## Wave 1 — The write path and the bootstrap. No decision required.

| # | Issue | Fix | Evidence | Falsified if |
|---|---|---|---|---|
| **W1.1** | FK check runs **after** `commit()`; the `except`'s `rollback()` rolls back nothing | **REPLACED — see below. The fix all four documents specify cannot work.** | `migrate_db.py:159-188` (cited as 161-183; drifted) | A violating migration leaves no row and no ledger entry |
| **W1.2** | `is_bootstrap = "BOOTSTRAP" in body[:500]` — the `--summary` a session types decides whether FKs are enforced | Delete the substring test **in both places** | `migrate_db.py:176` (cited as :174) **and an undocumented duplicate at :261** in the rebuild path | Probe A-3's payload is rejected under any wording |
| **W1.3** | A failed migration stays pending, is retried first forever, and voids everything behind it | `scripts/migrations/failed/` + print `N migration(s) not attempted`. **Not a `data_migrations` skip row** — `--rebuild` regenerates the ledger from files and would apply the abandoned migration anyway | `migrate_db.py:154-188`; `MIGRATIONS_DIR.glob("*.sql")` is non-recursive, so `failed/` is invisible to both paths | A failure at *k* leaves *k+1…n* attempted or explicitly skipped |
| **W1.4** | `next_gap_id` returns `GAP-1` on the empty table; `schemas/evidence_state.py:167` requires `^GAP-\d{3,4}$` | **`from scripts.db import next_gap_id`** — but the library function takes **no `conn`** and opens `GUIDEBOOK_DB_PATH`, while `assess_cell.py:491-492` **refuses the canonical DB**. A literal import silently reads the wrong database, and `assess_cell.py` is EXEMPT from `db_path_env_audit`, so nothing would catch it. **Give `db.py:next_gap_id` an optional `conn` parameter first** | `assess_cell.py:426-429` vs `db.py:149-158` | `assess_cell.py` completes against an empty `gaps` table, reading only `--db` |
| **W1.5** | **The documented setup command fails.** `pip install -r requirements.txt` → `Cannot uninstall PyYAML 6.0.1, RECORD file not found` | Relax to `PyYAML>=6.0,<7`; add `jsonschema>=4,<5`; delete the false sentence at `requirements.txt:4` | Reproduced in **three** independent containers. `ci.yml:215` and `:227` hand-install jsonschema. **CLAUDE.md §7 gives this as step one** | A clean container runs the documented command and gets a working environment |
| **W1.6** | CLAUDE.md §10 names `session_pointer_resolvable`, a check that does not exist | Name the dispatcher guarantee at `run_checks.py:217-238` **and name L04** — see below | grep → zero hits in `governance/`, `scripts/`, `.github/` | The named check exists |

### W1.1 — replaced. Why the agreed fix cannot work.

`scripts/emit_data_migration.py:201` wraps every emitted body:
`body = sql if args.no_transaction else f"BEGIN TRANSACTION;\n\n{sql}\n\nCOMMIT;\n"`. **The
migration script commits itself.** Python 3.11's `sqlite3.executescript()` additionally issues an
implicit COMMIT before running. By the time `executescript` returns, the data is durable —
so moving `foreign_key_check` above the runner's `conn.commit()` cannot meet this wave's own exit
condition, *"rejected with nothing written."* Four documents specified the four-line reorder;
none read the emitter.

**The fix that meets the condition: verify on a scratch snapshot, then apply.** Take a
`conn.backup()` snapshot to a tempfile, run the migration there, compare
`PRAGMA foreign_key_check` before and after, and only on a clean result apply to the real
database. This one block also subsumes W1.2's apply-path deletion and hosts W1.3's
remainder-print, so W1.1–W1.3 land as **one edit** to the same 35 lines.

### W1.6 — corrected. The dropped capability was not dropped.

All four documents state that the drift-reporting capability *"has no replacement."* **It has
one.** `scripts/tests/test_db_integrity.py:1063-1115`, check **L04** — *"sessions/LATEST-RESEARCH
gives citation_mining_session a subject"* — reads the pointer, queries the DB for the newest
session holding slug-linked Tier 1–2 sources, and fails when the pointer has drifted and the
pointed session holds zero subjects. It sits in the **blocking** `db_integrity` battery and is
documented at `check-registry.yaml:473`. It was created by commit `4fc6304` — *the same commit*
the sweep cites, whose message states the watcher's work was distributed, including *"pointer
drift vs the DB → test_db_integrity L04."* The sweep quoted the headline and not the message.

What is true: **L04 is dormant**, not absent. With `evidence_sources` empty it has nothing to
compare and passes regardless of `LATEST-RESEARCH` being seventeen days stale. Write that.

**Also in this wave:** guard the replay script; wire the registry's `deps:` field; repair
`check-registry.yaml:174`; fix `graph_audit.py:277`.

- **The replay script — R-01, ranked first in the register.**
  `scripts/migrations/session_2026_05_11g_replay.py:33` defaults to the **canonical DB**
  (`os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")`), does not import `_legacy_guard`,
  and replays a pre-reset JSON dump. It is the only `.py` among **347** files in the canonical
  migrations directory. Interim fix: import `assert_not_canonical` and make `--db` required.
  Permanent fix: W7.1. **Note the 20th file nobody counted:**
  `scripts/migrations/session_2026_05_11g_data.json`, the dump itself — retire both together.
- **R-05 recalibrated: "three unguarded direct writers" is one.**
  `scripts/migrate/init_database.py:18` hardcodes `data/db/guidebook.db` — a path that does not
  exist on disk — so it cannot touch the canonical DB. `scripts/migrate/phase_jv_appendix_a.py`
  contains **no sqlite reference at all**; it writes YAML to `data/jurisdictional_values/`. Only
  the replay script writes `data/guidebook.db`. (`phase_jv` still overwrites the dual-store YAML
  of the very table carrying the W5.1 false values — unguarded, but not a DB writer.)
  `_legacy_guard.py:46-60` is imported by exactly **7 of the 9** siblings, as recorded.
- **`deps:` — R-11.** `grep -n deps scripts/run_checks.py` → nothing. Missing pydantic presents
  as **five blocking `ModuleNotFoundError` failures**, reproduced live during revision 4's own
  re-derivation. Fix: verify each selected battery's declared deps before running anything;
  abort with the install command and **exit 2** — the runner could not run, distinct from a check
  failing. Also correct `check-registry.yaml:172` — `tests: {deps: []}` is false; three of the
  ten tests import pydantic transitively.
- **`check-registry.yaml:174` — R-12.** Still unquoted at HEAD, still parsing to
  `{'deps': ['pydantic'], 'description': 'Decision protocol', 'doctrine recheck': None,
  'adversarial-use.': None}`. Now reported in **five** documents, one line. Quote the string.
  Add a `--selftest` assertion that every battery has exactly the keys `{deps, description}` — a
  successfully-parsing wrong shape is invisible to the current C1–C7.
- **`graph_audit.py:277` — R-13.** Crash is in the **selftest path only**; the plain audit exits
  0. Guard leg 3 with a loud `[SKIP] … NOT-TESTABLE` that does not append a fabricated pass.

**Exit condition:** re-run the corridor walk's stage 4a ordering probe and stage 9. The probe must
be rejected *with nothing written*, and `assess_cell.py` must complete.

---

## Wave 2 — Rulings that gate everything after them

### D-A · Is value determination a machine stage or a human one? *(D-METH)*

`assess_cell.py:559` writes the literal `None, None, None` for `value_min`, `value_max`,
`value_unit`, unconditionally, on every path; it is the only corpus writer of
`evidence_cell_state`. No code path runs from N extracted values to one value —
`source_value_extractions` has zero writers, and convergence status is hard-coded
`pending_assessment` with the comment *"no rule exists for grading value-level convergence."*

**Recommendation: human, declared** — in `governance/pipeline-contract.yaml` under `judgment`,
with an input contract (a value row is written only by data migration, only onto a cell whose
state is `stated`/`provisional` with non-empty `governing_refs`, and only when every extraction
it rests on is reachable via `cell_source_links`), an acceptance condition (`value_unit` non-NULL
wherever `value_min`/`value_max` is; `value_min <= value_max`), and an attestation naming the
cell and the `doctrine_sha` it was judged under. `check: null` — the file's own
DECLARED-BUT-UNENFORCED convention. **Note the dependency:** naming a cell as an attestation
artifact requires W3.3's schema widening, or the criterion names the migration file instead.

### D-B · The derived-value marker — ratified, zero repository presence

Triangle ▲/◭/△ parallel to ●/◐/○; shape for derivation, fill for evidence strength. Verified at
HEAD: **zero glyph hits** across `governance/`, `schemas/`, `scripts/`, `decisions/`,
`references/`; no column; no validator; no renderer. **And no DR records it** — it exists only as
quotations in `workplan/` files, which W7.12 proposes to retire. **Write the DR** as part of W3.1.

The open question: **does a derived marker's fill inherit its input evidence's strength, or cap
one band below?**

- *For inheritance:* the ratified scheme separates the dimensions — shape for derivation, fill
  for strength. Capping encodes derivation twice and breaks the ●/◐/○ parallel.
- *For capping:* `governance/evidence-architecture.md:170` anchors the directness layer in
  GRADE's indirectness domain, and GRADE downgrades one level for indirectness. The repo's own
  precedent agrees — `assess_cell.py:35-37` caps any partially-assessed dimension at
  DOWN-WEIGHTED, *"never silently full-match."*
- *A resolution the vocabulary already supports:* key it to `synthesis_method_indicator` —
  `direct` inherits; `inferred` caps one band with `inference_basis` mandatory; `consensus` takes
  the band the convergence rules give the underlying set.

### D-C · Branch protection — **PREMISE DEAD. `main` is already protected.**

Verified twice at HEAD via the authenticated GitHub API:
`{"name":"main","sha":"3c936db85ed…","protected":true}` — and it is the only protected branch in
the repository. **Every document asserting otherwise is now stale in the opposite direction of
every prior check:** CLAUDE.md §0 and §7, `check-registry.yaml`'s NB, `references/tooling-register.md`
F2 and §6.7's preamble, this plan's own D-C, and the register's sequencing step 8.

**What remains is a configuration audit, not a switch.** The `protected: true` flag is returned
for anything from "require a PR" to the full nine-job set; the protection endpoint is not
readable from a session. Two of §6.7's three traps are now **live questions**:

1. **Is `Classify change (work kinds → batteries)` in the required set?** A GitHub job skipped by
   an `if:` condition reports as **passing** for required status checks. If only the battery jobs
   are required, a broken classifier skips every battery and the PR goes green on checks that
   never ran.
2. **Is `DB integrity (content checks)` in the required set?** It must not be — but note its
   original ground has changed: `test_db_integrity` is now **70/70 green** at HEAD, not red. The
   replacement ground stands: roughly 30 of the 70 reference only empty tables, so requiring it
   today locks in a vacuous green. It goes in after R-15's vacuity-warrant work.
3. Reviews must not be required on a single-author repo, or admin bypass must stay on.

**Also now retro-binding:** the standing rule *"no check promotions in the same window as branch
protection"* applies immediately — the window is open.

---

## Wave 3 — Free today, expensive after the first content batch

Every table named is empty. **Target order:** `source_value_extractions` →
`evidence_population_match` → `reasoning_doc_citations`; stages 8 and 9 each read all three.

| # | Fix | Why now |
|---|---|---|
| **W3.1** | **Implement the derived-value triangle.** Glyph and fill semantics into `tier-system.md` §5; **a `synthesis_method_indicator` column** — *not* `synthesis_method`: `armature_v4_resolutions.md:104` reserves that exact name for a **different** ratified vocabulary (`narrative`/`quantitative`/`mixed`) and gives `synthesis_method_indicator` at :110 for `direct`/`inferred`/`consensus` — plus `inference_basis`; a renderer that emits it; **and the DR that ratifies it** | Ratified doctrine, zero implementation |
| **W3.2** | **Split `evidence_population_match.target_population`** into `target_population_code` (FK, nullable) and `target_population_note` (free text, `NOT NULL` retained — R13 needs richness on the served side). **Correction: the 64 archived rows cannot be "hand-migrated"** — importing them violates the FK to an empty `evidence_sources` and contradicts DR-2026-08-06 §4.1 (*"Research resuming does not restore these rows"*). Instead: hand-classify them into a `(code, note)` worksheet committed as a DR appendix, proving the split carries all 30 values | **22 of 30 distinct pre-reset values are prose**, re-verified — e.g. *"Hardware operating force threshold for UPL/PAIN populations including RA"*, which is not even a population. A bare FK passes trivially on 0 rows and forbids 22 of 30 historical values |
| **W3.3** | **Doctrine binding on `evidence_cell_state`** — a `doctrine_sha TEXT` column with a 7-hex GLOB check, stamped by `assess_cell.py` — **or** widen `attestation.schema.json:13`'s `artifact` pattern so an attestation can name a row | Leg 4 of DR-2026-08-06's four-leg promise. Legs 1–3 have columns; leg 4 has nothing |
| **W3.4** | **`CHECK (evidence_type='co1' → tier=1)`** by table rebuild (SQLite cannot `ADD CONSTRAINT`), or a BEFORE INSERT/UPDATE trigger | Doctrine's most distinctive commitment is defended by nothing. `validate_source_co1_fields()` at `validate_evidence_state.py:76-121` scans `data/sources/*.yaml`, which does not exist — and its own comment admits two dormant bugs. **Check first:** `SELECT COUNT(*) FROM evidence_sources WHERE evidence_type='co1' AND tier<>1` on the archived DB |
| **W3.5** | **`assess_cell.py` must write `cell_source_links`.** Exact insertion point: **after line 573**, before line 575, where `cell_id` and `det["governing_refs"]` are both in scope. `role='governing'` is the only value the DDL's CHECK admits | The trial's first determination carried 7 governing refs and 0 junction rows, and `spec_page.py:217-223` therefore rendered *"records no governing sources … treat it as unevidenced."* **The honesty mechanism misreports** |
| **W3.6** | **Render the value, the marker band, and the gap link.** `spec_page.py:74-77` omits `value_min`, `value_max`, `value_unit` **and** `gap_register_id`. Refinement: the absence of *per-source* markers is deliberate and doctrinally argued (`citation()` docstring, :134-138) — the marker belongs at **cell level**, where the live `v_best_practice.strength_band` already supplies the band | Depends on **W3.1** and **D-A** |
| **W3.7** | **Populate `access_needs.typical_stakes`** — 16 of 17 NULL; only `A-TRIGGER` is graded. The three ratified values are `safety-critical` / `exclusion` / `friction` | `A-SIZE` and `A-REACH`, the two that reach corridor width, are both NULL. **The sixteen grades are judgment acts** — they set which parameters must be specified at the accommodating end — and need owner review plus an attestation |
| **W3.8** | **Give the six remaining stage-7 outputs a writer, or declare them hand-authored** in `pipeline-contract.yaml`: `spec_value_probes`, `item_bpc_links`, `cell_source_links` (discharged by W3.5), `extraction_population_links`, `case_studies`, `economics_entries` | **R12 instructs sessions to write `economics_entries` and no tool can.** (Correction: the contract is R1–**R15**, not R1–R13) |
| **W3.9** | **One locator representation instead of three** — the identical 16-column block in `jurisdictional_values` (16 of 32), `source_value_extractions` (16 of 49), `reasoning_doc_citations` (16 of 34). **Recommendation reversed to Candidate B** — see below | Free while empty, except `jurisdictional_values`' 109 rows |

### W3.9 — the shape decision, resolved against the plan's own test

- **Candidate A**, a `locators` table keyed `(owner_kind, owner_id)`: **FAILS.** `owner_id` is
  polymorphic, so it **cannot be constrained by a foreign key** — the identical construction the
  §2.1 retraction refused. It also forfeits three addable `locator_scheme` FKs.
- **Candidate B**, shared *definition* in place: one `LocatorBlock` Pydantic mixin inherited by
  the three models, one canonical DDL fragment, a `v_locators` UNION view, a small audit
  asserting via `PRAGMA table_info` that the three blocks stay column-identical, **plus the
  scheme registry** `locator_schemes(scheme PRIMARY KEY, …)` FK'd from all three — sized for the
  **~24 observed families, not 12** (the 2026-08-09 document's own count; a registry sized for 12
  fails closed on real input).

**Candidate B adds three enforced keys and destroys none. Take it.** This revises W3.9's net from
"−32 columns" to **−0 columns, +1 vocabulary table, 16 definitional copies → 1.** The owner's
standing constraint — *there are no limits on table sizes* — removes the only argument for A.

---

## Wave 4 — The adjudication apparatus

Gated on **D-A**. Carried from PR #93 unchanged: W4.1 a fourth directness dimension
(`claim_manoeuvre`/`claim_construct` + `construct_directness()`); W4.2 device-class
stratification; W4.3 `derived_from_cell_id` + `derivation_rule` with `derivation_sha` extended to
hash upstream cell ids; W4.4 extend `access_needs.design_obligation` to cells, curating any new
access-need code **from** `AX-WHM`, never as a coined umbrella; W4.5 `conflict_kind` with an
FK-keyed target pair per kind.

---

## Wave 5 — Corpus defects, independent of everything above

| # | Defect | Action |
|---|---|---|
| **W5.1** | **One extractor failure — now eight rows across five items.** It takes a number from anywhere in the value text and stamps the column's unit on it. `jv 40` E-12/ISO `81.0 mm` ← "EN 81-41" · **`jv 104` B-10/GB `54.0 Hz`** ← "EN 54-23", against sibling rows recording the ≤2 Hz photosensitive-epilepsy ceiling · `jv 46` G-04/FR `1300.0 m²` ← "1300×1300mm" · `jv 42` G-04/GB `1500.0 m²` ← "2200×1500mm" · `jv 16` E-07/DE `9.0` NULL-unit ← "R9–R13" · `jv 17` E-07/AU `3.0` NULL-unit ← "P3–P5" · **`jv 106` E-15/GB `2021.0` NULL-unit ← the YEAR in "Building Regs 2021", on a row whose text states the real quantity `Min Area: ≥12m²`** · **`jv 107` E-15/US `1.0` NULL-unit ← "Supplement 1 (2024)", an edition ordinal** | Correct all eight by compensating migration, keyed on the natural key `(item_code, jurisdiction, standard_name)` plus a current-value guard so re-application and reordering are no-ops. **Corrections are NULL where the text states no quantity** (jv 40, 104, 16, 17, 107), the stated figure where it does (jv 46 → 3.6, jv 42 → 4.7, jv 106 → 12.0 m²). **Reconcile the five shadow YAMLs in the same PR** — `data/jurisdictional_values/a-8_b10.yaml`, `a-9_e15.yaml`, `a-13_e07.yaml`, `a-18_e12.yaml`, `a-19_g04.yaml` still carry all eight bad numerics. **Do not ship without W5.6** |
| **W5.6** | **Pairs with W5.1.** `migration_reproducibility` compares `PRAGMA user_version` plus `COUNT(*)` on six tables at `scripts/audit/migration_reproducibility.py:55-63`: **93 of 4,245 rows, 2.2%.** `jurisdictional_values` is not among them | Widen to all non-exempt tables (**4,239 rows / 64 tables, 99.9%**) by dynamic enumeration. **Three co-edits:** the selftest's "missing tables are skipped" case inverts to "absent on one side is a MISMATCH"; the registry note rewrites its SCOPE paragraph; CLAUDE.md §0 rule 4 drops "as does anything in the other 55 tables". **See W9.1 — this has an owner gate the plan dropped** |
| **W5.2** | E-12's six values are all **platform-lift** specifications under an item named *Entrance Landing and Manoeuvring Space*. **Three facts no document assembled:** the source YAML is titled `Platform Lift Dimensions` (`data/jurisdictional_values/a-18_e12.yaml:2`); **`E-02` "Platform Lift" already exists as an active item**; and it has **zero** `jurisdictional_values` rows | Owner ruling. If E-12 does not cover lifts: `UPDATE jurisdictional_values SET item_code='E-02' WHERE item_code='E-12' AND source_section='A.18'` — FK-safe, E-02 exists. **Hold pending Wave H** — filing values under `E-02 Platform Lift (Where Full Passenger Lift Not Achievable)` files them under a name that is itself a specification |
| **W5.3** | `CORRIDOR-W.md:9,16,18` asserts **≥2440 mm** for DEAF signing pairs; E-08's *name* asserts **≥1200 mm**. **Wave H dissolves this as stated:** the ≥1200 exists only in an item name, and the 2440 carries **no source citation anywhere in its 23-line file** — `[UNVERIFIED-QUANT]`-shaped | Reconcile as two unevidenced assertions, not two rival claims. Second-order ruling stands: CORRIDOR-W was reclassified NOT-A-CONFLICT solely on the DEAF-vs-NDV/AUT sensory-load axis (:9-16) then declared retired as a **domain** (:20,:23). **Retirement verdicts should be per-axis**, and a domain file's banner should name the axis it adjudicated. Depends on **W4.5** |
| **W5.4** | **STALE AT REVISION 3's OWN SUBJECT.** Running the real `check_3_rule_resolution` over all 76 attestations at HEAD: **4 failures, 8 distinct unknown identifiers, and `integrity-protocol` is cited by ZERO attestations.** Commit `bb1a836` replaced it with `structure-auditor` and logged a forward-only `reattestation[]` entry — and `git merge-base --is-ancestor bb1a836 adfb675` returns **true**. The register's "4 committed attestations cite it" was a whole-file string grep hitting artifact paths and `bias_direction` prose; the real count was **1** | **(a)** The schema question is **already answered**: `references/skill-registry.md:22-35` states that CHECK 3 resolves against the registry **or** `EXTRA_RULE_IDS`, which is *"the ratified extension point"* per DR-2026-07-13. The live decision is only whether the 8 residual governance-rule names are admitted there (recommended — 6 of 8 name real governance objects) or corrected forward. **(b)** Register `integrity-protocol` and `supersession-audit` in `skill-registry.md` — but on **completeness grounds, not to clear a red check**: at HEAD it clears zero failures. **(c)** Add `--corpus` to `adherence_log_audit.py` and register `attestation_corpus` advisory with `EXAMINED:` — today every attestation check is diff-scoped (`:551-553`) and corpus validity is established by nothing (W6.4) |
| **W5.5** | `weighting_profile`: 5 rows, named by three pipeline stages, **touched by no code** — and `governance/evidence-architecture.md` I3 binds renders *"under any weighting profile"* | Owner ruling. **Retiring it is a doctrine edit** (amend I3), not dead-code removal; wiring it grows the renderer an audience dimension. Pair with the **11 unread views**: `v_code_floor_only`, `v_coverage_priority` (**7,210 rows, no reader**), `v_item_extractions`, `v_item_provenance`, `v_pending`, `v_pmp_latest_walk`, `v_registry_duplicate_descriptions`, `v_source_admission`, `v_source_reach`, `v_source_reach_all`, `v_value_independence` — **wire-or-retire ruling, not a cut**; several are declared query paths and `v_value_independence` is contract-cited |
| **W5.7** | **RE-DERIVED AND CONFIRMED** — the one entry the register never verified. `spec_page.py:73-79` and `population_page.py:75-81` both omit `gap_register_id`; a `pending` cell renders as the bare word (`spec_page.py:197`) with no `[BEST-PRACTICE-PENDING]` and no gap link; both determination tables iterate cell rows only, so **a population linked to the item with no cell is absent and unmarked**. `governance/mission-and-epistemics.md:120`: *"Silence on evidence-thin populations is not the default."* A working implementation exists at `pilot_renderings.py:214-236` and is **wired to nothing** | Add `gap_register_id` to both SELECTs; render pending with marker and link; build the table from `item_population_links LEFT JOIN evidence_cell_state`. **Refinements:** the population is not erased from the *page* (a separate "Applicable populations" table renders it); the all-empty case is honestly bannered; so the breach is **latent and fires on the first partial determination**, in exactly the thinnest-evidence populations |
| **W5.8** | **The nine standing advisory failures**, each re-derived, each with its resolution level. **Do not clear by silencing** | `validate_reasoning` — content (**and the registry note understates: ~14 findings, not one missing section**) · `validate_pydantic_schemas` — owner decision (does `schemas/*.py` mirror SQLite or the YAML layer?) · `retired_vocabulary` 69 — text fixes · `site_pages_fresh` 12 — regenerate · `research_dod` R1 — R-15 warrant · `test_verification_pipeline` 15/18 — R-15 warrant on the three G-legs · `test_directness_2_2` — **green standalone, red dispatched**: `run_checks.py:389` sets `GUIDEBOOK_DB_PATH`, so the live-smoke leg runs against the empty canonical table instead of skipping; the registry note's *"(it is, in CI)"* is wrong · `test_graph_audit` — R-13 · `register_integrity_check` — R-14, **cause now derived**: `evidence_cell_state` = 0 rows makes the completeness set-diff vacuous and `:182`'s `if db_rows:` disables the doc→DB direction. Plus `parts/v10` **stale in all 15 files with no `--check` mode to gate it** (the one place a *new* check is the resolution) and `room_page.py` querying **four** non-existent tables (not six) |

---

## Wave 6 — Method

| # | Issue | Status |
|---|---|---|
| **W6.1** | The trial has a 105-action verbatim log; the review pronouncing verdicts had none | `walk_harness.py` **DONE** |
| **W6.2** | The review cited no log identifier | **DONE** |
| **W6.3** | A syntax check passed for a test — `ast.parse()` is `EXAMINED: 0` wearing a green tick | **DONE** for the harness |
| **W6.4** | `attestation_evidence` is advisory *and* diff-scoped | folds into **W5.4(c)** |
| **W6.5** | E-08 was chosen for realism, and realism made it contaminating | pending |
| **W6.6** | **A regex classification is a candidate list, never a finding.** Now with six instances: 14 unknown rule ids (really 9); 77 "avoidable" f-string interpolations (really ~0, security-shaped); a table-type classifier putting 56 of 66 tables in one bucket; a source document nearly dropped for using prose headings; **"4 attestations cite `integrity-protocol`" (really 1)**; and revision 4's own 82-file "unreferenced" list (really 26) | → `references/project-standards.md` |
| **W6.7** | **Before building a detector, check whether one exists** — and check the quarantine list first | → same ledger |
| **W6.8** | **A convention-vs-enforcement gap detector**, with the confound stated: enforcers may have gone to conventions already judged important, so ~75%-vs-~50% is *consistent with* the spectrum working, not proof. **If it cannot be expressed as a registry check, that is evidence not to build it** | → same ledger |
| **W6.9** | **Every supersession publishes a loss-audit** | → same ledger; §0.4, §0.6, §0.7 are the instances |
| **W6.10** | **A correction that does not propagate is not a correction** | → same ledger; enforced by W8 |
| **W6.11** | **NEW — re-derive facts, not only arithmetic.** Revisions 1–3 each recomputed their predecessor's sums and inherited its observations. Revision 4 re-ran the observations and lost 31 claims, four of them premise-level. A successor that checks only the arithmetic launders its predecessor's errors through a clean audit trail | → same ledger |

**All six rules land in `references/project-standards.md` in its `RULE:`/`CONDITION:`/`ACTION:`/
`DATE:` format, with one paired Decision record** (RULE A12's CS8 requires the pairing). They must
not land in a workplan document again — three of them already lived there and died.

**And W6.6–W6.11 are what Wave L makes mechanical.** Each maps to a ledger block: W6.6 → the
`cull_candidates_raised` / `cull_candidates_adjudicated` split; W6.7 → `detector_checked` +
`detector_search_command`; W6.9 → the forward-only `supersedes:` + `loss_audit:` pair; W6.10 →
`prose_orphaned` and the `deliberately_not_swept` reasons; W6.11 → the `intent_written_at` /
`executed_at` delta. **A rule in the ledger is a rule a session cannot forget to apply**, which
is the whole argument for the enforcement spectrum (CLAUDE.md §2) applied to method rules.

---

## Wave 7 — Consolidation

Two folds proposed during the sweep were **retracted**. **The surviving test: a fold must not
destroy a key, and identical column shape is not identical meaning.**

| # | Action | Net | Gate |
|---|---|---|---|
| **W7.1** | **Retire the one-shot importer layer** — `scripts/convert/` (13), `scripts/db/` (3), `init_database.py`, `phase_jv_appendix_a.py`, the replay script **and its JSON dump**. Re-verified exactly: **19 files, 6,074 lines** | **−19 / −6,074.** Closes the one real unguarded writer | **owner** — retirement is guardrail 4; the plan's "Gate: none" contradicted its own Appendix B. **Caller sweep:** `check-registry.yaml:1201-1205` (names `version_retrofit.py` inside an *open owner question* — retiring it executes one branch), `schema_reference_drift_audit.py:18`, `db_path_env_audit.py:23-24`, `CLAUDE.md` §7, `_legacy_guard.py:23-25` |
| **W7.2** | **Merge eight of the ten single-invariant audit scripts** behind `scripts/audit/invariants.py --check <id>`. Registry dispatches by argument in **27 of 65** entries. `table_connectivity.py` and `pre_rehab_banner_audit.py` are quarantined and stay | −7 files, ~−150 lines | **Drop first if the result feels like `db.py` again.** Sequence *after* W7.4 |
| **W7.3** | **Five FK-safe folds G1–G5.** **Correction: "DDL only, all empty" is false for four of five.** Archived rows: `bpc_metadata` 83 · `citation_mining` 183 / `source_slug_links` 1,011 · the three vocabularies **3/3/2 live** · `search_coverage` 4,960 / `search_languages` 1,558. Only G4 is empty in both. **No inbound FKs to any fold target** (verified) | −6 tables | DDL + one 8-row data migration (G3). **G2 edits a blocking gate's DR-synced contract** — `citation_mining` is in `CORE_INVARIANTS`; needs a DR amendment |
| **W7.3-G5** | **CHANGED — `search_coverage`/`search_languages` are frozen by design, not fold candidates.** `db.py:316-325` raises `FrozenGridError` on any write; coverage's live mechanism is `search_executions` + the `v_coverage_*` views | −2 (retire) or −1 (fold) | **Recommend retire-to-W7.9 instead.** Folding two superseded frozen tables into a new frozen table is motion without progress |
| **W7.4** | **Resolve `scripts/db.py`** — 1,889 lines, 43 functions, **zero importers, zero subprocess callers** (re-verified by AST, not grep) | 0 or −1,889 | **owner. Recommend ADOPT.** Two facts harden it: DR-2026-08-06 §4.1 names `db.py log-search` as the resumption discipline, so deleting it strands an ADOPTED decision; and it carries write-time H05/H07 enforcement and the `FrozenGridError` refusals. **The delete branch also carries a 12-file caller sweep** — CLAUDE.md §4:169 plus 11 `skills/*_SKILL.md` |
| **W7.5** | **One `governance/frozen-surfaces.yaml`**; `.ignore` and `validate_cross_refs.REFERENCE_ONLY` (`:245-254`) generated from it. **Correction: "the DB returns 0 rows" is wrong** — a live grab-bar query returns **10 rows, five of them real code values** in `jurisdictional_values` (US 838–914 mm, GB 680, DE 850, AU 800–810). What returns zero is *evidence*. **Scope note:** the declaration must carry "cited-as-of-date" semantics for `decisions/` and `attestations/`, which hold 81 REF-IDs and 27 GAP-IDs and are forward-only | net 0 files | owner (`.ignore` scope is owner-gated by its own header) |
| **W7.6** | **Retire `references/global-reference-registry.{md,json}`** with a redirect stub. Line 6 and line 601 verbatim; 531 ids, **0 live**, 496 pre-reset, 35 that never existed, 367 missing. **The authority sentences go regardless of where the file lives** | −2 files | owner. Caller sweep enumerated: `convert_sources.py:6,97,293,313` · `db/migrate_all.py:841-842` · `conceptual-model.md:107` · `citation-tagging-protocol.md:9,17,100` · `phase-b-handoff.md:229,250` · `claim-reference-join.md:162` · `working/evidence-migration/registry-reconciliation.md:6` |
| **W7.7** | **One banner on all per-slug BPC files** — **86, not 85**: the census misses `references/bpc/thermoregulation-built-environment.md`, a full synthesis file sitting flat in the root where `validate_bpc.py:79-85` silently exempts it. **The 16 unbannered files are enumerated** in the frozen-corpus dossier | — | owner. **`pre_rehab_banner_audit` is RED on 68 slugs, not the 6 its quarantine note claims** — the reset emptied `bpc_metadata` underneath its DB-side invariants. Must declare `EXAMINED:` with `min_items` |
| **W7.8** | **Generate `workplan/INDEX.md`** — date-sorted, reset-relative status column, wave ids **and register ids**, registered for freshness like `context_map_fresh`. **74 files, 31,338 lines at HEAD** — the plan's own 31,189 went stale inside revision 3 | +1 generated | none. Note `workplan/deprecated/` (16 files) is outside `.ignore` |
| **W7.9** | **Cut `situations` and `external_root_registry`.** 0 rows live *and* archived, both verified | −2 tables, −1 view | owner, **last**. **Two corrections:** `v_root_id_conflicts` queries only `source_value_extractions` and **survives the cut**; the view that breaks is **`v_value_independence`**, the pipeline contract's cited H1 mechanism — making this partly **D-METH**. And `situations` is named in **five** governance documents including `RATIFICATION-RECORD-2026-07-21.md:32`, and is the native Co-1 entity — **DG-NON exposure the ledger did not flag** |
| **W7.10** | **Add `disposition:` to the quarantine schema** — not-a-gate / vacuous / red-with-findings / wrong-venue — plus `exit_condition:` on the promotable ones. **Correction: 15 carry `status: quarantined`, not 16**; a sixteenth carries a distinct `vacuous` status the proposal did not notice. **And `validate_conflicts` — the *live* plural validator — is itself quarantined**, contradicting sweep §1.7a (its own §1.6 table is right) | — | none. Sequence after W0.1 (membership 15→14) |
| **W7.11** | **Two unregistered surfaces.** `references/methodology/` un-finished split (containments re-derived: 98% / 91% / 93% / 85%); `working/` — 39 files, 1.1 MB, **188 REF-IDs of which 173 resolve pre-reset, 0 live, and 15 in neither**. Note `working/taxonomy/staged_schema_functional_axes.sql` is named by live doctrine — not uniformly dead | — | owner |
| **W7.12** | **Consolidate seven documents to four.** Keep this plan, `consolidated-review-and-plan.md`, `consolidation-sweep-and-adversarial-pass.md`, `per-stage-table-anatomy.md`. Retire the other three **after** W8's porting pass | −3 files, ~−900 lines | owner. **W8 first — non-negotiable** |
| **W7.13** | **Rename the consolidated review's Class IDs** to a non-colliding prefix. **`RR-` verified free repo-wide**; `CR-`, `RV-`, `CC-` and every single letter are taken. Every occurrence enumerated in the hygiene dossier, with one exclusion: **`consolidated:182`'s `rem C1` is the remediation register's C1 and must not be renamed.** G1–G5 are **out of scope** — they *are* cited externally (per-stage 79, 92, 109, 145, 250-252; this plan) so the "cited nowhere" premise fails for them | — | none |
| **W7.14** | **IMPOSSIBLE AS WRITTEN — drop or convert.** `scratchpad/stages.json` and the six siblings **never existed in the repository**: `git log --all --diff-filter=A -- '*stages.json'` returns nothing, and the authoring session's container is gone. The preservable content must be **re-derived** from its committed source, `2026-08-11-remediation-and-pipeline-anatomy.md` Part 2, and committed as e.g. `references/pipeline-stage-tables.json` — a new extraction, not a preservation | +1 or 0 | none. **Standing lesson:** evidence that lives only in a session container is not preserved by naming it in a workplan |

---

## Wave 8 — Document hygiene: port the unique content, then correct the stale text

**The precondition for W7.12.** Verified: `git diff adfb675 HEAD -- workplan/` shows the six
source documents are **byte-identical** to the state revision 3 cited — so every drifted line
number below was **wrong at derivation**, not moved by the merge.

| # | Document | Action |
|---|---|---|
| **W8.7** | **All six, plus one section marker — the first action in the plan.** The header text, adapted from the register's own Part 5 proposal (lines 254–258, never applied): `> *Finding statuses and figures in this document are superseded by `workplan/2026-08-12-resolution-plan.md` (Wave 8 · Appendix A). Its reasoning and evidence stand.*` Insert after: register **L10**, consolidated **L10**, sweep **L11**, ledger **L12**, pr93 **L8**, per-stage **L11**. The seventh is a Part-3 supersession marker in the sweep after **L463** | seven one-line insertions |
| **W8.1** | `reconciled-findings-register.md` — **port** §0.2 (**37–51**, cited 37–52) · §2.1 (**152–173**, cited 152–174) · Part 6 (**282–290**, exact). **Correct** R-07 at **L85** (the 27× claim → *latent, not published*) and R-24 at **L138** (**now to the revision-4 numbers: 4 of 76, 8 identifiers, `integrity-protocol` cited by zero** — not the 9-identifier framing revision 3 planned to write). Banner Part 4 after **L220** | retire with stub |
| **W8.2** | `pr93-reconciliation-and-shared-code.md` — **port** the R↔W cross-map (**27–36**, cited 27–37) into §0.3 (**done in this revision**). The 60-identifier port is **already satisfied** at this plan's W5.4. **Correct** Part 3 at **L237–239**, which announces register edits that were never made | retire with stub |
| **W8.3** | `fold-or-cut-ledger.md` — **port** Part 1 (**35–51**) · §2.6 (**191–192**, cited 192–195) · Part 4 (**223–229**) · Part 5 (**258–279**) · §7.2 (**338–383**). **Correct** L110–111 (−9→−6 should be −9→−3) · **L122** — *the heading is at 122, not the cited 124* · L304 and L306 (the closing paragraph still states pre-retraction figures) · L243–252 (proposes retiring two quarantined scripts while L228 says quarantine is terminal) | retire with stub, **or** keep as a fifth document with a banner |
| **W8.4** | `consolidated-review-and-plan.md` *(keeper)* — **the −3 rows are at L214–215, not the cited 216–217.** Correct to G1–G5's −6; L403 (−18/−5,850 → −19/−6,074); **L410 and L481–482 → 107, not the "105" this plan previously specified** — 105 inherits the −9 audit merge W7.2 revised to −7; **L467's "−9 files"**, **L473's undefined `G6`**, and **L206's "now 69 and ~29,000"** were all missed by revision 3. Reduce Part 3 (**239–301**) to a pointer — today two documents both present themselves as the plan. **And the five→six→eight propagation:** "five false values" is live at L26, 30, 75, 142, 160, 235, 417, 494–495 | keep, corrected |
| **W8.5** | `consolidation-sweep-and-adversarial-pass.md` *(keeper)* — Part 3 (**463–492**) marked superseded; **plus five factual corrections**: §1.1's "the DB returns zero rows" (it returns 10), the grab-bar count (now **126**, four of the new hits being PR #94's own documents), exempt_paths "69 entries" (measured 19 global / 163 per-entry / **62 distinct**), §1.9's "no replacement" (**refuted — L04**), §1.7a's "both registered" (**`validate_conflicts` is quarantined**), §1.5's "thirteen times / eight rows" (measured **21 mentions, 10 section-anchored; 10 rows + 1 comment**) | keep, banner + corrections |
| **W8.6** | `per-stage-table-anatomy.md` *(keeper)* — state the `sqlite_sequence` convention at **L11** and **L265**. **Plus: the unwritable-output count is 14, not 13** — `item_population_elaborations` is marked ⚠ NO WRITER in the document's own Stage 2 table and omitted from its own list. And the five→eight propagation at L81, L166, L246 | keep, corrected |
| **W8.8** | **NEW — the seventh stale document Wave 8 never covered.** `sessions/handoff-next-session.md` says *"PR: #91 (open)"*, `HEAD at handoff: 804a4bf` (five merges stale), and points at the remediation anatomy as "the plan to work from." **`.ignore` hides `sessions/**`, so it is invisible-and-wrong** | one-line fix, same class as W8.7 |

**W8 sequencing:** W8.7 first, then W8.1–W8.3 porting, then W8.4–W8.6 corrections, then W7.13
renames, then W7.12 retirement. **Retiring before porting is the one ordering that reproduces the
defect this wave exists to fix.**

**Commit hygiene:** `workplan/` is not a synthesis path — `check_doctrine_token.py:46-48` defines
`SYNTHESIS_RE = ^(references/bpc-reasoning|references/connection-reasoning|decisions|sessions)/`
— so no doctrine token and no attestation are owed. Format per `check_commit_msg.py:57`. **One
trap:** a commit that also updates `sessions/LATEST` touches a synthesis path — keep the pointer
update in its own commit with the token.

---

## Wave 9 — The dropped inheritance

Two ratified obligations and one gate that no wave carried. Found by re-reading the source
documents PR #94 cited but did not include.

| # | Item | Why it is here |
|---|---|---|
| **W9.1** | **W5.6 lost its owner gate in transit.** The locator-probes document (Part 4 fixes 1–3) and the remediation register's **D2/D3** make widening the blocking `COUNT(*)` **dependent on an exemption ruling first**: `url_verification_runs` is written by the bi-weekly `verify-urls.yml` cron and is **not** on DR-2026-05-28's exempt list, so a widened blocking gate **goes permanently red on a legitimate write the next time the cron runs.** The register carried the gate; this plan's W5.6 dropped it | **Executing W5.6 as written manufactures a permanently-red blocking gate.** Fix: a one-line DR extending the exemption to `url_verification_runs` (same class as `pipeline_runs`) *before* the widening |
| **W9.2** | **DR-2026-08-06 §4.4 — the frame's two missing vocabularies.** Languages and jurisdictions are two of the four quarters of the owner-defined frame and **neither has a canonical table**; jurisdiction is free text (`UK` 88, `GB` 5, `GB-SCT` 1, plus 12 compounds). The DR states: *"Building those two vocabularies is the first frame work after this reset."* **No wave item exists** | A ratified obligation the plan silently omits. Belongs in Wave 3 — cheapest while empty |
| **W9.3** | **The locator-probes Part 4 fix list, re-enumerated.** The register folded it into R-27 "rather than re-enumerated"; nothing since re-enumerated it. Eight items: (1) the exemption ruling → W9.1 · (2) promote `migration_reproducibility_deep` · (3) widen `COUNT(*)` → W5.6 · (4) Pydantic model for `reasoning_doc_citations` — **DONE** · (5) `CHECK` on `verification_status` — **owner, and register D4 already ruled DEFER; the plan neither carries nor re-opens it, which is a silent drop** · (6) **correct migration 053's committed-header numbers** ("85/9/3" sums to 97 ≠ 109) via a follow-on header, never by editing the migration · (7) `EXAMINED:` + fail-on-empty for probes E4/E6/E7 · (8) the R3 locator constraint, owner-deferred | Five of eight are owner-gated (the register said four — state the convention) |
| **W9.4** | **The 23 ledger-only migrations and the hand-maintained cutoff.** `data_migrations` holds 314 rows; 23 correspond to no file; the replay set is decided by `BASELINE_DATA_CUTOFF_TS = "20260515000000"` at `migrate_db.py:111`. The commit-91 review's explicit instruction — *"D2 should absorb F11 and the 23 ledger-only migrations before it is ruled on"* — was dropped by both the register and the plan | A dual representation inside the mechanism proposed as the sole source of truth |
| **W9.5** | **Run PMP on turning space.** The Progressive Measurement Probe is a real value-determination protocol whose direction table already contains the owner's parameter; `spec_value_probes` = 0 rows. D-A's framing (*"no code path runs from N values to one"*) restates the pre-correction wording without the PMP qualification: **the correct finding is that the protocol exists, is unrun, and is unwired** | Changes D-A's framing |
| **W9.6** | **DR-2026-08-06 §2's outstanding owner actions.** The archive **tag** was never created (`git ls-remote --tags` → only `phase-a-complete-20260419`); the branch `archive/pre-reset-corpus-2026-08-06` exists at `4fc6304` and is **unprotected** | The DR names both as owner actions; neither is done |

---

## Net accounting

**Baseline, re-derived at HEAD:** 133 executables (134 `.py` less the package marker — the C8
convention, still stated nowhere) · **40,393** script lines (*not* 40,171; neither source states
its counting recipe) · 66 tables (67 with `sqlite_sequence`) · 18 views · **74 workplans /
31,338 lines**.

**Executables and script lines**

| Action | Files | Lines |
|---|---|---|
| W7.1 one-shot layer | **−19** | **−6,074** |
| W7.2 audit merge (8 of 10) | −7 | ~−150 |
| Injection (2 seams, both into `db.py`) | **0** | ~−150 |
| W7.4 if `db.py` is not adopted | −1 | −1,889 |
| **Net (adopt branch)** | **133 → 107** | **40,393 → ~34,000 (−16%)** |

**Database objects — a range, not a point.** The plan's clean "66 → 58 / 18 → 16" holds only
under three assumptions, one of which contradicts this revision's own W3.9 recommendation:

| Action | Tables | Views |
|---|---|---|
| W7.3 folds G1–G4 | −4 | — |
| W7.3-G5 (fold −1, or retire −2) | −1 or −2 | — |
| W7.9 cuts | −2 | −1 (**not −2** — `v_root_id_conflicts` survives) |
| W3.9 Candidate B scheme registry | **+1** | +1 (`v_locators`) |
| **Wave L** `work_log` | **+1** | — |
| **Net** | **66 → 58–60** | **18 → 16–18 ± F6's ruling** |

**Wave L's cost, stated plainly:** +1 table, +1 generated file (`workplan/WORK-LOG.md`), +2
registry entries, and a per-change authoring burden of four hand-written blocks. It is the only
item in this plan that *adds* to every ledger. It earns that against the plan's own history:
four consolidation generations lost findings, and every loss was a change that recorded itself
without recording its consequences.

**Workplan documents.** **Correction: "74 → 72" is impossible under guardrail 2.**
Retire-with-stub leaves a file at every origin path, so the count *rises*: 74 → **75** (74, with
3 of them stubs, plus `INDEX.md`). Only the line count falls, by ~880.

**W7.1 alone is 94% of the executable line reduction** and closes the one real unguarded writer.

---

## Dependency graph

> **REVISED AT REVISION 5.** The M-sequence graph below supersedes the wave graph that follows
> it; the wave graph is retained because its intra-wave edges (W9.1→W5.6, W5.6-with-W5.1,
> D-A→W4, W0.3→W0.1) are all still live and are carried into the M-sequence unchanged.

```
M0 OWNER MEMO ──┬──▶ Q1 D-A ──────▶ M4 boundary ──▶ M7 Wave 4
                ├──▶ Q2 Wave H ───▶ M3 ──▶ W5.2, W5.3
                ├──▶ Q3 content ──────────────────▶ M6  ◀── THE TERMINAL STATE
                ├──▶ Q4 W9.1 DR ─▶ M2 (ships with W5.6)
                └──▶ Q5 db.py ───▶ M1 W1.4 clean fix

M1 WRITE PATH (Part II) ──▶ EVERYTHING THAT WRITES.
   │  one edit to migrate_db.py:158-186 · W1.4 · W1.5 · replay guard · deps
   ▼
M2 SUBSTRATE   W0.3 ─▶ W0.1 ─▶ W5.1(12 rows) ─▶ Part I §I.4 CHECK
   │                              ▲        │
   │             W9.1 exemption ──┘        └─▶ W5.6 widen gate (must ship together)
   ▼
M3 WAVE H      H3 (read-only) ─▶ H1/H2 migration ─▶ regenerate ─▶ H4 ─▶ H5
   ▼
M4 BOUNDARY    D-A declared · W3.5 + §I.7 demotion · W3.2 · W9.2 · W3.9-B
   │           · Part I §I.3 §I.5 §I.6 (table rebuilds, while empty)
   │           · Part IV work_log (derived)
   ▼
M5 HONESTY     W8.7 · W8.8 · INDEX · .ignore · CLAUDE.md corrections · W5.4(c)
   ▼
M6 CONTENT ◀── the exit condition for every move above
   ▼
M7 DEFERRED    W7.1 · W7.2 · Wave 4 · W5.7 · W5.8 · W7.5-W7.7 · views · cuts · memo 2
```

**The three orderings that must not be violated (revision 5):** M1 before any migration, because
every migration emitted through the unfixed path is immutable history. **Part I's constraints
before content**, because SQLite has no `ADD CONSTRAINT` and 39 tables are empty *today*. **W5.1
before Part I §I.4's CHECK**, because four of the eight NULL-unit rows are legitimate data that
the constraint would otherwise forbid (AE-1).

**Revision 4's wave graph, retained:**

```
WAVE L (ledger) ──▶ EVERYTHING. No change executes without an entry written first.
       │            L1 record shape · L2 five interrogations · L3 table + generated view
       ▼
WAVE H (hard-coding ruling) ──▶ W5.2 (E-12 re-key waits on it) ──▶ W5.3 (dissolves)
       │
W0.3 (unblind detector) ──▶ W0.1 (wire it) ──▶ W5.1 (correct 8 rows)
                                                     ▲          │
                                    W9.1 (exemption DR) ──▶ W5.6 (widen gate)
                                                     └── must ship together ──┘

W1.1+W1.2+W1.3 (one edit) ──▶ W1.4 ──▶ SEAM-A/B ──▶ W7.4 (adopt, ratified)
       │
W1 ──▶ W3 (free migrations) ──▶ W4 (adjudication)
       │                              ▲                ▲
       └────────── D-A (value: machine or human?) ─────┘
                            │
                     D-B fill band ──▶ W3.1 ──▶ W3.6
                     D-C ── PREMISE DEAD; now a configuration audit

R-15 (warranted floors) ──▶ W7.10 ──▶ W5.8 legs 5,6,7
W8.7 ──▶ W8.1-W8.3 (port) ──▶ W8.4-W8.6 ──▶ W7.13 ──▶ W7.12   (NON-NEGOTIABLE)
W9.2 (frame vocabularies) — Wave 3 class, cheapest while empty
```

**The ordering that must not be violated:** W3 before content; W8 before W7.12; W9.1 before
W5.6; W5.6 with W5.1. **But empty is not neutral** — W1.4 exists because the reset moved a
counter to a value its own schema forbids and broke the only determination writer, invisibly.

---

## What to do first

> **REVISED AT REVISION 5.** The order is now **M0 (memo) in parallel with M1 (write path), then
> M2, M3, M4, M5, M6** — see Part V. The single change from revision 4's ordering is that **L1 is
> no longer first**: Part IV's ledger is derived from `run_checks.py` output and git, so it is
> built *with* M4 rather than gating M1, and the moves before it are recorded by the same
> mechanism retrospectively. The reasoning below for H3, W8.7 and W0.3 is unchanged and stands.
>
> **The one-line answer: fix the write path, then constrain the empty tables, then produce
> content.** Everything else in this plan is either downstream of those three or reversible at
> any time.

**Revision 4's ordering, retained as record: L1, then H3, then W8.7, then W0.3+W0.1, then W1.1.**

**L1** is the record shape and the `work_log` migration. It is first because every item below
changes something, and the plan's entire failure history is changes that recorded themselves and
not their consequences. Building it after the first execution means the first execution is the
one thing never logged — and on this plan's evidence, the first execution is where the errors are.

**H3** — classify the 28 stripped values into "already held in `jurisdictional_values`" versus
"held nowhere else" *before* anything is renamed. It is a read-only query, it takes minutes, and
it is the difference between a rename and a data loss.

**W8.7** is seven one-line headers. Six documents in `workplan/` carry stale text a grep returns
as current — including a retraction whose own closing paragraph states the pre-retraction figure.
It costs minutes and stops the repository lying to its next session.

**W0.3 before W0.1.** Wiring a detector whose row filter is anti-correlated with its own defect
class produces a green that means nothing. Fix line 69, then wire it.

**W1.1** is no longer four lines — and that is the point. The repository whose cardinal rule is
*never write the database directly* commits foreign-key violations through its own sanctioned
write path, and the fix four documents agreed on would not have stopped it.

**And W5.1 does not ship without W5.6, which does not ship without W9.1.**

---

## Appendix A — The contradiction ledger

**Renamed `AC-` in revision 4.** The `C1`–`C15` series minted by revision 3 was a **fourth**
colliding C-series — after the remediation register's C1–C13, the locator probes' C1–C17, and
the consolidated review's Class C that W7.13 exists to rename. Generation 4 reproduced the
generation-2 defect inside the ledger written to catalogue it.

| # | Contradiction | Adjudication | Fixed by |
|---|---|---|---|
| **AC-1** | Ledger −9→−6 vs Part 0 −3 vs §7.1 −3 | L110 stale | W8.3 |
| **AC-2** | §2.3 heading vs its own correction box | **heading is at L122, not L124** | W8.3 |
| **AC-3** | Closing paragraph states pre-retraction figures | L304, L306 | W8.3 |
| **AC-4** | Consolidated Part 2 −3 vs Part 6 −8 | **rows at L214–215, not L216–217** | W8.4 |
| **AC-5** | Tables end-state 58 vs 56 | plan was wrong | §0.4 ✓ |
| **AC-6** | One-shot layer 19/6,074 vs 18/5,850 | 19/6,074 correct; **executables 107, not 105** | W8.4 |
| **AC-7** | "5 rows across 3 items" vs six | **now eight across five** | §0.7; W8.4/W8.6 |
| **AC-8** | Executables 132 vs 133 | 133 at HEAD; convention unstated — **and it belongs in the Net baseline, not W8.6** | Net accounting |
| **AC-9** | R-24 framing | **superseded twice — now 4/76, 8 ids, zero citing** | W8.1 |
| **AC-10** | R-07 "asserts" vs "latent" | recalibration never propagated | W8.1 |
| **AC-11** | Workplans 66→69→74; lines →31,189 | **74 / 31,338 — the plan's own figure went stale inside revision 3** | W7.8 |
| **AC-12** | Tables 66 vs 67 | `sqlite_sequence`; convention unstated | W8.6 |
| **AC-13** | Ledger: quarantine terminal, then proposes retiring two quarantined scripts | internal contradiction | W8.3, W7.2 |
| **AC-14** | pr93 Part 3 announces edits never made | two of five clauses false | W8.2 |
| **AC-15** | The register ends ID collisions, then the review mints colliding IDs | generation 3 | W7.13 |
| **AC-16** | "Three unguarded direct writers" | **one** — the other two cannot reach the canonical DB | W1 |
| **AC-17** | "`main` is not branch-protected" | **false — protected** | D-C, and six documents |
| **AC-18** | "Two blocking gates are red on `main` today" | **names zero red gates** — `test_db_integrity` is 70/70 | CLAUDE.md §7 |
| **AC-19** | W5.4's 5/76/9/one-skill | **4/76/8/zero**, stale at revision 3's own subject | W8.1, W5.4 |
| **AC-20** | "The drift capability has no replacement" | **L04 is the replacement, dormant** | W1.6, W8.5 |
| **AC-21** | "The DB returns 0 rows" for grab bar | **10 rows, 5 real code values** | W8.5 |
| **AC-22** | R-21 carried unverified | **CONFIRMED at code level, REFINED to latent** | W5.7 |
| **AC-23** | "13 unwritable outputs" | **14** — the document marks one it omits | W8.6 |
| **AC-24** | "16 checks quarantined" | **15 + 1 `vacuous`** | W7.10 |
| **AC-25** | "The live plural validators are both registered" | **`validate_conflicts` is quarantined** | W8.5 |
| **AC-26** | `pre_rehab_banner_audit` "RED (6 slugs)" | **68** — the reset emptied `bpc_metadata` | W7.7 |
| **AC-27** | `room_page.py` "six non-existent tables" | **four** | W5.8 |
| **AC-28** | "85 per-slug BPC files" | **86** | W7.7 |
| **AC-29** | W1.1's four-line reorder | **cannot work** — bodies self-commit | W1.1 |
| **AC-30** | W7.14's scratchpad artifacts | **never existed in the repository** | W7.14 |
| **AC-31** | "74 → 72 workplans" | **75** under retire-with-stub | Net accounting |

---

## Appendix B — Guardrail compliance of this session's output

**Complied.** Nothing executed: no file moved, no register edited, no DB write. Every owner-gated
class is proposed. All commits touch only `workplan/`, so no doctrine token or attestation is
owed. **The rewrite-in-place with a change log, rather than an eighth file, is the right
instinct** — and revision 4 keeps it deliberately, because W6.10's own rule says successors are
how corrections strand.

**Breached, carried from revision 3, now with a fourth:**

1. **Guardrail 3** — three registers in 78 minutes, none extending the other in place. → **W8.7.**
2. **Guardrail 1** — six documents carry live stale text at HEAD in a directory `.ignore` does
   not cover. → **W8.1–W8.6, W8.8.**
3. **R-17** — the terminal documents hardcoded volatile figures and got four wrong. → §0.4, W6.6.
4. **NEW — W6.11, committed by revision 3.** It re-derived arithmetic and inherited facts, and so
   carried four premise-level errors (AC-17, AC-18, AC-19, AC-29) into a document that presents
   itself as re-verified. → **W6.11, and this appendix.**

---

## Appendix C — Method of revision 4

Seven independent read-only passes, each re-running the evidence command named in the source
rather than reading the source's conclusion: the write path and bootstrap · gates, registry and
attestations · the false database values · schema, folds and cuts · workplan document hygiene ·
the frozen corpus and orientation documents · the week's PR history. Plus one mechanical
connectivity matrix over all 167 `.py` files in `scripts/`, `tools/` and `schemas/`, crossed with
the live schema and the check registry.

**Standing caveat, per W6.6:** the matrix is a candidate map. Its raw "82 unreferenced files"
figure is inflated by `schemas/` and entry points; the adjudicated 26 stands.

---

## Appendix D — Honest limits

- **`validate_pydantic_schemas`' 246 findings / 49 unmapped tables was not re-derived** — pydantic
  could not be installed in a read-only session. Carried on the documents' authority.
- **Branch protection's *configuration* is not readable** from a session; only the boolean was
  verified. `protected: true` does not distinguish classic protection from a ruleset.
- **"~30 of `test_db_integrity`'s 70 assertions reference only empty tables"** is carried, not
  classified assertion-by-assertion.
- **The eight W5.1 corrections are readings of `value_text`, not of the underlying standards.**
  Text-vs-BS-8300 verification is Phase-B work.
- **The W3.7 stakes grades are proposals** from the schema's own definitions; they are judgment
  acts and the item most likely to change under owner review.
- **All writer/reader claims are static greps** over non-legacy `.py`; dynamic SQL would evade
  them.
- **W5.7's behavioural assertion** (that the fixed renderer emits an explicit absence) was not
  demonstrated against a fixture; the code-level reading is robust, the behaviour is not yet shown.
- **Wave H's 28-name list has not been re-derived against the standard-designation exception**
  (H4): `E-09 Tactile Walking Surface Indicators (ISO 23599:2019)` contains digits that are a
  citation, not a determination. The permitted set is an open sub-question.
- **Counts here are as volatile as the ones this revision corrected.** The grab-bar count moved
  122 → 126 *because the finding was documented*. Re-derive before acting on any row.

---

---

## Appendix E — Verification log of revision 5

Every figure introduced by Parts I–VII was produced by running the command beside it against
`fd4c09d` on 2026-08-12. Reasoning-pass conclusions that could not be verified are marked as
carried, not stated.

| Claim | Command | Result |
|---|---|---|
| The canonical DB has zero triggers | `SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'` | **0** |
| `evidence_cell_state` carries no state-machine CHECKs | `SELECT sql FROM sqlite_master WHERE name='evidence_cell_state'` | Confirmed — enum CHECKs and one `json_valid` only; **no `doctrine_sha` column** |
| `governing_refs` is an FK-unreachable JSON blob | same | Confirmed: `governing_refs TEXT CHECK (… json_valid(…))` |
| `cell_source_links` exists with real FKs | `SELECT sql FROM sqlite_master WHERE name='cell_source_links'` | Confirmed — PK `(cell_id, ref_id)`, both FK'd, `role` CHECK admits only `'governing'` |
| FKs are disabled during every migration | `migrate_db.py` | Confirmed at **:161** (apply) and **:250** (rebuild) |
| The commit precedes the FK check | `migrate_db.py` | Confirmed — `conn.commit()` **:171**, `foreign_key_check` **:174** |
| The `except`'s rollback is inert | `migrate_db.py:183-184` | Confirmed — follows the commit at :171 |
| The BOOTSTRAP substring disables enforcement | `migrate_db.py` | Confirmed at **:176**, duplicated at **:261** |
| Migration bodies self-commit | `emit_data_migration.py:201` | Confirmed — `BEGIN TRANSACTION; … COMMIT;` |
| The divergence detector is blind to NULL-unit rows | `jurisdictional_divergence.py:69-71` | Confirmed — `WHERE value_numeric IS NOT NULL AND unit IS NOT NULL` |
| `assess_cell.py` re-implements `next_gap_id` wrongly | `assess_cell.py:426-429` | Confirmed — returns `GAP-1`; `db.py:149-158` zero-pads |
| `assess_cell.py` refuses the canonical DB | `assess_cell.py:490-491` | Confirmed — hence the import trap |
| **AE-1** — four NULL-unit rows are legitimate | `SELECT jv_id,item_code,jurisdiction,value_numeric,value_text FROM jurisdictional_values WHERE value_numeric IS NOT NULL AND unit IS NULL` | **8 rows; jv 14 (DCOF 0.42), 15 (PTV 36), 96 and 100 (occupant counts 50) are correct data.** The proposed one-line CHECK would destroy them |
| **AE-2** — jurisdiction vocabulary fragmentation | `SELECT DISTINCT jurisdiction` over the three carrying tables | **52 distinct free-text values** (12 / 48 / 17); `UK` appears 0× in `jurisdictional_values`, 1× in `lang_jur_map`, 7× in `term_aliases`; `ISO` and `EU` in a jurisdiction column; **`colloquial` in `term_aliases.jurisdiction`** |
| **AE-3** — vacuity-guard coverage | parse `check-registry.yaml` | **6 of 65 declare `min_items`** (9%), not 14 |
| `basis:` is half-empty | same | **32 of 65 `unattributed`**; next largest `hygiene` at 16 |
| Check register composition | same | 65 checks — **28 blocking, 34 advisory, 3 informational**; 16 quarantine entries |
| `locator_scheme` is unpopulated | `SELECT locator_scheme, COUNT(*) … GROUP BY 1` | **NULL on all 109 rows** — the 16-column block is free to reshape |
| `evidence_sources` width and Co-1 columns | `PRAGMA table_info(evidence_sources)` | 97 columns including `tier`, `evidence_type`, `co1_provenance`, `co1_source_type` |
| Empty-table count | `COUNT(*)` over every table | **39 of 67 empty**; `evidence_cell_state` 0, `evidence_sources` 0, `jurisdictional_values` 109, `items` 93 |
| `test_db_integrity` is green | `python3 scripts/tests/test_db_integrity.py` | **RESULTS: 70/70**, exit 0 |
| `main` is branch-protected | GitHub API branch listing | **`{"name":"main", …, "protected":true}`** — the only protected branch. CLAUDE.md §0/§7 remain stale |
| 28 of 93 item names carry digits | `SELECT name FROM items` + regex | **28 of 93** confirmed |

**Carried, not verified by revision 5:** every figure inherited from revision 4's Appendix C and
D (the `validate_pydantic_schemas` findings, the ~30 vacuous `test_db_integrity` assertions, the
pre-reset archived-row counts, the 133-executable and 40,393-line baselines, the W7.1 file list).
Revision 4's Appendix D limits all still apply, and **branch protection's *configuration* remains
unreadable from a session** — only the boolean was verified, so the three required-check traps in
`references/tooling-register.md` §6.7 stay live questions.

**Revision 5's own guardrail compliance.** Nothing executed: no file moved, no register edited,
no DB write, no migration emitted. All owner-gated classes are proposed. This commit touches only
`workplan/`, which `check_doctrine_token.py:46-48` excludes from `SYNTHESIS_RE`, so no doctrine
token and no attestation are owed. **Guardrail 3 complied with for the first time in this
sequence:** revision 5 extends the live plan in place rather than adding a tenth document —
which is also the rule it asks every future session to follow.

---

*Revision 5 was derived on 2026-08-12 against `fd4c09d` by two independent read-only reasoning
passes followed by a verification pass that re-ran every load-bearing claim either pass produced.
**Four did not survive, two of them headline recommendations** (Appendix E, AE-1 to AE-4). Part
VII is revision 5's loss-audit. Revision 4's own closing note stands: re-derive before acting.*

*Revision 4 re-derived every load-bearing claim on 2026-08-11 against `3c936db` by running the
command named beside it. Thirty-one claims did not survive; four were premise-level. §0.7 is
revision 4's loss-audit. The `run_checks --all` total is not written here, by rule. Re-derive
before acting.*
