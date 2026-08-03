#!/usr/bin/env python3
"""
Session 4 — Part 4 Category F+G citation tagging
Tags 154 claims across F-01–F-08 (env controls/air quality) and G-01–G-09 (seating/bathroom/furniture)
"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

T = 'TAGGED'
D = 'DEFERRED'

TAGS = {
    # ══════════════════════════════════════════════
    # F-01  Sensory Gradient (15 claims)
    # BPCs: sensory-processing-model-design-application, detectable-gradient-protocol-sensory-zones
    # ══════════════════════════════════════════════
    'CLAIM-P04-0234': (T, ['REF-00157', 'REF-00232']),   # 500 lux — entry zone
    'CLAIM-P04-0235': (T, ['REF-00157', 'REF-00232']),   # 300 lux — transition zone
    'CLAIM-P04-0236': (T, ['REF-00157', 'REF-00232']),   # 200 lux — primary occupied
    'CLAIM-P04-0237': (T, ['REF-00157', 'REF-00232']),   # ≤0.3s RT60 — sensory avoiding zone
    'CLAIM-P04-0238': (T, ['REF-00157', 'REF-00232']),   # 0-50 lux — sensory avoiding
    'CLAIM-P04-0239': (T, ['REF-00157', 'REF-00232']),   # ≤0.4s RT60 — sensory sensitivity
    'CLAIM-P04-0240': (T, ['REF-00157', 'REF-00232']),   # 50-200 lux — sensory sensitivity
    'CLAIM-P04-0241': (T, ['REF-00157', 'REF-00232']),   # ≤0.6s RT60 — sensory seeking
    'CLAIM-P04-0242': (T, ['REF-00157', 'REF-00232']),   # 300-500 lux — sensory seeking
    'CLAIM-P04-0243': (T, ['REF-00157', 'REF-00232']),   # ≤0.5s RT60 — low registration
    'CLAIM-P04-0244': (T, ['REF-00157']),                 # ≥15 dB SNR — low registration
    'CLAIM-P04-0245': (T, ['REF-00157', 'REF-00232']),   # ≥300 lux — low registration
    'CLAIM-P04-0246': (T, ['REF-00157', 'REF-00232']),   # ≥500 lux — low registration high needs
    'CLAIM-P04-0247': (T, ['REF-00229', 'REF-00157']),   # ≥300 lux DEM conflict note (DSDC 2024)
    'CLAIM-P04-0248': (T, ['REF-00157', 'REF-00232']),   # ≤200 lux NDV preference conflict note

    # ══════════════════════════════════════════════
    # F-03  Graduated Stimulation Re-entry (4 claims)
    # BPCs: sensory-relief-space-design, detectable-gradient-protocol-sensory-zones
    # ══════════════════════════════════════════════
    'CLAIM-P04-0249': (T, ['REF-00157', 'REF-00029']),   # 5m transition space
    'CLAIM-P04-0250': (T, ['REF-00157', 'REF-00161']),   # 5m zone depth spec
    'CLAIM-P04-0251': (T, ['REF-00157', 'REF-00232']),   # 200 lux intermediate stimulation
    'CLAIM-P04-0252': (T, ['REF-00157', 'REF-00029']),   # 5m no high-contrast buffer

    # ══════════════════════════════════════════════
    # F-04  Air Quality / VOC / Thermal Stability (8 claims)
    # BPC: air-quality-voc-chemical-sensitivity-built-environment
    # ══════════════════════════════════════════════
    'CLAIM-P04-0253': (T, ['REF-00127', 'REF-00322']),   # MERV 13 filtration (ASHRAE 52.2 + WELL v2)
    'CLAIM-P04-0254': (T, ['REF-00322', 'REF-00184']),   # ≥10 L/s fresh air (WELL v2 + CIBSE Guide A)
    'CLAIM-P04-0255': (T, ['REF-00304', 'REF-00042']),   # ≤0.5 mg/m³ VOC (ISO 16000-9 + Steinemann MCS)
    'CLAIM-P04-0256': (T, ['REF-00303', 'REF-00405']),   # ≤1°C/hr thermal stability (ISO 7730 + NICE NG206)
    'CLAIM-P04-0257': (T, ['REF-00303', 'REF-00405']),   # ≤2°C cross-zone variation
    'CLAIM-P04-0258': (T, ['REF-00303', 'REF-00184']),   # 3°C vestibule differential
    'CLAIM-P04-0259': (T, ['REF-00303', 'REF-00518']),   # 21°C target ambient (ISO 7730 + WHO Housing)
    'CLAIM-P04-0260': (T, ['REF-00002', 'REF-00364']),   # ≤0.5 mg FDR-OFS-03 MCAS co-occurrence (Afrin + Mast Cell Action)

    # ══════════════════════════════════════════════
    # F-05  Seated-Task Design [content moved to G-08] (6 claims)
    # BPC: pain-ofs-built-environment-design
    # ══════════════════════════════════════════════
    'CLAIM-P04-0261': (T, ['REF-00041', 'REF-00044']),   # 860mm seated surface height (Staud OFS + Steinfeld)
    'CLAIM-P04-0262': (T, ['REF-00044', 'REF-00415']),   # 1200mm reach range AFF (Steinfeld + PVA)
    'CLAIM-P04-0263': (T, ['REF-00044', 'REF-00415']),   # ≥690mm knee clearance height
    'CLAIM-P04-0264': (T, ['REF-00044', 'REF-00415']),   # 760mm knee clearance width
    'CLAIM-P04-0265': (T, ['REF-00044', 'REF-00415']),   # 480mm knee clearance depth
    'CLAIM-P04-0266': (T, ['REF-00041', 'REF-00405']),   # ≤760mm OFS-designated workstation height

    # ══════════════════════════════════════════════
    # F-06  Fragrance-Free Policy (1 claim)
    # BPC: air-quality-voc-chemical-sensitivity-built-environment
    # ══════════════════════════════════════════════
    'CLAIM-P04-0267': (T, ['REF-00304', 'REF-00042']),   # ≤0.5 mg/m³ commissioning hold point

    # ══════════════════════════════════════════════
    # F-07  Thermal Zoning (14 claims)
    # BPCs: ms-thermal-temperature-conflict-resolution, thermoregulation-built-environment
    # ══════════════════════════════════════════════
    'CLAIM-P04-0268': (T, ['REF-00388', 'REF-00014']),   # ≤18°C MS ambient (MSIF Atlas + Flensner 2011)
    'CLAIM-P04-0269': (T, ['REF-00184', 'REF-00303']),   # 5°C inter-room differential limit
    'CLAIM-P04-0270': (T, ['REF-00041', 'REF-00303']),   # ≤22°C PAIN radiant heating provision
    'CLAIM-P04-0271': (T, ['REF-00041']),                 # 0.5m radiant heater reach distance (OFS)
    'CLAIM-P04-0272': (T, ['REF-00518', 'REF-00321']),   # 16-24°C individual thermostat range (WHO + WELL v2)
    'CLAIM-P04-0273': (T, ['REF-00519', 'REF-00016']),   # >28°C tropical climate threshold (WHO Annex G + Griggs SCI)
    'CLAIM-P04-0274': (T, ['REF-00519', 'REF-00016']),   # 28°C tropical threshold (same context)
    'CLAIM-P04-0275': (T, ['REF-00268', 'REF-00016']),   # 30% SCI sweating capacity (Hayashi 2022 + Griggs 2019)
    'CLAIM-P04-0276': (T, ['REF-00388', 'REF-00041']),   # ≤18°C NEU/MS vs PAIN conflict note
    'CLAIM-P04-0277': (T, ['REF-00014', 'REF-00388']),   # 1-2°C MS diurnal fatigue (FDR-MST-02; Krupp 2003 — best available: Flensner + MSIF)
    'CLAIM-P04-0278': (T, ['REF-00371', 'REF-00303']),   # ≥30 min bathroom heat shock (MHLW Japan 2023 + ISO 7730)
    'CLAIM-P04-0279': (T, ['REF-00371', 'REF-00303']),   # ≥20°C bathroom anti-heat-shock temperature
    'CLAIM-P04-0280': (T, ['REF-00024', 'REF-00416']),   # ≤43°C anti-scald (Levine 2025 bathroom safety + RCOT 2019)
    'CLAIM-P04-0281': (T, ['REF-00024', 'REF-00416']),   # ≤43°C anti-scald (same — second extraction)

    # ══════════════════════════════════════════════
    # F-08  Thermal Transition (5 claims)
    # BPC: ms-thermal-temperature-conflict-resolution
    # ══════════════════════════════════════════════
    'CLAIM-P04-0282': (T, ['REF-00184', 'REF-00321']),   # ≤0.15 W/m²K U-value envelope
    'CLAIM-P04-0283': (T, ['REF-00184', 'REF-00321']),   # ≤3°C daily thermal swing (thermal mass)
    'CLAIM-P04-0284': (T, ['REF-00184']),                 # 15 min HVAC response time
    'CLAIM-P04-0285': (T, ['REF-00184', 'REF-00303']),   # ≥2m entry vestibule depth
    'CLAIM-P04-0286': (T, ['REF-00184', 'REF-00303']),   # >15°C seasonal differential threshold

    # ══════════════════════════════════════════════
    # G-01  Defensible Seating (2 claims)
    # BPC: mental-health-built-environment
    # ══════════════════════════════════════════════
    'CLAIM-P04-0287': (T, ['REF-00053', 'REF-00057']),   # 30% back-to-wall seating (description)
    'CLAIM-P04-0288': (T, ['REF-00053', 'REF-00057']),   # 30% spec line

    # ══════════════════════════════════════════════
    # G-02  Variety of Seating Types (11 claims)
    # BPCs: mobility-built-environment, ofs-built-environment
    # ══════════════════════════════════════════════
    'CLAIM-P04-0289': (T, ['REF-00044', 'REF-00265']),   # 450mm type A seat height (description)
    'CLAIM-P04-0290': (T, ['REF-00044', 'REF-00265']),   # 600mm type B seat height
    'CLAIM-P04-0291': (T, ['REF-00044', 'REF-00265']),   # 400mm type C seat height
    'CLAIM-P04-0292': (T, ['REF-00044', 'REF-00265']),   # 450mm type A spec
    'CLAIM-P04-0293': (T, ['REF-00044', 'REF-00265']),   # 600mm type B spec
    'CLAIM-P04-0294': (T, ['REF-00044', 'REF-00265']),   # 400mm type C spec
    'CLAIM-P04-0295': (D, []),    # OT evidence echo — 430-500mm seat heights
    'CLAIM-P04-0296': (D, []),    # OT evidence echo — 500mm (same paragraph)
    'CLAIM-P04-0297': (D, []),    # OT evidence echo — 40% sit-to-stand percentage
    'CLAIM-P04-0298': (D, []),    # OT evidence echo — 380mm
    'CLAIM-P04-0299': (D, []),    # OT evidence echo — 25%

    # ══════════════════════════════════════════════
    # G-03  Grab Bars (22 claims)
    # BPCs: accessible-bathroom-and-grab-bar, upper-limb-impairment-built-environment
    # ══════════════════════════════════════════════
    'CLAIM-P04-0300': (T, ['REF-00150', 'REF-00415']),   # 900mm bar range (description)
    'CLAIM-P04-0301': (T, ['REF-00024', 'REF-00333']),   # 700mm Tier 1 median height (Levine 2025 + Keall MHIPI)
    'CLAIM-P04-0302': (T, ['REF-00024', 'REF-00253']),   # 280mm above seat (Levine + BATH-OUT)
    'CLAIM-P04-0303': (T, ['REF-00024', 'REF-00400']),   # 45mm bar diameter (Levine + Newton 2023)
    'CLAIM-P04-0304': (T, ['REF-00340', 'REF-00333']),   # ≥1.5 kN static load (KITE 2025 + Keall MHIPI)
    'CLAIM-P04-0305': (T, ['REF-00340', 'REF-00333']),   # ≥2.5 kN peak dynamic fall-arrest
    'CLAIM-P04-0306': (T, ['REF-00150', 'REF-00415']),   # 18mm blocking plywood
    'CLAIM-P04-0307': (T, ['REF-00150', 'REF-00415']),   # 600mm blocking size (300×600mm)
    'CLAIM-P04-0308': (T, ['REF-00024', 'REF-00400']),   # 45mm wall clearance 35-45mm
    'CLAIM-P04-0309': (T, ['REF-00150', 'REF-00415']),   # 900mm bilateral bar range spec
    'CLAIM-P04-0310': (T, ['REF-00024', 'REF-00333']),   # 700mm Tier 1 median spec
    'CLAIM-P04-0311': (T, ['REF-00024', 'REF-00253']),   # 280mm above seat spec
    'CLAIM-P04-0312': (T, ['REF-00024', 'REF-00400']),   # 45mm bar diameter spec
    'CLAIM-P04-0313': (T, ['REF-00340', 'REF-00333']),   # ≥1.5 kN static load spec
    'CLAIM-P04-0314': (T, ['REF-00340', 'REF-00333']),   # ≥2.5 kN peak dynamic spec
    'CLAIM-P04-0315': (T, ['REF-00150']),                 # 18mm blocking spec
    'CLAIM-P04-0316': (T, ['REF-00150']),                 # 600mm blocking spec
    'CLAIM-P04-0317': (T, ['REF-00024', 'REF-00400']),   # 45mm wall clearance spec
    'CLAIM-P04-0318': (T, ['REF-00253', 'REF-00415']),   # 850mm shower fold-down bar (BATH-OUT + PVA)
    'CLAIM-P04-0319': (D, []),    # OT evidence echo — 32-45mm diameter biomechanics
    'CLAIM-P04-0320': (D, []),    # OT evidence echo — ≥1.5kN
    'CLAIM-P04-0321': (D, []),    # OT evidence echo — ≥2.5kN

    # ══════════════════════════════════════════════
    # G-04  Accessible Bathroom Wet Room (7 claims)
    # BPC: accessible-bathroom-and-grab-bar
    # ══════════════════════════════════════════════
    'CLAIM-P04-0322': (T, ['REF-00150', 'REF-00415']),   # 900mm shower area (description)
    'CLAIM-P04-0323': (T, ['REF-00150', 'REF-00415']),   # 900mm continuous wet room spec
    'CLAIM-P04-0324': (T, ['REF-00150', 'REF-00415']),   # 1500mm shower area dimension
    'CLAIM-P04-0325': (T, ['REF-00154', 'REF-00415']),   # ≤3mm zero threshold shower (BS 8300 threshold + PVA)
    'CLAIM-P04-0326': (T, ['REF-00150']),                 # 1200mm drain proximity
    'CLAIM-P04-0327': (T, ['REF-00150', 'REF-00415']),   # ≥900mm shower clear area
    'CLAIM-P04-0328': (T, ['REF-00150']),                 # 900mm preferred clear area

    # ══════════════════════════════════════════════
    # G-05  Adjustable-Height Work Surfaces (9 claims)
    # BPC: residential-kitchen-and-task-surfaces
    # ══════════════════════════════════════════════
    'CLAIM-P04-0329': (T, ['REF-00415', 'REF-00044']),   # 20% workstations height-adjustable
    'CLAIM-P04-0330': (T, ['REF-00044', 'REF-00415']),   # 650mm lower height limit
    'CLAIM-P04-0331': (T, ['REF-00044', 'REF-00415']),   # 870mm upper height limit
    'CLAIM-P04-0332': (T, ['REF-00044', 'REF-00415']),   # ≥600mm knee clearance depth
    'CLAIM-P04-0333': (T, ['REF-00415', 'REF-00044']),   # 20% spec line
    'CLAIM-P04-0334': (T, ['REF-00044', 'REF-00415']),   # 870mm height range spec
    'CLAIM-P04-0335': (T, ['REF-00044', 'REF-00415']),   # ≥600mm knee clearance spec
    'CLAIM-P04-0336': (D, []),    # OT evidence echo — 660-1200mm desk height range
    'CLAIM-P04-0337': (D, []),    # OT evidence echo — 660mm (same paragraph)

    # ══════════════════════════════════════════════
    # G-06  Reception Counter Accessible Height (13 claims)
    # BPCs: mobility-built-environment, ofs-built-environment
    # ══════════════════════════════════════════════
    'CLAIM-P04-0338': (T, ['REF-00044', 'REF-00150']),   # 860mm lowered section (description)
    'CLAIM-P04-0339': (T, ['REF-00044', 'REF-00150']),   # ≥690mm knee clearance (description)
    'CLAIM-P04-0340': (T, ['REF-00044', 'REF-00150']),   # 760mm lowered section height
    'CLAIM-P04-0341': (T, ['REF-00044', 'REF-00150']),   # 480mm knee clearance depth
    'CLAIM-P04-0342': (T, ['REF-00044', 'REF-00150']),   # 860mm spec line
    'CLAIM-P04-0343': (T, ['REF-00044']),                 # ≥690mm knee clearance spec
    'CLAIM-P04-0344': (T, ['REF-00044']),                 # 760mm knee clearance width spec
    'CLAIM-P04-0345': (T, ['REF-00044']),                 # 480mm knee clearance depth spec
    'CLAIM-P04-0346': (T, ['REF-00405', 'REF-00324']),   # 2-10 min orthostatic intolerance — default service position (NICE NG206 + JAN POTS)
    'CLAIM-P04-0347': (D, []),    # OT evidence echo — 760-860mm counter height
    'CLAIM-P04-0348': (D, []),    # OT evidence echo — ≥690mm knee clearance
    'CLAIM-P04-0349': (T, ['REF-00405', 'REF-00233']),   # 2-10 min FDR-OFS-01 orthostatic onset (NICE + Dysautonomia Network)
    'CLAIM-P04-0350': (T, ['REF-00405', 'REF-00233']),   # 2-10 min (same FDR paragraph, second extraction)

    # ══════════════════════════════════════════════
    # G-07  Waiting Area Seating (7 claims)
    # BPC: mobility-built-environment
    # ══════════════════════════════════════════════
    'CLAIM-P04-0351': (T, ['REF-00150', 'REF-00265']),   # 10m from reception
    'CLAIM-P04-0352': (T, ['REF-00044', 'REF-00150']),   # 10% wheelchair companion pairs
    'CLAIM-P04-0353': (T, ['REF-00044', 'REF-00150']),   # 1200mm companion pair area
    'CLAIM-P04-0354': (T, ['REF-00044', 'REF-00150']),   # 10% spec line
    'CLAIM-P04-0355': (T, ['REF-00044', 'REF-00150']),   # 1200×1200mm per pair spec
    'CLAIM-P04-0356': (T, ['REF-00036', 'REF-00405']),   # >5 min wait rest seating (Roxburgh ME/CFS + NICE NG206)
    'CLAIM-P04-0357': (T, ['REF-00150', 'REF-00405']),   # 20m toilet from waiting area

    # ══════════════════════════════════════════════
    # G-08  Bedroom Wardrobe and Storage Reach (20 claims)
    # BPCs: residential-kitchen-and-task-surfaces, pain-ofs-built-environment-design
    # ══════════════════════════════════════════════
    'CLAIM-P04-0451': (T, ['REF-00415', 'REF-00044']),   # 1050mm hanging rod max height (PVA + Steinfeld)
    'CLAIM-P04-0452': (T, ['REF-00415', 'REF-00044']),   # 1000-1100mm dual-rod upper height
    'CLAIM-P04-0453': (T, ['REF-00415', 'REF-00044']),   # 600mm dual-rod lower height
    'CLAIM-P04-0454': (T, ['REF-00415', 'REF-00044']),   # 380mm max shelf depth
    'CLAIM-P04-0455': (T, ['REF-00415', 'REF-00044']),   # 600mm pull-out drawer max depth
    'CLAIM-P04-0456': (T, ['REF-00415']),                 # 500mm AFF pull-out mechanism trigger
    'CLAIM-P04-0457': (T, ['REF-00415', 'REF-00044']),   # 600mm outswing clearance for sliding doors
    'CLAIM-P04-0458': (T, ['REF-00150', 'REF-00044']),   # 1500mm turning space
    'CLAIM-P04-0459': (T, ['REF-00150', 'REF-00044']),   # 1500mm turning space (repeated spec)
    'CLAIM-P04-0460': (D, []),    # illustration note — 380mm shelf depth plan view
    'CLAIM-P04-0461': (D, []),    # illustration note — 1500mm turning space plan view
    'CLAIM-P04-0462': (T, ['REF-00044', 'REF-00416']),   # 900mm FDR-TCOA-01 DEM carer reach (Steinfeld + RCOT)
    'CLAIM-P04-0463': (T, ['REF-00044', 'REF-00416']),   # 1050-1200mm carer reach range
    'CLAIM-P04-0464': (T, ['REF-00044']),                 # 600-900mm lower reach zone
    'CLAIM-P04-0465': (T, ['REF-00044', 'REF-00415']),   # 650-870mm adjustable work surface range
    'CLAIM-P04-0466': (T, ['REF-00044', 'REF-00415']),   # ≥680mm knee clearance depth
    'CLAIM-P04-0467': (T, ['REF-00044', 'REF-00415']),   # ≥900mm knee clearance width
    'CLAIM-P04-0468': (T, ['REF-00044', 'REF-00150']),   # 30% counter length at accessible height
    'CLAIM-P04-0469': (T, ['REF-00044', 'REF-00150']),   # 760-860mm counter height (G-08 context)
    'CLAIM-P04-0470': (T, ['REF-00036', 'REF-00514']),   # 25m rest seating from task location (Roxburgh + Wheels)

    # ══════════════════════════════════════════════
    # G-09  Bedroom Emergency Call and Overnight Lighting (10 claims)
    # BPCs: neurological-built-environment, ofs-built-environment
    # ══════════════════════════════════════════════
    'CLAIM-P04-0471': (T, ['REF-00416', 'REF-00265']),   # 100-150mm cord end AFF fall-recovery position
    'CLAIM-P04-0472': (T, ['REF-00416', 'REF-00265']),   # 500mm second cord position
    'CLAIM-P04-0473': (T, ['REF-00416', 'REF-00265']),   # 900mm luminaire control from pillow
    'CLAIM-P04-0474': (T, ['REF-00416', 'REF-00265']),   # 300-400mm pathway lighting height
    'CLAIM-P04-0475': (T, ['REF-00416']),                 # 5 lux pathway lighting minimum
    'CLAIM-P04-0476': (T, ['REF-00265', 'REF-00229']),   # 1200mm bedroom door identification (Habinteg + DSDC)
    'CLAIM-P04-0477': (T, ['REF-00265', 'REF-00416']),   # 1200mm medication storage AFF
    'CLAIM-P04-0478': (T, ['REF-00265', 'REF-00416']),   # 500mm medication storage reach
    'CLAIM-P04-0479': (T, ['REF-00265', 'REF-00044']),   # 1000mm clear floor at bed foot
    'CLAIM-P04-0480': (D, []),    # illustration note — plan showing 1000mm
}

# ── Validate ──
expected = 154
assert len(TAGS) == expected, f"Expected {expected}, got {len(TAGS)}"

# ── Load and apply ──
with open('references/claim-reference-join.json', encoding='utf-8') as f:
    data = json.load(f)

tagged_count = deferred_count = 0
errors = []
for claim in data:
    cid = claim['claim_id']
    if cid in TAGS:
        status, refs = TAGS[cid]
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
    for e in errors: print(f"  {e}")
    sys.exit(1)

all_tagged   = sum(1 for c in data if c.get('status') == 'TAGGED')
all_deferred = sum(1 for c in data if c.get('status') == 'DEFERRED')
all_orphaned = sum(1 for c in data if c.get('status') == 'ORPHANED')
all_pending  = sum(1 for c in data if c.get('status') == 'PENDING')

print(f"Session 4 applied: {tagged_count} TAGGED, {deferred_count} DEFERRED, 0 ORPHANED")
print(f"File totals:")
print(f"  TAGGED:   {all_tagged}")
print(f"  DEFERRED: {all_deferred}")
print(f"  ORPHANED: {all_orphaned}")
print(f"  PENDING:  {all_pending}")
print(f"  Total:    {len(data)}")

with open('references/claim-reference-join.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done — references/claim-reference-join.json updated.")
