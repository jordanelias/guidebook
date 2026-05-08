# CO-0009 Phase 0 Handoff — D-0141 through D-0150
**Issued:** 2026-05-07 (prep session)
**Phase target:** CO-0009 Phase 0 — author 10 decision records
**Sessions estimated:** 2 Opus sessions (per CO-0009 §7)
**Activation gate for:** all of CO-0009 (Phases 1–5: schema, skill modifications, new skills, wrapper, workplan integration)
**Pattern:** Governance documents only (decision register entries; no code, no schema work)
**Operative plan:** `workplan/workplan-item-audit-pipeline-co0009.md` v2 (PROPOSED)
**Doctrinal basis:** `governance/decision-protocol.md` (A12 CANONICAL) · `workplan/workplan-item-audit-pipeline-co0009.md` §4.1

---

## 1. What Phase 0 produces

10 entries appended to `data/decisions/decision_register.yaml`, IDs D-0141 through D-0150. Each entry is a complete decision record per `decision-protocol.md` §3.2 (required fields) and §3.3 (rationale length norm by category).

No code. No schema files. No new governance docs. The decision records ARE the deliverable.

---

## 2. Format reference

**Required fields per record (decision-protocol.md §3.2):**
`decision_id`, `category`, `delegation`, `delegation_rationale` (if non-default), `summary`, `outcome`, `rationale`, `alternatives_considered` (D-DOCT/D-METH only), `decision_date`, `decided_by`, `model_routing`, `effort_level`, `decision_artifacts`, `predecessors`, `supersedes`, `status`, `review_status`, `notes`

**Reference template:** D-0139 in `data/decisions/decision_register.yaml` (lines 4182–4258). Clean structure, full field set, current pattern.

**Rationale length norm (decision-protocol.md §3.3):**
- D-SCHEMA: 1–3 sentences
- D-OP: 1 sentence (1–2 OK if pattern conformance noted)
- D-METH: 2–5 sentences + `alternatives_considered`

**Model-routing notation (decision-protocol.md §4.2):**
`{model_tier}/{effort_level}/{reasoning_modifier}` — e.g. `opus/100/synth`. Validator regex: `^(opus|sonnet|haiku|human)/(150|125|100|75|50|none)/(synth|arbitrate|extract|format|route|none)$`.

---

## 3. Per-decision scope — read this before authoring each

### D-0141 — items table migration (D-SCHEMA, DG-REVIEW)
**Outcome:** Migrate `schemas/item.py` to tracking DB at `data/guidebook.db`. DDL per CO-0009 §4.2.
**Read first:** `schemas/item.py` (current Pydantic), CO-0009 §4.2 items DDL (lines ~80–95).
**Key point:** Existing Pydantic validator regex `^[A-K]-\d{2}$` rejects `A-10b` and other letter-suffix codes. Fix to `^[A-K]-\d{2}[a-z]?$` is part of this decision.
**Predecessors:** D-0138 (storage form), D-0139 (schema spec).
**Length:** 1–3 sentences rationale.

### D-0142 — item_audit_runs table (D-SCHEMA, DG-REVIEW)
**Outcome:** New table in tracking DB; pipeline state per item per session. DDL per CO-0009 §4.2.
**Read first:** CO-0009 §4.2 item_audit_runs DDL + §9.3 wrapper state notes.
**Key points:** `run_id` = `{item_code}_{session_filename}`; `steps_started`/`steps_complete` JSON arrays; `spec_hash` MD5 with normalisation per §9.7.
**Predecessors:** D-0141, D-0139.
**Length:** 1–3 sentences.

### D-0143 — conflicts table (tracking DB) (D-SCHEMA, DG-REVIEW)
**Outcome:** New `conflicts` table in tracking DB for per-item audit findings (CONF-NNNN). Distinct from website DB `conflict` table (15 domain-level records with codes like LIGHT-INT).
**Read first:** CO-0009 §4.2 conflicts DDL + §0 two-DB architecture + §9.6 (conflict content lives in two places by design).
**Key point:** No FK link to website DB possible (cross-DB FK impossible in SQLite); not a duplication, distinct purposes.
**Predecessors:** D-0139.
**Length:** 1–3 sentences. Boundary with website DB `conflict` is the methodological hinge — note explicitly.

### D-0144 — gap categories CONF + AUDT (D-SCHEMA, DG-REVIEW)
**Outcome:** Extend `gaps` CHECK constraint to include CONF and AUDT categories.
**Read first:** Current gaps CHECK in `schemas/gap.py` or migration files; CO-0009 §3.1 evidence-auditor change (writes EG for OVERCLAIMED/UNCERTAIN_REVIEW; AUDT for UNDISCLOSED-CONSENSUS/MARKER-STRATUM-MISMATCH).
**Predecessors:** prior gap-category decisions (search register for D-NNNN that established the existing CHECK).
**Length:** 1–3 sentences.

### D-0145 — citation_mining.deferred_reason column (D-SCHEMA, DG-REVIEW)
**Outcome:** Add `deferred_reason` text column to `citation_mining` table.
**Read first:** Current citation_mining schema; CO-0009 §3.1 (citation-miner inline depth-1 relevance-gated throughout steps 1–7).
**Predecessors:** original citation_mining schema decision.
**Length:** 1–3 sentences. Brief.

### D-0146 — merge connection-scout → connection-discovery (D-OP, DG-REVIEW)
**Outcome:** connection-scout is merged into connection-discovery (with `--mode` flag) and moved to `skills/deprecated/`.
**Read first:** `skills/connection-scout_SKILL.md`, `skills/connection-discovery_SKILL.md`, CO-0009 §3.1 (MAJOR change to connection-discovery).
**Key points:** New `--mode` flag values; non-connection exit routing; external mode; SPECULATIVE→gap rule.
**Delegation:** DG-REVIEW rationale required — first-of-kind operation (default DG-AUTO upgraded to DG-REVIEW).
**Length:** 1–2 sentences. Note pattern conformance.

### D-0147 — functional-deficit-auditor (D-METH, DG-NON)
**Outcome:** New skill; scope = ICF alignment of item functional-deficit framing; FDR trigger criteria.
**Read first:** ICF taxonomy reference in project (search `references/` and FDR-related skills); A6 §evidence hierarchy on Co-2 (clinical literature); existing FDR-ACG, FDR-related governance.
**Key points:** Imports FDR ICF taxonomy. Opus required for mechanism judgment. Boundary with FDR-specialist skill must be explicit.
**Length:** 2–5 sentences + `alternatives_considered` (D-METH requirement). New methodology = DG-NON.
**Effort:** 100 likely (per CO-0009 budget).

### D-0148 — economics-auditor (D-METH, DG-NON)
**Outcome:** New skill; scope = checklist application for item-level economic framing.
**Read first:** `skills/economics-researcher_SKILL.md` (boundary clause needed); recent economics-audit-research workplan.
**Key points:** Sonnet (no Opus). Checklist-based, not synthesis. Boundary with economics-researcher must be explicit (auditor flags; researcher synthesizes).
**Length:** 2–5 sentences + `alternatives_considered`. DG-NON.
**Effort:** 75 likely.

### D-0149 — audit-consolidator output contract (D-OP, DG-REVIEW)
**Outcome:** Output contract: research brief at `references/audit-briefs/{item_code}_brief.md`; updates `item_audit_runs.status=COMPLETE` and `brief_path`.
**Read first:** CO-0009 §2 wrapper architecture (consolidator step 8); §9.2 gap dedup responsibility; §9.4 output contract requirements.
**Delegation:** DG-REVIEW rationale required — first-of-kind operation.
**Length:** 1 sentence (D-OP norm).

### D-0150 — item-audit-pipeline wrapper architecture (D-OP, DG-REVIEW)
**Outcome:** Wrapper orchestrates 8 steps (§2 architecture), tracks state in `item_audit_runs`, handles session boundaries. `skip_steps` and `force_rerun` semantics per §2.
**Read first:** CO-0009 §2 (architecture) + §9.3 (wrapper state survival) + §9.7 (multi-session staleness detection).
**Key points:** Idempotency at DB level; spec_hash with normalisation; HANDED-OFF status on context pressure.
**Delegation:** DG-REVIEW rationale required — first-of-kind operation.
**Length:** 1–2 sentences. Wrapper is complex but D-OP rationale should stay tight; complexity lives in CO-0009 itself.

---

## 4. Authoring sequence (suggested)

**Session 1 (Opus, ~150 effort):**
- D-0141, D-0142, D-0143 (schema decisions; tightly coupled; read CO-0009 §4 once and produce three records).
- D-0144, D-0145 (lightweight schema extensions; share preamble of "extends existing CHECK constraint" pattern).

**Session 2 (Opus, ~150 effort):**
- D-0146 (operational; requires both scout and discovery skill reads).
- D-0147, D-0148 (new methodologies; DG-NON; require alternatives_considered; longest rationale).
- D-0149, D-0150 (operational; wrapper + consolidator).

Splitting at the schema/methodology boundary. If both can fit in one session, fine — but D-0147 and D-0148 alone may consume substantial budget and benefit from fresh context.

---

## 5. Commit convention

`citation-verifier: ` is wrong here. Use `decision-capture: D-NNNN[ — D-NNNN] {short summary} [YYYY-MM-DD HH:MM]`.

Example: `decision-capture: D-0141 — items table migration to tracking DB [2026-05-08 14:30]`

Or batch: `decision-capture: D-0141 — D-0145 schema decisions [2026-05-08 14:30]`

---

## 6. Validation

After each decision record commit:
1. Decision register is YAML — confirm `python3 -c "import yaml; yaml.safe_load(open('data/decisions/decision_register.yaml'))"` succeeds.
2. `decision_capture.py` validator (per `governance/decision-protocol.md` §7) — verify it runs clean. Location: `scripts/decision_capture.py` or similar (confirm in repo).
3. Sequential ID check: D-0141 follows D-0140; no gaps; no duplicates.

---

## 7. Open judgment calls (flag for project owner)

- **D-0143 boundary statement.** The two-DB conflict tables share domain taxonomy codes but are not FK-linked (cross-DB FK impossible). Decision must be explicit that this is intentional, not a duplication bug. CO-0009 §9.6 already states this; the decision record should reference rather than re-litigate.
- **D-0147 FDR-specialist boundary.** functional-deficit-auditor flags items where ICF alignment is questionable; FDR-specialist conducts deficit research. The boundary needs explicit articulation in the decision; without it, scope creep is the risk.
- **D-0150 HANDED-OFF status semantics.** §9.3 says wrapper state must survive context loss. The HANDED-OFF status implies an explicit "context exhausted, hand off cleanly" path. Decision should specify trigger condition (e.g., context >75%, or step boundary count, or explicit user signal).

---

## 8. Activation gate

Per CO-0009 §1 closing line: "Activation gate: D-0141 through D-0150 authored and status ACTIVE."

Decisions are authored at status ACTIVE if DG-NON (D-0147, D-0148) — these don't require review.
Decisions DG-REVIEW are authored at status PROPOSED with `review_status: PENDING`. They become ACTIVE on project-owner confirmation.

If all 8 DG-REVIEW decisions go to PROPOSED, CO-0009 Phase 0 produces 2 ACTIVE + 8 PROPOSED. Phase 1 (schema work) cannot start until the 8 are CONFIRMED.

This means **Phase 0 finishes with a project-owner review batch**, not with code work starting. Worth flagging to the user before Phase 0 starts so they expect the gate.
