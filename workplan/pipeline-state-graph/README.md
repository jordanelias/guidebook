# Pipeline state graph — audit instrument

A derived, self-checking model of the pipeline, tied to the owner's rulings and directions, for auditing agent work
(mine included) before and after it is done. **Uncommitted working material:** nothing here is a ruling, and it is not
wired into `governance/check-registry.yaml` (CLAUDE.md §8: nothing is added without naming what reads it — see
"Status" below).

## What is here

| file | what it is | how it is made |
|---|---|---|
| `atoms/atoms-*.jsonl` | every active statement of the owner's rulings, the ratified governance documents, the process rules and CLAUDE.md, reduced to one claim each, with a **verbatim quote**, source `file:line`, modality, speaker, date, status, enforcement | extracted by reading; quotes verified mechanically |
| `conflicts.yaml` → `CONFLICTS.md` | the **active-conflicts register**: adjudicated disagreements between atoms, or between an atom and the mechanism | hand-adjudicated; atom ids, classes and probes checked |
| `machines.yaml` → `STATE-GRAPH.md` §3 | state machines: who moves a row between states, under what guard | hand-authored; every guard carries a code needle re-read on each run |
| `STATE-GRAPH.md` §1, 2, 4–8 | stages, tables, foreign keys, views, writers, UNWRITABLE set, quarantined checks, ruling-vs-mechanism probes | **derived** from the live repo |
| `capabilities.yaml` → `CAPABILITIES.md` | the four-capability interrogation (mine one source across many parameters · grow the parameter base · synthesize across parameters · specify then render) | predicates evaluated against the live tree |
| `ATOMS.tsv`, `OPEN-QUESTIONS.tsv`, `AMBIGUITIES.tsv`, `graph.json` | flat views of the above for grep | generated |
| `build_graph.py` | the generator, checker and self-test | — |
| `verify_atoms.py` | stand-alone quote verifier for one atoms file | — |

## Commands

```
python3 workplan/pipeline-state-graph/build_graph.py --check      # verify only; exit 1 on any failure
python3 workplan/pipeline-state-graph/build_graph.py --selftest   # prove the checks can go red (mutation tests)
python3 workplan/pipeline-state-graph/build_graph.py              # regenerate every derived file
python3 workplan/pipeline-state-graph/build_graph.py --compare /path/to/other/checkout   # add a tree-vs-tree column
```

Needs `pyyaml` only. Reads `data/guidebook.db` read-only. Every figure in the generated files is a result; re-run
rather than trust one (rule 7a). `--check` prints `EXAMINED: n` for each class of subject.

## How to use it to audit yourself

1. **Before acting**, name the object (table, verb, check, document). Find its stage and writers in `STATE-GRAPH.md` §4
   and, if it holds a status, its machine in §3. If the action is a transition the machine does not list, or one it
   lists as having no writer, that is a finding, not a licence.
2. **Find the rulings that bind it:** `grep -i '<term>' workplan/pipeline-state-graph/ATOMS.tsv`. Prefer `OWNER_QUOTED`
   over `OWNER_RELAYED` over `RATIFIED_DOC`. A `SUPERSEDED`/`AMENDED` atom is history; its `superseded_by` and
   `status_evidence` say why. `.ignore` hides `sessions/`; this table does not.
3. **Check the register:** if the atoms you rely on appear in a `CONFLICTS.md` entry whose direction is `UNSETTLED`,
   do not pick a side — put the conflict to the owner. If the direction is stated, it is an inference from CLAUDE.md
   rule 0, not a ruling; say so when you act on it.
4. **Check the mechanism, not the prose.** A `FAIL` or `NOT-BUILT` probe means the ruling is not carried by the schema,
   code or CI; compliance is then yours (the rule 5 / rule 7 "you are the gate" case). A `PASS` means the probe could
   see the thing; it does not mean the ruling is fully carried.
5. **After acting**, run `--check`. If you changed a guard, a vocabulary or a ruling-bearing file, re-run the generator
   and read the diff of `CONFLICTS.md` and the probe table.

## What the checks prove, and what they do not

- **Proved mechanically:** each atom's quote occurs verbatim in its source; each conflict cites atoms that exist and
  probes that exist; each machine's states equal the column's own CHECK vocabulary; each transition's guard still
  appears in the cited function (or, for `absent: true`, still does not); each stage assignment is complete and
  agrees with the contract; each probe ran. `--selftest` shows these checks fail when the thing they guard is broken.
- **Not proved:** that an atom's `claim` is a fair reading of its quote; that the conflict directions are right; that
  the transition guards are *all* the guards; that a lexical probe (P-H, P-O, P-STATUS-WRITERS) has no false
  negative. Those are judgments, made by an agent, and the register marks its confidence.
- **The heuristic primitive tags** in `ATOMS.tsv`-style views (if you build any) are regex guesses and are not used by
  any check.

## Known gaps in coverage

- `references/project-standards.md` lines 300–512 were read through an agent, not first-hand; the rest of the ledger
  and the governance documents were read first-hand or by named agents whose atoms were verified against the source.
- Domain-content rules (door widths, thermal ranges, and the like in `references/`) are **out of scope**: the graph
  models the pipeline, not the guidebook's design content. Rule atoms touching those are excluded.
- Atoms record what a document says. Their `status` follows the document's own markers; a later ruling that
  supersedes a document without marking it is carried in `ambiguity` and in `conflicts.yaml`, not in `status`.
- The generator describes the checkout it is run in. The unreleased tooling branch is a column via `--compare`.

## Status

Not committed, not registered as a check. If kept, `--check` is the candidate registry entry (it prints
`EXAMINED:`, reads the repo only, and has a self-test); what reads it would be whoever audits before a batch. Under
CLAUDE.md rules 8 and 10 that registration belongs in a tooling-only PR, and the owner decides whether to keep it.
