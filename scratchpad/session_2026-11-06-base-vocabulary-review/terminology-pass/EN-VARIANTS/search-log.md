# Search log — terminology pass EN-VARIANTS (English register vs other English-language jurisdictions), session_2026-11-06-base-vocabulary-review

Each entry: query verbatim; prior expectation (written before the result); result; note on query shape (R14). Empties kept.

## B1. Base: held texts (derivation, not search)
- Query: `select ref_id, pub_title, standard_number, jurisdiction, url from evidence_sources where jurisdiction in ('US','UK','GB','AU','IE','NZ','SG')`, then a scan of every `retrieval-log/*/manifest.jsonl` for the URLs/ref_ids.
- Expectation: REF-00987, REF-00992, REF-00139 held; probably nothing for AU/NZ/IE.
- Result: all three held (sha a2f0dc7a…, 0e5d4dee…, 846c3044…). Also held, unexpectedly: IE TGD M 2022 (REF-01018, e6042db0…; REF-01015 was an earlier mis-admission the batch-22 record corrects), NZS 4121:2001 (REF-01016, archive.org mirror), and NCC 2022 Vol. 2 Part H8 (AU, housing). No AU Premises Standards and no NZ D1/AS1.
- Shape: the base lists sources admitted for ramp work, not instruments for terminology; the instrument list is therefore only partly derivable (same as FR D7).

## W1. AU Premises Standards
- Query (WebSearch): `Disability (Access to Premises — Buildings) Standards 2010 legislation.gov.au`
- Expectation: a legislation.gov.au compilation in PDF; a 2024 amendment possible.
- Result: Compilation No. 3 (2024-11-23, F2024C01272) found; retrieved 200 (7aab78bf…).
- Shape: exact title query; good.

## W2. NZ D1/AS1
- Query (WebSearch): `building.govt.nz D1 Access routes acceptable solution D1/AS1 PDF`
- Expectation: D1/AS1 PDF on building.govt.nz, possibly bot-blocked.
- Result: amd 6 (effective 1 Jan 2017) located. Direct fetch of PDF and of the listing page both returned the same 212-byte Incapsula JavaScript shell (d0203228…). The codehub "generated PDF" (904704e0…) is only the catalogue page. Wayback availability API gave snapshot 20261022090808; the `if_` form returned the 2.2 MB PDF (02132b6a…).
- Shape: the publisher block is a JS shell with HTTP 200, so a status check alone would have called it a success.

## W3. IE TGD M currency
- Query (WebSearch): `Technical Guidance Document M Access and Use 2022 gov.ie current edition`
- Expectation: 2022 edition current; a Changing Places amendment possible.
- Result: gov.ie lists the 2022 edition as "Current Edition"; a public consultation on Changing Places is noted but no newer edition was seen. Held copy is a Galway council mirror, not gov.ie bytes [UNVERIFIED identical].
- Shape: currency query only; no new retrieval.

## W4. AS 1428.1
- Query (WebSearch): `AS 1428.1:2021 Design for access and mobility Standards Australia store price`
- Expectation: sale only.
- Result: sale only (HIA non-member AUD 278; Standards Australia store listing "Current", sixth edition 2021). Results also showed third-party PDF mirrors of unknown provenance; not used. NOT-OBTAINABLE.

## L1. Reading-order locators (scripts, then reading)
- US: chapter offsets located by string search over the stripped HTML (`tools/h2t.py`); ch.2, ch.8, ch.10 and the DOJ text were grep-located for: microwave, locker, restroom, washroom, lift, kerb, reverberat, lux, luminance, reflectance, color, shelter, lavator, kitchen, storage, maneuvering, curb, acoustic, path of travel, elevator. Expectation: 'restroom' and 'path of travel' in the DOJ text. Result: 'restroom' 14 hits and 'path of travel' 40 hits, all in the DOJ regulation; 'microwave' 0; 'washroom' 0; 'kerb' 0.
- IE: term counts over the text layer (kerb 1, curb 0, washroom 0, restroom 0, lift 61, manoeuvr 9, maneuver 0, accessible route 0, approach route 4, gradient 35, Changing Places 33, reverberat 0, LRV 7, effective clear width 13). PyMuPDF confirms many near-empty pages (page 41: 459 chars, one image): provision lists are not in the text layer.
- B651-only headings, all six texts (whitespace-normalised, case-insensitive): microwave 0, speed bump/hump 0, planter 0, guy wire 0, gradation 0; landscap 2 (US 242.2 advisory, IE 1.1.3.5), vegetation 1 (US fishing piers), scaffold 1 (US 203.2 exemption).

## A1. Held English aliases (seeds) against the six texts
- Query: `select distinct alias, jurisdiction from term_aliases where lower(language)='en'`, each lower-cased and tested with `in` against the whitespace-collapsed lower-cased texts.
- Expectation: most aliases are generic English; jurisdiction tags mostly right.
- Result: 411 distinct (alias, jurisdiction) pairs; 93 occur in at least one text. 13 carry a jurisdiction (AU, UK, US). In own jurisdiction: yes for tactile ground surface indicator (AU), grab rail (UK), passenger lift (UK), tactile paving (UK), detectable warning surface (US), maneuvering clearance (US), truncated dome (US). No for beacon alarm, disabled parking, inclusive design, live subtitling (UK), accessible elevator, handicapped parking (US). 'passenger lift' (tagged UK) also occurs in AU, SG and IE; 'truncated dome' (tagged US) also in SG; 'tactile ground surface indicator' (AU) also in SG. The tags are too narrow and, for six aliases, unattested.
