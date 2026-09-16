# Adversarial pass — "retire in place, never hard-delete"

Target: the doctrine proposed in `scripts/migrations/076_never_reuse_identifiers.sql:38-45`
("The single rule that would make both unnecessary is `retire in place, never hard-delete`...").

**PREFATORY FINDING — the target has moved while this pass was running.** Commit `be85a94`
("governance: RETIRED tombstones are not live DOI claims; retire-in-place ruled
[2026-09-16 04:27]") is already in this branch's history and records:

> Owner ruling 2026-09-16 — **"retire in place then"**

`references/project-standards.md:3524-3578` is the ratified entry. The commit message states
outright: *"An adversarial pass on this proposal was already in flight when the ruling landed."*
So this is no longer a pass on an open proposal — it is a pass on an **owner-ratified doctrine**
whose implementation is partially built. CLAUDE.md rule 0 applies: the ruling wins over 076's
"named here and not smuggled in" framing, on contact, no edit needed to make that true. That
changes the shape of this report from "should this be adopted" to "does the ratified doctrine
survive scrutiny, and is it safe to rely on today."

---

## 1. Owner intent — would retire-in-place have satisfied the 2026-09-13 ruling?

**This is the strongest line, and the owner's own 2026-09-16 ruling text already concedes it**
(`references/project-standards.md`, the "AN EXECUTION CONDITION, NOT A RE-LITIGATION" paragraph):

> "the views (`v_best_practice` and the rest) may not filter on status, in which case
> retire-in-place would keep untrusted rows on the READING SURFACE — which would defeat the
> 2026-09-13 ruling's purpose rather than serve it."

I verified this against the live schema rather than taking the ruling's word for it:

```
python3 -c "
import sqlite3
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
for n,s in con.execute(\"select name,sql from sqlite_master where type='view'\"):
    print(n)
"
```

Of the views that read `specifications` or `evidence_sources` directly, **none filter on any
retirement/trust predicate**:

| View | Filters | Leaks a retired row? |
|---|---|---|
| `v_best_practice` | `state IN ('stated','provisional') AND code_floor_only=0` | No, **only if** 'retired' is added as a disjoint `state` value — see §5 |
| `v_pending` | `state='pending'` | No, same caveat |
| `v_code_floor_only` | `code_floor_only=1` only | **Yes** — no state filter at all |
| `v_divergence` | `ca.status='divergent'` only | **Yes** — no `ecs.state` filter at all (pre-existing gap, unrelated to this doctrine, but the same failure shape) |
| `v_source_reach_all` | none on `evidence_sources`/`specifications` state | **Yes** |
| `v_item_provenance` | none | **Yes** |
| `v_determination_provenance` | none | **Yes** |
| `v_evidence_authors` | none (reads `evidence_sources` directly) | **Yes** |
| `v_source_admission` | none | **Yes** |

(Full view SQL captured via `select name, sql from sqlite_master where type='view'` — 17 views
total; the 7 flagged "Yes" above have zero predicate touching any lifecycle/trust signal on the
tables in question.)

**Conclusion on intent:** if 229 untrusted circulation rows had been *retired* rather than
*deleted* on 2026-09-13, at least 7 named views — including `v_best_practice`, the view whose
name IS the render-facing claim of quality — would have continued to surface them exactly as
before, because none of the 22+ direct-query call sites (§3) or these 7 views drop a retired row.
**"Not able to be trusted... redo them all from the start" is a statement about reader-visible
trust, not merely identifier bookkeeping — and on the reader-visible axis, retire-in-place as it
stands today would have defied the ruling, not satisfied it.** The owner's 2026-09-16 ruling
recognizes exactly this and converts it into a precondition rather than ignoring it (see §7).
That is the correct response to the finding, but it means the precondition is currently unmet —
see §7 for the gap between "ruled" and "safe to use."

## 2. CLAUDE.md rule 5 — is a status column a second home for the fact?

**No, on the primary reading.** Rule 5 forbids the same *fact about a shared referent* being
written into two different tables ("point, do not copy" — e.g. an author name copied into
`evidence_sources` instead of reached via `evidence_source_authors`, which migration 063 fixed
per `scripts/migrations/076_never_reuse_identifiers.sql` view comments). A `status`/`state`
column recording a *row's own lifecycle* is intrinsic to that row, in its own table — it is the
single home the stage table (CLAUDE.md §3) already prescribes ("Each stage holds only its own
data"). `base_parameters.status` and `source_locators.status` are not copies of each other; they
are two tables each answering the same *kind* of question about themselves.

**But there is a real, narrower rule-5/rule-8 concern, evidenced in the schema itself.**
`evidence_sources` already carries **eight** independent status-shaped columns before any
retirement column is added:
`verification_status`, `verification_disposition` (OPEN/CLOSED), `verification_closure_reason`
(includes `'withdrawn'`), `data_capture_status`, `citation_mining_status`,
`processing_blocked_reason` (includes `'superseded'`), `metadata_integrity_status`,
`code_currency_status` — plus the nullable pointer `superseded_by_ref_id`
(`PRAGMA table_info(evidence_sources)`, columns 52-96 above). None of these is derived from any
other; nothing computes "is this row trustworthy" from the other eight. A **ninth** parallel
signal (a bare `retired` status, as opposed to reusing `verification_closure_reason='withdrawn'`
+ `verification_disposition='CLOSED'`, which already exist and are unused) is precisely the
"DERIVE IT, OR NAME WHO JUDGED IT" anti-pattern rule 8 names — a new field answering a question
an existing field combination could already answer, with no view deriving one from the other.
This is a real cost item, not a rule-5 violation in the letter, but a rule-8 violation in spirit
if the implementation adds a column instead of reusing/deriving from what is already there.

## 3. Query burden

Direct (non-view) reads/writes against the tables in question, by file (`grep -rn 'FROM
specifications\b\|UPDATE specifications\b' --include=*.py scripts/` etc.):

- `specifications`: **22** call sites across 12 files (`scripts/audit/register_integrity_check.py`,
  `adjudication_integrity.py`, `derivation_handshake_integrity.py`, `medical_lens_integrity.py`,
  `validate_verification_consistency.py`, `validate_evidence_state.py`,
  `scripts/assess/assess_cell.py`, `scripts/generate/pilot_renderings.py`,
  `scripts/generate/spec_page.py`, `scripts/db.py`, plus two test files).
- `evidence_sources`: **~24** files (`scripts/research/retrieval_log.py`,
  `emit_batch_sql.py`, `resolve_dois.py`, 8 `scripts/audit/*.py` modules,
  `validate_verification_consistency.py`, `emit_data_migration.py`, `audit_evidence_metadata.py`,
  `scripts/generate_parts.py`, `scripts/generate/pilot_renderings.py`, `scripts/db.py`, plus tests).
- `base_parameters`: **3** files.

**Existing status predicate discipline, measured:**
`grep -rn "status != 'retired'\|status <> 'retired'\|status = 'active'\|status IN ('active'"
--include=*.py scripts/` → **0 hits**. No reader in the tree today filters an active/retired
distinction on any of these three tables. `base_parameters.status` is checked in exactly one
place (`assess_cell.validate_parameter`, write-time only, refusing a *new* determination against
a merged/retired parameter — it does not stop an *existing* determination on a since-retired
parameter from continuing to join and render through `v_item_provenance`/`v_source_reach_all`,
both of which join `base_parameters` with no status filter).

**This is not hypothetical — it already happened once, in the mechanism this doctrine cites as
"already half-built."** `scripts/db.py:3011-3034` (the DOI duplicate-filing refusal, R9) had to
add `("source_locators", "AND COALESCE(status,'') <> 'RETIRED'")` as an exemption clause, and the
same missing exemption was independently present in `scripts/audit/research_batch_dod.py`'s R9a
and only fixed in the *same commit* (`be85a94`) that records the 2026-09-16 ruling — two call
sites, one bug, found because it blocked batch 08 from admitting a single re-run source. **The
failure mode this doctrine will multiply — a caller forgetting the new predicate — is not
speculative; it is the actual defect that forced the 2026-09-16 ruling to be recorded reactively
rather than designed proactively.** Scaling the same pattern across ~50 call sites and 7 views is
the same defect class, larger.

**Compare the two failure modes:** a forgotten `DELETE`-based clear (the old regime) fails loud —
`migration_reproducibility`'s row-count check goes red immediately, and no data can silently
reappear because it is gone. A forgotten status predicate under retire-in-place fails **silent**
— the row is still there, still joins, still counts toward `COUNT(*)` in whichever aggregate
view or audit forgot to exclude it, and nothing in `governance/check-registry.yaml` currently
tests for this (`grep -n "retire\|RETIRE" governance/check-registry.yaml` returns no check
enforcing reader-side status filtering — only vocabulary/prose mentions). Silent-wrong is a worse
failure mode than loud-wrong, and this doctrine trades one for the other without yet adding the
missing enforcement.

## 4. The empty-table trap (CLAUDE.md §4)

Retire-in-place **does not fix, and cannot fix retroactively**, the two live instances CLAUDE.md
names (`specifications.parameter_id NOT NULL → base_parameters` empty;
`item_taxonomy_links.item_code NOT NULL → items` empty) — those tables are already at 0 rows from
past hard deletes, and there is nothing to "un-delete" into a retired state. Migration 076's
`AUTOINCREMENT` seeding is the actual, orthogonal fix for the identity-reuse half of that damage;
retire-in-place is a *prevention* rule, not a repair mechanism, and the 076 migration is explicit
that both are needed together ("AUTOINCREMENT is compatible with it either way: belt and braces,
not a competing answer").

**Going forward, retire-in-place does prevent recurrence of exactly this trap**: a table that
never has all its rows deleted never returns to 0 rows (short of dropping the table itself, which
is a schema/code operation under CLAUDE.md §8, not a data operation this ruling governs). Had the
rule been in force before 2026-09-01/2026-09-13, `base_parameters`, `specifications` and `items`
would hold retired rows today instead of none, and the NOT-NULL-into-empty-table refusal would
never have fired. This is a genuine point in the doctrine's favor, not an objection.

## 5. Cost — concretely enumerated

Schema:
1. `specifications.state` CHECK has **no `retired` (or equivalent) value today**
   (`CHECK (state IN ('stated','provisional','pending','not_applicable'))`,
   `scripts/migrations/076_never_reuse_identifiers.sql:124-126`, unchanged as of `user_version=81`
   — confirmed live via `PRAGMA table_info(specifications)`). Contrary to the ruling's own framing
   that "the mechanism is already half-built," **the render-facing table has no mechanism at
   all** — the three examples the ruling names (`evidence_sources.superseded_by_ref_id`,
   `base_parameters.status`, `source_locators.status`) conspicuously do not include
   `specifications`, and that omission is not an oversight to paper over — it is the one table
   where the design work is still entirely undone.
2. `idx_spec_row_identity` (the UNIQUE index `assess_cell.py` relies on to refuse
   re-determination, `scripts/assess/assess_cell.py:1289-1334`) is a plain unique index, not
   partial. To let a retired cell's slot be re-determined it must become a partial index
   (`... WHERE state <> 'retired'`) — a schema migration, not a code change alone.
3. `evidence_sources` needs one designed, derived trust signal rather than a 9th independent
   status column (§2).

Writers:
4. `assess_cell.validate_cell_undetermined()` must move from "does any row exist for this cell"
   to "does a NOT-RETIRED row exist" — this is exactly the "SUPERSEDE DESIGN" the function's own
   docstring says is deliberately unbuilt ("there is no re-determination path... needs a SUPERSEDE
   DESIGN, which is an owner decision," lines 1307-1312). The 2026-09-16 ruling's ACTION item 3
   orders this rekeying but it has not been done — `grep -n "NOT RETIRED" scripts/assess/assess_cell.py`
   returns nothing.
5. Every writer that currently treats "row exists" as "slot taken" for these three tables needs
   the same re-audit already done once for `source_locators`/`evidence_sources` DOI-checking
   (§3) — `db.py`'s other existence refusals (`dbcore.exists`, `add-*` refusals) were not swept in
   the 2026-09-16 commit and should be assumed unswept until checked per-table.

Checks:
6. No registered check enforces the ruling's own ACTION item 2 ("sweep every reader that could
   surface a retired row... before the first retirement"). `governance/check-registry.yaml` has
   no `retire`/`RETIRE`-matching entry. `schema_reference_audit` (rule 4's enforcement) checks
   that a *name* resolves in the schema, not that a *query* excludes a lifecycle state — a
   different, currently nonexistent class of check.
7. `migration_reproducibility` (blocking) is COUNT-only (CLAUDE.md rule 3, and
   `governance/check-registry.yaml:229-236` states it in the check's own note: "An UPDATE changes
   no count, so value-level edits are invisible to it"). A retirement is an UPDATE. The one
   blocking gate that currently stops undocumented DB writes **cannot see a retirement at all** —
   protection for this exact operation now rests entirely on `migration_reproducibility_deep`,
   which is advisory. This is a genuine downgrade in gate coverage for the specific operation
   this doctrine makes routine, and it is the check-registry's own documented blind spot
   (line 253's note: "editing a row's tier and title... leave all seven invariants identical" —
   found by a prior adversarial trace, same failure shape as this one).

Views: 7 named in §1 need a new predicate once the trust signal exists.

## 6. Where hard delete is actually required

The doctrine is not exception-free — the owner's 2026-09-16 ruling itself carries ACTION item 4:
*"Where a row MUST genuinely leave (owner-ordered destruction, fabricated data), that is an
exception the owner rules on case by case, and it is recorded here."* Two real precedents already
exist, both predating and outside the ruling's prospective scope:

- **The 2026-09-01 retraction** (`recovered_from = 'retracted-2026-09-01-owner-ruling'`,
  6 rows visible in `source_locators` today, e.g. `REF-00965`-`REF-00970`): the corresponding
  `evidence_sources` rows were **hard-deleted**, not retired, per
  `scripts/migrations/data_20260902181820_2026-09-02-refid-highwater-repair.sql:20-25`, even
  though `evidence_sources` already had a working retire-in-place path available
  (`verification_disposition='CLOSED'`, `verification_closure_reason='withdrawn'`) that was not
  used. This is the sharpest evidence that the owner's actual practice for "this content must not
  be mistakable for live evidence" has been deletion, not flagging — and one of the deleted rows
  carried a real harm the flagged alternative would have risked perpetuating: a mangled,
  attribution-destroying author string ("andsensory E") on a Co-1 paper whose entire warrant is
  its community co-authorship (the migration's own note flags this: "AUTHOR STRING SUSPECT...a
  mangled parse of a community co-author").
- **The 2026-09-13 circulation clear itself** (229 rows) is the ruling's own subject and is
  explicitly not relitigated by the 2026-09-16 ruling ("does not reopen this ruling").

Both are real, evidenced cases where genuine removal — not retirement — was the owner's actual
choice, and the ruling's own text anticipates more will occur ("case by case"). The doctrine
survives this test because it names the exception rather than omitting it.

## 7. Verdict

**SURVIVES WITH CONDITIONS** — and the conditions are, almost verbatim, the ones the owner's own
2026-09-16 ruling already imposes, which this pass corroborates against the live schema rather
than merely repeating:

1. **The reader sweep (owner's ACTION item 2) is not done.** 7 views and ~50 direct call sites
   have zero retirement-aware predicate today; `specifications` has no vocabulary slot for
   "retired" at all. Until this sweep lands, no row should actually be retired-rather-than-deleted
   for `specifications`/`evidence_sources`, because doing so today would put an untrusted row back
   on the render surface with nothing filtering it — precisely the 2026-09-13 ruling's purpose,
   defeated.
2. **The supersede design (owner's ACTION item 3) is not done.** `assess_cell.py` still refuses
   re-determination on bare row-existence via a plain unique index, not `NOT RETIRED`; re-keying
   it requires a schema change (partial index) the ruling has not yet produced.
3. **Gate coverage should be named, not assumed.** Retirement operations are invisible to the one
   blocking data-integrity check (`migration_reproducibility`); if that gap is accepted, it should
   be stated in the check-registry note the way the count-only scope already is, not discovered
   again later as a surprise.

None of these is a reason to reverse the ruling — §4 and §6 show it is structurally sound and
already exception-aware, and §1's strongest objection was independently reached by the owner
before this report and turned into a precondition rather than argued away. The honest finding is
that **the doctrine is right and the implementation is roughly a third done** (the narrow
`source_locators`/DOI-check fix landed 2026-09-16; the view sweep and the supersede re-key have
not).
