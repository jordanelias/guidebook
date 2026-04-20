"""Session 13 tagging: Part 12 — case studies (47 claims)"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('references/claim-reference-join.json', encoding='utf-8') as f:
    data = json.load(f)

tagging = {
    # §12.01 — NHS Highland dementia residential home (dementia design, RHFAC)
    'CLAIM-P12-0001': ('TAGGED', ['REF-00229', 'REF-00150'], None),
    'CLAIM-P12-0002': ('TAGGED', ['REF-00432', 'REF-00229'], None),

    # §12.02 — Gallaudet University (DeafSpace)
    'CLAIM-P12-0003': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P12-0004': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P12-0005': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P12-0006': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P12-0007': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P12-0008': ('TAGGED', ['REF-00135', 'REF-00248'], None),

    # §12.03 — Kelsey Coalition housing (RHFAC Exceptional Access Level)
    'CLAIM-P12-0009': ('TAGGED', ['REF-00432', 'REF-00154'], None),
    'CLAIM-P12-0010': ('TAGGED', ['REF-00432', 'REF-00265'], None),
    'CLAIM-P12-0011': ('TAGGED', ['REF-00432', 'REF-00265'], None),
    'CLAIM-P12-0012': ('TAGGED', ['REF-00432', 'REF-00265'], None),
    'CLAIM-P12-0013': ('TAGGED', ['REF-00106', 'REF-00281'], None),

    # §12.04 — Dementia care facility (loop floor plan, acoustic)
    'CLAIM-P12-0014': ('TAGGED', ['REF-00142', 'REF-00229'], None),
    'CLAIM-P12-0015': ('TAGGED', ['REF-00292', 'REF-00106'], None),

    # §12.05 — Neurodivergent workplace (sensory gradient, ASPECTSS)
    'CLAIM-P12-0016': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P12-0017': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P12-0018': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P12-0019': ('TAGGED', ['REF-00029', 'REF-00157'], None),
    'CLAIM-P12-0020': ('TAGGED', ['REF-00029', 'REF-00157'], None),

    # §12.06 — Dementia specialist school retrofit (1980s building)
    'CLAIM-P12-0021': ('DEFERRED', [], 'building age descriptor — contextual date, not a citable design specification'),
    'CLAIM-P12-0022': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P12-0023': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P12-0024': ('TAGGED', ['REF-00142', 'REF-00029'], None),
    'CLAIM-P12-0025': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P12-0026': ('DEFERRED', [], 'measurement methodology — 500 Hz is standard octave band per ISO 3382-2, not a design claim'),

    # §12.07 — Singapore BCA Universal Design Index (HDB housing)
    'CLAIM-P12-0027': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P12-0028': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P12-0029': ('TAGGED', ['REF-00308', 'REF-00494'], None),
    'CLAIM-P12-0030': ('TAGGED', ['REF-00106', 'REF-00246'], None),
    'CLAIM-P12-0031': ('TAGGED', ['REF-00106', 'REF-00246'], None),

    # §12.08 — DeafSpace / dementia corridor case study (video-confirmed 1800mm)
    'CLAIM-P12-0032': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P12-0033': ('TAGGED', ['REF-00142', 'REF-00124'], None),
    'CLAIM-P12-0034': ('TAGGED', ['REF-00135', 'REF-00248'], None),
    'CLAIM-P12-0035': ('TAGGED', ['REF-00135', 'REF-00248'], None),

    # §12.09 — De Hogeweyk dementia village
    'CLAIM-P12-0036': ('TAGGED', ['REF-00512', 'REF-00229'], None),
    'CLAIM-P12-0037': ('TAGGED', ['REF-00512', 'REF-00229'], None),
    'CLAIM-P12-0038': ('TAGGED', ['REF-00512', 'REF-00229'], None),

    # §12.10 — Acoustic dementia intervention study
    'CLAIM-P12-0039': ('TAGGED', ['REF-00029', 'REF-00142'], None),
    'CLAIM-P12-0040': ('TAGGED', ['REF-00292', 'REF-00106'], None),

    # §12.11 — ASPECTSS retrofit classroom study
    'CLAIM-P12-0041': ('TAGGED', ['REF-00142', 'REF-00029'], None),
    'CLAIM-P12-0042': ('TAGGED', ['REF-00142', 'REF-00029'], None),

    # §12.12 — Korian/University of Bordeaux programme evaluation
    'CLAIM-P12-0043': ('TAGGED', ['REF-00229', 'REF-00297'], None),

    # §12.14 — HAFI / BC Housing home adaptation programme (Canada)
    'CLAIM-P12-0044': ('TAGGED', ['REF-00281', 'REF-00333'], None),
    'CLAIM-P12-0045': ('TAGGED', ['REF-00281', 'REF-00333'], None),
    'CLAIM-P12-0046': ('TAGGED', ['REF-00281', 'REF-00333'], None),
    'CLAIM-P12-0047': ('DEFERRED', [], 'editorial cross-reference note — not a standalone citable claim'),
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

pending_remaining = [c for c in data if c['part'] == 12 and c['status'] == 'PENDING']
print(f'TAGGED this session: {tagged_count}')
print(f'DEFERRED this session: {deferred_count}')
print(f'Still PENDING in Part 12: {len(pending_remaining)}')
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
