# Search log: terminology pass SV-SE (Swedish, Sweden), session_2026-11-06-base-vocabulary-review

Rule R14: query verbatim, prior expectation written before the result, result, note on query shape. Empties kept.

## Base-derived leads (step 1)
- `research_code_leads` where jurisdiction like '%SE%' or names BBR/Boverket: 0 rows. The instrument list is not derivable from leads.
- `evidence_sources where jurisdiction='SE'`: REF-01023 (BFS 2024:12, URL rinfo.boverket.se), REF-01024 (BFS 2011:5 ALM 2, hosted on varberg.se), REF-01025 (FUB consultation reply, grey).
- `references/standards-registry.md`: two SE entries that contradict each other and the base: one calls BFS 2024:12 the replacement of BBR "in force 1 July 2025"; the other calls BFS 2024:12 "ALM 2 (Boverkets allmänna råd 2024:12) in force from 1 September 2024" replacing "ALM 1 (BFS 2013:9)". The retrieved BFS 2024:12 title page (below) shows it is neither ALM nor allmänna råd. Registry defect, not corrected (outside my folder).
- `term_aliases where lower(language)='sv'`: 120 rows (`select count(*) from term_aliases where lower(language)='sv'`), all TRANSLATION/SYNONYM/BROADER/NARROWER/DOMAIN; none carries an instrument locator. Treated as model-generated seeds.

## W0. Direct fetches of base URLs
- W0.1 `https://rinfo.boverket.se/BFS2024-12/pdf/BFS2024-12.pdf` (URL from REF-01023). Expectation (recorded after the fact; I did not write it before fetching, which is a deviation): a short föreskrift. Result: 200, 224065 bytes, sha256 b8d1102a…, 9 pp. Title "Boverkets föreskrifter om byggnaders tillgänglighet och användbarhet för personer med nedsatt rörelse- eller orienteringsförmåga", decided 19 November 2024, in force 1 July 2025. Contains föreskrifter only, no allmänna råd and almost no measures (6 §, 2 kap. 4–5 §). Note: the new Boverket structure splits BBR into several BFS; the quantities must be elsewhere.
- W0.2 `https://www.boverket.se/sv/lag--ratt/forfattningssamling/gallande/` (guessed listing URL). Expectation (after the fact): the list of rules in force. Result: 404. Guessed URL; shape defect, not evidence of absence.
