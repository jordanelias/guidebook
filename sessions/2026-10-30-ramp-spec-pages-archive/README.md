# Archive: ramp-slope stress test and spec-page redesign session (2026-10-29 to 2026-10-30)

Index of everything this session produced, so none of it is lost. Start with the handoff note.

## Where the work is
- Git: commits `9c51ec35`, `933e1a46`, `525a2083`, `71e70edd`, `0ea535ec`, `2b3988c2` (plus the commit adding this folder).
- GitHub: branch `ramp-spec-pages-work` (NOT on `main`; `main` moved 2,203 commits and deleted the static render apparatus under RULINGS R1 on 2026-10-14, so landing this work on `main` needs a rebuild on the remote's design; see the handoff note section 7).
- Local: `C:\Github\guidebook`, local `main`.

## Documents
- Handoff and open work: `sessions/session_2026-10-30-spec-page-handoff.md`
- Owner requirements and design analysis: `audits/spec-page-design-requirements-2026-10-29.md`
- Defects and persona walkthrough: `audits/spec-page-design-defects-2026-10-30.md`
- Accessibility test record (partial): `audits/accessibility-audit-spec-page-v3-2026-10-30.md`
- Research batch findings: `audits/research-batch-ramp-slopes-2026-10-29/findings.md`
- Stress test: `audits/stress-test-ramp-slopes-2026-10-29/`
- Owner rules as memory notes: `memory-snapshot/` in this folder (copy of the Claude memory directory)

## Code and data
- Page generators: `scripts/generate/spec_page_v2.py`, `scripts/generate/spec_page_v3.py`
- Page data: `data/spec_pages/E-03.json`; pages in `site/specs/` (E-03 and the E-08 exemplar)
- Migrations: `scripts/migrations/026_classification_codes.sql` and the three data migrations dated 20261029-20261030; builders in `scripts/db/build_ramp_batch*_migration.py`
- Database as committed: `data/guidebook.db`

## Raw transcript (not in git)
The full session transcript (17.5 MB) and subagent logs stay at
`C:\Users\Jordan\.claude\projects\C--Github-guidebook\d9505991-620e-4974-95b2-b407384c5793.jsonl`
(and the folder of the same name for subagents and screenshots). Copying it into the repository was blocked by the
tool's permission check, so it was not added here. Back that file up outside the repo if you want it kept.
