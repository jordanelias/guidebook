# Brief: current-state extract of references/project-standards.md (one slice)

Source: /home/user/guidebook/references/project-standards.md (append-only owner-ruling ledger; ~8,600 lines; newest at the end). You get ONE line range. READ EVERY LINE of your range (Read tool, offset/limit in chunks of at most ~250 lines; do not skim, do not grep-sample). READ-ONLY on the repository. Write ONLY to your named output file in /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/ps-clean/. Canadian English.

## Task
Produce a CLEAN, CURRENT-STATE extract of your slice for a later adjudicator who must judge what is in force. REMOVE all discussion of changes, edit history and versions, namely:
- CORRECTION / AMENDED / SUPERSEDED / APPENDED / "was previously" / "replaces the earlier arrangement" narration, and accounts of how a rule came to be; sentences that say what an earlier text said and was withdrawn;
- version numbers, migration numbers used only as history, PR numbers, session ids and links, transcript greps, "Derive the times from..." lines, who wrote the entry and how;
- process chatter (coordinator/delegate narration, check lines about the check itself), proof narratives and anecdotes of past failures.
KEEP, in the entry's own words, only what is in force now:
- the owner's quoted words (these are the authority; keep them verbatim and marked as owner words);
- the operative rule: CONDITION / ACTION content, reduced to what binds now;
- each [ASSUMPTION] that a rule rests on, reduced to the bare reading, flagged "[unratified reading]" (these are the recorder's, not the owner's);
- open questions still unanswered (flag "[OPEN]") and held decisions;
- the date of the owner's statement as a bare ranking key (ISO date) — rule 0 ranks by date. Keep the entry's heading topic, shortened.
SUPERSESSION HANDLING: where a later entry in YOUR slice changes an earlier one, output only the resulting state, attributed to the later date. Where an entry's text says it was superseded by something OUTSIDE your slice, or you cannot tell, DO NOT guess: keep the entry and tag it "[STATUS UNCERTAIN: what the entry says about itself]". Never drop a ruling because it seems old; drop narration of history only. When unsure whether a sentence is history or a rule, KEEP it and tag [CHECK].
Never invent, merge, or reword an owner's quoted words. Do not decide anything. Do not summarise away a numeric or named value (keep derivation commands, never type counts that the entry only quotes as dated history).

## Output format
One section per ledger entry, in order:
### <ISO date> — <short topic> [line range in source, e.g. L123-L140]
Owner words: "..." (verbatim; omit the line if the entry holds none, and say "recorder/delegate entry — not owner words")
In force: bullet list of the current rules.
Open: bullets or "none".
Tags as above.
Entries that are pure history (nothing in force) get one line: "### <date> — <topic> [Lx-Ly]: nothing in force (history only: <few words>)". At the end add: "Slice stats: entries read N; entries reduced to nothing in force M; entries tagged [STATUS UNCERTAIN] K; lines read from-to." Return a 100-word note and the file path.
