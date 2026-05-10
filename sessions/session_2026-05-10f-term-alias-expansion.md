# Session: Term alias expansion — multilingual search infrastructure
**session_start:** 2026-05-10 22:45 UTC
**session_close:** 2026-05-11 00:15 UTC
**PI version:** v10.6
**workplan:** governance (term infrastructure)

## Summary

Evaluated 30h of multilingual/adversarial work and found critical infrastructure gap: FI and DA had 0 term aliases, 6 other languages had fewer than 25 each. Expanded term_aliases from 438 to 881 entries. Created scripts/generate_search_queries.py to operationalize aliases into per-language search queries.

## What changed

### term_aliases expansion (438 to 881, +443)

| Language | Before | After | Sources |
|---|---|---|---|
| DA | 0 | 77 | BR18, DS/ISO 21542, SBi-anvisning 272, DCH |
| FI | 0 | 79 | Helsinki esteettomyyssanakirja, Decree 241/2017, SFS |
| ES | 11 | 59 | CTE, NBR 9050, Ley General de Discapacidad |
| SV | 8 | 53 | BBR/Boverket, SS 91 42 21 |
| NL | 10 | 54 | Bouwbesluit 2012, NEN 1814 |
| NO | 9 | 53 | TEK17, NS 11001 |
| IT | 10 | 51 | DM 236/89, DPR 503/96, UNI |
| KO | 39 | 65 | Barrier-Free Living Act, KS |
| PT | 24 | 44 | NBR 9050, DL 163/2006 |
| ZH | 44 | 63 | GB 50763, JGJ 50, MZ/T 032 |
| DE | 76 | 76 | (already complete) |
| EN | 91 | 91 | (already complete) |
| FR | 57 | 57 | (already complete) |
| JA | 59 | 59 | (already complete) |

### Key terminology decisions (not just translations)

- FI "aistihuone" (sensory room) vs "rauhoittumistila" (calming space) vs "Snoezelen-tila" — three distinct Finnish concepts
- DA "sanserum" vs "hvilerum" vs "roligt rum" — Danish three-way split
- NL "snoezelruimte" (origin country) vs "prikkelarme ruimte" (low-stimulus) — Dutch conceptual framework
- KO "감각통합실" (SI room) vs "진정 공간" (calming space) — Korean clinical framing
- IT "percorso podotattile" / "LOGES" — Italian-specific tactile system
- NL "miva-toilet" — Dutch standard abbreviation for accessible toilet
- SV "RWC" (rullstolstoalett) — Swedish abbreviation
- NO "HC-toalett" — Norwegian abbreviation

### New script: scripts/generate_search_queries.py

Generates per-language search queries from term_aliases for any slug. Maps slug to items to term_item_links to terms to aliases, with fallback to slug-word matching. Includes adversarial suffix generation in all 14 languages.

## Commits

| SHA | Content |
|---|---|
| 47da23e421 | DB: term_aliases expansion 438 to 881 |
| 47ff5b4912 | Script: generate_search_queries.py |
| (this) | Session record |

## Downstream impact

1. Pre-LOG check 5 now passable for FI/DA — multilingual-research skill requires native_aliases for all 14 languages. FI and DA were previously blockers.
2. Slugs 5-8 FULL marking — marked via cross-jurisdictional synthesis without using term_aliases for search. Alias infrastructure now available but re-searching not done.
3. Tier 2 slugs — 6 slugs with NOT-RUN languages can use query generator for proper native-language search terms.

## next_action

1. Tier 2 multilingual redo using generate_search_queries.py for proper native-language queries
2. Slugs 5-8 spot-check — run per-language adversarial searches using new aliases on at least one batch-marked slug
3. PT expansion — still thinnest at 44 aliases (28/30 terms)

## blockers

None.
