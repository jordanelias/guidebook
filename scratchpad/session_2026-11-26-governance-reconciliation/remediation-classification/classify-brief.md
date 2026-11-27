# Brief: how much of the remediation plan needs doing to meet the project's goal

Repository /home/user/guidebook (branch ccr-64231823-gqy3xr). READ-ONLY: edit nothing in the repository, never write the database (copy it to a scratch path under the scratchpad directory and set GUIDEBOOK_DB_PATH inline on every call if you must run a writer, and prefer read-only queries: sqlite3 'file:data/guidebook.db?mode=ro'). Write only to your named output file in /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/. Canadian English, objective tone, no flattery. The Grep tool is blinded by .ignore for sessions/, transcripts/, _archived/, references/bpc/, references/search-log/, versions/, workplan/_superseded/: use `git grep` through Bash.

## The owner's question (typed, 2026-11-27)
"Have Opus adjudicate how much of this remediation plan needs to be done in order to meet our goal/mission of methodically performing research, recording data in a regimented way, correctly assigning parameters and relevancy to populations/needs/ICF, adjudicating this data in relationship to contemporaries, synthesize data into usable information that can be used to determine/specify accessible design techniques that can be rendered"
The owner's standing words: "this is a simple project where we build as little machinery as possible to enact our goal"; "Remember that this project is simple!!!"; CLAUDE.md section 8: before adding a check, script or table, state what wrong thing reaches the GUIDEBOOK if it does not exist; if the answer is about the apparatus rather than the book, do not add it; deleting is as cheap as adding and needs evidence, not permission. DR-2026-08-19 section 4: the only acceptance criterion apparatus cannot satisfy is one answered question, published: a determination, its governing sources, its population-match grading and its search log including the empty searches, rendered and readable.

## The six goal elements (use these labels)
E1 methodical research (search, log, screen, mine)
E2 regimented recording (admission, verification, translation, units, extraction)
E3 correctly assigning parameters and relevancy to populations / access needs / ICF (base vocabularies, lens links, the identity-need-ICF matrix)
E4 adjudicating the data in relation to contemporaries (compare, convergence, independence, conflicts)
E5 synthesizing into usable information that determines/specifies accessible design techniques (synthesis and the determination)
E6 render

## The plan
workplan/2026-11-12-bidirectional-pipeline/: REMEDIATION-WORKPLAN.md (index, owner decision register, section 10 Definition of Done D-01..D-21), tasks/T-*.md (one self-contained file per task), the generated batch plan scratchpad copy remediation-plan-generated.md, the open-task list open-tasks.tsv (73 open tasks; id, batch, kind, status, deps, file, title) in the scratchpad directory. The ledger references/project-standards.md holds the owner's rulings (find with `git grep -n -F '<quote>' -- references/project-standards.md`; the newest entries are at the end and supersede older plan text, CLAUDE.md rule 0). CLAUDE.md is the working guide. The pipeline stages: base, research, evidence, judgment, synthesis, specification, render (governance/pipeline-contract.yaml).

## Classify each assigned task, with evidence
Classes (exactly one per task):
- NEEDED-NOW: without it a goal element cannot be done at all, or a WRONG THING REACHES THE GUIDEBOOK (a wrong figure, wrong group, misquote, fabricated or mis-tiered source, a wrong marker). Name the element (E1..E6) and the specific wrong thing, and say whether it is on the shortest path to one published determination.
- NEEDED-LATER: serves a goal element but is not required before the first published determination; say why it can wait.
- APPARATUS: checks, tests, gates, instruments, registers, refactors or renames about the machinery; no wrong thing reaches the book if it is not done. Recommend RETIRE (delete the task file and anything it would add) or DEFER, with the CLAUDE.md section 8 reasoning.
- ALREADY-DONE-OR-SUPERSEDED: the defect no longer exists, the work merged under another task, a later owner ruling overtook it, or the task is withdrawn. Prove it: run or read the task's own evidence command read-only, read the code, grep the ledger.
- OWNER-HOLD: cannot proceed without an owner decision; name the decision and what it releases.
For every task: (1) read the task file's purpose, "Today" evidence and dependency sections (you need not read every line of long task files, but read enough to judge); (2) test whether the defect the task names is REAL TODAY: task files were written 2026-11-12 to 2026-11-26 and may be stale; run the task's read-only evidence command or read the code; (3) check the ledger for a later ruling that changes it; (4) record dependencies you find that the plan does not list.
Do not decide doctrine. If a classification turns on an owner meaning, say OWNER-HOLD and state the question plainly.

## Output format
A table first: id | title | class | element(s) | on the shortest path to one published determination? (y/n) | one-line reason | confidence. Then per-task detail: the evidence (command and result, or file:line quote), the wrong thing that reaches the book (for NEEDED-NOW), what to delete (for APPARATUS), the owner question (for OWNER-HOLD). Mark anything you could not verify [UNVERIFIED] with the reason, and say what you did not reach. End with a summary of at most 150 words: counts by class (derive them with a command over your own table, do not hand-count), and the tasks you consider the critical few. Return the file path.
