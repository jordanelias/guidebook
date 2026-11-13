"""Steps 5 to 8, third run: extractions with a lawful lens on an existing active parameter.

Changes from the second run (REPLAY-V3-BRIEF):
  F1  no `exceeds` edge: `exceeds` means "the referent's value is more than needed", the reverse of the
      source's pairing; no relation kind states "a higher figure recommended beside a stated floor", so
      the pairing is parked (park_v3.py) and a gap names the missing kind.
  F4  one lens rule: the words must name the function or need, not merely the feature. Item 2.4's
      absent finding is WRITTEN, on the ICF codes its words name ("tight grasping or twisting of the
      wrist"); the 9 m interval keeps A-EFFORT on "resting areas" as the judge's reading [ASSUMPTION].
  F5  the page-1 sentence's figures carry, beside MOB, the access need A-REACH (its design obligation
      names "doorway/turning clearance" and it absorbs wheelchair users) and ICF d465 "Moving around
      using equipment" (the sentence names wheelchairs and scooters), each on the sentence's words.
  F10 no pointer to a disposable database; F12 the magenta root basis as the brief words it."""
import json, sys
from common import run, pdfp, STEM, REF, SC

ANCHOR = 'retrieval-log/session_2026-11-13-edmonton-checklist-pass/1a117aff4c5947a8.pdf'
SEC = {'1': '1. PARKING AREAS', '2': '2. ENTRANCES', '5': '5. ELEVATORS', '6': '6. RAMPS',
       '7': '7. HANDRAILS', '8': '8. WASHROOMS'}
P1_SENTENCE = 'a wider turning radius and wider doors are required by many wheelchairs and scooters today'
P1_FINDING = ('there is a need to exceed minimum standards for accessibility where possible. For example, '
              'a wider turning radius and wider doors are required by many wheelchairs and scooters today')
CODE_BASIS = ('The source prints this figure in its Code (required) colour (blue; its legend on PDF p. 1 names blue '
              'Code (required) and magenta Best Practice) and states on PDF p. 1 that "Alberta Building Code requires '
              'the minimum standards for accessibility": the figure is presumed an echo of the Alberta building code '
              '(OR-19) and supplies no independent root. The code is not held, so root_ref_id is NULL and the root is '
              'untraced (precedent: canonical extractions 57 and 64); it is re-rooted when the code is admitted.')
BEST_BASIS = ('The source prints this figure in its Best Practice colour (magenta; its legend on PDF p. 1). Not attributed '
              'to a code by the source; the source names the City\'s Access Design Guide and the Barrier-Free Design '
              'Guide as references for best practice and dimensions, both unretrieved leads; independence from them unproven.')
LENS_P1 = ('Lens MOB, access need A-REACH and ICF d465 rest on the source\'s PDF p. 1 sentence "' + P1_SENTENCE + '", '
           'which names exactly door width and turning space: MOB for the wheelchair and scooter users it names; A-REACH '
           'because that need\'s design obligation names "doorway/turning clearance" and it absorbs wheelchair users; '
           'd465 "Moving around using equipment" because the sentence names wheelchairs and scooters. [ASSUMPTION] that a '
           'page-1 sentence naming these two quantities warrants their figures elsewhere in the document; a stricter '
           'reading of the lens writer\'s D-2 rule (the figure\'s own words) would move them under the owner\'s open '
           'question OD-47.')
P1_LENS = ['--identity', 'MOB', '--needs', 'A-REACH', '--icf', 'd465', '--lens-basis', 'named_in_text',
           '--lens-basis-text', P1_SENTENCE, '--device-class', 'mixed']
NONE = ['--relation', 'none']


def base(param, item, ct, text, setting, colour, notes, role='claim'):
    maj = item.split('.')[0]
    a = ['add-extraction', '--ref-id', REF, '--parameter-id', str(param), '--claim-type', ct,
         '--claim-text', text, '--source-section', f'{SEC[maj]}, item {item}', '--jurisdiction', 'CA',
         '--setting', setting, '--extraction-method', 'full-read', '--measurement-paradigm', 'stated_unmeasured',
         '--figure-role', role, '--file-anchor', ANCHOR, '--locator-scheme', 'section',
         '--loc-section', maj, '--loc-subsection', item,
         '--loc-note', f'PDF p. {pdfp(item)} (render p000{pdfp(item) - 1}, read in this run); colour from the text layer (items.json), checked on the render',
         '--session', STEM]
    a += ['--root-type', 'untraced' if colour == 'CODE' else 'committee_assertion',
          '--root-classification-basis', CODE_BASIS if colour == 'CODE' else BEST_BASIS]
    a += ['--notes', notes]
    return a


def val(v, unit, cmp_):
    return ['--claimed-value', v, '--claimed-unit', unit, '--comparator', cmp_]


def go(label, a, dry=False):
    rc, o = run(*a, step='add-extraction:' + label, dry=dry)
    eid = None
    try:
        eid = json.loads(o[o.index('{'):]).get('extraction_id')
    except Exception:
        pass
    print(label, rc, eid, '|', o.replace('\n', ' ')[-400:] if rc else '')
    return rc, eid, o


ROWS = {}
ROWS['850'] = base(9, '2.3', 'numerical', 'Doorway clearance is 850mm when the door is in the open 90 degree position',
                   'doorway; door open to 90 degrees', 'CODE',
                   'PDF p. 3, item 2.3 prints "Doorway clearance is 850mm when the door is in the open 90 degree position" in '
                   'blue, its Code (required) colour. Comparator >=: the source writes "is", and its page 1 calls the code '
                   '"the minimum standards for accessibility", so the figure is a floor. ' + LENS_P1
                   ) + val('850', 'mm', '>=') + P1_LENS + NONE
ROWS['920'] = base(9, '2.3', 'numerical', '(920mm/36” preferred)', 'doorway; door open to 90 degrees', 'BEST',
                   'PDF p. 3, item 2.3 prints "(920mm/36” preferred)" in magenta, its Best Practice colour, after the blue '
                   '850 mm. Comparator >=: a preferred clear width is read as a floor the committee sets above the code '
                   'figure. The source pairs it with the 850 mm figure; no relation kind in extraction_relations states that '
                   'pairing (exceeds says the referent is more than needed, the reverse of the source), so no edge is '
                   'written and the pairing is parked. ' + LENS_P1) + val('920', 'mm', '>=') + P1_LENS + NONE
ROWS['910'] = base(9, '5.3', 'numerical', 'with elevator door at least 910 – 915mm/36” wide', 'elevator door', 'BEST',
                   'PDF p. 5, item 5.3 prints "with elevator door at least 910 – 915mm/36” wide" in magenta. Comparator >= '
                   'on 910: "at least" opens the bound; the second figure, 915 mm, is not a ceiling the source states and is '
                   'kept here, not stored as a closed between. ' + LENS_P1) + val('910', 'mm', '>=') + P1_LENS + NONE
ROWS['1500car'] = base(5, '5.3', 'numerical',
                       'Preferred dimension of elevator car to allow for optimal turning radius of 1500x1500mm/60x60”',
                       'elevator car', 'BEST',
                       'PDF p. 5, item 5.3 prints "Preferred dimension of elevator car to allow for optimal turning radius of '
                       '1500x1500mm/60x60”" in magenta. Comparator >=: a preferred dimension is read as a floor. The source '
                       'calls a 1500 x 1500 mm square a "turning radius": stored as the side of the square, 1500 mm, as '
                       'canonical extraction 211 stores a 1.4 m x 1.4 m space as 1.4 m (select ref_id, setting from '
                       'source_value_extractions where extraction_id=211). Whether 1500 is a radius, a diameter or the side of '
                       'a square is ambiguous as printed; no follow-up reason holds that (a gap names it). ' + LENS_P1
                       ) + val('1500', 'mm', '>=') + P1_LENS + NONE
ROWS['9m'] = base(12, '6.2', 'numerical', 'Level landings/ resting areas provided at 9m/10yd intervals along ramp', 'ramp',
                  'CODE',
                  'PDF p. 6, item 6.2 prints "Level landings/ resting areas provided at 9m/10yd intervals along ramp" in '
                  'blue. Comparator <=: "provided at 9m intervals" sets the longest run between landings, a ceiling on the '
                  'run; the source does not print "maximum". Lens: access need A-EFFORT (design obligation "Cost little '
                  'energy; ... rest points") on the source\'s words "resting areas". [ASSUMPTION] the judge\'s reading that '
                  '"Level landings/ resting areas" names the resting function and not merely a feature; the rule applied '
                  'across this batch is that the words must name the function or need. No identity is named (OD-31); no '
                  'ICF code is linked, because the registry\'s b455 carries no title to read a warrant against.'
                  ) + val('9', 'm', '<=') + ['--needs', 'A-EFFORT', '--lens-basis', 'named_in_text',
                                              '--lens-basis-text', 'resting areas'] + NONE
ROWS['absent-force'] = base(6, '2.4', 'absent',
                            'Door operating device should not require tight grasping or twisting of the wrist (doors should have lever handles)',
                            'door operating device', 'CODE',
                            'PDF p. 3, item 2.4 prints "Door operating device should not require tight grasping or twisting '
                            'of the wrist (doors should have lever handles)" in blue: a grip and wrist requirement with no '
                            'force figure, so the source states nothing for parameter 6 operating force. Lens: ICF d440 '
                            '"Fine hand use" (the words "tight grasping") and d445 "Hand and arm use" (the words "twisting of '
                            'the wrist"), on the clause\'s own words. No access-need link: no design obligation in '
                            'access_needs names grip or wrist movement (A-PRECISION names imprecise input, A-REACH reach and '
                            'one-handed operation). No identity is named.', role='finding'
                            ) + ['--extraction-status', 'absent-confirmed', '--icf', 'd440', '--icf', 'd445',
                                 '--lens-basis', 'named_in_text', '--lens-basis-text',
                                 'tight grasping or twisting of the wrist'] + NONE
FNOTE = ('PDF p. 1 (no heading; the document\'s introduction) states that the minimum standards are inadequate for many '
         'wheelchairs and scooters (R7 harm/inadequacy). ' + LENS_P1)
ROWS['find9'] = ['add-extraction', '--ref-id', REF, '--parameter-id', '9', '--claim-type', 'qualitative',
                 '--claim-text', P1_FINDING, '--source-section', 'CHECKLIST FOR ACCESSIBILITY & UNIVERSAL DESIGN (introduction, PDF p. 1)',
                 '--jurisdiction', 'CA', '--setting', 'doors (general)', '--extraction-method', 'full-read',
                 '--measurement-paradigm', 'stated_unmeasured', '--figure-role', 'finding', '--harm-finding',
                 '--file-anchor', ANCHOR, '--locator-scheme', 'page', '--loc-section', '1',
                 '--loc-note', 'PDF p. 1 (render p0000, read in this run)', '--root-type', 'committee_assertion',
                 '--notes', FNOTE, '--session', STEM,
                 '--claimed-value', 'minimum-standard door widths are insufficient for many wheelchairs and scooters today; wider doors are required'] + P1_LENS
ROWS['find5'] = [x for x in ROWS['find9']]
ROWS['find5'][ROWS['find5'].index('--parameter-id') + 1] = '5'
ROWS['find5'][ROWS['find5'].index('--setting') + 1] = 'turning space (general)'
ROWS['find5'][ROWS['find5'].index('--claimed-value') + 1] = ('a minimum-standard turning radius is insufficient for many '
                                                              'wheelchairs and scooters today; a wider turning radius is required')
ROWS['find5'] += ['--relation', 'insufficient', '--to-label', 'Alberta Building Code', '--to-kind', 'standard',
                  '--stated', 'named', '--quote', 'Alberta Building Code requires the minimum standards for accessibility']

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    ids = {}
    for k in ['850', '920', '910', '1500car', '9m', 'absent-force']:
        _, ids[k], _ = go(k, ROWS[k], dry)
    f9 = ROWS['find9'] + (['--relation', 'none'] if dry else
                          ['--relation', 'insufficient', '--to-extraction', str(ids['850']), '--stated', 'inferred',
                           '--quote', 'there is a need to exceed minimum standards for accessibility where possible'])
    _, ids['find9'], _ = go('find9', f9, dry)
    _, ids['find5'], _ = go('find5', ROWS['find5'], dry)
    if not dry:
        json.dump(ids, open(SC + '/ids.json', 'w'))
    print(ids)
