# F6 — CODE-FIX DESIGN (read-only remediation design)

**Commissioned 2026-08-25. This file is this pass's only write.** Every line number below was
re-measured against the working tree at HEAD (`6f9fcf4`, DB sha256 `6cceacd2…` — note: the DB
moved since F4's `30a10669…`; all counts here are re-derived at the current state, with the
deriving command shown where it matters). Where a brief-supplied line number disagreed with the
tree, the measured number is used and the discrepancy is noted.

**Conventions.** Each item: WHERE · NOW · CHANGE · REFUSALS/TESTS · BLAST RADIUS · RISK.
"check_declared" = `dbcore.check_declared(conn, table, column, value, context)` (schema-CHECK
vocabulary, rule 5's single home; no-op where no CHECK exists — which makes CLI changes safe to
land BEFORE their vocabulary migrations). New migrations are numbered from the measured
high-water mark: last schema migration is `064_…`, `PRAGMA user_version` = 64, so new schema
migrations are 065, 066, 067 below.

**Line-number corrections to the brief, measured:**
- `anchoring()` is used at `assess_cell.py:295-296`, not `:314`.
- `PILOT_CELLS` is `assess_cell.py:116-131`, not `:114-130`; argparse is `:488-492`.
- The valueless bind is `assess_cell.py:552-566` (the `None, None, None` is line 561); `:565-573`
  in the brief is the neighbouring column list.
- `update_bpc_metadata`'s INSERT branch is `db.py:1775-1783`, not `:1770-1778`.
- `room_page.py`'s six bad references: measured lines given in P3.1 (brief's `:26,29` was only
  the first).
- `validate_evidence_state.py:76-110`: **the NameError and the retired-status test are already
  fixed at HEAD** (fixed between commits `038913b` and `f087737`; verified by
  `git show 038913b:scripts/validate_evidence_state.py | sed -n '96,101p'` vs HEAD). What
  remains of P4.5 is narrower — see P4.5.
- `adjudication_integrity.py` exit code: **NOT REPRODUCIBLE at HEAD** — see P4.7b.

---

# PHASE 0 — SAFETY

## P0.1 — Wire `dbcore.is_canonical()` into `connect()`

**WHERE:** `scripts/dbcore.py:83-101` (`connect()`), supported by `:51-60` (`db_path()`),
`:63-75` (`is_canonical()`), selftest additions near `:438-441`.
The two sanctioned canonical-writer call sites that must keep working:
`scripts/migrate_db.py:366` (`run_migrations`) and `scripts/migrate_db.py:440`
(`rebuild_from_migrations`).

**NOW** (`dbcore.py:83, 96-100`):
```python
def connect(dry_run: bool = False, readonly: bool = False, path=None):
    ...
    target = Path(path) if path is not None else db_path()
    if readonly:
        conn = sqlite3.connect(f"file:{target}?mode=ro", uri=True, timeout=10)
    else:
        conn = sqlite3.connect(str(target), timeout=10)
```

**CHANGE** — signature gains `allow_canonical: bool = False`; the refusal goes between the
`target =` line and the branch:

```python
def connect(dry_run: bool = False, readonly: bool = False, path=None,
            allow_canonical: bool = False):
    ...
    target = Path(path) if path is not None else db_path()
    if not readonly and not allow_canonical and is_canonical(target):
        raise PermissionError(
            "REFUSING a read-write open of the canonical database "
            f"({target}). CLAUDE.md rule 3: migrations only, via "
            "scripts/migrate_db.py (which does not pass through this function). "
            "Copy first, then point GUIDEBOOK_DB_PATH at the copy:\n"
            "    cp data/guidebook.db \"$SCRATCH\"\n"
            "    GUIDEBOOK_DB_PATH=\"$SCRATCH\" python3 scripts/db.py ...\n"
            "--dry-run is refused too: a rehearsal proves the same thing on the "
            "scratch copy without taking a write lock on the committed blob. "
            "A caller that must open the canonical file read-write passes "
            "allow_canonical=True at its own call site, in code, where a "
            "reviewer can grep for it.")
    if readonly:
        ...
```

**The override is a keyword argument, not an env var — and both migrate_db call sites need no
change at all.** `migrate_db.py:366` and `:440` call `sqlite3.connect(...)` directly, never
`dbcore.connect()`, so the guard cannot reach them (verified:
`grep -n "connect" scripts/migrate_db.py` — raw calls only). Recommended comment-only change at
each of those two sites: `# raw sqlite3.connect, DELIBERATELY outside dbcore.connect()'s
canonical-write guard: this file IS the sanctioned canonical writer (CLAUDE.md rule 3); CI's
rebuild-and-compare polices it.` The `allow_canonical` kwarg exists for any future caller that
must write canonical through dbcore (none exists today: `grep -rn "allow_canonical" scripts/
tools/` after landing must show only dbcore itself).

**What breaks if the override is a bare env var** (e.g. `GUIDEBOOK_ALLOW_CANONICAL=1`):
1. **Ambient authority.** It authorizes every `connect()` in the process tree, not one call site
   — including opens the operator did not know a script makes. A kwarg is scoped to the line
   that carries it.
2. **It teaches the bypass.** The harness resets env between shells, so the incantation must be
   typed inline — `GUIDEBOOK_ALLOW_CANONICAL=1 python3 …` — which is exactly the copy-pasteable
   shape that `GUIDEBOOK_DB_PATH=data/guidebook.db` already proved migrates into skill files and
   outlives its context (P0.2 is the standing evidence). The guard would ship with its own
   defeat-device idiom.
3. **Unreviewable.** An env var authorization happens at run time and leaves no trace in the
   tree; `allow_canonical=True` is greppable and diff-reviewable, and CLAUDE.md §1's
   burden-of-proof can be applied to each occurrence.
4. **Sticky.** One `export` in a profile or CI job disables the guard for everything after it,
   silently, forever.

**REFUSALS/TESTS:**
- Selftest additions (`dbcore.py` `_selftest()`, after the existing `is_canonical` checks at
  `:438-441`):
```python
    # The guard itself: rw-canonical refuses (dry-run included); readonly passes.
    for kwargs in ({}, {"dry_run": True}):
        try:
            with connect(path=CANONICAL_DB, **kwargs):
                pass
            check("connect() refuses canonical rw open (%s)" % (kwargs or "plain"), False,
                  "no exception raised")
        except PermissionError:
            check("connect() refuses canonical rw open (%s)" % (kwargs or "plain"), True)
    with connect(readonly=True, path=CANONICAL_DB) as c:
        check("readonly canonical open still works",
              c.execute("SELECT 1").fetchone()[0] == 1)
```
  (The `allow_canonical=True` positive path is deliberately NOT selftested — a test that opens
  the committed blob read-write to prove it can is a mutation risk with no caller to protect.)
- Prove nothing else breaks: `python3 scripts/run_checks.py --all` on a clean tree. Note
  `run_checks.py:447-448` does `env.setdefault("GUIDEBOOK_DB_PATH", "data/guidebook.db")` — all
  registered checks are read-only audits (verified: no registry `cmd` invokes a `db.py` write
  subcommand), so none trips the guard.

**BLAST RADIUS:** Every `db.py` write or `--dry-run` invocation with GUIDEBOOK_DB_PATH unset or
pointed at canonical now refuses loudly — that is the point, and the two skills in P0.2 are the
known callers that break, so **P0.2 lands in the same commit**. `db.py migrate` is unaffected
(subprocess to migrate_db.py). `assess_cell.py` unaffected (own refusal + raw connect;
`db_path_env_audit.py` EXEMPT entry documents it). Gates that fire: none on a clean tree;
`dbcore --selftest` gains 3 assertions (its EXAMINED count is derived, not hardcoded — no edit
needed there).

**RISK:** Low. The one behavioural surprise is dry-run refusal on canonical; the message names
the remedy. Rollback is deleting the guard block.

## P0.2 — Four skill lines instruct the canonical path on write commands

**WHERE:** `skills/connection-auditor_SKILL.md:185,192,199` ·
`skills/connection-discovery_SKILL.md:219`. (The other `GUIDEBOOK_DB_PATH=data/guidebook.db`
occurrences in those two skills — auditor `:45,:48,:79,:113`, discovery `:94,:209,:253` — are
read-only commands (`connections`, `next-id`, python `mode=ro`) and stay as they are; P0.1
still permits readonly canonical opens.)

**NOW** (auditor:185, representative of all four):
```bash
GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/db.py update-connection \
  --con-id CON-XXXX --status PENDING --session [session-name]
```

**CHANGE — three parts, per skill.**
1. Once per skill, before the first write command, insert the scratch preamble:
```bash
# WRITES GO TO A SCRATCH COPY, NEVER data/guidebook.db (CLAUDE.md §0.3, §4).
SCRATCH="${SCRATCH:-$(mktemp -d)/guidebook-scratch.db}"
[ -f "$SCRATCH" ] || cp data/guidebook.db "$SCRATCH"
```
2. The four write lines become (auditor:185 shown; :192 `--status CLOSED`, :199 `add-gap`, and
   discovery:219 `add-connection` identically re-prefixed):
```bash
GUIDEBOOK_DB_PATH="$SCRATCH" python3 scripts/db.py update-connection \
  --con-id CON-XXXX --status PENDING --session [session-name]
```
3. Once per skill, after the last write step, append the capture step (without it the scratch
   writes die with the container):
```bash
# Ship the delta as a migration (THE write path, CLAUDE.md §4):
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH" --out /tmp/batch.sql
python3 scripts/emit_data_migration.py --input /tmp/batch.sql --session [session-name]
python3 scripts/migrate_db.py
```
   (Verify emit_batch_sql's exact flag names with `python3 scripts/research/emit_batch_sql.py
   --help` before writing the skill text — this pass did not execute it.)

**REFUSALS/TESTS:** After P0.1, the OLD text fails mechanically (PermissionError), so the skills
cannot silently regress — the guard is the test. Grep-proof the sweep:
`grep -rn 'GUIDEBOOK_DB_PATH=data/guidebook.db' skills/ | grep -Ev "connections|next-id|mode=ro"`
must return nothing.

**BLAST RADIUS — a pre-existing capture gap this exposes:** `dbcore.WRITABLE_TABLES`
(`dbcore.py:353-386`) does **not** include `connections` or `connection_targets`, so
`emit_batch_sql.py` cannot capture the very writes these two skills make on scratch. Add both
names to `WRITABLE_TABLES` in the same commit (the constant's own comment — "a table cannot
again be writable by one and unknown to the other" — is the authority; this is that defect,
live). Both tables have ordinary PKs (`con_id`; composite `(con_id,target)`), same shapes the
diff already handles via `source_slug_links`.

**RISK:** Minimal; text + one constant. The one real risk is skill text drifting from
emit_batch_sql's actual flags — hence the `--help` verification instruction.

---

# PHASE 1 — THE FORWARD WALK

## P1.1 (+P1.11) — `add-source` cannot make an honest admission

**WHERE:** `scripts/db.py` — parser `:1055-1125` (esp. `--evidence-type` `:1085`,
`--verification-method` `:1100-1104`), dispatch `:1508-1560`, `insert_evidence_source`
`:1863-2026` (whitelist `_ES_COLS` `:1892-1915`, ref-id refusal `:1933-1950`, VERIFIED branch
`:1960-1976`, one-table R9 dedup `:1985-2000`, author write `:2007-2025`).
`scripts/tests/test_db_integrity.py:346-352` (I4) and `:312-318` (I1) are the gates being
reconciled. New migration: `scripts/migrations/065_evidence_type_and_tier_checks.sql`.

### (a) `--scope`

NOW: no `--scope` anywhere in db.py (`grep -- '--scope' scripts/db.py` → only log-search's
`--target-scope`); `scope` absent from `_ES_COLS`; yet `evidence_sources.scope` carries a live
CHECK `('high_control','lower_control','national','international','intrinsic')` and
`schemas/tier_derivation.py` needs it to derive a tier for `clinical` and `standard_eb` — the
bulk of any mobility batch. Every such admission is born failing `adjudication_integrity.py`
(S2 case 32/PART 5; the 2026-08-22 hand-repair migration
`data_20260822012400_…biblio-repair.sql` is the standing precedent).

CHANGE:
- Parser (after `:1085`): `p_as.add_argument("--scope", help="Evidence scope — the set is the "
  "column's own CHECK; required to derive a tier for clinical/standard_eb "
  "(schemas/tier_derivation.py).")`
- `_ES_COLS`: add `"scope"`.
- Dispatch: `if args.scope: data["scope"] = args.scope`.
- In `insert_evidence_source`, inside the `with connect(...)` block, before the INSERT:
```python
        if data.get("scope") is not None:
            dbcore.check_declared(conn, "evidence_sources", "scope",
                                  data["scope"], "add-source")
        # Tier must be DERIVABLE, not merely in range. Refuse at write time what
        # adjudication_integrity.py can only report after the fact.
        et = data.get("evidence_type")
        if et is not None:
            import importlib.util as _iu
            _root = str(Path(__file__).resolve().parents[1])
            if _root not in sys.path:
                sys.path.insert(0, _root)
            from schemas.tier_derivation import check_tier_consistency
            if not check_tier_consistency(et, data.get("scope"), data.get("tier")):
                raise ValueError(
                    f"(evidence_type={et!r}, scope={data.get('scope')!r}) does not "
                    f"derive stored tier {data.get('tier')!r} under the ratified "
                    f"(type x scope) -> tier ladder (schemas/tier_derivation.py). "
                    f"clinical/standard_eb REQUIRE --scope. Nothing was written.")
```
  (Verify `check_tier_consistency`'s exact signature/None-handling with
  `python3 -c "import sys; sys.path.insert(0,'.'); from schemas.tier_derivation import
  check_tier_consistency; help(check_tier_consistency)"` — assess_cell.py:203 calls it as
  `check_tier_consistency(evidence_type, scope, tier)`, which is the shape used here.)

### (b) VERIFIED never sets `verification_disposition='CLOSED'` (blocking I1)

NOW (`db.py:1961-1973`): the VERIFIED branch sets method/attempt refusals only; only the
UNVERIFIED branch (`:1975`) defaults a disposition. I1
(`test_db_integrity.py:312-318`) fails ANY `VERIFIED` row whose disposition is not `CLOSED`.

CHANGE — inside `if vs == "VERIFIED":`, after the verified_by_tool refusal (`:1972`):
```python
        if data.get("verification_disposition") not in (None, "CLOSED"):
            raise ValueError(
                f"VERIFIED with disposition {data['verification_disposition']!r} "
                f"contradicts blocking I1: VERIFIED means the verification effort "
                f"is finished, which is exactly what CLOSED records. One of the "
                f"two is wrong; nothing was written.")
        data.setdefault("verification_disposition", "CLOSED")
```
This is a state-machine consequence, not an invented fact — symmetrical with the existing
UNVERIFIED→OPEN default at `:1975`, and unlike the condemned `method='tool'` default it asserts
nothing about how verification happened.

### (c) `--evidence-type` vocabulary — CHECK migration FIRST, then `check_declared`

NOW: `evidence_sources.evidence_type` is bare TEXT, **no CHECK** (read the DDL); the CLI accepts
anything (`'empirical'` landed in S2 case 30/31). The list at `db.py:1223` belongs to
`add-supersession-check` and must NOT be copied (rule 5 — A-4 item 2). The vocabulary's ratified
single home in-schema already exists twice for OTHER columns:
`search_executions.target_evidence_type` CHECK and `supersession_check.anchor_evidence_type`'s
comment — both exactly `('clinical','sr_meta','standard_eb','national_fw','code','co1','co2',
'grey')`, matching `schemas/tier_derivation.py`'s ratified ladder.

CHANGE — **migration 065** (schema; SQLite cannot ADD a CHECK, so this is the documented
12-step table recreate; `evidence_sources` holds 10 rows, all in-vocab — verified:
`clinical×6, co1×3, sr_meta×1`; tiers 1,2,3 only):
```sql
-- 065_evidence_type_and_tier_checks.sql
-- AFTER_DATA: 20260825215123
--   (applies after the newest committed data migration on rebuild, so every
--    historical replay INSERTs into the pre-CHECK table; verify with
--    `python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db` before commit)
PRAGMA user_version = 65;
BEGIN TRANSACTION;
CREATE TABLE evidence_sources_new (
  -- EXACT copy of `SELECT sql FROM sqlite_master WHERE name='evidence_sources'`
  -- with two edits:
  --   evidence_type TEXT CHECK (evidence_type IS NULL OR evidence_type IN
  --     ('clinical','sr_meta','standard_eb','national_fw','code','co1','co2','grey')),
  --   tier INTEGER CHECK (tier IS NULL OR tier BETWEEN 1 AND 6),
  ...
);
INSERT INTO evidence_sources_new SELECT * FROM evidence_sources;
DROP TABLE evidence_sources;
ALTER TABLE evidence_sources_new RENAME TO evidence_sources;
CREATE INDEX idx_evidence_sources_standing
  ON evidence_sources(verification_status, verification_disposition);
COMMIT;
```
Implementation notes an implementer must not skip: (1) the full column list is pasted from the
live `sqlite_master` sql, not retyped; (2) the one index above is the ONLY index/trigger on the
table (measured — recreate it, nothing else); (3) child tables FK `evidence_sources(ref_id)` by
name, so the rename preserves them — run the rebuild + `PRAGMA foreign_key_check` to prove it;
(4) mirror the CHECKs in `schemas/evidence_source.py` (it already types via `schemas.enums`;
confirm `EvidenceType` members equal the 8 — `validate_pydantic_schemas --strict` is the gate).

CLI half (can land before or after 065 — `check_declared` no-ops until the CHECK exists), in
`insert_evidence_source` inside the connect block:
```python
        if data.get("evidence_type") is not None:
            dbcore.check_declared(conn, "evidence_sources", "evidence_type",
                                  data["evidence_type"], "add-source")
        if data.get("tier") is not None:
            dbcore.check_declared(conn, "evidence_sources", "tier",
                                  str(data["tier"]), "add-source")
```
(`check_values` parses `IN (...)` lists only; the `tier BETWEEN` form will not match — either
extend `dbcore.check_values` to parse BETWEEN, or rely on (a)'s `check_tier_consistency` refusal
for tier, which is stronger anyway. Recommended: the latter; drop the tier check_declared line.)

### (d) R9 dedup is one-table (`:1985-2000`); `add-locator` is the two-table model

NOW (`db.py:1992-2000`): DOI dedup queries `evidence_sources` only, with case-sensitive `=`.

CHANGE — replace the block with the `insert_locator` pattern (`db.py:2514-2529`):
```python
        doi = dbcore.norm_doi(data.get("doi"))
        if doi:
            data = dict(data, doi=doi)
            for table, hint in (
                    ("evidence_sources",
                     "R9: cross-file the existing ref_id rather than duplicating; "
                     "link that ref_id to your slug instead."),
                    ("source_locators",
                     "R9/runbook step 5: this DOI is already a LEAD in the clue "
                     "store — admit it UNDER THE STASH ref_id (reuse it as "
                     "--ref-id), never mint a second identity for one source.")):
                hit = conn.execute(
                    'SELECT ref_id FROM "%s" WHERE LOWER(TRIM(doi))=? '
                    'AND ref_id<>?' % table, (doi, data["ref_id"])).fetchone()
                if hit:
                    raise ValueError(
                        f"DOI {doi!r} is already held as {hit[0]} in {table}. "
                        f"{hint} Nothing was written.")
```
(The `superseded_by_ref_id` exclusion from the old query moves into the evidence_sources arm:
append `AND COALESCE(superseded_by_ref_id,'') = ''` to that table's WHERE.) Note the
source_locators arm deliberately allows `ref_id == hit` — admitting under the stash id is the
sanctioned promotion (runbook step 5), and `source_locators.status` flips to `'PROMOTED'` via a
follow-up `update-locator`… which does not exist (`insert_locator`'s own error text names it).
Smallest honest addition: `db.py update-locator --ref-id REF-NNNNN --status PROMOTED --session S`
(whitelist: `status`, `notes`; check_declared on status; refuse absent ref_id). Without it the
stash's `PROMOTED` state is unreachable and P2.1's promotions can never be marked consumed.

### (e) P1.11 — `--verification-method` choices vs blocking I4

NOW (`db.py:1100-1102`): `choices=["tool", "corroborated-not-retrieved", "co1-attestation",
"citing-bibliography"]`. The schema CHECK on `evidence_sources.verification_method` declares
FIVE values — those four plus **`direct-render`**. Blocking I4
(`test_db_integrity.py:346-352`) rejects any VERIFIED row whose method is not in
`('direct-render','co1-attestation','tool')`. So the CLI offers two methods that I4 rejects for
VERIFIED rows and omits the one I4 most naturally accepts. (`corroborated-not-retrieved` and
`citing-bibliography` are legitimate — for UNVERIFIED rows, recording how existence was
corroborated; the CLI must keep them for that path.)

CHANGE:
1. Parser `:1100-1104`: **delete the `choices=` list** (a hardcoded copy of a schema vocabulary,
   already drifted — the rule-5 shape); help text becomes: `"How the standing was established. "
   "The value set is evidence_sources.verification_method's own CHECK. For VERIFIED rows only "
   "an artefact-obtaining method is lawful (I4): direct-render / co1-attestation / tool."`
2. Single home for the I4 subset — add to `dbcore.py` (near `REF_ID_SHAPE`):
```python
# D-0157 / blocking invariant I4: the methods that OBTAIN the artefact and can
# therefore carry a VERIFIED standing. corroborated-not-retrieved and
# citing-bibliography attest existence only and cap at UNVERIFIED.
# ONE home; scripts/tests/test_db_integrity.py imports this set for I4.
I4_ARTEFACT_METHODS = frozenset({"direct-render", "co1-attestation", "tool"})
```
3. `insert_evidence_source`, in the VERIFIED branch (replacing the stale method list in the
   refusal text at `:1963-1968` too):
```python
        dbcore.check_declared(conn, "evidence_sources", "verification_method",
                              data["verification_method"], "add-source")   # in connect block
        if data["verification_method"] not in dbcore.I4_ARTEFACT_METHODS:  # in VERIFIED branch
            raise ValueError(
                f"verification_method {data['verification_method']!r} never obtained "
                f"the document, so it cannot carry VERIFIED (blocking I4). Artefact-"
                f"obtaining methods: {sorted(dbcore.I4_ARTEFACT_METHODS)}. File as "
                f"UNVERIFIED (disposition OPEN) with this method instead.")
```
   (Ordering note: `check_declared` needs `conn`, the I4 refusal does not; keep the I4 refusal
   in the pre-connect VERIFIED branch at `:1961-1976` and the check_declared with the other
   vocab checks inside the connect block.)
4. `test_db_integrity.py:349-351`: replace the literal `('direct-render','co1-attestation',
   'tool')` with the imported set (`sys.path` gains `scripts/`, as `db.py:48` does):
   `_I4 = ",".join(f"'{m}'" for m in sorted(dbcore.I4_ARTEFACT_METHODS))` interpolated into the
   query. This is the caller sweep for the new constant, done at birth.

### (f) Two small honesty fixes in the same function
- `:1944-1947` refusal text says *"mint above the source_locators high-water mark"* — the exact
  rule CLAUDE.md §4 now calls WRONG. Replace with: *"There is no allocator to guess at: mint
  with dbcore.next_ref_id(conn) — the union high-water mark over every ref-id home."*
- `add-source --dry-run` with `--slug` crashes (S2 case 4): dispatch `:1557-1559` calls
  `insert_source_slug_link` in a SECOND transaction after the first rolled back → FK failure
  (and in non-dry-run, a source can land with its link lost if the second call fails). CHANGE:
  `insert_evidence_source` gains `slug=None, local_ref_id=None` params; when given, the
  source_slug_links INSERT happens inside the SAME `with connect(dry_run)` block (move the body
  of `insert_source_slug_link` in; keep the old function delegating for other callers). Dispatch
  becomes one call.

### (g) Co-1 flags (the P4.5 write half, filed here because it is this parser)
`co1_provenance`, `co1_source_type`, `synthesis_attribution_required` are ALREADY in `_ES_COLS`
(`:1902-1903`) with no argparse flags — the CLI cannot file an honest Co-1 source. Add:
`--co1-provenance`, `--co1-source-type`, `--synthesis-attribution-required {0,1}`; dispatch
pass-throughs; refusals in `insert_evidence_source`:
```python
        if data.get("evidence_type") == "co1":
            if not data.get("co1_provenance"):
                raise ValueError(
                    "evidence_type=co1 requires --co1-provenance. Co-1's warrant is "
                    "co-production (CLAUDE.md §6): who produced this knowledge is part "
                    "of the evidence, not metadata.")
            if data.get("tier") not in (None, 1):
                raise ValueError("Co-1 is tier 1 by definition (co-primary, T-03); "
                                 f"got tier={data.get('tier')!r}.")
            if data.get("co1_source_type"):
                from schemas.enums import Co1SourceType
                try:
                    Co1SourceType(data["co1_source_type"])
                except ValueError:
                    raise ValueError(
                        f"co1_source_type {data['co1_source_type']!r} not in "
                        f"schemas.enums.Co1SourceType: "
                        f"{sorted(m.value for m in Co1SourceType)}")
```

**REFUSALS/TESTS (whole of P1.1):** on a scratch copy —
1. VERIFIED + `--verification-method tool --verified-by-tool crossref` → row lands with
   `verification_disposition='CLOSED'`; `test_db_integrity.py` I1/I2/I4/I4b all PASS.
2. VERIFIED + `corroborated-not-retrieved` → refused naming I4. UNVERIFIED + the same → lands
   OPEN.
3. VERIFIED + explicit `--verification-disposition OPEN`… (no such flag exists — the python API
   path) → refused naming I1.
4. `--scope wrong` → refused naming the CHECK set. `--evidence-type empirical` → refused (after
   065) naming the 8. `clinical` with no `--scope` → refused by the tier-derivability rule.
5. DOI present in `source_locators` under REF-00123 → refused telling you to admit under
   REF-00123.
6. `--dry-run --slug X --local-ref-id L-1` → exit 0, nothing written.
7. `--evidence-type co1` without `--co1-provenance` → refused.
8. `python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db` green after 065;
   `PRAGMA foreign_key_check` empty.

**BLAST RADIUS:** callers of `add-source` — DR-2026-08-19 runbook step 7 (its example already
passes `tool`; its prose lists the stale four-method set at `:855` — swept in P4.4);
`skills/` mentioning add-source (`grep -rln "add-source" skills/` and sweep choice lists);
`insert_source_slug_link`'s external callers (grep — dispatch only); `test_db_integrity.py`
edited in-place (I4 import). Gates: `validate_pydantic_schemas --strict` (schema mirror),
`migration_reproducibility` (065), `adjudication_integrity` (now un-failable via this CLI).

**RISK:** the 065 table recreate is the one genuinely risky change in Phase 1 — mitigated by
10-row size, AFTER_DATA ordering, rebuild + foreign_key_check as acceptance. Everything else is
additive refusals.


## P1.2 (+P1.10) — `db.py add-extraction`: the writer for `source_value_extractions`

**WHERE:** new subcommand in `scripts/db.py` (parser beside `add-locator` at `:899`; insert
function beside `insert_locator` at `:2496`); `dbcore.WRITABLE_TABLES` (`dbcore.py:353-386`);
companion subcommand `add-external-root`. The view contract being satisfied, read from
`sqlite_master`:

```sql
CREATE VIEW v_value_independence AS
    SELECT COALESCE(parameter_canonical, parameter) AS parameter,
           population_code,
           COUNT(DISTINCT COALESCE(root_ref_id, root_id)) AS independent_root_count
    FROM source_value_extractions
    WHERE root_type IN ('measurement_primary', 'participatory_finding',
                        'derived_calculation')
      AND (root_ref_id IS NOT NULL
           OR root_id IN (SELECT root_id FROM external_root_registry))
    GROUP BY COALESCE(parameter_canonical, parameter), population_code
```

**So the view counts a row ONLY when (1) `root_type` is one of the three independent kinds AND
(2) `root_ref_id` is set OR `root_id` is registered in `external_root_registry`.** A writer that
omits `root_type`/`root_ref_id`/`root_id` (the plan's original P1.2) leaves the view at 0 by
construction — P1.10 is therefore load-bearing, not optional.

**Schema facts the writer must honor** (from the table's DDL): NOT NULL: `ref_id`, `slug`
(FK slugs), `parameter`, `claim_type` (CHECK: numerical/range/qualitative/framework/absent),
`extraction_method` (CHECK: skim/full-read/re-read/auto-mined), `extraction_status`
(DEFAULT 'preliminary'; CHECK: preliminary/reviewed/verified/contradicted/absent-confirmed),
`created_at`, `updated_at`, `contested` (DEFAULT 0). FKs: `ref_id`→evidence_sources,
`population_code`→populations, `promoted_to_rdc_id`→reasoning_doc_citations,
`root_ref_id`→evidence_sources, `item_code`→items. CHECKs on `root_type` (5 values incl.
`committee_assertion`, `untraced`), `measurement_paradigm` (9), `device_class` (9). Table CHECK:
`claim_type='absent' ⇔ claimed_value IS NULL`. Locator columns: `locator_scheme`,
`loc_division…loc_subclause` (+`_end` variants), `loc_note`, plus `source_section` and
`file_anchor`.

**CHANGE — parser:**
```python
    p_ax = sub.add_parser("add-extraction",
                          help="Record one value/claim extracted from an admitted source "
                               "(source_value_extractions; feeds v_value_independence)")
    p_ax.add_argument("--ref-id", required=True)
    p_ax.add_argument("--slug", required=True)
    p_ax.add_argument("--item-code", required=True,
                      help="items FK. Nullable in the schema, but v_item_extractions and the "
                           "judgment stage join on it; an extraction not tied to an item is "
                           "unreachable downstream, so this CLI requires it.")
    p_ax.add_argument("--parameter", required=True)
    p_ax.add_argument("--parameter-canonical")
    p_ax.add_argument("--population", help="populations FK (population_code)")
    p_ax.add_argument("--jurisdiction")
    p_ax.add_argument("--claim-type", required=True)
    p_ax.add_argument("--claimed-value")
    p_ax.add_argument("--claimed-unit")
    p_ax.add_argument("--claim-text")
    p_ax.add_argument("--extraction-method", required=True)
    p_ax.add_argument("--extraction-status", default="preliminary")
    p_ax.add_argument("--root-type", required=True,
                      help="Where the value ultimately comes from. 'untraced' is the honest "
                           "unknown; only measurement_primary/participatory_finding/"
                           "derived_calculation count as independent roots (v_value_independence).")
    p_ax.add_argument("--root-ref-id", help="evidence_sources FK — the root, when it is an "
                                            "admitted source (often the source itself)")
    p_ax.add_argument("--root-id", help="external_root_registry FK — the root, when it is NOT "
                                        "an admitted source (dataset, campaign, standard body)")
    p_ax.add_argument("--root-population-note")
    p_ax.add_argument("--measurement-paradigm")
    p_ax.add_argument("--device-class")
    p_ax.add_argument("--setting")
    p_ax.add_argument("--contested", type=int, choices=[0, 1], default=0)
    p_ax.add_argument("--echo-of", help="extraction_id this row merely repeats (citation echo)")
    p_ax.add_argument("--source-section")
    p_ax.add_argument("--file-anchor")
    p_ax.add_argument("--locator-scheme")
    for _loc in ("division", "part", "section", "subsection", "paragraph",
                 "clause", "subclause"):
        p_ax.add_argument(f"--loc-{_loc}")
        p_ax.add_argument(f"--loc-{_loc}-end")
    p_ax.add_argument("--loc-note")
    p_ax.add_argument("--notes")
    p_ax.add_argument("--session", required=True)
    p_ax.add_argument("--dry-run", action="store_true")
```

**CHANGE — `insert_extraction(data, session, dry_run=False)`** (the refusal set, in order):
```python
_INDEPENDENT_ROOTS = ("measurement_primary", "participatory_finding",
                      "derived_calculation")   # mirror of the view's WHERE — see note below

def insert_extraction(data: dict, session: str, dry_run: bool = False) -> int:
    _COLS = frozenset({...every flag's column...})
    dbcore.validate_cols(data.keys(), _COLS, "insert_extraction")
    with dbcore.connect(dry_run) as conn:
        ref = dbcore.fold_ref(data.get("ref_id"))
        if not dbcore.exists(conn, "evidence_sources", "ref_id", ref):
            raise ValueError(f"ref_id {data.get('ref_id')!r} is not an admitted source. "
                             f"Extraction happens AFTER admission (add-source first); a "
                             f"value from a source that does not exist is a claim about "
                             f"nothing — the 2026-08-19 shape.")
        data["ref_id"] = ref
        for tbl, col, key in (("slugs", "slug", "slug"), ("items", "item_code", "item_code"),
                              ("populations", "population_code", "population_code")):
            v = data.get(key)
            if key != "population_code" or v is not None:
                if not dbcore.exists(conn, tbl, col, v):
                    raise ValueError(f"{key} {v!r} is not in `{tbl}`.")
        for col in ("claim_type", "extraction_method", "extraction_status",
                    "root_type", "measurement_paradigm", "device_class"):
            if data.get(col) is not None:
                dbcore.check_declared(conn, "source_value_extractions", col,
                                      data[col], "add-extraction")
        # The table CHECK, refused by NAME rather than left to SQLite:
        if data["claim_type"] == "absent" and data.get("claimed_value") is not None:
            raise ValueError("claim_type=absent asserts the source does NOT state a value; "
                             "--claimed-value contradicts that. One of the two is wrong.")
        if data["claim_type"] != "absent" and data.get("claimed_value") is None:
            raise ValueError(f"claim_type={data['claim_type']} requires --claimed-value "
                             f"(the schema's own pairing CHECK).")
        # A number needs its unit; a quantified claim needs its locator (R3).
        if data["claim_type"] in ("numerical", "range"):
            if not data.get("claimed_unit"):
                raise ValueError("numerical/range claims require --claimed-unit. A number "
                                 "without a unit is not a value.")
            loc_keys = [k for k in data if k.startswith("loc_")] + \
                       ["source_section", "file_anchor"]
            has_loc = any((data.get(k) or "").strip() for k in loc_keys
                          if isinstance(data.get(k), str))
            if not has_loc and "[UNVERIFIED-QUANT]" not in (data.get("notes") or ""):
                raise ValueError(
                    "R3: a quantified extraction needs a locator (loc-* / "
                    "--source-section / --file-anchor) or an explicit "
                    "[UNVERIFIED-QUANT] marker in --notes. A value without a locator "
                    "is the thing this table exists to prevent. Nothing was written.")
        # P1.10 — the independence contract. Without this, the row lands and
        # v_value_independence still reads 0.
        rt = data["root_type"]
        rref, rid = data.get("root_ref_id"), data.get("root_id")
        if rref and rid:
            raise ValueError("give --root-ref-id OR --root-id, not both — one root, one home.")
        if rref:
            rref = dbcore.fold_ref(rref)
            if not dbcore.exists(conn, "evidence_sources", "ref_id", rref):
                raise ValueError(f"root_ref_id {data.get('root_ref_id')!r} is not an "
                                 f"admitted source.")
            data["root_ref_id"] = rref
        if rid and not dbcore.exists(conn, "external_root_registry", "root_id", rid):
            raise ValueError(
                f"root_id {rid!r} is not registered. Register the external root first: "
                f"db.py add-external-root --root-id {rid} --description '...' "
                f"--root-type {rt} --session <S>. An unregistered root does not count "
                f"toward v_value_independence (its own WHERE clause).")
        if rt in _INDEPENDENT_ROOTS and not (rref or rid):
            raise ValueError(
                f"root_type={rt} claims an independent root but names none. Give "
                f"--root-ref-id (an admitted source) or --root-id (registered external "
                f"root) — or file the honest 'committee_assertion'/'untraced'. Without a "
                f"named root the row can never count as independent "
                f"(v_value_independence WHERE clause).")
        if data.get("echo_of") is not None and not dbcore.exists(
                conn, "source_value_extractions", "extraction_id", data["echo_of"]):
            raise ValueError(f"echo_of {data['echo_of']!r} is not a live extraction_id.")
        row = dict(data)
        row.update(dbcore.stamp_for(conn, "source_value_extractions", session))
        cols = ",".join(row)
        cur = conn.execute(
            f"INSERT INTO source_value_extractions ({cols}) "
            f"VALUES ({','.join('?' * len(row))})", list(row.values()))
        return cur.lastrowid
```
NOTE on `_INDEPENDENT_ROOTS`: this is a copy of the view's WHERE list — a rule-5 tension. The
schema cannot be the home here (a view WHERE clause is not readable by `check_values`). Put the
tuple in `dbcore` beside `I4_ARTEFACT_METHODS` with a comment naming `v_value_independence` as
the thing it mirrors, and add a selftest assertion that parses the view's SQL from
`sqlite_master` and compares — the same trick `check_values` uses, one regex:
`re.search(r"root_type IN \(([^)]*)\)", view_sql)`. That makes drift self-detecting.

**`external_root_registry` writer — build it** (why: the view's `root_id` arm is dead code
without it; 0 rows, no writer anywhere — measured; it is ~20 lines and the alternative is
hand SQL for exactly the class of provenance row that must never be hand-invented):
```python
    p_xr = sub.add_parser("add-external-root",
                          help="Register a value root that is not itself an admitted source "
                               "(dataset, measurement campaign, standards-body archive)")
    p_xr.add_argument("--root-id", required=True)
    p_xr.add_argument("--description", required=True)
    p_xr.add_argument("--root-type", required=True)
    p_xr.add_argument("--provenance")
    p_xr.add_argument("--root-population-note")
    p_xr.add_argument("--notes")
    p_xr.add_argument("--session", required=True)
    p_xr.add_argument("--dry-run", action="store_true")
```
Refusals: duplicate `root_id` (named, not INSERT OR IGNORE); `check_declared` on `root_type`;
non-empty description. Stamp via `stamp_for` (table carries created_at/created_by_session only).

**REFUSALS/TESTS:** on scratch — numerical claim without unit → refused; without locator →
refused naming R3; `root_type measurement_primary` with no root → refused naming the view;
`--root-id X` unregistered → refused pointing at add-external-root; after one good extraction:
`SELECT * FROM v_value_independence` returns 1 row with `independent_root_count`=1 — **this is
the P1.2 acceptance, the view moving off zero**; `v_item_extractions` returns the row joined to
its item.

**BLAST RADIUS:** `dbcore.WRITABLE_TABLES` += `"source_value_extractions"`,
`"external_root_registry"` (else emit_batch_sql silently DROPS these rows between scratch and
migration — the exact 8-locator-row failure the constant's comment records). PK for both is
simple (`extraction_id` AUTOINCREMENT / `root_id` TEXT) — the generic diff handles them. Docs
that say "no writer exists" (pipeline map/context map prose) go stale in the true direction.
`assess_cell.py:196-202`'s comment ("no assessment RULE for grading a value dimension") remains
true — P1.2 populates the substrate; the grading rule stays absent (see P1.8's boundary).

**RISK:** low; append-only new code. The one design judgment is requiring `--item-code` where
the schema allows NULL — recorded above with its reason; loosen to optional if a real non-item
extraction ever appears (that is a one-word change).

## P1.3 + P1.9 — the judgment writer and the blocking battery: RECOMMENDATION

**Every condition `validate_evidence_state.py` enforces on a `specifications` row**, enumerated
from `validate_cell_states_db` (`:216-302`) and `validate_convergence_db` (`:305-343`):

Cell rules:
1. `design_scale` ∈ {universal, population, person} when non-NULL (`:246-247`).
2. `pending` ⇒ `gap_register_id` present AND in `gaps` (`:249-253`).
3. `provisional` ⇒ confidence flag complete: `confidence_synthesis_basis` non-empty AND
   `confidence_dimensions_present` AND `confidence_dimensions_absent` non-empty JSON arrays
   (`:254-257`).
4. `provisional` ⇒ `convergence_id` NOT NULL (`:258-259`).
5. `not_applicable` ⇒ `not_applicable_rationale` (`:260-262`).
6. `stated` ⇒ `convergence_id` NOT NULL (`:263-265`).
7. `stated` ⇒ `code_floor_only`=0 (`:266-268`).
8. `stated` ⇒ `regulatory_stratum_only`=0 and `tier_basis` not ending
   `"(regulatory_stratum_only)"` (`:269-271`).
9. `stated`/`provisional` ⇒ `governing_refs` a non-empty well-formed JSON array (`:275-279`,
   anti-hallucination gate).
10. `stated` + single_axis convergence + clinical-only + all cited tiers = 3 ⇒ violation
    (T3-alone cap, `:282-301`).

Convergence rules: divergent ⇒ rationale + synthesis_approach; single_axis ⇒ rationale, ≤1
axis; convergent ⇒ ≥2 axes; discounted ∩ anchoring = ∅; five JSON columns well-formed.

**Recommendation: (b), sharpened — `assess_cell.py` is the sole sanctioned writer for
`stated` / `provisional` / `pending`, and P1.3's general `add-specification` is DROPPED.**
Reasons:
- A CLI that takes `--state stated` as an *argument* is an assertion channel: the operator
  asserts the determination instead of deriving it. To refuse dishonest input it would have to
  re-verify conditions 3, 4, 6-10 against the evidence — i.e. re-implement `determine()` — at
  which point it IS assess_cell with a worse provenance story. A green path that must be
  hand-asserted is the 2026-08-19 shape (F4's own closing warning).
- `assess_cell.py` already writes `convergence_assessment` + `specifications` + `gaps` in one
  act (`:525-575`) and pydantic-gates every row before insert (`:530`), satisfying conditions
  1-4, 6, 9, 10 by construction (7-8 by its G1 branch). There is **no CLI writer for
  `convergence_assessment` and none is needed** under this recommendation — the convergence row
  is derived, never asserted.
- What the recommendation must ALSO deliver (or the walk still fails):
  1. **assess_cell writes `specification_source_links`** — today NOTHING does, so every cell
     renders sourceless (spec_page's join `:98-105` finds nothing). After the specifications
     INSERT (`:552-566`), same transaction and same emitted SQL:
```python
        for _r in det["governing_refs"]:
            lvals = (specification_id, _r, "governing", STAMP, SESSION)
            conn.execute(
                "INSERT INTO specification_source_links (specification_id, ref_id, "
                "role, created_at, created_by_session) VALUES (?,?,?,?,?)", lvals)
            sql_lines.append(
                "INSERT INTO specification_source_links (specification_id, ref_id, role, "
                "created_at, created_by_session) VALUES (" +
                ", ".join(q(v) for v in lvals) + ");")
```
     `governing_refs` (JSON) + the junction is a dual home; written in one transaction from one
     in-memory list it cannot drift at write time. Guard the read path with a parity assertion
     added to `test_db_integrity.py` (K-series, beside K01): for every specifications row, the
     junction's ref set equals the JSON set. That is an amendment to an existing registered
     check, not a new registry entry. The true rule-5 end state — retire the JSON column and
     re-point its readers (`validate_evidence_state:275`, K01's payload, `register_integrity_
     check:144,382`) at the junction — is real debt; record it, do not attempt it inside this
     walk (three readers + a sha-shape change).
  2. **A narrow `db.py add-specification` restricted to `--state not_applicable`** — the one
     state `determine()` cannot derive (a human judgment that the parameter has no design
     implication for this population; condition 5 is its whole gate). Parser: `--item`,
     `--population`, `--rationale` (required), `--session`, `--dry-run`; the `--state` flag is
     refused for any other value with a message pointing at assess_cell. Refusals: FKs; UNIQUE
     (item, population) collision named; rationale non-empty. This closes the state machine
     without opening the assertion channel.
- **`add-spec-source-link` is NOT added.** With assess_cell writing links atomically, a second
  independent link writer is exactly the drift generator the parity check would then be blamed
  for surviving. Nothing needs it; §1's "nothing is added without naming what reads it" refuses
  it.

**TESTS:** run the (repaired) assess_cell on scratch for one anchored cell; then
`python3 scripts/validate_evidence_state.py --db $SCRATCH` → `OK cell-state machine` with 0
errors; `test_db_integrity.py` K01 + new link parity PASS; `spec_page.py` shows the sources.
Then break it on purpose: hand-delete one junction row on scratch → parity check fires.

**BLAST RADIUS:** `pipeline-contract.yaml` criteria naming a specifications writer (none name a
CLI — verified `check: null` entries only); WALK-REPAIR-PLAN's P1.3 text (superseded by this
recommendation); `WRITABLE_TABLES` += `"specifications"`, `"specification_source_links"`,
`"convergence_assessment"` — assess_cell emits its own SQL artifact, but the migration path for
its output runs through `emit_batch_sql` when driven from a scratch DB, and capture blindness
is the known failure. **RISK:** the dual-home JSON/junction decision is the contestable one —
recorded above with the parity guard and the consolidation debt named.

## P1.4 — `assess_cell.py`: de-pilot

**WHERE:** `scripts/assess/assess_cell.py:116-131` (`PILOT_CELLS`), `:488-495` (argparse +
canonical refusal), `:428-431` (its own `next_gap_id`), `:508-509` (hardcoded id bases),
`:496` (`conn = sqlite3.connect(args.db)`).

**The two live-data crashes, measured (S3 entries 3-4, reproduced against the committed DB):**
1. **Gap-id shape.** `next_gap_id()` (`:428-431`) returns `f"GAP-{mx + 1}"` → `"GAP-1"` (live
   gaps are all `GAP-B0N-NNN`, so the flat-numeric max is 0), and the script's own pydantic
   gate (`schemas/evidence_state.py:167`: `^GAP-\d{3,4}$`) rejects it. Crash on cell 1.
2. **Population code.** `PILOT_CELLS` entry 7 (`:129`) names `NEU`, absent from the live
   `populations` table (23 codes; renamed to `BRAIN`) → `validate_population` raises on cell 7.

**CHANGE:**
1. Argparse (`:488-492`) becomes:
```python
    ap.add_argument("--db", required=True, help="scratch DB (NEVER data/guidebook.db)")
    ap.add_argument("--emit-sql", required=True)
    ap.add_argument("--report-json", default=None)
    ap.add_argument("--item", required=True, help="items.item_code, e.g. E-12")
    ap.add_argument("--population", required=True, help="populations.population_code")
    ap.add_argument("--slug", default=None,
                    help="evidence slug. Default: derived from item_bpc_links where the item "
                         "has EXACTLY ONE link; refused with the candidate list otherwise.")
    ap.add_argument("--note", default="")
    ap.add_argument("--value-from-extraction", default=None,
                    help="comma-separated source_value_extractions.extraction_id list the "
                         "value tuple is derived from (P1.8); ids must belong to this item "
                         "and to governing sources")
```
   The canonical refusal at `:493-495` stays exactly as is (it is the reason
   `db_path_env_audit.py`'s EXEMPT entry for this file exists — do not "fix" it to read the env
   var).
2. Delete `PILOT_CELLS` (git is the archive; the emitted artifacts under `working/pilot/`
   remain the historical record). The main loop iterates the single
   `(args.item, args.population, slug, args.note)`.
3. Slug derivation:
```python
    if args.slug:
        slug = args.slug
    else:
        links = [r[0] for r in conn.execute(
            "SELECT slug FROM item_bpc_links WHERE item_code=?", (args.item,))]
        if len(links) != 1:
            legacy = conn.execute("SELECT bpc_source_slug FROM items WHERE item_code=?",
                                  (args.item,)).fetchone()
            sys.exit(f"REFUSING: cannot derive a slug for {args.item} "
                     f"(item_bpc_links has {len(links)}: {links}; legacy "
                     f"bpc_source_slug={legacy and legacy[0]!r}). Pass --slug explicitly.")
        slug = links[0]
```
4. Item existence refusal (currently only the population is validated):
   `if not conn.execute("SELECT 1 FROM items WHERE item_code=?", (args.item,)).fetchone():
   sys.exit(f"item {args.item!r} not in items")`.
5. Ids from the target DB instead of `CELL_ID_BASE` (`:508-509`): two runs against one scratch
   currently both mint 9001 and collide.
```python
    conv_id = conn.execute(
        "SELECT COALESCE(MAX(convergence_id), 0) FROM convergence_assessment").fetchone()[0]
    specification_id = conn.execute(
        "SELECT COALESCE(MAX(specification_id), 0) FROM specifications").fetchone()[0]
```
   Determinism note in the docstring updates: ids are a function of DB state, which the
   emitted-SQL replay caveat (`:501-507`) already handles for gap ids — extend that caveat's
   wording to name all three id families.
6. Gap-id fix — consolidate to ONE allocator. Add to `dbcore.py` (beside `next_ref_id`):
```python
def next_gap_id(conn) -> str:
    """Next flat-numeric gap id, zero-padded (GAP-NNN / GAP-NNNN).
    Scans EVERY gap_id; batch-scoped ids (GAP-B01-001) are recognised and
    skipped, never collided with. schemas/evidence_state.py:167 accepts only
    the flat shape for gap_register_id, so this is the shape cells may cite."""
    mx = 0
    for (g,) in conn.execute("SELECT gap_id FROM gaps"):
        m = re.fullmatch(r"GAP-(\d{3,4})", (g or "").strip())
        if m:
            mx = max(mx, int(m.group(1)))
    return "GAP-%03d" % (mx + 1) if mx < 999 else "GAP-%04d" % (mx + 1)
```
   `assess_cell.py:428-431` and `db.py:135-144` both delegate to it (P4.3 is the db.py half;
   note assess_cell already imports nothing from scripts/ — add
   `sys.path.insert(0, os.path.join(REPO_ROOT, "scripts")); import dbcore`).
7. Crash 2 disappears with `PILOT_CELLS`; `validate_population`'s refusal already reports a bad
   code cleanly for CLI input.

**REFUSALS/TESTS:** `--item E-03 --population MOB` on scratch with zero linked evidence →
`pending` cell + `GAP-001` (padded) + PASS through its own pydantic gate; run twice → distinct
ids, no collision; `--item X-99` → refused; `--population NEU` → refused naming the live table.
Determinism: same DB, same cell, two runs → byte-identical emitted SQL except ids (which are
state-derived — assert equality after replaying run 1).

**BLAST RADIUS:** `working/pilot/PILOT-MANIFEST.md` documents the 7-cell shape (prose, frozen);
`db_path_env_audit.py` EXEMPT entry unchanged; K01 unchanged (sha payload untouched here);
`register_integrity_check.py`'s ghost-row selftest unaffected. **RISK:** low; the only judgment
call is refusing ambiguous slug derivation rather than guessing — deliberate.

## P1.5 — `NOT_ASSESSED` and anchoring: conditions 1 and 3 ONLY

**WHERE:** `scripts/assess/assess_cell.py:248-250` (`anchoring()`), `:295-296` (its call sites
— brief said `:314`; measured 295-296), `:209` / `:421-422` / `:582`
(`needs_population_assessment` computed/aggregated/emitted). `schemas/directness.py:225-234`
(`consolidate()`) — **NO CHANGE THERE**, see below.

**Doctrinal basis, verified at `governance/evidence-methodology.md:129-132`:** "for the target
population" appears in condition 1 (T1 clinical) and condition 3 (Co-1) and NOT in 2 (T2
synthesis, "addressing the parameter") or 4 (Co-2 CPG, "addresses the design parameter"). A
population dimension that was never assessed cannot warrant the clause those two conditions
carry; T2/Co-2 anchor on parameter relevance by design and must not be demoted (C-5's
correction trail).

**NOW** (`:248-250` and `:295-296`):
```python
def anchoring(recs):
    """A source anchors only if its conditioning permits (§1.7): never NON-ANCHORING/DISCOUNTED."""
    return [r for r in recs if r["conditioning"] not in (COND_NON_ANCHORING, COND_DISCOUNTED)]
...
    anchors = anchoring(b["t1"]) + anchoring(b["co1"]) + anchoring(b["t2"]) + anchoring(b["co2"])
    t3c = anchoring(b["t3c"])
```

**CHANGE:**
```python
def anchoring(recs, require_population_assessment=False):
    """A source anchors only if its conditioning permits (§1.7): never
    NON-ANCHORING/DISCOUNTED. §2.2 conditions 1 (T1 clinical) and 3 (Co-1)
    additionally require the parameter addressed "for the target population"
    (evidence-methodology.md:129,131): a population dimension that was never
    assessed (NOT_ASSESSED) cannot warrant that clause, so it disqualifies
    anchoring for those two strata ONLY. Conditions 2 (T2) and 4 (Co-2) anchor
    on parameter relevance (:130,:132) and are not filtered — a blanket ban
    would wrongly demote them (C-5)."""
    out = [r for r in recs if r["conditioning"] not in (COND_NON_ANCHORING, COND_DISCOUNTED)]
    if require_population_assessment:
        out = [r for r in out if r["population_directness"] != NOT_ASSESSED]
    return out
...
    anchors = (anchoring(b["t1"], require_population_assessment=True)
               + anchoring(b["co1"], require_population_assessment=True)
               + anchoring(b["t2"]) + anchoring(b["co2"]))
    t3c = anchoring(b["t3c"])
```
`t3c` is deliberately unfiltered: T3's path to `provisional` is the tier3-threshold DR's
"direct parameter relevance", not the target-population clause. `PARTIAL`/`PROXY` still anchor
everywhere: they WERE assessed; down-weighting (via `consolidate()`) is their correct cost.

**`directness.py:225-234` — no change, and the reason recorded:** `consolidate()` already does
the right thing with `NOT_ASSESSED` (an unknown grade fails `pop_full` → `COND_DOWN_WEIGHTED`),
and the module docstring's additive rule ("every deviation … is engine-side and tagged
rule_version", pre-ratification) forbids moving the pilot's G2 semantics into the ratified
schema module. The change is engine-side, where G2 lives.

**Wire `needs_population_assessment` (the flag half of G2 — cap AND flag):** the aggregate at
`:421-422` finally gets a consumer in `main()`'s report loop (`:623-626`), plus the one output
that makes the flag actionable — say what the cap COST:
```python
    for r in report:
        print(f"{r['item_code']}×{r['population']:<5} ...")           # existing line
        if r["needs_population_assessment"]:
            print(f"    NEEDS POPULATION ASSESSMENT (G2 flag): "
                  f"{', '.join(r['needs_population_assessment'])} — grade with "
                  f"`db.py add-population-match` and re-run; an unassessed T1/Co-1 "
                  f"source cannot anchor `stated` (§2.2 conds 1,3).")
```
And in `determine()`, when the T1/Co-1 filter removed would-be anchors, record it so the report
can say "this cell would be stated if the match were graded": compute
`withheld = [r["ref_id"] for r in anchoring(b["t1"]) + anchoring(b["co1"])
if r["population_directness"] == NOT_ASSESSED]` and carry it into the report dict as
`anchors_withheld_pending_assessment`. (Pure addition; no schema column — it is session-facing
guidance, not a determination fact.)

**TESTS:** fixture on scratch: one T1 clinical VERIFIED source linked to the slug, NO
`evidence_population_match` row → cell must NOT be `stated`; report prints the flag and the
withheld ref. Add the match (`EXACT`) → re-run → `stated`. One T2 sr_meta source, no match row
→ `stated` (condition 2 unfiltered) — this is the regression test that the ban did not
generalise. **BLAST RADIUS:** none outside assess_cell (the flag was read by nothing — that was
the defect). **RISK:** doctrine-reading risk was retired by C-5/F1 (the text settles it);
flagged in the content section anyway for the owner's awareness, execution not gated.

## P1.6 — `update-bpc --population`

**WHERE:** `scripts/db.py:60-67` (`_BPC_META_COLS`, already whitelists `population`),
`:1039-1052` (parser — no `--population`), `:1421-1443` (dispatch), `:1759-1783`
(`update_bpc_metadata`; INSERT branch `:1775-1783` hits `bpc_metadata.population TEXT NOT NULL`
— brief said `:1770-1778`; measured 1775-1783). `bpc_metadata` = 0 rows, so the FIRST synthesis
write for any slug takes the INSERT branch and raises an uncaught `IntegrityError`.

**CHANGE:**
- Parser (after `:1041`): `p_ubpc.add_argument("--population",
  help="populations.population_code this BPC synthesises for. REQUIRED on the first write "
       "for a slug (bpc_metadata.population is NOT NULL).")`
- Dispatch (in the `data` assembly at `:1422-1437`): `if args.population is not None:
  data["population"] = args.population`.
- `update_bpc_metadata` INSERT branch — refuse by name instead of crashing:
```python
        else:
            if not data.get("population"):
                raise ValueError(
                    f"first bpc_metadata write for slug {slug!r} must carry "
                    f"--population (column is NOT NULL). Nothing was written.")
            row = {"slug": slug, **data, **audit(session)}
            ...
```
- Population vocabulary refusal (pointer discipline — free text here would be the umbrella
  problem D-18 documents): before the INSERT/UPDATE, inside the connect block:
```python
        if "population" in data and not conn.execute(
                "SELECT 1 FROM populations WHERE population_code=?",
                (data["population"],)).fetchone():
            raise ValueError(f"population {data['population']!r} is not a "
                             f"populations.population_code.")
```
**TESTS:** first `update-bpc --slug mobility-built-environment --evidence-state DRAFT
--session S` without `--population` → named refusal (not IntegrityError); with
`--population MOB` → row lands; second call without it → UPDATE branch, fine; bad code → vocab
refusal. **BLAST RADIUS:** skills/runbooks documenting update-bpc (`grep -rln "update-bpc"
skills/ decisions/` — sweep the examples to carry `--population` on first-write flows).
**RISK:** whether `population` should instead reference an umbrella-free key is D-18/owner
territory; this fix only makes the existing column reachable and FK-honest.

## P1.7 — `spec_page.py` renders no value at all

**WHERE:** `scripts/generate/spec_page.py:73-88` (cell query + dict), `:200-209` (`cell_rows`),
`:230-236` (table header). Verified: `grep -c value scripts/generate/spec_page.py` → 0.

**NOW** (`:73-88`):
```python
    cells = conn.execute(
        "SELECT specification_id, population_code, state, tier_basis, code_floor_only, "
        "falsification_condition, regulatory_stratum_only, confidence_synthesis_basis, "
        "has_unverified_sources, all_sources_disqualified "
        "FROM specifications WHERE item_code = ? ORDER BY population_code",
        (item_code,),
    ).fetchall()
    item["cells"] = [
        {"specification_id": r[0], "population_code": r[1], ...}
        for r in cells
    ]
```

**CHANGE — query** (add the three value columns + `design_scale`, which the page also never
shows though the state machine keys on it):
```python
    cells = conn.execute(
        "SELECT specification_id, population_code, state, tier_basis, code_floor_only, "
        "falsification_condition, regulatory_stratum_only, confidence_synthesis_basis, "
        "has_unverified_sources, all_sources_disqualified, "
        "value_min, value_max, value_unit, design_scale "
        "FROM specifications WHERE item_code = ? ORDER BY population_code",
        (item_code,),
    ).fetchall()
```
…and the dict gains `"value_min": r[10], "value_max": r[11], "value_unit": r[12],
"design_scale": r[13]`.

**CHANGE — value formatting** (one function, so the rule is stated once):
```python
def value_cell(c):
    """The evidence-anchored range (doctrine #1), rendered honestly.

    NULL handling is load-bearing: a `stated` cell without a value is a claim
    whose central fact is missing — say so, never render a bare dash that reads
    as 'not applicable'."""
    lo, hi, unit = c["value_min"], c["value_max"], c["value_unit"]
    if lo is None and hi is None:
        if c["state"] in ("stated", "provisional"):
            return ('<span class="warn">no value recorded</span>')
        return '<span class="empty">—</span>'
    u = f' {escape(unit)}' if unit else ' <span class="warn">[unit not recorded]</span>'
    def n(x):  # 1500.0 -> "1500", 1.25 -> "1.25"
        return escape(f"{x:g}")
    if lo is not None and hi is not None:
        return (f'{n(lo)}{u}' if lo == hi else f'{n(lo)}–{n(hi)}{u}')
    if lo is not None:
        return f'≥ {n(lo)}{u}'
    return f'≤ {n(hi)}{u}'
```
`[unit not recorded]` should be unreachable once P1.8's writer refuses value-without-unit; it
renders loudly rather than silently for hand-migrated rows.

**CHANGE — table** (`:200-209`, `:230-236`): insert a `Value` column right after `State`
(`<td>{value_cell(c)}</td>` in `cell_rows`; `<th>Value</th>` in the header), and a
`Design scale` cell (`{e(c["design_scale"] or "—")}`) after `Tier basis`. The `.warn` CSS class
exists (`.vs.warn`); add a standalone `.warn {{ color:#8a4b2d; font-weight:600; }}` beside it.

**How the value's sources are shown alongside:** no new mechanism — the value sits in the same
per-population row as State/Tier basis, and the existing "Governing sources" blocks
(`:210-236`, fed by the `specification_source_links` join at `:98-105`) are keyed by the same
`population_code` heading. After P1.3's link writing lands, the page shows value AND sources
for one cell with zero further renderer work. (The plan's regeneration correction applies:
`site/specs/` pages are rebuilt by `scripts/generate/build_site.py`, NOT
`regenerate_derived.sh`; the e2e script below invokes `spec_page.py` directly with `--output`.)

**TESTS:** unit-test `value_cell` shapes: (1200,1500,'mm')→"1200–1500 mm"; (1500,1500,'mm')→
"1500 mm"; (1200,None,'mm')→"≥ 1200 mm"; (None,None,·) on stated→"no value recorded";
(1200,1500,None)→ carries `[unit not recorded]`. Then the e2e grep (bottom of this file).
**BLAST RADIUS:** `build_site.py --check` (advisory `site_pages_fresh`) goes red for all ~87
committed pages until `build_site.py` is rerun — regenerate in the same commit.
**RISK:** minimal; display only.

## P1.8 — bind the value tuple in the judgment writer

**WHERE:** `scripts/assess/assess_cell.py:552-566` — the INSERT binds literal `None, None,
None` (line 561) for `value_min, value_max, value_unit` (columns named at `:569`). **Plus a
defect found by this pass while reading the same INSERT: `regulatory_stratum_only` is computed
by `determine()` (`:377`) and reported (`:581`) but ABSENT from the INSERT column list
(`:566-572`) — every regulatory-stratum cell is written with the column's DEFAULT 0, so G1's
flag never reaches the DB and validate_evidence_state's condition 8 tests the wrong value.**

**NOW** (`:552-566`, abbreviated):
```python
        vals = (specification_id, det["item_code"], det["population"], det["state"], det["design_scale"],
                this_conv, ..., RULE_VERSION, det["derivation_sha"], det["code_floor_only"],
                None, None, None,
                det["falsification"], ...)
        cols = ("specification_id, item_code, population_code, state, design_scale, convergence_id, "
                ... "rule_version, derivation_sha, code_floor_only, "
                "value_min, value_max, value_unit, falsification_condition, ...")
```

**CHANGE — derivation, not dictation.** The value tuple is derived from NAMED extraction rows,
never typed freehand (`--value-min 1500` freehand would be the fabrication channel wearing a
flag):

```python
def derive_value(conn, extraction_ids, item_code, governing_refs):
    """Value tuple from cited extractions. Pointer discipline: the cell's value
    is justified only by extractions (a) on this item, (b) from sources that
    GOVERN this cell, (c) numeric, (d) in one unit. Anything else refuses.
    No unit conversion, ever — a converted value is an invented value."""
    ids = [int(x) for x in extraction_ids.split(",")]
    rows = conn.execute(
        "SELECT extraction_id, ref_id, item_code, claim_type, claimed_value, "
        "claimed_unit FROM source_value_extractions WHERE extraction_id IN (%s)"
        % ",".join("?" * len(ids)), ids).fetchall()
    found = {r[0] for r in rows}
    if found != set(ids):
        sys.exit(f"REFUSING: extraction id(s) {sorted(set(ids) - found)} do not exist.")
    vals, units = [], set()
    for xid, ref, ic, ct, cv, cu in rows:
        if ic != item_code:
            sys.exit(f"REFUSING: extraction {xid} is for item {ic}, not {item_code}.")
        if ref not in governing_refs:
            sys.exit(f"REFUSING: extraction {xid}'s source {ref} does not govern this "
                     f"cell — a value from a non-governing source cannot set the "
                     f"cell's range.")
        if ct not in ("numerical", "range"):
            sys.exit(f"REFUSING: extraction {xid} is claim_type={ct}; only "
                     f"numerical/range extractions carry a value.")
        try:
            vals.append(float(cv))
        except (TypeError, ValueError):
            sys.exit(f"REFUSING: extraction {xid} claimed_value {cv!r} is not numeric.")
        units.add(cu)
    if len(units) != 1 or None in units:
        sys.exit(f"REFUSING: mixed or missing units {sorted(map(str, units))} — "
                 f"normalise in the extractions (with locators) first; this engine "
                 f"never converts.")
    return min(vals), max(vals), units.pop()
```
Driven from `--value-from-extraction` (P1.4's flag). In `main()`:
```python
    value_min = value_max = value_unit = None
    if args.value_from_extraction:
        if det["state"] not in ("stated", "provisional"):
            sys.exit(f"REFUSING: state={det['state']} carries no value.")
        value_min, value_max, value_unit = derive_value(
            conn, args.value_from_extraction, args.item, set(det["governing_refs"]))
```
The INSERT then binds `value_min, value_max, value_unit` in place of `None, None, None`, **and**
adds `regulatory_stratum_only` to both tuple (`det["regulatory_stratum_only"]`) and column list
(placeholder count 26 → 27).

**derivation_sha / K01:** the sha payload (`sha()` at `:280-283`) is deliberately UNCHANGED —
`test_db_integrity.py:1153-1159` (K01) recomputes `item|pop|sorted(refs)::rule_version` for
every attested row regardless of rule_version, so changing the shape would need K01 to branch
per rule_version. Known consequence, recorded: a value change with an unchanged governing set
does not move the sha — value-level staleness is P2.2's witness mechanism's job, not K01's. If
the sha is later extended, it must be `RULE_VERSION` bump + K01 branch in one commit.

**TESTS:** e2e below (the value appears in the DB row and on the page); refusal battery: wrong
item / non-governing ref / qualitative claim / mixed units / non-numeric — one command each.
K01 still PASS on scratch. **BLAST RADIUS:** `register_integrity_check.py` and
`pilot_renderings.py` SELECT lists don't name value_* (no change needed);
`validate_evidence_state` has no value rules today (none added — a value-consistency rule
belongs to the same future doctrine as the aggregation rule). **RISK:** the min/max-over-cited-
extractions rule is a small piece of judgment doctrine executed as code — flagged in the
content section; mitigation is that it only aggregates what an operator explicitly cited, and
the cited ids are visible in the run log/report (add them to the report dict:
`"value_from_extractions": ids`).

---

# PHASE 2 — BACKWARD / RE-ENTRANT EDGES

## P2.1 — `db.py promote-mined-leads`

**WHERE:** new subcommand in `scripts/db.py`. Inputs measured at HEAD (commands in-line):
- `citation_mining.connections_produced` — JSON arrays of **bare DOI strings** (not CON-ids,
  despite the column name): 138 distinct DOIs; 4 already in `source_locators`, 2 in
  `evidence_sources`, **133 in neither** (re-derived; F4's F4 row confirmed, off-by-one fixed).
- `sessions/artifacts/2026-05-24-b11-mobility-{backward,forward}-discoveries.json` — 269
  distinct DOIs across the two files (272 discovery rows incl. duplicates), 13 already in
  `source_locators`, 0 in `evidence_sources`, **256 in neither**; 27 discovery rows carry
  `doi: null` (mostly standards, e.g. BS8300:2001) and are SKIPPED and counted, never promoted
  without an identifier.

**The JSON parsing shape, from the actual artefacts:**
```python
# Both files: { "<ANCHOR>": { ...per-anchor metadata..., "discoveries": [ {...} ] } }
# backward discovery row: {"doi": str|None, "year": "2001" (STRING), "author": str,
#                          "title_short": str, "in_evidence_sources": bool}
# forward discovery row:  {"doi": str, "year": 2022 (INT), "first_author": str,
#                          "title_short": str, "in_evidence_sources": bool}
# NOTE the key drift: backward says "author", forward says "first_author"; year type
# differs. title_short is truncated mid-word ("…a systematic re") — NEVER a title.
author = disc.get("first_author") or disc.get("author")
year = str(disc["year"]) if disc.get("year") is not None else None   # source_locators.pub_year is TEXT
```

**CHANGE — subcommand:**
```python
    p_pm = sub.add_parser("promote-mined-leads",
                          help="Promote harvested DOIs (citation_mining.connections_produced "
                               "and, once, the sessions/artifacts mining passes) into the "
                               "clue store as REFERENCE-ONLY leads")
    p_pm.add_argument("--source", choices=["mining", "artifacts", "both"], default="mining")
    p_pm.add_argument("--artifact", action="append",
                      help="artefact JSON path (repeatable); required with "
                           "--source artifacts/both")
    p_pm.add_argument("--session", required=True)
    p_pm.add_argument("--dry-run", action="store_true")
    p_pm.add_argument("--limit", type=int, help="promote at most N (rehearsal aid)")
```
Core (`promote_mined_leads`):
```python
def promote_mined_leads(source, artifacts, session, dry_run=False, limit=None):
    leads = {}   # norm_doi -> {doi, pub_year, authors, recovered_from}
    with dbcore.connect(dry_run) as conn:
        if source in ("mining", "both"):
            for slug, gref, cp in conn.execute(
                    "SELECT slug, global_ref_id, connections_produced FROM citation_mining "
                    "WHERE connections_produced IS NOT NULL"):
                try:
                    arr = json.loads(cp)
                except json.JSONDecodeError:
                    print(f"NOTE: unparseable connections_produced on "
                          f"{slug}/{gref} — skipped", file=sys.stderr)
                    continue
                for d in arr:
                    nd = dbcore.norm_doi(d if isinstance(d, str) else None)
                    if nd:
                        leads.setdefault(nd, {
                            "doi": nd, "pub_year": None, "authors": None,
                            "recovered_from": f"citation_mining:{slug}:{gref}"})
        skipped_no_doi = 0
        if source in ("artifacts", "both"):
            for path in artifacts or []:
                doc = json.load(open(path))
                relpath = os.path.relpath(path, REPO_ROOT_STR)
                for anchor, m in doc.items():
                    for disc in m.get("discoveries", []):
                        nd = dbcore.norm_doi(disc.get("doi"))
                        if not nd:
                            skipped_no_doi += 1
                            continue
                        author = disc.get("first_author") or disc.get("author")
                        year = disc.get("year")
                        # artefact wins over bare-mining entry: it carries year/author
                        leads[nd] = {
                            "doi": nd,
                            "pub_year": str(year) if year is not None else None,
                            "authors": author,      # first author, VERBATIM from artefact
                            "recovered_from": f"{relpath}:{anchor}",
                        }
        # dedup against BOTH ref-id homes, case-folded (the P1.1(d)/add-locator rule)
        held = set()
        for table in ("source_locators", "evidence_sources"):
            held |= {dbcore.norm_doi(r[0]) for r in conn.execute(
                f'SELECT doi FROM "{table}" WHERE doi IS NOT NULL')}
        todo = [v for k, v in sorted(leads.items()) if k not in held]
        if limit:
            todo = todo[:limit]
        written = []
        for lead in todo:
            rid = dbcore.next_ref_id(conn)
            row = {
                "ref_id": rid, "doi": lead["doi"], "pub_year": lead["pub_year"],
                "authors": lead["authors"], "recovered_from": lead["recovered_from"],
                "status": "REFERENCE-ONLY",
                # title DELIBERATELY NULL: the artefacts' title_short is truncated
                # mid-word and must never be promoted as a title (owner-adjacent
                # ruling in WALK-REPAIR-PLAN P2.1). The CHECK is satisfied by doi.
                "notes": "promoted lead; title withheld (title_short truncated in "
                         "artefact — retrieve before citing)",
            }
            cols = ",".join(row)
            conn.execute(f"INSERT INTO source_locators ({cols}) "
                         f"VALUES ({','.join('?' * len(row))})", list(row.values()))
            written.append((rid, lead["doi"]))
        print(json.dumps({
            "candidates": len(leads), "already_held": len(leads) - len(todo),
            "promoted": len(written), "skipped_no_doi": skipped_no_doi,
            "dry_run": dry_run}, indent=2))
        return written
```
Notes: (1) each `next_ref_id(conn)` sees the rows inserted earlier in the same transaction, so
ids advance correctly; (2) `source_locators` carries NO audit columns (`stamp_for` returns {} —
call it anyway for schema-honesty: `row.update(dbcore.stamp_for(conn, "source_locators",
session))`); (3) idempotent by construction — a re-run finds everything in `held` and promotes
0; (4) `title` NULL is legal: the table CHECK requires ANY ONE identifier and `doi` is set.

**REFUSALS/TESTS:** `--dry-run` first: expect `candidates≈389 (133+256), promoted 389,
skipped_no_doi 27` on the current DB (re-derive at run time — these numbers age); run, re-run →
`promoted: 0`; `add-locator` with one of the promoted DOIs under a new ref-id → R9 refusal
(proves the store now defends the promotions); `add-source` with one of them → P1.1(d)'s
"admit under the stash ref_id" refusal. **BLAST RADIUS:** ref-id high-water jumps by ~389 —
anything that assumed contiguity (nothing does; `next_ref_id` is the rule); `unmined`/coverage
readers unaffected (they read other tables); P1.1(d) MUST land first (the brief's stated
dependency, with F4 S2's corrected mechanism: `add-locator` already dedups two-table, but an
un-fixed `add-source` could mint a second identity for a promoted lead AFTER promotion — the
admission side is the gate). **RISK:** low; append-only leads with honest provenance. The one
judgment: artefact metadata (year/author) is stored VERBATIM, never enriched from memory —
retrieval enrichment happens at admission via R10, where the payload log exists.

## P2.2 — the determination↔synthesis comparator (and P2.3's replacement)

**P2.3 as commissioned is WITHDRAWN — category error confirmed** (read
`SELECT sql FROM sqlite_master WHERE name='supersession_check'`: per-anchor literature-currency
outcomes — `outcome IN ('current_best','superseded_by','refined_by',…)`,
`check_method IN ('pubmed_search',…)`; no reference to `specifications`, no staleness flag).
`supersession_check` keeps its job. Judgment-staleness propagation is ABSENT (S4's verdict
stands) and is built HERE, on `derivation_sha` + this comparator — one mechanism, not two.

**Design.** The primitive that exists: `specifications.derivation_sha` ("staleness check" in
its own DDL comment; verified by K01). What is missing is a WITNESS: the sha a synthesis saw
when it cited a determination. Comparing live-to-live is a tautology; the witness must be
stored at synthesis time. That requires one new table (a pointer + witnessed-version record,
the same class as `data_migrations.content_sha` — not a rule-5 copy, because "the version this
synthesis read" is a fact about the synthesis event, reachable nowhere else):

**Migration 066:**
```sql
-- 066_synthesis_determination_links.sql
PRAGMA user_version = 66;
BEGIN TRANSACTION;
CREATE TABLE synthesis_determination_links (
    slug                 TEXT NOT NULL REFERENCES slugs(slug),
    specification_id     INTEGER NOT NULL REFERENCES specifications(specification_id),
    -- The witness: specifications.derivation_sha AS READ when the synthesis
    -- cited this cell. Not a copy of a live fact (rule 5): the live sha moves,
    -- this one records what the synthesis actually rested on — same class as
    -- data_migrations.content_sha.
    derivation_sha_at_synthesis TEXT NOT NULL,
    created_at           TEXT NOT NULL,
    created_by_session   TEXT NOT NULL,
    PRIMARY KEY (slug, specification_id)
);
COMMIT;
```
Writer: `db.py link-synthesis-determination --slug S --specification-id N --session X` —
refusals: slug has a `bpc_metadata` row (a synthesis must exist to cite); specification exists;
the witness sha is READ FROM THE ROW at write time, never passed as an argument (an argument
would be an assertion; the read is a fact). `WRITABLE_TABLES` += the new table.

**The comparator — `scripts/audit/synthesis_determination_sync.py`:**
```python
#!/usr/bin/env python3
"""For each synthesis, every determination it cites must (a) still exist and
(b) still say what it said. Divergence is a FINDING, printed with both shas —
never a silent overwrite in either direction. CLAUDE.md §1 burden of proof:
without this, a synthesis can cite a determination that no longer says what
the synthesis says it says, and nothing reports it. (Measured 2026-08-25:
8 scripts touch both specifications and bpc_metadata; all render, count or
audit; none compares.)"""
...
def audit(conn):
    findings, n = [], 0
    for slug, sid, sha_seen in conn.execute(
            "SELECT slug, specification_id, derivation_sha_at_synthesis "
            "FROM synthesis_determination_links"):
        n += 1
        row = conn.execute(
            "SELECT derivation_sha, item_code, population_code FROM specifications "
            "WHERE specification_id=?", (sid,)).fetchone()
        if row is None:
            findings.append(f"{slug} cites specification {sid}: ROW GONE — the "
                            f"determination this synthesis rests on no longer exists")
        elif (row[0] or "") != sha_seen:
            findings.append(
                f"{slug} cites {sid} ({row[1]}×{row[2]}): STALE — synthesis saw "
                f"{sha_seen[:12]}, live row is {(row[0] or 'NULL')[:12]}. The "
                f"judgment changed after the synthesis was written; re-open the "
                f"synthesis or re-witness the link. Neither happens silently.")
    print(f"EXAMINED: {n}")
    ...exit 1 on findings, 0 otherwise; n==0 prints NOTHING-IN-SCOPE...
```

**Where it registers** (`governance/check-registry.yaml`, battery `data`, beside
`test_db_integrity`):
```yaml
  - id: synthesis_determination_sync
    cmd: [python3, scripts/audit/synthesis_determination_sync.py]
    battery: data
    kinds: [research, governance]
    level: advisory        # promote to blocking when bpc_metadata is first non-empty:
                           # a blocking gate today would be NOTHING-IN-SCOPE forever (§2(a))
    basis: synthesis/determination-currency
    cost: fast
    no_floor: 0 links until the first synthesis cites a determination — empty-by-decision,
      the mechanism must exist BEFORE the first synthesis so the first synthesis can be linked.
```
(If `basis:` values are contract-validated — C7 in the selftest — add the matching criterion id
under the `synthesis` stage in `pipeline-contract.yaml`, or reuse an existing `check: null`
criterion there; run `run_checks.py --selftest` to prove the basis resolves. This is the
registry-is-a-caller lesson from CLAUDE.md §5.)

**This is the plan's ONE new check** (A-4 item 1 said P2.2 must be stated as the exception —
stated here, with the burden-of-proof line inside the script's docstring where it cannot drift
from the code).

**TESTS:** scratch: write a cell, a bpc_metadata row, a link; run → EXAMINED: 1, PASS. Rerun
assess_cell for the same cell with a changed governing set (sha moves) → comparator exits 1
naming both shas. Delete the specifications row (scratch only) → ROW GONE finding.
**BLAST RADIUS:** registry (+1 entry), contract (basis), WRITABLE_TABLES, `--selftest` C7.
**RISK:** the witness table is the design decision most worth an owner glance (new table vs the
plan's "no new table" claim) — argued above; the alternative (a JSON column on bpc_metadata)
stores the same facts with worse joins.

## P2.5 — `connections.opus_reviewed`: DELETE (recommended), with the code

**WHERE:** `scripts/db.py:1374` (`"opus_reviewed": 0` in add-connection's data dict);
`schemas/connection.py:35` (`opus_reviewed: bool = False`); declared only in the 057 baseline
(`scripts/migrations/057_baseline_2026-08-12.sql:143`). Readers: **none** (measured; the only
other hits are a prose comment in `validate_pydantic_schemas.py:132` and this design).
`generate_parts.py build_part05` (`:245-266`) filters on `status` only.

**Recommendation: DELETE, under §1 symmetry.** Evidence: hardcoded to 0 at the only write site,
never settable, never read, 0 rows in the table; no committed data migration INSERTs it
(`grep -rn opus_reviewed scripts/migrations/data_*` → nothing), so CLAUDE.md rule 5's
can-never-drop clause does not bind — the column is droppable, not merely retirable. "Make it
real" is REJECTED here because it sets routing doctrine (must connections pass Opus review
before rendering in Part 5?) that no ratified record states — F4's content-costume finding;
that question goes to the owner (content section below), and if the owner later wants the gate,
it returns as a ratified rule with a reader, not as a dead flag.

**CHANGE:**
1. `db.py:1374`: delete the line `"opus_reviewed": 0,`.
2. `schemas/connection.py:35`: delete the field.
3. **Migration 067:**
```sql
-- 067_drop_opus_reviewed.sql
-- opus_reviewed: hardcoded 0 at its only write site, no reader repo-wide, no
-- data migration ever INSERTed it, 0 rows in the table. CLAUDE.md §1: deleting
-- is as cheap as adding; a field that looks like a safeguard and is not.
PRAGMA user_version = 67;
BEGIN TRANSACTION;
ALTER TABLE connections DROP COLUMN opus_reviewed;
COMMIT;
```
   (SQLite 3.45.1 in this container supports DROP COLUMN; the CHECK is column-level and travels
   with it; measured: no index, view or trigger references the column. CI's rebuild replays 057
   creating it and 067 dropping it — verify with `migrate_db.py --rebuild`.)
4. Sweep: update the prose comment in `validate_pydantic_schemas.py:129-135` (drop the name
   from the example list); `grep -rn opus_reviewed` over the live tree must return only
   `_archived/` and the immutable 057 baseline.

**Rendering half:** `build_part05` needs NO change — it already renders PENDING connections
under an explicit "Pending connections (open co-occurrence questions)" heading (`:256`), which
is honest labeling, not leakage. If the owner rules that unreviewed connections must NOT render
at all, that is a one-line status filter added THEN, under the ruling.

**TESTS:** rebuild green; `add-connection` on scratch lands without the key;
`validate_pydantic_schemas --strict` green (model and table agree in the new direction).
**RISK:** none beyond the owner-question above — the delete arm is pure code.

---

# PHASE 3 — RENDER TRUTHFULNESS

## P3.1 — `room_page.py`: six nonexistent objects, one key mismatch — REWRITE, not rename

**WHERE / NOW — every bad reference, measured:**

| Line(s) | References | Live schema says |
|---|---|---|
| `:26` | `SELECT * FROM room WHERE room_id = ?` | table is `rooms`, PK is `room_code` |
| `:29` | `SELECT * FROM room LIMIT 0` | same |
| `:35` | `FROM room_item ri WHERE ri.room_id = ?` + cols `design_stage, must_appear_on, notes` | table is `room_items` keyed `room_code`; its ONLY payload cols are `applicability, applicability_note` — `design_stage`/`must_appear_on` exist NOWHERE |
| `:44-45, :84-85` | `room_item_population` | **no such table, and no successor** |
| `:51` | `SELECT title FROM specification` | `specifications` exists but has NO `title` column and is keyed (item×population), not item; item display name lives in `items.name` |
| `:66` | `room_dar_provision` | **no such table** |
| `:75` | `room_conflict` | **no such table** (the live `conflicts` table is item/domain-scoped, no room key) |
| `render_html` `:95-…` | `room["room_label"]`, `building_type`, `evidence_density`, `criticality_note` | `rooms` columns are `room_code, name, category, description, status, notes` — none of the four exists |

Two renames (the plan's original P3.1) leave the script crashed at `:44`, `:51`, `:66`, `:75`
and then again in `render_html`. The Template-3 page (design-stage matrix, DAR provisions,
conflict register, per-room population applicability) has **no backing model in the live
schema**; only `rooms` (17 rows) and `room_items` (0 rows) exist.

**CHANGE — rewrite thin against what exists** (chosen over deletion because `rooms` now holds
17 real rows, `site/rooms/` pages exist and are linked, and `build_site.py`'s own docstring
`:6-9` wants the crash gone; deletion remains the §1-legal fallback if the owner retires the
room surface):

```python
def query_room(conn, room_code):
    room = conn.execute(
        "SELECT room_code, name, category, description, status, notes "
        "FROM rooms WHERE room_code = ?", (room_code,)).fetchone()
    if not room:
        return None
    d = dict(zip(("room_code", "name", "category", "description", "status", "notes"), room))
    d["items"] = [dict(zip(("item_code", "item_name", "applicability",
                            "applicability_note"), r))
                  for r in conn.execute(
            "SELECT ri.item_code, i.name, ri.applicability, ri.applicability_note "
            "FROM room_items ri JOIN items i ON i.item_code = ri.item_code "
            "WHERE ri.room_code = ? ORDER BY ri.item_code", (room_code,))]
    return d
```
`render_html` shrinks to: header (`room_code`, `name`, `category`, `status`), description,
notes, and ONE item table (Code · Item · Applicability · Note) linking each row to
`/specs/<item_code>.html`; an honest empty-state banner when `room_items` has no rows
("No items are linked to this room yet — `room_items` is unpopulated; the Template-3 matrix
(design stages, DAR provisions, conflict register) renders when its backing tables exist").
Delete the design-stage/DAR/conflict/population-matrix sections and their CSS — git archives
them; re-adding them without backing tables would be prose contradicting the database, §2(b)'s
exact defect in HTML form. `generate()`/`main()` keep their shape; variable `room_id` renamed
`room_code` throughout (`:252-261`).

**REFUSALS/TESTS:** `python3 scripts/generate/room_page.py R-BA --output /tmp/r_ba.html` exits
0 and the page carries the empty-state banner; a scratch `room_items` row renders one matrix
line; nonexistent room → the existing not-found error path. **BLAST RADIUS:** `site/rooms/*`
(17 stale files — regenerate all in the same commit or delete them until driven by
build_site.py); `build_site.py:6-9` docstring says room_page "crashes against the live schema
(no `rooms` table)" — now doubly stale; update it. `architecture/page-templates.md` Template 3
remains the aspiration — nothing in this fix contradicts it; it renders when its tables are
migrated (owner/content territory, flagged below). **RISK:** low; the deleted sections are the
recorded loss, named in the commit.

## P3.2 — `index.html` hardcodes its statistics

**WHERE:** `index.html:7` (meta description: "91 provisions, 661 evidence sources, 10
categories"), `:92` (the sentence *"Every count below is a live COUNT() against
data/guidebook.db"* — **currently false**), `:94-112` (stat tiles: 91 / 661 / 245 / 32),
`:117-…` (hand-picked "Recently modified"), `:148` ("All 91 provisions by category") and ten
per-category `sec-meta` counts (`:156,:256,:326,:366,:431,:511,:556,:611,:646,:676`).
Live: items = **93** (by category A19 B12 C6 D11 E14 F8 G9 H5 I4 K5), evidence_sources =
**10**, gaps OPEN = 5, connections = 0.

**CHANGE — make the false sentence true instead of deleting it: generate the page.**
1. Move `index.html` → `scripts/generate/templates/index.template.html`, with placeholders:
   `@N_ITEMS@`, `@N_SOURCES@`, `@N_XREFS@`, `@N_GAPS_OPEN@`, `@CATEGORY_SECTIONS@`,
   `@RECENT_ITEMS@`, `@GENERATED_STAMP@`.
2. New `scripts/generate/index_page.py` (same DB-path/`--check` conventions as spec_page):
```python
COUNTS = {
    "@N_ITEMS@":     "SELECT COUNT(*) FROM items",
    "@N_SOURCES@":   "SELECT COUNT(*) FROM evidence_sources",
    "@N_XREFS@":     "SELECT COUNT(*) FROM connections",
    "@N_GAPS_OPEN@": "SELECT COUNT(*) FROM gaps WHERE status='OPEN'",
}
# @CATEGORY_SECTIONS@: iterate SELECT category, COUNT(*) FROM items GROUP BY
# category ORDER BY category; within each, SELECT item_code, name FROM items
# WHERE category=? ORDER BY item_code — the per-category markup block is lifted
# verbatim from the current hand version so the design does not change.
# @RECENT_ITEMS@: SELECT item_code, name FROM items ORDER BY updated_at DESC
# LIMIT 5 (verify items carries updated_at: PRAGMA table_info(items); if it
# does not, drop the section rather than fake it).
```
   Output path `REPO_ROOT / "index.html"`; `--check` renders to memory and byte-compares
   against the committed file, exit 1 on drift.
3. Labels adjust to what is actually counted: "661 evidence sources · tiered" becomes the live
   number with the same label; "Cross-references" counts `connections` (0 today — honest);
   "Open gaps" counts OPEN gaps (5). The meta description at `:7` is templated from the same
   numbers. `@GENERATED_STAMP@` + a one-line drift warning satisfy §2(b)'s second arm for any
   prose that stays hand-written.
4. Drive + gate: add `index_page.py` to `build_site.py`'s build and to its `--check` sweep —
   the existing advisory `site_pages_fresh` registry entry (`check-registry.yaml:1359-1360`)
   then covers it with **no new registry entry**.

**TESTS:** `python3 scripts/generate/index_page.py && python3 scripts/generate/build_site.py
--check` green; hand-edit a count in index.html → `--check` exits 1 (the CLAUDE.md §7
"don't hand-edit generated output" trap now has an enforcer for this file). **BLAST RADIUS:**
index.html becomes generated output — add it to the §7 trap list's mental model; any styling
edit now goes to the template. **RISK:** template extraction is mechanical but 803 lines —
byte-compare the first generated output against the current file MINUS the corrected numbers to
prove nothing else changed.

## P3.3 — `register_integrity_check.py` prints "(DB cross-check on)" while the path never ran

**WHERE:** `scripts/audit/register_integrity_check.py:130-153` (`check()` builds `db_rows` from
0-row `specifications`), `:182`-region (`if db_rows:` gates every per-cell DB comparison),
`:362-366` (the selftest's own comment admitting the vacuity), `:425-431` (`main()` prints the
claim keyed on `args.db` alone).

**NOW** (`:429-431`):
```python
    n_cells = len(parse(doc))
    print(f"PASS: I1–I5 hold across {n_cells} cells × {len(ROLES)} registers"
          + (" (DB cross-check on)" if args.db else ""))
```

**CHANGE:** `check()` returns what it examined; the print reports what actually happened.
```python
def check(doc, db_path=None):
    ...
    return errors, len(db_rows)          # every return path; (errors, 0) for the early one
```
```python
    errors, n_db = check(doc, db_path=args.db or None)
    ...
    n_cells = len(parse(doc))
    if args.db:
        db_note = (f" (DB cross-check on: {n_db} specifications row(s))" if n_db
                   else " (DB cross-check REQUESTED BUT VACUOUS: specifications has "
                        "0 rows — the doc→DB and DB→doc comparisons examined nothing)")
    else:
        db_note = ""
    print(f"PASS: I1–I5 hold across {n_cells} cells × {len(ROLES)} registers{db_note}")
    print(f"EXAMINED: {n_cells + n_db}")
```
Caller sweep for the signature change: `main()` `:424` and `selftest()` (it calls `check()` —
`grep -n "check(" scripts/audit/register_integrity_check.py` and update each unpacking; the
selftest's ghost-row harness at `:362-380` then asserts `n_db == 1` on its injected row, which
turns the vacuity comment at `:362-366` from an admission into a test).

**TESTS:** run against the live DB → the VACUOUS wording appears; run the selftest → ghost-row
sub-test still FIRES and now also asserts the count. **BLAST RADIUS:** the registry entry for
this check (basis `render/...`) unchanged; any output-parsing consumer of the PASS line —
`grep -rn "DB cross-check" scripts/ tools/ .github/` → only this file. **RISK:** none; honesty
of an output line plus a counted subject.

## P3.4 — `parts/` freshness gate

**WHERE:** `scripts/generate_parts.py` (fingerprint already computed `:83-95` and EMBEDDED in
every file: `**Source DB fingerprint:** \`<fp>\`` via `header()` `:105-109`; measured in
`parts/v10/part04.md:5`); `governance/pipeline-contract.yaml:138-142` (`render-freshness`,
`check: null`); `governance/check-registry.yaml` (new advisory entry).

**CHANGE:**
1. `generate_parts.py` gains `--check`:
```python
    ap.add_argument("--check", action="store_true",
                    help="verify parts/v10/*.md embed THIS DB state's fingerprint; "
                         "write nothing; exit 1 on drift")
```
```python
    if args.check:
        fp, _blob = fingerprint(conn)
        import re as _re
        pat = _re.compile(r"\*\*Source DB fingerprint:\*\* `([0-9a-f]{12})`")
        stale, missing, n = [], [], 0
        for _key, fn, _l, _t in PARTS + [("manifest", "manifest.md", "", "")]:
            path = os.path.join(args.out, fn)
            if not os.path.exists(path):
                missing.append(fn); continue
            n += 1
            m = pat.search(open(path, encoding="utf-8").read())
            if not m or m.group(1) != fp:
                stale.append(f"{fn} (embeds {m.group(1) if m else 'NO FINGERPRINT'}, "
                             f"DB is {fp})")
        print(f"EXAMINED: {n}")
        if stale or missing:
            print("STALE parts/ vs DB:", *stale, *(f"MISSING {f}" for f in missing),
                  sep="\n  ")
            print("regenerate: python3 scripts/generate_parts.py")
            return 1
        print(f"parts/ fresh at fingerprint {fp}")
        return 0
```
   (PARTS is the module's own file list `:47-62` — reuse it; do not glob, so a stray file
   cannot fail the gate.)
2. Registry (advisory — same level as `site_pages_fresh`, same rationale):
```yaml
  - id: parts_fresh
    cmd: [python3, scripts/generate_parts.py, --check]
    battery: data
    kinds: [research, governance]
    level: advisory
    basis: render/render-freshness
    cost: fast
```
3. `pipeline-contract.yaml:142`: `check: null` → `check: scripts/generate_parts.py --check`,
   and trim the criterion's now-false clause "parts/ has no committed fingerprint gate".
   Run `run_checks.py --selftest` (C7: every basis resolves) — the registry-is-a-caller trap.

**Known honest limit, restated not hidden:** the fingerprint hashes COUNTS + user_version
(`:83-95`'s own comment) — an UPDATE-only change is invisible to it. It is a cheap label, the
same one `build_site.py` uses; the byte-level truth stays `--check`-by-regeneration.
**TESTS:** clean tree → EXAMINED: 14, exit 0; apply any data migration on a scratch checkout →
exit 1 naming each file. **RISK:** none; advisory.

---

# PHASE 4 — APPARATUS HONESTY

## P4.1 — attestation window: one commit locally, whole branch on CI

**WHERE:** `scripts/audit/adherence_log_audit.py:569-570` (`--base` default `HEAD~1`);
`scripts/run_checks.py:206-207` (`expand()`), `:210-221` (`run_check()` builds cmd), `:432-438`
(the `--changed-from` base is computed for SELECTION and never given to the checks),
`:491-494` (the run loop); `governance/check-registry.yaml:899-956` (the four
`adherence_log_audit` entries carry no `--base`); `.github/workflows/ci.yml:210-225`
(fetch-depth 0; on a PR merge ref, `HEAD~1` = the base-branch tip, so the same default means
"the whole branch" there and "the last commit" locally — OPUS D-11's mechanism, verified).

**CHANGE — a `@BASE@` token, the same mechanism as `@SESSION@`:**
1. `run_checks.py:206-207`:
```python
def expand(cmd, session, base):
    return [part.replace("@SESSION@", session).replace("@BASE@", base) for part in cmd]
```
2. `run_check()` gains `base` (`:210`), passes it (`:221` → `cmd = expand(check["cmd"],
   subject, base)`); the loop at `:491-494` passes it; `main()` computes it once, right after
   the selection block (`:438`):
```python
    diff_base = args.changed_from or "HEAD~1"
```
   With `--changed-from origin/main`, every check that declares `@BASE@` now audits the same
   window the selection classified — locally AND on CI (CI's battery jobs run `--kinds …`
   without `--changed-from`; give them the same truth by having ci.yml's battery step export
   the base: change the attestation job's run line to
   `python3 scripts/run_checks.py --battery attestation --kinds "…" --github --base-ref origin/${{ github.base_ref || 'main' }}`
   and add `--base-ref` as an explicit override for `diff_base` in main(). On push builds
   `github.base_ref` is empty → `origin/main`, which is the honest window for main too.)
3. Registry — the four entries (`:900`, `:921`, `:938`, `:956`) each gain the token:
```yaml
    cmd: [python3, scripts/audit/adherence_log_audit.py, --check, presence, --base, "@BASE@"]
```
   and their `no_floor`/`note` prose ("HEAD~1..HEAD") is updated to name the computed window.
4. `adherence_log_audit.py` needs no change — `--base` already exists; the default simply stops
   being load-bearing.

**TESTS:** locally: commit A touches a synthesis path, commit B is docs-only; old behaviour:
`--battery attestation --changed-from origin/main` after B → NONE/PASS; new: FAILs (or examines
the synthesis file) exactly as CI would. `run_checks.py --selftest` (it exercises CLI paths —
C6 etc.) still green; add one selftest case: a dummy check with `@BASE@` in cmd receives the
literal passed base. **BLAST RADIUS:** the four attestation checks only (no other registry cmd
gains the token yet); preflight.sh (calls run_checks with `--changed-from`) now predicts CI —
the stated goal. **RISK:** low; token expansion is inert for every cmd that lacks it.

## P4.2 — jurisdiction vocabulary: members FIRST, then the check, ONE change

**WHERE:** `schemas/enums.py:140-178` (`JurisdictionCode` — 24 country codes + `ISO`, `EU`;
no `ES`, `PT`, `FI`); `scripts/db.py:2370-2408` (`insert_jurisdictional_value` — validates
item FK and tier band, **no jurisdiction check of any kind**). `jurisdictional_values.
jurisdiction` is bare `TEXT NOT NULL` (no CHECK), live values incl. 20 × `GB` (the recorded
D-6/C-1 backlog — `UK` is the project convention).

**Owner ruling honoured: both edits land in ONE commit, members first in the diff.**
1. `schemas/enums.py` — insert alphabetically into the country block:
```python
    ES = "ES"   # Spain
    FI = "FI"   # Finland
    PT = "PT"   # Portugal
```
   (Bucket-2 targets the schema could not represent — OPUS C-3; adding members is inert on its
   own: the enum's only importer, `scripts/validate_jurisdiction.py:29-31`, treats members as
   the valid set, so additions can only turn findings green, never red.)
2. `db.py insert_jurisdictional_value` — after the item-FK refusal (`:2381-2382`):
```python
        jur = data.get("jurisdiction")
        _root = str(Path(__file__).resolve().parents[1])
        if _root not in sys.path:
            sys.path.insert(0, _root)
        from schemas.enums import JurisdictionCode
        try:
            JurisdictionCode(jur)
        except ValueError:
            raise ValueError(
                f"jurisdiction {jur!r} is not a JurisdictionCode member "
                f"(schemas/enums.py — the ratified A3 list; UK not GB, by project "
                f"convention). A value outside the list is a doctrine change: add the "
                f"member in the same change as the first row that needs it. "
                f"Nothing was written.")
```
   The vocabulary's single home is the enum (there is no schema CHECK to read, and live rows
   are a sample that would legitimise `GB` — `check_vocab` is exactly wrong here; the enum is
   the ratified home the docstring names).

**TESTS:** `add-jurisdictional-value … --jurisdiction ES` → lands (the batch's own target —
proving member-first ordering mattered); `--jurisdiction GB` → refused naming the convention;
`--jurisdiction XX` → refused; `validate_jurisdiction.py` still green. **BLAST RADIUS:**
`validate_jurisdiction.py` (reads the enum — green-only change); any prose listing "24 country
codes" (the enum's own docstring `:143` — update to 27); the 20 live GB rows are UNTOUCHED
(data backlog under its existing ruling; the refusal stops the bleeding, the migration that
renames them is that ruling's business, not this fix's). **RISK:** none beyond the recorded GB
question, which is already owner-ruled territory.

## P4.3 — `next_gap_id()` mints a shape the register no longer uses

**WHERE:** `scripts/db.py:135-144`; live gap ids: `GAP-B01-001…GAP-B02-001` (5 rows, ALL
batch-scoped); `schemas/evidence_state.py:167` accepts only `^GAP-\d{3,4}$` for
`gap_register_id`; `schemas/gap.py:31-32` accepts any `GAP-*`.

**NOW:** `GLOB 'GAP-[0-9]*'` finds no live row → returns un-padded-adjacent `GAP-001`; no
collision today, but two allocators exist (this one and `assess_cell.py:428-431`, which mints
UN-padded `GAP-1` and crashes its own pydantic gate — P1.4 crash 1).

**CHANGE:** both delegate to the single `dbcore.next_gap_id(conn)` specified in P1.4 item 6
(zero-padded flat-numeric mint; batch-scoped ids recognised and skipped). `db.py:135-144`
becomes:
```python
def next_gap_id() -> str:
    with connect(readonly=True) as conn:
        return dbcore.next_gap_id(conn)
```
**The format question, named and bounded:** whether NEW gaps should be batch-scoped
(`GAP-B03-001`) rather than flat-numeric is a register-naming convention — content-adjacent.
The code fix does not decide it: it makes the flat mint CORRECT (padded, collision-free,
pydantic-passing, the only shape a cell may cite per `evidence_state.py:167`). If the owner
wants batch-scoped minting, that is a later `--batch` parameter plus a widened
`evidence_state.py:167` regex — the regex widening (to also accept `GAP-B\d{2}-\d{3}`) is
needed EITHER WAY the moment a cell cites a live batch-scoped gap, and is recommended now:
```python
        if v is not None and not re.match(r"^GAP-(\d{3,4}|B\d{2}-\d{3})$", v):
```
(schema↔DB drift is a bug, CLAUDE.md §7 — the model currently rejects every gap id in the
committed register.) **TESTS:** `db.py next-id gaps` → `GAP-001`; after inserting it, → 
`GAP-002`; `EvidenceStateRecord(gap_register_id="GAP-B01-001")` validates after the regex fix.
**BLAST RADIUS:** `next-id` dispatch (`:1328-1334`) unchanged; pydantic mirror tests
(`validate_pydantic_schemas`). **RISK:** none.

## P4.4 — runbook repairs (`decisions/DR-2026-08-19-research-restart-operative-instrument.md`)

**Form of the edit — flagged as process, decided here as design:** the DR is RATIFIED but is
"meant to be RUN"; its steps have been overtaken by later owner rulings (the 2026-08-24
pointer ruling abolished step 7's dual write; the 2026-08-20 cull deleted step 0's script; the
CLI grew `add-candidate`). The edit is therefore a **dated correction, marked in place** — not
a silent rewrite: each corrected passage gets a `> **CORRECTED 2026-08-25:**` block quote
under it and the stale text struck with `~~…~~`. Attestation required (touching `decisions/` —
CLAUDE.md rule 2).

1. **`:794`** — NOW: `python3 scripts/audit/table_connectivity.py   # record 0 of 80`.
   The script was deleted in cull commit `80a34d1`. CHANGE: strike the line;
   correction block: *"table_connectivity.py was deleted in the 2026-08-20 cull; the step-0
   pre-state record is complete without it (sha256 + dod + test_db_integrity + rebuild)."* No
   substitute command — substituting a different tool's number for "0 of 80" would fake
   continuity of a metric that no longer exists.
2. **`:830`** — NOW: `**Step 4 — screen and stage (R7, R15).** No CLI; scratch SQL.` CHANGE:
   *"CLI: `db.py add-candidate` (exec-id FK, slug FKs, disposition/locator vocab from the
   schema's own CHECKs, and the R15 ADMITTED⇒RESOLVED refusal built in — db.py:823-838,
   :2270-2313). Scratch SQL for candidates is no longer lawful; the CLI refuses what R15
   forbids."*
3. **`:854-864`** — NOW: the "mandatory companion UPDATE" block: hand-SQL for
   `doi_resolution_outcome/pages/url`, then `UPDATE search_executions … admitted_ref_ids='[…]'`
   + junction INSERT + candidate UPDATE, citing H03/H04/H05. CHANGE (correction block):
   - `--url/--url-accessed/--pages/--doi-resolution-outcome` are add-source flags since Act 2;
     `--scope` since P1.1. The companion UPDATE for evidence_sources is DEAD — strike it.
   - `admitted_ref_ids` dual write: ABOLISHED by owner ruling 2026-08-24 (`db.py:394-400`
     "intentionally NOT written"; H03/H04 REMOVED — `test_db_integrity.py:1038`). Strike;
     `search_admissions` junction is the sole carrier, written by `log-search
     --admitted-ref-id` or `update-search` (P4.6).
   - the counts UPDATE → `db.py update-search` (P4.6); the candidate disposition UPDATE →
     `db.py update-candidate` (P4.6). Until those land, the correction block says so
     explicitly ("hand SQL remains the only path for THESE TWO statements; that is the P4.6
     coverage bug, not a licence").
   - `:855`'s method list gains `direct-render` (P1.1e).
4. Also swept while in the file: `:944` names H03/H04 as live parity gates — same correction
   block as (3).

**TESTS:** none mechanical (prose); the grep that proves the sweep:
`grep -n "table_connectivity\|admitted_ref_ids='\|No CLI; scratch SQL" decisions/DR-2026-08-19-*.md`
returns only struck/corrected lines. **RISK:** editing a ratified instrument — mitigated by the
marked-correction form; if the owner prefers a separate corrections annex, the same blocks move
there verbatim (flagged in the content section).

## P4.5 — Co-1: what actually remains

**Measured correction to the brief:** `validate_evidence_state.py:76-110`'s two bugs (the
`r.get` NameError and the retired-status test) are **already fixed at HEAD** — the current code
tests `vs == "UNVERIFIED" and disp == "CLOSED"`; the comment at `:96-101` narrates the repair.
Settle it yourself: `git show 038913b:scripts/validate_evidence_state.py | sed -n '94,100p'`
(old, broken) vs `sed -n '100,110p' scripts/validate_evidence_state.py` (current).

**What remains, and the fixes:**
1. **The write half** — `--co1-provenance` / `--co1-source-type` /
   `--synthesis-attribution-required` on add-source: designed at P1.1(g).
2. **The read half is vacuous, §2(a)-style:** `validate_source_co1_fields` runs only over
   `data/sources/*.yaml`, guarded by `os.path.isdir(source_dir)` (`:452-456`) — the directory
   does not exist, so the Co-1 rules examine NOTHING while the actual Co-1 rows (3 live) sit in
   the DB. CHANGE: add a DB arm beside `validate_db()`:
```python
def validate_co1_db(conn):
    """A5 §6.3 Co-1 rules over evidence_sources (the rows that exist), not a
    YAML directory that never did."""
    errors, n = [], 0
    for ref, vs, disp, reason, tier in conn.execute(
            "SELECT ref_id, verification_status, verification_disposition, "
            "verification_closure_reason, tier FROM evidence_sources "
            "WHERE evidence_type='co1'"):
        n += 1
        if vs == "UNVERIFIED" and (disp or "").upper() == "CLOSED":
            errors.append(f"Co-1 {ref} UNVERIFIED+CLOSED "
                          f"({reason or 'no reason recorded'}) — cells citing it as "
                          f"sole Co-1 evidence must downgrade to pending (A6 §2.8)")
        if tier is not None and tier != 1:
            errors.append(f"Co-1 {ref} has tier={tier}; Co-1 is tier 1 (T-03)")
    return errors, n
```
   Called from `validate_db()` and folded into its error/count return; the check's EXAMINED
   rises by the live Co-1 count (3 today) — the gate finally has its subject. The YAML arm
   stays for the day the directory exists.

**TESTS:** live DB → +3 examined, 0 errors; scratch with a tier-2 co1 row → error. **BLAST
RADIUS:** `validate_evidence_state` registry entry (blocking) — its subject count changes,
nothing else. **RISK:** none.

## P4.6 — R8 ordering: `update-search` (and the step-7 `update-candidate` it implies)

**WHERE:** new subcommands in `scripts/db.py`. The R8 bind (OPUS D-4, verified): step 3 logs
every query with counts 0 BEFORE screening; step 7 completes `results_screened`/
`results_admitted`; `log_search` is append-only INSERT (`:404-407`) — so the sanctioned path
either violates R8's ordering or hand-writes the UPDATE that blocking H05 audits.

**`update-search` design:**
```python
    p_us = sub.add_parser("update-search",
                          help="Complete a search_executions row's YIELD after screening "
                               "(R8: the query was logged BEFORE screening; this is the "
                               "step-7 completion, identity fields immutable)")
    p_us.add_argument("--exec-id", required=True, type=int)
    p_us.add_argument("--results-found", type=int)
    p_us.add_argument("--results-screened", type=int)
    p_us.add_argument("--results-admitted", type=int)
    p_us.add_argument("--saturation-signal")
    p_us.add_argument("--findings-note")
    p_us.add_argument("--admitted-ref-id", action="append",
                      help="repeatable; writes the search_admissions junction row(s) in the "
                           "same transaction (the sole carrier of the admission edge)")
    p_us.add_argument("--session", required=True)
    p_us.add_argument("--dry-run", action="store_true")
```
Refusals in `update_search(...)`:
- `exec_id` must exist (named refusal).
- **Identity is immutable**: the updatable set is exactly `{results_found, results_screened,
  results_admitted, saturation_signal, findings_note}` — a whitelist constant beside
  `_BPC_META_COLS`; `slug/query_text/engine/…` are refused by construction (no flags) AND by
  the whitelist (python-API path).
- H07: repeated `--admitted-ref-id` values refused (same code as `log_search:371-377`).
- Each admitted ref must exist in `evidence_sources` (same as `log_search:425-430`); an
  `(exec_id, ref_id)` pair already in `search_admissions` → named refusal ("one admission edge
  per (search, source); it is already recorded"), not a PK crash.
- H05: after writing the junction rows, `results_admitted` (given or derived) must equal
  `SELECT COUNT(*) FROM search_admissions WHERE exec_id=?` — refuse on disagreement, naming
  both numbers; if `--results-admitted` omitted but refs given, derive it.
- Counts may not DECREASE below the junction count (screened ≥ admitted enforced likewise).

**`update-candidate` design** (the other hand-SQL statement on step 7's mandatory path):
```python
    p_ucand = sub.add_parser("update-candidate", help="Move a staged candidate's disposition")
    p_ucand.add_argument("--candidate-id", required=True)
    p_ucand.add_argument("--disposition", required=True)
    p_ucand.add_argument("--locator-status")
    p_ucand.add_argument("--notes")
    p_ucand.add_argument("--session", required=True)
    p_ucand.add_argument("--dry-run", action="store_true")
```
Refusals: candidate exists; `check_vocab` on disposition/locator_status (schema CHECKs);
R15 both halves — `ADMITTED` requires `locator_status='RESOLVED'` (existing rule,
`insert_search_candidate:2297-2302`) AND `--notes` beginning with the literal `RESOLVED:`
(the runbook's re-described-from-source predicate, `:863-864`).

**TESTS:** the R8 sequence end-to-end on scratch: `log-search` (found N, screened 0, admitted
0) → `add-candidate` → `add-source` → `update-search --exec-id E --results-screened N
--admitted-ref-id REF-X` → junction row exists, counts agree; `test_db_integrity` H05/H07
(surviving forms) PASS; second identical `--admitted-ref-id` → refused. **BLAST RADIUS:**
runbook step 7's correction block (P4.4-3) points here; skills that narrate step 7. **RISK:**
low; mirrors log_search's own refusal code.

## P4.7 — the four dropped-without-deferral items

**(a) `add-population-match` same-session divergent grade crashes (S2 case 24).**
WHERE: `db.py:2363` — `row["match_id"] = f"{session[:24]}-{ref}-{data['target_population']}"`;
a second grade from the same session mints the same PK → uncaught IntegrityError, which
silently abolishes the same-session half of the dissent mechanic CLAUDE.md §4 celebrates.
CHANGE (replacing `:2362-2363`):
```python
        if row.get("match_id") is None:
            base = f"{session[:24]}-{ref}-{data['target_population']}"
            mid, i = base, 1
            while dbcore.exists(conn, "evidence_population_match", "match_id", mid):
                i += 1
                mid = f"{base}-{i}"
            row["match_id"] = mid
```
plus `p_epm.add_argument("--match-id")` (the S2-suggested explicit override; dispatch
pass-through — the column is already in `_COLS`). The divergence NOTE at `:2350-2356` already
prints; unchanged. TEST: same session, same (ref, population), two grades → both land,
`…-2` suffix, NOTE printed twice.

**(b) `adjudication_integrity` exit code — NOT REPRODUCIBLE at HEAD; no change.** `audit()`
returns `0 if not viol else 1` (`:136`) and `main` propagates it (`:171-178`). Reproduced this
pass with a scratch copy + induced violation: **EXIT 1, VERDICT FAIL** (fixture command:
`cp data/guidebook.db $SP/f.db; python3 - <<… UPDATE tier=5 …>>;
GUIDEBOOK_DB_PATH=$SP/f.db python3 scripts/audit/adjudication_integrity.py; echo $?`). S2's
"EXIT: 0" is most plausibly a piped invocation capturing the wrong status (`| tee` swallows
it without `pipefail`). Disposition: RECORDED, re-verify with the bare command before filing
any fix; if it still shows 0 unpiped, the file has a second entry point somewhere and THAT is
the finding.

**(c) `source_locators.jurisdiction`: 818/875 unusable, no reader.** Re-measured shape: 385
NULL, 89 `'—'`, dozens of URLs and slug-strings; ISO-code rows are a small minority. There is
no reader to fix and the batch's bucket filter cannot run on it. Disposition — **recorded
deferral with a tripwire, not a silent pass**: (1) no writer change (P2.1 writes NULL
jurisdiction — honest); (2) the bucket-driven batch must derive jurisdiction from
`evidence_sources`/retrieval, never from this column, and the promotion notes say so; (3) the
normalisation is a DATA migration authored when the batch's bucket queries exist to name what
"usable" means — authoring it now would invent a target vocabulary for 875 rows nothing reads.
Settling command for the future author:
`SELECT jurisdiction, COUNT(*) FROM source_locators GROUP BY 1 ORDER BY 2 DESC;`
(4) tripwire: one line in `audit_evidence_metadata.py` (or the eventual bucket query's own
EXAMINED) reporting the non-ISO share, so the deferral is visible, not forgotten.

**(d) `spec_value_probes` / `items.pmp_*` writers absent while the
progressive-measurement skill teaches raw INSERT.** Every mobility item is a quantity; probes
are the vetting path. Design (Phase-4 depth):
- `db.py add-value-probe`: flags mirroring the DDL's NOT NULLs — `--probe-id --walk-id --slug
  --item-code --spec-value-origin --spec-unit --direction --population --claim-type
  --step-index --phase …` (dump the full column list with
  `python3 -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"SELECT sql FROM sqlite_master WHERE name='spec_value_probes'\").fetchone()[0])"`
  — this pass read the first half; the implementer pastes the rest). Refusals: FK slug/item;
  `check_declared` on `direction/claim_type/phase` (all CHECKed); duplicate probe_id;
  population in `populations`; origin requires unit (the R3 family).
- `db.py update-pmp --item CODE [--delta-min N] [--direction up|down] [--empirical-ceiling N]
  [--gap-signed N] --session S`: whitelist exactly the five `pmp_*` columns (measured:
  `pmp_delta_min, pmp_direction, pmp_last_walk_at, pmp_empirical_ceiling, pmp_gap_signed`);
  `pmp_last_walk_at` is stamped by the writer (`dbcore.now()`), never passed — it records the
  walk event. Refusal: item FK; at least one field.
- `WRITABLE_TABLES` += `"spec_value_probes"` (items is UPDATE-only here — the emit path diffs
  INSERTs; an items UPDATE ships via `emit_data_migration` as usual — note this in the
  subcommand's help so the capture gap is named where the operator stands).
- The skill sweep: replace the raw-INSERT teaching with these subcommands (grep
  `skills/*progressive*` / `grep -rln spec_value_probes skills/`).

---

# DEPENDENCY GRAPH — what must precede what

```
P0.1 ──┬── P0.2 (same commit: P0.1 breaks P0.2's old text mechanically)
       │
       ▼
P1.1 (add-source honest: scope/I1/I4/dedup/co1) ──────────┬─► P2.1 promote-mined-leads
  │     [065 evidence_type+tier CHECK can trail P1.1;     │      (admission-side dedup is
  │      check_declared no-ops until it lands]            │       the gate — F4 S2 corrected
  ▼                                                       │       mechanism)
P1.2 add-extraction + add-external-root (+WRITABLE_TABLES)│
  ▼                                                       │
P1.4 assess_cell de-pilot (needs dbcore.next_gap_id) ◄────┼── P4.3 (same dbcore function —
  ▼                                                       │        land together)
P1.5 anchoring conditions 1+3 ──► P1.8 value binding ─────┤
  ▼                                   ▲                   │
P1.3' assess_cell writes spec links + │ (P1.8 needs P1.2's│
      narrow add-specification        │  extraction rows) │
  ▼                                   │                   │
P1.7 spec_page value column ──────────┴───────────────────┴─► E2E WALK (below)
  ▼
P1.6 update-bpc --population ──► 066 + link-synthesis-determination ──► P2.2 comparator
                                                  (P2.3 replacement — same mechanism)
P2.5 delete opus_reviewed (067) ── independent
P3.1 room_page rewrite · P3.2 index generator · P3.3 register honesty · P3.4 parts --check
                                              ── all independent of the walk and of each other
P4.1 @BASE@ · P4.2 enum+check · P4.5 co1-db-arm · P4.6 update-search/-candidate ·
P4.7a match-id suffix                          ── independent; P4.4 (runbook text) LAST,
                                                  after P1.1/P4.6 exist to be pointed at
```

**The true critical path** is seven items long:
**P0.1 → P1.1 → P1.2 → P1.4 → (P1.5, P1.8, P1.3′) → P1.7 → E2E.**
Everything else can proceed in parallel or wait. The single most load-bearing edit in the
repository is P1.1's I1/I4 reconciliation — without it every admission is born failing a
blocking gate, which is the condition that manufactured the 2026-08-19 fabrication.
