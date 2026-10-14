# The Phase 3 and 4.1 adversarial pass (read-only Fable antagonist, detached worktree at 838a7ae) and what became of each finding
Every finding was reproduced or checked against the artifact. Repairs sit on the branch that introduced the defect and were merged upward (`git log --oneline --merges stack/5.research-parameter-note`).

| finding | verdict | disposition |
|---|---|---|
| F1 `amend-source --field co1_source_type` stored a retired value (the generic path gates nothing on a column with no CHECK) | sustained, reproduced | evidence branch: constrained to the enum; O05, fault-injected |
| F2 ratified doctrine still named the five retired Co-1 types and said no value distinguished participatory work; six ACTIVE atoms quoted it | sustained | evidence branch: `evidence-architecture.md`, `held-tensions.md` and the mapping reference name the live values; atoms rewritten, EVI-154 deleted; listed as owner merges |
| F3 the cell-level floor of the mean is attributed to the owner, whose 2026-09-13 rulings are about a derived figure's inputs | sustained | specification branch: comments say whose function it is and that the subject is RULINGS R7 as amended by R49(a); **owner item** (also: the gate-capped provisional row keeps its anchors' band) |
| F4 the 4.1 commit's claim about the kept verbs is false for four | sustained | claim corrected in the notes (erratum); the four are kept as the CLI's only route for a correction |
| F5 CLAUDE.md section 6 still said the rename was "not yet applied" | sustained | 3.base branch |
| F6 prose callers of the 4.1 deletions | sustained for the instrument README (fixed in the 4.1 merge commit); **declined** for `architecture/sqlite-data-layer.md`, a 2026-05-05 design record |
| F7 hand-typed numbers | sustained | the "46 occurrences" entry and the "23 data migrations" comment carry the command; the "about 9,700" in the 4.1 commit message cannot be amended and is corrected in the notes (9,898 at the time) |
| F8 `add-candidate` accepted a `--found-under-slug` on a slugless search | sustained | 3.research part 2 branch: refused, N04 extended, fault-injected |
| F9 the third-part `BY` quote is the delegation entry's own sentence | withheld for the owner | owner item in the evidence and judgment notes |
| F10 base and research notes omitted the owner-merge list | sustained | notes; the list is now a command with the names beside it |
| F11 a `confirms` edge from a finding row about another parameter counted | sustained | specification branch: both rows must share a parameter; test, fault-injected. "Several findings confirm one code" is not separately tested: every anchoring tier is the full band, so the floor of their mean is full whatever the number |
| F12 the grain change was presented as continuity | sustained | notes now say REF-00993's grain flips and that no live determination moved (engine output equal before and after except the marker) |

**Process slips of mine in the repair, disclosed.** The upward-merge helper, run on a branch that already contained its predecessor, committed a regeneration-only commit named as a merge; it was dropped by `git reset --hard` to the previous commit on a branch never published, and the real merge followed. A test-file conflict between O05 and V01/V02 (both appended at the same place) was resolved by keeping both, O05 first.
