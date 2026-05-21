#!/usr/bin/env python3
"""Recover canonical DOIs for the 8 IDENTIFIER-TRUNCATED + IDENTIFIER-404 rows
via Crossref bibliographic phrase search (query.bibliographic + author + year filter)."""
import json
import re
import sqlite3
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

DB = sqlite3.connect('data/guidebook.db')
DB.row_factory = sqlite3.Row
UA = "Guidebook-Recovery/1.0 (mailto:[email protected])"


def normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def clean_title_for_search(t):
    """Strip the citation-shorthand tail (journal name, page refs, etc.) before searching."""
    if not t:
        return ""
    # Strip patterns like ". <Journal name>" at the end
    t = re.sub(r'\.\s+[A-Z][A-Za-z]+\s+[A-Z][A-Za-z]+.*$', '', t)
    t = re.sub(r'\.\s+(JMIR|Build Res Inf|Frontiers.*|PMC\d+).*$', '', t)
    t = re.sub(r'\*[^*]+\*\s*$', '', t)  # *italics journal*
    return t.strip()


def search_crossref(title, author=None, year=None):
    """Bibliographic phrase search. Returns top match or None."""
    params = {'query.bibliographic': title, 'rows': 5}
    if author:
        params['query.author'] = author
    if year:
        params['filter'] = f'from-pub-date:{year-1},until-pub-date:{year+1}'
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        items = data.get('message', {}).get('items', []) or []
        return items
    except Exception as e:
        return f"error:{type(e).__name__}"


targets = ['REF-00029', 'REF-00244', 'REF-00528', 'REF-00534',
           'REF-00535', 'REF-00543', 'REF-00630', 'REF-00637']

for ref in targets:
    r = DB.execute('SELECT * FROM evidence_sources WHERE ref_id=?', (ref,)).fetchone()
    title = clean_title_for_search(r['pub_title'])
    author = r['first_author_last']
    year = r['pub_year']
    print(f"--- {ref} ---")
    print(f"  stored: author={author!r} year={year}")
    print(f"  cleaned title for search: {title[:80]}")
    print(f"  stored DOI: {r['doi']}")

    if not title or len(title.split()) < 3:
        print(f"  -> SKIP (title too short for reliable search)")
        print()
        continue

    items = search_crossref(title, author, year)
    if isinstance(items, str):
        print(f"  -> ERROR {items}")
        print()
        continue
    if not items:
        print(f"  -> NO MATCHES")
        print()
        continue

    # Cross-check top result
    top = items[0]
    cr_title = (top.get('title') or [''])[0]
    cr_first = (top.get('author') or [{}])[0]
    cr_last = cr_first.get('family', '')
    parts = top.get('issued', {}).get('date-parts', [[None]])
    cr_year = parts[0][0] if parts and parts[0] else None

    a, b = normalize(cr_title), normalize(title)
    shared = set(a.split()) & set(b.split())
    title_ok = len(shared) >= 4 or (len(shared) >= 3 and len(b.split()) <= 5)
    author_ok = (not author) or (normalize(cr_last) == normalize(author))
    year_ok = (not year) or (not cr_year) or abs(int(year) - int(cr_year)) <= 1

    verdict = "MATCH" if (title_ok and author_ok and year_ok) else "HOLD"
    print(f"  top result: {cr_last} ({cr_year}) | {cr_title[:70]}")
    print(f"  DOI: {top.get('DOI')}")
    print(f"  checks: title_ok={title_ok} author_ok={author_ok} year_ok={year_ok}")
    print(f"  -> {verdict}")
    print()
    time.sleep(0.3)
