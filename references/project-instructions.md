# Project Instructions — Accessible Built Environments Guidebook
**Revised:** 2026-03-29

## Identity
**Repo:** `jordanelias/guidebook` · branch `main`
**PAT:** [stored in Claude Project custom instructions — not committed to repo]
**Commit convention:** `{skill-name}: {action} [{YYYY-MM-DD HH:MM}]`
**Active version:** V9.0 2026-03-20

## Architecture
- Conversation model: Sonnet 4.6. All assembly, drafting, research, coordination, GitHub operations.
- Opus 4.6: best-practice synthesis, evidence arbitration, cross-referential judgment. Requires Opus selected in model picker — no programmatic escalation path exists.
- Artifact proxy: routes all model strings to Sonnet 4.5. Not a sub-model routing mechanism. Use only for user-facing interactive deliverables. Serial calls only (concurrent → 429). `show_widget` has no proxy access.
- PI text governs where PI and skill file conflict. Where a GitHub skill file has been updated more recently than the PI, the GitHub file governs for execution details; PI governs for model assignment and trigger conditions.

## Session Protocol
**Start (every conversation):**
1. GET `sessions/LATEST` → GET that session file. Report `session_close`, `next_action`, blockers.
2. GET `gap_register.md` — extract OPEN P1 items only (filtered, not full load).
3. GET `references/project-standards.md`.
4. GET `skills/workplan-orchestrator_SKILL.md`. Present workplan for user approval.
Other skills: GET from GitHub `skills/{name}_SKILL.md` only when identified in workplan AND user approves.

**Close (~85% context or natural conclusion):**
Complete current stage. Commit all work to GitHub. Invoke `session-consolidator`. Bullet-point handoff.

## Standing Rules
1. Never process >500 lines as single input.
2. All timestamps: `YYYY-MM-DD HH:MM` via `date -u`.
3. Default output: `.md`. DOCX only if requested.
4. `research-log-manager CHECK` before any research; `LOG` after. Skipping = error.
5. Sources confirmed real. "I don't know" > invention. 2 failed searches → CLOSED-DELETED.
6. Sonnet never determines best practice. Flag for Opus session.
7. Structural changes → `toc-editor` first. Change Order required.
8. Connectors (PubMed, Consensus, Scholar Gateway) only when task requires research.
9. DD = Design Development. RFO = Ready for Occupancy.
