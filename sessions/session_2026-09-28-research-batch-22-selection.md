# Batch 22 — bucket-1/2 exhaustion for parameter 3 (ramp gradient) × MOB: Norway, Ontario, ISO, Ireland, New Zealand, Finland

**Session id:** `session_2026-09-28-research-batch-22-selection`
**Branch:** `claude/research-batch-apparatus-fnnd5b` (continued on the same branch as batch 21; PR #165 was still open/unmerged at session start)
**Cell:** parameter 3 (`ramp gradient`) × MOB.
**Session kind:** research (writes rows only — evidence, judgment, research-stage tables). No tooling, schema or script changes ship in this PR (rule 10). Two tooling defects were *found* this session (GAP-056, GAP-057) but not fixed here.
**Scope:** owner ruling 2026-09-28, "jurisdiction scope: buckets 1–2 exhausted before reaching further, for any slug" (`references/project-standards.md`) — bucket 1 (UN, ISO, CA, US, UK, DE, NO, SE, JP, AU) and bucket 2 (EU, SG, NZ, IE, FR, ES, PT, FI, NL, KR) per `workplan/2026-08-18-research-frame-proposal.md` §10 / OD-2. Uganda explicitly excluded from further research per owner instruction this same working session.

**Derive every figure.** Re-run the command beside a number rather than trust the sentence.

---

## 0. The independent adversarial pass, and what it found

<!-- FILLED IN AFTER THE ANTAGONIST AGENT REPORTS BACK. Do not ship this section as a placeholder. -->

---

## 1. Canada, Norway, ISO — REF-01012, REF-01013, REF-01014

**REF-01012 — Norway, TEK17 § 12-16(2).** First hit was the retired **TEK10** (`tek10.no`/an equivalent mirror self-disclosing "TEK10 er tidligere regelverk"); caught before use by reading the page's own supersession notice. Correct current instrument found at the renumbered section (12-16, not TEK10's 12-18). Tiered: general max 1:15, relaxed to 1:12 for runs under 3.0 m. `evidence_type=code, tier=6`.

**REF-01013 — Ontario, OBC 3.8.3.4(1)(b).** CSA B651 (the national standard) is Cloudflare-blocked on direct fetch (403) and Wayback access to `web.archive.org` failed for an extended period this session with a proxy-level `ws_closed_mid_exchange` condition (confirmed via `/__agentproxy/status` and a known-good control URL also failing — a genuine session-level outage, not a technique failure) — worked around by pivoting to the sub-national Ontario Building Code, per the user's own standing guidance that a bucket country's "exhaustion" may be satisfied at a provincial/state level where the national instrument is unreachable. Retrieved via a non-governmental mirror (`buildingcode.online`), which self-discloses it is not the official copy — `metadata-quality=GREY`, `verification-status=UNVERIFIED` accordingly. Two ramp provisions exist in the OBC: §3.4.6.7 "Ramp Slope" (general, occupancy-dependent, 1:6–1:10, **not** accessibility-specific) and §3.8.3.4 "Ramps" (explicitly "a barrier-free path of travel", 1:12) — only the latter is this parameter; the distinction is recorded on the extraction's own notes so a later reader does not conflate them. A second, independent search corroborated the gradient specifically against the current (2024, O.Reg 163/24) edition: unchanged at 1:12 (only the minimum width changed, 900→1000 mm, out of this parameter's scope).

**REF-01014 — ISO/CD 21542, 2007 committee draft.** The document is explicitly **not** the final published standard — its own cover states "This document is not an ISO International Standard… may not be referred to as an International Standard." `metadata-quality=GREY`, `verification-status=UNVERIFIED` reflects this. `evidence_type=standard_eb, scope=international, tier=4` (`schemas/tier_derivation.py`: `standard_eb/international → 4`). Two extractions: the numerical schedule (1:20 preferred tier, full Table 2/3 graduated schedule in notes) and a qualitative R7 harm/limitation finding — the drafting committee's own rationale that anything steeper than 1:12 "means a risk of accident… is not suitable for independent use" and is scoped to existing environments only. Both PDF-sourced, `--verbatim-exempt` (content streams undecodable by `quote_in_artefacts`; text independently extracted via PyMuPDF, matched against the persisted artefact's sha256).

A dedicated `research_code_leads` entry was **not** filed for the published ISO 21542:2011/2021 edition from this exec; see §3 for the one that was, filed via a different route (the UNICEF tertiary citation).

## 2. UN — screened, not admitted (exec 113)

No UN-Habitat-authored instrument with an independent, quantified ramp-gradient value was found. The one substantive UN-system document surfaced, UNICEF's *Accessibility Technical Cards* (2022), discusses ramp gradient at length (a detailed rise/slope/landing-interval schedule, p.14; a "gradients of pathway" passage, p.7) — but **every quantified figure in it is explicitly captioned to a third party**: the rise/slope table `(Source: ISO 2011)`, Figure 14 `(Source: ADA 1994)`, the pathway-gradient figures `(Source: UNESCO 1990, Centre for Accessible Environments and RIBA 2004)`. Checked 25+ figure captions across the 44pp document; none is UNICEF-original. Not admitted — filing it as a distinct evidentiary source would cite a tertiary restatement of standards already represented (REF-01014) or lead-filed (below) elsewhere in this corpus, the rule-5 "second table, same fact" shape applied to provenance rather than schema. Filed instead as `candidate_id=135` (disposition `OUT-OF-SCOPE`) and two `research_code_leads` (94: ISO 21542:2011 published edition, distinct from REF-01014's 2007 draft; 95: "UNESCO 1990", title unconfirmed).

UN has no `JurisdictionCode` enum value (`schemas/enums.py`) — moot here since nothing was admitted under it, but would block a future UN-jurisdiction admission. `INT` is the correct existing meta-code for genuinely cross-jurisdictional UN-system material (precedent: REF-00994, the IPC Accessibility Guide), not a missing "UN" code — this is a narrower, already-solved case of the gap batch 21 hit with Uganda, not a new instance of it.

## 3. Bucket-2 sweep — REF-01015 (Ireland), REF-01016 (New Zealand), REF-01017 (Finland)

**REF-01015 — Ireland, Technical Guidance Document M (Access and Use) 2022, clause 1.1.3.4.** Official `assets.gov.ie` PDF. Preferred maximum 1:20; relaxed to 1:12 where flights ≤2000 mm. Table 1 gives a three-tier graduated schedule (1:20/10 m/500 mm; 1:15/5 m/333 mm; 1:12/2 m/166 mm), interpolation permitted between tiers — structurally the same shape as REF-01012's tiering. The superseded 2000 edition was found and correctly excluded (`candidate_id=134`, `EXHAUSTED`). `evidence_type=code, tier=6, metadata-quality=COMPLETE-STATUTORY, verification-status=VERIFIED`.

**REF-01016 — New Zealand, NZS 4121:2001 clause 6.4.2.2.** A purchased Standards New Zealand document with no free official copy; the only full-text source found is a non-official archive.org mirror (`dn710908.ca.archive.org`) — same provenance shape as REF-01013's Ontario mirror, graded the same way (`metadata-quality=GREY, verification-status=UNVERIFIED`). Internal content verified self-consistent (correctly cites the real Building Act 1991 s.47A(3), the actual incorporation-by-reference mechanism). Binding maximum 1 in 12; non-binding commentary recommends 1 in 14 "wherever achievable" — captured in `claimed_unit`, not as a second extraction, to avoid implying two independently-sourced values. The standard's own RAMP/route boundary (steeper than 1:20, not steeper than 1:12) is the same boundary drawn independently by REF-01013 (OBC) and REF-01014 (ISO draft) — third jurisdiction this batch to state it without apparent cross-reference.

**REF-01017 — Finland, Government Decree 241/2017 on Accessibility of Buildings, §2(2).** First hit was the retired **F1 (2005)** regulation (`edilex.fi`); caught by a second, targeted search confirming supersession effective 1 Jan 2018 — the same TEK10/TEK17 trap as REF-01012, recognised and avoided the same way (`candidate_id=133`, `EXHAUSTED`). Retrieved from Finland's own official statute portal, Finlex (Ministry of Justice). **The current decree TIGHTENS, not loosens, the old rule**: F1 (2005) permitted 8%/1:12.5 generally (up to 6 m before a landing) and reserved 5%/1:20 for landing-free runs; 241/2017 inverts this — 5%/1:20 is now the general ceiling, and 8%/1:12.5 only a narrow exception for total height differences ≤1000 mm (continuous rise ≤500 mm before a landing). This is the strictest general ramp ceiling of any jurisdiction admitted this batch.

The claim text is Finnish-language original (Finnish and Swedish are both official enacted languages of Finnish statute; this is not an R11 back-translation). Finnish statutory prose spells cardinal numbers as words ("viisi prosenttia", "kahdeksan prosenttia") and never as digits anywhere in the text — `claimed_value` is left in that spelled-out form rather than converted to "5%", because no digit-bearing value can pass `_require_verbatim`'s digit-check for a language that never writes digits (GAP-056, below); the digit-equivalent is given only as an editorial gloss in `claimed_unit`/notes, explicitly marked non-verbatim.

## 4. GAP-056 — `_require_verbatim`'s digit-check has no path for spelled-out cardinal numbers

`scripts/db.py`'s digit-check (~line 6579) was widened in an earlier session to accept CJK numerals alongside Arabic digits, but has no equivalent for Latin-script languages that spell cardinals as words (Finnish, as encountered this session; also true of Swedish, French, German, etc. prose). A digit-bearing `claimed_value` is refused because no digit occurs in the (genuinely verbatim) claim text; `--verbatim-exempt` cannot rescue it either, because exemption is explicitly refused whenever the text DOES verify — which it does here. Worked around for REF-01017 by using the source's own spelled-out value as `claimed_value` (§3). Filed `SW/P3`. Same R5 principle ("non-English work is academic, not lesser") that motivated the original CJK fix applies here.

## 5. GAP-057 — no sanctioned path to backfill `evidence_sources.pages`/`article_number` for a non-DOI regulatory source

Discovered when six of this batch's admissions (REF-01012 through REF-01017) turned out to have been added without `--pages` (an operator omission — the flag exists at `add-source` time, and other tier≥4 rows in the corpus do carry it). `amend-source` blanket-refuses `pages`/`article_number` as bibliographic fields "not amendable by hand", directing to `correct-source` — which can only populate them from a structured citation-service payload (Crossref/PubMed-shaped JSON) that does not exist, and cannot exist, for a government regulation or standard. Net effect: once such a source is added without `--pages`, there is no sanctioned way to add one afterward, even though the real locator is known and already verified one table over, on each source's own `source_value_extractions` row (`source_section`/`loc_section`/`loc_paragraph`/`loc_clause` — all populated, all verbatim-checked). Filed `SW/P3`, with a suggested fix direction: either gate an `amend-source` path for these two fields on `evidence_type IN ('code','standard')`, or have R3 additionally accept a populated extraction-level locator as satisfying the clause-citation intent, rather than requiring a second copy of the same fact on `evidence_sources`.

## 6. R1 — a genuine, honestly-null Co-1/Co-2 pass (exec 122, 123)

Two targeted searches: a general lived-experience/DPO query (exec 122, `target_evidence_type=co1`) returned exclusively commercial ramp-vendor content (BraunAbility, RapidRamp, Adapta Ramps, Gilani Engineering, Enable Access) plus a Wikipedia article and a patent filing — no disabled-person-authored or co-produced material. A named-OT-body query (exec 123, `target_evidence_type=co2`, RCOT) surfaced RCOT's real, current "Adaptations without delay" publication — but it addresses adaptation process/delay reduction, not ramp technical specifications, and is off-point for this parameter; remaining hits were OT-sector secondary content restating figures already independently admitted this batch from primary code sources, with no distinct CPG-sourced figure of their own. Neither search was converted into an admission. This project's corpus already holds Co-1 admissions on this exact parameter from batch 9 (`session_2026-09-16-research-batch-09-ramp-gradient-co1`) — not re-run or re-admitted here, per R9.

## 7. What this session touched, derived

```
python3 -c "
import sqlite3
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
for t in ('evidence_sources','evidence_source_authors','source_slug_links','source_value_extractions',
          'evidence_population_match','search_candidates','search_executions','search_admissions',
          'citation_mining','observed_terms','research_code_leads','gaps',
          'adversarial_passes','adversarial_findings','economics_entries','search_execution_artefacts'):
    n = con.execute(f\"select count(*) from {t} where created_by_session like '%research-batch-22-selection%' or updated_by_session like '%research-batch-22-selection%'\").fetchone()[0]
    if n: print(t, n)
"
```

(At the time this section was drafted, pre-migration, against the scratch DB: `evidence_sources` 6, `evidence_source_authors` 6, `source_slug_links` 6, `source_value_extractions` 7, `evidence_population_match` 6, `search_candidates` 3, `search_executions` 18, `search_admissions` 6, `observed_terms` 6, `research_code_leads` 2, `gaps` 2, `search_execution_artefacts` 12 — re-run the query above against the committed DB after migration; do not trust this parenthetical.)

## 8. Gates

<!-- FILLED IN AFTER THE ADVERSARIAL PASS AND FINAL DoD RE-RUN -->

## 9. What the next batch takes

- Bucket 1 is now fully exhausted for this slug/parameter (UN screened-not-admitted counts as exhausted per the standing order's own definition — a logged `search_executions` row exists for every bucket-1 jurisdiction). Bucket 2 has 3 of 10 jurisdictions searched (IE, NZ, FI) — EU, SG, FR, ES, PT, NL, KR remain.
- GAP-056 (spelled-out-numeral digit-check) and GAP-057 (regulatory-source `pages` backfill) — both tooling-only fixes, ship in a separate PR per rule 10.
- `research_code_leads` 94 (ISO 21542:2011 published edition) and 95 (UNESCO 1990) — both `REFERENCE-ONLY`, not yet independently retrieved.
- Candidate 135 (UNICEF Accessibility Technical Cards) — `OUT-OF-SCOPE`, needs no further action unless a future session finds UNICEF's own originated figures elsewhere in its toolkit (`accessibilitytoolkit.unicef.org`, not the same document, not checked this session).
- Candidates 133/134 (superseded FI/IE editions) — `EXHAUSTED`, need no further action; retained only so a future session does not re-discover and re-admit them.
- REF-01013 (Ontario) and REF-01016 (NZ) both carry `GREY`/`UNVERIFIED` on non-official mirrors — a future session with different network/paywall access should attempt CSA B651 (Canada) and an official Standards NZ copy of NZS 4121 directly.
