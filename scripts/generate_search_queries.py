#!/usr/bin/env python3
"""Generate multilingual search queries for a slug using term_aliases.

Usage: python3 scripts/generate_search_queries.py <slug> [--adversarial] [--harm]

Reads term_aliases from data/guidebook.db, maps slug to relevant terms
via items→term_item_links, and generates search queries for each language.

THREE QUERY MODES, on two different adversarial axes:

  standard      What provision is recommended, and at what value.

  --adversarial Interrogates THE EVIDENCE: is this study limited, contested,
                criticised? Suffixes translate "criticism limitation evidence".

  --harm        Interrogates THE EFFECT ON PEOPLE: who does this provision
                fail, exclude, or actively hurt? Suffixes translate
                "harm adverse-effect barrier exclusion".

The distinction matters and was a structural blind spot until 2026-07-24.
Only --adversarial existed, so the *generator* could ask whether a source was
weak but never whether a design harmed somebody.

Scope that claim precisely (corrected by adversarial review the same day, after
an earlier draft of this note overstated it):
  * All 50 rows of search_executions contain zero queries with harm / adverse /
    barrier / fail / risk / detriment. But search_executions is not the whole
    search history — search_coverage tracks 4960 slug x jurisdiction cells and
    98 markdown search logs predate the structured log.
  * Harm-oriented searching HAS happened, slug by slug, without tooling: the
    search logs mention barrier in 32 files, risk in 11, failure in 6. The
    vestibular-balance slug goes further and sets its PICO outcome to "falls,
    fall-injury, balance recovery, vision-induced dizziness" — an explicitly
    harm-framed question.
So the gap is not that nobody ever looked. It is that looking for harm was left
to whoever thought of it, in one language, with no generated queries and no
structured record — while looking for what works was tooled and tracked.

Evidence of what does not work for people is evidence. Absence of it is a
finding about the search protocol, not about the built environment.

Owner directive 2026-07-24: "our search slugs need to include harm... we need to
record all evidence of failures/what doesn't work for people."

Output: JSON array of {language, standard_query, terms_used,
                       adversarial_query?, harm_query?}
"""
import sqlite3
import json
import sys
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'guidebook.db')

ADVERSARIAL_SUFFIXES = {
    'DA': 'kritik begrænsning evidens',
    'DE': 'Kritik Einschränkung Evidenz',
    'EN': 'criticism limitation evidence',
    'ES': 'crítica limitación evidencia',
    'FI': 'kritiikki rajoitus näyttö',
    'FR': 'critique limitation preuve',
    'IT': 'critica limitazione evidenza',
    'JA': '批判 限界 エビデンス',
    'KO': '비판 한계 근거',
    'NL': 'kritiek beperking bewijs',
    'NO': 'kritikk begrensning evidens',
    'PT': 'crítica limitação evidência',
    'SV': 'kritik begränsning evidens',
    'ZH': '批评 局限 证据',
}

# Harm-axis suffixes: what a provision costs the people it was not designed for.
# Deliberately NOT synonyms of the adversarial set above — those question the
# source, these question the outcome. Terms chosen to surface adverse-effect
# reporting, access barriers, and exclusion, including post-occupancy findings
# where a compliant building still failed somebody.
#
# TRANSLATION STATUS: first pass, EN-anchored. Per the project's multilingual
# protocol these belong in term_aliases with per-language review rather than
# hardcoded here; several are literal renderings that a native-speaker pass
# should confirm before non-EN results are treated as saturated. Flagged, not
# silently trusted.
HARM_SUFFIXES = {
    'DA': 'skade utilsigtet virkning barriere udelukkelse',
    'DE': 'Schaden unerwünschte Wirkung Barriere Ausschluss',
    'EN': 'harm adverse effect barrier exclusion',
    'ES': 'daño efecto adverso barrera exclusión',
    'FI': 'haitta haittavaikutus este poissulkeminen',
    'FR': 'préjudice effet indésirable obstacle exclusion',
    'IT': 'danno effetto avverso barriera esclusione',
    'JA': '有害 悪影響 障壁 排除',
    'KO': '피해 부작용 장벽 배제',
    'NL': 'schade nadelig effect barrière uitsluiting',
    'NO': 'skade uheldig virkning hindring ekskludering',
    'PT': 'dano efeito adverso barreira exclusão',
    'SV': 'skada negativ effekt hinder uteslutning',
    'ZH': '危害 不良影响 障碍 排斥',
}

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_search_queries.py <slug> [--adversarial]")
        sys.exit(1)
    
    slug = sys.argv[1]
    adversarial = '--adversarial' in sys.argv
    harm = '--harm' in sys.argv
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Find items linked to this slug
    items = conn.execute("""
        SELECT item_code FROM items WHERE bpc_source_slug = ?
    """, (slug,)).fetchall()
    
    if not items:
        print(f"No items linked to slug '{slug}'. Using slug name as concept basis.", 
              file=sys.stderr)
    
    # Find terms linked to those items
    term_ids = set()
    for item in items:
        links = conn.execute("""
            SELECT term_id FROM term_item_links WHERE item_code = ?
        """, (item['item_code'],)).fetchall()
        for link in links:
            term_ids.add(link['term_id'])
    
    # If no item-term links, try to match slug words to term canonical names
    if not term_ids:
        slug_words = slug.replace('-', ' ').split()
        for word in slug_words:
            # Exclude functional_axis pseudo-terms (E12): their canonical_en are common
            # words ("balance", "pain", "orientation") that would spuriously match many
            # slugs and inject axis translations into query generation uncontrolled.
            matches = conn.execute("""
                SELECT term_id FROM terms
                WHERE lower(canonical_en) LIKE ?
                  AND (domain IS NULL OR domain != 'functional_axis')
            """, (f'%{word}%',)).fetchall()
            for m in matches:
                term_ids.add(m['term_id'])
    
    if not term_ids:
        print(f"No terms found for slug '{slug}'.", file=sys.stderr)
        sys.exit(1)
    
    # Get all languages
    languages = [r[0] for r in conn.execute(
        "SELECT DISTINCT language FROM term_aliases ORDER BY language"
    ).fetchall()]
    
    results = []
    for lang in languages:
        # Get aliases for all relevant terms in this language
        aliases = []
        terms_used = []
        for tid in sorted(term_ids):
            rows = conn.execute("""
                SELECT ta.alias, ta.alias_type, t.canonical_en
                FROM term_aliases ta
                JOIN terms t ON ta.term_id = t.term_id
                WHERE ta.term_id = ? AND ta.language = ?
                ORDER BY 
                    CASE ta.alias_type 
                        WHEN 'TRANSLATION' THEN 1 
                        WHEN 'SYNONYM' THEN 2 
                        WHEN 'DOMAIN' THEN 3 
                        WHEN 'NARROWER' THEN 4 
                        WHEN 'BROADER' THEN 5 
                    END
            """, (tid, lang)).fetchall()
            
            if rows:
                terms_used.append(rows[0]['canonical_en'])
                # Use TRANSLATION first, then first SYNONYM
                for r in rows:
                    if r['alias_type'] in ('TRANSLATION', 'SYNONYM', 'DOMAIN'):
                        aliases.append(r['alias'])
                        if len(aliases) >= 2 * len(term_ids):
                            break
        
        if not aliases:
            continue
        
        # Build standard query: top 3-4 aliases
        std_terms = aliases[:min(4, len(aliases))]
        standard_query = ' '.join(std_terms)
        
        # Suffix tables are keyed by uppercase ISO code; term_aliases.language
        # returns lowercase. Normalise before lookup.
        #
        # BUG FIX 2026-07-24: this lookup previously used the raw `lang`, so
        # ADVERSARIAL_SUFFIXES.get(lang) missed on every language and every
        # "adversarial" query ever generated was a truncated standard query with
        # no criticism terms appended — the adversarial mode was inert for its
        # entire existence. Found by the harm_suffix_available diagnostic below.
        lang_key = (lang or '').upper()

        # Build adversarial query: top 2 aliases + adversarial suffix
        adv_terms = aliases[:min(2, len(aliases))]
        adv_suffix = ADVERSARIAL_SUFFIXES.get(lang_key, '')
        adversarial_query = ' '.join(adv_terms) + ' ' + adv_suffix

        # Build harm query: top 2 aliases + harm suffix. Same alias base as the
        # adversarial query so the two are comparable; only the axis differs.
        harm_terms = aliases[:min(2, len(aliases))]
        harm_suffix = HARM_SUFFIXES.get(lang_key, '')
        harm_query = ' '.join(harm_terms) + ' ' + harm_suffix

        entry = {
            'language': lang,
            'standard_query': standard_query,
            'terms_used': terms_used,
        }
        if adversarial:
            entry['adversarial_query'] = adversarial_query.strip()
        if harm:
            # Emitted even where no harm suffix exists for the language, so a
            # missing translation shows up as a bare query rather than silently
            # dropping the language from harm coverage.
            entry['harm_query'] = harm_query.strip()
            entry['harm_suffix_available'] = lang_key in HARM_SUFFIXES

        results.append(entry)
    
    print(json.dumps(results, ensure_ascii=False, indent=2))
    conn.close()

if __name__ == '__main__':
    main()
