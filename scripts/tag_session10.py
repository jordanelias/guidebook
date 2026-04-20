"""Session 10 tagging: Part 7 — non-residential design matrices (111 claims)"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('references/claim-reference-join.json', encoding='utf-8') as f:
    data = json.load(f)

tagging = {
    # §7.0 — whole-building non-residential summary rows
    'CLAIM-P07-0001': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P07-0002': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P07-0003': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P07-0004': ('TAGGED', ['REF-00371', 'REF-00388'], None),
    'CLAIM-P07-0005': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P07-0006': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P07-0007': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P07-0008': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P07-0009': ('TAGGED', ['REF-00036', 'REF-00514'], None),

    # §7.1 — Education
    'CLAIM-P07-0010': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P07-0011': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P07-0012': ('TAGGED', ['REF-00157', 'REF-00029'], None),
    'CLAIM-P07-0013': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P07-0014': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P07-0015': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P07-0016': ('TAGGED', ['REF-00124', 'REF-00142'], None),
    'CLAIM-P07-0017': ('TAGGED', ['REF-00124', 'REF-00289'], None),
    'CLAIM-P07-0018': ('TAGGED', ['REF-00157', 'REF-00029'], None),
    'CLAIM-P07-0019': ('TAGGED', ['REF-00157', 'REF-00044'], None),
    'CLAIM-P07-0020': ('ORPHANED', [], None),  # EXPERT CONSENSUS — no standard
    'CLAIM-P07-0021': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P07-0022': ('ORPHANED', [], None),  # DEM/NDV[IntD-proxy] — TIER 4–5; no standard
    'CLAIM-P07-0023': ('ORPHANED', [], None),  # DEM/NDV[IntD-proxy] — TIER 4–5; no standard
    'CLAIM-P07-0024': ('TAGGED', ['REF-00157', 'REF-00029'], None),
    'CLAIM-P07-0025': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P07-0026': ('TAGGED', ['REF-00041', 'REF-00303'], None),
    'CLAIM-P07-0027': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P07-0028': ('TAGGED', ['REF-00308', 'REF-00494'], None),

    # §7.2 — Health
    'CLAIM-P07-0029': ('TAGGED', ['REF-00150', 'REF-00229'], None),
    'CLAIM-P07-0030': ('TAGGED', ['REF-00303', 'REF-00518'], None),
    'CLAIM-P07-0031': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P07-0032': ('DEFERRED', [], 'cross-reference parsing artifact — "13 min" = MERV-13 filter rating misextracted as time value'),
    'CLAIM-P07-0033': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P07-0034': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P07-0035': ('TAGGED', ['REF-00014', 'REF-00371'], None),
    'CLAIM-P07-0036': ('ORPHANED', [], None),  # EXPERT CONSENSUS — no standard
    'CLAIM-P07-0037': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P07-0038': ('TAGGED', ['REF-00041', 'REF-00303'], None),
    'CLAIM-P07-0039': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P07-0040': ('TAGGED', ['REF-00308', 'REF-00494'], None),

    # §7.3 — Workplace / Office
    'CLAIM-P07-0041': ('TAGGED', ['REF-00405', 'REF-00029'], None),
    'CLAIM-P07-0042': ('TAGGED', ['REF-00041', 'REF-00388'], None),
    'CLAIM-P07-0043': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P07-0044': ('TAGGED', ['REF-00157', 'REF-00029'], None),
    'CLAIM-P07-0045': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P07-0046': ('TAGGED', ['REF-00124', 'REF-00142'], None),
    'CLAIM-P07-0047': ('ORPHANED', [], None),  # EXPERT CONSENSUS — no standard
    'CLAIM-P07-0048': ('ORPHANED', [], None),  # DEM/NDV[IntD-proxy] — TIER 4–5; no standard
    'CLAIM-P07-0049': ('TAGGED', ['REF-00157', 'REF-00029'], None),
    'CLAIM-P07-0050': ('TAGGED', ['REF-00142', 'REF-00157'], None),
    'CLAIM-P07-0051': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P07-0052': ('TAGGED', ['REF-00041', 'REF-00303'], None),
    'CLAIM-P07-0053': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P07-0054': ('TAGGED', ['REF-00308', 'REF-00494'], None),

    # §7.4 — Retail
    'CLAIM-P07-0055': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P07-0056': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P07-0057': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P07-0058': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P07-0059': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P07-0060': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P07-0061': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P07-0062': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P07-0063': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P07-0064': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P07-0065': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P07-0066': ('TAGGED', ['REF-00416', 'REF-00052'], None),
    'CLAIM-P07-0067': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P07-0068': ('TAGGED', ['REF-00041', 'REF-00303'], None),
    'CLAIM-P07-0069': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P07-0070': ('TAGGED', ['REF-00308', 'REF-00494'], None),

    # §7.5 — Civic / Cultural (library, theatre, museum, place of worship)
    'CLAIM-P07-0071': ('TAGGED', ['REF-00142', 'REF-00218'], None),
    'CLAIM-P07-0072': ('TAGGED', ['REF-00494', 'REF-00308'], None),
    'CLAIM-P07-0073': ('ORPHANED', [], None),  # EXPERT CONSENSUS — no standard
    'CLAIM-P07-0074': ('TAGGED', ['REF-00494', 'REF-00308'], None),
    'CLAIM-P07-0075': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P07-0076': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P07-0077': ('ORPHANED', [], None),  # EXPERT CONSENSUS — no standard
    'CLAIM-P07-0078': ('ORPHANED', [], None),  # EXPERT CONSENSUS — no standard
    'CLAIM-P07-0079': ('TAGGED', ['REF-00494', 'REF-00308'], None),
    'CLAIM-P07-0080': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P07-0081': ('TAGGED', ['REF-00041', 'REF-00303'], None),
    'CLAIM-P07-0082': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P07-0083': ('TAGGED', ['REF-00308', 'REF-00494'], None),

    # §7.6 — Hospitality / Leisure (hotel, restaurant, pool)
    'CLAIM-P07-0084': ('TAGGED', ['REF-00371', 'REF-00388'], None),
    'CLAIM-P07-0085': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P07-0086': ('TAGGED', ['REF-00150', 'REF-00308'], None),
    'CLAIM-P07-0087': ('TAGGED', ['REF-00494', 'REF-00308'], None),
    'CLAIM-P07-0088': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P07-0089': ('TAGGED', ['REF-00142', 'REF-00218'], None),
    'CLAIM-P07-0090': ('TAGGED', ['REF-00142', 'REF-00218'], None),
    'CLAIM-P07-0091': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P07-0092': ('TAGGED', ['REF-00494', 'REF-00308'], None),
    'CLAIM-P07-0093': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P07-0094': ('TAGGED', ['REF-00041', 'REF-00303'], None),
    'CLAIM-P07-0095': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P07-0096': ('TAGGED', ['REF-00308', 'REF-00494'], None),

    # §7.7 — Transport / Transit
    'CLAIM-P07-0097': ('TAGGED', ['REF-00157', 'REF-00437'], None),
    'CLAIM-P07-0098': ('TAGGED', ['REF-00273', 'REF-00289'], None),
    'CLAIM-P07-0099': ('TAGGED', ['REF-00157', 'REF-00437'], None),
    'CLAIM-P07-0100': ('DEFERRED', [], 'cross-reference parsing artifact — "000 lux" = ≥1000 lux exterior luminance misextracted'),
    'CLAIM-P07-0101': ('TAGGED', ['REF-00437', 'REF-00229'], None),
    'CLAIM-P07-0102': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P07-0103': ('TAGGED', ['REF-00306', 'REF-00437'], None),
    'CLAIM-P07-0104': ('TAGGED', ['REF-00306', 'REF-00494'], None),
    'CLAIM-P07-0105': ('ORPHANED', [], None),  # EXPERT CONSENSUS — no standard
    'CLAIM-P07-0106': ('TAGGED', ['REF-00157', 'REF-00437'], None),
    'CLAIM-P07-0107': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P07-0108': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P07-0109': ('TAGGED', ['REF-00041', 'REF-00303'], None),
    'CLAIM-P07-0110': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P07-0111': ('TAGGED', ['REF-00308', 'REF-00494'], None),
}

tagged_count = 0
deferred_count = 0
orphaned_count = 0

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
        elif status == 'ORPHANED':
            orphaned_count += 1

pending_remaining = [c for c in data if c['part'] == 7 and c['status'] == 'PENDING']
print(f'TAGGED this session: {tagged_count}')
print(f'DEFERRED this session: {deferred_count}')
print(f'ORPHANED this session: {orphaned_count}')
print(f'Still PENDING in Part 7: {len(pending_remaining)}')
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
