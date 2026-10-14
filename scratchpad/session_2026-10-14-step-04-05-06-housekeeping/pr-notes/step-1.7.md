# PR body notes, step 1.7 (skills diet) -- branch stack/1.7-skills-diet (stacked on 1.6)
14 skills deleted (plan says 15): supersession-audit KEPT (the plan's command does not search skills; gap-driven-mining and the orchestrator name it). skills/deprecated (12 files) deleted. 14 .claude/skills links deleted.
Lines removed outright: 1,593 (14 skills) + 1,156 (deprecated) = 2,749 (plan: 2,990 with supersession-audit's 241).
R45 implemented: "Retired rule identifiers" block + _load_skill_ids reads it; 8 attestations cite unknown ids at base and still 8 after (23 would have newly failed).
[CORRECTION: the commit message's preflight line is garbled. Measured after the link fix: 59 green, 8 nothing-in-scope, 7 advisory failures, the same seven as step 1.6.]
No test covers _load_skill_ids; none added. Remaining dangling skill mentions are in the orchestrator catalogue and three other skills (not blocking).
