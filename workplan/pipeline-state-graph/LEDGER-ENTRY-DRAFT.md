# Draft ledger entry (not in the ledger)

**Status:** DRAFT, written by the assistant on 2026-10-14 after the owner's message (`transcripts/harness_db856d85/main.jsonl:7814`). The ledger (`references/project-standards.md`) is the owner's append-only record; this text is **not** in it. The owner makes the resolutions of `RULINGS.md` section (G) effective by appending it (or an amended version) in one commit. Until then (G) is the assistant's resolution under the owner's message, and no destructive step (1.4, 1.5) runs.

---

## Owner delegation 2026-10-14 — the simplification plan's §4 items are resolved by the assistant, including searches without a slug

Asked to design step 1.5a of `workplan/2026-10-12-simplification-workplan.md` and shown its §4 list of items waiting for the owner, the owner wrote (both absorbed mid-turn; `transcripts/harness_db856d85/main.jsonl:7802` and `:7814`):

> "design 15a for me so long as it makes sense with system"

> "§4, including the nullable-slug question.
>
> no idea what these are, but resolve them for me in a logical manner"

**What this does.** It hands every item in §4 of the plan to the assistant to resolve, on the premises already in the repository (LED-154 already delegates items presented to the owner to Fable 5.1). The resolutions, with their premises, inference and what would overturn each, are in `workplan/pipeline-state-graph/RULINGS.md` section (G); this entry does not copy them (point, do not copy). In short: the proposed rulings R1 to R42 are adopted as amended by the rehearsals; R12's language conjunct survives; the bytes pointer takes the favoured `retrievals` shape, to be rehearsed before it is built; `case_studies` and `economics_entries` are not folded; a full-read figure marked preliminary may set a value when tagged; a search may be recorded without a slug when it names a parameter or a mined source (R43); `PopulationCode` is retired (R44); the retired rule identifiers stay readable (R45); the frozen coverage verbs and the register text are deleted (R46, R47); the marker readings are fixed (R48); the five row-bearing drops of R3, the names of R14 (M4), the root key of R24 and the columns of R25 are confirmed (R49).

**What it does not do.** It executes nothing. Each step lands in its own pull request, which the owner reads before it merges; the destructive steps (1.4 and 1.5) drop only rows the entry states are reconstructible, or whose record survives in the git history of the blob. The owner can overturn any resolution by a later statement (rule 0).

**The one supersession this entry decides** (R24): the rule becomes that `source_value_extractions.root_id` references `external_root_registry` and nothing else; an in-corpus root is named by `root_ref_id`, which is how the two columns already divide. It replaces the sentence of `governance/evidence-architecture.md` (a) that let a `root_id` resolve to a `root_ref_id`. The `SUPERSEDES`/`BY` pair is **not** written here: `supersession_backpointer_audit` requires the target document to carry the pointer in the same change, so the pair, the amended sentence and the update of atom EVI-162 arrive together in the pull request that builds the key (plan step 3 judgment).

CONDITION: any session asking whether the plan's §4 items are still waiting for the owner, whether a row-bearing table may be dropped, whether a search may be recorded without a slug, what names the identity registry takes, whether `root_id` may name an in-corpus source, or whether the simplification plan may be executed.
ACTION: (1) Treat the §4 items as resolved by `RULINGS.md` section (G) unless the owner says otherwise. (2) Execute the plan one step per pull request, opened last, and put each owner-merge edit in the diff of its own step. (3) Do not drop a row-bearing table except in steps 1.4 and 1.5, after `--rebuild` shows the rows are reproduced or the entry's record of survival applies. (4) The nullable-slug resolution (R43) is rehearsed before it is built. (5) The owner's override of any resolution is a later statement and wins.
DATE: 2026-10-14 — owner statements, quoted above.
