# DR-2026-09-26 (v2): Six recurring defect shapes. The pass gets a record, provenance gets an artefact, and research and tooling ship apart

> **STATUS: PROPOSED, NOT RATIFIED.** Committed so the plan is not lost to container recycling between sessions; it binds nothing until the owner answers §9. v2 repairs v1's mechanisms after an independent adversarial review (different model, fresh context) found verified errors in v1. §0.3 lists every finding, what v2 changed, and how the change was checked. The six root causes are not re-diagnosed here — they were established by a separate read-only diagnostic survey (Fable, 2026-09-26) and are re-verified, not re-derived, in §0.2.
> Every figure was measured on 2026-09-26 against `origin/main` @ `cf35d441` and
> `origin/claude/batch-20-audit-cluster-templer-fhwa` @ `fe0dcd17` (PR #159, not yet merged at the time this was written — check current state before acting on anything below). The command that produced each
> figure sits beside it. Re-run the command rather than trusting the sentence (CLAUDE.md rule 7a). Several commands read the
> branch's DB, so extract it once: `git show origin/claude/batch-20-audit-cluster-templer-fhwa:data/guidebook.db > $SCRATCH/b20.db`.
>
> **To land fully** (per §11): after the owner answers §9 and after PR #159 merges, this status line updates to RATIFIED, a register row is added, and construction proceeds per §7.

## §A How to use this document

| If you are | Read |
|---|---|
| The owner, ratifying | §C, then §9 (seven questions; OQ-2 is withdrawn), then §8 (what each mechanism can and cannot be shown to do) |
| A session building a phase | §7 for the order (nothing starts before PR #159 merges), then that decision's "proposed" and "compliance" subsections |
| Checking that the diagnosis was verified and not taken on faith | §0.2, then each "finding" subsection |
| Checking what changed from v1 | §0.3 |

## §B What this amends on ratification

| Document | Change |
|---|---|
| `decisions/DR-2026-08-19-…` §7 | The "optional single migration" (`adversarial_findings`) is **built** (§1) |
| same, §12.1 step 7 and §12.2 | An appended SUPERSEDED-IN-PART callout (§4) and an appended AMENDED callout (§6). Nothing is edited in place |
| `references/project-standards.md` | One **new, later-dated** CORRECTION entry carrying the seed `SUPERSEDES` lines (§4). The 2026-09-25 and 2026-09-26 entries are not touched |
| `governance/pipeline-contract.yaml` | `evidence/discovery-provenance` gains a check (§2), and its text changes when `connections_produced` retires (§5, phase 2b). New `cross_stage` criteria `doctrine-currency` (§4) and `research-tooling-separation` (§6) |
| `governance/check-registry.yaml` | Five new entries: `adversarial_pass_recorded`, `provenance_artefact_audit`, `provenance_attribution_audit`, `supersession_backpointer_audit`, `research_tooling_separation`. `claims_docket`'s note is corrected (§1) |
| `scripts/run_checks.py` | `SESSION_POINTERS` gains `CURRENT`, and the selftest asserts that every declared `session_pointer` is a known key (§1) |
| `CLAUDE.md` | §2: rule 0's enforcement line (§4) and a research/tooling separation rule (§6). §7: the `CURRENT` trap gains "and it holds the DB session stem" (§1) |
| `governance/research-contract.yaml` and its `.claude/settings.json` copy | A SUPERSEDED marker on R13, **conditional on OQ-6** (§4). Only the owner can regenerate the settings.json half |
| `scripts/tests/test_db_integrity.py` | The H05 comment's existing SUPERSEDED marker gains its ruling's anchoring quote (§4) |
| `.claude/agents/antagonist.md`, `.claude/commands/{adversarial,batch-done,session-open}.md` | A report block, a no-launch rule, the adversarial audit run on `CURRENT`, and the DB-stem form and session kind at open |
| `workplan/2026-09-10-batch-06-runbook.md`, `skills/citation-miner_SKILL.md` | The live `add-candidate` invocation gains `--surfaced-in`, and the staging instruction is written where R15's anchor points (§2) |

## §C What this decides, in one page

1. **RC4: the adversarial pass gets a record, and its absence goes red** (§1). Two tables, three verbs and one check. The reviewer's model is **derived from the assistant turns of its transcript**, because batch 20's "different model" antagonist ran on the same model as its author. The check reads the live-session pointer `scratchpad/CURRENT`. v1's `LATEST-RESEARCH` names the previous session until close.
2. **RC1: a candidate is checked against the bytes of the payloads its search returned** (§2). The search→payload edge is recorded **when the search is logged**, in a junction that points into the unedited retrieval log. v1 put that edge in the manifest `fetch()` writes, but the search does not exist yet when `fetch()` runs.
3. **RC2: the curated-list detector learns the shapes the shortcut actually takes** (§3). Only an exact match with a CHECK can fail; a subset is reported. Derivation then becomes the default write path, sequenced last because it has the widest blast radius.
4. **RC3: currency lives at the superseded text itself, not in an index** (§4). A ruling that names what it supersedes is checked to have marked it. Every pointer is anchored on a quote that occurs once, never on a `DATE:` line.
5. **RC5: the discovery route is typed, and the dual home the contract already forbids is settled** (§5). The owner's 2026-09-26 ruling already chose which home. History is corrected through writers, not hand SQL.
6. **RC6: research and the tooling it uses ship in separate PRs** (§6). This rule governs the building of everything above, from the first PR.
7. **Nothing here starts before PR #159 merges** (§7). Several phases depend on what only that branch holds.

---

## §0 Header, and what was verified

**Category:** D-OP and D-SCHEMA, with two D-METH questions (§9).
**Delegation:** DG-REVIEW for the mechanisms. DG-NON for OQ-1 and OQ-7. OQ-5 is DG-REVIEW, and is asked anyway (§9).
**Status:** v2, PROPOSED — see status line above.
**Relates to:** DR-2026-08-19 §7, §12.1 step 7 and §12.2. The ledger RULE of 2026-08-19 (adversarial review), and the rulings of 2026-09-25 and 2026-09-26, which exist only on PR #159's branch until it merges. DR-2026-09-11 clause 2. Research batch 20 (PR #159) is the specimen.

### §0.1 Why a DR, and why a successor is allowed

DR-2026-08-19 §11 property 3 is corrected in its own text. The successor-prohibition check was "SPENT 2026-08-19": it self-expired at `evidence_sources >= 1`, and "a successor plan is no longer build-rejected". This is a decision record, not a plan. It makes six decisions, and each has its own reversal (§10).

### §0.2 The survey, verified

| RC | Verdict | What verification added |
|---|---|---|
| RC4 | **Held** | The pipeline contract names an enforcer for the pass, and that enforcer does not test it (§1.1). Batch 20's "independent" antagonist ran on the author's model (§1.1). |
| RC1 | **Held** | The true discovery route was written on the candidate row in prose while its typed pointer contradicted it. A naive artefact check would have gone green, and a naive DOI match would have gone red on the correct rows too (§2.1). |
| RC2 | **Held in direction** | The survey's 26/46 depends on its definition, and mine differs (§3.1). The detector's blind spots are named: module-level constants, range mirrors, and comment-only vocabularies. |
| RC3 | **Held, and undercounted** | More than five stores are involved (§4.1). The two register stores stopped at D-0188. The contract text injected into every session serves a superseded line. One of v1's two specimens is weaker than v1 said (§4.1). |
| RC5 | **Held** | The contract already names the dual home and forbids adding a writer before it is settled. The owner has already chosen the event home (§5.1). |
| RC6 | **Held** | S01 itself was born inside the repair step of an adversarial review (§6.1). PR #159 also ships the `dbcore` helper this DR cites (§6.1). |

### §0.3 What v2 corrects

The review's findings are F1–F11. Checking them against the live repository turned up N1–N12, which the review did not raise. Where this DR disagrees with a finding, the row says so.

| # | Finding | What v2 does | Checked by |
|---|---|---|---|
| F1 | v1's RC1/RC5 acceptance could not go red on the specimen. `surfaced_in` was never backfilled. Backfilling manifests would edit committed artefacts. `migrate_db.py` has no cutoff flag | The search→payload edge moves out of the manifest into a DB junction. History gets it through writers, and no artefact is edited. `surfaced_in` is backfilled on 123–125. Acceptance runs on scratch copies of two committed DB blobs, with the new schema applied by `migrate_db`'s own atomic applier and no data migration, plus a fixture for the refusals (§8). `--schema-only` cannot do this job (N12) | `grep -n add_argument scripts/migrate_db.py` lists `--dry-run`, `--schema-only`, `--rebuild`, `--session` and `--selftest`, and no cutoff; the DB path comes from `GUIDEBOOK_DB_PATH`. A scratch prototype over the real batch-19 payloads: before the repair, 123 and 124 fail while 117 and 121 pass. After it, all four pass and 125 is reported (§8) |
| F2 | RC4's check used `LATEST-RESEARCH`, which names the previous session. `read_pointer` returns the `.md` form raw. `connection_targets` has no session column | The check uses `CURRENT` and strips `.md`. Its tables come from the RULE's own text and its columns are derived by suffix. `SESSION_POINTERS` must gain `CURRENT`, or the entry silently SKIPs (N4) | Pointer contents on both refs. `run_checks.py` `SESSION_POINTERS` and `read_pointer`. A table/column query (§1.2d) |
| F3 | Several phases depend on #159. Migration 096 is taken on the branch. 1c needs an owner-run `--write` | Every phase starts after #159 merges, each with a stated reason. Migration numbers are assigned at build time. The owner's `research_contract_hook.py --write` step is named inside 1c | Migration listings on both refs. The 09-25/09-26 `DATE:` grep. Execs 99 and 100 are absent from main. The `research_contract_sync` entry (§7) |
| F4 | RC3's "red on real history" is impossible, because no `SUPERSEDES` line exists | §8 says the audit examines nothing on current state. The red is shown on the seed PR's own hunks, removed one at a time in a scratch copy | `git grep -c 'SUPERSEDES:'` exits 1 on both refs |
| F5 | §3.2(b)'s DDL-comment removal needs a table rebuild, which contradicts §3.3 | (b) no longer removes the comment, so §3.3 is now true. v2 does **not** fold the removal into 1b: `search_executions` carries five views and two inbound FKs, whereas 096 rebuilt a table with none (§3.2b) | `sqlite_master` queries (§3.2b) |
| F6 | The historical UPDATE had no sanctioned writer. §5.3's reproducibility reasoning was wrong in kind | `amend-search` gains typed setters on the precedent of its existing `--set-target-evidence-type`, and `reattribute-candidate` gains `--surfaced-in`. §5.3 is rewritten. **Partial disagreement:** on main, `amend-search` does more than append a note (it already re-types `target_evidence_type` and raises `harm_finding`). The finding's conclusion holds, because nothing can set the new columns | The `amend_search` source in `scripts/db.py` (`grep -n 'def amend_search' scripts/db.py`) |
| F7 | `dbcore.require_reason` does not exist. `DATE:` lines are not unique | Ledger references anchor on a quote that occurs exactly once, everywhere (§1.2b, §4.2). **Partial disagreement:** `require_reason` does not exist on main, but it does exist on the branch this DR also measured. PR #159 introduces it in `4f41b11b`. v2 cites it as #159's, with a fallback | `git grep -n 'def require_reason' origin/main origin/claude/batch-20-audit-cluster-templer-fhwa -- scripts/dbcore.py`. `git log -S 'def require_reason' origin/claude/batch-20-audit-cluster-templer-fhwa -- scripts/dbcore.py`. `grep '^DATE:' references/project-standards.md \| sort \| uniq -d \| wc -l` |
| F8 | The `mining_direction` refusal would refuse ordinary calls (the column is NULL on 40 of 91 rows) | `mining_direction not in (None, "none")` | `select mining_direction, count(*) from search_executions group by 1` on main. A scratch probe (§5.2c) |
| F9 | `role` may duplicate existing fields. RC4's scope pre-decides OQ-8. The seeds edit committed ledger entries. Class-3 subset matching is unsafe as blocking | `role` is dropped (§2.2a gives the reasoning). The scope is the RULE's limb-(a) tables. The seeds become a new CORRECTION entry. Class 3 fails only on equality; a subset is reported, and three legitimate subsets exist on main today | The manifest key tally, the ledger parse, the ledger's CORRECTION convention, and an AST scan (§2.2a, §1.2d, §4.2c, §3.2a) |
| F10 | OQ-2 contradicts §1.4. OQ-5 cites the wrong authority | OQ-2 is withdrawn, and promotion becomes a stated engineering criterion (§1.4). OQ-5's authority is corrected: the question is not on `decision-protocol.md` §2.4's always-DG-NON list | `governance/decision-protocol.md` §2.2–§2.4 |
| F11 | Several derive commands do not reproduce as claimed | Each is corrected in place: which DB holds `internet-archive` (§3.1), the SELF-AUTHORED range (§6.1), the sweep commands (§2.3), the `connections_produced` readers (§5.2a), Class 6's mechanism (§3.2c), model normalisation (§1.2b) and the #159 file list (§6.1) | Each command was run on 2026-09-26 |
| N1 | **The search does not exist when `fetch()` writes the manifest.** Batch 19 logged exec 90 and exec 91 after fetching their payloads | The edge is recorded at `log-search`/`amend-search` time (§2.2b) | §2.1 |
| N2 | **Payloads JSON-escape the DOI's slash** (`10.3390\/ijerph18062953`). v1's `norm_doi` substring test misses every DOI in such a payload | Matching uses `retrieval_log.normalise_quote` over `decode_artefact` output | §2.1 |
| N3 | **`CURRENT` has not always held the DB stem.** Batches 11–15 wrote branch slugs | `/session-open` writes the DB stem, and the audit prints the stem it resolved | §1.2(d) |
| N4 | **An undeclared `session_pointer` silently SKIPs an advisory check**, because `read_pointer` catches `KeyError` | Add `CURRENT`, and add a selftest assertion | §1.2(d) |
| N5 | **`connections_produced` is `NOT NULL DEFAULT '[]'`,** so rule 5's "NULL forward" is unavailable and a retired writer would state "found nothing" | Phase 2b rebuilds `citation_mining` to relax NOT NULL, as 067 already rebuilt it once | §5.2(a) |
| N6 | **v1's specimen (i) is weaker than stated.** §12.1 already sits under a section-level SUPERSEDED head (2026-09-10). Batch 20 did mark the H05 note | §4.1 states both | §4.1 |
| N7 | **v1's `/batch-done` edit (`--battery research`) repeats F2 three times.** Three other research checks read `LATEST-RESEARCH` | `/batch-done` runs this one audit on `CURRENT` | §1.2(f) |
| N8 | **main's `LATEST-RESEARCH` names batch 18 although batch 19 merged.** The pointer is not reliably moved at close either | This supports F2 | `cat sessions/LATEST-RESEARCH` on main |
| N9 | **v1's §3.1 figure is not what v1's Class 6 counted** | Class 6 now prints both (§3.2c) | §3.2(c) |
| N10 | **Only 11 of 24 historical mining rows have a derivable, FK-valid `mined_ref_id`** | The rest stay NULL and are reported | §5.2(d) |
| N11 | **`log-search` already refuses a missing prior on every search.** v1 described its planned-only refusal as "R8 unchanged" while waiving the prior for non-planned origins | v2 keeps the refusal for every origin (§5.2c) | `grep -n 'prior-expectation is required' scripts/db.py` |
| N12 | **`migrate_db.py --schema-only` applies nothing in this repository.** Migrations 085–095 carry `AFTER_DATA` markers, so the plan interleaves data steps, and `--schema-only` stops at the first data step even when every earlier step is already applied. It is not a substitute for the cutoff flag v1 assumed | §8's scratch demonstrations apply the numbered schema migrations with `migrate_db._prepare_body` and `_apply_atomically`, which `run_migrations` itself calls, and run no data migration | `grep -l 'AFTER_DATA:' scripts/migrations/*.sql`. `GUIDEBOOK_DB_PATH=$SCRATCH/copy.db python3 scripts/migrate_db.py --schema-only --dry-run` on a scratch copy of main prints *"--schema-only stops here: 11 schema migration(s) are gated behind data migrations by AFTER_DATA"*, and the schema stays at 95 |

---

## §1 Decision 1: RC4. The adversarial pass gets a record, and its absence goes red

### §1.1 Finding

- **No table exists.** `select name from sqlite_master where name like '%adversar%'` returns nothing, on main and on the batch-20 branch.
- **The requirement already exists three times, and none of them is enforced:**
  - **The ledger.** RULE 2026-08-19, ACTION (2): *"records SURVIVED claims as well as SUSTAINED ones — a zero-finding pass must be able to show what it attacked, or it is indistinguishable from a pass that never ran."*
  - **DR-2026-09-11 clause 2**, the owner's ruling: *"a task is done when the antagonist reports what it attacked the claim with."*
  - **`governance/pipeline-contract.yaml`, `cross_stage/definition-of-done`:** *"No … ready-for-review PR while … an independent adversarial pass is unrun/unapplied."*
- **The contract's enforcer for the third one does not test it.** The registry gives `claims_docket` the basis `cross_stage/definition-of-done`. That script scans added prose for claim-words, and `grep -n -i adversar scripts/audit/claims_docket.py` finds the word in comments only. The one blocking check with "adversarial" in its name, `audit_adversarial_use`, validates the misuse-vector catalogue, which is a different thing.
- **The gates hand work to the pass.** `research_batch_dod.py`'s R7 and R13 comments delegate two questions to the "Standing subjects of every adversarial pass" (`skills/adversarial-research_SKILL.md`):
  - whether a harm finding actually reached its flagged row;
  - whether a `mismatch_note` is true against the payload.

  So a COMPLIANT DoD vouches for two properties whose only examiner may never have run, and `/batch-done` does not mention the pass (`grep -c -i adversar .claude/commands/batch-done.md` prints 0).
- **A subagent cannot launch the reviewer.** Batch 20 §0: the authoring subagent had no agent-launching tool, so it ran a self-administered pass. That pass *"missed every one of the independent pass's findings."*
- **The claimed model independence did not happen.** Batch 20 §0 calls the antagonist "read-only, a different model", and `.claude/agents/antagonist.md` declares `model: fable`. The committed transcript of that pass shows `claude-opus-5-5` on every assistant turn, the same model the authoring subagent ran on. Derive it from the assistant turns only:
  ```
  B=origin/claude/batch-20-audit-cluster-templer-fhwa
  for f in 2026-09-25T05-15-51_adversarial_a1efd54a 2026-09-25T04-19-11_other_acceda5e; do
    git show $B:transcripts/harness_34e8c762/subagents/$f.jsonl | python3 -c 'import sys,json,collections,re; print(dict(collections.Counter(re.sub(r"\[[^]]*\]$","",r["message"]["model"]) for r in map(json.loads,sys.stdin) if r.get("type")=="assistant" and isinstance(r.get("message"),dict) and r["message"].get("model"))))'
  done
  ```
  v1's `grep -o '"model":"[^"]*"'` counts every record type. On the author transcript it also finds `claude-opus-5-5[1m]` once, on an `attachment` record rather than an assistant turn; the normalisation rule is in §1.2(b). The record cannot say why this happened, and this DR does not guess. The point is that only the transcript knows which model served.

### §1.2 Decision proposed

**(a) A schema migration, `NNN_adversarial_passes_and_findings.sql`.** NNN is the next free number on main **at build time, after PR #159 merges** (§7). The migration is additive and needs no rebuild.

```sql
CREATE TABLE adversarial_passes (
  pass_id             INTEGER PRIMARY KEY,
  subject_session     TEXT NOT NULL,   -- BARE stem of the batch attacked; the writer strips a trailing .md
  subject_commit      TEXT NOT NULL,   -- the sha the reviewer read
  reviewer_transcript TEXT NOT NULL,   -- tracked path under transcripts/
  reviewer_models     TEXT NOT NULL CHECK (json_valid(reviewer_models) AND json_type(reviewer_models) = 'array'),
                                       -- DERIVED by the writer (rule in (b)); never typed
  author_transcript   TEXT NOT NULL,
  author_models       TEXT NOT NULL CHECK (json_valid(author_models) AND json_type(author_models) = 'array'),
  closed_at           TEXT,
  created_by_session  TEXT NOT NULL,
  created_at          TEXT NOT NULL,
  CHECK (reviewer_transcript <> author_transcript)   -- a self-administered pass is not a pass
) STRICT;

CREATE TABLE adversarial_findings (
  finding_id      INTEGER PRIMARY KEY,
  pass_id         INTEGER NOT NULL REFERENCES adversarial_passes(pass_id),
  lens            TEXT NOT NULL CHECK (lens IN (
                    'L1-existence','L2-fidelity','L3-independence','L4-tier','L5-population',
                    'L6-contrary','L7-recognition','L8-query-shape',
                    'S1-harm-reached-row','S2-mismatch-note-vs-payload','S3-containment')),
  subject_table   TEXT,                -- POINTER to the row attacked (rule 5); never a copy of it
  subject_key     TEXT,
  claim_attacked  TEXT NOT NULL,
  method          TEXT NOT NULL,
  artefact        TEXT,                -- what the claim was attacked WITH (DR-2026-09-11 clause 2)
  verdict         TEXT NOT NULL CHECK (verdict IN
                    ('SUSTAINED','SURVIVED','NOT-ATTACKED','WITHHELD-FOR-OWNER')),
  disposition     TEXT CHECK (disposition IS NULL OR disposition IN
                    ('REPAIRED','REJECTED','PROVISIONAL-DISPUTED','OWNER-RULED')),
  disposition_ref TEXT,                -- a data migration path; a quote-anchored ledger pointer; or the reason
  created_by_session TEXT NOT NULL,
  created_at      TEXT NOT NULL
) STRICT;
```

`adversarial_passes` as written was created on a scratch copy of the batch-20 DB (SQLite 3.45.1). The JSON and cross-column CHECKs are accepted on a STRICT table.

- **No `independence` column.** Whether the reviewer was a different model is **computed** from the two model lists (disjoint or not), never asserted (rule 8).
- **The lens set** is the eight lenses of DR-2026-08-19 §7 and the 2026-08-19 RULE, plus the three standing subjects of the adversarial-research skill. The CHECK becomes the set's one machine-readable home, and the prose stays as explanation.

**(b) Three writers in `scripts/db.py`.**

- **`record-adversarial-pass --subject-session S --subject-commit SHA --reviewer-transcript P --author-transcript Q`**
  - `S` is accepted in either spelling and stored as the bare stem, using the rule `research_batch_dod.py` already applies (strip a trailing `.md`).
  - **The served-model rule.** The writer reads `message.model` on records whose `type` is `assistant`, and nothing else in the file. It removes one trailing bracketed suffix from each string (`re.sub(r"\[[^\]]*\]$", "", s)`), because that suffix is a context-window annotation, not a different model. It stores the sorted list of distinct results. When a transcript shows two different normalised models, such as a mid-run fallback, both are listed, and any overlap with the other side counts as same-model.
  - It refuses when:
    - either file is untracked or lies outside `transcripts/`;
    - both paths name the same file, because a self-administered pass is not a pass (batch 20 §0 says this about its own);
    - a transcript has no assistant turn carrying a model;
    - the reviewer's final message carries no findings block (c).
  - It writes one findings row per block entry. The writer never retypes a finding.
- **`dispose-adversarial-finding --finding-id N --disposition D --ref R`**
  - `REPAIRED` refuses unless R is an existing file under `scripts/migrations/` whose name matches `migrate_db.DATA_PATTERN`. The pattern is the one home of what a data migration is called.
  - `OWNER-RULED` refuses unless R has the form `references/project-standards.md :: "<verbatim quote>"` and the quote occurs **exactly once** in the ledger under §4.2(a)'s normalisation. That is the same anchor the `SUPERSEDES` grammar uses, applied everywhere a ledger entry is referenced. It is **not** keyed on a `DATE:` line: `grep '^DATE:' references/project-standards.md | sort | uniq -d | wc -l` counts the `DATE:` texts that close more than one entry (28 at `cf35d441`), and the most repeated, `DATE: 2026-08-27 — owner ruling, quoted above.`, closes 13 (`… | sort | uniq -c | sort -rn | head -1`).
  - `REJECTED` and `PROVISIONAL-DISPUTED` require `--reason` through `dbcore.require_reason`. **That helper is not on main at `cf35d441`.** PR #159 introduces it (`4f41b11b`; `git grep -n 'def require_reason' origin/claude/batch-20-audit-cluster-templer-fhwa -- scripts/dbcore.py`). This DR builds after #159 merges, so the helper exists at build time. Should #159 not merge, the writer uses the inline pattern the helper replaced: `reason = (reason or "").strip()`, then `raise Refusal(...)`, as `reattribute_candidate` does on main.
- **`close-adversarial-pass --pass-id N`** refuses unless all of these hold:
  - every lens in `dbcore.check_values(conn, "adversarial_findings", "lens")` has at least one row;
  - at least one row is SURVIVED;
  - every NOT-ATTACKED row's `method` says why;
  - every SURVIVED row names an `artefact` that exists on disk.

**(c) A report block for the antagonist.** In `.claude/agents/antagonist.md`, "Report shape" gains a closing fenced block, `json adversarial-findings`, with one object per finding in the columns above. The antagonist stays read-only, and the record is derived from its own words.

**(d) A check, `adversarial_pass_recorded`,** backed by `scripts/audit/adversarial_pass_audit.py`. The registry entry, in its own schema:

```yaml
- id: adversarial_pass_recorded
  cmd: [python3, scripts/audit/adversarial_pass_audit.py, --session, '@SESSION@']
  battery: research
  kinds: [data, synthesis]
  level: advisory
  basis: cross_stage/definition-of-done
  cost: fast
  requires_session: true
  session_pointer: CURRENT
  no_floor: 'session-scoped — the subject is the rows the session named by scratchpad/CURRENT wrote into
    the tables the 2026-08-19 RULE names in its limb (a). A session that wrote none owes no pass and reports
    NOTHING-IN-SCOPE; a session that wrote some and has no closed pass FAILS, so an empty subject cannot
    pass silently.'
```

Four facts about the live code decide how this entry works:

1. **`CURRENT`, not `LATEST-RESEARCH`.** `sessions/LATEST` and `LATEST-RESEARCH` move at CLOSE, so for the whole life of a session they name the previous one (CLAUDE.md §7), and `/batch-done` runs before close. On main at `cf35d441`, `LATEST-RESEARCH` names batch 18, although batch 19 has merged (`cat sessions/LATEST-RESEARCH`). `scratchpad/CURRENT` moves at OPEN, and `/batch-done` already reads it.
2. **`SESSION_POINTERS` must gain `CURRENT`.** It holds only `LATEST` and `LATEST-RESEARCH` (`grep -n -A4 '^SESSION_POINTERS' scripts/run_checks.py`). `read_pointer` returns `''` for an unknown name, because it catches `KeyError`, and `run_check` then SKIPs an advisory check that requires a session. Registering `session_pointer: CURRENT` without editing the dict switches the check off without a word. So 1a adds `"CURRENT": os.path.join(REPO_ROOT, "scratchpad", "CURRENT")`, and `--selftest` gains an assertion that every `session_pointer` in the registry is a key of `SESSION_POINTERS`.
3. **Spellings differ by pointer.** `LATEST-RESEARCH` holds the `.md` form, and `CURRENT` holds the bare form (compare `git show origin/claude/batch-20-audit-cluster-templer-fhwa:sessions/LATEST-RESEARCH` with `…:scratchpad/CURRENT`). The audit strips a trailing `.md` and matches both spellings in SQL. No row in any writable table carries the `.md` form today. This prints 0 on main:
   ```
   python3 -c "import sys,sqlite3; sys.path.insert(0,'scripts'); import dbcore; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); print(sum(c.execute(f'select count(*) from \"{t}\" where \"{col}\" like ?',('%.md',)).fetchone()[0] for t in dbcore.writable_tables(c) for col in [r[1] for r in c.execute(f'pragma table_info(\"{t}\")')] if col.endswith('_by_session')))"
   ```
4. **`CURRENT` has not always held the DB stem.** Batches 11–15 wrote branch slugs such as `batch-15-t2-synthesis-threshold`, while their rows are stamped `session_2026-09-18-research-batch-15-…`. From batch 16 on, `CURRENT` held the DB stem. Derive: `git log -p --format=%h -- scratchpad/CURRENT | grep '^+[^+]'`. A wrong-form value matches no row, and the audit would report NOTHING-IN-SCOPE. At `/batch-done`, its sibling `research_batch_dod` fails R9a/R9b on the same empty subject (see the `research_dod_session` registry note), so the mismatch does surface, but not in this check. 1a therefore amends `/session-open` to write the DB stem form, and the audit prints the stem it resolved.

**The subject, derived rather than listed:**

- **Tables.** The audit takes the backticked names in the 2026-08-19 RULE's limb (a) from `references/project-standards.md`. It anchors on the quote *"An adversarial pass may be commissioned ONLY against a diff that (a) wrote rows to the research tables ("*, which must occur exactly once, or the audit exits 2 ("cannot run"). The ruling is the list's one home, so no copy of it lives in code (rule 8). Today the parse yields 11 tables, and all 11 are live, captured by `dbcore.writable_tables`, and carry `created_by_session`.
- **Columns.** The audit uses every column of those tables whose name **ends** in `_by_session` (`PRAGMA table_info`). A substring match would be wrong, because `bpc_metadata.supersession_check_complete` contains "session". `connection_targets` is the one writable table with no such column, which is why v1's "any row carrying its stem in any writable table" could not be applied as written.
- **Scope held to the RULE.** v1 scoped the check to every writable table, which would have implemented OQ-8's wider scope while claiming to defer it. v2 checks only the RULE's tables until the owner answers OQ-8.
- **Limb (b) is not mechanised.** It covers synthesis artifacts, which are a property of a changeset rather than of rows. It is named here, not implemented.

```
python3 - <<'PY'
import re, sqlite3
t = open('references/project-standards.md', encoding='utf-8').read()
a = 'An adversarial pass may be commissioned ONLY against a diff that (a) wrote rows to the research tables ('
assert t.count(a) == 1
i = t.index(a) + len(a); tables = re.findall(r'`([a-z_]+)`', t[i:t.index(')', i)])
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)   # after #159 merges; before, $SCRATCH/b20.db
S = 'session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa'
for tb in tables:
    cols = [c[1] for c in con.execute(f'PRAGMA table_info("{tb}")') if c[1].endswith('_by_session')]
    print(tb, sum(con.execute(f'select count(*) from "{tb}" where "{c}" in (?,?)', (S, S + '.md')).fetchone()[0] for c in cols))
PY
```

- **It FAILS** when the session wrote any row into those tables and no closed pass names that session. On the batch-20 DB, batch 20 wrote into six of the eleven.
- **It REPORTS, and never fails on,** two things: a pass whose model lists overlap, and a SUSTAINED row with no disposition.
- **`EXAMINED`** counts the rows the session wrote into those tables. Findings rows are reported separately.

**(e) Correct the registry in the same PR.** `claims_docket`'s note should say it covers only the Mode-3 half of `definition-of-done`.

**(f) Command edits.**
- **`/adversarial`:** a session with no agent-launching tool says so in its handback and stops. It does not record a self-administered pass.
- **`/batch-done`:** add `python3 scripts/audit/adversarial_pass_audit.py --session "$(cat scratchpad/CURRENT)"` beside its existing `research_batch_dod.py` line. v1 added `run_checks.py --battery research` here instead. That battery's other session-scoped checks, `research_dod_session`, `author_fidelity` and `citation_mining_session`, declare `LATEST-RESEARCH` (`grep -n 'session_pointer' governance/check-registry.yaml`), so mid-session they would examine the previous batch: F2's defect three more times.
- **`/session-open`:** write the DB session stem into `CURRENT` (point 4 above), and record the session kind (§6).

**(g) Readers.** The first reader is `research_batch_dod.py`: R7 and R13 print the S1 and S2 verdicts instead of pointing at a skill section. The book-facing reader comes later. DR-2026-08-19 §7 already states it ("Disputed → the cell caps at `provisional`"), and nothing mechanises it: the determination engine would refuse `stated` while a SUSTAINED finding on a governing source is undisposed. It is proposed here, not built.

### §1.3 Compliance

- **Rule 3.** One additive schema migration. Rows enter only through db.py, then emit, then migrate. Once a committed data migration INSERTs into these tables they can never be dropped (rule 5), so reversing them means retiring the writer, not dropping the table.
- **Rule 4.** Nothing is renamed. `dbcore.writable_tables` derives the capture set from INSERT literals, so the new tables are captured automatically; assert this with `dbcore --selftest`. The Pydantic mirror must be added. So must an entry in `validate_pydantic_schemas`' curated `MODEL_TABLE_MAP`, which rule 8 names as a violation: this adds one entry to it and fixes nothing. `SESSION_POINTERS` gains a key and nothing is removed from it.
- **Rule 5.** Findings point at `(subject_table, subject_key)` and copy nothing. The model columns hold facts about Layer-4 transcripts, which SQL cannot query, and the writer is their only author.
- **Rule 7a.** No counts. The lens set lives in the CHECK, the table set lives in the RULE, and the check prints `EXAMINED`.
- **Rule 8.** Vocabularies come through `dbcore.schema_choices`. Models are derived. Independence is computed. The scoped tables are parsed from the ruling.
- **Layers.**
  - The tables are Layer 1, at judgment: they judge recorded research and point backward along the spine.
  - The verbs are Layer 2.
  - The check, the `run_checks.py` pointer, and the edits to commands and agents are Layer 0.
  - The rows are Layer 3, and the transcripts are Layer 4.
- **§8: what reaches the book without it.** An interpretive overclaim reaches a governing source's extraction. Batch 20 §0b had two:
  - #2: an untested Table 20 cell typed `measurement_primary`;
  - #1: a comparison checked against only one of footnote c's two warrants.

  Only a fresh reader caught either.

### §1.4 Owner-gating

The mechanism mechanises methodology that is already canonical: the 2026-08-19 RULE, DR-2026-08-19 §7, DR-2026-09-11 clause 2, and `cross_stage/definition-of-done`. Under `governance/decision-protocol.md` §2.2 that is D-SCHEMA → **DG-REVIEW**, and under CLAUDE.md §8 code needs no sign-off, so it can be built.

**The check's level follows from the same reasoning, so it is not an owner question.** v1 asked the owner (OQ-2) whether to promote the check to blocking, while arguing here that the requirement is already canonical. Both cannot be true.

- The cost v1 cited, 15–25% per batch (DR-2026-08-19 §7's estimate), was accepted when the owner ratified that DR and the definition-of-done criterion.
- A batch run wholly inside a subagent is already non-compliant with `definition-of-done` today, because it cannot run an independent pass.
- A blocking check enforces what is ratified and adds no obligation. The level is therefore a rollout decision on the registry's own precedent: `author_fidelity` stays advisory "until it has demonstrated a NON-VACUOUS subject across more than the one session that created the log".
- **The promotion criterion:** the first research batch whose pass is recorded, closed and disposed, with `EXAMINED` above zero (batch 21 at the earliest). The session that observes it promotes the check in a tooling PR, and that PR tells the owner. It does not ask.

One point is not code:
- **Whether a same-model pass counts as independent** (OQ-1). DR-2026-09-11 has Opus executing agonist-antagonist, but for an *enumerated queue*, and its own text says "a queue, not a class". The check's FAIL condition does not depend on this answer; it only reports same-model passes. The owner's answer decides whether that report becomes a failure.

### §1.5 Cost and blast radius

Small and isolated: one additive migration, three verbs, one audit script, one line in `run_checks.py` plus a selftest assertion, and four markdown edits. No existing writer changes.

### §1.6 What could go wrong

The check rewards the existence of SURVIVED rows. A reviewer under the author's completion pressure can emit eleven of them, each naming a file it never opened. That reviewer might be on the same model, launched at the end of a long batch and asked "is it ready?". This table then becomes the attestation's `independent_reviewer_counterclaim` again (`minLength: 30`): a field that is always populated and never informative. The refusals raise the cost of theatre. They do not detect it, and only OQ-1 does.

---

## §2 Decision 2: RC1. A candidate is checked against the bytes of the payloads its search returned

### §2.1 Finding

- **The lineage holds.** Each of these compares two homes of one fact:
  - H03 and H04 were deleted on 2026-08-24 for that shape.
  - H05 was deleted for the same reason; its record is dated 2026-09-02.
  - S01 was born on 2026-09-18, in commit `f3434e7d` ("adversarial review — machinery repaired, not instances"). It compares `search_candidates.exec_id` with `search_admissions.exec_id`.
  - H01, H02, H06 and H07 were deleted on 2026-09-21.

  On the branch, `link_admission` writes an edge only when a candidate row already names that exec. Its own docstring says S01 "cannot fail on an edge written here."
- **The specimen is sharper than the survey says.** Candidate 124's own `locator` reads *"deposited reference bb0030 in REF-01006's Crossref record"*. The true route was on the row in prose, while its typed `exec_id` named exec 91, a search targeted at `co1`. The truth was recorded, the typed pointer contradicted it, and no gate reads prose. On main at `cf35d441`, candidates 123 and 124 still point at exec 91 and 125 at exec 90. On the branch, they point at 99, 99 and 100 (`select candidate_id, exec_id from search_candidates where candidate_id >= 123` on each DB).
- **The harm reaches the book.** `v_coverage_branch` sums `results_admitted` by `target_evidence_type`. Had exec 91's count been raised, a T3 facility census would have counted as Co-1 yield. Batch 20 §0c withheld that raise for exactly this reason.
- **One gate already compares a record with an artefact.** `author_fidelity` (`retrieval_log.py --verify-authors`) does, and it is the gate that caught the fabrication in CLAUDE.md §5(c). It is the model for this fix.
- **A naive artefact check would have passed GAP-050.** Pinto's DOI appears in two batch-19 payloads (`grep -l ijerph18062953 retrieval-log/session_2026-09-20-research-batch-19-pre1990-chain-steinfeld-walter-templer/*`):
  - `9a51a98c7235d28f.json` is M1, the backward-mining deposit: the true route.
  - `21741431ca20572e.xml` is C9, "Co-1: Raghuram 2026 full text XML", whose reference list contains the DOI.

  A check asking "does the DOI appear in a payload fetched during exec 91's pass" goes **green through C9**. It goes red only when scoped to exec 91's *result-set* payloads, none of which contain the DOI. Garg's DOI (candidate 123) sits in the same two files. For Templer, the FHWA identifier and the report's title appear only in `c9361532746ffec9.json`, a transcription of REF-01005's bibliography written by the session itself, and in none of exec 90's T1–T7 payloads.
- **N1. The search does not exist when its payloads are written.** v1 put `exec_id` into the manifest line that `fetch()` writes. In practice a search is logged after its payloads are fetched:
  - batch 19 fetched T1–T7 between 03:05:59 and 03:07:11 and logged exec 90 at 03:10;
  - it fetched C1–C9 between 03:16:06 and 03:17:18 and logged exec 91 at 03:22.

  All times are UTC, from manifest `retrieved_at` against `select exec_id, created_at from search_executions where exec_id in (90,91)`. Batch 20's driver `scratchpad/session_2026-09-25-…/w03_pinto_mining.sh` names the already-persisted artefact inside its `log-search` call, and reads `exec_id` from `log-search`'s own JSON output. R8 requires logging before *screening*, not before fetching, so this order complies. No manifest line can carry an id that does not yet exist.
- **N2. Payload bytes JSON-escape the DOI's slash.** M1 stores Pinto's DOI as `10.3390\/ijerph18062953` (`grep -o '10\.3390.\{0,2\}ijerph18062953' retrieval-log/session_2026-09-20-…/9a51a98c7235d28f.json`). `dbcore.norm_doi` is `strip().lower()`, so a `norm_doi` substring test misses every DOI in a Crossref or Europe PMC JSON payload. Measured on a scratch prototype: that test called all four DOI-bearing specimen-era attributions unsupported, **including the two correct ones** (117, 121). v1 specified that test. `retrieval_log.normalise_quote`, the letters-and-digits normaliser already applied to extraction quotes, over `decode_artefact` output, finds all of them.
- **The specimen's search→payload edges are derivable from the searches' own verbatim query text**, which R8 made verbatim. A scratch prototype used this rule: a payload belongs to a search in the same session when that search's `query_text` contains the payload URL's host and its longest non-numeric query value, both percent-decoded and normalised by `normalise_quote`. A payload matching two searches is left unlinked. On batch 19 it gives:
  - exec 90 → T1, T2, T4, T5 and T6;
  - exec 91 → C1, C2, C3 and C6;
  - T3, and the shared ERIC file `d03a6fc8797e5f99.json`, match both searches and stay unlinked. That file is a byte-identical empty result (`numFound: 0`) for both T7 and C4, and artefact names are content-addressed;
  - C9 was fetched by a PMCID path with no query string, and links to nothing;
  - exec 99's own `query_text` names M1 by filename.

### §2.2 Decision proposed

This is built together with §5; the two are one mechanism.

**(a) No new manifest fields. This answers F9's question about `role`.** v1 added `exec_id` and `role` to the lines `fetch()` and `record_file()` write.
- `exec_id` cannot be written there, because the search does not yet exist (N1).
- `role` was partly a second home for facts already stored:
  - Its `render` and `derived` values restate `derived`/`derivation_kind`, which `_append_derived` writes on every derived line. On main all five derived lines carry `derivation_kind` `page-render` or `pdf-bibliography`: `cat retrieval-log/*/manifest.jsonl | python3 -c 'import sys,json,collections; print(collections.Counter((r.get("derived"), r.get("derivation_kind")) for r in map(json.loads, filter(str.strip, sys.stdin))))'`.
  - Its `reference-list` value restates "a record fetched for the mined source". The structured manifest `ref_id` (since 2026-09-13) and §5's `mined_ref_id` already say that together.
- What remains of `role`, "this payload is a result of that search", is a fact about the search. It is known only once the search is logged, so v2 writes it there.

`retrieval_log.py`'s writers and signatures are unchanged.

**(b) A junction, `search_execution_artefacts`,** added in §5's migration:

```sql
CREATE TABLE search_execution_artefacts (
  exec_id            INTEGER NOT NULL REFERENCES search_executions(exec_id),
  artefact           TEXT NOT NULL,   -- retrieval-log/<session stem>/<file>: a POINTER into Layer 4
  created_by_session TEXT NOT NULL,
  created_at         TEXT NOT NULL,
  PRIMARY KEY (exec_id, artefact)
) STRICT;
```

It is many-to-many on purpose: one content-addressed file can be the result of two searches, as `d03a6fc8797e5f99.json` is for T7 and C4. It has two writers:
- `log-search --result-artefact PATH`, repeatable, at insert;
- `amend-search --add-result-artefact PATH`, for a search already logged: history, or a payload fetched after logging. The required `--append-note` carries the warrant, and the link is appended to `findings_note` the way amend-search's existing typed setters append their trail.

Both writers refuse unless:
- PATH resolves to a line in a retrieval-log manifest, using the cross-session resolution `derive()` already performs;
- a derived line, followed along `derived_from`, ends at a non-derived line with a 2xx `status`;
- **for a mining search** (`mined_ref_id` set, §5), the payload's manifest `ref_id`, or that of its chain root, equals `mined_ref_id`. Payloads fetched before 2026-09-13 carry no structured `ref_id` and cannot be linked to a mining search; the audit reports them and nothing guesses;
- **for any other search**, its own `query_text` contains the payload URL's host and its longest non-numeric query value, as in the §2.1 derivation, now used as a refusal. A URL with no query string must have its **full path**, percent-decoded, in `query_text`; a final segment such as `fullTextXML` is too generic to identify anything. R8 already demands the query verbatim, so this asks nothing new, and **it is what refuses C9 as a result of exec 91.**

**(c) Two columns on `search_candidates`,** added in §5's migration:
- `surfaced_in`: the path of the payload the candidate appeared in;
- `surfaced_quote`: a verbatim string from that payload, used only when the candidate carries no DOI.

**(d) Writer refusals.**

`add-candidate` requires `--surfaced-in` and refuses unless one of these holds:
- `(exec_id, surfaced_in)` is a row of `search_execution_artefacts`, and the candidate's identifier occurs in the payload. The identifier is the single DOI in `locator` or, failing that, `--surfaced-quote`, which is then required. The match is `normalise_quote(identifier) in normalise_quote(decode_artefact(bytes))`, **not** `norm_doi` (N2).
- `surfaced_in` is a tracked file under `transcripts/`, for a route that was never persisted, as with exec 100. The identifier must occur in that file, and the audit reports the row as `TRANSCRIPT-ONLY`.

`reattribute-candidate` gains `--surfaced-in` and `--surfaced-quote` under the same refusals. With an unchanged `exec_id` it sets only those two columns, and only from NULL to a value; changing a value already set is a reattribution and needs a new exec. Its existing required `--reason` names the judge.

**(e) One audit script, `scripts/audit/provenance_artefact_audit.py`, registered twice.** The precedent is `citation_mining_session` and `citation_mining_backlog_t2`: one script, two registrations.
- **`provenance_artefact_audit`: `--mode surfaced`, blocking, `min_items: 1`.**
  - **Subject:** every candidate carrying `surfaced_in`.
  - **Behaviour:** it re-derives (d) from bytes, and FAILs any row the writer would refuse today.
  - **What it catches that the write-time refusal does not:** a row that reached the DB without the writer, such as hand SQL inside a data migration (§6.6), and a payload changed or removed after the write. `TRANSCRIPT-ONLY` rows are reported.
  - **Non-vacuous from its first run,** because §5.2(d) sets `surfaced_in` on 123, 124 and 125.
- **`provenance_attribution_audit`: `--mode attribution`, advisory, `min_items: 1`.**
  - **Subject:** every candidate *without* `surfaced_in` whose search has linked payloads.
  - **Behaviour:** it FAILs when the candidate's DOI occurs in none of them. It reports two cases without failing: `UNLINKED`, when the search has no linked payload, and `NO-IDENTIFIER`, when the candidate has no DOI.
  - **Why advisory:** its history links are derived by the §2.1 rule, which errs toward not linking, and anything it finds in history is a finding for a batch, not a defect in the PR that lands it.
- **Both registrations:** battery `research`, kinds `[data]`, basis `evidence/discovery-provenance`, the criterion that today reads "No committed enforcer".

**(f) S01 stays.** It caught real drift on 2026-09-18 (candidates 107 and 108) when the two pointers came from different writers. Its PASS line is reworded to say *agreement, not truth*.

**(g) A selftest class, C10.** `run_checks.py --selftest` gains C10, which reports and never fails, on the pattern of C7's `unattributed` count. Every check may declare `compares: record-artefact | record-record | shape`, and the counts of `record-record` and undeclared checks are printed so they can ratchet. This is the brake, at registration time, on the shape being born a fourth time.

**Alternative considered and rejected.** Making staged admissions a view over `search_candidates` would retire the copied edge, which is rule 5's clean form. It would also reopen the owner's 2026-09-26 ruling on `link-admission`, `unlink-admission` and raise-only `results_admitted` within a day of that ruling. Under rule 0 this DR builds on the ruling instead.

### §2.3 Compliance

- **Rule 3.** One schema migration (§5.2b). History gains pointer rows and column values, all through writers (§5.2d). No committed payload or manifest line is edited.
- **Rule 4. v1's sweep was wrong, and v2 changes what needs sweeping.**
  - **The `retrieval_log` writers no longer change.** v1's `git grep -n 'fetch(\|record_file(' scripts skills` found no caller in `skills/`, and it missed prose callers. For the record:
    - the code callers are `scripts/research/page_image.py` (`record_file`) and `retrieval_log.py`'s own `backfill()` (`fetch`);
    - the prose that names `fetch()` is in `references/project-standards.md` (three places) and `architecture/meta-scripts-spec.md`.

    Derive them with `git grep -n -E 'import retrieval_log|retrieval_log\.(fetch|derive|record_file)' -- scripts skills .claude` and `git grep -n -E 'retrieval_log|record_file' -- references/project-standards.md architecture governance`. None of them needs changing.
  - **`add-candidate` gains a required flag.** Sweep with `git grep -n -E 'add-candidate|reattribute-candidate' -- . ':(exclude)transcripts' ':(exclude)scratchpad' ':(exclude)retrieval-log' ':(exclude)scripts/migrations' ':(exclude)data' ':(exclude)tools'`.
    - **Operative callers it finds:** `workplan/2026-09-10-batch-06-runbook.md`, which holds a full `add-candidate` invocation in the live runbook; and, once #159 merges, `scripts/tests/test_db_amend_writers.py`, whose `candidate()` helper stages rows.
    - **Mentions only, with no invocation:** DR-2026-08-19 near line 998 (inside the superseded §12.1), `references/project-standards.md`, and `scripts/tests/test_db_integrity.py`'s S01 message.
    - Frozen records under `sessions/` and `attestations/` are not edited.
  - **The staging skills.** v1 named research-log-manager, citation-miner and gap-driven-mining as skills to sweep. None of them names `add-candidate`, `search_candidates` or the retrieval log: `git grep -l -E 'retrieval-log|add-candidate|search_candidates' -- skills .claude` finds only `skills/adversarial-research_SKILL.md`, `.claude/agents/antagonist.md`, and the contract hook in `.claude/settings.json`. R15's anchor in `research-contract.yaml` names `skills/citation-miner_SKILL.md`, which is where the staging instruction belongs; writing it there is part of this phase.
- **Rule 5.** The junction is the one typed home of a fact held today only in prose: manifest purpose labels and `query_text`. `surfaced_in` points and copies nothing.
- **Rules 7a and 8.** Both audit modes print `EXAMINED`. No new vocabulary is added. The identifier match reuses the one normaliser the repository already applies to quotes.
- **Layers.** A Layer 0 check compares Layer 3 rows with Layer 4 artefacts, which is the direction RC1 says every gate should face. The junction is Layer 1, at research; the writers are Layer 2.

### §2.4 Owner-gating

Code: D-SCHEMA applying canonical methodology, so **DG-REVIEW**. The 2026-09-26 ruling (2) is honoured, not reopened.

### §2.5 Cost and blast radius

Medium: one table, two columns, refusals on four verbs (`log-search`, `amend-search`, `add-candidate`, `reattribute-candidate`), and one script registered twice. `retrieval_log.py` does not change. No rebuild is needed.

### §2.6 What could go wrong

- **The link is still declared by the session.** A session that links a record such as C9 as a "result" of a query defeats the check. The query-text refusal raises the price: a false link now needs a false `query_text`, which R8's verbatim rule already forbids. It does not make a false link impossible.
- **The mechanism types which search a payload belongs to, not which part of the payload a candidate came from.** A single-record fetch, such as a full text or a Crossref work, logged as a non-mining lookup can surface candidates from its reference list. That is mining without `mined_ref_id`, and the DOI is in the bytes either way. The fixture asserts this acceptance (§8), so the gap stays visible.
- **A derived artefact is checked for ancestry, not fidelity.** The chain rule proves that `c9361532746ffec9.json` has a fetched ancestor. It does not prove that the session's transcription of that ancestor is faithful. If the chain rule is relaxed once under deadline, "the candidate appears in the artefact" becomes "the candidate appears in a file the same session wrote". That is RC1 moved one directory down.

---

## §3 Decision 3: RC2. The detector sees the shortcut's real shapes, and derivation becomes the default path

### §3.1 Finding

- **Derivation is opt-in, confirmed.** Most writer functions call no derive-helper, on main and on the branch.
  - **Definitions.** A writer is a top-level def containing INSERT, UPDATE or DELETE SQL. A derive-helper is any of `check_values`, `check_vocab`, `check_declared`, `fk_declared`, `schema_choices`, `check_expression`, `next_ref_id`, `ref_id_high_water` or `live_vocab`, counted one call deep.
  - **Result.** A scratch AST pass gave 32 of 49 on main and 34 of 53 on the branch. The pass is not in the repository, so **do not cite these figures.** Class 6's report line (§3.2c) will compute them.
  - **What the figure means.** A STRICT CHECK still refuses a bad value at write time, so the figure bounds the exposure. It does not count defects.
- **The detector is blind to the common shapes, confirmed.**
  - Run `grep -c 'choices=' scripts/db.py` against `grep -c 'choices=dbcore\.\(schema_choices\|check_values\)' scripts/db.py` (CLAUDE.md rule 8's own pair).
  - Yet `python3 scripts/audit/derived_not_curated_audit.py` examines only a few literals (read its `EXAMINED:` line) and prints `VERDICT: CLEAN`.
  - It cannot see the module-level `_VALID_CONFLICT_STATUS`, `_VALID_ITEM_STATUS` and `_VALID_RUN_STATUS` (`grep -n '^_VALID_' scripts/db.py`; the fourth name that grep lists, `_VALID_DIRECTIONS`, is a legitimate subset, §3.2a). Each of the three **equals** its column's live CHECK (`dbcore.check_values` on `conflicts.status`, `items.status` and `item_audit_runs.status`). All three survive on the branch.
  - It also cannot see `--target-tier choices=range(1, 7)`, which mirrors `target_tier IS NULL OR target_tier BETWEEN 1 AND 6` (`dbcore.check_expression(conn, "search_executions", "target_tier")`), a CHECK that `check_values` cannot parse.
- **"Only after a CHECK exists" is confirmed in the specimen.** `search_executions.engine` has no CHECK. Its vocabulary lives only in a DDL comment (`pubmed|crossref|scholar|biorxiv|medrxiv|consensus|web|registry|manual`), and live rows hold values outside it.
  - **Which DB holds what.** On main the one Internet Archive row is spelled `archive-org`. The batch-20 branch adds `internet-archive` (exec 100, written by batch 20). So both spellings of one index coexist on the branch, and on main only once #159 merges. Derive with `select engine, count(*) from search_executions group by engine` against `data/guidebook.db` and against `$SCRATCH/b20.db`.
  - **The comment probe was re-run for v2** across every table on both DBs. It matched column lines whose comment holds three or more pipe-separated tokens, with no CHECK and an empty `check_values`, and it still finds exactly this one column.
- **The repair is per-column and reactive.** Migration 089 fixed one column after a failure. The header of 091 records that 090 wrote *"A CURATED LIST INSIDE THE MIGRATION THAT WAS MEANT TO RETIRE CURATED LISTS"*, and 091, titled "remaining vocabularies", did not reach `engine`.

### §3.2 Decision proposed

**(a) Widen `derived_not_curated_audit.py`,** which is already registered and blocking, with three classes:
- **Class 3:** a module-level string collection in a writer module that **equals** a live CHECK IN-list. It FAILs. **A subset is printed as `SUBSET`, and never fails.** v1 failed subsets too, which would have been red on main from day one over legitimate business rules. A scratch AST scan of `db.py`, `dbcore.py` and `assess/assess_cell.py` against every live CHECK finds three subsets today, each a deliberate restriction:
  - `_VALID_DIRECTIONS` ⊂ `search_executions.mining_direction`;
  - `_ROW_ONLY_RELATIONS` ⊂ `extraction_relations.relation`;
  - `assess_cell.VALUE_SUPPLYING_ROLES` ⊂ `source_value_extractions.figure_role`.

  Equality matches exactly the three frozensets named in §3.1. The class computes both lists; neither is quoted as a fact.
- **Class 4:** a numeric `choices=`, meaning a `range` or an integer list, that mirrors a `BETWEEN` CHECK, read through `dbcore.check_expression`.
- **Class 5:** a DDL comment that enumerates three or more pipe-separated values on a column with no CHECK. It is **reported, not failed**, because the remedy needs judgment.

**(b) Fix main in the same PR, so it stays green.** Replace the three frozensets and the numeric mirror with `dbcore.check_values` or `schema_choices`. `_VALID_CONFLICT_STATUS` equals both `conflicts.status` and `decisions.status`, so name the column its writer actually writes.

**v1 also deleted the comment vocabulary on `engine`; v2 does not.**
- The comment lives inside the CREATE TABLE text in `sqlite_master`, and SQLite cannot alter it. Removing it means rebuilding `search_executions`.
- That table carries five dependent views (`v_coverage_jurisdiction`, `v_coverage_language`, `v_coverage_branch`, `v_coverage_priority`, `v_source_admission`) and inbound FKs from `search_candidates` and `search_admissions`. Derive: `select name from sqlite_master where type='view' and sql like '%search_executions%'`, plus a `PRAGMA foreign_key_list` scan.
- 096 used the rebuild technique on `search_candidates`, and its own header records that no view, trigger or FK referred to that table. It is not a precedent for this table's blast radius, and no rebuild of `search_executions` is scheduled.
- Class 5 only reports, so the comment does not turn main red.
- The comment goes whenever `search_executions` is next rebuilt for its own reason. A CHECK on `engine` would be such a reason. Its vocabulary is not doctrinal, and live rows are only a sample of it (CLAUDE.md §4). That CHECK is not proposed here.

**(c) Later (phase 4): one write choke point,** `dbcore.write_row(conn, table, row, session, op)`.
- It stamps rows via `stamp_for`, validates every value with `check_declared` and `fk_declared`, then executes.
- Writers move to it one at a time.
- **Class 6, as it will actually work.** At run time it counts raw INSERT and UPDATE statements outside `dbcore.write_row` in each writer module, twice: once on the working tree, and once on `git show origin/main:<module>`. It fails if the working-tree count is higher. **Nothing is stored.** v1 said this ran "on `research_contract_baseline_ratchet`'s pattern", but that check compares a *committed baseline file* with origin/main's copy of it, which is a different mechanism. Class 6 borrows only its base-ref convention: `origin/main` is passed as an argument, and an unreadable base ref exits 2, because absent is not innocent. Class 6 also prints §3.1's writer/derive-helper measure, which it never fails on, so that figure finally has a command.

**A rule-4 trap in (c), named before anyone builds it.** `dbcore._writer_tables()` derives the capture set with a regex over `INSERT INTO <table>` literals in `db.py` and `assess/assess_cell.py` (`grep -n '_INSERT_RE\|_WRITER_MODULES' scripts/dbcore.py`). Moving the INSERTs behind `write_row(conn, "table", …)` removes those literals, and `writable_tables()` goes blind: the `WRITABLE_TABLES` failure, a ninth time. The same commit must make `_writer_tables` read `write_row`'s table argument, with `dbcore --selftest` asserting the capture set is unchanged before and after.

### §3.3 Compliance

- **Rule 8** is the point, and the fix introduces no list.
- **Rule 4.** (b) removes symbols, so sweep with `git grep -n '_VALID_CONFLICT_STATUS\|_VALID_ITEM_STATUS\|_VALID_RUN_STATUS'`. (c) touches `_writer_tables`, handled as above.
- **Rule 7a.** Class 6 computes its baseline from `origin/main` and never stores it.
- **Rule 3.** (a) and (b) need no migration. **This is now true.** v1 made the claim while (b) removed a DDL comment, which needs a table rebuild (F5).
- **Layers.** The detector is Layer 0; the choke point is Layer 1.

### §3.4 Owner-gating

This is code, DG-AUTO or DG-REVIEW. One exception: if class 5 prompts a CHECK on a doctrinal column (tier, population or jurisdiction), the vocabulary is the owner's to set. `engine` is not doctrinal.

### §3.5 Cost and blast radius

(a) and (b) are small: one script and a few db.py lines. (c) has the **largest blast radius in this DR**: every writer in a module of more than 7,000 lines (`wc -l scripts/db.py`). Each writer is migrated separately and fault-injected the way `test_db_amend_writers.py` does it.

### §3.6 What could go wrong

A choke point that validates everything against the CHECK makes the CHECK the only home. The curating then moves from Python lists into schema migrations. Those are written under the same fix-forward pressure (096 was a mid-batch table rebuild) and are immutable once committed (rule 3), so a wrong vocabulary becomes harder to correct than the list it replaced.

---

## §4 Decision 4: RC3. Currency lives at the superseded text

### §4.1 Finding

- **There are more than five stores.** Binding text lives in:
  - DRs (`decisions/*.md`);
  - the append-only ledger (`references/project-standards.md`);
  - `data/decisions/decision_register.yaml`;
  - the `decisions` table;
  - CLAUDE.md, which is edited in place;
  - `governance/research-contract.yaml`, plus its SessionStart copy in `.claude/settings.json`, held equal by the parity check `research_contract_sync`;
  - code docstrings and comments declared as a ruling's "one home" (the 2026-09-26 ruling names `_results_admitted_after`);
  - `sessions/*.md`, which `.ignore` hides.
- **The register stores stopped.** The `decisions` table and the YAML register both end at D-0188 (2026-09-11), while the ledger carries later rulings. Derive:
  - `select max(decision_id), max(decision_date) from decisions`
  - `grep -oE 'D-0[0-9]{3}' data/decisions/decision_register.yaml | sort -u | tail -1`
  - `grep '^DATE:' references/project-standards.md | tail -1` (on main this is a 2026-09-18 entry; the 2026-09-25 and 2026-09-26 rulings exist only on the branch until #159 merges)

  `decisions.supersedes` is `'[]'` on every row: `select supersedes, count(*) from decisions group by 1`.
- **Superseded text was left unmarked in the specimen batch.** The v2 checks refine v1's two instances:
  - **(i)** The 2026-09-26 ruling (1) names DR-2026-08-19 step 7's *"the count must agree exactly"* as superseded for post-insert writes. Batch 20 appended an AMENDED callout to step 4 and **none to step 7** (diff the DR between main and the branch). **The v2 check found this weaker than v1 said:** all of §12.1 already sits under a section-level head, *"SUPERSEDED 2026-09-10 — see `workplan/2026-09-10-batch-06-runbook.md`"*, which calls it "a historical record only", and the runbook does not repeat the sentence. What remains is the gap batch 20's own step-4 callout names: *"a reader who stops here still takes it as the list"*. A reader who reaches line ~910 by grep, which is how this repository is read, meets the sentence with no local mark.
  - **(ii)** The 2026-09-25 ruling (3) supersedes the contract's *"Children/general-population/no-participants = PROXY"* as applied to a facility audit. The ledger says in terms that *"The contract's wording was not edited"*. That line is **injected into every session** by the SessionStart hook (`grep -c 'no-participants = PROXY' .claude/settings.json` prints 1), so the most-read store serves the superseded rule.
  - **A counter-example:** the same 2026-09-26 ruling also names the H05 note in `scripts/tests/test_db_integrity.py`, and batch 20 *did* append a `SUPERSEDED IN PART 2026-09-26 BY OWNER RULING (references/project-standards.md; GAP-051)` block there. The practice happens sometimes. Its marker identifies the ruling by date and gap id, not by anything the ledger holds uniquely.

### §4.2 Decision proposed

**Build no index.** A currency index would be the next store. Currency goes at the text a reader actually meets.

**(a) A ledger trailer, anchored on quotes at both ends.**

```
SUPERSEDES: <target path> :: "<verbatim quote from the target>"
  BY: references/project-standards.md :: "<verbatim quote from the superseding ruling>"
```

- **Normalisation.** Both quotes must occur **exactly once** in their files after normalisation. For each line, strip leading whitespace and one leading run of comment or quote markers (`#`, `>`, `//`, `--`), join the lines with spaces, and collapse whitespace. This lets a quote survive YAML folding, Markdown blockquotes and `#` comment wrapping. Without it, `"nothing updates it thereafter"` occurs 0 times in `test_db_integrity.py`, because a `# ` sits between "nothing" and "updates"; with it, the quote occurs once.
- **`BY` is always required.** v1 keyed markers on "the ledger DATE", but `DATE:` lines are not unique (§1.2b). With `BY` present, every `SUPERSEDES` line names its ruling on its own, including when it sits in a later entry.

**(b) An audit, `scripts/audit/supersession_backpointer_audit.py`.**
- **What it reads:** every `SUPERSEDES` line, in the ledger and in any DR that uses the same trailer. It opens each target with plain file I/O, so `.ignore` cannot hide `sessions/`.
- **It FAILS when:**
  - the target quote occurs 0 times, meaning the target was edited in place, which the append-not-edit practice forbids;
  - the target quote occurs more than once, which is ambiguous;
  - the `BY` quote does not occur exactly once in the ledger;
  - no line containing `SUPERSEDED` or `AMENDED` **and the `BY` quote verbatim** sits in the target quote's paragraph or in the paragraph or blockquote immediately after it. Paragraphs are split on blank lines and on comment-only lines.
- **`EXAMINED`** counts `SUPERSEDES` lines. Today there are none: `git grep -c 'SUPERSEDES:' <ref> -- references decisions` exits 1 on both refs. So until the seeds land, the audit reports NOTHING-IN-SCOPE, and that report is correct (§8).
- **Registration:** battery `governance`, kinds `[governance, synthesis]`, level advisory, `min_items: 1` once the seeds land. Its basis is a new criterion, `cross_stage/doctrine-currency`.

**(c) Seed it with a new, separately dated ledger entry. The 2026-09-25 and 2026-09-26 entries are not touched.**
- **Why a new entry.** v1 appended `SUPERSEDES` lines to those two entries. That is an in-place edit of committed ledger text: the shape this section itself forbids for a target. The ledger's own convention for a retroactive account is a later-dated entry: `grep -n '^CORRECTION' references/project-standards.md` lists them. One example is *"CORRECTION — 2026-09-10. **`v_item_extractions` is DELETED; the ledger entry that names it live stands as written and is superseded here, not edited.**"* So 1c appends `CORRECTION — <PR date>. Back-pointers for the rulings of 2026-09-25 (3) and 2026-09-26 (1), recorded retroactively; the entries themselves stand as written.`
- **The seed lines.** The entry carries up to three `SUPERSEDES` lines. Each quote below was checked to occur exactly once under (a)'s normalisation, against the branch's files:
  1. `decisions/DR-2026-08-19-research-restart-operative-instrument.md :: "the junction rows and the count must agree exactly"`, BY the 2026-09-26 ruling's heading text ``"`search_executions.results_admitted` IS RAISE-ONLY AFTER INSERT."``, whose backticks are part of the quote. The marker is an appended SUPERSEDED-IN-PART callout under step 7. It touches `decisions/`, so an attestation is owed (rule 2).
  2. `scripts/tests/test_db_integrity.py :: "nothing updates it thereafter"`, with the same BY. Batch 20's existing marker lacks the BY quote, so the audit is red on it until the quote is appended to that comment. Code comments are code, and git history is their archive (CLAUDE.md §8).
  3. `governance/research-contract.yaml :: "Children/general-population/no-participants = PROXY."`, BY `"A FACILITY AUDIT'S POPULATION GRADE DOES NOT TURN ON WHETHER ITS AUDITORS WERE DISABLED"`. **This seed is conditional on OQ-6.** The marker has to sit in R13's `hook:` text to reach the injected copy, so it changes the text every session reads. The 2026-09-25 ruling reserved "whether [the contract's wording] should change" to the owner. Recording a supersession the owner stated is rule 0; whether a marker in injected text counts as rewording is the owner's call. If the owner says it does, 1c ships seeds 1 and 2 only.
- **The owner's step inside 1c.** If seed 3 ships, `research_contract_sync` goes red. It is blocking, with kinds `[governance, tooling]`, and it only compares; it never writes (`scripts/generate/research_contract_hook.py`: `--check` gates, `--write` regenerates). The PR stays red until `.claude/settings.json` is regenerated with `python3 scripts/generate/research_contract_hook.py --write`. **Only the owner can run that step:** settings.json is harness configuration, and the classifier blocks agent self-modification (CLAUDE.md §7). The PR description lists it as the owner's step, and the PR is not presented as green until it is done.

**(d) CLAUDE.md rule 0** gains the line: *"→ PARTLY ENFORCED by `supersession_backpointer_audit`, for supersessions a `SUPERSEDES` line names. Naming them is yours."*

### §4.3 Compliance

- **Rule 5.** A back-pointer is a pointer, and nothing is restated.
- **Rule 8.** The supersession list has one home, the `SUPERSEDES` lines, and the audit derives everything else from them. Quotes replace dates as anchors, because dates were not unique.
- **Rule 2.** Seed 1 touches `decisions/`, so an attestation is owed. The ledger itself is not a rule-2 path.
- **Append-only.** No committed ledger entry is edited. One entry is appended.
- **Layers.** Layer 0. The 2026-09-09 layer model does not place the ledger itself, and this is stated rather than assigned.

### §4.4 Owner-gating

The mechanism is D-OP first-of-kind → **DG-REVIEW**. Three questions are the owner's: OQ-4, the relay and backfill question; OQ-5, the two register stores; and OQ-6, the R13 wording, now including whether seed 3 counts as rewording.

### §4.5 Cost and blast radius

Small: one script, a grammar line, one appended ledger entry, two or three markers, and, if seed 3 ships, one settings.json regeneration that the owner runs.

### §4.6 What could go wrong

A `SUPERSEDES` line written by the session that relayed a ruling records that session's reading of how far the ruling reaches. The audit then protects that reading mechanically, so a relay error becomes enforced doctrine, with a green check vouching for a supersession the owner never stated. Anchoring on the ruling's own words (`BY`) narrows this, because the line must quote something the ledger actually says. It does not prevent it.

---

## §5 Decision 5: RC5. The discovery route is typed, and its dual home is settled

### §5.1 Finding

- **The survey holds.** `search_candidates.exec_id` is the only discovery pointer. `search_executions` requires `query_text`, `engine` and `depth_method ∈ {scoping, systematic}`. It has `mining_direction`, but no column says *which* source was mined, and nothing can say "catalogue lookup", "surfaced by a pass", "owner-supplied" or "promoted from the lead index".
- **The workarounds show in `engine`:** `multi-index` (exec 91 is one row carrying five queries), `crossref-deposit`, `pdf-bibliography`, `source_locators` and, on the branch, `internet-archive`.
- **The contract already names the dual home, and forbids adding a writer until it is settled.** From `evidence/discovery-provenance`: *"No committed enforcer … the discovery route is already held by search_admissions … and by citation_mining.connections_produced … DO NOT ADD A WRITER WITHOUT SETTLING THE DUAL HOME FIRST."*
- **The owner has already chosen the event home.** The 2026-09-26 ruling (2) says to log each real discovery step "as a backfill search", which is a `search_executions` row, on batch 17's precedent.
- **R8 cannot see these steps.** The injected R8 reads "Log EVERY query verbatim before screening", and says nothing about a step that is not a query. That is how both GAP-050 steps went unlogged.

### §5.2 Decision proposed

**(a) Settle the dual home, following the 2026-09-26 ruling.**
- **The event home.** `search_executions`, together with its linked payloads (§2.2b), becomes the one record of a discovery event, including mining. A mining pass is a row with `mined_ref_id`, and the payloads it read are linked to it.
- **`citation_mining.connections_produced` is a copy** of what those payloads contain. It retires in **phase 2b**, a PR of its own after phase 2, in this order: readers, then rebuild, then writer.
- **Why the order changes from rule 5's (N5).** The column is `TEXT NOT NULL DEFAULT '[]'` (`PRAGMA table_info(citation_mining)`). A retired writer cannot write NULL, and a new row would carry `'[]'`, which every reader takes as "this pass produced nothing". `dbcore.governing_refs`' own docstring records that failure for `governing_refs`. So 2b includes a 096-shaped rebuild of `citation_mining` that relaxes NOT NULL. The rebuild is cheap:
  - no view, trigger or FK depends on `citation_mining`: `select name from sqlite_master where sql like '%connections_produced%'` returns only `citation_mining`, and a `PRAGMA foreign_key_list` scan finds no inbound FK;
  - migration 067 already rebuilt the table once (`grep -n 'connections_produced' scripts/migrations/067_*.sql`).

  Rule 5 still forbids dropping the column, because committed data migrations INSERT it: `git grep -l connections_produced -- 'scripts/migrations/data_*' | wc -l` (17 at `cf35d441`).
- **The full reader sweep.** v1 listed five readers. Derive the set with `git grep -l connections_produced -- . ':(exclude)scripts/migrations/data_*' ':(exclude)transcripts' ':(exclude)retrieval-log' ':(exclude)scratchpad' ':(exclude)_archived' ':(exclude)audits' ':(exclude)sessions' ':(exclude)versions' ':(exclude)workplan/_superseded'`, plus the `sqlite_master` query above.
  - **Code:** `scripts/db.py`, both `log-mining`'s merge and the mining-status read; and `scripts/tests/test_db_integrity.py` (a comment).
  - **Skills:** `citation-miner`, `bibliography-compiler`, and `adversarial-research`, whose standing containment query and its "not built" note both turn on this column.
  - **Governing prose v1 missed:** `governance/pipeline-contract.yaml`, whose criterion text names the column as a home and must be rewritten when it retires, and `architecture/sqlite-data-layer.md`.
  - **Generated surfaces v1 missed:** `tools/data-atlas.html`, `tools/pipeline-walk.html` and `tools/schema-walkability.html`. Regenerate these with `scripts/regenerate_derived.sh`, and never hand-edit them.
  - **Historical plans v1 missed:** six live files under `workplan/`. They are records of what was planned and are not edited; they are listed so that nobody reads them as current.
  - **Schema text:** `057_baseline_2026-08-12.sql` and `067_…`. These are immutable.
- **Named residual.** `citation_mining.backward`/`forward` are a per-source status that `is-mined` reads, and they overlap "a mining search exists for this source and direction". This DR does not settle that overlap. The clean form is deriving `is-mined` from `search_executions`, which is a follow-on. A refusal that keeps the two in step would be a parity check (rule 5), and is not proposed.
- **Unchanged from v1.** `evidence_sources.derivation_chain` and `search_queries_used` stay unreachable, as the criterion records, and are named for retirement.

**(b) A schema migration, in place.** NNN is the next free number at build time, after 1a's. The migration applied cleanly to a scratch copy of the batch-20 DB (SQLite 3.45.1) with `foreign_keys=ON`. The cross-column CHECK fired on a violating UPDATE, every existing row took the default, and every view still resolved. No rebuild and no view drop are needed.

```sql
ALTER TABLE search_executions ADD COLUMN origin TEXT NOT NULL DEFAULT 'planned'
  CHECK (origin IN ('planned','incidental','adversarial-pass','owner-supplied','lead-index'));
ALTER TABLE search_executions ADD COLUMN mined_ref_id TEXT REFERENCES evidence_sources(ref_id);
ALTER TABLE search_executions ADD COLUMN origin_pass_id INTEGER
  REFERENCES adversarial_passes(pass_id) CHECK (origin_pass_id IS NULL OR origin = 'adversarial-pass');
ALTER TABLE search_candidates ADD COLUMN surfaced_in TEXT;      -- §2.2(c)
ALTER TABLE search_candidates ADD COLUMN surfaced_quote TEXT;   -- §2.2(c)
CREATE TABLE search_execution_artefacts ( … );                  -- §2.2(b), verbatim
```

`origin` is the **initiation** axis: why the step was run. `mining_direction` stays the **method** axis. The two are orthogonal, so no fact gains a second home.

**(c) `log-search` gains** `--origin` (choices via `dbcore.schema_choices`), `--mined-ref-id`, `--origin-pass-id` and `--result-artefact` (§2.2b). It refuses:
- **`mining_direction not in (None, "none")` without `--mined-ref-id`.** v1 wrote "`≠ 'none'`". The column is NULL on 40 of main's 91 rows (`select mining_direction, count(*) from search_executions group by 1`), and in Python `None != 'none'` is true, so v1's condition would have refused every ordinary call that leaves the flag out;
- **`--mined-ref-id` with `mining_direction in (None, "none")`,** because a mined source with no direction is incoherent;
- **`origin` other than `planned` together with any `--target-*` flag.** A lookup targets no tier, which keeps it out of `v_coverage_branch`'s Co-1 count;
- **`adversarial-pass` without `--origin-pass-id`.**

**The prior stays required for every origin.** Today `log-search` refuses a missing `--prior-expectation` on *every* search (`grep -n 'prior-expectation is required' scripts/db.py`). v1 called its "`planned` without a prior" refusal "R8 unchanged", while waiving the prior for non-planned origins. That waiver is the erosion §5.6 names, and it is unnecessary: the existing refusal already accepts an honest sentence, and execs 77, 99 and 100 each carry *"BACKFILL, AND THE PRIOR IS THE ABSENCE OF ONE"*. A non-planned row also states in its `query_text` what was done, as the 2026-09-26 ruling requires ("logged as what it was, not dressed as a designed query").

**(d) History, through writers only.**
- **The writers.**
  - `amend-search` gains `--set-origin`, `--set-mined-ref-id`, `--set-origin-pass-id` and `--add-result-artefact`. The precedent is its existing `--set-target-evidence-type` on main: the value is checked with `dbcore.check_declared` or `dbcore.fk_declared`, the replaced value is appended to `findings_note` after the `|| CORRECTED <date>:` marker, and the required `--append-note` carries the warrant. `--set-mined-ref-id` refuses when `mining_direction in (None, "none")`, and when a different value is already set. `--set-origin adversarial-pass` without a pass id is accepted only here, for history, and only when the note says no pass record exists. The CHECK permits a NULL pass id.
  - `reattribute-candidate` gains `--surfaced-in` and `--surfaced-quote` (§2.2d).
- **The one historical data migration.** It is emitted from a scratch run of those verbs, with the phase-2 session as the named judge (rule 8), and sets only what the rows' own records state:
  - **`origin`:** exec 77 → `incidental` (its note: *"a locator hunt that incidentally surfaced two admissible sources"*). Exec 100 → `adversarial-pass` with a NULL pass id, because batch 19's pass predates `adversarial_passes` (its text: *"run by batch 19's independent adversarial pass"*). Exec 99, the backward pass R2 obliges, keeps `planned`.
  - **`mined_ref_id`:** set on mining rows whose own `query_text` names exactly one REF id that exists in `evidence_sources`. That is 11 of the 24 mining rows on the branch DB. Exec 7 names two sources. Execs 17 and 18 name REF ids no longer in `evidence_sources`, and the FK refuses them. The forward rows 19–28 name DOIs that resolve to no `evidence_sources` row. All of these stay NULL and are reported. Derive with a query over `search_executions` where `mining_direction in ('backward','forward','both')`, extracting `REF-\d{5}` and checking existence.
  - **Result-payload links:** derived by the §2.1 rule over every session with a manifest. Only unambiguous links are written; ambiguous and unmatched payloads are listed in the PR and left unlinked.
  - **`surfaced_in`:**
    - 123 and 124 → `retrieval-log/session_2026-09-20-research-batch-19-pre1990-chain-steinfeld-walter-templer/9a51a98c7235d28f.json` (M1, named by exec 99's own `query_text`);
    - 125 → `transcripts/harness_ca1ae452/subagents/2026-09-20T03-41-13_other_aaddd48c.jsonl`, the transcript exec 100's `query_text` cites, with `surfaced_quote` `provisionsforeld00temp`. That string occurs in the transcript (`grep -c provisionsforeld00temp …` prints 8), and the lookup's response was never persisted.
- **Nothing is rewritten.** No manifest, payload, committed migration or session record is edited.

**(e) The criterion gets a check.** `discovery-provenance`'s `check:` becomes §2's `provenance_artefact_audit`.

### §5.3 Compliance

- **Rule 5.** This settles a named dual home instead of adding a third: the event home is chosen in phase 2, and the copy retires in 2b. The `backward`/`forward` flag overlap is named as a residual, not hidden.
- **Rule 3.**
  - The schema change is additive. Neither new numbered migration needs an `AFTER_DATA` marker of its own. 095's marker (`20260920060857`, batch 19's last data migration) already places every later numbered migration after batch 19's data and before batch 20's on rebuild (`grep -h 'AFTER_DATA:' scripts/migrations/095_*.sql`; `migrate_db.build_plan`). So the phase-2 columns exist before any data migration that fills them is replayed.
  - History changes only through `amend-search` and `reattribute-candidate`, then `emit_batch_sql`, then a data migration. CLAUDE.md §4 forbids hand SQL against a table the CLI can reach, and v1 named no writer for these columns.
  - **v1's reproducibility reasoning was wrong in kind.** v1 said the historical UPDATE is "invisible to the count-only `migration_reproducibility`, visible to `migration_reproducibility_deep`". An UPDATE inside a *committed* data migration is replayed identically by a rebuild, so both checks agree with the committed DB by construction, and neither reports anything. The count-versus-row distinction concerns writes that bypass migrations entirely, such as the scheduled `source-verification` workflow (CLAUDE.md rule 3). Neither check can say whether a correction is *right*. That is carried by the named judge's warrant in `findings_note`, and by §8's demonstrations.
- **Rule 4.**
  - Sweep `connections_produced`'s readers (the list in (a)) in phase 2b.
  - `mining_direction`'s readers are unaffected, because the column stays: `research_batch_dod` R2, db.py, `v_source_admission`, and the prose in `architecture/meta-scripts-spec.md` (`git grep -l mining_direction -- scripts skills governance references architecture .claude`).
- **Rules 7a and 8.** The vocabularies live in CHECKs. `mined_ref_id` is derived from each row's own text, and every row it cannot be derived for is reported rather than guessed.
- **Layers.** The schema is Layer 1 at the research stage; `log-search` and `amend-search` are Layer 2.

### §5.4 Owner-gating

D-SCHEMA → **DG-REVIEW**. One question goes to the owner as OQ-7: whether a non-planned origin can discharge a contract leg. This DR assumes R1's Co-1 leg cannot and R2's mining floor can, which is a methodology reading.

### §5.5 Cost and blast radius

Medium: an additive migration, refusals and setters on existing verbs, and one historical data migration. Phase 2b adds one retired writer, its readers, and a cheap rebuild of a table nothing depends on.

### §5.6 What could go wrong

A typed `incidental` origin makes unplanned discovery cheap and respectable. v2 keeps the prior required, so a session cannot skip it by relabelling, but "no prior was written" is still an accepted prior. A session under time pressure can stop pre-registering queries and "discover" through lookups whose priors all read as absent. R8's discipline would then erode through the door built to record its exceptions honestly. The ratio of non-planned to planned rows per batch is the thing to watch, and a batch can derive it from `origin`.

---

## §6 Decision 6: RC6. Research and the tooling it uses ship apart

### §6.1 Finding

- **The runbook still prescribes one long session.** DR-2026-08-19 §12.2 reads "**Target** (one long session)". The batch-06 runbook that superseded §12.1 prescribes no session shape.
- **The risk has been named since May; it became a header, and then not even that.**
  - Seven DRs carry a "Self-review caveat … `[SELF-AUTHORED — bias risk]`", dated 2026-05-13 through 2026-07-12, and **none after**: `git grep -l 'SELF-AUTHORED' -- decisions | sort`. v1 said "from DR-2026-05-13 onward", which overstated the range.
  - Batch 2 and batch 19 each defer a tooling change as one to make deliberately, not "at the end of a long session". Batch 2 says it about instrumenting the DoD gate; batch 19 says it about `_AMENDABLE`.
- **Batch 20's PR ships rows and tooling together.** Derive:
  ```
  git diff --stat cf35d441 origin/claude/batch-20-audit-cluster-templer-fhwa -- scripts/ schemas/
  git diff --name-only cf35d441 origin/claude/batch-20-audit-cluster-templer-fhwa -- governance/
  ```
  - **Under `scripts/`** (12 files at `fe0dcd17`): `db.py`, `dbcore.py`, `research/emit_batch_sql.py`, `audit/research_protocol_audit.py`, `tests/test_db_amend_writers.py` (new), `tests/test_db_integrity.py`, schema migration `096_candidate_disposition_exhausted.sql`, and five data migrations. `schemas/` is untouched. v1's list missed `research_protocol_audit.py` and `test_db_integrity.py`.
  - **Under `governance/`:** `check-registry.yaml`, which registers the new `test_db_amend_writers` check, and the regenerated `context-map.yaml`.
  - **The `dbcore` helper this DR cites.** The same diff introduces `dbcore.require_reason` and `append_dated_note` (commit `4f41b11b`), the helper §1.2(b) relies on.

  By the batch's own record, that code included:
  - `link-admission`, which was a tautology (§0c #1);
  - `unlink-admission`, which was **"unshippable"**, because the capture path refused its DELETE and its test never passed through capture (§0d);
  - pre-write quote checks that "were vacuous" (§0b).

  The record's own summary: *"Every correctness defect was found by running the code, not by any gate."*
- **S01 itself came from this pattern.** It was born inside the repair step of an adversarial review (`f3434e7d`).

### §6.2 Decision proposed

**(a) A check, `research_tooling_separation`** (`scripts/audit/`).
- **Registration:** battery `governance`, kinds `[data]`, level advisory, `no_floor: 'changeset-scoped — …'` (a declared kind), and the basis is a new criterion, `cross_stage/research-tooling-separation`.
- **Research data:** any path classified `data` by the registry's `kinds:` globs, or any file under `scripts/migrations/` matching `migrate_db.DATA_PATTERN`.
- **Tooling:** any path classified `tooling`, or any path classified `schema` that is not a data migration. That covers numbered migrations, identified by `migrate_db.SCHEMA_PATTERN`, and `schemas/**`.
- **It FAILS** when one changeset contains both.
- **Why the migration patterns are needed.** The kind globs alone cannot separate the two, because `schema`'s glob `scripts/migrations/**` comes first and first match wins. Classified through `run_checks.classify`, PR #159's data migrations land in `schema`, not `data`. The patterns in `migrate_db.py` are the one home of that distinction.
- Scratchpad driver scripts belong to no kind and stay allowed.
- **Named residual:** `governance/check-registry.yaml` is kind `governance`, so a registry entry registering new tooling alongside research rows passes. PR #159 does exactly that. Adding the path to the check would be a curated list, and is not proposed.

**(b) An AMENDED callout, appended under DR-2026-08-19 §12.2.** The target shape becomes a coordinator that dispatches three things in turn:
1. a research session that writes rows only;
2. the antagonist, launched from the coordinator, because a subagent cannot launch it;
3. a data-only repair.

A writer gap met mid-batch is filed as a GAP and handled in one of two ways: the rows stay unwritten, or they are written through verbs the CLI already has. The fix itself ships in a tooling-only PR merged to main, and the batch branch takes it with `git merge origin/main` (rebase is blocked, per CLAUDE.md §7).

**(c) CLAUDE.md §2 gains the rule** with its enforcement line, and `/session-open` records whether the session is a research session or a tooling session.

**(d) This DR's own remediation follows (b) from its first PR:** tooling only, with no research rows. Phase 2's historical data migration corrects existing rows and adds no research. It is still research data by (a)'s definition, so it ships in its own data-only PR after phase 2's tooling PR merges.

### §6.3 Compliance

- **Rule 8.** No list: the kinds come from the registry, and the migration patterns come from `migrate_db.py`.
- **Rule 9.** This means more PRs, each opened last and left unwatched.
- **§8: what reaches the book without it.** Rows vouched for by writers that never went through capture, review or CI (`unlink-admission`), and gates that manufacture agreement (S01 after `link-admission`). The diff-scoped gate reads the check.
- **Layers.** Layer 0.

### §6.4 Owner-gating

The check is code. The callout changes the practice a ratified instrument prescribes, which is D-OP first-of-kind → **DG-REVIEW**, and the owner may prefer to sign it. There is a trade here: in batch 20 an **owner ruling** itself required a mid-batch schema migration (096). Under (a), that ruling would have waited for its own PR. Accepting that latency is the owner's decision (OQ-3).

### §6.5 Cost and blast radius

The code is small. The real cost is latency, because every writer gap becomes a stop-and-merge.

### §6.6 What could go wrong

When every writer gap costs a separate PR and a merge, a batch under deadline stops filing gaps. It writes the missing shape as hand SQL inside its own data migration instead. This check cannot see that, because a data migration counts as research data. It is exactly what CLAUDE.md §4 forbids, because it bypasses every refusal db.py has. `provenance_artefact_audit` in surfaced mode (§2.2e) catches the one instance of this that touches candidate provenance, and nothing catches the rest.

---

## §7 Sequence

**Nothing starts before PR #159 merges.** No phase needs to race #159, and several cannot be built without it:
- **Migration numbers.** On main the highest numbered migration is 095 (`ls scripts/migrations | grep -E '^[0-9]{3}_' | tail -1`), and #159 has already used 096 (`git ls-tree --name-only origin/claude/batch-20-audit-cluster-templer-fhwa scripts/migrations/ | grep -E '/[0-9]{3}_' | tail -1`). A migration built against `cf35d441` would take 096 and collide once #159 merges. Every number here is therefore assigned **at build time, on post-#159 main**. With nothing else landing first, 1a takes 097 and phase 2 takes 098. Re-derive rather than trust this sentence.
- **Rows.** Execs 99 and 100, and the reattribution of 123–125, exist only on the branch (`select exec_id from search_executions where exec_id in (99,100)` returns nothing on main).
- **Rulings.** The 2026-09-25 and 2026-09-26 ledger entries exist only on the branch: `git grep -c '^DATE: 2026-09-2[56]' origin/main -- references/project-standards.md` exits 1, and the same command on the branch prints 2.
- **Code.** `dbcore.require_reason` exists only on the branch (§1.2b).

**RC4 comes first: agreed, but not for the survey's reason.** RC1's fix does not need RC4 to be verified, because §8 verifies it mechanically. RC4 comes first for three other reasons:
1. §5's schema has a foreign key into `adversarial_passes`.
2. RC4's rows, broken down by lens, are the only measure of whether the other fixes change what a fresh reader finds.
3. Nothing else touches interpretive overclaim.

**One override:** RC6's *working rule* governs how RC4 is built, so it applies from day zero, before its check exists.

| Phase | PR (each tooling-only unless marked) | Starts after | Why that dependency | Acceptance (§8) |
|---|---|---|---|---|
| 0 | None. Adopt §6.2(b) and (d) as the working rule for this remediation | Owner's nod; #159 merged | — | n/a |
| 1a | RC4: schema migration (097 if nothing else lands first), three verbs, audit, `SESSION_POINTERS` + selftest, report block, command edits | #159 merged | **Hard:** migration number 096 is taken | Red on batch 20's real rows; green path and same-model line on a fixture and on the real transcripts |
| 1b | RC2 (a) and (b): detector classes 3–5, and the fixes that keep main green. No migration | #159 merged | **Soft:** #159 changes 481 lines of `db.py` (`git diff --stat`), and building against the old file invites conflicts; the frozensets survive it | Red on post-#159 main before (b), green after |
| 1c | RC3: audit, trailer grammar, one new ledger entry, two or three markers. **Owner step:** `python3 scripts/generate/research_contract_hook.py --write`, only if seed 3 ships (OQ-6) | #159 merged | **Hard:** the rulings the seeds anchor on exist only on the branch | Red on the PR's own hunks removed one at a time; green with them |
| 1d | RC6 (a)–(c) | #159 merged | **Soft** | Red on PR #159's range |
| 2 | RC5 + RC1: one schema migration (098 if nothing else lands first), junction, columns, writer flags and refusals, the audit registered twice | 1a merged | **Hard:** FK into `adversarial_passes`; execs 99 and 100 | Refusals on a fixture |
| 2-data | The historical data migration (§5.2d), data-only | 2 merged | RC6: data ships apart | Attribution red on the pre-repair state, green on the repaired state (§8) |
| 2b | `connections_produced` retirement: readers switched, `citation_mining` rebuild relaxing NOT NULL, writer retired, criterion text rewritten | 2-data merged | Needs linked payloads to derive from | Reader sweep empty; rebuild reproduces every other column byte-for-byte |
| 3 | Research batch 21, under all of the above | 1–2b merged | — | Its pass is recorded, closed and disposed; its candidates carry `surfaced_in` |
| 4 | RC2 (c): the choke point, one writer at a time | 3 | — | Capture set unchanged at each step (`dbcore --selftest`) |

**Levels.**
- **RC4's check** is promoted by the criterion in §1.4. It is an engineering step, and not OQ-2, which is withdrawn.
- **RC6's check** stays advisory until OQ-3 is answered and one clean batch has passed it.
- **`provenance_artefact_audit`** is blocking from the start, because it has real subjects on day one (§5.2d) and is green on them by construction.
- **`provenance_attribution_audit`** stays advisory (§2.2e).

## §8 Acceptance: what each mechanism can be shown to do, and on what

The 2026-08-19 RULE forbids an adversarial pass whose subject is a Decision Record, so this DR is not tested by critique. It is tested by CLAUDE.md §1's own question: *could the check have gone red on the defect in front of you?*

v1 claimed each mechanism "goes red on state the repository already holds". For two of them that was impossible. It needed history rewritten or a tool operation that does not exist. v2 says for each mechanism what is shown on committed state, and what is shown on a fixture and why. **Fixtures and scratch copies are what the review itself used to check v1's SQL. Nothing committed is edited to stage a demonstration.**

| Mechanism | Red, shown on | Green, shown on | Cannot be shown on real state, and why |
|---|---|---|---|
| RC4 `adversarial_pass_recorded` | **Committed state:** `adversarial_pass_audit.py --session session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa` on post-#159 main. Batch 20 wrote into six of the RULE's tables, and no pass row exists | **A fixture:** a scratch DB copy and two synthetic transcripts, the reviewer's ending in a findings block, go through record, dispose and close | Batch 20's pass cannot be made green. Its antagonist's final message has no findings block, so `record-adversarial-pass` refuses it. That red is permanent for batch 20 and correct: the pass ran, but was never recorded in a checkable form |
| RC4 served-model rule | — | **Committed state:** the derivation run on batch 20's two real transcripts gives `["claude-opus-5-5"]` for both, so the same-model line prints (§1.1 command) | — |
| RC1/RC5 refusals | **A fixture test** (`scripts/tests/`, fault-injected like `test_db_amend_writers.py`). It uses a scratch DB and a temporary retrieval-log root holding *copies* of batch 19's real C1–C4, C6, C9 and M1 bytes with their real manifest lines. Refused: Pinto under exec 91 with `--surfaced-in` M1 (not linked to exec 91); C9 linked as a result of exec 91 (the query-text rule); C1 as Pinto's payload (DOI absent); C9 linked to a mining search on REF-01006 (manifest `ref_id` is null) | Pinto under a mining search on REF-01006 with M1 linked | The test also asserts one **accepted** case. A *new*, non-mining search whose `query_text` names C9's full path accepts C9 as its result. Pinto's DOI is in C9's reference list, so Pinto is accepted under a search not typed as mining. That is §2.6's second residual, documented rather than hidden |
| RC1/RC5 attribution mode | **Committed state, pre-repair:** `git show cf35d441:data/guidebook.db > $SCRATCH/pre.db`. Apply the post-#159 numbered schema migrations (096, then 1a's, then phase 2's) to that copy with `migrate_db._prepare_body` and `_apply_atomically`, the calls `run_migrations` makes, and apply **no** data migration, so #159's reattribution of 123–125 never reaches the copy. `--schema-only` cannot do this (N12). Then link execs 90 and 91's derived payloads with `amend-search --add-result-artefact` on that copy. **Red on 123 and 124** (exec 91: Garg's and Pinto's DOIs are in none of C1, C2, C3, C6), **green on 117** (exec 90, via T6) **and 121** (exec 91, via C1). 125 reports `NO-IDENTIFIER` | **Committed state, repaired:** post-#159 main plus phase 2 and 2-data. Green on 117 and 121 in attribution mode; green on 123 and 124 in surfaced mode (via M1, linked to exec 99); 125 reports `TRANSCRIPT-ONLY` | 125 cannot go red on real state, because its pre-repair row has no DOI and no `surfaced_quote`. Adding one to the pre-repair copy would be staging history. The fixture covers the no-DOI refusal |
| RC2 classes 3–5 | **Committed state:** post-#159 main before (b). Class 3 equality on the three frozensets; class 4 on `--target-tier`. Class 3 subset lines and the class 5 line on `engine` print and do not fail | The same PR after (b) | — |
| RC3 back-pointer audit | **The seed PR's own hunks, in a scratch working copy.** (1) The seed entry without its markers: red on every seed line. (2) Batch 20's existing H05 marker: red until the BY quote is appended. (3) Seed 1's quoted words altered: red, because the quote is gone | The PR as submitted, `EXAMINED` 2 or 3 | Nothing can go red on today's state: no `SUPERSEDES` line exists anywhere (`git grep -c 'SUPERSEDES:'` exits 1), and NOTHING-IN-SCOPE is the correct report. "Red while the back-pointers are absent" is only meaningful once the lines exist, so the demonstration is the PR minus a hunk |
| RC6 `research_tooling_separation` | **Committed state:** PR #159's range, `cf35d441..fe0dcd17`, reproducible from the two shas after merge: `data/guidebook.db` together with `scripts/db.py`, `scripts/dbcore.py` and migration 096 | Any tooling-only phase of this DR | — |

**The pre-repair and repaired attribution results above were measured on 2026-09-26** by a scratch prototype of the attribution mode over the real batch-19 payloads, applied to copies of main's DB at `cf35d441` and of the branch's DB. They were not produced by the audit, which does not exist yet. The prototype also reproduced N2: with `norm_doi` matching instead of `normalise_quote`, all four DOI-bearing rows went red, including the correct ones.

**A mechanism that cannot be made red on committed state or on a fixture built from committed bytes is not accepted.**

## §9 Owner questions: one sitting

| # | Question | Recommended | Why it is not a session's to answer |
|---|---|---|---|
| **OQ-1** | Is a same-model antagonist an independent pass? Batch 20's was: opus-5-5 on both sides, although the agent file names fable. DR-2026-09-11 has Opus run agonist-antagonist for an enumerated queue only | Require a different model where one is available; record and report where not | D-METH, new methodology: **DG-NON** |
| **OQ-2** | *Withdrawn.* v1 asked whether to promote `adversarial_pass_recorded` to blocking | — | It enforces a requirement the owner already ratified (§1.4), so its level is a rollout step under the registry's own promotion convention. The PR that promotes it tells the owner; it does not ask. The number is kept so v1's cross-references still resolve |
| **OQ-3** | Accept RC6's latency, including owner-ordered schema changes leaving the batch PR, and sign the §12.2 callout? | Yes | It changes a ratified runbook's practice (D-OP first-of-kind, DG-REVIEW, and you may prefer to sign it) |
| **OQ-4** | May a session write `SUPERSEDES` lines for a ruling it relays in its own words? Backfill the ledger, or go forward only? | Yes, with the relayed ruling quoted back to you in the PR. Forward only, plus the specimen seeds, which go in one new dated entry (§4.2c) | How far a ruling reaches is the owner's to say |
| **OQ-5** | The `decisions` table and the YAML register both stop at D-0188 while the ledger continues. Revive them, or retire both and name the ledger the single home? | Retire; rulings actually land in the ledger | **v1's stated authority was wrong.** `decision-protocol.md` §2.4's always-DG-NON list has ten items, and the register is not among them. By §2.2 this is D-OP, and a store with material consequence is upgraded to DG-REVIEW by §2.3. It is asked anyway for two reasons. Retiring the store amends `decision-protocol.md` §5, which names the YAML register "canonical" and which you ratified. And two scripts read the register: `scripts/doctrine_recheck.py` and `scripts/decision_capture.py` (`git grep -l decision_register -- scripts`) |
| **OQ-6** | Reword the contract's R13 ("no-participants = PROXY") after the 2026-09-25 ruling (3)? And does a SUPERSEDED marker placed in R13's injected text count as the rewording that ruling reserved to you? | Your call on the wording, as that ruling reserved it. On the marker: it is not a rewording, because it records your stated supersession and changes no rule text. If you say it is, seed 3 waits (§4.2c) | Reserved by the ruling |
| **OQ-7** | Can a non-planned discovery discharge R1's Co-1 leg or R2's mining floor? | R1 no, R2 yes | A methodology reading of the contract, with a doctrinal flow-through into Co-1 coverage. D-METH, upgraded to **DG-NON** by §2.3 |
| **OQ-8** | Widen RC4's subject beyond the 2026-08-19 RULE's limb-(a) table list, to any row a batch wrote (terms included)? The TERM-089 ruling came out of batch 20's pass | Yes | The RULE's scope is the owner's directive. **The check as specified in v2 implements only the RULE's list** (§1.2d), so this question is genuinely open. A wider scope would also have to handle `connection_targets`, which has no session column |

## §10 Reversal

- Each decision can be reversed on its own by a later DR.
- A check is quarantined by moving its entry to the registry's `quarantine:` list.
- The callouts and the ledger entry are appended, so reversing one means appending another.
- **Schema is the exception.** It is additive, but once a data migration INSERTs into the `adversarial_*` tables, into `search_execution_artefacts` or into the new columns, rule 5 forbids dropping them. Reversal then means retiring the writer and writing NULL going forward. That is cheap in behaviour and permanent in schema, and the owner should ratify knowing that. The `citation_mining` rebuild in 2b is the one step that cannot be un-done by a later rebuild without re-imposing NOT NULL over rows that by then carry NULL.

## §11 What this does not do

- **Re-diagnose.** §0.2 confirms the six root causes and adds facts only.
- **Touch doctrine or content.** It leaves tier definitions, the population taxonomy, the CRPD posture and every determination alone.
- **Reopen the 2026-09-25/26 rulings.** `link-admission`, `unlink-admission` and raise-only `results_admitted` stand, and the ledger entries that record them are not edited.
- **Rewrite history.** No committed migration, commit message, session record, retrieval-log payload or manifest line is edited. History gains pointer rows, two column values per corrected row, and one appended ledger entry, all through writers or append-only practice.
- **Retire any store.** OQ-5 is the owner's decision.
- **Settle `citation_mining`'s `backward`/`forward` flags.** They are named as an overlap with mining searches (§5.2a) and left for a follow-on.
- **Mechanise the RULE's limb (b)** (synthesis artifacts), or widen RC4's scope before OQ-8 is answered.
- **Split search, screening and grading into separate sessions.** Blind-then-compare grading (DR-2026-08-19 §7) stays available but is not mandated.
- **Create a workplan.** To land, the status line at the top of this document updates to RATIFIED, and a register row is added, after the owner answers §9 and after PR #159 merges.
