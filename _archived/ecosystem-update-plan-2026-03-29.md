# Ecosystem Update Plan + Work Triage
**Date:** 2026-03-29  
**Basis:** Audit conversation 2026-03-28/29 — model proxy test, session history scan, PI review

---

## Part 1: Ecosystem Update Plan

### 1.1 Ground Truth — What Was Established This Conversation

| Finding | Confirmed |
|---|---|
| Artifact proxy routes ALL model strings to Sonnet 4.5-20250929 | ✓ Test result |
| `show_widget` cannot call the artifact API | ✓ "Failed to fetch" |
| Only `create_file` + `present_files` HTML artifacts have proxy access | ✓ |
| `max_tokens` above 1000 is accepted and honoured | ✓ 602-word response, stop_reason: end_turn |
| Proxy injects ~3,262 input tokens of overhead per call | ✓ Usage field |
| True Opus requires Opus conversation session — no programmatic escalation path exists | ✓ |
| The SKILL.md format is the official Anthropic Agent Skills standard (Oct 2025) | ✓ |
| Native claude.ai skill loading (Settings upload) would eliminate startup GET overhead | ✓ |

---

### 1.2 Immediate Fixes (This Session or Next)

#### FIX-01: Retire the `opus-passthrough.html` template
The current template is actively misleading. Every call routes to Sonnet 4.5 regardless of model field.

**Replace with `model-passthrough.html`:**
```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Sonnet Passthrough</title></head>
<body>
<pre id="output">Ready.</pre>
<script>
/*
 * ARTIFACT API REALITY (confirmed 2026-03-29):
 * - This proxy routes ALL model strings to Sonnet 4.5-20250929
 * - The model field is IGNORED by the claude.ai artifact proxy
 * - True Opus requires running this conversation in an Opus session
 * - max_tokens above 1000 IS honoured (proxy does not cap it)
 * - Proxy injects ~3,000 tokens of system overhead per call
 */

const SYSTEM = [
  "You are the evidence synthesis authority for the Accessible Built Environments Guidebook.",
  "Evidence hierarchy (higher governs on conflict):",
  "  Tier 1: OT clinical research — intervention-tested",
  "  Co-1: Lived experience / participatory design (CRPD Art. 4.3)",
  "  Tier 2: Disability-led NGO / DPO / advocacy guidelines",
  "  Co-2: OT clinical practice guidelines",
  "  Tier 3: Systematic reviews and meta-analyses",
  "  Tier 4: International standards with evidence basis",
  "  Tier 5: National beyond-code frameworks",
  "  Tier 6: Statutory codes — reference baseline only",
  "",
  "Best-practice sequencing: Ideal → Best Practice → Acceptable → Minimum",
  "Never anchor on statutory minimums. Where evidence is thin, state THIN and give the highest-ambition defensible specification.",
  "All specifications must be actionable by an architect.",
  "Output exactly the format requested. No preamble. No commentary."
].join("\n");

const USER = `REPLACE_WITH_TASK`;

async function run() {
  document.getElementById("output").textContent = "Running...";
  try {
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "claude-sonnet-4-6",
        max_tokens: 4000,
        system: SYSTEM,
        messages: [{ role: "user", content: USER }]
      })
    });
    const data = await res.json();
    if (data.error) {
      document.getElementById("output").textContent = "ERROR: " + JSON.stringify(data.error);
      return;
    }
    const text = data.content?.filter(b => b.type === "text").map(b => b.text).join("\n") || JSON.stringify(data);
    document.getElementById("output").textContent = text;
  } catch (err) {
    document.getElementById("output").textContent = "Error: " + err.message;
  }
}

run();
</script>
</body>
</html>
```

**Changes from current template:**
- Renamed to reflect reality (Sonnet, not Opus)
- max_tokens: 4000 (confirmed safe)
- Project-aware SYSTEM prompt with evidence hierarchy + sequencing doctrine
- Comment block documenting the proxy reality
- Error surface (shows API error JSON, not silent failure)

#### FIX-02: Archive `/mnt/project/comprehensive-audit-2026-03-27.md`
Commit to `misc/archived/comprehensive-audit-2026-03-27.md` on GitHub. Remove from `/mnt/project/` context. Saves ~4,500 tokens per session.

#### FIX-03: Update PI — Model Roles section

Replace current Model Roles table with:

```
## Model Roles

**CONFIRMED 2026-03-29:** The claude.ai artifact proxy routes ALL model strings to
Sonnet 4.5-20250929. The model field in artifact fetch calls is ignored. True Opus
requires running the conversation itself in an Opus session. No programmatic
Sonnet→Opus escalation path exists via artifacts.

| Role | Model | How to invoke |
|---|---|---|
| Default (assembly, writing, analysis, routing) | Sonnet 4.6 | Conversation default |
| Synthesis / judgment (best-practice, evidence arbitration) | Opus 4.6 | Open Opus session explicitly |
| Mechanical tasks (chunking, formatting, extraction) | Artifact passthrough (Sonnet 4.5 via proxy) | model-passthrough.html |

Sonnet sessions handle all assembly, collation, drafting, and coordination.
Opus sessions handle best-practice determination, evidence arbitration, and cross-referential synthesis.
Sonnet never determines best practice — if in a Sonnet session, flag for Opus session and continue.
```

#### FIX-04: Update PI — remove or relocate low-utility sections

| Section | Action | Token saving |
|---|---|---|
| Workflow Reference table | Remove — lives in workplan | ~350/session |
| Session-Close YAML schema | Remove — lives in session-consolidator | ~200/session |
| Unresolved Blockers table | Remove — lives in session YAML | ~80/session |
| Skill Design Principles | Remove — belongs in skill-creator | ~100/session |
| GitHub API operational detail | Reduce to: repo, branch, PAT, commit convention only | ~80/session |

#### FIX-05: Add missing skills to PI Skill Registry
Add: `vol2-item-formatter` (Sonnet), `bibliography-compiler` (Haiku). Both are active in the endnote pipeline and currently unregistered. `workplan-orchestrator` cannot sequence them.

#### FIX-06: Integrate endnote amendments into PI
`misc/endnote-downstream-amendments-2026-03-27.md` specifies changes to `item-specification-writer`, `vol2-item-formatter`, `chunk-assembler`, `cross-reference-resolver`, and the PI itself. None are in the current PI. This is a CRITICAL blocker for Phase 3.

---

### 1.3 Short-Term Fixes (Before Phase 2B Resumes)

#### FIX-07: Add LATEST session file mechanism to `session-consolidator`
At session close, write filename of current session to `sessions/LATEST`. Session start reads `sessions/LATEST` in one GET instead of listing and sorting the directory. Eliminates sort-order ambiguity and race conditions.

#### FIX-08: Fix timestamp source in `session-consolidator`
Replace inline Claude date estimates with `date -u +%Y-%m-%d\ %H:%M` via bash. One call at session open sets the canonical timestamp. Eliminates UTC/system-prompt date conflict.

#### FIX-09: Add YAML pre-commit blocker validation to `session-consolidator`
Before writing session close YAML: GET prior session YAML, diff `blockers` list against current gap register OPEN items, close any now-CLOSED. Prevents stale blocker propagation.

#### FIX-10: Document `show_widget` limitation in PI
Add to Standing Rules: "`show_widget` does not have artifact API proxy access. Only `create_file` + `present_files` HTML artifacts can call `api.anthropic.com`. Never use `show_widget` for model sub-calls."

---

### 1.4 Before Phase 3 (Medium-Term)

#### FIX-11: Upload skills to claude.ai Settings (native loading)
The GET-from-GitHub pattern adds 3–6 API calls per session start. Native skill loading (Settings → Skills upload) would eliminate this overhead. Keep GitHub as source of truth for version control; upload to claude.ai Settings for runtime. Estimated saving: ~500 tokens × sessions remaining.

#### FIX-12: Integrate endnote pipeline into PI Workflow Reference
Add the complete Item Specification workflow with all four steps: `research-log-manager RETRIEVE` → `item-specification-writer` (REF-IDs) → `vol2-item-formatter` (validation) → deferred to assembly: `bibliography-compiler` → `cross-reference-resolver`.

#### FIX-13: Rotate GitHub PAT to scoped token
Current PAT is embedded in PI system prompt, visible in every session context. Replace with a read/write scoped PAT (no admin permissions). Document rotation schedule.

---

## Part 2: Work Triage — All Incorrect "Opus" Outputs

### 2.1 Triage Framework

Three verdicts:

**ACCEPT** — Sonnet 4.5 output is sufficient for this task type; no material risk from model difference; proceed to Phase 3 as-is.

**FLAG** — Sonnet 4.5 output is plausible but the judgment was consequential enough that Opus review is warranted before Phase 3 writing. Flag in gap register; schedule Opus session review.

**REDO** — Output involves safety-critical specifications, architecture-altering decisions, or contains confirmed errors. Must be redone in an Opus session before any Phase 3 use.

---

### 2.2 Instance Triage

#### GROUP A: Pre-Passthrough In-Session "Escalations" (March 17–20)
Sessions 2026-03-17 through 2026-03-20. `escalations_triggered: 1–6`. Handled inline by Sonnet. No passthrough existed. Outputs: grab bar type conflict, turning circle, B-10 seizure, DEAF RT60, sensory room, circadian lighting.

**Verdict: FLAG**

Rationale: These were genuine evidence conflicts routed to "Opus" judgment but resolved by Sonnet inline. The outputs influenced gap register entries and BPC positions. They are not wrong per se, but the reasoning was Sonnet-level, not Opus-level. Review in a dedicated Opus session against the relevant BPC entries before Phase 3 writing for affected items.

Affected items: G-03 (grab bar type), circulation geometry, A-08/A-13 (acoustic), B-10 (seizure safety), sensory room provisions, circadian lighting.

---

#### GROUP B: `residential-accessible-home-case-studies` BPC Synthesis
Session 2026-03-27-1830. "In-session Opus 4.6 synthesis." 8 governing principles, 4 tension resolutions, 8 provisions.

**Verdict: FLAG**

Rationale: Framework/methodology slug — the synthesis distils case study patterns, not dimensional specifications. Sonnet 4.5 is capable of this category of synthesis. The output is structurally sound. However, the "governing principles" inform how case studies are selected and weighted in Phase 3. Opus review recommended before Part 13 writing.

Action: In Opus session, load BPC, read current synthesis, confirm or amend governing principles. 30-minute task.

---

#### GROUP C: 6-Slug BPC Synthesis Batch (Session 2026-03-28-1850)
Via passthrough (Sonnet 4.5). Slugs and verdicts individually:

**`acoustics-speech-intelligibility-disability`**
Key finding: 0.6 s is failure boundary, not compliant specification.
Verdict: **FLAG** — framing correction is significant (affects A-02, A-08, A-13 specs). Opus should confirm the boundary language before it propagates to items.

**`sensory-relief-space-design`**
Key finding: toilet adjacency underclaimed; approach sequence underclaimed.
Verdict: **FLAG** — underclaimed provisions become underclaimed specs in Phase 3. Opus review of toilet adjacency mandatory status.

**`ndv-aut-built-environment-quantified-thresholds`**
Key finding: evidence gap is structural; process-based design is highest-ambition spec.
Verdict: **FLAG** — this is a judgment call about what counts as sufficient specification under thin evidence. Opus should confirm the process-based design conclusion.

**`cross-population-conflict-resolutions`**
Key findings: A-04/B-05/A-09 unsupported; OFS/MCAS chemical sensitivity conflict unaddressed.
Verdict: **REDO** — three item specifications (A-04, B-05, A-09) are identified as unsupported. GAP-OPS-01 exists but the synthesis itself needs Opus confirmation of which values are defensible vs. which require [UNSUPPORTED] markers. This directly affects Phase 3 writing.

**`upper-limb-impairment-built-environment`**
Key finding: ADA 18-inch toilet centreline is most consequential evidence-practice conflict in guidebook.
Verdict: **REDO** — "most consequential evidence-practice conflict in guidebook" is Sonnet's own assessment. If accurate, this determination shapes toilet compartment specs for all populations. Opus must review the evidence and either confirm or revise the conflict assessment before Phase 3.

**`fold-down-grab-bar-specification`**
Key finding: WHO APS-15:2022 110 kg rating dangerously inadequate given 1.3 kN peak force. GAP-OPS-02 raised.
Verdict: **REDO** — safety-critical. Sonnet identified a load-bearing safety gap between WHO standard (110 kg) and measured peak forces (1.3 kN ≈ 130 kg). This finding, if correct, means any specification citing WHO APS-15:2022 as compliant is actively unsafe. Opus must verify the biomechanical reasoning before this propagates to grab bar specs.

---

#### GROUP D: E-14 Entrance Rest Seating (Sessions 2026-03-28-2130 and 2026-03-28-2230)
Via passthrough (Sonnet 4.5). Item drafted and committed to GitHub. Key corrections: seat height 440–480mm (not 480 min), alcove 1200mm (not 900mm), recline mandatory Tier 1 OFS/PAIN.

**Verdict: FLAG**

Rationale: The dimensional corrections (seat height range, alcove depth) are sourced from BPC evidence. Sonnet 4.5 applied them correctly per the BPC. The item is Phase 3-ready pending one action:

REF:seating-entrance:02 was removed (hallucination confirmed). Remaining citations need verification before the item is marked Phase 3-complete. The item exists as a committed file — Opus review should confirm the specification logic, not redraft from scratch.

Action: In Opus session, load E-14 draft, confirm specification logic against BPC Key sources. Verify remaining 3 citations. 20-minute task.

---

#### GROUP E: T0 Candidate Assessments (Sessions 2026-03-28-1715 and 2026-03-28-1830)
In-session (Sonnet). 7 candidates: 4 CONFIRMED, 1 PARTIAL (E-14), 1 REJECTED (T0-03 retreat room), 1 already-actioned.

**Verdict: FLAG for T0-03 specifically; ACCEPT for remainder**

Rationale: The 4 CONFIRMED candidates were actioned into items B-12, E-10, E-12, E-13 already drafted. Reversing these would require undrafting committed items — high disruption, low benefit. Accept.

T0-03 REJECTED (retreat/reset room) on the basis of DEAF emergency isolation conflict — this is a genuine judgment call. The reasoning is sound (sound attenuation provisions exclude DEAF emergency communication access), but Opus should confirm the rejection logic and whether any provision structure could preserve T0 status while respecting DEAF requirements.

---

#### GROUP F: Connection Register CON-0050–CON-0084 (Session 2026-03-28-2240)
Via passthrough (Sonnet 4.5). 35 new connections. 14 HIGH, 20 MODERATE, 1 SPECULATIVE.

**Verdict: ACCEPT for HIGH confidence; FLAG for MODERATE**

Rationale: Connection discovery is pattern recognition across BPC corpus — a task where Sonnet 4.5 performs well. The HIGH confidence connections (14) have been confirmed across multiple evidence streams. Accept these for Phase 3 briefing.

MODERATE connections (20) represent weaker signals. These are already in the gap register as P3 items. They should be presented to Opus for confirmation before being elevated to item briefings. This is already the correct workflow (MODERATE → gap register → Opus confirmation before use).

SPECULATIVE (1): stays in gap register, no action.

---

### 2.3 Redo Schedule

All redo and flag work requires an Opus session. The only way to run Opus is to open the conversation with Opus selected.

**Redo Session 1 — Safety-Critical Specifications**
Priority: REDO items only.
Load: `fold-down-grab-bar-specification` BPC, `upper-limb-impairment-built-environment` BPC, `cross-population-conflict-resolutions` BPC.
Tasks:
1. Opus reviews grab bar load rating reasoning — confirm or revise 200 kg recommendation vs. WHO 110 kg
2. Opus reviews ADA 18-inch toilet centreline conflict — confirm or revise "most consequential" assessment
3. Opus reviews A-04/B-05/A-09 unsupported values — determine which require [UNSUPPORTED] markers
Output: Amended best_practice_synthesis sections for 3 BPCs; updated GAP-OPS-01/02 with Opus determination.
Estimated effort: 1 Opus session.

**Redo Session 2 — Consequential Judgments**
Priority: FLAG items with Phase 3 writing implications.
Load: `acoustics-speech-intelligibility-disability`, `sensory-relief-space-design`, `ndv-aut-built-environment-quantified-thresholds` BPCs; T0-03 rejection record; E-14 draft.
Tasks:
1. Confirm 0.6 s as failure boundary framing for acoustic items
2. Confirm toilet adjacency mandatory status for sensory relief space
3. Confirm process-based design as highest-ambition spec for NDV/AUT quantified thresholds
4. Review T0-03 rejection — can retreat room achieve T0 with modified provision structure?
5. Confirm E-14 specification logic; verify remaining citations
Output: Amended synthesis sections; T0-03 verdict confirmed or reversed; E-14 marked Phase 3-ready.
Estimated effort: 1 Opus session.

**Redo Session 3 — Framework Synthesis Review**
Priority: FLAG items that inform Phase 3 structure.
Load: `residential-accessible-home-case-studies` synthesis; pre-passthrough escalation outputs (grab bar, turning circle, seizure, DEAF RT60).
Tasks:
1. Review 8 governing principles — confirm or amend for Part 13 case study structure
2. Review pre-passthrough escalation determinations — confirm Sonnet positions or revise
Output: Confirmed or amended framework synthesis; escalation determinations validated.
Estimated effort: 1 Opus session.

**CON-0050–0084 MODERATE batch review** — route into Redo Session 1 or 2 as a parallel task. Opus reviews 20 MODERATE connections in batch, elevates or downgrade each. 30 minutes additional.

---

### 2.4 What Does Not Need Redoing

| Item | Reason |
|---|---|
| All Sonnet-attributed assembly work (drafting, formatting, filing) | Correctly attributed to Sonnet throughout |
| CON-0001–0038 (pre-passthrough connections) | In-session Sonnet work on connection discovery — appropriate model for this task |
| CON-0085–0092 (external mode connections) | Correctly attributed to Sonnet + web search |
| INTRA/INTER/BOTH tagging (CON-0001–0038) | Correctly attributed to Sonnet |
| Gap register entries from Opus synthesis | Gaps are correct even if the synthesis model was wrong — they identify real issues |
| REF:seating-entrance:02 deletion | Correct action regardless of which model identified the hallucination |

---

### 2.5 Impact on Phase 3 Gate

Phase 3 writing cannot begin on any item whose best_practice_synthesis is in the REDO category. Affected items at risk:

- All grab bar items (fold-down-grab-bar-specification REDO)
- All toilet compartment items involving ADA 18-inch centreline (upper-limb REDO)
- A-04, B-05, A-09 (cross-population-conflict-resolutions REDO)
- A-02, A-08, A-13 (acoustics FLAG — can begin with caveat, complete before finalisation)
- A-16 (sensory-relief FLAG — toilet adjacency must be resolved before finalisation)

All other items can proceed to Phase 3 with standard evidence-auditor review.

---

### 2.6 Updated Workplan Impact

| Workplan session | Change |
|---|---|
| Phase 0R (reconciliation) | Add ecosystem fixes FIX-01 through FIX-10 |
| New: Opus Review Session A | Redo Session 1 — safety-critical (grab bar, toilet centreline, A-04/B-05/A-09) |
| New: Opus Review Session B | Redo Session 2 — consequential judgments (acoustics, sensory relief, E-14, T0-03) |
| New: Opus Review Session C | Redo Session 3 — framework synthesis + escalation review |
| Phase 3 (all item writing) | No REDO items begin Phase 3 writing until Opus Review Sessions A and B complete |

Net addition to workplan: 3 sessions. These replace the original 22-session plan's assumption that Opus synthesis was already done. It was not.

---

*End of document*
