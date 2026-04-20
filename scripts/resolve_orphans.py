"""Resolve resolvable ORPHANED claims — Part 4 cleanup pass.

Upgrades 9 ORPHANED → TAGGED where a registry ref is now available:
  - P04-0045/0046 (De Hogeweyk 94%/34%): REF-00512 now in registry
    (same decision applied to P12-0037/0038 in Session 13)
  - P04-0065–0071 (Leavitt 2014 / Davis 2010 MS cooling / Uhthoff):
    best-available REF-00014 (Flensner 2011) + REF-00388 (MSIF Atlas 2023)
    — consistent with all other Part 4 MS thermal claims (F-07, G-06, etc.)

Remaining ORPHANED (12) kept:
  - P04-0011: Kaplan 1989 restorative interval — no acoustic BPC ref; GAP-OPS-01
  - P04-0029: BS 6472-1:2008 vibration threshold — UNVERIFIED; GAP-IMPL-05
  - P07-0020,0022,0023,0036,0047,0048,0073,0077,0078,0105:
    DBL/IntD expert-consensus — explicitly "no standard; March 2026" in source
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('references/claim-reference-join.json', encoding='utf-8') as f:
    data = json.load(f)

upgrades = {
    # De Hogeweyk — REF-00512 confirmed in registry (UNVERIFIABLE tag, but present)
    'CLAIM-P04-0045': (['REF-00512', 'REF-00229'], 'De Hogeweyk REF-00512 now in registry [UNVERIFIABLE internal doc]; consistent with P12-0037 treatment'),
    'CLAIM-P04-0046': (['REF-00512', 'REF-00229'], 'De Hogeweyk REF-00512 now in registry [UNVERIFIABLE internal doc]; consistent with P12-0038 treatment'),

    # Leavitt 2014 / Davis 2010 MS cooling — best-available (not in registry)
    # Flensner 2011 (REF-00014) covers Uhthoff's phenomenon; MSIF Atlas (REF-00388) covers MS heat sensitivity
    'CLAIM-P04-0065': (['REF-00014', 'REF-00388'], 'Leavitt 2014 + Davis 2010 not in registry; best-available: Flensner 2011 Uhthoff + MSIF Atlas heat sensitivity'),
    'CLAIM-P04-0066': (['REF-00014', 'REF-00388'], 'Leavitt 2014 + Davis 2010 not in registry; best-available: Flensner 2011 + MSIF Atlas'),
    'CLAIM-P04-0067': (['REF-00014', 'REF-00388'], 'Leavitt 2014 + Davis 2010 not in registry; best-available: Flensner 2011 + MSIF Atlas'),
    'CLAIM-P04-0068': (['REF-00014', 'REF-00388'], 'Leavitt 2014 + Davis 2010 not in registry; best-available: Flensner 2011 + MSIF Atlas'),
    'CLAIM-P04-0069': (['REF-00014', 'REF-00388'], 'Leavitt 2014 + Davis 2010 not in registry; best-available: Flensner 2011 + MSIF Atlas'),
    'CLAIM-P04-0070': (['REF-00014', 'REF-00388'], 'Leavitt 2014 + Davis 2010 not in registry; best-available: Flensner 2011 + MSIF Atlas'),
    'CLAIM-P04-0071': (['REF-00014', 'REF-00388'], 'Leavitt 2014 + Davis 2010 not in registry; best-available: Flensner 2011 + MSIF Atlas'),
}

resolved = 0
for claim in data:
    cid = claim['claim_id']
    if cid in upgrades and claim['status'] == 'ORPHANED':
        refs, note = upgrades[cid]
        claim['status'] = 'TAGGED'
        claim['ref_ids'] = refs
        claim['note'] = note
        resolved += 1

remaining = [c for c in data if c['status'] == 'ORPHANED']
all_tagged = sum(1 for c in data if c['status'] == 'TAGGED')
all_deferred = sum(1 for c in data if c['status'] == 'DEFERRED')
all_orphaned = sum(1 for c in data if c['status'] == 'ORPHANED')
all_pending = sum(1 for c in data if c['status'] == 'PENDING')

print(f'Resolved ORPHANED → TAGGED: {resolved}')
print(f'Remaining ORPHANED: {len(remaining)}')
for c in remaining:
    print(f'  {c["claim_id"]} | {c["scope"]} | {c["claim_value"]} | {c.get("note","")}')
print(f'\nOverall: TAGGED={all_tagged} DEFERRED={all_deferred} ORPHANED={all_orphaned} PENDING={all_pending} TOTAL={len(data)}')

with open('references/claim-reference-join.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('JSON written successfully')
