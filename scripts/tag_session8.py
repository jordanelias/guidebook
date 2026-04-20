"""Session 8 tagging: Parts 3 + 5 — conflict resolution (42 + 79 = 121 claims)"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('references/claim-reference-join.json', encoding='utf-8') as f:
    data = json.load(f)

tagging = {
    # === PART 3: Conflict Resolution Framework ===

    # part3-intro
    'CLAIM-P03-0001': ('DEFERRED', [], 'editorial evidence density metadata note'),

    # §3.1 — thermal conflict threshold
    'CLAIM-P03-0002': ('TAGGED', ['REF-00014', 'REF-00388'], None),

    # §3.2.3 — epidemiological multi-condition prevalence
    'CLAIM-P03-0003': ('TAGGED', ['REF-00333', 'REF-00388'], None),
    'CLAIM-P03-0004': ('TAGGED', ['REF-00333', 'REF-00388'], None),

    # §3.3 — OFS/MOB seating resolution
    'CLAIM-P03-0005': ('TAGGED', ['REF-00405', 'REF-00036'], None),

    # §3.6 — NDV educational prevalence
    'CLAIM-P03-0006': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P03-0007': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P03-0008': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P03-0009': ('TAGGED', ['REF-00029', 'REF-00124'], None),

    # §3.7 — point vs range conflict (grab bar diameter)
    'CLAIM-P03-0010': ('TAGGED', ['REF-00154', 'REF-00340'], None),

    # §3.9 — conflict resolution strategies
    'CLAIM-P03-0011': ('TAGGED', ['REF-00157', 'REF-00308'], None),
    'CLAIM-P03-0012': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P03-0013': ('TAGGED', ['REF-00154', 'REF-00340'], None),
    'CLAIM-P03-0014': ('TAGGED', ['REF-00154', 'REF-00340'], None),
    'CLAIM-P03-0015': ('TAGGED', ['REF-00154', 'REF-00340'], None),

    # §3.10 — multi-population conflict resolution tables
    'CLAIM-P03-0016': ('TAGGED', ['REF-00405', 'REF-00036'], None),
    'CLAIM-P03-0017': ('TAGGED', ['REF-00036', 'REF-00154'], None),
    'CLAIM-P03-0018': ('TAGGED', ['REF-00036', 'REF-00154'], None),
    'CLAIM-P03-0019': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P03-0020': ('TAGGED', ['REF-00154', 'REF-00340'], None),
    'CLAIM-P03-0021': ('TAGGED', ['REF-00340', 'REF-00154'], None),
    'CLAIM-P03-0022': ('TAGGED', ['REF-00157', 'REF-00405'], None),

    # §3.11 — applied case studies (memory care, office, school, acute care, mixed-tenure)
    'CLAIM-P03-0023': ('TAGGED', ['REF-00026', 'REF-00229'], None),
    'CLAIM-P03-0024': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P03-0025': ('TAGGED', ['REF-00229', 'REF-00360'], None),
    'CLAIM-P03-0026': ('TAGGED', ['REF-00026', 'REF-00229'], None),
    'CLAIM-P03-0027': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P03-0028': ('TAGGED', ['REF-00135', 'REF-00289'], None),
    'CLAIM-P03-0029': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P03-0030': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P03-0031': ('TAGGED', ['REF-00036', 'REF-00405'], None),
    'CLAIM-P03-0032': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P03-0033': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P03-0034': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P03-0035': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P03-0036': ('TAGGED', ['REF-00154', 'REF-00308'], None),
    'CLAIM-P03-0037': ('TAGGED', ['REF-00229', 'REF-00333'], None),
    'CLAIM-P03-0038': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P03-0039': ('TAGGED', ['REF-00229', 'REF-00437'], None),
    'CLAIM-P03-0040': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P03-0041': ('TAGGED', ['REF-00405', 'REF-00233'], None),
    'CLAIM-P03-0042': ('TAGGED', ['REF-00014', 'REF-00388'], None),

    # === PART 5: Conflict Resolution Application ===

    # §5.1 — range specification rationale (grab bar example)
    'CLAIM-P05-0001': ('TAGGED', ['REF-00154', 'REF-00340'], None),
    'CLAIM-P05-0002': ('TAGGED', ['REF-00154', 'REF-00340'], None),
    'CLAIM-P05-0003': ('TAGGED', ['REF-00154', 'REF-00340'], None),

    # §5.2 — COLOUR-CONT conflict
    'CLAIM-P05-0004': ('TAGGED', ['REF-00360', 'REF-00437'], None),
    'CLAIM-P05-0005': ('TAGGED', ['REF-00360', 'REF-00437'], None),
    'CLAIM-P05-0006': ('TAGGED', ['REF-00229', 'REF-00360'], None),

    # §5.2 — ACOUSTIC-LVL conflict
    'CLAIM-P05-0007': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P05-0008': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P05-0009': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P05-0010': ('TAGGED', ['REF-00142', 'REF-00124'], None),

    # §5.2 — GRAB BAR DIAMETER conflict
    'CLAIM-P05-0011': ('TAGGED', ['REF-00154', 'REF-00340'], None),
    'CLAIM-P05-0012': ('TAGGED', ['REF-00154', 'REF-00340'], None),
    'CLAIM-P05-0013': ('TAGGED', ['REF-00154', 'REF-00340'], None),
    'CLAIM-P05-0014': ('TAGGED', ['REF-00340', 'REF-00311'], None),
    'CLAIM-P05-0015': ('TAGGED', ['REF-00154', 'REF-00340'], None),
    'CLAIM-P05-0016': ('TAGGED', ['REF-00154', 'REF-00340'], None),
    'CLAIM-P05-0017': ('TAGGED', ['REF-00154', 'REF-00340'], None),
    'CLAIM-P05-0018': ('TAGGED', ['REF-00154', 'REF-00340'], None),
    'CLAIM-P05-0019': ('TAGGED', ['REF-00154', 'REF-00340'], None),

    # §5.2 — TEMP-RANGE conflict
    'CLAIM-P05-0020': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P05-0021': ('TAGGED', ['REF-00388', 'REF-00014'], None),
    'CLAIM-P05-0022': ('TAGGED', ['REF-00405', 'REF-00233'], None),
    'CLAIM-P05-0023': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P05-0024': ('TAGGED', ['REF-00014', 'REF-00388'], None),

    # §5.2 — SURFACE-TEXT conflict (TWSI)
    'CLAIM-P05-0025': ('TAGGED', ['REF-00306'], None),
    'CLAIM-P05-0026': ('TAGGED', ['REF-00306'], None),
    'CLAIM-P05-0027': ('TAGGED', ['REF-00306'], None),

    # §5.2 — SPATIAL-OPEN conflict (DeafSpace vs enclosure)
    'CLAIM-P05-0028': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P05-0029': ('TAGGED', ['REF-00135', 'REF-00308'], None),
    'CLAIM-P05-0030': ('TAGGED', ['REF-00135', 'REF-00248'], None),

    # §5.2 — LIGHT-INT conflict (multiple pops)
    'CLAIM-P05-0031': ('TAGGED', ['REF-00229', 'REF-00360'], None),
    'CLAIM-P05-0032': ('TAGGED', ['REF-00229', 'REF-00437'], None),
    'CLAIM-P05-0033': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P05-0034': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P05-0035': ('TAGGED', ['REF-00229', 'REF-00437'], None),
    'CLAIM-P05-0036': ('TAGGED', ['REF-00229', 'REF-00437'], None),
    'CLAIM-P05-0037': ('TAGGED', ['REF-00229', 'REF-00157'], None),
    'CLAIM-P05-0038': ('TAGGED', ['REF-00229', 'REF-00437'], None),
    'CLAIM-P05-0039': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P05-0040': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P05-0041': ('TAGGED', ['REF-00229', 'REF-00360'], None),
    'CLAIM-P05-0042': ('TAGGED', ['REF-00029', 'REF-00157'], None),

    # §5.2 — FRAGRANCE conflict
    'CLAIM-P05-0043': ('TAGGED', ['REF-00042', 'REF-00002'], None),

    # §5.2 — DOOR-OPERATION conflict
    'CLAIM-P05-0044': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P05-0045': ('TAGGED', ['REF-00308', 'REF-00157'], None),
    'CLAIM-P05-0046': ('TAGGED', ['REF-00308', 'REF-00494'], None),

    # §5.3 — resolved conflicts application
    'CLAIM-P05-0047': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P05-0048': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P05-0049': ('TAGGED', ['REF-00142', 'REF-00289'], None),
    'CLAIM-P05-0050': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P05-0051': ('TAGGED', ['REF-00135', 'REF-00308'], None),

    # §5.41 — memory care case study (DEM+MOB)
    'CLAIM-P05-0052': ('TAGGED', ['REF-00229', 'REF-00360'], None),
    'CLAIM-P05-0053': ('DEFERRED', [], 'OT evidence echo — repeats ≥300 lux DEM (CLAIM-P05-0052)'),
    'CLAIM-P05-0054': ('TAGGED', ['REF-00229', 'REF-00157'], None),
    'CLAIM-P05-0055': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P05-0056': ('TAGGED', ['REF-00026', 'REF-00229'], None),
    'CLAIM-P05-0057': ('DEFERRED', [], 'OT evidence echo — repeats ≥15m wandering loop (CLAIM-P05-0056)'),

    # §5.42 — co-working office case study (NDV+DEAF)
    'CLAIM-P05-0058': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P05-0059': ('TAGGED', ['REF-00135', 'REF-00289'], None),
    'CLAIM-P05-0060': ('TAGGED', ['REF-00289', 'REF-00142'], None),
    'CLAIM-P05-0061': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P05-0062': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P05-0063': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P05-0064': ('TAGGED', ['REF-00029', 'REF-00157'], None),

    # §5.43 — acute care / mixed-tenure case study
    'CLAIM-P05-0065': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P05-0066': ('TAGGED', ['REF-00014', 'REF-00388'], None),
    'CLAIM-P05-0067': ('TAGGED', ['REF-00014', 'REF-00405'], None),
    'CLAIM-P05-0068': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P05-0069': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P05-0070': ('TAGGED', ['REF-00026', 'REF-00229'], None),
    'CLAIM-P05-0071': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P05-0072': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P05-0073': ('TAGGED', ['REF-00044', 'REF-00494'], None),
    'CLAIM-P05-0074': ('TAGGED', ['REF-00044', 'REF-00154'], None),
    'CLAIM-P05-0075': ('TAGGED', ['REF-00014', 'REF-00388'], None),

    # §5.5.2 — MHIPI cost-of-modification evidence
    'CLAIM-P05-0076': ('TAGGED', ['REF-00333', 'REF-00265'], None),
    'CLAIM-P05-0077': ('TAGGED', ['REF-00265', 'REF-00333'], None),

    # §5.5.4 — RCT outcomes (Szanton 2019, Sheffield 2013 — best-available: MHIPI)
    'CLAIM-P05-0078': ('TAGGED', ['REF-00333'], None),
    'CLAIM-P05-0079': ('TAGGED', ['REF-00333'], None),
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

for p in [3, 5]:
    pending_remaining = [c for c in data if c['part'] == p and c['status'] == 'PENDING']
    print(f'Still PENDING in Part {p}: {len(pending_remaining)}')
    for c in pending_remaining:
        print(f'  MISSED: {c["claim_id"]}')

print(f'TAGGED this session: {tagged_count}')
print(f'DEFERRED this session: {deferred_count}')

total = len(data)
all_tagged = sum(1 for c in data if c['status'] == 'TAGGED')
all_deferred = sum(1 for c in data if c['status'] == 'DEFERRED')
all_orphaned = sum(1 for c in data if c['status'] == 'ORPHANED')
all_pending = sum(1 for c in data if c['status'] == 'PENDING')
print(f'\nOverall: TAGGED={all_tagged} DEFERRED={all_deferred} ORPHANED={all_orphaned} PENDING={all_pending} TOTAL={total}')

with open('references/claim-reference-join.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('JSON written successfully')
