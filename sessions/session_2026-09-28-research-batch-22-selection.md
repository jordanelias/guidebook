# Batch 22 — bucket-1/2 exhaustion for parameter 3 (ramp gradient) × MOB: Norway, Ontario, ISO, Ireland, New Zealand, Finland — and a CRITICAL misidentified source caught by an independent adversarial pass

**Session id:** `session_2026-09-28-research-batch-22-selection`
**Branch:** `claude/research-batch-apparatus-fnnd5b` (continued on the same branch as batch 21; PR #165 was still open/unmerged at session start)
**Cell:** parameter 3 (`ramp gradient`) × MOB.
**Session kind:** research, in intent — but this branch has carried Layer-0/doctrine prose (CLAUDE.md, `references/project-standards.md`) alongside research rows since at least batch 21, and this batch added more (the Wayback trap entry, the bucket-scope ruling). Named as an accepted, not-fixed-this-session rule-10 deviation (§0, finding 56), not corrected retroactively.

**Derive every figure.** Re-run the command beside a number rather than trust the sentence.

---

## 0. The independent adversarial pass, and what it found

An independent `antagonist` agent (model `claude-fable-5-1`, different from this session's `claude-sonnet-5`) reviewed the scratch DB, every persisted artefact, and the harness transcript against commit `3d1ebf3785a333067af9dcf54580347a89460966`. Full report: `transcripts/harness_360642ec/subagents/2026-09-28T20-28-42_adversarial_adbde794.jsonl`. Recorded as `pass_id=3`.

**19 SUSTAINED (2 CRITICAL, 5 HIGH, 8 MEDIUM, 4 unranked-but-real), 6 SURVIVED, 1 NOT-ATTACKED.** 10 SUSTAINED findings repaired; 9 recorded PROVISIONAL-DISPUTED with a reason (not silently accepted, and several of those ARE fixed but via a plain commit rather than a data migration — see the note at the end of this section).

### 0a. CRITICAL — REF-01015 was stamped as the 2022 edition of Ireland's TGD Part M. It is actually the 2010 edition, retired since 1 January 2024.

`add-source` wrote `pub_year=2022`, title and institution from the WebSearch result's own title ("Building Regulations Technical Guidance Document M 2022 Access and Use"), never from the retrieved payload. The persisted PDF's own title page reads "Building Regulations **2010** ... Technical Guidance Document M ... Access and Use", ISBN 978-1-4064-2317-4, copyright "© Government of Ireland **2010**", PDF metadata `creationDate D:20101110120009Z` — CLAUDE.md 5(c)'s exact shape, caught by an independent pass, not self-caught.

**Fixed:** retrieved and byte-verified the genuine 2022 edition (galway.ie mirror, 180pp, title page and copyright page checked directly), admitted it as **REF-01018** with a fresh, payload-verified extraction, population-match and term observation. REF-01015's `pub_year`/`pub_title`/`institution` **cannot be corrected by any sanctioned writer** — `amend-source` refuses them as bibliographic, `correct-source` refuses because this row has no DOI to key a payload to (the exact GAP-043 mechanism, now confirmed to reach core identity fields, not just `pages`/`article_number`). Flagged with a 1300-character correction in `evidence_sources.notes` (the one field `amend-source` can still touch) naming the true identity and pointing to REF-01018. The clause-1.1.3.4 text extraction_id=78 quoted is genuinely in the persisted 2010 PDF and was, in substance, unchanged Irish law from 2010 through the 2022 edition — the extraction is not false, only REF-01015's stated *identity* was. Candidate 134's own redescription (which had said the 2000 edition was "replaced by the 2022 edition ... admitted this batch as REF-01015") was itself now false and corrected via `resolve-candidate`.

### 0b. CRITICAL — GAP-057 was the third filing of the same defect GAP-043 already names, the second on this branch in one day.

GAP-043 (extended by batch 21 the same day) already states: a DOI-less regulatory source that omits `--pages` at admission has no sanctioned path to add it afterward, and already proposes the same two fixes GAP-057 proposed. This session filed GAP-057 without searching the gaps register first — the exact rule-5-in-the-gaps-register failure batch 21's own GAP-054 already demonstrates and names as remediated.

**Fixed:** closed GAP-057 `CLOSED-DUPLICATE`; its one genuinely new fact (six more DOI-less sources hit the same wall, not just REF-01010) folded into GAP-043 via `amend-gap`.

### 0c. HIGH — REF-01013 (Ontario) is stamped `pub_year=2024`, citing "O. Reg. 163/24", on the strength of an unverified WebSearch summary; the actual persisted artefact says it is 2012/2017 text and explicitly disclaims being current.

The persisted page (`buildingcode.online`) reads: "This is a plain-language summary of the **2012/2017** Ontario Building Code text above ... Always confirm current requirements against the **2024 edition** (O.Reg. 163/24)" — i.e. the artefact says outright it is not the 2024 text. This batch's own exec 111 flagged an identical WebSearch-summary risk and refused to use it as evidence; the same standard was not applied here.

**Fixed as far as sanctioned tools allow:** flagged via `evidence_sources.notes` (the pub_year/pub_title fields are equally unfixable, same mechanism as §0a). A CanLII retrieval attempt for the actual current consolidated regulation (O.Reg 332/12) failed (403) this session; not pursued further. REF-01013's verified content is the 2012/2017 text; the 1:12 figure stands on that, not on any confirmed 2024 text.

### 0d. HIGH — three admissions (REF-01012, REF-01013, REF-01014) had zero `search_admissions` edges; `v_coverage_jurisdiction` read NO/CA/ISO as `admitted=0` on this slug despite three real admissions.

The two-step "generic exec, then specific artefact-linking exec" pattern used throughout this batch never actually carried `--admitted-ref-id` for these three (it did for IE/NZ/FI). Since this project's own exhaustion-tracking mechanism is read off `v_coverage_jurisdiction` (per this session's own correction to its bucket-scope ruling), this actively broke the record the ruling depends on.

**Fixed:** backfilled via three new log-search execs (125, 126, 127) carrying `--admitted-ref-id`, since `link-admission` refuses without a resolved-candidate row for a direct (non-candidate-staged) admission. `v_coverage_jurisdiction` now correctly reads NO/CA/ISO/IE/NZ/FI all `admitted>=1`.

### 0e. HIGH — the population-match grade PARTIAL, applied to all six of this batch's code/standard admissions, misapplied the 2026-09-25 owner ruling and cited a precedent that does not exist.

The ruling (references/project-standards.md, point 3) is scoped explicitly to grading a **facility audit's** population match (worked example: REF-01007, a census of facilities) — it presupposes "what was measured," which a statute has no analogue for. This batch's mismatch_notes instead cited a "REF-01010 PARTIAL precedent" — **REF-01010 carries zero population-match rows in this corpus.** The actual, correctly-reasoned precedent for a code/standard source is REF-00987 (ADA), REF-00994 (IPC guide) and REF-00995 (a regional decree), all graded **PROXY**: "a standard asserts a figure, it does not study a population, so there is no population-of-study to compare against MOB."

**Fixed:** added a corrected PROXY population-match row for all seven admissions (REF-01012 through REF-01018), each explicitly naming the misapplication and the real precedent. The earlier PARTIAL rows are left in place (append-only, `evidence_population_match` enforces no uniqueness) — read the PROXY rows as the corrected grade.

### 0f. Named, not fixed this session

- **REF-01014 (ISO/CD 21542) is tiered T4 `standard_eb`**, with no distinction in the tier ladder between a 2007 committee draft ("may not be referred to as an International Standard") and a published edition. Already heavily caveated (GREY/UNVERIFIED, notes, lead 94). Whether the ladder itself should distinguish draft from published is a doctrine question, left open.
- **REF-01017 (Finland)'s Finlex page is marked "up-to-date prior to amendment 683/2024."** Checked (not independently retrieved): 683/2024 amends section 1 of the decree, not section 2 where the ramp-gradient clause sits — caveat recorded in notes, not independently confirmed.
- **`source_value_extractions` 76-79 use `--verbatim-exempt` for PDF-sourced quotes** when `record_file(kind='text-extraction')` — used later the same session for candidates 133-135 — could have produced a decodable derived artefact instead. No fabrication risk (the pass independently confirmed every quote is genuinely in the bytes); not re-derived given the marginal correctness gain.
- **A CSA B651 candidate could not be filed.** `add-candidate --surfaced-in` requires a linked result-artefact; the CSA fetch failed (403), and a derived artefact's chain traces back to that same failed retrieval and is refused too. `search_candidates` appears built for retrieved-then-screened content, not a blocked-nothing-retrieved case — a real, narrower tooling gap, not filed as a formal GAP given time. The block is recorded honestly in exec 109's findings_note.
- **This branch's rule-10 containment** (Layer-0 prose shipping alongside research rows, batches 21 and 22 both) is named, not undone.
- **extraction_id=80's `claimed_value='viisi prosenttia'`** is GAP-056's concrete shape (§4 below) — a tooling fix, not attempted here.
- Two findings turned out to be about **prose files, not database rows** (the false Wayback/CSA claim in `CLAUDE.md`, §0g below, and this section's own earlier "bucket 1 exhausted" overclaim) — fixed by direct edit, disposed as PROVISIONAL-DISPUTED on the adversarial-findings ledger only because that ledger's REPAIRED disposition requires a data-migration `--ref`, which a prose fix has none of; both are, in fact, fixed.

### 0g. MEDIUM — `CLAUDE.md` itself claimed Wayback succeeded for a Canadian standards PDF blocked by 403; every attempt this batch failed.

Six attempts, all a proxy-level connection reset (confirmed session-level via a control URL and `/__agentproxy/status`), not a Wayback-side 404. **Fixed:** corrected the `CLAUDE.md` §7 trap entry to state the CSA B651 failure accurately, keeping the genuine SciELO success (batch 21) as the positive example.

### 0h. Six SURVIVED findings (confirmed correct, no action needed)

The four owner quotations in this session's ruling text are verbatim against the harness transcript; REF-01012's TEK17 claim, REF-01014's ISO Table 2/3 values, and REF-01016's T6 tiering (tier-system.md names NZS 4121 explicitly) all held under independent re-verification; the R7 harm-finding chain on the ISO draft reached both the exec flag and the extraction row consistently; the Co-1/Co-2 pass's null result and the batch-9 precedent it cites both checked out.

---

## 1. Norway, Ontario, ISO — REF-01012, REF-01013, REF-01014

**REF-01012 — TEK17 § 12-16(2).** First hit was the retired TEK10; caught before use by the page's own "TEK10 er tidligere regelverk" notice. Tiered: general max 1:15, relaxed to 1:12 for runs under 3.0 m.

**REF-01013 — OBC 3.8.3.4(1)(b).** CSA B651 (the national standard) is Cloudflare-blocked (403); Wayback access failed with a proxy-level connection reset across every attempt (§0g). Pivoted to the Ontario Building Code, per the user's own guidance that sub-national jurisdictions may satisfy a bucket country's coverage. Retrieved via a non-governmental mirror (`buildingcode.online`) — `metadata-quality=GREY`, `verification-status=UNVERIFIED`. See §0c for the unresolved 2024-edition question. Two ramp provisions exist (§3.4.6.7 general, not accessibility-specific, vs §3.8.3.4 barrier-free) — only the latter is this parameter.

**REF-01014 — ISO/CD 21542, 2007 committee draft.** Self-declares "not an ISO International Standard." See §0f for the tier caveat. Two extractions: the numerical schedule and a qualitative R7 harm/limitation finding (the drafting committee's own rationale for the 1:12 ceiling).

## 2. UN — screened, not admitted (exec 113)

No UN-Habitat-authored instrument with an independent, quantified value was found. UNICEF's *Accessibility Technical Cards* (2022) discusses ramp gradient at length, but every quantified figure is captioned to a third party (ISO 2011, ADA 1994, UNESCO 1990, Centre for Accessible Environments/RIBA 2004) — checked 25+ figure captions, none UNICEF-original. Not admitted; filed as `candidate_id=135` (`OUT-OF-SCOPE`) and two `research_code_leads` (94: ISO 21542:2011 published edition; 95: "UNESCO 1990"). UN has no `JurisdictionCode` value; `INT` is the correct existing meta-code for genuinely cross-jurisdictional UN-system material (precedent REF-00994), not a missing "UN" code.

**Not all nine links this WebSearch returned were individually screened and recorded** (§0, finding 46) — the one substantive hit was screened thoroughly; the other eight were not re-derived after the fact.

## 3. Bucket-2 sweep — REF-01015/REF-01018 (Ireland), REF-01016 (New Zealand), REF-01017 (Finland)

See §0a for REF-01015/REF-01018. **REF-01016 — NZS 4121:2001 clause 6.4.2.2**, a purchased Standards NZ document retrieved only via a non-official archive.org mirror (`metadata-quality=GREY`). Binding max 1 in 12; commentary recommends 1 in 14 "wherever achievable." **REF-01017 — Finland Decree 241/2017 §2(2).** First hit was the retired F1 (2005); caught by a second search confirming supersession (1 Jan 2018) — the current decree **tightens** the old rule (5%/1:20 general with an 8%/1:12.5 narrow exception, inverting F1's own default/exception shape). Finnish-original claim text (`claimed_value` is left as the source's own spelled-out cardinal, "viisi prosenttia" — see §4, GAP-056). See §0f for the 683/2024 currency caveat.

`FI` **has no `JurisdictionCode` value**, alongside `UN` — written into `evidence_sources`, `search_executions` and `source_value_extractions` this batch. `jurisdiction_db_vocabulary` reports this class `REPORTED (not blocking — owner decision)`, the same treatment as Uganda in batch 21 (§7a there). **Not caught when checking the enum for UN** — the earlier check should have cross-referenced the whole bucket-1/2 list, not just the jurisdiction being admitted at that moment. Left to the owner alongside Uganda's open question: admit `FI` (a bucket-2 member the owner's own ruling names) to the 24/32-code enum, or accept the vocabulary check's non-blocking treatment as sufficient.

## 4. GAP-056 — `_require_verbatim`'s digit-check has no path for spelled-out cardinal numbers

`scripts/db.py`'s digit-check was widened for CJK numerals but not for Latin-script languages that spell cardinals as words (Finnish "viisi prosenttia," also true of Swedish, French, German prose). A digit-bearing `claimed_value` is refused because no digit occurs in the verbatim text; `--verbatim-exempt` cannot rescue it because exemption is refused whenever the text DOES verify. Worked around for REF-01017 by using the source's own spelled-out value as `claimed_value`. `SW/P3`.

## 5. R1 — a genuine, honestly-null Co-1/Co-2 pass (exec 122, 123)

A general lived-experience query returned exclusively commercial ramp-vendor content; a named-OT-body query (RCOT) surfaced a real but off-point publication (adaptation process delays, not ramp specifications). Neither converted to an admission. The corpus already holds Co-1 admissions on this exact parameter from batch 9 (REF-00989) — not re-run here, per R9.

## 6. What this session touched, derived

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

Two data migrations: `data_20260928210349_2026-09-28-research-batch-22-selection.sql` (the substantive batch plus the adversarial-pass recording — 129 inserts, 1 update) and a second, following this file's own commit, for the finding disposals and pass closure.

## 7. Gates

`research_batch_dod.py --session session_2026-09-28-research-batch-22-selection` — **NON-COMPLIANT: 1 rule** (R3 — pages/article_number unset on seven regulatory sources, GAP-043's exact mechanism, reasoned waiver). Every other rule PASS. `jurisdiction_db_vocabulary` — `FAIL`, all `REPORTED`/non-blocking (`FI`, `UN`, plus batch 21's pre-existing `UG`) — owner decision, not remediated (§3). `adversarial_pass_audit` — pass recorded and closed (§0).

Two reasoned waivers ship in this PR: R3 (seven sources' `pages`, GAP-043) and the jurisdiction vocabulary (`FI`/`UN`, alongside batch 21's `UG`). Both are owner-decision items this session is not authorised to resolve, not corners cut on the research itself.

## 8. What the next batch takes

- **Whether `FI` (and Uganda's `UG`) join the jurisdiction enum**, or the vocabulary check gains a formal non-blocking exemption path — owner call, alongside batch 21's §7a.
- Bucket 1 is searched for every member on this slug (UN screened-not-admitted, NO/CA/ISO/AU/SE/DE all carry at least one logged search) — **but "exhausted" should be verified against `v_coverage_jurisdiction` directly before the next batch assumes it**, not inferred from this file's prose (an earlier draft of this section overclaimed full exhaustion; corrected).
- Bucket 2 has IE, NZ, FI searched; EU, SG, FR, ES, PT, NL, KR remain.
- GAP-043 (extended again) and GAP-056 — both tooling-only fixes, ship in a separate PR per rule 10.
- `research_code_leads` 94 (ISO 21542:2011 published) and 95 (UNESCO 1990) — `REFERENCE-ONLY`.
- A future session with different network/paywall access should attempt CSA B651 (Canada), an official Standards NZ copy of NZS 4121, and Ontario's actual current O.Reg 332/12/163-24 text directly — none of REF-01013/01016's underlying "current edition" claims are independently confirmed.
- Candidates 133/134/135 — `OUT-OF-SCOPE`, need no further action.
