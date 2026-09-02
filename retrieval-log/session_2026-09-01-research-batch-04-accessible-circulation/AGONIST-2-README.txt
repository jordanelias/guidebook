AGONIST-2 (T1/T2 academic pass) retrieval payloads.
Session: session_2026-09-01-research-batch-04-accessible-circulation
Every bibliographic field in scratchpad/.../agonist-2/BRIEF.md traces to a file here.

THIS DIRECTORY IS SHARED WITH AGONIST-1 (the Co-1 / T2-advocacy / Co-2 pass), which is writing
into it concurrently. AGONIST-2 wrote only these files:
  crossref_10.1007_s10694-025-01740-y.json      crossref_10.1080_17483107.2026.2716524.json
  crossref_10.1016_j.ajem.2025.10.042.json      crossref_10.1155_2019_9717208.json
  crossref_10.1016_j.apergo.2006.04.023.json    crossref_10.1177_0361198118787082.json
  crossref_10.1016_j.apmr.2019.03.017.json      crossref_10.1186_s12984-016-0128-7.json
  crossref_10.1016_j.cities.2025.106220.json    crossref_10.1371_journal.pone.0269657.json
  crossref_10.1016_j.jelekin.2013.06.009.json   crossref_10.3130_aija.84.1779.json
  crossref_10.1016_j.jobe.2022.104643.json      crossref_10.3141_2145-08.json
  crossref_10.1038_s41598-022-18142-7.json      crossref_10.7224_1537-2073.2020-128.json
  crossref_10.1080_10803548.2019.1567974.json   crossref_query_turning-footprint.json
  crossref_10.1080_17483100802542603.json       doaj_geoerg.json
  europepmc_10.1016_j.apergo.2006.04.023.json   europepmc_scirep.json
  unpaywall_10.1155_2019_9717208.json           s2_* (the 7 listed below)
  s2_10.1007_s10694-025-01740-y.json  s2_10.1016_j.ajem.2025.10.042.json
  s2_10.1016_j.apergo.2006.04.023.json  s2_10.1016_j.cities.2025.106220.json
  s2_10.1016_j.jobe.2022.104643.json  s2_10.1080_17483107.2026.2716524.json
  s2_10.1155_2019_9717208.json
  ERROR-NOT-A-SOURCE_guessed-doi_10.1016_j.ajem.2025.09.049.json
  BLOCKED-403_geoerg2019_not-a-pdf.html

TWO FILES THAT ARE NOT SOURCES AND MUST NOT BE READ AS ONES:

ERROR-NOT-A-SOURCE_guessed-doi_10.1016_j.ajem.2025.09.049.json
  I constructed this DOI from memory while reaching for Shapovalov et al. 2025 (automatic-door
  trauma). It resolved cleanly to a DIFFERENT paper (Brown et al., point-of-care ultrasound in
  the ED). Retained deliberately as evidence of the error. The correct identifier, obtained via
  PubMed PMID 41192188, is 10.1016/j.ajem.2025.10.042 -> crossref_10.1016_j.ajem.2025.10.042.json

BLOCKED-403_geoerg2019_not-a-pdf.html
  The HTTP 403 body returned by downloads.hindawi.com and by Wiley pdfdirect when attempting the
  full text of Geoerg et al. 2019 (10.1155/2019/9717208). It is a publisher block page, NOT the
  article. No quantified value in BRIEF.md is drawn from it.
