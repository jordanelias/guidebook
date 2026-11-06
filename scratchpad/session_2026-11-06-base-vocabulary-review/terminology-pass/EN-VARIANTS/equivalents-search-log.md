# Equivalents search log: EN-VARIANTS, session_2026-11-06-base-vocabulary-review

Second pass (equivalence-class discovery). Each FETCH entry's prior line is appended by the same command before `retrieval_log.fetch()` runs; the Result line is appended after. Tier-1 entries are greps over the first pass's saved texts (`text/<sha12>.txt`). Interpretations of each result are recorded under "Reading" after the fact and say so.

## Tier 1: second reading of the six instruments already held (greps over text/)
- Prior (written before the greps): parking forms will be "accessible parking space(s)" in the US, "parking bay designated for disabled people" in the UK, "accessible parking lot" in SG, "accessible carparking space" in AU, "designated car parking space" in IE, little in NZ D1/AS1 (delegates to NZS 4121); no "handicapped" anywhere; "elevator" only in US.
- Query: case-insensitive regex counts per text for: accessible parking, handicap, disabled parking, disabled person, barrier[- ]free, blue badge, badge, accessibility parking, mobility parking, designated (accessible )?(parking|bay|space), parking (bay|space|lot|stall)s?, car park, elevator, \blifts?\b, inclusive, universal, wheelchair[- ]friendly, wheelchair[- ]accessible, stair ?lift, restroom, washroom, toilet, disabled people, people with disabilit, persons with disabilit, impair.
- Result: US accessible parking 7, elevator 111, lift 67, handicap 0, wheelchair-accessible 11; UK car park 19, parking bay 12, lift 55, elevator 0, inclusive 7, universal 3, disabled people 41; SG accessible parking 5, handicap 2 (both organisation names), barrier-free 3, lift 98, elevator 0; AU parking 28 (as "carparking"), lift 90, elevator 0; NZ car park 6, lift 7; IE designated parking 3, disabled person 5, universal 17, lift 38, elevator 0. "blue badge", "wheelchair friendly", "accessibility parking", "mobility parking", "barrier free parking" 0 in all six.
- Shape: counts only; every row entered in equivalents.tsv was then read in context with page and line (helper prints pdftotext page by form-feed count; the US text is HTML with no pages, so its locator is the section number).

### FETCH 19:56:48 UTC
- URL: https://www.gov.uk/apply-blue-badge
- Purpose: UK tier 4 public service page, Blue Badge
- Prior (written before fetch): Blue Badge as the permit name; 'disabled parking' or 'disabled parking bays' possible; no 'handicapped'
- Shape: direct URL from memory of gov.uk service path
- Result: status 200, 70764 bytes, sha256 0f0826b58ed20ce2, artefact 0f0826b58ed20ce2.html, text 5633 chars -> text/eq-0f0826b58ed2.txt

### FETCH 19:56:49 UTC
- URL: https://www.legislation.gov.uk/uksi/2000/682/made
- Purpose: UK tier 2 statute, Disabled Persons (Badges for Motor Vehicles) (England) Regulations 2000
- Prior (written before fetch): 'disabled person's badge' as the statutory form; 'Blue Badge' probably absent from the 2000 text
- Shape: direct legislation.gov.uk ELI path
- Result: status 200, 77633 bytes, sha256 ea6351aae5e4a04e, artefact ea6351aae5e4a04e.html, text 30703 chars -> text/eq-ea6351aae5e4.txt

### FETCH 19:56:49 UTC
- URL: https://www.irishstatutebook.ie/eli/1997/si/182/made/en/print
- Purpose: IE tier 2 statute, Road Traffic (Traffic and Parking) Regulations 1997
- Prior (written before fetch): 'disabled person's parking bay' and 'disabled person's parking permit'
- Shape: direct ELI print path
- Result: status 200, 126729 bytes, sha256 f92c0d22786813cc, artefact f92c0d22786813cc.html, text 51595 chars -> text/eq-f92c0d227868.txt

### FETCH 19:56:50 UTC
- URL: https://www.access-board.gov/ada/guides/chapter-5-parking/
- Purpose: US tier 4 public-body guidance, US Access Board guide to parking
- Prior (written before fetch): 'accessible parking spaces', 'van-accessible', 'access aisle'; maybe mention of 'handicapped' signs absent
- Shape: direct URL from memory
- Result: status 200, 80830 bytes, sha256 68cdbb4e2cbae537, artefact 68cdbb4e2cbae537.html, text 29816 chars -> text/eq-68cdbb4e2cba.txt

### FETCH 19:56:51 UTC
- URL: https://mutcd.fhwa.dot.gov/htm/2009/part2/part2b.htm
- Purpose: US tier 3 signage manual, MUTCD 2009 Part 2B
- Prior (written before fetch): R7-8 'RESERVED PARKING' with the International Symbol of Accessibility; possibly 'persons with disabilities'
- Shape: direct HTML path; 2009 edition, superseded by the 11th edition (2023)
- Result: status 200, 371304 bytes, sha256 a8f3e3a8ff0989b2, artefact a8f3e3a8ff0989b2.html, text 139057 chars -> text/eq-a8f3e3a8ff09.txt

### FETCH 19:56:52 UTC
- URL: https://www.dmv.ca.gov/portal/vehicle-registration/disabled-person-parking-placards-plates/
- Purpose: US-CA tier 4 public service page, California DMV
- Prior (written before fetch): 'Disabled Person Parking Placards' and 'disabled person parking'
- Shape: direct URL from memory
- Result: status 200, 101579 bytes, sha256 70930685b8c5dd60, artefact 70930685b8c5dd60.html, text 15707 chars -> text/eq-70930685b8c5.txt

### FETCH 19:56:53 UTC
- URL: https://www.nysenate.gov/legislation/laws/VAT/1203-B
- Purpose: US-NY tier 2 statute, Vehicle and Traffic Law 1203-B
- Prior (written before fetch): 'handicapped parking' or 'parking for persons with disabilities' in New York law
- Shape: direct URL; section number from memory, may be wrong
- Result: status 200, 34406 bytes, sha256 6091a31d4d5cff9c, artefact 6091a31d4d5cff9c.html, text 2661 chars -> text/eq-6091a31d4d5c.txt

### FETCH 19:56:53 UTC
- URL: https://www.txdmv.gov/motorists/disabled-parking-placards
- Purpose: US-TX tier 4 public service page, TxDMV
- Prior (written before fetch): 'disabled parking placards'
- Shape: direct URL from memory
- Result: status 404, 130202 bytes, sha256 a973a22e5cb2f0e1, artefact a973a22e5cb2f0e1.xml, text 7439 chars -> text/eq-a973a22e5cb2.txt

### FETCH 19:57:17 UTC
- URL: https://www.infrastructure.gov.au/infrastructure-transport-vehicles/transport-accessibility/australian-disability-parking-scheme
- Purpose: AU tier 4 public-body page, Australian Disability Parking Scheme
- Prior (written before fetch): 'disability parking permit' and 'Australian Disability Parking Scheme'; perhaps 'accessible parking'
- Shape: direct URL from memory of the department path
- Result: status None, 0 bytes, sha256 e3b0c44298fc1c14, artefact e3b0c44298fc1c14.txt, text 0 chars -> text/eq-e3b0c44298fc.txt

### FETCH 19:57:17 UTC
- URL: https://www.service.nsw.gov.au/transaction/apply-for-a-mobility-parking-scheme-permit
- Purpose: AU-NSW tier 4 service page, Mobility Parking Scheme
- Prior (written before fetch): 'Mobility Parking Scheme permit', 'mobility parking spaces'
- Shape: direct URL from memory
- Result: status 404, 11028 bytes, sha256 b294570e4646f738, artefact b294570e4646f738.html, text 297 chars -> text/eq-b294570e4646.txt

### FETCH 19:57:19 UTC
- URL: https://www.ccsdisabilityaction.org.nz/mobility-parking
- Purpose: NZ tier 5 DPO/disability organisation page, CCS Disability Action Mobility Parking
- Prior (written before fetch): 'mobility parking permit', 'mobility parks'
- Shape: direct URL from memory
- Result: status 200, 392337 bytes, sha256 3d6e27e8be13c982, artefact 3d6e27e8be13c982.html, text 15025 chars -> text/eq-3d6e27e8be13.txt

### FETCH 19:57:19 UTC
- URL: https://at.govt.nz/driving-parking/parking-permits/mobility-parking
- Purpose: NZ-AUK tier 4 transport operator page, Auckland Transport mobility parking
- Prior (written before fetch): 'mobility parking', 'mobility parking spaces'
- Shape: direct URL guessed from site structure
- Result: status 404, 1147875 bytes, sha256 21ca294ebfd35728, artefact 21ca294ebfd35728.html, text 70353 chars -> text/eq-21ca294ebfd3.txt

### FETCH 19:57:23 UTC
- URL: https://www.ontario.ca/page/get-accessible-parking-permit
- Purpose: CA-ON tier 4 public service page, ServiceOntario Accessible Parking Permit
- Prior (written before fetch): 'Accessible Parking Permit', 'accessible parking space'
- Shape: direct URL from memory
- Result: status 200, 132390 bytes, sha256 1afbf8bfed40d98d, artefact 1afbf8bfed40d98d.html, text 23019 chars -> text/eq-1afbf8bfed40.txt

### FETCH 19:57:23 UTC
- URL: https://www.ontario.ca/laws/regulation/900581
- Purpose: CA-ON tier 2 regulation, R.R.O. 1990 Reg. 581 under the Highway Traffic Act
- Prior (written before fetch): title 'Accessible Parking for Persons with Disabilities'; earlier 'disabled person parking permit' wording in history
- Shape: direct e-Laws URL; page may be a JS shell
- Result: status 200, 34264 bytes, sha256 5f9b8b544c8f1753, artefact 5f9b8b544c8f1753.html, text 20256 chars -> text/eq-5f9b8b544c8f.txt

### FETCH 19:57:23 UTC
- URL: https://www.sparc.bc.ca/our-work/parking-permits/
- Purpose: CA-BC tier 4/5 permit administrator page, SPARC BC
- Prior (written before fetch): 'parking permit program for people with disabilities', 'accessible parking'
- Shape: direct URL guessed
- Result: status 406, 300 bytes, sha256 8970d3ea60596066, artefact 8970d3ea60596066.html, text 235 chars -> text/eq-8970d3ea6059.txt

## Web searches (WebSearch tool, US-indexed engine); priors written before the searches ran
- S1 query `Australian Road Rules rule 203 "parking area for people with disabilities"`. Prior: the model road rules and a state copy (NSW legislation) use "parking area for people with disabilities" and "disability parking permit".
- S2 query `Singapore accessible parking lots car park label scheme persons with disabilities LTA`. Prior: an LTA or HDB page with "Car Park Label", "accessible parking lots", perhaps "handicapped lots" on older pages.
- S3 query `"Know your traffic signs" pdf disabled badge holders only`. Prior: the DfT booklet shows "Disabled badge holders only" and "Blue Badge" signs.
- S4 query `Scope disability language guide "handicapped"`. Prior: Scope (a UK disabled people's organisation) lists "handicapped" as a word to avoid.
- S5 query `CSA B355 platform lifts and stair lifts for barrier-free access`. Prior: CSA store title "Platform lifts and stair lifts for barrier-free access" (Canadian product standard).
- S6 query `ADA National Network guidelines writing about people with disabilities handicapped`. Prior: a public-body factsheet saying "handicapped" is outdated and "accessible parking" is preferred.

### FETCH 19:58:13 UTC
- URL: https://www.legislation.wa.gov.au/legislation/prod/filestore.nsf/FileURL/mrdoc_42731.htm/$FILE/Local%20Government%20(Parking%20for%20People%20with%20Disabilities)%20Regulations%202014%20-%20%5B00-c0-00%5D.html
- Purpose: AU-WA tier 2 regulation, Local Government (Parking for People with Disabilities) Regulations 2014
- Prior (written before fetch): 'parking for people with disabilities', 'ACROD' permit naming possible, 'disability parking permit'
- Shape: URL from search S1
- Result: status 200, 121791 bytes, sha256 1a252efe5202f1a9, artefact 1a252efe5202f1a9.html, text 5996 chars -> text/eq-1a252efe5202.txt

### FETCH 19:58:15 UTC
- URL: https://www.darwin.nt.gov.au/sites/default/files/page/file/Disability%20Parking%20Permits.pdf
- Purpose: AU-NT tier 4 municipal page, City of Darwin Disability Parking Permits
- Prior (written before fetch): 'disability parking permit', 'disabled parking bays'
- Shape: URL from search S1
- Result: status 200, 278213 bytes, sha256 fc24ec8b34a056c4, artefact fc24ec8b34a056c4.pdf, text 2639 chars -> text/eq-fc24ec8b34a0.txt

### FETCH 19:58:18 UTC
- URL: https://www.enablingguide.sg/im-looking-for-disability-support/transport/car-park-label-scheme
- Purpose: SG tier 4 public-body page, SG Enable Enabling Guide, Car Park Label Scheme
- Prior (written before fetch): 'accessible parking lots', 'Car Park Label'; maybe 'handicapped lots' absent
- Shape: URL from search S2
- Result: status 200, 111126 bytes, sha256 f087e6f007f515a9, artefact f087e6f007f515a9.html, text 11369 chars -> text/eq-f087e6f007f5.txt

### FETCH 19:58:20 UTC
- URL: https://msf.gov.sg/media-room/article/Number-of-applications-received-for-HDB-season-parking-for-disabled-car-park-lots
- Purpose: SG tier 4 ministry page, MSF reply on HDB season parking for disabled car park lots
- Prior (written before fetch): 'disabled car park lots' and 'accessible car park lots' both
- Shape: URL from search S2
- Result: status 200, 128815 bytes, sha256 1b4445080240fc99, artefact 1b4445080240fc99.html, text 2728 chars -> text/eq-1b4445080240.txt

### FETCH 19:58:23 UTC
- URL: https://www.gov.uk/government/publications/know-your-traffic-signs/on-street-parking-control-signs-and-road-markings
- Purpose: UK tier 3 signage guide, Know Your Traffic Signs (DfT)
- Prior (written before fetch): 'disabled badge holders only', 'Blue Badge'
- Shape: URL from search S3
- Result: status 200, 191941 bytes, sha256 91e6b01f121a56b7, artefact 91e6b01f121a56b7.html, text 33675 chars -> text/eq-91e6b01f121a.txt

### FETCH 19:58:24 UTC
- URL: https://www.infrastructure-ni.gov.uk/publications/disabled-badge-holders-only-all-times-sign
- Purpose: UK-NIR tier 3 signage page, DfI Northern Ireland
- Prior (written before fetch): 'Disabled Badge Holders Only At All Times' sign
- Shape: URL from search S3
- Result: status 200, 34068 bytes, sha256 7022a5b345d8f0b0, artefact 7022a5b345d8f0b0.html, text 1803 chars -> text/eq-7022a5b345d8.txt

### FETCH 19:58:25 UTC
- URL: https://www.northumberland.gov.uk/NorthumberlandCountyCouncil/media/About-the-Council/equality/Language-Disability.pdf
- Purpose: UK tier 4 municipal language guidance, Northumberland County Council
- Prior (written before fetch): 'handicapped' listed as a term to avoid; 'disabled people' preferred (social model)
- Shape: URL from search S4
- Result: status 200, 178041 bytes, sha256 93a4dca2e6a63393, artefact 93a4dca2e6a63393.pdf, text 4651 chars -> text/eq-93a4dca2e6a6.txt

### FETCH 19:58:26 UTC
- URL: https://adata.org/factsheet/ADANN-writing
- Purpose: US tier 4 federally funded network factsheet, ADA National Network writing guidelines
- Prior (written before fetch): 'handicapped' listed under Don't use; 'accessible parking' recommended
- Shape: URL from search S6
- Result: status 200, 45809 bytes, sha256 50a9025a245a9a7d, artefact 50a9025a245a9a7d.html, text 8579 chars -> text/eq-50a9025a245a.txt

### FETCH 19:58:28 UTC
- URL: https://scc-ccn.ca/standardsdb/standards/4033416
- Purpose: CA tier 4 standards-body database page, CSA B355:24 title
- Prior (written before fetch): title 'Platform lifts and stair lifts for barrier-free access'
- Shape: URL from search S5
- Result: status 403, 5434 bytes, sha256 1802e07d0c34010e, artefact 1802e07d0c34010e.html, text 18 chars -> text/eq-1802e07d0c34.txt

### FETCH 19:58:28 UTC
- URL: https://laws-lois.justice.gc.ca/eng/acts/A-0.6/FullText.html
- Purpose: CA tier 2 federal statute, Accessible Canada Act
- Prior (written before fetch): long title 'An Act to ensure a barrier-free Canada'; defines 'barrier' and 'disability'; uses 'accessible'
- Shape: direct Justice Laws full-text path from memory
- Result: status 200, 302145 bytes, sha256 38e031a479bb9beb, artefact 38e031a479bb9beb.html, text 156022 chars -> text/eq-38e031a479bb.txt

### FETCH 19:58:28 UTC
- URL: https://www.ontario.ca/laws/regulation/010209
- Purpose: CA-ON tier 2 regulation, O. Reg. 209/01 Elevating Devices
- Prior (written before fetch): 'elevating device', 'elevator', 'lifts for persons with physical disabilities' referencing CSA B355
- Shape: direct e-Laws URL from memory
- Result: status 200, 106873 bytes, sha256 b2acf7df9b4f0b43, artefact b2acf7df9b4f0b43.html, text 71228 chars -> text/eq-b2acf7df9b4f.txt
- S7 query `"wheelchair friendly" council accessible toilets parking site:gov.au OR site:govt.nz`. Prior: a few council pages use "wheelchair friendly" for venues or paths, rarely for parking; may return nothing official.

### FETCH 20:00:11 UTC
- URL: https://www.orderline.com/default/csa-b355-24-national-standard-of-canada-platform-lifts-and-stair-lifts-for-barrier-free-access
- Purpose: CA tier 4 reseller listing of CSA B355:24 (title only), after SCC returned 403
- Prior (written before fetch): title 'Platform lifts and stair lifts for barrier-free access'; former title 'Lifts for persons with physical disabilities' possibly in description
- Shape: URL from search S5; reseller, used only for the title as written
- Result: status 403, 5788 bytes, sha256 dc41f41dbcc2abdc, artefact dc41f41dbcc2abdc.html, text 18 chars -> text/eq-dc41f41dbcc2.txt

### FETCH 20:00:28 UTC
- URL: https://www.bellingen.nsw.gov.au/Community/Community-Support/People-with-Disability/Accessible-Services-Information-and-Features
- Purpose: AU-NSW tier 4 municipal page, Bellingen Shire Council
- Prior (written before fetch): 'wheelchair-friendly paths' and 'designated parking spaces'
- Shape: URL from search S7
- Result: status 200, 117070 bytes, sha256 32a36a2ae646e4d2, artefact 32a36a2ae646e4d2.html, text 21068 chars -> text/eq-32a36a2ae646.txt

### FETCH 20:00:30 UTC
- URL: https://libraries.darebin.vic.gov.au/services/accessibility/accessible-facilities
- Purpose: AU-VIC tier 4 public library page, Darebin Libraries
- Prior (written before fetch): 'accessibility parking' and 'accessible toilets'
- Shape: URL from search S7
- Result: status 200, 91125 bytes, sha256 68abbbf5f3803634, artefact 68abbbf5f3803634.html, text 5917 chars -> text/eq-68abbbf5f380.txt

### FETCH 20:00:32 UTC
- URL: https://www.gleneira.vic.gov.au/services/disability-and-accessibility/disability-access-and-getting-around
- Purpose: AU-VIC tier 4 municipal page, Glen Eira City Council
- Prior (written before fetch): 'disabled parking spaces', 'Accessible Parking Permit' (Victoria)
- Shape: URL from search S7
- Result: status 200, 91620 bytes, sha256 86e1882bd6390c65, artefact 86e1882bd6390c65.html, text 3425 chars -> text/eq-86e1882bd639.txt

### FETCH 20:00:34 UTC
- URL: https://www.auckland.ac.nz/en/about-us/about-the-university/equity-diversity-inclusion/facilities-spaces/accessible-spaces-parking.html
- Purpose: NZ tier 4 public-institution page, University of Auckland accessible spaces and car parking
- Prior (written before fetch): 'mobility friendly car parks', 'mobility parking', 'accessible toilets', maybe 'lift'
- Shape: URL from search S7
- Result: status 200, 203288 bytes, sha256 9fe9bbe69d881009, artefact 9fe9bbe69d881009.html, text 13243 chars -> text/eq-9fe9bbe69d88.txt
- S8 query `"barrier-free parking" by-law city Canada`. Prior: Ontario or Alberta municipal by-laws or design standards use "barrier-free parking space(s)", the pre-AODA Ontario usage.

### FETCH 20:00:56 UTC
- URL: https://www.toronto.ca/zoning/bylaw%5Famendments/ZBL_NewProvision_Chapter200_15.htm
- Purpose: CA-ON tier 2/4 municipal zoning by-law, City of Toronto By-law 569-2013 s. 200.15 (accessible parking)
- Prior (written before fetch): 'accessible parking space' with 'accessible barrier free aisle'; both qualifiers in one clause
- Shape: URL from search S8
- Result: status 200, 57863 bytes, sha256 34259fb864c27a24, artefact 34259fb864c27a24.html, text 21109 chars -> text/eq-34259fb864c2.txt

### FETCH 20:00:57 UTC
- URL: https://saultstemarie.ca/wp-content/uploads/2025/10/Zoning_ParkingAmendments_PKG.pdf
- Purpose: CA-ON tier 4 municipal zoning amendment package, Sault Ste. Marie
- Prior (written before fetch): 'barrier-free parking spaces' as the zoning term
- Shape: URL from search S8
- Result: status 200, 681328 bytes, sha256 5a26f5582faea7e2, artefact 5a26f5582faea7e2.pdf, text 41050 chars -> text/eq-5a26f5582fae.txt

## Readings (written after the results, and marked as such)
- Search results S1–S8 returned URLs only; no form was taken from a search snippet. Every form in `equivalents.tsv` comes from a fetched text (`text/eq-<sha12>.txt`) or a first-pass text, and `python3 -I equivalents-build.py` re-verifies every quote (whitespace-collapsed) and exits 1 on a miss.
- Failed or empty fetches, kept: Australian Disability Parking Scheme page (status None, 0 bytes); Service NSW Mobility Parking Scheme (404, URL guessed); Auckland Transport mobility parking (404, URL guessed); TxDMV disabled parking placards (404, URL guessed); SPARC BC (406, bot refusal); SCC standards database CSA B355:24 (403) and Orderline reseller listing (403). The CSA B355 title "Platform lifts and stair lifts for barrier-free access" is therefore NOT attested here; it appears only in search snippets (S5), which are not attestation.
- Priors versus results: NY statute used "handicapped" as expected (prior said "handicapped parking" or "persons with disabilities"; it is the former). MUTCD 2009 legend "RESERVED PARKING for persons with disabilities" matched the prior. UK SI 2000/682 as made does not use "Blue Badge" (prior right); GOV.UK does. "accessibility parking" (owner form) was attested only on one Victorian library page; "wheelchair friendly" only on one NSW council page; "barrier-free parking" only in an Ontario municipal zoning package and, stacked with "accessible", in Toronto's by-law. Northumberland's guidance listing "people with disabilities" under Avoid was not predicted.
- Query shape: direct URLs from memory failed 5 of 17 (guessed paths and one bot refusal); search-derived URLs failed 2 of 16 (both standards-store pages, 403). Count: `grep -c "^### FETCH" equivalents-search-log.md`.
