# Wave 8 — Document hygiene: port the unique content, then correct the stale text

**Read `00-holistic-execution-plan.md` first.** **This wave is the non-negotiable precondition
for W7.12.**

**Sequence:** W8.7 → W8.1–W8.3 (port) → W8.4–W8.6 (correct) → W7.13 (rename) → W7.12 (retire).
**Retiring before porting is the one ordering that reproduces the defect this wave exists to
fix.**

**One filename correction that governs the whole wave:** the plan names W8.6's target
`2026-08-12-per-stage-table-anatomy.md`. **The file at HEAD is
`workplan/2026-08-11-per-stage-table-anatomy.md`** — there is no 2026-08-12 variant.

**Commit hygiene, verified:** `workplan/` is **not** a synthesis path —
`scripts/ci_helpers/check_doctrine_token.py:46-48` defines `SYNTHESIS_RE` as matching only
`references/bpc-reasoning|references/connection-reasoning|decisions|sessions`. **No doctrine
token, no attestation owed for W8.1–W8.7.** Format per `check_commit_msg.py:57`.
**The trap: W8.8 touches `sessions/` and IS a synthesis path — its own commit, with token and
attestation.**

---

## W8.7 — The seven one-line supersession headers. **The first action in the plan.**

Cheap, and it stops the repository lying to its next session. **All seven anchors confirmed at
HEAD.**

**The header text** (identical for insertions 1–6; reproduce the backtick nesting exactly):

```
> *Finding statuses and figures in this document are superseded by `workplan/2026-08-12-resolution-plan.md` (Wave 8 · Appendix A). Its reasoning and evidence stand.*
```

| # | File | Insert after | Context |
|---|---|---|---|
| 1 | `2026-08-11-reconciled-findings-register.md` | **L10** | L10 is the Doctrine-SHA/Environment line; L11 blank; L12 begins `> **The reconciliation is not clerical.**` |
| 2 | `2026-08-11-consolidated-review-and-plan.md` | **L10** | L10 `**Doctrine SHA:** …`; L12 begins `> **The single most important thing found this session…**` |
| 3 | `2026-08-11-consolidation-sweep-and-adversarial-pass.md` | **L11** | L11 Doctrine-SHA/Environment; L13 begins `> **Read §0.2 before §1.**` |
| 4 | `2026-08-11-fold-or-cut-ledger.md` | **L12** | L12 `**Subject:** …`; L14 is `---` |
| 5 | `2026-08-11-pr93-reconciliation-and-shared-code.md` | **L8** | L7–8 the Subject lines; L10 begins `> **The most useful result is not a merge conflict…**` |
| 6 | `2026-08-11-per-stage-table-anatomy.md` | **L11** | L11 `**Subject:** …`; L13 is `---`. **Path corrected from the plan's 2026-08-12** |
| 7 | Sweep Part-3 marker (same file as #3) | **L463** | L463 `## Part 3 — Recommended sequence`; L465 `Nothing here is executed. …`. **Different text** — it marks one section: `> *This sequence is superseded by `workplan/2026-08-12-resolution-plan.md` (Wave 8 · Appendix A). Its reasoning and evidence stand.*` |

A blockquote legally interrupts a paragraph in CommonMark, so inserting directly after the status
line renders correctly.

**Verification:** `grep -c "superseded by .workplan/2026-08-12-resolution-plan.md" workplan/*.md`
→ 7; each file's diff is exactly one added line.

**Note:** after these insertions **every anchor in W8.1–W8.6 below shifts +1** in its file. Either
apply W8.7 in the same edit and adjust, or re-locate by content.

---

## W8.1 — `reconciled-findings-register.md` — port, correct, retire with stub

### Ports (ranges verified; two corrected)
- **§0.2, the namespace-collision table — `L37-51`** (the plan cited 37–52; §0.3 begins L53). It
  is the only place the four-way `C1`/`C4`/`D2`/`F6`/`F9` collision is tabulated. **When porting,
  note beside it that revision 4's Appendix A records the collision recurring a fourth time —
  the `AC-` rename.**
- **§2.1, the REFUTED "a missing dependency produces a pass" — `L152-173`** (cited 152–174). It
  records a *tested* refutation: with `jsonschema` shadowed by a raising stub, the audit still
  exits 1, because `check_1_schema` appends an issue on `ImportError`. **A2's consequence clause
  is refuted; the dependency defect is real but the "silent pass" that made it urgent is not.**
- **Part 6 — `L273-294`.** **The plan's "282–290, exact" is only the third bullet** — the
  near-miss where the locator-probes document was nearly dropped because it uses prose headings
  rather than IDs. **Port at minimum L282-290; recommended the full L273-294**, or the R-21 and
  R-26/R-27 caveats die with the retirement.

### Corrections
- **R-07 at `L85`** — replace the "asserts 27×" sentence with the **latent, not published**
  recalibration: no rendered surface emits 54 Hz; the only shipped match is the bibliographic
  string "BS EN 54-23:2010" in `parts/v10/part13.md`. **The row would poison the first
  determination to read it** — which is a different and more precise claim.
- **R-24 at `L138`** — replace with the revision-4 numbers: **4 of 76, 8 distinct identifiers,
  `integrity-protocol` cited by ZERO.** The "4 committed attestations cite it" was a whole-file
  string grep hitting artifact paths and `bias_direction` prose. Register `integrity-protocol`
  and `supersession-audit` **on completeness grounds, not to clear a red check** — at HEAD it
  clears zero failures.
- **Banner Part 4 after `L220`** (`## Part 4 — Sequencing`).
- **Same-pass candidate the plan does not list: `L139` (R-25)** carries the "13 times / 8 rows"
  armature figures that W8.5 corrects in the sweep. Fix both or they contradict.

**Risk:** R-24's replacement hardcodes volatile counts. **Date them.**

---

## W8.2 — `pr93-reconciliation-and-shared-code.md`

- **The cross-map is at `L27-36`** (cited 27–37) and is **already ported** into the resolution
  plan's §0.3. The 60-identifier port is already satisfied at W5.4. **No further port needed.**
- **Part 3's false announcement at `L237-239`** — verified false in **both** clauses: the
  register at HEAD ends at R-27 (no R-28…R-32 exist), and its Part 4 carries no retirement
  marking. Replace with an explicit correction:
  > **CORRECTION (2026-08-12): the edits this item announced were never made.** The register was
  > never given R-28…R-32 and its Part 4 was never marked retired. The five §1.2 items live as
  > resolution-plan items instead (W1.4; D-B/W3.1; W5.2; W5.3; D-A), and the Part-4 supersession
  > is now recorded by the banner W8.1 places on the register itself.

**Falsifier worth stating:** someone "fixes" this by *adding* R-28…R-32 to the register — which
would execute a stale instruction against a document being retired, the exact inverse of the
intended correction.

---

## W8.3 — `fold-or-cut-ledger.md`

**Ports, all ranges verified:** Part 1 `L35-51` (phase-multiplicity distribution) · §2.6
`L191-192` (**cited 192–195 — corrected**): *"`v_coverage_priority` — 7,210 rows and no reader at
all"* · Part 4 bucket table `L223-229` (registered 55/16,815 · library 29/8,883 · workflow
6/3,281 · quarantined 16/3,590 · unreferenced 26/7,330) · Part 5 `L258-279` (the skills negative
result) · §7.2 `L338-383` (**the source text for W6.8**).

**Corrections:**
- **`L110-111`** — the box says "corrected from −9 to −6 (66 → 60)". **The right figure is −3
  (66 → 63)**, which §7.1 and Part 0 both state; this box alone kept the intermediate.
- **`L122`** — **the heading is at 122, not the cited 124.** Make it agree with its own
  correction box at `L133-149`.
- **`L304`** — "removes 9 tables" → **3**. **And add a pointer:** the −32 columns is separately
  revised to a definitional consolidation (−0 columns) by W3.9 Candidate B, or the keeper and
  this ledger disagree.
- **`L306`** — "seven of the nine table folds" is pre-retraction.
- **`L243-252` vs `L228`** — the internal contradiction. `L228` says quarantine is terminal;
  `L251-252` proposes "−26 if the singular validators and the surplus initialisers go too" — and
  **`validate_item.py` and `validate_conflict.py` are both quarantined.** Replace with: realistic
  net **−19 with high confidence**; the further −7 includes two quarantined scripts and **waits on
  W7.10's `disposition:` ruling. It is not a free cut.**

**Open choice:** retire with stub, **or** keep as a fifth document with a banner (§0.6's
lower-effort variant). **If the keep option is taken, W7.12's "−3 files / ~−900 lines" and the
net file count both change — record the choice in the Wave-L entry before the W7.12 commit.**

---

## W8.4 — `consolidated-review-and-plan.md` *(KEEPER)*

**Anchors, all confirmed:** `L214-215` (the Class-F −3 rows — **the plan's own correction of its
earlier "216–217" is right**) · `L403` (−18/−5,850 → **−19/−6,074**) · `L410` (133 → **107**;
40,171 → **40,393**; −18% → **−16%**) · `L467` ("−9 files" → **−7**) · `L473` (**`G6` is
undefined** — the G-series ends at G5; rewrite as "this audit merge (W7.2)") · `L481-482` (the
summary table: **107, −26: −19 one-shot, −7 merged audits**) · `L206` (E5's "now 69 and ~29,000"
→ **75 files / 32,411 lines at HEAD, and the count moves every session — re-derive, never cite**).

### The "five false values" sweep, re-run
**The plan's list of eight sites is complete and correct:** `L26`, `L30`, `L75`, `L142`, `L160`,
`L235`, `L417`, `L494-495`. **But every one must now go to *nine* rows across *six* items**, not
eight across five — Wave 5 found jv 52 after the plan was written.

### Four adjacent stale sites the plan does not enumerate
`L90`, `L147`, `L187`, `L246` all carry the **superseded W5.4 numbers** ("5 of 76 attestations",
"only 1 of 9", "9 unresolvable rule ids", "correct 5 attestations forward-only"). **Correct all
four to 4 of 76 / 8 identifiers / cited by zero in the same pass**, or the keeper contradicts the
correction W8.1 makes to the register.

### Part 3 — range corrected
**Part 3 spans `L225-301`**, not the cited 239–301 (which is only §3.1–§3.6). Reduce `L239-301`
to a pointer and **retain §3.0 only if its P1–P4 rows are stamped with their wave ids**
(P1 = W0.1, P2 = W5.1, P3 = W1.1–1.3, P4 = W1.4); otherwise reduce `L225-301` entire. Today two
documents both present themselves as the plan.

---

## W8.5 — `consolidation-sweep-and-adversarial-pass.md` *(KEEPER)*

Part 3 spans **`L463-492`**; its marker is W8.7 #7.

| Target | Correction |
|---|---|
| **`L94`** | "The live database returns **zero rows**" → **10 rows, five of them real code values** (US 838–914 mm, GB 680, DE 850, AU 800–810). **What returns zero is *evidence***. The reader-impact point survives intact |
| **`L85`** (+ echoes at `L350`, `L444`) | "122 files" → **"returned 122 at `1f15381`; 126 at 2026-08-12 HEAD, the four new hits being the documents reporting this finding — a dated measurement, not an invariant."** Re-derived: 126 confirmed. **The count moved because the finding was documented** |
| **`L74`** | `exempt_paths` "69 entries" → **19 global entries + 163 per-entry paths, 62 distinct** — re-measured and confirmed |
| **`L327-328`** | "**has no replacement**" → **refuted. L04 is the replacement, dormant.** `test_db_integrity.py:1063-1115` (`record("L04", …)` at `:1108`), blocking `db_integrity` battery, documented at `check-registry.yaml:473`, created by the same commit `4fc6304` — **but with `evidence_sources` empty it has nothing to compare and passes regardless of the pointer being weeks stale** |
| **`L253-254`** | "both registered" → **`validate_conflicts` is quarantined**, as this document's own §1.6 table says |
| **`L206`, `L208`** | "thirteen times" → **21 mentions, 10 section-anchored**; "eight committed rows" → **10 rows plus 1 comment** *(carried from revision 4, not independently re-counted — flag if precision matters)* |

**Risk:** the grab-bar number is self-referentially unstable — every correction document adds a
hit. **The corrected text must carry a date**, per R-17.

---

## W8.6 — `per-stage-table-anatomy.md` *(KEEPER)*

- **`L11`** and **`L265`** — state the counting convention: 66 tables, **67 counting
  `sqlite_sequence`**, SQLite's own AUTOINCREMENT counter, excluded by convention. (AC-12.)
- **The unwritable-output count is 14, not 13 — confirmed.** `L27-30` lists 13; the missing member
  is **`item_population_elaborations`, which the document marks ⚠ NO WRITER in its own Stage 2
  table at `L94`** and omits from its own list. If it joins the list, the Stage-2 row at `L37`
  moves from 2 to 3 — **adjudicate in the same edit.**
- **The parity caveat that must be stated in one sentence.** The document also marks
  `case_studies` (`L162`), `room_items`/`rooms` (`L95`, `L226`), `weighting_profile` (`L96`) and
  `external_root_registry` (`L164`) with ⚠ and excludes all of them. `weighting_profile`
  legitimately fails the definition's "the pipeline reads it" half (that is W5.5's different
  defect); `external_root_registry` is a cut candidate; `rooms` is seeded. **But `case_studies` is
  excluded while `economics_entries` — the identical class (empty, contract-instructed, no
  writer) — is included.** Keep 14 **plus a stated exclusion reason for `case_studies`**, or the
  count is 15. **Encoding 14 without that sentence reproduces AC-23's exact defect: the
  document's own marks contradicting its own list.**
- **Five→nine propagation — the plan's three sites are the complete list:** `L81`, `L166`,
  `L246`.
- **Beyond spec: `L226`** still says `room_page.py` queries **six** non-existent tables. **Both
  readings are defensible and the honest fix states both:** six queried names are absent from the
  live schema (`room`, `room_item`, `room_item_population`, `specification`,
  `room_dar_provision`, `room_conflict`); **two are singular/plural misnames with live
  counterparts** (`rooms` 17 rows, `room_items`), and **four have no counterpart at all.** Write
  it that way rather than picking a number.

---

## W8.8 — `sessions/handoff-next-session.md` — the seventh stale document

**`.ignore` hides `sessions/**` from ripgrep, so this file is invisible-and-wrong.** Read it by
explicit path. Three stale fields confirmed: **`L4`** `PR: #91 (open)` (merged), **`L5`**
`HEAD at handoff: 804a4bf` (five merges behind), **`L9`** the plan to work from (a W8.7-bannered
source document).

**Insert after `L9`:**
```
> **STALE HANDOFF (2026-08-12):** PR #91 is merged and `804a4bf` is five merges behind; the plan
> to work from is `workplan/2026-08-12-resolution-plan.md` — always locate the current plan via
> the newest dated `workplan/` file (CLAUDE.md §9), never via this file.
```

**This is the wave's only synthesis-path touch.** Its own commit, carrying
`[DOCTRINE: <7-hex>]` before the timestamp plus attestation backfill-on-touch. **Forgetting that
is the single easiest compliance failure in all of Wave 8.**

---

## Re-derivation notes

| Cited | Status |
|---|---|
| W8.7's seven anchors (L10, L10, L11, L12, L8, L11, L463) | **ALL CONFIRMED** |
| W8.6's target filename | **CORRECTED** — `2026-08-11-…`, not `2026-08-12-…` |
| W8.1 §0.2 37–52 · §2.1 152–174 · Part 6 "282–290 exact" | **CORRECTED** — 37–51 · 152–173 · Part 6 is 273–294 (282–290 is one bullet) |
| W8.1 R-07 L85 · R-24 L138 · Part 4 L220 | **CONFIRMED** |
| W8.2 cross-map 27–37 | **CORRECTED — 27–36**; Part 3 falsity at L237-239 **CONFIRMED** |
| W8.3 §2.6 "192–195" | **CORRECTED — 191–192** |
| W8.3 L110-111, L122, L304, L306, L243-252 | **ALL CONFIRMED** as revision 4 cites them |
| W8.4 L214-215 (not 216-217), L403, L410, L467, L473, L481-482, L206 | **ALL CONFIRMED** |
| W8.4's eight "five false values" sites | **CONFIRMED complete** — but all must go to **nine across six** |
| Four further stale W5.4-number sites at L90, L147, L187, L246 | **NEW** — not in the plan's spec |
| W8.4 Part 3 "239–301" | **CORRECTED — Part 3 is 225–301** |
| W8.5 grab-bar 126; exempt_paths 19/163/62 | **RE-MEASURED AND CONFIRMED** |
| W8.5 §1.9 "no replacement" | **REFUTED** — L04 at `test_db_integrity.py:1063-1115`, dormant |
| W8.6 "14 not 13" | **CONFIRMED**, with a `case_studies` boundary call that must be stated |
| W8.6 L226 "six vs four" | **BOTH READINGS TRUE** — state it as six absent, two misnames, four with no table |
| `SYNTHESIS_RE` at `check_doctrine_token.py:46-48`; `check_commit_msg.py:57` | **CONFIRMED** |
