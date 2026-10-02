#!/usr/bin/env bash
# WP10 (batch 23's owed judgement and repairs), written through T1's verbs on a scratch copy.
# Usage: DB=<scratch copy of data/guidebook.db at user_version 101> bash wp10.sh
# Every call carries GUIDEBOOK_DB_PATH inline (CLAUDE.md section 4).
set -u
S=session_2026-10-01-research-batch-23
run() { GUIDEBOOK_DB_PATH="$DB" python3 scripts/db.py "$@" --session "$S" || { echo "FAILED: $*" >&2; exit 1; }; }

# (a) adjudicate the 14 observations
# Slope phrases name TERM-001 (ramp gradient: the slope of an accessible ramp).
run adjudicate-term --observation-id 81 --outcome NAMES-EXISTING --term-id TERM-001 --rationale "'ramplutning' is the Swedish compound for ramp slope; the context states a ratio (1:12) and calls it a safety risk. It is the slope of the ramp, which is TERM-001's definition."
run adjudicate-term --observation-id 82 --outcome NAMES-EXISTING --term-id TERM-001 --rationale "'inclinação' (Anexo 2.5.1 1) is the gradient of the ramp stated as a percentage bounded by a rise and a horizontal projection. It is the slope of the ramp, TERM-001. The rise and the projection are separate concepts (TERM-090 level difference, TERM-091 ramp run length)."
run adjudicate-term --observation-id 83 --outcome NAMES-EXISTING --term-id TERM-001 --rationale "'pendiente' in SUA 1 4.3.1 is the ramp's longitudinal gradient (a maximum percentage, with exceptions). TERM-001's definition is the slope of an accessible ramp as a ratio or percentage."
run adjudicate-term --observation-id 84 --outcome NAMES-EXISTING --term-id TERM-001 --rationale "'pendiente longitudinal' (Orden TMA/851/2021 art. 14.2 c) is the running gradient of a ramp section, tiered by its length. It is the slope of the ramp, TERM-001; the qualifier 'longitudinal' separates it from the cross slope, which this source states separately and which is not this term."
run adjudicate-term --observation-id 85 --outcome NAMES-EXISTING --term-id TERM-001 --rationale "'Pendientes longitudinales máximas' is the Metodología's table heading for the maximum running gradients of ramps by length (p. 24). The ramp's slope, TERM-001; the cross slope on the same page is a different quantity."

# Element phrases name TERM-089 (ramp): narrower phrases are adjudicated to the element, not minted
# (that term's own scope note).
run adjudicate-term --observation-id 75 --outcome NAMES-EXISTING --term-id TERM-089 --rationale "'경사로' is the Korean word for ramp, the element whose gradient the clause bounds (12분의 1 이하). Element phrase, TERM-089; its gradient is TERM-001."
run adjudicate-term --observation-id 89 --outcome NAMES-EXISTING --term-id TERM-089 --rationale "'경사로' in the official law.go.kr Annex 1, same clause and same word as observation 75 (the NEPLA mirror). The ramp element, TERM-089."
run adjudicate-term --observation-id 76 --outcome NAMES-EXISTING --term-id TERM-089 --rationale "'hellingbaan' is the Dutch term for the ramp the Bbl requires where a level difference exceeds 20 mm. Element phrase, TERM-089 (the scope note already names 'hellend vlak' as a narrower Dutch phrase)."
run adjudicate-term --observation-id 77 --outcome NAMES-EXISTING --term-id TERM-089 --rationale "'hellingbaan' on the IPLO page: 'bedoeld voor personen om hoogteverschillen mee te kunnen overbruggen', which is TERM-089's definition (an inclined surface that bridges a level difference)."
run adjudicate-term --observation-id 79 --outcome NAMES-EXISTING --term-id TERM-089 --rationale "'ramp' in BFS 2024:12 2 kap. 4 §: the element that must incline at most 1:12 to meet the requirement of 1 and 2 §§. Ramp element, TERM-089."
run adjudicate-term --observation-id 87 --outcome NAMES-EXISTING --term-id TERM-089 --rationale "'hellingbanen' (plural) in Ieder(in)'s letter: the ramp element whose requirements the letter says will be aligned with NEN 9120. Element phrase, TERM-089."
run adjudicate-term --observation-id 86 --outcome NAMES-EXISTING --term-id TERM-089 --rationale "'plan incliné' is the arrêté's term for an inclined plane laid out where a level difference must be overcome, here bounded at a slope of 6 % or less. The French counterpart of the Dutch 'hellend vlak' already named in TERM-089's scope note; the ramp element."
run adjudicate-term --observation-id 90 --outcome NAMES-EXISTING --term-id TERM-089 --rationale "'rampas' in Anexo 2.5.1 of Decreto-Lei 163/2006: the ramp element, whose clause says it must have the least possible slope and meet one of the listed conditions. TERM-089; the slope is TERM-001."

# 'utjämning till 0-nivå': the Allmänt råd under the heading 'Utjämningar mellan gångytor' in ALM 2 8 §
# bounds the slope of a levelling to zero level between walking surfaces at crossings, parking spaces
# and boarding places. Whether that is the ramp element (a curb-ramp class, as for observation 61) or a
# distinct transition element is not settled by the advisory text alone.
run adjudicate-term --observation-id 88 --outcome DEFERRED --rationale "'utjämning till 0-nivå' names a levelling between walking surfaces to zero level (the text's examples are crossings, parking spaces for people with mobility limitations, and boarding places) with a slope bound of 1:12. It may be the ramp element in its curb-ramp class (TERM-089, as 'curb ramp' was for REF-01008) or a distinct transition element; the advisory text under 8 § does not say which, and the binding provision it advises on was not read in this pass. Deferred, not declared out of scope."

# (b) TERM-089 is an element, not a quantity under determination. The quantities that bear on it are other
# terms. TERM-001 is already parameter 3.
run decline-parameter --term-id TERM-089 --reason "An element, not a quantity under determination: its slope is TERM-001 (ramp gradient, parameter 3), its length TERM-091 and its landings TERM-092. A determination is keyed on a quantity; 'ramp' has no value to determine. The term stays in the vocabulary and keeps its adjudications."

# (c) supersede the NEPLA mirror by the official file
run supersede-source --ref-id REF-01019 --by REF-01031 --reason "REF-01019 is the NEPLA wiki's transcription of the Enforcement Rule's Annex 1 (title, year and author identical to REF-01031, the official law.go.kr file read afterwards). Its extractions 82 and 83 carry the same text and figures as 107 and 108 on REF-01031; the independence count already follows root_ref_id to REF-01031. Superseded so the mirror is not counted as a second source (assess_cell.gather_sources) and test_db_integrity D04 reads one live source."

# (d) close pass 4 (never pass 1: the 2026-09-27 owner ruling holds it open; pass 2 was left open by its session).
# Finding 80's only resolving artefact is the database file (a containment diff of canonical against a scratch
# snapshot that was not preserved); the verb prints that as REPORTED and the session record discloses it.
run close-adversarial-pass --pass-id 4

# (e) the three stale code leads (R15): point at the rows that replace them, never copy their values.
run update-code-lead --lead-id 91 --status RETRIEVED --clause "DB-SUA, SUA 1, 4.3.1 apartado 1 (REF-01027, extractions 98 and 99)" --append-note "Retrieved from the primary text as REF-01027 in batch 23. The primary's figures are source_value_extractions 98 and 99; the secondary-page tiers in recovered_from were not read from the primary and are superseded by those rows. The clause is SUA 1 4.3.1, not 'DB-SUA 9'."
run update-code-lead --lead-id 92 --clause "arrêté du 8 décembre 2014, art. 2 (reproduced in the DHUP guide, REF-01030 p. 12); arrêté du 20 avril 2017 not retrieved" --append-note "Status stays REFERENCE-ONLY: the arrêté du 20 avril 2017 (new ERP) is still not retrieved (Légifrance blocks automated retrieval). The 2014 arrêté's art. 2 is reproduced in REF-01030 (extractions 103 to 105); the vendor-page figures in recovered_from (5 percent recommended; 8, 10 and 12 percent exceptions) were not read from either arrêté and are not confirmed."
run update-code-lead --lead-id 93 --append-note "No longer unadmitted: admitted in batch 23 as REF-01029 (T3 grey, authored by CERMI Comunidad de Madrid, supported by the Ayuntamiento; extractions 101 and 102). Candidate 132 resolved to it. The recovered_from text above predates the admission."

# (f) gaps. close-gap carries no reason; the reasons are in the session record.
run close-gap --gap-id GAP-005 --status CLOSED-FIXED
run close-gap --gap-id GAP-055 --status CLOSED-FIXED
run close-gap --gap-id GAP-058 --status CLOSED-FIXED
run close-gap --gap-id GAP-060 --status CLOSED-FIXED
run close-gap --gap-id GAP-059 --status CLOSED-DECIDED

# (g) gaps found by T1's independent review (PR #168) and left for a schema or owner decision.
run add-gap --category SW --priority P2 --skill research-batch --section "schema views over evidence_sources" --description "SIX VIEWS DO NOT FILTER A SUPERSEDED SOURCE, SO A TOMBSTONE STILL READS AS LIVE THROUGH THEM. supersede-source (T1, PR #168) writes evidence_sources.superseded_by_ref_id; assess_cell.gather_sources and test_db_integrity D04 and A09 honour it, and the writers observe-term, add-extraction and add-population-match now refuse a superseded source, but the views that read evidence_sources do not. Derive the set: select name from sqlite_master where type='view' and sql like '%evidence_sources%' and sql not like '%superseded%' (v_convergence_sources, v_determination_provenance, v_evidence_authors, v_item_provenance, v_source_admission, v_source_reach_all on 2026-10-02). v_evidence_authors is read by the scheduled resolve_dois.py, citation_mining_completeness.py and code_currency_audit.py; v_source_admission by research_protocol_audit.py. First live case: REF-01019, superseded by REF-01031 in batch 23. Remedy is a schema change (a view migration), so it ships in a tooling-only PR; decide per view whether a tombstone should be hidden (a determination view) or shown with its pointer (an audit view). Recorded in supersede_source's docstring as a known gap."
run add-gap --category DEC --priority P2 --skill research-batch --section "schemas/enums.py Co1SourceType; schemas/directness.py grain_for; evidence_sources.co1_source_type" --description "THE LIVE CO-1 SOURCE TYPES ARE NOT THE ENUM THE WRITER CHECKS, AND THE ENGINE GRADES THEM BY FALLBACK. Derive: select ref_id, co1_source_type from evidence_sources where evidence_type='co1' (REF-00989 lived_experience_publication, REF-00993 dpo_position_statement, REF-01006 and REF-01009 participatory_research on 2026-10-02) against list(schemas.enums.Co1SourceType). All four values are outside the enum. grain_for('co1', 1, <unknown>) returns individual grain (G3), so every live Co-1 source grades individual-grain; a DPO position statement arguably carries population grain. amend-source --field evidence_type --replacement co1 --co1-source-type enforces enum membership (T1, PR #168), so retyping a source TO co1 with these values is refused until the taxonomy is settled; add-source does not check membership (zero null values today, so requiring presence is safe, membership is not). The column has no CHECK. This is a doctrine question (which community-grain classes the evidence model recognises) before it is a tooling one, so it needs an owner decision: widen the enum to what the corpus uses, or recode the four rows to the enum. The Co-1 warrant is co-production (CLAUDE.md section 6); a misgrained Co-1 source understates the community evidence."
