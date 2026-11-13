"""Step 5(c) and 8: figures whose clause names no person, function or need are NOT written; each is
parked as the exact db.py argv it would have run, lens blank, waits_on AQ-1. Edges between parked
rows name the other parked row by its key (resolved to an extraction_id on replay)."""
import json
from common import SESS
from ext_v2 import base, val, FLOOR, PREF

OUT = SESS + '/parked-writes.jsonl'
NONE = ['--relation', 'none']
L = []


def park(key, argv, edges=(), extra=None):
    rec = {'key': key, 'waits_on': 'AQ-1', 'lens': '', 'argv': argv,
           'lens_note': 'Lens left blank: the clause names no person, function or need; OD-31 forbids ALL as an identity and the lens writer needs words that warrant a code (ADJUDICATION R6, AQ-1).'}
    if edges:
        rec['edges'] = [dict(e, verb='relate-extraction') for e in edges]
    if extra:
        rec.update(extra)
    L.append(rec)


THR = ('Figure role condition: the source states the slope at which a path of travel becomes a ramp, not a value of '
       'ramp gradient (ADJUDICATION F7); never anchors.')
park('6.1-1in20', base(3, '6.1', 'numerical', 'Ramps are used for any slope steeper than 1 in 20 in a path of travel.',
                       'ramp in a path of travel', 'BEST', THR, role='condition') + ['--claimed-value', '1:20', '--claimed-unit', 'rise:run ratio'] + NONE)
park('6.1-1in16', base(3, '6.1', 'numerical', 'Preferred maximum slope is 1 in 16', 'ramp in a path of travel', 'BEST',
                       'Comparator <=: a preferred maximum slope is a ceiling on gradient (lower is better for parameter 3).')
     + val('1:16', 'rise:run ratio', '<=') + NONE,
     edges=[{'relation': 'condition_on', 'to_parked': '6.1-1in20', 'stated': 'named', 'quote': 'Ramps are used for any slope steeper than 1 in 20 in a path of travel.'},
            {'relation': 'exceeds', 'to_parked': '6.1-1in12', 'stated': 'named', 'quote': 'Preferred maximum slope is 1 in 16 (1 in 12 in AB building code)'}])
park('6.1-1in12', base(3, '6.1', 'numerical', '(1 in 12 in AB building code)', 'ramp; the source attributes it to the AB (Alberta) building code', 'CODE',
                       'Comparator <=: the source attributes a 1 in 12 slope to the Alberta building code, a maximum.')
     + val('1:12', 'rise:run ratio', '<=') + NONE,
     edges=[{'relation': 'condition_on', 'to_parked': '6.1-1in20', 'stated': 'named', 'quote': 'Ramps are used for any slope steeper than 1 in 20 in a path of travel.'}])
park('1.2-1500', base(4, '1.2', 'numerical', 'Barrier-free unobstructed path of travel (minimum width of 1500mm/59”)',
                      'path of travel from parking area to building entrance (exterior)', 'BEST',
                      'Comparator >=: the source prints "minimum width". The words in parentheses are the Best Practice run; the rest of the item is Code (required).')
     + val('1500', 'mm', '>=') + NONE, extra={'also_waits_on': 'AQ-6 (which route term the path is)'})
park('2.10-1100', base(4, '2.10', 'numerical', 'Corridors should be 1100mm/43”', 'corridor', 'CODE', FLOOR) + val('1100', 'mm', '>=') + NONE)
park('2.10-1800', base(4, '2.10', 'numerical', '(recommend 1800mm/71”)', 'corridor', 'BEST', PREF) + val('1800', 'mm', '>=') + NONE,
     edges=[{'relation': 'exceeds', 'to_parked': '2.10-1100', 'stated': 'named', 'quote': 'Corridors should be 1100mm/43” (recommend 1800mm/71”)'}])
park('6.2-1500', base(4, '6.2', 'numerical', 'With the ramp at any point shall not be less than 1500mm/60”', 'ramp', 'BEST',
                      'Comparator >=: "shall not be less than". The sentence as printed has no subject noun; read as a ramp width only provisionally (ADJUDICATION F2); its observation is DEFERRED as unsettled.')
     + val('1500', 'mm', '>=') + NONE)
park('6.2-870', base(4, '6.2', 'numerical', '870mm/34” min clearspace between handrails', 'ramp; between handrails', 'CODE',
                     'Comparator >=: "min". ' + FLOOR) + val('870', 'mm', '>=') + NONE)
park('1.8-2750', base(11, '1.8', 'numerical', 'a clear height of not less than 2750mm/108” at the pull-up space and along the vertical access and egress routes',
                      'passenger loading zone: pull-up space and access and egress routes', 'CODE', 'Comparator >=: "not less than".')
     + val('2750', 'mm', '>=') + NONE)
park('2.4-absent-force', base(6, '2.4', 'absent', 'Door operating device should not require tight grasping or twisting of the wrist (doors should have lever handles)',
                              'door operating device', 'CODE', 'The source states a grip requirement and no force figure for operating a door (R7 absence).',
                              role='finding') + ['--extraction-status', 'absent-confirmed'] + NONE,
     extra={'note': 'Brief step 8: when parked, raise nothing (no absence follow-up).'})

with open(OUT, 'w') as f:
    for r in L:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(len(L), 'parked to', OUT)
