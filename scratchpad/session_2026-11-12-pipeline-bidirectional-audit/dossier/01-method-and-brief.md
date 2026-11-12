# 01 — Objective, method, and standing constraints (shared by every agent)

## The owner's objective (verbatim)

> "ensure that our pipeline can be run in all directions at any stage in such a manner where we can dynamically research, adjudicate, synthesize, specify and render across a multitude of languages and jurisdictions."

Decomposed (this decomposition is the assistant's and is itself auditable):

- **D1 Omnidirectional.** A run may *enter* at any stage (base, research, evidence, judgment, synthesis, specification, render) and move *forward*, *backward* (re-entry: a render question sends work to judgment; a judgment gap sends work to research), or *laterally* (across slugs, parameters, lenses, jurisdictions, languages).
- **D2 Dynamic.** A run is initiated for an arbitrary request — a parameter × lens × jurisdiction × language cell — and executes the verbs it needs now, not only as a pre-planned batch.
- **D3 Multilingual and multijurisdictional.** Identity of concepts, sources, terms, codes and determinations does not depend on English or on one jurisdiction; adding a language or a jurisdiction is data, not code.
- **D4 Verifiable.** Every stage boundary has a precondition, a postcondition and a pointer back to its inputs, so a run in any direction can be checked and a result traced to its evidence.

## Method: top-down + bottom-up handshake

1. **Top-down (TD).** From the owner's prose and the contract, derive *what each stage and each stage boundary must offer* for D1–D4. Output: requirements ledger and an interface specification, expressed at table/column/verb level where possible. TD may not read code to decide what is required.
2. **Bottom-up (BU).** From tables, columns, constraints, views, `db.py` verbs, scripts, checks and skills, establish *what each stage can actually do today and in which directions*, by reading code and querying the database read-only. BU may not read the owner's prose to decide what exists. BU states what is enforced, what is only conventional, and what is absent.
3. **Handshake (HS).** At each stage boundary and each stage, meet TD's required interface against BU's observed capability. Every requirement receives one verdict: `MET` (enforced, evidenced), `PARTIAL` (exists, not enforced or one-directional), `UNMET` (absent), `CONTRADICTED` (code or data do the opposite), `UNPROVEN` (cannot be determined; say why). Every capability BU finds that no requirement asks for is `ORPHAN` (apparatus nothing in the book needs: CLAUDE.md §8). HS then attacks both legs.

Independence matters: TD and BU run without seeing each other's output.

## Standing constraints (from CLAUDE.md and the owner's preferences — they bind the audit and the plan)

- **Read-only.** Do not write `data/guidebook.db`; open it with `sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)`. Do not edit repo files, run git write commands, or run `scripts/run_checks.py --all`. Write only your named output file(s) under `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/`. Use `python3 -I` for scripts that read untrusted data.
- **Derive, never quote, a count** (rule 7a). Where you cite a number, give the command that produced it.
- **`.ignore` hides frozen records from the Grep tool**; owner rulings live in `sessions/`. Use `grep -r` / `git grep` through Bash. Never report a ruling absent from a search that could not have seen it. `[A-Z]-NN` item codes are prior-version content, never a container.
- **Rule 0.** A live owner ruling supersedes every ratified record it touches. Where two owner statements conflict, the later governs and the conflict is reported, not resolved by weight.
- **Owner-gated.** Mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory are the owner's to change (CLAUDE.md §8). An improvement that touches one is recorded as `OWNER DECISION REQUIRED`, with options, never decided.
- **Rule 10.** Tooling (schema, `db.py` verbs, checks) and research rows ship in separate PRs; any improvement plan must respect that ordering.
- **Rule 8 / minimise code.** Every proposed addition names what reads it and what wrong thing reaches the guidebook without it. Order of preference: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code.
- **A pass that examined nothing is not a pass.** State the subject of every check you cite; a 0-row object is unproven, not clean.
- **Evidence grammar.** Claims carry `file:line`, a query and its result, or a verbatim quote with source. Mark each claim `VERIFIED` (you saw it), `INFERRED` (follows from what you saw; say from what) or `UNVERIFIED`.
- **Language.** Canadian English; exacting, no flattery or encouragement; verdict first; problems ranked worst first; no false balance.
