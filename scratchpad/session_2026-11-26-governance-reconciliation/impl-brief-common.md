# Common brief: apply the owner-approved reconciliation items (2026-11-26)

Repository: /home/user/guidebook, branch ccr-64231823-gqy3xr. Canadian English. Objective tone.

## What the owner approved (typed, this session)
"approve A and B all; reject C4; D1 retire"
So: items A1-A5 and B1-B10 of /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/approval-list.md are APPROVED. C4 is NOT APPROVED: the owner rejected the drafted text, then said the project needs ONE order of authority and asked why there would be several, so a corrected single order will be put to them separately. Until they answer, do not write any order-of-authority sentence, any DR history note about authority, or any change to which document answers "what to do now". D1 (retire the three e120 rows) is handled by someone else; do not touch the database. NOTHING ELSE is approved: do not touch items C1-C3, C5-C10, D2-D7, E, or anything not named in your assignment. If an approved item cannot be done without touching an unapproved one, do the approved part only and report the rest as SKIPPED with the reason.

## Where the exact texts are
- approval-list.md (the approved list; read all of it).
- adjudication.md (pass 1) and adjudication-2.md (pass 2): proposed texts. Where the antagonists contradict them, the antagonists' corrected text prevails: antagonist-1.md, antagonist-2.md (section "Corrections to proposed text" and its approval list), antagonist-3.md, and claude-md-audit.md for CLAUDE.md edits. All in the same scratchpad directory. They are model output: verify every quoted line in the repository before editing; if the text at a cited line is not what the report says, stop on that item and report.
- The ledger (references/project-standards.md, append-only) holds the owner's words; find rulings with `git grep -n -F '<quote>' -- references/project-standards.md` (the Grep tool is blinded by .ignore for sessions/, transcripts/, _archived/, references/bpc/, references/search-log/, versions/, workplan/_superseded/).

## Rules
1. Edit ONLY the files in your assignment, using the Edit tool. Do NOT run git commit, git add, git push, git stash or any git write. Do not edit data/guidebook.db or any migration. Do not create new documents (one log file for your own work, below, is the exception).
2. Minimal change: prefer deleting or repointing a stale sentence over adding text. No hand-typed counts or volatile facts (CLAUDE.md rules 7/7a); give a derivation command instead if a number is unavoidable. No version pins. No history or "this used to say" narrative in the files you edit (the owner asked for change-log and version discussion to be stripped); a one-line dated pointer note is allowed only where an item explicitly calls for a banner.
3. Do not change numbering of CLAUDE.md rules or sections. Do not touch the SPINE line, the goal sentence, rule 0, rule 9, the tier line, or the Co-1 warrant text in CLAUDE.md, except where an item below names that exact line.
4. After each edit, `git diff -- <file>` and confirm the change is exactly the intended one. Sweep prose callers of anything you change with `git grep -n -F` (CLAUDE.md rule 4).
5. Write a log of your work to /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/impl-<LETTER>.md: for each item ID: DONE / SKIPPED / PARTIAL, file:line before and after (short quotes), any caller you swept, and anything you found that the reports got wrong. End with the command `git diff --stat` output restricted to your files.
6. Final reply: under 150 words and the log path.
