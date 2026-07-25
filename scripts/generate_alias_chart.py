#!/usr/bin/env python3
"""Render references/synonym-chart.md from the DB vocabulary tables.

Read-only. The DB is canonical; this file is derived. Regenerate after any
vocabulary migration:  python3 scripts/generate_alias_chart.py > references/synonym-chart.md
"""
import sqlite3
from collections import defaultdict
import os
DB=os.environ.get('GUIDEBOOK_DB_PATH','data/guidebook.db')
con=sqlite3.connect(f'file:{DB}?mode=ro',uri=True); con.row_factory=sqlite3.Row
LANGS=[('en','EN'),('de','DE'),('fr','FR'),('es','ES'),('it','IT'),('pt','PT'),('nl','NL'),
       ('sv','SV'),('no','NO'),('da','DA'),('fi','FI'),('ja','JA'),('zh','ZH'),('ko','KO')]
terms=list(con.execute("SELECT term_id,canonical_en,definition,domain,scope_note FROM terms ORDER BY domain,term_id"))
al=defaultdict(lambda: defaultdict(list))
for r in con.execute("SELECT term_id,alias,language,alias_type FROM term_aliases ORDER BY term_id,language,alias_type,alias"):
    al[r['term_id']][r['language']].append((r['alias'],r['alias_type']))
bydom=defaultdict(list)
for t in terms: bydom[t['domain'] or 'unclassified'].append(t)

out=[]
w=out.append
w("# Cross-Language Synonym Chart\n")
w("**Generated:** 2026-07-25 · derived from `data/guidebook.db` (`terms` / `term_aliases` / `term_item_links`)\n")
w("> **Generated file — do not hand-edit.** The database is canonical. Regenerate with")
w("> `python3 scripts/generate_alias_chart.py`. To change vocabulary, emit a data migration")
w("> (`scripts/emit_data_migration.py`) — never write the DB directly.\n")
w("## What this is\n")
w("Equivalent terms grouped under one concept, so that a search for *corridor* also finds")
w("*hallway*, *circulation route* and *Flurbreite* — and so that two documents using")
w("different words for the same thing are recognisably about the same thing.\n")
w("`scripts/generate_search_queries.py` reads these groups to build per-language search")
w("queries. Every slug in the corpus resolves to at least one concept.\n")
w("### Relation types\n")
w("| Type | Meaning |")
w("|---|---|")
w("| `SYNONYM` | Equivalent wording for the same concept |")
w("| `TRANSLATION` | Primary equivalent in that language |")
w("| `NARROWER` | A specific instance or sub-case |")
w("| `BROADER` | The containing concept |")
w("| `DOMAIN` | Project/population shorthand (e.g. `NDV`, `OT`) |")
w("| `DEPRECATED` | Retained so old wording still resolves; do not use in new text |\n")
w("### Provenance and limits\n")
w("Non-English equivalents are **model-generated and pending native-speaker review** — they")
w("are a *retrieval aid, not authoritative terminology*. Each row carries that status in")
w("`term_aliases.notes`. Verification protocol: `references/native-alias-verification.md`.")
w("Five languages required by `lang_jur_map` (AR, BN, HI, ID, SW) still carry **no aliases**")
w("and cannot be searched until vocabulary is built from published glossaries.\n")
counts={l:con.execute("SELECT COUNT(*) FROM term_aliases WHERE language=?",(l,)).fetchone()[0] for l,_ in LANGS}
w(f"**Coverage:** {len(terms)} concepts · {sum(counts.values())} aliases · {len(LANGS)} languages "
  f"(of 19 required)\n")
w("| " + " | ".join(u for _,u in LANGS) + " |")
w("|" + "---|"*len(LANGS))
w("| " + " | ".join(str(counts[l]) for l,_ in LANGS) + " |\n")
w("---\n")
for dom in sorted(bydom):
    w(f"## {dom.replace('_',' ').title()}\n")
    for t in bydom[dom]:
        w(f"### {t['term_id']} · {t['canonical_en']}\n")
        if t['definition']: w(f"{t['definition']}\n")
        if t['scope_note']: w(f"> **Scope:** {t['scope_note']}\n")
        en=al[t['term_id']].get('en',[])
        if en:
            w("**English group:** " + ", ".join(
                f"`{a}`" + ("" if ty=="SYNONYM" else f" *({ty.lower()})*") for a,ty in en) + "\n")
        rows=[]
        for code,up in LANGS:
            if code=='en': continue
            vals=al[t['term_id']].get(code,[])
            if vals: rows.append(f"| {up} | " + ", ".join(a for a,_ in vals) + " |")
        if rows:
            w("| Lang | Equivalents |"); w("|---|---|"); out.extend(rows); w("")
        items=[r[0] for r in con.execute("SELECT item_code FROM term_item_links WHERE term_id=? ORDER BY item_code",(t['term_id'],))]
        if items: w(f"**Linked items:** {', '.join(items)}\n")
print("\n".join(out))
