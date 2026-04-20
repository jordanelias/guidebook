"""Session 11 tagging: Part 8 — engineering targets (116 claims)"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('references/claim-reference-join.json', encoding='utf-8') as f:
    data = json.load(f)

tagging = {
    # 9.1.2 — Acoustic engineering schedule (conceptual)
    'CLAIM-P08-0001': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P08-0002': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P08-0003': ('TAGGED', ['REF-00305', 'REF-00302'], None),
    'CLAIM-P08-0004': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P08-0005': ('TAGGED', ['REF-00142', 'REF-00218'], None),
    'CLAIM-P08-0006': ('TAGGED', ['REF-00029', 'REF-00142'], None),

    # 9.1.3 — Electrical engineering schedule (conceptual)
    'CLAIM-P08-0007': ('TAGGED', ['REF-00022', 'REF-00185'], None),
    'CLAIM-P08-0008': ('TAGGED', ['REF-00022', 'REF-00185'], None),
    'CLAIM-P08-0009': ('TAGGED', ['REF-00157', 'REF-00437'], None),
    'CLAIM-P08-0010': ('TAGGED', ['REF-00157', 'REF-00437'], None),
    'CLAIM-P08-0011': ('TAGGED', ['REF-00185', 'REF-00157'], None),
    'CLAIM-P08-0012': ('TAGGED', ['REF-00185', 'REF-00157'], None),
    'CLAIM-P08-0013': ('TAGGED', ['REF-00437', 'REF-00157'], None),
    'CLAIM-P08-0014': ('TAGGED', ['REF-00149', 'REF-00401'], None),
    'CLAIM-P08-0015': ('TAGGED', ['REF-00437', 'REF-00157'], None),
    'CLAIM-P08-0016': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P08-0017': ('TAGGED', ['REF-00437', 'REF-00150'], None),
    'CLAIM-P08-0018': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P08-0019': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P08-0020': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P08-0021': ('TAGGED', ['REF-00152', 'REF-00157'], None),
    'CLAIM-P08-0022': ('TAGGED', ['REF-00273', 'REF-00248'], None),
    'CLAIM-P08-0023': ('TAGGED', ['REF-00150', 'REF-00416'], None),

    # 9.1.4 — Mechanical engineering schedule (conceptual)
    'CLAIM-P08-0024': ('TAGGED', ['REF-00305', 'REF-00302'], None),
    'CLAIM-P08-0025': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P08-0026': ('TAGGED', ['REF-00042', 'REF-00304'], None),
    'CLAIM-P08-0027': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P08-0028': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P08-0029': ('TAGGED', ['REF-00304', 'REF-00322'], None),
    'CLAIM-P08-0030': ('TAGGED', ['REF-00042', 'REF-00304'], None),
    'CLAIM-P08-0031': ('TAGGED', ['REF-00303', 'REF-00184'], None),
    'CLAIM-P08-0032': ('TAGGED', ['REF-00371', 'REF-00388'], None),
    'CLAIM-P08-0033': ('TAGGED', ['REF-00371', 'REF-00388'], None),

    # 9.2.1 — Acoustic design stage (detailed)
    'CLAIM-P08-0034': ('TAGGED', ['REF-00142', 'REF-00218'], None),
    'CLAIM-P08-0035': ('TAGGED', ['REF-00142', 'REF-00218'], None),
    'CLAIM-P08-0036': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P08-0037': ('TAGGED', ['REF-00305', 'REF-00302'], None),
    'CLAIM-P08-0038': ('TAGGED', ['REF-00305', 'REF-00302'], None),
    'CLAIM-P08-0039': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P08-0040': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P08-0041': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P08-0042': ('TAGGED', ['REF-00029', 'REF-00142'], None),

    # 9.2.2 — Electrical design stage (detailed)
    'CLAIM-P08-0043': ('TAGGED', ['REF-00022', 'REF-00185'], None),
    'CLAIM-P08-0044': ('TAGGED', ['REF-00022', 'REF-00185'], None),
    'CLAIM-P08-0045': ('TAGGED', ['REF-00022', 'REF-00185'], None),
    'CLAIM-P08-0046': ('TAGGED', ['REF-00022', 'REF-00185'], None),
    'CLAIM-P08-0047': ('TAGGED', ['REF-00022', 'REF-00185'], None),
    'CLAIM-P08-0048': ('TAGGED', ['REF-00157', 'REF-00437'], None),
    'CLAIM-P08-0049': ('TAGGED', ['REF-00157', 'REF-00437'], None),
    'CLAIM-P08-0050': ('TAGGED', ['REF-00185', 'REF-00157'], None),
    'CLAIM-P08-0051': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P08-0052': ('TAGGED', ['REF-00185', 'REF-00157'], None),
    'CLAIM-P08-0053': ('TAGGED', ['REF-00185', 'REF-00157'], None),
    'CLAIM-P08-0054': ('TAGGED', ['REF-00437', 'REF-00229'], None),
    'CLAIM-P08-0055': ('TAGGED', ['REF-00437', 'REF-00229'], None),
    'CLAIM-P08-0056': ('TAGGED', ['REF-00437', 'REF-00157'], None),
    'CLAIM-P08-0057': ('TAGGED', ['REF-00437', 'REF-00157'], None),
    'CLAIM-P08-0058': ('TAGGED', ['REF-00149', 'REF-00401'], None),
    'CLAIM-P08-0059': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P08-0060': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P08-0061': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P08-0062': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P08-0063': ('TAGGED', ['REF-00152', 'REF-00157'], None),
    'CLAIM-P08-0064': ('TAGGED', ['REF-00273', 'REF-00248'], None),
    'CLAIM-P08-0065': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P08-0066': ('TAGGED', ['REF-00135', 'REF-00492'], None),
    'CLAIM-P08-0067': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P08-0068': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P08-0069': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P08-0070': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P08-0071': ('TAGGED', ['REF-00150', 'REF-00416'], None),
    'CLAIM-P08-0072': ('TAGGED', ['REF-00265', 'REF-00416'], None),
    'CLAIM-P08-0073': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P08-0074': ('TAGGED', ['REF-00289', 'REF-00142'], None),

    # 9.2.3 — Mechanical design stage (detailed)
    'CLAIM-P08-0075': ('TAGGED', ['REF-00142', 'REF-00305'], None),
    'CLAIM-P08-0076': ('TAGGED', ['REF-00142', 'REF-00305'], None),
    'CLAIM-P08-0077': ('TAGGED', ['REF-00305', 'REF-00302'], None),
    'CLAIM-P08-0078': ('TAGGED', ['REF-00305', 'REF-00302'], None),
    'CLAIM-P08-0079': ('TAGGED', ['REF-00305', 'REF-00302'], None),
    'CLAIM-P08-0080': ('TAGGED', ['REF-00042', 'REF-00304'], None),
    'CLAIM-P08-0081': ('TAGGED', ['REF-00304', 'REF-00322'], None),
    'CLAIM-P08-0082': ('TAGGED', ['REF-00042', 'REF-00304'], None),
    'CLAIM-P08-0083': ('TAGGED', ['REF-00492', 'REF-00152'], None),
    'CLAIM-P08-0084': ('TAGGED', ['REF-00303', 'REF-00184'], None),
    'CLAIM-P08-0085': ('TAGGED', ['REF-00371', 'REF-00388'], None),
    'CLAIM-P08-0086': ('TAGGED', ['REF-00014', 'REF-00371'], None),
    'CLAIM-P08-0087': ('TAGGED', ['REF-00371', 'REF-00388'], None),

    # 9.3.3 — Construction/commissioning phase
    'CLAIM-P08-0088': ('TAGGED', ['REF-00305', 'REF-00302'], None),
    'CLAIM-P08-0089': ('TAGGED', ['REF-00371', 'REF-00388'], None),

    # 9.5 — Structural provisions
    'CLAIM-P08-0090': ('TAGGED', ['REF-00340', 'REF-00150'], None),
    'CLAIM-P08-0091': ('TAGGED', ['REF-00150', 'REF-00340'], None),
    'CLAIM-P08-0092': ('TAGGED', ['REF-00311', 'REF-00416'], None),

    # 9.6.2 — DBL coordination zones
    'CLAIM-P08-0093': ('TAGGED', ['REF-00203', 'REF-00188'], None),
    'CLAIM-P08-0094': ('TAGGED', ['REF-00203', 'REF-00188'], None),
    'CLAIM-P08-0095': ('TAGGED', ['REF-00203', 'REF-00188'], None),

    # 9.6.3 — DBL communication clearances
    'CLAIM-P08-0096': ('TAGGED', ['REF-00414', 'REF-00203'], None),
    'CLAIM-P08-0097': ('TAGGED', ['REF-00414', 'REF-00203'], None),
    'CLAIM-P08-0098': ('TAGGED', ['REF-00414', 'REF-00203'], None),
    'CLAIM-P08-0099': ('TAGGED', ['REF-00306', 'REF-00203'], None),
    'CLAIM-P08-0100': ('TAGGED', ['REF-00414', 'REF-00203'], None),
    'CLAIM-P08-0101': ('TAGGED', ['REF-00203', 'REF-00188'], None),
    'CLAIM-P08-0102': ('TAGGED', ['REF-00203', 'REF-00188'], None),
    'CLAIM-P08-0103': ('TAGGED', ['REF-00203', 'REF-00188'], None),
    'CLAIM-P08-0104': ('TAGGED', ['REF-00203', 'REF-00406'], None),
    'CLAIM-P08-0105': ('TAGGED', ['REF-00203', 'REF-00406'], None),
    'CLAIM-P08-0106': ('TAGGED', ['REF-00203', 'REF-00406'], None),
    'CLAIM-P08-0107': ('TAGGED', ['REF-00203', 'REF-00308'], None),
    'CLAIM-P08-0108': ('TAGGED', ['REF-00203', 'REF-00406'], None),
    'CLAIM-P08-0109': ('TAGGED', ['REF-00414', 'REF-00203'], None),

    # §8.1.4 — Thermal envelope engineering
    'CLAIM-P08-0110': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P08-0111': ('TAGGED', ['REF-00518', 'REF-00303'], None),
    'CLAIM-P08-0112': ('TAGGED', ['REF-00518', 'REF-00303'], None),
    'CLAIM-P08-0113': ('TAGGED', ['REF-00303', 'REF-00518'], None),
    'CLAIM-P08-0114': ('TAGGED', ['REF-00303', 'REF-00014'], None),
    'CLAIM-P08-0115': ('TAGGED', ['REF-00303', 'REF-00518'], None),
    'CLAIM-P08-0116': ('TAGGED', ['REF-00303', 'REF-00388'], None),
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

pending_remaining = [c for c in data if c['part'] == 8 and c['status'] == 'PENDING']
print(f'TAGGED this session: {tagged_count}')
print(f'DEFERRED this session: {deferred_count}')
print(f'Still PENDING in Part 8: {len(pending_remaining)}')
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
