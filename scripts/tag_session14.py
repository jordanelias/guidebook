"""Session 14 tagging: Parts 1, 9, 10 — introduction methodology, checklist, DAR (40 claims)"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('references/claim-reference-join.json', encoding='utf-8') as f:
    data = json.load(f)

tagging = {
    # Part 1 §1.9.1 — Derivation methodology (dimensional specification provenance)
    'CLAIM-P01-0001': ('TAGGED', ['REF-00154', 'REF-00495'], None),   # 6 mm threshold
    'CLAIM-P01-0002': ('TAGGED', ['REF-00340', 'REF-00150'], None),   # 450–500 mm grab bar height
    'CLAIM-P01-0003': ('TAGGED', ['REF-00044', 'REF-00265'], None),   # 40% population figure
    'CLAIM-P01-0004': ('TAGGED', ['REF-00044', 'REF-00150'], None),   # 380 mm seat height
    'CLAIM-P01-0005': ('TAGGED', ['REF-00154', 'REF-00495'], None),   # 6 mm threshold (duplicate)
    'CLAIM-P01-0006': ('TAGGED', ['REF-00044', 'REF-00113'], None),   # 18% population figure
    'CLAIM-P01-0007': ('TAGGED', ['REF-00154', 'REF-00265'], None),   # 25 mm tolerance

    # Part 9 §9.9 — Thermal checklist (MS heat sensitivity)
    'CLAIM-P09-0001': ('TAGGED', ['REF-00014', 'REF-00388'], None),   # ≤18°C MS Uhthoff

    # Part 9 §9.11 — DeafBlind (DBL) design checklist
    'CLAIM-P09-0002': ('TAGGED', ['REF-00203', 'REF-00308'], None),   # ≥1500mm DBL corridor
    'CLAIM-P09-0003': ('TAGGED', ['REF-00306', 'REF-00203'], None),   # 900–1200mm tactile map zone
    'CLAIM-P09-0004': ('TAGGED', ['REF-00203', 'REF-00406'], None),   # ≤3 s response time
    'CLAIM-P09-0005': ('TAGGED', ['REF-00203', 'REF-00414'], None),   # ≤600 mm face-to-face
    'CLAIM-P09-0006': ('TAGGED', ['REF-00203', 'REF-00308'], None),   # ≥1500mm DBL route width
    'CLAIM-P09-0007': ('TAGGED', ['REF-00203', 'REF-00188'], None),   # ≥900mm intervenor zone
    'CLAIM-P09-0008': ('TAGGED', ['REF-00203', 'REF-00188'], None),   # 1500mm intervenor clear floor
    'CLAIM-P09-0009': ('TAGGED', ['REF-00414', 'REF-00203'], None),   # ≤600mm Protactile face-to-face
    'CLAIM-P09-0010': ('TAGGED', ['REF-00414', 'REF-00203'], None),   # ≥1500mm Protactile clear floor

    # Part 10 §10.1 — DAR structural provisions cost table
    'CLAIM-P10-0001': ('TAGGED', ['REF-00265', 'REF-00281'], None),   # 39% adapted need stat
    'CLAIM-P10-0002': ('TAGGED', ['REF-00311', 'REF-00150'], None),   # ≥3600mm hoist track run
    'CLAIM-P10-0003': ('TAGGED', ['REF-00173', 'REF-00265'], None),   # 1200mm lift structural zone
    'CLAIM-P10-0004': ('TAGGED', ['REF-00265', 'REF-00150'], None),   # ≥850mm stairlift stair width
    'CLAIM-P10-0005': ('TAGGED', ['REF-00154', 'REF-00265'], None),   # ≥950mm door structural opening

    # Part 10 §10.2 — DAR-01 to DAR-05 specification rows
    'CLAIM-P10-0006': ('TAGGED', ['REF-00154', 'REF-00265'], None),   # DAR-01 ≥950mm structural opening
    'CLAIM-P10-0007': ('TAGGED', ['REF-00154', 'REF-00265'], None),   # DAR-02 1400mm floor zone
    'CLAIM-P10-0008': ('TAGGED', ['REF-00340', 'REF-00150'], None),   # DAR-03 800–900mm grab bar AFF
    'CLAIM-P10-0009': ('TAGGED', ['REF-00340', 'REF-00311'], None),   # DAR-03 ≥135kg load capacity
    'CLAIM-P10-0010': ('TAGGED', ['REF-00150', 'REF-00265'], None),   # DAR-03 1800mm shower zone
    'CLAIM-P10-0011': ('TAGGED', ['REF-00311', 'REF-00340'], None),   # DAR-04 ≥135kg hoist SWL
    'CLAIM-P10-0012': ('TAGGED', ['REF-00311', 'REF-00150'], None),   # DAR-04 600mm hoist clearance
    'CLAIM-P10-0013': ('TAGGED', ['REF-00265', 'REF-00150'], None),   # DAR-05 ≥850mm stair width

    # Part 10 §10.3 — Housing stock accessibility statistics
    'CLAIM-P10-0014': ('TAGGED', ['REF-00265', 'REF-00281'], None),   # 12.6% accessible stock
    'CLAIM-P10-0015': ('TAGGED', ['REF-00265', 'REF-00281'], None),   # 3.3% statistic
    'CLAIM-P10-0016': ('TAGGED', ['REF-00265', 'REF-00281'], None),   # 41% statistic

    # Part 10 §10.4 — US visitability / Fair Housing minimum dimensions
    'CLAIM-P10-0017': ('TAGGED', ['REF-00492', 'REF-00494'], None),   # ≥815mm interior door
    'CLAIM-P10-0018': ('TAGGED', ['REF-00494', 'REF-00492'], None),   # ≥915mm hallway width
    'CLAIM-P10-0019': ('TAGGED', ['REF-00106', 'REF-00246'], None),   # <0.5% construction cost
    'CLAIM-P10-0020': ('TAGGED', ['REF-00494', 'REF-00492'], None),   # 815mm US Fair Housing

    # Part 10 §10.6 — Sweden BFS 2024:12 (Boverket) accessible apartment standard
    'CLAIM-P10-0021': ('TAGGED', ['REF-00308', 'REF-00150'], None),   # ≥850mm Boverket door width

    # Part 10 §10.7 — Programme evaluation case data
    'CLAIM-P10-0022': ('TAGGED', ['REF-00106', 'REF-00281'], None),   # 25% Kelsey Ayer Station DAR
    'CLAIM-P10-0023': ('TAGGED', ['REF-00281', 'REF-00333'], None),   # 30–40% HAFI BC Housing
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

pending_remaining = [c for c in data if c['status'] == 'PENDING']
print(f'TAGGED this session: {tagged_count}')
print(f'DEFERRED this session: {deferred_count}')
print(f'Still PENDING (all parts): {len(pending_remaining)}')
for c in pending_remaining:
    print(f'  MISSED: {c["claim_id"]} (Part {c["part"]})')

total = len(data)
all_tagged = sum(1 for c in data if c['status'] == 'TAGGED')
all_deferred = sum(1 for c in data if c['status'] == 'DEFERRED')
all_orphaned = sum(1 for c in data if c['status'] == 'ORPHANED')
all_pending = sum(1 for c in data if c['status'] == 'PENDING')
print(f'\nOverall: TAGGED={all_tagged} DEFERRED={all_deferred} ORPHANED={all_orphaned} PENDING={all_pending} TOTAL={total}')

with open('references/claim-reference-join.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('JSON written successfully')
