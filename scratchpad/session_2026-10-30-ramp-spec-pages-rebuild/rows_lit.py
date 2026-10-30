#!/usr/bin/env python3
"""Abstract-level rows for REF-01033..01036 (v2, after the adversarial pass). usage: rows_lit.py check|dry|write"""
import sys
sys.path.insert(0, 'scratchpad/session_2026-10-30-ramp-spec-pages-rebuild')
import rows_p12 as m

m.ROWS.clear()
ABS = 'Abstract read only (no full text); skimmed, so the finding sets no value and confirms nothing.'
CERV_Q = ('five wheelchair users with cervical cord injury were examined to evaluate the influence of different gradients '
          '(5%, 6.7%, 8.3%, 10% and 12.5%) with 3m length in laboratory')
VAL = {}


def f(key, p, ref, text, sect, ctype='qualitative', val=None, unit=None, ident=None, needs=None, icf=None, setting='ramp',
      notes=ABS, cmp=None, role='finding', rel=('none',)):
    m.add(key, p, ref, None, val or VAL.get(key), unit, text, sect, dict(section='abstract'), notes, rel=rel, cmp=cmp, role=role,
          ctype=ctype, identity=ident, needs=needs, icf=icf, method='skim', setting=setting)


# REF-01033 Hashizume 2015 (proceedings chapter; PubMed 26294512, Crossref abstract identical)
f('H-cerv', 3, 'REF-01033', CERV_Q, 'Abstract (Crossref and PubMed records)', ctype='range', val='5 to 12.5', unit='%', ident='SCI',
  cmp='between', role='condition', setting='laboratory slope, 3 m',
  notes='Quantity: gradients tested, 3 m long, five wheelchair users with cervical cord injury. The tested gradients are the condition under which the two findings below hold. ' + ABS)
f('H-var', 3, 'REF-01033', 'the normalized power of subjects with cervical cord injury was significant difference between each subject in the ability to climb a slope',
  'Abstract (Crossref and PubMed records)', val='significant difference between each subject in the ability to climb a slope', ident='SCI',
  setting='laboratory slope, 3 m', rel=('condition_on', 'H-cerv', CERV_Q),
  notes='The between-person spread, not the mean, is what bears on a design value; the abstract sets no threshold. ' + ABS)
f('H-pow', 3, 'REF-01033', 'Mean normalized power were 0.23W/kg on a 5% slope, 0.24W/kg on 6.7%, and 0.26W/kg on 8.3% respectively.',
  'Abstract (Crossref and PubMed records)', val='Mean normalized power were 0.23W/kg on a 5% slope, 0.24W/kg on 6.7%, and 0.26W/kg on 8.3%', ident='SCI',
  setting='laboratory slope, 3 m', rel=('condition_on', 'H-cerv', CERV_Q),
  notes='Five people, so the means rest on n=5; no figure is given for 10% or 12.5%. ' + ABS)
f('H-dist', 12, 'REF-01033', 'A mean oxygen uptake and heart rate were increased as the distance increased and their results indicated the extremely high exercise intensity at a final interval that were 1.2liter /min and 152bpm.',
  'Abstract (Crossref and PubMed records)', val='the extremely high exercise intensity at a final interval', needs='A-EFFORT',
  setting='long sidewalk slope, 120 m at 8%',
  notes='PROXY: sixteen unimpaired subjects (non-wheelchair users) propelling a wheelchair on a 120 m, 8% slope (the abstract frames it as a sidewalk); no figure for wheelchair users on the long slope. It is the only held source measuring effort against distance on a slope, which is the quantity a rest landing interrupts. ' + ABS)
# REF-01034 Lenker 2016
LK = 'Lens MOB is the wheelchair users among the participants; the sample also included people with vision impairment. '
f('L-812', 3, 'REF-01034', 'The 1:8 and 1:12 slopes were usable and acceptable for most participants.', 'Abstract (landing page)', ident='MOB',
  val='usable and acceptable for most participants', setting='transit bus boarding ramp (vehicle, not a building)',
  notes=LK + '27 adults: manual wheelchair users, power wheelchair users, and people with vision impairment using a cane or service animal; four slopes, the abstract names 1:4, 1:8 and 1:12 only. ' + ABS)
f('L-14', 3, 'REF-01034', 'The data indicate that the 1:4 slope is too steep for safe unassisted boarding and disembarking.', 'Abstract (landing page)', ident='MOB',
  val='too steep for safe unassisted boarding and disembarking', setting='transit bus boarding ramp (vehicle, not a building)',
  notes=LK + 'A vehicle boarding ramp, so a steeper slope than a building ramp is in question. A failure finding. ' + ABS)
f('L-str', 3, 'REF-01034', 'Many manual wheelchair users lacked the strength needed for unassisted ascent.', 'Abstract (landing page)', ident='MOB',
  val='lacked the strength needed for unassisted ascent', setting='transit bus boarding ramp (vehicle, not a building)',
  notes='Which slopes are meant is not stated in the abstract. An inadequacy finding. ' + ABS)
# REF-01035 Har-Nir 2023
f('HN-up', 3, 'REF-01035', 'The most demanding effort was during uphill walking, with pwMS rating it more demanding compared with the healthy controls.',
  'Abstract (PubMed record 36458477)', ident='MS', val='most demanding effort was during uphill walking', setting='treadmill, level, uphill and downhill walking',
  notes='Eighteen ambulatory people with multiple sclerosis (mean EDSS 2.9) and 23 healthy adults; slope not stated in the abstract. ' + ABS)
f('HN-perc', 3, 'REF-01035', 'pwMS describe the effort of walking on different slopes higher than normal, regardless of the energy expenditure values.',
  'Abstract (PubMed record 36458477)', ident='MS', needs='A-EFFORT', val='describe the effort of walking on different slopes higher than normal',
  setting='treadmill, level, uphill and downhill walking', notes=ABS)
# REF-01036 Liu 2023: no identity lens; the participants are described only as 'qualified older adults'
f('Liu-RW', 3, 'REF-01036', 'With the RW use, downward walking show a faster velocity, higher cadence, less stance time, bigger steps and strides than upward walking (p≤.05); but no differences were seen with cane use.',
  'Abstract (PubMed record 37540908)', icf='d450', val='no differences were seen with cane use', setting='incline walking, rolling walker (RW) and cane',
  notes='Twenty-six "qualified" older adults each walked with a cane and a rolling walker as experimental conditions; the abstract states no impairment and no habitual device use, so no identity lens is attached (the functional lens d450, walking, is). Incline angle not stated. ' + ABS)
m.ROWS[-1]['exempt'] = 'the persisted PubMed XML spells the less-than-or-equal sign as the character reference &#x2264; (p&#x2264;.05); the quote is the decoded text and the only mismatch is that spelling'

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'check':
        m.check()
    else:
        m.run(mode)
