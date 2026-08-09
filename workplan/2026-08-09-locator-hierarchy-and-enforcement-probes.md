# 2026-08-09 — Locator hierarchy: follow-on work, and an enforcement probe of the session's stipulations

**Status:** IN PROGRESS
**Predecessor:** `scripts/migrations/053_locator_hierarchy.sql` (schema 53, columns added, no row touched)
**Governing decision:** `decisions/DR-2026-08-06-clean-room-evidence-reset.md` §3 — adequacy of
identification and verification is **class-relative**

---

## Part 1 — Locator hierarchy: three findings, each demonstrated

Migration 053 added the levels `division > part > section > subsection > paragraph > clause >
subclause` (plus `_end` spans and `loc_note`) to `jurisdictional_values`,
`source_value_extractions` and `reasoning_doc_citations`. It deliberately touched no row.
Working the decomposition against real strings produced three findings that change what the
follow-on migration has to do.

### 1.1 The scheme registry must be a table, not a dict

`locator_scheme` is not a label. It is a pointer, and it answers three questions no row can
answer for itself:

| Job | Why the row cannot answer it | Live example |
|---|---|---|
| Which levels exist | Same depth, different name per family | ISO's top numbered level is a *clause*; ADA's is a *section*; NCC sits beneath a *volume* |
| How to render | Sigil and separator are family properties | `§404.2.5` · `clause 20` · `Art. R111-19-2` · `Vol 1 D3.3` |
| How to sort | String order is wrong by default | `§12.10` sorts before `§12.9` as text; correct as levels |

Demonstrated: as text, `['§12.10', '§12.2', '§12.9', '§9.1']`; cast per level,
`['§9.1', '§12.2', '§12.9', '§12.10']`.

The prototype held this as a Python dict. That is the wrong home — renderer, sorter and
validator would each need a copy, and copies drift. **One `locator_schemes` table**, keyed by
the same string `locator_scheme`, storing per family: the ordered level names, the sigil, the
separator, and the sort-cast rule. Then `locator_scheme` becomes a genuine FK and the twelve
document families live in the data are data, not code.

Twelve families are live in 109 rows: DIN 19 · AS/NZS 16 · ADA 15 · BS 15 · ISO 12 ·
Arrêté 5 · EN 4 · TEK17 4 · Building Regs 2 · ANSI 2 · NCC 2 · IPC 1.

### 1.2 The round-trip is a verifier, and it gates the splitting migration

Decompose → re-render → diff against the original string. The first hand-decomposition of eight
real citations scored **5/8**, and the three misses were the mechanism working:

- `ADA 2010 §404.2.5` — filled section+subsection, **silently dropped the paragraph `.5`**
- `BS 8300-2:2018 §8.2.1` — same, dropped `.1`
- `NCC Vol 1 D3.3` — identity edited (`NCC` → `NCC 2022`), a normalization, not a loss

Corrected to three levels where the document has three: **8/8 lossless.**

A regex split with no round-trip assertion would have written that loss into the DB and nothing
downstream would ever have known — the string it came from is the only witness, and the
migration overwrites it. **Requirement:** every row the splitting migration touches must satisfy
`rendered == original` **or** carry an explicit normalization note. Neither silently.

### 1.3 The re-key is required — the collision is reproduced, not predicted

`UNIQUE (item_code, jurisdiction, standard_name)` is unique today **only because
`standard_name` still carries the clause.** Inserting two genuine ADA citations —
`§404.2.5` and `§604-608` — against one item in one jurisdiction raised:

```
sqlite3.IntegrityError: UNIQUE constraint failed:
  jurisdictional_values.item_code, jurisdictional_values.jurisdiction,
  jurisdictional_values.standard_name
```

Migration 053's header predicted this. It is now demonstrated. The key must gain the locator
levels — **and the `ref_id` FK the table has never had** — in the same migration that unpacks
`standard_name`. Verified as of 053: zero such collisions exist in live data, so nothing is
broken by the wait.

### 1.4 Still owner-gated (unchanged from 053)

Splitting the ~17 genuine multi-document rows. Three of the 21 rows containing `/` are **false
positives** — `ANSI/ASA S12.60-2010`, `AS/NZS 1428.4.1:2009`, `AS/NZS 2107:2016` are single
standards jointly issued, and splitting them would invent a source. Of the rest, some are two
independent attestations of one requirement and some are one document citing another
(`IPC / ADA reference`). Those mean different things for code convergence and cannot be told
apart by a regex.

---

## Part 2 — Enforcement probe

Every stipulation this session identified for data management and evidence sourcing, tested
adversarially: **attempt what should be refused, and record whether it actually is.** A rule
that lives only in prose is a rule the next session breaks.

Three verdicts:

- **ENFORCED** — the attempt was mechanically refused
- **UNENFORCED** — the attempt succeeded; the rule is documentation only
- **VACUOUS** — a check exists and passed, but examined nothing

The vacuous verdict is separate because this repository has produced that failure mode
repeatedly, and it looks exactly like success.

Findings and the resulting fix list are recorded below as the probe runs.

### 2.1 The headline: a tampered committed migration silently rewrote 80 rows, and the blocking gate printed PASS

The decisive probe. Append one legal statement to the most recent committed data migration —

```sql
UPDATE slugs SET status = 'STUB' WHERE status = 'ACTIVE';
```

— and rebuild. All 80 ACTIVE slugs change status. Then:

| Gate | Level | Result |
|---|---|---|
| `migration_reproducibility` | **blocking** | **exit 0** — `PASS: the committed DB matches what the migration history produces.` |
| `migration_reproducibility --deep` | advisory | exit 1 — `slugs CONTENT 80 rows; status(80), created_at(1), updated_at(1)` |

**The mechanism that catches this exists, works, and is correct. It simply does not block.**
The blocking gate compares `PRAGMA user_version` plus `COUNT(*)` on six tables, and an UPDATE
changes neither — so it does not merely miss the tamper, it *affirms* the DB as reproducible.

This measures the owner-gated decision already pending in
`references/tooling-register.md` §4.2. It is no longer a design argument: promoting
`migration_reproducibility_deep` to blocking is the single highest-value fix on this list.

**Getting to the result took four attempts, and the three failures matter.** Tampering an
*early* migration was absorbed — later migrations re-created the rows, and deep saw only a
1-row `TIMESTAMPS` difference and passed. Tampering with `slug_id` failed on a nonexistent
column. Tampering with `status='TAMPERED'` was refused by a real CHECK constraint on
`slugs.status` — a genuine enforcement, found by accident. A probe that fails for the wrong
reason reads exactly like a rule being enforced.

### 2.2 Scope of the blind spot, measured

| | |
|---|---|
| tables | 66 total · **6 counted** · 2 exempt (DR-2026-05-28) |
| rows | 4,245 total · **93 counted — 2.2%** |
| largest unwatched | `term_aliases` 2,382 · `item_population_links` 372 · `data_migrations` 314 · `item_axis_links` 158 · `decisions` 157 · `jurisdictional_values` 109 · `slugs` 106 |

`DELETE FROM jurisdictional_values` — all 109 rows, the frame data the clean-room reset
deliberately preserved — passes the blocking gate with exit 0.

### 2.3 Verdicts

**ENFORCED — verified by attempting the refused thing**

| Probe | Stipulation | Evidence |
|---|---|---|
| E1 | VERIFIED without `--verification-method` refused (D-0157) | exit 1 |
| E2 | R9 — duplicate DOI refused | first insert 0, duplicate 1 |
| E5 | Frozen coverage grid refuses writes | exit 2, `search_coverage is FROZEN` |
| D7 | `GUIDEBOOK_DB_PATH` contract | 52/54 honour it, 2 documented exemptions |
| — | `slugs.status` CHECK constraint | refused `'TAMPERED'` |

**UNENFORCED — the attempt succeeded; the rule is documentation only**

| Probe | Stipulation | What happened |
|---|---|---|
| D1 | Direct UPDATE to a *counted* table caught | exit 0 — UPDATE does not change COUNT |
| D2 | Direct UPDATE to an uncounted table caught | exit 0 |
| D3 | Deleting an entire uncounted table caught | 109 → 0 rows, exit 0 |
| D6 | Committed data migrations are immutable | §2.1 |
| D5b | Migration 053's three tables have model parity | `reasoning_doc_citations` has 16 new locator columns and **no Pydantic model at all** |
| D5 | Table ↔ Pydantic parity is checked | nothing checks it; 29 model modules for 66 tables |
| E3 | `verification_status` constrained to VERIFIED/UNVERIFIED | **no CHECK constraint** — while `verification_disposition`, `verification_method` and `verification_closure_reason` all have one. The primary D-0157 field is the only unconstrained one of the four. |
| E7 | R13 — no admission without a population-match row | `add-source` exit 0 with none |
| E9 | R3 — no code value without a locator | INSERT with no locator succeeded. 109/109 carry `source_section` **by practice, not by constraint** |

**VACUOUS — a check exists and passed, but examined nothing**

| Probe | Stipulation | Subject count |
|---|---|---|
| E4 | T4–T6 walled off from ●/◐ (Option A) | `evidence_cell_state` = 0 |
| E6 | R8 — zero-yield searches cannot be deleted | `search_executions` = 0 |

These are the *expected* post-reset state, and DR-2026-08-06 §4.2 declares it. The obligation
is that they **say** `EXAMINED: 0` rather than print a pass — the failure mode this repository
has now produced four times.

### 2.4 Fix list, in priority order

1. **Promote `migration_reproducibility_deep` to blocking.** Owner-gated
   (`tooling-register.md` §4.2). §2.1 is the evidence the decision was waiting on. Caveat to
   carry into it: deep's volatile-column classifier absorbed a real tamper whose only surviving
   trace was a timestamp, so `TIMESTAMPS`-only differences need a second look before that
   classification is trusted to be benign.
2. **Add the `CHECK` constraint to `verification_status`.** Cheap, schema-only, and it closes
   the one unconstrained field of D-0157's four.
3. **Give `reasoning_doc_citations` a Pydantic model,** or record why it has none. Migration 053
   put 16 columns into a table that is mirrored nowhere.
4. **Build a table ↔ model parity check.** "Drift is a bug, not a convention" is currently
   enforced by nothing.
5. **Decide R3 and R13 at the constraint layer.** Both are 100%-observed practice with zero
   mechanical backing, so both survive only as long as every future session remembers them.
   R3 is the more tractable: a code value with no locator is refusable at insert.
6. **Make the vacuous pair declare their subject count** when their subjects repopulate.

### 2.5 The pattern behind the findings: this repo detects wrong content, not absent content

Three independent probes, three different layers, one shape:

| Layer | Probe | Corruption | Deletion |
|---|---|---|---|
| Database | D1–D3 | UPDATE a value — passes | DELETE all 109 rows — **passes** |
| Register documents | `register_integrity_check --selftest` | 11 of 12 mutations **FIRED** | "a whole cell section deleted" — **SILENT** |
| Check subjects | E4, E6, and the six vacuous gates found earlier | wrong subject fails | no subject **passes** |

Every one of these gates was built to answer "is this value right?" and each answers it well.
None was built to answer "is this still here?" — and absence is the cheaper failure to cause,
the harder one to notice, and the one that looks most like success.

This reframes the fix list. `migration_reproducibility_deep` at blocking (fix 1) closes the
database row; the `--selftest` miss is the same bug in the document layer and should be fixed
with it, not filed separately. The vacuity guards already built are the third instance,
retrofitted after the fact — which is why the `EXAMINED: <n>` convention exists and why it
should be the default for a new check rather than something added once a gate has embarrassed
itself.

**Method note.** Probes live at `scratchpad/probe.py` and never write to the canonical DB —
every one works on a copy. Whether any of this earns a place in the check registry is a
separate call: a probe suite is a diagnostic, and adding files is itself a drift risk.
