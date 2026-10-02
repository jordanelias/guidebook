#!/usr/bin/env bash
# WP10 second pass: fixes for the independent review of data_20261002023004 (section 8 of the session record).
# Run on a scratch copy of data/guidebook.db AFTER that migration is applied.
# Usage: DB=<scratch copy> bash wp10b.sh
set -u
S=session_2026-10-01-research-batch-23
run() { GUIDEBOOK_DB_PATH="$DB" python3 scripts/db.py "$@" --session "$S" || { echo "FAILED: $*" >&2; exit 1; }; }

# (1) Observation 88: the DEFERRED (adjudication 77) rested on "the binding provision was not read". The persisted
# ALM 2 text carries it directly above the Allmänt råd. A second adjudication on the same observation is permitted
# (divergent judgements read as a contest); this one is the later and better-grounded.
run adjudicate-term --observation-id 88 --outcome NAMES-EXISTING --term-id TERM-089 --rationale "Supersedes adjudication 77 (DEFERRED), whose stated ground, that the binding provision was not read, was wrong: the persisted ALM 2 text (BFS 2011:5, PDF p. 4) carries 8 § directly above the Allmänt råd, and it reads 'På dessa platser ska delar av nivåskillnaderna utjämnas med ramp till 0-nivå'. The levelling 'till 0-nivå' is made with a ramp, and the advisory then bounds that ramp's slope (1:12) and width (90-100 cm), at crossings, parking spaces and boarding places. That is the ramp element in its curb-ramp class, a narrower phrase adjudicated to TERM-089 as 'curb ramp' was (adjudication 61) and 'short ramps' (adjudication 63); its slope is TERM-001."

# (2) Lead 85 (GAP-005's own case): it still says the law was not retrieved and holds the false attribution.
run update-code-lead --lead-id 85 --status RETRIEVED --clause "Cabinet Order 379/2006 Art. 19(2) (REF-00990, extractions 22 and 23); MLIT Ordinance 114/2006 Art. 11(1)(6) ro (REF-00991, extraction 24)" --append-note "The figures REF-00989 attributes to the Barrier-Free Law are now read from the instruments that carry them. The mandatory 1:12 and the 1:8 relaxation for a rise of 16 cm or less are in Cabinet Order 379/2006 (REF-00990, extractions 22 and 23). The 1:15 outdoor figure is not in that Order; it is in MLIT Ordinance 114/2006, the voluntary guidance standard (REF-00991, extraction 24, whose note records the zero occurrences). The Act itself was not retrieved; the Order under it, which holds the figures, was. Read those rows, not the secondary attribution recorded above."

# (3) Lead 92: say which vendor-page figure each retrieved row confirms or contradicts.
run update-code-lead --lead-id 92 --append-note "Per figure, against REF-01030: the 5 percent is the ministry commentary's recommendation, not the arrêté's requirement (extraction 105). The 2014 arrêté's art. 2 sets 6 percent with tolerances to 10 percent over at most 2 m and 12 percent over at most 0.50 m (extraction 103), so the vendor-page 8 percent exception is contradicted for that existing-ERP regime and its 10 and 12 percent figures differ in length bound. Whether the 2017 new-ERP arrêté states any of the vendor figures is unread."

# (4) GAP-062 named three readers of v_evidence_authors; the derivation shows more.
run amend-gap --gap-id GAP-062 --append-note "The readers of v_evidence_authors named above are not the whole set. Derive them: grep -rln v_evidence_authors scripts/ tools/*.py, excluding scripts/migrations/ and __pycache__. It includes scripts/generate/spec_page.py (render stage, via specification_source_links governing links; supersede-source refuses a source a live specification rests on, so a tombstone reaches that page only through a retired specification), tools/regenerate_vetting_surface.py, scripts/audit/source_slug_links_duplicates.py, scripts/audit_evidence_metadata.py, scripts/db.py and test_db_integrity.py. Found by the independent review of the migration that filed this gap."
