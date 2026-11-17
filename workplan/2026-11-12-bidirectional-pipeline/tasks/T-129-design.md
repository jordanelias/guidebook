# T-129 design — a merge of two terms is a row, the survivor is derived, and the consolidation sweep proposes, a judge decides, and it ends

_Written 2026-11-17 by an Opus-class adjudicator on the owner's instruction of 2026-11-16 ("have Opus collate all of my questions about this and all of your answers/findings then adjudicate best fixes before planning out how to build followed by folding it into remediation plan"; "ensure compliance with layer architecture, prioritize long-term integrity of project re provenance and consistency"). Plan document: it changes no script, schema, row or ruling. Every count is given as the command that produces it; re-run it. SQL marked **sketch** is a shape, not a file to paste unread. Canadian English. It governs two tasks: section A is T-129 (the merge, NOT FOR SONNET), section B is T-130 (the proposer and its bound, a Sonnet-class executor may run it from this file). The adjudication that chose it is `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md`._

## 0. Verdict

**Two terms judged to name one concept are merged by a row, never by rewriting the rows that point at them.** A new base table, `term_merges`, holds one row per merge (the folded term, its survivor, who judged it, when, why) and retires in place when a merge is undone. One view, `v_term_survivor`, follows the live merges to each term's survivor; it is the single home of "which concept is this term now". Rows of every stage that point at the folded term keep pointing at it (they record what their writer said, when it said it); every writer that takes a term id resolves it through the view and refuses a folded term, naming the survivor; every name screen and every reader of a concept's forms reads the survivor's class (its own forms and those of every term folded into it). A judgment that two near-named terms are **not** one concept is a typed row of T-029's term-relation table, kind `distinct`, with its warrant; `add-term --distinct-from` writes it instead of leaving the judgment in the adjudication's free-text rationale.

**The sweep is a read verb, a bound held in the contract, and the batch.** `db.py consolidation-candidates` proposes pairs of live concepts that may be one (four derived reasons, each with the rows that show it); an Opus-class session judges each (merge, relate, distinct, or leave); a judged pair is not proposed again until either concept's class gains or changes a form after the judgment; the session stops when a pass proposes nothing or when the pass number reaches `consolidation.max_passes` in `governance/pipeline-contract.yaml`. Termination does not depend on the bound (section B4); the bound caps effort, as the owner asked ("limited repetitions to ensure exit").

**Confidence.** High (about 85%) that merging by a row with a derived survivor is the right shape for terms: it is the shape the project already uses for every other successor (identity codes, specifications, translations, connections), it leaves every earlier judgment readable as it was made, and it costs one table and one view. Medium (about 65%) on the four proposal reasons being enough: a cross-language duplicate with no seed, no translation and no shared form is not proposed, and only reading finds it (section B6).

## 1. What the rulings require

| Ruling (find it with) | Requirement | Met by |
|---|---|---|
| CLAUDE.md rule 5; OD-18 (`grep -E '^OD-18:' references/project-standards.md`: "status updates on earlier rows allowed, copies of later facts forbidden") | one home per fact; point, do not copy | the merge is one row in base; no row of a later stage is rewritten or copied |
| "retire in place then" (`grep -n -F 'retire in place then' references/project-standards.md | head -3`); OD-29 (`grep -E '^OD-29:' references/project-standards.md`: "both retire in place") | a data row is retired with a reason, never deleted or overwritten | `term_merges` and T-029's rows carry `retired_at`, `retired_by_session`, `retirement_reason` |
| CLAUDE.md rule 8 | derive it, or name who judged it | the survivor and the candidates are derived; each merge and each `distinct` names its judge (session), its time and its reason in named columns |
| O5, O7, O8 of 2026-10-12 (`grep -n -F 'handshake ALL directions' references/project-standards.md`) | centralised, pointers; handshakes in all directions | one resolver view read by every writer and reader; a refusal at every writer that meets a folded id |
| E4 (`grep -n -E '^\| E4 ' references/project-standards.md`) | model-generated aliases are search aids, never vocabulary | a seed may **propose** a pair (reason R3) and never refuses, names or merges anything |
| OD-03 and the T-028 design (`tasks/T-028-design.md`) | a concept is its id; its names are forms in `term_aliases` | the survivor's class is the union of member forms through `v_term_survivor`; no form is moved or copied |
| The 2026-11-06 schema-shape statement (CLAUDE.md §4) | one value per cell; no correction appended to a note | the merge's judge, time and reason are columns, not a dated line in `notes` (the shape `merge-parameter` uses, section A7) |
| CLAUDE.md §8 | the least code that closes the defect | one table, one view, two verbs (`merge-term`, `unmerge-term`), one read verb, one contract key, one kind on T-029's table |

## A. T-129: the merge

### A1. Why a row and a derived survivor, not a re-point (the push `merge-parameter` uses)

- **What `merge-parameter` does** (`grep -n -A30 'def merge_parameter' scripts/db.py`): it sets the folded parameter's `status` and `merged_into`, then UPDATEs `parameter_id` on every row of every table whose foreign key points at `base_parameters`, and appends a dated `MERGED` line to each moved row's `notes`. The moved rows no longer say which parameter their writer named; that fact survives only in prose. It has never been run (`python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select count(*) from base_parameters where status='merged'\").fetchone())"`).
- **Why that shape fails for terms.** The rows that point at a term are (derive: the FK loop of section A5) its forms (`term_aliases`), the adjudications that named it (`term_adjudications`, a judgment-stage record of what an adjudicator said of an observation), the parameter keyed on it (`base_parameters`), a declination (`parameter_declinations`), the searches that used its forms (`search_execution_forms`, through T-026 and T-028's `form_id`), and T-029's relations. Re-pointing an adjudication would make it say the adjudicator named a term it never named; re-pointing a form would make the form's history say it was always a form of the survivor. Both are overwrites of a record (test 2 of the adjudication). A row plus a derived survivor keeps every record as written and makes the merge itself the record.
- **The cost, stated.** Every reader that must see a concept's whole class reads through `v_term_survivor`. Section A5 derives the set of those readers and section A8's red tests hold each.

### A2. The table (sketch; one schema migration, derive its number, never type it)

```
CREATE TABLE term_merges (
  merge_id            INTEGER PRIMARY KEY AUTOINCREMENT,
  from_term_id        TEXT NOT NULL REFERENCES terms(term_id),     -- the folded term
  into_term_id        TEXT NOT NULL REFERENCES terms(term_id),     -- its survivor at the time of the merge
  reason              TEXT NOT NULL CHECK (length(trim(reason)) > 0),
  candidate_reason    TEXT,     -- the proposer's reason code (R1..R4, section B2) that put the pair before the judge, NULL when none did
  created_at          TEXT NOT NULL, created_by_session TEXT NOT NULL,   -- the judge and the time (dbcore.stamp_for)
  retired_at          TEXT, retired_by_session TEXT, retirement_reason TEXT,
  CHECK (from_term_id <> into_term_id),
  CHECK ((retired_at IS NULL AND retired_by_session IS NULL AND retirement_reason IS NULL)
      OR (retired_at IS NOT NULL AND retired_by_session IS NOT NULL AND length(trim(retirement_reason)) > 0))
);
CREATE UNIQUE INDEX ux_term_merges_live_from ON term_merges(from_term_id) WHERE retired_at IS NULL;
```

- `candidate_reason` takes its vocabulary from a CHECK in the same migration (`'R1','R2','R3','R4'`), read by `dbcore.check_values`, so the reason codes have one home and the proposer prints them from there.
- No `notes` column: the judgment is in its own cells.
- `terms` is not altered (no `status`, no `merged_into` on it): whether a term is folded is derived from `term_merges`, so it cannot disagree with it.
- Stage: **base** (the vocabulary layer); Layer 3 rows, Layer 1 schema. `governance/stage-map.yaml` gets `term_merges: base` under `tables:`.

### A3. The view (sketch)

```
CREATE VIEW v_term_survivor AS
WITH RECURSIVE walk(term_id, survivor_id, hops) AS (
  SELECT term_id, term_id, 0 FROM terms
  UNION ALL
  SELECT w.term_id, m.into_term_id, w.hops + 1
    FROM walk w JOIN term_merges m ON m.from_term_id = w.survivor_id AND m.retired_at IS NULL
   WHERE w.hops < (SELECT COUNT(*) FROM terms))          -- a cycle cannot form (A4), and this bounds the walk if one did
SELECT term_id, survivor_id, hops FROM walk w
 WHERE NOT EXISTS (SELECT 1 FROM term_merges m WHERE m.from_term_id = w.survivor_id AND m.retired_at IS NULL);
```

One row per term: its live survivor (itself when unmerged) and how many merges lie between. It reads base only, so it spans no stage. Python reads it through one helper, `dbcore.term_survivor(conn, term_id)`, which returns the survivor or None for an unknown id; no other code follows `term_merges` itself.

### A4. The verbs

- `db.py merge-term --from TERM-A --into TERM-B --reason TXT [--candidate-reason R1|R2|R3|R4] --session X [--dry-run]`. Refuses, each refusal naming the next action:
  - the same id twice; a blank reason; an unknown id;
  - `--from` already folded (names its survivor: nothing to do, or `unmerge-term` first); `--into` folded (names its survivor: merge into it). So `into` is always live and no cycle can form;
  - **`--from` carries an active parameter** (`base_parameters.status = 'active'` on `--from`): "merge the parameters first with `merge-parameter`, or merge in the other direction". A parameter is keyed on one term; the survivor carries the concept's parameter. When both carry an active parameter, `merge-parameter` is a separate judgment (it moves figures) and runs first;
  - the two disagree on parameter standing: one has a live declination (`parameter_declinations.revoked_at IS NULL`) and the other an active parameter (names `revoke-declination` or `decline-parameter`);
  - a live T-029 row of kind `distinct` between the two (through their survivors): "a judge recorded these as distinct (row N, session S): retire that row with its reason first". A judge changes its mind by a retirement with a reason, never by writing over it;
  - a `candidate_reason` outside the column's CHECK (`dbcore.check_declared`).
  - On success it writes one `term_merges` row and nothing else; it prints the survivor's class size before and after (derived) and every row of every table that points at `--from` (derived by the FK loop of A5) as "now read through the survivor".
- `db.py unmerge-term --merge-id N --reason TXT --session X [--dry-run]`: retires the merge row in place. Refuses a retired row, a blank reason, and an unmerge that would leave a term the survivor of a later merge whose own from-term now resolves elsewhere (derive by re-walking: refuse when `v_term_survivor` would change for any term other than the folded one and its own folded descendants; list them).
- **Every writer that takes a term id resolves it and refuses a folded one, naming the survivor:** `add-alias`, `add-term --distinct-from`, `adjudicate-term --term-id`, `add-parameter`, `decline-parameter`, `rename-term`, `amend-term`, `mint-term-from-catalogue` (its clash screen), T-029's writer, and `request-translation` / `record-translation` when the pointer resolves to a `term_aliases` row of a folded term (it may still be translated: the refusal is only for writing a **new** form or relation to a folded id; a translation of a held form is not refused). Derive the set at execution: `git grep -n -E "term_id|--term-id|--from-term|--distinct-from" -- scripts/db.py` and every parser flag whose value is checked against `terms`.
- **Every name screen reads the survivor's class:** `_name_holder` and `_near_terms` (as T-028 leaves them) report the survivor id, never a folded id, and a near match with a folded term's form is a near match with its survivor.

### A5. The readers (the caller sweep is the design's main cost)

Derive the full set at execution; never use a list typed here as the set:

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(t,f[3]) for (t,) in c.execute(\"select name from sqlite_master where type='table'\") for f in c.execute(f'pragma foreign_key_list(\"{t}\")') if f[2]=='terms'])"
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([n for (n,) in c.execute(\"select name from sqlite_master where type='view' and (sql like '%terms%' or sql like '%term_aliases%' or sql like '%term_id%')\")])"
git grep -n -E "FROM terms|JOIN terms|term_aliases" -- scripts schemas skills .claude ':(exclude)scripts/migrations'
```

A reader is in scope when it answers a question about a **concept** (its names, its forms, its coverage, whether it is a parameter, whether a name is taken). It reads the survivor's class: `JOIN v_term_survivor s ON s.term_id = x.term_id` and groups or filters on `s.survivor_id`. A reader that answers a question about a **record** (what this adjudication named, what this search used) is not changed. Known on 2026-11-17: `v_term_names` (T-028), T-057's base coverage view, the views of A5's second command that print a parameter's name through `terms`, `_name_holder`, `_near_terms`, `scripts/audit/alias_provenance_audit.py`. A view is a caller (CLAUDE.md rule 4): each one rewritten is recreated in the migration, and a view that renders 0 rows on the base is unproven, not clean (exercise it on the fixture of A8).

### A6. `distinct`, on T-029's table

T-029 (amended 2026-11-17) adds the kind `distinct` to its CHECK and retire-in-place columns to its table. **This task** makes `add-term --distinct-from TERM-X` write one `distinct` row per named term, in the same transaction as the term and its adjudication, its warrant the new term's NAMES-NEW adjudication (`term_adjudications.adjudication_id`) and its reason the `--rationale` text, so the judgment that two near names are two concepts is a typed pointer the sweep reads, not a sentence. A `distinct` row is symmetric in meaning; the writer stores it with the lower term id first and refuses a second live row for the same pair.

### A7. What this does not change

- `merge-parameter` keeps its re-point. It moves figures, which the engine gathers by `parameter_id`, and T-059 rewrites that gather. The adjudication registers the difference (`OPEN-ITEMS-PLAN.md` OI-78): when T-059's gather is rewritten, the parameter merge should take this design's shape (a merge row, a survivor view, no re-point, no `MERGED` note line), while no parameter merge has yet been run.
- No trigger is added. The refusal lives in the writers (one home per rule, a refusal that names the next action); a route that bypasses them (a data migration) is caught by the test of A8 run on the rebuilt database and by `term_merge_integrity` below.
- **One read-only integrity check, `scripts/audit/term_merge_integrity.py`**, registered `level: advisory`, `battery: data`, `kinds: [data]`, `basis: unattributed` with `no_floor:` opening `vocabulary-owed —` (no merge exists until a judge makes one): for every live merge, `into` resolves to a live survivor; no live row written **after** the merge's `created_at` (by `created_at`) in a table of A5's first command points at the folded term (a writer that should have refused did not); no live `distinct` row and live merge join the same pair. It prints `EXAMINED: <live merges>`. What reaches the guidebook without it: a form or a parameter filed under a folded term by a route that skipped the writers, so the concept's figures or names split again with nothing red. Ratchet to blocking with `min_items: 1` by T-132, the tooling task after T-131 writes the first merge (rule 10: never in T-131's research pull request).

### A8. Red tests (prefix `T129-`; confirm free first: `git grep -c '"T129-' -- scripts/tests` prints nothing)

Test file `scripts/tests/test_term_merges.py`, registered `test_term_merges` (`battery: tests`, `kinds: [tooling, schema]`, `level: advisory`, `basis: hygiene`, `no_floor: selftest — …`). Every probe chosen by query on a scratch copy; fixtures labelled `TASK-FIXTURE`.

| Case | Red before | Green after |
|---|---|---|
| T129-01 | `merge-term` is not a verb | a merge writes one row; `v_term_survivor` maps the folded term to the survivor; no other table's row count or content changes (hash every table but `term_merges` before and after) |
| T129-02 | — | each refusal of A4 fires alone, on a probe no other refusal stops, and its text names the next action |
| T129-03 | a form added to a folded term is accepted | `add-alias` (and each writer of A4, derived) refuses the folded id and names the survivor |
| T129-04 | a near match on a folded term's form names the folded term | `_near_terms` / `_name_holder` name the survivor |
| T129-05 | — | each concept reader of A5 (derived list) returns the survivor's class: the folded term's forms are counted under the survivor and the folded term has no row of its own |
| T129-06 | `--distinct-from` leaves no typed row | a `distinct` row with the NAMES-NEW adjudication as warrant; a merge of that pair is refused until the row is retired |
| T129-07 | — | `unmerge-term` retires the row; the survivor view returns the folded term to itself; every A5 reader shows two classes again; the retired row is still there with its reason |
| T129-08 | — | a chain (A into B, then B into C) resolves A to C with `hops = 2`; `merge-term --into A` is refused naming C |
| T129-09 | — | `term_merge_integrity` on a copy where an `INSERT` (as a data migration would) files a form under a folded term after the merge: listed, exit 1; removed: exit 0 |
| T129-10 | — | `term_merges` is in `dbcore.writable_tables(conn)` (the capture set), so a merge made on a scratch copy reaches the canonical database through `emit_batch_sql.py` |

## B. T-130: the proposer, its bound, and the loop

### B1. The verb

`db.py consolidation-candidates [--pass N] [--language L]`, read-only (it opens the database `mode=ro`). It prints one line per (pair, reason) with the rows that show it, then `EXAMINED: <pairs of live survivors considered>` and `CANDIDATES: <pairs proposed>`; both counts are computed. Exit 0 whether or not it proposes: it is a read, not a check (a check red whenever the base has work to do is red by construction, CLAUDE.md rule 6). The candidates are printed at the end of a batch by `.claude/commands/batch-done.md`'s COVERAGE section, where the owner reads coverage.

### B2. The four reasons (each derived; the codes are the CHECK of `term_merges.candidate_reason`)

A pair is two distinct **survivors** (`v_term_survivor`). Only `term_aliases` member rows (T-028: `alias_type` not `NARROWER` or `BROADER`) are forms; tokens are `_name_tokens` (T-009, script-aware); a near match is `_near_terms`' rule (subset or superset of token sets, the contained side of two or more tokens when it is the held one).

- **R1 shared form.** One form text (case-folded) held as a member by both classes in the same language, attested (`attestation` not `model_seed`). T-028 §5's conflation query, over survivors. Evidence printed: the two `form_id`s.
- **R2 near form.** A near match, in the same language, between an attested member form of one class and an attested member form of the other, or (language EN only, as T-028 leaves the label screen) a label (`terms.canonical_en`). Evidence: the two `form_id`s, or the form and the label.
- **R3 seed bridge.** A `model_seed` form of one class, in language L, is an exact or near match of an attested member form of the other class in L. Proposal only: a seed never refuses, names or merges (E4). Evidence: the seed's and the attested form's `form_id`s.
- **R4 translation bridge.** A row of `v_translations_current` with `status = 'reviewed'` (T-049; OD-30) pointing at a member form of one class, into language L, is an exact or near match of a member form, or (L = EN) the label, of the other class. Evidence: the `translation_id` and the matched `form_id` or label.

### B3. What is not proposed again

A pair is **judged** when a live row joins its two survivors in `term_merges` (it would no longer be a pair), or in T-029's table (any kind: `distinct`, broader, part of, adjacent, element has parameter, element has provision). A judged pair is proposed again only when the base has grown under the judgment: some member form of either class (or a reviewed translation of one) has `created_at` or `updated_at` later than the judging row's `created_at`. Derived; nothing stored. So when the base is extended (T-069 promotes forms, T-107 attests them, T-112 translates them), the pairs it touches come back on their own.

### B4. The bound, and why the loop ends without it

- **Held once, in data.** `governance/pipeline-contract.yaml` gains one top-level key, appended at the end of the file (the atoms of `workplan/pipeline-state-graph/atoms/` cite its lines by number until T-134 merges: T-049 item 4 has the rule): `consolidation:` with `max_passes: 3`. `schemas/pipeline_contract.py` gains the optional model (`extra="forbid"`, one field `max_passes: int`, `ge=1`). No number appears in the verb's code.
- **The loop** (the session's, written in `skills/run-pipeline_SKILL.md` and `.claude/commands/batch-done.md`): run `consolidation-candidates --pass 1`; judge every line; run `--pass 2`; and so on. Stop when a pass prints `CANDIDATES: 0`, or after the pass whose number equals `max_passes`. With `--pass N` the verb prints `pass N of M` (M read from the contract); `--pass` above M is refused, naming what to do: "the bound is reached: list what remains in the pull request; the next batch starts again at pass 1". A pair left unjudged is printed again in each pass and ends in that list.
- **Termination without the bound.** Within a sweep no form is added (a judge writes merges and relations only). Each pass either judges a proposed pair, which leaves the unjudged set for good (B3: only a later form brings it back, and none is written), or merges two classes, which lowers the number of live survivors by one. The live survivors are finite and only fall; the unjudged pairs among them are finite; so after at most (survivors − 1) merges plus one pass that judges everything left, a pass proposes nothing. The bound exists because the owner asked for limited repetitions, and to cap a batch's effort, not to make the loop end.
- **Why 3.** Pass 1 judges what the write-time screens let through; pass 2 judges the pairs pass 1's merges created (a merged class has new forms); pass 3 catches a chain. A base that still proposes after three passes is changing faster than one batch should consolidate it, and the remainder is listed, not lost. The owner may change the one line.

### B5. Who judges, and what each verdict writes

Opus-class (the decision is what a phrase names, in its own language). Per line: **one concept** → `merge-term` (direction: into the class that carries an active parameter; else into the class whose label is an attested form, `v_term_names.label_is_attested_form`; else the lower id) with the reason and `--candidate-reason`; **related, not one** → T-029's writer with the kind and its warrant; **two concepts** → T-029 `distinct` with its warrant; **cannot tell** → leave it (listed again; ends in the pull request's list). **A pair either of whose terms has a domain in `dbcore.NON_QUANTITY_DOMAINS`** (lenses, populations, conditions, methods, law, economics: `grep -n '^NON_QUANTITY_DOMAINS' scripts/dbcore.py`) is not merged by the judge: it is listed for the owner in the pull request, because a merge there can bear on the population taxonomy (CLAUDE.md §8). Identity, ICF and access-need codes are not terms and are never proposed; their consolidation is `retire-identity` with the owner's approval, as now.

### B6. What the sweep cannot find

A cross-language duplicate with no attested form in a shared language, no seed in the other's language near the other's attested form, and no reviewed translation. Only reading finds it: the base coverage view (T-057) makes the owed form searches visible, and T-069 and T-107 attest the forms that then bring such a pair into R1 or R2.

### B7. Red tests (prefix `T130-`)

Test file `scripts/tests/test_consolidation_candidates.py`, registered `test_consolidation_candidates` as T129's file is. On a scratch copy, build each fixture: T130-01 R1 fires on a shared attested form and not on a shared `model_seed` form; T130-02 R2 fires on a same-language near pair and not across languages; T130-03 R3 fires on a seed bridge and the seed never appears as a refusal anywhere (`add-term` with the seed's text is not refused because of it); T130-04 R4 fires on a reviewed translation and not on a `translated` (unreviewed) one; T130-05 a pair judged `distinct` is not proposed, and is proposed again after a new attested form is added to either class; T130-06 a merged pair is never proposed and the survivor's class carries the folded forms into later proposals; T130-07 `--pass` above the contract's bound is refused, naming the next action, and a temporary copy of the contract with another bound (loaded by the function's `contract_path` keyword, which the CLI does not expose, as T-049's AT-108) changes the refusal point with no file under `scripts/` changed; T130-08 an AST scan of the verb's functions finds no integer constant equal to the contract's bound and no reason code typed outside the column's CHECK; T130-09 the verb writes nothing (`sha256` of the copy before and after); T130-10 a pair with a `NON_QUANTITY_DOMAINS` term is printed with the mark `owner` and the judge's verbs are not suggested for it.

## C. Rejected alternatives

- **A. `merge-parameter`'s re-point for terms.** Overwrites records (A1).
- **B. `status` and `merged_into` columns on `terms`, as on `base_parameters`.** An unmerge would overwrite them, and the judge, time and reason need columns of their own; one row per merge keeps each and retires in place. `terms` is read by views that a rebuild would have to recreate (`select name from sqlite_master where type='view' and sql like '%terms%'`).
- **C. Triggers that refuse a write to a folded term.** A second home for a rule the writers hold, invisible to the refusal register (T-088) and unable to name the next action; the integrity check catches a route that bypasses the writers.
- **D. A `same_as` or `equivalent` kind on T-029's table.** T-029 dropped `equivalent` because two terms naming one concept are a dual home and the act is a merge (its section 4 item 2); a merge row with a derived survivor is that act.
- **E. A stored candidate list or a pass counter table.** Both are derivable (rule 8): the candidates from the base, the bound from the contract, and who judged what from the judging rows. The pass a judgment was made in is not a fact the book needs.
- **F. A registered check that fails while candidates exist.** Red by construction; the candidates are printed where coverage is read.
- **G. Using `model_seed` aliases in the write-time near screen (G4).** E4: a seed is never vocabulary; a seed that refused a real concept's name would let a model's guess block an observed phrase. Seeds propose (R3) and the judge decides.

## D. Where the owner may disagree

(1) That an Opus-class judge may merge two vocabulary concepts on its recorded reason, reversibly, without the owner's confirmation of each (pairs touching `NON_QUANTITY_DOMAINS` excepted); the owner reads the list in the pull request. (2) The bound of three. (3) That a cross-language identical string is proposed (R1 within a language only; across languages only through R3 or R4): the owner question on cross-language clashes is OD-68, and its answer may add a fifth reason. Each is reversible by one line or one verb.
