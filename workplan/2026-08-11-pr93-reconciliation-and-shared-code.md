# 2026-08-11 — PR #93 reconciled with this session, and the shared-code question

**Status:** RECONCILIATION — nothing executed. PR #93 merged to `main` at 16:52 UTC today, after
this branch was cut. It is now merged in (`d09f923`, no conflicts). This document states what
#93 supersedes in my work, what my work adds to it, where we **disagree**, and answers the
owner's question about injectable shared code with measurement.
**Subject:** `d09f923` (my branch + `bc81070`). 133 executables (was 132 — #93 adds
`walk_harness.py`).

> **The most useful result is not a merge conflict, it is an agreement with a gap.** #93's
> **W5.4** says the 76-attestation corpus "has never been checked" for invalid rule identifiers.
> I ran that check (§1.4). And #93's **W5.1** predicts the mis-parse sweep is "systematic, not a
> one-off" without running it. I ran that too, and it is (§1.3).

---

## Part 1 — Where #93 and this session meet

### 1.1 What #93 supersedes in my work

**My reconciled register's Part 4 sequencing is superseded by `2026-08-12-resolution-plan.md`.**
Its six waves are better than my ten-step list: it separates the write path (W1) from the free
migrations (W3) from the adjudication apparatus (W4), gates W3/W4 on two named owner rulings, and
states a dependency graph. My register should point at it rather than compete. The overlap is
near-total on the items we share:

| My ID | #93 | Verdict |
|---|---|---|
| R-02 FK check after commit | **W1.1** | same finding; #93 adds the fix spec (move `foreign_key_check` above `commit()`) |
| R-03 "bootstrap" substring disables FK failure | **W1.2** | same; #93 adds the remedy (explicit `--allow-fk-violations` a human types) |
| R-04 failed migration wedges the queue | **W1.3** | same; #93 adds `--skip <id>` + "N not attempted" reporting |
| R-01/R-05 unguarded writers | W1 "also in this wave" | same |
| R-11 `deps:` never read · R-12 malformed YAML · R-13 `graph_audit:277` | W1 "also in this wave" | same |
| R-06 the 81 mm mis-parse | **W5.1** | same row; #93 additionally calls for the sweep |
| R-24 unregistered skills | **W5.4** | same; #93's fix is better (§1.4) |
| R-17 attestation checks are diff-scoped | **W6.4** | same |

### 1.2 What #93 has that I did not — five items I was missing

1. **W1.4 — `next_gap_id` returns `GAP-1` on the post-reset empty table**, and
   `schemas/evidence_state.py:167` requires `^GAP-\d{3,4}$`, so the only determination writer
   aborts on the first cell needing a gap. **The clean-room reset broke the determination
   writer.** I read this in the commit-91 review and failed to carry it into my register. It is
   also the subject of §2 below.
2. **A ratified marker scheme with zero repository presence.** The owner established on
   2026-08-12 that derived values carry a **triangle** — ▲ / ◭ / △ parallel to ● / ◐ / ○, shape
   for derivation, fill for evidence strength. No glyph in `governance/`, `schemas/`, `scripts/`,
   `decisions/` or `references/`; no column; no validator; no renderer. My documents describe the
   ●/◐/○ scheme as current and are now incomplete.
3. **W5.2** — E-12's six jurisdictional values are all *platform-lift* specifications under an
   item named *Entrance Landing and Manoeuvring Space for Power Wheelchair Users*. An owner
   scoping question sitting under the same rows as my R-06.
4. **W5.3** — `references/conflict-matrices/CORRIDOR-W.md` asserts **≥2440 mm** for DEAF signing
   pairs; E-08 asserts **≥1200 mm**. Four months, neither aware of the other. This lands squarely
   in my §1.1 frozen-corpus finding and I did not find it.
5. **D-A** — is value determination a machine stage or a human one? `assess_cell.py` writes
   `value_min`/`value_max`/`value_unit` as `None` unconditionally. Nothing in my work noticed
   that the pipeline determines a *state* and never a *number*.

### 1.3 What this session has that #93 does not

- **The frozen-corpus layer entirely** (my R-18 to R-20): three "frozen" registers intersecting
  in one entry; `global-reference-registry` declaring itself authoritative over the DB; 70 BPC
  banners naming a superseded event and 16 carrying none; 176 dangling REF-IDs. #93's W5.3 is one
  instance of this class, found independently and not generalised.
- **The volume analysis** (`2026-08-11-fold-or-cut-ledger.md`) — nothing in #93 asks what can be
  folded or cut.
- **The ID-namespace collision** — `C1`/`C4`/`D2` meaning three different findings across four
  documents. #93 adds a fifth and sixth document to that namespace (`W1.1`…, `D-A`/`D-B`), and to
  its credit the `W`-prefix does not collide with anything.
- **R-07 and R-08 — the sweep W5.1 asked for, run.** #93 says the extractor's failure "is
  systematic, not a one-off" and stops there. Running it: a second designation mis-parse at
  **B-10, `value_numeric = 54.0`, `unit = 'Hz'`, from the standard name "EN 54-23"**, on a row
  whose text states no rate — against sibling rows for the same parameter recording the **≤2 Hz
  photosensitive-epilepsy ceiling**. Plus class ordinals (`R9–R13` → `9.0`, `P3–P5` → `3.0`)
  stored as quantities with NULL unit. **W5.1's prediction is confirmed and has a
  safety-relevant member.**

### 1.4 W5.4's uncheckable check, checked

#93 states the defect precisely: `attestation_evidence` "fires only when an attestation names one,
which is the wrong end; it is also advisory *and* diff-scoped, so it merged in #92 and the
74-attestation corpus has never been checked for this."

**I ran `check_3_rule_resolution` over the whole corpus.** Result:

| | |
|---|---|
| attestations | **76** |
| failing CHECK 3 | **5** |
| distinct unknown identifiers | **9** — `forward-only-migrations`, `doctrine-token-on-synthesis-paths`, `decision-protocol`, `evidence-architecture`, `migration-discipline`, `retire-not-delete`, `tier-system`, `commit-msg-format`, `integrity-protocol` |
| valid id universe | 60 = 47 skill ids + 13 `EXTRA_RULE_IDS` |

**This corrects both of us in the same direction.** My R-24 framed it as two missing skills
affecting four attestations; #93's W5.4 framed it as "register both ids." Neither is the shape of
the problem: **only one of the nine unknown identifiers is a skill.** The other eight are
*governance rule* names — `retire-not-delete`, `commit-msg-format`, `forward-only-migrations` —
which are real operative rules that attestations reasonably cite and which the registry has no
place for. So W5.4's "register both ids" fixes one ninth of it.

The remedy is the one #93 already names and should be widened: a check that validates the **whole
corpus**, plus a decision about whether `rules_in_scope` may cite governance rules at all — and if
so, where their stable identifiers live. That is a schema question (`attestation.schema.json`
constrains the field), not a registry-entry question.

> **My own correction, recorded.** My first pass at this used a regex over the registry text and
> reported **14** unknown identifiers. It was wrong: it ignored `EXTRA_RULE_IDS`, the allowlist
> the real check consults. Running the actual function returned 9. Third time this session that
> a proxy measurement of mine inflated a finding — the same failure mode #93's Direction 2 records
> about itself ("a proxy failure, measuring tag citation and reading it as coverage").

### 1.5 Where we disagree — W3.2

#93's **W3.2** proposes: *"FK on `evidence_population_match.target_population` → `populations`.
0 rows."* My fold ledger's §2.1 retraction reached the opposite conclusion on the same column,
and the disagreement is substantive.

**Both of us are right about the live table and it does not settle the question.** The table is
empty, so the FK applies trivially today. But the **pre-reset** data shows how the column was
actually used: **22 of its 30 distinct values are prose, not codes** — *"Autistic students in
school built environments"*, *"DEAF/HoH adults relying on lipreading"*, *"Hardware operating force
threshold for UPL/PAIN populations including RA"*.

W3.2's own justification points the same way without noticing: it says the column "accepts
`WHEELCHAIR-USERS-GENERALLY` — the umbrella the work-from-axes rule prohibits." That is a *code*,
and a bad one. So the column has held both codes and prose, and the FK would forbid the prose.

**The unresolved question is what the column is for.** Its sibling is `study_population`, also
prose, and contract rule **R13** requires grading population-of-STUDY against population-SERVED —
a comparison that needs descriptive richness on both sides. An FK to `populations` makes the
served side a code and discards that.

**Recommendation, replacing both:** split it — `target_population_code` (FK'd, nullable) and
`target_population_note` (free text) — and hand-migrate the 64 archived rows, since no parser will
do it. This satisfies W3.2's aim (a real key, no umbrellas) without breaking R13's grading. It is
more work than either shortcut and it is the only version that survives the archived data.

---

## Part 2 — The shared-code question, measured

*Owner's question: how many scripts carry duplicates or variants of the same process, and how far
can injectable shared code enforce consistency?*

### 2.1 Copy-paste duplication is low. That is not where the problem is.

AST-normalised comparison of every function body ≥120 characters across all 133 executables:
**6 clusters of byte-identical functions, 6 redundant copies total** (`normalize_title_words`,
`_date_part`, `source_caveats`, `git`, `normalize`, `check`). Nothing systemic.

**The variance is in re-implementation, not duplication:**

| Process | Definitions | Distinct implementations |
|---|---|---|
| `main` | 79 files | — |
| `audit` | 22 files | — |
| `selftest` | 16 files | — |
| **DB connection** | 80 files open sqlite directly | **4 idioms**: 45 `uri+ro`+env · 42 plain+env · 34 plain+const · 5 `uri+ro`+const |
| **Repo-root resolution** | — | **4 idioms**: 46 `os.path.abspath(__file__)` · 32 nested `os.path.dirname` · 8 `Path(...).parents[N]` · 3 `Path(...).parent.parent` |
| **Verdict reporting** | — | **7 formats**: `EXAMINED:`(13) · `RESULTS: X/Y`(11) · `PASS: …`(5) · `OK/ERROR`(4) · `[PASS]/[FAIL]`(4) · `ALL PASS`(4) · `RESULT: PASS`(3) |

CLAUDE.md §7 already documents the last row as a live hazard — *"Read the exit code, not the
wording"* — which is a workaround for a problem one shared reporter would remove.

### 2.2 The injectable library already exists and has **zero** consumers

**`scripts/db.py` — 1,889 lines, 43 top-level functions** — is described by CLAUDE.md §4 as "the
read/query workhorse." It provides `connect()`, `now()`, `audit(session)`, `next_con_id()`,
`insert_connection()`, `next_gap_id()`, `insert_gap()`, `close_gap()`, `log_mining()`,
`log_search()`, `upsert_search_coverage()`, `next_term_id()` and thirty more.

| | |
|---|---|
| scripts that open sqlite directly | **80** |
| scripts that `import db` | **0** |
| scripts that shell out to `db.py` | **0** |

**Every one of the 80 rolls its own.** The library is not under-used; it is unused.

### 2.3 The proof that this costs correctness, not just tidiness

`scripts/db.py:149`:

```python
def next_gap_id() -> str:
    ...ORDER BY CAST(SUBSTR(gap_id,5) AS INTEGER) DESC LIMIT 1
    if not row: return "GAP-001"
    return f"GAP-{int(row['gap_id'].split('-')[1]) + 1:03d}"
```

`scripts/assess/assess_cell.py:426`:

```python
def next_gap_id(conn):
    rows = [...]
    mx = max(..., default=0)
    return f"GAP-{mx + 1}"        # -> "GAP-1" on an empty table
```

The schema requires `^GAP-\d{3,4}$`. **The library version zero-pads and satisfies it; the
re-implementation does not.** So **W1.4 — a Wave-1 write-path bug that breaks the only
determination writer — is a re-implementation of a function the repository already had
correct.** The resolution plan's fix is "zero-pad to three digits." The better fix is
`from db import next_gap_id`, and the finding underneath it is that nothing prevented the
re-implementation.

### 2.4 What to inject, and what not to

Not a framework, and not a rewrite of 80 scripts. Four narrow seams, each already proven by an
existing enforcer:

| Seam | What it replaces | Why it is safe |
|---|---|---|
| **`connect(readonly=True/False)`** | 4 connection idioms | `db_path_env_audit.py` already enforces the env-var half and gets **74%** compliance; the read-only check added 2026-08-06 gets **76%**. Both dimensions with an enforcer sit near 75%; both without one sit near 50%. The mechanism is proven. |
| **`repo_root()`** | 4 path idioms | pure, no I/O, mechanically substitutable |
| **`report(name, examined, failures)`** | 7 verdict formats | removes the hazard CLAUDE.md §7 documents; must emit `EXAMINED: <n>` so `run_checks.vacuity_failure()` can see a subject count — the convention that already exists |
| **id allocators** (`next_gap_id`, `next_con_id`, `next_term_id`) | the §2.3 class | these are where a variant becomes a schema violation rather than a style difference |

**The lever is not the library — it is the check.** A shared module with no enforcer reproduces
`db.py`: correct, comprehensive, and imported by nobody. Each seam ships **with** a registered
check that fails a new script rolling its own, and lands in the existing
`governance/check-registry.yaml` rather than a new register (guardrail 3).

**Sequencing:** id allocators first (§2.3 is a live bug), then `connect()`, then `report()`, then
`repo_root()` — descending by consequence, and each is independently abandonable.

**And the honest limit.** This is a single-author pre-launch repository; style consistency for
its own sake buys nothing. Three of the four seams above are worth doing only because they carry
an enforcer that closes a *correctness* gap: an unpadded id that violates the schema, a writable
handle where a read-only one was intended, a verdict that cannot be distinguished from a vacuous
pass. `repo_root()` is the one with no correctness argument, and it should be last or not at all.

---

## Part 3 — Disposition

1. My reconciled register (`2026-08-11-reconciled-findings-register.md`) gains R-28…R-32 for
   §1.2's five items, and its **Part 4 sequencing is retired in favour of the resolution plan's
   six waves.**
2. **W5.1 is confirmed and extended** — the sweep it asked for is run, with a safety-relevant
   member (§1.3).
3. **W5.4 is confirmed and widened** — 5 attestations, 9 identifiers, only one of them a skill
   (§1.4).
4. **W3.2 is contested** — the split, not the FK (§1.5).
5. The shared-code work (§2.4) is new and belongs in the resolution plan's Wave 1, because
   §2.3 is Wave 1.

*Every measurement re-derived on 2026-08-11 against `d09f923`. §1.4 corrects a proxy measurement
of my own that inflated 9 to 14; treat the rest with the same suspicion and re-derive.*
