# Wave H — The hard-coding ruling. **First among the substantive waves.**

**Read `00-holistic-execution-plan.md` first.** **Precondition: L1 exists.**

**Owner-ruled 2026-08-11.** DG-NON — work-product inclusion/exclusion and trajectory are
owner-only, and the owner has ruled:

> *"We aren't supposed to have any specifications/coded items like E-02."*
> *"This is bonkers and should not be the case."*
> *"Hard-coding undermines the entire project."*

**What remains is execution shape**, proposed here. **Exact new-name wording still wants owner
sign-off** — the plan supplies only five targets; everything else below is proposed.

**The fix is cheap.** `items.name` **is not a key**: the DDL has `item_code TEXT PRIMARY KEY`,
`item_id TEXT UNIQUE`, and `name TEXT NOT NULL` with **no unique constraint and no index**. All
**14 inbound FKs target `item_code`** — enumerated and confirmed. Four views read `items` but
recompute from the table, so a rename needs no view edit. **This is not K3's FATAL 278-file
rename.**

---

## H3 — Classify every value before stripping it. **Do this first.**

**Read-only. Minutes. It is the difference between a rename and a data loss.**

### The plan's two-way partition is refuted — there are four classes

| Class | Count | Meaning |
|---|---|---|
| **(a)** | **5** | Already held in `jurisdictional_values` for that item — the name duplicates a correctly-held value; stripping loses nothing |
| **(b)** | **17** | Held nowhere else — an unevidenced assertion; its removal is the point |
| **(n)** | **4** | The digit is a **metric or standard designation**, not a determination — the H4 permitted-set class |
| **mixed** | **2** | E-03 and H-01 — part (a), part (b) |

**No class (c) exists** — with `evidence_sources`, `evidence_cell_state` and
`source_value_extractions` all at 0 rows, nothing in the repository is "correctly evidenced," so
**H3's falsifier cannot fire today.** Re-check immediately before cutting the migration (W6.11).

### And "the 28 numbers" undercounts

**Seven names carry more than one number** (A-16, B-11, E-01, E-04, E-05, G-05/G-06 as ranges,
H-01), so the act strips **~35 distinct determinations**, not 28.

### The full classification

| item | number(s) | jv rows | class | evidence |
|---|---|---|---|---|
| A-02 | NRC ≥0.85 | 0 | **(b)** | — |
| A-03 | STC ≥35 | 0 | **(b)** | — |
| A-06 | NRC ≥0.70 | 0 | **(b)** | — |
| A-08 | NC-25 | 0 | **(b)** | — |
| A-10b | RT60 | 0 | **(n)** | reverberation-time metric designation |
| A-14 | STC ≥50 | 0 | **(b)** | — |
| A-16 | ≥8 m²; per 500 m² GFA | 0 | **(b)** ×2 | two determinations in one name |
| A-18 | RT60 | 0 | **(n)** | as A-10b |
| B-01 | ≥150 EML | 0 | **(b)** | — |
| B-04 | IEEE 1789-2015 | 0 | **(n)** | standard designation — but *"Compliant"* is a conformity determination |
| B-05 | ≥5 m | 0 | **(b)** | — |
| B-06 | ≥300 Lux | 0 | **(b)** | — |
| B-08 | ≤30 Gloss Units | 0 | **(b)** | — |
| B-11 | ≤2700 K; 19:00 | 0 | **(b)** ×2 | a quantity **and** a clock condition |
| C-04 | ≥30 LRV | 5 | **(a)** | jv 92 (GB, BS 8300), jv 93 (AU, AS 1428.1:2021). **jv 91 US reads "None specified; Significant gap"** — the name universalises GB/AU |
| D-11 | every 20 m | 0 | **(b)** | — |
| E-01 | 1400×1100 mm | 7 | **(a)** | jv 79/80/82/83/84 all "1100×1400mm" (EN 81-70 Type 2) — **but jv 78 US = 1730×1370 and jv 81 AU = 1400×1600.** Same EN-promotion pattern as E-08 |
| E-03 | ≤1:20 | 8 | **mixed** | "1:20" appears only in `value_text` as *"Preferred"* (jv 49 GB, jv 52 NO outdoor, jv 55 ISO); `value_numeric` records the **max** gradient. **The name promotes a preference to the parameter's identity** |
| E-04 | 3600 mm | **0** | **(b)** | zero backing rows — the plan's exemplar, confirmed |
| E-05 | 3000×2000 mm | 0 | **(b)** | — |
| E-07 | PTV ≥36 | 4 | **(a)** | jv 15 only (GB). jv 14 US DCOF 0.42, jv 16 DE R-class, jv 17 AU P-class are **unrepresentable in PTV** — confirms "adopts Britain's metric" |
| E-08 | ≥1200 mm | 7 | **(a)** | jv 72 (GB) and jv 77 (ISO) at 1200; **US 915 (jv 71) and AU 1000 (jv 74) below; DE 1500 (jv 73) and NO 1500 (jv 75) above** |
| E-09 | ISO 23599:2019 | 7 | **(n)** | standard designation — **but jv 56–62 record seven different national standards with incompatible dome geometries** (JIS T 9251, ADA §705/PROWAG, DfT 2021, AS/NZS 1428.4.1, DIN 32984, ISO 23599, BCA 2019). Naming ISO privileges one exactly as E-07/E-08 do — an argument for stripping citations too |
| F-04 | MERV 13+ | 0 | **(b)** | — |
| G-05 | `650--870 mm` | 0 | **(b)** | — |
| G-06 | `760--860 mm` | 0 | **(b)** | — |
| H-01 | `400--1100 mm` | 6 | **mixed** | lower bound 400 has **no row** (US 380, GB 750, DE 850, AU 900, FR 900, ISO 800) → (b); upper bound 1100 is (a)-partial |
| I-01 | ≤22 N | 4 | **(a)** | jv 19 only (US, ADA §404.2.9). GB 30 N, AU 20 N, ISO 25 N — **adopts the US value; a fourth single-jurisdiction promotion** |

**Transcribe this table into the migration's own comment block**, per H3's instruction — and
**do not let the comment claim a two-way partition the data refutes.**

**For the 17 (b) rows:** if the owner wants the values preserved pending evidence, the vehicle is
a `gaps` row per item ("parameter has no recorded jurisdictional value") — **not**
`jurisdictional_values` (they are not code values) and **not** `evidence_cell_state` (0 rows, and
D-A is unruled).

---

## H1 + H2 — The rename

### H2's count could not be reproduced

**The plan's "23 of 93 carry a prescriptive condition clause" has no stated criterion.** 62 of 93
carry *some* parenthetical; an enumeration of applicability clauses ("where/when the provision
applies") yields **~31 candidates**, overlapping the 28. **Pin the criterion in the migration
comment and either reproduce 23 or correct it before cutting H2.**

### Proposed mapping
*(¶ = the plan's own target · ✂ = whole parenthetical is determinations)*

| item | proposed |
|---|---|
| A-02 | ¶ **Acoustic Absorption at Ceiling** — note this changes the provision noun ("Panels"→"Absorption"), a semantic shift beyond stripping; wants an explicit owner nod |
| A-03 | **Acoustic Door Sound Insulation** ✂ |
| A-06 | **Fabric Wall Panels at Acoustic Reflection Points** |
| A-08 | **HVAC Noise Control** ✂ |
| A-10b | **keep** — (n) |
| A-14 | **Double-Leaf Partition** |
| A-16 | **Sensory Room / Quiet Room Provision** ✂ |
| A-18 | **keep** — (n) |
| B-01 | **Circadian Lighting** ✂ |
| B-04 | **Flicker-Free LED Luminaires** — recommend stripping the whole parenthetical (H4 open) |
| B-05 | **Gradual Lighting Transition Zones** ✂ |
| B-06 | **Individual Dimming Control** ✂ |
| B-08 | **Matte, Low-Reflectance Floor Finishes** ✂ |
| B-11 | **Warm Colour Temperature for Evening** ✂ |
| C-04 | **LRV Contrast** |
| D-11 | **Safe Accessible Garden** ✂ |
| E-01 | **Accessible Lift** ✂ |
| E-03 | **Ramp Gradient** ✂ — also drops the "MS Fatigue and Temporal Accessibility" rationale tail; **rationale belongs in reasoning docs, not names** |
| E-04 | **Accessible Parking** ✂ |
| E-05 | **Weather Protection at Entry** ✂ |
| E-07 | ¶ **Slip Resistance** |
| E-08 | ¶ **Corridor Clear Width** |
| E-09 | **Tactile Walking Surface Indicators** *or* keep the ISO citation — H4's open question; the seven-standards evidence argues for stripping |
| F-04 | **Air Quality** — or **Air Quality (Filtration, VOC, Thermal Stability)** without the MERV grade, since the parenthetical also carries sub-parameter identity |
| G-05 | **Adjustable-Height Work Surfaces and Desks** ✂ |
| G-06 | **Reception Counter — Accessible Height Section** |
| H-01 | **Controls at Accessible Height** ✂ — "One-Fist Operable" is itself a determination |
| I-01 | **Hardware Operability** ✂ |
| **E-15** | **Changing Places Facility** — **repairs the data truncation in the same migration** |
| E-02 | ¶ **Platform Lift** |
| A-05 | ¶ **Floor Covering: Carpet** |

**H2-only candidates:** A-17, B-07, B-10, C-03, C-06, D-07, D-08, E-06, E-10, F-02, F-05, F-06,
G-03, I-02.

**New finding — a determination spelled as a word.**
`G-02 Variety of Seating Types (Three Heights at Every Seating Area)` carries a determination
that **evades H4's `\d` gate entirely.** Add it to H2's list and to H4's note.

### Mechanism

> **⚠ GUARD STRINGS MUST BE COPIED FROM THE DATABASE, NEVER FROM THIS DOCUMENT.**
> Cycle-1 verification found this document had rendered `650--870`, `760--860` and
> `400--1100` with **en-dashes** where the database stores **double hyphens**. A
> `WHERE name='…'` guard transcribed from prose would have matched **zero rows and
> reported success** — three renames silently not happening. The names also mix
> `—` em-dash (G-06, E-03), `×` (E-01, E-05), `≥`/`≤`, and `²` (A-16).
> **Build every guard with `SELECT item_code, name FROM items` and never by hand.**

1. Ledger entry (`plan_item: H1`), intent written first.
2. `changes.sql`, 28–45 statements with a **current-value guard** (the W5.1 idempotence pattern):
   ```sql
   UPDATE items SET name='Corridor Clear Width',
                    updated_at=datetime('now'), updated_by_session='<session>'
    WHERE item_code='E-08'
      AND name='Corridor Clear Width (≥1200 mm Minimum on All Primary Routes)';
   ```
   Prepend the H3 table as an SQL comment block.
3. `emit_data_migration.py` → `migrate_db.py` → `--rebuild` check. Expect the emitter's
   `UPDATE — check WHERE clause` warnings (non-blocking, `:52`); ENUM_GUARDS do not fire.
   **Wave H does not need W1.1 first** — a single-table UPDATE cannot violate an FK.
4. **Regenerate**, and note what cannot be regenerated:
   - `python3 scripts/generate_parts.py` — E-08's old name ships at `parts/v10/part04.md:92`.
   - `python3 scripts/generate/build_site.py` — **drives `site/specs/` only** (its own docstring,
     `:5-16`).
   - `population_page.py` — **no driver exists**; loop it over the 11 population codes
     (`:249-259` renders one page per argv).
   - **`site/rooms/` cannot be regenerated at all.** `room_page.py:26-84` reads six relations
     absent from the live schema. **The 9 stale `site/rooms/*.html` carrying old names need an
     owner disposition** — hand-edit the frozen renders, or retire them. **The plan's Mechanism
     paragraph does not cover this.**
5. **Hand edits:** `index.html` — **29 hit lines, enumerated**: A-02 at 120 and 166 · A-03:171 ·
   A-06:186 · A-08 at 125 and 196 · A-10b:211 · A-14:231 · A-16:241 · B-01:261 · B-04:276 ·
   B-05:281 · B-06:286 · B-08:296 · B-11:311 · C-04:346 · D-11:421 · E-01:436 · E-03:446 ·
   E-04:451 · E-05:456 · E-07:466 · E-08:471 · E-09:476 · F-04:531 · G-05:581 · G-06:586 ·
   H-01:616 · I-01:651. Plus `specs/e-08.html:987` and — only if A-10b is renamed at all —
   `data/question-headings.yaml:39`. `tools/evidentiary-audit-dashboard.html` is regenerated by
   `regenerate-derived.yml`; **confirm regeneration rather than hand-editing it.**

### Blast radius, re-measured

| Class | Count | Disposition |
|---|---|---|
| Generated — regenerate | **50** | `parts/v10/part04.md` · `site/specs/*.html` (28) · `site/populations/*.html` (11) · `site/rooms/*.html` (**9 — unregenerable, see above**) · the dashboard |
| Must-fix by hand | **3** | `index.html`, `specs/e-08.html`, `data/question-headings.yaml` (conditional) |
| Frozen `references/` — leave | **20** | 15 audit-briefs, a reasoning doc, `claim-reference-join.json`, a methodology file, `part04-item-index.md`, `toc.md` |
| Immutable migrations — leave | **4** | `012_baseline_2026-05-15.sql`, `052_extraction_item_edge.sql`, and two data migrations |
| Cold storage — leave | **26** | `_archived/**` (19), `audits/` (2), `sessions/` (3), `versions/` (2) |
| Live workplan/working | **4** | incl. the resolution plan itself, which quotes the names *as findings* — leave |

**Two plan figures corrected:** *"1 code file"* is **REFUTED — zero live `.py` files contain any
full name string** (the only `.py` hit repo-wide is archived). *"13 live files outside the
generated and frozen sets"* measures **10** at HEAD — and the count moved partly **because the
plan itself now quotes the names**, the same self-referential drift Appendix D warns about.

---

## H4 — The standing gate

**The permitted set is now derived** (Appendix D said it was not), and it is small and closed:

- **(n1) metric designations** — `RT60` (A-10b, A-18);
- **(n2) standard designations** — `\b(ISO|EN|DIN|IEEE|JIS|BS|AS(/NZS)?)\s?\d` (B-04, E-09), *if*
  the owner rules citations stay.

**So H4's falsifier — "the check cannot express the permitted set without an unbounded exception
list" — does NOT fire.**

**But state the blind spot in the check's note: determinations spelled as words evade `\d`
entirely.** Live instance: G-02's "Three Heights".

Implement as `scripts/audit/item_name_determinations.py` (stdlib, prints `EXAMINED: 93`),
registered `advisory`, battery `data`, `basis: unattributed` until the Wave-H DR ratifies it.
**Sequencing note: do not create the eleventh single-invariant audit file without recording it in
the ledger's `culling` block** — W7.2 is merging the other ten.

---

## H5 — Audit the other seeded vocabularies. **It closes clean.**

Re-run at HEAD:

| Vocabulary | Digits | Condition clauses |
|---|---|---|
| `axes.name` (17) | **0** | 0 |
| `rooms.name` (17) | **0** | 0 |
| `populations.display_name` (23) | **0** | one scope marker, *"applies to all populations (scope marker)"* — not a prescription |
| `access_needs` (17) | **0** | (no `name` column; `need_code`/`family`) |
| `slugs.slug` (106) | 1 — `co1-housing-research-global-south` | a tier label, not a determination |

**H5's falsifier fires: no other vocabulary carries determinations in its names. H5 closes as a
clean audit with no follow-on migration.**

*Caveat:* name-like columns only. `axes.mechanism` and `access_needs.design_obligation` are
definitionally prose, not names, and were out of scope.

---

## H6 — The three off-frame populated tables

| Table | Rows | Finding | Disposition |
|---|---|---|---|
| `rooms` | 17 | All `category`/`description` NULL, all active, all created by one session. **Sole inbound FK is `room_items.room_code`, and `room_items` = 0 rows — so `rooms` connects to nothing live.** `room_page.py` does not even read it (it reads a nonexistent singular `room`), and **`build_site.py:7-8`'s docstring claims `rooms` doesn't exist — stale, it does** | **Owner ruling (DG-NON):** register as frame, or reset. Either way the 9 stale `site/rooms/*.html` need H1 step 4's disposition |
| `weighting_profile` | 5 | **Zero live code readers — confirmed by a repo-wide grep including legacy.** Only migrations, governance prose, forward-only DRs, generated context-map, workplans, archive | **W5.5.** Retirement is a doctrine edit (amend `evidence-architecture.md` I3), not dead-code removal |
| `item_population_elaborations` | 3 | All `population_code='MOB'`, all `evidence_ref_id` NULL, and **`spec_variant_b` carries numeric synthesis — *"~1700mm vs 1500mm"*** — the reset's target class verbatim | **Reset it.** One data migration `DELETE FROM item_population_elaborations;` — FK-safe at 0 child rows |

**Before the delete:** confirm the three rows exist in
`_archived/data/corpus-pre-reset-2026-08-06.db` (they were created 2026-05-11, so they should —
**but verify, do not assume**). And check **which** `test_db_integrity` assertion references the
table, so the delete does not flip a check verdict unnoticed — record it in the ledger's `breaks`
block.

---

## Cycle-1 verification: **NO-GO**. Six blockers before any migration is emitted.

An adversarial verification pass on 2026-08-12 returned no-go. Each of these independently
produces a silent no-op, a failed migration, or a half-executed ruling.

| # | Blocker | Correction |
|---|---|---|
| **B1** | **Guard-string byte mismatch** — this document rendered en-dashes where the DB stores double hyphens (G-05, G-06, H-01) | Corrected above; build every guard from `SELECT name FROM items` |
| **B2** | **`jurisdictional_values.evidence_tier` is `INTEGER NOT NULL DEFAULT 6`** — it cannot be nulled; an `UPDATE … SET evidence_tier=NULL` aborts the migration | State its disposition explicitly: leave at the meaningless default with a comment, or relax the constraint by table rebuild |
| **B3** | **Skills sweep incomplete** — `question-author_SKILL.md:68` carries `B-01 Circadian Lighting (≥150 EML)`, missed by the 65/66/71 enumeration. Six further skill files carry determinations: `cross-population-conflict-mapper` (≥300 lux, ≤3000K, ≥2400 mm, ≥30 LRV as live population requirements), `adversarial-research`, `functional-deficit-auditor`, `progressive-measurement`, `markdown-formatter`, `prose-style-checker` | Enumerate all with per-line dispositions; the meta-exemplar class (detectors teaching detection) needs an owner call |
| **B4** | **`item_axis_links` row 162 (E-08/AX-BAL)** — a 1,093-character evidence note carrying `fall rate 0.81 CI 0.68-0.97`, six REF-IDs, and the claim *"registered as GAP-300 (P2, OPEN), with GAP-301"* while `gaps` holds **0 rows** | Add to the clear census; do not leave a live claim that unregistered gaps are registered |
| **B5** | **Gap allocator emits an id the validation layer rejects** — `assess_cell.py:429` yields `GAP-1`; the `gaps` DDL has no format CHECK so it writes, but `schemas/evidence_state.py:166-169` requires `^GAP-\d{3,4}$` and will reject it later | Allocate via `db.py`'s zero-padded scheme; fix `:429` to `GAP-{mx+1:03d}` before any repopulation |
| **B6** | **YAML dual store keeps every retired value alive** — `data/jurisdictional_values/*.yaml` holds 109 records with full values, and `test_db_integrity` L02 compares **counts only**, so clearing the DB leaves the determinations in-repo with a green check | Clear the YAML mirror in the same PR; extend L02 to compare what survives, not row counts |

**Sequencing finding:** once jv values are cleared, "held in `jurisdictional_values`" is true of
nothing, so **every** stripped name value becomes class (b). Either run the name strip **before**
the jv clear, or freeze this classification in the migration comment as an explicit pre-clear
snapshot. As written it would be false at execution time.

---

## Re-derivation notes

| Claim | Status |
|---|---|
| 28 of 93 names carry a digit | **CONFIRMED** |
| `items.name` is not a key; 14 inbound FKs all target `item_code` | **CONFIRMED** — exact list match |
| 23 of 93 carry a condition clause | **UNREPRODUCIBLE** — no criterion stated; ~31 by enumeration. Pin it before H2 |
| H3 is a two-way (a)/(b) partition | **REVISED — four classes**: 5 (a) / 17 (b) / 4 (n) / 2 mixed; no (c) is currently possible |
| "the 28 numbers" | **REVISED — ~35 determinations**; seven names carry more than one |
| E-08's jv set; E-07 adopts Britain's metric; E-04 has zero rows | **CONFIRMED** |
| E-15's name is truncated in the data | **NEW** — recorded in no prior document |
| G-02 carries a word-spelled determination | **NEW** — evades H4's `\d` gate |
| Blast radius "1 code file" | **REFUTED — zero live `.py` hits** |
| Blast radius "13 live files" | **REVISED — 10** |
| 4 immutable migrations · 20 frozen references · 51 rendered | **CONFIRMED** (51 = 50 generated + `specs/e-08.html`) |
| H4's falsifier | **DOES NOT FIRE** — permitted set is two patterns |
| H5's falsifier | **FIRES — H5 closes clean** |
| H6 counts 17 / 5 / 3 | **CONFIRMED**; plus `rooms` is fully disconnected and all 3 elaborations are unevidenced |
| `site/rooms/` regeneration | **NEW — impossible**; blocks H1's mechanism as written |
