---
name: gap-driven-mining
description: >
  Gap-driven evidence mining: starts from a parameter × population × outcome shortfall
  recorded in the gaps table and runs a deterministic search matrix to find evidence
  that closes the gap, partial evidence that narrows it, or a logged null result.
  Companion to citation-miner: citation-miner mines OUT from confirmed anchor sources;
  this skill mines IN to gaps that have no anchor. Runs in two modes: BATCH (sweep over
  OPEN+ADDRESSABLE gaps; manual or semiannual invocation) and INLINE (called by other
  research skills when they encounter an addressable gap mid-task). Depth-1 only —
  discovered sources are recorded but NOT mined further within the same pass.
  ALWAYS use when asked to: close evidence gaps, mine for gap closure, sweep open
  gaps, gap-driven research, address THIN-BASE flags, find evidence for parameter X.
  Trigger on: "gap-driven mining", "close evidence gap", "sweep gaps", "find evidence
  for THIN-BASE", "0/N Co-1 jurisdictions", "no indexed evidence", "mine for the gap".
---

**Model:** Sonnet 4.6 (search + candidate harvesting) → Opus 4.7 for outcome judgment when ≥3 candidates returned
**Connectors:** PubMed (required), Scholar Gateway (required for Co-1 / lived experience), Cochrane (via web_fetch), CrossRef (via web_fetch), standards-body catalogs (via web_fetch). Activate for the pass.
**SQLite:** `data/guidebook.db` via `scripts/db.py`
**Authoritative DR:** `decisions/DR-2026-05-26-gap-driven-mining-protocol.md`
**Schema:** `gaps.mining_addressability` column + `gap_mining` table (migration 017)

---

## 0. Connector availability (read BEFORE mining)

Before any gap-driven mining pass, probe connector availability. The matrix in §3 names required connectors per gap pattern — if a required connector is unavailable, the affected pattern's attempt is marked `deferred` rather than `null_result`, and `notes` records the blocker.

- **PubMed** — required for clinical / SR-meta / numerical-spec gap patterns. If unavailable, ABORT the pass and log `[GAP — PubMed connector unavailable]`. Web-search-only substitution carries high fabrication risk (per GAP-278).
- **Scholar Gateway** — required for Co-1 / lived-experience / design-literature patterns. If unavailable, mark Co-1 attempts `deferred` with `notes = "Scholar Gateway unavailable — Co-1 search DEFERRED"`. Do NOT substitute PubMed for Scholar Gateway on Co-1: they index different corpora, and PubMed will miss the lived-experience / DPO publications that are exactly what Co-1 gaps require.
- **Cochrane Library** (via `web_fetch` to cochranelibrary.com) — required for SR-meta gap patterns. Web_fetch acceptable.
- **CrossRef** (via `web_fetch` to api.crossref.org) — fetches metadata on candidates the primary connector returns.
- **Standards-body catalogs** (ISO, IEC, EN, BSI, ANSI, plus jurisdiction-specific) — required for "standards not promoted" gap pattern.

**Partial-availability rule:** If a connector required for a gap's pattern is unavailable, that gap's `gap_mining` row is recorded with `outcome = 'deferred'` and `notes` naming the blocker (≥10 chars per SQL CHECK constraint). The gap stays OPEN and re-enters the queue when connectors recover.

---

## 1. Two Modes

### INLINE mode (called from another research skill)

When `adversarial-research`, `functional-deficit-researcher`, `multilingual-research`, or `content-gap-analyzer` is operating in a gap's neighborhood:

1. Calling skill passes: `(gap_id)` plus any candidate sources already surfaced during its own work.
2. This skill checks:
   ```bash
   python3 scripts/db.py unmined-gaps --gap-id {gap_id}
   ```
   Returns the gap's `mining_addressability` and the most recent `gap_mining.outcome` (if any).
3. If `mining_addressability != 'ADDRESSABLE'` → return early; the calling skill stays on its primary task.
4. If most recent `outcome = 'closure_evidence_found'` → return early (gap already closed by mining).
5. If most recent `outcome IN ('null_result', 'partial_evidence_found')` and `attempt_at` is within 6 months AND no caller-provided new candidates → return early (per §5 re-eligibility).
6. Otherwise run the §3 matrix for the gap's pattern, log the `gap_mining` row, return discoveries to caller.

### BATCH mode (standalone sweep)

When invoked directly to sweep OPEN gaps:

1. Query addressable queue:
   ```bash
   python3 scripts/db.py unmined-gaps --priority P1
   # then
   python3 scripts/db.py unmined-gaps --priority P2
   ```
   Each returns gaps with `mining_addressability = 'ADDRESSABLE'`, `status LIKE 'OPEN%'`, and either no `gap_mining` row OR most recent `attempt_at` older than 6 months.
2. For each gap, in priority order:
   - Run the §3 matrix for the gap's pattern (the matrix entry is selected by parsing the gap's description; see §2).
   - Aggregate candidates across all matrix entries before outcome judgment (cluster pattern per §3).
   - Log the `gap_mining` row.
   - If `outcome = 'closure_evidence_found'`, perform the §4 closure workflow.
3. Report: total attempts, outcomes by category, gaps closed, gaps still open, deferrals.

**Depth-1 enforced (both modes):** discovered sources are INSERTed to `evidence_sources` + `source_slug_links` but their citation networks are NOT mined in the same pass. Hand off to `citation-miner` for backward/forward graph traversal as a separate operation.

---

## 2. Pattern detection (which matrix entry applies)

Parse the gap row to select the matrix entry:

| Gap description contains | Pattern key | Matrix entry |
|---|---|---|
| `THIN-BASE`, `thin base`, `[RESEARCH TASK]` | `thin_base_primary_clinical` | §3.1 |
| `Co-1 evidence 0/`, `0/N jurisdictions`, `Co-1 anchor missing` | `co1_zero_jurisdictions` | §3.2 |
| `no indexed evidence`, `no source for`, `no published evidence base` | `numerical_spec_uncited` (if gap description contains units mm/s/lux/dB/etc.) OR `qualitative_uncited` (otherwise) | §3.3 / §3.4 |
| `standards named ... not promoted`, `standard not in evidence base` | `standards_not_promoted` | §3.5 |
| `population structurally invisible`, `population invisible in N BPCs` | `cross_population_invisibility` | §3.6 |

If a gap matches multiple keys, the higher-§-numbered match takes precedence (more specific). If a gap matches no key, route to `gap_recategorized` outcome with `notes` describing the unmatchable shape (≥20 chars per SQL CHECK constraint) and surface to owner.

---

## 3. Search strategy matrix

Each entry below specifies primary / secondary / tertiary strategies. Mining runs ALL applicable strategies in a single attempt before outcome judgment (composite cluster-search pattern per `supersession-audit_SKILL.md` §3 — ~5× fewer tool calls than per-strategy sequential evaluation with no loss of findings).

### 3.1 thin_base_primary_clinical

**Primary:** PubMed search.
- Query: parameter terms AND population terms AND outcome terms (parameter/population/outcome extracted from the gap's `section` field and the linked item's metadata).
- Publication-type filter: `Randomized Controlled Trial[Publication Type] OR Clinical Trial[Publication Type] OR Practice Guideline[Publication Type]`
- Year filter: no constraint (THIN-BASE means there's no prior anchor to compare against).
- Sort: relevance; max_results 20.

**Secondary:** Cochrane Library direct (via web_fetch to cochranelibrary.com search). Look for any Cochrane review covering the same population × intervention.

**Tertiary:** Scholar Gateway, scoped to clinical literature on the parameter.

**Required connectors:** PubMed, Cochrane (via web_fetch). Scholar Gateway preferred but not blocking.

### 3.2 co1_zero_jurisdictions

**Primary:** Scholar Gateway. Query:
- Lived-experience / participatory-design / DPO terms AND parameter terms AND population terms.
- Year filter: typically no constraint; older DPO position papers remain valid (per `supersession-audit_SKILL.md` Co-1 supersession rule).

**Secondary:** Direct DPO/NGO publication catalogs. Named-organization fetch list (project-canonical):
- General disability: International Disability Alliance (IDA), Disabled Peoples' International (DPI)
- Mobility: ENIL (European Network on Independent Living), Spinal Injuries Association (UK), United Spinal (USA)
- Deaf / hard-of-hearing: World Federation of the Deaf (WFD), Hearing Loss Association of America (HLAA), RNID (UK)
- Blind / low-vision: World Blind Union (WBU), RNIB (UK), American Council of the Blind (ACB), American Foundation for the Blind (AFB)
- Little people / dwarfism: LPA Medical Resource Center (USA), Restricted Growth Association (UK)
- Cognitive / neurodevelopmental: Inclusion International, Autism-Europe, Autistic Self Advocacy Network (ASAN)
- Mental health: Mind (UK), NAMI (USA), Mental Health Europe

**Tertiary:** Multilingual-research handoff for non-anglophone jurisdictions named in the gap.

**Required connectors:** Scholar Gateway. PubMed is NOT a substitute (different corpus).

**Outcome rule:** Co-1 evidence accumulates rather than supersedes (per `supersession-audit_SKILL.md` §3 Co-1 rule). The default outcome for any Co-1 gap with new lived-experience finds is `partial_evidence_found` until the cumulative Co-1 corpus crosses the slug's worked-example threshold (defined per slug; see `decisions/DR-2026-05-26-gap-driven-mining-protocol.md` §Out-of-scope — the threshold is owner-determined per pilot).

### 3.3 numerical_spec_uncited

**Primary:** PubMed search.
- Query: parameter+population+outcome.
- No tier filter (THIN-BASE may surface evidence at any tier).
- Sort: relevance; max_results 20.

**Secondary:** Scholar Gateway. Same query.

**Required connectors:** PubMed. Scholar Gateway preferred.

**Mandatory follow-up if discoveries surface:** the gap's outcome cannot be `closure_evidence_found` until the discovered source's spec value is validated by `progressive-measurement` skill (PMP walk). The intermediate state is `partial_evidence_found` with `notes` recording the PMP queue position. See §4 for the closure workflow.

### 3.4 qualitative_uncited

**Primary:** PubMed search.
- Query: parameter+population+outcome (parameter is a qualitative concept rather than a numerical value).
- Publication-type filter: no constraint.

**Secondary:** Scholar Gateway. Same query.

**Tertiary:** Direct standards-body catalog if the gap involves a normative requirement (e.g., "should be / shall be" claims).

**Required connectors:** PubMed. Scholar Gateway preferred.

### 3.5 standards_not_promoted

**Primary:** Direct standards-body catalog fetch (via web_fetch).
- For named standards in the gap description (e.g., "JGJ 450-2018", "DIN EN 54-2"): fetch the catalog page for the standard, verify it exists, harvest metadata (issuing body, edition year, jurisdiction, supersession history).
- Statutory metadata (issuing body / edition year / jurisdiction / standard number) qualifies the candidate as `metadata_quality = COMPLETE-STATUTORY` (per PI rule #10 amended 2026-05-18).

**Secondary:** Multilingual-research skill if the standard is non-English (e.g., JGJ is Chinese; standards-body publication is in Chinese).

**Required connectors:** web_fetch to the standards-body catalog; multilingual-research as needed.

**No PMP required.** Standards-promotion gaps are about adding an existing real standard to the evidence base, not validating a numerical value.

### 3.6 cross_population_invisibility

**Primary:** Population-coded PubMed query.
- Query: population terms (named populations from the gap description, e.g., "DEAF", "DBL", "IntD") AND domain terms (the BPC topic; e.g., "circulation", "wayfinding", "emergency egress").

**Secondary:** Scholar Gateway with same query.

**Tertiary:** Multilingual-research handoff if a population's primary literature is in a non-anglophone language (relevant for international DPO position papers).

**Required connectors:** PubMed, Scholar Gateway. Multilingual-research as needed.

**Outcome rule:** The gap closes when each BPC named in the gap description has at least one cited source covering the previously-invisible population (cross-checked via `evidence_population_match` rows). Until then, the outcome is `partial_evidence_found` with `notes` enumerating which BPCs still lack coverage.

---

## 4. Outcome judgment and writes

For each gap, after running the matrix:

| candidates returned | judgment workflow |
|---|---|
| 0 | Outcome = `null_result`. Record `search_strategy_record` and close. |
| 1-2 | Sonnet reads abstract(s); applies the §4.1 decision rules. For ambiguous cases, escalate to Opus. |
| 3+ | Opus reads abstracts; multi-candidate synthesis. |

### 4.1 Five-outcome decision rules

**`closure_evidence_found`**: at least one candidate is verified-grade evidence (`metadata_quality ∈ {COMPLETE, COMPLETE-STATUTORY}`, `verification_status ∈ {VERIFIED, UNVERIFIED-1}`) AND addresses the gap's parameter × population × outcome AND (if a numerical-spec gap) has cleared the PMP walk under `progressive-measurement` AND the four rule #7 fields (`falsification_condition`, `confidence_interval`, `shift_conditions`, `named_dissenter`) populate before the gap moves to `CLOSED-FIXED`.

**`partial_evidence_found`**: candidates exist but none alone closes the gap. Common cases: (a) Co-1 evidence below the worked-example threshold for the slug; (b) numerical-spec gap where the PMP walk is queued but not complete; (c) cross-population-invisibility gap where some BPCs gained coverage but others did not. The `notes` field enumerates the remaining shortfall.

**`null_result`**: every matrix strategy ran cleanly (all required connectors available, all queries executed) and returned 0 relevant candidates. The gap stays OPEN; re-eligible after 6 months per §5.

**`gap_recategorized`**: during the pass, the gap is discovered to not actually be mining-addressable (e.g., description revealed a content-authorship issue or a database correction need). Set `mining_addressability = 'NOT-ADDRESSABLE'` (separate `update-gap-addressability` call), and record `notes` (≥20 chars) explaining the re-categorization. The gap is then handled by its appropriate skill.

**`deferred`**: a required connector for the gap's pattern is unavailable, or the candidates returned cannot be evaluated without a downstream skill (e.g., a non-English candidate where multilingual-research is offline). Record `notes` (≥10 chars) naming the blocker. The gap is re-eligible immediately when blockers clear.

### 4.2 Recording the attempt

For each gap attempted, write one `gap_mining` row via:

```bash
python3 scripts/db.py add-gap-mining \
    --gap-id {GAP-NNN} \
    --search-strategy '{"strategies": [{"tool":"pubmed","query":"...","date_filter":"...","candidates_returned":N}, ...]}' \
    --candidates-returned {total across all strategies} \
    --candidates-reviewed {total reviewed} \
    --outcome {closure_evidence_found|partial_evidence_found|null_result|gap_recategorized|deferred} \
    --discoveries '["REF-00NNN","REF-00NNN"]'   # FK list of verified+INSERTed ref_ids \
    --candidate-dois '["10.xxxx/yyyy"]'         # DOIs of unverified candidates (PI rule #10 gate) \
    --check-method {pubmed_cluster|scholar_gateway_lived_experience|cochrane_direct|standards_body_direct|multilingual_research|composite} \
    --notes "..." \
    --session {SESSION}
```

The `candidate-dois` field is the rule #10 gate: candidates returned by the search but not yet verified live as DOIs only; they are NOT auto-INSERTed to `evidence_sources`. A subsequent verification pass (separate session) promotes them. Mirrors `supersession_check.superseding_dois`.

### 4.3 Closure workflow (when outcome = closure_evidence_found)

The `gap_mining` row alone does NOT close the gap. The closure workflow:

1. INSERT verified candidates to `evidence_sources` with `discovery_method = 'gap_driven:GAP-NNN'`. Use `scripts/db.py add-source` per existing protocol.
2. Add `source_slug_links` rows linking each new source to the slug(s) the gap implicates.
3. Add `evidence_population_match` rows per rule #7 (grade EXACT/PARTIAL/PROXY/MISMATCH; ref_id FK).
4. Populate the four rule #7 fields on the gap row:
   ```bash
   python3 scripts/db.py update-gap-research-fields \
       --gap-id GAP-NNN \
       --falsification-condition "..." \
       --confidence-interval "..." \
       --shift-conditions "..." \
       --named-dissenter "..." \
       --session {SESSION}
   ```
5. (Numerical-spec gaps only) Run `progressive-measurement` skill PMP walk. The PMP walk produces `spec_value_probes` rows; the gap cannot close until strict-termination is met.
6. (Discoveries that supersede existing anchors only) Write a `supersession_check` row per `supersession-audit` skill §4. The gap_mining row and the supersession_check row both reference the same discovery; they describe orthogonal relationships (gap-closure vs anchor-replacement).
7. Close the gap:
   ```bash
   python3 scripts/db.py close-gap --gap-id GAP-NNN --status CLOSED-FIXED --session {SESSION}
   ```

---

## 5. Cross-session idempotency and re-eligibility

`gap_mining` is append-only. Each pass adds rows; older rows are retained for audit history. The operative outcome for each gap is the row with `MAX(attempt_at)`.

**Re-eligibility rules:**

| Previous outcome | When re-eligible |
|---|---|
| `null_result` | After 6 months (`attempt_at < today - 6mo`), with publication-date filter set to `> previous attempt_at` to scope search to truly new literature. |
| `partial_evidence_found` | Immediately if new candidate sources surface from any direction (citation-miner BATCH, an adjacent gap's mining, supersession-audit). |
| `deferred` | Immediately when the blocking connector recovers. |
| `gap_recategorized` | Never via gap-mining (the gap is now handled by another skill). |
| `closure_evidence_found` | Never unless the gap is reopened (e.g., a cited discovery is retracted). |

This protocol is semiannual-sweep-ready: re-run the BATCH query filtered to `attempt_at < (today - 6 months)` with publication-date filter `> previous attempt_at`.

---

## 6. Discovery cross-write with citation-miner (BATCH-mode handshake)

The DR-2026-05-26 attestation logged one deviation: BATCH-mode citation-miner can discover a source that closes a previously mining-addressable gap. This skill specifies the handshake.

**Trigger.** When `citation-miner` BATCH writes a new `evidence_sources` row whose population-match (via `evidence_population_match`) matches an OPEN+ADDRESSABLE gap's pattern (parameter × population × outcome inferred from the gap's `section` and description), citation-miner emits a handshake event.

**Handshake.** The handshake event is a hint, not an auto-write. Specifically:

1. Citation-miner records the candidate gap match in its session report: `[CANDIDATE-GAP-MATCH: GAP-NNN via REF-NNN]`.
2. The next gap-driven-mining invocation (INLINE or BATCH) treats the candidate as a pre-surfaced source for that gap (skipping primary search; running secondary/tertiary only as needed for triangulation).
3. The outcome judgment runs normally per §4.1. The matrix attempt's `notes` records the citation-miner provenance: `"discovered via citation-miner BATCH backward_from:REF-XXX; primary search skipped"`.
4. If the outcome is `closure_evidence_found`, the §4.3 closure workflow runs. The `gap_mining.search_strategy_record` JSON has a single strategy entry `{"tool":"citation_miner_handshake","candidates_returned":1,"candidates_reviewed":1}` if no further search was needed.

**Anti-pattern.** Citation-miner does NOT auto-write `gap_mining` rows. The matrix in §3 still runs (or is explicitly skipped per the handshake record) so the gap's closure has an auditable mining attempt. A `gap_mining` row written without a §3 matrix attempt would create the topic-evidence-vs-claim-evidence anti-pattern PI rule #7 fights.

---

## 7. Spot-check requirement (per PI rule #11 attestation)

When this skill is invoked, the audit trail must include:

- `[READ: DR-2026-05-26-gap-driven-mining-protocol.md]` tag.
- At least one `[STAGE: gap-driven-mining-{GAP-NNN}]` boundary per gap attempted.
- For BATCH mode: a session-end summary `[STAGE: gap-driven-mining-batch-summary]` enumerating outcomes by category, deferred connector blockers (if any), and remaining queue size.

Per-session attestation requirement: when this skill writes any `gap_mining` rows whose outcome is `closure_evidence_found` (which involves synthesis-bearing writes per §4.3), the session's commit message carries `[DOCTRINE: <sha>]` and the relevant `attestations/sessions_<file>.json` includes `gap-driven-mining` in `rules_in_scope` with status `FIRED` and an `evidence_path` pointing to the `gap_mining` rows written (use `db://gap_mining/GAP-NNN` token form).

---

## 8. Anti-patterns

**Treating citation-miner and gap-driven-mining as substitutes.** Citation-miner is anchor-source-keyed (start from a confirmed source, traverse its citation network). Gap-driven-mining is gap-keyed (start from a parameter × population × outcome shortfall, search for evidence that addresses it regardless of whether it cites existing anchors). Each closes a different class of evidence-base failure. Running citation-miner on a slug whose gaps are not anchor-shaped will not close those gaps; running gap-driven-mining on a slug whose anchors are simply unmined will produce noise.

**Auto-promoting candidates to evidence_sources.** PI rule #10 forbids INSERTing search candidates as `evidence_sources` rows without verification (existence + content). Candidates live as DOIs in `gap_mining.candidate_dois` until verified. The verification is a separate operation governed by `citation-verifier` skill.

**Closing a numerical-spec gap without PMP.** Rule #8 requires the PMP walk for any BPC item asserting a numerical spec value. A `gap_mining` row with `outcome = closure_evidence_found` on a numerical-spec gap is invalid without a corresponding `spec_value_probes` walk passing strict-termination. The `gap_mining_audit.py` Level-2 audit script checks this invariant.

**Substituting one connector for another on Co-1.** PubMed indexes biomedical literature; Scholar Gateway indexes design / lived-experience / DPO publications. They do not overlap on the corpus Co-1 evidence requires. Running PubMed search on a `co1_zero_jurisdictions` gap is the topic-evidence vs. claim-evidence anti-pattern (rule #7) in connector form.

**Topic evidence vs. claim evidence.** Same anti-pattern as rule #7 and rule #8 fight: "evidence ON the parameter" ≠ "evidence supporting the specific claim the gap's slug needs." The `evidence_population_match` grade (EXACT/PARTIAL/PROXY/MISMATCH) is the project's canonical gate against this — every discovery logged under §4.3 step 3 must grade EXACT or PARTIAL to count toward closure.

**Closing a gap without populating rule #7 fields.** `outcome = closure_evidence_found` is necessary but not sufficient for `status = CLOSED-FIXED`. The four adversarial-research fields (`falsification_condition`, `confidence_interval`, `shift_conditions`, `named_dissenter`) must populate first. Per §4.3 step 4.

---

## 9. Edge cases

**Gap's parameter / population / outcome can't be expressed in English search terms.** Mark `outcome = deferred`, `notes = "non-English search terms required; queued for multilingual-research handoff"`. Do not guess.

**Gap matches no pattern in §2.** Outcome = `gap_recategorized`. Set `mining_addressability = 'NOT-ADDRESSABLE'` and notes the shape (≥20 chars). The gap returns to triage.

**Gap's slug is RETRACTED-PRE-REHAB.** The gap is still mineable; closure does NOT lift the slug's retraction banner. Per `decisions/DR-2026-05-23-pre-rehab-banner-cohort-definition.md`, banner removal is a separate Phase-E.2g rehabilitation transaction. The `gap_mining` row records the discovery; the slug's banner persists until E.2g reverification.

**Candidate identified but it's behind a paywall and the abstract is too thin to grade.** Per rule #10 sub-rule 2 (`PAYWALL` value-match), `outcome = partial_evidence_found` with `notes = "candidate {ref or doi} behind paywall; cannot grade value-match; queued for downgrade or non-paywalled corroboration"`. The candidate stays in `gap_mining.candidate_dois`; it is not promoted.

**Two different gaps share a discovered source.** Each gap gets its own `gap_mining` row referencing the same discovery in `discoveries_logged`. The `evidence_sources` row exists once; the `source_slug_links` rows link it to each implicated slug; the two `gap_mining` rows describe the gap-closure dimension per gap.
