# Pipeline state graph — audit instrument

A derived, self-checking model of the pipeline, tied to the owner's rulings and directions, for auditing agent work
(mine included) before and after it is done. It is working material: **not a ruling, not registered as a check, and not
in a PR.** Where it says a ruling is carried or not carried by the schema, code or CI, that is a probe result you can
re-run; where it says a direction follows from CLAUDE.md rule 0, that is an inference an agent made. Two independent
adversarial passes (a Fable 5.1 agent each; the second attacked the first's findings and the repairs) have corrected
it; both are summarised below, and neither is proof.

## What is here

| file | what it is | how it is made |
|---|---|---|
| `atoms/atoms-*.jsonl` | one claim per line — the owner's rulings, ratified governance documents, process rules, CLAUDE.md — each with a **verbatim quote**, source `file:line`, modality, speaker, date, status, enforcement | extracted by reading; quotes verified mechanically; claims reviewed only on a sample |
| `conflicts.yaml` → `CONFLICTS.md` | the **active-conflicts register**: adjudicated disagreements between atoms, or between an atom and the mechanism, plus a table of atom statuses that lag a later ruling | hand-adjudicated; atom ids, classes and probes checked |
| `machines.yaml` → `STATE-GRAPH.md` §3 | state machines: who moves a row between states, under what guard | hand-authored; every guard carries a code needle re-read on each run |
| `STATE-GRAPH.md` §1, 2, 2a, 4–9 | stages, tables, foreign keys (including forward-pointing ones), views, writers, the UNWRITABLE set, quarantined checks, ruling-vs-mechanism probes, tree delta | **derived** from the live repo |
| `capabilities.yaml` → `CAPABILITIES.md` | the four-capability interrogation (mine one source across many parameters · grow the parameter base · synthesize across parameters · specify then render) | predicates evaluated against the live tree |
| `ATOMS.tsv`, `OPEN-QUESTIONS.tsv`, `AMBIGUITIES.tsv`, `graph.json` | flat views for grep | generated |
| `build_graph.py` | the generator, checker and self-test | — |
| `verify_atoms.py` | stand-alone quote verifier for one atoms file | — |

`atoms-added.jsonl` (`ADD-nnn`) holds atoms added after the adversarial review; `atoms-wrk.jsonl` (`WRK-nnn`)
holds the 2026-08-18 owner rulings recorded in `workplan/` that the first extraction missed (many are marked PROPOSED:
the frame proposal is mostly the author's own text around the six rulings R1–R6).

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
   and, if it holds a status, its machine in §3. A transition the machine does not list, or lists as having no writer,
   is a finding, not a licence.
2. **Find the rulings that bind it:** `grep -i '<term>' workplan/pipeline-state-graph/ATOMS.tsv`. Prefer `OWNER_QUOTED`
   over `OWNER_RELAYED` over `RATIFIED_DOC`; an `AGENT_PROPOSAL` is not a ruling even where later text relies on it.
   `SUPERSEDED` is history (`status_evidence` and `superseded_by` say why). **`AMENDED` is not history:** the quote is
   either the amended, live form or the pre-amendment form that a later ruling changed in part — read
   `status_evidence`/`ambiguity` to see which. `.ignore` hides `sessions/` from the Grep tool; this table does not.
3. **Check the register:** if the atoms you rely on appear in a `CONFLICTS.md` entry whose direction is `UNSETTLED`,
   do not pick a side — put it to the owner. If the direction is stated, it is an inference from rule 0, not a ruling;
   say so when you act on it.
4. **Check the mechanism, not the prose.** A `FAIL` or `NOT-BUILT` probe means the ruling is not carried by the schema,
   code or CI, so compliance is yours (the rule 5 / rule 7 "you are the gate" case). A `PASS` means the probe could see
   the thing and found it; it does not mean the ruling is fully carried. Several probes are lexical (P-H, P-O,
   P-STATUS-WRITERS) and the register says so.
5. **After acting**, run `--check`. If you changed a guard, a vocabulary or a ruling-bearing file, regenerate and read
   the diff of `CONFLICTS.md` and the probe table.

## What the checks prove, and what they do not

- **Proved mechanically:** each atom's quote occurs verbatim in its source, within three lines of the cited line; each conflict cites atoms that exist and
  probes that exist; each machine's state set (or `vocabs:` entry) equals the column's own CHECK, and the count of
  abstract machines with no single column is printed; each transition's guard still appears in the cited function (or,
  for `absent: true`, still does not); every stage assignment is complete and agrees with the contract; every probe ran
  and its source contains a literal path that can return PASS (or INFO) -- a reachability lint, **not** evidence that the
  probe tests the right thing: P-R passed that lint while testing the wrong function and reporting a built feature as
  not built; each status correction's `current` status is re-read and each deciding atom must exist, be dated no
  earlier than the atom it corrects, and not itself be superseded -- nothing checks that it says what `why` claims. `--selftest` shows these checks fail when what they guard is broken,
  including a mutation of probe reachability, of a capability verdict and of the stage map.
- **Not proved:** that an atom's `claim` is a fair reading of its quote (an adversarial pass drew 40 atoms at random
  and found 2 unfair, which were repaired; the remaining atoms are unaudited beyond that sample); that a conflict's
  direction is right (the same pass found several direction and speaker errors in the S1 entries, which were repaired
  and re-checked against the sources); that the transition guards are all the guards; that a lexical probe has no
  false negative. These are judgments, and each conflict records its confidence.
- **The adversarial passes** are reviews by other agents, not proofs. Pass 1 found direction, speaker and probe errors
  in the severity-1 entries; pass 2 found one false probe verdict (P-R), a settlement resting on an unsourced relay
  (C-027), mis-tagged speakers and statuses (CLM-*, EVI-059/060, WRK-199/200/201/204/222), and a machine edge that
  contradicted its own guard (M08), and sampled 30 of the workplan atoms (3 failures). The repairs were applied, the
  remaining workplan atoms were **not** re-audited beyond that sample, and C-029, C-032, C-034 and C-039 were not
  re-read by pass 2 beyond their atom lists.

## Known gaps in coverage

- `references/project-standards.md` lines 300–512 were read through an agent, not first-hand.
- Domain-content rules (door widths, thermal ranges and the like in `references/`) are **out of scope**: the graph models
  the pipeline, not the guidebook's design content.
- `workplan/`: the three ruling-bearing files named in the operative instrument's supersession table
  (`2026-08-18-research-frame-proposal.md`, `2026-08-18-handoff-next-session.md`,
  `2026-08-20-adversarial-adjudication-a18-aut.md`) are atomised (`WRK-`). The two documents it labels OPERATIVE
  execution plans (`2026-08-22-master-execution-plan.md`, `2026-08-22-agonist-antagonist-execution-plan.md`) and the
  rest of `workplan/` are **not** atomised.
- Atoms record what a document says. A later ruling that supersedes a document without marking it is carried in
  `ambiguity` and in `conflicts.yaml`, not in `status`. About thirty quotes appear in more than one atom (a ledger entry
  restating a DR); `--check` prints the distinct-quote count.
- The generator describes the checkout it is run in. The unreleased tooling branch is a column via `--compare`.

## Process note

Run the generator from the repository root. Calling it (or any other command) with the working directory inside this
folder made the transcript-preservation hook write a copy of the transcripts under it, and a `git add` of the folder
committed that copy; it was removed in a later commit, but the blobs remain in the branch's history.

## Status

Committed to the working branch; not registered in `governance/check-registry.yaml`. PR #171 (batch-24 research) was merged
on 2026-10-10, so the instrument and the workplan are the only unmerged content; they contain no research rows and ship as
their own tooling-and-documents PR (CLAUDE.md rule 10). If kept, `--check` is the candidate registry entry (it prints `EXAMINED:`, reads the repo only, and has a
self-test). The owner decides whether to keep it.
