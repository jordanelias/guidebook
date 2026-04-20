"""Session 9 tagging: Part 6 — residential design matrices (115 claims)"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('references/claim-reference-join.json', encoding='utf-8') as f:
    data = json.load(f)

tagging = {
    # §6.0 — whole-dwelling matrix summary rows
    'CLAIM-P06-0001': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P06-0002': ('TAGGED', ['REF-00492', 'REF-00152'], None),

    # §6.1 — Entry
    'CLAIM-P06-0003': ('TAGGED', ['REF-00265', 'REF-00416'], None),
    'CLAIM-P06-0004': ('TAGGED', ['REF-00265', 'REF-00150'], None),
    'CLAIM-P06-0005': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P06-0006': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P06-0007': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P06-0008': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P06-0009': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P06-0010': ('TAGGED', ['REF-00265', 'REF-00150'], None),
    'CLAIM-P06-0011': ('TAGGED', ['REF-00265', 'REF-00154'], None),
    'CLAIM-P06-0012': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P06-0013': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P06-0014': ('TAGGED', ['REF-00492', 'REF-00152'], None),

    # §6.2 — Parking / Garage
    'CLAIM-P06-0015': ('TAGGED', ['REF-00265', 'REF-00416'], None),
    'CLAIM-P06-0016': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P06-0017': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P06-0018': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P06-0019': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P06-0020': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P06-0021': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P06-0022': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P06-0023': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P06-0024': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P06-0025': ('TAGGED', ['REF-00150', 'REF-00308'], None),

    # §6.3 — Laundry / Utility
    'CLAIM-P06-0026': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P06-0027': ('TAGGED', ['REF-00416', 'REF-00150'], None),
    'CLAIM-P06-0028': ('TAGGED', ['REF-00416', 'REF-00150'], None),
    'CLAIM-P06-0029': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P06-0030': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P06-0031': ('TAGGED', ['REF-00044', 'REF-00154'], None),

    # §6.4 — Bedroom
    'CLAIM-P06-0032': ('TAGGED', ['REF-00303', 'REF-00518'], None),
    'CLAIM-P06-0033': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P06-0034': ('TAGGED', ['REF-00311', 'REF-00416'], None),
    'CLAIM-P06-0035': ('TAGGED', ['REF-00265', 'REF-00416'], None),
    'CLAIM-P06-0036': ('TAGGED', ['REF-00150', 'REF-00265'], None),
    'CLAIM-P06-0037': ('TAGGED', ['REF-00150', 'REF-00265'], None),
    'CLAIM-P06-0038': ('TAGGED', ['REF-00265', 'REF-00150'], None),
    'CLAIM-P06-0039': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P06-0040': ('TAGGED', ['REF-00303', 'REF-00041'], None),
    'CLAIM-P06-0041': ('TAGGED', ['REF-00041', 'REF-00303'], None),
    'CLAIM-P06-0042': ('TAGGED', ['REF-00303', 'REF-00518'], None),
    'CLAIM-P06-0043': ('TAGGED', ['REF-00311', 'REF-00416'], None),
    'CLAIM-P06-0044': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P06-0045': ('TAGGED', ['REF-00150', 'REF-00265'], None),
    'CLAIM-P06-0046': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P06-0047': ('TAGGED', ['REF-00303', 'REF-00518'], None),

    # §6.5 — Bathroom
    'CLAIM-P06-0048': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P06-0049': ('TAGGED', ['REF-00371', 'REF-00388'], None),
    'CLAIM-P06-0050': ('TAGGED', ['REF-00371', 'REF-00014'], None),
    'CLAIM-P06-0051': ('TAGGED', ['REF-00150', 'REF-00229'], None),
    'CLAIM-P06-0052': ('TAGGED', ['REF-00303', 'REF-00518'], None),
    'CLAIM-P06-0053': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P06-0054': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P06-0055': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P06-0056': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P06-0057': ('TAGGED', ['REF-00150', 'REF-00311'], None),
    'CLAIM-P06-0058': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P06-0059': ('TAGGED', ['REF-00142'], None),
    'CLAIM-P06-0060': ('TAGGED', ['REF-00014', 'REF-00371'], None),
    'CLAIM-P06-0061': ('TAGGED', ['REF-00371', 'REF-00388'], None),
    'CLAIM-P06-0062': ('TAGGED', ['REF-00303', 'REF-00405'], None),
    'CLAIM-P06-0063': ('TAGGED', ['REF-00150', 'REF-00229'], None),
    'CLAIM-P06-0064': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P06-0065': ('TAGGED', ['REF-00014', 'REF-00371'], None),
    'CLAIM-P06-0066': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P06-0067': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P06-0068': ('TAGGED', ['REF-00044', 'REF-00154'], None),

    # §6.6 — Living / Reception
    'CLAIM-P06-0069': ('TAGGED', ['REF-00303', 'REF-00518'], None),
    'CLAIM-P06-0070': ('TAGGED', ['REF-00486', 'REF-00150'], None),
    'CLAIM-P06-0071': ('TAGGED', ['REF-00150', 'REF-00486'], None),
    'CLAIM-P06-0072': ('TAGGED', ['REF-00150', 'REF-00486'], None),
    'CLAIM-P06-0073': ('TAGGED', ['REF-00150', 'REF-00265'], None),
    'CLAIM-P06-0074': ('TAGGED', ['REF-00265', 'REF-00416'], None),
    'CLAIM-P06-0075': ('TAGGED', ['REF-00044', 'REF-00150'], None),
    'CLAIM-P06-0076': ('TAGGED', ['REF-00044', 'REF-00150'], None),
    'CLAIM-P06-0077': ('TAGGED', ['REF-00150', 'REF-00157'], None),  # EN 14501 not in registry; best-avail
    'CLAIM-P06-0078': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P06-0079': ('TAGGED', ['REF-00150', 'REF-00486'], None),

    # §6.7 — Kitchen
    'CLAIM-P06-0080': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P06-0081': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P06-0082': ('TAGGED', ['REF-00416', 'REF-00152'], None),
    'CLAIM-P06-0083': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P06-0084': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P06-0085': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P06-0086': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P06-0087': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P06-0088': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P06-0089': ('TAGGED', ['REF-00044', 'REF-00416'], None),
    'CLAIM-P06-0090': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P06-0091': ('DEFERRED', [], 'cross-reference parsing artifact — "760W" = 760mm Width in counter spec, not a unit value'),
    'CLAIM-P06-0092': ('TAGGED', ['REF-00044', 'REF-00052'], None),
    'CLAIM-P06-0093': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P06-0094': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P06-0095': ('TAGGED', ['REF-00044', 'REF-00154'], None),

    # §6.8 — Internal Circulation
    'CLAIM-P06-0096': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P06-0097': ('TAGGED', ['REF-00036', 'REF-00514'], None),
    'CLAIM-P06-0098': ('TAGGED', ['REF-00150', 'REF-00229'], None),
    'CLAIM-P06-0099': ('TAGGED', ['REF-00150', 'REF-00229'], None),
    'CLAIM-P06-0100': ('TAGGED', ['REF-00150', 'REF-00229'], None),
    'CLAIM-P06-0101': ('TAGGED', ['REF-00150', 'REF-00265'], None),
    'CLAIM-P06-0102': ('TAGGED', ['REF-00265', 'REF-00150'], None),
    'CLAIM-P06-0103': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P06-0104': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P06-0105': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P06-0106': ('TAGGED', ['REF-00150', 'REF-00265'], None),

    # §6.9 — Stair / Lift
    'CLAIM-P06-0107': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P06-0108': ('TAGGED', ['REF-00265', 'REF-00416'], None),
    'CLAIM-P06-0109': ('TAGGED', ['REF-00265', 'REF-00416'], None),
    'CLAIM-P06-0110': ('TAGGED', ['REF-00265', 'REF-00416'], None),
    'CLAIM-P06-0111': ('TAGGED', ['REF-00265', 'REF-00150'], None),
    'CLAIM-P06-0112': ('TAGGED', ['REF-00360', 'REF-00437'], None),
    'CLAIM-P06-0113': ('TAGGED', ['REF-00360', 'REF-00437'], None),
    'CLAIM-P06-0114': ('TAGGED', ['REF-00150', 'REF-00308'], None),

    # §6.10 — DAR summary row
    'CLAIM-P06-0115': ('TAGGED', ['REF-00265', 'REF-00150'], None),
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

pending_remaining = [c for c in data if c['part'] == 6 and c['status'] == 'PENDING']
print(f'TAGGED this session: {tagged_count}')
print(f'DEFERRED this session: {deferred_count}')
print(f'Still PENDING in Part 6: {len(pending_remaining)}')
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
