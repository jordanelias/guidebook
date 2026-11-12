# STRESS-BRIEF — run the pipeline base → render, then in every direction, and log all behaviour

Owner instruction (2026-11-12): "stress test run pipeline all directions and log all behaviour/outputs"; "do it across three different unrelated topics"; "work from base to render". Fable holds the authority to stress test, patch and iterate on the code pipeline (code, schema, scripts, checks, skills only; doctrine is the owner's). **This pass is STRESS TEST AND LOG ONLY: do not patch repo code.** A defect is recorded with its reproduction, not repaired; patches follow in a separate pass informed by the logs.

Read first: `/home/user/guidebook/CLAUDE.md`; `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/dossier/01-method-and-brief.md` (standing constraints bind you); the audit's `audit/hs-handshake-matrix.md` §0–§1 and `audit/hs-improvement-programme.md` §1 (what is already known to be broken — your job is to reproduce, extend and *find what the audit missed*, not to restate it); `.claude/skills/run-pipeline/SKILL.md` (the sanctioned orchestration).

## Hard rules

1. **Scratch only.** Copy the canonical DB to your own scratch file under your topic folder's `scratch/` (outside git: `/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/stress-<topic>/`). Never write `data/guidebook.db`. The canonical sha256 must be identical at the end (the harness records it on every call).
2. **Every command through the harness**, so that all behaviour is logged automatically:
   `python3 -I /home/user/guidebook/scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress/run_logged.py --db <SCRATCH.db> --log <TOPIC>/log.jsonl --tag <scenario-id> --note "<what you expect>" -- <command...>`
   It sets `GUIDEBOOK_DB_PATH` for the child, records argv, rc, seconds, full stdout/stderr, row-count changes per table and the canonical hash. Write the **expectation before each run** (`--note`), then compare — a surprise is a finding. Do not summarise away failures: refusals, tracebacks, silent no-ops (rc 0, nothing changed) and green-but-examined-nothing results are all behaviour to log.
3. **Writes that touch the tree** (`emit_data_migration.py`, `migrate_db.py` on a real path, anything that writes under `scripts/migrations/`) run only in a **clone**: `git clone --quiet /home/user/guidebook <scratchdir>/clone` and use the harness's `--cwd <scratchdir>/clone` with the clone's own scratch DB. Never emit a migration into `/home/user/guidebook`.
4. **No repo edits** outside `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress/<topic>/`. No state-changing git commands, no `run_checks.py --all` (individual `scripts/audit/*.py` and `--battery <name>` on the scratch DB are fine), no `bootstrap.sh`, no `pip install -r requirements.txt`, no spawning agents.
5. **Fixtures are labelled.** Anything you invent to exercise a path (a source, a term, an alias, a jurisdiction) is marked `STRESS-FIXTURE` in its text and in the log note, lives in the scratch DB only, and never carries a bibliographic field written from memory as if real (CLAUDE.md §5c). Real retrieval is allowed and encouraged for real sources: use `scripts/research/retrieval_log.py fetch` (persist payloads under your scratch dir, not `retrieval-log/` in the repo) through the egress proxy; a blocked source is a logged behaviour (try the Wayback route of CLAUDE.md §7 once).
6. **Derive every number** with its command; mark claims VERIFIED / INFERRED / UNVERIFIED. Canadian English. Verdict first.

## Protocol (per topic)

### Pass 1 — FORWARD, base → render, in stage order, for ONE concrete cell of your topic
For each stage use the sanctioned verbs (`db.py --help`; the run-pipeline skill) and log each step; at every stage boundary record: what the previous stage handed over, what this stage required, what it refused, and what pointer lets you get back.
1. **base**: is the topic's vocabulary there (terms, aliases, parameters, lens rows, language/jurisdiction rows)? Dynamically define a NEW parameter for the topic from an observed term (`observe-term` → `adjudicate-term` → `add-parameter`, or the declined route). Try to add a new language and a new jurisdiction by data only.
2. **research**: log a search (with prior expectation), stage candidates, resolve/admit one real source; mine its citations one step; a gap-driven search. Include one non-English search.
3. **evidence**: admit a real source with retrieval and author verification; admit a non-English one (record its own-language title, aliases with in-language source); a case study or economics entry if the topic offers one.
4. **judgment**: read the source ONCE against ALL defined parameters (the scan contract: `record-scan`, `add-extraction`, catalogue mode); record population-match; extraction relations (conditions, comparators, derived). Then define a parameter AFTER the reading and observe what the system says about the already-read source (read-once test).
5. **synthesis**: find equivalences / adjacencies / similarities / commonalities across parameters, clauses, instruments, jurisdictions, languages (connections, conflicts, convergence); attempt a coarser, abstract parameter that unifies clause-level figures in different units.
6. **specification**: determine the cell (`assess_cell` and its gates) for ≥3 lenses (identity / ICF / access-need / medical) and compare outputs; attempt retire/re-determine; raise and resolve a gate.
7. **render**: run every renderer or view that exists for the determination (`scripts/generate/*`, the `v_*` views, any page generator); try to produce what a reader would see, in two languages if anything allows; try to trace a rendered claim back to retrieved bytes by pointers only.
Then replay the **write path** in a clone: capture → `emit_batch_sql.py` → `emit_data_migration.py` → `migrate_db.py` → `migrate_db.py --rebuild`, and record whether the rebuilt DB equals the scratch DB (row counts, then `migration_reproducibility --deep`).

### Pass 2 — BACKWARD
From the render/specification output, walk back by pointers: specification → extraction → source → locator → retrieved payload → search execution → gap. Then **re-entry**: from a judgment-stage finding that a source is insufficient, create a research gap and re-enter research; from a render question to a judgment recheck. Record where the walk breaks and where the system offers no pointer.

### Pass 3 — COLD ENTRY at every stage
With no upstream work for the request, start at each of the seven stages in turn and record what it does or refuses (the 7×7 direction matrix of `workplan/pipeline-state-graph/walkability.py` is the claim to test, cell by cell for your topic).

### Pass 4 — LATERAL
Same parameter across ≥3 jurisdictions and ≥3 languages (≥1 non-Latin script across the three-topic programme; pick for your topic), across ≥2 lenses; add jurisdiction-specific values and a unit mix (mm/cm/in, °C/°F, dB/% as the topic requires); sub-national instrument; edition currency; a superseded standard.

### Pass 5 — ADVERSARIAL INPUTS
Duplicate DOI (R9), a fabricated author on a fixture, a mixed-script quote against `--quote` verification, a number written in words, a unit hidden in prose, an out-of-vocabulary value, a wrong-session-id form, a rename of a vocabulary term, a retire of a parameter that has extractions.

## Output (your topic folder)
- `log.jsonl` — the harness log (authoritative, complete).
- `00-summary.md` — verdict first: how far a base→render run got and where it stopped, per stage; the direction matrix for your topic with observed behaviour (MECHANISED / MANUAL / PROSE-ONLY / NONE / BROKEN); the ten worst behaviours; what matches the audit's predictions and what the audit missed or got wrong.
- `behaviours.md` — one entry per notable behaviour: scenario id (the `--tag`), expectation, observed, rc, evidence line in `log.jsonl` (give the tag and timestamp), classification (as-designed / defect / silent-no-op / vacuous-pass / refusal-correct / refusal-wrong / doc-contradiction), and the reproduction command.
- `defects.md` — each defect once, ranked by harm to the guidebook (a value published for the wrong people outranks a convenience gap), with the minimal reproduction and the stage; **no repair proposed**.
- `scenarios.md` — the scenario list with tags and pass/fail against expectation.
Reply with the paths, the three worst behaviours, counts derived with commands (log lines, scenarios, defects), the hash check, and anything you could not run.
