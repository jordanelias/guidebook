#!/usr/bin/env python3
"""Abstract-level rows for REF-01033..01037. usage: rows_lit.py check|dry|write"""
import sys, subprocess
sys.path.insert(0, 'scratchpad/session_2026-10-30-ramp-spec-pages-rebuild')
import rows_p12 as m

m.ROWS.clear()
ABS = 'Abstract read only (no full text); skimmed, so the finding sets no value and confirms nothing.'

VAL = {}

def f(key, p, ref, jur, text, sect, ctype='qualitative', val=None, unit=None, ident=None, needs=None, setting='ramp', notes=ABS, cmp=None, role='finding', rel=('none',)):
    val = val or VAL.get(key)
    m.add(key, p, ref, jur, val, unit, text, sect, dict(section='abstract'), notes, rel=rel, cmp=cmp, role=role, ctype=ctype,
          identity=ident, needs=needs, method='skim', setting=setting)

# REF-01033 Hashizume 2015 (proceedings chapter)
f('H-dist', 12, 'REF-01033', None, 'A mean oxygen uptake and heart rate were increased as the distance increased and their results indicated the extremely high exercise intensity at a final interval that were 1.2liter /min and 152bpm.',
  'Abstract (Crossref record)', val='the extremely high exercise intensity at a final interval', ident=None, needs='A-EFFORT',
  setting='long slope, 120 m at 8%, laboratory-measured',
  notes='Setting per the abstract: a 120 m, 8% slope. PROXY: sixteen unimpaired subjects (non-wheelchair users) propelled a wheelchair; the abstract gives no figure for wheelchair users on the long slope. It is the only held source measuring effort against distance on a slope, which is the quantity a rest landing interrupts. ' + ABS)
m.ROWS[-1]['ctype'] = 'qualitative'
f('H-cerv', 3, 'REF-01033', None, 'five wheelchair users with cervical cord injury were examined to evaluate the influence of different gradients (5%, 6.7%, 8.3%, 10% and 12.5%) with 3m length in laboratory',
  'Abstract (Crossref record)', ctype='range', val='5 to 12.5', unit='% gradient tested, 3 m long, five wheelchair users with cervical cord injury', ident='SCI', cmp='between', role='condition', setting='laboratory slope, 3 m',
  notes='The tested gradients are the condition; the abstract reports no result for this group, so no finding is recorded for it. ' + ABS)
# REF-01034 Lenker 2016
VAL['L-812'] = 'usable and acceptable for most participants'
f('L-812', 3, 'REF-01034', None, 'The 1:8 and 1:12 slopes were usable and acceptable for most participants.', 'Abstract (landing page)', ident='MOB',
  setting='transit bus boarding ramp (vehicle, not a building)', notes='Lens MOB is the wheelchair users among the participants; the sample also included people with vision impairment. 27 adults: manual wheelchair users, power wheelchair users, and people with vision impairment using a cane or service animal; four slopes, the abstract names 1:4, 1:8 and 1:12 only. ' + ABS)
VAL['L-14'] = 'too steep for safe unassisted boarding and disembarking'
f('L-14', 3, 'REF-01034', None, 'The data indicate that the 1:4 slope is too steep for safe unassisted boarding and disembarking.', 'Abstract (landing page)', ident='MOB',
  setting='transit bus boarding ramp (vehicle, not a building)', notes='Lens MOB is the wheelchair users among the participants; the sample also included people with vision impairment. A vehicle boarding ramp, so a steeper slope than a building ramp is in question. ' + ABS)
VAL['L-str'] = 'lacked the strength needed for unassisted ascent'
f('L-str', 3, 'REF-01034', None, 'Many manual wheelchair users lacked the strength needed for unassisted ascent.', 'Abstract (landing page)', ident='MOB',
  setting='transit bus boarding ramp (vehicle, not a building)', notes='Which slopes are meant is not stated in the abstract. ' + ABS)
# REF-01035 Har-Nir 2023
VAL['HN-up'] = 'most demanding effort was during uphill walking'
f('HN-up', 3, 'REF-01035', None, 'The most demanding effort was during uphill walking, with pwMS rating it more demanding compared with the healthy controls.', 'Abstract (PubMed record 36458477)', ident='MS',
  setting='treadmill, level, uphill and downhill walking',
  notes='Eighteen ambulatory people with multiple sclerosis (mean EDSS 2.9) and 23 healthy adults; slope not stated in the abstract. The abstract also reports that perceived effort did not follow energy expenditure. ' + ABS)
VAL['HN-perc'] = 'describe the effort of walking on different slopes higher than normal'
f('HN-perc', 3, 'REF-01035', None, 'pwMS describe the effort of walking on different slopes higher than normal, regardless of the energy expenditure values.', 'Abstract (PubMed record 36458477)', ident='MS', needs='A-EFFORT',
  setting='treadmill, level, uphill and downhill walking', notes=ABS)
# REF-01036 Liu 2023
VAL['Liu-RW'] = 'no differences were seen with cane use'
f('Liu-RW', 3, 'REF-01036', None, 'With the RW use, downward walking show a faster velocity, higher cadence, less stance time, bigger steps and strides than upward walking (p≤.05); but no differences were seen with cane use.', 'Abstract (PubMed record 37540908)', ident='MOB',
  setting='incline walking, rolling walker (RW) and cane',
  notes='Twenty-six older adults; the lens MOB (walking and balance limitation) is assigned from the use of a cane or rolling walker: the abstract names the group by age and device, and no identity in the vocabulary names older adults. Incline angle not stated in the abstract. ' + ABS)

m.ROWS[-1]['exempt'] = 'the persisted PubMed XML spells the less-than-or-equal sign as the character reference &#x2264; (p&#x2264;.05); the quote is the decoded text and the only mismatch is that spelling'

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'check':
        m.check()
    else:
        for r in m.ROWS:
            ar = m.argv(r, {}) + (['--dry-run'] if mode == 'dry' else [])
            p = subprocess.run(ar, capture_output=True, text=True)
            out = (p.stdout + p.stderr).strip()
            print(r['key'], 'param', r['param'], '->', 'ok' if p.returncode == 0 else 'FAIL ' + out[-350:])
            if p.returncode:
                sys.exit(1)
