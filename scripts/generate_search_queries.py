#!/usr/bin/env python3
"""Generate multilingual search queries for a slug using term_aliases.

Usage: python3 scripts/generate_search_queries.py <slug> [--adversarial]

Reads term_aliases from data/guidebook.db, maps slug to relevant terms
via items→term_item_links, and generates search query pairs for each
language: a standard query and an adversarial query.

Output: JSON array of {language, standard_query, adversarial_query, terms_used}
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_search_queries.py <slug> [--adversarial]")
        sys.exit(1)
    
    slug = sys.argv[1]
    adversarial = '--adversarial' in sys.argv
    
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
            matches = conn.execute("""
                SELECT term_id FROM terms 
                WHERE lower(canonical_en) LIKE ?
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
        
        # Build adversarial query: top 2 aliases + adversarial suffix
        adv_terms = aliases[:min(2, len(aliases))]
        adv_suffix = ADVERSARIAL_SUFFIXES.get(lang, '')
        adversarial_query = ' '.join(adv_terms) + ' ' + adv_suffix
        
        entry = {
            'language': lang,
            'standard_query': standard_query,
            'terms_used': terms_used,
        }
        if adversarial:
            entry['adversarial_query'] = adversarial_query.strip()
        
        results.append(entry)
    
    print(json.dumps(results, ensure_ascii=False, indent=2))
    conn.close()

if __name__ == '__main__':
    main()
