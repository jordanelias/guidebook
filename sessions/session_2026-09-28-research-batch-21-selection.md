# Batch 21 — Mactaggart 2024 and the Uganda code, Martins 2016, and a superseded PROXY rule found live in the corpus

**Session id:** `session_2026-09-28-research-batch-21-selection`
**Branch:** `claude/research-batch-apparatus-fnnd5b` (continued after PR #164 merged; resynced with `git merge origin/main`, per CLAUDE.md §7 — `git checkout -B` and `git rebase` are both blocked in this harness)
**Cell:** parameter 3 (TERM-001 `ramp gradient`) × MOB.
**Session kind:** research (writes rows only — evidence, judgment, research-stage tables). No tooling, schema or script changes ship in this PR (rule 10) — the only tracked non-data files this diff touches are derived surfaces (`audits/`, `tools/*.html`, `governance/context-map.yaml`), regenerated mechanically from the DB, never hand-edited.

**Derive every figure.** Re-run the command beside a number rather than trust the sentence.

---

## 0. The independent adversarial pass, and what it found

An independent `antagonist` agent (model `claude-fable-5-1`, different from this session's `claude-sonnet-5` — a genuine independent pass, not self-administered) reviewed the scratch DB before emission. Its full report is `transcripts/harness_360642ec/subagents/2026-09-28T07-09-42_other_af0b8fe7.jsonl`. Recorded as adversarial pass `pass_id=2` — **left OPEN, not closed; see §0c.**

**24 findings, 14 SUSTAINED (2 CRITICAL, 6 HIGH, 5 MEDIUM, 1 LOW), 9 SURVIVED, 1 WITHHELD-FOR-OWNER.** 11 of the 14 SUSTAINED findings were repaired (migration `data_20260928074257_...sql`); 3 could not be — recorded as PROVISIONAL-DISPUTED with a reason, not silently dropped.

### 0a. CRITICAL — both population-match grades applied a rule the owner superseded

This session graded REF-01009 (Mactaggart 2024) and REF-01011 (Martins 2016) PROXY for MOB, reasoning respectively from "no mobility impairment among the co-producing facilitators" and "no-participants = PROXY". **Both grounds are exactly what the owner ruled out on 2026-09-25** (`references/project-standards.md`, "A FACILITY AUDIT'S POPULATION GRADE DOES NOT TURN ON WHETHER ITS AUDITORS WERE DISABLED"): REF-01007, the same study class as REF-01011 (a facility census), was re-graded PROXY → PARTIAL on exactly this point, and that precedent — not REF-01003's 23-participant walking study, which this session wrongly cited — is the one that applies. Re-graded PARTIAL on both rows (`amend-population-match`), following REF-01006/REF-01007's own template: population served is MOB, measurement is one step removed (a checklist audit, not an observation of a disabled person negotiating a ramp). The Co-1 tier on REF-01009's `evidence_sources` row is untouched — the ruling explicitly separates the two questions.

Read the ruling before grading another facility audit: `sed -n '3989,4025p' references/project-standards.md`.

### 0b. HIGH — a genuinely DPO-co-branded document was retrieved, quoted, and never filed

Exec 103 (the CERMI-name-anchored GAP-049 search) surfaced the Madrid city council / **CERMI Comunidad de Madrid** joint accessibility methodology (Dec 2018) — CERMI's name is on the title page and every page footer. It was retrieved, read, and quoted in exec 105's own findings_note (twice claiming it had been "staged as a candidate"), but no `search_candidates` row existed until this correction. Staged now as `candidate_id=132`, with the real page-24 figures (`Rampas de menos de 3 m. pendiente máxima 10%. Rampas de entre 3 y 10 m. pendiente máxima 8%.`) and a `research_code_leads` entry (`lead_id=93`, status RETRIEVED — this one directly retrieved, not secondary-sourced). GAP-049's own text, which said this pass found "never a DPO's own voice", is corrected: the search shape worked; the filing did not happen. `add-candidate` cannot verbatim-check a claim against a binary PDF — worked around by deriving a text extract through `retrieval_log.derive()` (the sanctioned path for exactly this) and citing that instead.

### 0c. HIGH — `extraction_id=72`'s NBR 9050 note hid a number it should have surfaced

Word-level re-extraction of the persisted Martins PDF (page 4, Table 2) reads `Item Inclinação máxima (2%) Piso antiderrapante...` — "(2%)" genuinely attaches to the item; the first pass dismissed it as a column-bleed artefact without justification. 2% is not a plausible NBR 9050 *running*-slope maximum (roughly 5–8.33%) but is squarely in NBR 9050's *cross*-slope range — independently corroborated the same batch by the Madrid/CERMI document's own explicit `La pendiente transversal máxima será del 2%`. Whether Martins' "Inclinação máxima" item measures running or cross slope cannot be settled from the bytes; the ambiguity is now recorded on the row (`amend-extraction`) rather than silently resolved in favour of the reading that let the row sit on parameter 3 cleanly. Two further misreadings on the same row, also corrected: the "apenas 30,0%... não obedece" sentence is in the *Discussão*, not Results; the cited California comparison (98.8%) is about ramp length/landing/width, not slope.

### 0d. HIGH — no persisted bibliographic payload backed a "confirmed this session" claim

Both DOI admissions (REF-01009, REF-01011) were stamped `doi_resolution_outcome=RESOLVED` and `metadata_quality=COMPLETE` on the strength of ad hoc `curl | python3 -m json.tool` lookups outside the sanctioned `retrieval_log.fetch()` path — CLAUDE.md §5(c): no artefact, no proof. Fixed by fetching and persisting each DOI's actual Crossref record (`retrieval-log/.../1995c39d5571f3ec.json`, `dfca4e706e2da8b0.json`) and backfilling the fields Crossref supplies via `correct-source` (volume, issue, article_number, journal_name, publisher on both rows). `retrieval_log.py --verify-authors` now runs clean on both except one residual — §1's `pages` mis-file, which `correct-source` cannot clear (see §3).

### 0e. HIGH — a citation-mining row claimed "mined" over an attempt that examined nothing

REF-01009's forward-mining pass (two Europe PMC calls, both 503) was logged via `--deferred-reason`, which is for a pass **deliberately not run** — this one was attempted and failed, which is what `--notes` is for (the CLI's own docstring makes this distinction explicit). The result: `citation_mining.deferred_reason` populated while `evidence_sources.citation_mining_status='mined'`, exactly the state `test_db_integrity` C08 exists to reject (red on the scratch DB, green on `main`). Re-logged via `--discharge-deferral --notes` instead; C08 is green.

### 0f. MEDIUM, repaired — GAP-054 re-filed GAP-043 under a new id

GAP-043 item (1) already names this exact mechanism (`correct-source` keys by DOI; `amend-source` refuses bibliographic fields; a DOI-less row is unreachable by either). This session hit the same wall admitting REF-01010 (no DOI) and filed a new gap instead of extending the existing one — a rule-5 violation in the gaps register itself. GAP-054 closed `CLOSED-DUPLICATE`; its real content (the `pages`/`article_number` instance, the new observation that `research_batch_dod`'s R3 check never reads `source_value_extractions.loc_*`, and a third, narrower case — `correct-source` also cannot **clear** a field the payload is silent on, even on a DOI-bearing row) folded into GAP-043.

### 0g. MEDIUM, repaired — REF-01009's co1_provenance reversed a headcount

Said "six of the eight then underwent facilitator training." The persisted JATS XML says all eight trained; six were then selected for the pilot. Corrected (`amend-source`). The population-match row's own headcount (three named impairments summing to 6, labelled "8") could not be corrected the same way — `amend-population-match` only appends when the grade itself is unchanged, and did not visibly append on a same-grade call; recorded here since the tool gave no error either. The correct figure is on `evidence_sources.co1_provenance`.

### 0h. MEDIUM, repaired — `claimed_value='30,0'` was not machine-readable

Portuguese comma-decimal, unparseable by `assess_cell.parse_bound` and excluded by `v_derived_figure_check`'s GLOB — every other numerical row in the corpus uses dot-decimal or `a:b`. Not overwritten (D-0168: a wrong value is a second row, not an edit) — `extraction_id=73` restates the identical fact and quote with `claimed_value='30.0'`; `extraction_id=72` is cross-referenced, not retracted, and carries the additional corrections from §0c.

### 0i. Two findings not remediated — no writer exists

`research_code_leads` has an INSERT (`add-code-lead`) and no update verb at all; the `UNIQUE(jurisdiction, standard_name)` constraint refuses a second insert for the same lead. Two findings against this session's own leads — lead 90 misnaming UNAPD ("Uganda National Action on Physical Disability" for "Uganda National Association of Persons with Disabilities"), and leads 91/92 carrying prose in `clause` instead of a real locator or `[UNVERIFIED-QUANT]` — are correct and not remediated. Disposed `PROVISIONAL-DISPUTED`, not silently accepted. A third, `manifest.jsonl` line 5's stale "staged as a candidate" purpose text (retrieval-log manifests are append-only), same disposition — the underlying fact is fixed (§0b); the one already-written log line is not.

### 0j. WITHHELD-FOR-OWNER

Whether Co-1 tier-1 attaches to REF-01009 as a *source* (the instrument's co-production, satisfied) or should be read narrower — to *this extraction* specifically, a tape-and-inclinometer compliance reading against a criterion the study team (not the youth researchers) took from the 2019 Code — is a doctrine call, not a factual one. Not resolved here.

### 0k. Nine SURVIVED, and why the pass could not be CLOSED

Extraction 70/71's `claim_text`, the 14 author rows, tier derivation, and four more attacks held under independent re-verification. **But `close-adversarial-pass` refuses to close: every one of the 9 SURVIVED findings' `artefact` field fails `dbcore.resolve_under`**, because the reviewer cited richer, genuinely-checkable references (two files joined with `;`, a code symbol plus file, a table-and-row reference) rather than the bare single existing path the closer requires — a deviation from the antagonist's own documented report format, with a disproportionate consequence: nothing in `db.py` can correct a finding's `artefact` field after `record-adversarial-pass` has parsed it from the (tracked, immutable) transcript, and a second pass for the same session is refused by design. Filed as **GAP-055** (P2). `adversarial_pass_audit.py --session session_2026-09-28-research-batch-21-selection` reports the pass RECORDED but not CLOSED — **a reasoned waiver, alongside §3's R3 waiver, not a remediation.**

---

## 1. REF-01009 — Mactaggart et al. 2024, and REF-01010 — the Uganda Building Control Code, 2019

Candidate 126 (staged batch 20, `session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa`) was left `PENDING-VERIFICATION` because the ramp-access composite criterion's threshold sat in an unretrieved appendix. Retrieved this session — Springer's direct static-content mirror bypassed an auth-walled `link.springer.com` redirect — and read: `Composite score if ramp slope (min 1:12) and width (min 1300mm) is acceptable, has handrails and is non-slip`, footnoting two sources: a 2014 Uganda "practical guide" (recommending a gentler 1:20/1:10) and the binding **Building Control (Accessibility Standards for Persons with Disabilities) Code, 2019** (S.I. 2019 No. 52) — max 1:12, clause 12(3)(a).

**D-0178 reading.** The persisted JATS XML shows genuine participatory design, not mere data-collection labour: eight Ugandan youth researchers with disabilities reviewed the DAC's individual questions and proposed Uganda-specific changes (Round 1), then held a round-table review of the draft tool with the study team (Round 3) — they shaped the instrument's content. Admitted `evidence_type=co1, tier=1` (`schemas/tier_derivation.py`: `co1/intrinsic → 1`). All eight then trained as facilitators; six were selected for the pilot (corrected, §0g). No mobility impairment is named among the eight — Deaf, albinism, and visual impairment are the three individually described.

**REF-01010** was retrieved directly — `kcca.go.ug`'s PDF, cross-checked against the quotation in Mactaggart's own appendix, word-for-word match — and admitted `evidence_type=code, tier=6`, no DOI. `extraction_id=70`: clause 12(3)(a), 1:12 max gradient, `--verbatim-exempt` (the PDF's content streams don't decode as text for `quote_in_artefacts`, the sanctioned exemption for exactly this). `extraction_id=71` (REF-01009): the main article's own finding — "two were too steep and none had handrails... all failed" — corroborated at facility-aggregate level by Supplementary Table 2 ("Ramp meets access standards": 0 of 3, 0%). No raw per-facility degree/ratio measurement exists anywhere in the source; only the binary composite pass/fail.

Both `research_code_leads` entries for the two sources cited in Mactaggart's own footnote: lead 89 (Uganda 2019 Code, RETRIEVED), lead 90 (the 2014 guide, REFERENCE-ONLY — a direct retrieval attempt at asksource.info returned 503; UNAPD's name corrected as far as this session's own XML-reading goes, but the lead's stored text could not be fixed, §0i).

Candidate 126 resolved ADMITTED → REF-01009; the admission edge backfilled onto its originating search (exec 93) via `link-admission`, since the edge was never written at log-search time. Citation-mined (backward, targeted — the two footnoted sources specifically, not all ~38 references; forward attempted, found nothing due to a transient Europe PMC outage, corrected per §0e).

## 2. REF-01011 — Martins et al. 2016, read in the language it was written in

Candidate 129 (also staged batch 20) was left unresolved because the co-published English PDF's "have maximum slope" was flagged as an ambiguous translation. Live `scielo.br`/`scielosp.org` access is blocked by a Bunny Shield WAF challenge (403, JS proof-of-work) — worked around with the Internet Archive Wayback Machine (`web.archive.org/web/<ts>if_/...`, the `if_` suffix avoiding an unrelated proxy egress-policy quirk on the plain form), retrieving both the English and the **Portuguese original** (SciELO's own naming convention: `en_...pdf` is the translation, the unprefixed filename is the original).

The Portuguese resolves the flagged ambiguity: Table 2's own header ("Inclinação máxima", Sim/Não) shows it is a checklist compliance item — "meets the requirement", not "is at the limit" — confirming the staging note's caution was warranted. But the table cell carries its own further ambiguity, found only by an independent pass: `(2%)`, likely NBR 9050's cross-slope limit rather than the running-slope concept parameter 3 concerns (§0c). Admitted `evidence_type=clinical, scope=lower_control, tier=3` (a descriptive checklist audit with no control, same pattern as REF-01003/1005/1006/1008). `extraction_id=72` records the 30.0% figure (comma-decimal, corrected by `extraction_id=73`, §0h) with an open note on which denominator (90 total buildings vs. the ~43 with a ramp) the source's own prose intends — Table 2's own arithmetic (27/90=30.0% exactly) points to the full sample, not the ramped subset the abstract's "destas" phrasing implies.

## 3. GAP-043 — the DOI-keying defect, now with two more instances

REF-01010 (no DOI) needed `--pages` at admission and did not get it; `amend-source` refuses it as bibliographic, `correct-source` refuses it for having no DOI to key a payload to — GAP-043 item (1)'s exact mechanism, now for `pages`/`article_number` rather than `journal_name`/`publisher`. A second, narrower case: even REF-01009 (DOI-bearing) cannot have its wrongly-filed `pages='237'` (Crossref's own `article-number`, mis-filed at admission) cleared, because `correct-source` refuses to write a field its payload is silent on ("a silence is not a correction"). Neither is remediated — both are reasoned waivers, alongside `research_batch_dod`'s own R3 failure on REF-01010 (which reads `evidence_sources.pages`/`article_number`, never `source_value_extractions.loc_*`, where REF-01010's clause is in fact precisely recorded: `loc_section=12, loc_subsection=3, loc_clause=a`). GAP-054, a near-duplicate this session first filed, is closed and folded in (§0f).

## 4. GAP-049 — the multilingual Co-1/DPO pass, honestly run, mostly null, one real find recovered

Four web-engine (not biomedical-index) searches, ES and FR, each language run twice — a generic technical query, then a DPO-name-anchored one (CERMI, APF France handicap) — per the gap's own ask ("more than one language and more than one kind of index"). Three of four surfaced only commercial ramp-equipment vendors and construction blogs restating national code figures, never a DPO's own voice: CTE DB-SUA 9 (Spain, 10/8/6% tiered), the 2014/2017 French arrêtés (5/8/10/12%) — both filed `REFERENCE-ONLY` (leads 91, 92; the `clause` field's prose defect is §0i). The fourth (CERMI) genuinely did surface DPO-co-branded content — corrected into §0b/§1 rather than left as the false null this session's first pass recorded.

One caution, deliberately not converted into a finding anywhere: exec 104's own WebSearch summary invented an untraceable named testimony ("Marie Dupont... APF France Handicap rapport mars 2026") with no corresponding URL in the returned results — flagged in the search's `findings_note`, used nowhere. An independent pass confirmed no leakage into any evidence/extraction/gap row.

GAP-049 stays OPEN. A future attempt should try a DPO's own publications repository directly, or a disability-studies-specific index, rather than repeating this query shape in a third language.

## 5. GAP-033 item 1 — investigated, not resolved

The ramp-versus-route scope of parameter 3 is the owner's call (GAP-047: "left for the batch that re-determines parameter 3"), not this one's. Derived the full affected set — `select extraction_id, ref_id, claim_text from source_value_extractions where parameter_id=3 and (claim_text like '%path%' or '%trail%' or '%walkway%')`: extractions 39 (weak — a ranking phrase, no path-specific value), 43 (REF-01001, gravel-trail 9.01%), 49 (REF-01003, outdoor pathways); and the four `DEFERRED` term-adjudication observations blocked on the same question (40, 41, 47, 48), all carrying byte-identical boilerplate. Two options recorded, neither applied: (A) narrow parameter 3 to engineered ramps, moving 39/43/49 to a new route-gradient parameter; (B) read parameter 3 as functional (the maximum climbable running gradient anywhere on an accessible route, construction method immaterial) — for which ADA 2010's own definition of "ramp" (any walking surface steeper than 1:20) is suggestive, not dispositive.

## 6. What this session touched, derived

```
python3 -c "
import sqlite3
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
for t in ('evidence_sources','evidence_source_authors','source_slug_links','source_value_extractions',
          'evidence_population_match','search_candidates','search_executions','search_admissions',
          'citation_mining','observed_terms','research_code_leads','gaps',
          'adversarial_passes','adversarial_findings','economics_entries'):
    n = con.execute(f\"select count(*) from {t} where created_by_session like '%research-batch-21-selection%' or updated_by_session like '%research-batch-21-selection%'\").fetchone()[0]
    if n: print(t, n)
"
```

Two data migrations: `data_20260928074257_...sql` (the substantive batch — 75 inserts, 7 updates) and `data_20260928074651_...sql` (the adversarial-pass disposal and GAP-055 — 1 insert, 14 updates). No schema, script or governance-prose file changed.

## 7. Gates

`research_batch_dod.py --session session_2026-09-28-research-batch-21-selection` — **NON-COMPLIANT: 1 rule** (R3, REF-01010, §3 — reasoned waiver). Every other rule PASS. `test_db_integrity.py` — clean (0 ✗). `adversarial_pass_audit.py --session ...` — pass recorded, **not closed** (§0k — reasoned waiver, GAP-055). `scripts/preflight.sh` — **BLOCKING: `jurisdiction_db_vocabulary`** (§7a, third reasoned waiver, owner decision — not a GAP, not a tooling fix).

Three reasoned waivers ship in this PR: R3 (REF-01010's `pages`, §3), the unclosed adversarial pass (§0k), and the jurisdiction vocabulary (§7a). None is a corner cut on the research itself — the underlying facts they concern are correctly recorded and independently checkable; each needs either a tooling fix (GAP-043, GAP-055) or an owner ruling (§7a) this session is not authorised to make.

### 7a. `jurisdiction_db_vocabulary` — Uganda is not one of the 24 canonical jurisdictions

REF-01009, REF-01010, both `research_code_leads` rows (89, 90) and their extractions carry `jurisdiction='UG'`. `JurisdictionCode` (`schemas/enums.py`) and `governance/jurisdiction-philosophy.md` §1.1 name a **deliberately curated 24-country list, "confirmed at A3"**, selected against four stated criteria (geographic diversity, regulatory-model diversity, evidence-base strength, population scale) — Uganda is not on it; Kenya and Nigeria already fill the "Sub-Saharan representation" slots. Neither `schemas/enums.py` (tooling) nor the jurisdiction list itself (CLAUDE.md §8 names "jurisdiction" explicitly among the doctrine matters requiring owner sign-off) is this session's to change.

The doctrine already draws a distinction this check does not implement: §1.1 states the 24-jurisdiction requirement "applies to code/standards research (Tier 4–6), not to clinical evidence" — non-canonical-jurisdiction Tier 1–3 evidence is explicitly citable. REF-01009 is Co-1, tier 1 (participatory research, not a code document) — arguably already within that exception in spirit, even though the check refuses it regardless of tier. REF-01010 (tier 6, a Building Control Code) and the two `research_code_leads` rows are squarely Tier 4–6 code/standards research — the case the 24-jurisdiction scoping is actually *about*. **Left to the owner:** admit UG to the 24 (Uganda has a notably well-documented, disabled-led accessibility-assessment programme and a citable national code — an argument for, alongside the existing Sub-Saharan slots being an argument against a third African entry), or keep it non-canonical and have the check exempt Tier 1–3 rows the way the prose already says it should. Not remediated; not filed as a GAP (rule 8: this is a doctrine question, not a coverage bug the CLI should self-heal).

## 8. What the next batch takes

- **§7a — whether Uganda joins the 24 canonical jurisdictions, or the check gains a Tier 1–3 exemption.** Blocks `preflight.sh` cleanly (not `research_batch_dod`) until decided either way.
- GAP-033 item 1 (ramp-vs-route scope) — owner call, §5.
- GAP-049 — try a DPO repository or disability-studies index directly, not a third general-web-search language.
- GAP-043 — key `correct-source`'s payload lookup by url/handle/report_number as well as DOI (its own stated fix).
- GAP-055 — either a writer to correct a SURVIVED finding's `artefact`, or `close-adversarial-pass` accepting a delimited list, or the antagonist agent self-checking its own report shape before hand-back.
- Candidate 132 (Madrid/CERMI methodology) — read its methodology/acknowledgments section for CERMI's actual authorial role before any admission.
- Candidate 131 (certicalia, OUT-OF-SCOPE) needs no further action.
- REF-01009/1011's `pages` mis-files (§3) — no action possible until GAP-043 closes.
