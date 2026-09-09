// ITEMS — architect-facing spec data

export const ITEMS = [

  // ─────────── E-08 — Corridor Clear Width ───────────
  {
    cd:"E-08",
    t:"Corridor Clear Width ≥1200 mm on Primary Routes",
    q:"Can two power wheelchairs pass each other?",
    s:"Minimum clear width permitting two power wheelchairs to pass on primary circulation routes.",
    body:"Clear width is measured between obstructions, not between finished walls. Skirting boards, pin-boards, projecting signage, fire-hose reels, drinking fountains, and surface-mounted lighting all reduce effective width. Where these projections are unavoidable, the corridor must be widened to maintain ≥1200 mm between the projections themselves. Local widening to 1500 mm at door approaches and turning points.",
    why:"Two wheelchair users cannot meet in a 900 mm corridor. The cost of single-width corridors is daily — they exclude two people with mobility devices from being together in the building.",

    dimensions:[
      { dim:"Clear width — primary routes", value:"≥1200", unit:"mm", note:"Between fixed obstructions, not finished wall faces" },
      { dim:"Clear width — door approach", value:"≥1500", unit:"mm", note:"Localised widening at all door operations" },
      { dim:"Turning circle — power wheelchair", value:"≥1540", unit:"mm dia", note:"At dead-end termination of any corridor" },
      { dim:"Passing bay — single-width corridors only", value:"1800 × 2000", unit:"mm", note:"Maximum 12 m apart where 1200 mm cannot be achieved" },
      { dim:"Headroom", value:"≥2000", unit:"mm", note:"Continuous; signage and ducts must not encroach" },
      { dim:"Maximum projection from wall", value:"≤100", unit:"mm", note:"Below 2000 mm AFF; above this projection unrestricted" },
    ],
    performance:[
      { metric:"Two-wheelchair passing", target:"Pass without contact", measure:"Field verify with two test wheelchairs, 700 mm wide each" },
      { metric:"Cane sweep clearance", target:"Both walls reachable from centre", measure:"Long-cane technique per O&M training standards" },
    ],
    codes:[
      { ref:"AS 1428.1:2021", clause:"§7.1 (Continuous accessible path of travel)", jurisdiction:"AU" },
      { ref:"AS 1428.2:1992", clause:"§9 (Enhanced widths for circulation)", jurisdiction:"AU" },
      { ref:"NCC 2022 Vol 1", clause:"D4D5", jurisdiction:"AU" },
      { ref:"ADA 2010", clause:"§403.5.1 (1525 mm passing requirement)", jurisdiction:"US" },
      { ref:"ISO 21542:2021", clause:"§8.4", jurisdiction:"INTL" },
    ],
    products:["No products — this is dimensional planning. Specify in plan and section."],
    schedule:"Primary circulation routes shall provide minimum clear width of 1200 mm measured between fixed obstructions, increasing to 1500 mm at door approaches and turning points. Headroom to be maintained at 2000 mm minimum continuous. No projections below 2000 mm AFF to exceed 100 mm from finished wall face. Where 1200 mm cannot be achieved continuously, passing bays of 1800 × 2000 mm at maximum 12 m centres.",
    detail:[
      { title:"Wall-mounted equipment", items:[
        "Set fire-hose reels in recessed wall niches — full depth.",
        "Drinking fountains in alcoves, not surface-mounted.",
        "Pin-boards flush-set; if surface, count the projection toward 100 mm limit.",
        "Light fittings recessed or above 2000 mm AFF.",
        "Skirting boards count toward width if >100 mm from wall.",
      ]},
      { title:"At door operations", items:[
        "Widen to 1500 mm starting 600 mm before the door swing.",
        "Door swing must not encroach into the 1200 mm continuous width.",
        "Allow 300 mm latch-side clearance on pull side per AS 1428.1 §13.",
      ]},
      { title:"At corners and changes of direction", items:[
        "Inside corners: confirm 1200 mm maintained on the diagonal.",
        "T-junctions: 1500 × 1500 mm clear at the junction itself.",
        "Right-angle turns: see D-07 for blind-corner treatment.",
      ]},
    ],
    diagram:{
      type:"plan",
      svg:`<svg viewBox="0 0 320 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan diagram showing 1200 mm clear corridor with 1500 mm widening at door approach">
        <rect x="0" y="0" width="320" height="160" fill="none"/>
        <rect x="10" y="20" width="300" height="120" fill="none" stroke="#1A1612" stroke-width="2"/>
        <line x1="10" y1="80" x2="180" y2="80" stroke="#1A1612" stroke-width="0.5" stroke-dasharray="4 3"/>
        <text x="20" y="55" font-family="JetBrains Mono, monospace" font-size="10" fill="#1A1612">1200 mm clear</text>
        <line x1="20" y1="65" x2="170" y2="65" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="20" y1="62" x2="20" y2="68" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="170" y1="62" x2="170" y2="68" stroke="#1A1612" stroke-width="0.6"/>
        <text x="20" y="105" font-family="JetBrains Mono, monospace" font-size="10" fill="#1A1612">two passes</text>
        <circle cx="60" cy="105" r="14" fill="none" stroke="#1A1612" stroke-width="1"/>
        <circle cx="130" cy="105" r="14" fill="none" stroke="#1A1612" stroke-width="1"/>
        <rect x="195" y="20" width="115" height="120" fill="#1A1612" fill-opacity="0.05" stroke="none"/>
        <text x="205" y="55" font-family="JetBrains Mono, monospace" font-size="10" fill="#1A1612">1500 mm</text>
        <text x="205" y="68" font-family="JetBrains Mono, monospace" font-size="10" fill="#1A1612">door zone</text>
        <line x1="280" y1="20" x2="280" y2="80" stroke="#1A1612" stroke-width="2.5"/>
        <path d="M 280 80 Q 270 60 250 50" fill="none" stroke="#1A1612" stroke-width="1" stroke-dasharray="2 2"/>
        <text x="225" y="135" font-family="JetBrains Mono, monospace" font-size="9" fill="#6B5F50">door</text>
      </svg>`
    },
    install:[
      "Set out from clear zones, not wall lines. Mark the 1200 mm zone on slab before partition framing.",
      "Verify clear width after services rough-in but before linings — projection from MEP fixings is the most common failure.",
      "Door swing arcs to be confirmed in plan and field-verified before frame fixing.",
    ],
    failures:[
      "Specifying 1200 mm wall-to-wall and losing 60 mm to skirting and 80 mm to pinboards on each side — effective 920 mm.",
      "Surface-mounted hand sanitiser dispensers added late in design or post-occupation, projecting 150 mm.",
      "Fire-hose reels set surface to wall instead of recessed.",
      "Door swings overlapping the 1200 mm clear zone, locking width to 800 mm during operation.",
    ],
    popReasons:{
      "MOB":"Power wheelchairs are 700–800 mm wide; passing requires 1200 mm minimum at the projections.",
      "ALL":"Wider corridors benefit families, mobility-aid users of all kinds, evacuation flow."
    },
    evidence:[
      { tier:"6", source:"AS 1428.1:2021 — Design for access and mobility, Part 1: General requirements" },
      { tier:"4", source:"ISO 21542:2021 — Building construction: Accessibility and usability" },
      { tier:"3", source:"Steinfeld et al., 'Universal Design: Designing Inclusive Environments' (2012)" }
    ],
    tr:0, p:["MOB","ALL"], cat:"E", topics:["circulation"],
    rooms:["R-HAL","NR-HLT","NR-EDU","NR-WRK","NR-CUL","NR-TRP"],
    related:[
      { cd:"D-07", why:"Blind-corner treatment requires width to give reaction space" },
      { cd:"E-10", why:"Rest seating must be in alcoves to preserve corridor width" },
      { cd:"E-11", why:"Automatic doors eliminate door-swing width loss" },
      { cd:"D-04", why:"Landmarks at decision points work with adequate width to orient" },
    ]
  },

  // ─────────── G-04 — Accessible Bathroom Wet Room ───────────
  {
    cd:"G-04",
    t:"Accessible Bathroom — Wet Room, Zero Threshold",
    q:"Is the bathroom a wet room with zero threshold?",
    s:"Roll-in shower with no curb, graded waterproof floor, slip-resistant finish, and clear transfer zones.",
    body:"The accessible bathroom is the most complex single-room integration in the guidebook. Wet-room configuration eliminates the threshold problem. Floor falls (1:80 to drain) handle water management without curbs. Linear drain at the shower head prevents wet-zone water reaching transfer zones. WC and shower clear zones overlap with circulation; positioning is the design problem.",
    why:"The bathroom is where mobility, dignity, and safety meet most directly. A 25 mm shower curb defeats wheelchair entry as completely as a stair would.",

    dimensions:[
      { dim:"Minimum room — corner WC layout", value:"2400 × 2100", unit:"mm", note:"Per AS 1428.1 §15. Wet room adds shower clear zone overlap" },
      { dim:"WC clear floor space — alongside", value:"950 × 1300", unit:"mm", note:"Beside the pan, free of obstruction" },
      { dim:"WC clear floor space — in front", value:"1200 × 1900", unit:"mm", note:"Excluding the pan footprint" },
      { dim:"Shower clear zone", value:"1200 × 1200", unit:"mm", note:"Free of obstruction at floor level" },
      { dim:"Pan height — toilet", value:"460–480", unit:"mm AFF", note:"To top of seat" },
      { dim:"Pan setback from wall", value:"400", unit:"mm", note:"Centreline to side wall, transfer side" },
      { dim:"Floor fall to drain", value:"1:80", unit:"max", note:"Steeper than 1:80 affects wheelchair stability; 1:100 preferred" },
      { dim:"Linear drain — length", value:"≥800", unit:"mm", note:"Across full shower head wall, channel grate" },
      { dim:"Shower controls — height", value:"900–1100", unit:"mm AFF", note:"Mixer, divertor, hand shower clip" },
      { dim:"Shower controls — offset", value:"600–650", unit:"mm", note:"From back wall on entry side" },
      { dim:"Door clear opening", value:"≥850", unit:"mm", note:"Per AS 1428.1 §13. 870 mm preferred for power wheelchair" },
      { dim:"Door swing — outward", value:"required", unit:"", note:"Inward swing is non-compliant — blocks rescue access" },
      { dim:"Threshold to door", value:"0", unit:"mm", note:"Continuous floor finish under door" },
    ],
    performance:[
      { metric:"Slip resistance — wet", value:"P5 / R12", target:"Pendulum Test Value ≥45 wet", measure:"AS 4586 wet pendulum test" },
      { metric:"Slip resistance — dry", value:"P4 minimum", target:"Pendulum Test Value ≥35 dry", measure:"AS 4586 dry pendulum test" },
      { metric:"Waterproofing", target:"Class 3 wet area", measure:"AS 3740-2021 — Waterproofing of domestic wet areas" },
      { metric:"Drainage capacity", target:"No standing water 60 sec post-flow", measure:"On-site test at commissioning" },
    ],
    codes:[
      { ref:"AS 1428.1:2021", clause:"§15 (Sanitary facilities)", jurisdiction:"AU" },
      { ref:"AS 1428.1:2021", clause:"§15.2 (Toilet pan setback and height)", jurisdiction:"AU" },
      { ref:"AS 3740:2021", clause:"§4 (Wet area waterproofing)", jurisdiction:"AU" },
      { ref:"AS 4586:2013", clause:"Slip resistance classification", jurisdiction:"AU" },
      { ref:"NCC 2022 Vol 2", clause:"H4P1, H4D2 (Wet areas)", jurisdiction:"AU" },
      { ref:"ADA 2010", clause:"§604, §608 (Toilet and shower)", jurisdiction:"US" },
    ],
    products:[
      "Linear shower drain — channel grate, 800–1200 mm",
      "Wall-faced toilet pan with concealed cistern (cleaning + transfer clearance)",
      "Single-lever mixer, anti-scald limited (38°C max delivery)",
      "Hand shower on slide rail, 1200 mm vertical adjustment",
      "Slip-resistant tile or vinyl, P5 wet rated",
      "Graded substrate (cement screed) prior to waterproofing",
    ],
    schedule:"Bathroom configured as wet room. Continuous slip-resistant floor finish (AS 4586 P5 wet, P4 dry) with falls to linear drain at shower head wall. No threshold at door or shower. Toilet wall-faced, 460–480 mm seat height, set 400 mm centreline from transfer wall. Shower controls 900–1100 mm AFF, offset 600 mm from back wall on entry side. Anti-scald mixer limited to 38°C delivery. Door clear opening 850 mm minimum, outward swing. Waterproofing to AS 3740 Class 3.",
    detail:[
      { title:"Floor falls and drainage", items:[
        "Set out floor falls before substrate placement; verify with laser before screed.",
        "Linear drain along full shower head wall — not corner gully.",
        "Falls 1:80 maximum; 1:100 preferred for wheelchair stability.",
        "Falls direct water away from WC and door zones.",
        "Drain channel set 5 mm below adjacent floor finish to receive water.",
      ]},
      { title:"Waterproofing", items:[
        "Membrane to 1800 mm above floor in shower zone, 150 mm elsewhere.",
        "Membrane returns 100 mm up door reveal.",
        "Cove all internal corners — no sharp returns.",
        "Penetration seals at all services; test before tiling.",
      ]},
      { title:"Grab bar provision (coordinate with G-03)", items:[
        "Behind WC — 600 mm horizontal, 800 mm AFF.",
        "Beside WC transfer side — 800 mm horizontal, 800 mm AFF.",
        "Shower wall — 600 mm vertical entry, 800 mm horizontal at controls.",
        "All bars rated to 1.5 kN downward, 1.0 kN outward per AS 1428.1.",
        "Backing — 18 mm ply or proprietary fixing system, full wall before lining.",
      ]},
      { title:"Door operation", items:[
        "Outward swing mandatory — inward swing blocks rescue.",
        "D-pull or lever hardware (see I-01).",
        "Threshold continuous floor finish — no aluminium track.",
        "Clear opening 850 mm minimum with door at 90°.",
      ]},
    ],
    diagram:{
      type:"plan",
      svg:`<svg viewBox="0 0 320 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan of accessible wet-room bathroom showing WC clear zone, shower clear zone, linear drain, and door swing">
        <rect x="20" y="20" width="280" height="200" fill="none" stroke="#1A1612" stroke-width="2"/>
        <!-- WC -->
        <ellipse cx="80" cy="60" rx="22" ry="16" fill="none" stroke="#1A1612" stroke-width="1.2"/>
        <rect x="60" y="40" width="40" height="14" fill="#1A1612" fill-opacity="0.1" stroke="#1A1612" stroke-width="0.8"/>
        <!-- WC clear zone alongside -->
        <rect x="105" y="30" width="80" height="80" fill="none" stroke="#1A1612" stroke-width="0.6" stroke-dasharray="4 3"/>
        <text x="115" y="65" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">WC zone</text>
        <text x="115" y="78" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">950 × 1300</text>
        <!-- Shower clear zone -->
        <rect x="200" y="30" width="80" height="80" fill="#1A1612" fill-opacity="0.04" stroke="#1A1612" stroke-width="0.6" stroke-dasharray="4 3"/>
        <text x="215" y="55" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">SHOWER</text>
        <text x="212" y="68" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">1200 × 1200</text>
        <!-- Linear drain at shower wall -->
        <rect x="200" y="28" width="80" height="4" fill="#1A1612"/>
        <text x="200" y="22" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">linear drain ≥800</text>
        <!-- Shower controls -->
        <circle cx="206" cy="90" r="3" fill="#1A1612"/>
        <text x="160" y="125" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">controls offset 600</text>
        <!-- Falls arrows -->
        <path d="M 110 180 L 240 50" stroke="#1A1612" stroke-width="0.4" stroke-dasharray="2 2"/>
        <text x="55" y="180" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">fall 1:80 →</text>
        <!-- Door -->
        <line x1="120" y1="220" x2="170" y2="220" stroke="#fff" stroke-width="3"/>
        <line x1="120" y1="220" x2="170" y2="220" stroke="#1A1612" stroke-width="1.5" stroke-dasharray="4 2"/>
        <path d="M 120 220 Q 120 195 145 195" fill="none" stroke="#1A1612" stroke-width="0.8" stroke-dasharray="2 2"/>
        <text x="115" y="235" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">≥850 mm</text>
        <!-- Vanity zone (not detailed) -->
        <rect x="20" y="170" width="60" height="50" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.6"/>
        <text x="25" y="200" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">vanity</text>
      </svg>`
    },
    install:[
      "Set out falls before substrate. Use laser level; mark drain centre line on slab.",
      "Coordinate plumbing rough-in with grab-bar backing — both behind walls before lining.",
      "Door reveal waterproofing must complete before frame fix.",
      "Anti-scald mixer commissioned and certified at handover; document delivery temperature.",
      "Threshold confirmed level after final floor finish — measure with straight edge.",
    ],
    failures:[
      "Shower curb retained 'just in case' — defeats wheelchair entry.",
      "Floor falls set after framing; drain ends up at high point of slab.",
      "Falls steeper than 1:80 cause wheelchair tip risk in transfer.",
      "Inward-swinging door blocks rescue when occupant falls against it.",
      "Anti-scald mixer omitted; delivery >43°C scalds in seconds.",
      "Grab bar backing forgotten; bars cannot be installed at certification stage.",
      "Linear drain replaced with corner gully — water tracks across WC zone.",
    ],
    popReasons:{
      "MOB":"Roll-in access without curb is the only configuration that works for wheelchair users; transfer zones must align with WC and shower.",
      "ALL":"Wet-room configuration supports aging in place and rescue access for any user.",
    },
    evidence:[
      { tier:"6", source:"AS 1428.1:2021 — Sanitary facilities" },
      { tier:"6", source:"AS 3740:2021 — Waterproofing of domestic wet areas" },
      { tier:"Co-2", source:"OT Australia — Bathroom modification practice guidelines" },
    ],
    tr:0, p:["MOB","ALL"], cat:"G", topics:["toileting"],
    rooms:["R-BA","NR-HLT","NR-HOS"],
    related:[
      { cd:"G-03", why:"Grab bars complete the bathroom configuration; backing must coordinate" },
      { cd:"E-07", why:"Slip resistance is critical in continuously wet environments" },
      { cd:"I-03", why:"Bathroom hardware and anti-scald mixer follow the same one-hand principle" },
      { cd:"H-01", why:"Shower controls must comply with reach-range requirements" },
      { cd:"B-12", why:"Overnight pathway lighting terminates at the bathroom" },
    ]
  },

  // ─────────── A-02 — Acoustic Ceiling Panels ───────────
  {
    cd:"A-02",
    t:"Acoustic Ceiling Panels, NRC ≥0.85",
    q:"How much do voices and footsteps reverberate in this space?",
    s:"Acoustic ceiling treatment in occupied spaces. Reduces reverberation and supports speech intelligibility.",
    body:"NRC (Noise Reduction Coefficient) is the average sound absorption across speech frequencies, on a scale from 0 (perfect reflector) to 1 (perfect absorber). NRC ≥0.85 is achievable with several product types. Specify ceiling-to-floor coverage of at least 70% of ceiling area. Avoid hard plaster ceilings in any space where speech intelligibility matters.",
    why:"Reverberation degrades speech intelligibility, increases listening effort, and triggers sensory overload. The cost is highest for the populations with least margin: hearing-aid users, neurological populations, and those for whom speech in noise is already a struggle.",

    dimensions:[
      { dim:"Coverage area — minimum", value:"≥70%", unit:"of ceiling", note:"Continuous; islands less effective" },
      { dim:"Panel-to-deck cavity", value:"≥150", unit:"mm", note:"Plenum depth affects low-frequency absorption" },
      { dim:"Suspension drop — clear height retained", value:"≥2700", unit:"mm AFF", note:"Plenum can compromise headroom" },
      { dim:"RT60 target — meeting/learning spaces", value:"≤0.6", unit:"sec", note:"500–1000 Hz octaves, occupied" },
      { dim:"RT60 target — open-plan office", value:"≤0.4", unit:"sec", note:"500–1000 Hz octaves, occupied" },
      { dim:"RT60 target — auditoria (speech)", value:"≤0.9", unit:"sec", note:"With absorption + diffusion balance" },
    ],
    performance:[
      { metric:"NRC (Noise Reduction Coefficient)", target:"≥0.85", measure:"ASTM C423 / ISO 354 reverberation chamber" },
      { metric:"αw (weighted sound absorption coefficient)", target:"≥0.85, Class A", measure:"ISO 11654" },
      { metric:"AC (Articulation Class)", target:"≥210", measure:"ASTM E1110 — for open-plan speech privacy" },
      { metric:"CAC (Ceiling Attenuation Class)", target:"≥35", measure:"ASTM E1414 — where rooms share plenum" },
      { metric:"Light reflectance", target:"≥0.80", measure:"ASTM E1477 — for daylight redistribution" },
    ],
    codes:[
      { ref:"AS/NZS 2107:2016", clause:"Recommended design sound levels and reverberation times", jurisdiction:"AU/NZ" },
      { ref:"BB93", clause:"Acoustic design of schools (UK)", jurisdiction:"UK" },
      { ref:"ANSI/ASA S12.60-2010", clause:"Classroom acoustics", jurisdiction:"US" },
      { ref:"WELL Building Standard v2", clause:"Sound concept S03", jurisdiction:"INTL" },
      { ref:"NCC 2022 Vol 1", clause:"F7P1 (Healthcare/aged care acoustic)", jurisdiction:"AU" },
    ],
    products:[
      "Mineral fibre ceiling tile (NRC 0.85–0.95)",
      "Perforated metal pan with mineral wool backing",
      "Wood wool cement panel (NRC 0.85–1.00)",
      "Stretched-fabric acoustic ceiling system",
      "Suspended baffle/cloud arrays (where full plane unavailable)",
    ],
    schedule:"Suspended acoustic ceiling system, NRC ≥0.85 per ASTM C423, covering ≥70% of ceiling plane. Plenum cavity ≥150 mm to deck. Where rooms share plenum, system to achieve CAC ≥35. Light reflectance ≥0.80. Where suspended ceiling is not feasible, equivalent absorption to be provided via wall panels and baffles to achieve target RT60 per AS/NZS 2107 occupied condition.",
    detail:[
      { title:"Coverage strategy", items:[
        "Continuous plane preferred over islands.",
        "Where MEP services prevent full plane: ≥70% with islands ≥1.2 m on shortest dimension.",
        "Avoid linear gaps perpendicular to room long axis (creates flutter).",
        "Coordinate with lighting (B-04, B-07) — recessed luminaires reduce effective absorption area.",
      ]},
      { title:"Suspension and plenum", items:[
        "150 mm minimum drop to allow low-frequency absorption.",
        "Suspension grid concealed where possible (visual quality, especially in healthcare).",
        "Lay-in tiles must be removable for service access without lifting adjacent.",
        "Seismic restraints where applicable — verify with structure.",
      ]},
      { title:"Where rooms share plenum", items:[
        "Specify CAC ≥35 to prevent flanking transmission.",
        "Consider plenum barriers above demising walls (extends partition above ceiling).",
        "Coordinate with A-14 (double-leaf partition) — both required where high acoustic separation needed.",
      ]},
      { title:"Hard ceilings (where required by structure or aesthetic)", items:[
        "Compensate with wall panels (A-06) at ≥30% wall area.",
        "Add suspended baffles at ≥1 unit per 4 m² floor area.",
        "Verify final RT60 by acoustic calculation before finalising.",
      ]},
    ],
    diagram:{
      type:"section",
      svg:`<svg viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Section diagram showing suspended acoustic ceiling at 150 mm plenum, panels covering 70% of ceiling plane">
        <!-- Slab above -->
        <rect x="20" y="20" width="280" height="14" fill="#1A1612" fill-opacity="0.85"/>
        <text x="20" y="14" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">slab / deck above</text>
        <!-- Plenum -->
        <rect x="20" y="34" width="280" height="40" fill="#1A1612" fill-opacity="0.04"/>
        <text x="200" y="58" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">plenum ≥150</text>
        <!-- Suspension wires -->
        <line x1="60" y1="34" x2="60" y2="74" stroke="#1A1612" stroke-width="0.4"/>
        <line x1="120" y1="34" x2="120" y2="74" stroke="#1A1612" stroke-width="0.4"/>
        <line x1="180" y1="34" x2="180" y2="74" stroke="#1A1612" stroke-width="0.4"/>
        <line x1="240" y1="34" x2="240" y2="74" stroke="#1A1612" stroke-width="0.4"/>
        <!-- Acoustic ceiling -->
        <rect x="20" y="74" width="280" height="6" fill="#1A1612" fill-opacity="0.25" stroke="#1A1612" stroke-width="0.5"/>
        <text x="105" y="92" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">NRC ≥0.85, ≥70% coverage</text>
        <!-- Floor -->
        <rect x="20" y="180" width="280" height="6" fill="#1A1612" fill-opacity="0.6"/>
        <!-- Sound absorption indication -->
        <path d="M 80 180 Q 90 130 100 80" fill="none" stroke="#1A1612" stroke-width="0.5" stroke-dasharray="2 2"/>
        <path d="M 90 180 Q 100 130 110 80" fill="none" stroke="#1A1612" stroke-width="0.5" stroke-dasharray="2 2"/>
        <!-- Person dimension -->
        <line x1="260" y1="80" x2="260" y2="180" stroke="#1A1612" stroke-width="0.4"/>
        <line x1="257" y1="80" x2="263" y2="80" stroke="#1A1612" stroke-width="0.4"/>
        <line x1="257" y1="180" x2="263" y2="180" stroke="#1A1612" stroke-width="0.4"/>
        <text x="265" y="135" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">≥2700</text>
        <text x="265" y="146" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">AFF</text>
      </svg>`
    },
    install:[
      "Set out grid before MEP rough-in to coordinate diffuser, sprinkler, and luminaire positions.",
      "Verify CAC requirement before tile selection — many high-NRC tiles have low CAC.",
      "Field RT60 measurement at commissioning — required for healthcare and education projects.",
      "Lay-in tiles to be 600 × 600 or 1200 × 600; verify accessibility for service tasks.",
    ],
    failures:[
      "Specifying NRC ≥0.85 but allowing only 50% coverage — effective absorption inadequate.",
      "Hard plaster ceiling with 'feature' acoustic panels — fails RT60 entirely.",
      "Plenum used for return air without CAC consideration — speech privacy lost.",
      "High-NRC, low-CAC tiles selected without checking — adjacent rooms hear everything.",
      "Recessed luminaires reduce effective absorption to <60% without compensation.",
    ],
    popReasons:{
      "ALL":"Reverberation reduces speech intelligibility for everyone; some populations cannot compensate.",
      "DEAF":"Hearing aids amplify reverberation along with target speech — high RT60 makes loops effectively unusable.",
      "NDV":"Reverberant rooms produce auditory overload disproportionate to the actual sound source.",
      "NEU":"Listening effort in reverberant spaces consumes cognitive resources needed elsewhere.",
    },
    evidence:[
      { tier:"4", source:"AS/NZS 2107:2016 reverberation time requirements" },
      { tier:"4", source:"BB93 (UK) — Acoustic design of schools" },
      { tier:"3", source:"Picard & Bradley (2001), 'Revisiting speech interference in classrooms', Audiology" },
    ],
    tr:0, p:["ALL"], cat:"A", topics:["sensory"],
    rooms:["NR-EDU","NR-HLT","NR-WRK","NR-CUL","R-LIV"],
    related:[
      { cd:"A-05", why:"Soft floor finishes complete the absorption strategy" },
      { cd:"A-06", why:"Wall panels treat reflection paths the ceiling cannot reach" },
      { cd:"A-10", why:"Hearing loops require low RT60 to function" },
      { cd:"A-11", why:"Assembly spaces have stricter reverberation requirements" },
      { cd:"A-14", why:"Where ceilings share plenum, partition + ceiling integration is required" },
    ]
  },

  // ─────────── B-04 — Flicker-Free LED ───────────
  {
    cd:"B-04",
    t:"Flicker-Free LED, IEEE 1789-2015 Compliant",
    q:"Do the lights flicker — even imperceptibly?",
    s:"Specify only luminaires that meet recommended flicker thresholds across all dimming levels.",
    body:"IEEE 1789-2015 defines two regions: 'low-risk' and 'no-effect'. Specify 'no-effect' where possible; require 'low-risk' as minimum. Crucially, the standard must apply across the dimming range — many fixtures are flicker-free at full output but flicker badly when dimmed.",
    why:"Flicker that 'isn't visible' is still detected by the visual cortex. Sensitive populations experience consequences — migraine, seizure, sensory overload — without being able to identify the cause.",

    dimensions:[
      { dim:"Mounting height — task lighting", value:"600–800", unit:"mm above task", note:"For local control luminaires" },
      { dim:"Mounting height — general", value:"≥2700", unit:"mm AFF", note:"Or per architectural reflected ceiling plan" },
      { dim:"Spacing-to-mounting-height ratio", value:"per manufacturer", unit:"", note:"Verify uniformity ≥0.7 in design" },
    ],
    performance:[
      { metric:"Flicker — IEEE 1789-2015 'no-effect' region", target:"Mod% < (Frequency × 0.0333) for f<90 Hz, < (Frequency × 0.08) for f≥90 Hz", measure:"IEEE 1789-2015 percentile flicker measurement" },
      { metric:"Flicker — minimum 'low-risk' compliance", target:"Mod% < (Frequency × 0.08) for f<90 Hz", measure:"As above" },
      { metric:"Across dimming range", target:"Compliant at 1%, 10%, 50%, 100%", measure:"Test at minimum 4 dimming levels" },
      { metric:"Stroboscopic Visibility Measure (SVM)", target:"≤0.4", measure:"CIE TN 006:2016" },
      { metric:"Colour rendering — CRI", target:"≥80, R9 ≥50", measure:"CIE 13.3" },
      { metric:"TM-30 Rf / Rg", target:"Rf ≥85, Rg 95–105", measure:"IES TM-30-20 (preferred over CRI)" },
    ],
    codes:[
      { ref:"IEEE 1789-2015", clause:"Recommended Practices for Modulating Current in High-Brightness LEDs", jurisdiction:"INTL" },
      { ref:"CIE TN 006:2016", clause:"Visual aspects of time-modulated lighting systems", jurisdiction:"INTL" },
      { ref:"AS/NZS 1680.1:2006", clause:"Interior and workplace lighting — General principles", jurisdiction:"AU/NZ" },
      { ref:"WELL Building Standard v2", clause:"L02 (Visual Lighting Design)", jurisdiction:"INTL" },
    ],
    products:[
      "LED luminaire with constant-current driver, ≥3000 Hz PWM frequency",
      "Drivers with CCR (constant-current reduction) dimming preferred over PWM at low percentages",
      "DALI-2 compatible drivers (verifiable performance metrics)",
      "Avoid: low-cost LED retrofits, magnetic transformer + LED combinations",
    ],
    schedule:"All luminaires throughout the project to comply with IEEE 1789-2015 'no-effect' region across the full operational dimming range (1–100%). Drivers to be constant-current; PWM dimming where used to operate above 3000 Hz. Manufacturer flicker performance data required for submittal review across at least 4 dimming levels (1%, 10%, 50%, 100%). Stroboscopic Visibility Measure (CIE TN 006) ≤0.4. CRI ≥80, R9 ≥50, or TM-30 Rf ≥85.",
    detail:[
      { title:"Driver selection", items:[
        "Constant-current reduction (CCR) drivers preferred for sensitive applications.",
        "PWM drivers acceptable only above 3000 Hz operating frequency.",
        "Verify driver behaviour at 1% dim — many drivers fail compliance below 10%.",
        "DALI-2 certification provides verifiable performance metrics.",
      ]},
      { title:"Dimming range coordination", items:[
        "Specify dimming range required by use (1–100% for sensitive spaces).",
        "Match dimmer to driver — incompatible pairings cause flicker even with compliant fixtures.",
        "Verify with manufacturer compatibility chart before specification.",
      ]},
      { title:"Submittal review", items:[
        "Require IEEE 1789-2015 test data at submittal.",
        "Require SVM test data per CIE TN 006.",
        "Reject products with 'compliant at 100%' only — must be across range.",
      ]},
    ],
    diagram:{
      type:"chart",
      svg:`<svg viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="IEEE 1789-2015 flicker risk regions chart showing modulation percentage vs frequency">
        <!-- Axes -->
        <line x1="40" y1="170" x2="300" y2="170" stroke="#1A1612" stroke-width="1"/>
        <line x1="40" y1="170" x2="40" y2="20" stroke="#1A1612" stroke-width="1"/>
        <text x="155" y="190" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612" text-anchor="middle">Frequency (Hz)</text>
        <text x="20" y="100" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612" transform="rotate(-90 20 100)" text-anchor="middle">Mod %</text>
        <!-- frequency labels -->
        <text x="80" y="183" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">90</text>
        <text x="160" y="183" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">1000</text>
        <text x="260" y="183" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">3000+</text>
        <!-- High risk (red zone, top) -->
        <path d="M 40 20 L 80 20 L 80 110 L 40 170 Z" fill="#1A1612" fill-opacity="0.5"/>
        <text x="50" y="55" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">HIGH RISK</text>
        <!-- Low-risk -->
        <path d="M 80 20 L 160 20 L 160 130 L 80 110 Z" fill="#1A1612" fill-opacity="0.2"/>
        <text x="105" y="80" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">LOW-RISK</text>
        <!-- No-effect -->
        <path d="M 160 20 L 300 20 L 300 170 L 160 130 Z" fill="#1A1612" fill-opacity="0.05"/>
        <text x="200" y="80" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">NO-EFFECT (target)</text>
        <text x="200" y="92" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">specify here</text>
      </svg>`
    },
    install:[
      "Specify driver model alongside fixture — drivers determine flicker, not LEDs.",
      "Field measure flicker at commissioning with PocketFlicker or equivalent meter.",
      "Test at multiple dimming levels — 1%, 10%, 50%, 100%.",
      "Document results in O&M manual.",
    ],
    failures:[
      "Specifying 'flicker-free' without referencing IEEE 1789 — meaningless without thresholds.",
      "Compliant at 100%, severe flicker at 5% — common with cheap dimmers.",
      "Magnetic transformer + LED retrofit — produces 100/120 Hz flicker like fluorescent.",
      "Mismatched dimmer and driver — even compliant fixtures flicker.",
      "Cost cuts at procurement substituting non-compliant drivers post-specification.",
    ],
    popReasons:{
      "ALL":"Universal benefit; no population is harmed by flicker-free light.",
      "NDV":"Visible and sub-visible flicker triggers visual cortex hyperexcitation and sensory overload.",
      "NEU":"Post-concussion visual sensitivity; flicker triggers headache and cognitive symptoms.",
      "PAIN":"Flicker triggers migraine directly; fibromyalgia symptom flare.",
    },
    evidence:[
      { tier:"4", source:"IEEE 1789-2015 — Recommended practices for modulating current in LEDs" },
      { tier:"4", source:"CIE TN 006:2016 — Visual aspects of time-modulated lighting systems" },
      { tier:"3", source:"Wilkins (1995), 'Visual stress and migraine'" },
    ],
    tr:0, p:["ALL"], cat:"B", topics:["lighting"],
    rooms:["ALL"],
    related:[
      { cd:"B-03", why:"Eliminating fluorescents is the first step; LED specification is the second" },
      { cd:"B-06", why:"Dimming control compounds risk if drivers flicker at low output" },
      { cd:"B-07", why:"Indirect lighting reduces visual stress further" },
    ]
  },

  // ─────────── C-04 — LRV Contrast ───────────
  {
    cd:"C-04",
    t:"LRV Contrast ≥30 at Critical Junctions",
    q:"Can low-vision users see edges, doors, controls?",
    s:"Light reflectance value differential between adjacent surfaces at doors, edges, controls.",
    body:"Light Reflectance Value differential of 30 percentage points between adjacent surfaces at every critical junction. Measured under specified lighting conditions on as-installed surfaces — not from manufacturer brochure.",
    why:"Without contrast, low-vision users cannot find doors, controls, or edges. The cost is high — failure to navigate, falls, inability to use the environment.",

    dimensions:[
      { dim:"LRV differential — minimum", value:"≥30", unit:"percentage points", note:"Adjacent surfaces at critical junctions" },
      { dim:"LRV differential — preferred", value:"≥40", unit:"percentage points", note:"Where wayfinding is primary function" },
      { dim:"Glazing visual indicator — band 1", value:"900–1000", unit:"mm AFF", note:"Lower band — wheelchair eye level" },
      { dim:"Glazing visual indicator — band 2", value:"1500–1600", unit:"mm AFF", note:"Upper band — standing eye level" },
      { dim:"Indicator band height", value:"≥75", unit:"mm", note:"Continuous solid band" },
      { dim:"Stair nosing contrast strip width", value:"50–75", unit:"mm", note:"On both tread and riser" },
    ],
    performance:[
      { metric:"LRV — light surface", target:"Measured value", measure:"BS 8493:2008 / NCS or RAL with LRV value" },
      { metric:"LRV differential", target:"≥30 percentage points", measure:"Field measurement with LRV meter or reference card" },
      { metric:"Glazing manifestation visibility", target:"Detectable from 2 m at design lighting", measure:"AS 1428.1 §6.6 verification" },
    ],
    codes:[
      { ref:"AS 1428.1:2021", clause:"§6.6 (Luminance contrast — glazing)", jurisdiction:"AU" },
      { ref:"AS 1428.1:2021", clause:"§11 (Stair nosings, contrast)", jurisdiction:"AU" },
      { ref:"AS 1428.4.1:2009", clause:"Tactile indicators — luminance contrast", jurisdiction:"AU" },
      { ref:"BS 8493:2008", clause:"Light reflectance value of a surface", jurisdiction:"UK" },
      { ref:"ADA 2010", clause:"§504.4 (Stair nosing)", jurisdiction:"US" },
    ],
    products:[
      "Door hardware contrasting frame: contrast measured plate to frame, not plate to wall",
      "Stair nosing — solid contrasting strip, 50–75 mm",
      "Glazing manifestation — applied film, fritted glass, or etched bands",
      "Switch and outlet plates — contrast specified to wall finish, not just to switch",
      "Tactile ground surface indicators — colour LRV per AS 1428.4.1",
    ],
    schedule:"Luminance contrast (LRV differential) of 30 percentage points minimum maintained at: door leaves vs. frames, frames vs. walls, control plates vs. surrounds, stair nosings on both tread and riser, glazing manifestations at two heights (900–1000 mm and 1500–1600 mm AFF), tactile ground surface indicators per AS 1428.4.1. Verify by field measurement on installed materials, not manufacturer literature.",
    detail:[
      { title:"Door hardware", items:[
        "Lever or D-pull plate contrasts ≥30 LRV against door leaf.",
        "Door leaf contrasts ≥30 LRV against frame.",
        "Frame contrasts ≥30 LRV against wall.",
        "Strike plates and hinges considered as part of frame visual identity.",
      ]},
      { title:"Glazing", items:[
        "Two horizontal bands of solid manifestation per AS 1428.1.",
        "Lower band 900–1000 mm AFF — wheelchair seated eye level.",
        "Upper band 1500–1600 mm AFF — standing eye level.",
        "Bands ≥75 mm high; LRV differential ≥30 against background seen through glazing.",
        "Frosted bands work in light conditions; etched in light + dark.",
      ]},
      { title:"Stair nosings", items:[
        "Solid contrasting strip 50–75 mm wide on both tread and riser.",
        "LRV differential ≥30 against tread and riser surface respectively.",
        "Anti-slip per AS 4586 P4 minimum on the strip.",
      ]},
      { title:"Switches, outlets, controls", items:[
        "Plate-to-wall contrast — not actuator-to-plate alone.",
        "Coordinate with wall finish — light walls require dark plates and vice versa.",
        "Avoid stainless steel on grey paint — common LRV failure.",
      ]},
      { title:"Floor materials at thresholds", items:[
        "Inverse rule for dementia (see C-05): adjacent floor materials should NOT contrast — DEM populations read contrast as a step or hole.",
        "Resolve by matching LRV across adjacent flooring while maintaining slip-rating differentiation.",
      ]},
    ],
    diagram:{
      type:"elevation",
      svg:`<svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Elevation diagram of door, frame, and wall showing three LRV zones with required contrast differentials">
        <!-- Wall -->
        <rect x="10" y="10" width="300" height="200" fill="#1A1612" fill-opacity="0.06"/>
        <text x="20" y="30" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">WALL</text>
        <text x="20" y="44" font-family="JetBrains Mono, monospace" font-size="9" fill="#6B5F50">LRV 80</text>
        <!-- Frame -->
        <rect x="100" y="40" width="120" height="170" fill="#1A1612" fill-opacity="0.5"/>
        <text x="105" y="58" font-family="JetBrains Mono, monospace" font-size="9" fill="#F2EBDD">FRAME</text>
        <text x="105" y="72" font-family="JetBrains Mono, monospace" font-size="9" fill="#F2EBDD">LRV 25</text>
        <!-- Door leaf -->
        <rect x="115" y="55" width="90" height="155" fill="#1A1612" fill-opacity="0.18"/>
        <text x="125" y="75" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">DOOR</text>
        <text x="125" y="89" font-family="JetBrains Mono, monospace" font-size="9" fill="#6B5F50">LRV 60</text>
        <!-- Lever -->
        <rect x="190" y="130" width="14" height="22" fill="#1A1612"/>
        <text x="208" y="145" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">LEVER</text>
        <text x="208" y="156" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">LRV 10</text>
        <!-- Contrast indicators -->
        <line x1="240" y1="44" x2="240" y2="72" stroke="#1A1612" stroke-width="0.8"/>
        <text x="245" y="60" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">Δ55</text>
        <line x1="240" y1="89" x2="240" y2="156" stroke="#1A1612" stroke-width="0.8"/>
        <text x="245" y="125" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">Δ50</text>
        <text x="20" y="200" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">Wall–Frame: Δ55 ✓</text>
      </svg>`
    },
    install:[
      "Specify LRV at procurement — request manufacturer LRV data not just colour name.",
      "Field measure with LRV meter at handover — common discrepancy between brochure and as-installed.",
      "Lighting at measurement point matches design lighting; LRV is a reflected metric.",
      "Document measured LRV in O&M manual.",
    ],
    failures:[
      "Stainless steel switch plates on light grey wall — LRV nearly identical, no contrast.",
      "White door, white frame, white wall — three indistinguishable surfaces.",
      "Glass doors without manifestation — invisible to low vision; head-strike risk.",
      "Manifestation only at one height — wheelchair eye level missed.",
      "Manifestation at low-LRV against bright window light — invisible silhouetted.",
      "Floor material contrast read as step by DEM populations (see C-05 inverse rule).",
    ],
    popReasons:{
      "VIS":"Contrast is the primary means of distinguishing visual elements; without 30+ LRV differential, edges and controls disappear.",
      "DEM":"Contrast supports recognition of doors and toilets specifically; opposite rule applies to floor material adjacencies.",
      "ALL":"Contrast benefits all users in low-light or peripheral-vision conditions.",
    },
    evidence:[
      { tier:"6", source:"AS 1428.1:2021 — contrast requirements" },
      { tier:"4", source:"BS 8493:2008 — Light reflectance value of a surface" },
      { tier:"3", source:"Bright & Cook (2010), 'Disability and Inclusive Design'" },
    ],
    tr:0, p:["VIS","DEM","ALL"], cat:"C", topics:["wayfinding"],
    rooms:["ALL"],
    related:[
      { cd:"C-05", why:"Floor LRV is the deliberate exception — adjacent floors should NOT contrast for dementia populations" },
      { cd:"D-08", why:"Signage contrast follows same LRV principle" },
      { cd:"B-08", why:"Matte finishes preserve true LRV under all lighting" },
      { cd:"E-09", why:"Tactile indicator visual contrast follows same rule" },
    ]
  },

  // ─────────── E-01 — Accessible Lift ───────────
  {
    cd:"E-01",
    t:"Accessible Lift, 1400×1100 mm Car, All Floors",
    q:"Can a power wheelchair use the lift?",
    s:"Power-wheelchair-compatible lift to every level. No exceptions.",
    body:"Lift car interior dimensions, control heights, audible and visual signalling, and emergency communication all coordinated. Every floor served — half-accessible buildings are not accessible.",
    why:"A lift that doesn't fit a power wheelchair is not an accessible lift. A lift that doesn't reach every floor is segregation.",

    dimensions:[
      { dim:"Car interior — depth", value:"≥1400", unit:"mm", note:"Per AS 1735.12. 1600 mm preferred for circulation" },
      { dim:"Car interior — width", value:"≥1100", unit:"mm", note:"Per AS 1735.12" },
      { dim:"Door clear opening", value:"≥900", unit:"mm", note:"With doors fully open" },
      { dim:"Door dwell time — minimum", value:"≥5", unit:"sec", note:"Default; extendable via control" },
      { dim:"Car operating panel — high control", value:"900–1100", unit:"mm AFF", note:"Top of tallest button" },
      { dim:"Car operating panel — side wall offset", value:"≥400", unit:"mm", note:"From car corner" },
      { dim:"Hall call button height", value:"900–1100", unit:"mm AFF", note:"Both up and down within range" },
      { dim:"Mirror — opposite door", value:"continuous to 1500", unit:"mm AFF", note:"For reversing-out visibility" },
      { dim:"Handrail height", value:"850–950", unit:"mm AFF", note:"Three walls minimum" },
      { dim:"Emergency call button — height", value:"900–1100", unit:"mm AFF", note:"Distinguishable by touch" },
      { dim:"Floor-to-floor levelling tolerance", value:"±6", unit:"mm", note:"At every stop, every load" },
      { dim:"Lobby clear floor space — front", value:"≥1540 dia", unit:"mm", note:"Power wheelchair turning circle" },
    ],
    performance:[
      { metric:"Levelling accuracy", target:"±6 mm at every stop", measure:"Field test at empty, half-load, full-load conditions" },
      { metric:"Door dwell time — adjustable", target:"5–20 sec range", measure:"Verify control commissioning" },
      { metric:"Audible floor announcement", target:"Speech intelligible at 1.5 m", measure:"Field test with calibrated SLM" },
      { metric:"Visual floor indication", target:"Visible from car centre", measure:"Field verify; height + character size per AS 1735.12" },
      { metric:"Emergency communication", target:"Two-way audible + visual", measure:"AS 1735.12 §15" },
    ],
    codes:[
      { ref:"AS 1735.12:1999", clause:"Lifts for facilities for persons with disabilities", jurisdiction:"AU" },
      { ref:"AS 1735.12:1999", clause:"§5 (Car dimensions)", jurisdiction:"AU" },
      { ref:"AS 1735.12:1999", clause:"§9 (Controls and signalling)", jurisdiction:"AU" },
      { ref:"AS 1735.12:1999", clause:"§15 (Emergency communication)", jurisdiction:"AU" },
      { ref:"NCC 2022 Vol 1", clause:"E3D1 (Lift requirements)", jurisdiction:"AU" },
      { ref:"ADA 2010", clause:"§407 (Elevators)", jurisdiction:"US" },
      { ref:"EN 81-70", clause:"Accessibility to lifts for persons with disabilities", jurisdiction:"EU" },
    ],
    products:[
      "Type B lift car (AS 1735.12) — 1400 × 1100 mm minimum",
      "Type C lift car preferred where possible — 2000 × 1400 mm (stretcher capability)",
      "Tactile and Braille floor designations on car operating panel",
      "Two-way emergency intercom with visual call status",
      "Audible floor announcement with adjustable volume",
      "Mirror — opposite door, full width, 900 mm to 1500 mm AFF",
    ],
    schedule:"Accessible lift to AS 1735.12, Type B minimum (Type C preferred), serving all floors. Car internal dimensions ≥1400 × 1100 mm clear. Door clear opening 900 mm minimum, dwell time adjustable 5–20 seconds. Car operating panel mounted with top buttons 900–1100 mm AFF, tactile and Braille floor designations, raised symbols. Hall call buttons 900–1100 mm AFF. Audible floor announcement and visual floor indication. Two-way emergency intercom with visual status indication. Mirror opposite door, 900–1500 mm AFF. Levelling accuracy ±6 mm at all stops under all load conditions.",
    detail:[
      { title:"Car operating panel", items:[
        "Floor buttons in single column or matrix; lowest button ≥900 mm AFF.",
        "Tactile/raised characters AND Braille for floor designation.",
        "Visual indication of selected floor (illumination).",
        "Audible feedback on press.",
        "Door open/close, alarm, intercom buttons distinguishable by tactile difference.",
        "Side-wall mounted, ≥400 mm from car corner.",
      ]},
      { title:"Floor announcement", items:[
        "Voice announcement on arrival at every floor.",
        "Volume adjustable; hearing-loop compatible audio output.",
        "Visual floor indicator (digit) ≥50 mm character height.",
        "Direction-of-travel arrows visible in lift lobby.",
      ]},
      { title:"Emergency communication", items:[
        "Two-way intercom — voice + visual call-acknowledged.",
        "Activates monitored response.",
        "Visual indication for occupant who cannot hear acknowledgement.",
        "Tactile button distinguishable from floor selection.",
      ]},
      { title:"Lobby", items:[
        "Clear turning circle 1540 mm at lift lobby.",
        "Hall call height 900–1100 mm AFF.",
        "Visual + audible call acknowledgement.",
        "Floor designation at door — tactile + visual + Braille.",
      ]},
    ],
    diagram:{
      type:"plan",
      svg:`<svg viewBox="0 0 280 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan diagram of accessible lift car interior with dimensions, COP, mirror, and handrails">
        <!-- Car interior -->
        <rect x="40" y="40" width="200" height="160" fill="none" stroke="#1A1612" stroke-width="2"/>
        <!-- Door at bottom -->
        <line x1="80" y1="200" x2="200" y2="200" stroke="#fff" stroke-width="3"/>
        <line x1="80" y1="200" x2="200" y2="200" stroke="#1A1612" stroke-width="1.2" stroke-dasharray="4 2"/>
        <text x="105" y="215" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">≥900 mm</text>
        <!-- Width dimension -->
        <line x1="40" y1="25" x2="240" y2="25" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="40" y1="22" x2="40" y2="28" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="240" y1="22" x2="240" y2="28" stroke="#1A1612" stroke-width="0.6"/>
        <text x="115" y="18" font-family="JetBrains Mono, monospace" font-size="10" fill="#1A1612">≥1100 mm</text>
        <!-- Depth dimension -->
        <line x1="255" y1="40" x2="255" y2="200" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="252" y1="40" x2="258" y2="40" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="252" y1="200" x2="258" y2="200" stroke="#1A1612" stroke-width="0.6"/>
        <text x="261" y="123" font-family="JetBrains Mono, monospace" font-size="10" fill="#1A1612" transform="rotate(90 261 123)">≥1400 mm</text>
        <!-- COP on side wall -->
        <rect x="42" y="100" width="6" height="60" fill="#1A1612" fill-opacity="0.25" stroke="#1A1612" stroke-width="0.5"/>
        <text x="55" y="125" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">COP</text>
        <text x="55" y="138" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">900–1100</text>
        <!-- Mirror opposite door (top wall) -->
        <line x1="80" y1="40" x2="200" y2="40" stroke="#1A1612" stroke-width="3" stroke-opacity="0.4"/>
        <text x="100" y="58" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">mirror</text>
        <!-- Handrails (3 walls) -->
        <line x1="44" y1="50" x2="44" y2="180" stroke="#1A1612" stroke-width="1"/>
        <line x1="236" y1="50" x2="236" y2="180" stroke="#1A1612" stroke-width="1"/>
        <line x1="50" y1="48" x2="230" y2="48" stroke="#1A1612" stroke-width="1"/>
        <text x="115" y="158" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">handrails 3 walls</text>
      </svg>`
    },
    install:[
      "Coordinate lift well dimensions with manufacturer car size — manufacturer minimums vary.",
      "Lobby clear floor space verified before partition framing.",
      "Levelling commissioned at empty, half-load, and full-load.",
      "Audible system commissioned with hearing-aid compatibility test.",
      "Tactile and Braille designations to be field-verified — common manufacturer omission.",
    ],
    failures:[
      "Type A lift specified instead of Type B — fits manual chair but not power wheelchair.",
      "Lift serves all floors except the basement carpark — accessible parking unreachable.",
      "Door dwell defaults to 3 seconds — wheelchair user trapped repeatedly.",
      "COP at standard 1200 mm AFF — top buttons unreachable for shorter users.",
      "Levelling drift over time produces 30 mm step at car-to-floor — wheelchair tip risk.",
      "Emergency intercom voice-only — Deaf occupant cannot communicate.",
    ],
    popReasons:{
      "MOB":"Power wheelchair dimensions require minimum car size; smaller cars exclude the user.",
      "ALL":"Step-free vertical access benefits everyone; lifts are universal infrastructure.",
    },
    evidence:[
      { tier:"6", source:"AS 1735.12:1999 — Lifts for facilities for persons with disabilities" },
      { tier:"4", source:"EN 81-70 — Accessibility to lifts" },
    ],
    tr:0, p:["MOB","ALL"], cat:"E", topics:["circulation"],
    rooms:["NR-EDU","NR-HLT","NR-WRK","NR-RET","NR-CUL","NR-HOS","NR-TRP"],
    related:[
      { cd:"E-06", why:"Level entry leads to the lift; both required for through accessibility" },
      { cd:"H-01", why:"Lift controls follow the same accessible-control reach envelope" },
      { cd:"E-09", why:"Tactile floor indicators at the lift lobby identify the lift entry" },
      { cd:"H-04", why:"Emergency intercom follows the same multi-modal communication principle" },
    ]
  },

  // ─────────── B-10 — Visual Fire Alarm ───────────
  {
    cd:"B-10",
    t:"Visual Fire Alarm with Strobe VAD Throughout",
    q:"Will deaf occupants see the fire alarm?",
    s:"Visual alarm devices in every space, including bathrooms and bedrooms.",
    body:"Strobe Visual Alarm Devices to AS 4428.16 in every occupied space. The audible-only fire alarm has been the failure mode in fatal incidents — Deaf occupants in bathrooms, bedrooms, kitchens, lifts, all unaware of the alert.",
    why:"Audible-only fire alarm is a death sentence for Deaf occupants. This is non-negotiable.",

    dimensions:[
      { dim:"Mounting height — wall", value:"2000–2400", unit:"mm AFF", note:"Per AS 4428.16; coordinate with fitting heights" },
      { dim:"Mounting height — ceiling", value:"per coverage", unit:"", note:"Centre of effective candela coverage" },
      { dim:"Spacing — corridors", value:"≤30", unit:"m", note:"Maximum between VADs" },
      { dim:"Coverage — single VAD", value:"per cd rating", unit:"", note:"AS 4428.16 Annex A coverage table" },
      { dim:"Bedroom unit — pillow shaker offset", value:"≤1500", unit:"mm from pillow", note:"Tactile alert for sleep" },
    ],
    performance:[
      { metric:"VAD candela rating", target:"per coverage area", measure:"AS 4428.16 Annex A — minimum cd by room dimensions" },
      { metric:"Flash rate", target:"1–2 Hz", measure:"Photometric — must avoid seizure-trigger frequencies (5–30 Hz)" },
      { metric:"Synchronisation across multiple VADs", target:"Within 200 ms", measure:"Field test where multiple visible from single position" },
      { metric:"Wall reflectance for effective coverage", target:"≥0.40 LRV", measure:"Coordinate with C-04" },
    ],
    codes:[
      { ref:"AS 4428.16:2010", clause:"Fire detection, warning, control and intercom systems — Visual warning devices", jurisdiction:"AU" },
      { ref:"AS 1670.1:2018", clause:"Fire detection, warning, control and intercom systems — Design", jurisdiction:"AU" },
      { ref:"NCC 2022 Vol 1", clause:"E2 (Fire safety, occupant warning)", jurisdiction:"AU" },
      { ref:"NFPA 72", clause:"§18.5 (Visible signalling)", jurisdiction:"US" },
      { ref:"BS 5839-1", clause:"Visual alarm device requirements", jurisdiction:"UK" },
    ],
    products:[
      "Strobe Visual Alarm Devices to AS 4428.16, candela-rated per room dimensions",
      "Synchronised VAD systems where multiple visible from single position",
      "Bedroom systems — combined VAD + pillow shaker + bedside indicator",
      "Bathroom-rated IP-rated VAD for wet zones",
      "Lift-car VAD coordinated with AS 1735.12 emergency systems",
    ],
    schedule:"Visual Alarm Devices to AS 4428.16 in every occupied space, including bedrooms, bathrooms, kitchens, lifts, and accessible toilets. VAD candela rating per AS 4428.16 Annex A coverage tables for the room dimensions. Synchronised flash where multiple VADs visible from single position. Bedroom installations to include pillow-shaker tactile alert. Coordinate with fire system designer for compliance with AS 1670.1.",
    detail:[
      { title:"Bathrooms — special considerations", items:[
        "Strobe must be visible from shower with door closed.",
        "IP rating to suit wet zone.",
        "Mount on wall opposite shower or above mirror.",
        "Coordinate with G-04 wet-room layout — VAD placement in design phase.",
      ]},
      { title:"Bedrooms — sleep environments", items:[
        "Combined VAD + pillow shaker + bedside indicator.",
        "Pillow shaker within 1500 mm of bed head, mattress-mounted.",
        "Bedside indicator at low height — visible from supine position.",
        "Wall VAD synchronised with bedside.",
      ]},
      { title:"Lifts and stairs", items:[
        "VAD inside lift car with audible alarm — Deaf occupant trapped otherwise.",
        "Stair landings — VAD at every landing for evacuation.",
        "Stair core door identification supports evacuation.",
      ]},
      { title:"Synchronisation", items:[
        "Multiple VADs visible from single position must be synchronised.",
        "Asynchronous flashing increases seizure risk and visual overload.",
        "Field test at commissioning.",
      ]},
    ],
    diagram:{
      type:"plan",
      svg:`<svg viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan showing VAD coverage zones in a multi-room occupancy">
        <!-- Building outline -->
        <rect x="20" y="20" width="280" height="160" fill="none" stroke="#1A1612" stroke-width="2"/>
        <!-- Room divisions -->
        <line x1="120" y1="20" x2="120" y2="180" stroke="#1A1612" stroke-width="1"/>
        <line x1="220" y1="20" x2="220" y2="180" stroke="#1A1612" stroke-width="1"/>
        <line x1="120" y1="100" x2="220" y2="100" stroke="#1A1612" stroke-width="1"/>
        <!-- VADs as filled circles -->
        <circle cx="70" cy="100" r="6" fill="#1A1612"/>
        <circle cx="170" cy="60" r="6" fill="#1A1612"/>
        <circle cx="170" cy="140" r="6" fill="#1A1612"/>
        <circle cx="270" cy="100" r="6" fill="#1A1612"/>
        <!-- Coverage circles -->
        <circle cx="70" cy="100" r="42" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.4" stroke-dasharray="2 2"/>
        <circle cx="170" cy="60" r="32" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.4" stroke-dasharray="2 2"/>
        <circle cx="170" cy="140" r="32" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.4" stroke-dasharray="2 2"/>
        <circle cx="270" cy="100" r="42" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.4" stroke-dasharray="2 2"/>
        <!-- Labels -->
        <text x="42" y="50" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">LIVING</text>
        <text x="138" y="40" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">BED</text>
        <text x="138" y="125" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">BATH</text>
        <text x="240" y="50" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">KITCHEN</text>
        <text x="20" y="195" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">● VAD     ─ ─ coverage radius (cd-rated)</text>
      </svg>`
    },
    install:[
      "Coordinate VAD placement in design phase with architect and ME — not last-minute by fire contractor.",
      "Bathroom VAD mount before tile lining.",
      "Bedroom pillow-shaker integration with mattress procurement.",
      "Synchronisation tested at commissioning where multiple VADs visible.",
      "Coverage tested in actual lighting conditions (daylight + artificial).",
    ],
    failures:[
      "Audible-only fire alarm — direct cause of fatalities for Deaf occupants.",
      "VAD in main rooms only; bathrooms and bedrooms omitted.",
      "Insufficient candela for room size — alarm not visible from corners.",
      "Asynchronous flash from multiple VADs — seizure trigger.",
      "Strobe rate within seizure-trigger band (5–30 Hz) — incorrect specification.",
      "Lift car VAD omitted — Deaf occupant trapped during alarm.",
    ],
    popReasons:{
      "DEAF":"Cannot hear audible alarm; visual signal is the only path to evacuation.",
      "DBL":"Visual alarm plus tactile (pillow shaker, wearable) is the only path; audible inadequate.",
    },
    evidence:[
      { tier:"6", source:"AS 4428.16:2010 — Visual warning devices" },
      { tier:"6", source:"NFPA 72 — National Fire Alarm and Signalling Code" },
      { tier:"Co-1", source:"Deafness Forum — case studies of audible-alarm failure events" },
    ],
    tr:0, p:["DEAF","DBL"], cat:"B", topics:["safety"],
    rooms:["ALL"],
    related:[
      { cd:"H-04", why:"Door-entry visual alerting follows the same multi-modal principle" },
      { cd:"H-03", why:"Visual paging and captioning extend the principle to non-emergency communication" },
      { cd:"E-09", why:"Tactile indicators support evacuation for blind users — different modality, same goal" },
    ]
  },

  // ─────────── D-04 — Landmarks ───────────
  {
    cd:"D-04",
    t:"Landmarks at Every Decision Point",
    q:"At each decision point, is there a memorable landmark?",
    s:"Distinct, memorable visual features at each junction or directional choice.",
    body:"At every junction or directional choice, a distinct visual landmark — artwork, an object, a window, a colour-marked wall — that is memorable and unique within the building. Memory of place is anchored to landmarks, not to abstract location names.",
    why:"Decision points without landmarks fail for DEM and VIS populations. Memory is procedural, not propositional — people remember 'turn at the painting' rather than 'turn at corridor C-3'.",

    dimensions:[
      { dim:"Spacing — primary route", value:"≤15", unit:"m between landmarks", note:"Memory anchors fade beyond this" },
      { dim:"Spacing — secondary route", value:"at every junction", unit:"", note:"Mandatory at decision points" },
      { dim:"Visual prominence — minimum dimension", value:"≥600", unit:"mm", note:"Visible at 5 m" },
      { dim:"Mounting height — visual centre", value:"1400–1600", unit:"mm AFF", note:"Standing eye level" },
      { dim:"Tactile landmark — within reach", value:"800–1100", unit:"mm AFF", note:"For blind users using cane" },
      { dim:"LRV contrast — landmark to background", value:"≥40", unit:"percentage points", note:"Higher than C-04 baseline for prominence" },
    ],
    performance:[
      { metric:"Recognition test", target:"Identifiable from 5 m at 100 lux", measure:"Field walk-through with users" },
      { metric:"Distinctiveness", target:"Each landmark unique in building", measure:"Audit at design phase" },
      { metric:"Tactile dimension", target:"Identifiable by touch alone", measure:"Field test with blind user (where possible)" },
    ],
    codes:[
      { ref:"AS 1428.1:2021", clause:"§7 (Continuous accessible path of travel — wayfinding)", jurisdiction:"AU" },
      { ref:"WHO Age-Friendly Cities", clause:"Built environment design", jurisdiction:"INTL" },
      { ref:"Dementia Care Mapping (DCM-8)", clause:"Environmental design indicators", jurisdiction:"INTL" },
    ],
    products:[
      "Artwork — original or commissioned, scaled to corridor width",
      "Objects in alcoves — sculptural, vitrine-displayed, or domestic objects",
      "Landmark windows — daylight feature with view",
      "Memory boxes (D-06) — domestic items at residential entries",
      "Colour-blocked wall sections — coordinated with C-02 wayfinding palette",
      "Tactile features — sculptural relief, textured panels at reach height",
    ],
    schedule:"At every decision point on primary and secondary circulation routes, provide a distinctive visual landmark — artwork, object in alcove, daylight feature, or colour-blocked wall segment. Each landmark unique within the building. Visual prominence ≥600 mm minimum dimension, mounting 1400–1600 mm AFF visual centre. LRV contrast ≥40 to background. Where serving blind users, include tactile landmark within reach height (800–1100 mm AFF). Spacing maximum 15 m on primary routes; mandatory at every junction.",
    detail:[
      { title:"Selection of landmark type", items:[
        "Original artwork preferred — scale and locality build identity.",
        "Avoid mass-produced prints, generic motivational signage.",
        "Domestic objects in residential dementia care — familiar typology.",
        "Daylight features (windows with view) doubly effective: orientation by sun position.",
      ]},
      { title:"Placement", items:[
        "At every junction — the landmark is what you see when deciding.",
        "Primary direction first — landmark visible from approach.",
        "Avoid placing landmark behind the decision point — useless after the turn.",
        "Coordinate with B-09 — daylight at landmarks reinforces.",
      ]},
      { title:"For VIS and DBL populations", items:[
        "Tactile dimension within reach (800–1100 mm AFF).",
        "Distinctive auditory signature where possible (water feature, wind chime).",
        "Olfactory signature acceptable in residential — not in F-02 fragrance-free zones.",
      ]},
      { title:"Building-wide audit", items:[
        "List all junctions; verify a unique landmark at each.",
        "Visual logbook in O&M for replacement matching (artwork degrades).",
        "Familiarity is the goal — once landmarks are known, do not relocate.",
      ]},
    ],
    diagram:{
      type:"plan",
      svg:`<svg viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan showing landmark positions at three corridor decision points">
        <!-- Corridors -->
        <rect x="20" y="80" width="280" height="40" fill="#1A1612" fill-opacity="0.04" stroke="#1A1612" stroke-width="0.6"/>
        <rect x="100" y="20" width="40" height="60" fill="#1A1612" fill-opacity="0.04" stroke="#1A1612" stroke-width="0.6"/>
        <rect x="200" y="120" width="40" height="60" fill="#1A1612" fill-opacity="0.04" stroke="#1A1612" stroke-width="0.6"/>
        <!-- Landmarks (dark squares) -->
        <rect x="125" y="68" width="14" height="14" fill="#1A1612"/>
        <text x="142" y="78" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">artwork</text>
        <circle cx="200" cy="100" r="7" fill="#1A1612"/>
        <text x="212" y="103" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">window</text>
        <polygon points="220,118 234,118 234,132" fill="#1A1612"/>
        <text x="244" y="128" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">sculpture</text>
        <!-- Decision point indicators -->
        <circle cx="120" cy="100" r="14" fill="none" stroke="#1A1612" stroke-width="0.5" stroke-dasharray="2 2"/>
        <circle cx="220" cy="100" r="14" fill="none" stroke="#1A1612" stroke-width="0.5" stroke-dasharray="2 2"/>
        <text x="20" y="195" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">decision points: ─ ─ each with unique landmark</text>
      </svg>`
    },
    install:[
      "Landmark selection in design — not value-engineered out at construction.",
      "Coordinate with FF&E budget; reserve landmark allocation.",
      "Lighting for landmarks designed in B-06 / B-07 strategy.",
      "Document landmarks in O&M — for replacement and staff orientation.",
    ],
    failures:[
      "Generic 'corridor C-3' signage with no visual anchor.",
      "Identical landmarks at multiple junctions — defeats memorability.",
      "Landmarks behind decision points — useless after the turn.",
      "Removed during refurbishment without replacement.",
      "Mass-produced art — does not build building identity over time.",
      "No tactile dimension — invisible to blind users.",
    ],
    popReasons:{
      "DEM":"Landmarks anchor procedural memory of routes; verbal directions fail without them.",
      "VIS":"Landmarks at decision points can include tactile or auditory features.",
      "NEU":"Landmarks reduce dependence on cognitive mapping during recovery.",
    },
    evidence:[
      { tier:"3", source:"Marquardt (2011), 'Wayfinding for people with dementia'" },
      { tier:"4", source:"WHO Age-Friendly Cities — environmental design" },
      { tier:"Co-1", source:"Lived-experience accounts, dementia advocacy organisations" },
    ],
    tr:1, p:["DEM","VIS","NEU"], cat:"D", topics:["wayfinding"],
    rooms:["R-HAL","NR-HLT","NR-EDU","NR-CUL","NR-TRP"],
    related:[
      { cd:"D-02", why:"Landmarks reinforce the primary route" },
      { cd:"D-08", why:"Signage and landmarks together support recognition" },
      { cd:"C-02", why:"Colour-coded wayfinding zones can incorporate landmark colour" },
      { cd:"D-06", why:"Memory boxes are landmarks at residential entries" },
      { cd:"B-09", why:"Daylight features are landmarks with circadian benefit" },
    ]
  },

  // ─────────── A-16 — Sensory Room ───────────
  {
    cd:"A-16",
    t:"Sensory Room or Quiet Room, Minimum 8 m²",
    q:"Where does someone go when overwhelmed?",
    s:"Dedicated low-stimulation refuge space in any building serving sensitive populations.",
    body:"A sensory room is a dedicated, signed, available space with low light, low noise, soft furnishing, no scent, individual control of all variables, and access without permission. The minimum dimensions accommodate one person plus a support person plus a wheelchair turning radius. Larger versions support sensory regulation activities (weighted equipment, soft seating).",
    why:"Sensory overload requires somewhere to go. A toilet cubicle is not adequate. A first-aid room repurposed as default is not adequate. The provision must be dedicated, available, and recognised.",

    dimensions:[
      { dim:"Floor area — minimum", value:"≥8", unit:"m²", note:"Accommodates one person + support person + wheelchair turn" },
      { dim:"Floor area — preferred", value:"12–16", unit:"m²", note:"Allows regulation activities and equipment" },
      { dim:"Ceiling height", value:"≥2700", unit:"mm AFF", note:"Match adjacent occupied spaces" },
      { dim:"Door clear opening", value:"≥850", unit:"mm", note:"Per AS 1428.1; outward swing for rescue access" },
      { dim:"Turning circle", value:"≥1540", unit:"mm dia", note:"Power wheelchair turn" },
      { dim:"Lighting illuminance — minimum (dimmed)", value:"≤50", unit:"lux", note:"Local control" },
      { dim:"Lighting illuminance — maximum", value:"≤300", unit:"lux", note:"Local control; never bright" },
      { dim:"Acoustic — RT60", value:"≤0.4", unit:"sec", note:"500–1000 Hz, occupied" },
      { dim:"Acoustic — STC to adjacent", value:"≥50", unit:"", note:"To prevent ingress; A-14 partition" },
      { dim:"Background noise level", value:"≤NC-25", unit:"", note:"HVAC must be silent" },
      { dim:"Temperature — adjustable range", value:"18–24", unit:"°C", note:"Local control" },
    ],
    performance:[
      { metric:"Light dimming range", target:"5 lux to 300 lux", measure:"Field measurement at occupant position" },
      { metric:"RT60", target:"≤0.4 sec, 500–1000 Hz", measure:"ISO 3382 occupied condition" },
      { metric:"Acoustic isolation", target:"STC ≥50 from adjacent", measure:"AS/NZS ISO 717.1" },
      { metric:"HVAC noise", target:"≤NC-25", measure:"AS/NZS 2107 occupied condition" },
      { metric:"Air change rate", target:"≥6 ACH", measure:"Per F-04 air quality standards" },
      { metric:"Olfactory neutrality", target:"Fragrance-free per F-02", measure:"Policy + ventilation strategy" },
    ],
    codes:[
      { ref:"AS 1428.1:2021", clause:"Door, clear floor space, turning circle requirements", jurisdiction:"AU" },
      { ref:"WELL Building Standard v2", clause:"M07 (Restorative spaces)", jurisdiction:"INTL" },
      { ref:"NDIS Practice Standards", clause:"Sensory regulation environments", jurisdiction:"AU" },
    ],
    products:[
      "Soft seating — beanbag, weighted, or recliner; user choice",
      "Dimmable, flicker-free LED with separate task and ambient control",
      "Acoustic wall panels (NRC ≥0.85) on three walls minimum",
      "Acoustic carpet or sealed cork flooring",
      "Blackout blinds or shutters where windows present",
      "Local thermostat (per H-02)",
      "Sensory equipment as appropriate — weighted blanket, fidget items, regulation tools",
      "Optional: white-noise machine (NOT sound masking — different application)",
    ],
    schedule:"Dedicated sensory / quiet room, minimum 8 m². Signed and unlocked during operating hours. Lighting locally controllable from 5 to 300 lux, flicker-free per B-04. Acoustic treatment to RT60 ≤0.4 sec, STC ≥50 to adjacent spaces. HVAC noise ≤NC-25; vibration isolation per A-09. Air quality per F-04; fragrance-free per F-02. Local thermostat 18–24°C range. Furnishing: soft seating with user choice, weighted equipment as briefed. Power outlets at 400 mm AFF (low) and 1100 mm AFF (high) per H-01. No clinical aesthetic.",
    detail:[
      { title:"Location strategy", items:[
        "Adjacent to high-stimulation zones (assembly, learning, treatment) so retreat is short.",
        "Not adjacent to plant rooms, kitchens, or noisy circulation.",
        "Visible signage — no hunting for the room when overwhelmed.",
        "Multiple rooms preferred over single large room — concurrent occupants.",
      ]},
      { title:"Acoustic isolation", items:[
        "Walls: STC ≥50 to all adjacent — typically double-leaf partition (A-14).",
        "Door: STC ≥35 acoustic-rated, with door seal.",
        "Floor/ceiling: high impact isolation; no mechanical equipment above.",
        "HVAC: dedicated branch with attenuators; no shared duct with active spaces.",
      ]},
      { title:"Lighting", items:[
        "Two channels: ambient and task.",
        "Ambient: 5–100 lux range, warm CCT.",
        "Task: 100–300 lux for activities, dimmable.",
        "Both flicker-free per B-04.",
        "Local control — wall switch with rotary or slider, not capacitive touch.",
      ]},
      { title:"Furnishing", items:[
        "Soft, low-stim materials — no patterned upholstery.",
        "Multiple seating types — supine, seated, beanbag.",
        "Weighted equipment as briefed.",
        "Storage for personal items — small lockable cubby.",
        "No corporate or clinical signage.",
      ]},
      { title:"Operations", items:[
        "Door handle indicates 'in use' visibly — no knock to enter.",
        "No time limits (within reason) — recovery takes the time it takes.",
        "Cleaning between uses — fragrance-free products only.",
      ]},
    ],
    diagram:{
      type:"plan",
      svg:`<svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan of sensory room showing soft seating, lighting controls, dimensions, and acoustic isolation">
        <!-- Room outline (double line indicates STC partition) -->
        <rect x="30" y="30" width="260" height="170" fill="none" stroke="#1A1612" stroke-width="2"/>
        <rect x="34" y="34" width="252" height="162" fill="none" stroke="#1A1612" stroke-width="0.5"/>
        <text x="42" y="50" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">SENSORY ROOM</text>
        <text x="42" y="63" font-family="JetBrains Mono, monospace" font-size="9" fill="#6B5F50">≥8 m²</text>
        <!-- Soft seating -->
        <ellipse cx="100" cy="120" rx="32" ry="22" fill="#1A1612" fill-opacity="0.15" stroke="#1A1612" stroke-width="0.6"/>
        <text x="80" y="123" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">soft seat</text>
        <!-- Beanbag -->
        <circle cx="200" cy="100" r="20" fill="#1A1612" fill-opacity="0.15" stroke="#1A1612" stroke-width="0.6"/>
        <text x="184" y="103" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">beanbag</text>
        <!-- Wheelchair turn -->
        <circle cx="170" cy="160" r="38" fill="none" stroke="#1A1612" stroke-width="0.4" stroke-dasharray="3 2"/>
        <text x="155" y="165" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">1540 turn</text>
        <!-- Door -->
        <line x1="60" y1="200" x2="100" y2="200" stroke="#fff" stroke-width="3"/>
        <line x1="60" y1="200" x2="100" y2="200" stroke="#1A1612" stroke-width="1.2" stroke-dasharray="3 2"/>
        <path d="M 60 200 Q 60 180 80 180" fill="none" stroke="#1A1612" stroke-width="0.6" stroke-dasharray="2 2"/>
        <text x="55" y="215" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">≥850 outward</text>
        <!-- Light control -->
        <rect x="270" y="90" width="6" height="20" fill="#1A1612"/>
        <text x="245" y="84" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">light + therm</text>
        <!-- Annotations (right side legend) -->
        <text x="225" y="200" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">═ STC ≥50</text>
        <text x="225" y="210" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">5–300 lux</text>
      </svg>`
    },
    install:[
      "Acoustic isolation completed before lining; field-tested at handover.",
      "HVAC commissioned to NC-25 — frequent failure point.",
      "Lighting commissioned across full range; flicker tested at low end.",
      "Signage and operating policy in place at handover.",
    ],
    failures:[
      "Repurposed first-aid room — clinical aesthetic, not low-stim.",
      "Sensory room locked — defeats availability when needed.",
      "Located adjacent to plant or kitchen — acoustic isolation insufficient.",
      "HVAC noise above NC-30 — defeats the purpose.",
      "Capacitive light control without tactile feedback — fails for VIS.",
      "Cleaning with fragranced products — defeats fragrance-free requirement.",
      "No signage — occupants don't know it exists.",
    ],
    popReasons:{
      "NDV":"Sensory overload recovery requires withdrawal from stimulus. The room is the recovery instrument.",
      "OFS":"Orthostatic episode requires lying down somewhere safe.",
      "PAIN":"Pain spike requires a place to recover without performing.",
      "NDV/MH":"Anxiety or panic requires retreat without explanation.",
    },
    evidence:[
      { tier:"Co-2", source:"OT Australia — Sensory regulation in built environments" },
      { tier:"Co-1", source:"Aspect — Quiet space provisioning standards" },
      { tier:"3", source:"Bogdashina (2003), 'Sensory Perceptual Issues in Autism'" },
    ],
    tr:1, p:["NDV","OFS","PAIN","NDV/MH"], cat:"A", topics:["refuge"],
    rooms:["NR-EDU","NR-HLT","NR-WRK","NR-RET","NR-TRP"],
    related:[
      { cd:"D-05", why:"Smaller alcoves serve different needs along the same gradient" },
      { cd:"F-01", why:"Sensory gradient leads naturally toward refuge spaces" },
      { cd:"F-02", why:"Fragrance-free requirement is critical here" },
      { cd:"A-14", why:"Double-leaf partition delivers required STC ≥50 isolation" },
      { cd:"H-02", why:"Individual environmental control implements local light + temp" },
    ]
  },

  // ─────────── E-10 — Rest Seating ───────────
  {
    cd:"E-10",
    t:"Rest Seating on Circulation Routes, ≤20 m Intervals",
    q:"How far before someone needs to sit down?",
    s:"Seating in alcoves along all primary routes longer than 20 metres.",
    body:"Seating in alcoves at maximum 20 m intervals. Alcove rather than corridor projection — seating must not narrow effective width (E-08). Multiple seat heights at each location.",
    why:"For OFS, PAIN, and older populations, distance is measured in seating intervals, not metres. Without seating, accessible buildings remain inaccessible.",

    dimensions:[
      { dim:"Spacing — primary routes", value:"≤20", unit:"m between seats", note:"Maximum interval" },
      { dim:"Spacing — preferred", value:"15", unit:"m", note:"For populations with severe fatigue (OFS, advanced PAIN)" },
      { dim:"Alcove width — minimum", value:"≥1500", unit:"mm", note:"Wheelchair-companion seat alongside" },
      { dim:"Alcove depth — minimum", value:"≥600", unit:"mm beyond seat front", note:"Preserves corridor clear width" },
      { dim:"Seat height — low", value:"380", unit:"mm AFF", note:"For shorter or recovering users" },
      { dim:"Seat height — standard", value:"450", unit:"mm AFF", note:"Most users" },
      { dim:"Seat height — elevated", value:"520", unit:"mm AFF", note:"For users with hip/knee pain or limited mobility" },
      { dim:"Backrest height", value:"≥400", unit:"mm above seat", note:"For supportive rest" },
      { dim:"Armrest height", value:"200–250", unit:"mm above seat", note:"For sit-to-stand assistance" },
      { dim:"Seat depth", value:"450–500", unit:"mm", note:"Allows feet flat on floor" },
      { dim:"Wheelchair-companion space", value:"≥900 × 1300", unit:"mm", note:"Beside seat group" },
    ],
    performance:[
      { metric:"Sit-to-stand support", target:"Armrests structural to user weight", measure:"Per BS EN 16139 / AS 4688" },
      { metric:"Slip resistance — base", target:"P4 minimum", measure:"AS 4586" },
      { metric:"Cleanability", target:"Wipeable; replaceable upholstery", measure:"Specification review" },
    ],
    codes:[
      { ref:"AS 1428.2:1992", clause:"§16 (Seating and resting places)", jurisdiction:"AU" },
      { ref:"AS 1428.1:2021", clause:"§7 (Rest areas on accessible paths)", jurisdiction:"AU" },
      { ref:"BS 8300-2:2018", clause:"Resting places", jurisdiction:"UK" },
      { ref:"WHO Age-Friendly Cities", clause:"Outdoor spaces and buildings", jurisdiction:"INTL" },
    ],
    products:[
      "Bench with backrest and armrests — not backless benches",
      "Single chairs with backrest and armrests — multiple heights at each location",
      "Wheelchair-companion seating (single or two-seat with adjacent wheelchair space)",
      "Robust, replaceable upholstery — anti-microbial in healthcare",
    ],
    schedule:"Rest seating in alcoves at maximum 20 m intervals along all primary circulation routes. Each alcove minimum 1500 × 600 mm beyond corridor clear width. At least three seat heights provided across each pair of locations: 380, 450, and 520 mm AFF. Backrests minimum 400 mm above seat; armrests 200–250 mm above seat structural for sit-to-stand. Wheelchair-companion space 900 × 1300 mm beside seat group at every location.",
    detail:[
      { title:"Alcove vs. corridor projection", items:[
        "Alcoves preserve E-08 corridor clear width.",
        "Corridor-projecting seating is non-compliant where it reduces width below 1200 mm.",
        "Coordinate alcove with structure — bay framing must allow.",
      ]},
      { title:"Seat height variety", items:[
        "Three heights minimum across locations: 380, 450, 520 mm AFF.",
        "Each individual location need not have all three; pairs of nearby locations should.",
        "Healthcare and aged care: prioritise 520 mm (sit-to-stand assistance).",
      ]},
      { title:"Armrests and backrests", items:[
        "Both required — backless benches do not support recovery rest.",
        "Armrests structural to user weight (sit-to-stand load test).",
        "Armrest fronts protrude ≤25 mm beyond seat front to support push-up.",
      ]},
      { title:"Wheelchair-companion provision", items:[
        "Adjacent space 900 × 1300 mm at every location.",
        "Allows wheelchair user and walking companion to rest together.",
        "Not a replacement for seated provision — additional.",
      ]},
      { title:"Lighting and weather", items:[
        "Lighting to seating per B-06.",
        "Where seating is at external transition, weather protection per E-05.",
      ]},
    ],
    diagram:{
      type:"plan",
      svg:`<svg viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan showing rest seating alcove off corridor, with three seat heights and wheelchair companion space">
        <!-- Corridor -->
        <rect x="20" y="100" width="280" height="60" fill="#1A1612" fill-opacity="0.04" stroke="#1A1612" stroke-width="0.6"/>
        <text x="30" y="135" font-family="JetBrains Mono, monospace" font-size="9" fill="#6B5F50">corridor 1200 clear</text>
        <!-- Alcove -->
        <rect x="100" y="40" width="140" height="60" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.8"/>
        <text x="105" y="55" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">alcove ≥1500 × 600</text>
        <!-- Three seats -->
        <rect x="115" y="65" width="20" height="22" fill="#1A1612" fill-opacity="0.4" stroke="#1A1612" stroke-width="0.6"/>
        <text x="118" y="82" font-family="JetBrains Mono, monospace" font-size="7" fill="#F2EBDD">380</text>
        <rect x="145" y="65" width="20" height="22" fill="#1A1612" fill-opacity="0.4" stroke="#1A1612" stroke-width="0.6"/>
        <text x="148" y="82" font-family="JetBrains Mono, monospace" font-size="7" fill="#F2EBDD">450</text>
        <rect x="175" y="65" width="20" height="22" fill="#1A1612" fill-opacity="0.4" stroke="#1A1612" stroke-width="0.6"/>
        <text x="178" y="82" font-family="JetBrains Mono, monospace" font-size="7" fill="#F2EBDD">520</text>
        <!-- Wheelchair companion -->
        <rect x="205" y="62" width="28" height="32" fill="none" stroke="#1A1612" stroke-width="0.6" stroke-dasharray="3 2"/>
        <text x="207" y="80" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">w/c</text>
        <text x="207" y="91" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">space</text>
        <!-- Spacing indicator -->
        <line x1="20" y1="180" x2="300" y2="180" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="20" y1="177" x2="20" y2="183" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="300" y1="177" x2="300" y2="183" stroke="#1A1612" stroke-width="0.6"/>
        <text x="135" y="195" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">≤20 m to next alcove</text>
      </svg>`
    },
    install:[
      "Alcoves coordinated in plan and structure — not retrofit.",
      "Seat heights selected by procurement to provide variety at each location pair.",
      "Sit-to-stand load test on installed armrests at handover.",
      "Where mounted to walls, fix to backing — 300 kg downward load.",
    ],
    failures:[
      "Backless benches — do not support recovery rest.",
      "Corridor-projecting seating — narrows clear width below E-08 minimum.",
      "Single seat height (450 mm) — excludes shorter and elderly users.",
      "No wheelchair-companion space — wheelchair user and companion separated.",
      "Seating spacing >25 m — fatigue accumulates between alcoves.",
      "Armrests too low or unstable — sit-to-stand fails.",
    ],
    popReasons:{
      "MOB":"Manual wheelchair propulsion is fatiguing; rest required at intervals.",
      "PAIN":"Walking tolerance varies day to day; seating supports flexible occupation.",
      "OFS":"Orthostatic intolerance — must be able to sit before symptoms escalate.",
      "DEM":"Confusion increases with fatigue; seating supports orientation.",
    },
    evidence:[
      { tier:"Co-2", source:"OT clinical practice — fatigue management in built environments" },
      { tier:"4", source:"BS 8300-2:2018 — Resting places" },
      { tier:"3", source:"WHO Age-Friendly Cities checklist" },
    ],
    tr:1, p:["MOB","PAIN","OFS","DEM"], cat:"E", topics:["circulation"],
    rooms:["NR-HLT","NR-CUL","NR-TRP","R-HAL"],
    related:[
      { cd:"G-02", why:"Multiple seat heights at each location — same principle" },
      { cd:"E-08", why:"Seating in alcove preserves corridor width" },
      { cd:"E-05", why:"Weather protection at external rest seating" },
      { cd:"B-06", why:"Lighting to seating supports rest activity" },
    ]
  },

  // ─────────── H-01 — Controls Reach ───────────
  {
    cd:"H-01",
    t:"Controls at 400–1100 mm AFF, One-Fist Operable",
    q:"Can controls be operated with one closed fist?",
    s:"All switches, plates, and operable hardware within seated reach and operable without grip.",
    body:"All operable controls — switches, outlets, intercoms, security panels, lift call buttons — between 400 and 1100 mm above finished floor level. Operation must require less than 22 N force and be possible with a closed fist. The reach envelope is the seated power-wheelchair user; the force envelope is grip-impaired upper limb.",
    why:"Controls outside the seated reach envelope or requiring fine motor manipulation exclude users with mobility, upper-limb, or grip-strength impairments.",

    dimensions:[
      { dim:"Mounting — minimum height", value:"≥400", unit:"mm AFF", note:"Lowest button or actuator" },
      { dim:"Mounting — maximum height", value:"≤1100", unit:"mm AFF", note:"Highest button or actuator" },
      { dim:"Side-approach offset", value:"≥500", unit:"mm from corner", note:"Allows wheelchair side-on approach" },
      { dim:"Front-approach clear floor", value:"≥800 × 1300", unit:"mm", note:"Per AS 1428.1 §5" },
      { dim:"Operating force — maximum", value:"≤22", unit:"N", note:"Per AS 1428.1 §17" },
      { dim:"Actuator size — minimum", value:"≥30 × 30", unit:"mm", note:"Identifiable by closed fist" },
      { dim:"Tactile differentiation", value:"between adjacent functions", unit:"", note:"For VIS / DBL users" },
    ],
    performance:[
      { metric:"Operating force", target:"≤22 N", measure:"AS 1428.1 §17 — push-pull gauge" },
      { metric:"Closed-fist operability", target:"Functional with closed fist", measure:"User trial; size, force, and shape" },
      { metric:"Audible feedback", target:"Click or tone on actuation", measure:"Field verification" },
      { metric:"Visible feedback", target:"Lit indication of state", measure:"Field verification under design lighting" },
    ],
    codes:[
      { ref:"AS 1428.1:2021", clause:"§16 (Reach ranges)", jurisdiction:"AU" },
      { ref:"AS 1428.1:2021", clause:"§17 (Operating force)", jurisdiction:"AU" },
      { ref:"AS 1428.2:1992", clause:"§7 (Reach ranges, enhanced)", jurisdiction:"AU" },
      { ref:"ADA 2010", clause:"§308 (Reach ranges), §309 (Operable parts)", jurisdiction:"US" },
      { ref:"ISO 21542:2021", clause:"§18 (Operable elements)", jurisdiction:"INTL" },
    ],
    products:[
      "Rocker switches (large action area; closed-fist operable)",
      "Toggle switches with extended levers (non-rotary)",
      "Push-button actuators ≥30 mm diameter",
      "Avoid: small toggle switches, rotary dials, capacitive touch without tactile feedback",
      "Lift call panels — buttons ≥30 × 30 mm with tactile differentiation",
    ],
    schedule:"All operable controls (switches, outlets, intercoms, security, lift calls, environmental controls) mounted between 400 and 1100 mm above finished floor level. Operating force ≤22 N. Actuator size ≥30 × 30 mm. Tactile differentiation between adjacent functions. Audible and visible feedback on actuation. Side-approach offset ≥500 mm from internal corners. Front-approach clear floor space ≥800 × 1300 mm at primary controls.",
    detail:[
      { title:"Switch and outlet placement", items:[
        "Light switches: 900–1100 mm AFF, side-of-door with 500 mm corner offset.",
        "Power outlets: 400–600 mm AFF preferred (low height accommodates wheelchair).",
        "Where two outlets stacked, top ≤1100 mm.",
        "Outlets in kitchens: ≥150 mm above bench, accessible to seated user.",
      ]},
      { title:"Actuator selection", items:[
        "Rocker switches preferred — large action area, closed-fist operable.",
        "Toggle switches with extended levers acceptable; small toggles non-compliant.",
        "Capacitive touch only with confirming tactile feedback — pure-glass touch fails for VIS.",
        "Rotary dials non-compliant for primary functions.",
      ]},
      { title:"Audible and visible feedback", items:[
        "Click or tone on actuation — 'did it work?' is the question.",
        "Lit state indication — visible under design lighting (not blown out by daylight).",
        "Combined audible + visible serves both DEAF and VIS.",
      ]},
      { title:"Heights for specific functions", items:[
        "Light switches: 900–1100 mm AFF",
        "GPOs: 400–600 mm AFF",
        "Thermostats: 900–1100 mm AFF",
        "Intercom buttons: 900–1100 mm AFF",
        "Lift call: 900–1100 mm AFF",
        "Door access pads: 900–1100 mm AFF",
        "Security keypads: 900–1100 mm AFF",
      ]},
    ],
    diagram:{
      type:"elevation",
      svg:`<svg viewBox="0 0 320 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Elevation showing reach range envelope and control mounting heights">
        <!-- Wall -->
        <rect x="20" y="10" width="280" height="220" fill="#1A1612" fill-opacity="0.03" stroke="#1A1612" stroke-width="0.6"/>
        <!-- Floor line -->
        <line x1="20" y1="220" x2="300" y2="220" stroke="#1A1612" stroke-width="2"/>
        <!-- Reach envelope (seated wheelchair user) -->
        <path d="M 80 120 Q 80 220 200 220 Q 200 120 80 120" fill="#1A1612" fill-opacity="0.08" stroke="#1A1612" stroke-width="0.5" stroke-dasharray="4 3"/>
        <text x="100" y="170" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">reach envelope</text>
        <text x="100" y="183" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">seated, w/c</text>
        <!-- Heights -->
        <line x1="50" y1="120" x2="50" y2="220" stroke="#1A1612" stroke-width="0.5"/>
        <line x1="47" y1="120" x2="53" y2="120" stroke="#1A1612" stroke-width="0.5"/>
        <line x1="47" y1="220" x2="53" y2="220" stroke="#1A1612" stroke-width="0.5"/>
        <text x="20" y="125" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">1100</text>
        <text x="30" y="225" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">FFL</text>
        <line x1="50" y1="180" x2="80" y2="180" stroke="#1A1612" stroke-width="0.5" stroke-dasharray="2 2"/>
        <text x="20" y="185" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">400</text>
        <!-- Controls inside envelope -->
        <rect x="220" y="115" width="14" height="20" fill="#1A1612" fill-opacity="0.4"/>
        <text x="240" y="128" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">switch 950</text>
        <rect x="220" y="195" width="14" height="20" fill="#1A1612" fill-opacity="0.4"/>
        <text x="240" y="208" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">GPO 450</text>
        <!-- One-fist annotation -->
        <text x="20" y="50" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">≤22 N · closed fist · ≥30×30 mm</text>
      </svg>`
    },
    install:[
      "Set-out drawings to mark all control heights before electrical rough-in.",
      "Field verify after first-fix; before plasterer/lining boxes get covered.",
      "Operating force test on installed switches — gauge available.",
      "Audible/visible feedback verified at commissioning.",
    ],
    failures:[
      "Default electrical layout: switches at 1300 mm AFF — out of reach.",
      "GPOs at 300 mm — too low even for wheelchair side reach.",
      "Decorative small toggle switches selected for aesthetic — non-compliant.",
      "Capacitive touch panels without tactile feedback — fails for VIS.",
      "Switches at internal corners — wheelchair cannot approach.",
      "Operating force >30 N (typical of cheap rocker mechanisms) — fails OFS, PAIN.",
    ],
    popReasons:{
      "MOB":"Seated reach envelope determines control accessibility.",
      "ALL":"One-fist operability benefits everyone in carrying or one-handed conditions.",
    },
    evidence:[
      { tier:"6", source:"AS 1428.1:2021 — Reach ranges and operating force" },
      { tier:"6", source:"ADA 2010 §308, §309" },
    ],
    tr:0, p:["MOB","ALL"], cat:"H", topics:["control"],
    rooms:["ALL"],
    related:[
      { cd:"I-01", why:"Hardware specification follows same operability principle" },
      { cd:"H-02", why:"Environmental controls follow same reach envelope" },
      { cd:"E-11", why:"Where automation is provided, reach-range still applies to manual override" },
    ]
  },

];
