#!/usr/bin/env python3
"""
Session 3 — Part 4 Category D+E citation tagging
Tags 193 claims across D-01–D-11 and E-01–E-15/E-10/E-12/E-13
"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

T = 'TAGGED'
D = 'DEFERRED'

# (status, ref_ids list)
TAGS = {
    # ── D-01 Loop floor plan ──
    'CLAIM-P04-0115': (T, ['REF-00026', 'REF-00229']),   # loop corridor ≤5m dead-end

    # ── D-02 Single primary route ──
    'CLAIM-P04-0116': (T, ['REF-00409', 'REF-00047']),   # 20m cognitive route limit

    # ── D-03 Toilet visibility ──
    'CLAIM-P04-0117': (T, ['REF-00026', 'REF-00229']),   # 1600mm sightline height
    'CLAIM-P04-0118': (T, ['REF-00026', 'REF-00229']),   # 1600mm sightline spec
    'CLAIM-P04-0119': (T, ['REF-00405', 'REF-00026']),   # ≤20m MS bladder urgency
    'CLAIM-P04-0120': (T, ['REF-00361']),                 # 47% toilet-finding figure (Marquardt wayfinding)
    'CLAIM-P04-0121': (D, []),    # OT evidence echo — repeats ≤20m spec
    'CLAIM-P04-0122': (D, []),    # OT evidence echo — repeats 20m spec

    # ── D-04 Landmarks at decision points ──
    'CLAIM-P04-0123': (T, ['REF-00409', 'REF-00026']),   # ≥5m visible landmark
    'CLAIM-P04-0124': (T, ['REF-00409', 'REF-00026']),   # ≥5m approach visibility

    # ── D-05 Enclosed low-stimulation spaces ──
    'CLAIM-P04-0125': (T, ['REF-00157', 'REF-00232']),   # ≤0.4s RT60 in description
    'CLAIM-P04-0126': (T, ['REF-00157', 'REF-00232']),   # ≤0.4s RT60 spec
    'CLAIM-P04-0127': (T, ['REF-00157']),                 # 100% dimming range
    'CLAIM-P04-0128': (T, ['REF-00157']),                 # 10 lux minimum dim
    'CLAIM-P04-0129': (T, ['REF-00232']),                 # 300mm proprioceptive floor zone (Dunn NDV)

    # ── D-06 Memory boxes ──
    'CLAIM-P04-0130': (T, ['REF-00229', 'REF-00026']),   # 300mm shadow box (description)
    'CLAIM-P04-0131': (T, ['REF-00229']),                 # 300×300mm shadow box spec
    'CLAIM-P04-0132': (T, ['REF-00229', 'REF-00026']),   # 1500mm AFF mounting height

    # ── D-07 No blind corners ──
    'CLAIM-P04-0133': (T, ['REF-00026', 'REF-00248']),   # 300mm treatment (description)
    'CLAIM-P04-0134': (T, ['REF-00026']),                 # ≥300mm mirror
    'CLAIM-P04-0135': (T, ['REF-00026', 'REF-00248']),   # 2m approach sightline

    # ── D-08 Pictogram + single-word signage ──
    'CLAIM-P04-0136': (T, ['REF-00151', 'REF-00199']),   # ≥150mm character height (description)
    'CLAIM-P04-0137': (T, ['REF-00151', 'REF-00199']),   # 10m viewing distance
    'CLAIM-P04-0138': (T, ['REF-00151', 'REF-00199']),   # 50mm pictogram height
    'CLAIM-P04-0139': (T, ['REF-00151', 'REF-00199']),   # ≥150mm at 10m spec
    'CLAIM-P04-0140': (T, ['REF-00151']),                 # 10m viewing distance spec
    'CLAIM-P04-0141': (T, ['REF-00151', 'REF-00437']),   # 1600mm AFF Braille
    'CLAIM-P04-0142': (T, ['REF-00151', 'REF-00437']),   # 0.8mm raised lettering
    'CLAIM-P04-0143': (T, ['REF-00151', 'REF-00437']),   # 1600mm AFF tactile lettering

    # ── D-10 Transparent glazed panels ──
    'CLAIM-P04-0144': (T, ['REF-00135', 'REF-00248']),   # 1000mm vision panel height
    'CLAIM-P04-0145': (T, ['REF-00135', 'REF-00248']),   # 1800mm AFF panel position
    'CLAIM-P04-0146': (D, []),    # "Class 2 minimum" — glazing standard cross-ref (BS EN 12600 not in registry)

    # ── D-11 Safe accessible garden ──
    'CLAIM-P04-0147': (T, ['REF-00026', 'REF-00229']),   # 20m loop path
    'CLAIM-P04-0148': (T, ['REF-00026', 'REF-00015']),   # 20m seating interval (Gonzalez sensory garden)
    'CLAIM-P04-0149': (T, ['REF-00044', 'REF-00265']),   # 450mm seat height
    'CLAIM-P04-0150': (T, ['REF-00026', 'REF-00229']),   # ≤20m key evidence (non-English Danish)
    'CLAIM-P04-0151': (D, []),    # date reference "1990s" in key evidence text

    # ── E-01 Accessible lift ──
    'CLAIM-P04-0152': (T, ['REF-00173', 'REF-00151']),   # 1400mm car depth (description)
    'CLAIM-P04-0153': (T, ['REF-00173', 'REF-00151']),   # 1100mm car width
    'CLAIM-P04-0154': (T, ['REF-00173', 'REF-00151']),   # ≥900mm door clear width
    'CLAIM-P04-0155': (T, ['REF-00173', 'REF-00151']),   # 1200mm controls AFF
    'CLAIM-P04-0156': (T, ['REF-00173', 'REF-00151']),   # ≥1400mm car deep spec
    'CLAIM-P04-0157': (T, ['REF-00173', 'REF-00151']),   # 1100mm car wide spec
    'CLAIM-P04-0158': (T, ['REF-00173', 'REF-00151']),   # ≥900mm door spec
    'CLAIM-P04-0159': (T, ['REF-00173', 'REF-00151']),   # 1200mm controls
    'CLAIM-P04-0160': (T, ['REF-00173']),                 # ≥50mm push-pad
    'CLAIM-P04-0161': (D, []),    # OT evidence echo — 1100mm WC biomechanics

    # ── E-02 Platform lift ──
    'CLAIM-P04-0162': (T, ['REF-00173', 'REF-00370']),   # 1400mm platform lift (description)
    'CLAIM-P04-0163': (T, ['REF-00173', 'REF-00370']),   # 2m max travel
    'CLAIM-P04-0164': (T, ['REF-00173']),                 # 0.15m/s max speed
    'CLAIM-P04-0165': (T, ['REF-00173']),                 # 1400mm car minimum spec
    'CLAIM-P04-0166': (T, ['REF-00173', 'REF-00370']),   # 2m maximum travel spec
    'CLAIM-P04-0167': (T, ['REF-00173']),                 # 0.15m/s speed spec
    'CLAIM-P04-0168': (D, []),    # OT evidence echo — 1400mm/2m specs
    'CLAIM-P04-0169': (D, []),    # OT evidence echo — 2m spec

    # ── E-03 Ramp gradient ──
    'CLAIM-P04-0170': (T, ['REF-00151', 'REF-00370']),   # 9m max continuous run
    'CLAIM-P04-0171': (T, ['REF-00151', 'REF-00370']),   # 9m rest platform interval
    'CLAIM-P04-0172': (T, ['REF-00151', 'REF-00370']),   # 1500mm rest platform
    'CLAIM-P04-0173': (T, ['REF-00151']),                 # 1000mm handrail height
    'CLAIM-P04-0174': (T, ['REF-00151']),                 # 300mm horizontal extension
    'CLAIM-P04-0175': (T, ['REF-00341']),                 # 35% shoulder load reduction (Koontz 2012)

    # ── E-04 Accessible parking ──
    'CLAIM-P04-0176': (T, ['REF-00151', 'REF-00370']),   # 3600mm bay width (description)
    'CLAIM-P04-0177': (T, ['REF-00151', 'REF-00370']),   # 4500mm van bay width
    'CLAIM-P04-0178': (T, ['REF-00151', 'REF-00370']),   # 3600mm standard bay spec
    'CLAIM-P04-0179': (T, ['REF-00151']),                 # ≤50m distance to entry
    'CLAIM-P04-0180': (T, ['REF-00151', 'REF-00495']),   # 5% minimum quantity
    'CLAIM-P04-0181': (D, []),    # retrofit cost note — echoes 3600mm spec
    'CLAIM-P04-0182': (D, []),    # OFS exertion budget note echoing ≤50m spec

    # ── E-05 Weather protection at entry ──
    'CLAIM-P04-0183': (T, ['REF-00265', 'REF-00370']),   # ≥3000mm canopy depth
    'CLAIM-P04-0184': (T, ['REF-00265', 'REF-00370']),   # ≥2000mm canopy width
    'CLAIM-P04-0185': (T, ['REF-00265', 'REF-00370']),   # ≥2500mm canopy height
    'CLAIM-P04-0186': (T, ['REF-00265']),                 # ≥100 lux entry lighting
    'CLAIM-P04-0187': (D, []),    # OT evidence echo — canopy compensates for rain

    # ── E-06 Level entry ──
    'CLAIM-P04-0188': (T, ['REF-00154', 'REF-00495']),   # ≤4mm threshold (description)
    'CLAIM-P04-0189': (T, ['REF-00154', 'REF-00495']),   # ≤4mm preferred threshold
    'CLAIM-P04-0190': (T, ['REF-00154', 'REF-00214']),   # ≤10mm drainage constraint
    'CLAIM-P04-0191': (T, ['REF-00154', 'REF-00370']),   # 1500mm level surface

    # ── E-08 Corridor clear width ──
    'CLAIM-P04-0192': (T, ['REF-00151', 'REF-00044']),   # ≥1200mm (CON-0007 companion note)
    'CLAIM-P04-0193': (T, ['REF-00151', 'REF-00044']),   # 1200mm description
    'CLAIM-P04-0194': (T, ['REF-00151']),                 # 1000mm code minimum reference
    'CLAIM-P04-0195': (T, ['REF-00151', 'REF-00044']),   # 1200mm minimum spec
    'CLAIM-P04-0196': (T, ['REF-00044', 'REF-00265']),   # 1500mm best practice/companion
    'CLAIM-P04-0197': (T, ['REF-00151']),                 # 10m passing bay interval
    'CLAIM-P04-0198': (T, ['REF-00044', 'REF-00265']),   # 1500mm companion width
    'CLAIM-P04-0199': (T, ['REF-00151']),                 # 1200mm primary routes
    'CLAIM-P04-0200': (T, ['REF-00151']),                 # <1200mm passing bay trigger
    'CLAIM-P04-0201': (T, ['REF-00151', 'REF-00044']),   # 1500mm passing bay
    'CLAIM-P04-0202': (T, ['REF-00151']),                 # ≤10m passing bay intervals
    'CLAIM-P04-0203': (T, ['REF-00151']),                 # 300mm skirting/kickplate
    'CLAIM-P04-0204': (D, []),    # retrofit cost note — echoes 1200mm spec
    'CLAIM-P04-0205': (D, []),    # retrofit cost note — repeats 1200mm
    'CLAIM-P04-0206': (D, []),    # OT evidence echo — 1200mm biomechanics
    'CLAIM-P04-0207': (D, []),    # OT evidence echo — 1000mm code minimum
    'CLAIM-P04-0208': (D, []),    # OT evidence echo — 1200mm corridor biomechanics

    # ── E-09 TWSI (ISO 23599) ──
    'CLAIM-P04-0209': (T, ['REF-00306']),                 # 6mm TWSI stair head profile
    'CLAIM-P04-0210': (T, ['REF-00306']),                 # 18% stair fall risk statistic
    'CLAIM-P04-0211': (T, ['REF-00306']),                 # 5mm profile height ISO 23599
    'CLAIM-P04-0212': (T, ['REF-00306']),                 # 1mm tolerance
    'CLAIM-P04-0213': (T, ['REF-00306']),                 # 3mm DEM environment TWSI max
    # E-09 claims 0214-0218: misplaced E-05 canopy content at L2016-2032
    'CLAIM-P04-0214': (T, ['REF-00265', 'REF-00370']),   # ≥3000mm canopy (misplaced E-05 content)
    'CLAIM-P04-0215': (T, ['REF-00265', 'REF-00370']),   # ≥2000mm canopy width (misplaced)
    'CLAIM-P04-0216': (T, ['REF-00265', 'REF-00370']),   # ≥2500mm canopy height (misplaced)
    'CLAIM-P04-0217': (T, ['REF-00265']),                 # ≥100 lux (misplaced E-05)
    'CLAIM-P04-0218': (D, []),    # OT evidence echo (misplaced E-05 canopy OT note)

    # ── E-11 Automatic doors ──
    'CLAIM-P04-0219': (T, ['REF-00155', 'REF-00370']),   # 20N max opening force (description)
    'CLAIM-P04-0220': (T, ['REF-00155', 'REF-00494']),   # 22N force ref
    'CLAIM-P04-0221': (T, ['REF-00155']),                 # 20N manual operation spec
    'CLAIM-P04-0222': (T, ['REF-00155']),                 # 100% slow-open profile

    # ── E-15 Changing Places ──
    'CLAIM-P04-0223': (T, ['REF-00153', 'REF-00370']),   # ≥2700mm ceiling height
    'CLAIM-P04-0224': (T, ['REF-00153', 'REF-00044']),   # 800mm bench width
    'CLAIM-P04-0225': (T, ['REF-00153', 'REF-00044']),   # 450-1000mm height-adjustable range
    'CLAIM-P04-0226': (T, ['REF-00153']),                 # ≥250kg bench rating
    'CLAIM-P04-0227': (T, ['REF-00153']),                 # 250kg hoist rating
    'CLAIM-P04-0228': (T, ['REF-00153', 'REF-00370']),   # 600mm WC clear side
    'CLAIM-P04-0229': (T, ['REF-00153', 'REF-00370']),   # 700mm WC preferred clearance
    'CLAIM-P04-0230': (T, ['REF-00153']),                 # 450-500mm WC height
    'CLAIM-P04-0231': (T, ['REF-00153', 'REF-00044']),   # 1400mm clear floor zone depth
    'CLAIM-P04-0232': (T, ['REF-00044', 'REF-00151']),   # ≥900mm carer circulation
    'CLAIM-P04-0233': (T, ['REF-00151']),                 # 750-850mm wash basin height

    # ── E-12 Entrance landing / power wheelchair ──
    'CLAIM-P04-0485': (T, ['REF-00153', 'REF-00370']),   # 1800mm landing (description)
    'CLAIM-P04-0486': (T, ['REF-00153', 'REF-00370']),   # 1800mm landing (description)
    'CLAIM-P04-0487': (T, ['REF-00153', 'REF-00370']),   # 1500mm landing standard
    'CLAIM-P04-0488': (T, ['REF-00153', 'REF-00370']),   # 1500mm standard
    'CLAIM-P04-0489': (T, ['REF-00153', 'REF-00370']),   # 1800×1800mm landing spec
    'CLAIM-P04-0490': (T, ['REF-00153', 'REF-00370']),   # 1800×1800mm spec
    'CLAIM-P04-0491': (T, ['REF-00153', 'REF-00370']),   # 500mm latch-side clearance
    'CLAIM-P04-0492': (T, ['REF-00265', 'REF-00370']),   # 1800mm canopy depth
    'CLAIM-P04-0493': (T, ['REF-00265', 'REF-00370']),   # 2000mm canopy width
    'CLAIM-P04-0494': (T, ['REF-00154']),                 # >6mm threshold exclusion
    'CLAIM-P04-0495': (T, ['REF-00154', 'REF-00153']),   # <1800mm landing exclusion
    'CLAIM-P04-0496': (D, []),    # illustration note echoing 1800mm spec
    'CLAIM-P04-0497': (D, []),    # illustration note echoing 500mm spec

    # ── E-13 Entrance cognitive legibility ──
    'CLAIM-P04-0498': (T, ['REF-00437', 'REF-00265']),   # 3m luminance contrast assessment
    'CLAIM-P04-0499': (T, ['REF-00265', 'REF-00370']),   # 50mm button diameter
    'CLAIM-P04-0500': (T, ['REF-00265', 'REF-00370']),   # 900-1200mm AFF controls
    'CLAIM-P04-0501': (T, ['REF-00265', 'REF-00370']),   # 150 lux entry lighting
    'CLAIM-P04-0502': (T, ['REF-00265', 'REF-00437']),   # 150mm address numerals
    'CLAIM-P04-0503': (T, ['REF-00265', 'REF-00437']),   # 1200-1600mm AFF numerals
    'CLAIM-P04-0504': (D, []),    # illustration placeholder note

    # ── E-10 Rest seating (canonical at L3205) — 54 claims ──
    'CLAIM-P04-0505': (D, []),    # revision note referencing old ≤20m spec
    'CLAIM-P04-0506': (T, ['REF-00036', 'REF-00514']),   # ≤25m canonical interval (Roxburgh + Wheels)
    'CLAIM-P04-0507': (D, []),    # revision note old ≤20m — same revision text
    'CLAIM-P04-0508': (T, ['REF-00036', 'REF-00514']),   # 25m description
    'CLAIM-P04-0509': (T, ['REF-00036', 'REF-00514']),   # 25m spec line
    'CLAIM-P04-0510': (T, ['REF-00036']),                 # 25m where achievable
    'CLAIM-P04-0511': (T, ['REF-00036', 'REF-00514']),   # 30m secondary routes max
    'CLAIM-P04-0512': (T, ['REF-00514', 'REF-00044']),   # 200mm recess from path
    'CLAIM-P04-0513': (T, ['REF-00514', 'REF-00044']),   # 900mm alcove width
    'CLAIM-P04-0514': (T, ['REF-00044', 'REF-00265']),   # 450mm seat height
    'CLAIM-P04-0515': (T, ['REF-00044', 'REF-00265']),   # 480mm seat height minimum
    'CLAIM-P04-0516': (T, ['REF-00044', 'REF-00514']),   # 200mm arm extension
    'CLAIM-P04-0517': (D, []),    # retrofit note echoing alcove spec
    'CLAIM-P04-0518': (D, []),    # cross-reference note to D-11 / G-02 / GAP-F
    'CLAIM-P04-0519': (D, []),    # illustration note — 900mm
    'CLAIM-P04-0520': (D, []),    # illustration note — 200mm
    'CLAIM-P04-0521': (D, []),    # illustration note — 450mm
    'CLAIM-P04-0522': (D, []),    # illustration note — 480mm
    'CLAIM-P04-0523': (D, []),    # E-14 cross-reference note referencing 25-30m
    'CLAIM-P04-0524': (T, ['REF-00044', 'REF-00265']),   # 450-460mm reclinable seating at entrance
    'CLAIM-P04-0525': (T, ['REF-00036', 'REF-00514']),   # 3m from entrance threshold
    'CLAIM-P04-0526': (T, ['REF-00044', 'REF-00514']),   # ≥1200mm alcove width
    'CLAIM-P04-0527': (T, ['REF-00044']),                 # ≥300mm arm extension
    'CLAIM-P04-0528': (T, ['REF-00044', 'REF-00514']),   # ≥450mm back support height
    'CLAIM-P04-0529': (T, ['REF-00044', 'REF-00514']),   # 400-450mm seat depth
    'CLAIM-P04-0530': (T, ['REF-00044', 'REF-00514']),   # 200-250mm arm forward extension
    'CLAIM-P04-0531': (T, ['REF-00044']),                 # 180-220mm arm height
    'CLAIM-P04-0532': (T, ['REF-00514']),                 # 40mm minimum cushion foam
    'CLAIM-P04-0533': (T, ['REF-00044', 'REF-00514']),   # ≥900mm clear floor space
    'CLAIM-P04-0534': (T, ['REF-00044']),                 # 1400mm clear floor depth
    'CLAIM-P04-0535': (T, ['REF-00044', 'REF-00265']),   # 440-480mm entrance seating height
    'CLAIM-P04-0536': (T, ['REF-00036', 'REF-00514']),   # 5m from entrance threshold
    'CLAIM-P04-0537': (T, ['REF-00044', 'REF-00514']),   # ≥1200mm alcove width
    'CLAIM-P04-0538': (T, ['REF-00044']),                 # ≥200mm alcove depth
    'CLAIM-P04-0539': (T, ['REF-00044']),                 # ≥200mm arm extension
    'CLAIM-P04-0540': (T, ['REF-00044']),                 # 180-250mm arm height
    'CLAIM-P04-0541': (T, ['REF-00044']),                 # 40mm arm clearance
    'CLAIM-P04-0542': (T, ['REF-00044', 'REF-00514']),   # ≤50mm seat compression
    'CLAIM-P04-0543': (T, ['REF-00044']),                 # ≥900mm clear floor space
    'CLAIM-P04-0544': (T, ['REF-00044']),                 # 1200mm clear floor depth
    'CLAIM-P04-0545': (T, ['REF-00044', 'REF-00265']),   # 440-480mm upright seating at entrance
    'CLAIM-P04-0546': (T, ['REF-00036']),                 # 5m from threshold
    'CLAIM-P04-0547': (T, ['REF-00044']),                 # ≥900mm alcove width
    'CLAIM-P04-0548': (T, ['REF-00044']),                 # ≥200mm alcove depth
    'CLAIM-P04-0549': (T, ['REF-00044']),                 # ≥350mm back support
    'CLAIM-P04-0550': (T, ['REF-00044']),                 # ≥380mm seat depth
    'CLAIM-P04-0551': (T, ['REF-00044']),                 # ≥150mm arm extension
    'CLAIM-P04-0552': (T, ['REF-00044']),                 # 180-250mm arm height
    'CLAIM-P04-0553': (T, ['REF-00044', 'REF-00514']),   # 440-480mm bench seating
    'CLAIM-P04-0554': (T, ['REF-00044', 'REF-00514']),   # 300mm back support minimum
    'CLAIM-P04-0555': (T, ['REF-00036']),                 # 5m from threshold
    'CLAIM-P04-0556': (T, ['REF-00044']),                 # ≥900mm alcove width
    'CLAIM-P04-0557': (T, ['REF-00044']),                 # ≥200mm alcove depth
    'CLAIM-P04-0558': (D, []),    # policy cross-ref: seating deferred to first covered point if no canopy
}

# ── Validate completeness ──
expected = 193
assert len(TAGS) == expected, f"Expected {expected} entries, got {len(TAGS)}"

# ── Load and update JSON ──
with open('references/claim-reference-join.json', encoding='utf-8') as f:
    data = json.load(f)

tagged_count = 0
deferred_count = 0
skipped = 0
errors = []

for claim in data:
    cid = claim['claim_id']
    if cid in TAGS:
        status, refs = TAGS[cid]
        # Validate TAGGED always has refs
        if status == 'TAGGED' and not refs:
            errors.append(f"TAGGED with no refs: {cid}")
            continue
        claim['status'] = status
        claim['ref_ids'] = refs
        if status == 'TAGGED':
            tagged_count += 1
        else:
            deferred_count += 1

if errors:
    print("ERRORS:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

orphaned = sum(1 for c in data if c.get('status') == 'ORPHANED')
all_tagged = sum(1 for c in data if c.get('status') == 'TAGGED')
all_deferred = sum(1 for c in data if c.get('status') == 'DEFERRED')
all_pending = sum(1 for c in data if c.get('status') == 'PENDING')

print(f"Session 3 applied: {tagged_count} TAGGED, {deferred_count} DEFERRED, 0 ORPHANED")
print(f"File totals after update:")
print(f"  TAGGED:   {all_tagged}")
print(f"  DEFERRED: {all_deferred}")
print(f"  ORPHANED: {orphaned}")
print(f"  PENDING:  {all_pending}")
print(f"  Total:    {len(data)}")

with open('references/claim-reference-join.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done — references/claim-reference-join.json updated.")
