# RETAINED — what to keep from the stress tests across topics, what to discard, and why

_Handshake leg, 2026-11-12 (UTC). Authority: the owner's statement of 2026-11-12 (fourth), `references/project-standards.md` (`grep -n -F 'Owner statement 2026-11-12 (fourth)' references/project-standards.md`): "permission to retain information from the stress tests across topics if fable deems them worthwhile". Its ledger reading, marked there as an unratified assumption: records may be kept; rows labelled `STRESS-FIXTURE` are not retained as data; a real research row is entered by migration, in a research pull request apart from tooling, after re-retrieval and verification. The judgments below are this leg's and are reasoned in `audit/hs-stress-audit.md` (HS-5). Nothing here is implemented._

## 0. Verdict first

**Keep the behaviours, six probes as future regression tests, and the two logs that hold unique evidence. Keep no database row: none of the rows the scripts wrote is research. Discard the nine scratch databases, the generated HTML, and seven of the nine round-1 logs as evidence (they repeat one sequence).**

No real source was retrieved in either round, so there is no real research row to retain. Six statements in the probe strings name real instruments from memory; they may be kept only as leads to verify, by the route in §3.

## 1. Keep

### 1.1 Behaviours (as findings, in `audit/hs-stress-audit.md` §1)
All of B-01 to B-61. The ones that hold in every topic and should be read before any research in any topic:
- A parameter can be minted from any term in one command, and each one adds an owed reading per source (B-05, B-06).
- Research batches are serial: a second batch captured from the same base fails at rebuild (B-40).
- `add-source` will write a source with no verification standing (B-12).
- The claimed-number check accepts a shifted decimal (HS-5 §2.3 item 1).
- The engine stores a `pending` row and a gap for any lens asked (B-17).
- A second run for a live cell is refused; retire first (B-37).
- `run_checks.py --battery <name>` needs `--kinds`, `--all` or `--changed-from` (B-53).

### 1.2 Probes worth making permanent (each as a test in the existing `scripts/tests/` battery, in a tooling pull request; none exists yet)
| Probe | Becomes the regression test for | Change needed first |
|---|---|---|
| `lang_probe.py` string pairs | IMP-23 (AT-59, AT-60) | pairs that differ only in a vowel sign, a voicing mark, pointing, a tone mark or a decimal point; drop `dbcore.normalise_quote_text`, which is a whitespace helper for ledger quotes and not a copy of the quote normaliser |
| The decimal-shift and digit-substring cases of HS-5 §2.3 | IMP-44 (AT-79) | run through `add-extraction` with a scan recorded |
| The crosstopic replay (three captures, one history) | IMP-41 (AT-101) | add the capture-time check of batch B against the canonical copy after batch A |
| `add-parameter` on an element term and on a legal-concept term | IMP-42 (AT-77) | none |
| `add-source` with no verification standing | IMP-43 (AT-78) | add the case with a URL |
| `delete-connection` on a missing id | IMP-45 (AT-100) | none |
| Two fresh copies, one cell, byte-identical output | REQ-025 | already asserted in spirit by `scripts/tests/test_assess_cell_pilot.py`; keep only if that file lacks the two-copy form |
| The lens matrix on parameters 3 and 12 with the gates | IMP-08 (AT-50, AT-51) | HS-5 §5 scenario 2 |

### 1.3 Records
- `stress/results/acoustics/log.jsonl` and `stress/results/crosstopic/log.jsonl`: one full round-1 sequence and the only cross-batch replay.
- From the other topics, only what differs: `base.add-parameter-existing-term` (reach, thermal, grabbar, method), the luminance determinations for parameter 8, and each topic's `lateral.script-probe` line.
- `stress/results2/chain/log.jsonl` and `stress/results2/tools/log.jsonl`: the only record of a full-read scan written by the sanctioned verb, of the follow-up and alias-promotion routes, and of the diff-scoped gate's state on a copy of `main`.
- `stress/results2/sweep/log.jsonl`: keep as a map of each verb's first refusal message; it is not evidence that a verb works.
- The scripts `stress_run.py`, `stress_run2.py`, `lang_probe.py`, `run_logged.py`, with the changes listed in HS-5 §4 made in a later pass.

### 1.4 Cross-topic facts about the base (leads for base work, not rows)
- Topics with no matching term at all: flash, cost (`base.terms-for-topic` returns no row).
- Terms that exist and are not parameters, and should not become one as they stand: `TERM-008` (an element), `TERM-041` (a functional axis), `TERM-075` (a legal concept); `TERM-063` needs a quantity before it can be one.
- Every slug the script used exists (`base.slug`), each with zero searched pairs.

## 2. Discard

| What | Why |
|---|---|
| Every row written by the scripts: sources `REF-01037` and after in each scratch copy, the term `wheelchair propulsion` and its parameter, the fixture searches, connections, gaps, case study, code lead, follow-up, the changed definition of `TERM-001`, the resolved gate, the closed adversarial pass | Labelled `STRESS-FIXTURE` or made with fixture arguments; they exercised a path and are not research. They exist only in scratch copies; none may be captured into a migration |
| The scratch databases, clones, `owner_browser.html` files and rebuilt databases under `…/scratchpad/stress-run/` | Reproducible from the scripts; outside git |
| The round-1 logs of the other seven topics, as evidence of anything beyond §1.3 | They repeat the acoustics sequence step for step |
| The engine reports under `results/*/determinations/` | Every one is `pending`; six carry figures and say only that parameter 8 has no direction |
| The probe sentences themselves ("Die Nachhallzeit … höchstens 0,6 s" and the rest) as content | Invented by the script's author to exercise scripts and number formats; they are not quotations of any source and must never be entered as a quote, an alias or an observed term |

## 3. Real research that could be retained, and the only route by which it may enter

No row qualifies today. The following are **leads**, named in the `method` topic's probe strings from memory and unverified. Each may enter the database only as follows: (1) a tooling-independent research pull request; (2) the instrument is retrieved through `scripts/research/retrieval_log.py` and persisted, or its location logged where the file is large (PS:5126); (3) it is recorded as a code lead (`db.py add-code-lead`) or staged locator, and admitted with `add-source` only after re-retrieval, with its bibliographic fields taken from the payload and its verification standing stated (CLAUDE.md §5(c); R10); (4) the rows reach `data/guidebook.db` by `emit_batch_sql.py` → `emit_data_migration.py` → `migrate_db.py`. None of the six may be typed in from this file.

| Lead (as the script wrote it; unverified) | Note |
|---|---|
| Ontario Building Code, O. Reg. 332/12, Section 3.8 | the database already holds `REF-01013`, titled "Ontario Building Code — O. Reg. 163/24, s.3.8.3.4"; the two regulation numbers differ and must be reconciled from the instrument, not from either string. Sub-national: waits on OD-01 |
| Code de construction du Québec, chapitre I, section 3.8 | sub-national; waits on OD-01 |
| Landesbauordnung Nordrhein-Westfalen, § 49 | sub-national; waits on OD-01 |
| Código Técnico de la Edificación, DB-SUA, Anejo A | in scope under the P1+P2+P3 answer (ES) |
| 建築基準法施行令第126条の2 | the article number is the script's and is unverified |
| D.M. 236/1989, art. 4.1 | in scope under the P1+P2+P3 answer (IT) |

Whether any of them is worth admitting is a research judgment for the session that takes the topic; this file only says they are not to be lost and not to be trusted.

## 4. What must not be carried across topics

- The parameter ids and `ref_id`s the scripts allocated (13, 14, `REF-01037` to `REF-01039`, `TERM-095`, `GAP-103`, `GAP-104`, `CON-0001`): the next real batch will allocate the same values.
- Any conclusion that a verb "works" from round 2's sweep: most verbs ran with `--dry-run` on placeholder arguments.
- Any conclusion about lenses from the per-topic determinations: all are `pending`.
