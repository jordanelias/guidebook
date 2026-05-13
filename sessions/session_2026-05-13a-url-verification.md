# Session: URL-fetch verification (Stream 1+2+3) + Tier-A metadata corrections
**session_start:** 2026-05-13 01:00 UTC
**session_close:** 2026-05-13 02:00 UTC
**PI version (live):** v10.8
**Operative workplan:** `audits/bpc-rewrite-workplan-2026-05-11.md`

## Summary

Phase B URL verification, unblocked by the network-allowlist expansion noted as a blocker at the close of session_2026-05-12j. Three streams worked end-to-end against real HTTP, with Tier-A mechanical metadata corrections applied where multi-source authoritative agreement existed and downstream impact was bounded. Starting state: VERIFIED=361 (53%), UNVERIFIED-1=8, NULL=305. Ending state: VERIFIED=369 (55%), UNVERIFIED-1=1, UNVERIFIED-CLOSED=5, NULL=299.

## Work completed

### Stream 1 — direct URL fetches (6 URL-only NULL-verification records)
Records identified at session_2026-05-12j close as URL-blocked. All 6 attempted; result distribution:
- **VERIFIED via url-fetch (5):** REF-00298 (KfW Altersgerecht), REF-00300 (RHFAC retrofit cost), REF-00312 (KfW Altersgerecht — same page as REF-00298 but cited from a different slug), REF-00521 (Lindenwood DigitalCommons), REF-00627 (J-STAGE AIJA, Japanese calm-down spaces study).
- **UNVERIFIED-1 (1):** REF-00297. URL HTTP 200, but page is a DStGB press release describing the underlying TERRAGON study — title in DB had a one-word typo ('Bauen' vs 'Wohnen'); corrected under Tier A.

### Stream 2 — web-search URL discovery for the 4 grey-lit UNVERIFIED-1 records
- **VERIFIED (3):**
  - REF-00268 → Provan/Lane/Horne Rowan (2023) LSE CASE Report 147 for Habinteg, PDF at `eprints.lse.ac.uk/121508/1/casereport147.pdf`. URL field populated (was NULL).
  - REF-00378 → RCOT (2019) *Adaptations Without Delay* (Russell/Walker/Copeman/Porteus, commissioned from Housing LIN), PDF at housinglin.org.uk. URL populated; title corrected under Tier A.
  - REF-00023 → Steinfeld/Maisel/Feathers/D'Souza (2010) *Anthropometry and Standards for Wheeled Mobility: An International Comparison*, Assistive Technology 22(1):51-67, PMID 20402047. DOI/PMID/year corrected under Tier A.
- **UNVERIFIED-CLOSED (1):** REF-00128 — no Marquardt EADDAT-validation paper at 30 care homes in HERD exists. Strong lead documented: Fleming R (2011) Australas J Ageing, doi:10.1111/j.1741-6612.2010.00444.x, PMID 21923702 (same 30-facility EAT validation, but author/journal/tool differ from DB record). Content swap deferred to review.

### Stream 3 — ASPECTSS cluster recheck via real GET (not HEAD)
DOI `10.3389/fpsyt.2021.727353` returns HTTP 404 on `doi.org` GET (prior session reported 403 from HEAD only; GET is authoritative, 404 = DOI not registered). CrossRef `/works/{doi}` also 404. Per literature search, Mostafa's "ASPECTSS 2.0 Design Index" (2021) exists as a design guide for Dublin City University's Autism Friendly University initiative, not as a Frontiers in Psychiatry article. All 4 cluster records (REF-00051, REF-00129, REF-00517, REF-00592) → UNVERIFIED-CLOSED. Content swap deferred.

### Tier A — mechanical metadata corrections applied
Following the precedent set by session_2026-05-12j (which corrected REF-00204, REF-00332, REF-00006, REF-00068/151 DOIs once the underlying paper was unambiguously identified):
- **REF-00023:** doi `10.1080/10400430903496580` → `10.1080/10400430903520280` (suffix typo; confirmed by PubMed/CrossRef/ERIC); pub_year 2011 → 2010; pmid 20402047 added; PubMed URL added; `doi_resolution_outcome` → RESOLVED. Author-table edit (D'Souza is 4th of 4 authors, not 1st) deferred — `author_count_is_complete=0` already flags incompleteness; CrossRef enrichment via the corrected DOI will fill the missing rows.
- **REF-00297:** pub_title 'Bauen' → 'Wohnen' (`Barrierefreies Wohnen im Kostenvergleich`, confirmed by the cited DStGB page).
- **REF-00378:** pub_title 'Housing Adaptations Without Delay' → 'Adaptations Without Delay' (confirmed by PDF and RCOT publication page).

### Tier A.fix — reframe "duplicate" notes (correction of my own earlier framing)
Slug-link analysis showed that REF-00298/REF-00312 and the 4 ASPECTSS records each cite distinct slugs:
- REF-00298 → `accessible-design-economics-cost-premium`; REF-00312 → `construction-cost-data` (different BPCs).
- REF-00051/129/517/592 → 4 different sensory/framework slugs.

Per migration precedent `iec_60118_4_triplicate_documented_2026-05-12` (REF-00200/00328/00348 all share doi=10.31030/2853913 as INTENTIONAL distinct-scope citations of one standard), these are intentional multi-scope citations, not duplicates. Verification notes corrected on all 6 records to remove the misleading dedup framing.

### Rule #7 spot-check (GAP-189, ISO 23599 TWSI thin-base research)
- 4 adversarial-research protocol fields all populated and substantive.
- No topic-vs-claim conflation detected (the cited ISO 23599 IS the specific subject of the claim).
- **SCHEMA GAP FOUND:** `evidence_population_match` has no `gap_id` column, so closed gaps cannot be linked formally to their evidence_population_match rows. Rule #7's per-cited-study EXACT/PARTIAL/PROXY/MISMATCH grading has no FK path to a gap. Flag for governance/schema review.

### Rule #8 spot-check (PMP-B01-001, circadian lighting melanopic EDI)
- Empirical ceiling 285 EML ≈ 259 m-EDI defensible (just above Brown 2022's 250 m-EDI consensus, within walk tolerance).
- Step reasoning correctly uses Brown 2022's numerical threshold, not topic-evidence pattern.
- **SCHEMA/INSTRUMENTATION GAP FOUND:** `spec_value_probes.search_query` and `.search_query_alt` are NULL on all 8 probe rows. Rule #8 requires a step to pass only if "a second alt-phrasing search corroborates" — but the queries themselves aren't captured for audit. The walk's PASS/FAIL judgements may be correct, but they're un-auditable as written. Flag for governance/schema review.

## State deltas

| Metric                          | Session start | Session end | Δ   |
|---|---|---|---|
| VERIFIED                        | 361 (53%)     | 369 (55%)   | +8  |
| UNVERIFIED-1                    | 8             | 1           | −7  |
| UNVERIFIED-CLOSED               | 0             | 5           | +5  |
| NULL verification               | 305           | 299         | −6  |
| url_resolution_outcome=RESOLVED | 0             | 7           | +7  |
| url_resolution_outcome=RESOLVED-PARTIAL | 0     | 1           | +1  |
| url_resolution_outcome=DEAD     | 0             | 4           | +4  |
| Records with URL populated      | (n)           | +2          | +2 (REF-00268, REF-00378) |
| url_verification_runs rows      | 0             | 1           | +1  |

## Deliverables committed

| File | Action |
|---|---|
| `data/guidebook.db` | Stream 1+2+3 verification writes + Tier-A metadata corrections + reframe notes |
| `sessions/session_2026-05-13a-url-verification.md` | NEW — this file |
| `sessions/LATEST` | Updated pointer |

## Open items / flags for next session

**Content-review queue (DOI/title/author corrections beyond Tier-A scope):**
- REF-00023: author rewrite (Steinfeld E 1st of 4, not D'Souza 1st of 1) — pending CrossRef enrichment via corrected DOI.
- REF-00128: candidate content swap to Fleming 2011 *Australas J Ageing* (different author/journal/tool, but same 30-care-homes EAT validation).
- ASPECTSS cluster (REF-00051/129/517/592): each row needs an independent decision — replace with the actual Mostafa 2021 DCU AFU design guide citation, or close the slot.
- REF-00521 tier=4 may be miscategorised for a Lindenwood faculty paper (closer to tier 3 clinical/applied) — flag for Phase E per-BPC review.

**Slug evidence-base impact:**
- `design-framework-evidence-audit`: lost both REF-00128 and REF-00129 — drops from 6 VERIFIED to 4 (still over rule-#10 threshold but worth watching).
- `ndv-aut-built-environment-quantified-thresholds`, `detectable-gradient-protocol-sensory-zones`, `sensory-processing-model-design-application`: each lost 1 source.
- No slug fell to 0 VERIFIED.

**Schema gaps surfaced by rule #7 / rule #8 spot-checks:**
- Add `evidence_population_match.gap_id` FK column (rule #7 audit support).
- Make `spec_value_probes.search_query` and `.search_query_alt` NOT NULL or populate retroactively (rule #8 audit support).

**Remaining 299 NULL verification:**
- Stream 1 was exhaustive — no URL-bearing NULL records remain.
- 299 remaining are no-doi-no-url, mostly tier 4/5/6 standards/codes/national_fw — Phase B.7 (manual/institutional verification) work.

## YAML session-close block

```yaml
session_id: session_2026-05-13a-url-verification
session_close: 2026-05-13 02:00 UTC
deliverables_committed:
  - data/guidebook.db
  - sessions/session_2026-05-13a-url-verification.md (NEW)
  - sessions/LATEST (updated)
gaps_raised: 2 (schema instrumentation — see "Schema gaps surfaced")
gaps_resolved: 0
skills_invoked: []  # No skill files invoked directly — all work via direct DB + url-fetch
                   # (workplan-orchestrator, research-log-manager, session-consolidator
                   #  are skill files but no procedural invocation was tracked this session)
next_action: >
  Content review for REF-00128 (Fleming swap?), ASPECTSS cluster (DCU AFU guide?),
  and REF-00023 author rewrite via CrossRef enrichment.
  OR begin Phase B.7 manual-verification for the 299 no-doi-no-url remainder.
  OR address the two schema gaps surfaced by spot-checks before they accumulate.
blockers:
  - 299 no-doi-no-url sources require manual/institutional verification (Phase B.7)
  - Content decisions queued (4 items above)
  - 2 schema gaps in audit support (rule #7 epm.gap_id; rule #8 query capture)
verification_state:
  VERIFIED: 369 (55%)
  UNVERIFIED-1: 1
  UNVERIFIED-CLOSED: 5
  NULL: 299
  url_RESOLVED: 7
  url_RESOLVED-PARTIAL: 1
  url_DEAD: 4
spot_checks_completed:
  rule_7: GAP-189 (protocol OK; schema gap flagged)
  rule_8: PMP-B01-001 (ceiling defensible; instrumentation gap flagged)
```
