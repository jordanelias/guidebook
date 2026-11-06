# Pipeline batch: catalogue readings of two held codes against parameters 4, 5, 6, 8, 9 and 11

**Session id:** `session_2026-11-06-pipeline-batch`
**Branch:** `ccr-f9662223-3a0e7g`
**Session kind:** research (rows only). No schema, script or check change. Tooling gaps found are listed in section 4 and not patched (CLAUDE.md rule 10).
**Pointers:** `sessions/LATEST` and `sessions/LATEST-RESEARCH` move to this session.

**Derive every figure.** Re-run the command beside a number rather than trust the sentence.

## 1. What this session did

The request was "perform a pipeline batch", with no scope. The reading taken: parameters 4 to 11 held rows from one source only (the Singapore code), and the catalogue reading owed on each admitted source (R16) had been recorded for five sources. This batch read two sources already admitted and already persisted, UK Approved Document M volume 2 (REF-00992) and the 2010 ADA Standards (REF-00987), against those parameters. No source was admitted.

- Rows: `select parameter_id, ref_id, count(*) from source_value_extractions where created_by_session = 'session_2026-11-06-pipeline-batch' group by 1, 2`.
- Parameters 7 and 10 (reverberation time, colour temperature): no value found in either source. Parameter 5: ADA 304.3.1 only. The UK text states a 1500 mm square at an entrance landing (2.7(d)) and before a lifting device (3.28(a)) but calls neither a turning space, so neither is filed on parameter 5.
- Searches: two PubMed searches for the turning-space and door-width anchors (executions 197, 198), and after the critic's report two looser shapes (199, 200). Candidates 150 to 155 are staged `PENDING-VERIFICATION` on abstracts only; none was admitted because Europe PMC reports no open full text for the two main anchors and the abstracts state no dimension. The Koontz 2010 and King 2011 DOIs are RETIRED stash rows (REF-00784, REF-00972): an admission cross-files to those ids. The Steinfeld 2010 DOI sits on two unrelated stash rows (REF-00059, REF-00192, GAP-008), so its cross-filing id is not settled.

## 2. The adversarial pass and what it changed

Pass 8, a read-only critic against commit `dd07c9df`: thirteen sustained findings, four survived, one not attacked, one withheld for the owner. Dispositions are in `adversarial_findings` (`select finding_id, lens, severity, disposition from adversarial_findings where pass_id = 8`). The substantive ones: the search that surfaced a harm statement about the US turning-space figure did not carry the flag; the first scan declared headroom and turning absent from the UK text on a keyword search that missed the figures' own spellings (2.1 m, 1.5 m); six parameter 4 and 11 figures were left unextracted; an exec 198 diagnosis named one cause and argued another. All were repaired by a second migration, except two, below.

- **Lens (finding 147), PROVISIONAL-DISPUTED.** Rows 168 to 186 carry lenses that are inconsistent across the two sources (the ADA door and turning rows are `MOB` though their clauses name no population; the UK door-force rows are `MOB` alone though para 2.9 also names limited strength, which no identity code covers). No writer changes a lens column and a second row would duplicate the figure. The lens is the reader's filing, and judgment re-keys it.
- **Gate scope (finding 153), PROVISIONAL-DISPUTED.** `research_batch_dod.py` reads neither `source_scans` nor `source_value_extractions`; COMPLIANT here examined two searches and the candidates, not the nineteen original content rows. It is cited as nothing more than that.
- **Extraction 183 (ADA 1525 mm) stays `contested = 0`.** Exec 197 now carries `harm_finding`; no writer amends `contested`, and the harm statement is an abstract-level hypothesis. Candidate 150's own `harm_finding` is 0 and no writer raises it.
- **Candidate 151's title reads "D Souza"** (the payload is `D'Souza`). No writer amends a title; the correction is on the row's note.
- **Not closed.** `close-adversarial-pass` was not run. Finding 160 is withheld for the owner (section 4).

## 3. Disclosures

- The prior on searches 197 and 198 is stated in the transcript before they ran; `log-search` wrote it with the results, so it is not independently timestamped. The priors on searches 199 and 200 were written after the critic reported their hit counts and say so.
- The scans are `pre-screen` readings of a derived text, located by keyword and by clause number; neither document was read end to end, and diagrams and figures (images) were not read. Scans 6 and 7 are superseded in part by scans 8 and 9 (same source, same mode); the notes of the later scan say what changed.
- Every extraction is `skim`, `preliminary`.
- The UK Approved Document says "For use in England" on its first pages; the rows carry `UK`, the only spelling the jurisdiction vocabulary allows.
- The new UK width and height rows in metres (1.5 m, 2.1 m) will not compose with millimetre rows from other sources until the engine owns a length family (GAP-072).
- No Co-1 retrieval for door or corridor width was done. Exec 198 is a query-shape failure and not an absence; exec 200 shows the index holds on-topic work.
- The Europe PMC checks that support "no open full text" are persisted (`retrieval-log/session_2026-11-06-pipeline-batch/198b3da3fb3d7b6a.json`, `c4c1f76df9877588.json`) but cannot be linked to exec 197: the writer requires the search's query text to name the same host.

## 4. For the owner

1. Whether an instrument for England only (the Approved Document) should be representable below `UK` in the jurisdiction vocabulary (finding 160, WITHHELD-FOR-OWNER).
2. Tooling gaps, none patched: the DoD gate does not read extractions or scans (finding 153); `amend-extraction` cannot change a lens column; no writer raises a candidate's `harm_finding` or corrects a candidate's title; `amend-search --add-result-artefact` cannot link a Europe PMC payload to a PubMed search. They are not filed as GAP rows here (a gap row ships with research rows, and these are tooling), and are named so the owner can decide which to file.
3. Full-text retrieval for the three anthropometry anchors (candidates 150 to 155): none is reachable from this environment; a library route is the owner's.
