"""Session 6 tagging: Part 4 Category H-I-K (94 claims)"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('references/claim-reference-join.json', encoding='utf-8') as f:
    data = json.load(f)

tagging = {
    # Part 4 intro
    'CLAIM-P04-0001': ('DEFERRED', [], 'methodology note — RT60 at 500 Hz octave band (acoustic measurement standard per ISO 3382-2)'),

    # H-01 All Controls at Accessible Height
    'CLAIM-P04-0358': ('TAGGED', ['REF-00492', 'REF-00152', 'REF-00212', 'REF-00308'], None),
    'CLAIM-P04-0359': ('TAGGED', ['REF-00492', 'REF-00152', 'REF-00308'], None),
    'CLAIM-P04-0360': ('TAGGED', ['REF-00492', 'REF-00152', 'REF-00212'], None),
    'CLAIM-P04-0361': ('TAGGED', ['REF-00492', 'REF-00152', 'REF-00308'], None),
    'CLAIM-P04-0362': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P04-0363': ('TAGGED', ['REF-00212'], None),
    'CLAIM-P04-0364': ('TAGGED', ['REF-00212'], None),
    'CLAIM-P04-0365': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P04-0366': ('TAGGED', ['REF-00044', 'REF-00212'], None),
    'CLAIM-P04-0367': ('DEFERRED', [], 'retrofit cost note'),
    'CLAIM-P04-0368': ('DEFERRED', [], 'OT evidence echo — repeats reach range values already tagged upstream'),
    'CLAIM-P04-0369': ('DEFERRED', [], 'OT evidence echo — repeats force value already tagged upstream'),
    'CLAIM-P04-0370': ('DEFERRED', [], 'OT evidence echo — repeats push-pad size already tagged upstream'),

    # H-02 Individual Environmental Control
    'CLAIM-P04-0371': ('TAGGED', ['REF-00157', 'REF-00150'], None),
    'CLAIM-P04-0372': ('TAGGED', ['REF-00152', 'REF-00492'], None),
    'CLAIM-P04-0373': ('TAGGED', ['REF-00152', 'REF-00492'], None),
    'CLAIM-P04-0374': ('TAGGED', ['REF-00416', 'REF-00415'], None),
    'CLAIM-P04-0375': ('TAGGED', ['REF-00416', 'REF-00415'], None),
    'CLAIM-P04-0376': ('TAGGED', ['REF-00416', 'REF-00415'], None),
    'CLAIM-P04-0377': ('TAGGED', ['REF-00157'], None),
    'CLAIM-P04-0378': ('TAGGED', ['REF-00416', 'REF-00150'], None),
    'CLAIM-P04-0379': ('DEFERRED', [], 'DAR cost specification (NC premium) — cost note not a citable research claim'),

    # H-03 Visual Paging and Real-Time Captioning
    'CLAIM-P04-0380': ('TAGGED', ['REF-00248', 'REF-00273'], None),

    # H-04 Accessible Intercom and Video Door Entry
    'CLAIM-P04-0381': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P04-0382': ('TAGGED', ['REF-00135', 'REF-00492'], None),
    'CLAIM-P04-0383': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P04-0384': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P04-0385': ('TAGGED', ['REF-00135', 'REF-00492'], None),
    'CLAIM-P04-0386': ('TAGGED', ['REF-00492', 'REF-00152'], None),

    # I-01 Hardware Throughout
    'CLAIM-P04-0387': ('TAGGED', ['REF-00308', 'REF-00200', 'REF-00150', 'REF-00492'], None),
    'CLAIM-P04-0388': ('TAGGED', ['REF-00308', 'REF-00200', 'REF-00150'], None),
    'CLAIM-P04-0389': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P04-0390': ('DEFERRED', [], 'OT evidence echo — repeats lever hardware force and spec values'),

    # I-02 Kitchen One-Handed Operation
    'CLAIM-P04-0391': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P04-0392': ('TAGGED', ['REF-00492', 'REF-00052', 'REF-00383'], None),
    'CLAIM-P04-0393': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P04-0394': ('TAGGED', ['REF-00416', 'REF-00052'], None),

    # I-03 Bathroom UPL Anti-Scald
    'CLAIM-P04-0395': ('TAGGED', ['REF-00371', 'REF-00416', 'REF-00014'], None),
    'CLAIM-P04-0396': ('TAGGED', ['REF-00388', 'REF-00014'], None),
    'CLAIM-P04-0397': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P04-0398': ('TAGGED', ['REF-00371', 'REF-00416'], None),
    'CLAIM-P04-0399': ('TAGGED', ['REF-00388', 'REF-00014'], None),
    'CLAIM-P04-0400': ('TAGGED', ['REF-00388', 'REF-00014'], None),
    'CLAIM-P04-0401': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P04-0402': ('TAGGED', ['REF-00152', 'REF-00492'], None),
    'CLAIM-P04-0403': ('TAGGED', ['REF-00388', 'REF-00014'], None),
    'CLAIM-P04-0404': ('DEFERRED', [], 'OT evidence echo — repeats TMV temperature values already tagged'),
    'CLAIM-P04-0405': ('DEFERRED', [], 'OT evidence echo — repeats anti-scald specification'),

    # H-05 Nurse Call and Personal Emergency Response
    'CLAIM-P04-0406': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P04-0407': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P04-0408': ('TAGGED', ['REF-00150'], None),
    'CLAIM-P04-0409': ('TAGGED', ['REF-00150', 'REF-00492'], None),
    'CLAIM-P04-0410': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P04-0411': ('TAGGED', ['REF-00150'], None),

    # I-04 Ceiling Hoist (new)
    'CLAIM-P04-0412': ('TAGGED', ['REF-00311', 'REF-00150', 'REF-00416'], None),
    'CLAIM-P04-0413': ('TAGGED', ['REF-00311', 'REF-00150', 'REF-00416'], None),
    'CLAIM-P04-0414': ('TAGGED', ['REF-00416'], None),
    'CLAIM-P04-0415': ('TAGGED', ['REF-00416', 'REF-00265'], None),

    # I-04 Bathroom Drainage (retired I-04 content, still enumerated)
    'CLAIM-P04-0416': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P04-0417': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P04-0418': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P04-0419': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P04-0420': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P04-0421': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P04-0422': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P04-0423': ('DEFERRED', [], 'OT evidence echo — repeats drain grating gap spec (CLAIM-P04-0418)'),
    'CLAIM-P04-0424': ('DEFERRED', [], 'OT evidence echo — wheelchair caster diameter 100mm is mechanical context not a specification value'),
    'CLAIM-P04-0425': ('DEFERRED', [], 'OT evidence echo — repeats drain/caster gap relationship context'),

    # K-01 Intervenor Adjacency at Service Counters
    'CLAIM-P04-0426': ('TAGGED', ['REF-00203', 'REF-00306'], None),
    'CLAIM-P04-0427': ('TAGGED', ['REF-00203'], None),
    'CLAIM-P04-0428': ('DEFERRED', [], 'cross-reference parsing artifact — claim_value "06 min" = "G-06 minimum" within spec text; not a specification value'),
    'CLAIM-P04-0429': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P04-0430': ('TAGGED', ['REF-00203'], None),
    'CLAIM-P04-0431': ('TAGGED', ['REF-00203'], None),
    'CLAIM-P04-0432': ('DEFERRED', [], 'retrofit cost note'),
    'CLAIM-P04-0433': ('DEFERRED', [], 'OT evidence echo — repeats 1500mm approach zone (CLAIM-P04-0426)'),

    # K-02 Tactile Building Map Station
    'CLAIM-P04-0434': ('TAGGED', ['REF-00203', 'REF-00306'], None),
    'CLAIM-P04-0435': ('TAGGED', ['REF-00203', 'REF-00306'], None),
    'CLAIM-P04-0436': ('TAGGED', ['REF-00203', 'REF-00306'], None),
    'CLAIM-P04-0437': ('TAGGED', ['REF-00203', 'REF-00306'], None),
    'CLAIM-P04-0438': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P04-0439': ('TAGGED', ['REF-00492', 'REF-00152'], None),

    # K-03 Haptic Communication Clear Floor Zone
    'CLAIM-P04-0440': ('TAGGED', ['REF-00203', 'REF-00188', 'REF-00414'], None),
    'CLAIM-P04-0441': ('TAGGED', ['REF-00203', 'REF-00188'], None),
    'CLAIM-P04-0442': ('TAGGED', ['REF-00203', 'REF-00188', 'REF-00414'], None),
    'CLAIM-P04-0443': ('DEFERRED', [], 'retrofit cost note'),
    'CLAIM-P04-0444': ('DEFERRED', [], 'OT evidence echo — repeats 1500mm haptic zone (CLAIM-P04-0440)'),

    # K-04 Vibrotactile Alert Provision
    'CLAIM-P04-0445': ('TAGGED', ['REF-00203', 'REF-00406'], None),
    'CLAIM-P04-0446': ('TAGGED', ['REF-00203', 'REF-00406'], None),
    'CLAIM-P04-0447': ('TAGGED', ['REF-00203', 'REF-00406'], None),
    'CLAIM-P04-0448': ('TAGGED', ['REF-00492', 'REF-00203'], None),
    'CLAIM-P04-0449': ('TAGGED', ['REF-00492', 'REF-00203'], None),
    'CLAIM-P04-0450': ('DEFERRED', [], 'OT evidence echo — repeats 20-200 Hz vibrotactile frequency (CLAIM-P04-0445)'),
}

tagged_count = 0
deferred_count = 0

for claim in data:
    cid = claim['claim_id']
    if cid in tagging and claim['status'] == 'PENDING':
        status, refs, note = tagging[cid]
        claim['status'] = status
        if refs:
            claim['ref_ids'] = refs
        if note:
            claim['note'] = note
        if status == 'TAGGED':
            tagged_count += 1
        elif status == 'DEFERRED':
            deferred_count += 1

pending_remaining = [c for c in data if c['part'] == 4 and c['status'] == 'PENDING']
print(f'TAGGED this session: {tagged_count}')
print(f'DEFERRED this session: {deferred_count}')
print(f'Still PENDING in Part 4: {len(pending_remaining)}')
if pending_remaining:
    for c in pending_remaining:
        print(f'  MISSED: {c["claim_id"]}')

# Overall stats
total = len(data)
all_tagged = sum(1 for c in data if c['status'] == 'TAGGED')
all_deferred = sum(1 for c in data if c['status'] == 'DEFERRED')
all_orphaned = sum(1 for c in data if c['status'] == 'ORPHANED')
all_pending = sum(1 for c in data if c['status'] == 'PENDING')
print(f'\nOverall: TAGGED={all_tagged} DEFERRED={all_deferred} ORPHANED={all_orphaned} PENDING={all_pending} TOTAL={total}')

with open('references/claim-reference-join.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('JSON written successfully')
