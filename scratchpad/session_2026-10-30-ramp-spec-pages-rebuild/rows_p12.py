#!/usr/bin/env python3
"""Parameter 12 (ramp run length, TERM-091) rows, and the parameter 3 condition rows they point at.
usage: rows_p12.py check|dry|write   (GUIDEBOOK_DB_PATH must name the scratch copy for dry|write)

A run cap stated per gradient is conditioned on that gradient (relation condition_on needs a ROW to
point at), so where no parameter 3 row holds the gradient tier this driver writes one (figure_role
condition) first and points the parameter 12 row at it. An absolute cap uses relation none.
"""
import json, subprocess, sys
sys.path.insert(0, 'scripts/research')
import retrieval_log as rl

SES = open('scratchpad/CURRENT').read().strip()

SG_T5 = ("Gradient of ramp Maximum run of ramp (mm) Provision of colour contrast, handrails and edge protection "
         "1:12 6000 Mandatory 1:14 9000 1:16 12000 1:20 15000 1:24 18000 1:25 or gentler Non-mandatory")
SG_T4 = ("Changes in vertical rise (mm) Gradient not steeper than 0 to 15 1:2 More than 15 to 50 1:5 "
         "More than 50 to 175 1:10 Exceeding 175 1:12")
SG_NOTE = ("Table 5 pairs each gradient with a maximum run; the pairing is split into a parameter 3 condition row (the gradient) "
           "and a parameter 12 row (the run). Landing depth is 1500 mm (4.6.5.2(a)). Read from the page image (PDF page 47) as well as "
           "the text layer. Version 1.1 (1 March 2026) is the current edition; v1.0 (7 April 2025) is superseded.")
FR_A = 'En cas de plan incliné de pente supérieure ou égale à 5 %, un palier de repos est nécessaire tous les 10 m.'
FR_B = ('Il est recommandé de prévoir un palier de repos tous les 10 m dès qu’une pente supérieure à 2 % est aménagée '
        'sur une longue distance, sans attendre le seuil réglementaire de 5 %')
FR_SECT = 'Guide illustré, Accessibilité des ERP / IOP, cheminement extérieur'

ROWS = []


def add(key, param, ref, jur, val, unit, text, sect, loc, notes, rel=None, cmp='<=', role='claim', exempt=None, ctype='numerical', **extra):
    ROWS.append(dict(ctype=ctype, **extra, key=key, param=param, ref=ref, jur=jur, val=val, unit=unit, text=text, sect=sect, loc=loc,
                     notes=notes, rel=rel, cmp=cmp, role=role, exempt=exempt))


# ---------- parameter 3 rows that parameter 12 rows point at ----------
add('SG-T4', 3, 'REF-00139', 'SG', '1:12', 'rise:run ratio (maximum gradient where the change in vertical rise exceeds 175 mm)', SG_T4,
    'Code on Accessibility 2025, 4.5.1, Table 4', dict(section='4.5', subsection='4.5.1', clause='Table 4'),
    'Current edition (v1.1). Table 4 steps the permitted gradient by rise: 1:2 to 15 mm, 1:5 to 50 mm, 1:10 to 175 mm, 1:12 above. 4.6.2.1 requires a ramp to meet Table 4 and be consistent between landings. Read from the page image (PDF page 43).',
    rel=('none',))
for g in ('1:12', '1:14', '1:16', '1:20', '1:24'):
    add('SG-' + g, 3, 'REF-00139', 'SG', g, 'rise:run ratio (a gradient tier in Table 5 to which a maximum run applies)', SG_T5,
        'Code on Accessibility 2025, 4.6.5.2(b), Table 5', dict(section='4.6.5', subsection='4.6.5.2', clause='b'),
        SG_NOTE + f' Tier: {g}.', rel=('none',), role='condition')
add('FR-5', 3, 'REF-01030', 'FR', '5', '% (slope from which a rest landing every 10 m is required on an inclined plane)', FR_A,
    FR_SECT, dict(section='plan incliné'), 'Threshold at which the requirement applies, not a limit on gradient.', rel=('none',), cmp='>=', role='condition')
add('FR-2', 3, 'REF-01030', 'FR', '2', '% (slope above which the guide recommends a rest landing every 10 m over a long distance)', FR_B,
    FR_SECT + ', recommandations', dict(section='recommandations'), 'Threshold at which the recommendation applies, not a limit on gradient.', rel=('none',), cmp='>', role='condition')

# ---------- parameter 12 ----------
add('UK-10', 12, 'REF-00992', 'UK', '10', 'm maximum going (horizontal length) of any ramp flight',
    'no flight has a going greater than 10m, or a rise of more than 500mm', 'Approved Document M Volume 2, paragraph 1.26 c.',
    dict(section='1.26', clause='c'),
    'Absolute cap: it applies at every gradient. Table 1 in the same paragraph lets the going lengthen only as the gradient gentles, to 1:20 at 10 m; those goings are held on parameter 3 (extractions 25, 26). Rest landings are named in the preceding text.',
    rel=('none',))
add('IE-10', 12, 'REF-01018', 'IE', '10', 'm maximum going of a flight at gradient 1:20 (Table 2)',
    'Table 2 Limits for Ramp Gradients and Lengths Maximum Going of a Flight Maximum Gradient Maximum Rise Not exceeding 10 m 1:20 500 mm Not exceeding 5 m 1:15 333 mm Not exceeding 2 m 1:12 166 mm',
    'Technical Guidance Document M 2022, Table 2', dict(section='1.1.3.4', clause='Table 2'),
    'Row "Not exceeding 10 m / 1:20 / 500 mm". The steeper rows (5 m at 1:15, 2 m at 1:12) are goings at which a steeper gradient is permitted and are not repeated here; extraction 81 holds the gradient.',
    rel=('condition_on', 'IE-81', 'Not exceeding 10 m 1:20 500 mm'))
for g in ('1:12', '1:14', '1:16', '1:20', '1:24'):
    run = {'1:12': '6', '1:14': '9', '1:16': '12', '1:20': '15', '1:24': '18'}[g]
    add('SG12-' + g, 12, 'REF-00139', 'SG', run, f'm maximum run of ramp at gradient {g} (Table 5)', SG_T5,
        'Code on Accessibility 2025, 4.6.5.2(b), Table 5', dict(section='4.6.5', subsection='4.6.5.2', clause='b'),
        SG_NOTE + f' Row: {g}, {run} m.', rel=('condition_on', 'SG-' + g, SG_T5))
add('DE-6', 12, 'REF-00988', 'DE', '6', 'm maximum length of a ramp run before a landing',
    'Rampenläufe dürfen max. 6 m lang sein. Danach muss ein Podest vorgesehen werden, das mindestens 150 cm lang ist.',
    'DGUV Fachinfoblatt Teil 2 Kapitel 4.3', dict(section='4.3'),
    'Secondary (T5) guidance; the same paragraph gives the maximum slope 6 % and a landing at least 150 cm long.', rel=('none',),
    exempt=('the persisted page is HTML with named character entities (Rampenl&auml;ufe d&uuml;rfen max. 6 m lang sein); '
            'the quote is the entity-decoded text and the only mismatch is the entity spelling of a-umlaut and u-umlaut'))
add('NZ-9000', 12, 'REF-01016', 'NZ', '9000', 'mm maximum interval between landings on a ramp',
    'Ramps require level platforms or landings at the top and bottom, wherever there is a change in direction, wherever doors open off them and at intervals not exceeding 9000 mm',
    'NZS 4121:2001, 6.5.1', dict(section='6.5', subsection='6.5.1'),
    'Edition held is 2001; whether it is the current edition is not established here (REF-01016 is UNVERIFIED). Landings are at least 1200 mm (6.5.2), 1500 mm where possible.', rel=('none',))
add('ES-9', 12, 'REF-01027', 'ES', '9', 'm maximum length of a ramp section (tramo), horizontal projection, on an accessible route',
    'Los tramos tendrán una longitud de 15 m como máximo, excepto si la rampa pertenece a itinerarios accesibles, en cuyo caso la longitud del tramo será de 9 m, como máximo',
    'DB SUA, SUA 1, 4.3.2 apartado 1', dict(section='SUA 1', subsection='4.3.2', paragraph='1'),
    'General limit 15 m; 9 m on accessible routes. Parking ramps shared by vehicles and people are not limited.', rel=('none',))
add('ES851-9', 12, 'REF-01028', 'ES', '9', 'm maximum length of a ramp section at slope 8%, horizontal projection',
    'La pendiente longitudinal máxima será del 10% para tramos de hasta 3,00 m de longitud, y del 8% para tramos de hasta 9,00 m de longitud, medidos en proyección horizontal.',
    'Orden TMA/851/2021, art. 14 apartado 2 c)', dict(section='art. 14', paragraph='2', clause='c'),
    'Public urban space. The 10% / 3,00 m tier is not repeated here; extraction 100 holds the slope.', rel=('condition_on', 'ES-100', None))
add('PT-10', 12, 'REF-01032', 'PT', '10', 'm maximum horizontal projection of a ramp at gradient not above 6%',
    'Ter uma inclinação não superior a 6 %, vencer um desnível não superior a 0,6 m e ter uma projecção horizontal não superior a 10 m',
    'Decreto-Lei 163/2006, Anexo, secção 2.5, ponto 2.5.1', dict(section='2.5', subsection='2.5.1', clause='1'),
    'Interpolated values permitted. Point 2.5.5 requires a resting platform where the projection exceeds the figure for the gradient, at the base and top of each flight and at changes of direction.', rel=('condition_on', 'PT-109', None))
add('PT-5', 12, 'REF-01032', 'PT', '5', 'm maximum horizontal projection of a ramp at gradient not above 8%',
    'Ter uma inclinação não superior a 8 %, vencer um desnível não superior a 0,4 m e ter uma projecção horizontal não superior a 5 m',
    'Decreto-Lei 163/2006, Anexo, secção 2.5, ponto 2.5.1', dict(section='2.5', subsection='2.5.1', clause='2'),
    'Interpolated values permitted; see the 6% row.', rel=('condition_on', 'PT-110', None))
add('FR-10a', 12, 'REF-01030', 'FR', '10', 'm maximum spacing of rest landings (paliers de repos) on an inclined plane of slope 5% or more',
    FR_A, FR_SECT, dict(section='plan incliné'),
    'Required. A rest landing is also required at the top and bottom of every inclined plane whatever its length.', rel=('condition_on', 'FR-5', None))
add('FR-10b', 12, 'REF-01030', 'FR', '10', 'm recommended spacing of rest landings once any slope above 2% is laid over a long distance',
    FR_B, FR_SECT + ', recommandations', dict(section='recommandations'),
    'A recommendation, stated against the regulatory threshold of 5%: the guide advises resting at the same spacing from a gentler slope than the rule requires.', rel=('condition_on', 'FR-2', None))

EXISTING = {'IE-81': 81, 'ES-100': 100, 'PT-109': 109, 'PT-110': 110}


def check():
    bad = 0
    for r in ROWS:
        if r['exempt']:
            continue
        qs = {r['text']} | ({r['rel'][2]} if len(r['rel']) > 2 and r['rel'][2] else set())
        for q in qs:
            hit = rl.locate_quote(q, ref_id=r['ref'])
            if hit[0] != 'scoped':
                bad += 1
                print(hit[0].upper(), r['key'], q[:80], '|', hit[1][:90])
    print('rows', len(ROWS), 'quote misses', bad)


def argv(r, ids):
    a = ['python3', 'scripts/db.py', 'add-extraction', '--ref-id', r['ref'], '--parameter-id', str(r['param'])] + (['--identity', r.get('identity', 'MOB')] if r.get('identity', 'MOB') else []) + (['--needs', r['needs']] if r.get('needs') else []) + [
         '--claim-type', r.get('ctype', 'numerical')] + (['--claimed-value', r['val']] if r['val'] else []) + (['--claimed-unit', r['unit']] if r['unit'] else []) + ['--claim-text', r['text'],
         '--source-section', r['sect']] + (['--jurisdiction', r['jur']] if r['jur'] else []) + ['--setting', r.get('setting', 'ramp'),
         '--extraction-method', r.get('method', 'full-read'), '--extraction-status', 'preliminary',
         '--figure-role', r['role']] + (['--comparator', r['cmp']] if r['cmp'] else []) + [ '--locator-scheme', 'section', '--notes', r['notes'], '--session', SES]
    for k, v in r['loc'].items():
        a += ['--loc-' + k, v]
    if r['exempt']:
        a += ['--verbatim-exempt', r['exempt']]
    rel = r['rel']
    if rel[0] == 'none':
        a += ['--relation', 'none']
    else:
        target = ids.get(rel[1]) or EXISTING[rel[1]]
        quote = rel[2] or r['text']
        a += ['--relation', 'condition_on', '--to-extraction', str(target), '--to-label', '-',
              '--stated', 'named', '--quote', quote]
    return a


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'check':
        check()
        sys.exit()
    ids = {}
    for r in sorted(ROWS, key=lambda r: r['param']):  # parameter 3 rows first
        a = argv(r, ids) + (['--dry-run'] if mode == 'dry' else [])
        p = subprocess.run(a, capture_output=True, text=True)
        out = p.stdout + p.stderr
        if p.returncode:
            print('FAIL', r['key'], out.strip()[-400:])
            sys.exit(1)
        try:
            j = json.loads(out[out.index('{'):out.rindex('}') + 1])
            ids[r['key']] = j['extraction_id']
        except Exception:
            pass
        print(r['key'], ids.get(r['key']), 'ok', 'dry' if mode == 'dry' else 'written')
