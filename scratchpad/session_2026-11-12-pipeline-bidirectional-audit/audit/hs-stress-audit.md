# HS-5 — Audit of the stress-test results (rounds 1 and 2)

_Handshake leg, 2026-11-12 (UTC). Subject: `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress/` — round 1 `results/<topic>/log.jsonl` (nine topics and `crosstopic`), round 2 `results2/{sweep,chain,tools}/log.jsonl`, the scripts `stress_run.py`, `stress_run2.py`, `lang_probe.py`, and the scratch databases they left under `/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/stress-run/`. The scripts log; they do not judge. This file judges, and audits the scripts as well. `sha256sum data/guidebook.db` before and after this pass: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`; the stress scripts record the same hash around every step (`grep -c '"canonical_moved": true' results/*/log.jsonl results2/*/log.jsonl` returns 0 for each file). Re-runs by this leg were on fresh copies under `…/scratchpad/hs3/`. `stress_run.py` and `stress_run2.py` were not edited._

## 0. Verdict first

_Final pass: round 3 (`results3/`) is audited in §7. Where §7 overturns a sentence of §0 to §6, §7 governs; the sentences overturned are listed at the head of §7._

**The stress tests confirm the audit's main findings, overturn one of its withdrawals, and expose five defects it had not found. They are also much narrower than their step counts suggest, and three of their "passes" tested nothing.**

1. **Coverage is wide in invocation and thin in effect.** Round 1 runs the same script nine times; its topics differ only in slug, language, lenses and probe strings, so most "same across nine topics" results are one result repeated. Across both rounds no extraction, no citation-mining row and no candidate was written; every one of the determinations reported per topic is `pending`; no determination passed through the write path; and no registry battery ran (each of the ten `--battery` calls ended in a usage error).
2. **Confirmed:** the engine stores a row for any lens named; coverage owes the pairs the owner scoped out; sub-national and script-tagged codes cannot be represented; the name screens fail outside ASCII; a new parameter makes every source owed again and nothing discharges it; gaps are untyped; nothing can hold a render question; the engine is deterministic; the single-batch write path round-trips by row counts.
3. **Overturned:** the withdrawal of IMP-11 on the ground that replay of two scratch copies was untested. It is now tested: three independently captured batches fail at rebuild on `evidence_sources.ref_id` (`crosstopic.005`). Research batches are serial.
4. **New defects** (ranked in §3): the claimed-number check accepts decimal shifts and digit substrings; `add-parameter` promotes an element, a functional-axis term and a legal concept to parameters; `add-source` writes a source with no verification standing and no source type; `delete-connection` reports deleting a row that does not exist; CLAUDE.md's `--battery <name>` instruction does not run as written.
5. **Now measured, where the audit said "not run":** `run_checks.py --selftest` passes; `run_checks.py --changed-from origin/main --explain` on a scratch copy returns PASS with 60 green, 5 nothing-in-scope and 10 advisory failures; `migration_reproducibility`, `schema_reference_audit` and `claude_md_spine` pass with a non-zero subject.

Counts are commands (run in `stress/`):
- log lines and return codes, round 1: `python3 -I -c "import json,glob,collections;c=collections.Counter(str(json.loads(l)['rc']) for f in glob.glob('results/*/log.jsonl') for l in open(f));print(sum(c.values()),dict(c))"`; round 2: the same over `results2/*/log.jsonl`.
- distinct `db.py` verbs reached in round 1: `python3 -I -c "import json,glob;print(len({json.loads(l)['argv'][3] for f in glob.glob('results/*/log.jsonl') for l in open(f) if json.loads(l)['argv'][2:3]==['scripts/db.py']}))"`.
- engine reports by state: `python3 -I -c "import json,glob,collections;print(collections.Counter((lambda j:(j[0] if isinstance(j,list) else j)['state'])(json.load(open(f))) for f in glob.glob('results/*/determinations/*.json')))"`.
- behaviours by class in this file: `grep -c '| defect |$' hs-stress-audit.md` and likewise for `as-designed`, `refusal-correct`, `refusal-wrong`, `silent no-op`, `vacuous pass`, `doc-contradiction`, `unresolved`.

Status marks: **V** = seen in the log line named or re-run by this leg; **I** = inferred, basis given; **U** = unverified.

---

## 1. Classification of behaviours

Scope: **S** = identical in all nine round-1 topics (the script runs the same step) · **T** = differs by topic · **R2** = round 2. Cause: **P** = pipeline behaviour · **X** = induced by the script's own arguments or SQL · **P/X** = both. Tags are the scenario names; prefix the topic and number to find the line (`grep -n '<name>' results/<topic>/log.jsonl`).

| id | scope | behaviour | evidence | cause | class |
|---|---|---|---|---|---|
| B-01 | S | `coverage` requires all 70 pairs for a slug, the four scoped-out languages included; `scope_status` NULL on every row | `base.coverage`, `base.scope-status` [V] | P | defect |
| B-02 | S | A parameter is defined in three commands from two words of a held quote (`observe-term` → `add-term` → `add-parameter`) | `base.observe-term`, `base.add-term-new`, `base.add-parameter-new-term` [V] | P | as-designed |
| B-03 | S | `adjudicate-term --outcome NAMES-NEW` refused, naming `add-term --from-observation` | `base.adjudicate-names-new` [V] | P | refusal-correct |
| B-04 | S | A name carrying "not above 0.6 s" refused | `base.add-term-value-bearing` [V] | P | refusal-correct |
| B-05 | T | `add-parameter` promoted `grab bar` (an element), `Reach & manipulation` (domain `functional_axis`), `thermal comfort`, `jurisdictional accessibility standards` (domain `legal`), and in every topic `wheelchair propulsion` (an activity) | `base.add-parameter-existing-term` in reach, thermal, grabbar, method; `base.add-parameter-new-term` everywhere [V]; domains: `select term_id, canonical_en, domain from terms where term_id in ('TERM-008','TERM-041','TERM-063','TERM-075')` [V] | P | defect |
| B-06 | S | Each new parameter adds one `NOT-READ` pair per live source; `READ-NOTHING-FOUND` does not move; `scan_debt` rises by the same amount | `judgment.scan-ledger-by-status`, `judgment.scan-debt-after-new-parameter` [V] | P | as-designed |
| B-07 | S | `observe-term` accepts any non-empty locator text (`STRESS-FIXTURE locator`) | `select locator from observed_terms order by observation_id desc limit 1` on a topic copy [V] | P | as-designed |
| B-08 | S | `log-search` accepted with a non-English query and a prior expectation; language folded to upper case | `research.log-search-fixture` [V] | P | as-designed |
| B-09 | S | `add-candidate` refused: `--surfaced-in` names no linked artefact; candidate staging not exercised | `research.add-candidate-fixture` [V] | X | refusal-correct |
| B-10 | S | `log-search --session <stem>.md` accepted and the row stored under the bare stem | `research.log-search-wrong-session-form`; `select created_by_session from search_executions order by exec_id desc limit 4` [V] | P | as-designed |
| B-11 | S | Duplicate DOI refused, naming the existing `ref_id` | `evidence.add-source-duplicate-doi` [V] | P | refusal-correct |
| B-12 | S | `add-source` wrote a fixture source with an invented author and no retrieval (`UNVERIFIED`); with fewer arguments it wrote one with `verification_status` NULL and `source_type` NULL | `evidence.add-source-fixture`, `cold.evidence.add-source-minimal`, `lateral.add-source-jurisdiction-UK`; `select ref_id, source_type, verification_status from evidence_sources order by rowid desc limit 3` on a topic copy [V] | P | defect |
| B-13 | S | Two `add-extraction` probes (a quote found in no file; a number in words) refused for "no source_scans row covers", before either guard was reached | `judgment.add-extraction-unfound-quote`, `adversarial.number-in-words-claim` [V] | X | refusal-correct |
| B-14 | S | `record-scan` with an unknown hash refused | `judgment.record-scan-bogus-sha` [V] | P | refusal-correct |
| B-15 | S | `add-connection` accepted between the two newest parameters with a free description; nothing reads the row | `synthesis.add-connection-fixture` [V] | P | as-designed |
| B-16 | S | `add-gap` accepted free text; `gaps` has no parameter, lens, jurisdiction or language column | `synthesis.add-gap-reentry-fixture`, `synthesis.gaps-columns` [V] | P | as-designed |
| B-17 | S/T | Every per-topic determination is `pending`, and a row plus a gap is stored for every lens asked, relevant or not | `results/*/determinations/*.json` (count by the command in §0); `specification.assess.*` [V] | P | defect |
| B-18 | T | Luminance, parameter 8: the same five figures (tags `BLIND`, `MOB`, `ALL`) are linked for every lens asked (`BLIND`, `VES`, `AUT`, `ALL`, an ICF code, an access need) | `select l.role, x.identity_code, count(*) …` on `stress-run/luminance/assess-8-identity-VES.db` [V] | P | defect |
| B-19 | S | Determination views return 0 rows in the topic database, because every engine run was on a separate copy | `render.views-with-rows` [V] | X | vacuous pass |
| B-20 | S | The walkability instrument exits 0 over `NO PATH` lines | `render.walkability` [V] | P | defect |
| B-21 | S | `owner_browser_build.py` writes one HTML file embedding the database; no page of a determination exists | `render.owner-browser-build`, `render.ls-render-surfaces` [V] | P | as-designed |
| B-22 | S | The backward funnel query failed on a column that does not exist (`l.locator`); the backward walk was not tested | `backward.extraction-funnel` [V] | X | vacuous pass |
| B-23 | S | No table can hold a reader's or a render question | `backward.render-question-table` [V] | P | defect |
| B-24 | S | Cold entry at base: `add-term` without an observation ends in a usage error naming the flag, not the route | `cold.base.add-term-without-observation` [V] | P | refusal-correct |
| B-25 | S | Cold entry at research without a subject: refused, naming the three ways to give one | `cold.research.log-search-without-slug` [V] | P | refusal-correct |
| B-26 | S | Cold entry at judgment on an unadmitted source: refused, naming `add-source` | `cold.judgment.add-extraction-absent-ref` [V] | P | refusal-correct |
| B-27 | S | Cold entry at synthesis on a parameter that does not exist: refused | `cold.synthesis.add-connection-absent-parameter` [V] | P | refusal-correct |
| B-28 | S | Cold entry at specification with no figure: a `pending` row and a gap are written | `cold.specification.assess-cell-zero-evidence` [V] | P | defect |
| B-29 | S | Cold entry at render: `v_best_practice` returns no row and nothing says which of "not relevant", "not researched", "researched, empty" applies | `cold.render.best-practice-for-parameter-without-spec` [V] | P | silent no-op |
| B-30 | T | The script probe reports no normalisation collision in any topic. Its paired strings differ in digits, which the normaliser keeps | `lateral.script-probe`; re-run of `lang_probe.py` with pairs differing only in a vowel sign, a voicing mark or a decimal point reports three collisions [V] | X | vacuous pass |
| B-31 | T | The value screen fires on ASCII digits only: it passes full-width digits, a number in words, and "no more than three" in French, German, Arabic, Hindi and Thai | `lateral.script-probe` in acoustics, reach, cost, flash [V] | P | defect |
| B-32 | T | The name tokeniser returns nothing for a non-Latin string without ASCII digits or letters | `lateral.script-probe` in flash, acoustics [V] | P | defect |
| B-33 | S | `add-source --jurisdiction UK` accepted; `CA-ON`, `DE-NW`, `XX` refused with one message that lists the enum and names the admission route | `lateral.add-source-jurisdiction-*` [V] | P | refusal-correct |
| B-34 | S | `log-search --language zh` and `ar` accepted with no jurisdiction (`in_research_scope: false`), although Arabic is scoped out; `zh-Hant` and `ZZ` refused | `lateral.log-search-language-*` [V] | P | defect |
| B-35 | S | `retire-parameter 3` refused for an open determination gate; the follow-up query failed on a column that does not exist | `adversarial.retire-parameter-with-extractions`, `adversarial.post-retire-state` [V] | P/X | refusal-correct |
| B-36 | S | The same cell on two fresh copies gives byte-identical SQL and report | `determinism.compare` [V] | P | as-designed |
| B-37 | S | A second run for a live cell is refused, naming `retire-specification` | `determinism.assess-same-db-run2` [V] | P | refusal-correct |
| B-38 | S | One batch: capture, migration file in a clone, rebuild; the rebuilt database matches the scratch copy in every table's row count but the migration ledger | `writepath.*` [V]; `PRAGMA foreign_key_check` on `stress-run/acoustics/rebuilt-out.db` returns no row [V] | P | as-designed |
| B-39 | S | Every rebuild prints "158 FK violations after 081_icf_registry.sql (advisory)" | `writepath.migrate-rebuild` [V] | P | as-designed |
| B-40 | — | Three independently captured batches applied to one history: rebuild fails, `UNIQUE constraint failed: evidence_sources.ref_id` | `crosstopic.005.rebuild-with-all-deltas` [V]; each batch inserts explicit ids (`grep -c '^INSERT' stress-run/<topic>/batch.sql`) [V] | P | defect |
| B-41 | R2 | Sweep: every verb invoked once, most with `--dry-run`; nothing written; many refusals name the script's placeholder value | `results2/sweep/log.jsonl` (counts by the command in §4) [V] | X | vacuous pass |
| B-42 | R2 | `delete-connection --con-id CON-1` on a database with no connection prints `{"deleted": "CON-1"}` and exits 0; `update-connection` on the same id refuses | `chain.031`, `chain.030`, `sweep.035` [V] | P | silent no-op |
| B-43 | R2 | `record-scan --method full-read --text-scope full` accepted for `REF-00139` against its held text file | `chain.002` [V] | P | as-designed |
| B-44 | R2 | `add-extraction` refused: a quantified claim needs a locator or an `[UNVERIFIED-QUANT]` note. No extraction was written in either round | `chain.004` [V] | X | refusal-correct |
| B-45 | R2 | `observe-term` refused: the surface form the script built is not in its quote | `chain.003` [V] | X | refusal-correct |
| B-46 | R2 | `log-mining` refused for want of `--notes` or `--deferred-reason`; `is-mined` and `unmined` read; no mining row was written in either round | `chain.005` to `chain.007` [V] | X | refusal-correct |
| B-47 | R2 | `link-source-slug` filed a source under an unrelated stub slug | `chain.010` [V] | P | as-designed |
| B-48 | R2 | A follow-up was raised and resolved | `chain.024`, `chain.025` [V] | P | as-designed |
| B-49 | R2 | `add-alias` from an adjudicated observation promoted the existing alias row (the first use of the observation pointer); the `--alias-type` given was set aside and reported | `chain.034` [V] | P | as-designed |
| B-50 | R2 | Free-text warrants accept any non-empty string: a term's definition was replaced on the reason `1`; the one open determination gate was resolved on the rationale `STRESS-FIXTURE` | `chain.035`, `chain.043` [V] | P | as-designed |
| B-51 | R2 | The determination for parameter 3 × `MOB` after the gate was resolved carries the same derivation hash as this leg's run with the gate open | `chain.054` against HS-2 F-01's run [V] | P | as-designed |
| B-52 | R2 | Capture after the chain: inserts and updates both captured; the determination was run on a separate copy and is not in the capture | `chain.055`; `grep -o -E '^(INSERT INTO|UPDATE) "?[a-z_]+' stress-run/chain/batch.sql` [V] | P/X | as-designed |
| B-53 | R2 | `run_checks.py --battery <name>` alone ends in a usage error, ten times; CLAUDE.md §1 says "Use `--battery <name>` to answer a targeted question" | `tools.055` to `tools.064`; `python3 scripts/run_checks.py --help` shows `--battery schema --kinds data` [V] | P/X | doc-contradiction |
| B-54 | R2 | `run_checks.py --selftest`: PASS. `--changed-from origin/main --explain`: PASS, with advisory failures in `scan_debt`, `verified_scan_integrity`, `validate_schema_cross_check`, `skill_vocabulary_audit`, `retired_vocabulary`, `research_dod`, `research_tooling_separation`, `research_protocol_audit`, `metadata_integrity_audit`, `test_scan_contract` | `tools.065`, `tools.066` [V] | P | as-designed |
| B-55 | R2 | Three checks exit 0 having examined nothing: `extraction_follow_up_audit`, `medical_lens_integrity`, `validate_schema` | `tools.013`, `tools.022`, `tools.045` [V] | P | vacuous pass |
| B-56 | R2 | Six audit scripts need arguments and ended in usage errors | `tools.003`, `.005`, `.027`, `.029`, `.030`, `.036` [V] | X | vacuous pass |
| B-57 | R2 | `doctrine_recheck.py` run bare exits 1 on three governance documents absent since its prior snapshot; it is registered blocking and the diff-scoped gate is green | `tools.047`; registry level by YAML load [V]; why the gate is green [U] | P | unresolved |
| B-58 | R2 | `validate_cross_refs.py` (blocking, no floor) reports 0 issues over "0 CON-IDs" and the prior version's BPC and search-log files; it prints no `EXAMINED:` | `tools.041` [V] | P | vacuous pass |
| B-59 | R2 | `citation_mining_completeness`: every slug-linked T1–T2 source has a mining row; fewer are marked mined | `tools.006` [V] | P | as-designed |
| B-60 | R2 | `migration_reproducibility`, `schema_reference_audit`, `claude_md_spine`, `identifier_floor_audit` pass with a non-zero subject on a copy of `main` | `tools.024`, `.035`, `.008`, `.017` [V] | P | as-designed |
| B-61 | R2 | No tool wrote into the repository tree | `tools.067` [V] | P | as-designed |

**Systemic against topic-specific.** Everything marked S is one behaviour observed nine times by construction; it is systemic in the sense that the code path does not depend on the topic, and it is not nine confirmations. What the topics add is B-05 (four different kinds of non-parameter promoted), B-18 (the one topic whose parameter holds figures under several lens tags) and B-30 to B-32 (the per-script strings).

---

## 2. Against the audit's predictions

### 2.1 Confirmed
| Prediction (file) | Stress evidence |
|---|---|
| The engine stores a row for a lens no figure carries (HS-1 REQ-074, HS-3 IMP-09) | B-17, B-28 |
| The lens selects nothing (HS-1 HS-A02) | B-18; `determinism.assess-a`: parameter 3 × `ALL` is `provisional` on 27 sources although parameter 3 holds no `ALL` figure |
| Scope is in no table; coverage owes what was scoped out (HS-2 F-14) | B-01, B-34 |
| Sub-national and variant codes cannot be represented (HS-2 F-13, F-19) | B-33, B-34 |
| Name screens fail outside ASCII (HS-1 REQ-034, REQ-055) | B-31, B-32 |
| A new parameter re-opens every source; a full read does not carry (HS-1 §5.2) | B-06 |
| Gaps are untyped; no carrier for a render question (HS-1 §0 D1) | B-16, B-23 |
| Determinism; refusal of a second live cell (HS-1 REQ-025, REQ-072) | B-36, B-37 |
| Specification gates examine nothing live on `main` (HS-2 F-11) | B-55; `validate_evidence_state` `EXAMINED: 13` in `tools.042` |
| Stage-pair instrument exits 0 over missing paths (HS-2 F-03) | B-20 |

### 2.2 Contradicted or changed
1. **IMP-11's withdrawal.** HS-3 withdrew it because "replay of two separate copies was not tested" and a convention would do. B-40 tests it: the second batch fails at rebuild on the first id it shares. The failure is loud, and it means every later research batch must be regenerated after an earlier one merges, which for research rows means re-running the session's verbs. Reinstated in corrected form as IMP-41, with OD-27.
2. **"Not run" statements.** HS-1 §8, HS-2 §4 and FC §5 said `run_checks.py` was run in no mode and listed `migration_reproducibility`, `schema_reference_audit` and `claude_md_spine` as unrun. They are now measured on a scratch copy (B-54, B-60). Still unrun: `run_checks.py --all`; any single battery (B-53); `research_dod_session` on its own.
3. **The round trip.** HS-1 §8 called capture → migration → rebuild "inferred from the tools' existence". It holds for one batch, by row counts (B-38). It is still untested for a batch carrying a determination, and for content rather than counts.
4. **The alias pointer.** HS-1 REQ-058 said no alias is attested by pointer and implied the route was unexercised. The route works (B-49); the data fact stands.
5. **F-10's collisions.** Round 1 reports none. That is the script (B-30), not a contradiction: with pairs that differ only in a mark, the same probe reports them.

### 2.3 Missed by the audit, found through the stress tests
Ranked by harm to the book.
1. **The claimed-number check compares digit runs as substrings of a quote from which punctuation has been stripped** (`scripts/db.py:8559-8563` with `retrieval_log.normalise_quote`). Seen in the probe output (`1.2m` normalises to `12m`; `1.234,56 €` to `123456`) and then tested on the live functions: a claimed `12` is accepted against "no higher than 1.2 m", `0.6` against "6.0 s", `8.33` against "83.3 %", `5` against "1:15 in 2015". A value with a shifted decimal point, or any value whose digits occur inside another number of the quote, verifies. [V]
2. **`add-parameter` has no test of what a parameter is** (B-05). An element, a functional axis and a legal concept each became a determinable parameter, each adding one owed reading per source and a `pending` row and gap per lens asked. The ledger rule that a parameter and its element are distinct terms (PS:612) is not held by the writer. [V]
3. **Parallel batches cannot both land** (B-40). [V]
4. **`add-source` writes a source with no verification standing and no source type** (B-12). The research contract says `UNVERIFIED` is a real value to be said (`governance/research-contract.yaml:217-219`, written for sources carrying a URL; the URL case was not tested). `select sum(verification_status is null) from evidence_sources` is 0 on `main`, so the committed rows all carry one; the writer does not require it. [V]
5. **`delete-connection` reports success on a row that does not exist** (B-42). [V]
6. **CLAUDE.md §1's `--battery <name>` does not run without a selector** (B-53). [V]
7. **A registered test fails on `main` at advisory level** (`test_scan_contract`, with `validate_schema_cross_check` and `research_dod`; B-54). The audit's lists of standing advisory failures did not include them. What each fails on was not read. [V for the names; U for the causes]

---

## 3. Programme deltas (carried into `hs-improvement-programme.md` §7 and `fa-corrections-for-suite.md` §6)

| New or changed | What | Test | Gate |
|---|---|---|---|
| IMP-44 (new) | The claimed-number check compares numbers with their decimal position, not digit runs | AT-79 | none |
| IMP-42 (new) | `add-parameter` refuses a term that states no quantity kind; the quantity-kind half of IMP-30 moves ahead of any further parameter | AT-77 | none for the refusal; OD-24 for the policy |
| IMP-41 (reinstates IMP-11's subject) | Research batches are serial; the second of two parallel batches should be refused at capture with the regeneration step named, not first at rebuild | AT-101 | OD-27 if parallel batches are wanted |
| IMP-43 (new) | `add-source` requires an explicit verification standing and source type | AT-78 | none |
| IMP-45 (new) | `delete-connection` refuses an id that is not a row | AT-100 | none |
| IMP-02 (extended) | CLAUDE.md §1: `--battery <name>` needs `--kinds`, `--all` or `--changed-from` | AT-102 | none |
| IMP-09, IMP-12, IMP-17, IMP-18, IMP-23, IMP-27, IMP-28 | unchanged; each now has a stress reproduction (B-17, B-16, B-33, B-01, B-31, B-06) | as before | as before |

**Ordering.** IMP-43, IMP-44 and IMP-45 join the doable-now set (no owner word, no dependency, nothing red on `main`). IMP-42 with the quantity-kind column becomes a precondition of minting any further parameter and of the reading task R-2, because each parameter multiplies what must be read (B-06). The preconditions of a first live determination are unchanged; IMP-44 is added as a precondition of writing new extractions (R-2, R-3).

---

## 4. Where the scripts are too weak to have tested what they claim

| # | Claim | What actually ran | Fix to the script (proposed, not made) |
|---|---|---|---|
| W-1 | Nine unrelated topics | One fixed sequence nine times; the same source (`REF-00986`), the same observed phrase, parameters 3 and 7 in every topic | Draw the observed phrase, the source and the parameters from the topic; report topic-independent steps once |
| W-2 | Forward base → render | No extraction, candidate or mining row was written; the engine ran on separate copies; render queries ran on a database with no determination | Use one held source with a text layer (`REF-00139`): scan, extract with a quote and locator taken from the text, determine on the same database, then query the views |
| W-3 | Specification across lenses | Every per-topic report is `pending`; only the determinism runs reach a value, on one lens | Add parameters 3 and 12 under several lens tags, and run `test_db_integrity` and the three specification checks on each copy |
| W-4 | Backward walk | The funnel query names a column that does not exist | Join `source_locators` on `ref_id`; walk a live determination through `v_determination_provenance`, `v_source_admission` and `search_execution_artefacts` |
| W-5 | Script and number-format collisions | Paired strings differ in digits; a function with another purpose (`dbcore.normalise_quote_text`, whitespace only) is labelled "the dbcore copy" | Pair strings that differ only in a vowel sign, a voicing mark, pointing, a tone mark or a decimal point; add non-ASCII digits; drop the mislabelled function |
| W-6 | Adversarial inputs | The unfound quote and the number in words were stopped earlier, by the missing scan; `retire-parameter` by an open gate; the post-retire query failed | Record a scan first; choose a parameter with no open gate; fix the query (`base_parameters.status`) |
| W-7 | Write-path replay | No determination, link row or engine gap is in any captured batch; equality is by row count | Determine on the topic database before capture; compare content (`migration_reproducibility_deep`) |
| W-8 | Every verb invoked (round 2 sweep) | Most with `--dry-run`, on placeholder arguments; a refusal of the placeholder says nothing about the verb. Count them: `python3 -I -c "import json;r=[json.loads(l) for l in open('results2/sweep/log.jsonl') if '.verb.' in l];print(len(r),sum('--dry-run' in x['argv'] for x in r),sum(x['rc']!=0 for x in r),sum(x['rc']!=0 and 'STRESS-FIXTURE' in x['stdout']+x['stderr'] for x in r))"` | Build arguments from the column's own CHECK (`dbcore.check_values`) and real ids; run without `--dry-run` on a fresh copy |
| W-9 | Every battery run | Ten usage errors | `run_checks.py --battery <name> --all`, or `--kinds` with the kinds the battery serves |
| W-10 | "Silent no-op" detection | The harness compares row counts, so an UPDATE is invisible and a dry run looks like a no-op | Hash the tables a verb names, or diff with `emit_batch_sql.py` after each step |
| W-11 | Citation mining and cross-comparison traced | `is-mined`, `unmined`, `citation_mining_completeness` and `mining_screen --compare` read; `log-mining`, `add-conflict`, `relate-extraction`, `derive-extraction`, `add-supersession-check`, `add-population-match` were refused on placeholder arguments | As W-8 |

---

## 5. Further stress tests that would add audit surface

Seven scenarios the two rounds did not cover. Each names what it would settle.

1. **One real source read to the end.** `REF-00139`: full-read scan with the open pass, observations with locators, several extractions under more than one lens tag, a relation edge, a population match, then a determination on the same database and the blocking checks. Settles whether the judgment writers accept correct input (no leg has seen one extraction written).
2. **Evidenced cells across lenses, with the gates.** Parameters 3 and 12 under `MOB`, `SCI`, `MS`, `ALL`, an ICF code and an access need, each followed by `test_db_integrity`, `validate_evidence_state`, `derivation_handshake_integrity`. Becomes the red-then-green harness for IMP-08.
3. **Write path with a determination, compared by content.** Determine on the topic database, capture, emit, rebuild, `migration_reproducibility_deep`. Settles the engine half of the round trip.
4. **Two batches, at capture.** Apply batch A to a clone's canonical copy, then run `emit_batch_sql.py` for batch B against it. Settles whether the collision is caught before rebuild and what the message tells the session to do (AT-101).
5. **Fidelity guards through the writers.** With a scan recorded: quotes differing from the held text only in a mark, a decimal shift, a digit substring, non-ASCII digits, a number in words. Settles IMP-23 and IMP-44 at the writer, not the pure function.
6. **Parameter life cycle and catalogue growth.** Define a parameter, read one source against it by a targeted scan, then decline, merge and retire where no gate is open; watch `v_scan_ledger` and the extractions each time. Settles what a change of grain does to completed scans (REQ-099).
7. **Backward and re-entry in rows.** From a live determination: provenance views to source, admission, search and artefact; raise a follow-up and a gate, re-read, retire and re-determine; check the supersession pointer. Settles HS-1's direction matrix cells marked unexercised.

---

## 6. What this pass could not resolve

- Why `doctrine_recheck.py` exits 1 bare while the diff-scoped gate is green (B-57).
- What `test_scan_contract`, `validate_schema_cross_check` and `research_dod` fail on (B-54).
- Whether `add-source` refuses a NULL verification standing when a URL is given.
- Whether `emit_batch_sql.py` refuses the second parallel batch at capture (scenario 4).
- Whether an open determination gate changes anything the engine stores (B-51 shows the hash does not move).
- Round 2's sweep refusals were read at their messages; the split between script-induced and semantic refusal is by the placeholder appearing in the message and is a lower bound.

---

## 7. Round 3 (`results3/`), and what it overturns

Round 3 (`stress_run3.py`) was written to repair the faults §4 named and to run the scenarios of §5. Parts: `probes`, `real`, `guards`, `batches`, `lifecycle`, `reentry`, `batteries`. Counts: `python3 -I -c "import json,glob,collections;c=collections.Counter(str(json.loads(l)['rc']) for f in glob.glob('results3/*/log.jsonl') for l in open(f));print(sum(c.values()),dict(c))"`.

### 7.0 Sentences of §0 to §6 that no longer stand
| Earlier sentence | Now |
|---|---|
| "no extraction … was written" (§0 item 1, §2, §4 W-2) | Three extractions were written on `REF-00139` under three lens tags, with a relation edge and a population match (`real.add-extraction.SCI`, `.MS`, `.ALL`, `real.relate-extraction`, `real.add-population-match`) [V]. No candidate and no citation-mining row has been written in any round. |
| "every one of the determinations … is `pending`" (§0 item 1) | True of rounds 1 and 2. Round 3 holds six `provisional` determinations on one database (`real.assess.*`) [V]. |
| "no determination passed through the write path" (§0 item 1, §2.2 item 3) | Round 3 attempted it and failed at rebuild. **The failure is the script's:** its clone was reused across three runs and held three migration files of the same batch (`ls <stress-run>/real/clone/scripts/migrations | grep 20261112`). Re-run by this leg in a clean clone with one migration emitted from the same `batch.sql`: rebuild exits 0 and the rebuilt database equals the scratch database row for row in every table but the migration ledger; six live determinations; `PRAGMA foreign_key_check` empty [V]. The write path carries determinations. |
| "no registry battery ran" (§0 item 1, §2.2 item 2) | All ten ran as `--battery <name> --all` and returned PASS (`results3/batteries/log.jsonl`) [V]. |
| "parallel batches … surface at rebuild"; AT-101 unproven (§2.2 item 1, §3) | The second batch is refused **at capture**: "the scratch was copied from a different base, or rows were deleted. Refusing to emit" (`batches.capture-B-against-A`) [V]. The message does not name the remedy. |
| The claimed-number finding was "not yet through the writer" (§2.3 item 1) | Reproduced at the writer (7.2). |
| F-10's collisions were shown only on mark-only pairs by this leg (§2.2 item 5) | Reproduced by the script's own probe (7.1). |

### 7.1 Classification, round 3
| id | part | behaviour | evidence | cause | class |
|---|---|---|---|---|---|
| B-62 | probes | Quotes differing only in a vowel sign (Devanagari), a tone mark (Thai), pointing (Hebrew), vowel marks (Arabic) or voicing (kana) normalise to one string; `0.6`, `0,6` and full-width `０．６` collide | `results3/probes/log.jsonl` `collisions_rl.normalise_quote` [V] | P | defect |
| B-63 | probes | The name tokeniser returns nothing for every non-Latin probe string, Hangul included | same line, `empty_name_token_sets` [V] | P | defect |
| B-64 | real | A full-read scan, an observation, an adjudication, three extractions, a relation edge and a second population grade were written by the sanctioned verbs | `real.record-scan` to `real.add-population-match` [V] | P | as-designed |
| B-65 | real | A byte-identical extraction is refused; a divergent one is written with a note | `real.add-extraction.MOB`, `.SCI` [V] | P | refusal-correct |
| B-66 | real | Six determinations of parameter 3 on one database (`MOB`, `SCI`, `MS`, `ALL`, an ICF code, an access need) report the same sources, the same extraction count and the same marker, with figures tagged `SCI`, `MS` and `ALL` present | `real.assess.*`; `real/assess-*.json` [V] | P | defect |
| B-67 | real | With six live determinations: `test_db_integrity` exits 1 at C10; `validate_evidence_state` PASS over live and retired cells; `derivation_handshake_integrity` CLEAN over six | `real.gate.*` [V] | P | as-designed |
| B-68 | real | Determination views return rows once determinations exist | `real.render-views` [V] | P | as-designed |
| B-69 | real | Rebuild fails on a duplicated batch | `real.migrate-rebuild`; three files in the reused clone [V] | X | vacuous pass |
| B-70 | guards | Claimed `1:1`, `1.2` and `112` are each accepted against a quote stating `1:2`, `1:5`, `1:12` | `guards.digit-substring`, `.decimal-shift`, `.drop-colon` [V] | P | defect |
| B-71 | guards | Claimed `twelve` is accepted: a value with no digit is not checked at all | `guards.number-in-words` [V] | P | defect |
| B-72 | guards | Claimed `1:120` refused; claimed full-width `１：１２` refused | `guards.extra-digit`, `.fullwidth-digits` [V] | P | refusal-correct |
| B-73 | guards | A unit cell holding prose ("mm per metre of rise (stated 1:12)") is accepted | `guards.unit-in-prose` [V] | P | defect |
| B-74 | guards | A quote with a Cyrillic look-alike letter is refused as not found | `guards.quote-homoglyph` [V] | P | refusal-correct |
| B-75 | guards | The extra-space and truncated-quote probes were stopped by a missing locator argument | `guards.quote-extra-space`, `.quote-truncated` [V] | X | vacuous pass |
| B-76 | batches | Batch B, captured from the old base after batch A is applied, is refused at capture | `batches.capture-B-against-A` [V] | P | refusal-correct |
| B-77 | lifecycle | A new parameter adds one owed pair per source; a targeted full read of a held text discharges its pair as read-nothing-found; retiring the parameter removes its pairs | `lifecycle.ledger-*`, `lifecycle.targeted-scan` [V] | P | as-designed |
| B-78 | lifecycle | `thermal comfort` promoted to a parameter again | `lifecycle.add-parameter` [V] | P | defect |
| B-79 | lifecycle | `merge-parameter --from 11 --into 3` refused for the open gate on parameter 3; merge is untested | `lifecycle.merge-parameter` [V] | X | vacuous pass |
| B-80 | reentry | Retire, then determine the same cell again: the new row is written and the retired row's `superseded_by_specification_id` stays NULL | `reentry.retire-specification`, `reentry.assess-2-same-cell`, `reentry.supersession-pointer` (row 9 against row 10) [V] | P | defect |
| B-81 | reentry | A follow-up is raised and resolved; the one open gate is resolved; `raise-determination-gate` refused for a missing argument | `reentry.*` [V] | P/X | as-designed |
| B-82 | batteries | Every battery PASS. Advisory failures: `scan_debt` (data); `verified_scan_integrity` (db_integrity); `test_scan_contract` (tests); `validate_schema_cross_check` (schema); `skill_vocabulary_audit`, `retired_vocabulary`, `research_tooling_separation` (governance); `research_dod`, `research_protocol_audit`, `metadata_integrity_audit` (research). Nothing-in-scope: `extraction_follow_up_audit`, `citation_mining_session`, `medical_lens_integrity`, `adversarial_pass_recorded`, `search_log_completeness` | `results3/batteries/log.jsonl`, the `RESULT:`, `NON-BLOCKING failures` and `NOTHING-IN-SCOPE` lines [V] | P | as-designed |

Round-3 rows by class: `grep -c -E '^\| B-(6[2-9]|7[0-9]|8[0-2]) .*\| defect \|$' hs-stress-audit.md`, and likewise for the other classes.

### 7.2 What round 3 settles
1. **The number check fails at the writer** (B-70, B-71). IMP-44 stands and is widened: a claimed value with no digit must be refused or carried by a typed exemption, not passed unchecked.
2. **The normaliser collisions are real** (B-62) and the tokeniser is empty for every non-Latin script tried (B-63). IMP-23 stands.
3. **Lens-blindness holds on real multi-lens rows on one database** (B-66). IMP-08 stands as the first precondition of a determination.
4. **The write path carries a determination** (7.0, this leg's clean re-run). The precondition list for a first live determination loses nothing and gains nothing.
5. **Parallel batches are stopped at capture** (B-76). IMP-41 is reduced to a sentence in the pipeline skill and, optionally, a clearer message; AT-101 is green for the refusal. OD-27 stands only as the owner's choice.
6. **Catalogue growth has a working discharge route where the text is held** (B-77): a targeted full read. OD-23's option (a) is therefore supported by the code today for held texts; what is missing is still the inventory that would make a re-read unnecessary.
7. **Re-determination leaves no supersession pointer** (B-80). New: IMP-46, AT-103.
8. **The writer accepts prose in the unit cell** (B-73). This is the prior workplan's T-1a refusal, unbuilt; no new entry.
9. **The blocking batteries are green on a copy of `main`** (B-82). Every earlier "unrun" statement about batteries is withdrawn.

### 7.3 Still untested after three rounds
A candidate staged and resolved; a citation-mining row; `merge-parameter` and `decline-parameter` on a parameter with figures; `raise-determination-gate`; a non-English source read end to end; `add-source` with a URL and no standing; a quote differing from the held text only in a mark, through the writer with a locator given; a session-scoped gate with `scratchpad/CURRENT` set.

### 7.4 Script faults in round 3 (proposed fixes, not made)
The clone is reused across runs (delete it first, or emit into a fresh directory); two guard probes omit the locator; `raise-determination-gate` omits `--trigger-evidence-type`; the merge probe targets a parameter with an open gate.

## 8. Final pass: what the stress logs were used for after round 3

- **Timings** (REQ-101, efficient): read from the logs' `seconds` field; no efficiency task follows (HS-3 §9.1).
- **Refusal messages** (REQ-103, operational dead ends): the distinct `REFUSING` messages across all three rounds, and how many carry a cue to a next action, are counted by the command in workplan task T-043. The cue test is a regular expression and therefore a heuristic [I]; the task lists the messages it flags so a person can judge each.
- **Characterisation harness** (REQ-101, clean and centralized): the scripts are repaired and given a normalised log diff by workplan task T-014; tasks that claim to preserve behaviour cite that diff.
- **Not added:** no new stress round was run in the final pass.

