# Execution plan — walk the pipeline with provenance

**Status:** ACTIVE (rev 2). **Written** 2026-08-20. **Revised** 2026-08-20 18:18 UTC.
**Author:** Opus 5, from four read-only Fable 5 audits of rev 1 (factual re-measurement ·
strategic steelman · command-level dry-run · confirmation-and-runbook) plus Opus 5 adjudication.
Rev 2 replaces rev 1 in place; rev 1 is in git history. Nothing is quoted forward from rev 1
without re-measurement.

**Goal, in the owner's words:** *break out of recursion to effectively do research that can walk
the pipeline with provenance.*

**Relation to the operative instrument.** This does **not** supersede
`decisions/DR-2026-08-19-research-restart-operative-instrument.md`. It executes its §3 step 5 and
its §4 acceptance criterion. Two honest frictions with that DR are recorded in §8 rather than
finessed.

---

## 0. What rev 1 got wrong

Rev 1 was accurate on its census and its Class-A/Class-B sort — re-measured, it holds. It failed
on the parts that touch execution. All seven corrections below were verified live at `83b5b40`,
canonical sha256 `ebab426f…8c692b`, `user_version` 60.

**0.1 — There is a determination engine, and it is not usable for this cell.**
`scripts/assess/assess_cell.py` (34 KB) writes `specifications` and `convergence_assessment`, is
pydantic-validated, refuses the canonical DB by design (`:491-492`), emits replayable SQL, and is
a **registered check** (`test_assess_cell_pilot`, registry `:1234`). Rev 1's claim that "there is
no production writer" is true only as *no writer against canonical*.

It was then run live on a scratch copy for this exact cell:

```
determine(conn,'A-18','AUT','room-acoustic-performance') →
  state       = 'stated'                       ← violates §9 forbid 5
  tier_basis  = 'CO1+T2'
  governing   = ['REF-00607','REF-00965','REF-00966','REF-00968']   ← REF-00607 is PROXY
  convergence = 'pending_assessment', 2 axes (clinical + co1)
  down_weighted = all four anchoring sources
```

It anchors on REF-00607 — a systematic review of *predominantly normal-hearing listeners*,
graded PROXY for AUT at MB1-008 — as a second "clinical" axis, and has no input for the
chain-of-one lineage or the DR §7 dispute cap. **New defect, not previously recorded: a cell in
which every anchoring source is down-weighted still returns `stated`.** That is an engine bug and
is logged in §1 as B6-a; it is not fixed here.

**Consequence: the walk cell is written by hand SQL.** Not by `assess_cell.py`, not by a new
CLI. Using the engine would require editing its hardcoded `PILOT_CELLS` roster (`:114-129`) —
which is precisely the wording-evasion §9 forbids.

**0.2 — The capture path in rev 1 cannot carry the rows.**
`scripts/research/emit_batch_sql.py:37-49` diffs a fixed `TABLES` list containing none of
`specifications`, `specification_source_links`, `convergence_assessment`, `item_bpc_links`. It
exits "no delta". **The hand-written SQL file is itself both the capture and the migration
source**; `emit_batch_sql.py` is not used in this phase at all.

**0.3 — Phase 0 and Phase 1 were one phase drawn as two, gated backwards.**
Rev 1's Phase 0 SQL carried `<placeholders>` that rev 1's Phase 1 was to author, while §12 gated
Phase 1 *behind* Phase 0, and Phase 0 applied its migration to append-only canonical. Rev 1's
Phase 1 contained no write step at all. Worse, `'<JSON array — …>'` is not valid JSON, so
`validate_evidence_state.py:253-258` FAILs a `provisional` cell and preflight could never go
green. **Merged into one phase (§4).**

**0.4 — The repository holds no full text, and two of three sources cannot be fetched here.**
All five retrieval-log artefacts are Crossref *metadata* JSON (12–35 KB), two with a JATS
abstract. Rev 1 commanded "read the three Co-1 sources in full — not the abstracts, not the
payload metadata" and named no retrieval step. Probed live:

| Source | OA status | Full text obtainable from this environment |
|---|---|---|
| REF-00966 | free (PMC10726197) | **Yes** — 231 KB, 71.8k chars, Methods/Results/Discussion present |
| REF-00965 | CC-BY hybrid (vol 233, art 110581) | **No** — Elsevier 403; keyless article API returns coredata only |
| REF-00968 | gold OA CC-BY (vol 12 iss 1) | **No** — T&F 403; Bristol PURE exposes no file; DOAJ links back to T&F |

**Degraded mode is therefore load-bearing for two of three sources, not a fallback** (§4.3). A
plan that says "read them in full" without it becomes, on contact, "author from abstracts" — the
2026-08-19 fabrication pattern in a new costume.

**0.5 — Two walk hops in rev 1 were factually wrong.**
- REF-00968 is admitted under **exec 6** ("unpredictable intermittent sound and sensory load…"),
  not exec 1. The backward walk traverses execs **1 and 6**.
- **DEM does not appear in `population_axis_map` for either of A-18's axes.** AX-SPR → NDV/AUT/
  ADHD (PRIMARY), MH/BRAIN/VES (SECONDARY), EPI (SITUATIONAL); AX-AUD → DEAF (ALIAS), DEAFBLIND
  (PRIMARY). DEM maps to AX-COG-O/AX-ARO/AX-VIS-L/AX-AMB. **DEM reaches this slug via
  `item_population_links` (8 of 13 items), not the axis map.**

**0.6 — B5-f, found during execution: the provenance mechanism fails the project's own syntax
gate the moment it retrieves anything that is not JSON.**

`scripts/research/retrieval_log.py:96` writes every artefact as `<sha16>.json` regardless of
content type:

```python
(d / f"{sha[:16]}.json").write_text(body, encoding="utf-8")
```

`check_json` (registry `:192`, battery `syntax`, **`kinds: [always]`, `level: blocking`**) parses
every `*.json` file in the repo. So retrieving an HTML full text, an XML stub, a Cloudflare
challenge page or an empty body produces a file that is invalid JSON with a `.json` extension,
and CI goes red. Proved on this branch: the first commit of real retrieval artefacts turned
`Syntax (UTF-8, JSON, YAML)` red at `047d3b7`, with 6 of 15 artefacts unparseable.

**This is a structural reason the project has never held a full text.** Every prior artefact was
Crossref metadata, which happens to be JSON, so the contradiction stayed invisible. The two
mechanisms the repository relies on — persist what you received, and validate what you committed —
are in direct conflict, and the conflict surfaces exactly when research starts working.

*Interim repair applied here (data only, no apparatus change):* each artefact was given its true
extension and `manifest.jsonl`'s `artefact` field updated to match. The `sha[:16]` stem is
unchanged, so every sha256 linkage still resolves, and `_logged_payloads()` already tolerates a
non-JSON artefact (it parses inside a `try`). `check_json` now passes with `EXAMINED: 144`.

*Real fix, Phase 5, ~3 lines:* sniff the body and choose the extension at write time. **Not done
here** — §9 forbid 1 bars apparatus changes before Phase 5, and §10's phase gate says unpredicted
apparatus is a finding, not a task. This is that finding, recorded rather than quietly built.

**0.7 — Corrections to rev 1's record.** `gap_mining_audit` is **not** NOTHING-IN-SCOPE: it
prints `EXAMINED: 4, PASS` with an actionable informational (4 OPEN gaps lack
`mining_addressability`). "Triggers zero of the 66 checks" is not literal — 9 registry entries
carry `kinds: [always]` and do run on the file; the fair claim is *unchecked for meaning*.
"B-before-E appears only in two comments" is false, and rev 1's own excuse is also false:
`.ignore` **deliberately does not hide `decisions/`**, so ripgrep-visible counterexamples existed
in `workplan/` and the DR. Line drift: `check: null` at `pipeline-contract.yaml:117`;
`def citation` at `spec_page.py:131`; single-axis error at `validate_evidence_state.py:328`;
registry is 1,655 lines; `.git` is 16 MB. Counts "68 dangling workplan refs" and "27 unmarked
quantified claims" are scope- and regex-dependent — independent re-derivations gave 52–72 and
18–29. **Phases 5 and 6 re-derive their own lists and never target rev 1's numbers.**

---

## 1. Two kinds of block

Unchanged from rev 1 and re-verified. **Class A resolves by doing research; Class B does not
resolve no matter how much research is done.** Confusing them is how apparatus became the work.

**Class A — empty because the content does not exist yet.** `specifications`,
`specification_source_links`, `convergence_assessment`, `bpc_metadata`,
`reasoning_doc_citations`, `spec_value_probes`, `source_value_extractions`, `gap_mining`,
`connections` — all 0 rows. `jurisdictional_values` 109 rows, 0 with a stored value. 93
`site/specs/*.html` reading "Best-practice determination: **not yet computed**". Five checks
reporting `EXAMINED: 0`.

> **`item_bpc_links` is removed from Class A by D-1 (§2c).** It is scaffolding, not an answer-side
> table, and its emptiness is not a content gap a determination fills. It is 0 rows and should
> **stay** 0 rows unless and until an item↔slug bridge is earned by evidence rather than asserted.
>
> **`reasoning_doc_citations` is Class A only in appearance.** Its `source_ref_id` is
> `NOT NULL REFERENCES evidence_sources(ref_id)`, so it cannot receive the one reasoning document
> that exists until that document's 11 cited sources are admitted — and they cannot be admitted
> while R9 is blind to `source_locators`. Its emptiness is **FK-blocked by OD-5**, which makes it a
> Class-B dependency wearing a Class-A face. See D-2.

**Rule: report as NOTHING-IN-SCOPE, never as a failure, and never build apparatus to observe it.
A vacuous check means content is missing, never that a check is missing.**

**Class B — genuine defects.** Carried forward from rev 1 §1 unchanged and re-verified: B1-a…f
(write-path gaps), B2-a…e (orphans and stale hardcoded facts), B3-a…e (blind spots), B4-a…d
(rendering edge), B5-a…e (provenance). Plus **B5-f** (§0.7, found during execution: every
retrieval artefact is written `.json` regardless of content type, so a blocking always-on gate
fails the moment a non-JSON payload is retrieved) and **B6-a**, new in rev 2: `assess_cell.py` returns
`stated` for a cell whose every anchoring source is down-weighted (§0.1).

---

## 2. Standing authorisations — and their evidentiary status

1. **Owner, 2026-08-20:** *"Permission to change CI, CLAUDE.md, skills, tools and anything else
   that are currently preventing required overhaul."*
2. **Owner, 2026-08-19:** `_archived/` may grow; it is the home for retired **content**. Git
   history remains the archive for **code**.
3. **Owner, 2026-08-20:** *"the scratchpad… needs to be getting saved always for provenance."*
4. **CLAUDE.md §1:** removal needs *evidence*, not permission; addition carries the burden of proof.

> **Flag (F20).** Quotes 1–3 appear **nowhere in the repository outside this plan**. They may well
> be genuine instructions given in chat, but they are unverifiable from the record while being
> load-bearing for every Class-B fix below. They are recorded here as *claimed* authorisations,
> not as evidence. Item 4 is verifiable and is the one doing real work.

**Still owner-gated and untouched:** the DG-NON class — mission, audience, CRPD posture,
population taxonomy, evidence-tier definitions, jurisdiction and work-product inclusion,
licensing, trajectory. And `.ignore` edits.

---

## 2b. The cull, executed 2026-08-20 — apparatus does not leave by being planned

`workplan/2026-08-18-cull-execution-plan.md:595` already authorised this, on 2026-08-18:
*"Archive outright (~5,000 LOC, no caller and no subject): `tests/probe_pipeline.py` (1,718) + …"*
It was still in the tree two days later. **A cull that becomes another document is the ratchet
in its purest form**, and it is the reason this plan's §9 forbid 1 alone cannot break the
recursion: refusing to add is only half of it.

Deleted, with evidence, per CLAUDE.md §1 (git history is the archive for CODE — deleted, not
copied to `_archived/`):

| File | LOC | Evidence |
|---|---|---|
| `scripts/tests/probe_pipeline.py` | 1,718 | unregistered; no caller in `scripts/`, `tools/`, `.github/` or the registry; last touched 2026-08-12; already authorised for removal on 2026-08-18 |
| `scripts/probes/citation_mining_pipeline.py` | 254 | **zero** references anywhere in the repo; last touched 2026-07-25, before the 2026-08-06 clean-room evidence reset; superseded by the live path (`citation_mining_completeness.py`, `research_batch_dod.py`, `db.py log-mining`). Its directory `scripts/probes/` held nothing else and is gone |

**1,972 LOC removed. Callers swept** (`governance/context-map.yaml`'s `probe_pipeline` block);
both YAMLs still parse; the registry still resolves 66 checks.

**Consequence worth recording: nothing reads `source_locators` at all any more.** `probe_pipeline.py`
was the last live script that touched it, and it never ran. The 835 held identifiers are now
formally unread by any executable surface — which sharpens OD-5 rather than softening it, and
should be stated that way rather than discovered again later.

### The rest of the cull, executed the same day — 6,716 LOC

The owner directed the 2026-08-18 plan be performed **in its entirety**. Its §15.2 (DELETE 13
registry entries) and §15.3 (archive outright ~5,000 LOC) were then executed.

**What the census found on contact: the cull had already been half-done, in the worse direction.**
Twelve of the thirteen §15.2 registry entries were *already gone* — and every script they invoked
was still on disk. Deregistering a check and leaving its code is the same accretion in a quieter
form: the apparatus stops being watched but does not stop existing. A further 3,612 LOC sat in a
16-entry `quarantine` section, every file present.

**Deleted: 21 files, 4,744 LOC** — `walk_harness.py` (closing D4) · `item_audit_pipeline.py` ·
`verify_resolved_dois.py` · `generate_search_queries.py` · `generate_alias_chart.py` ·
`check_phase_a_complete.py` · `validate_commits.py` · `validate_item.py` · `validate_conflict.py` ·
`validate_conflicts.py` · `validate_temporal.py` · `validate_audit_runs.py` ·
`contamination_sampler.py` · `table_connectivity.py` · `schema_reference_drift_audit.py` ·
`jurisdictional_divergence.py` + its wrapper test · `full_db_metadata_verification.py` ·
`workplan_naming_audit.py` · `migrate/migrate_decisions.py` + `_legacy_guard.py` (closing D2).
With the earlier pass: **6,716 LOC and 23 files.**

**Registry: 66 → 63 checks; quarantine 16 → 4.** Fifteen entries removed. Zero registry entries
now point at a missing file.

**Kept deliberately:** `adjudication_integrity.py` — quarantined, but its wrapper
`test_adjudication_integrity` is a *live registered check*, so the code is reachable. `code_currency_audit.py`
and `pre_rehab_banner_audit.py` — quarantined but not named for deletion by §15.2; deleting
unnamed things because they sit nearby is how a cull becomes a purge. `generate_parts.py` — a
call-graph orphan that assembles the actual deliverable, which §15.3 flags must **never** be culled.

**The sweep, which is where the real work was** (CLAUDE.md §0.4 — *"a sweep that stops at the
filename is not a sweep"*):

- `pipeline_contract_audit.py`'s selftest fixture named `validate_conflicts.py` and began
  reporting BROKEN instead of QUARANTINED. **This is the second time that one fixture has been
  broken by a change to its subject**, and its own comment records the first. Re-pointed, with a
  note: if it breaks a third time, derive the path from the registry instead — the hardcoded name
  is the defect.
- `graph/extract_code.py` excluded `schema_reference_drift_audit.py` by name and documented itself
  as *complementing* it. It **supersedes** it; corrected, and the dead exclusion removed.
- `doctrine_recheck.py` instructed the reader to run a sampler that no longer exists.
- `alias_provenance_audit.py`, `validate_pydantic_schemas.py`, two skills, `time-model.md` §6 and
  `doctrine-recheck.md` §7 all swept. The two governance sections are kept as *specifications* with
  a banner saying the code is gone — deleting the spec would have destroyed the design record.

**A method error of my own, corrected:** I hand-edited `governance/context-map.yaml`, which is
**generated output** (CLAUDE.md §7). Regenerating it dropped 52 lines and swept every dead
reference automatically — which is precisely why hand-editing it was wrong.

**Verification.** `preflight.sh` **PASS**, 27 green (was 25 before the cull). `run_checks --selftest`
PASS. `graph_audit` PASS, EXAMINED 821. `test_pipeline_contract` restored to PASS. The two
remaining advisory failures — `retired_vocabulary` (65 occurrences) and `test_verification_pipeline`
(14/18) — were measured **identical on `origin/main`** in a worktree and are pre-existing debt, not
this cull's. Canonical DB sha256 unchanged.

**Four candidates were investigated and NOT culled**, recorded so the work is not repeated:
`validate_commits.py`, `full_db_metadata_verification.py` and `test_adjudication_integrity.py` are
all **registered checks**; `scripts/audit/graph/__init__.py` is a live package marker. An initial
census flagged all four as orphans and was wrong — the registry parse missed them. **The caller
sweep is what caught it**, which is exactly the failure §0 rule 4 of CLAUDE.md exists to prevent.

Also investigated and **rejected**: culling `scripts/assess/assess_cell.py` and the pilot
apparatus. It looked like the strongest candidate — §0.1 proves the engine returns a wrong
determination — but `governance/evidence-architecture.md` is **CANONICAL, ratified 2026-07-13**,
and `scripts/generate/pilot_renderings.py` is the single source of truth for `REGISTER_MAP`,
`ROLES` and `tuple_class`, imported by the live `register_integrity_check.py`. Deleting it would
have destroyed a ratified doctrine's only implementation. **Evidence governs deletion in both
directions.**

---

## 2c. Owner directives, 2026-08-21 — three standing rules

Recorded verbatim in substance because each changes what this plan may do, and one of them
invalidates part of it. **All three are doctrine (the DG-NON class) and should be lifted into a DR;
a workplan is the wrong home for a standing rule.** Flagged for the owner.

### D-1. Scaffolding is research-support only. It must not cross into any other stage.

*Owner:* *"scaffolding is to strictly be used in support of conducting research… I do not want any
links, maps, etc from scaffolding to be imported into any other stage due to contamination. Instead,
I want these quarantined and digested into slugs/sources to read/research leads."*

**Measured warrant of the scaffolding, 2026-08-21 — the directive is evidenced, not precautionary:**

| Table | Rows | Evidence borne |
|---|---|---|
| `item_population_links` | 372 | `rationale_ref` **NULL on all 372** |
| `item_axis_links` | 158 | `source` populated 158/158, but its content is authorship provenance (*"E3 harvest from item function + FDA audit-briefs"*), not citation |
| `population_axis_map` | 53 | **no evidence-bearing column exists in the schema** |

**Zero REF-ids appear in any scaffolding rationale or source column.** These 583 rows are
judgement-seeded mappings from 2026-05-11, 2026-07-21 and 2026-07-24 sessions carrying no
evidential warrant.

**This is a change, not a confirmation.** The scaffolding is currently wired into downstream stages:
`item_bpc_links` and `item_population_links` are read by `scripts/generate/build_site.py` and
`scripts/generate/spec_page.py` (render); `scripts/assess/assess_cell.py` reads `item_bpc_links`,
`slugs` and `axes` (determination). **§4.4 of this plan instructed writing `item_bpc_links` as part
of the walk, and §4.6's sideways walk traverses `item_axis_links` → `population_axis_map`. Both are
withdrawn.** Nothing has been contaminated yet only because the answer side is 0 rows — no import
has occurred. The directive arrived before the damage.

**Operative rule.** Scaffolding may orient a search and nominate what to read. It may not supply,
imply or stand in for an evidential link in `specifications`, `specification_source_links`,
`convergence_assessment`, or any rendered determination. Where it suggests a relationship, that
relationship is digested into a slug or a source as a **read/research lead** — the treatment
`source_locators` already receives — and must be earned by admission before it carries weight.

### D-2. Prose is a supplement, never the body of reasoning.

*Owner:* *"prose should only be a supplement if it is ever used, never as the body which contains
our reasoning itself because it means that our research and reasoning isn't being ingested by
relevant tables."*

Correct, and the schema already agrees: **`reasoning_doc_citations`** exists for exactly this —
`claim_type`, `claimed_value`, `source_ref_id`, `value_match`, `claim_match`, and fourteen locator
columns for clause-level citation. It holds **0 rows** and has never been written to, while a
registered audit watches it and reports `EXAMINED: 0`.

**The structural reason, which closes a loop.** `source_ref_id` is
`NOT NULL REFERENCES evidence_sources(ref_id)`. The reasoning doc's claims therefore **cannot be
filed** until its 11 cited sources are admitted — and they cannot be admitted because the R9 gate
cannot see `source_locators`, where all 11 sit. Two of those 11 are the OD-5 witnesses themselves
(REF-00561 `10.3390/app11093942`; REF-00578 `10.1044/2016_AJA-15-0064`). The prose is not
un-ingested through indiscipline; the ingestion path is FK-blocked by the exact defect OD-5 names.
**OD-5 unblocks D-2.**

### D-3. Blocking-and-vacuous is three different conditions, not one.

The five blocking gates reporting `EXAMINED: 0` do so for three distinct reasons, per the registry's
own `no_floor` notes. **Blocking is a configured level; it is not caused by absence of data.**

| Check | Why it examines nothing | Will data alone fix it? |
|---|---|---|
| `validate_evidence_state` | corpus emptied by decision | **yes** |
| `validate_verification_consistency` | corpus emptied by decision | **yes** |
| `attestation_presence` | changeset-scoped to `HEAD~1..HEAD`, **not** the 79 attestations on disk | no |
| `attestation_schema` | changeset-scoped; 0 means this commit changed none | no |
| `check_rendered_docs` | `--all` deliberately declines the 1 document present (REFERENCE-only since the 2026-08-06 reset) | no |

The two attestation gates would read 0 on a fully populated project whenever a commit touches no
synthesis path. Do not treat "vacuous" as a single condition, and do not expect content alone to
retire all five.

---

## 3. Definitions — so the acceptance test cannot be passed by wording

- **"The batch"** = the commits of one R1–R15 admission-to-determination walk. Phases A and 5–7
  are **apparatus commits, explicitly outside the batch**.
- **"Zero apparatus"** means **no script, check, or registry entry added *or modified*** — with
  exactly one named exception, the Phase A hook. Editing `PILOT_CELLS` or `TABLES` to squeak past
  the word "new" is forbidden by name.
- **Whole-plan apparatus ceiling:** ≤ 80 LOC (Phase A) + ~24 (Phase 5.2/5.3) + ~15 lines
  (Phase 6) + 300 LOC (Phase 7) = **~420 LOC net**, across the entire plan. Anything over is not
  built; it is done by hand and the hand-SQL is saved to the scratchpad.

---

## 4. Phase A → Phase 1. The walk, as one phase

**Preconditions.**
- **P1. `pip3 install "pydantic==2.13.3"`.** pydantic is **absent** from this container though
  `requirements.txt` pins it. Without it `validate_evidence_state.py`, `assess_cell.py` and the
  registered `test_assess_cell_pilot` all crash on import and preflight cannot go green.
  **Do not run `pip3 install -r requirements.txt`** — it fails, because PyYAML 6.0.3 cannot
  uninstall the Debian-managed 6.0.1. Install pydantic alone.
- **P2.** Clean tree on the work branch; `origin/main` fetched.
- **P3.** `sha256sum data/guidebook.db` = `ebab426f…8c692b`; census 5/5/12 and the four answer-side
  tables at 0.
- **P4.** `S=session_2026-08-20-provenance-walk` — **bare stem** in the DB, `.md` only in pointer
  files and `emit_data_migration --session`. `SCRATCH` derived from the live scratchpad path at
  runtime. **Never hardcode a session UUID** — rev 1 did, and it was a dead path.
- **P5.** `python3 scripts/audit/research_batch_dod.py --selftest` → 15/15.

### Phase A — the scratchpad hook, first — LANDED 2026-08-20

**Provenance is not only about citations. It governs tier grading too.** A tier is a
*judgement*; a judgement with no recorded derivation is an assertion. `co1_provenance` and
`co1_source_type` are NULL on all three Co-1-tiered rows, so the project's strongest evidential
claim — CRPD Art 4.3 co-primacy — currently rests on nothing a reader can audit. That is the same
defect class as a bibliographic field written from memory, one level up. **No tier is graded or
re-graded in this project without its warrant recorded in the row and its derivation in the
scratchpad.**

### Phase A — the scratchpad hook, first

Rev 1 scheduled this *after* the acts it exists to make reproducible, quoting its own reasoning
that without it the determination is "as auditable as the author lists were on 2026-08-19."
It goes first.

A `PostToolUse` hook in `.claude/settings.json` appends one JSON line per Bash invocation
(`ts, cwd, command, exit_code, stdout_sha256, bytes`) to a committed `scratchpad/<session>/
commands.jsonl`, plus a `record` subcommand on the existing `scripts/research/retrieval_log.py`
for manifest-shaped artefact lines. **≤80 LOC, no new file, no registry entry.** This is the
plan's one named apparatus exception (§3).

*What wrong thing reaches the guidebook without it:* an unreproducible determination.

### 4.1 Retrieve, and log every attempt including the refusals

`retrieval_log.py` has **no fetch subcommand** — its CLI is `--session` plus one of
`--verify-authors` | `--backfill`. Retrieval is the importable API `fetch(url, session, purpose)`,
which writes the artefact and its manifest line *before* returning. **`fetch()` decodes as text —
never put a binary PDF through it.** Use HTML/JSON/XML routes only.

A 403 is still persisted with its exit code. **That artefact is the recorded refusal** and is what
makes degraded mode auditable rather than asserted.

Retrieve: the PMC full text for REF-00966; the full-text *attempts* for REF-00965 and REF-00968;
and OpenAlex/EPMC/DOAJ corroboration for all three.

**Check before proceeding:** the PMC artefact is ≥200 KB and contains a real Methods section. Any
source whose artefact is a challenge page (~5 KB) or coredata stub (~2 KB) is **degraded**.

### 4.2 Backfill the bibliography from payloads on disk

`volume` and `issue` are NULL on all five rows while **the held Crossref payloads already carry
them** (92c0026c → vol 233; 514f77d5 → vol 5 iss 4 pp 411-422; 81980e4f → vol 12 iss 1), and
Europe PMC and OpenAlex corroborate independently. `co1_source_type` is NULL on all three Co-1
sources.

Read the values off the payloads. **Never write a bibliographic field from memory when a payload
is in hand.** REF-00965 has no issue number — do not invent one.

### 4.3 Author the determination

> **HALTED 2026-08-20. The determination was not authored, and must not be until §8 of
> `workplan/2026-08-20-adversarial-adjudication-a18-aut.md` is worked.** The agonist/antagonist
> pass refuted the determination's core claim before it was written: on-parameter,
> population-justified reverberation criteria for learning spaces **exist** and the batch's nine
> searches did not reach them — not one paired a reverberation term with a learning-space term and
> a neurodivergent population. One of the missed sources, **REF-00561** (`10.3390/app11093942`,
> "Indoor Acoustic Requirements for Autism-Friendly Spaces"), has been held in `source_locators`
> since 2026-08-06, invisible to the R9 gate. That is OD-5's **second** witness. Authoring "the
> evidence distinguishes neither" on this search frame would have rendered a coverage failure as
> an epistemic finding. The steps below stand; their input does not yet exist.



**This is the only act in the plan that apparatus cannot perform**, and §0.1 sharpens why: the
engine *can* compute a state mechanically, and what it computes is wrong. The judgment is the work.

1. **Read REF-00966 in full.** Read REF-00965 and REF-00968 from abstract + payload, and **mark
   each as degraded, per source, in `confidence_dimensions_absent` and in the determination
   prose.** Degraded mode is declared, never silent.
2. **State the requirement class**, not a value. Whether the AUT requirement is a *level* (a lower
   RT60 figure) or a *class* (control and predictability). "The evidence distinguishes neither" is
   an acceptable determination **provided** the falsification condition names the discriminating
   evidence. A fabricated resolution is not.
3. **Author no value.** `value_min`/`value_max`/`value_unit` stay NULL. No admitted source supports
   a population-differentiated RT60 threshold for AUT.
4. **Carry the guard forward:** *"That is a real finding about what disabled people report. It is
   not a finding that rooms need less acoustic treatment."* Restoration is not silence.
5. **Preserve Co-1 attribution.** REF-00966's community co-authors — **Catherine Woolley** and
   **Emily ("@21andsensory"**, whom Crossref renders `family:"andsensory", given:"Emily"`) — were
   deleted once already. They appear in the attribution or the determination is not authored.

**Honest statement of what this teaches.** The batch's existing answer is already "NOT SETTLED,
and my first answer was wrong." Converting that into rows and a rendered page is a **pipeline
proof, not a research result.** It satisfies §4 of the instrument, and it should be claimed as
exactly that and nothing more.

### 4.4 Write to scratch, by hand

`convergence_assessment(1)`: `status='single_axis'`; **only** `co1_sources` populated — the
validator errors if more than one of clinical/co1/co2 is non-empty; `down_weighted_sources` =
`["REF-00607"]` (PROXY, MB1-008); `discounted_sources` = `["REF-00967"]` (AUT MISMATCH, MB1-007);
rationale names the axis *and* the chain-of-one lineage.

`specifications(1)`: `state='provisional'` — forced by DR §7 and by the evidence (single axis,
chain-dependent, no regulatory baseline). Requires non-empty `confidence_synthesis_basis` and
**genuinely valid JSON arrays** in both confidence-dimension columns. `design_scale='population'`,
`tier_basis='Co-1'`, `governing_refs` = the three Co-1 refs, all four flags 0.

Then `specification_source_links` (three `governing` rows).

> **`item_bpc_links` is NOT written — withdrawn by D-1 (§2c).** It is scaffolding: an
> item↔slug bridge carrying no evidential warrant. Writing it as part of a determination would
> import an unevidenced mapping into the answer side, which is exactly the contamination D-1
> forbids. The cell's link to its evidence runs through `specification_source_links` alone.

`specification_id=1`/`convergence_id=1` collide with nothing — both tables are empty, and
`assess_cell.py`'s `CELL_ID_BASE 9000` reserves a disjoint range. **No `BEGIN;`/`COMMIT;`
wrapper** — the migration runner owns the transaction.

### 4.5 Emit, apply, verify

Hand SQL → `emit_data_migration.py --input` → `migrate_db.py` → `migrate_db.py --rebuild`.
`emit_batch_sql.py` is **not** used (§0.2). The canonical sha256 is captured before and must not
move until `migrate_db.py` runs; after it, it must differ. Canonical is append-only: a wrong
migration is fixed **forward** with a compensating migration, never by hand-reverting the blob.

### 4.6 Render, and walk it in three directions

`build_site.py --only A-18` (writes `site/specs/a-18.html`), then `regenerate_derived.sh`.

- **FORWARD** payload → manifest → REF-00965 → RAP-01 → MB1-001 (AUT, EXACT) →
  `specification_source_links(1)` → `specifications(1)` → `site/specs/a-18.html`.
- **BACKWARD** page → cell → links → REF-00965/966/968 → `search_admissions` **exec 1 (965, 966)
  and exec 6 (968)** → two query texts → three artefacts → three DOIs.
- **SIDEWAYS — withdrawn by D-1 (§2c).** The former hop traversed `item_axis_links` →
  `population_axis_map`, both scaffolding with zero REF-ids in any rationale or source column. A
  walk that resolves through them would present an unevidenced mapping as pipeline provenance.
  Scaffolding may still *orient* the next search; it may not appear as a hop in a provenance walk.
  GAP-B01-002 (DEM) and GAP-B01-003 (MH, BRAIN) are named as still OPEN from the `gaps` table
  directly.

Transcript into `scratchpad/<session>/notes.md`, every hop resolving to a real row or file.

### 4.7 Acceptance

1. `grep -c 'REF-00965' site/specs/a-18.html` ≥ 1.
2. Walk transcript exists, all three directions, both exec ids, DEM hop correct.
3. `preflight.sh` exit 0 **and** `validate_evidence_state.py` prints **`EXAMINED: 2`** (one cell +
   one convergence row — rev 1 said 1).
4. `git diff --stat` shows **zero files added or modified under `scripts/`** and zero registry
   entries, except the Phase A hook commit.
5. Every degraded source is named as degraded, per source, in the rendered output.

**Known non-zero exits, expected and recorded, not "fixed":**
`research_batch_dod.py --session "$S"` → **exit 1, R1 only** (this session runs no Co-1 searches).
Either record the expectation or omit the command. `gap_mining_audit` → PASS with an
informational.

**Pointers:** update `sessions/LATEST`. **Do not update `sessions/LATEST-RESEARCH`** — this
session admits nothing. Touching `sessions/` triggers the rule-2 attestation.

---

## 5–7. After the walk

Carried from rev 1, re-ordered behind the walk and unchanged in substance.

**Phase 5 — provenance.** Widen `verify_authors()` beyond the ordered surname sequence to the
fields the payloads already hold (title, year, journal, volume, issue, pages, given names) —
proven necessary: REF-00966's payload carries vol 5 iss 4, the DB stores NULL, the verifier prints
CLEAN. Rename its result to `CLEAN (authors only)` until it lands. Emit `BACKFILL: n` beside
`EXAMINED: n`. Pure-data backfill of `evidence_population_match.gap_id` (12 NULL),
`slugs.serves_axes`, `search_executions.terms_used` (0 of 9). **~24 LOC.**

**Phase 6 — the rendering edge.** B4-a `regenerate_derived.sh` calls `build_site.py` and
`generate_parts.py` (+2). B4-b `spec_page.py` SELECT gains `doi, url`; `citation()` renders a
chaseable link (+3). B4-d map `references/search-log/**` and `retrieval-log/**` to an **advisory**
kind (+2). B2-b the dangling `#bibliography` anchor. B2-c `parts/v10/part13.md:12`'s hardcoded
"0 sources". B2-d the stale `no_floor` annotations. B2-e the dangling workplan refs — **re-derive
the list; do not target rev 1's "68".**

**Phase 7 — the write path, capped at 300 LOC inside `scripts/db.py`, zero new files.** Ordered by
damage caused: `add-authors` (the fabrication vector), `next-ref-id` (allocate above the
`source_locators` high-water REF-00964, not above `evidence_sources`), widen `_ES_COLS`,
`finish-search`, `add-match`. **`add-cell` is deferred pending §8.1.**

**Phase 8 — the next batch, aimed.** OD-5 first (the R9 gate is blind to 835 held identifiers);
then GAP-B01-003 (closes on two well-formed logged absences, zero admissions needed); then
GAP-B01-002 (DEM — 8 of 13 items, nothing above PROXY: the population weighted heaviest is served
worst); then the 11 orphan citations in `references/bpc-reasoning/room-acoustic-performance.md`
(0 of 11 resolve); then the unmarked quantified claims in `source_locators.standard_number` —
**re-derive that list too.**

---

## 8. Two frictions with the operative instrument, recorded not finessed

**8.1 — DR §12.5 says `specifications` is permanently manual.** Verbatim: *"**Permanently
manual:** … **anything touching `specifications` or the reasoning doc**, which sits at the Opus
synthesis floor behind the B-before-E gate. The contract's premise is that these are judgment acts
machinery can only *check*."* A `db.py add-cell` is machinery touching `specifications`. A
defensible counter-reading exists — the clause protects *judgment*, not the *transport* of a
judgment already made — but it must be argued and signed, not assumed. **`add-cell` is therefore
deferred out of Phase 7 pending a one-line DR amendment.** §0.1 strengthens the DR's side of this:
the one engine that automated the judgment got it wrong.

**8.2 — This document should not exist.** DR §11 property 5 permits only search logs, migrations,
the §3 fixes, the record-correction PR, or the rendered determination as successor artifacts. A
workplan is none of those. Rev 1 sheltered under "workplan is the rule-free class," which cites a
cost table, not a permission. **This is a real breach of the instrument's termination property,
owned here rather than argued away.** It is why §9 retires this file by deletion.

---

## 9. What this plan forbids

1. **No apparatus added *or modified*** before Phase 5 — the Phase A hook excepted by name.
   Editing `PILOT_CELLS` or `TABLES` to pass on the word "new" is forbidden.
2. **No apparatus built to observe a Class-A emptiness.**
3. **No bibliographic field written from memory when a payload is in hand.**
4. **No value authored without a locator.** `value_min`/`value_max` stay NULL; unlocated
   quantified claims carry `[UNVERIFIED-QUANT]`.
5. **No `stated` cell in the walk phase.** Single-axis, chain-dependent Co-1 evidence with no
   regulatory baseline caps at `provisional`. *The engine disagrees; the engine is wrong (§0.1).*
6. **No writing to `data/guidebook.db` directly.** Scratch → `emit_data_migration.py` →
   `migrate_db.py`. Append-only; fix forward.
7. **No deleting or backfilling an empty search.** A zero-yield search is a completed unit of work.
8. **No silent degraded mode.** A source read from an abstract is named as such, per source, in the
   rendered output.

---

## 10. Acceptance and termination

The plan's own test — the recursion is broken when:

1. A §4-satisfying artifact exists: a determination, rendered as the answer.
2. **Zero apparatus added or modified in the batch's commits** (§3's definition, not a wording).
3. At least one GAP-B01 gap closed by its own falsification condition.
4. The first pass survives its adversarial pass without headline retractions.
5. The session record ends by naming the next **research question**, not the next governance act.

Condition 5 is the one this plan is most likely to fail, and it is checked last on purpose.
Condition 4 is executed per DR §7 — **blind-then-compare across lenses L1–L8, no third judge**;
sustained findings are corrected by migration in the same pass, disputed ones cap the cell at
`provisional` with the dispute recorded, doctrine-level ones go to the owner.

**Phase gate.** If any phase requires apparatus that phase did not predict, **stop and record why
— that is a finding about the pipeline, not a task.** Rev 1 tripped this gate three times before
execution began, which is what §0 is.

**This document retires itself.** When the five conditions hold it is deleted — not archived to
`_archived/`, since §8.2 concedes it should not have existed. The next artifact is a search log.
