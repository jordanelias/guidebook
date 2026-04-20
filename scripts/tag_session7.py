"""Session 7 tagging: Part 2 — disability population categories (83 claims)"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('references/claim-reference-join.json', encoding='utf-8') as f:
    data = json.load(f)

tagging = {
    # §2.1 MOB — Mobility (24 claims)
    'CLAIM-P02-0001': ('TAGGED', ['REF-00494', 'REF-00308'], None),
    'CLAIM-P02-0002': ('TAGGED', ['REF-00044', 'REF-00468'], None),
    'CLAIM-P02-0003': ('TAGGED', ['REF-00044', 'REF-00468'], None),
    'CLAIM-P02-0004': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P02-0005': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P02-0006': ('TAGGED', ['REF-00494', 'REF-00154'], None),
    'CLAIM-P02-0007': ('TAGGED', ['REF-00494', 'REF-00154'], None),
    'CLAIM-P02-0008': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P02-0009': ('TAGGED', ['REF-00494', 'REF-00308'], None),
    'CLAIM-P02-0010': ('TAGGED', ['REF-00494', 'REF-00308'], None),
    'CLAIM-P02-0011': ('TAGGED', ['REF-00494', 'REF-00308'], None),
    'CLAIM-P02-0012': ('TAGGED', ['REF-00494', 'REF-00308'], None),
    'CLAIM-P02-0013': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P02-0014': ('TAGGED', ['REF-00494', 'REF-00308'], None),
    'CLAIM-P02-0015': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P02-0016': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P02-0017': ('TAGGED', ['REF-00410', 'REF-00308'], None),
    'CLAIM-P02-0018': ('TAGGED', ['REF-00308', 'REF-00154'], None),
    'CLAIM-P02-0019': ('TAGGED', ['REF-00113'], None),
    'CLAIM-P02-0020': ('TAGGED', ['REF-00340', 'REF-00154'], None),
    'CLAIM-P02-0021': ('TAGGED', ['REF-00036', 'REF-00154'], None),
    'CLAIM-P02-0022': ('TAGGED', ['REF-00036', 'REF-00514'], None),
    'CLAIM-P02-0023': ('TAGGED', ['REF-00036', 'REF-00154'], None),
    'CLAIM-P02-0024': ('DEFERRED', [], 'editorial evidence confidence note'),

    # §2.2 UPL — Upper Limb Impairment (9 claims)
    'CLAIM-P02-0025': ('TAGGED', ['REF-00152', 'REF-00492'], None),
    'CLAIM-P02-0026': ('TAGGED', ['REF-00152', 'REF-00308'], None),
    'CLAIM-P02-0027': ('TAGGED', ['REF-00152', 'REF-00308'], None),
    'CLAIM-P02-0028': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P02-0029': ('TAGGED', ['REF-00333', 'REF-00150'], None),
    'CLAIM-P02-0030': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P02-0031': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P02-0032': ('TAGGED', ['REF-00494', 'REF-00150'], None),
    'CLAIM-P02-0033': ('TAGGED', ['REF-00150', 'REF-00340'], None),

    # §2.3 VIS — Visual Impairment (4 claims)
    'CLAIM-P02-0034': ('TAGGED', ['REF-00437', 'REF-00360'], None),
    'CLAIM-P02-0035': ('TAGGED', ['REF-00306'], None),
    'CLAIM-P02-0036': ('TAGGED', ['REF-00360', 'REF-00437'], None),
    'CLAIM-P02-0037': ('TAGGED', ['REF-00306'], None),

    # §2.4 DEAF — Deaf and Hard of Hearing (9 claims)
    'CLAIM-P02-0038': ('TAGGED', ['REF-00289'], None),
    'CLAIM-P02-0039': ('TAGGED', ['REF-00289', 'REF-00124'], None),
    'CLAIM-P02-0040': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P02-0041': ('TAGGED', ['REF-00142', 'REF-00289'], None),
    'CLAIM-P02-0042': ('TAGGED', ['REF-00142', 'REF-00289'], None),
    'CLAIM-P02-0043': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P02-0044': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P02-0045': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P02-0046': ('DEFERRED', [], 'editorial evidence confidence note'),

    # §2.5 NEU — Neurological (6 claims)
    'CLAIM-P02-0047': ('TAGGED', ['REF-00388', 'REF-00010'], None),
    'CLAIM-P02-0048': ('TAGGED', ['REF-00157', 'REF-00010'], None),
    'CLAIM-P02-0049': ('TAGGED', ['REF-00157', 'REF-00308'], None),
    'CLAIM-P02-0050': ('TAGGED', ['REF-00010'], None),
    'CLAIM-P02-0051': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P02-0052': ('TAGGED', ['REF-00157'], None),

    # §2.6 DEM — Dementia (4 claims)
    'CLAIM-P02-0053': ('TAGGED', ['REF-00229', 'REF-00360'], None),
    'CLAIM-P02-0054': ('TAGGED', ['REF-00229', 'REF-00360'], None),
    'CLAIM-P02-0055': ('TAGGED', ['REF-00229', 'REF-00360'], None),
    'CLAIM-P02-0056': ('TAGGED', ['REF-00229'], None),

    # §2.7 NDV — Neurodivergent / Autism (7 claims)
    'CLAIM-P02-0057': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P02-0058': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P02-0059': ('TAGGED', ['REF-00029', 'REF-00124'], None),
    'CLAIM-P02-0060': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P02-0061': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P02-0062': ('TAGGED', ['REF-00029', 'REF-00232'], None),
    'CLAIM-P02-0063': ('TAGGED', ['REF-00029', 'REF-00142'], None),

    # §2.8 MH — Mental Health (1 claim)
    'CLAIM-P02-0064': ('TAGGED', ['REF-00157', 'REF-00029'], None),

    # §2.9 PAIN — Chronic Pain / Fatigue (7 claims)
    'CLAIM-P02-0065': ('TAGGED', ['REF-00041', 'REF-00388'], None),
    'CLAIM-P02-0066': ('TAGGED', ['REF-00041', 'REF-00388'], None),
    'CLAIM-P02-0067': ('TAGGED', ['REF-00036', 'REF-00416'], None),
    'CLAIM-P02-0068': ('TAGGED', ['REF-00036'], None),
    'CLAIM-P02-0069': ('TAGGED', ['REF-00036', 'REF-00514'], None),
    'CLAIM-P02-0070': ('TAGGED', ['REF-00036'], None),
    'CLAIM-P02-0071': ('TAGGED', ['REF-00036', 'REF-00154'], None),

    # §2.10 DBL — DeafBlind (8 claims)
    'CLAIM-P02-0072': ('TAGGED', ['REF-00203', 'REF-00188'], None),
    'CLAIM-P02-0073': ('TAGGED', ['REF-00203', 'REF-00308'], None),
    'CLAIM-P02-0074': ('TAGGED', ['REF-00203', 'REF-00306'], None),
    'CLAIM-P02-0075': ('TAGGED', ['REF-00203', 'REF-00414'], None),
    'CLAIM-P02-0076': ('TAGGED', ['REF-00414', 'REF-00203'], None),
    'CLAIM-P02-0077': ('TAGGED', ['REF-00203', 'REF-00414'], None),
    'CLAIM-P02-0078': ('TAGGED', ['REF-00203', 'REF-00188'], None),
    'CLAIM-P02-0079': ('TAGGED', ['REF-00306', 'REF-00203'], None),

    # §2.11 OFS — Orthostatic / Fatigue Sensitivity (4 claims)
    'CLAIM-P02-0080': ('TAGGED', ['REF-00405', 'REF-00036'], None),
    'CLAIM-P02-0081': ('TAGGED', ['REF-00036'], None),
    'CLAIM-P02-0082': ('TAGGED', ['REF-00405', 'REF-00233'], None),
    'CLAIM-P02-0083': ('TAGGED', ['REF-00157', 'REF-00405'], None),
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

pending_remaining = [c for c in data if c['part'] == 2 and c['status'] == 'PENDING']
print(f'TAGGED this session: {tagged_count}')
print(f'DEFERRED this session: {deferred_count}')
print(f'Still PENDING in Part 2: {len(pending_remaining)}')
if pending_remaining:
    for c in pending_remaining:
        print(f'  MISSED: {c["claim_id"]}')

total = len(data)
all_tagged = sum(1 for c in data if c['status'] == 'TAGGED')
all_deferred = sum(1 for c in data if c['status'] == 'DEFERRED')
all_orphaned = sum(1 for c in data if c['status'] == 'ORPHANED')
all_pending = sum(1 for c in data if c['status'] == 'PENDING')
print(f'\nOverall: TAGGED={all_tagged} DEFERRED={all_deferred} ORPHANED={all_orphaned} PENDING={all_pending} TOTAL={total}')

with open('references/claim-reference-join.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('JSON written successfully')
