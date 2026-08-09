# 2026-08-09 — Locator hierarchy follow-on, and an enforcement probe of the session's stipulations

**Status:** IN PROGRESS
**Predecessor:** `scripts/migrations/053_locator_hierarchy.sql` (schema 53, columns added, no row touched)
**Governing decision:** `decisions/DR-2026-08-06-clean-room-evidence-reset.md` §3 — adequacy of
identification and verification is **class-relative**

> **This document was adversarially reviewed on 2026-08-09 and substantially corrected.**
> The first draft's central organising claim was a misdiagnosis, one of its findings was
> simply false, and its top-priority fix rested on a false premise about what an owner
> decision was waiting for. §4 is the correction log; the review is not hidden in it.
> **Verification note:** the probe harness lives in session scratch (`/tmp`), not in the repo.
> Every verdict below is reproducible only by re-running the command quoted with it. Where a
> claim has no quoted command, treat it as unaudited.

---

## Part 1 — Locator hierarchy: three findings

Migration 053 added the levels `division > part > section > subsection > paragraph > clause >
subclause` (plus `_end` spans and `loc_note`) to `jurisdictional_values`,
`source_value_extractions` and `reasoning_doc_citations`. It deliberately touched no row.

### 1.1 The scheme registry: a table is preferable, for FK integrity — not because a dict drifts

`locator_scheme` answers three questions no row can answer for itself:

| Job | Why the row cannot answer it | Live example |
|---|---|---|
| Which levels exist | Same depth, different name per family | ISO's top numbered level is a *clause*; ADA's is a *section*; NCC sits beneath a *volume* |
| How to render | Sigil and separator are family properties | `§404.2.5` · `clause 20` · `Art. R111-19-2` · `Vol 1 D3.3` |
| How to sort | String order is wrong by default | as text `['§12.10','§12.2','§12.9','§9.1']`; cast per level `['§9.1','§12.2','§12.9','§12.10']` |

**The first draft argued "a dict means renderer, sorter and validator each need a copy, and
copies drift." That is false in Python and the repo is its own counterexample:**
`register_integrity_check.py:34` imports `REGISTER_MAP` from the renderer, commented
"(single source of truth)", with a `lint_register_map` guard against content regressions —
one definition, three consumers, no copies. The honest argument for a table is narrower:
**FK integrity**, so a mistyped `locator_scheme` is refused at insert. That is respectable but
modest for a dozen rarely-changing values, and a `CHECK` constraint gets most of it. Against
it: a new table needs a schema migration, a seed migration, and a Pydantic mirror — and §2.3
below records that this repo does not reliably keep tables mirrored, so the proposal creates a
fresh instance of the defect it sits next to. The sort-cast rule is inert data until code
interprets it, so sorter logic stays in code either way; a table relocates parameters, not
behaviour.

**Recommendation, hedged to the evidence:** a table is preferable for FK enforcement; an
imported dict plus a lint is a defensible alternative. This is not the settled question the
first draft made it.

**How many families?** Not twelve. The twelve leading-token families cover **97 of 109 rows**.
Twelve rows fall outside all of them — `AD M`, `BB93`, `BCA Code 2019`, `CSA B651:2023`,
`DfT Guidance 2021`, `E DIN 18040-2:2023`, `IBC 2024 / A117.1`, `IEC 60118-4:2018`,
`JIS T 9251:2014`, `NFPA 72 / ADA §702`, `NS 8175:2019`, `SIA 500` — each effectively its own
family, giving roughly **24**. The counted twelve are DIN 19 · AS/NZS 16 · ADA 15 · BS 15 ·
ISO 12 · Arrêté 5 · EN 4 · TEK17 4 · Building Regs 2 · ANSI 2 · NCC 2 · IPC 1, and even DIN's
19 depends on an unstated call: excluding `E DIN 18040-2:2023` gives 19, including it 20.
**A registry sized for 12 when the data holds ~24 is the kind of undercount that makes a
lookup table fail closed on real input.**

### 1.2 The round-trip detects LOSS. It does not verify correctness.

Decompose → re-render → diff against the original string. The first hand-decomposition of
eight real citations scored **5/8**:

- `ADA 2010 §404.2.5` — filled section+subsection, **silently dropped the paragraph `.5`**
- `BS 8300-2:2018 §8.2.1` — same, dropped `.1`
- `NCC Vol 1 D3.3` — identity edited (`NCC` → `NCC 2022`)

Corrected to three levels where the document has three: **8/8 lossless.**

The circularity objection fails — string equality cannot be gamed by the author who wrote the
decomposition. But the first draft's title claim ("the round-trip **is a verifier**") overruns
what that establishes, in three ways that must be declared rather than discovered later:

1. **Blind to render-identical misassignment.** Putting ADA's `.5` in `loc_subsection` rather
   than `loc_paragraph` re-renders byte-identically when adjacent levels share sigil and
   separator. The level semantics that are the entire point of the scheme go unverified.
2. **Decomposer and renderer share one author and one scheme table.** A shared
   misunderstanding of a family's structure passes 8/8 forever.
3. **The escape hatch is unenforced by this document's own taxonomy.** "`rendered == original`
   **or** an explicit normalization note" — the NCC row failed the diff and was waved through
   as "a normalization, not a loss" by authorial fiat. Any failure can be.

n=8 hand-picked rows licenses nothing about the other ~101.

**Requirement, restated to what it supports:** every row the splitting migration touches must
satisfy `rendered == original`, or carry a normalization note **that names which token
changed**. To establish more, two things are needed: a second decomposer (or the eventual
regex splitter) run blind against the same rows with disagreements adjudicated, and a mutation
test that perturbs level assignment *without* changing the rendered string — confirming the
round-trip cannot catch it, so the blind spot is declared.

### 1.3 The re-key is sound future-proofing. It was not "reproduced."

`UNIQUE (item_code, jurisdiction, standard_name)` is unique today **only because
`standard_name` still carries the clause.** Post-unpack, both ADA rows carry the document
identity `'ADA 2010'`, and against one item in one jurisdiction that raises:

```
IntegrityError: UNIQUE constraint failed: jurisdictional_values.item_code,
  jurisdictional_values.jurisdiction, jurisdictional_values.standard_name
```

**The first draft wrote that "inserting two genuine ADA citations — `§404.2.5` and `§604-608`
— raised" this. As worded that is false:** those two raw strings differ, so the constraint
could not fire on them. What was actually inserted was the *post-unpack identity* for both
rows, which is the correct test — but is not what the sentence said.

And "reproduced, not predicted" was inflation. What the probe showed is that a UNIQUE
constraint raises on a duplicate key: SQLite semantics, never in doubt. The empirical question
is whether *live* data collides after decomposition, and the answer — confirmed independently
— is **zero collisions across all 109 rows**. Nothing was reproduced that the migration header
had not already settled deductively. The recommendation survives as future-proofing; the
evidentiary claim does not.

**Open and unargued:** the header asserts the key must gain the locator "**and the `ref_id` FK
that table has never had** — in the same migration." No argument is given for the coupling,
and it sits in unacknowledged tension with DR-2026-08-06 §3, which *defends* this table's lack
of `ref_id` as class-appropriate (the source of a code value is the code standard itself).
Either the coupling gets an argument or the FK is separated from the re-key.

### 1.4 Multi-document rows: 18, not "~17"

21 rows contain `/`; 3 are false positives (`ANSI/ASA S12.60-2010`, `AS/NZS 1428.4.1:2009`,
`AS/NZS 2107:2016` — single standards jointly issued, and splitting them would invent a
source). 21 − 3 = **18**, and `DIN 18040 + DIN EN 81-41` is a **19th** multi-document row
joined by `+` rather than `/`, which no slash-based scan would find. Of the rest, some are two
independent attestations of one requirement and some are one document citing another
(`IPC / ADA reference`); those mean different things for code convergence and cannot be told
apart by a regex. **Splitting remains owner-gated.**

### 1.5 Migration 053's committed header carries unaudited numbers

Its rationale states "85 rows cite one level, 9 cite two, 3 cite three." That sums to **97, not
109**; only **24** of 109 rows carry an explicit `§` locator; "3 cite three" reproduces exactly
(`§404.2.5`, `§404.2.9`, `§4.3.6`); and **"85" is numerically identical to the count of rows
carrying no locator at all** — which is the likeliest explanation and would make the sentence
mean the opposite of what it says. No parse rule is committed anywhere, so none of it is
reproducible.

**This is worse than a wrong number in a workplan: it is wrong prose inside a committed
migration, which is the artifact future sessions treat as settled.** It is deliberately **not**
being edited here — migrations are immutable once committed, and §2.1 demonstrates that editing
one is undetectable, so doing it casually would be the exact act this document warns about.
The correction belongs in a follow-on migration's header or a DR, and the numbers should be
regenerated from a committed parse rule or struck.

---

## Part 2 — Enforcement probe

Every stipulation identified this session, tested by **attempting what should be refused**.
Verdicts: **ENFORCED** (mechanically refused) · **UNENFORCED** (the attempt succeeded) ·
**VACUOUS** (a check passed having examined nothing).

### 2.1 A tampered committed migration rewrote 80 rows, and the blocking gate printed PASS

Append one legal statement to the most recent committed data migration —

```sql
UPDATE slugs SET status = 'STUB' WHERE status = 'ACTIVE';
```

| Gate | Level | Result |
|---|---|---|
| `migration_reproducibility` | **blocking** | **exit 0** — `PASS: the committed DB matches what the migration history produces.` |
| `migration_reproducibility --deep` | advisory | exit 1 — `slugs CONTENT 80 rows; status(80)` (and `data_migrations`, whose ledger `content_sha` tracks the tampered file) |

80 is `SELECT COUNT(*) FROM slugs WHERE status='ACTIVE'`, of 106. The blocking gate compares
`PRAGMA user_version` plus `COUNT(*)` on six tables; an UPDATE changes neither, so the gate
does not merely miss the tamper — it *affirms* the DB as reproducible.

**What this is and is not.** It is a genuinely new *vector* — tampering with committed
migration history, testing immutability (D6) — where the 2026-08-01 demonstration recorded in
`tooling-register.md` §4.2 (F10) hand-edited a scratch DB. It is **not** new evidence that the
blocking gate is tamper-blind. See §2.4: the first draft claimed it settled an owner decision
it says nothing about.

**Getting here took four attempts, and the three failures are the method's point.** Tampering
an *early* migration was absorbed — later migrations re-created the rows, and deep saw a 1-row
`TIMESTAMPS` difference and passed. Tampering with `slug_id` failed on a nonexistent column.
`status='TAMPERED'` was refused by a real CHECK on `slugs.status` — a genuine enforcement found
by accident. **A probe that fails for the wrong reason reads exactly like a rule being
enforced**, which is how unenforced rules survive audits.

### 2.2 Scope of the blind spot, measured

| | |
|---|---|
| tables | 66 total · **6 counted** · 2 exempt (DR-2026-05-28) |
| rows | 4,245 total · **93 counted — 2.2%** (all of it `items`; the other five are 0 post-reset) |

Largest unwatched: `term_aliases` 2,382 · `item_population_links` 372 · `data_migrations` 314 ·
`item_axis_links` 158 · `decisions` 157 · `term_item_links` 147 · `jurisdictional_values` 109 ·
`slugs` 106. *(The first draft's version of this list omitted `term_item_links`, the
sixth-largest — a list about absence-blindness that dropped a row.)*

`DELETE FROM jurisdictional_values` — all 109 rows of frame data the reset deliberately
preserved — passes the blocking gate at exit 0. An INSERT to a counted table *is* caught;
only **count-preserving** writes are invisible.

### 2.3 Verdicts

**ENFORCED — verified by attempting the refused thing**

| Probe | Stipulation | Evidence |
|---|---|---|
| E1 | VERIFIED without `--verification-method` refused (D-0157) | `ValueError`, exit 1 |
| E2 | R9 — duplicate DOI refused | first 0, duplicate `already filed as …(R9)` exit 1 |
| E5 | Frozen coverage grid refuses writes | `search_coverage is FROZEN`, exit 2 (`FrozenGridError`) |
| D7 | `GUIDEBOOK_DB_PATH` contract | 52/54 honour it, 2 documented exemptions |
| — | `slugs.status` CHECK | refused `'TAMPERED'` |

**UNENFORCED**

| Probe | Stipulation | What happened |
|---|---|---|
| D1 | Direct UPDATE to a *counted* table caught | exit 0 |
| D2 | Direct UPDATE to an uncounted table caught | exit 0 |
| D3 | Deleting an entire uncounted table caught | 109 → 0, exit 0 |
| D6 | Committed data migrations are immutable | §2.1 |
| D5b | Migration 053's three tables have model parity | `reasoning_doc_citations` has 16 new locator columns and **no Pydantic model at all** (verified: zero `class ReasoningDocCitation` hits repo-wide) |
| E3 | `verification_status` constrained **at the SQL layer** | no CHECK, while `verification_disposition`, `verification_method`, `verification_closure_reason` all have one |

**E3 is narrower than the first draft claimed.** The field *is* constrained three other ways —
a Pydantic `VerificationStatus` enum (`schemas/enums.py:265`), argparse `choices`, and `db.py`
refusing VERIFIED without a method. It is unconstrained only in SQL, which matters exactly
because **migrations bypass all three**.

**RETRACTED — the first draft was wrong**

| Probe | First-draft claim | Fact |
|---|---|---|
| D5 | "Table ↔ Pydantic parity is checked by nothing" | **False.** `validate_pydantic_schemas --strict` is registered and running (`check-registry.yaml:605`, advisory, 236 findings); its registry note calls it "the only tool that checks it." The defensible narrow claims are that it is *advisory not blocking*, and that it compares columns of tables that *have* models — so it structurally cannot flag D5b's model-less table. |

That error has a history: `tooling-register.md` §F3 records making the identical mistake twice
in one day — *"before calling a tool broken, check whether it has a mode you did not invoke…
The lesson did not generalise by being written down."* **This was the third instance.** The
first draft then proposed building a duplicate checker, which would have violated standing
guardrail 3 (extend the existing apparatus, don't spin up a new sweep).

**VACUOUS — passed having examined nothing**

| Probe | Subject count |
|---|---|
| E4 — T4–T6 walled off from ●/◐ (Option A) | `evidence_cell_state` = 0 |
| E6 — R8, zero-yield searches undeletable | `search_executions` = 0 |
| E7 — R13, no admission without a population-match row | `evidence_sources` = 0 |

E7 moved here from UNENFORCED. Calling R13 "100%-observed practice" was compliance asserted
over an empty set — the very failure this document catalogues, committed in its own fix list.
Historically it is worse than vacuous: DR-2026-08-06 §1 records **824 of 863 sources with no
recorded admission.** The reset happened *because* R13 was not practised.

### 2.4 What the findings actually share: scope-blindness, not deletion-blindness

**The first draft claimed a pattern — "this repo detects wrong content, not absent content" —
and it does not survive.** Three reasons, each sufficient:

1. **It is backwards for the database layer.** §2.1's headline *is* the blocking gate failing
   to detect wrong content. Within its six-table scope, `COUNT(*)` catches deletion and is
   blind to UPDATEs — the opposite of the slogan.
2. **The register-selftest instance was misdiagnosed.** `register_integrity_check.py` contains
   a purpose-built absence detector (lines 158–170: *"row exists but no rendering appears in
   the document; suppression of a determination is an integrity failure"*), added after a real
   incident where a document froze at 7 of 15 cells. Its selftest was SILENT on "a whole cell
   section deleted" because `evidence_cell_state` has **0 rows**: `set(db_rows) - set(cells)`
   is empty whatever is deleted, and the empty dict also disables the doc→DB cross-check at the
   `if db_rows:` gate. **That is vacuity (E4's class), not deletion-blindness** — so the true
   clustering is selftest+vacuity together and the DB gate apart. The one layer the draft said
   "was never built to answer *is this still here?*" is the one layer that demonstrably was.
   The selftest also self-reports the miss and exits 1; the draft did not mention that it
   already knows.
3. **"Fix them together" was rhetorical.** Fix 1 is a registry flip on one check; the selftest
   needs a fixture DB or a fail-on-empty guard in a different script. Three findings, three
   remediations.

**What they do share is scope-blindness: each check's subject set is narrower than its claim.**
Six tables of 66; a document comparison with zero DB rows; a marker checker with zero cells.
That frame is honest, but it is not a discovery — the registry already carries `EXAMINED:` and
fail-on-empty guards (`readonly_db_open_audit`, `session_pointer_resolvable`), and CLAUDE.md §10
already says "when a check passes, check that it had a subject." It also covers only ~3 of the
9 findings: E3's missing CHECK and D5b's missing model fit it not at all.

### 2.5 Fixing D5b uncovered a quieter gap: an unmapped model is invisible, exactly like a missing one

`validate_pydantic_schemas` does not discover models by convention — it reads a curated
`MODEL_TABLE_MAP`. **A model that exists but is not in that map is reported in the "no mapped
model" list exactly as if it did not exist**, so its mirror can drift with nothing to notice.

Migration 053's three tables were in three different states, and only one was healthy:

| Table | Before | After |
|---|---|---|
| `source_value_extractions` | mapped, compared | unchanged (drift: 11 columns, pre-existing) |
| `reasoning_doc_citations` | **no model at all** | model written, 34/34 parity, compound CHECK mirrored → **OK** |
| `jurisdictional_values` | model existed, **never mapped** | mapped → **DRIFT**, 5 audit columns (`jv_id`, `created_at`, `created_by_session`, `updated_at`, `updated_by_session`) |

The `jurisdictional_values` drift was invisible for as long as the map lacked the entry. It is
mild — housekeeping columns, the same shape as `slug.Slug`'s — and **the 16 locator columns
show no drift**, which was the thing worth confirming. Mapped tables went 15 → 17; unmapped
live tables 51 → 49; total findings 241 → 246, all five newly *visible* rather than newly
caused.

This is the same shape as the vacuity findings and belongs with them (§2.4): the checker's
subject set was narrower than its claim, and the shortfall was silent.

---

## Part 3 — The owner decision, and the input it was actually waiting for

The first draft made promoting `migration_reproducibility_deep` to blocking its top fix,
asserting "§2.1 is the evidence the decision was waiting on." **That is false, and the error is
instructive.** The deep check was *created* on 2026-08-01 *because of* a tamper demonstration
— registry note: *"Added 2026-08-01 after an adversarial trace showed the blocking check above
passes on a tampered DB."* Tamper-blindness was never the open question. `tooling-register.md`
§4.2 states twice what is: *"an owner choice between widening the DR's exemption list and
requiring those jobs to emit migrations. Promoting it before that decision would block every
data PR on a divergence the project may well consider legitimate."*

So the useful contribution is not a fifth tamper demo. **It is enumerating the legitimate
writers, which is what the decision needs and what nobody had written down.**

### 3.1 Every table written outside migrations, measured

| Table | Written by | Trigger | On the DR-2026-05-28 exemption list? |
|---|---|---|---|
| `evidence_source_authors` | `resolve_dois.py:558` INSERT | weekly Mon 06:00 | **yes** |
| `pipeline_runs` | `resolve_dois.py:1013` UPDATE | weekly | **yes** |
| `url_verification_runs` | `verify_urls.py:483` UPDATE | bi-weekly | **NO** — 5 rows live |
| `evidence_sources` | `resolve_dois.py:590` UPDATE | weekly | **NO** — counted, but UPDATE is count-preserving so the blocking gate is blind; deep would fire |

**The exemption list covers two of four write targets.** That is the decision, stated concretely
for the first time: `url_verification_runs` and `evidence_sources`-by-DOI-resolution are
legitimate out-of-migration writers that are not exempt.

### 3.2 Why this is prospective, not current

Deep passes **today** — clean-state run: exit 0, one table differing in timestamps only
(`slugs`), `VERDICT: PASS`. The post-reset emptying of `evidence_sources` removed the 277-row
divergence that originally justified advisory status. **The trap is the next cron run:** the
bi-weekly `verify-urls.yml` writes `url_verification_runs`, deep fires, and a newly-blocking
gate goes permanently red on a legitimate write — the *"once red is normal, a newly-red check
carries no information"* ecology that §4.4 of the register names as the worst outcome.

**There is a window.** Deep is green now and the corpus is empty; this is the cheapest moment
this decision will ever have. It is still owner-gated, and this document does not take it.

### 3.3 The cheaper fix that dominates for deletions — and its identical blocker

For the *absence* failures (D3: a whole table deleted passes), widening the blocking gate's
`COUNT(*)` from 6 tables to all non-exempt tables is trivial and carries none of deep's
volatile-classifier risk. **But it inherits exactly the same blocker:** `url_verification_runs`
would be counted, and the next cron run diverges. Both fixes are gated on §3.1, which is
therefore the real first step — not a fallback.

**And note F2, which the first draft's ranking ignored entirely: `main` is not
branch-protected**, so *no* blocking promotion stops anything. Enabling protection (§6.7) is
the highest-value act available, it is an owner action, and it was not on the list.

---

## Part 4 — Fix list

Ordered by what is actually unblocked, with gating stated.

| # | Fix | Gate | Notes |
|---|---|---|---|
| 1 | **Decide the exemption list** for `url_verification_runs` and `evidence_sources`-by-DOI (§3.1) | **owner** | Blocks fixes 2 and 3 both. Window is open now (§3.2) |
| 2 | Promote `migration_reproducibility_deep` to blocking | **owner**, after 1 | Carry the caveat: deep's volatile classifier absorbed a real tamper whose only surviving trace was a timestamp, so `TIMESTAMPS`-only results need a second look |
| 3 | Widen the blocking gate's `COUNT(*)` to all non-exempt tables | **owner**, after 1 | Closes every deletion in §2.2; cheaper than 2 and independent of it |
| 4 | ~~Give `reasoning_doc_citations` a Pydantic model~~ **DONE** — and it uncovered a second, quieter gap (§2.5) | none | Model written with full 34/34 parity and the table's compound CHECK mirrored; **plus** two `MODEL_TABLE_MAP` entries, because `jurisdictional_values` already had a model that was never mapped |
| 5 | Add a `CHECK` to `verification_status` | **owner (D-SCHEMA)** | *Not* "cheap, schema-only" as first drafted: CLAUDE.md §4 makes enum changes Change-Order gated, and `tooling-register` §4.1 names constraining this field "the wrong unilateral act" — four vocabularies coexisted, 81 out-of-enum rows, each with a ratification history. The reset makes the *migration* cheap; the *vocabulary ratification* is still owner-gated |
| 6 | Correct migration 053's header numbers (§1.5) | none | Via a follow-on header or DR — **not** by editing the committed migration |
| 7 | Give the vacuous three (E4, E6, E7) an `EXAMINED: <n>` line and fail-on-empty | none | Extends the existing convention; does not add a sweep |
| 8 | R3 locator constraint on code values | **owner**, deferred | Genuinely tractable. R13 is **not**: with zero admissions, drift costs nothing today, and hard-coding a population-of-study grading obligation before DR-2026-08-06 §3's class-relative correction lands risks re-freezing the academic default the DR repudiated — a T6 statutory code has no study population to grade |
| — | ~~Build a table ↔ model parity check~~ | — | **RETRACTED.** `validate_pydantic_schemas` exists (§2.3) |

**On "unenforced" as a verdict.** Not every unenforced rule is a defect. CLAUDE.md §2's
five-level spectrum promotes a rule "only when it's mechanically checkable **and drift is
costly**," and levels 2–3 (audit script, CI non-blocking) provide mechanical memory without
ossification. The first draft's framing — that these rules "survive only as long as every
future session remembers them" — was a false binary that skipped those levels.

---

## Part 5 — Correction log

What the 2026-08-09 adversarial review changed. Recorded because a document that quietly
absorbs its own corrections teaches the next session nothing.

| # | First draft said | Correction |
|---|---|---|
| C1 | "This repo detects wrong content, not absent content" — a unifying pattern | Misdiagnosis. Backwards for the DB layer; the register selftest instance is **vacuity**, not deletion-blindness. Replaced with scope-blindness (§2.4) |
| C2 | "Nothing checks table ↔ model parity" | **False.** `validate_pydantic_schemas` is registered and running. Third instance of an error class the register already documents |
| C3 | "§2.1 is the evidence the owner decision was waiting on" | False. Deep was created *because of* a tamper demo; the decision waits on the exemption list. Replaced with §3.1, which supplies it |
| C4 | Promoting deep is "the single highest-value fix" | Indefensible: `main` isn't branch-protected, so no promotion stops anything; and a cheaper fix (§3.3) dominates for deletions |
| C5 | "Twelve families are live in 109 rows" | Twelve cover **97**; ~24 families exist |
| C6 | R13 is "100%-observed practice" | Vacuous over 0 rows, and historically falsified (824/863 unadmitted) |
| C7 | The collision was "reproduced, not predicted" | Inflation. Zero live rows collide; the insert demonstrated SQLite semantics. Recommendation survives as future-proofing |
| C8 | "inserting §404.2.5 and §604-608 raised UNIQUE" | False as worded — those strings differ. The real test used post-unpack identity |
| C9 | The round-trip "is a verifier" | Detects **loss** only; blind to render-identical misassignment; its normalization escape hatch is unenforced (§1.2) |
| C10 | A dict "means copies, and copies drift" | False in Python; `REGISTER_MAP` is the repo's counterexample. Real argument is FK integrity (§1.1) |
| C11 | Fix "add a CHECK — cheap, schema-only" | Owner-gated D-SCHEMA; §4.1 names it "the wrong unilateral act" |
| C12 | "~17 multi-document rows" | 18, plus a 19th joined by `+` |
| C13 | "29 model modules" | 31 |
| C14 | "Largest unwatched tables: …" | Omitted `term_item_links` (147), the sixth-largest |
| C15 | E3 "no CHECK constraint" framed as unprotected | Constrained by Pydantic enum, argparse, and `db.py`; unconstrained **only in SQL** — which matters because migrations bypass all three |
| C16 | "Probes live at `scratchpad/probe.py`" | Not in the repo — session `/tmp`. And `probe_results.json` records only the 8 E-probes; each run overwrote it, so the D findings including §2.1 are attested by terminal output alone |
| C17 | Migration 053's header depth figures | Sum to 97 ≠ 109; "85" likely counts rows with *no* locator (§1.5) |

**Method note.** The review ran as three read-only passes with separate lenses (accuracy,
logic, methodology) so they could not converge on one blind spot. The methodology pass
terminated early on a model quota and was completed directly; C15 and C16 are its findings.
