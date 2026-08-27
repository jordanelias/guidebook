# B2 — Keys, pointers, reference identifiers, and cardinality

**Adversarial audit of `WALKABILITY-PLAN.md` (all 1,312 lines, including Part 10), 2026-08-27.**
Lens: would the proposed keys actually work in SQLite, express the ruled cardinality, and survive
the data that exists. Every finding binds to a measurement against `data/guidebook.db`
(`user_version` 64, read-only), a file:line, or a test run on a scratch `:memory:` DB under the
session scratchpad — SQLite **3.45.1**, the container's own. No tracked file was edited; this
report is the only tracked-tree write.

**Count conventions, stated up front.** "Live rows" means the committed DB this session, read-only.
Plan line numbers are against the 1,312-line file as of this audit. "Callers" are non-archived
tree files matched by `grep -rln`, `__pycache__` and `skills/deprecated/` excluded. Test
transcripts are quoted verbatim from the scratch runs; every one is re-runnable from the SQL shown.

---

## BLOCKERS

### B2-1 · The corrected K1 placement is still unwritable — the plan adopted A3-F3's move and dropped its remedy

Plan 9.3 K1 (line 916) moves the lead key to the admission: `evi_sources.research_item_id NOT NULL`.
But `evi_sources` is renamed `evidence_sources` — **10 live rows**, and measured this session:

```python
SELECT ref_id FROM evidence_sources WHERE ref_id NOT IN (SELECT ref_id FROM source_locators)
# → REF-00965, REF-00966, REF-00967, REF-00968, REF-00969, REF-00970   (six, verified)
```

A NOT NULL column added to a 10-row table needs a value for all 10; six have no lead to point at.
A3-F3's smallest fix carried the answer — *"backfill the six no-lead sources with
`origin='hand-entered'` lead rows in the same migration, declared as legacy in its header"* — and
K1 **drops that clause while adopting the placement**, and separately brands backfill "the §2(c)
class with paperwork." As written, the T-A2 migration cannot ship: NOT NULL fails on live data, or
the column goes nullable and the ruled "the hand-off is a NOT NULL FK" spine is broken at hop one.

**The measurement that dissolves the §2(c) charge, which nobody ran:** all six have
`search_admissions` rows naming their discovering search —

```
REF-00965→exec 1 · REF-00966→exec 1 · REF-00967→exec 6 · REF-00968→exec 6 ·
REF-00969→exec 13 · REF-00970→exec 10      (SELECT ref_id, exec_id FROM search_admissions)
```

A lead row minted from that recorded act is **not** retroactive fabrication — the provenance
exists, at act grain, in a keyed table. **Smallest fix:** restore the backfill clause to K1, with
`origin='searched'` derived from the admission rows (not `'hand-entered'`, which the data
contradicts), and cite the six exec_ids in the migration header.

### B2-2 · The plan ships two contradictory DDL sources for the same keys, and its own acceptance query fails on its own corrected schema — tested

The plan's rule "Where Part 9 and an earlier part disagree, Part 9 wins" (line 862) is a footnote;
Part 7's T-A2 table is what a migration writer transcribes — exactly the A3-F1 defect class the
plan quotes approvingly, reproduced:

- **Line 735** (T-A2 hand-off table): evidence gains `research_item_id NOT NULL` **on `evi_items`**
  — refuted by 9.3 K1 (line 916), never edited.
- **Lines 744–759** (T-A2 `jud_items` column set): still carries `population_match_grade NOT NULL`,
  `study_population`, `sample_size`, `mismatch_note` "in from evidence_population_match" — the fold
  9.1-X4 (line 872) explicitly struck ("keep it as a satellite keyed on the source"). §10.3's
  jud payload (line 1211) agrees with X4 and disagrees with T-A2.
- **Line 495** (6.3 forward gap query, named as the T-A3 acceptance test): joins
  `evi_items.research_item_id`. Tested against the 9.3-corrected schema:

```
I1: plan 6.3 forward-gap query FAILS on the 9.3-corrected schema -> no such column: e.research_item_id
I2: corrected form works:
    SELECT r.ref_id FROM res_items r
      LEFT JOIN evi_sources s ON s.research_item_id = r.ref_id WHERE s.ref_id IS NULL;  -- → RES-2 ✓
```

**Failure scenario:** T-A2 is transcribed from Part 7, ships the refuted column and the refuted
fold; or T-A3's acceptance query errors and the walk is "proven" with an ad-hoc rewritten query no
document specifies. **Smallest fix:** edit lines 735, 744–759, 495 in place to the Part-9/Part-10
positions. Three edits.

### B2-3 · The per-stage allocator instruction re-arms a silent-zero defect five times, and the selftest is structurally unable to catch it — tested

Plan 6.4 (line 529) instructs the per-stage allocators to follow "the pattern `dbcore.next_ref_id()`
already establishes." The pattern includes `scripts/dbcore.py:196–198`:

```python
except sqlite3.OperationalError:
    continue          # table absent in a fixture/scratch schema
```

with `_REF_ID_HOMES = ("source_locators", "evidence_sources")` **hardcoded** (dbcore.py:180). T-B.4
renames both tables. Tested:

```
H1: next_ref_id on a post-rename schema (res_items/evi_sources hold REF-00964/REF-00970)
    -> REF-00001            # silent skip of both absent homes; should be REF-00971
H2: dbcore --selftest builds its OWN tables named source_locators/evidence_sources (dbcore.py:415-418)
    -> selftest stays GREEN after the rename. The plan's "run --selftest after any rename" defence
       cannot see this failure, by construction.
```

The safety valve for fixtures becomes a wrong answer on the real schema, and the first post-rename
mint collides with `REF-00001` (or whatever low id a table holds) — caught only by PK failure if
the id exists, silently minted if it does not. Copying this pattern into five new allocators
reproduces the trap five times, which is precisely what 6.4 says re-minting the REF-VERIFIED ids
is meant to prevent — the trap is in the *skip*, not in the malformed ids.

**Smallest fix:** in the same commit as any home rename: absent home **raises** unless an explicit
`fixture=True` is passed, and the selftest gains one assertion against the *live* schema
(`all home tables exist in sqlite_master`), not fixture tables it creates itself.

---

## MAJORS

### B2-4 · Q1 has a FOURTH option nobody considered, and it is the only one that satisfies the owner's sentence AND keeps the contest — tested

9.2 sends the owner (a) `UNIQUE(evidence_item_id)` — literal 1:1, abolishes dissent — versus (b)
NOT NULL, no UNIQUE — keeps dissent, exceeds the sentence. SQLite has a third shape neither
document reached, using the plan's own `dissent_of` column:

```sql
CREATE UNIQUE INDEX one_primary_judgment_per_evidence
  ON jud_items(evidence_item_id) WHERE dissent_of IS NULL;
```

Tested (F1/F2): a second *primary* judgment on the same evidence row is **refused**
(`UNIQUE constraint failed`); a dissent row (`dissent_of` set) is **accepted**. The owner's *"each
row of evidence provides one row for judgment"* holds literally for the primary judgment; dissent
is representable only as an explicit, typed contest naming what it contests — which is what T-A2's
own `dissent_of` note says a dissent should be. This also closes A3-F5's open item ("nothing
distinguishes a dissent row from an accidental duplicate") **in DDL**: an accidental duplicate
primary is now a constraint failure, not a silent second row. **Fix:** put this to the owner as
option (c) beside (a) and (b); it is strictly stronger than (b) and strictly more faithful than
either.

### B2-5 · Option (d) — the junction with `UNIQUE(judgment_item_id)` 9.2 recommends "outright" — breaks ratified re-entrancy — tested

Tested (G1): under `UNIQUE(judgment_item_id)`, once JUD-1 is linked to SYN-1, linking it to SYN-2
is refused. `governance/pipeline-map.yaml` (2026-08-21, cited by CLAUDE.md as still holding)
establishes that a walk **re-enters** stages: a v2 synthesis on a re-entered slug — new evidence
arrives, the slug is re-synthesized — must cite the same judgments v1 cited. Under (d) it cannot,
unless v1's links are **deleted**, destroying the record of what the superseded synthesis rested
on — an audit-trail loss in the provenance spine whose whole purpose is audit. The exact-N:1
reading is faithful to the sentence at a single instant and false over the pipeline's ruled
lifecycle. (J.2's *comparative* syntheses are unaffected — they consume via `syn_synthesis_links`
— it is *supersession* that breaks.) **Fix:** 9.2's recommendation must carry a supersession
answer before "(d) outright" is defensible: either a `superseded_by` marker on the link with the
UNIQUE scoped to live links (a partial index — same mechanism as B2-4: 
`UNIQUE(judgment_item_id) WHERE superseded_at IS NULL`, expressible because the predicate lives on
the link), or accept M:N plus writer+check. The partial-index form preserves N:1-at-any-moment,
which is arguably what the owner's present-tense sentence states.

### B2-6 · K3 is wrong that DDL cannot carry "≥1 per synthesis" — a deferred circular FK enforces it at COMMIT — tested

K1/K3 (line 918, adopting A3-F2): "Not expressible in SQLite… DDL alone cannot carry it." The
standard mechanisms indeed fail, all tested this session:

```
B: CHECK-with-subquery REFUSED: "subqueries prohibited in CHECK constraints"
C: generated-col-subquery REFUSED: "subqueries prohibited in generated columns"
D: trigger AFTER INSERT ON syn_items fires BEFORE any link can exist (item-then-links order) — aborts the valid write
A: FK source columns are NOT auto-indexed (only PK/UNIQUE get autoindexes) — 6.3's premise confirmed
```

But this works, and neither A3 nor the plan tried it:

```sql
CREATE TABLE syn_judgment_links(link_id TEXT PRIMARY KEY,
   synthesis_item_id TEXT NOT NULL REFERENCES syn_items(synthesis_id) DEFERRABLE INITIALLY DEFERRED,
   judgment_item_id  TEXT NOT NULL REFERENCES jud_items(judgment_id)  DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE syn_items(synthesis_id TEXT PRIMARY KEY,
   anchor_link_id TEXT NOT NULL REFERENCES syn_judgment_links(link_id) DEFERRABLE INITIALLY DEFERRED);
```

Tested (E1–E3): item+link in one transaction **commits**; an item with no link is **refused at
COMMIT** (`FOREIGN KEY constraint failed`); deleting the anchor link afterwards is **refused**. This
kills A3-F2's exact failure scenario — *"the session dies before the links land"* — at the engine,
not the writer: a partial write cannot commit. Caveats, honestly: (i) enforcement requires
`PRAGMA foreign_keys=ON` per connection — `dbcore.connect` sets it, raw connects may not, and
`migrate_db` replays with FK off (its before/after `foreign_key_check` diff backstops that path);
(ii) `anchor_link_id` privileges one link — it is a pointer, not a copy, but the writer must still
choose it; (iii) with a surrogate `link_id`, add `UNIQUE(synthesis_item_id, judgment_item_id)` or
the same pair inserts twice (tested, E4). **Fix:** K3 keeps its transactional writer and blocking
check (they own the vocabulary and refusals), and gains the deferred-FK shape so the invariant has
a DDL owner too. "DDL alone cannot carry it" should be corrected to "a plain junction alone cannot."

### B2-7 · The reference-id proposal never says what happens to the 875 existing REF- ids — and one branch recreates U-7

6.4 mints `RES-NNNNN`; §10.3 makes `res_item_id TEXT PRIMARY KEY -- RES-00001` the identity of
`res_items` = today's `source_locators`, 875 rows keyed `REF-*`. Nowhere does the plan say whether
those 875 re-mint.

- **If they re-mint:** the 4-row lead↔source shared identity (`REF-00325/561/578/607` in both
  tables, verified) is severed; every REF- id quoted as a *lead* in sessions, attestations,
  DR-2026-07-13, and the 6 data-migration files that write `source_locators` now names only the
  evidence row; no sweep for any of this is listed in T-B.
- **If they do not:** the column holds two shapes (`REF-*` legacy, `RES-*` new), C.1's ambiguity —
  *"REF-00325 does not tell you which stage it lives in"* — survives for the entire live corpus,
  i.e. the stated purpose of the stable codes fails for every row that exists today. And
  `evi_sources.research_item_id` becomes **byte-identical to `ref_id`** on every promoted lead —
  the exact shape of U-7 (`source_ref` = `ref_id`, 25/25 rows), the live rule-5 violation this same
  plan fixes at T-0.2. A pointer whose value always equals the row's own key is a copy of identity
  wearing a key's name.

**Fix:** one paragraph in 6.4 choosing a branch. The cheap coherent choice: freeze `REF-` as a
third closed namespace (recognised, never minted — dbcore already has the concept), mint `RES-`
only for new leads, and accept the two-shape column with `REF_ID_SHAPE` widened per stage.

### B2-8 · Re-minting the 11 `REF-VERIFIED-*` ids is mandated on a false necessity

6.4 (line 543): the 11 ids "must be re-minted **before** the per-stage allocators are written —
otherwise the same trap is reproduced five more times." Measured: the trap bites only hand-rolled
`MAX()` — verified live, `SELECT MAX(ref_id)` → `REF-VERIFIED-012` while `dbcore.next_ref_id` →
`REF-00971` — because `_MINTABLE.fullmatch` (dbcore.py:177) already excludes non-`REF-\d{5}`
shapes. Any allocator built on that pattern is immune with the malformed ids **left in place**; the
part of the pattern that actually reproduces the trap is B2-3's silent skip, which re-minting does
not touch. Meanwhile dbcore.py:174 declares REF-VERIFIED a **closed namespace, "RECOGNISED but
never MINTED"** — a deliberate design decision in code — and the ids are referenced by
`test_db_integrity.py`, `db.py`, `graph_audit.py`, `decisions/DR-2026-07-13-pipeline-contract.md`,
and the 057 baseline (grep, 9 files). Re-minting is churn across all of them, with citation-breaking
risk, purchasing nothing the regex has not already purchased. Note also: the namespace already has
a **gap** — `REF-VERIFIED-008` is absent (11 ids across the range 001–012, verified) — which no
document mentions and which demonstrates that gaps are tolerated and `max+1` never reuses them.
**Fix:** strike the re-mint precondition; keep the ids; require every per-stage allocator to use
`fullmatch` on its own strict shape (and `\d{5,}`, see B2-14).

### B2-9 · K2's re-key of `bpc_metadata` — the plan asks what breaks, and the answer is five callers it never names

Verified: **0 inbound FKs, 0 views** read `bpc_metadata` — the DDL side of the re-key is free. The
breakage is all in code that assumes **PK slug = one row per slug** (grep, 13 files; the five that
encode the assumption):

| caller | assumption | failure after re-key |
|---|---|---|
| `scripts/db.py:1766–1781` (`update_bpc_metadata`) | UPSERT keyed by slug | `UPDATE … WHERE slug=?` rewrites **every** row for the slug — a v2 or comparative synthesis is silently overwritten by an update aimed at the primary. A corruption vector, in the sanctioned writer |
| `scripts/tests/test_db_integrity.py:689` (D03) | "No duplicate slugs in bpc_metadata" | turns red on the **first legitimate** comparative synthesis (J.2's whole point) |
| `tools/evidentiary_audit.py:247` | dict comprehension keyed by slug | multi-row slugs silently collapse, last row wins |
| `scripts/generate_parts.py:294` · `scripts/generate/population_page.py:67` | one row per slug renders one entry | duplicate/garbled render entries |

**Fix:** K2 gains a caller list (these five by name plus the remaining eight files from the grep),
and D03 is rewritten to "no duplicate `(slug, kind='primary', superseded_at IS NULL)`" — the
invariant that survives the re-key.

### B2-10 · Law 2's checker flags every hand-off key the plan itself mints

Law 2 (§10.2, line 1155): an FK column must equal `singular(target) + "_id"`, checkable
mechanically; its own example resolves `evidence_item_id` → `evidence_items`. But Part 6.2 names
the tables **`evi_items` / res_items / jud_items / syn_items / spe_items`** — so
`singular(target)+"_id"` yields `evi_item_id`, `res_item_id`, … while every hand-off column the
plan writes is `research_item_id`, `evidence_item_id`, `judgment_item_id`, `synthesis_item_id`,
`specification_item_id` (lines 495–499, 735–737, 745–747, 1206). The `wiring_grammar` check that
T-C promotes to **blocking** (line 1261) therefore reds on the entire spine at the moment of
promotion — or is written with a prefix→full-word mapping table, which is a second stored home of
the stage vocabulary, the exact drift hazard A2-W6 already flagged for `stage_id[:3]`.
**Fix:** decide once in §10.2: either columns take the prefix form (`evi_item_id` — derivable,
consistent, ugly) or Law 2's `singular()` is defined as `stage_prefix⁻¹ + "_item"` **derived from
`pipeline-contract.yaml` at check time**, never stored. State it; the checker cannot be written
otherwise.

### B2-11 · §10.3's TOPIC block writes the same fact into every stage row with no agreement constraint — F3's defect, generalized to the spine

The consolidated spine (line 1190) puts `slug`, `item_code`, `population_code` on **all five**
hand-off objects. For fan-in stages that is legitimately new scope (a synthesis owns its topic).
For `jud_items` — whose parent `evi_items` row already carries `slug` (NOT NULL, verified),
`item_code` and `population_code` (both nullable, verified) — it is the same fact reachable by the
NOT NULL pointer, restated, with divergence representable: a judgment can carry slug X over a
parent extraction carrying slug Y and pass every constraint. That is A3-F3's charge against
`research_item_id` on extractions ("copies one fact… with divergence representable"), accepted by
this plan at K1, reproduced one hop later by the same plan's Part 10. Note T-A2 makes
`jud_items.item_code NOT NULL` while the parent's is nullable — so judgment must *assert* an
item the extraction may not state, unsourced. **Fix:** either drop TOPIC from `jud_items` (reach
it by join — rule 5's own answer), or name it a deliberate judgment act ("judgment assigns the
item") in the migration header and add the writer refusal + check for parent agreement where the
parent states a value.

---

## DEFECTS

### B2-12 · `spe_items`' key is stated four ways; the backward gap query assumes a fifth

(1) 6.4: mint `SPE-NNNNN`; (2) T-A2 line 419: "Keys on the canonical parameter (08-26)"; (3) 9.6:
FK to a minted parameter-code registry; (4) §10.3: `spe_item_id TEXT PRIMARY KEY`. (1)+(3)+(4) are
mutually compatible (stable row id + parameter FK); (2) is the position A3-F11/9.6 refuted and it
still stands in the transcription table. The 6.3 backward query (line 498–499) selects
`s.ref_id` from `spe_items` — a column no variant defines. The query's *shape* is correct — tested
(I3) against a mock: `LEFT JOIN … WHERE l.synthesis_item_id IS NULL` returns exactly the zero-link
specification — so the fix is one column name, but as the named T-A3 acceptance test it must name a
column that will exist.

### B2-13 · T-A2's "two tables need create-copy-swap" undercounts under the plan's own Part 10

`evi_items` and `syn_items` are counted (line 766). But §10.3 re-keys `evi_items` from
`extraction_id INTEGER` to `EVI-`-coded `evi_item_id` — a re-key, not a rename — and `spe_items`
from `specification_id INTEGER` (verified PK) to its minted code: **four** rebuilds, still all on
0-row tables, so the cost claim survives but the count is wrong, and T-A2's own FK sketch
(`evidence_item_id NOT NULL REFERENCES evi_items(extraction_id)`, line 746) pins the surrogate
integer §10.3 abolishes — a keyed spine that would need re-keying by the plan's own later section.
One pass of Part 7 against Part 10 fixes both.

### B2-14 · Allocator arithmetic edge: the 5-digit shape freezes the high-water at 99999

`"REF-%05d" % 100000` → `REF-100000`, which `_MINTABLE = REF-(\d{5})` **fullmatch refuses** — so
once any id passes 99999, `ref_id_high_water` stops seeing the top of the range and `next_ref_id`
returns a colliding id forever (loud PK failure each time, but permanent). 875 rows today; distant,
but the per-stage patterns are being written now: make them `\d{5,}` with `%05d` formatting, which
keeps 5-digit padding and survives overflow. One character per allocator.

### B2-15 · Junction indexing: the plan says "index every hand-off column" but not which direction the composite PK already covers

Tested (J1–J3): a junction PK `(specification_item_id, synthesis_item_id)` gives the left-prefix
lookup a covering index; the other direction is a `SCAN` until an explicit second index exists.
And the FK-source no-auto-index premise of 6.3 is **confirmed** (test A: only the PK autoindex
exists). So the rule is: junction = PK + exactly one extra index on the right column; the plan
should state the PK column order per junction (it never does). Live precedent already in the
schema: `idx_search_admissions_ref` (verified, J4) — `search_admissions` learned this lesson.

### B2-16 · Two dispositions for `governing_refs`; and Law 3 applied to `admitted_ref_ids` must be a delete, not a junction

§10.5 T-B (line 1260): the packed `specifications.governing_refs` "→ junctions, priority." §10.3
consolidation 2 (line 1237): `governing_refs` is a judgment-fact **copy** reached through
`spe_synthesis_links → syn_judgment_links`, i.e. it should not exist at all. Both cannot land.
(The pointer-chain position is the rule-5-correct one.) Similarly, Law 3 "kills all 7 packed
columns; each becomes a junction or is deleted": for `search_executions.admitted_ref_ids` the
junction **already exists** — `search_admissions`, kept at 9.5 — so the conversion must be the
delete branch; a new junction would be a second home of the edge that 9.5 just saved from its
worse home.

---

## Answers to the assigned questions

1. **K1 placement:** the move to the admission is right in grain (source-grained fact on a
   source-grained row) and wrong in execution — unwritable over the six no-lead sources the moment
   NOT NULL is declared (B2-1); and the plan left its own superseded placement in the transcription
   table and the acceptance query (B2-2). The six are real (verified) and *handled by neither*
   version as written; the admission rows make a truthful backfill possible.
2. **Cardinality:** the fourth option is the partial UNIQUE index (B2-4) — it, not (b), should
   face the owner's sentence; and (d) as recommended breaks re-entrancy (B2-5), fixable by the same
   partial-index mechanism on the link.
3. **≥1 invariant:** SQLite *can* do better — deferred circular FK, tested working with refusal at
   COMMIT and protected anchor (B2-6); CHECK-subquery, generated columns, and triggers all fail,
   tested, exactly as A3-F2 said.
4. **Reference identifiers:** the union-high-water rule is correct today (REF-00971, verified) and
   the "computed, never stored" principle is safe *given loud PK collisions* — the hazards are the
   hardcoded, silently-skipping home list (B2-3, the one genuine BLOCKER in this area), the
   unstated fate of the 875 legacy ids (B2-7), a re-mint mandate with a false rationale (B2-8), and
   a digit-width freeze (B2-14). Concurrency: two parallel scratch batches can mint the same id;
   the collision surfaces loudly at migration apply via the PK — safe against silent corruption,
   unsafe for parallel batches; the serial-batch discipline should be stated once in 6.4.
5. **Bidirectional walkability:** SQLite does **not** auto-index FK sources (tested, confirmed);
   6.3's core claim stands. The forward query is dead under the plan's own correction (tested,
   B2-2); the backward query is correct SQL with a nonexistent column name (B2-12); junction PKs
   cover one direction free (B2-15).
6. **`bpc_metadata` re-key:** nothing breaks in the schema (0 inbound FKs, 0 views — verified);
   five code callers break, one of them the sanctioned writer, with a silent-overwrite corruption
   vector (B2-9).
7. **Copies left standing:** T-A2's folded grade columns (B2-2); the TOPIC block on `jud_items`
   (B2-11); `research_item_id` degenerating to a copy of `ref_id` under one unchosen namespace
   branch (B2-7); `governing_refs`' junction disposition versus its pointer-chain disposition
   (B2-16).

## Attacked and could not break

- **The backward walk mechanism** (FK/junction as pointer): sound; every backward hop is an
  indexed lookup once the PKs exist.
- **6.3's premise** that FK declaration creates no index: confirmed by test, not just asserted.
- **`dbcore.next_ref_id` on the current schema:** REF-00971, correct, malformed ids excluded;
  the 875/10/4-overlap/6-no-lead figures and the 11 malformed ids all reproduce exactly (with the
  unreported gap at `REF-VERIFIED-008`).
- **The deferred-FK happy path and the ≥1 gap-check SQL shape** (I3): both behave as the plan
  needs.
- **M-4's disposal of the spec→render junction**: consistent everywhere it is mentioned; no
  dangling reference to it survives in Parts 6, 7, or 10.
- **The AFTER_DATA reading** of `migrate_db.py` (:283–330): the plan's mechanism claim for T-B is
  accurate as cited.

---

**Digest (5 lines):**
1. BLOCKERS: K1's NOT NULL is unwritable over the six no-lead sources and the plan dropped A3's backfill remedy (the six's admission rows make a truthful one possible); Part 7/6.3 still carry the refuted key placement and folded columns, and the T-A3 acceptance query fails on the plan's own corrected schema (tested); the per-stage allocator pattern inherits dbcore's silent-skip — after the rename `next_ref_id` mints REF-00001 and the selftest structurally cannot see it (tested).
2. Cardinality: a FOURTH option — partial UNIQUE `WHERE dissent_of IS NULL` — satisfies the owner's 1:1 and keeps dissent (tested); the recommended (d) `UNIQUE(judgment_item_id)` breaks ratified re-entrancy on re-synthesis (tested) and needs a supersession-scoped partial index instead.
3. ≥1-per-synthesis IS expressible in DDL: deferred circular FK refuses a zero-link synthesis at COMMIT and protects the anchor (tested); CHECK-subqueries, generated columns and triggers all fail as A3 said (tested).
4. Identifiers: the 875 legacy REF- ids' fate is unstated (one branch recreates U-7, the other defeats the codes' purpose); the REF-VERIFIED re-mint mandate rests on a false necessity; digit-width freezes at 99999; `bpc_metadata`'s re-key breaks five code callers including a silent-overwrite in `db.py`'s own writer.
5. Self-consistency: Law 2's checker flags every hand-off column the plan mints (`evidence_item_id` vs table `evi_items`); `spe_items`' key is stated four ways plus a fifth in its acceptance query; `governing_refs` has two contradictory dispositions inside Part 10.
