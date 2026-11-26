import sqlite3, sys
c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
q = lambda s, *a: c.execute(s, a).fetchall()
esc = lambda x: '' if x is None else str(x).replace('|', '\\|').replace('\n', ' ')
o = []
v = q('pragma user_version')[0][0]
o.append(f"# Base gathered: ICF codes, access needs, identities\n\nGenerated from `data/guidebook.db` (schema {v}) by `gather_base.py`; re-run rather than trust. Read-only.\n")

# ICF
rows = q("select icf_code, component, is_range, title, title_source from base_icf order by component, icf_code")
used = {r[0]: [] for r in rows}
for t, col in (('access_need_icf', 'access need'), ('identity_icf_map', 'identity'), ('identity_need_icf', 'identity-need triple'),
               ('extraction_lens_links', 'extraction'), ('gaps', 'gap')):
    for (k, n) in q(f"select icf_code, count(*) from {t} where icf_code is not null group by 1"):
        if k in used: used[k].append(f"{n} {col}")
o.append(f"## 1. ICF codes in `base_icf` ({len(rows)})\n")
names = {'b': 'b: body functions', 'd': 'd: activities and participation', 'e': 'e: environmental factors', 's': 's: body structures'}
for comp in 'bdes':
    r = [x for x in rows if x[1] == comp]
    o.append(f"### {names[comp]} ({len(r)})\n")
    if not r: o.append("None.\n"); continue
    o.append("| code | range | title (as stored) | title source | referenced by |\n|---|---|---|---|---|")
    for code, _, rng, title, src in r:
        o.append(f"| {code} | {'yes' if rng else ''} | {esc(title) or '(none stored)'} | {esc(src)} | {esc('; '.join(used[code]))} |")
    o.append("")

# needs
needs = q("select need_code, family, design_obligation, absorbs, notes from access_needs order by family, need_code")
o.append(f"## 2. Access needs in `access_needs` ({len(needs)})\n")
o.append("| need | family | design obligation | absorbs | ICF codes (`access_need_icf`, confidence) | notes |\n|---|---|---|---|---|---|")
for code, fam, ob, ab, nt in needs:
    icf = ', '.join(f"{i} ({cf})" for i, cf in q("select icf_code, confidence from access_need_icf where need_code=? order by icf_code", code))
    o.append(f"| {code} | {esc(fam)} | {esc(ob)} | {esc(ab)} | {icf} | {esc(nt)} |")
o.append("")

# identities
ids = q("select identity_code, display_name, category, description, parent_code, is_compound, status, superseded_by_identity, superseded_by_need from base_taxonomy_identity order by category, identity_code")
o.append(f"## 3. Disability identities in `base_taxonomy_identity` ({len(ids)})\n")
o.append("| code | display name | category | description | parent | compound | status | superseded by | ICF codes (`identity_icf_map`, live rows) |\n|---|---|---|---|---|---|---|---|---|")
for code, dn, cat, d, par, comp, st, sbi, sbn in ids:
    icf = ', '.join(i for (i,) in q("select distinct icf_code from identity_icf_map where identity_code=? and retired_at is null order by icf_code", code))
    sb = sbi or sbn or ''
    o.append(f"| {code} | {esc(dn)} | {esc(cat)} | {esc(d)} | {esc(par)} | {'yes' if comp else ''} | {esc(st)} | {esc(sb)} | {icf} |")
o.append("")
open(sys.argv[1], 'w').write('\n'.join(o))
print(len(rows), len(needs), len(ids))
