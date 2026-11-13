"""Parked writes, third run. Two kinds of line in parked-writes.jsonl:

  kind "extraction": a figure whose clause names no person, function or need. Not written; the exact
      db.py add-extraction argv with its lens left blank, waits_on OD-47 (the adjudication's AQ-1).
  kind "pairing": the source's own pairing of a higher recommended figure with the figure it prints in
      its Code colour. No relation kind in extraction_relations states that pairing (`exceeds` is the
      reverse: "the referent's value is more than needed"), so no edge is written; the line is the
      relate-extraction argv with the relation left as a marked hole, waits_on the missing kind.

Each line is dry-run twice against the scratch copy (no write): once as it stands, to capture the
refusal, and once with a probe lens (extraction lines only), to show that the lens is the only thing
missing. Item 6.2's 1500 mm is NOT parked: its sentence has no subject noun and its observation is
DEFERRED as unsettled (decided once, F9). Item 2.4's absent finding is written (ext_v3.py), not parked."""
import json
from common import run, SESS
from ext_v3 import base, val, NONE

OUT = SESS + '/parked-writes.jsonl'
HOLE = '<NO RELATION KIND IN extraction_relations.relation STATES THIS PAIRING>'
L = []


def park(key, argv, edges=(), also=None):
    rec = {'key': key, 'kind': 'extraction', 'waits_on': 'OD-47', 'lens': '', 'argv': argv,
           'lens_note': 'Lens left blank: the clause names no person, function or need; OD-31 forbids ALL as an identity and the lens writer needs words that warrant a code.'}
    if edges:
        rec['edges'] = edges
    if also:
        rec['also_waits_on'] = also
    L.append(rec)


def pairing(key, frm, to, quote, note):
    argv = ['relate-extraction', '--from', frm, '--relation', HOLE, '--to-extraction', to, '--stated', 'named',
            '--quote', quote, '--notes', note, '--session', 'session_2026-11-13-edmonton-checklist-pass']
    L.append({'key': key, 'kind': 'pairing', 'waits_on': 'no relation kind states a recommended figure beside a stated floor',
              'argv': argv, 'from': frm, 'to': to,
              'why_not_exceeds': 'exceeds means "the source asserts the referent\'s value is more than needed" (extraction_relations DDL); the source says the reverse.'})


park('6.1-1in20', base(3, '6.1', 'numerical', 'Ramps are used for any slope steeper than 1 in 20 in a path of travel.',
                       'ramp in a path of travel', 'BEST',
                       'PDF p. 6, item 6.1 prints "Ramps are used for any slope steeper than 1 in 20 in a path of travel." in '
                       'magenta: the slope at which a path of travel becomes a ramp, not a value of ramp gradient. Figure '
                       'role condition; it never anchors.', role='condition')
     + ['--claimed-value', '1:20', '--claimed-unit', 'rise:run ratio'] + NONE)
park('6.1-1in16', base(3, '6.1', 'numerical', 'Preferred maximum slope is 1 in 16', 'ramp in a path of travel', 'BEST',
                       'PDF p. 6, item 6.1 prints "Preferred maximum slope is 1 in 16" in magenta, before the blue "(1 in 12 '
                       'in AB building code)". Comparator <=: a preferred maximum slope is a ceiling on gradient.')
     + val('1:16', 'rise:run ratio', '<=') + NONE,
     edges=[{'verb': 'relate-extraction', 'relation': 'condition_on', 'to_parked': '6.1-1in20', 'stated': 'named',
             'quote': 'Ramps are used for any slope steeper than 1 in 20 in a path of travel.',
             'meaning_checked': 'condition_on: "this figure only holds given a second figure this project also holds as a row"; a preferred maximum ramp slope holds only for a slope steeper than 1 in 20, which the source makes a ramp.'}])
park('6.1-1in12', base(3, '6.1', 'numerical', '(1 in 12 in AB building code)', 'ramp; the source attributes it to the AB (Alberta) building code', 'CODE',
                       'PDF p. 6, item 6.1 prints "(1 in 12 in AB building code)" in blue. Comparator <=: the slope the '
                       'source attributes to the Alberta building code, a maximum.')
     + val('1:12', 'rise:run ratio', '<=') + NONE,
     edges=[{'verb': 'relate-extraction', 'relation': 'condition_on', 'to_parked': '6.1-1in20', 'stated': 'named',
             'quote': 'Ramps are used for any slope steeper than 1 in 20 in a path of travel.',
             'meaning_checked': 'as for 6.1-1in16.'}])
park('1.2-1500', base(4, '1.2', 'numerical', 'Barrier-free unobstructed path of travel (minimum width of 1500mm/59”)',
                      'path of travel from parking area to building entrance (exterior)', 'BEST',
                      'PDF p. 2, item 1.2 prints "minimum width of 1500mm/59”" in magenta inside a blue sentence about the '
                      '"Barrier-free unobstructed path of travel" from parking area to building entrance. Comparator >=: '
                      '"minimum width".') + val('1500', 'mm', '>=') + NONE,
     also='OD-52 (which route term the path is; its width observation is DEFERRED on it)')
park('2.10-1100', base(4, '2.10', 'numerical', 'Corridors should be 1100mm/43”', 'corridor', 'CODE',
                       'PDF p. 3, item 2.10 prints "Corridors should be 1100mm/43”" in blue, under the ENTRANCES heading. '
                       'Comparator >=: "should be" in the colour the source\'s page 1 calls the minimum standards, so a floor.')
     + val('1100', 'mm', '>=') + NONE)
park('2.10-1800', base(4, '2.10', 'numerical', '(recommend 1800mm/71”)', 'corridor', 'BEST',
                       'PDF p. 3, item 2.10 prints "(recommend 1800mm/71”)" in magenta after the blue 1100 mm. Comparator '
                       '>=: a recommended corridor width is read as a floor the committee sets above the code figure.')
     + val('1800', 'mm', '>=') + NONE)
park('6.2-870', base(4, '6.2', 'numerical', '870mm/34” min clearspace between handrails', 'ramp; between handrails', 'CODE',
                     'PDF p. 6, item 6.2 prints "870mm/34” min clearspace between handrails" in blue. Comparator >=: "min".')
     + val('870', 'mm', '>=') + NONE)
park('1.8-2750', base(11, '1.8', 'numerical', 'a clear height of not less than 2750mm/108” at the pull-up space and along the vertical access and egress routes',
                      'passenger loading zone: pull-up space and access and egress routes', 'CODE',
                      'PDF p. 2, item 1.8 prints "a clear height of not less than 2750mm/108” at the pull-up space and along '
                      'the vertical access and egress routes" in blue. Comparator >=: "not less than".')
     + val('2750', 'mm', '>=') + NONE)
pairing('pair-2.3-920-850', '229', '228', 'Doorway clearance is 850mm when the door is in the open 90 degree position (920mm/36” preferred)',
        'PDF p. 3, item 2.3: the magenta "(920mm/36” preferred)" printed beside the blue 850 mm floor.')
pairing('pair-2.10-1800-1100', '<extraction_id of parked 2.10-1800>', '<extraction_id of parked 2.10-1100>',
        'Corridors should be 1100mm/43” (recommend 1800mm/71”)',
        'PDF p. 3, item 2.10: the magenta "(recommend 1800mm/71”)" printed beside the blue 1100 mm.')
pairing('pair-6.1-1in16-1in12', '<extraction_id of parked 6.1-1in16>', '<extraction_id of parked 6.1-1in12>',
        'Preferred maximum slope is 1 in 16 (1 in 12 in AB building code)',
        'PDF p. 6, item 6.1: the magenta preferred maximum 1 in 16 printed beside the blue 1 in 12 the source attributes to the Alberta building code (a stricter ceiling beside the code ceiling).')

if __name__ == '__main__':
    with open(OUT, 'w') as f:
        for r in L:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(len(L), 'lines to', OUT)
    # dry runs: no write
    for r in L:
        a = r['argv']
        if r['kind'] == 'extraction':
            rc0, o0 = run(*a, dry=True)
            text = a[a.index('--claim-text') + 1]
            probe = a + ['--identity', 'MOB', '--lens-basis', 'named_in_text', '--lens-basis-text', text.split()[0].strip('(')]
            rc1, o1 = run(*probe, dry=True)
            r['dry_run_as_parked'] = {'exit': rc0, 'out': o0.replace('\n', ' ')[-300:]}
            r['dry_run_with_probe_lens'] = {'exit': rc1, 'out': o1.replace('\n', ' ')[-160:]}
        else:
            if r['from'].isdigit():
                rc0, o0 = run(*a, dry=True)
                r['dry_run_as_parked'] = {'exit': rc0, 'out': o0.replace('\n', ' ')[-300:]}
        print(r['key'], {k: v for k, v in r.items() if k.startswith('dry_run')})
    with open(OUT, 'w') as f:
        for r in L:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
