"""Session 12 tagging: Part 11 — economics / cost-benefit analysis (191 claims)"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('references/claim-reference-join.json', encoding='utf-8') as f:
    data = json.load(f)

tagging = {
    # part11-intro
    'CLAIM-P11-0001': ('TAGGED', ['REF-00106', 'REF-00475'], None),
    'CLAIM-P11-0002': ('DEFERRED', [], 'cross-reference parsing artifact — "0004 Pa" = CO-0004 part-numbering cross-reference, not a unit value'),
    'CLAIM-P11-0003': ('TAGGED', ['REF-00106', 'REF-00475'], None),

    # §11.1.2 — TERRAGON/DStGB Germany + Ielegems & Vanrie Belgium
    'CLAIM-P11-0004': ('TAGGED', ['REF-00475', 'REF-00476'], None),
    'CLAIM-P11-0005': ('TAGGED', ['REF-00475', 'REF-00476'], None),
    'CLAIM-P11-0006': ('TAGGED', ['REF-00292', 'REF-00293'], None),
    'CLAIM-P11-0007': ('TAGGED', ['REF-00292', 'REF-00293'], None),
    'CLAIM-P11-0008': ('TAGGED', ['REF-00292', 'REF-00293'], None),
    'CLAIM-P11-0009': ('TAGGED', ['REF-00292', 'REF-00293'], None),

    # §11.1.3 — Part 7 cross-reference note
    'CLAIM-P11-0010': ('DEFERRED', [], 'cross-reference note to Part 7 acoustic cost data — not a primary research claim'),

    # §11.2.1 — Synthesis of cost premium evidence
    'CLAIM-P11-0011': ('TAGGED', ['REF-00475', 'REF-00476'], None),
    'CLAIM-P11-0012': ('TAGGED', ['REF-00475', 'REF-00476'], None),
    'CLAIM-P11-0013': ('TAGGED', ['REF-00475', 'REF-00476'], None),
    'CLAIM-P11-0014': ('TAGGED', ['REF-00292', 'REF-00293'], None),
    'CLAIM-P11-0015': ('TAGGED', ['REF-00292', 'REF-00293'], None),
    'CLAIM-P11-0016': ('TAGGED', ['REF-00106', 'REF-00092'], None),
    'CLAIM-P11-0017': ('TAGGED', ['REF-00106', 'REF-00092'], None),
    'CLAIM-P11-0018': ('TAGGED', ['REF-00475', 'REF-00106'], None),

    # §11.2.2 — Retrofit cost multiple (20× more expensive)
    'CLAIM-P11-0019': ('TAGGED', ['REF-00336', 'REF-00337'], None),

    # §11.2.3 — Summary table
    'CLAIM-P11-0020': ('TAGGED', ['REF-00475', 'REF-00292'], None),
    'CLAIM-P11-0021': ('TAGGED', ['REF-00475', 'REF-00292'], None),

    # §11.3.4 — Social cost of inaccessibility (Tibble 40 countries)
    'CLAIM-P11-0022': ('TAGGED', ['REF-00374'], None),

    # §11.3.1 — De Hogeweyk wayfinding outcomes
    'CLAIM-P11-0023': ('TAGGED', ['REF-00512'], None),
    'CLAIM-P11-0024': ('TAGGED', ['REF-00512'], None),

    # §11.3.3 — Property value lift (elevator) + population benefit
    'CLAIM-P11-0025': ('TAGGED', ['REF-00281', 'REF-00282'], None),
    'CLAIM-P11-0026': ('TAGGED', ['REF-00265', 'REF-00333'], None),

    # §11.4.1 — Accessible routes / site items cost table
    'CLAIM-P11-0027': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # E-06 level entry 0%
    'CLAIM-P11-0028': ('TAGGED', ['REF-00475', 'REF-00292'], None),   # E-08 ≥1200mm
    'CLAIM-P11-0029': ('TAGGED', ['REF-00475', 'REF-00292'], None),   # E-08 0–0.3%
    'CLAIM-P11-0030': ('TAGGED', ['REF-00475', 'REF-00292'], None),   # E-08 ≥1500mm
    'CLAIM-P11-0031': ('TAGGED', ['REF-00292', 'REF-00106'], None),   # E-08 0.1–0.5%
    'CLAIM-P11-0032': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # door ≥850mm
    'CLAIM-P11-0033': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # door 0%
    'CLAIM-P11-0034': ('TAGGED', ['REF-00106', 'REF-00292'], None),   # auto door 0.1–0.3%
    'CLAIM-P11-0035': ('TAGGED', ['REF-00281', 'REF-00355'], None),   # lift shaft 0.5–1.5%
    'CLAIM-P11-0036': ('TAGGED', ['REF-00281', 'REF-00355'], None),   # lift fit-out 2–5%
    'CLAIM-P11-0037': ('TAGGED', ['REF-00281', 'REF-00355'], None),   # lift ≤3m travel
    'CLAIM-P11-0038': ('TAGGED', ['REF-00281', 'REF-00355'], None),   # lift NR 0.3–1%
    'CLAIM-P11-0039': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # parking 0%
    'CLAIM-P11-0040': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # TWSI 0–0.1%
    'CLAIM-P11-0041': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # signage 0–0.1%
    'CLAIM-P11-0042': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # signage ≤30m
    'CLAIM-P11-0043': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # signage 0–0.1%
    'CLAIM-P11-0044': ('TAGGED', ['REF-00292', 'REF-00265'], None),   # canopy 2000mm
    'CLAIM-P11-0045': ('TAGGED', ['REF-00292', 'REF-00265'], None),   # canopy 0.1–0.3%

    # §11.4.2 — Sanitary / bathroom items
    'CLAIM-P11-0046': ('TAGGED', ['REF-00292', 'REF-00106'], None),   # ambulant WC 0.1–0.3%
    'CLAIM-P11-0047': ('TAGGED', ['REF-00292', 'REF-00355'], None),   # accessible WC 0.3–0.8%
    'CLAIM-P11-0048': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # WC 0% (if on brief)
    'CLAIM-P11-0049': ('TAGGED', ['REF-00292', 'REF-00106'], None),   # roll-in shower 0.2–0.5%
    'CLAIM-P11-0050': ('TAGGED', ['REF-00292', 'REF-00106'], None),   # height-adjustable 0.3–0.8%
    'CLAIM-P11-0051': ('TAGGED', ['REF-00265', 'REF-00355'], None),   # Type B bath 0.5–1.0%
    'CLAIM-P11-0052': ('TAGGED', ['REF-00355', 'REF-00292'], None),   # Changing Places 0.8–1.5%
    'CLAIM-P11-0053': ('TAGGED', ['REF-00292', 'REF-00475'], None),   # heated floor 0.2–0.4%
    'CLAIM-P11-0054': ('TAGGED', ['REF-00371', 'REF-00024'], None),   # >10°C heat shock
    'CLAIM-P11-0055': ('TAGGED', ['REF-00024', 'REF-00371'], None),   # ≥15mm threshold fall

    # §11.4.3 — Acoustic items
    'CLAIM-P11-0056': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # acoustic zoning 0%
    'CLAIM-P11-0057': ('TAGGED', ['REF-00142', 'REF-00124'], None),   # ≥50dB STC acoustic
    'CLAIM-P11-0058': ('TAGGED', ['REF-00292', 'REF-00336'], None),   # acoustic zoning 0.3–0.8%
    'CLAIM-P11-0059': ('TAGGED', ['REF-00292', 'REF-00475'], None),   # impact sound 0.2–0.6%
    'CLAIM-P11-0060': ('TAGGED', ['REF-00142', 'REF-00124'], None),   # RT ≤0.4s spec
    'CLAIM-P11-0061': ('TAGGED', ['REF-00292', 'REF-00106'], None),   # RT control 0.3–0.7%
    'CLAIM-P11-0062': ('TAGGED', ['REF-00289', 'REF-00106'], None),   # hearing loop 0.1–0.3%
    'CLAIM-P11-0063': ('TAGGED', ['REF-00289', 'REF-00106'], None),   # loop counter 0–0.1%
    'CLAIM-P11-0064': ('TAGGED', ['REF-00289', 'REF-00142'], None),   # ≤35dB(A) loop
    'CLAIM-P11-0065': ('TAGGED', ['REF-00289', 'REF-00106'], None),   # loop counter 0.2–0.5%
    'CLAIM-P11-0066': ('TAGGED', ['REF-00029', 'REF-00142'], None),   # sensory room RT ≤0.3s
    'CLAIM-P11-0067': ('TAGGED', ['REF-00029', 'REF-00292'], None),   # sensory room 0.5–1.2%

    # §11.4.4 — Visual / lighting items
    'CLAIM-P11-0068': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # tonal contrast 0%
    'CLAIM-P11-0069': ('TAGGED', ['REF-00292', 'REF-00106'], None),   # high CRI 0.1–0.3%
    'CLAIM-P11-0070': ('TAGGED', ['REF-00292', 'REF-00106'], None),   # glare control 0.1–0.2%
    'CLAIM-P11-0071': ('TAGGED', ['REF-00437', 'REF-00229'], None),   # ≥300 lux spec
    'CLAIM-P11-0072': ('TAGGED', ['REF-00292', 'REF-00106'], None),   # illuminance 0–0.2%
    'CLAIM-P11-0073': ('TAGGED', ['REF-00437', 'REF-00486'], None),   # window head ≥2100mm
    'CLAIM-P11-0074': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # window 0%
    'CLAIM-P11-0075': ('TAGGED', ['REF-00292', 'REF-00106'], None),   # circadian lighting 0.3–0.8%
    'CLAIM-P11-0076': ('TAGGED', ['REF-00149', 'REF-00106'], None),   # visual fire alarm 0.1–0.2%
    'CLAIM-P11-0077': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # colour coding 0%

    # §11.4.5 — Wayfinding / cognitive items
    'CLAIM-P11-0078': ('TAGGED', ['REF-00475', 'REF-00026'], None),   # loop floor plan 0%
    'CLAIM-P11-0079': ('TAGGED', ['REF-00475', 'REF-00026'], None),   # toilet visible 0%
    'CLAIM-P11-0080': ('TAGGED', ['REF-00475', 'REF-00361'], None),   # visual access 0%
    'CLAIM-P11-0081': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # landmark objects 0–0.1%
    'CLAIM-P11-0082': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # pictogram signage 0–0.1%
    'CLAIM-P11-0083': ('TAGGED', ['REF-00029', 'REF-00292'], None),   # quiet retreat 0.1–0.3%
    'CLAIM-P11-0084': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # defensible seating 0%
    'CLAIM-P11-0085': ('TAGGED', ['REF-00265', 'REF-00292'], None),   # outdoor loop 0.1–0.3%
    'CLAIM-P11-0086': ('TAGGED', ['REF-00026'], None),                # 47% toilet visibility

    # §11.4.6 — Thermal control items
    'CLAIM-P11-0087': ('TAGGED', ['REF-00292', 'REF-00106'], None),   # individual HVAC 0.3–0.8%
    'CLAIM-P11-0088': ('TAGGED', ['REF-00518', 'REF-00303'], None),   # ≤0.15W U-value
    'CLAIM-P11-0089': ('TAGGED', ['REF-00518', 'REF-00475'], None),   # high-perf envelope 1–3%
    'CLAIM-P11-0090': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # thermal mass 0%
    'CLAIM-P11-0091': ('TAGGED', ['REF-00322', 'REF-00106'], None),   # air quality 0.2–0.5%

    # §11.4.7 — Assistive technology provisions
    'CLAIM-P11-0092': ('TAGGED', ['REF-00265', 'REF-00106'], None),   # conduit/AT provision 0–0.1%
    'CLAIM-P11-0093': ('TAGGED', ['REF-00265', 'REF-00292'], None),   # smart home base 0.2–0.6%
    'CLAIM-P11-0094': ('TAGGED', ['REF-00265', 'REF-00106'], None),   # voice-activated control 0.3–0.8%
    'CLAIM-P11-0095': ('TAGGED', ['REF-00265', 'REF-00150'], None),   # nurse call 0.1–0.3%

    # §11.4.8 — Outdoor / landscape items
    'CLAIM-P11-0096': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # level access route 0%
    'CLAIM-P11-0097': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # accessible parking 0%
    'CLAIM-P11-0098': ('TAGGED', ['REF-00475', 'REF-00036'], None),   # outdoor seating 0–0.1%
    'CLAIM-P11-0099': ('TAGGED', ['REF-00265', 'REF-00015'], None),   # sensory garden 0.1–0.3%

    # §11.4.9 — Kitchen items
    'CLAIM-P11-0100': ('TAGGED', ['REF-00416', 'REF-00052'], None),   # knee clearance ≥700mm
    'CLAIM-P11-0101': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # knee clearance 0%
    'CLAIM-P11-0102': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # front controls 0%
    'CLAIM-P11-0103': ('TAGGED', ['REF-00292', 'REF-00416'], None),   # adj worktop manual 0.3–0.8%
    'CLAIM-P11-0104': ('TAGGED', ['REF-00292', 'REF-00416'], None),   # adj worktop electric 0.5–1.2%
    'CLAIM-P11-0105': ('TAGGED', ['REF-00292', 'REF-00416'], None),   # pull-out shelving 0.2–0.5%
    'CLAIM-P11-0106': ('TAGGED', ['REF-00292', 'REF-00416'], None),   # side-opening oven 0.1–0.2%

    # §11.4.10 — Bedroom items
    'CLAIM-P11-0107': ('TAGGED', ['REF-00265', 'REF-00044'], None),   # bed transfer ≥1200mm
    'CLAIM-P11-0108': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # bed transfer 0%
    'CLAIM-P11-0109': ('TAGGED', ['REF-00150', 'REF-00486'], None),   # windowsill ≤600mm
    'CLAIM-P11-0110': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # windowsill 0%
    'CLAIM-P11-0111': ('TAGGED', ['REF-00311', 'REF-00265'], None),   # hoist blocking ≥3600mm
    'CLAIM-P11-0112': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # hoist blocking 0%
    'CLAIM-P11-0113': ('TAGGED', ['REF-00311', 'REF-00292'], None),   # hoist fit-out 0.3–0.8%
    'CLAIM-P11-0114': ('TAGGED', ['REF-00292', 'REF-00416'], None),   # pull-down wardrobe 0.1–0.3%

    # §11.4.11 — Fire safety items
    'CLAIM-P11-0115': ('TAGGED', ['REF-00106', 'REF-00292'], None),   # refuge 0.2–0.5%
    'CLAIM-P11-0116': ('TAGGED', ['REF-00149', 'REF-00401'], None),   # visual/tactile alarm 0.1–0.3%
    'CLAIM-P11-0117': ('TAGGED', ['REF-00203', 'REF-00106'], None),   # vibrating pillow 0.05–0.1%
    'CLAIM-P11-0118': ('TAGGED', ['REF-00173', 'REF-00292'], None),   # evacuation lift 1–3%

    # §11.4.12 — Hardware items
    'CLAIM-P11-0119': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # lever handles 0%
    'CLAIM-P11-0120': ('TAGGED', ['REF-00492', 'REF-00152'], None),   # rocker switch height
    'CLAIM-P11-0121': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # rocker switch 0%
    'CLAIM-P11-0122': ('TAGGED', ['REF-00492', 'REF-00152'], None),   # power outlets height
    'CLAIM-P11-0123': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # power outlets 0%
    'CLAIM-P11-0124': ('TAGGED', ['REF-00106', 'REF-00308'], None),   # door closers 0.05–0.1%
    'CLAIM-P11-0125': ('TAGGED', ['REF-00135', 'REF-00106'], None),   # intercom 0.1–0.3%
    'CLAIM-P11-0126': ('TAGGED', ['REF-00150', 'REF-00308'], None),   # handrail 40–45mm
    'CLAIM-P11-0127': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # handrail 0%
    'CLAIM-P11-0128': ('TAGGED', ['REF-00475', 'REF-00106'], None),   # nosings 0–0.1%

    # §11.4.13 — Cost-by-design-stage table
    'CLAIM-P11-0129': ('TAGGED', ['REF-00475', 'REF-00292'], None),
    'CLAIM-P11-0130': ('TAGGED', ['REF-00475', 'REF-00106'], None),
    'CLAIM-P11-0131': ('TAGGED', ['REF-00475', 'REF-00292'], None),
    'CLAIM-P11-0132': ('TAGGED', ['REF-00292', 'REF-00106'], None),
    'CLAIM-P11-0133': ('TAGGED', ['REF-00336', 'REF-00337'], None),

    # §11.5 — Co-benefits / value engineering
    'CLAIM-P11-0134': ('TAGGED', ['REF-00265', 'REF-00475'], None),   # 48% energy co-benefit
    'CLAIM-P11-0135': ('TAGGED', ['REF-00371', 'REF-00303'], None),   # >10°C thermal
    'CLAIM-P11-0136': ('TAGGED', ['REF-00265', 'REF-00292'], None),   # 3% value engineering risk

    # §11.6.1 — Evidence summary (key metrics)
    'CLAIM-P11-0137': ('TAGGED', ['REF-00292', 'REF-00293'], None),   # 0.94%
    'CLAIM-P11-0138': ('TAGGED', ['REF-00292', 'REF-00293'], None),   # 3.92%
    'CLAIM-P11-0139': ('TAGGED', ['REF-00026'], None),                # 47% toilet visibility
    'CLAIM-P11-0140': ('TAGGED', ['REF-00024', 'REF-00371'], None),   # ≥15mm threshold
    'CLAIM-P11-0141': ('TAGGED', ['REF-00371'], None),                # >10°C heat shock
    'CLAIM-P11-0142': ('TAGGED', ['REF-00512'], None),                # 94% De Hogeweyk
    'CLAIM-P11-0143': ('TAGGED', ['REF-00512'], None),                # 34%
    'CLAIM-P11-0144': ('TAGGED', ['REF-00297'], None),                # 31% medication
    'CLAIM-P11-0145': ('TAGGED', ['REF-00374'], None),                # 5.7% social cost
    'CLAIM-P11-0146': ('TAGGED', ['REF-00281', 'REF-00282'], None),   # 5.53% elevator
    'CLAIM-P11-0147': ('TAGGED', ['REF-00265', 'REF-00106'], None),   # 50% rent/ESG uplift
    'CLAIM-P11-0148': ('TAGGED', ['REF-00374', 'REF-00477'], None),   # 5.7% household cost

    # §11.7 — Design stage recommendations
    'CLAIM-P11-0149': ('TAGGED', ['REF-00026'], None),                # 47% toilet visibility
    'CLAIM-P11-0150': ('TAGGED', ['REF-00265', 'REF-00475'], None),   # 1–3% grab bar now

    # §11.8.1 — Evidence narrative (De Hogeweyk / Village Landais)
    'CLAIM-P11-0151': ('TAGGED', ['REF-00475', 'REF-00292'], None),   # 4% conclusion
    'CLAIM-P11-0152': ('TAGGED', ['REF-00512'], None),                # 94% De Hogeweyk
    'CLAIM-P11-0153': ('TAGGED', ['REF-00512'], None),                # 34%
    'CLAIM-P11-0154': ('TAGGED', ['REF-00026'], None),                # 47% toilet (Marquardt)
    'CLAIM-P11-0155': ('TAGGED', ['REF-00297'], None),                # 31% medication

    # §11.8.1 — Government adaptation program budgets
    'CLAIM-P11-0156': ('TAGGED', ['REF-00336', 'REF-00337'], None),   # 761m budget
    'CLAIM-P11-0157': ('TAGGED', ['REF-00336', 'REF-00337'], None),   # 600m
    'CLAIM-P11-0158': ('TAGGED', ['REF-00336', 'REF-00337'], None),   # 50m
    'CLAIM-P11-0159': ('TAGGED', ['REF-00334', 'REF-00335'], None),   # <4% (KfW)

    # §11.8.3 — International programs table
    'CLAIM-P11-0160': ('TAGGED', ['REF-00334', 'REF-00335'], None),   # 10% KfW
    'CLAIM-P11-0161': ('TAGGED', ['REF-00334', 'REF-00335'], None),   # 12.5%
    'CLAIM-P11-0162': ('TAGGED', ['REF-00334', 'REF-00335'], None),   # 90%
    'CLAIM-P11-0163': ('TAGGED', ['REF-00334', 'REF-00335'], None),   # 50%
    'CLAIM-P11-0164': ('TAGGED', ['REF-00334', 'REF-00335'], None),   # ≤10mm threshold
    'CLAIM-P11-0165': ('TAGGED', ['REF-00246'], None),                # 300mm Norway
    'CLAIM-P11-0166': ('TAGGED', ['REF-00246'], None),                # 25% Norway
    'CLAIM-P11-0167': ('DEFERRED', [], 'cross-reference parsing artifact — "000mm" = 3,000mm Boverket canopy dimension misextracted'),
    'CLAIM-P11-0168': ('TAGGED', ['REF-00292', 'REF-00293'], None),   # 0.94% Belgium
    'CLAIM-P11-0169': ('TAGGED', ['REF-00292', 'REF-00293'], None),   # 3.92%
    'CLAIM-P11-0170': ('TAGGED', ['REF-00336', 'REF-00337'], None),   # 90% Spain (best-avail)
    'CLAIM-P11-0171': ('TAGGED', ['REF-00336', 'REF-00337'], None),   # 50% Spain
    'CLAIM-P11-0172': ('TAGGED', ['REF-00336', 'REF-00337'], None),   # 3% Spain

    # §11.9 — Evidence citation table
    'CLAIM-P11-0173': ('TAGGED', ['REF-00026'], None),                # 47% toilet (Marquardt)
    'CLAIM-P11-0174': ('TAGGED', ['REF-00024', 'REF-00371'], None),   # ≥15mm threshold AIJ
    'CLAIM-P11-0175': ('TAGGED', ['REF-00512'], None),                # 94% loop plan
    'CLAIM-P11-0176': ('TAGGED', ['REF-00512'], None),                # 34%
    'CLAIM-P11-0177': ('TAGGED', ['REF-00297'], None),                # 31% medication
    'CLAIM-P11-0178': ('TAGGED', ['REF-00212', 'REF-00492'], None),   # 300mm reach zone
    'CLAIM-P11-0179': ('TAGGED', ['REF-00212', 'REF-00492'], None),   # 200mm
    'CLAIM-P11-0180': ('TAGGED', ['REF-00212', 'REF-00492'], None),   # 300mm
    'CLAIM-P11-0181': ('TAGGED', ['REF-00265', 'REF-00371'], None),   # 1–3% grab bar blocking

    # §11.10.4 — Editorial citation action items (all DEFERRED — not primary research claims)
    'CLAIM-P11-0182': ('DEFERRED', [], 'editorial citation action item — instruction to add Marquardt citation to item D-03'),
    'CLAIM-P11-0183': ('DEFERRED', [], 'editorial citation action item — instruction to add AIJ citation to item G-04'),
    'CLAIM-P11-0184': ('DEFERRED', [], 'editorial citation action item — instruction to add MHLW citation to Appendix C'),
    'CLAIM-P11-0185': ('DEFERRED', [], 'editorial citation action item — instruction to add DIN 18040-2 citation to item E-06'),
    'CLAIM-P11-0186': ('DEFERRED', [], 'editorial citation action item — instruction to add Danish dementia research citation to D-11'),
    'CLAIM-P11-0187': ('DEFERRED', [], 'editorial citation action item — storage reach zone reconciliation instruction'),
    'CLAIM-P11-0188': ('DEFERRED', [], 'editorial citation action item — reach zone reconciliation instruction'),
    'CLAIM-P11-0189': ('DEFERRED', [], 'editorial citation action item — reach zone reconciliation instruction'),
    'CLAIM-P11-0190': ('DEFERRED', [], 'editorial citation action item — reach zone reconciliation instruction'),
    'CLAIM-P11-0191': ('DEFERRED', [], 'editorial citation action item — reach zone reconciliation instruction'),
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

pending_remaining = [c for c in data if c['part'] == 11 and c['status'] == 'PENDING']
print(f'TAGGED this session: {tagged_count}')
print(f'DEFERRED this session: {deferred_count}')
print(f'Still PENDING in Part 11: {len(pending_remaining)}')
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
