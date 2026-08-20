# Execution plan — walk the pipeline with provenance

**Status:** ACTIVE. **Written** 2026-08-20. **Author:** Opus 5, from four read-only Fable 5 audits
(walkability · recursion-blockers · §4 acceptance · provenance integrity), each claim re-verified
against the live repo before it was written down.

**Relation to the operative instrument.** This does **not** supersede
`decisions/DR-2026-08-19-research-restart-operative-instrument.md`. It executes its §3 step 5
("Render the determination and read it") and its §4 acceptance criterion, which remain unmet. The
instrument said "no successor document is owed"; this is a workplan file — the rule-free class —
not a DR, and §9 of this plan retires it by deletion the moment its acceptance test passes.

**Goal, in the owner's words:** *break out of recursion to effectively do research that can walk
the pipeline with provenance.*

---

## 0. The finding, in one page

Every fact below was measured on 2026-08-20 against `data/guidebook.db` (`user_version` 60) at
commit `0ac1500`. Nothing here is quoted from a prior document.

**The pipeline is populated from retrieved payload through citation-mining, and then stops dead.**

```
retrieval-log payload  →  evidence_sources  →  source_slug_links  →  evidence_population_match
     5 payloads              5 rows                5 rows                  12 rows
                                    ↓
                            specifications  ····  0 rows  ← THE CLIFF
                                    ↓
                     specification_source_links  ····  0 rows
                                    ↓
                           site/specs/*.html  ····  "not yet computed"
```

`specifications`, `specification_source_links`, `convergence_assessment`, `bpc_metadata`,
`item_bpc_links`, `reasoning_doc_citations`, `spec_value_probes`, `source_value_extractions` are
**all zero rows**. The entire answer-side of the schema exists and has never been written to.

Four consequences, each independently verified:

1. **No REF-id, DOI, or source title appears anywhere in `site/` or `parts/`.** `grep -rEo
   'REF-[0-9]{5}' site/ parts/` → 0 hits. The only rendered surface carrying the five REF-ids is
   `tools/spec-curation-vetting-surface.html` — a dashboard, not the book.

2. **There is no production writer for `specifications`.** `INSERT INTO specifications` appears
   only in `scripts/tests/` fixtures and two audit self-tests. `scripts/db.py` exposes 30+
   subcommands and not one writes a cell. The record that holds a determination, its
   `value_min/value_max/value_unit`, `governing_refs`, `tier_basis` and `falsification_condition`
   cannot be written without first writing code. **That is the recursion in one sentence.**

3. **The §4 criterion fails on exactly one component — "a determination" — and the reason given
   for not authoring it is not a gate.** The batch deferred synthesis to "the Opus floor behind
   the B-before-E gate." `grep` finds "B-before-E" only in two *comments* inside
   `scripts/audit_evidence_metadata.py` (lines 59, 169), about metadata honesty, with no bearing
   on synthesis. `governance/pipeline-contract.yaml:113-116` carries the `opus-routing` criterion
   with **`check: null`** — declared, unenforced. `best_practice_synthesis` is not a database
   column; it is a document class. The one act only research can perform was blocked by a
   sentence.

4. **The book's own outputs are unpoliced while the apparatus is heavily policed.**
   `run_checks.classify()` maps `references/search-log/…` → **no kind** and `retrieval-log/…` →
   **no kind**; `scripts/migrations/*.sql` → `schema`, `site/specs/*.html` → `render`,
   `sessions/*.md` → `synthesis`. The §4 acceptance artifact — the file the instrument names as
   *the* deliverable — triggers **zero** of the 66 registered checks (≈17,880 LOC of check
   scripts, 1,656-line registry).

---

## 1. Two kinds of block — the distinction that governs this whole plan

Every blocker found was sorted into one of two classes. **Class A resolves by doing research.
Class B does not resolve no matter how much research is done.** Confusing the two is how the last
nine months were spent: Class A emptiness was read as a defect, apparatus was built to police it,
and the apparatus became the work.

### Class A — EMPTY BECAUSE THE CONTENT DOES NOT EXIST YET

Not defects. No code, no gate, no decision fixes any of these. They resolve the moment a
determination is authored and rows are written. **Nothing in Class A justifies building anything.**

| Surface | Measured state | Resolves when |
|---|---|---|
| `specifications` | 0 rows | a determination is authored |
| `specification_source_links` | 0 rows | ↑ same act |
| `convergence_assessment` | 0 rows | ↑ same act |
| `item_bpc_links` | 0 rows | ↑ same act (13 items on this slug) |
| `bpc_metadata` | 0 rows | a slug reaches BPC closure |
| `reasoning_doc_citations` | 0 rows | a reasoning doc's citations resolve (needs Class-B fix B2-a first) |
| `spec_value_probes`, `source_value_extractions`, `gap_mining`, `connections` | 0 rows | later pipeline stages run |
| `jurisdictional_values` | 109 rows, **0** with a stored value | a code/standard clause is actually held |
| `validate_evidence_state`, `validate_verification_consistency`, `pmp_audit`, `gap_mining_audit`, `population_integrity_audit`, `reasoning_doc_citations_audit` | NOTHING-IN-SCOPE (`EXAMINED: 0`) | their subject tables receive rows |
| `site/specs/*.html` showing "Best-practice determination: **not yet computed**" | 93 pages | `specifications` receives rows |

**Rule for this class:** report as NOTHING-IN-SCOPE, never as a failure, and **never** build
apparatus to observe it. A vacuous check is not evidence that a check is needed; it is evidence
that content is needed.

### Class B — GENUINE DEFECTS

These persist through any amount of research. Each is listed with the evidence and the fix tier.

**B1 — read/write gaps (no path exists to write true data)**

| # | Defect | Evidence | Fix |
|---|---|---|---|
| B1-a | No writer for `specifications` / `specification_source_links` / `convergence_assessment` | `db.py` has no subcommand; only test fixtures INSERT | hand SQL against scratch (Phase 1) → CLI later (Phase 4) |
| B1-b | No writer for `search_candidates`, `evidence_population_match`, `economics_entries`, `case_studies`, `jurisdictional_values` | zero mentions in `db.py` | Phase 4, capped |
| B1-c | No writer for `evidence_source_authors` | zero mentions in `db.py` — **this gap is where the 2026-08-19 fabrication entered** | Phase 4, first |
| B1-d | `_ES_COLS` whitelist (`db.py:1607-1623`) excludes `url`, `pages`, `article_number`, `standard_number`, `doi_resolution_outcome`, `first_author_last`, `subtype`, `citation_count`, `superseded_by_ref_id`, `author_count_is_complete`, `citation_mining_status` | R10 unsatisfiable through the CLI; every admission needs a hand-written companion UPDATE | Phase 4 |
| B1-e | No `ref_id` allocator — `db.py next-id` covers only `connections\|gaps\|terms\|conflicts` | minting is done by eyeballing the stash high-water mark (REF-00964); the runbook's own `REF-00001` example collides from the second admission | Phase 4 |
| B1-f | No `finish-search` — `results_screened` / `results_admitted` / `admitted_ref_ids` maintained by hand | three-way parity kept manually | Phase 4 |

**B2 — orphans, dangling references and stale hardcoded facts**

| # | Defect | Evidence | Fix |
|---|---|---|---|
| B2-a | `references/bpc-reasoning/room-acoustic-performance.md` cites 11 REF-ids; **0 of 11 resolve** in `evidence_sources`; 11 of 11 sit in `source_locators` | REF-00325, 00335, 00561, 00571, 00576, 00577, 00578, 00580, 00589, 00726, 00727 | Phase 5 (re-admit) or explicit demotion to leads |
| B2-b | `site/index.html:28` links `#bibliography`; `grep -c 'id="bibliography"'` → **0** | dangling anchor; no generator writes `index.html` | Phase 3 |
| B2-c | `parts/v10/part13.md:12` hardcodes "**0 sources in the evidence base**" — DB says 5 | direct violation of CLAUDE.md §2(b) | Phase 3 |
| B2-d | 6 registry `no_floor` annotations still say "0 today" for checks that now have subjects (`evidence_sources` 5, `citation_mining` 5, `search_executions` 9, `evidence_population_match` 12) | the registry's own bookkeeping is stale | Phase 3 |
| B2-e | 68 pre-existing dangling `workplan/` references (carried from the 2026-08-19 review) | logged, unswept | Phase 3 |

**B3 — blind spots and unpopulated-but-populatable links**

| # | Defect | Evidence | Fix |
|---|---|---|---|
| B3-a | R9 duplicate gate queries `evidence_sources` only — **blind to 835 `source_locators` rows**; no live script reads or writes `source_locators` at all | proved live: REF-00607 caught only by hand; the retracted "no Tier-1 threshold" claim hinged on stash rows REF-00578/REF-00325 | OD-5 + one schema migration (Phase 5) |
| B3-b | `evidence_population_match.gap_id` NULL on 12 of 12 | column exists, never written | Phase 2, pure data |
| B3-c | `citation_mining.connections_produced` = `'[]'` in 5 of 5; the mined identifiers live only in `notes` | "81 identifiers stay in this note" | Phase 5 (needs B3-a) |
| B3-d | `slugs.serves_axes` populated on 1 of 106 | working detour exists via `items.bpc_source_slug` → `item_axis_links` (158 rows) | Phase 2, pure data |
| B3-e | `search_executions.terms_used` populated on 0 of 9 | column exists | Phase 2, pure data |

**B4 — the rendering edge (code, small and specific)**

| # | Defect | Evidence | Fix |
|---|---|---|---|
| B4-a | `scripts/regenerate_derived.sh:15-17` — the self-declared "single sanctioned regeneration entry point" — calls only three dashboard writers. It **never** calls `scripts/generate/build_site.py` or `scripts/generate_parts.py` | a DB change regenerates dashboards, not the book | +2 lines |
| B4-b | `scripts/generate/spec_page.py:95-97` SELECTs `ref_id, author_display, author_display_note, pub_year, pub_title, tier, verification_status` — **no `doi`, no `url`**; `citation()` at :132-150 therefore cannot print a chaseable identifier | a reader can see a REF-id but cannot reach the source | +2 lines in the SELECT, +1 in `citation()` |
| B4-c | `scripts/generate_parts.py:330` — per-source bibliography is an explicit stub ("render at Phase E") | `parts/` structurally cannot carry REF/DOI | Phase 3 |
| B4-d | `run_checks.classify()` returns **no kind** for `references/search-log/**` and `retrieval-log/**` | the §4 deliverable is unchecked | Phase 3, 2 registry lines |

**B5 — provenance (the owner's standing requirement)**

| # | Defect | Evidence | Fix |
|---|---|---|---|
| B5-a | `--verify-authors` compares **one property**: the ordered surname sequence. Title, year, journal, volume, issue, pages and given names are all present in the held payloads and **none are compared** | demonstrated: REF-00966's payload carries `volume: 5, issue: 4`; the DB stores both NULL; the verifier prints CLEAN | ~20 lines inside the existing verifier (Phase 2) |
| B5-b | All five batch-1 payloads are marked `BACKFILL (not contemporaneous)` — retrieved 17:54:3x, four hours after the 13:39 rows they attest | the chain terminates at bytes received *after* authoring | procedural + a verifier caveat (Phase 2) |
| B5-c | No column ties an `evidence_sources` row to its retrieval artefact; the join is DOI-by-convention through free-text `purpose` | works 5/5 today, guaranteed to rot | one schema migration (Phase 5) |
| B5-d | **The scratchpad is not persisted at all.** `retrieval-log/` holds payloads; nothing holds the commands run, the hand-written SQL executed against the scratch DB, the subagent reports, or the scratch DB's own delta. The container is ephemeral | the determination will not be reproducible | Phase 2 — a `PostToolUse` hook, harness-level |
| B5-e | 27 `source_locators.standard_number` rows carry quantified claims (`"$12,200–$15,150/unit"`, `"6,073 deaths… ~2.3× traffic fatalities"`, `"72% designers"`) with no locator and no `[UNVERIFIED-QUANT]` marker | the exact "X% across N (Author Year)" template `project-standards.md` names highest-risk, sitting where R9 and the author verifier cannot see | Phase 5, with B3-a |

**Not a defect, recorded so it is not re-litigated:** `attestations/` assert nothing a machine
reads for meaning — verified against `scripts/audit/adherence_log_audit.py` (check_5 tests row
COUNT > 0; check_6 measures textual similarity, not content). CLAUDE.md §0 already names rule 2
the next ceremony to cut. This plan neither strengthens nor removes it.

---

## 2. Standing authorisations

Recorded because the last nine months show that unrecorded permission decays into blanket caution.

1. **Owner, 2026-08-20:** *"Permission to change CI, CLAUDE.md, skills, tools and anything else
   that are currently preventing required overhaul."* Every Class-B fix below is covered. No
   further sign-off is sought for anything in Class B.
2. **Owner, 2026-08-19:** `_archived/` is allowed to grow; it is the home for retired **content**.
   Git history remains the archive for **code** — retired code is deleted, not copied.
3. **Owner, 2026-08-20:** *"the scratchpad… needs to be getting saved always for provenance."*
   Phase 2 makes this mechanical rather than remembered.
4. **CLAUDE.md §1:** removal needs *evidence*, not permission; addition carries the burden of
   proof. Every addition in this plan states what wrong thing reaches the **guidebook** without it.

**Still owner-gated and deliberately untouched:** content and doctrine (the DG-NON class) —
mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction and
work-product inclusion, licensing, trajectory. And `.ignore` edits.

---

## 3. Phase 0 — Walk one cell to the page. Zero new code. Zero new checks.

**Purpose.** Prove the pipeline is walkable end to end *before* any further apparatus exists. If
this phase needs a new script, the diagnosis in §0 is wrong and the plan stops for re-derivation.

**Target cell: `A-18` × `AUT`.**
- `A-18` = "RT60 in Occupied Learning and Listening Spaces", `items.bpc_source_slug =
  'room-acoustic-performance'`. Chosen because the batch's research question is literally about
  RT60: *"is the requirement a level (a lower reverberation figure), or a class of requirement —
  control and predictability?"*
- `AUT` is the only population on this slug carrying **two EXACT-graded Co-1 matches** (MB1-001 →
  REF-00965; MB1-004 → REF-00966), plus REF-00968 at PARTIAL.
- `DEM` is deliberately **not** the demonstration cell: it holds 8 of the slug's 13 items and no
  admission above PROXY. That is GAP-B01-002 and it is Phase 5 work, not something to paper over.

**Step 0.1 — scratch.** Per CLAUDE.md §0.3, canonical is never written directly.

```bash
S=session_2026-08-20-provenance-walk
SCRATCH=/tmp/claude-0/-home-user-guidebook/191e3639-80b1-5667-9c1c-b5be88ffcce9/scratchpad/walk.db
sha256sum data/guidebook.db | tee /tmp/canonical.sha256.before
cp data/guidebook.db "$SCRATCH"
```

`GUIDEBOOK_DB_PATH="$SCRATCH"` is prefixed **inline on every call** — the harness resets env
between shells.

**Step 0.2 — the three data rows.** Hand-written SQL against the scratch (B1-a: no writer exists).
Column names, CHECK vocabularies and FK targets below were read off the live DDL, not remembered.

```sql
-- 1. The convergence assessment. status='single_axis' is forced, not chosen:
--    validate_evidence_state.py:333 errors if axes > 1, and the three Co-1 sources
--    are ONE axis. REF-00607 (T2) is PROXY-graded for AUT, so it goes in
--    down_weighted_sources, which is not counted as an anchoring axis (§1.7 directness).
INSERT INTO convergence_assessment
  (convergence_id, status, clinical_sources, co1_sources, co2_sources,
   down_weighted_sources, discounted_sources, rationale, synthesis_approach,
   created_at, created_by_session, updated_at, updated_by_session)
VALUES
  (1, 'single_axis', NULL, '["REF-00965","REF-00966","REF-00968"]', NULL,
   '["REF-00607"]', NULL,
   '<names the axis (Co-1 lived experience, CRPD Art 4.3 co-primary) AND states the
     chain-of-one problem: REF-00968 cites REF-00965; REF-00965 cites REF-00966.
     Three documents, one lineage. REF-00607 is down-weighted for AUT: its 23-study
     base is predominantly NORMAL-HEARING adult listeners (match grade PROXY, MB1-008).>',
   NULL, '<ts>', '$S', '<ts>', '$S');

-- 2. The cell. state='provisional' is forced by DR §7 (disputed cells cap at provisional)
--    AND by the evidence: single axis, chain-dependent, no regulatory baseline admitted.
--    value_min/value_max/value_unit stay NULL ON PURPOSE — the determination is a
--    requirement CLASS, not a level. The schema supports that; asserting a number here
--    would be the fabrication of 2026-08-19 in a new costume.
INSERT INTO specifications
  (specification_id, item_code, population_code, state, design_scale, convergence_id,
   confidence_dimensions_present, confidence_dimensions_absent, confidence_synthesis_basis,
   tier_basis, governing_refs, value_min, value_max, value_unit,
   falsification_condition, code_floor_only, has_unverified_sources,
   all_sources_disqualified, regulatory_stratum_only,
   created_at, created_by_session, updated_at, updated_by_session)
VALUES
  (1, 'A-18', 'AUT', 'provisional', 'population', 1,
   '<JSON array — the confidence dimensions actually present>',
   '<JSON array — those absent: e.g. no regulatory baseline, no independent Co-1 lineage,
     no controlled room-side measurement graded above PROXY for AUT>',
   '<synthesis basis, prose>',
   'Co-1',
   '["REF-00965","REF-00966","REF-00968"]',
   NULL, NULL, NULL,
   '<falsification condition — doctrine #6. What evidence overturns this?>',
   0, 0, 0, 0,
   '<ts>', '$S', '<ts>', '$S');

-- 3. The join that makes the page cite anything. Until migration 044 this edge lived
--    only as a JSON array the generator never read, so every page it produced cited
--    NOTHING while presenting a confident determination (spec_page.py:88-92).
INSERT INTO specification_source_links (specification_id, ref_id, role, created_at, created_by_session)
VALUES (1,'REF-00965','governing','<ts>','$S'),
       (1,'REF-00966','governing','<ts>','$S'),
       (1,'REF-00968','governing','<ts>','$S');

-- 4. The item↔slug bridge (migration 013), so the page names its governing BPC.
INSERT INTO item_bpc_links (item_code, slug, link_type, rationale, created_at, created_by_session)
VALUES ('A-18','room-acoustic-performance','primary','<rationale>','<ts>','$S');
```

`<...>` placeholders are authored in Phase 1 from the sources, not filled in here. **Writing them
from memory is the exact failure of 2026-08-19.**

**Step 0.3 — capture, emit, apply.**

```bash
GUIDEBOOK_DB_PATH="$SCRATCH" python3 scripts/audit/research_batch_dod.py --session "$S"
sha256sum -c /tmp/canonical.sha256.before          # canonical must NOT have moved
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH" --out /tmp/delta.sql
python3 scripts/emit_data_migration.py --input /tmp/delta.sql --session "$S.md" \
       --summary "A-18 x AUT: first determination cell, its convergence and its governing sources"
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db     # reproducibility
```

**Step 0.4 — render.**

```bash
python3 scripts/generate/build_site.py --only A-18
bash scripts/regenerate_derived.sh
```

**Step 0.5 — the walk, executed and recorded.** Not asserted — *run*, both directions, and the
transcript saved into the scratchpad (§5):

```
FORWARD   payload 92c0026c79a3bfca.json → manifest line 2 → evidence_sources REF-00965
          → source_slug_links RAP-01 → evidence_population_match MB1-001 (AUT, EXACT)
          → specification_source_links(1) → specifications(1) → site/specs/a-18.html

BACKWARD  site/specs/a-18.html → cell 1 → specification_source_links → REF-00965/966/968
          → search_admissions (exec_id 1) → search_executions.query_text
             "autistic adults lived experience of noise and reverberation in buildings,
              qualitative interview and participatory design studies"
          → retrieval-log/…/manifest.jsonl lines 2-3
          → artefacts 92c0026c79a3bfca.json / 514f77d5b50c7aef.json
          → DOI 10.1016/j.apacoust.2025.110581 / 10.1089/aut.2022.0024

SIDEWAYS  A-18 → item_axis_links → AX-AUD (b230; d310, d115) + AX-SPR (b156, b140; d230, d160)
          → population_axis_map → AUT/NDV/DEM
          gaps GAP-B01-002 (DEM) / GAP-B01-003 (MH, BRAIN) still OPEN and visibly so
```

**Phase 0 acceptance (all four, or the phase has not passed):**
1. `grep -c 'REF-00965' site/specs/a-18.html` ≥ 1.
2. Both directions walked with every hop resolving to a real row or file — transcript in the
   scratchpad.
3. `bash scripts/preflight.sh` green, `validate_evidence_state` reporting `EXAMINED: 1` rather
   than NOTHING-IN-SCOPE.
4. **The diff contains zero new scripts, zero new checks, zero new registry entries.** This is the
   recursion test. If Phase 0 cannot be done without building something, the build is the finding.

---

## 4. Phase 1 — Author the determination

**This is the only act in the entire plan that apparatus cannot perform.** It is DR §3 step 5 and
the sole unmet component of §4.

**Preconditions, all now known to be satisfied:** the Opus floor is met by the authoring model;
`opus-routing` carries `check: null` and blocks nothing; "B-before-E" is a comment in an unrelated
script. There is no gate. There never was.

**Method — requirement-class first, then value, then solution** (the owner's ordering):

1. **Read the three Co-1 sources in full.** Not the abstracts, not the stored `notes`, and not the
   payload metadata. GAP-B01-001 exists precisely because the batch recorded claims against
   sources it had not read, and its closing condition is *"a reader other than the authoring
   session has read all five sources and confirmed or corrected every claim recorded against
   them."*
2. **State the requirement class.** The batch's own answer was *"NOT SETTLED, and my first answer
   was wrong."* The honest determination available on this evidence is at the class level:
   whether the AUT requirement is a *level* (a lower RT60 figure) or a *class* (control and
   predictability of the acoustic environment). Author whichever the sources support, including
   "the evidence distinguishes neither" if that is what they show — a rendered, sourced,
   falsifiable "we cannot yet distinguish these" **is** a determination and satisfies §4. A
   fabricated resolution does not.
3. **Do not author a value.** No admitted source supports a population-differentiated RT60
   threshold for AUT. `value_min`/`value_max`/`value_unit` stay NULL and the `falsification_
   condition` names what evidence would let a value be authored. (REF-00578 / Iglehart 2016,
   `10.1044/2016_aja-15-0064`, is held in the stash and manipulates RT at 0.3/0.6/0.9 s — that is
   Phase 5 work under B3-a, not a shortcut here.)
4. **Carry the guard forward.** The rendered log's existing guard — *"That is a real finding about
   what disabled people report. It is not a finding that rooms need less acoustic treatment"* —
   must survive into the determination text. Restoration is not silence.
5. **Preserve Co-1 attribution.** Under CRPD Art 4.3 the disabled people who produced Co-1 work
   are part of the evidence, not metadata. REF-00966's community co-authors (**Catherine Woolley**,
   **Emily @21andsensory** — Crossref renders the latter `family:"andsensory", given:"Emily"`) were
   deleted once already. They appear in the determination's attribution or the determination is
   not authored.

**Then regenerate and read it.** The instrument's words: *render the determination and read it.*
Update `references/search-log/sensory-environment/room-acoustic-performance.md` — §4's "NOT
SETTLED" is succeeded by the determination, and §5's "No determination is authored" becomes false
and is corrected. Note the file has **no committed renderer**; it is a point-in-time generation
and must be regenerated by hand from the post-synthesis DB. Building that renderer is out of scope
(it is apparatus, and one file does not justify it).

**Phase 1 acceptance:** §4's six components all hold — (1) one research question, (2) a
determination, (3) its governing sources, (4) its population-match grading, (5) its search log
including the empty searches, (6) rendered and readable as output. Components 1, 4, 5 and 6
already hold; this phase supplies 2 and repairs 3.

---

## 5. Phase 2 — Provenance: the scratchpad, always, and the verifier widened

### 5.1 The scratchpad is persisted mechanically, not by memory

**What wrong thing reaches the guidebook without this:** an unreproducible determination. Phase 1
writes hand-authored SQL and prose derived from a reading of sources; without a persisted record
of the commands run and the SQL executed, the determination's derivation is exactly as auditable
as the author lists were on 2026-08-19 — which is to say, not at all. This clears the §1 burden of
proof.

**Mechanism: a `PostToolUse` hook in `.claude/settings.json`** — the same harness-level rationale
that file already records for `SessionStart` and `Stop`: *"an agent must choose to load prose, and
attention degrades as context fills. Hooks run at the HARNESS level."* The scratchpad is saved
because the harness saves it, not because a session remembers to.

**Layout — committed, alongside `retrieval-log/`:**

```
scratchpad/<session>/
  commands.jsonl     one line per Bash invocation: ts, cwd, command, exit, stdout_sha256, bytes
  sql/NNN-<slug>.sql every statement executed against the scratch DB, in order
  agents/<name>.md   every subagent report, verbatim
  delta.sql          the emit_batch_sql.py output that became the migration
  scratch.sha256     sha256 of the scratch DB at seal time
  notes.md           free-text working notes
  manifest.jsonl     sha256 + bytes + purpose per artefact (same shape as retrieval-log)
```

Cost check, since storage objections are how this gets refused: `.git` is 18 MB and
`retrieval-log/` is 128 KB for a five-source batch. The owner's ruling stands — *"the repository
has more than enough room… it is very unlikely we will ever have to look through them unless we
are auditing for fidelity."* That is exactly right, and it is exactly when they are
irreplaceable.

**Budget:** ≤80 LOC total (the hook command plus a `record` subcommand appended to the existing
`scripts/research/retrieval_log.py`, which already owns the `<session>/manifest.jsonl` shape). **No
new script file. No new registry entry in this phase.**

### 5.2 The author verifier is widened to every field the payload already holds

`verify_authors()` (`scripts/research/retrieval_log.py:143-195`) compares the ordered surname
sequence under NFKD folding and nothing else. Extend the comparison to the fields already sitting
in the stored payloads: `title` → `pub_title`, `issued` → `pub_year`, `container-title` →
`journal_name`, `volume`, `issue`, `page` → `pages`/`pages_start`/`pages_end`, and
`author[].given` → `evidence_source_authors.first_name`.

**What wrong thing reaches the guidebook without it:** a fabricated title, year or journal over a
correct DOI passes CLEAN today. Proven, not hypothesised: REF-00966's payload carries
`volume: 5, issue: 4`; the DB stores both NULL; the verifier prints CLEAN.

**Budget: ~20 lines inside the existing function.** Zero new files, zero storage, zero new checks.
Rename the reported result from `CLEAN` to `CLEAN (authors only)` until the widening lands, so the
tool stops overstating.

### 5.3 Contemporaneity is labelled

`--verify-authors` prints CLEAN over `BACKFILL` payloads with no caveat, though
`retrieval_log.py:198-204` internally knows the difference. Emit `BACKFILL: n` alongside
`EXAMINED: n`. **~4 lines.** Future sessions retrieve *through* `fetch()`, whose write-before-return
guarantee makes the payload contemporaneous by construction.

### 5.4 Pure-data provenance backfill (zero code, one migration)

- `evidence_population_match.gap_id` — 12 rows, currently NULL: point each at the gap it bears on.
- `slugs.serves_axes` for `room-acoustic-performance` — derive from `item_axis_links`, do not
  guess.
- `search_executions.terms_used` — 9 rows, currently 0 populated.

---

## 6. Phase 3 — Make the rendering edge and the check surface tell the truth

All Class-B, all small, all covered by the standing authorisation.

| Fix | Change | Lines |
|---|---|---|
| B4-a | `scripts/regenerate_derived.sh`: add `python3 scripts/generate/build_site.py` and `python3 scripts/generate_parts.py` to the regeneration set, before the `--check` gates | +2 |
| B4-b | `scripts/generate/spec_page.py:95-97`: add `e.doi, e.url` to the SELECT; `citation()`:132-150 renders the DOI as a link | +3 |
| B4-d | `governance/check-registry.yaml` kinds: map `references/search-log/**` and `retrieval-log/**` to a kind so the §4 deliverable is inside the check surface at all | +2 |
| B2-b | `site/index.html:28` — remove the dangling `#bibliography` link or give it a target | 1 |
| B2-c | `parts/v10/part13.md:12` — replace the hardcoded "0 sources" with a generated count or a dated drift warning (CLAUDE.md §2(b)) | 1 |
| B2-d | 6 stale `no_floor: "0 today"` registry annotations — re-derive from the live DB | 6 |
| B2-e | Sweep the 68 pre-existing dangling `workplan/` references | — |

**Deliberately NOT done here:** `generate_parts.py:330`'s bibliography stub (B4-c). `parts/` is
a v10 snapshot and the book's spine is `site/specs/`. Doing both doubles the render surface for
one walkable cell. Revisit when a second slug has a determination.

---

## 7. Phase 4 — The write path, capped

**The cap is the point.** §12.5 of the instrument currently defers all of this to "batch 2
automates," which guarantees one more code-before-research cycle. This phase exists to end that,
and it runs **after** Phase 0 and Phase 1 have already landed a determination — so the code is
written against a proven need, not a predicted one.

**Hard budget: 300 LOC total, all inside `scripts/db.py`. Zero new files. Zero new checks.**
Anything that does not fit is not built; it is done by hand and the hand-SQL is saved to the
scratchpad, which is now automatic.

Ordered by damage already caused:

1. **`db.py add-authors`** (B1-c) — the fabrication vector. Writes `evidence_source_authors`
   directly from a logged payload, never from prose. ~60 LOC.
2. **`db.py next-ref-id`** (B1-e) — allocate above the `source_locators` high-water mark, not
   above `evidence_sources`, or it collides with a held identifier. ~20 LOC.
3. **Widen `_ES_COLS`** (B1-d) — add `url`, `pages`, `article_number`, `standard_number`,
   `doi_resolution_outcome`, `first_author_last`, `subtype`, `citation_count`,
   `superseded_by_ref_id`, `author_count_is_complete`, `citation_mining_status`. This deletes the
   mandatory hand-written companion UPDATE from every admission. ~15 LOC.
4. **`db.py finish-search`** (B1-f) — one call maintains the three-way parity between
   `results_screened`, `results_admitted`, `admitted_ref_ids` and the `search_admissions` junction.
   ~40 LOC.
5. **`db.py add-match`** (B1-b) — `evidence_population_match`, the R13 grading write. ~35 LOC.
6. **`db.py add-cell`** (B1-a) — `specifications` + `specification_source_links` +
   `convergence_assessment`, written as one transaction so a cell can never exist without its
   convergence row or its source links. ~90 LOC. **Written only after Phase 1 has done it by hand
   once** — the hand-execution defines the interface.

`search_candidates`, `economics_entries`, `case_studies` and `jurisdictional_values` get **no
writer** in this phase. Batch 1 wrote zero rows to all four. Build them when a batch needs them.

---

## 8. Phase 5 — The next batch, aimed at the open gaps

Only now does more research start, and it is aimed rather than opportunistic.

**5.1 — OD-5, the highest-value open decision.** The R9 duplicate gate is blind to 835 held
identifiers and no live script reads `source_locators` at all. Batch 1 proved it load-bearing
three separate ways. This needs one owner signature plus one schema migration whose SQL is already
drafted in the instrument's §6, plus the R9 union query change. **It is a prerequisite for 5.2 and
5.3.**

**5.2 — Close GAP-B01-003 (cheapest close, no admission required).** Its condition is *"MH and
BRAIN each carry either a graded admission or a logged, well-formed absence."* Two well-formed
searches, logged verbatim before screening per R8, with an R14 diagnosis distinguishing
query-shape failure from wrong index from genuine absence. Zero admissions needed.

**5.3 — Close GAP-B01-002 (the one that matters most).** DEM carries 8 of the slug's 13 items and
no admission above PROXY — the population weighted heaviest was served worst. The gap row already
names three admission-ready DOIs: Markussen 2024 `10.3397/in_2024_4004`, Faieta 2023
`10.1016/j.apmr.2022.12.188`, Salminen 2024 `10.3233/shti240942`. One full R1–R15 admission walk,
now through the Phase 4 write path, with contemporaneous `fetch()` payloads.

**5.4 — Resolve the 11 orphan citations (B2-a).** `references/bpc-reasoning/room-acoustic-
performance.md` cites 11 REF-ids, none of which resolve. After 5.1 they are promotable from
`source_locators` as data. Either promote them through a full admission walk **or** demote the
document's claims to leads and say so in the document. Leaving 11 orphan citations in the only
reasoning deliverable is not an option.

**5.5 — Sweep the 27 unmarked quantified claims in `source_locators.standard_number`** (B5-e).
Each gets a locator or an `[UNVERIFIED-QUANT]` marker.

---

## 9. Acceptance and termination

**The plan's own acceptance test** — Fable's five conditions for an unqualified "the recursion is
broken", adopted verbatim:

1. A §4-satisfying artifact — a determination, rendered as the answer.
2. **Zero** new scripts, checks or registry entries in the batch's commits.
3. At least one GAP-B01 gap closed by its own falsification condition.
4. A first pass that survives its adversarial pass without headline retractions.
5. A session record that ends by naming the next **research question**, not the next governance
   act.

Condition 5 has a measured precedent: the last session record ends by naming OD-5. That is a
governance act. Point 5 is the one this plan is most likely to fail, and it is checked last on
purpose.

**Phase gates.** Phase 0 must pass with a zero-apparatus diff before Phase 1 begins. Phase 1 must
land a rendered determination before Phase 4 writes a single line of CLI. **If any phase requires
apparatus that phase did not predict, stop and record why — that is a finding about the pipeline,
not a task.**

**This document retires itself.** When §9's five conditions hold, this file moves to
`_archived/workplan/` (content, per the 2026-08-19 ruling) and nothing replaces it. The next
artifact is a search log, not a plan.

---

## 10. What this plan forbids

1. **No new check, script or registry entry before Phase 4** — and in Phase 4 only the six named,
   inside `scripts/db.py`, within 300 LOC.
2. **No apparatus built to observe a Class-A emptiness.** A vacuous check means content is
   missing, never that a check is missing.
3. **No bibliographic field written from memory when a payload is in hand.** The payloads are on
   disk; there is no circumstance in which recall is the cheaper path.
4. **No value authored without a locator.** `value_min`/`value_max` stay NULL until a source
   supports them; a quantified claim without a locator carries `[UNVERIFIED-QUANT]`.
5. **No `stated` cell in Phase 0 or 1.** Single-axis, chain-dependent Co-1 evidence with no
   regulatory baseline caps at `provisional`, per DR §7 and `validate_evidence_state.py:253-258`.
6. **No writing to `data/guidebook.db` directly.** Scratch → `emit_batch_sql.py` →
   `emit_data_migration.py` → `migrate_db.py`. Append-only; fix forward.
7. **No deleting or backfilling an empty search.** A zero-yield search is a completed unit of work
   (R8).

---

## 11. Risk register

| Risk | Why it is real here | Mitigation |
|---|---|---|
| Phase 1 authors a determination the sources do not support, to satisfy §4 | §4 is the criterion under pressure; 2026-08-19 fabricated author lists under exactly this pressure | "the evidence distinguishes neither" is an acceptable determination; `value_*` stay NULL; the mandatory adversarial pass runs before the commit is final |
| Phase 4's 300-LOC cap is exceeded "just this once" | every one of the ~35k executable LOC was added just this once | anything over the cap is done by hand; the hand-SQL is saved to the scratchpad automatically |
| The scratchpad hook is written, then quietly disabled when it is noisy | the doctrine token was also enforced push-only and never caught anything | the hook writes files; if `scratchpad/<session>/` is absent at session close, the session is not reproducible and says so in its record |
| Phase 3's classifier change pulls the search log into blocking checks and makes the deliverable expensive to publish | this is precisely the CLAUDE.md §0 rule-2 tax pattern | map to an advisory kind first; promote only if a real defect gets through |
| GAP-B01-001 cannot be closed by the authoring session by definition | its condition requires a reader other than the authoring session | left open and named as owner-side work; it does not block Phases 0–4 |

---

## 12. Sequence

```
Phase 0  walk one cell, zero apparatus          ── gate: zero-apparatus diff
   ↓
Phase 1  author the determination               ── gate: §4's six components hold
   ↓
Phase 2  scratchpad always + verifier widened   ── ≤80 + ~24 LOC, no new files
   ↓
Phase 3  rendering edge + check surface truthful ── ~15 lines across 7 files
   ↓
Phase 4  the write path, capped at 300 LOC      ── only after a determination exists
   ↓
Phase 5  OD-5 → GAP-B01-003 → GAP-B01-002 → orphans → quantified-claim sweep
   ↓
retire this file to _archived/workplan/; next artifact is a search log
```
