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
import re
import sys
import os

DB_PATH = os.environ.get(
    'GUIDEBOOK_DB_PATH',
    os.path.join(os.path.dirname(__file__), '..', 'data', 'guidebook.db'))

# --- slug -> term matching (token-based; replaced substring matching 2026-07-25) --------
#
# The fallback used to test `lower(canonical_en) LIKE '%<slug word>%'`. Substring
# matching produced silent false positives that no one saw because the generator
# prints queries, not the terms behind them:
#   'room'   matched  head-ROOM clearance
#   'ot'     matched  vibr-OT-actile alert
#   'aut'    matched  dys-AUT-onomia
#   'read'   matched  Adaptable READ-iness
#   'and'    matched  every canonical containing the word "and"
# Token equality kills all of these. Aliases are indexed too, so the synonym
# chart itself drives retrieval rather than the canonical name alone.

# Tokens too common across the slug corpus to discriminate (df >= ~7 of 106),
# plus generic English. Dropping them prevents shotgun matches such as
# 'accessibility' pulling in seven unrelated terms.
_STOP = {
    "environment", "built", "design", "and", "for", "the", "of", "in", "to",
    "with", "on", "by", "a", "an", "or", "at", "as", "its", "per", "non",
    "all", "general", "global", "v2", "access", "accessibility", "accessible",
    "disability", "impairment", "provision", "space", "room", "free",
    "material", "time", "load", "post", "care", "setting", "data", "based",
    "using", "review", "analysis", "study", "user", "control",
}


def _stem(w):
    """Crude singulariser. Must not strip the 's' of access/cross/analysis."""
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith("s") and len(w) > 3 and not w.endswith(("ss", "is", "us", "as")):
        return w[:-1]
    return w


def _tokens(text):
    return {_stem(w) for w in re.split(r'[^a-z0-9]+', text.lower())
            if len(w) >= 2 and w not in _STOP} - _STOP


def _term_token_index(conn):
    """term_id -> token set, drawn from canonical_en AND its English aliases.

    Functional-axis pseudo-terms stay excluded: their canonical names are common
    words ("balance", "pain", "orientation") that would match many slugs and
    inject axis translations into query generation uncontrolled.
    """
    idx = {}
    for r in conn.execute(
            "SELECT term_id, canonical_en FROM terms "
            "WHERE domain IS NULL OR domain != 'functional_axis'"):
        idx[r['term_id']] = _tokens(r['canonical_en'])
    for r in conn.execute(
            "SELECT term_id, alias FROM term_aliases WHERE language = 'en'"):
        if r['term_id'] in idx:
            idx[r['term_id']] |= _tokens(r['alias'])
    return idx


def _slug_token_df(conn):
    df = {}
    for (slug,) in conn.execute("SELECT slug FROM slugs").fetchall():
        for w in _tokens(slug):
            df[w] = df.get(w, 0) + 1
    return df


def match_terms_by_slug(conn, slug):
    """Return {term_id: {matching tokens}} for a slug with no item->term links."""
    idx = _term_token_index(conn)
    df = _slug_token_df(conn)
    hits = {}
    for w in _tokens(slug):
        for tid, toks in idx.items():
            if w in toks:
                hits.setdefault(tid, set()).add(w)
    # Precision rule: once a slug matches on a *specific* token (rare across the
    # corpus), discard terms resting only on generic ones. Without this,
    # 'wheelchair'-plus-'housing' slugs drag in every loosely related term.
    specific = {t for t, ws in hits.items() if any(df.get(w, 0) <= 4 for w in ws)}
    if specific:
        hits = {t: ws for t, ws in hits.items() if t in specific}
    return hits

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
    
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
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
    
    # If no item-term links, match slug tokens against term canonical names and
    # their English aliases (see match_terms_by_slug for why this is not LIKE).
    if not term_ids:
        term_ids |= set(match_terms_by_slug(conn, slug))
    
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
