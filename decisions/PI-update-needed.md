# PI v10.6 Update Required

**Pending owner action.** The DR-2026-05-09 adopted protocol requires PI update to add standing rule #7. Cannot be edited from repo — owner must update Project Instructions in claude.ai.

## Copy-paste-ready text

Add to `<standing_rules>` in PI v10.5 → v10.6:

```markdown
7. **Adversarial research protocol.** All research-generating gap closures must populate four protocol fields before status changes to CLOSED-FIXED or CLOSED-RESOLVED:
   - `gaps.confidence_interval` (numerical range, e.g., "60-75%")
   - `gaps.shift_conditions` (specific conditions that would shift CI up/down)
   - `gaps.named_dissenter` (specific contrary view OR "NONE FOUND" with logged search queries)
   - `gaps.falsification_condition` (specific finding that would invalidate)

   Per cited study, log to `evidence_population_match` with grade (EXACT/PARTIAL/PROXY/MISMATCH) and `ref_id` foreign key.

   Critical pattern to watch: conflating "evidence on the topic" with "evidence supporting the specific claim". A real citation about a domain does not validate every specific claim in that domain. The protocol exists to expose this bias.

   Audit query: `scripts/audit/research_protocol_audit.py` (level 2 enforcement). Skill: `skills/adversarial-research_SKILL.md`. Decision record: `decisions/DR-2026-05-09-adversarial-research-protocol.md`.

   The reviewer is the truth-source — the protocol creates audit trails, not truth. Spot-check at minimum 1 closed gap per session: trace cited evidence to specific claim, verify match.
```

## Update changelog

```markdown
- **V10.6 (2026-05-XX)** — Standing rule #7 added: adversarial research protocol enforcement (per DR-2026-05-09). Schema applied to tracking DB. Pattern documented: "topic-evidence vs claim-evidence" conflation must be detected during gap closure review.
```

## Files affected (already in repo)

- `decisions/DR-2026-05-09-adversarial-research-protocol.md` — ADOPTED
- `workplan/research-protocol-adversarial.md` — v2 protocol document
- `skills/adversarial-research_SKILL.md` — skill file
- `scripts/audit/research_protocol_audit.py` — audit query (6 checks)
- `data/guidebook.db` — schema with new fields + `evidence_population_match` table

## Owner action checklist

- [ ] Update PI in claude.ai project knowledge with above text
- [ ] Bump version to v10.6
- [ ] Update PI changelog
- [ ] Add `adversarial-research` to skills_assigned list
- [ ] Decide enforcement level promotion (level 2 → level 3 once Phase 1 hooks ship)
- [ ] Establish spot-check schedule (per session: 1 random closure verification)
