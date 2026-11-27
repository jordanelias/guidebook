# CLAUDE.md audit: saliency and efficacy, with a proposed replacement

Written 2026-11-26 by a read-only Opus-class auditor for the owner's approval. Repository read at `origin/main` `71b7c58`. Nothing in the repository was edited. The proposed file is `/tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/CLAUDE.proposed.md`. Line numbers ("L") are of the current `CLAUDE.md` at `71b7c58`; they drift, so locate by the quoted text.

**Owner's instruction (typed, 2026-11-26):** "please have Opus audit claude.md for saliency and efficacy. ensure we strip out all extraneous stuff like change logs and version discussion etc. we want to make sure that claude.md points correctly but also contains some strict rules of operation for us".

**Approval.** The ledger entry "Owner statements 2026-11-20 (third)" carries ACTION (1): "Do not rewrite `CLAUDE.md` until the owner approves the content above". The whole proposal therefore waits for the owner. Within it, OWNER-ONLY marks a change to the goal sentence, rule 0, rule 9, the tier and Co-1 definitions or the layer model (that entry: "The owner approves the goal sentence, rule 0, rule 9, the tier and Co-1 definitions, and the fate of the layer model"). DELEGABLE marks process wording, traps and command lists, which that entry says a session may reorder and reword. **Every OWNER-ONLY block is byte-identical in the proposed file.** The OWNER-ONLY changes are listed separately in section 2b and are not applied.

**Inputs reconciled.** `scratchpad/adjudication.md` (ADJ-), `scratchpad/adjudication-2.md` (ADJ2-), `scratchpad/antagonist-1.md` (its attack on ADJ-) and `scratchpad/ecosystem-census.md`. Where the antagonist overturned the first pass, this audit follows the antagonist: the seven-rank authority order of ADJ-04 is not applied (it ranks delegated resolutions above doctrine and CLAUDE.md, against the owner's "as always refer to doctrine/mission/claude.md etc for guidance as required", ledger "Owner statements 2026-11-25"), and the synthesis floor uses "Opus-class or above", not a closed list.

## Size, measured (re-run; do not trust the figures)

| Measure | Command |
|---|---|
| Current words | `wc -w < CLAUDE.md` (5809 at `71b7c58`) |
| Proposed words | `wc -w < /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/CLAUDE.proposed.md` (4040 when written) |
| The rewrite spec's target (unratified, not binding) | `echo $(( $(git show origin/main:CLAUDE.md \| wc -w) / 4 ))` (1452) |
| Words in OWNER-ONLY verbatim blocks | about 800 (goal, simplicity sentence, the three things, rule 0, rule 9, the layer quote, the tier and Co-1 lines) |

The quarter target cannot be met while rules 0 to 10, §3, §7 and §8 stay in CLAUDE.md: the OWNER-ONLY text alone is more than half of it. It is reachable only by the rewrite spec's move of those rules into a separate working-rules file, which the same ledger entry reserves to the owner (item O-09). This proposal keeps every rule in place and every number unchanged, and cuts history, proofs, duplicates and stale claims.

## Why the numbering is kept

Rule and section numbers are cited by number across the tree, including immutable migrations, executable scripts, the check registry, slash commands and skills. Sweep command (approximate: a bare "rule N" can belong to another numbering): `git grep -n -E 'CLAUDE\.md[^a-z]*(rule|section|§)|CLAUDE.md §|rule [0-9]+[a-c]?\b' -- scripts governance skills .claude decisions architecture | wc -l` (938 lines at `71b7c58`). The tally by token is in `/tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/rulecallers_tally.txt`. Several earlier renumberings already broke callers that were never repaired (section 3e). Any renumbering repeats that. The proposal keeps rules 0, 1–7, 7a, 8–10, sections §1–§9 and the labels §5(a), (b), (c).

Two callers parse CLAUDE.md mechanically, and both still pass on the proposed file (emulated, since the repository was not edited):
- `scripts/audit/claude_md_spine.py` (blocking): exactly one line matching `^\s*SPINE:` and equal to `governance/pipeline-contract.yaml` `stages:`. Emulated: one line, equal.
- `scripts/tests/test_db_amend_writers.py` (T126-30) reads `\bT(\d)[–-]T6\*\* the regulatory stratum` from CLAUDE.md. Emulated: matches, tier 4. **This is a second content pin that no document mentions;** the tier line must keep the literal "**T4–T6** the regulatory stratum".

---

## 1. Summary table

| Section / rule | Verdict | Reason (evidence in section 2) |
|---|---|---|
| Goal: goal sentence (L5-6) | KEEP verbatim | OWNER-ONLY |
| Goal: simplicity sentence (L8) | KEEP verbatim | Owner's words, 2026-11-25 (seventh) |
| Goal: the three things (L10-18) | KEEP verbatim | Spec item 2; item 3 is Co-1 doctrine |
| Goal: authority sentence (L20-23) | KEEP verbatim | Correct as far as it goes; the replacement order of ADJ-04 was found false by the antagonist. Alternatives in O-07 |
| Goal: correction-history rule (L25-27) | TIGHTEN | C-02 |
| §9 doctrine paragraph (L527-531) | MOVE to Goal | C-01: the spec's goal section carries "a thinking tool, not an authority"; first screen |
| §1 run-first block | TIGHTEN | C-03 to C-07: SessionStart already runs ensure-deps; preflight.sh already runs the selftest; one false claim; one duplicate trap merged |
| §1 agents and commands | KEEP, tighten | All seven exist under `.claude/` |
| §2 intro | TIGHTEN | C-08 |
| Rule 0 | KEEP verbatim | OWNER-ONLY; proposed deletion of its Proof in O-01 |
| Rule 1 | TIGHTEN | C-09: `ci.yml:257` is a wrong line pointer |
| Rule 2 | TIGHTEN | C-10: only `.md` files are gated; attestation file name is `<dir>_<stem>.json` |
| Rule 3 | KEEP | Enforcement claim verified |
| Rule 4 | TIGHTEN, MERGE in 7a's prose-caller sweep | C-12 |
| Rule 5 | TIGHTEN | C-13 |
| Rule 6 | TIGHTEN | C-14: SubagentStop hook already runs the preserver |
| Rule 7 | TIGHTEN (keep number) | C-15: proof deleted; callers cite "rule 7" |
| Rule 7a | TIGHTEN | C-16: proof is a correction history (forbidden by L25-26) and carries a now-false claim |
| Rule 8 | TIGHTEN | C-17: both `--tier` examples are stale; proof deleted |
| Rule 9 | KEEP verbatim | OWNER-ONLY; stale enforcement sentence and narrative in O-02, O-03 |
| Rule 10 | TIGHTEN | C-19: Batch 20 anecdote deleted |
| §3 layer quote | KEEP verbatim | OWNER-ONLY (fate of the layer model, O-08) |
| §3 spine line, stage table | KEEP verbatim | Pinned by `claude_md_spine`; table cited by `governance/stage-map.yaml` |
| §3 surrounding prose | TIGHTEN | C-20 to C-24; one internal contradiction ("base is not a stage") removed |
| §4 | TIGHTEN | C-25 to C-29: owner's 2026-11-21 hand-correction exception added; duplicate probe replaced by pointer; contradictory "two refusals" sentence fixed |
| §5(a) | KEEP | Verified (`NOTHING-IN-SCOPE` in `run_checks.py`) |
| §5(b) | TIGHTEN | C-30: names `index.html`, which is not at the root |
| §5(c) | TIGHTEN | C-31: narrative condensed; duplicate of Goal item 1 deleted |
| §6 tier line, marker line, Co-1 warrant | KEEP verbatim | OWNER-ONLY; changes owed by owner words in O-05, O-06 |
| §6 cell states | TIGHTEN | C-32: point at the CHECK; owner ruling OR-1 |
| §6 ICF frame, synthesis floor | TIGHTEN | C-33 to C-35: "axis" vocabulary dropped; floor contradicts owner 2026-07-25 |
| §6 key rulings | TIGHTEN (point, not restate) | C-36 |
| §7 traps | TIGHTEN | C-37 to C-43: 1100 → about 475 words; one stale enforcement claim corrected; two duplicates replaced by pointers |
| §8 | TIGHTEN | C-45: sign-off list narrower than decision-protocol §2.4, replaced by a pointer |
| §9 | TIGHTEN, re-point | C-46: "What to do now" routes to a spent plan; two "Entity model, ICF frame" files are history; architecture file is the claude.ai-surface one |

---

## 2. Itemised change list

Convention: a short current text is quoted whole; a long one is quoted by its first and last words with its line range. Every DELEGABLE item below is applied in the proposed file.

### 2a. DELEGABLE changes (applied in the proposed file)

**C-01 — Move the doctrine paragraph from §9 into the Goal section.**
- Current (L527-531): "A reference on architecture, accessibility and built-environment standards centred on **disabled people**. Fixed doctrine: a **thinking tool and advocacy project, not an authority** — … *inclusion of persons with disabilities*."
- Proposed: the same text, verbatim, placed after the three things never to be got wrong.
- Reason: the rewrite spec's section 1 puts "a thinking tool, not an authority" with the goal. Doctrine that frames every task belongs on the first screen, not at the foot of the file.
- Breaks: none (no caller cites §9 for this paragraph; swept with `git grep -n -E 'CLAUDE\.md.{0,6}(§ ?9|section 9)'`).
- Class: DELEGABLE (a move, no rewording). Confidence: high.

**C-02 — Tighten the correction-history rule.**
- Current (L25-27): "**Correction histories do not live here.** When a sentence in this file is found wrong, fix the sentence and put the account of the error in the commit message; `git log -p CLAUDE.md` is the record. This file is loaded into every turn, so every line of narrative is paid for on every turn."
- Proposed: "When a sentence in this file is found wrong, fix the sentence and put the account of the error in the commit message; `git log -p CLAUDE.md` is the record. This file is loaded into every turn, so every line is paid for on every turn."
- Reason: the bold heading repeats the sentence after it.
- Breaks: none. Class: DELEGABLE. Confidence: high.

**C-03 — Replace "run ensure-deps first" with the fact that SessionStart runs it.**
- Current (L33-35, L61-66): "`bash .claude/hooks/ensure-deps.sh # pydantic + jsonschema. DO THIS FIRST`" … "**A fresh container has no `pydantic`, … it pins `PyYAML==6.0.3` against the Debian-managed 6.0.1, pip refuses to uninstall it, and nothing lands. Install packages individually. `governance/check-registry.yaml`'s `batteries:` is the one home of the dependency list."
- Proposed: "SessionStart runs `.claude/hooks/ensure-deps.sh`, which exits 0 even when it fails, and without `pydantic` the governance battery is red on untouched `main`: check `python3 -c 'import pydantic, jsonschema'` before believing a red result. **Never `pip install -r requirements.txt`** (its PyYAML pin cannot replace the system copy, so nothing lands); install packages individually. The dependency list's one home is `governance/check-registry.yaml`'s `batteries:`."
- Reason: `.claude/settings.json` SessionStart[0] already runs `ensure-deps.sh` (second hook of the group). The version numbers are volatile facts (rule 7a). The import check is the decision a session actually has to make.
- Breaks: none. `.claude/commands/orient.md` still runs the script, harmlessly.
- Class: DELEGABLE. Confidence: high.

**C-04 — State when `/session-open` must run.**
- Current (L57): "`/session-open` to open a batch".
- Proposed (first sentence of §1): "`/orient` starts any session; run `/session-open` before the first Bash call of a batch (§7)."
- Reason: the PostToolUse hook files every Bash call under whatever `scratchpad/CURRENT` names (`.claude/hooks/record-command.py` `open_session()`). "Before the first Bash call" is stated only in `.claude/commands/session-open.md`. It is the one instruction that must precede the first action, and CLAUDE.md did not carry it.
- Breaks: none. Class: DELEGABLE. Confidence: high.

**C-05 — Collapse the three gate commands to the one that runs both.**
- Current (L42-46): "`scripts/preflight.sh` … `python3 scripts/run_checks.py --changed-from origin/main --explain` … `python3 scripts/run_checks.py --selftest # AFTER ANY RENAME — see rule 4`".
- Proposed: "`scripts/preflight.sh # THE gate: registry selftest, then the checks your diff vs origin/main warrants`" and "`scripts/preflight.sh --explain # the same, with why each check was or was not selected`".
- Reason: `scripts/preflight.sh` runs `run_checks.py --selftest`, then `run_checks.py --changed-from "$BASE"` with any extra arguments passed through (read: the body after `echo "===== preflight: registry selftest ====="`). The three lines were one command written three ways.
- Breaks: none. `.claude/commands/batch-done.md:134` cites §1 for the diff-scoped gate, which remains.
- Class: DELEGABLE. Confidence: high (the `--explain` pass-through was read in the script, not run).

**C-06 — Correct a false claim about the selftest.**
- Current (L68-70): "**`--changed-from` does not run `--selftest`, and the selftest is where a rename fails.** … CI runs the selftest and your local gate does not."
- Proposed: "A bare `run_checks.py --changed-from` skips the selftest, where a rename fails (rule 4)."
- Reason: the local gate CLAUDE.md names first, `preflight.sh`, runs the selftest.
- Breaks: none. Class: DELEGABLE. Confidence: high.

**C-07 — Merge the `--all` trap into §1.**
- Current (L485-489): "**`run_checks.py --all` over `--changed-from origin/main` is the expensive default.** … not to re-confirm a result the scoped run already gave."
- Proposed: in §1, "`--all` is for a corpus-wide question only."
- Reason: duplicate of §1's own `--battery` paragraph, which it cites ("§1 says what it selects").
- Breaks: none. Class: DELEGABLE. Confidence: high.

**C-08 — §2 intro.**
- Current (L76-77): "Each rule carries what enforces it. **"NOT ENFORCED" means you are the gate** — no check will catch you, and the unenforced rules are where the defects recorded below actually occurred."
- Proposed: "Each rule names what enforces it. **"NOT ENFORCED" means you are the gate.**"
- Reason: "the defects recorded below" are the Proof narratives this proposal deletes.
- Breaks: `governance/check-registry.yaml:883` cites "the state CLAUDE.md §2 calls 'you are the gate'", which remains. Class: DELEGABLE. Confidence: high.

**C-09 — Rule 1's enforcement pointer.**
- Current (L90): "→ Enforced by `check_commit_msg.py`, **push events only** (`ci.yml:257`) — skipped on every PR."
- Proposed: "→ Enforced by `scripts/ci_helpers/check_commit_msg.py` on **push events only** (the `commit-msg` job of `.github/workflows/ci.yml`); never on a PR."
- Reason: line 257 is not the job (`grep -n "if: github.event_name == 'push'" .github/workflows/ci.yml` prints 265; the census found the call at 274). A line number is a volatile fact.
- Breaks: none. Class: DELEGABLE. Confidence: high.

**C-10 — Rule 2's scope and file name.**
- Current (L92-96): "Touching `references/connection-reasoning/`, `decisions/` or `sessions/` needs `attestations/<slug>.json` … **No gate reads the free text for meaning**, which is where attestations have actually caught deviations."
- Proposed: "A changed `.md` file under `references/connection-reasoning/`, `decisions/` or `sessions/` needs `attestations/<dir>_<stem>.json`, valid against `schemas/attestation.schema.json`. → … **No gate reads the free text for meaning**; you are its gate."
- Reason: `scripts/audit/adherence_log_audit.py` `SYNTHESIS_PATH_RE` matches `.md` only, and `_attestation_path_for()` names the file `<dir>_<stem>.json`.
- Breaks: none. Class: DELEGABLE. Confidence: high.

**C-11 — Rule 3.** Current (L98-100) restated the write path; proposed points to §4 ("Migrations only, by the write path of §4"). Enforcement sentence kept. Reason: one home for the write path. Breaks: `.claude/settings.json` `_permissions_comment` quotes "Never write data/guidebook.db directly. Migrations only." — still present. DELEGABLE. High.

**C-12 — Rule 4: delete the proof; absorb the prose-caller sweep from 7a.**
- Current (L107-108): "*Proof: migration 064 exists because 063 swept eight Python readers and six skills and missed `v_item_provenance`; …*". Current (L157-160, in 7a): "**The third shape has no gate at all: a PROSE CALLER restating a checked fact.** … grep `governance/`, `references/` and `architecture/` for sentences repeating it".
- Proposed: "**A VIEW IS A CALLER. So is a skill, the check registry, and prose.** … After changing any checked value or name, `git grep` `governance/`, `references/`, `architecture/`, `scripts/`, `skills/` and `.claude/` for sentences restating it."
- Reason: the proof is history with hand-typed counts; the sweep instruction is a rule-4 action that sat inside 7a's proof. `scripts/`, `skills/` and `.claude/` are added because this audit found prose callers there (section 3).
- Breaks: none; "treat a 0-row object as unproven, not clean" (quoted by `scripts/dbcore.py:1837`) is kept. Class: DELEGABLE. Confidence: high.

**C-13 — Rule 5: tighten.** Current (L112-119) "**A column a committed data migration INSERTs can be dropped only by a schema migration the replay plan orders after every one of them** (`migrate_db.build_plan()`; …) … writer-retire, reader-retire, NULL forward." Proposed: same content in plainer order ("then retire the writer, then the readers, then NULL forward"). `migrate_db.build_plan` and `AFTER_DATA` verified in `scripts/migrate_db.py`. DELEGABLE. High.

**C-14 — Rule 6.**
- Current (L123-124): "A read-only subagent writes nothing at all, so its entire workings live in `~/.claude/projects`, which a fresh clone does not inherit."
- Proposed: "`python3 scripts/preserve_transcripts.py` copies transcripts out of ephemeral `~/.claude/projects`, which a fresh clone does not inherit (the SubagentStop hook runs it for subagents; committing is yours)".
- Reason: `.claude/settings.json` `SubagentStop` already runs the preserver. The decision left to the session is the commit.
- Breaks: none. Class: DELEGABLE. Confidence: high.

**C-15 — Rule 7: delete the proof.** Current (L133-134): "*Proof: this file carried three figures under a paragraph warning they were dated. …*". Proposed: deleted; the rule text is kept, with "in derived documents" dropped because L132 already says "every volatile fact". Callers citing "rule 7" (`git grep -n 'rule 7\b'`) keep a rule 7. DELEGABLE. High.

**C-16 — Rule 7a: delete the proof.**
- Current (L144-156): "*Proof, all measured 2026-09-16 — and re-derive rather than trust these … both now reading "derive the counts, never quote them".*" and (L160-162) "*Proof: the 2026-09-16 floor ratchet … when it held 2.*"
- Proposed: deleted. The rule's operative text (command not result; the "wrong tomorrow" test; the list of shapes) is kept.
- Reason: L148-150 is a correction history ("This sentence first said 'eleven … three of them BLOCKING' … The true figure was four"), which L25-26 forbids in this file. It also says `citation_mining_session` "is blocking"; the registry says `level: advisory` (read with `yaml.safe_load` on `governance/check-registry.yaml`). The proof is now itself wrong.
- Breaks: none. Class: DELEGABLE. Confidence: high.

**C-17 — Rule 8: delete two stale examples and the proof.**
- Current (L177-179): "`add-source --tier` asking an operator to retype what `derive_tier(evidence_type, scope)` already knows is the anti-pattern in one line". Current (L192-195): "Also outstanding: `amend-source --tier` asking for a value the machine can derive. A hand-typed figure in the registry's `note:` … finds two shapes only)." Current (L180-186): "*Proof: `dbcore.WRITABLE_TABLES` was a curated list … the burden of proof moved to the exclusions.*"
- Proposed: deleted; the enforcement list is kept, with `derived_not_curated_audit.py` named as the judge.
- Reason: both examples are false today. `scripts/db.py` `add-source --tier`: "optional: the tier is derived from --evidence-type and --scope; a value that disagrees is refused". `amend-source --tier`: "the tier moves to the one value the ratified ladder derives … a value that disagrees is refused. The tier is never set on its own." The registry-grep sentence is rule 7a's case and is covered there.
- Breaks: none. Class: DELEGABLE. Confidence: high.

**C-18 — Blank line between rule 8 and rule 9.** Current: L195 runs straight into L196 ("**9. Do not watch PRs…"), so rule 9's heading reads as part of rule 8's paragraph. Proposed: one blank line. Rule 9's text is unchanged. DELEGABLE (whitespace). High.

**C-19 — Rule 10.** Current (L218-221): "Batch 20 shipped `link-admission` (a tautology), … not by any gate.'" and (L223-224) "(advisory; DR-2026-09-26-recurring-defect-shapes-remediation.md section 6, RC6) … named, not patched." Proposed: anecdote deleted; "(advisory)" and the named residual kept in one sentence. DELEGABLE. High.

**C-20 — §3: delete the retired-map note.** Current (L240-241): "`layer-N` in a frozen record is the retired `pipeline-map.yaml`'s old table bucketing, not this." Proposed: deleted. Reason: history about frozen records; the file is under `_archived/`. DELEGABLE. High.

**C-21 — §3: delete the second spelling of the stages.** Current (L248-250): "Owner's own formulation, 2026-08-27: *"you research slugs, evidence research, judge evidence, synthesize judgments, specify syntheses, and render specifications."*" Proposed: deleted. Reason: the next line of the file says "Never spell the stages out a second time in this file"; the ledger keeps the quote. DELEGABLE. Confidence: medium (it removes an owner quotation from CLAUDE.md, not from the record).

**C-22 — §3: point at the stage map.** Current (L264-265): "**Derive any table-to-stage assignment against these seven stages**; every assignment written before 2026-08-27 predates them." Proposed: "Table-to-stage judgments live in `governance/stage-map.yaml`." Reason: "seven" is a hand-typed count of the spine; the date clause is history; the stage map is the home (its header: "which pipeline stage each table belongs to"). DELEGABLE. High.

**C-23 — §3: remove an internal contradiction.**
- Current (L270): "Convention: `base` is not a stage, so a view reading one stage plus base crosses nothing." Against L249-250: "`base` is the vocabulary layer the machine gates as a stage."
- Proposed: "Every stage points into `base`, so a view reading one stage plus `base` is not counted as crossing." (ADJ2-C9 item 1.)
- Reason: one file, two answers; `claude_md_spine.py`'s own docstring records the same contradiction having stood in CLAUDE.md for thirteen days once before.
- Breaks: `governance/stage-map.yaml:35` cites §3 for "the most protected" object; kept. Class: DELEGABLE. Confidence: high.

**C-24 — §3 re-entrancy, condensed** to one sentence (L272-274). DELEGABLE. High.

**C-25 — §4: add the owner's hand-correction exception.**
- Current (L294): "**Do not hand-write SQL against a table the CLI can reach.**" (no exception).
- Proposed, appended: "Exception (owner, 2026-11-21): a qualitative judgment or wording cell may be corrected by hand in a data migration, with the old value, the new value, the reason and the session recorded in the migration header and in the gap's resolution. Ask the owner before treating any other kind of column as qualitative."
- Reason: owner's words, ledger "Owner statements 2026-11-21": "I think GAP-368 points towards Claude having permission to hand edit as required for specific columns" / "We just need to ensure that you make transparent and record your hand fixes". Its ACTION (1) names the migration header and the gap resolution; ACTION (2): "Do not extend this to a column outside the owner's meaning of 'qualitative'; ask." Without the sentence, CLAUDE.md contradicts a live owner ruling. The recorder's list of excluded columns is an `[ASSUMPTION]` and is not written as a rule.
- Breaks: none. Class: DELEGABLE (settled by owner words; ADJ2-C5). Confidence: high.

**C-26 — §4: the "two refusals" sentence.**
- Current (L299-304): "**Two refusals are deliberately absent and must stay absent:** `add-population-match` does not enforce uniqueness … — and `insert_economics_entry` refuses `--year`/`--journal` for an entry carrying a `ref_id`, … (`grep -n 'def insert_economics_entry' scripts/db.py`; locate by symbol, never by line number)."
- Proposed: "One refusal is deliberately absent and must stay absent: `add-population-match` does not enforce uniqueness on (ref_id, population), so a dissenting adversarial grade lands as a second row and divergent grades read as a contest."
- Reason: the second clause describes a refusal that is present (and, through argparse, unreachable), so the sentence contradicts itself. The economics behaviour is documented at its home, `scripts/db.py` `insert_economics_entry` ("THE DUAL-HOME REFUSAL, and a note on WHICH LAYER ENFORCES IT").
- Breaks: `scripts/db.py:7394` ("which CLAUDE.md §4 lists among the refusals", for `evidence_population_match`) still holds. Class: DELEGABLE. Confidence: medium.

**C-27 — §4 schema shape.** Current (L309-310): "More columns mean more specificity, and specificity is what keeps later stages from parsing prose. Run … ; it reports the cells that hold two things." Proposed: the rationale sentence and the gloss deleted; the rule and the command kept. DELEGABLE. High.

**C-28 — §4 ref_id.** Proposed adds `python3 scripts/db.py next-id ref` (verified: `next-id` choices include `ref`) beside `dbcore.next_ref_id(conn)`. DELEGABLE. High.

**C-29 — §4 emptied foreign key: history out, duplicate probe out.**
- Current (L323-329): "`specifications` was in this state after migration 071 re-keyed it … Whether a determination can be written today is a question for the derivation below …" and the 9-line probe (L330-340).
- Proposed: "The refusal comes only at INSERT, so the schema looks healthy, a rebuild reproduces it and every gate stays green. Derive the UNWRITABLE set before planning any write (the `db-census` agent; its file holds the probe), and never quote it."
- Reason: the 071 account is history; the probe is a byte-for-byte second home of `.claude/agents/db-census.md` (lines 30-39, "The unwritable-table probe").
- Breaks: none found (`git grep -n -E 'CLAUDE\.md.{0,30}(probe|snippet|derivation below|UNWRITABLE)'` finds no caller of the CLAUDE.md copy). Class: DELEGABLE. Confidence: high.

**C-30 — §5(b).** Current (L350-351): "See rule 7. Counts in this file, in `index.html`, in manifests and in audits have all drifted." Proposed: "See rules 7 and 7a." Reason: history; root `index.html` does not exist (`git ls-files | grep -E '^index\.html$'` is empty; only `_archived/` copies). DELEGABLE. High.

**C-31 — §5(c).**
- Current (L353-361): "On 2026-08-19 all five sources in the first research batch were stored with **invented co-authors** … (owner, 2026-11-06, fifth statement; the ledger reads the small-payload carve-out as unratified). … **Never write a bibliographic field from memory when a payload is in hand.**"
- Proposed: "A gate that asks whether author fields are *populated* passes invented authors — including the erasure of a Co-1 paper's disabled co-authors. **Verification must leave an artefact:** … An artefact a search-execution or admission gate must find is committed; a large PDF, page or extracted text is logged by where it was retrieved from, not committed (owner, 2026-11-06)."
- Reason: dated narrative and hand-typed counts out; the mechanism kept; the last line duplicates Goal item 1 ("A bibliographic field is never written from memory").
- Breaks: `scripts/research/retrieval_log.py:2109` cites "CLAUDE.md §5(c)'s control"; kept. Class: DELEGABLE. Confidence: high.

**C-32 — §6 cell states.**
- Current (L373): "Cell states: `stated` / `provisional` / `pending` / `not_applicable`."
- Proposed: "Cell states: the `specifications.state` CHECK (`dbcore.check_values`). No row is stored for a parameter and lens a determination does not concern (owner, 2026-10-29, OR-1)."
- Reason: rule 8 (a vocabulary comes from the column's own CHECK; verified the CHECK holds those four values today), and the owner's 2026-10-29 words, "Do not store table rows for parameters when there is a missing lens for a disability population or access need" (ledger; `governance/evidence-methodology.md:176` carries the SUPERSEDES note).
- Breaks: none. Class: DELEGABLE (ADJ2-C9 item 3; settled by owner words). Confidence: medium.

**C-33 — §6 "never bare axis codes".** Current (L378) "never bare axis codes"; proposed "never bare codes". Reason: the axis vocabulary is dropped (`scripts/migrations/109_drop_axes.sql`); "AX-" "should never ever exist anywhere" (owner, 2026-09-13). DELEGABLE (ADJ2-C9 item 4). High.

**C-34 — §6.** Current (L379): "(owner, 2026-08-27, overruling `DR-2026-08-24` §2.4)"; proposed "(owner, 2026-08-27)". History out. DELEGABLE. High.

**C-35 — §6 synthesis floor.**
- Current (L381-382): "Only Opus-class models write `best_practice_synthesis`."
- Proposed: "Only an Opus-class model or above (Fable-class included; `governance/decision-protocol.md` §4.2; owner, 2026-07-25) writes a determination (`specifications`)."
- Reason: owner directive 2026-07-25, "best_practice_synthesis can be fable as well" (ledger, the rule whose ACTION (3) reads "Opus-class or above, which includes Fable-class"); decision-protocol §4.2: "`fable` is a synthesis-capable tier alongside `opus`". No object named `best_practice_synthesis` exists (`select count(*) from sqlite_master where name='best_practice_synthesis'` is 0). Wording follows the antagonist (an open floor, not a closed list: the rule's ACTION (4) says "Do not re-pin the floor").
- Breaks: collides with `workplan/2026-11-12-bidirectional-pipeline/tasks/T-120-doctrine-amendments-and-deletions.md` item 3, which edits the same sentence (name only). If this lands first, T-120 drops its CLAUDE.md part. `skills/run-pipeline_SKILL.md:370` ("CLAUDE.md §6 reserves best-practice synthesis to Opus-class models") stays roughly true. The SessionStart contract in `.claude/settings.json` ("Never author best_practice_synthesis below the Opus floor") is generated from `governance/research-contract.yaml` and is T-120's.
- Class: DELEGABLE (settled by owner words). Confidence: high.

**C-36 — §6 the key: point, do not restate.**
- Current (L384-402): "**Both halves of the determination's key are RULED.** - **Lens.** Owner ruling 2026-08-28 … migration 138 … migration 065 built. - **Subject.** … - Migration 071 (the P1.0 migration) dropped … A ruling can be in the repository, … the traversal D-0184 measured and rejected."
- Proposed: one paragraph: subject (`parameter_id`, owner 2026-08-26, with the grep for its five-clause ACTION), `items` a rollup never a key, lens (at least one of three columns, real FKs, owner 2026-08-28 as relaxed by D-0182), `population_code` and the medical lens retired, `slug × population` no part of the key (D-0184), `PRAGMA table_info(specifications)` to verify, and "search for both halves of a question before calling either open".
- Reason: migration numbers and the story of how the key was built are history; the rulings live in the ledger.
- Breaks: `skills/run-pipeline_SKILL.md:237` cites §6 for the 2026-08-27 lens ruling; kept. Class: DELEGABLE. Confidence: medium.

**C-37 — §7 Wayback trap.**
- Current (L408-422): "… (measured 2026-09-28) … Succeeded for a SciELO article blocked by a Bunny Shield challenge (batch 21). **Failed for a Canadian standards PDF (CSA B651) blocked by a 403** (batch 22): … via `/__agentproxy/status`'s `recentRelayFailures`. Recorded here as a genuine limit of this technique, not a second success story — a prior version of this entry wrongly claimed both cases succeeded."
- Proposed: the procedure only (find snapshot, fetch `if_` form, retry once, try the plain form, persist through `retrieval_log.fetch()`, and "Resets on every form while a known-good control URL also fails mean the session's proxy, not the snapshot").
- Reason: batch narratives and a correction account (forbidden by L25-26). The control-URL test is kept because it decides when to stop.
- Breaks: `skills/run-pipeline_SKILL.md:151,170` cite §7 for "Wayback first"; kept. Class: DELEGABLE. Confidence: high.

**C-38 — §7 `.ignore`: point at the file.** Current (L423-425) lists eight directories. Proposed: "its entries are the list (`cat .ignore`)". Reason: rule 8 (a list kept beside the thing it describes); the list was already incomplete (`.ignore` also hides `references/audits/`). The two strict sentences ("Owner rulings live overwhelmingly in `sessions/`"; "Never report a ruling absent from a search that could not have seen it") are kept. DELEGABLE. High.

**C-39 — §7 `CURRENT`.** Current (L429-444), 16 lines including "batches 11–15 wrote branch slugs …" and "(and did, 2026-09-27)". Proposed: 5 lines: what `CURRENT` names, the LATEST pointers, the stem form, the identical folder name, `/session-open` sets both, move both in one action if the PR merges. Reason: history out; the procedure's home is `.claude/commands/session-open.md`, which carries all of it. Callers kept: "names the PREVIOUS session" (`governance/check-registry.yaml:892,946`, `scripts/audit/adversarial_pass_audit.py:31`, `scripts/run_checks.py:88`); "named identically" (`scripts/audit/search_log_completeness.py:66,180`, `scripts/dbcore.py:1171`); "in one action" (`.claude/commands/session-open.md:35`). DELEGABLE. High.

**C-40 — §7 item layer.** Current (L449, L456-458): "(migration 121 dropped `conflicts.item_code`; `add-conflict` takes `--parameter-id`)" and the archived-index prefix command. Proposed: deleted; the owner's reason, the rule and the live-surface command kept. Reason: history; the regex `\b[A-Z]-[0-9]{2}\b` already covers every prefix. Callers kept: `scripts/db.py:8513`, `scripts/validate_parameters.py:10`, `skills/connection-discovery_SKILL.md:21`. DELEGABLE. High.

**C-41 — §7 SessionStart trap**, trimmed by one clause. DELEGABLE. High.

**C-42 — §7 PI versioning.** Current (L467): "highest-numbered `governance/project-instructions-v*.md` is live". Proposed: "the numerically highest `governance/project-instructions-v*.md` (`ls governance/project-instructions-v*.md | sort -V | tail -1`) serves the claude.ai surface and lags doctrine." Reason: lexical order prints `v10_9`, numeric order `v10_14` (ADJ-09k); "live" overstated it for a Claude Code session. The phrase "PI versioning is intentional" is kept (quoted by `governance/retired-vocabulary.yaml:230`). DELEGABLE. High.

**C-43 — §7 the two appending files: correct a stale enforcement claim.**
- Current (L474-484): "… together the two largest token costs in the 2026-09 transcripts. … **That is rule 6's own argument** … `scripts/fix_stop_hook_loop.sh` patches the harness hook to read that exclusion from `git config stophook.ignorePath`. **An agent cannot apply it:** the harness classifier blocks it as self-modification, so the owner runs it or approves it when the agent asks."
- Proposed: "… SessionStart runs `scripts/fix_stop_hook_loop.sh` silently to add that exclusion to the hook; whether it took: `grep -c stophook.ignorePath ~/.claude/stop-hook-git-check.sh`."
- Reason: `.claude/settings.json` SessionStart[1] runs the script on every session (`>/dev/null 2>&1 || true`). In this container it did not take: the script's anchor ("`if ! git diff --quiet || ! git diff --cached --quiet; then`") no longer occurs in `~/.claude/stop-hook-git-check.sh`, whose line now reads "`if ! git diff --quiet || { ! git diff --cached --quiet && ! branch_moved_under_checkout; }; then`"; the script's `assert` fails after it has written a `.bak`, and `grep -c stophook.ignorePath` prints 0. The derivation command replaces a claim that is false in both halves.
- Breaks: T-120 item 3 says "CLAUDE.md §7 records the same limit for the stop-hook patch"; that pointer loses its referent. The script itself is a deletion candidate under §8 (vacuous against the current hook); not proposed here.
- Class: DELEGABLE. Confidence: high for this container; [UNVERIFIED] for other containers.

**C-44 — (the `--all` trap) merged into C-07.**

**C-45 — §8.**
- Current (L499-506, L501-502, L507-509, L517-518): separate bullets for the code archive and "Nothing is added without naming what reads it"; the sign-off list "mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction, licensing, trajectory"; two dated owner paraphrases; "… is how this file became a ratchet."
- Proposed: the archive bullet shortened; the sign-off list replaced by "the list in `governance/decision-protocol.md` §2.4"; "name what reads it" merged into the burden-of-proof bullet; the owner paraphrases condensed to "(owner, 2026-10-12 and 2026-11-06: the minimum that performs the action correctly)"; the ratchet clause deleted.
- Reason: the CLAUDE.md list is narrower than decision-protocol §2.4 (which also reserves major work-products, the Co-1 source corpus, adversarial-use catalogue retirement and counsel-review queue resolution; ADJ-09i, confirmed by the antagonist). A second, shorter copy of the owner-only list is how a session concludes something is delegable that is not.
- Breaks: callers cite §8 for "what wrong thing reaches the guidebook" and "an unread field, an uncalled script" (`scripts/db.py:4250`, `scripts/audit/observation_verbatim_audit.py:15`, several tests); both phrases kept. Class: DELEGABLE. Confidence: high.

**C-46 — §9: re-point.**
- Current (L533-544): "Pre-launch, single author (`@jordanelias`). The governance and tooling are elaborate; **the content is barely started.** Query the DB for the real state." and the table (quoted in section 4 below).
- Proposed: heading "## 9. Where to look"; "Single author, pre-launch. Query the database for the real state."; the corrected table and history list in section 4.
- Reason: "the content is barely started" is a volatile state claim (rule 7). Pointer defects are in section 4.
- Breaks: `governance/retired-vocabulary.yaml:849` cites "§9-2" (already broken; that section was removed long ago). Class: DELEGABLE. Confidence: high for the "What to do now" and history rows (ADJ-04's row fix survives the antagonist, who says the proven conflict "is closed by deleting that row"); medium for the architecture classification.

### 2b. OWNER-ONLY changes (not applied; the proposed file keeps the current text)

**O-01 — Rule 0: delete its Proof.** Current (L83-84): "*Proof: on 2026-08-18 the owner ruled `axes` a bad coined term, marked "do not relitigate", and the next day a batch framed four of five searches on bare `axis_code`, hiding a second mechanism.*" Proposed: delete. Reason: narrative with a hand count; the ledger holds the event. Confidence: high.

**O-02 — Rule 9: delete the PR number and the Proof.** Current (L199-200): "(observed on #158: a `subscription.created` event arrived with no subscribe call)"; (L205-207): "*Proof: in the 2026-09 transcripts most wake-ups … the batch that opened early.*" Proposed: delete both; the rule's imperatives are unchanged. Confidence: high.

**O-03 — Rule 9: the enforcement sentence is stale.**
- Current (L208-210): "→ **PARTLY ENFORCED** once the owner adds both `subscribe_pr_activity` tools, `send_later` and `create_trigger` to `permissions.deny` in `.claude/settings.json`: …"
- Proposed (ADJ-06): "→ **PARTLY ENFORCED** by `permissions.deny` in `.claude/settings.json`, which stops explicit subscription and polling only if its names match the tools the session exposes; it does not stop the subscription PR creation makes, so the unsubscribe step is yours. Never deny `unsubscribe_pr_activity`."
- Reason: the entries exist (`.claude/settings.json` `permissions.deny`: `mcp__github__subscribe_pr_activity`, `mcp__Claude_Code_Remote__subscribe_pr_activity`, `mcp__Claude_Code_Remote__send_later`, `mcp__Claude_Code_Remote__create_trigger`). In this session the tools are named `mcp__claude-code-remote__…` (lower case, hyphenated). Confidence: high that the sentence is stale; medium on whether the names match ([UNVERIFIED] normalisation).

**O-04 — `.claude/settings.json` deny names** (harness configuration; the owner applies it): add `mcp__claude-code-remote__subscribe_pr_activity`, `mcp__claude-code-remote__send_later`, `mcp__claude-code-remote__create_trigger` beside the existing entries. Confidence: medium.

**O-05 — Tier line: T3 gloss and Co-2.**
- Current (L367-370): "… **T2** synthesis · **Co-2** OT professional-body CPGs · **T3** grey primary · **T4–T6** the regulatory stratum, walled off from full-strength anchoring."
- Proposed: "… **T2** synthesis · **Co-2** OT professional-body CPGs, **co-primary with T2** · **T3** lower-control primary (clinical or grey) · **T4–T6** the regulatory stratum, walled off from full-strength anchoring."
- Reason: tier-system.md:19 defines T3 as "Clinical primary research at lower control level … plus grey-literature primary research" (ADJ-09j). Co-2 is "co-primary with Tier 2" in the ledger's core RULE (`references/project-standards.md:17`) and in the owner's words of 2026-11-26 reported by ADJ2-B ("Co-2 is co-primary with tier 2."; not yet appended to the ledger, [UNVERIFIED] as a ledger entry). Keep "**T4–T6** the regulatory stratum" literally: `test_db_amend_writers.py` parses it. Confidence: high.

**O-06 — Marker line.**
- Current (L372): "Markers: **●** confirmed · **◐** policy/standards only · **○** grey, thin or unverified (the source could not be retrieved). Unmarked is an error."
- Proposed (ADJ2-A pointer form): "Markers: ●, ◐, ○ and ⚠ — which tier takes which, and when ⚠ replaces the circle, is `governance/tier-system.md` §5 (owner, 2026-11-14). Unmarked is an error."
- Reason: the owner answered OD-57 ("od57 yes") to a question that named "replacing the ○ gloss in `CLAUDE.md` §6", and OD-64 (triangle for every grey basis). The ◐ gloss is also wrong, since ◐ now carries T3 non-grey research (antagonist OM-02), and ⚠ is missing. tier-system §5 itself is stale until T-120 item 2a lands, so the pointer form is right only together with T-120. Coordinate: this line and T-120 item 2a must be edited once. Confidence: high on the substance; the timing is the owner's.

**O-07 — The authority sentence (L20-23).**
- Current: "Where it disagrees with `decisions/DR-2026-08-19-research-restart-operative-instrument.md`, that instrument wins and this file is what to correct — **unless a live owner ruling has superseded the instrument itself, per rule 0, in which case the ruling wins over both.**"
- Options: (a) leave it; the §9 row fix (C-46) already removes the proven conflict. (b) The antagonist's sentence: "The owner's words govern (rule 0). Delegated resolutions are made against the doctrine, this file and the ledger, and never bind what decision-protocol §2.4 reserves (owner, 2026-11-25: "as always refer to doctrine/mission/claude.md etc for guidance as required"). A recorder's [ASSUMPTION] is not the owner's words." Do not use ADJ-04's seven-rank order (the antagonist found it inverts the owner's words).
- Class: OWNER-ONLY (it states the reach of rule 0 and of the owner's delegations). Recommendation: (b), appended after the current sentence. Confidence: medium.

**O-08 — The layer model (§3, L232-241).** Keep, move or delete. The rewrite spec moves §3 to a working-rules file. Rule 10 depends on it ("anything Layer 0/1/2"). This proposal keeps the quote verbatim and deletes only the retired-map note (C-20).

**O-09 — The rewrite spec's working-rules file.** Moving rules 0, 1, 4, 5, 6, 9, 10, §3, §7 and §8 to a separate file is the only route to the quarter-size target. Cost: one tooling PR, a new file every session must be pointed to, and a caller sweep. Section numbers would still need to resolve, since script comments and immutable migrations cite them. Recommendation: not needed for saliency once the history is gone; owner's call.

**O-10 — Goal sentence and simplicity sentence.** No change proposed.

---

## 3. Callers swept, and what each depends on

### 3a. Mechanical (code reads CLAUDE.md content)
- `scripts/audit/claude_md_spine.py` — exactly one `SPINE:` line equal to the contract. Kept byte-identical.
- `scripts/tests/test_db_amend_writers.py` T126-30 — the literal "**T4–T6** the regulatory stratum" (regex `\bT(\d)[–-]T6\*\* the regulatory stratum`). Kept byte-identical (O-05 keeps it too).
- `scripts/audit/supersession_backpointer_audit.py` — anchors on quotes in a target file. No `SUPERSEDES:` line targets CLAUDE.md (`git grep -n -E 'SUPERSEDES: *CLAUDE\.md'` is empty), so no deletion breaks it.
- `governance/retired-vocabulary.yaml` — lists CLAUDE.md in fourteen entries' `exempt_paths`. None of those tokens occurs in the current or the proposed CLAUDE.md, so the exemptions are already unused; the proposal adds no retired token (checked against every entry).

### 3b. Callers that quote CLAUDE.md (command: `python3 /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/cm/quotes.py <file>`)
Eight quoted phrases are present in the current file, and all eight are present in the proposed one: "PI versioning is intentional" (`governance/retired-vocabulary.yaml:230`), "vocabularies come from the schema" (`scripts/db.py:3560`), "bare stem in the DB, `.md` in pointers" (`scripts/dbcore.py:220`), "treat a 0-row object as unproven, not clean" (`scripts/dbcore.py:1837`), "the worst failure available here" (`scripts/research/retrieval_log.py:529`), "T4–T6 the regulatory stratum" (the test above), rule 0's enforcement line (`decisions/DR-2026-09-26-recurring-defect-shapes-remediation.md:567`), and `references/project-standards.md`. The other twenty quoted phrases were already absent before this proposal (for example `scripts/audit/db_path_env_audit.py:5`, "Every DB-aware script honours GUIDEBOOK_DB_PATH", which CLAUDE.md §7 no longer says).

### 3c. Callers by section (executable and configuration files; `git grep -n 'CLAUDE\.md' -- scripts .claude governance .github skills ':!scripts/migrations' ':!governance/*.md'`, 258 lines, saved as `/tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/code_callers.txt`)
- §1: `.claude/commands/orient.md:5`, `session-open.md:6`, `batch-done.md:134` (orientation and the diff gate); `governance/check-registry.yaml:161` (the dependency list's one home). All kept.
- §2: `governance/check-registry.yaml:883` ("you are the gate"); `governance/pipeline-contract.yaml:375`. Kept.
- §3: `governance/stage-map.yaml:35,74,93` (stage table, "most protected" view). Kept.
- §4 (38 lines, mostly `scripts/db.py`, `scripts/dbcore.py`, `scripts/assess/assess_cell.py`, two skills): the write path, "db.py refuses", vocabularies from the schema, the ref_id union, "a table the CLI cannot reach is a coverage bug", the emptied-FK failure, the population-match absence. All kept. `skills/run-pipeline_SKILL.md:29` (scratch DB) kept.
- §5(a) and §5(c): `governance/check-registry.yaml:491`, `scripts/audit/research_batch_dod.py:578`, `scripts/audit/research_protocol_audit.py:141,173`, `scripts/research/retrieval_log.py:1007,2109`, `scripts/tests/_baseline_ddl.py:25`, `governance/pipeline-contract.yaml:239`. Labels kept.
- §6: `scripts/db.py:4454` (Co-1 erasure sentence), `:10554` (codes with names), `:12181` (T4–T6 stratum); `governance/owner-browser.yaml:263` (Co-1 co-primary); `skills/run-pipeline_SKILL.md:237,370`. Kept; `:370` is affected by C-35.
- §7 (32 lines): `CURRENT` and the session-id forms (C-39, kept), Wayback (C-37, kept), item layer (C-40, kept), PI versioning (kept), `.ignore`'s own header comment ("§7's trap note about this very file", kept).
- §8: tests and audits cite "what wrong thing reaches the guidebook" and "an unread field, an uncalled script". Kept.
- Rule numbers: unchanged, so no rule-number caller breaks. Rules 7, 7a and 8 keep their imperatives.

### 3d. Callers this proposal breaks or weakens
- T-120 item 3 ("CLAUDE.md §7 records the same limit for the stop-hook patch"): C-43 removes that limit because it is false.
- T-120 items 2a and 3 edit CLAUDE.md §6's marker line and synthesis sentence. C-35 does the synthesis sentence; O-06 is the marker line. Edit each once.
- `.claude/commands/orient.md:25-27` routes "what to do now" to DR-2026-08-19 (paired with C-46; ADJ2-C4). Not edited here.

### 3e. Callers already broken before this proposal (not caused by it; listed for the reconciliation)
- Burden of proof cited as "CLAUDE.md §1" (it is §8): `scripts/audit/claude_md_spine.py:4`, `identifier_floor_audit.py:5`, `judgment_handoff_shape.py:4`, `schema_reference_audit.py:5`, `research_tooling_separation.py:87`, `extraction_relations_integrity.py:6`, `citation_mining_completeness.py:229`, `scripts/tests/test_record_command_session.py:4`.
- Old structure "§2(a)/(b)/(c)", "§2a", "§0 rule 4", "§10", "§9-2": `scripts/run_checks.py:77-79`, `scripts/tests/test_db_integrity.py:74,604`, `scripts/audit/research_batch_dod.py:881`, `scripts/audit/migration_reproducibility.py:56`, `scripts/audit/citation_mining_completeness.py:75,215`, `scripts/db.py:4730`, `scripts/dbcore.py:2150`, `scripts/audit/readonly_db_open_audit.py:16`, `scripts/generate/context_map.py:138,294` (and its generated `governance/context-map.yaml:563`), `skills/evidence-metadata-rehabilitation_SKILL.md:71`, `governance/retired-vocabulary.yaml:246,849`.
- Content cited from CLAUDE.md that it no longer holds: `governance/research-contract.yaml:102` (R3 anchor "CLAUDE.md §6" for quantified claims), `scripts/audit/research_batch_dod.py:41` (same), `scripts/audit/db_path_env_audit.py:5,139` (GUIDEBOOK_DB_PATH statement in §7), `scripts/audit/readonly_db_open_audit.py:80`, `scripts/audit/adherence_log_audit.py:345` ("§3: Retire *here*, don't delete"), `scripts/dbcore.py:15` ("schema drift is a bug, not a convention", §8), `governance/retired-vocabulary.yaml:150`.
- Callers that contradict CLAUDE.md: `scripts/preflight.sh` header and its PyYAML check ("pip install -r requirements.txt jsonschema"; "pip install -r requirements.txt") and `scripts/research/page_image.py:109` (the same, citing CLAUDE.md §1) instruct the install that §1 forbids.

---

## 4. Answers to the audit questions

### SALIENCY

**(a) What a session must know before its first action, and where the current file puts it.**

| Must know | Current location | First screen? | Proposed |
|---|---|---|---|
| Run `/session-open` before the first Bash call of a batch, or the command log is misfiled | Not in CLAUDE.md as a timing; L57 "to open a batch"; L429 trap | No | §1, first sentence (C-04) |
| The owner's words supersede every record (rule 0) | L79 | No | Unchanged position (OWNER-ONLY); the authority sentence above §1 refers to it |
| Never write the DB directly; the write path | L98, L288 | No | Unchanged; rule 3 points to §4 |
| Fetch before writing a bibliographic field | L14 | Yes | Unchanged |
| Missing `pydantic` makes main look red | L61 | No | §1 (C-03) |
| The Grep tool cannot see `sessions/`, where rulings live | L423 | No | §7, unchanged position; `/orient` also says it |
| Where "what to do now" is | L538 (wrong target) | No | §9, corrected (C-46) |

The first screen (L1-35) holds the goal, the three things, the authority sentence and the correction rule. In the proposal it holds the same plus the doctrine paragraph, and §1 starts with the session-open timing.

**(b) History, proofs, anecdotes, correction accounts, PR or batch numbers, and derived counts.** Each is listed with its disposition in section 2: L63-64 (version numbers, C-03), L83-84 (O-01), L90 (line number, C-09), L95-96 (C-10), L107-108 (C-12), L133-134 (C-15), L144-156 and L160-162 (correction history and a now-false claim, C-16), L177-186 and L192-195 (stale examples, proof, C-17), L199-200 and L205-207 (PR #158, Proof; O-02), L218-221 (Batch 20, C-19), L240-241 (C-20), L248-250 (C-21), L265 ("seven stages", "before 2026-08-27", C-22), L323-326 (migration 071, C-29), L350-351 (index.html, C-30), L353-356 and L359 (C-31), L379 (C-34), L388-390 and L397-398 (migrations 138, 065, 071, C-36), L412-413 and L417-422 (measured date, batches 21-22, correction account, C-37), L435-437 and L440-444 (batches 11-15, 2026-09-27, C-39), L449 and L456-458 (migration 121, archived index, C-40), L474-479 (token-cost narrative, C-43), L517-518 (C-45), L533 (owner handle, "content is barely started", C-46). Hand-typed counts among them: "four of five" (L84), "eight … six" (L107), "three figures" (L133), "eleven … three … four" (L148-149), "(16/640)", "8 rows" (L154-155), "0 rows when it held 2" (L162), "EIGHT", "seven", "four tables" (L181-185), "two shapes only" (L195), "five sources", "Six gates" (L353-355), "seven stages" (L265). Kept dates are owner-ruling locators (fixed facts that find the ledger entry), not volatile facts.

**(c) Strict imperatives versus narrative.** Already strict and checkable: rules 1, 2, 3, 9's imperatives, 10; §4's write path and "inline on every call"; §7's APPEND rule, session-id forms, "never report a ruling absent from a search that could not have seen it", "treat every `[A-Z]-NN` code as prior-version content". Strict but unenforced: rules 4, 5, 6, 7, 7a, 8 (they say so). Narrative a session had to interpret: every Proof block; rule 8's "anti-pattern in one line" example; §3's re-entrancy paragraph; §6's "A ruling can be in the repository … search stops at the first answer"; §7's Wayback success and failure stories; the stop-hook paragraph's "That is rule 6's own argument … which is why it beats a remembered rule". The proposal keeps each imperative and turns the narrative into either a command or nothing.

**(d) Duplicates.** Inside CLAUDE.md: rules 7, 7a and 8 overlap (kept as three numbers because callers cite each; each compressed to its own clause: 7 what to derive, 7a how a number is written, 8 vocabularies, identifiers and judgments); §5(b) restates rule 7 (now a pointer); §5(c)'s last line repeats Goal item 1 (deleted); §1's `--battery` paragraph and the `--all` trap (merged); rule 6 and the two-appending-files trap repeated the "red by construction" argument (once now); 7a carried rule 4's prose-caller sweep (moved). Against other files: the `CURRENT` procedure duplicates `.claude/commands/session-open.md` (condensed with a pointer); the UNWRITABLE probe duplicates `.claude/agents/db-census.md` (pointer); the `.ignore` directory list duplicates `.ignore` (pointer); the owner-only list duplicates and narrows decision-protocol §2.4 (pointer); the key rulings restate the ledger (condensed with the grep that finds them); the tier and marker lines duplicate `governance/tier-system.md` §1 and §5 (OWNER-ONLY; O-06 makes the marker line a pointer); the layer quote duplicates the ledger (OWNER-ONLY). The write path is restated in `.claude/settings.json`'s comment, `governance/research-contract.yaml`, `.claude/agents/db-census.md` and `.claude/commands/adversarial.md` (census 4e); CLAUDE.md §4 is the right home and those should point (not in scope here).

**(e) Buried or contradictory instructions.**
- Buried: rule 9's unsubscribe step sits mid-paragraph (OWNER-ONLY text; only the missing blank line before rule 9 is fixed, C-18). The prose-caller sweep was inside 7a's proof (C-12). The session-open timing was absent (C-04).
- Contradictions inside CLAUDE.md: "base … gated as a stage" against "`base` is not a stage" (C-23); "your local gate does not [run the selftest]" against `preflight.sh` (C-06); "Two refusals are deliberately absent" followed by a refusal that is present (C-26); rule 7a's proof against the registry (C-16); the PI trap's "highest-numbered" (ambiguous, C-42); §9's "what to do now" against rule 7's "derive … the active plan" (C-46).
- Contradictions with owner words: the synthesis floor (C-35); "Do not hand-write SQL" without the 2026-11-21 exception (C-25); the cell-state list against OR-1 (C-32); the marker and tier glosses (O-05, O-06).
- Contradictions with the tooling: rule 8's two `--tier` examples (C-17); the stop-hook claim (C-43); rule 9's enforcement sentence (O-03).
- With the harness: rule 9 against the default subscription (rule 9 governs: CLAUDE.md is loaded as the user's instructions, which override defaults; ADJ-06). Rule 6 ("commit … at every natural break") against the Bash tool's "Commit or push only when the user asks": rule 6 is the owner's standing instruction, so it is the user asking; no text added. Rule 1 and the harness's commit trailer are compatible (the trailer follows the subject line).

### EFFICACY (enforcement claims verified)

| Rule / trap | Named enforcement | Exists? | Claim true? | Changes a decision? | Verdict |
|---|---|---|---|---|---|
| 0 | `supersession_backpointer_audit` | yes, advisory | yes | yes | KEEP (OWNER-ONLY) |
| 1 | `check_commit_msg.py`, push only | yes | yes; line pointer wrong | yes | TIGHTEN |
| 2 | `attestation_presence`, `attestation_schema` | yes, both blocking | yes; scope is `.md` only | yes | TIGHTEN |
| 3 | `migration_reproducibility` (counts), `_deep` advisory | yes | yes (header: "C3 each core table's row count matches") | yes | KEEP |
| 4 | `schema_reference_audit`, selftest C7 | yes, blocking; C7 present | yes | yes | TIGHTEN |
| 5 | none | — | — | yes | TIGHTEN |
| 6 | none, deliberately; `preserve_transcripts.py --check` | yes | yes; SubagentStop hook unmentioned | yes | TIGHTEN |
| 7 | none | — | — | yes | TIGHTEN |
| 7a | selftest C9, `no_floor_kinds` | yes | yes | yes | TIGHTEN |
| 8 | `check_values`, `identifier_floor_audit`, `writable_tables`, `adjudication_integrity`, `derived_not_curated_audit.py` | all exist | yes; examples false | yes | TIGHTEN |
| 9 | `permissions.deny` "once the owner adds" | entries exist | stale; names may not match | yes | KEEP (OWNER-ONLY; O-03) |
| 10 | `research_tooling_separation` advisory | yes | yes | yes | TIGHTEN |
| Trap: Wayback | `retrieval_log.fetch()` | yes | yes | yes | TIGHTEN |
| Trap: `.ignore` | — | `.ignore` | list incomplete | yes | TIGHTEN |
| Trap: `CURRENT` | `record-command.py` `open_session()` | yes | yes | yes | TIGHTEN |
| Trap: rebase blocked | harness | — | [UNVERIFIED] not tested | yes | KEEP |
| Trap: item layer | — | archived index exists | yes | yes | TIGHTEN |
| Trap: session ids | — | `emit_data_migration --session` exists | yes | yes | KEEP |
| Trap: SessionStart APPEND | `research_contract_hook.py` reads `[0]["hooks"][0]` | yes | yes | yes | KEEP |
| Trap: PI versioning | — | yes | ambiguous | rarely | TIGHTEN |
| Trap: bootstrap.sh | — | yes | [UNVERIFIED] PAT gate not read | yes | KEEP |
| Trap: two appending files | `fix_stop_hook_loop.sh` | yes | false: runs at SessionStart; fails on the current hook | yes | TIGHTEN |
| Trap: `--all` | — | yes | yes | yes | MERGE into §1 |

Every path and script named in the current file was checked (`/tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/claudemd_out.txt` for the current file; `cm/paths_proposed.py` for the proposed). Broken pointers in the current file: `ci.yml:257` (wrong line), `index.html` (not at the root), and the archived-only `pipeline-map.yaml` (named as retired, so intentional). All seven agents and commands named exist. In the proposed file every path resolves; the tokens the checker reports as missing are slash commands, basenames, placeholders or prose.

### POINTING: corrected table for §9

| Question | Current target | Defect | Proposed target |
|---|---|---|---|
| What to do now | DR-2026-08-19 | Spent as a plan (its §3 "next act" is of 2026-08-22; the owner named the remediation plan on 2026-11-25); contradicts rule 7 | `/orient`; the ACTION lines of the newest entries at the tail of `references/project-standards.md`, and the plan they name |
| Latest rulings | ledger tail | — | unchanged |
| Doctrine | `governance/mission-and-epistemics.md` | — | unchanged |
| Tiers, markers, weighting | `tier-system.md`, `evidence-architecture.md` | marker table stale until T-120 (O-06) | unchanged |
| Entity model, ICF frame | `conceptual-model.md`, `functional-taxonomy.md` | both built on deleted layers (ADJ-01, ADJ-02) | "The schema: `sqlite_master` and `PRAGMA table_info`" and "ICF codes and the three lenses: §6; `python3 scripts/db.py icf-glossary`" (the antagonist noted ADJ-01 dropped the entity-model key without a replacement; this restores it) |
| Decision process | `decision-protocol.md` + recent DRs | — | "Who decides what: `decision-protocol.md` (§2.4 lists what only the owner decides)" |
| Architecture | `architecture/project-architecture-guidebook-v2.3.md` | written for "claude.ai chat with Code Interpreter", PI-centred | "Stages and their criteria; which stage a table is in: `governance/pipeline-contract.yaml`; `governance/stage-map.yaml`" |
| (missing) | — | the research contract R-rules are cited in §7 but not routed | "Research rules: `governance/research-contract.yaml`" |
| (missing) | — | — | "Checks: `governance/check-registry.yaml`; `run_checks.py --list`" |

History, not live guidance (named in the proposed §9): `governance/conceptual-model.md`, `governance/functional-taxonomy.md`, `architecture/project-architecture-guidebook-v2.3.md`, `governance/project-instructions-v*.md`, and everything `.ignore` hides. DR-2026-08-19 is not history: it keeps its rank above this file (L20-23, verbatim); it is only not the plan.

### STRICT RULES that stay in CLAUDE.md, by likelihood of need

| # | Rule (one imperative) | Enforcement | Where in the proposal |
|---|---|---|---|
| 1 | Derive every figure, and write the command, not the number. | C9 for `no_floor` only; otherwise you | rules 7, 7a |
| 2 | Write the database only through scratch copy → `db.py` → `emit_batch_sql.py` → `emit_data_migration.py` → `migrate_db.py`, with `GUIDEBOOK_DB_PATH` inline on every call. | `migration_reproducibility` (counts only) | rule 3, §4 |
| 3 | Fetch and log before you write any author, title or figure. | `retrieval_log.py --verify-authors` when run; otherwise you | Goal 1, §5(c) |
| 4 | Treat a live owner statement as superseding every record it touches, and record the supersession. | partly, `supersession_backpointer_audit` | rule 0 |
| 5 | Search rulings with `git grep`, and never report one absent from a search that could not see `sessions/`. | none | §7 |
| 6 | Run `/session-open` before the first Bash call of a batch; `CURRENT`, its folder and the DB stem must match. | none | §1, §7 |
| 7 | Sweep views, skills, the registry and prose before calling a rename done. | `schema_reference_audit`, selftest C7 | rule 4 |
| 8 | Point, do not copy, across tables. | none | rule 5 |
| 9 | Take every vocabulary from the column's CHECK and every ref_id from `next_ref_id`. | `check_values`, `identifier_floor_audit` | rule 8, §4 |
| 10 | Confirm a passing check examined something. | NOTHING-IN-SCOPE reporting | §5(a) |
| 11 | Run the gate once, at PR time, with `scripts/preflight.sh`. | none | §1 |
| 12 | Commit as `{skill}: {action} [YYYY-MM-DD HH:MM]`. | push events only | rule 1 |
| 13 | Attest every changed `.md` under `decisions/`, `sessions/` or `references/connection-reasoning/`. | blocking | rule 2 |
| 14 | Ship tooling and research rows in separate PRs, tooling first. | advisory | rule 10 |
| 15 | Open the PR last, unsubscribe at once, and do not watch it. | partly, deny list | rule 9 |
| 16 | Commit the scratchpad and transcripts at natural breaks. | none, deliberately | rule 6 |
| 17 | Keep the original beside every translation, and keep Co-1 co-producers credited. | none | Goal 2-3, §6 |
| 18 | Before adding apparatus, name what wrong thing reaches the guidebook and what reads it. | review | §8 |

No new rule, check or table is proposed. The one added sentence (C-25) records an owner ruling that CLAUDE.md currently contradicts.

---

## 5. Not reached or not verified

- [UNVERIFIED] Whether Claude Code's permission matching normalises MCP server names (`Claude_Code_Remote` against `claude-code-remote`) (O-03, O-04).
- [UNVERIFIED] `scripts/preflight.sh --explain` end to end; the pass-through was read in the script, not run (C-05). No check suite was run, by instruction.
- [UNVERIFIED] Whether the stop-hook patch fails in containers other than this one (C-43); verified here only.
- [UNVERIFIED] The owner's 2026-11-26 Co-2 words as a ledger entry: reported by ADJ2-B, not yet appended (O-05). The ledger's core RULE already says it.
- [UNVERIFIED] That `git rebase` and `git checkout -B` are still blocked in this harness, and that `scripts/bootstrap.sh` is PAT-gated (neither was tried or read in full).
- [UNVERIFIED] The classification of `architecture/project-architecture-guidebook-v2.3.md` as history. Its header says "Surface: claude.ai chat with Code Interpreter" and it is PI-centred; its enforcement-spectrum section is still cited by audits ("level 2 on the enforcement spectrum"). Confidence medium.
- The rule-number tally counts every "rule N" token, some of which belong to other numberings (research-contract R-rules, DR rules); only the CLAUDE.md-explicit lines in executable and configuration files (section 3c) were read one by one.
- The twenty quoted phrases already absent from CLAUDE.md were listed, not each traced to its original wording.
- The proposed file was not placed in the repository, so `claude_md_spine` and the T126-30 test were emulated with their own regular expressions, not run.
- `.claude/README.md`, `governance/research-contract.yaml` and the four restatements of the write path were not audited beyond the lines cited.
