# S5 — RENDER STAGE smoke test log
2026-08-25

Baseline `git status --short` (pre-existing, NOT mine, left untouched throughout):
```
 M scratchpad/session_2026-08-23-research-batch-03-forward-mining/commands.jsonl
 M sessions/LATEST
?? scratchpad/session_2026-08-25-pipeline-smoke-test-mobility/
?? sessions/session_2026-08-25-pipeline-smoke-test-mobility.md
```
`git stash list`: empty throughout.
DB sha256 at start: `30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf`
DB sha256 at end:   `30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf` (unchanged — matches PROTOCOL's expected `30a10669...`)
Scratch DB: `$SMOKE/s5-render.db` (copy of canonical; unused for writes — every generator either took a `--out` redirect into `$SMOKE/render-out/` or, having no redirect flag, was run once and its output was byte-compared to `git show HEAD:<path>` before deciding whether a restore was needed).

---

## 1. Inventory of the render surface

```
parts/        -> 88_to_90/ (_MOVED.md stub), _archived/ (_MOVED.md stub), deprecated/ (_MOVED.md stub), v10/ (manifest.md + part00..part13.md, 15 files)
site/         -> assets/, index.html(15461B), populations/ (6 files), rooms/ (17 files), specs/ (93 files)
tools/        -> README.md, evidentiary-audit-dashboard.html, evidentiary_audit.py,
                 pipeline-completeness-dashboard.html, pipeline_completeness.py,
                 regenerate_vetting_surface.py, spec-curation-vetting-surface.html
audits/       -> 15 files (json/md/csv), _archived/
```

`scripts/regenerate_derived.sh` **EXISTS** (CLAUDE.md §7's "don't hand-edit generated output" trap names it correctly — no ABSENT finding here). Read in full:

```
15  python3 tools/pipeline_completeness.py
16  python3 tools/evidentiary_audit.py
17  python3 tools/regenerate_vetting_surface.py
19  # then --check on the first two
```

**FINDING: `regenerate_derived.sh` drives only 3 of the ~11 render generators named in my brief.** It never calls `scripts/generate_parts.py`, `scripts/generate/build_site.py`, `scripts/generate/spec_page.py`, `scripts/generate/room_page.py`, `scripts/generate/population_page.py`, `scripts/generate/pilot_renderings.py`, `scripts/generate/context_map.py`, or `scripts/generate/research_contract_hook.py`. This is the mechanical root of finding (5) below: "the single sanctioned regeneration entry point" (its own header comment, line 7) does not regenerate `parts/` or `site/` at all.

---

## 2-4. Per-generator / per-gate runs

### 1. `scripts/regenerate_derived.sh` (read only, not executed as a whole — its 3 sub-tools run individually below to control blast radius)
STAGE: render
FINDING: see per-tool entries 2-4 below.

### 2. `tools/pipeline_completeness.py` (writer, then `--check`)
INVOKED   : `python3 tools/pipeline_completeness.py` ; `python3 tools/pipeline_completeness.py --check`
STAGE     : render
EXIT      : 0 / 0   RUNTIME: <1s each
READS     : `data/guidebook.db` (items, evidence_sources, specifications, gaps, search_candidates, bpc_metadata, terms, populations, connections, conflicts, convergence_assessment — many unrelated scalar tables), `governance/pipeline-contract.yaml` (via `gather_enforcement`, for per-stage verifiable/incomplete criterion counts)
WRITES    : `tools/pipeline-completeness-dashboard.html` (default path) — confirmed byte-identical to committed (`git status --short` clean after the writer ran)
EXAMINED  : dashboard is a multi-metric aggregate, not a single-corpus scan (registry's own `no_floor` note, check-registry.yaml:1284-1289) — no single EXAMINED count printed by the writer; `--check` printed `OK: pipeline-completeness-dashboard.html is current.`
OUTPUT    : `Wrote .../pipeline-completeness-dashboard.html — data as-of 2026-08-23 · 0/372 cells determined · 0/0 slugs synthesized.`
FINDING   : PASS (fresh, deterministic — no `datetime.now()`/`strftime` call anywhere in the file, grepped)
LOCATION  : n/a
NOTE      : Confirms `specifications` (0 rows) drives "0/372 cells determined" — the dashboard is telling the truth about the mobility batch's absence.

### 3. `tools/evidentiary_audit.py` (writer, then `--check`)
INVOKED   : `python3 tools/evidentiary_audit.py` ; `python3 tools/evidentiary_audit.py --check`
STAGE     : render
EXIT      : 0 / 0
READS     : `data/guidebook.db` (evidence base per ACTIVE slug), writes into `audits/` and `tools/`
WRITES    : `audits/evidentiary-base-audit.{md,json,csv}` + item variant, `tools/evidentiary-audit-dashboard.html` — byte-identical to committed
EXAMINED  : 80 (one row per ACTIVE slug walked by `compute()`) — printed verbatim: `EXAMINED: 80`
OUTPUT    : `OK: all audit outputs are up to date.` / `EXAMINED: 80`
FINDING   : PASS — and this **contradicts a stale note in the registry itself**, see §5/§8 finding below.
LOCATION  : `governance/check-registry.yaml:1303` claims "STALE on main as of 2026-08-01"; measured 2026-08-25 it is current.
NOTE      : The registry's own freshness-check documentation has itself drifted (§2(b) applies recursively to the governance files, not just index.html/parts/).

### 4. `tools/regenerate_vetting_surface.py`
INVOKED   : `python3 tools/regenerate_vetting_surface.py`
STAGE     : render
EXIT      : 0
READS     : `data/guidebook.db`
WRITES    : `tools/spec-curation-vetting-surface.html` — byte-identical to committed
EXAMINED  : not separately printed by this tool; `git status --short` clean post-run is the freshness proof
FINDING   : PASS
NOTE      : This is the ONE render surface `regenerate_derived.sh` actually keeps current (matches contract note "only the vetting surface auto-regenerates").

### 5. `scripts/generate/spec_page.py E-08` and `E-03` (the mobility question, part 1)
INVOKED   : `python3 scripts/generate/spec_page.py E-08` ; `python3 scripts/generate/spec_page.py E-03`
STAGE     : render
EXIT      : 0 / 0   RUNTIME: <1s each
READS     : `data/guidebook.db` — `items`, `item_population_links`, `item_bpc_links`, `bpc_metadata`, `specifications` (WHERE item_code=E-08/E-03 — 0 rows both)
WRITES    : `site/specs/e-08.html`, `site/specs/e-03.html` — **byte-identical to `git show HEAD:<path>`** (`cmp` clean both). Script printed "5811 bytes"/"4722 bytes" but the files on disk are 5819/4734 bytes — this is the script's own `len(str)` (Unicode codepoints: ≥/≤ in item names) vs on-disk UTF-8 byte count, not a content diff. No restore needed — nothing was dirtied.
EXAMINED  : 1 item each
OUTPUT    : `site/specs/e-08.html:81` — `item_bpc_links (the intended many-to-many bridge, migration 013) has no row for this item yet`; `:87` — `No Progressive Measurement Probe walk recorded for this item.`; `:92` (and `e-03.html:83`) — `<p class="honest-banner">Best-practice determination: <strong>not yet computed</strong> for this item, for any population. See workplan/best-practices-assessment-system.md.</p>`
FINDING   : PASS — the page renders honestly. No fabricated content, no silent empty section (matches CLAUDE.md's "honesty requirement" cited in the script's own docstring).
LOCATION  : `site/specs/e-08.html:92`, `site/specs/e-03.html:83`
NOTE      : **This is what a reader sees today for E-08/E-03: an honest "not yet computed" banner.** Confirms `specifications=0` is correctly propagated end-to-end rather than papered over.

### 6. `scripts/generate/build_site.py --check`
INVOKED   : `python3 scripts/generate/build_site.py --check`
STAGE     : render
EXIT      : 0
READS     : `items` (93 rows) — the driver's own docstring is explicit: it drives `site/specs/` only, not `site/populations/` or `site/rooms/`
WRITES    : NONE (`--check` only)
EXAMINED  : 93 — printed verbatim `EXAMINED: 93`
OUTPUT    : `FRESH: 93 page(s) match a fresh render.`
FINDING   : PASS
NOTE      : `site/specs/` (93/93 pages) is the one static-page family with a *complete* fresh/stale proof, deterministic, and currently green.

### 7. `scripts/generate/population_page.py MOB`
INVOKED   : `python3 scripts/generate/population_page.py MOB`
STAGE     : render
EXIT      : 0
READS     : `populations`, `item_population_links`, `items`, `bpc_metadata`, `specifications` WHERE population=MOB
WRITES    : `site/populations/mob.html` — byte-identical to committed (cmp-equivalent: `git status --short` stayed clean)
EXAMINED  : 1 population
FINDING   : PASS (fresh)
LOCATION  : n/a
NOTE      : Mobility's own population page is not stale, but has no dedicated `_fresh` gate in the registry (see §5).

### 8. `scripts/generate/room_page.py R_COR`
INVOKED   : `python3 scripts/generate/room_page.py R_COR`
STAGE     : render
EXIT      : 1 (uncaught `sqlite3.OperationalError`)
READS     : attempts `SELECT * FROM room WHERE room_id = ?` — table **`room` does not exist**
WRITES    : NONE — crashed before writing
EXAMINED  : 0 — crashed, no subject reached
OUTPUT    :
```
scripts/generate/room_page.py:26: sqlite3.OperationalError: no such table: room
```
FINDING   : FAIL (script is broken against the live schema)
LOCATION  : `scripts/generate/room_page.py:26` and `:29` — both query `FROM room` (singular). Live schema has `rooms` (plural) and `room_items`, confirmed via `sqlite_master`.
NOTE      : `build_site.py`'s own docstring (line 7-8) already flags this generator as broken, but is itself imprecise about *why*: it says "no `rooms` table" when a `rooms` table does exist — the actual defect is the script querying the wrong (singular) name. The 17 committed `site/rooms/*.html` files therefore have **no working regenerator today** — any drift in `rooms`/`room_items` from what those 17 files show is silently unrecoverable by the sanctioned tool.

### 9. `scripts/generate/pilot_renderings.py` (has `--out`, redirected to scratch)
INVOKED   : `python3 scripts/generate/pilot_renderings.py --db data/guidebook.db --out $SMOKE/render-out/pilot.html`
STAGE     : render
EXIT      : 0   RUNTIME: 0.04s
READS     : `data/guidebook.db` (cell/register tuples)
WRITES    : `$SMOKE/render-out/pilot.html` only (984 bytes) — **no tracked file touched**, redirect flag used per PROTOCOL preference order
EXAMINED  : 0
OUTPUT    : `0 cells rendered × 6 roles -> .../pilot.html`
FINDING   : VACUOUS (correctly so — `specifications`/convergence_assessment empty)
NOTE      : `register_integrity_check.py` imports `REGISTER_MAP`/`tuple_class` from this file's *fixtures*, not from this empty live output, which is why its `--selftest` still fires meaningfully (entry 14 below) despite this being 0 cells.

### 10. `scripts/generate_parts.py --mode full` (mobility question, part 2 — the refusal)
INVOKED   : `python3 scripts/generate_parts.py --mode full --out $SMOKE/render-out/parts_full`
STAGE     : render
EXIT      : 3
READS     : `specifications` (0 rows) — gate check only, refuses before further reads
WRITES    : NONE — redirected `--out` target was never created
EXAMINED  : 0 — refused before examining
OUTPUT    :
```
full mode refused — gate not met:
  - specifications is empty (no synthesised cells; Phase E / 4.3)
Use --mode stub to render current state.
```
FINDING   : PASS (a REFUSAL, and a working one — this is the generator correctly declining to synthesize a full guidebook part out of zero judgment/synthesis rows)
NOTE      : Directly answers the mobility question below.

### 11. `scripts/generate_parts.py --mode stub` (redirected)
INVOKED   : `python3 scripts/generate_parts.py --mode stub --out $SMOKE/render-out/parts_stub`
STAGE     : render
EXIT      : 0
READS     : `items`(93), `populations`(23), `bpc_metadata`(0), slugs(106), connections(0), conflicts(0), `evidence_sources`(10), gaps(5), `specifications`(0), `convergence_assessment`(0), `terms`(88), `PRAGMA user_version`(64)
WRITES    : `$SMOKE/render-out/parts_stub/{manifest.md,part00..13.md}` (15 files, 25870 bytes) — scratch only
EXAMINED  : 15 files / fingerprint over 12 tables
OUTPUT    : `DB fingerprint: 4810634e8b3f (mode=stub)` — **differs from committed `parts/v10/manifest.md:5`'s `c1dc69b7e186`**
FINDING   : **FAIL — `parts/v10/` is genuinely STALE, not just theoretically unguarded.**
LOCATION  : `parts/v10/manifest.md:5` (`c1dc69b7e186`) vs live fresh render (`4810634e8b3f`); `diff` of fingerprint inputs:
```
committed:  evidence_sources=0;gaps=0;...;user_version=57
live fresh: evidence_sources=10;gaps=5;...;user_version=64
```
also `parts/v10/part13.md:12` — "0 sources in the evidence base" — actually 10 today.
NOTE      : **7 schema migrations (57→64) and 10 evidence sources have landed since `parts/v10/` was last generated, and nothing caught it** — `render-freshness`'s `check: null` in the contract (line 138-142) is not a theoretical gap, it is live drift, measured. No restore needed — output stayed entirely under `$SMOKE/`.

### 12. `scripts/generate/context_map.py --check`
INVOKED   : `python3 scripts/generate/context_map.py --check`
STAGE     : render (registry battery) / substrate (content — it maps the whole repo, not book pages)
EXIT      : 1
READS     : DB + full filesystem/registry scan
WRITES    : NONE (`--check`)
EXAMINED  : 1 (the single committed `governance/context-map.yaml`, per its `min_items:1` "one file that always exists" note)
OUTPUT    : `STALE: governance/context-map.yaml differs from a fresh generation.`
FINDING   : FAIL (advisory level, so non-blocking) — a real, live, currently-red check
LOCATION  : `governance/context-map.yaml` (whole file, vs live regeneration)
NOTE      : Advisory, not part of the render *book surface* strictly, but registered in the `render` battery — reported for completeness of the battery run in entry 18.

### 13. `scripts/generate/research_contract_hook.py --check`
INVOKED   : `python3 scripts/generate/research_contract_hook.py --check`
STAGE     : render (derived-artifact battery, cross_stage in effect — it derives a SessionStart hook, substrate-adjacent)
EXIT      : 0
READS     : `governance/research-contract.yaml`, `.claude/settings.json`
WRITES    : NONE
EXAMINED  : 51 — `EXAMINED: 51 contract line(s)`
OUTPUT    : `PASS: contract and enforcer agree on 15 rule ids` / `PASS: the SessionStart hook matches governance/research-contract.yaml`
FINDING   : PASS
NOTE      : Not directly in my brief's numbered list but named in it — included for completeness; not mobility-relevant.

### 14. `scripts/audit/register_integrity_check.py --selftest`
INVOKED   : `python3 scripts/audit/register_integrity_check.py --selftest`
STAGE     : render
EXIT      : 0
READS     : own fixtures (`REGISTER_MAP`/`tuple_class` imported from `scripts/generate/pilot_renderings.py`), DB cross-check on
WRITES    : NONE
EXAMINED  : 15 cells × 6 registers (mutation-tested, 12 tamper cases, all FIRED)
OUTPUT    :
```
FIRED: I3 best-practice on regulatory-stratum-only
FIRED: I3 bypass: 'recommended standard' synonym in RSO body
FIRED: I3 amended: above-weak-band marker on RSO
...
clean pass on untampered document: yes
PASS: I1–I5 hold across 15 cells × 6 registers (DB cross-check on)
```
FINDING   : PASS — and this is decisive evidence for §6 below: the fired tamper case is explicitly **"I3 amended: above-weak-band marker on RSO"**, i.e. the code enforces the *amended* (flagged weak-band-only) form, catching an above-band injection, not the repealed absolute (no-language-at-all) form.
LOCATION  : `scripts/audit/register_integrity_check.py:10-13` (docstring: "I3 As amended by DR-2026-07-21 Option A... this checker enforced [the absolute form] until 2026-08-04"), `:227-250` (I3 AS AMENDED logic), `:326-330` (the fired tamper case itself)
NOTE      : See §6 — this contradicts `governance/pipeline-contract.yaml:126-129`.

### 15. `scripts/audit/matrix_consistency.py`
INVOKED   : `python3 scripts/audit/matrix_consistency.py`
STAGE     : render
EXIT      : 0
READS     : `schemas/directness.py`, compares to `evidence-architecture.md §3`
WRITES    : NONE
EXAMINED  : 10 — `EXAMINED: 10`
OUTPUT    : `PASS: 10/10 outcomes match evidence-architecture.md §3`
FINDING   : PASS

### 16. `scripts/audit/check_rendered_docs.py --all`
INVOKED   : `python3 scripts/audit/check_rendered_docs.py --all`
STAGE     : render
EXIT      : 0
READS     : `specs/` directory glob (finds 1 file, reference-only)
WRITES    : NONE
EXAMINED  : 0 — printed verbatim: `EXAMINED: 0 rendered document(s) — 1 present under specs/, reference-only since the 2026-08-06 reset; pass --doc to check a live one`
FINDING   : NOTHING-IN-SCOPE (by policy, per registry note — deliberate, not an accident: the `min_items` guard was retired 2026-08-06 for this exact reason)
NOTE      : `scripts/run_checks.py` correctly classified this as **"BLOCKING and vacuous"** and escalated it in its summary (see entry 18) — CLAUDE.md §2(a)'s machinery is working here.

### 17. `node scripts/audit/render_audit.js`
INVOKED   : `node scripts/audit/render_audit.js`
STAGE     : render
EXIT      : 0
READS     : `specs/*.html` (1 document)
WRITES    : NONE
EXAMINED  : 1 — `EXAMINED: 1`
OUTPUT    : `RESULTS: 6/6 checks passed (1 document(s), 0 failure(s), 0 warning(s))`
FINDING   : PASS
NOTE      : **node IS available** (`/opt/node22/bin/node`, v22.22.2) — the "if not, that is a finding" branch in my brief does not apply; no ABSENT here.

### 18. `python3 scripts/run_checks.py --battery render --kinds render,data --explain`
INVOKED   : `python3 scripts/run_checks.py --battery render --kinds render,data --explain`
STAGE     : render
EXIT      : 0
READS     : `governance/check-registry.yaml`
WRITES    : NONE
EXAMINED  : selected 7 of 63 registered checks (4 quarantined)
OUTPUT    :
```
[PASS] pipeline_completeness_fresh   0.1s
[PASS] evidentiary_audit_fresh       0.1s
[FAIL] context_map_fresh             0.3s  (advisory)
[PASS] site_pages_fresh              0.0s  (advisory)
[NONE] check_rendered_docs           0.0s
[PASS] register_integrity_check      0.2s  (advisory)
[PASS] render_audit_browser          2.2s  (advisory)
NOTHING-IN-SCOPE (1): check_rendered_docs
  BLOCKING and vacuous (1): check_rendered_docs — a gate that examined nothing gated nothing.
NON-BLOCKING failures (1): context_map_fresh
RESULT: PASS — 5 check(s) green, 1 nothing-in-scope, 1 advisory failure(s)
```
FINDING   : PASS overall, with 1 correctly-escalated NOTHING-IN-SCOPE and 1 live advisory FAIL
NOTE      : Confirms §2(a)'s "gate that passes having examined nothing... escalates blocking-and-vacuous" machinery is real and firing correctly today, on this exact battery.

---

## 5. The freshness contract — verified against the live registry

`governance/pipeline-contract.yaml:138-142` states: *"Rendered artifacts (parts/, site/) are not stale vs the DB state that produced them. Only the vetting surface auto-regenerates; parts/ has no committed fingerprint gate."* (`check: null`)

Cross-checked against `governance/check-registry.yaml` (line numbers from this run):

| Surface | Gate | Level | Registry line | Verified state |
|---|---|---|---|---|
| `tools/pipeline-completeness-dashboard.html` | `pipeline_completeness_fresh` | **blocking** | 1273-1289 | PASS, fresh |
| `audits/evidentiary-base-audit*`, `tools/evidentiary-audit-dashboard.html` | `evidentiary_audit_fresh` | **blocking** | 1290-1305 | PASS, fresh (registry's own note claims STALE — wrong, see §8) |
| `tools/spec-curation-vetting-surface.html` | (no dedicated `*_fresh` id — kept current by `regenerate_derived.sh` calling the writer directly) | n/a | — | fresh |
| `governance/context-map.yaml` | `context_map_fresh` | advisory | 1307-1338 | **FAIL, stale** |
| `site/specs/*.html` (93 files) | `site_pages_fresh` | advisory | 1339-1358 | PASS, fresh |
| `site/populations/*.html` (6 files) | **none** | — | — | fresh today (manually verified), unguarded |
| `site/rooms/*.html` (17 files) | **none** | — | — | generator is BROKEN (`room_page.py`, entry 8) — unguarded AND unregenerable |
| `parts/v10/*.md` (15 files) | **none** | — | — | **STALE**, measured (entry 11) |
| `index.html` | **none** | — | — | **STALE**, measured (§8) |

**Verdict: the contract's claim is correct as stated, and actually understates the problem.** It says parts/ has no fingerprint gate; true. It does not mention that `site/populations/`, `site/rooms/`, and `index.html` *also* have no gate, and that of the five ungated surfaces, two (`parts/v10`, `index.html`) are demonstrably stale right now, not merely theoretically at risk. `site_pages_fresh` (site/specs/) exists and is advisory, not blocking — so even the one gated static-page surface would not block a merge if it went red.

---

## 6. Register invariants I1-I5 — the I3 form claim

`governance/pipeline-contract.yaml:126-129` (inline comment) says:

> "NB register_integrity_check.py still enforces I3's repealed absolute form (ENGINE-LAG → DR-2026-07-21 §5)."

**This is FALSE as of 2026-08-25, and the file that makes the claim carries the evidence of its own error nearby in the same repo:**

- `scripts/audit/register_integrity_check.py:10-13` (its own module docstring): *"I3 As amended by DR-2026-07-21 Option A: a regulatory-stratum-only cell renders as FLAGGED weak-band (○, code-derived) best practice — never unflagged, never [above-band]... The absolute form ('no best-practice language, ever') was repealed; **this checker enforced it until 2026-08-04.**"*
- `governance/check-registry.yaml:1383-1395`: *"De-quarantined 2026-08-04: both stated blockers were cleared — it now defaults its document and DB paths... and **enforces amended I3 rather than the repealed absolute form.**"*
- Live `--selftest` run (entry 14 above) fired the tamper case **"I3 amended: above-weak-band marker on RSO"** — a tamper that only makes sense to test if the amended (weak-band-permitted, above-band-forbidden) form is what's enforced. Code at `:227-250` (amended-I3 branch) and `:326-330` (the fired case) confirm this mechanically, not just in prose.

FINDING: FAIL — `governance/pipeline-contract.yaml:126-129` is stale prose contradicting the current code, exactly the §2(b) failure mode, and located in the one file whose job is to be the authoritative machine-readable spine.
LOCATION: `governance/pipeline-contract.yaml:126-129` (wrong) vs `scripts/audit/register_integrity_check.py:10-13,227-250,326-330` and `governance/check-registry.yaml:1383-1395` (right, and mutually consistent).
NOTE for the mobility batch: **a regulatory-stratum-only mobility value (e.g. a bucket-1 code-derived corridor width with no independent clinical/Co-1 backing) is correctly renderable today as flagged weak-band (○) best-practice language** — not silently suppressed. A batch producing only code-floor cells for E-08/E-03 would not be blocked from rendering *something*, provided it is flagged and never promoted to ●/◐. The contract's own comment, if trusted at face value, would have led a session to believe such a cell could never carry best-practice language at all — itself a misdirection risk for anyone who reads the contract instead of the code.

---

## 7. Markers and prose discipline

**Mechanical marker-presence enforcement is narrow and does not cover the render surface generally.**

- `scripts/audit/register_integrity_check.py` checks *band-correctness* (○ vs ● vs ◐ vs unflagged) but only over its own `REGISTER_MAP`/pilot-renderings fixtures (15 synthetic cells × 6 registers), not over `site/specs/*.html` or `parts/v10/*.md`.
- `scripts/audit/check_rendered_docs.py` checks *preconditions* for an existing `●` (convergence_assessment status, governing-source recording) but has no rule for "a determination is present and carries NO marker at all" — and today it EXAMINES 0 documents (entry 16), so even its narrow scope is untested against real content.
- No script in `scripts/` or `tools/` implements a general "every rendered specification cell must carry ●/◐/○, unmarked is an error" sweep across `site/` or `parts/`.

**FINDING: ABSENT** — a general marker-presence gate over the actual book surface does not exist. Nearest existing surface: `register_integrity_check.py`'s I1-I5 battery (fixture-scoped) and `check_rendered_docs.py` (currently vacuous). What would have to exist: a check that walks `site/specs/*.html` (or `parts/`) once `specifications` is non-empty and asserts every rendered cell/value carries exactly one of ●/◐/○. Given `specifications=0` today, there is nothing yet for such a check to have caught — but nothing would catch it either, when the mobility batch lands.

### The 12 named skill files — file existence and mechanical attempt

All 12 exist under `skills/`. **None names or wraps an executable enforcement script of its own; none is referenced in `governance/check-registry.yaml`** (grepped all 12 names — zero matches). Each is a pure LLM-prompt playbook (frontmatter `name:`/`description:`/trigger phrases, then procedural instructions for an agent to follow by hand) — there is nothing to "run" mechanically beyond reading the file, which I did for all 12.

| Skill | Lines | Named script | check-registry entry |
|---|---|---|---|
| prose-style-checker | 140 | none | absent |
| voice-style | 534 | none | absent |
| table-formatter | 170 | none | absent |
| markdown-formatter | 108 | none | absent |
| toc-editor | 285 | `scripts/db.py` (gap CRUD, substrate) | absent |
| structure-auditor | 110 | `scripts/db.py add-gap` (substrate) | absent |
| practice-note-generator | 33 | none | absent |
| question-author | 123 | references `scripts/schemas/specification.py` drift, no own script | absent |
| find-and-replace | 176 | `scripts/db.py` (substrate) | absent |
| version-diff | 33 | none | absent |
| github-io | 289 | `scripts/db.py` queries (substrate) | absent |
| github-filing | 98 | none | absent |

FINDING: ABSENT (as a mechanical gate) for all 12, PASS (as a documented procedure) for all 12 — the file:line distinction the protocol wants doesn't apply because there's no code to point a line number at; the finding IS the absence.
NOTE: This means the "prose discipline" and "Unmarked is an error" rule (CLAUDE.md §6) is currently enforced **only by an agent choosing to follow these playbooks**, with zero machine backstop over the render surface, and zero registry entry to even remind a session these exist.

---

## 8. Hand-written counts audit (§2(b))

Live DB counts (2026-08-25, canonical, read-only):
```
items = 93            (by category: A=19 B=12 C=6 D=11 E=14 F=8 G=9 H=5 I=4 K=5; 10 distinct categories)
populations = 23
specifications = 0
evidence_sources = 10
source_locators = 875
gaps = 5
search_candidates = 60
bpc_metadata = 0
user_version = 64
```

### `index.html` — DRIFTED, hand-written, no generator exists for this file

| Location | Claims | True (live DB) | Drift |
|---|---|---|---|
| `index.html:7` (meta description) | "91 provisions, 661 evidence sources, 10 categories" | 93 items, 10 evidence_sources, 10 categories | provisions off by **2**; evidence sources off by **651** |
| `index.html:148` | "All 91 provisions by category" | 93 | off by 2 |
| `index.html:156` (Cat. A) | "18 provisions" | 19 (`items WHERE category='A'`) | off by 1 |
| `index.html:256` (Cat. B) | "12 provisions" | 12 | match |
| `index.html:326` (Cat. C) | "6 provisions" | 6 | match |
| `index.html:366` (Cat. D) | "11 provisions" | 11 | match |
| `index.html:431` (Cat. E — mobility's own category) | "14 provisions" | 14 | match |
| `index.html:511` (Cat. F) | "7 provisions" | 8 | off by 1 |
| `index.html:556` (Cat. G) | "9 provisions" | 9 | match |
| `index.html:611` (Cat. H) | "5 provisions" | 5 | match |
| `index.html:646` (Cat. I) | "4 provisions" | 4 | match |
| `index.html:676` (Cat. K) | "5 provisions" | 5 | match |

FINDING: FAIL — `grep -rln "index.html" scripts/ tools/` finds no generator; `governance/check-registry.yaml:142` lists it only as a member of the "content" path group, with **no `*_fresh` check targeting it**. It is a hand-authored file with hand-authored counts, currently wrong in 3 places (total, Cat. A, Cat. F) and grossly wrong on "661 evidence sources" (actual 10 — almost certainly a pre-clean-room-reset figure, per check-registry's own "post clean-room-reset" language elsewhere, never updated).
LOCATION: `index.html:7,148,156,511` (wrong); `:256,326,366,431,556,611,646,676` (currently correct, but equally unguarded).
NOTE: CLAUDE.md §2(b) explicitly names `index.html` as a site of past drift ("Counts in this file, in `index.html`, in manifests and in audits have all drifted") — this is that exact failure mode, live and reproducible today, not merely historical.

### `parts/v10/` — DRIFTED, but DB-derived (staleness, not hand-writing)

`parts/v10/part13.md:12` — "0 sources in the evidence base" — actual 10. This is not a hand-written number; it's a stale *generated* number (see §4 entry 11 — fingerprint `c1dc69b7e186` vs live `4810634e8b3f`). Root cause is the same as `index.html`'s (no freshness gate), different mechanism (staleness of a generator vs. hand-authored prose).

### `tools/*.html`

All three dashboards (`pipeline-completeness-dashboard.html`, `evidentiary-audit-dashboard.html`, `spec-curation-vetting-surface.html`) are DB-generated and confirmed fresh (entries 2-4) — no hand-written-count violation found here.

### `governance/check-registry.yaml` itself

`governance/check-registry.yaml:1303` — "STALE on main as of 2026-08-01" for `evidentiary_audit_fresh` — measured 2026-08-25, this check now PASSES (entry 3). The note is stale prose about a check's staleness that has itself gone stale. Minor (advisory-adjacent, not a rendered book surface) but the same failure class.

---

## 9. `tools/pipeline_completeness.py` and the stage-id spine

- Five stage ids confirmed in `governance/pipeline-contract.yaml`: `research` (:36), `evidence-collection` (:52), `judgment` (:68), `synthesis` (:103), `render` (:119) — exactly CLAUDE.md's list.
- `stage_label()` is derived, never stored: `tools/pipeline_completeness.py:42-43`:
  ```python
  def stage_label(stage_id: str) -> str:
      return stage_id.replace("-", " ")
  ```
  Confirmed: no second dict/table anywhere mapping id→display string (grepped).

**FINDING: FAIL — rule 5 violation found. `tools/pipeline_completeness.py:37` hardcodes a second, independent copy of the five-id SET (not just the display form):**
```python
STAGES = ["research", "evidence-collection", "judgment", "synthesis", "render"]
```
This list is a Python literal, not parsed from `governance/pipeline-contract.yaml` at runtime. `gather_enforcement()` (`:254-276`) *does* read the contract YAML for per-stage criterion counts, but it silently drops any stage id from the YAML that isn't already a key in this hardcoded `STAGES`-derived dict (`:270-272`: `if sid not in out: continue`) — so a stage renamed or added in the contract would be silently ignored by the dashboard rather than erroring, exactly the failure class CLAUDE.md §5 warns about ("`--changed-from` does not run the selftest, and the selftest is where a rename fails" — this is the analogous risk one level down, in a script `--changed-from` also would not catch since `tools/` isn't swept the same way).
LOCATION: `tools/pipeline_completeness.py:37` (second home) vs `governance/pipeline-contract.yaml:36,52,68,103,119` (declared single home per CLAUDE.md's own text and `check-registry.yaml`'s `basis: <stage>/<criterion>` pointers, e.g. `check-registry.yaml:1074` `basis: evidence-collection/evidence-verification-gate`, which correctly points rather than copies).
Grep confirmation (no other second home found): `grep -rn "evidence-collection" scripts/ tools/ schemas/ governance/` → only `tools/pipeline_completeness.py:37,40,135,522`, its own generated dashboard HTML (derived output, not a source), `governance/pipeline-contract.yaml:52` (the declared home), and `governance/check-registry.yaml:1074` (a pointer, not a copy).

---

## 10. The end of the chain — what a reader would see today, mobility item

For **E-08 (corridor clear width)** or **E-03 (ramp gradient)**, a reader of the published `site/specs/e-08.html` / `e-03.html` sees, today: item metadata (name, category, status=active), an honest **"Best-practice determination: not yet computed for this item, for any population"** banner, and an explicit note that `item_bpc_links` has no row for this item. Nothing fabricated, nothing silently omitted. This is a PASS for honesty, and a demonstration that `specifications=0` is correctly wired through to the actual rendered page, not just through the dashboards.

For `parts/v10/` (the assembled book), the reader would see a document that is 7 migrations and 10 evidence sources out of date, with no marker anywhere on the page that it is stale — because no freshness gate covers it. For `index.html`, the reader sees "91 provisions, 661 evidence sources" — wrong on both counts, unmarked as an estimate.

**What the render stage currently PROVES (mechanically, with a green gate)**: `site/specs/` (93/93 pages) matches the live DB exactly, right now, via `site_pages_fresh`/`build_site.py --check`; the two `tools/` dashboards and the vetting surface are byte-fresh; the register invariants I1-I5 (amended form) hold under mutation-testing against their own fixtures.

**What it currently only ASSERTS (no gate, prose/convention only)**: that `parts/` and `index.html` are trustworthy (they are not, measured); that `site/populations/` and `site/rooms/` are trustworthy (rooms' generator is actively broken); that rendered markers are present and correctly banded outside the fixture set; that the 12 prose-discipline skills were actually followed on any given page.

**Answer to the concrete mobility question** (§3 of the brief): if a mobility batch produced one judgment row (`specifications`) and one synthesis row (`convergence_assessment`/`best_practice_synthesis`) for, say, E-08 × MOB:
1. `python3 scripts/generate/spec_page.py E-08` would need to be re-run by hand to update `site/specs/e-08.html` — nothing regenerates it automatically, and `site_pages_fresh` (advisory, not blocking) would go from PASS to FAIL and *report* the drift, but not block a merge.
2. `python3 scripts/generate_parts.py --mode full` would very likely **still refuse** — its gate (entry 10) checks `specifications is empty`, a repo-wide condition, not a per-item one; one row would clear the "empty" bar (`COUNT(*) > 0`) after which it may proceed to `--mode full`, but this needs re-verification against the actual gate predicate once the row exists — I did not have a mobility judgment row to test the boundary condition directly (PROTOCOL forbids me from writing one).
3. `index.html`'s counts would need a **manual hand-edit** — there is no command a session could run instead; the file has no generator (confirmed by grep, §8).
4. `parts/v10/`, `site/populations/mob.html`, and (if fixed) `site/rooms/*.html` would all need the same manual `python3 scripts/generate_parts.py`/`population_page.py MOB`/`room_page.py` re-run — none is wired into `scripts/regenerate_derived.sh`, so a session that only runs the "single sanctioned regeneration entry point" (its own self-description) would miss all of them.

FINDING: ABSENT — there is no single command a session could run after a mobility batch to bring every render surface current; `regenerate_derived.sh` is not that command despite its docstring's framing, because it drives only 3 of ~8 generators (§1).

---

## S5 SUMMARY

### (a) Verdict table

| # | Invocation | Level | EXAMINED | Verdict |
|---|---|---|---|---|
| 2 | `tools/pipeline_completeness.py` (+`--check`) | blocking | multi-metric, no single count | PASS, fresh, deterministic |
| 3 | `tools/evidentiary_audit.py` (+`--check`) | blocking | 80 | PASS, fresh (registry note claiming STALE is itself stale) |
| 4 | `tools/regenerate_vetting_surface.py` | n/a (no dedicated `_fresh` id) | — | PASS, fresh |
| 5 | `scripts/generate/spec_page.py` E-08, E-03 | n/a | 1 each | PASS — honest "not yet computed" render |
| 6 | `scripts/generate/build_site.py --check` | advisory | 93 | PASS, fresh |
| 7 | `scripts/generate/population_page.py MOB` | n/a, unguarded | 1 | PASS, fresh (today) |
| 8 | `scripts/generate/room_page.py R_COR` | n/a, unguarded | 0 | **FAIL — crashes, wrong table name** |
| 9 | `scripts/generate/pilot_renderings.py` | n/a | 0 | VACUOUS (correctly — 0 cells) |
| 10 | `scripts/generate_parts.py --mode full` | n/a | 0 | PASS — correct refusal |
| 11 | `scripts/generate_parts.py --mode stub` | n/a, unguarded | 15 files / 12-table fingerprint | **FAIL — parts/v10 measured stale** |
| 12 | `scripts/generate/context_map.py --check` | advisory | 1 | **FAIL — stale**, currently red |
| 13 | `scripts/generate/research_contract_hook.py --check` | n/a | 51 | PASS |
| 14 | `scripts/audit/register_integrity_check.py --selftest` | advisory | 15×6 cells, 12 tampers | PASS — enforces amended I3 |
| 15 | `scripts/audit/matrix_consistency.py` | (governance/schema kind; not in render battery selection) | 10 | PASS |
| 16 | `scripts/audit/check_rendered_docs.py --all` | blocking | 0 | NOTHING-IN-SCOPE (policy, correctly escalated) |
| 17 | `node scripts/audit/render_audit.js` | advisory | 1 | PASS — node available |
| 18 | `run_checks.py --battery render` | — | 7 of 63 selected | PASS overall (1 advisory FAIL, 1 escalated NOTHING-IN-SCOPE) |
| 7b | 12 named skills | — | n/a (no executable) | ABSENT as mechanical gates, all files exist |

### (b) Ranked blockers (file:line)

1. **`governance/pipeline-contract.yaml:126-129`** — asserts `register_integrity_check.py` "still enforces I3's repealed absolute form"; FALSE, contradicted by the checker's own docstring (`scripts/audit/register_integrity_check.py:10-13`), its amended-I3 code (`:227-250,326-330`), and `governance/check-registry.yaml:1383-1395`. This is the governing contract file being wrong about the one thing it exists to be right about — highest-priority fix, one line edit.
2. **`tools/pipeline_completeness.py:37`** — a second, hardcoded home for the 5-stage-id set, silently dropping any stage the contract adds/renames (`:270-272`). Rule-5 violation in the exact script whose entire job is to be the pipeline spine's dashboard.
3. **`index.html:7,148,156,511`** — hand-written, unguarded, wrong today (91 vs 93 provisions; 10 vs 661 "evidence sources"; Cat. A and Cat. F off by 1 each). No generator exists for this file at all.
4. **`parts/v10/*.md`** (all 15 files, e.g. `manifest.md:5`, `part13.md:12`) — measured stale (fingerprint `c1dc69b7e186` vs live `4810634e8b3f`; 7 migrations and 10 evidence sources behind). No fingerprint gate exists, as the contract itself says — but the drift is not hypothetical, it is present now.
5. **`scripts/generate/room_page.py:26,29`** — queries nonexistent table `room`; live schema has `rooms`. All 17 committed `site/rooms/*.html` pages are unregenerable by the sanctioned tool.
6. **`scripts/regenerate_derived.sh:15-17`** — the file's own header claims to be "the single sanctioned regeneration entry point after ANY data/guidebook.db change," but drives only `pipeline_completeness.py`, `evidentiary_audit.py`, `regenerate_vetting_surface.py` — never `generate_parts.py`, `build_site.py`, `spec_page.py`, `population_page.py`, `room_page.py`, `pilot_renderings.py`. A session trusting this script's self-description will not regenerate `parts/` or `site/`.
7. **`governance/context-map.yaml`** — currently STALE per `context_map_fresh` (advisory, so non-blocking, but red).
8. **`governance/check-registry.yaml:1303`** — "STALE on main as of 2026-08-01" for `evidentiary_audit_fresh`; measured PASS today. Minor, self-referential §2(b) drift.

### (c) The ABSENT list

- A general marker-presence gate ("unmarked is an error") over `site/specs/` or `parts/` — does not exist; nearest surface is the fixture-scoped `register_integrity_check.py` and the currently-vacuous `check_rendered_docs.py`.
- Any executable script backing any of the 12 named prose/formatting/authoring skills — all 12 are pure playbooks, zero registry presence, zero mechanical enforcement.
- A single command that brings every render surface (`site/specs/`, `site/populations/`, `site/rooms/`, `parts/v10/`, `index.html`, `tools/*.html`) current after a DB change — `regenerate_derived.sh` covers 3 of ~8 generators only.
- A freshness gate for `index.html`, `site/populations/*.html`, `site/rooms/*.html`, `parts/v10/*.md` — none registered (only `site/specs/` and the two `tools/` dashboards + vetting surface are gated).
- A working `room_page.py` — exists as a file, crashes on invocation.
- Direct evidence of the `--mode full` boundary condition with a nonzero `specifications` count — PROTOCOL forbids writing evidence, so this remains untested; the refusal predicate (`specifications is empty`) was read from the tool's own message, not from its source, and should be confirmed against `scripts/generate_parts.py`'s source by whichever agent actually runs a real mobility batch.

### (d) Restore ledger

**No tracked file was left in a dirty state at any point.** Every generator that lacked a redirect flag (`spec_page.py`, `population_page.py`) produced output byte-identical to `git show HEAD:<path>` (verified with `cmp`/`git status --short` after each run), so no restore was ever necessary. Every generator with a redirect flag (`pilot_renderings.py --out`, `generate_parts.py --out`) was pointed at `$SMOKE/render-out/`. Writers with no redirect but a `--check` companion (`pipeline_completeness.py`, `evidentiary_audit.py`, `regenerate_vetting_surface.py`) were run as writers once, confirmed clean via `git status --short`, then their `--check` variant was also run.

| File touched | Dirtied? | How verified clean | Restore action |
|---|---|---|---|
| `site/specs/e-08.html` | No | `cmp` vs `git show HEAD:` — byte-identical | none needed |
| `site/specs/e-03.html` | No | `cmp` vs `git show HEAD:` — byte-identical | none needed |
| `site/populations/mob.html` | No | `git status --short` clean after run | none needed |
| `tools/pipeline-completeness-dashboard.html` | No | `git status --short` clean after run | none needed |
| `tools/evidentiary-audit-dashboard.html`, `audits/evidentiary-base-audit.*` | No | `git status --short` clean after run | none needed |
| `tools/spec-curation-vetting-surface.html` | No | `git status --short` clean after run | none needed |
| `site/rooms/r_cor.html` (attempted) | No | script crashed before any write | none needed |
| `governance/context-map.yaml` | No | ran `--check` only, never the writer | none needed |
| `parts/v10/*` (attempted stub/full) | No | both runs used `--out $SMOKE/...` | none needed |
| `pilot.html` (attempted) | No | used `--out $SMOKE/...` | none needed |

Final `git status --short` (identical to baseline, only my own untracked scratchpad additions present):
```
?? scratchpad/session_2026-08-25-pipeline-smoke-test-mobility/commands.jsonl
?? scratchpad/session_2026-08-25-pipeline-smoke-test-mobility/logs/
```
`git stash list`: empty, start and end.
Canonical `data/guidebook.db` sha256: `30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf`, unchanged start to end.
