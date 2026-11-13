"""Steps 5 to 8: extractions with a lawful lens on an existing active parameter; the rest
PARKED as the exact argv (lens blank, waits_on AQ-1) in parked-writes.jsonl."""
import json, sys
from common import run, pdfp, STEM, REF, SESS

ANCHOR = 'retrieval-log/session_2026-11-13-edmonton-checklist-pass/1a117aff4c5947a8.pdf'
SEC = {'1': '1. PARKING AREAS', '2': '2. ENTRANCES', '5': '5. ELEVATORS', '6': '6. RAMPS',
       '7': '7. HANDRAILS', '8': '8. WASHROOMS'}
P1_SENTENCE = 'a wider turning radius and wider doors are required by many wheelchairs and scooters today'
P1_FINDING = ('there is a need to exceed minimum standards for accessibility where possible. For example, '
              'a wider turning radius and wider doors are required by many wheelchairs and scooters today')
LEGEND = 'the source legend on PDF p. 1 names blue Code (required) and magenta Best Practice'
CODE_BASIS = ('The source prints this figure in its Code (required) colour (blue; ' + LEGEND + ') and states on '
              'PDF p. 1 that "Alberta Building Code requires the minimum standards for accessibility": the figure '
              'restates the Alberta building code, presumed an echo (OR-19), and supplies no independent root. The '
              'code is not held here, so root_ref_id is NULL and the root is untraced (precedent: extractions 57 and '
              '64); T-071 step 3 re-roots it when the code is admitted (lead staged with add-locator).')
BEST_BASIS = ('The source prints this figure in its Best Practice colour (magenta; ' + LEGEND + '): the committee\'s '
              'own recommendation, not attributed to a code.')
MOB_NOTE = ('[ASSUMPTION] Lens MOB rests on the source\'s PDF p. 1 sentence "' + P1_SENTENCE + '", which names exactly '
            'the two quantities door width and turning space; a stricter reading of the lens writer\'s D-2 rule (the '
            'figure\'s own words) would move this figure under the owner\'s open question AQ-1 (ADJUDICATION F4, 6).')


def base(param, item, ct, text, setting, colour, notes, role='claim'):
    maj = item.split('.')[0]
    a = ['add-extraction', '--ref-id', REF, '--parameter-id', str(param), '--claim-type', ct,
         '--claim-text', text, '--source-section', f'{SEC[maj]}, item {item}', '--jurisdiction', 'CA',
         '--setting', setting, '--extraction-method', 'full-read', '--measurement-paradigm', 'stated_unmeasured',
         '--figure-role', role, '--file-anchor', ANCHOR, '--locator-scheme', 'section',
         '--loc-section', maj, '--loc-subsection', item,
         '--loc-note', f'PDF p. {pdfp(item)} (render p000{pdfp(item) - 1}); colour read from the text layer (items.json)',
         '--session', STEM]
    if colour == 'CODE':
        a += ['--root-type', 'untraced', '--root-classification-basis', CODE_BASIS]
    else:
        a += ['--root-type', 'committee_assertion', '--root-classification-basis', BEST_BASIS]
    a += ['--notes', f'PDF p. {pdfp(item)}, item {item}. Source class: {"Code (required), blue" if colour == "CODE" else "Best Practice, magenta"}. ' + notes]
    return a


def val(v, unit, cmp_):
    return ['--claimed-value', v, '--claimed-unit', unit, '--comparator', cmp_]


MOB = ['--identity', 'MOB', '--lens-basis', 'named_in_text', '--lens-basis-text', P1_SENTENCE, '--device-class', 'mixed']
NONE = ['--relation', 'none']
FLOOR = ('Comparator >=: the source writes "is"; its PDF p. 1 frames the Code class as "the minimum standards for '
         'accessibility", so the figure is a floor (ADJUDICATION R8).')
PREF = 'Comparator >=: a "preferred" or "recommend" figure is a floor the committee sets above the code figure (ADJUDICATION R8).'


def go(label, a, dry=False):
    rc, o = run(*a, step='add-extraction:' + label, dry=dry)
    eid = None
    try:
        eid = json.loads(o[o.index('{'):]).get('extraction_id')
    except Exception:
        pass
    print(label, rc, eid, '|', o.replace('\n', ' ')[-300:] if rc else '')
    return rc, eid, o


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    ids = {}
    # (a) door width and turning, MOB on the page-1 sentence
    a = base(9, '2.3', 'numerical', 'Doorway clearance is 850mm when the door is in the open 90 degree position',
             'doorway; door open to 90 degrees', 'CODE', FLOOR + ' ' + MOB_NOTE) + val('850', 'mm', '>=') + MOB + NONE
    rc, ids['850'], _ = go('850', a, dry)
    a = base(9, '2.3', 'numerical', '(920mm/36” preferred)', 'doorway; door open to 90 degrees', 'BEST',
             PREF + ' ' + MOB_NOTE) + val('920', 'mm', '>=') + MOB
    if dry or not ids['850']:
        a += NONE
    else:
        a += ['--relation', 'exceeds', '--to-extraction', str(ids['850']), '--stated', 'named',
              '--quote', 'Doorway clearance is 850mm when the door is in the open 90 degree position (920mm/36” preferred)']
    rc, ids['920'], _ = go('920', a, dry)
    a = base(9, '5.3', 'numerical', 'with elevator door at least 910 – 915mm/36” wide', 'elevator door', 'BEST',
             'Comparator >= on 910: the source prints "at least 910 – 915mm"; the second figure, 915 mm, is not a '
             'ceiling the source states and is kept here, not as a closed between (ADJUDICATION F7). ' + MOB_NOTE
             ) + val('910', 'mm', '>=') + MOB + NONE
    rc, ids['910'], _ = go('910', a, dry)
    car = base(5, '5.3', 'numerical', 'Preferred dimension of elevator car to allow for optimal turning radius of 1500x1500mm/60x60”',
               'elevator car', 'BEST',
               PREF + ' The source writes "turning radius of 1500x1500mm": a square space, stored as its side (precedent: '
               'a square turning space stored as its side, extraction 211 in the first scratch database). Whether 1500 '
               'is a radius, a diameter or the side of a square is ambiguous as printed (ADJUDICATION F7). ' + MOB_NOTE
               ) + val('1500', 'mm', '>=') + MOB + NONE
    rc, ids['1500car'], o = go('1500car', car + ['--value-as-written', '1500x1500mm'], dry)
    if rc:
        print('value-as-written refused; retrying without it, the ambiguity in notes')
        rc, ids['1500car'], _ = go('1500car-no-vaw', car, dry)
    # (b) 9 m landing interval: A-EFFORT on "resting areas"
    a = base(12, '6.2', 'numerical', 'Level landings/ resting areas provided at 9m/10yd intervals along ramp', 'ramp', 'CODE',
             'Comparator <=: "provided at 9m intervals" sets the longest run between landings, a ceiling on the run '
             '(ADJUDICATION F7, R8); the source does not print "maximum". Lens: the access need for effort and fatigue '
             '(A-EFFORT) on the source\'s words "resting areas"; no identity is named (OD-31).'
             ) + val('9', 'm', '<=') + ['--needs', 'A-EFFORT', '--lens-basis', 'named_in_text', '--lens-basis-text', 'resting areas'] + NONE
    rc, ids['9m'], _ = go('9m', a, dry)
    # step 7: page-1 inadequacy findings
    fnote = ('The source\'s page-1 statement that the minimum standards are inadequate for many wheelchairs and scooters '
             '(R7 harm/inadequacy). No printed heading; the page is the document\'s introduction. ' + MOB_NOTE)
    fd = ['add-extraction', '--ref-id', REF, '--parameter-id', '9', '--claim-type', 'qualitative', '--claim-text', P1_FINDING,
          '--source-section', 'CHECKLIST FOR ACCESSIBILITY & UNIVERSAL DESIGN (introduction, PDF p. 1)', '--jurisdiction', 'CA',
          '--setting', 'doors (general)', '--extraction-method', 'full-read', '--measurement-paradigm', 'stated_unmeasured',
          '--figure-role', 'finding', '--harm-finding', '--file-anchor', ANCHOR, '--locator-scheme', 'page', '--loc-section', '1',
          '--loc-note', 'PDF p. 1 (render p0000)', '--root-type', 'committee_assertion', '--notes', 'PDF p. 1. ' + fnote,
          '--session', STEM, '--claimed-value', 'minimum-standard door widths are insufficient for many wheelchairs and scooters today; wider doors are required'] + MOB
    if dry or not ids['850']:
        fd += NONE
    else:
        fd += ['--relation', 'insufficient', '--to-extraction', str(ids['850']), '--stated', 'inferred',
               '--quote', 'there is a need to exceed minimum standards for accessibility where possible']
    rc, ids['find9'], _ = go('finding-9', fd, dry)
    ft = [x if x != '9' else '5' for x in fd[:5]] + fd[5:]
    ft[ft.index('doors (general)')] = 'turning space (general)'
    ft[ft.index('--claimed-value') + 1] = 'a minimum-standard turning radius is insufficient for many wheelchairs and scooters today; a wider turning radius is required'
    ft = ft[:ft.index('--relation')] if '--relation' in ft else ft
    ft += ['--relation', 'insufficient', '--to-label', 'Alberta Building Code',
           '--to-kind', 'standard', '--stated', 'named', '--quote', 'Alberta Building Code requires the minimum standards for accessibility']
    rc, ids['find5'], o5 = go('finding-5', ft, dry)
    json.dump(ids, open(SESS + '/../../scratchpad/' + STEM + '/.ids.json' if False else '/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/replay/ids.json', 'w'))
    print(ids)
