import { useState, useEffect, useRef, useCallback, useMemo } from "react";

/* ════════════════════════════════════════════════════════════════════
   DATA
   ════════════════════════════════════════════════════════════════════ */

const POPS = [
  { code:"MOB", label:"Mobility & Strength", desc:"Wheelchair users, ambulant mobility, reduced strength and endurance." },
  { code:"VIS", label:"Vision Impairment", desc:"Blind, low vision, colour vision deficiency. Tactile and auditory environment critical." },
  { code:"DEAF", label:"Deaf / Hard of Hearing", desc:"Deaf, hard of hearing, hearing device users. Visual environment and STI critical." },
  { code:"NEU", label:"Neurological / ABI", desc:"Acquired brain injury, post-concussion syndrome, stroke. Sensory sensitivity and fatigue." },
  { code:"DEM", label:"Dementia", desc:"All dementia types. Wayfinding, cognitive simplicity, familiar environments." },
  { code:"NDV", label:"Neurodivergence", desc:"Autism, ADHD, sensory processing differences. Sensory control paramount." },
  { code:"NDV/MH", label:"Mental Health & PTSD", desc:"PTSD, trauma-informed design, anxiety, depression. Defensible space and autonomy." },
  { code:"PAIN", label:"Chronic Pain", desc:"Chronic pain conditions, fibromyalgia. Vibration control, warmth, rest." },
  { code:"DBL", label:"DeafBlind", desc:"Combined deaf and blind, distinct from VIS or DEAF alone. Tactile communication paramount." },
  { code:"OFS", label:"Orthostatic & Fatigue", desc:"ME/CFS, POTS, MCAS. Positional tolerance, rest, environmental sensitivity." },
];

const CATEGORIES = [
  { letter:"A", name:"Acoustics" },
  { letter:"B", name:"Lighting" },
  { letter:"C", name:"Colour & Surface" },
  { letter:"D", name:"Spatial & Wayfinding" },
  { letter:"E", name:"Entry & Circulation" },
  { letter:"F", name:"Sensory Zoning" },
  { letter:"G", name:"Furniture & Fixtures" },
  { letter:"H", name:"Controls & Technology" },
  { letter:"I", name:"Upper Limb" },
];

const TIERS = [
  { v:0, n:"Universal", d:"Code compliance. The floor — not the aspiration." },
  { v:1, n:"Population-Informed", d:"Evidence-based ranges. The aspiration of this guidebook." },
  { v:2, n:"Person-Specific", d:"OT assessment resolves position within the range." },
];

const TOPICS = [
  { id:"sensory", label:"Sensory environment" },
  { id:"lighting", label:"Lighting" },
  { id:"wayfinding", label:"Wayfinding" },
  { id:"refuge", label:"Refuge" },
  { id:"control", label:"Personal control" },
  { id:"entry", label:"Entry" },
  { id:"circulation", label:"Circulation" },
  { id:"materials", label:"Materials" },
  { id:"safety", label:"Safety" },
  { id:"toileting", label:"Toileting" },
  { id:"communication", label:"Communication" },
];

const BUILDINGS = {
  res: {
    label: "Residential",
    desc: "Single-dwelling and multi-residential. Private and shared spaces.",
    rooms: [
      { code:"R-ENT", name:"Entry", note:"The threshold between outside and inside.", body:"The entry sets the tone of the dwelling and determines who can use it. A failure here propagates: a stepped threshold means a wheelchair user can't get in at all. Weather protection, automatic operation, and legibility together make a domestic entry that is welcoming rather than negotiated." },
      { code:"R-HAL", name:"Hallway", note:"Primary internal circulation.", body:"Hallways are where buildings reveal whether they were designed for a body or for a plan. Width determines passability; landmarks determine wayfinding; surface determines acoustics; lighting determines safety at night." },
      { code:"R-LIV", name:"Living Room", note:"Shared occupied space.", body:"The most occupied room in most homes. The living room hosts long stretches of presence — sustained, varied, often unstructured. It must serve sleep-adjacent rest, focused activity, social gathering, and solitary regulation, sometimes within a single afternoon." },
      { code:"R-KIT", name:"Kitchen", note:"Task-heavy, surface-rich.", body:"The kitchen is the densest concentration of operable elements in a domestic environment. Heights, reach, weight, heat, slip — every dimension of the body matters. Designed well, it serves any user; designed default, it excludes a large fraction." },
      { code:"R-BED", name:"Bedroom", note:"Private rest and sleep.", body:"Sleep quality is the foundation of cognitive, mood, and pain regulation. Lighting (B-01, B-11), acoustics (A-08, A-14), thermal control (H-02), and emergency provision (G-09) all converge here." },
      { code:"R-BA", name:"Bathroom", note:"Wet, transferable, intimate.", body:"The bathroom is where mobility, dignity, and safety meet most directly. Wet-room configuration eliminates the threshold problem; bilateral grab bars handle the transfer problem; one-hand operation handles the upper-limb problem." },
      { code:"R-LAU", name:"Laundry", note:"Task space, often overlooked.", body:"Often the last room considered for accessibility. Reach ranges, control heights, and seated-task design here determine whether someone manages their own laundry independently." },
    ]
  },
  nres: {
    label: "Non-Residential",
    desc: "Public and semi-public buildings. Workplaces, services, civic spaces.",
    rooms: [
      { code:"NR-EDU", name:"Education", note:"Schools, universities, training.", body:"Educational environments serve a population that includes many disabled and neurodivergent learners. Acoustic quality, sensory regulation, and spatial predictability are decisive for learning outcomes." },
      { code:"NR-HLT", name:"Healthcare", note:"Hospitals, clinics, allied health.", body:"Healthcare buildings serve people in their most vulnerable states. They are also disproportionately occupied by older, disabled, neurodivergent, and chronically ill people. Every accessibility consideration in this guidebook applies with greater weight in healthcare environments." },
      { code:"NR-WRK", name:"Workplace", note:"Offices and shared workspaces.", body:"Workplaces have the longest sustained occupation per day of any building type. Sensory regulation, individual control, and refuge provision determine whether disabled and neurodivergent employees can sustain employment." },
      { code:"NR-RET", name:"Retail", note:"Shops, supermarkets, services.", body:"Retail accessibility determines who can participate in everyday economic life. Counter heights, hearing loops, automatic doors, and circulation width are the basics; sensory environment determines whether sensitive populations can shop." },
      { code:"NR-CUL", name:"Cultural", note:"Museums, theatres, libraries.", body:"Cultural institutions are frequently late adopters of accessibility provision but disproportionately host Deaf, blind, and disabled audiences. Hearing loops, captioning, and tactile wayfinding are foundational." },
      { code:"NR-HOS", name:"Hospitality", note:"Hotels, restaurants, cafés.", body:"Hospitality is where accessibility provision is often optional, segregated, or absent. Universal design here means accessible rooms are not 'special' rooms; bathrooms work for all guests; circulation accommodates everyone." },
      { code:"NR-TRP", name:"Transport", note:"Stations, airports, interchanges.", body:"Transport infrastructure is where failure to provide tactile indicators, hearing loops, and visual paging directly excludes from movement. Accessible transport infrastructure is foundational to participation." },
    ]
  }
};

// ITEMS — architect-facing spec data

const ITEMS = [

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

// ROOMS_SYNTHESIS — design synthesis data for all 14 rooms
// Merged at access time with the static room records in BUILDINGS

const ROOMS_SYNTHESIS = {

  // ═══════════════════════════════════════════════════════════════
  // R-BA — BATHROOM (priority: maximum integration density)
  // ═══════════════════════════════════════════════════════════════
  "R-BA": {
    synthesis: "The accessible bathroom is the most integrated room in the guidebook. Eight specifications touch the same 5 m² of plan, and they all need to coordinate before lining begins. Get the sequence wrong and you end up with grab bars without backing, falls steeper than 1:80, drains at the high point of the slab, or anti-scald mixers commissioned after handover when the inspector is gone.\n\nThe wet-room move (G-04) eliminates the threshold problem and the curb problem in one decision, but in exchange it demands that the entire room participate in waterproofing and falls. Floor falls of 1:80 maximum to a linear drain at the shower head wall direct water away from WC and door zones. Falls steeper than 1:80 cause wheelchair stability problems during transfer; falls shallower produce standing water. The drain at the head wall (not corner gully) prevents wet-zone water from tracking across the room.\n\nGrab bars (G-03) require structural backing — typically 18 mm ply or proprietary fixings — full wall before tile or panel lining. The backing must coordinate with G-04 plumbing rough-in: the same wall holds the shower mixer, the WC cistern, the grab bars, and often the towel rail. If the plumber sets out without knowing where the bars go, the bars cannot be installed at certification stage. This is the most common bathroom integration failure.\n\nAnti-scald mixers (I-03) are non-negotiable for bilateral one-handed operation. Hot water delivery limited to 38°C protects from scald and supports users with reduced sensation. Mixer height per H-01 (900–1100 mm AFF) and offset from back wall (600–650 mm) determine reach from the seated transfer position. LRV contrast (C-04) at the WC, grab bars, and controls supports low-vision use, but the floor follows the dementia exception (C-05) — adjacent floor materials should NOT contrast, since DEM populations read floor contrast as a step or hole. Visual fire alarm (B-10) must be visible from the shower with the door closed — IP-rated, mounted opposite. Overnight pathway lighting (B-12) terminates here.",

    sequence: [
      { step: 1, focus: "Set out floor falls", why: "Determine drain centreline, mark on slab. Falls cannot be added later; substrate is built to falls." },
      { step: 2, focus: "Coordinate plumbing rough-in with grab-bar backing", why: "Same wall, both before lining. Plumber and carpenter align before either begins." },
      { step: 3, focus: "Confirm grab-bar positions per AS 1428.1", why: "Behind WC, beside transfer side, in shower. Position determines backing extent." },
      { step: 4, focus: "Specify anti-scald mixer at procurement", why: "38°C-limited, lever or paddle. Specifying late means substitution risk." },
      { step: 5, focus: "Verify door swing outward", why: "Inward is a rescue failure when occupant falls against door. Hardware order reflects this." },
      { step: 6, focus: "Lay waterproofing to AS 3740", why: "1800 mm in shower zone, returns at door reveal. Test before tile." },
      { step: 7, focus: "Tile or panel only after waterproofing flood-test", why: "Slip rating verified on installed surface, not from brochure." },
      { step: 8, focus: "Commission anti-scald + grab-bar load test", why: "Document delivered temperature and bar load capacity at handover." }
    ],

    interactions: [
      { specs: ["G-04", "G-03"], note: "Wet-room walls and grab-bar backing share the same plane — plumbing rough-in and ply backing must coordinate before lining or bars cannot be installed at certification" },
      { specs: ["G-04", "E-07"], note: "Falls steeper than 1:80 combined with slip rating below P5 wet creates fall risk during transfer — both must be in spec together" },
      { specs: ["I-03", "H-01"], note: "Anti-scald mixer location must be operable from seated transfer position — height (900–1100 AFF) and offset (600–650 from back wall) coordinate" },
      { specs: ["B-10", "G-04"], note: "Visual alarm must be IP-rated for wet zone and visible from shower with door closed — placement decided in design phase, not by fire contractor late" },
      { specs: ["C-04", "C-05"], note: "Bathroom is one of the rare rooms where the dementia floor-contrast exception applies — continuous floor LRV intentional even as walls and fixtures contrast" },
      { specs: ["B-12", "G-04"], note: "Overnight pathway lighting terminates seamlessly across the threshold — no aluminium track or contrast change at door" }
    ],

    clearances: [
      { what: "Room minimum (corner WC layout)", dim: "2400 × 2100 mm", ref: "AS 1428.1 §15" },
      { what: "WC clear floor space — alongside", dim: "950 × 1300 mm", ref: "Beside the pan, free of obstruction" },
      { what: "WC clear floor space — in front", dim: "1200 × 1900 mm", ref: "Excluding pan footprint" },
      { what: "Shower clear zone", dim: "1200 × 1200 mm", ref: "Free of obstruction at floor level" },
      { what: "Door clear opening", dim: "≥850 mm", ref: "Outward swing mandatory" },
      { what: "WC pan height", dim: "460–480 mm AFF (top of seat)", ref: "AS 1428.1 §15.2" },
      { what: "WC pan setback from transfer wall", dim: "400 mm centreline", ref: "AS 1428.1 §15.2" },
      { what: "Floor fall to drain", dim: "1:80 maximum (1:100 preferred)", ref: "Steeper risks wheelchair stability" },
      { what: "Linear drain length", dim: "≥800 mm at shower head wall", ref: "Channel grate, full wall length" },
      { what: "Shower controls — height", dim: "900–1100 mm AFF", ref: "Per H-01 reach range" },
      { what: "Shower controls — offset from back wall", dim: "600–650 mm on entry side", ref: "Operable from transfer position" }
    ],

    failures: [
      "Shower curb retained 'just in case' — defeats wheelchair entry entirely; this is a fundamental misunderstanding of accessible design",
      "Grab-bar backing forgotten or set without coordinating to bar positions — bars cannot be installed at certification",
      "Plumber sets out without backing coordination; bar fixings clash with concealed pipes",
      "Floor falls set after framing rather than before substrate; drain ends up at high point of slab — water pools",
      "Anti-scald mixer omitted from spec or substituted at procurement; delivery >43°C scalds in seconds",
      "Inward-swinging door blocks rescue when occupant falls against it",
      "Linear drain at shower head wall replaced with corner gully — water tracks across WC clear zone",
      "Bathroom VAD omitted; Deaf occupant in shower with door closed has no fire alarm signal"
    ],

    diagram: {
      type: "plan",
      svg: `<svg viewBox="0 0 360 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan of accessible wet-room bathroom showing zone overlay with WC clear zone, shower clear zone, linear drain, fall direction, door swing, and fixture coordination">
        <rect x="20" y="20" width="320" height="220" fill="none" stroke="#1A1612" stroke-width="2"/>
        <rect x="24" y="24" width="312" height="212" fill="none" stroke="#1A1612" stroke-width="0.4"/>
        <text x="30" y="40" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">BATHROOM — wet room</text>
        <text x="30" y="52" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">2400 × 2100 minimum</text>

        <ellipse cx="80" cy="80" rx="22" ry="16" fill="none" stroke="#1A1612" stroke-width="1.2"/>
        <rect x="60" y="60" width="40" height="14" fill="#1A1612" fill-opacity="0.1" stroke="#1A1612" stroke-width="0.6"/>
        <text x="105" y="84" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">WC</text>

        <rect x="120" y="50" width="80" height="80" fill="none" stroke="#1A1612" stroke-width="0.6" stroke-dasharray="4 3"/>
        <text x="135" y="85" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">WC clear zone</text>
        <text x="135" y="98" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">950 × 1300</text>

        <rect x="220" y="50" width="100" height="100" fill="#1A1612" fill-opacity="0.05" stroke="#1A1612" stroke-width="0.6" stroke-dasharray="4 3"/>
        <text x="240" y="80" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">SHOWER</text>
        <text x="237" y="93" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">1200 × 1200 clear</text>

        <rect x="220" y="46" width="100" height="4" fill="#1A1612"/>
        <text x="220" y="40" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">linear drain ≥800 — at head wall</text>

        <circle cx="226" cy="105" r="3" fill="#1A1612"/>
        <text x="232" y="108" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">mixer</text>
        <text x="180" y="170" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">600 from back wall</text>

        <path d="M 130 220 L 280 60" stroke="#1A1612" stroke-width="0.5" stroke-dasharray="2 3"/>
        <text x="35" y="220" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">→ falls 1:80 max →</text>

        <line x1="120" y1="240" x2="180" y2="240" stroke="#fff" stroke-width="3"/>
        <line x1="120" y1="240" x2="180" y2="240" stroke="#1A1612" stroke-width="1.5" stroke-dasharray="4 2"/>
        <path d="M 120 240 Q 120 215 145 215" fill="none" stroke="#1A1612" stroke-width="0.8" stroke-dasharray="2 2"/>
        <text x="115" y="255" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">≥850 outward</text>

        <line x1="40" y1="160" x2="40" y2="220" stroke="#1A1612" stroke-width="2"/>
        <line x1="40" y1="200" x2="50" y2="200" stroke="#1A1612" stroke-width="1.2"/>
        <text x="55" y="190" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">grab bars</text>
        <text x="55" y="200" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">+ backing</text>

        <rect x="290" y="200" width="40" height="32" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.6"/>
        <text x="294" y="218" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">vanity</text>
      </svg>`
    }
  },

  // ═══════════════════════════════════════════════════════════════
  // R-KIT — KITCHEN (priority: high integration)
  // ═══════════════════════════════════════════════════════════════
  "R-KIT": {
    synthesis: "The kitchen is the densest concentration of operable elements in a domestic environment. Heights, reach, weight, heat, slip, contrast — every dimension of the body matters. Designed well, it serves any user. Designed default — single counter height, fixed-position controls, glossy patterned splashback — it excludes a large fraction of the population from independent meal preparation.\n\nSeated-task design (F-05) is the planning module for the entire kitchen. Every routine task — chopping, washing, cooking, cleaning — must be achievable from a seated position. This drives counter heights, knee clearance, sink position, cooktop type, and storage location simultaneously. Adjustable-height surfaces (G-05, 650–870 mm AFF) are the gold standard. Where adjustable is not feasible, provide a tiered approach: one prep zone at 750 mm AFF (seated work), one zone at 870 mm AFF (standing work).\n\nOne-handed operation throughout (I-02) follows from the same principle. Single-lever taps with anti-scald limit. Side-opening ovens not under-bench. Induction cooktops with front-edge controls (not centre or rear). Drawers with full-extension runners. Lever or D-pull hardware (I-01) on every door and drawer. Anti-scald mixer (I-03) at the sink — kitchen scalding is real and frequent.\n\nReach (H-01) governs control placement: switches, GPOs, range-hood controls, dishwasher start, all within 400–1100 mm AFF. GPOs above the bench (≥150 mm above counter) for plug accessibility from the seated position; below-counter GPOs are unreachable from a wheelchair and a back-strain hazard from standing.\n\nFlicker-free under-cabinet lighting (B-04) is critical because the kitchen is a focused-task environment where bad lighting compounds all the other accessibility problems. Choose drivers carefully — many under-cabinet LED strips flicker badly when dimmed. Slip resistance (E-07, P5 wet) at the sink approach and around the dishwasher.\n\nLRV contrast (C-04) at counter front edges, hob ring, sink rim, control plates. Pattern avoidance (C-03) on splashback and floor — patterned tiles confuse low-vision users and dementia populations. The kitchen is where 'aesthetic' specifications most often conflict with accessibility; resolve in favour of accessibility.",

    sequence: [
      { step: 1, focus: "Establish seated-task envelope (F-05)", why: "Determines counter heights, knee clearances, and reach zones for every other decision" },
      { step: 2, focus: "Specify adjustable-height counter zones (G-05)", why: "650–870 mm AFF range; allocate which zones adjust" },
      { step: 3, focus: "Plan reach envelope for controls (H-01)", why: "All switches, GPOs, appliance controls 400–1100 mm AFF; stack GPOs above counter" },
      { step: 4, focus: "Select appliances for one-handed operation (I-02)", why: "Side-opening ovens, induction cooktop with front-edge controls, full-extension drawers" },
      { step: 5, focus: "Specify anti-scald mixer at sink (I-03)", why: "Single-lever, 38°C-limited; same hardware logic as bathroom" },
      { step: 6, focus: "Coordinate slip-resistant floor (E-07)", why: "P5 wet at sink approach and around dishwasher; consistent across kitchen floor" },
      { step: 7, focus: "Plan under-cabinet flicker-free LED (B-04)", why: "Drivers verified across full dimming range; task lighting is the most-used in kitchen" },
      { step: 8, focus: "Verify LRV contrast on edges and controls (C-04)", why: "Counter front, hob ring, sink rim, switches — measurable on installed materials" }
    ],

    interactions: [
      { specs: ["F-05", "G-05", "H-01"], note: "Seated-task design, adjustable counters, and reach range must coordinate — together they define the kitchen's operating envelope; any one decided in isolation fails the others" },
      { specs: ["I-02", "I-03"], note: "One-handed kitchen operation includes anti-scald taps; both follow the same upper-limb logic — the kitchen's sink is one fixture serving two specs" },
      { specs: ["H-01", "C-04"], note: "Control placement and contrast: GPOs above bench need contrast against splashback; switch plates need contrast against wall — not actuator-against-plate alone" },
      { specs: ["B-04", "F-04"], note: "Under-cabinet LED selection affects both flicker and air quality (driver heat dispersion); cheap drivers fail both" },
      { specs: ["C-03", "C-04"], note: "Pattern avoidance and contrast operate on the same visual system — busy splashback patterns defeat contrast at the cooktop" },
      { specs: ["E-07", "G-04"], note: "Slip resistance continuity from kitchen to adjacent bathroom or laundry — no abrupt change in PTV at the threshold" }
    ],

    clearances: [
      { what: "Kitchen circulation — minimum aisle", dim: "≥1200 mm between bench fronts", ref: "Permits wheelchair turn within space" },
      { what: "Knee clearance under counter", dim: "≥800 W × 700 H × 480 D mm", ref: "AS 1428.2 §11" },
      { what: "Counter height — seated zone", dim: "750 mm AFF (or adjustable to 650)", ref: "G-05" },
      { what: "Counter height — standing zone", dim: "870 mm AFF (or adjustable to 870)", ref: "G-05" },
      { what: "Sink height — seated", dim: "Rim 800 mm AFF", ref: "Knee clearance preserved beneath" },
      { what: "Cooktop edge from seated zone", dim: "≤300 mm reach to controls", ref: "Front-edge controls preferred" },
      { what: "GPOs above bench", dim: "150–300 mm above counter", ref: "Per H-01 reach range" },
      { what: "Switch height", dim: "900–1100 mm AFF", ref: "H-01" },
      { what: "Storage reach — high", dim: "≤1100 mm AFF (seated) or pull-down", ref: "Above this is inaccessible from seated" },
      { what: "Storage reach — low", dim: "≥400 mm AFF (seated) or pull-out", ref: "Below this is inaccessible without floor transfer" }
    ],

    failures: [
      "Single counter height (900 mm AFF) throughout — excludes seated work entirely",
      "Wall ovens above counter height — door operation requires standing reach plus heat tolerance",
      "Cooktop with rear or centre controls — reach across hot zone unsafe and unreachable seated",
      "GPOs at standard 300 mm AFF below counter — unreachable from wheelchair, back-strain standing",
      "Glossy patterned splashback — defeats contrast at cooktop, confuses low vision",
      "Knee clearance compromised by deep skirting or lower drawer face — wheelchair cannot pull in",
      "Under-cabinet LED with PWM driver flickering at 5% dim — task lighting failure point",
      "Anti-scald mixer omitted at kitchen sink — scald incidents are statistically frequent",
      "Patterned floor tile — confuses depth perception, dementia trip hazard"
    ],

    diagram: {
      type: "plan",
      svg: `<svg viewBox="0 0 360 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan of accessible kitchen showing seated-task zone, adjustable counter, reach envelope, and circulation aisle">
        <rect x="20" y="20" width="320" height="200" fill="none" stroke="#1A1612" stroke-width="2"/>
        <text x="30" y="38" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">KITCHEN — galley</text>

        <rect x="20" y="50" width="320" height="40" fill="#1A1612" fill-opacity="0.08" stroke="#1A1612" stroke-width="0.5"/>
        <text x="30" y="74" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">upper bench — 870 standing zone</text>

        <rect x="20" y="180" width="320" height="40" fill="#1A1612" fill-opacity="0.04" stroke="#1A1612" stroke-width="0.5"/>
        <rect x="100" y="180" width="80" height="40" fill="#1A1612" fill-opacity="0.12" stroke="#1A1612" stroke-width="0.6"/>
        <text x="105" y="205" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">seated zone</text>
        <text x="105" y="216" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">650–750 AFF</text>
        <rect x="100" y="180" width="80" height="40" fill="none" stroke="#1A1612" stroke-width="0.4" stroke-dasharray="3 2"/>
        <text x="200" y="205" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">cooktop</text>
        <text x="200" y="216" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">front controls</text>
        <text x="248" y="205" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">sink</text>
        <text x="248" y="216" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">anti-scald</text>

        <line x1="20" y1="135" x2="340" y2="135" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="20" y1="132" x2="20" y2="138" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="340" y1="132" x2="340" y2="138" stroke="#1A1612" stroke-width="0.6"/>
        <text x="155" y="130" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">aisle ≥1200 mm</text>

        <circle cx="170" cy="135" r="14" fill="none" stroke="#1A1612" stroke-width="0.5" stroke-dasharray="2 2"/>
        <text x="155" y="155" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">w/c turn</text>

        <text x="30" y="100" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">GPOs ≥150 above counter</text>
        <text x="30" y="170" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">knee clearance ≥800 × 700 × 480</text>
      </svg>`
    }
  },

  // ═══════════════════════════════════════════════════════════════
  // R-BED — BEDROOM (priority: sleep ecosystem)
  // ═══════════════════════════════════════════════════════════════
  "R-BED": {
    synthesis: "The bedroom is a sleep ecosystem. Sleep quality is the foundation of cognitive, mood, and pain regulation across nearly every population in this guidebook — disrupted sleep accelerates dementia symptoms, deepens depression, undermines brain-injury recovery, amplifies chronic pain, and depletes neurological reserve. The bedroom either supports sleep or it doesn't, and the difference is in the integration of acoustics, lighting, thermal control, and emergency provision.\n\nAcoustic isolation is the foundation. Three specifications coordinate: HVAC noise control (A-08, ≤NC-25 maximum), HVAC vibration isolation (A-09), and double-leaf partition (A-14, STC ≥50) where the bedroom adjoins occupied or service spaces. The lift shaft adjacent to a bedroom is the most common aged-care failure case. The kitchen on the other side of a single-leaf partition is the most common residential failure case. Plant rooms above are the most common multi-residential failure case. Address all three at planning.\n\nCircadian lighting (B-01) supports the daily rhythm: ≥150 EML at eye level during daytime, dropping to <50 EML in evening. Warm CCT after 19:00 (B-11, ≤2700 K) reinforces the sleep cue. Sensor-activated overnight pathway lighting (B-12) provides safe nocturnal toilet access without waking the user fully — 5–10 lux warm CCT at floor level, on motion. Flicker-free LED throughout (B-04) — the bedside lamp is a focused light source where flicker is most perceptible.\n\nIndividual environmental control (H-02) means thermostat and lighting controllable from bed. Per H-01, controls 400–1100 mm AFF — bedside switch within reach from supine. Visual fire alarm (B-10) coordinated with pillow-shaker for Deaf occupants. Bedroom emergency call + overnight lighting (G-09) is a code requirement in aged care and a wise provision elsewhere. Wardrobe reach (G-08) for dressing without standing.\n\nFor occupants whose pain or fatigue confines them to the bedroom for extended periods (OFS, advanced PAIN), the bedroom is also the living room — air quality, thermal stability, individual control, and visual access all matter more.",

    sequence: [
      { step: 1, focus: "Plan acoustic isolation", why: "A-14 partition + A-08 HVAC + A-09 vibration coordinate; addressing one without others fails the room" },
      { step: 2, focus: "Specify circadian lighting strategy", why: "B-01 daytime + B-11 evening CCT shift + B-12 overnight pathway — three coordinated zones in time" },
      { step: 3, focus: "Locate bedside controls within reach (H-01)", why: "Light, thermostat, emergency call all 400–1100 mm AFF; reachable from supine" },
      { step: 4, focus: "Confirm wardrobe reach configuration (G-08)", why: "Hanging rail at 1100 mm AFF (seated reach); shelf at 400–1100 mm; pull-down rail above" },
      { step: 5, focus: "Coordinate VAD + pillow shaker (B-10, G-09)", why: "Deaf occupants asleep need tactile + visual; mattress-mounted shaker plus wall-mounted strobe" },
      { step: 6, focus: "Verify flicker-free at bedside lamps", why: "B-04 across full dimming range; bedside is focused-light environment where flicker is most perceptible" },
      { step: 7, focus: "Specify air quality + thermal stability (F-04, H-02)", why: "MERV 13+, low-VOC, individual thermostat — for extended-occupation users" }
    ],

    interactions: [
      { specs: ["A-08", "A-09", "A-14"], note: "Three acoustic specs coordinate — HVAC noise, vibration, and partition isolation each address a different transmission path; missing one undermines the others" },
      { specs: ["B-01", "B-11", "B-12"], note: "Daytime, evening, and overnight lighting — three zones in time, all on the same tunable LED system; specify together or the system cannot deliver all three" },
      { specs: ["B-10", "G-09"], note: "Bedside emergency call and visual fire alarm typically coexist on the same wall — specify together to avoid duplication and ensure both reachable from bed" },
      { specs: ["H-02", "H-01"], note: "Individual thermostat and lighting control on the same bedside panel — both within 400–1100 mm AFF, operable supine" },
      { specs: ["G-08", "H-01"], note: "Wardrobe reach configuration follows the same reach envelope as control placement — high shelf inaccessible without pull-down rail" }
    ],

    clearances: [
      { what: "Room minimum (single bed, accessible)", dim: "3000 × 3500 mm", ref: "Bed + wheelchair turn + transfer space + furniture" },
      { what: "Wheelchair turn space — beside bed", dim: "≥1540 mm dia", ref: "Power wheelchair turn" },
      { what: "Transfer space — bedside", dim: "1500 × 800 mm", ref: "On at least one side; both preferred" },
      { what: "Bed height", dim: "450–500 mm AFF (top of mattress)", ref: "Standard transfer height; adjustable preferred" },
      { what: "Bedside switch height", dim: "400–1100 mm AFF (reachable supine)", ref: "H-01" },
      { what: "Wardrobe hanging rail — accessible", dim: "1100 mm AFF (or pull-down to 1100)", ref: "G-08" },
      { what: "Wardrobe shelf range", dim: "400–1100 mm AFF", ref: "Reach envelope; above requires pull-down" },
      { what: "VAD mounting", dim: "Wall, opposite bed, 2000–2400 AFF", ref: "B-10 / AS 4428.16" },
      { what: "Pillow shaker offset from pillow", dim: "≤1500 mm", ref: "B-10 — tactile reach when sleeping" },
      { what: "Acoustic partition rating to adjacent", dim: "STC ≥50 (occupied), STC ≥45 (corridor)", ref: "A-14" },
      { what: "HVAC background noise", dim: "≤NC-25 (≈30–35 dB(A))", ref: "A-08" }
    ],

    failures: [
      "Bedroom adjacent to lift shaft, plant room, or kitchen with single-leaf partition — A-14 STC ≥50 not achieved",
      "HVAC commissioned to NC-30 instead of NC-25 — sleep disruption from constant low-frequency noise",
      "Bedside lamp with PWM driver flickering at low dim — focused-light flicker is most perceptible",
      "Single-CCT lighting throughout the day — circadian disruption, sleep cue lost",
      "No overnight pathway lighting; overhead light required for toilet trips — disrupts sleep return",
      "Bedside switch at 1300 mm AFF — out of reach from supine",
      "VAD without pillow shaker — Deaf occupant asleep cannot be alerted",
      "Wardrobe rail at 1700 mm AFF without pull-down — entire wardrobe inaccessible to seated user",
      "Air quality not addressed for extended-occupation users — MCAS triggers, OFS symptom escalation"
    ],

    diagram: {
      type: "plan",
      svg: `<svg viewBox="0 0 360 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan of accessible bedroom showing bed position, transfer zones both sides, wheelchair turn, and zone callouts for acoustic, lighting, and emergency provisions">
        <rect x="20" y="20" width="320" height="240" fill="none" stroke="#1A1612" stroke-width="2"/>
        <rect x="24" y="24" width="312" height="232" fill="none" stroke="#1A1612" stroke-width="0.4"/>
        <text x="30" y="40" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">BEDROOM</text>
        <text x="30" y="52" font-family="JetBrains Mono, monospace" font-size="8" fill="#6B5F50">3000 × 3500 minimum</text>

        <rect x="120" y="80" width="120" height="80" fill="#1A1612" fill-opacity="0.18" stroke="#1A1612" stroke-width="0.8"/>
        <rect x="120" y="80" width="120" height="20" fill="#1A1612" fill-opacity="0.4"/>
        <text x="160" y="95" font-family="JetBrains Mono, monospace" font-size="8" fill="#F2EBDD">pillow</text>
        <text x="165" y="135" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">BED</text>

        <rect x="60" y="80" width="50" height="80" fill="none" stroke="#1A1612" stroke-width="0.6" stroke-dasharray="3 2"/>
        <text x="65" y="120" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">transfer</text>
        <text x="65" y="131" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">1500 × 800</text>

        <rect x="250" y="80" width="50" height="80" fill="none" stroke="#1A1612" stroke-width="0.6" stroke-dasharray="3 2"/>
        <text x="255" y="120" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">transfer</text>

        <circle cx="180" cy="200" r="38" fill="none" stroke="#1A1612" stroke-width="0.4" stroke-dasharray="3 2"/>
        <text x="160" y="205" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">1540 turn</text>

        <rect x="115" y="74" width="6" height="14" fill="#1A1612"/>
        <text x="100" y="74" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">switch + call</text>
        <rect x="239" y="74" width="6" height="14" fill="#1A1612"/>
        <text x="240" y="74" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">switch + call</text>

        <rect x="120" y="80" width="120" height="6" fill="none" stroke="#1A1612" stroke-width="0.5"/>
        <text x="155" y="78" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">pillow shaker zone</text>

        <circle cx="320" cy="60" r="6" fill="#1A1612"/>
        <text x="280" y="63" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">VAD</text>

        <rect x="290" y="200" width="40" height="50" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.5"/>
        <text x="294" y="225" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">wardrobe</text>
        <text x="294" y="236" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">G-08</text>
      </svg>`
    }
  },

  // ═══════════════════════════════════════════════════════════════
  // R-LIV — LIVING ROOM (priority: extended occupation)
  // ═══════════════════════════════════════════════════════════════
  "R-LIV": {
    synthesis: "The living room is the most occupied space in most homes — long stretches of unstructured presence, sleep-adjacent rest, focused activity, social gathering, and solitary regulation, often within a single afternoon. The accessibility brief is therefore breadth, not depth: the room must accommodate every kind of occupation a body can do.\n\nAcoustic ceiling treatment (A-02, NRC ≥0.85 over 70%+ of ceiling area) reduces reverberation that otherwise compounds across television, conversation, kitchen noise from adjacent space, and circulation. Where the living room shares partition with bedrooms, A-14 (STC ≥50) prevents night-time disturbance.\n\nLighting is the most multi-mode system in the room. Individual dimming (B-06, ≥300 lux range) lets occupants find their comfortable level — different bodies need different light. Warm CCT in evening (B-11, ≤2700 K) supports circadian regulation. Flicker-free across the dimming range (B-04). Where the living room hosts daytime activity for extended-occupation users (DEM, OFS, NEU, NDV/MH), circadian lighting (B-01) at ≥150 EML supports daily rhythm.\n\nThree seat heights at every gathering (G-02 — 380, 450, 520 mm AFF) is the single most underspecified provision in this room. A single sofa height excludes everyone whose body needs different. Defensible seating (G-01, back-to-wall with sightline to entry) is critical for trauma-informed and sensory-sensitive populations — at least one seat in every grouping should not require the occupant to sit with their back to the room.\n\nMuted, low-chroma palette (C-01) and pattern avoidance (C-03) are the visual baseline. Plain finishes throughout. Saturated accent walls and patterned upholstery defeat both NDV and DEM populations simultaneously. LRV contrast at controls and door frames (C-04) — but not adjacent floor materials, per the dementia exception (C-05).\n\nIndividual environmental control (H-02) for thermostat and lighting on the wall reachable from primary seating. Reach range (H-01) for all controls. Visual fire alarm (B-10) on the wall most visible from primary seating positions.",

    sequence: [
      { step: 1, focus: "Set acoustic baseline (A-02 ceiling, A-14 to bedrooms)", why: "Reverberation control before reflective finishes are introduced" },
      { step: 2, focus: "Plan lighting zones (B-01, B-06, B-11)", why: "Circadian + dimmable + warm-evening; tunable LED system specified once for all three" },
      { step: 3, focus: "Locate seating with three heights (G-02) and at least one defensible position (G-01)", why: "Furniture layout affects partition planning; defensible seating needs wall against back" },
      { step: 4, focus: "Specify muted palette (C-01) and pattern avoidance (C-03)", why: "Material selection at design phase; substitution at procurement is the failure mode" },
      { step: 5, focus: "Place environmental controls within reach (H-01, H-02)", why: "Thermostat and dimmer accessible from primary seated position" },
      { step: 6, focus: "Position VAD per visibility from seating (B-10)", why: "Wall opposite primary seating; verified by line-of-sight check" },
      { step: 7, focus: "Coordinate flicker-free LED with dimmer compatibility (B-04, B-06)", why: "Mismatched dimmer-driver pairs flicker even with compliant fixtures" }
    ],

    interactions: [
      { specs: ["A-02", "A-05"], note: "Ceiling and floor absorption together cover most reflection paths — soft floor finishes complete the strategy ceiling alone cannot" },
      { specs: ["B-01", "B-06", "B-11"], note: "Circadian, dimmable, and warm-evening lighting all on the same tunable LED + driver system; specify together" },
      { specs: ["B-04", "B-06"], note: "Driver compatibility with dimmer is the failure point; flicker-free at 100% but flickering at 5% is a common spec gap" },
      { specs: ["G-01", "D-07"], note: "Defensible seating and no-blind-corners both serve trauma-informed populations; the room geometry determines whether back-to-wall seating is possible" },
      { specs: ["G-02", "E-10"], note: "Three seating heights principle applies in living and on circulation routes — same reasoning, room-scale and corridor-scale" },
      { specs: ["C-01", "C-03"], note: "Muted palette and pattern avoidance work together — saturated patterned upholstery defeats both" }
    ],

    clearances: [
      { what: "Living room minimum (accessible)", dim: "4000 × 4500 mm", ref: "Multiple seating + circulation + wheelchair turn" },
      { what: "Wheelchair turn — primary occupied zone", dim: "≥1540 mm dia", ref: "Within reach of seating group" },
      { what: "Circulation around furniture", dim: "≥1000 mm clear", ref: "≥1200 mm preferred for primary route" },
      { what: "Primary seating to TV/focal point", dim: "Per use — 2.5–3.5 × screen diagonal", ref: "Standard residential" },
      { what: "Three seat heights at gathering", dim: "380 / 450 / 520 mm AFF", ref: "G-02" },
      { what: "Defensible seat — back to wall", dim: "≥1 seat per group, sightline to entry", ref: "G-01" },
      { what: "Control wall — thermostat / dimmer", dim: "Reachable from primary seat, 400–1100 AFF", ref: "H-01, H-02" }
    ],

    failures: [
      "Hard plaster ceiling, glossy floor, and patterned cushions — RT60 high, speech intelligibility lost",
      "Single sofa height (450 mm) — excludes shorter and elderly users from the gathering",
      "Open-plan with kitchen adjacent — A-14 cannot be applied; acoustic separation impossible",
      "Saturated accent wall as 'feature' — NDV and DEM populations both excluded",
      "Patterned rug 'softening' the space — confuses depth perception, dementia trip hazard",
      "Single-CCT downlights — no circadian support for extended-occupation users",
      "Defensible seating absent — trauma-informed populations cannot relax",
      "Dimmer mismatched with LED driver — flicker at low settings, headache trigger"
    ],

    diagram: {
      type: "plan",
      svg: `<svg viewBox="0 0 360 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan of accessible living room with sofa group, three seat heights, defensible seating, wheelchair turn, and control locations">
        <rect x="20" y="20" width="320" height="200" fill="none" stroke="#1A1612" stroke-width="2"/>
        <text x="30" y="38" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">LIVING ROOM</text>

        <rect x="40" y="160" width="120" height="40" fill="#1A1612" fill-opacity="0.18" stroke="#1A1612" stroke-width="0.6"/>
        <text x="55" y="185" font-family="JetBrains Mono, monospace" font-size="8" fill="#F2EBDD">sofa — 450</text>

        <rect x="200" y="80" width="50" height="40" fill="#1A1612" fill-opacity="0.18" stroke="#1A1612" stroke-width="0.6"/>
        <text x="207" y="105" font-family="JetBrains Mono, monospace" font-size="7" fill="#F2EBDD">chair</text>
        <text x="207" y="116" font-family="JetBrains Mono, monospace" font-size="6" fill="#F2EBDD">520</text>
        <text x="200" y="74" font-family="JetBrains Mono, monospace" font-size="6" fill="#1A1612">defensible — back to wall</text>

        <rect x="270" y="100" width="40" height="40" fill="#1A1612" fill-opacity="0.18" stroke="#1A1612" stroke-width="0.6"/>
        <text x="278" y="125" font-family="JetBrains Mono, monospace" font-size="6" fill="#F2EBDD">380</text>

        <circle cx="200" cy="170" r="38" fill="none" stroke="#1A1612" stroke-width="0.4" stroke-dasharray="3 2"/>
        <text x="178" y="175" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">1540 turn</text>

        <rect x="50" y="40" width="60" height="14" fill="#1A1612" fill-opacity="0.4"/>
        <text x="55" y="51" font-family="JetBrains Mono, monospace" font-size="7" fill="#F2EBDD">TV / focal</text>

        <rect x="22" y="100" width="6" height="20" fill="#1A1612"/>
        <text x="32" y="115" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">therm + dim</text>
        <circle cx="335" cy="50" r="6" fill="#1A1612"/>
        <text x="290" y="52" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">VAD</text>
      </svg>`
    }
  },

  // ═══════════════════════════════════════════════════════════════
  // R-HAL — HALLWAY (priority: circulation backbone)
  // ═══════════════════════════════════════════════════════════════
  "R-HAL": {
    synthesis: "The hallway is where buildings reveal whether they were designed for a body or for a plan. Width determines passability, landmarks determine wayfinding, surface determines acoustics, lighting determines safety at night. Five specifications coordinate, and the failure of any one degrades the whole.\n\nClear width (E-08, ≥1200 mm continuous, ≥1500 mm at door approaches) is measured between obstructions, not finished walls. Skirting, pin-boards, fire-hose reels, drinking fountains, surface-mounted lighting all reduce effective width. The most common failure is specifying 1200 mm wall-to-wall and losing 100 mm to projections each side. Rest seating (E-10) at maximum 20 m intervals must sit in alcoves rather than corridor projections — corridor-projecting seating defeats E-08 entirely.\n\nLandmarks at decision points (D-04) anchor procedural memory of routes. Each junction needs a unique, memorable visual feature — artwork, daylight, sculptural object — placed where it can be seen on approach. No blind corners (D-07): curved or splayed corners or convex mirrors at concealed junctions, so wheelchair users have reaction time and trauma-informed populations are not entrapped.\n\nLighting (B-04 flicker-free, B-12 overnight pathway) supports both daytime safety and night transit. The hallway's overnight lighting is the bridge between bedroom and bathroom — sensor-activated, low-level, warm CCT, at floor level. Bright overhead at 3 a.m. is wrong even where well-intentioned.\n\nLRV contrast (C-04) at door frames, leaves, hardware, and along the corridor edge for low-vision wayfinding. Pattern avoidance on the floor (C-03) — patterned carpet runners are the most common dementia-trip-hazard flooring choice. Acoustic absorption: carpet (A-05) reduces footfall and reverberation that otherwise carry through the hallway and into adjacent occupied spaces.",

    sequence: [
      { step: 1, focus: "Set out clear width (E-08) accounting for projections", why: "1200 mm continuous between obstructions — verify after MEP rough-in, before lining" },
      { step: 2, focus: "Plan landmark positions at every decision point (D-04)", why: "One unique landmark per junction; coordinate with FF&E budget so they're not value-engineered out" },
      { step: 3, focus: "Address blind corners (D-07)", why: "Splayed walls, curved corners, or convex mirrors where geometry forces concealment" },
      { step: 4, focus: "Locate rest seating in alcoves (E-10)", why: "≤20 m intervals; alcoves preserve corridor width" },
      { step: 5, focus: "Specify floor finish for acoustic + visual (A-05, C-03, C-04)", why: "Carpet for absorption; plain pattern for clarity; LRV contrast at edges, not field" },
      { step: 6, focus: "Plan overnight pathway lighting (B-12)", why: "Sensor-activated low-level LED, warm CCT, at floor level — bedroom-to-bathroom path" },
      { step: 7, focus: "Verify all hardware and frames meet contrast (C-04)", why: "Door frame against wall, leaf against frame, hardware against leaf — three contrasts, each ≥30 LRV" }
    ],

    interactions: [
      { specs: ["E-08", "E-10"], note: "Clear width and rest seating directly conflict if seating projects from corridor — alcoves resolve; corridor-projecting seating reduces width below E-08 minimum" },
      { specs: ["D-04", "D-07"], note: "Landmarks and blind-corner treatment both serve wayfinding — landmark visibility on approach to corner depends on no-blind-corner geometry" },
      { specs: ["A-05", "B-08"], note: "Carpet for acoustic absorption and matte finish for visual — same flooring decision serves both, but carpet pattern selection critical for C-03" },
      { specs: ["B-12", "C-04"], note: "Overnight pathway lighting and LRV contrast — at low light levels, contrast must be sufficient to remain visible" },
      { specs: ["E-08", "D-07"], note: "Width and corner reaction time work together — narrower corridor + blind corner is unsafe in combination, less so individually" }
    ],

    clearances: [
      { what: "Clear width — primary route", dim: "≥1200 mm between obstructions", ref: "E-08; not wall-to-wall" },
      { what: "Clear width — door approach", dim: "≥1500 mm", ref: "Localised widening 600 mm before door swing" },
      { what: "Headroom", dim: "≥2000 mm continuous", ref: "Signage, ducts must not encroach below" },
      { what: "Maximum projection from wall", dim: "≤100 mm below 2000 mm AFF", ref: "Above unrestricted" },
      { what: "Rest seating spacing", dim: "≤20 m intervals", ref: "E-10; alcove dimensions ≥1500 × 600" },
      { what: "Landmark spacing — primary route", dim: "≤15 m between landmarks", ref: "D-04" },
      { what: "Turning circle — dead-end", dim: "≥1540 mm dia", ref: "Power wheelchair" },
      { what: "Overnight pathway light level", dim: "5–10 lux at floor", ref: "B-12; warm CCT only" },
      { what: "Door frame to wall LRV", dim: "≥30 percentage points", ref: "C-04" }
    ],

    failures: [
      "1200 mm wall-to-wall corridor losing 200 mm to skirting and pinboards each side — effective 800 mm",
      "Surface-mounted hand sanitiser dispensers added post-occupation, projecting 150 mm",
      "Rest seating projecting from corridor — width below 1200 at the seat",
      "Identical landmarks at multiple junctions — defeats memorability",
      "Patterned carpet runner — dementia trip hazard, low-vision confusion",
      "Bright overhead lights at night — wakes user fully, disrupts sleep return",
      "Door frame matching wall (white-on-white) — door invisible to low vision",
      "Blind corner without mirror or splay — wheelchair entrapment risk"
    ],

    diagram: {
      type: "plan",
      svg: `<svg viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan of hallway showing 1200 mm clear width, rest seating alcove, landmark, and door approach widening">
        <rect x="20" y="80" width="360" height="60" fill="#1A1612" fill-opacity="0.04" stroke="#1A1612" stroke-width="0.8"/>

        <line x1="20" y1="100" x2="380" y2="100" stroke="#1A1612" stroke-width="0.4" stroke-dasharray="3 2"/>
        <line x1="20" y1="120" x2="380" y2="120" stroke="#1A1612" stroke-width="0.4" stroke-dasharray="3 2"/>
        <text x="100" y="115" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">≥1200 clear</text>

        <rect x="120" y="50" width="60" height="30" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.6"/>
        <rect x="135" y="58" width="14" height="14" fill="#1A1612" fill-opacity="0.4"/>
        <text x="125" y="46" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">rest alcove</text>
        <text x="125" y="76" font-family="JetBrains Mono, monospace" font-size="6" fill="#F2EBDD">E-10</text>

        <rect x="240" y="60" width="14" height="20" fill="#1A1612"/>
        <text x="220" y="56" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">landmark</text>
        <text x="220" y="46" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">D-04</text>

        <rect x="300" y="80" width="60" height="60" fill="#1A1612" fill-opacity="0.08" stroke="#1A1612" stroke-width="0.5"/>
        <text x="305" y="120" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">≥1500 door zone</text>
        <line x1="360" y1="80" x2="360" y2="130" stroke="#1A1612" stroke-width="2.5"/>
        <path d="M 360 130 Q 350 115 335 110" fill="none" stroke="#1A1612" stroke-width="0.8" stroke-dasharray="2 2"/>

        <line x1="20" y1="180" x2="380" y2="180" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="20" y1="177" x2="20" y2="183" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="380" y1="177" x2="380" y2="183" stroke="#1A1612" stroke-width="0.6"/>
        <text x="160" y="195" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">≤20 m to next alcove · ≤15 m landmarks</text>

        <circle cx="60" cy="155" r="3" fill="#1A1612"/>
        <text x="35" y="170" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">B-12 night</text>
      </svg>`
    }
  },

  // ═══════════════════════════════════════════════════════════════
  // R-ENT — ENTRY (priority: threshold)
  // ═══════════════════════════════════════════════════════════════
  "R-ENT": {
    synthesis: "The entry sets the tone of the dwelling and determines who can use it. A failure here propagates: a stepped threshold means a wheelchair user cannot enter at all. Weather protection, automatic operation, level entry, and legibility together make a domestic entry that is welcoming rather than negotiated.\n\nLevel entry (E-06, zero step) is the foundational decision. Drainage and weather management are resolved without ramps where possible — falls in the slab, threshold sealing without raised lip, drainage grates flush. A 25 mm threshold defeats wheelchair entry as completely as a stair would. Where site levels prevent zero-step at grade, ramp gradient (E-03) ≤1:20 with landings, but level remains the goal.\n\nWeather protection (E-05, 3000 × 2000 mm covered area) supports the user during the moment of entry — fumbling for keys, shifting bags, transferring from chair to standing. The cover is functional, not stylistic.\n\nAutomatic sliding doors (E-11) eliminate the operation problem entirely. Where automation isn't feasible, lever or D-pull hardware (I-01) at compliant operating force (≤22 N). Door clear opening ≥850 mm.\n\nEntrance landing for power wheelchair (E-12, ≥1540 mm clear after door swing). Cognitive legibility (E-13) — single primary route from entry, visible reception or destination, landmarks beginning at the threshold (D-04, D-02).\n\nLighting transition (B-05, ≥5 m gradual) prevents the visual shock of bright-to-dark at threshold — important for VIS, DEM, and NEU populations whose visual adaptation is impaired. LRV contrast at frames, hardware, and threshold (C-04). Slip resistance (E-07, P5 wet) on entry mat and adjacent floor — wet weather makes this critical. Visual fire alarm coverage from entry (B-10).",

    sequence: [
      { step: 1, focus: "Confirm level entry (E-06)", why: "Site levels and drainage strategy resolve without threshold; structural decision before everything else" },
      { step: 2, focus: "Plan weather protection (E-05)", why: "3000 × 2000 mm covered approach; supports operation moment" },
      { step: 3, focus: "Specify automatic doors (E-11)", why: "Sensor-activated sliding; manual override per E-11 detail" },
      { step: 4, focus: "Verify entrance landing (E-12)", why: "≥1540 mm clear inside door swing for power wheelchair turn" },
      { step: 5, focus: "Plan lighting transition (B-05)", why: "≥5 m gradient from external to internal levels — eye adaptation" },
      { step: 6, focus: "Coordinate slip resistance (E-07) inside and outside", why: "P5 wet across the threshold; no abrupt PTV change" },
      { step: 7, focus: "Confirm cognitive legibility (E-13, D-02, D-04)", why: "Single primary route + first landmark visible from threshold" }
    ],

    interactions: [
      { specs: ["E-06", "E-05"], note: "Level entry depends on weather protection — without cover, drainage strategy must include thresholds that defeat E-06" },
      { specs: ["E-11", "I-01"], note: "Automatic doors and lever hardware are alternatives at the same threshold; specify which serves the primary entrance — automation preferred" },
      { specs: ["B-05", "C-04"], note: "Lighting transition and contrast: at the threshold, both eye adaptation and contrast visibility shift — landmark must be visible across the transition" },
      { specs: ["E-12", "E-08"], note: "Entrance landing and corridor width — landing must be ≥1540 mm clear, opening into corridor of ≥1200 mm" },
      { specs: ["E-13", "D-02"], note: "Entrance cognitive legibility and single primary route are the same provision viewed from inside vs at threshold" }
    ],

    clearances: [
      { what: "Threshold step", dim: "0 mm (level entry)", ref: "E-06; ramp ≤1:20 only where site forces" },
      { what: "Weather protection", dim: "≥3000 × 2000 mm covered", ref: "E-05" },
      { what: "Door clear opening", dim: "≥850 mm", ref: "E-11; 870 mm preferred for power wheelchair" },
      { what: "Entrance landing — internal", dim: "≥1540 mm clear after door swing", ref: "E-12" },
      { what: "Lighting transition zone", dim: "≥5 m gradient", ref: "B-05" },
      { what: "Slip resistance", dim: "P5 wet, P4 dry continuous across threshold", ref: "E-07" },
      { what: "Mat well — recessed", dim: "Flush with floor, not raised edge", ref: "Avoid trip hazard" },
      { what: "Hardware operating force", dim: "≤22 N", ref: "I-01 / H-01" }
    ],

    failures: [
      "25 mm threshold strip 'for weather' — defeats wheelchair entry",
      "Manual swinging door with closer at 30 N — fails OFS, PAIN, MOB users",
      "Mat with raised edge — trip hazard at the threshold",
      "Bright entry vestibule, dark corridor beyond — no transition zone, eye adaptation fails",
      "Glass door without manifestation — head-strike risk for low vision",
      "Step-down to side entrance bypassed by 'accessible' rear entrance — segregation",
      "No first landmark visible from threshold — wayfinding fails at arrival",
      "Slip rating drops at internal floor — wet feet, fall risk"
    ],

    diagram: {
      type: "plan",
      svg: `<svg viewBox="0 0 360 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Plan of accessible entry showing weather protection, level threshold, automatic door, entrance landing, and lighting transition">
        <rect x="20" y="20" width="320" height="180" fill="none" stroke="#1A1612" stroke-width="2"/>

        <rect x="20" y="20" width="120" height="180" fill="#1A1612" fill-opacity="0.03"/>
        <text x="30" y="40" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">EXTERIOR</text>

        <rect x="40" y="60" width="100" height="100" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.5" stroke-dasharray="4 3"/>
        <text x="50" y="115" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">cover</text>
        <text x="50" y="126" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">3000 × 2000</text>

        <line x1="140" y1="80" x2="140" y2="140" stroke="#1A1612" stroke-width="3"/>
        <text x="115" y="74" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">auto sliding</text>
        <text x="115" y="155" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">≥850 clear</text>

        <text x="135" y="180" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">▬▬▬ level — 0 step</text>

        <circle cx="180" cy="110" r="32" fill="none" stroke="#1A1612" stroke-width="0.5" stroke-dasharray="3 2"/>
        <text x="160" y="115" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">1540 turn</text>

        <rect x="240" y="80" width="14" height="40" fill="#1A1612" fill-opacity="0.4"/>
        <text x="222" y="76" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">landmark</text>
        <text x="225" y="138" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">D-04 visible</text>

        <line x1="155" y1="200" x2="320" y2="200" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="155" y1="197" x2="155" y2="203" stroke="#1A1612" stroke-width="0.6"/>
        <line x1="320" y1="197" x2="320" y2="203" stroke="#1A1612" stroke-width="0.6"/>
        <text x="190" y="215" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">≥5 m lighting transition</text>
      </svg>`
    }
  },

  // ═══════════════════════════════════════════════════════════════
  // R-LAU — LAUNDRY (compact)
  // ═══════════════════════════════════════════════════════════════
  "R-LAU": {
    synthesis: "Often the last room considered for accessibility, the laundry serves a daily task whose accessibility determines whether someone manages their own household independently. Reach ranges (H-01), control heights, and seated-task design (F-05) here decide whether a wheelchair user, a chronic-pain occupant, or an OFS user can do their own laundry.\n\nFront-loading machines on plinths bring the door opening into the seated reach envelope (door centre 700–900 mm AFF). Top-loaders are non-accessible by default. Knee clearance under the folding counter (G-05) supports seated folding work. Lever hardware (I-01) on every door and detergent storage. Anti-scald taps (I-03) at the laundry trough.\n\nFlicker-free LED (B-04). LRV contrast at the door, the machine controls, the trough rim. Slip resistance (E-07, P5 wet) at the trough approach.",

    sequence: [
      { step: 1, focus: "Specify front-loading machines on plinth", why: "Door centre 700–900 AFF brings load/unload into reach envelope" },
      { step: 2, focus: "Plan folding counter with knee clearance (G-05)", why: "Seated folding requires under-counter space" },
      { step: 3, focus: "Locate controls and GPOs (H-01)", why: "Machine controls and outlets within 400–1100 AFF" },
      { step: 4, focus: "Specify anti-scald trough mixer (I-03)", why: "Single-lever, 38°C-limited" }
    ],

    interactions: [
      { specs: ["F-05", "G-05"], note: "Seated-task design and adjustable counters coordinate at the folding zone — both depend on knee clearance" },
      { specs: ["I-01", "I-02"], note: "One-handed operation on doors and on machines — same upper-limb logic across the room" }
    ],

    clearances: [
      { what: "Floor area — minimum accessible", dim: "2400 × 2400 mm", ref: "Machines + folding + wheelchair turn" },
      { what: "Front-loader door centre", dim: "700–900 mm AFF", ref: "Achieved with plinth" },
      { what: "Folding counter knee clearance", dim: "≥800 W × 700 H × 480 D mm", ref: "G-05" },
      { what: "Trough rim height", dim: "800 mm AFF (knee clearance below)", ref: "Knee clearance preserved" },
      { what: "Wheelchair turn", dim: "≥1540 mm dia", ref: "Power wheelchair" }
    ],

    failures: [
      "Top-loader on floor — door inaccessible from seated position",
      "Folding counter without knee clearance — seated folding impossible",
      "Trough taps with rotary handles — fails I-01 operating force and one-handed criteria",
      "GPOs at 300 mm AFF — unreachable from wheelchair"
    ],

    diagram: null
  },

  // ═══════════════════════════════════════════════════════════════
  // NR-EDU — EDUCATION (priority: acoustic + sensory integration)
  // ═══════════════════════════════════════════════════════════════
  "NR-EDU": {
    synthesis: "Educational environments serve a population that includes many disabled and neurodivergent learners. Acoustic quality, sensory regulation, and spatial predictability are decisive for learning outcomes. The classroom that 'works' for neurotypical learners may be unusable for the 20–30% of learners with sensory, attention, hearing, or processing differences.\n\nAcoustics first. NRC ≥0.85 ceiling treatment (A-02) over ≥70% of ceiling area achieves RT60 ≤0.6 sec in occupied condition — the threshold below which speech intelligibility recovers and listening effort drops. HVAC noise (A-08, ≤NC-25) is the second baseline; loud HVAC defeats acoustic ceiling work. No sound masking (A-13). Where group communication occurs, room perimeter hearing loop (A-11) for hearing-aid users. The 'flutter echo' between parallel hard walls is eliminated through wall absorption (A-06) at reflection points.\n\nLighting: eliminate fluorescents (B-03), specify flicker-free LED (B-04, IEEE 1789-2015 'no-effect' across full dimming range). Individual dimming (B-06) per zone where teaching can occur in different modes. Circadian lighting (B-01) where extended occupation occurs.\n\nLow-stimulation enclosed spaces (D-05) — focus rooms, alcoves, library carrels — distributed throughout. Sensory rooms (A-16, ≥8 m²) on every floor or every 50 students. Sensory gradient (F-01) from arrival to occupation: corridors quieter than the entry, classrooms quieter than corridors, focus rooms quieter than classrooms.\n\nCognitive simplicity (D-02) — predictable building plan, single primary route, minimal decisions at arrival. Landmarks (D-04) at every junction. Pictogram signage (D-08). Corridor width (E-08, ≥1200 mm) for wheelchair use during peak transitions.\n\nAccessible toilets per code, but also: no-blind-corner geometry (D-07) on circulation, defensible seating (G-01) in waiting areas, three seat heights (G-02) at every gathering. Visual fire alarm (B-10) throughout, including bathrooms. Captioning (H-03) in assembly spaces.",

    sequence: [
      { step: 1, focus: "Plan acoustic baseline (A-02 ceiling, A-08 HVAC, A-13 no masking)", why: "Acoustic environment is the highest-leverage learning intervention; specify before finishes" },
      { step: 2, focus: "Eliminate fluorescents and verify flicker-free (B-03, B-04)", why: "Sub-perceptual flicker triggers sensory cascades; affects 10–15% of learners materially" },
      { step: 3, focus: "Distribute focus rooms and sensory rooms (D-05, A-16)", why: "Retreat at every scale — alcoves, focus rooms, dedicated sensory rooms" },
      { step: 4, focus: "Plan sensory gradient (F-01)", why: "High-stim arrival, calmer corridors, calmest learning spaces; spatial sequence in plan" },
      { step: 5, focus: "Verify cognitive legibility (D-02, D-04)", why: "Single primary route + landmarks at every junction; reduces arrival cognitive load" },
      { step: 6, focus: "Specify hearing loops in assembly (A-11)", why: "Classrooms and lecture halls — perimeter loops; counter loops at admin" },
      { step: 7, focus: "Coordinate visual alarm + captioning (B-10, H-03)", why: "Multi-modal communication for Deaf students throughout" }
    ],

    interactions: [
      { specs: ["A-02", "A-08", "A-13"], note: "Three acoustic baselines: ceiling absorption alone fails if HVAC is loud; both fail if masking is added — must specify together" },
      { specs: ["A-11", "A-02"], note: "Hearing loops require RT60 ≤0.6 sec; perimeter loop in reverberant room delivers garbled audio to hearing aids" },
      { specs: ["B-03", "B-04"], note: "Eliminating fluorescents is necessary; replacing with non-compliant LED is also a failure — both specs together" },
      { specs: ["A-16", "D-05"], note: "Sensory rooms and focus alcoves serve different needs along the same gradient; distributed network beats single 'special' room" },
      { specs: ["F-01", "A-04"], note: "Spatial sensory gradient and graduated acoustic zoning are the same principle in different dimensions" },
      { specs: ["D-02", "D-04"], note: "Single primary route and landmarks: route legibility depends on landmark visibility on approach" }
    ],

    clearances: [
      { what: "Classroom RT60 (occupied)", dim: "≤0.6 sec, 500–1000 Hz", ref: "A-02 / AS/NZS 2107" },
      { what: "Background noise (HVAC)", dim: "≤NC-25 (≈30–35 dB(A))", ref: "A-08" },
      { what: "Sensory room — minimum", dim: "≥8 m² (12–16 m² preferred)", ref: "A-16" },
      { what: "Focus room — typical", dim: "4–6 m²", ref: "D-05; smaller scale than sensory" },
      { what: "Corridor clear width — primary", dim: "≥1200 mm continuous, ≥1500 at doors", ref: "E-08" },
      { what: "Sensory rooms per floor", dim: "≥1 per floor or per 50 students", ref: "D-05 / A-16 distribution" },
      { what: "Hearing loop coverage", dim: "Whole-room perimeter in assembly", ref: "A-11; field-strength tested" },
      { what: "Visual alarm — coverage", dim: "Per AS 4428.16 Annex A by room dim", ref: "B-10" }
    ],

    failures: [
      "Hard plaster ceiling 'for projection clarity' — RT60 1.2 sec, speech unintelligible",
      "Fluorescents retained for 'cost reasons' — 15% of students materially affected",
      "Sensory room locked at admin desk — defeats availability when needed",
      "Single sensory room serving 800-student secondary — under-provision",
      "Hearing loop installed in reverberant room — garbled audio worse than no loop",
      "Sound masking added 'for privacy' — neurological populations excluded",
      "Identical wayfinding signage at every junction — landmarks fail",
      "Corridors at 1100 mm — peak transition wheelchair-pedestrian conflict"
    ],

    diagram: {
      type: "plan",
      svg: `<svg viewBox="0 0 400 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Schematic plan of education building showing sensory gradient from entry through corridors to classrooms with sensory room, focus alcoves, and assembly space">
        <rect x="20" y="20" width="360" height="200" fill="none" stroke="#1A1612" stroke-width="2"/>

        <rect x="20" y="20" width="80" height="200" fill="#1A1612" fill-opacity="0.12"/>
        <text x="30" y="40" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">ENTRY</text>
        <text x="30" y="52" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">high stim</text>

        <rect x="100" y="20" width="80" height="200" fill="#1A1612" fill-opacity="0.07"/>
        <text x="110" y="40" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">CORRIDOR</text>
        <text x="110" y="52" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">medium</text>

        <rect x="180" y="20" width="120" height="120" fill="#1A1612" fill-opacity="0.04"/>
        <text x="190" y="40" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">CLASSROOMS</text>
        <text x="190" y="52" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">RT60 ≤0.6</text>

        <rect x="180" y="140" width="120" height="80" fill="#1A1612" fill-opacity="0.04"/>
        <text x="190" y="160" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">ASSEMBLY</text>
        <text x="190" y="172" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">A-11 loop</text>

        <rect x="300" y="20" width="80" height="100" fill="#1A1612" fill-opacity="0.02" stroke="#1A1612" stroke-width="0.6"/>
        <text x="310" y="40" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">SENSORY</text>
        <text x="310" y="52" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">low stim</text>
        <text x="310" y="64" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">A-16</text>

        <rect x="300" y="120" width="40" height="40" fill="#1A1612" fill-opacity="0.02" stroke="#1A1612" stroke-width="0.4"/>
        <text x="305" y="135" font-family="JetBrains Mono, monospace" font-size="6" fill="#1A1612">focus</text>
        <text x="305" y="146" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">D-05</text>

        <line x1="20" y1="230" x2="380" y2="230" stroke="#1A1612" stroke-width="0.6" marker-end="url(#a)"/>
        <text x="160" y="225" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">→ sensory gradient (F-01) →</text>
      </svg>`
    }
  },

  // ═══════════════════════════════════════════════════════════════
  // NR-HLT — HEALTHCARE (priority: maximum complexity)
  // ═══════════════════════════════════════════════════════════════
  "NR-HLT": {
    synthesis: "Healthcare buildings serve people in their most vulnerable states. They are also disproportionately occupied by older, disabled, neurodivergent, and chronically ill people. Every accessibility consideration in this guidebook applies with greater weight in healthcare environments. The waiting room is a sensory environment for hours. The corridor is an emergency route. The bathroom is a clinical hand-over space. The bedroom is an extended-occupation environment for someone unable to leave.\n\nCirculation is the backbone. Loop floor plans (D-01) in dementia care eliminate dead-end distress. Toilet visibility (D-03) from primary occupied spaces supports continence. Corridor width (E-08) at hospital scale typically ≥1800 mm to accommodate beds, trolleys, two wheelchair users, and staff simultaneously. Rest seating (E-10) at ≤20 m intervals — patients tire faster than the building.\n\nAcoustic strategy is layered. Buffer zones (A-01) between sensitive occupied spaces (consult rooms, bedrooms) and noise sources (corridors, plant, kitchens). Ceiling treatment (A-02, NRC ≥0.85) throughout. HVAC noise control (A-08, ≤NC-25). Vibration isolation (A-09) — plant rooms isolated from inpatient floors. Counter hearing loop (A-10) at every reception, admissions, pharmacy, and ward station.\n\nWaiting areas need defensible seating (G-01) for trauma-informed care, three seat heights (G-02), and rest at intervals. Sensory gradient (F-01) from entry through admission to treatment — most healthcare arrival is high-stim with loud announcements, bright fluorescent (often), busy visual environment; the gradient inward should reduce all of this.\n\nSensory rooms (A-16) on every ward — for paediatrics, mental health, oncology, dementia. Olfactory control (F-02, fragrance-free zones) for chemotherapy and chronic illness populations. Air quality (F-04, MERV 13+ minimum, MERV 16 in immunocompromised areas).\n\nLighting must support both circadian regulation (B-01, ≥150 EML daytime) and clinical task lighting. No fluorescents (B-03). Flicker-free (B-04) throughout. Warm CCT evening in patient rooms (B-11).\n\nWayfinding is a clinical safety issue. Loop plans, single primary route from arrival, landmarks at every decision point, pictogram signage, no blind corners. Visual fire alarm throughout including bathrooms (B-10). Captioning in assembly and information delivery (H-03).",

    sequence: [
      { step: 1, focus: "Plan circulation (D-01 loops, D-02 single primary route, E-08 width)", why: "Building organization sets the limits on every other accessibility provision" },
      { step: 2, focus: "Establish acoustic zones (A-01 buffers, A-02 ceiling, A-08 HVAC)", why: "Acoustic baseline for clinical and inpatient environments" },
      { step: 3, focus: "Locate sensory rooms (A-16) and refuge alcoves (D-05) on every ward/floor", why: "Distributed network — accessible from every primary occupied space" },
      { step: 4, focus: "Specify hearing loops (A-10) at every counter and (A-11) in assembly", why: "Reception, admissions, pharmacy, ward stations — all counter loops" },
      { step: 5, focus: "Design waiting areas (G-01 defensible, G-02 three heights, E-10 rest)", why: "Long sustained occupation; one-size seating fails" },
      { step: 6, focus: "Plan sensory gradient (F-01) from entry to treatment", why: "Decompression sequence built into spatial organisation" },
      { step: 7, focus: "Specify olfactory + air quality (F-02, F-04)", why: "Fragrance-free policy + MERV 13–16 filtration; chemo-sensitive population" },
      { step: 8, focus: "Coordinate circadian + clinical lighting (B-01, B-03, B-04, B-11)", why: "Two requirements (rest + task) on the same tunable LED system" }
    ],

    interactions: [
      { specs: ["D-01", "D-03", "D-04"], note: "Loop plan, toilet visibility, and landmarks all serve dementia wayfinding — the loop fails without landmarks; toilet visibility fails without simple plan" },
      { specs: ["A-01", "A-14", "A-08"], note: "Buffers, partitions, HVAC quiet — three transmission paths addressed together; missing one undermines isolation" },
      { specs: ["A-16", "D-05", "F-01"], note: "Sensory rooms, refuge alcoves, and sensory gradient are a coordinated network — single sensory room without alcoves and gradient is under-provisioned" },
      { specs: ["A-10", "A-11"], note: "Counter loops at one-to-one exchange, perimeter loops in group settings — both required across the healthcare estate" },
      { specs: ["G-01", "G-02", "E-10"], note: "Defensible seating, three heights, and rest at intervals coordinate in waiting areas — all three needed for sustained occupation" },
      { specs: ["B-01", "B-11"], note: "Daytime circadian and evening warm CCT — same tunable system, different time profiles" },
      { specs: ["B-10", "H-03"], note: "Visual alarm and captioning extend the multi-modal principle from emergency to information communication" },
      { specs: ["F-02", "F-04"], note: "Fragrance-free policy and MERV filtration — policy fails without ventilation strategy" }
    ],

    clearances: [
      { what: "Corridor — primary clinical", dim: "≥1800 mm clear", ref: "Beds, trolleys, two w/c passing simultaneously" },
      { what: "Corridor — secondary", dim: "≥1500 mm clear", ref: "Single bed + pedestrian" },
      { what: "Patient bedroom (single accessible)", dim: "≥3500 × 4500 mm", ref: "Bed, transfer space both sides, w/c turn" },
      { what: "Consult room", dim: "≥3000 × 3500 mm", dim_note: "Examination + w/c access + clinician + companion", ref: "AS 1428 dimensions" },
      { what: "Sensory room (per ward/floor)", dim: "≥8 m² (12 m² preferred)", ref: "A-16" },
      { what: "Waiting area — three seat heights", dim: "380 / 450 / 520 mm AFF distributed", ref: "G-02" },
      { what: "Buffer zone width to sensitive space", dim: "≥600 mm physical or STC ≥45", ref: "A-01" },
      { what: "Counter hearing loop coverage", dim: "1.2 m radius from counter", ref: "A-10 / IEC 60118-4" },
      { what: "Air filtration — general", dim: "MERV 13 minimum", ref: "F-04; MERV 16 in immunocompromised" },
      { what: "RT60 — clinical", dim: "≤0.6 sec, 500–1000 Hz", ref: "A-02 / AS/NZS 2107" }
    ],

    failures: [
      "Dead-end corridor in dementia care unit — daily distress and behavioural escalation",
      "Bedroom adjacent to lift shaft on inpatient floor — A-14 STC 35 instead of ≥50, sleep disruption",
      "Single sensory room for 200-bed facility — under-provision; locked at admin",
      "Counter without hearing loop at reception — every Deaf patient excluded from intake",
      "Fluorescent overhead in waiting room — sensory cascades for NDV/NEU/PAIN populations",
      "Single seat height in waiting — excludes elderly, pain, and orthostatic populations",
      "Fragrance from cleaning products in chemotherapy area — MCAS triggers, excluded patients",
      "Visual alarm omitted from bathrooms — Deaf patient in shower has no alert",
      "Wayfinding entirely text-based — fails reading-impaired and dementia populations"
    ],

    diagram: {
      type: "plan",
      svg: `<svg viewBox="0 0 420 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Schematic plan of healthcare ward showing loop circulation, distributed sensory rooms, central station, patient rooms, and shared facilities">
        <rect x="20" y="20" width="380" height="240" fill="none" stroke="#1A1612" stroke-width="2"/>

        <path d="M 60 60 L 360 60 L 360 220 L 60 220 Z" fill="none" stroke="#1A1612" stroke-width="1" stroke-dasharray="4 3"/>
        <text x="180" y="56" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">loop circulation — D-01</text>

        <rect x="80" y="80" width="60" height="50" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.5"/>
        <text x="92" y="100" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">PATIENT</text>
        <text x="92" y="111" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">ROOM</text>

        <rect x="160" y="80" width="60" height="50" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.5"/>
        <text x="172" y="100" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">PATIENT</text>

        <rect x="240" y="80" width="60" height="50" fill="#1A1612" fill-opacity="0.06" stroke="#1A1612" stroke-width="0.5"/>
        <text x="252" y="100" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">PATIENT</text>

        <rect x="320" y="80" width="40" height="50" fill="#1A1612" fill-opacity="0.02" stroke="#1A1612" stroke-width="0.6"/>
        <text x="328" y="100" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">SENS</text>
        <text x="328" y="112" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">A-16</text>

        <rect x="160" y="150" width="100" height="50" fill="#1A1612" fill-opacity="0.12" stroke="#1A1612" stroke-width="0.6"/>
        <text x="180" y="172" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">STATION</text>
        <text x="170" y="184" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">A-10 loop · A-08 quiet</text>

        <rect x="80" y="150" width="60" height="50" fill="#1A1612" fill-opacity="0.04" stroke="#1A1612" stroke-width="0.5"/>
        <text x="92" y="170" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">WAITING</text>
        <text x="86" y="183" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">G-01 · G-02</text>

        <rect x="280" y="150" width="80" height="50" fill="#1A1612" fill-opacity="0.04" stroke="#1A1612" stroke-width="0.5"/>
        <text x="296" y="172" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">SHARED BATH</text>
        <text x="296" y="184" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">G-04 · D-03</text>

        <text x="30" y="40" font-family="JetBrains Mono, monospace" font-size="8" fill="#1A1612">WARD</text>
        <text x="30" y="265" font-family="JetBrains Mono, monospace" font-size="7" fill="#6B5F50">corridor ≥1800 — beds, trolleys, w/c</text>
      </svg>`
    }
  },

  // ═══════════════════════════════════════════════════════════════
  // NR-WRK — WORKPLACE (priority: sustained occupation)
  // ═══════════════════════════════════════════════════════════════
  "NR-WRK": {
    synthesis: "Workplaces have the longest sustained occupation per day of any building type. Sensory regulation, individual control, and refuge provision determine whether disabled and neurodivergent employees can sustain employment. The open-plan office that 'works' for neurotypical staff may be unworkable for the 20–30% with sensory, attention, or stress-related differences.\n\nAcoustic baseline: NRC ≥0.85 ceiling (A-02), HVAC ≤NC-30 (A-08 — slightly relaxed from healthcare), no sound masking (A-13), buffer zones (A-01) between focus and collaboration zones. Open-plan office without these provisions is sensory exclusion at scale.\n\nLighting: eliminate fluorescents (B-03), flicker-free LED (B-04), individual dimming where possible (B-06). Circadian lighting (B-01, ≥150 EML) supports sustained alertness without depending on caffeine and willpower alone. Where individual control isn't possible at desks, zoned control with override.\n\nLow-stimulation focus rooms (D-05) and phone booths distributed throughout — quiet for solo focus, not just conference. Sensory rooms (A-16) on every floor — for migraine recovery, sensory regulation, breastfeeding, prayer.\n\nSeated-task design (F-05) at every workstation. Adjustable-height desks (G-05, sit-stand). Defensible seating (G-01) in shared spaces — at least one back-to-wall option in every gathering area. Three seat heights at every meeting room (G-02).\n\nIndividual environmental control (H-02) for thermostat and lighting — central control assumes everyone shares one comfort range; they don't. Olfactory control (F-02, fragrance-free policy + ventilation) and air quality (F-04, MERV 13+) for chemically sensitive employees. Visual alarm throughout (B-10), captioning in meeting rooms (H-03), counter hearing loop at reception (A-10).",

    sequence: [
      { step: 1, focus: "Plan acoustic zoning (A-01, A-02, A-08, A-13)", why: "Open-plan acoustic strategy — buffer zones between focus and collaboration; no masking" },
      { step: 2, focus: "Distribute focus rooms and sensory room (D-05, A-16)", why: "Multiple per floor; not just 'phone booths' — quiet rooms for solo focus" },
      { step: 3, focus: "Specify lighting (B-01 circadian, B-03 no fluorescents, B-04 flicker-free)", why: "Sustained alertness + sensory regulation; same tunable LED system" },
      { step: 4, focus: "Plan adjustable workstations (G-05, F-05)", why: "Sit-stand desks throughout; not just for 'requested accommodations'" },
      { step: 5, focus: "Distribute defensible seating in shared spaces (G-01)", why: "At least one back-to-wall option in every gathering" },
      { step: 6, focus: "Specify individual environmental control (H-02)", why: "Per-zone thermostat and lighting; central control fails sensitive populations" }
    ],

    interactions: [
      { specs: ["A-02", "A-13", "A-01"], note: "Open-plan acoustics: ceiling absorption + no masking + zonal buffers — all three together; any one omitted defeats the others" },
      { specs: ["D-05", "A-16"], note: "Focus rooms (small, distributed) and sensory rooms (larger, dedicated) serve different use cases; both required in workplaces with extended occupation" },
      { specs: ["G-01", "D-07"], note: "Defensible seating and no-blind-corners — open-plan layouts without these are stress environments for trauma-informed populations" },
      { specs: ["B-01", "H-02"], note: "Circadian lighting and individual control — sounds contradictory but coordinated: zone-level circadian default with individual override" },
      { specs: ["F-05", "G-05", "H-01"], note: "Seated tasks, adjustable counters, reach envelope — same logic across workstation, kitchenette, and meeting room" }
    ],

    clearances: [
      { what: "Workstation footprint (accessible)", dim: "≥1800 × 1500 mm", ref: "Desk + wheelchair turn + chair area" },
      { what: "Adjustable desk range", dim: "650–1200 mm AFF", ref: "G-05; sit-stand standard" },
      { what: "Focus room — typical", dim: "4–6 m²", ref: "D-05; one per 25–50 staff" },
      { what: "Sensory room", dim: "≥8 m² per floor", ref: "A-16" },
      { what: "Open-plan acoustic zoning", dim: "Buffer ≥600 mm or STC 45 partition", ref: "A-01" },
      { what: "RT60 — open plan", dim: "≤0.4 sec, 500–1000 Hz", ref: "A-02 occupied" },
      { what: "HVAC noise — open office", dim: "≤NC-30 (slightly relaxed from clinical)", ref: "A-08" },
      { what: "Meeting room — three seat heights", dim: "380/450/520 mm distributed", ref: "G-02" },
      { what: "Hearing loop at reception", dim: "1.2 m radius from counter", ref: "A-10" }
    ],

    failures: [
      "Open-plan with hard ceiling and floor — RT60 1.0 sec, focus impossible for any population",
      "Sound masking added 'for privacy' — neurological and neurodivergent staff excluded from focus",
      "Fluorescent overhead retained — 15% of staff materially affected, often without diagnosis",
      "Single 'wellness room' for 200 staff — under-provisioned, occupied permanently by one user",
      "Fixed-height desks throughout — wheelchair users, OFS, and pain populations unable to work",
      "Central HVAC with one thermostat per floor — comfort-range mismatch for sensitive populations",
      "No defensible seating in collaboration zones — trauma-informed staff cannot relax",
      "Reception without hearing loop — Deaf visitors and staff excluded from arrival"
    ],

    diagram: {
      type: "plan",
      svg: `<svg viewBox="0 0 420 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Schematic workplace plan showing open-plan zone, focus rooms, sensory room, meeting room, and reception with hearing loop">
        <rect x="20" y="20" width="380" height="200" fill="none" stroke="#1A1612" stroke-width="2"/>

        <rect x="40" y="60" width="160" height="140" fill="#1A1612" fill-opacity="0.04" stroke="#1A1612" stroke-width="0.5"/>
        <text x="60" y="85" font-family="JetBrains Mono, monospace" font-size="9" fill="#1A1612">OPEN PLAN</text>
        <text x="60" y="98" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">A-02 · A-13 · G-05</text>

        <rect x="60" y="110" width="20" height="14" fill="#1A1612" fill-opacity="0.18"/>
        <rect x="90" y="110" width="20" height="14" fill="#1A1612" fill-opacity="0.18"/>
        <rect x="120" y="110" width="20" height="14" fill="#1A1612" fill-opacity="0.18"/>
        <rect x="60" y="140" width="20" height="14" fill="#1A1612" fill-opacity="0.18"/>
        <rect x="90" y="140" width="20" height="14" fill="#1A1612" fill-opacity="0.18"/>
        <rect x="120" y="140" width="20" height="14" fill="#1A1612" fill-opacity="0.18"/>

        <rect x="220" y="60" width="60" height="50" fill="#1A1612" fill-opacity="0.02" stroke="#1A1612" stroke-width="0.6"/>
        <text x="232" y="80" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">FOCUS</text>
        <text x="232" y="92" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">D-05</text>

        <rect x="290" y="60" width="60" height="50" fill="#1A1612" fill-opacity="0.02" stroke="#1A1612" stroke-width="0.6"/>
        <text x="302" y="80" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">FOCUS</text>

        <rect x="220" y="130" width="60" height="50" fill="#1A1612" fill-opacity="0.02" stroke="#1A1612" stroke-width="0.6"/>
        <text x="232" y="150" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">SENSORY</text>
        <text x="232" y="162" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">A-16</text>

        <rect x="290" y="130" width="60" height="50" fill="#1A1612" fill-opacity="0.04" stroke="#1A1612" stroke-width="0.5"/>
        <text x="298" y="150" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">MEETING</text>
        <text x="298" y="162" font-family="JetBrains Mono, monospace" font-size="6" fill="#6B5F50">A-11 · G-02</text>

        <rect x="40" y="20" width="80" height="30" fill="#1A1612" fill-opacity="0.12" stroke="#1A1612" stroke-width="0.5"/>
        <text x="48" y="40" font-family="JetBrains Mono, monospace" font-size="7" fill="#1A1612">RECEPTION · A-10</text>
      </svg>`
    }
  },

  // ═══════════════════════════════════════════════════════════════
  // NR-RET — RETAIL (compact)
  // ═══════════════════════════════════════════════════════════════
  "NR-RET": {
    synthesis: "Retail accessibility determines who can participate in everyday economic life. Counter heights, hearing loops, automatic doors, and circulation width are the basics; sensory environment determines whether sensitive populations can shop. Many retail environments fail at all of these simultaneously — bright fluorescent lighting, loud music, narrow aisles, single counter height, no hearing loop, manual swing doors with closers.\n\nReception/service counter at 760–860 mm AFF (G-06) with hearing loop (A-10). Aisle width ≥1200 mm (E-08) — typical retail aisles at 900 mm exclude wheelchair users entirely. Automatic sliding doors at primary entrance (E-11). Lifts to all floors (E-01). Visual alarm (B-10) throughout. LRV contrast at controls and signage (C-04). Pictogram signage (D-08).\n\nLighting: no fluorescents (B-03), flicker-free LED (B-04). Acoustic ceiling treatment (A-02) — retail with hard ceilings is acoustically punishing. Sensory-friendly hour provisions are operational, not architectural, but the architecture must support them — dimmable lighting, ability to mute music.",

    sequence: [
      { step: 1, focus: "Reception counter height + hearing loop (G-06, A-10)", why: "Service counter is the first failure point" },
      { step: 2, focus: "Aisle width and circulation (E-08)", why: "≥1200 mm primary; ≥1500 at decision points" },
      { step: 3, focus: "Automatic doors and level entry (E-11, E-06)", why: "Threshold-free arrival" },
      { step: 4, focus: "Eliminate fluorescents (B-03, B-04)", why: "Sensory environment for shopping" }
    ],

    interactions: [
      { specs: ["G-06", "A-10"], note: "Counter height and hearing loop coordinate at every service point — Deaf customer cannot transact without loop" },
      { specs: ["E-08", "E-11"], note: "Aisle width and door automation — both required for independent navigation" }
    ],

    clearances: [
      { what: "Service counter height", dim: "760–860 mm AFF", ref: "G-06" },
      { what: "Aisle width — primary", dim: "≥1200 mm", ref: "E-08" },
      { what: "Aisle width — secondary", dim: "≥1000 mm acceptable", ref: "Local widening at decision points" },
      { what: "Hearing loop coverage", dim: "1.2 m radius from counter", ref: "A-10" },
      { what: "Door clear opening", dim: "≥850 mm; auto sliding preferred", ref: "E-11" }
    ],

    failures: [
      "Counter at 1100 mm AFF — fixed-height standard retail counter, inaccessible to seated customers",
      "No hearing loop at any counter — Deaf customer cannot transact",
      "Aisles at 800 mm — wheelchair users cannot enter",
      "Fluorescent overhead + bright music — sensory exclusion",
      "Manual swing doors with closers — fails OFS, PAIN, MOB users"
    ],

    diagram: null
  },

  // ═══════════════════════════════════════════════════════════════
  // NR-CUL — CULTURAL (compact)
  // ═══════════════════════════════════════════════════════════════
  "NR-CUL": {
    synthesis: "Cultural institutions are frequently late adopters of accessibility provision but disproportionately host Deaf, blind, and disabled audiences. Hearing loops, captioning, and tactile wayfinding are foundational. Heritage buildings present specific challenges where structural changes are constrained — but accessibility cannot be deferred indefinitely behind 'heritage'.\n\nAcoustic ceiling treatment in galleries and assembly spaces (A-02). Room perimeter hearing loops in theatres, lecture halls, and tour-meeting points (A-11). Counter loops at admissions, shop, café (A-10). Visual paging and captioning (H-03) for performances and information. Tactile wayfinding (E-09) at level changes. Three seat heights in seating areas (G-02), defensible seating in cafés and rest spaces (G-01). Sensory room (A-16) for sensory-friendly visit planning.\n\nLandmarks at every junction (D-04) — cultural buildings often have complex plans where wayfinding is otherwise punishing. Visual fire alarm (B-10) throughout including theatres.",

    sequence: [
      { step: 1, focus: "Plan accessible routes through galleries (E-08, D-04)", why: "Width + landmarks; cultural buildings often have complex plans" },
      { step: 2, focus: "Specify hearing loops in assembly (A-11)", why: "Theatres, lecture halls, tour points" },
      { step: 3, focus: "Provide captioning and visual paging (H-03)", why: "Performances and information delivery" },
      { step: 4, focus: "Tactile wayfinding (E-09)", why: "Level changes, stair tops" }
    ],

    interactions: [
      { specs: ["A-11", "H-03"], note: "Hearing loops serve hearing-aid users; captioning serves Deaf users — both required, neither sufficient alone" }
    ],

    clearances: [
      { what: "Gallery circulation", dim: "≥1500 mm clear", ref: "Allows wheelchair plus standing visitor" },
      { what: "Theatre — accessible seating", dim: "Distributed, multiple heights", ref: "Not segregated 'wheelchair section' alone" },
      { what: "Hearing loop coverage", dim: "Full audience area", ref: "A-11; field-strength tested" }
    ],

    failures: [
      "Hearing loop installed 'in the front rows only' — Deaf audience excluded from rear seats",
      "Captioning deferred 'until requested' — implicit segregation",
      "Heritage buildings cited as exemption from any accessibility provision",
      "Tactile indicators omitted at gallery level changes — fall hazard for blind visitors"
    ],

    diagram: null
  },

  // ═══════════════════════════════════════════════════════════════
  // NR-HOS — HOSPITALITY (compact)
  // ═══════════════════════════════════════════════════════════════
  "NR-HOS": {
    synthesis: "Hospitality is where accessibility provision is often optional, segregated, or absent. 'Accessible rooms' as separate category from standard rooms is itself a design failure. Universal design here means the bathroom works for all guests, circulation accommodates everyone, and the 'accessible room' is just a room with adjustable provisions.\n\nLevel entry (E-06), lifts to all floors (E-01), accessible bathrooms in every guest room (G-04 — wet-room configuration), three seat heights in restaurant and lobby (G-02), individual environmental control in rooms (H-02), warm CCT evening (B-11) for sleep regulation, flicker-free LED (B-04), visual fire alarm + pillow shaker in every room (B-10), counter hearing loop at reception (A-10).",

    sequence: [
      { step: 1, focus: "Wet-room bathroom in every guest room (G-04)", why: "Standard provision, not 'accessible room' segregation" },
      { step: 2, focus: "Plan circulation (E-01 lift, E-08 corridor, E-11 doors)", why: "Threshold-free throughout" },
      { step: 3, focus: "Specify VAD + pillow shaker every room (B-10)", why: "Deaf guest provision, every room not 'on request'" },
      { step: 4, focus: "Reception hearing loop (A-10)", why: "Check-in is the first failure point" }
    ],

    interactions: [
      { specs: ["G-04", "B-12"], note: "Wet-room bathroom and overnight pathway lighting — guest in unfamiliar room at night needs both" }
    ],

    clearances: [
      { what: "Guest room — accessible standard", dim: "Full G-04 bathroom; transfer space both sides of bed", ref: "Not segregated category" },
      { what: "Restaurant — three seat heights", dim: "380/450/520 mm distributed", ref: "G-02" }
    ],

    failures: [
      "Two 'accessible rooms' per 200-room hotel — segregation, often unavailable when needed",
      "Bathroom with grab rails and shower seat as 'accessible' — but with raised threshold and inward-swing door",
      "VAD only in 'accessible rooms' — Deaf guest in standard room has no fire alarm"
    ],

    diagram: null
  },

  // ═══════════════════════════════════════════════════════════════
  // NR-TRP — TRANSPORT (compact)
  // ═══════════════════════════════════════════════════════════════
  "NR-TRP": {
    synthesis: "Transport infrastructure is where failure to provide tactile indicators, hearing loops, and visual paging directly excludes from movement. The platform edge without tactile warning is a fall hazard. The platform without visual paging is inaccessible to Deaf travellers. The station without hearing loop at counters and ticket machines is inaccessible to hearing-aid users.\n\nTactile walking surface indicators (E-09, ISO 23599) at all platform edges and stair tops. Counter hearing loops (A-10) at every ticket office, information desk, and customer service point. Visual paging and real-time captioning (H-03) for announcements. Visual fire alarm (B-10) throughout. Lifts to every level (E-01). Level entry to vehicles where infrastructure permits. Accessible toilets to G-04. Landmarks at every decision point (D-04) — stations are notorious for cognitive complexity. Rest seating at platforms and concourses (E-10).",

    sequence: [
      { step: 1, focus: "Tactile indicators at all platform edges + stair tops (E-09)", why: "Foundational safety provision" },
      { step: 2, focus: "Hearing loops at every counter and ticket machine (A-10)", why: "Ticket purchase failure point" },
      { step: 3, focus: "Visual paging + captioning (H-03)", why: "Announcement accessibility" },
      { step: 4, focus: "Lifts and level boarding (E-01)", why: "Step-free vertical and lateral access" }
    ],

    interactions: [
      { specs: ["E-09", "C-04"], note: "Tactile and visual contrast at platform edges work together — both needed for low-vision plus tactile-only users" },
      { specs: ["A-10", "H-03"], note: "Counter loops and captioning — different communication contexts, both required" }
    ],

    clearances: [
      { what: "Tactile warning at platform edge", dim: "Per ISO 23599 truncated dome pattern", ref: "E-09" },
      { what: "Tactile width", dim: "≥600 mm parallel to edge", ref: "E-09" },
      { what: "Counter hearing loop coverage", dim: "1.2 m radius", ref: "A-10" },
      { what: "Concourse rest seating", dim: "≤30 m intervals (transit relaxed from ≤20)", ref: "E-10" }
    ],

    failures: [
      "Platform edge without tactile warning — fall hazard for blind travellers",
      "Visual paging only on 'accessibility' platforms — Deaf travellers excluded elsewhere",
      "Ticket machine without hearing loop — Deaf customer cannot use",
      "Stairs without tactile warning at top — fall hazard"
    ],

    diagram: null
  }
};

/* ════════════════════════════════════════════════════════════════════
   HELPERS
   ════════════════════════════════════════════════════════════════════ */

const totalItems = ITEMS.length;
const getPop = (c) => POPS.find(p => p.code === c);
const getTopic = (id) => TOPICS.find(t => t.id === id);
const getCategory = (l) => CATEGORIES.find(c => c.letter === l);
const getItem = (cd) => ITEMS.find(i => i.cd === cd);

const ALL_ROOMS = [
  ...BUILDINGS.res.rooms.map(r => ({ ...r, building: "res" })),
  ...BUILDINGS.nres.rooms.map(r => ({ ...r, building: "nres" }))
];
const getRoom = (code) => {
  const base = ALL_ROOMS.find(r => r.code === code);
  if (!base) return null;
  const synthesis = ROOMS_SYNTHESIS[code];
  return synthesis ? { ...base, ...synthesis } : base;
};

const itemsForRoom = (code) => ITEMS.filter(i => i.rooms.includes(code) || i.rooms.includes("ALL"));
const itemsForPopulation = (code) => ITEMS.filter(i => i.p.includes(code) || i.p.includes("ALL"));
const headingFor = (item, mode) => mode === "question" && item.q ? item.q : item.t;

/* ════════════════════════════════════════════════════════════════════
   BASE COMPONENTS
   ════════════════════════════════════════════════════════════════════ */

// Click-citation popover. Opens beside cite, dismisses on outside-click or Escape, restores focus.
function Cite({ code, onJump }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);
  const popRef = useRef(null);

  useEffect(() => {
    if (!open) return;
    const onDown = (e) => {
      if (ref.current && !ref.current.contains(e.target) && popRef.current && !popRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    const onKey = (e) => {
      if (e.key === "Escape") {
        setOpen(false);
        ref.current?.focus();
      }
    };
    document.addEventListener("mousedown", onDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  const pop = getPop(code);
  const isAll = code === "ALL";

  return (
    <span className="cite-wrap">
      <button
        ref={ref}
        type="button"
        onClick={() => setOpen(o => !o)}
        className={"cite" + (isAll ? " cite-all" : "") + (open ? " cite-open" : "")}
        aria-expanded={open}
        aria-haspopup="dialog"
        aria-label={isAll ? "Universal — relevant to all populations" : (pop ? `${pop.label}: tap for details` : code)}>
        {code}
      </button>
      {open && (
        <div ref={popRef} role="dialog" aria-label={isAll ? "Universal" : pop?.label} className="popover">
          <div className="popover-arrow" aria-hidden="true" />
          {isAll ? (
            <>
              <p className="popover-code">ALL</p>
              <p className="popover-name">Universal</p>
              <p className="popover-desc">A specification that applies regardless of population — typically Tier 0 code-compliance items, or universal-design provisions that benefit everyone.</p>
            </>
          ) : pop ? (
            <>
              <p className="popover-code">{pop.code}</p>
              <p className="popover-name">{pop.label}</p>
              <p className="popover-desc">{pop.desc}</p>
              <p className="popover-meta">{itemsForPopulation(pop.code).length} relevant specifications</p>
              {onJump && (
                <button onClick={() => { setOpen(false); onJump(pop.code); }} className="popover-jump">
                  View all entries for {pop.code} →
                </button>
              )}
            </>
          ) : (
            <p className="popover-name">{code}</p>
          )}
        </div>
      )}
    </span>
  );
}

function TierTag({ tier }) {
  const t = TIERS.find(x => x.v === tier);
  if (!t) return null;
  const marks = ["━━━", "━━", "━"][tier];
  return (
    <span className="tiertag" aria-label={`Tier ${tier}: ${t.n}`}>
      <span className="tiertag-bar" aria-hidden="true">{marks}</span>
      <span className="tiertag-num">T{tier}</span>
    </span>
  );
}

function CrumbBar({ trail }) {
  return (
    <nav className="crumb" aria-label="Breadcrumb">
      {trail.map((c, i) => {
        const isLast = i === trail.length - 1;
        return (
          <span key={i} className="crumb-item">
            {!isLast && c.go ? (
              <button className="crumb-link" onClick={c.go}>{c.label}</button>
            ) : (
              <span className={isLast ? "crumb-current" : "crumb-link-static"} aria-current={isLast ? "page" : undefined}>{c.label}</span>
            )}
            {!isLast && <span className="crumb-sep" aria-hidden="true"> / </span>}
          </span>
        );
      })}
    </nav>
  );
}

function Accordion({ title, count, defaultOpen = false, children }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <section className="acc">
      <button className="acc-head" onClick={() => setOpen(o => !o)} aria-expanded={open}>
        <span className="acc-title">{title}</span>
        {count !== undefined && <span className="acc-count">{count}</span>}
        <span className="acc-tog" aria-hidden="true">{open ? "−" : "+"}</span>
      </button>
      {open && <div className="acc-body">{children}</div>}
    </section>
  );
}

function ToggleBar({ mode, setMode }) {
  return (
    <div className="toggle-bar" role="radiogroup" aria-label="Reading mode">
      <button
        role="radio"
        aria-checked={mode === "spec"}
        onClick={() => setMode("spec")}
        className={"toggle-bar-btn" + (mode === "spec" ? " toggle-bar-btn-on" : "")}>
        Specifications
      </button>
      <button
        role="radio"
        aria-checked={mode === "question"}
        onClick={() => setMode("question")}
        className={"toggle-bar-btn" + (mode === "question" ? " toggle-bar-btn-on" : "")}>
        Questions
      </button>
    </div>
  );
}

/* ════════════════════════════════════════════════════════════════════
   ARCHITECT-DATA COMPONENTS
   ════════════════════════════════════════════════════════════════════ */

function DimTable({ rows }) {
  if (!rows || rows.length === 0) return null;
  return (
    <div className="adt-wrap" role="region" aria-label="Dimensions table">
      <table className="adt">
        <thead>
          <tr>
            <th scope="col">Dimension</th>
            <th scope="col">Value</th>
            <th scope="col">Unit</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>
              <td className="adt-dim">
                {r.dim}
                {r.note && <span className="adt-note">{r.note}</span>}
              </td>
              <td className="adt-val">{r.value}</td>
              <td className="adt-unit">{r.unit}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function PerfTable({ rows }) {
  if (!rows || rows.length === 0) return null;
  return (
    <div className="adt-wrap" role="region" aria-label="Performance criteria table">
      <table className="adt">
        <thead>
          <tr>
            <th scope="col">Metric</th>
            <th scope="col">Target</th>
            <th scope="col">Measurement method</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>
              <td className="adt-dim">{r.metric}</td>
              <td className="adt-val">{r.target}</td>
              <td className="adt-meas">{r.measure}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function CodesByJurisdiction({ rows }) {
  if (!rows || rows.length === 0) return null;
  // Group by jurisdiction
  const byJur = {};
  rows.forEach(r => {
    const j = r.jurisdiction || "OTHER";
    (byJur[j] = byJur[j] || []).push(r);
  });
  const jurOrder = ["AU", "AU/NZ", "US", "UK", "EU", "INTL", "OTHER"];
  const sorted = jurOrder.filter(j => byJur[j]);
  return (
    <div className="codes-list">
      {sorted.map(j => (
        <details key={j} className="codes-jur" open={j === "AU" || j === "AU/NZ"}>
          <summary className="codes-jur-head">
            <span className="codes-jur-label">{j}</span>
            <span className="codes-jur-count">{byJur[j].length}</span>
            <span className="codes-jur-tog" aria-hidden="true">+</span>
          </summary>
          <ul className="codes-jur-list">
            {byJur[j].map((r, i) => (
              <li key={i} className="codes-jur-row">
                <span className="codes-ref">{r.ref}</span>
                <span className="codes-clause">{r.clause}</span>
              </li>
            ))}
          </ul>
        </details>
      ))}
    </div>
  );
}

function ProductsList({ items }) {
  if (!items || items.length === 0) return null;
  return (
    <ul className="prod-list">
      {items.map((p, i) => (
        <li key={i} className="prod-li">{p}</li>
      ))}
    </ul>
  );
}

function ScheduleBlock({ text }) {
  const [copied, setCopied] = useState(false);
  if (!text) return null;
  const onCopy = () => {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => {
        setCopied(true);
        setTimeout(() => setCopied(false), 1800);
      }).catch(() => {});
    }
  };
  return (
    <div className="sched-block">
      <button onClick={onCopy} className="sched-copy" aria-label="Copy schedule text to clipboard">
        {copied ? "Copied" : "Copy"}
      </button>
      <p className="sched-text">{text}</p>
    </div>
  );
}

function DetailAccordion({ groups }) {
  if (!groups || groups.length === 0) return null;
  return (
    <div className="det-list">
      {groups.map((g, i) => (
        <Accordion key={i} title={g.title} count={g.items.length} defaultOpen={i === 0}>
          <ul className="det-items">
            {g.items.map((item, j) => (
              <li key={j} className="det-item">{item}</li>
            ))}
          </ul>
        </Accordion>
      ))}
    </div>
  );
}

function SvgDiagram({ diagram }) {
  if (!diagram || !diagram.svg) return null;
  return (
    <figure className="diagram">
      <div className="diagram-frame" dangerouslySetInnerHTML={{ __html: diagram.svg }} />
      {diagram.type && (
        <figcaption className="diagram-caption">
          {diagram.type === "plan" && "Plan diagram"}
          {diagram.type === "section" && "Section diagram"}
          {diagram.type === "elevation" && "Elevation diagram"}
          {diagram.type === "chart" && "Reference chart"}
          {diagram.type === "isometric" && "Isometric diagram"}
        </figcaption>
      )}
    </figure>
  );
}

function InstallList({ items }) {
  if (!items || items.length === 0) return null;
  return (
    <ol className="install-list">
      {items.map((it, i) => (
        <li key={i} className="install-li">{it}</li>
      ))}
    </ol>
  );
}

function FailurePatterns({ items }) {
  if (!items || items.length === 0) return null;
  return (
    <ul className="fail-list">
      {items.map((it, i) => (
        <li key={i} className="fail-li">{it}</li>
      ))}
    </ul>
  );
}

/* ════════════════════════════════════════════════════════════════════
   ROOM SYNTHESIS COMPONENTS
   ════════════════════════════════════════════════════════════════════ */

function SynthesisSection({ prose }) {
  if (!prose) return null;
  // Split by double newlines for paragraphs
  const paragraphs = prose.split("\n\n");
  return (
    <div className="synth-prose">
      {paragraphs.map((p, i) => <p key={i}>{p}</p>)}
    </div>
  );
}

function SequenceList({ steps }) {
  if (!steps || steps.length === 0) return null;
  return (
    <ol className="seq-list">
      {steps.map(s => (
        <li key={s.step} className="seq-item">
          <span className="seq-num">{String(s.step).padStart(2, "0")}</span>
          <div className="seq-body">
            <p className="seq-focus">{s.focus}</p>
            <p className="seq-why">{s.why}</p>
          </div>
        </li>
      ))}
    </ol>
  );
}

function InteractionsList({ items, goSpec }) {
  if (!items || items.length === 0) return null;
  return (
    <ul className="int-list">
      {items.map((it, i) => (
        <li key={i} className="int-item">
          <p className="int-specs">
            {it.specs.map((cd, j) => (
              <span key={cd}>
                {goSpec ? (
                  <button onClick={() => goSpec(cd)} className="int-spec-btn">{cd}</button>
                ) : (
                  <span className="int-spec">{cd}</span>
                )}
                {j < it.specs.length - 1 && <span className="int-sep" aria-hidden="true"> + </span>}
              </span>
            ))}
          </p>
          <p className="int-note">{it.note}.</p>
        </li>
      ))}
    </ul>
  );
}

function ClearancesTable({ rows }) {
  if (!rows || rows.length === 0) return null;
  return (
    <div className="adt-wrap" role="region" aria-label="Clearances table">
      <table className="adt">
        <thead>
          <tr>
            <th scope="col">Element</th>
            <th scope="col">Dimension</th>
            <th scope="col">Reference</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>
              <td className="adt-dim">{r.what}</td>
              <td className="adt-val">{r.dim}</td>
              <td className="adt-meas">{r.ref}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/* ════════════════════════════════════════════════════════════════════
   SCREENS
   ════════════════════════════════════════════════════════════════════ */

// ─── Preface ─────────────────────────────────────────────────────────
function PrefaceScreen({ mode, goPop, goCat, goRoom }) {
  return (
    <div className="screen">
      <header className="hero">
        <p className="hero-eyebrow">A guidebook for</p>
        <h1 className="hero-title">Accessible<br/>Built<br/>Environments</h1>
        <p className="hero-version">V9.0 · April 2026</p>
      </header>

      <section className="prose-section">
        <h2 className="sec-h">What this is</h2>
        <p>A field guide for designing buildings that work for the bodies and minds people actually have. Each entry pairs a specification — the architectural deliverable — with a question — the lived experience the deliverable answers. Both are the same content; choose your reading voice with the toggle at the top.</p>
        <p>The toggle is persistent. Switch any time.</p>
      </section>

      <section className="prose-section">
        <h2 className="sec-h">How to read it</h2>
        <p><strong>Specifications</strong> are written for architects, builders, occupational therapists, and clients commissioning work. They name what to specify, what to measure, what to verify, and what to procure.</p>
        <p><strong>Questions</strong> are written for occupants, family, advocates, building owners, and anyone evaluating a space. They name what to look for, what to ask about, what to expect.</p>
        <p>Each entry carries population codes — <Cite code="MOB" onJump={goPop}/> for mobility, <Cite code="VIS" onJump={goPop}/> for vision, and so on — that link to the population's needs.</p>
      </section>

      <section className="prose-section">
        <h2 className="sec-h">The three tiers</h2>
        <ul className="tier-list">
          {TIERS.map(t => (
            <li key={t.v} className="tier-li">
              <span className="tier-mark"><TierTag tier={t.v}/></span>
              <div className="tier-body">
                <p className="tier-name">{t.n}</p>
                <p className="tier-desc">{t.d}</p>
              </div>
            </li>
          ))}
        </ul>
      </section>

      <section className="prose-section">
        <h2 className="sec-h">Where to start</h2>
        <p>By building type — <button className="inline-link" onClick={() => goRoom("R-BA")}>a bathroom</button>, <button className="inline-link" onClick={() => goRoom("NR-EDU")}>a classroom</button>, <button className="inline-link" onClick={() => goRoom("NR-HLT")}>a clinic</button>. By category — <button className="inline-link" onClick={() => goCat("A")}>acoustics</button>, <button className="inline-link" onClick={() => goCat("B")}>lighting</button>, <button className="inline-link" onClick={() => goCat("E")}>circulation</button>. By population — start with the people who will use the space.</p>
      </section>
    </div>
  );
}

// ─── Buildings list ──────────────────────────────────────────────────
function BuildingsScreen({ goRoom }) {
  return (
    <div className="screen">
      <header className="screen-head">
        <h1 className="screen-h">Buildings</h1>
        <p className="screen-sub">Rooms organised by building type. Each room shows how its applicable specifications integrate.</p>
      </header>

      {Object.entries(BUILDINGS).map(([key, b]) => (
        <section key={key} className="bld-group">
          <h2 className="bld-h">{b.label}</h2>
          <p className="bld-desc">{b.desc}</p>
          <ul className="bld-rooms">
            {b.rooms.map(r => {
              const items = itemsForRoom(r.code);
              const t0 = items.filter(i => i.tr === 0).length;
              return (
                <li key={r.code}>
                  <button className="bld-room" onClick={() => goRoom(r.code)}>
                    <div className="bld-room-head">
                      <span className="bld-room-code">{r.code}</span>
                      <span className="bld-room-name">{r.name}</span>
                    </div>
                    <p className="bld-room-note">{r.note}</p>
                    <p className="bld-room-stats">
                      <span>{items.length} entries</span>
                      <span className="bld-room-stats-sep">·</span>
                      <span>{t0} critical</span>
                    </p>
                  </button>
                </li>
              );
            })}
          </ul>
        </section>
      ))}
    </div>
  );
}

// ─── Specs list ──────────────────────────────────────────────────────
function SpecsScreen({ mode, goSpec, focusCat }) {
  const grouped = useMemo(() => {
    const out = {};
    ITEMS.forEach(it => {
      (out[it.cat] = out[it.cat] || []).push(it);
    });
    Object.values(out).forEach(arr => arr.sort((a,b) => a.cd.localeCompare(b.cd)));
    return out;
  }, []);

  return (
    <div className="screen">
      <header className="screen-head">
        <h1 className="screen-h">Specifications</h1>
        <p className="screen-sub">{ITEMS.length} entries across {CATEGORIES.length} categories. Reading mode: <strong>{mode === "spec" ? "Specifications" : "Questions"}</strong>.</p>
      </header>

      {CATEGORIES.map(cat => {
        const items = grouped[cat.letter] || [];
        if (items.length === 0) return null;
        return (
          <section key={cat.letter} className="cat-group" id={`cat-${cat.letter}`}>
            <h2 className="cat-h">
              <span className="cat-letter">{cat.letter}</span>
              <span className="cat-name">{cat.name}</span>
              <span className="cat-count">{items.length}</span>
            </h2>
            <ul className="spec-list">
              {items.map(it => (
                <li key={it.cd}>
                  <button className="spec-row" onClick={() => goSpec(it.cd)}>
                    <div className="spec-row-l">
                      <span className="spec-row-cd">{it.cd}</span>
                      <TierTag tier={it.tr}/>
                    </div>
                    <div className="spec-row-r">
                      <p className="spec-row-t">{headingFor(it, mode)}</p>
                      <p className="spec-row-pops">
                        {it.p.slice(0, 4).map(p => (
                          <span key={p} className="spec-row-pop">{p}</span>
                        ))}
                        {it.p.length > 4 && <span className="spec-row-pop spec-row-pop-more">+{it.p.length - 4}</span>}
                      </p>
                    </div>
                  </button>
                </li>
              ))}
            </ul>
          </section>
        );
      })}
    </div>
  );
}

// ─── Populations ─────────────────────────────────────────────────────
function PopulationsScreen({ goSpec, initialOpen }) {
  return (
    <div className="screen">
      <header className="screen-head">
        <h1 className="screen-h">Populations</h1>
        <p className="screen-sub">Ten populations, each with specific environmental needs. Codes are used throughout the guidebook to indicate which entries are relevant.</p>
      </header>

      <ul className="pop-list">
        {POPS.map(p => {
          const relevant = itemsForPopulation(p.code);
          return (
            <li key={p.code}>
              <Accordion
                title={<span><span className="pop-acc-code">{p.code}</span>{" "}{p.label}</span>}
                count={relevant.length}
                defaultOpen={initialOpen === p.code}>
                <p className="pop-desc">{p.desc}</p>
                <p className="pop-rel-h">Relevant entries</p>
                <ul className="pop-rel-list">
                  {relevant.map(it => (
                    <li key={it.cd}>
                      <button className="pop-rel-row" onClick={() => goSpec(it.cd)}>
                        <span className="pop-rel-cd">{it.cd}</span>
                        <span className="pop-rel-t">{it.t}</span>
                        <TierTag tier={it.tr}/>
                      </button>
                    </li>
                  ))}
                </ul>
              </Accordion>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

// ─── Master Index ────────────────────────────────────────────────────
function MasterIndexScreen({ mode, goSpec, goRoom }) {
  const [filterPop, setFilterPop] = useState("ALL");
  const [filterTier, setFilterTier] = useState("ALL");
  const [filterCat, setFilterCat] = useState("ALL");
  const [filterTopic, setFilterTopic] = useState("ALL");
  const [filterRoom, setFilterRoom] = useState("ALL");
  const [searchText, setSearchText] = useState("");

  const filtered = useMemo(() => {
    return ITEMS.filter(it => {
      if (filterPop !== "ALL" && !it.p.includes(filterPop) && !it.p.includes("ALL")) return false;
      if (filterTier !== "ALL" && it.tr !== Number(filterTier)) return false;
      if (filterCat !== "ALL" && it.cat !== filterCat) return false;
      if (filterTopic !== "ALL" && !it.topics.includes(filterTopic)) return false;
      if (filterRoom !== "ALL" && !it.rooms.includes(filterRoom) && !it.rooms.includes("ALL")) return false;
      if (searchText) {
        const q = searchText.toLowerCase();
        const hay = (it.cd + " " + it.t + " " + (it.q || "") + " " + (it.s || "") + " " + (it.body || "")).toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
  }, [filterPop, filterTier, filterCat, filterTopic, filterRoom, searchText]);

  const reset = () => {
    setFilterPop("ALL"); setFilterTier("ALL"); setFilterCat("ALL");
    setFilterTopic("ALL"); setFilterRoom("ALL"); setSearchText("");
  };
  const anyActive = filterPop !== "ALL" || filterTier !== "ALL" || filterCat !== "ALL" || filterTopic !== "ALL" || filterRoom !== "ALL" || searchText !== "";

  return (
    <div className="screen">
      <header className="screen-head">
        <h1 className="screen-h">Index</h1>
        <p className="screen-sub">Filter by any combination of population, tier, category, topic, or room.</p>
      </header>

      <div className="idx-search">
        <input
          type="search"
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          placeholder="Search title, code, or description"
          className="idx-search-input"
          aria-label="Search the index"
        />
      </div>

      <div className="idx-filters">
        <div className="idx-fg">
          <label className="idx-fg-l">Population</label>
          <select value={filterPop} onChange={(e) => setFilterPop(e.target.value)} className="idx-fg-s">
            <option value="ALL">All populations</option>
            {POPS.map(p => <option key={p.code} value={p.code}>{p.code} — {p.label}</option>)}
          </select>
        </div>
        <div className="idx-fg">
          <label className="idx-fg-l">Tier</label>
          <select value={filterTier} onChange={(e) => setFilterTier(e.target.value)} className="idx-fg-s">
            <option value="ALL">All tiers</option>
            {TIERS.map(t => <option key={t.v} value={t.v}>T{t.v} — {t.n}</option>)}
          </select>
        </div>
        <div className="idx-fg">
          <label className="idx-fg-l">Category</label>
          <select value={filterCat} onChange={(e) => setFilterCat(e.target.value)} className="idx-fg-s">
            <option value="ALL">All categories</option>
            {CATEGORIES.map(c => <option key={c.letter} value={c.letter}>{c.letter} — {c.name}</option>)}
          </select>
        </div>
        <div className="idx-fg">
          <label className="idx-fg-l">Topic</label>
          <select value={filterTopic} onChange={(e) => setFilterTopic(e.target.value)} className="idx-fg-s">
            <option value="ALL">All topics</option>
            {TOPICS.map(t => <option key={t.id} value={t.id}>{t.label}</option>)}
          </select>
        </div>
        <div className="idx-fg">
          <label className="idx-fg-l">Room</label>
          <select value={filterRoom} onChange={(e) => setFilterRoom(e.target.value)} className="idx-fg-s">
            <option value="ALL">All rooms</option>
            <optgroup label="Residential">
              {BUILDINGS.res.rooms.map(r => <option key={r.code} value={r.code}>{r.code} — {r.name}</option>)}
            </optgroup>
            <optgroup label="Non-Residential">
              {BUILDINGS.nres.rooms.map(r => <option key={r.code} value={r.code}>{r.code} — {r.name}</option>)}
            </optgroup>
          </select>
        </div>
      </div>

      <div className="idx-summary">
        <p className="idx-count">{filtered.length} of {ITEMS.length} entries</p>
        {anyActive && <button onClick={reset} className="idx-reset">Reset filters</button>}
      </div>

      <ul className="idx-results">
        {filtered.map(it => (
          <li key={it.cd}>
            <button className="spec-row" onClick={() => goSpec(it.cd)}>
              <div className="spec-row-l">
                <span className="spec-row-cd">{it.cd}</span>
                <TierTag tier={it.tr}/>
              </div>
              <div className="spec-row-r">
                <p className="spec-row-t">{headingFor(it, mode)}</p>
                <p className="spec-row-pops">
                  {it.p.slice(0, 4).map(p => <span key={p} className="spec-row-pop">{p}</span>)}
                  {it.p.length > 4 && <span className="spec-row-pop spec-row-pop-more">+{it.p.length - 4}</span>}
                </p>
              </div>
            </button>
          </li>
        ))}
      </ul>

      {filtered.length === 0 && (
        <p className="idx-empty">No entries match these filters. Try resetting or relaxing one filter.</p>
      )}
    </div>
  );
}

/* ════════════════════════════════════════════════════════════════════
   DETAIL PAGES
   ════════════════════════════════════════════════════════════════════ */

// ─── Spec Detail ─────────────────────────────────────────────────────
function SpecDetail({ cd, mode, goBack, goSpec, goPop, goRoom, goCat }) {
  const item = getItem(cd);
  if (!item) return (
    <div className="screen">
      <p>Specification not found.</p>
      <button onClick={goBack} className="back-btn">← Back</button>
    </div>
  );

  const cat = getCategory(item.cat);
  const heading = headingFor(item, mode);
  const counterpart = mode === "spec" ? item.q : item.t;
  const roomsByBld = useMemo(() => {
    const out = { res: [], nres: [] };
    if (item.rooms.includes("ALL")) {
      return { all: true };
    }
    item.rooms.forEach(rc => {
      const r = ALL_ROOMS.find(x => x.code === rc);
      if (r) out[r.building].push(r);
    });
    return out;
  }, [item.rooms]);

  return (
    <div className="screen detail">
      <CrumbBar trail={[
        { label: "Specs", go: goBack },
        { label: cat ? `${cat.letter} · ${cat.name}` : item.cat, go: () => goCat(item.cat) },
        { label: item.cd }
      ]}/>

      <header className="detail-head">
        <p className="detail-cat">{cat ? cat.name : item.cat}</p>
        <h1 className="detail-h">{heading}</h1>
        {counterpart && (
          <blockquote className="detail-counter">
            <p className="detail-counter-l">{mode === "spec" ? "Question" : "Specification"}</p>
            <p>{counterpart}</p>
          </blockquote>
        )}
        <div className="detail-meta">
          <TierTag tier={item.tr}/>
          <span className="detail-tier-d">{TIERS.find(t => t.v === item.tr)?.d}</span>
        </div>
      </header>

      {item.s && (
        <section className="detail-section">
          <h2 className="detail-h2">Summary</h2>
          <p className="detail-prose">{item.s}</p>
        </section>
      )}

      {item.body && (
        <section className="detail-section">
          <h2 className="detail-h2">Specification in detail</h2>
          <p className="detail-prose">{item.body}</p>
        </section>
      )}

      {item.why && (
        <section className="detail-section">
          <h2 className="detail-h2">Why it matters</h2>
          <p className="detail-prose">{item.why}</p>
        </section>
      )}

      {item.dimensions && item.dimensions.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Dimensions</h2>
          <DimTable rows={item.dimensions}/>
        </section>
      )}

      {item.performance && item.performance.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Performance criteria</h2>
          <PerfTable rows={item.performance}/>
        </section>
      )}

      {item.codes && item.codes.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Codes and standards</h2>
          <CodesByJurisdiction rows={item.codes}/>
        </section>
      )}

      {item.products && item.products.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Product types</h2>
          <p className="detail-prose-sm">Manufacturer-neutral product types. Verify performance per the criteria above on actual products at submittal.</p>
          <ProductsList items={item.products}/>
        </section>
      )}

      {item.schedule && (
        <section className="detail-section">
          <h2 className="detail-h2">Schedule language</h2>
          <p className="detail-prose-sm">Drop-in language for project schedules. Adjust references to suit jurisdiction.</p>
          <ScheduleBlock text={item.schedule}/>
        </section>
      )}

      {item.detail && item.detail.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Detail items</h2>
          <DetailAccordion groups={item.detail}/>
        </section>
      )}

      {item.diagram && (
        <section className="detail-section">
          <h2 className="detail-h2">Diagram</h2>
          <SvgDiagram diagram={item.diagram}/>
        </section>
      )}

      {item.install && item.install.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Installation notes</h2>
          <InstallList items={item.install}/>
        </section>
      )}

      {item.failures && item.failures.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Common failures</h2>
          <FailurePatterns items={item.failures}/>
        </section>
      )}

      <section className="detail-section">
        <h2 className="detail-h2">Relevant populations</h2>
        <ul className="pop-reasons">
          {item.p.map(code => {
            const pop = code === "ALL" ? null : getPop(code);
            const reason = item.popReasons?.[code];
            return (
              <li key={code} className="pop-reason">
                <p className="pop-reason-h">
                  <Cite code={code} onJump={goPop}/>
                  <span className="pop-reason-name">{code === "ALL" ? "Universal" : pop?.label}</span>
                </p>
                {reason && <p className="pop-reason-t">{reason}</p>}
              </li>
            );
          })}
        </ul>
      </section>

      {!roomsByBld.all && (roomsByBld.res?.length > 0 || roomsByBld.nres?.length > 0) && (
        <section className="detail-section">
          <h2 className="detail-h2">Where it applies</h2>
          {roomsByBld.res?.length > 0 && (
            <div className="rooms-by-bld">
              <h3 className="rooms-bld-h">Residential</h3>
              <ul className="rooms-bld-list">
                {roomsByBld.res.map(r => (
                  <li key={r.code}>
                    <button className="rooms-bld-row" onClick={() => goRoom(r.code)}>
                      <span className="rooms-bld-code">{r.code}</span>
                      <span className="rooms-bld-name">{r.name}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {roomsByBld.nres?.length > 0 && (
            <div className="rooms-by-bld">
              <h3 className="rooms-bld-h">Non-Residential</h3>
              <ul className="rooms-bld-list">
                {roomsByBld.nres.map(r => (
                  <li key={r.code}>
                    <button className="rooms-bld-row" onClick={() => goRoom(r.code)}>
                      <span className="rooms-bld-code">{r.code}</span>
                      <span className="rooms-bld-name">{r.name}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      )}
      {roomsByBld.all && (
        <section className="detail-section">
          <h2 className="detail-h2">Where it applies</h2>
          <p className="detail-prose">Applies in all room types — universal provision.</p>
        </section>
      )}

      {item.related && item.related.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Related entries</h2>
          <ul className="rel-list">
            {item.related.map(r => {
              const ref = getItem(r.cd);
              return (
                <li key={r.cd}>
                  <button className="rel-row" onClick={() => goSpec(r.cd)}>
                    <p className="rel-row-h">
                      <span className="rel-row-cd">{r.cd}</span>
                      {ref && <span className="rel-row-t">{ref.t}</span>}
                    </p>
                    <p className="rel-row-why">{r.why}</p>
                  </button>
                </li>
              );
            })}
          </ul>
        </section>
      )}

      {item.evidence && item.evidence.length > 0 && (
        <Accordion title="Evidence and references" count={item.evidence.length}>
          <ul className="evid-list">
            {item.evidence.map((e, i) => (
              <li key={i} className="evid-row">
                <span className="evid-tier">Tier {e.tier}</span>
                <span className="evid-source">{e.source}</span>
              </li>
            ))}
          </ul>
        </Accordion>
      )}

      {item.topics && item.topics.length > 0 && (
        <section className="detail-section detail-topics">
          <p className="detail-topics-l">Topics</p>
          <ul className="topics-tags">
            {item.topics.map(t => {
              const topic = getTopic(t);
              return <li key={t} className="topic-tag">{topic ? topic.label : t}</li>;
            })}
          </ul>
        </section>
      )}
    </div>
  );
}

// ─── Room Detail ─────────────────────────────────────────────────────
function RoomDetail({ code, mode, goBack, goSpec, goPop }) {
  const room = getRoom(code);
  const items = useMemo(() => itemsForRoom(code), [code]);
  const [expanded, setExpanded] = useState({});

  if (!room) return (
    <div className="screen">
      <p>Room not found.</p>
      <button onClick={goBack} className="back-btn">← Back</button>
    </div>
  );

  const stats = {
    total: items.length,
    t0: items.filter(i => i.tr === 0).length,
    t1: items.filter(i => i.tr === 1).length,
    t2: items.filter(i => i.tr === 2).length,
  };

  const byCat = useMemo(() => {
    const out = {};
    items.forEach(it => { (out[it.cat] = out[it.cat] || []).push(it); });
    Object.values(out).forEach(arr => arr.sort((a,b) => a.cd.localeCompare(b.cd)));
    return out;
  }, [items]);

  const t0Items = items.filter(i => i.tr === 0);
  const buildingLabel = room.building === "res" ? "Residential" : "Non-Residential";

  return (
    <div className="screen detail">
      <CrumbBar trail={[
        { label: "Buildings", go: goBack },
        { label: buildingLabel, go: goBack },
        { label: room.name }
      ]}/>

      <header className="detail-head">
        <p className="detail-cat">{room.code}</p>
        <h1 className="detail-h">{room.name}</h1>
        <p className="detail-prose-lead">{room.note}</p>
      </header>

      {room.body && (
        <section className="detail-section">
          <p className="detail-prose">{room.body}</p>
        </section>
      )}

      {room.synthesis ? (
        <section className="detail-section">
          <h2 className="detail-h2">Design synthesis</h2>
          <SynthesisSection prose={room.synthesis}/>
        </section>
      ) : (
        <section className="detail-section detail-pending">
          <h2 className="detail-h2">Design synthesis</h2>
          <p className="detail-pending-t">Synthesis content for this room is not yet authored. The list of applicable specifications below is complete.</p>
        </section>
      )}

      {room.sequence && room.sequence.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Sequence of design decisions</h2>
          <p className="detail-prose-sm">Order matters. These decisions constrain each other; addressing them in this order avoids the most common integration failures.</p>
          <SequenceList steps={room.sequence}/>
        </section>
      )}

      {room.interactions && room.interactions.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Critical interactions</h2>
          <p className="detail-prose-sm">Where one specification's resolution constrains another. Tap a code to view the spec.</p>
          <InteractionsList items={room.interactions} goSpec={goSpec}/>
        </section>
      )}

      <section className="detail-section">
        <h2 className="detail-h2">Applicable entries</h2>
        <div className="room-stats">
          <div className="rs-box">
            <p className="rs-num">{stats.total}</p>
            <p className="rs-l">Total</p>
          </div>
          <div className="rs-box">
            <p className="rs-num">{stats.t0}</p>
            <p className="rs-l">T0 critical</p>
          </div>
          <div className="rs-box">
            <p className="rs-num">{stats.t1}</p>
            <p className="rs-l">T1 informed</p>
          </div>
          <div className="rs-box">
            <p className="rs-num">{stats.t2}</p>
            <p className="rs-l">T2 person</p>
          </div>
        </div>
      </section>

      {t0Items.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Critical entries (Tier 0)</h2>
          <p className="detail-prose-sm">These are non-negotiable in this room — code compliance and the floor of accessibility.</p>
          <ul className="critical-list">
            {t0Items.map(it => (
              <li key={it.cd}>
                <button className="critical-row" onClick={() => goSpec(it.cd)}>
                  <span className="critical-cd">{it.cd}</span>
                  <span className="critical-t">{headingFor(it, mode)}</span>
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="detail-section">
        <h2 className="detail-h2">All entries by category</h2>
        {CATEGORIES.map(cat => {
          const inCat = byCat[cat.letter];
          if (!inCat || inCat.length === 0) return null;
          return (
            <div key={cat.letter} className="cat-group cat-group-room">
              <h3 className="cat-h-room">
                <span className="cat-letter">{cat.letter}</span>
                <span className="cat-name">{cat.name}</span>
                <span className="cat-count">{inCat.length}</span>
              </h3>
              <ul className="spec-list">
                {inCat.map(it => {
                  const isExp = !!expanded[it.cd];
                  return (
                    <li key={it.cd}>
                      <div className={"room-spec-row" + (isExp ? " is-expanded" : "")}>
                        <button
                          className="room-spec-head"
                          onClick={() => setExpanded(e => ({...e, [it.cd]: !e[it.cd]}))}
                          aria-expanded={isExp}>
                          <div className="room-spec-l">
                            <span className="spec-row-cd">{it.cd}</span>
                            <TierTag tier={it.tr}/>
                          </div>
                          <p className="room-spec-t">{headingFor(it, mode)}</p>
                          <span className="room-spec-tog" aria-hidden="true">{isExp ? "−" : "+"}</span>
                        </button>
                        {isExp && (
                          <div className="room-spec-body">
                            <p className="room-spec-s">{it.s}</p>
                            <button className="room-spec-go" onClick={() => goSpec(it.cd)}>
                              Open full entry →
                            </button>
                          </div>
                        )}
                      </div>
                    </li>
                  );
                })}
              </ul>
            </div>
          );
        })}
      </section>

      {room.clearances && room.clearances.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Clearances</h2>
          <p className="detail-prose-sm">Room-specific clear-zone dimensions. Coordinate with applicable specifications above.</p>
          <ClearancesTable rows={room.clearances}/>
        </section>
      )}

      {room.failures && room.failures.length > 0 && (
        <section className="detail-section">
          <h2 className="detail-h2">Common failure patterns</h2>
          <p className="detail-prose-sm">Where rooms typically fail to integrate the applicable specifications.</p>
          <FailurePatterns items={room.failures}/>
        </section>
      )}

      {room.diagram && (
        <section className="detail-section">
          <h2 className="detail-h2">Schematic plan</h2>
          <SvgDiagram diagram={room.diagram}/>
        </section>
      )}
    </div>
  );
}

/* ════════════════════════════════════════════════════════════════════
   APP
   ════════════════════════════════════════════════════════════════════ */

export default function App() {
  const [tab, setTab] = useState("preface"); // preface | buildings | specs | people | index
  const [mode, setMode] = useState("spec"); // spec | question
  const [view, setView] = useState({ kind: "tab" }); // tab | spec | room
  const [popInitial, setPopInitial] = useState(null);
  const [catFocus, setCatFocus] = useState(null);

  const go = (next) => {
    if (typeof window !== "undefined") window.scrollTo(0, 0);
    setView(next);
  };

  const goTab = (t) => { setTab(t); go({ kind: "tab" }); setPopInitial(null); setCatFocus(null); };
  const goSpec = (cd) => go({ kind: "spec", cd });
  const goRoom = (code) => go({ kind: "room", code });
  const goPop = (code) => { setTab("people"); setPopInitial(code); go({ kind: "tab" }); };
  const goCat = (letter) => { setTab("specs"); setCatFocus(letter); go({ kind: "tab" }); };

  // Scroll to category when focused
  useEffect(() => {
    if (catFocus && tab === "specs" && view.kind === "tab") {
      const el = typeof document !== "undefined" ? document.getElementById(`cat-${catFocus}`) : null;
      if (el && el.scrollIntoView) {
        setTimeout(() => el.scrollIntoView({ behavior: "smooth", block: "start" }), 60);
      }
    }
  }, [catFocus, tab, view.kind]);

  let body;
  if (view.kind === "spec") {
    body = <SpecDetail
      cd={view.cd}
      mode={mode}
      goBack={() => { setView({ kind: "tab" }); setTab("specs"); }}
      goSpec={goSpec} goPop={goPop} goRoom={goRoom} goCat={goCat}/>;
  } else if (view.kind === "room") {
    body = <RoomDetail
      code={view.code}
      mode={mode}
      goBack={() => { setView({ kind: "tab" }); setTab("buildings"); }}
      goSpec={goSpec} goPop={goPop}/>;
  } else if (tab === "preface") {
    body = <PrefaceScreen mode={mode} goPop={goPop} goCat={goCat} goRoom={goRoom}/>;
  } else if (tab === "buildings") {
    body = <BuildingsScreen goRoom={goRoom}/>;
  } else if (tab === "specs") {
    body = <SpecsScreen mode={mode} goSpec={goSpec} focusCat={catFocus}/>;
  } else if (tab === "people") {
    body = <PopulationsScreen goSpec={goSpec} initialOpen={popInitial}/>;
  } else if (tab === "index") {
    body = <MasterIndexScreen mode={mode} goSpec={goSpec} goRoom={goRoom}/>;
  }

  return (
    <div className="app">
      <Style/>
      <header className="app-top">
        <ToggleBar mode={mode} setMode={setMode}/>
      </header>
      <main className="app-main">
        {body}
      </main>
      <nav className="app-nav" aria-label="Primary navigation">
        {[
          { id: "preface", label: "Preface" },
          { id: "buildings", label: "Buildings" },
          { id: "specs", label: "Specs" },
          { id: "people", label: "People" },
          { id: "index", label: "Index" },
        ].map(t => (
          <button
            key={t.id}
            onClick={() => goTab(t.id)}
            className={"nav-btn" + (tab === t.id && view.kind === "tab" ? " nav-btn-on" : "")}
            aria-current={tab === t.id && view.kind === "tab" ? "page" : undefined}>
            {t.label}
          </button>
        ))}
      </nav>
    </div>
  );
}

/* ════════════════════════════════════════════════════════════════════
   STYLES
   ════════════════════════════════════════════════════════════════════ */

function Style() {
  return (
    <style>{`
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;0,8..60,700;1,8..60,400;1,8..60,500&family=JetBrains+Mono:wght@400;500;600&display=swap');

      * { box-sizing: border-box; }

      :root {
        --ink: #1A1612;
        --ink-soft: #6B5F50;
        --ink-faint: #A39788;
        --bone: #F2EBDD;
        --bone-deep: #E8DFCC;
        --bone-soft: #EDE5D2;
        --bone-light: #F7F1E5;
        --line: rgba(26, 22, 18, 0.18);
        --line-soft: rgba(26, 22, 18, 0.08);
        --serif: 'Source Serif 4', Georgia, serif;
        --sans: 'Inter', system-ui, -apple-system, sans-serif;
        --mono: 'JetBrains Mono', ui-monospace, monospace;
      }

      .app {
        max-width: 430px;
        margin: 0 auto;
        background: var(--bone);
        color: var(--ink);
        min-height: 100vh;
        font-family: var(--sans);
        position: relative;
        font-size: 16px;
        line-height: 1.55;
      }

      .app-top {
        position: sticky;
        top: 0;
        z-index: 50;
        background: var(--bone);
        border-bottom: 1px solid var(--line);
      }

      .app-main {
        padding-bottom: 88px;
        min-height: 100vh;
      }

      /* ─── Toggle Bar ─── */
      .toggle-bar {
        display: flex;
        gap: 0;
        padding: 10px 16px;
        background: var(--bone);
      }
      .toggle-bar-btn {
        flex: 1;
        padding: 10px 14px;
        background: transparent;
        border: 1px solid var(--ink);
        color: var(--ink);
        font-family: var(--mono);
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        cursor: pointer;
        min-height: 44px;
        transition: all 120ms ease;
      }
      .toggle-bar-btn:first-child { border-radius: 4px 0 0 4px; border-right: none; }
      .toggle-bar-btn:last-child { border-radius: 0 4px 4px 0; }
      .toggle-bar-btn:hover { background: var(--bone-deep); }
      .toggle-bar-btn:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
        z-index: 1;
      }
      .toggle-bar-btn-on {
        background: var(--ink);
        color: var(--bone);
      }
      .toggle-bar-btn-on:hover { background: var(--ink); }

      /* ─── Bottom Nav ─── */
      .app-nav {
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 430px;
        display: flex;
        background: var(--bone);
        border-top: 1px solid var(--ink);
        z-index: 40;
      }
      .nav-btn {
        flex: 1;
        padding: 14px 4px 16px;
        background: transparent;
        border: none;
        color: var(--ink);
        font-family: var(--mono);
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        cursor: pointer;
        min-height: 56px;
        transition: background 120ms ease;
      }
      .nav-btn:hover { background: var(--bone-deep); }
      .nav-btn:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: -2px;
      }
      .nav-btn-on {
        background: var(--ink);
        color: var(--bone);
      }
      .nav-btn-on:hover { background: var(--ink); }

      /* ─── Screen ─── */
      .screen { padding: 8px 0 32px; }
      .screen-head {
        padding: 24px 20px 8px;
        border-bottom: 1px solid var(--line-soft);
      }
      .screen-h {
        font-family: var(--serif);
        font-weight: 500;
        font-size: 32px;
        line-height: 1.1;
        margin: 0 0 8px;
        letter-spacing: -0.01em;
      }
      .screen-sub {
        margin: 0;
        color: var(--ink-soft);
        font-size: 14px;
      }

      /* ─── Hero ─── */
      .hero {
        padding: 56px 20px 36px;
        border-bottom: 1px solid var(--line);
      }
      .hero-eyebrow {
        font-family: var(--mono);
        font-size: 11px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--ink-soft);
        margin: 0 0 20px;
      }
      .hero-title {
        font-family: var(--serif);
        font-weight: 500;
        font-size: 48px;
        line-height: 0.98;
        margin: 0 0 28px;
        letter-spacing: -0.02em;
      }
      .hero-version {
        font-family: var(--mono);
        font-size: 12px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--ink-soft);
        margin: 0;
      }

      /* ─── Prose sections ─── */
      .prose-section {
        padding: 28px 20px;
        border-bottom: 1px solid var(--line-soft);
      }
      .prose-section:last-child { border-bottom: none; }
      .sec-h {
        font-family: var(--serif);
        font-weight: 500;
        font-size: 22px;
        line-height: 1.2;
        margin: 0 0 12px;
      }
      .prose-section p {
        margin: 0 0 12px;
        font-family: var(--serif);
        font-size: 17px;
        line-height: 1.55;
      }
      .prose-section p:last-child { margin-bottom: 0; }
      .inline-link {
        background: none;
        border: none;
        padding: 0;
        font: inherit;
        color: var(--ink);
        text-decoration: underline;
        text-underline-offset: 3px;
        text-decoration-thickness: 1px;
        cursor: pointer;
      }
      .inline-link:hover { text-decoration-thickness: 2px; }
      .inline-link:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }

      .tier-list {
        list-style: none;
        padding: 0;
        margin: 16px 0 0;
      }
      .tier-li {
        display: flex;
        gap: 14px;
        padding: 14px 0;
        border-top: 1px solid var(--line-soft);
      }
      .tier-li:first-child { border-top: none; }
      .tier-mark { padding-top: 2px; }
      .tier-name {
        font-family: var(--mono);
        font-size: 12px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin: 0 0 4px;
      }
      .tier-desc {
        margin: 0;
        font-size: 14px;
        color: var(--ink-soft);
        line-height: 1.5;
      }

      /* ─── Cite popover ─── */
      .cite-wrap { position: relative; display: inline-block; }
      .cite {
        display: inline-flex;
        align-items: center;
        background: transparent;
        border: 1px solid var(--ink);
        color: var(--ink);
        padding: 1px 5px;
        font-family: var(--mono);
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.04em;
        cursor: pointer;
        border-radius: 2px;
        margin: 0 1px;
        line-height: 1.4;
        min-height: 18px;
        vertical-align: 1px;
      }
      .cite:hover { background: var(--ink); color: var(--bone); }
      .cite-open { background: var(--ink); color: var(--bone); }
      .cite-all { font-style: italic; }
      .cite:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }

      .popover {
        position: absolute;
        top: calc(100% + 8px);
        left: 50%;
        transform: translateX(-50%);
        z-index: 100;
        background: var(--ink);
        color: var(--bone);
        padding: 14px 16px;
        border-radius: 4px;
        width: 280px;
        max-width: calc(100vw - 32px);
        font-family: var(--sans);
        box-shadow: 0 6px 24px rgba(0,0,0,0.18);
      }
      .popover-arrow {
        position: absolute;
        top: -6px;
        left: 50%;
        transform: translateX(-50%) rotate(45deg);
        width: 12px;
        height: 12px;
        background: var(--ink);
      }
      .popover-code {
        font-family: var(--mono);
        font-size: 11px;
        letter-spacing: 0.08em;
        margin: 0 0 4px;
        opacity: 0.6;
      }
      .popover-name {
        font-family: var(--serif);
        font-size: 16px;
        font-weight: 500;
        margin: 0 0 6px;
      }
      .popover-desc {
        font-size: 13px;
        line-height: 1.5;
        margin: 0 0 10px;
        opacity: 0.92;
      }
      .popover-meta {
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin: 0 0 8px;
        opacity: 0.6;
      }
      .popover-jump {
        background: none;
        border: 1px solid var(--bone);
        color: var(--bone);
        padding: 6px 10px;
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        cursor: pointer;
        border-radius: 3px;
        width: 100%;
        text-align: left;
      }
      .popover-jump:hover { background: var(--bone); color: var(--ink); }
      .popover-jump:focus-visible {
        outline: 2px solid var(--bone);
        outline-offset: 2px;
      }

      /* ─── Tier tag ─── */
      .tiertag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.06em;
        color: var(--ink);
      }
      .tiertag-bar {
        font-family: var(--mono);
        letter-spacing: 0;
        font-size: 10px;
      }
      .tiertag-num { font-weight: 600; }

      /* ─── Crumb ─── */
      .crumb {
        padding: 12px 20px 4px;
        font-family: var(--mono);
        font-size: 11px;
        letter-spacing: 0.04em;
        color: var(--ink-soft);
      }
      .crumb-item { display: inline; }
      .crumb-link {
        background: none;
        border: none;
        padding: 0;
        color: var(--ink);
        text-decoration: underline;
        text-underline-offset: 2px;
        cursor: pointer;
        font: inherit;
      }
      .crumb-link:hover { text-decoration-thickness: 2px; }
      .crumb-link:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }
      .crumb-link-static { color: var(--ink-soft); }
      .crumb-current { color: var(--ink); font-weight: 500; }
      .crumb-sep { color: var(--ink-faint); margin: 0 4px; }

      /* ─── Accordion ─── */
      .acc {
        border-top: 1px solid var(--line-soft);
      }
      .acc-head {
        width: 100%;
        background: transparent;
        border: none;
        padding: 14px 20px;
        text-align: left;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 10px;
        min-height: 50px;
        font: inherit;
      }
      .acc-head:hover { background: var(--bone-soft); }
      .acc-head:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: -2px;
      }
      .acc-title {
        flex: 1;
        font-family: var(--mono);
        font-size: 12px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-weight: 600;
      }
      .acc-count {
        font-family: var(--mono);
        font-size: 10px;
        color: var(--ink-soft);
        padding: 2px 6px;
        border: 1px solid var(--line);
        border-radius: 2px;
      }
      .acc-tog {
        font-family: var(--mono);
        font-size: 18px;
        line-height: 1;
        width: 16px;
        text-align: center;
      }
      .acc-body {
        padding: 4px 20px 20px;
      }

      /* ─── Buildings ─── */
      .bld-group {
        padding: 28px 20px;
        border-bottom: 1px solid var(--line-soft);
      }
      .bld-h {
        font-family: var(--serif);
        font-weight: 500;
        font-size: 24px;
        margin: 0 0 6px;
      }
      .bld-desc {
        margin: 0 0 18px;
        font-size: 14px;
        color: var(--ink-soft);
      }
      .bld-rooms {
        list-style: none;
        padding: 0;
        margin: 0;
        display: grid;
        gap: 10px;
      }
      .bld-room {
        width: 100%;
        background: var(--bone-soft);
        border: 1px solid var(--line);
        padding: 14px 16px;
        text-align: left;
        cursor: pointer;
        font: inherit;
        color: var(--ink);
        border-radius: 4px;
        min-height: 80px;
        transition: background 120ms ease, border-color 120ms ease;
      }
      .bld-room:hover { background: var(--bone-deep); border-color: var(--ink); }
      .bld-room:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }
      .bld-room-head {
        display: flex;
        align-items: baseline;
        gap: 10px;
        margin-bottom: 4px;
      }
      .bld-room-code {
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.06em;
        color: var(--ink-soft);
      }
      .bld-room-name {
        font-family: var(--serif);
        font-size: 18px;
        font-weight: 500;
      }
      .bld-room-note {
        font-size: 13px;
        color: var(--ink-soft);
        margin: 0 0 6px;
      }
      .bld-room-stats {
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.06em;
        color: var(--ink-soft);
        margin: 0;
        display: flex;
        gap: 6px;
      }
      .bld-room-stats-sep { opacity: 0.5; }

      /* ─── Cat groups + spec list ─── */
      .cat-group {
        padding: 24px 20px;
        border-bottom: 1px solid var(--line-soft);
      }
      .cat-h, .cat-h-room {
        display: flex;
        align-items: baseline;
        gap: 12px;
        margin: 0 0 14px;
        font-family: var(--mono);
        font-size: 12px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 600;
      }
      .cat-h-room { font-size: 11px; margin-top: 18px; }
      .cat-letter {
        background: var(--ink);
        color: var(--bone);
        padding: 3px 7px;
        border-radius: 2px;
        font-family: var(--mono);
        font-size: 11px;
      }
      .cat-name { flex: 1; }
      .cat-count {
        color: var(--ink-soft);
        font-size: 10px;
        padding: 2px 6px;
        border: 1px solid var(--line);
        border-radius: 2px;
      }
      .spec-list {
        list-style: none;
        padding: 0;
        margin: 0;
        display: grid;
        gap: 6px;
      }
      .spec-row {
        width: 100%;
        background: var(--bone-soft);
        border: 1px solid var(--line);
        padding: 12px 14px;
        text-align: left;
        cursor: pointer;
        font: inherit;
        color: var(--ink);
        border-radius: 3px;
        display: flex;
        gap: 12px;
        align-items: flex-start;
        min-height: 60px;
        transition: background 100ms ease;
      }
      .spec-row:hover { background: var(--bone-deep); }
      .spec-row:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }
      .spec-row-l {
        display: flex;
        flex-direction: column;
        gap: 4px;
        flex-shrink: 0;
        min-width: 60px;
      }
      .spec-row-cd {
        font-family: var(--mono);
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.04em;
      }
      .spec-row-r { flex: 1; min-width: 0; }
      .spec-row-t {
        font-family: var(--serif);
        font-size: 15px;
        margin: 0 0 4px;
        line-height: 1.35;
      }
      .spec-row-pops {
        margin: 0;
        display: flex;
        gap: 4px;
        flex-wrap: wrap;
      }
      .spec-row-pop {
        font-family: var(--mono);
        font-size: 9px;
        letter-spacing: 0.04em;
        color: var(--ink-soft);
        padding: 1px 4px;
        border: 1px solid var(--line);
        border-radius: 2px;
      }
      .spec-row-pop-more { font-style: italic; }

      /* ─── Detail page ─── */
      .detail { padding-top: 0; }
      .detail-head {
        padding: 12px 20px 24px;
        border-bottom: 1px solid var(--line);
      }
      .detail-cat {
        font-family: var(--mono);
        font-size: 11px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--ink-soft);
        margin: 0 0 8px;
      }
      .detail-h {
        font-family: var(--serif);
        font-weight: 500;
        font-size: 28px;
        line-height: 1.15;
        margin: 0 0 16px;
        letter-spacing: -0.01em;
      }
      .detail-counter {
        margin: 0 0 16px;
        padding: 14px 16px;
        background: var(--bone-soft);
        border-left: 3px solid var(--ink);
        border-radius: 0 3px 3px 0;
      }
      .detail-counter-l {
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--ink-soft);
        margin: 0 0 6px;
      }
      .detail-counter p:last-child {
        margin: 0;
        font-family: var(--serif);
        font-style: italic;
        font-size: 16px;
        line-height: 1.45;
      }
      .detail-meta {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 12px;
      }
      .detail-tier-d {
        font-size: 12px;
        color: var(--ink-soft);
      }

      .detail-section {
        padding: 24px 20px;
        border-bottom: 1px solid var(--line-soft);
      }
      .detail-section:last-child { border-bottom: none; }
      .detail-h2 {
        font-family: var(--mono);
        font-size: 11px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-weight: 600;
        margin: 0 0 14px;
      }
      .detail-prose, .detail-prose-lead {
        font-family: var(--serif);
        font-size: 16px;
        line-height: 1.55;
        margin: 0 0 12px;
      }
      .detail-prose:last-child { margin-bottom: 0; }
      .detail-prose-lead {
        font-size: 17px;
        color: var(--ink-soft);
        font-style: italic;
        margin: 0;
      }
      .detail-prose-sm {
        font-family: var(--serif);
        font-size: 14px;
        line-height: 1.5;
        color: var(--ink-soft);
        margin: 0 0 14px;
        font-style: italic;
      }
      .detail-pending {
        background: var(--bone-soft);
        border-radius: 3px;
      }
      .detail-pending-t {
        font-style: italic;
        color: var(--ink-soft);
        margin: 0;
      }
      .detail-topics {
        background: var(--bone-soft);
        border-bottom: none;
        padding: 18px 20px;
      }
      .detail-topics-l {
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--ink-soft);
        margin: 0 0 8px;
      }
      .topics-tags {
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
      }
      .topic-tag {
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.04em;
        padding: 3px 8px;
        background: var(--bone);
        border: 1px solid var(--line);
        border-radius: 2px;
      }

      /* ─── Architect tables (DimTable, PerfTable, Clearances) ─── */
      .adt-wrap {
        overflow-x: auto;
        border: 1px solid var(--line);
        border-radius: 3px;
        background: var(--bone-light);
      }
      .adt {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
      }
      .adt th, .adt td {
        padding: 10px 12px;
        text-align: left;
        vertical-align: top;
      }
      .adt thead th {
        background: var(--ink);
        color: var(--bone);
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 600;
      }
      .adt tbody tr {
        border-top: 1px solid var(--line-soft);
      }
      .adt tbody tr:first-child { border-top: none; }
      .adt-dim {
        font-family: var(--sans);
        font-weight: 500;
      }
      .adt-note {
        display: block;
        font-family: var(--serif);
        font-style: italic;
        font-size: 12px;
        color: var(--ink-soft);
        margin-top: 4px;
        font-weight: 400;
      }
      .adt-val {
        font-family: var(--mono);
        font-weight: 600;
        white-space: nowrap;
      }
      .adt-unit {
        font-family: var(--mono);
        color: var(--ink-soft);
        white-space: nowrap;
      }
      .adt-meas {
        font-family: var(--serif);
        font-size: 12px;
        color: var(--ink-soft);
        line-height: 1.4;
      }

      /* ─── Codes by jurisdiction ─── */
      .codes-list {
        display: grid;
        gap: 6px;
      }
      .codes-jur {
        border: 1px solid var(--line);
        border-radius: 3px;
        background: var(--bone-light);
        overflow: hidden;
      }
      .codes-jur-head {
        list-style: none;
        cursor: pointer;
        padding: 12px 14px;
        display: flex;
        align-items: center;
        gap: 12px;
        min-height: 44px;
      }
      .codes-jur-head::-webkit-details-marker { display: none; }
      .codes-jur-head:hover { background: var(--bone-deep); }
      .codes-jur-label {
        font-family: var(--mono);
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.06em;
        flex: 1;
      }
      .codes-jur-count {
        font-family: var(--mono);
        font-size: 10px;
        color: var(--ink-soft);
      }
      .codes-jur-tog {
        font-family: var(--mono);
        font-size: 16px;
        width: 16px;
        text-align: center;
      }
      .codes-jur[open] .codes-jur-tog::before { content: "−"; }
      .codes-jur:not([open]) .codes-jur-tog { content: "+"; }
      .codes-jur[open] .codes-jur-tog { font-size: 0; }
      .codes-jur[open] .codes-jur-tog::before { font-size: 16px; }
      .codes-jur-list {
        list-style: none;
        padding: 0 14px 12px;
        margin: 0;
      }
      .codes-jur-row {
        padding: 8px 0;
        border-top: 1px solid var(--line-soft);
        display: flex;
        flex-direction: column;
        gap: 3px;
      }
      .codes-jur-row:first-child { border-top: none; }
      .codes-ref {
        font-family: var(--mono);
        font-size: 12px;
        font-weight: 600;
      }
      .codes-clause {
        font-family: var(--serif);
        font-size: 13px;
        color: var(--ink-soft);
      }

      /* ─── Products list ─── */
      .prod-list {
        list-style: none;
        padding: 0;
        margin: 0;
        display: grid;
        gap: 8px;
      }
      .prod-li {
        padding: 10px 14px;
        background: var(--bone-light);
        border-left: 2px solid var(--ink);
        font-family: var(--serif);
        font-size: 14px;
        line-height: 1.45;
      }

      /* ─── Schedule block ─── */
      .sched-block {
        position: relative;
        background: var(--ink);
        color: var(--bone);
        padding: 18px 20px;
        border-radius: 3px;
      }
      .sched-text {
        margin: 0;
        font-family: var(--serif);
        font-size: 14px;
        line-height: 1.6;
        padding-right: 70px;
      }
      .sched-copy {
        position: absolute;
        top: 12px;
        right: 12px;
        background: transparent;
        border: 1px solid var(--bone);
        color: var(--bone);
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 5px 10px;
        cursor: pointer;
        border-radius: 2px;
        min-height: 32px;
      }
      .sched-copy:hover { background: var(--bone); color: var(--ink); }
      .sched-copy:focus-visible {
        outline: 2px solid var(--bone);
        outline-offset: 2px;
      }

      /* ─── Detail accordion ─── */
      .det-list {
        border: 1px solid var(--line);
        border-radius: 3px;
        overflow: hidden;
      }
      .det-list .acc { border-top: 1px solid var(--line-soft); }
      .det-list .acc:first-child { border-top: none; }
      .det-list .acc-head { padding: 14px 16px; }
      .det-list .acc-body { padding: 0 16px 16px; }
      .det-items {
        list-style: none;
        padding: 0;
        margin: 0;
      }
      .det-item {
        padding: 8px 0 8px 16px;
        position: relative;
        font-family: var(--serif);
        font-size: 14px;
        line-height: 1.5;
        border-top: 1px solid var(--line-soft);
      }
      .det-item:first-child { border-top: none; }
      .det-item::before {
        content: "·";
        position: absolute;
        left: 4px;
        font-weight: 600;
        color: var(--ink-soft);
      }

      /* ─── Diagram ─── */
      .diagram {
        margin: 0;
        background: var(--bone-light);
        border: 1px solid var(--line);
        border-radius: 3px;
        padding: 16px;
      }
      .diagram-frame { width: 100%; }
      .diagram-frame svg { width: 100%; height: auto; display: block; }
      .diagram-caption {
        margin: 12px 0 0;
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--ink-soft);
      }

      /* ─── Install + Failure ─── */
      .install-list {
        list-style: none;
        counter-reset: ins;
        padding: 0;
        margin: 0;
        display: grid;
        gap: 8px;
      }
      .install-li {
        counter-increment: ins;
        padding: 10px 14px 10px 44px;
        background: var(--bone-light);
        position: relative;
        font-family: var(--serif);
        font-size: 14px;
        line-height: 1.5;
        border-radius: 3px;
        border-left: 2px solid var(--ink);
      }
      .install-li::before {
        content: counter(ins, decimal-leading-zero);
        position: absolute;
        left: 14px;
        top: 11px;
        font-family: var(--mono);
        font-size: 11px;
        font-weight: 600;
        color: var(--ink-soft);
      }
      .fail-list {
        list-style: none;
        padding: 0;
        margin: 0;
        display: grid;
        gap: 6px;
      }
      .fail-li {
        padding: 10px 14px 10px 30px;
        background: var(--bone-light);
        position: relative;
        font-family: var(--serif);
        font-size: 14px;
        line-height: 1.5;
        border-radius: 3px;
      }
      .fail-li::before {
        content: "✕";
        position: absolute;
        left: 12px;
        top: 11px;
        font-family: var(--mono);
        font-size: 12px;
        font-weight: 600;
        color: var(--ink);
      }

      /* ─── Synthesis sections ─── */
      .synth-prose p {
        font-family: var(--serif);
        font-size: 16px;
        line-height: 1.6;
        margin: 0 0 14px;
      }
      .synth-prose p:last-child { margin-bottom: 0; }

      .seq-list {
        list-style: none;
        padding: 0;
        margin: 0;
        display: grid;
        gap: 12px;
      }
      .seq-item {
        display: flex;
        gap: 14px;
        padding: 14px;
        background: var(--bone-light);
        border-left: 2px solid var(--ink);
        border-radius: 0 3px 3px 0;
      }
      .seq-num {
        font-family: var(--mono);
        font-size: 18px;
        font-weight: 600;
        color: var(--ink);
        flex-shrink: 0;
        line-height: 1;
        padding-top: 2px;
      }
      .seq-body { flex: 1; }
      .seq-focus {
        font-family: var(--serif);
        font-size: 16px;
        font-weight: 500;
        margin: 0 0 4px;
        line-height: 1.35;
      }
      .seq-why {
        margin: 0;
        font-family: var(--serif);
        font-size: 14px;
        font-style: italic;
        color: var(--ink-soft);
        line-height: 1.5;
      }

      .int-list {
        list-style: none;
        padding: 0;
        margin: 0;
        display: grid;
        gap: 10px;
      }
      .int-item {
        padding: 14px;
        background: var(--bone-light);
        border: 1px solid var(--line);
        border-radius: 3px;
      }
      .int-specs {
        margin: 0 0 8px;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 4px;
      }
      .int-spec, .int-spec-btn {
        font-family: var(--mono);
        font-size: 11px;
        font-weight: 600;
        background: var(--ink);
        color: var(--bone);
        padding: 3px 7px;
        border: none;
        border-radius: 2px;
        cursor: pointer;
        line-height: 1.3;
      }
      .int-spec-btn:hover { background: var(--ink-soft); }
      .int-spec-btn:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }
      .int-sep {
        font-family: var(--mono);
        font-size: 11px;
        color: var(--ink-soft);
        margin: 0 2px;
      }
      .int-note {
        margin: 0;
        font-family: var(--serif);
        font-size: 14px;
        line-height: 1.5;
      }

      /* ─── Pop reasons + rooms by building ─── */
      .pop-reasons, .rel-list, .evid-list, .rooms-bld-list, .pop-rel-list, .critical-list {
        list-style: none;
        padding: 0;
        margin: 0;
        display: grid;
        gap: 8px;
      }
      .pop-reason {
        padding: 12px 14px;
        background: var(--bone-soft);
        border: 1px solid var(--line);
        border-radius: 3px;
      }
      .pop-reason-h {
        margin: 0 0 6px;
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .pop-reason-name {
        font-family: var(--serif);
        font-size: 15px;
        font-weight: 500;
      }
      .pop-reason-t {
        margin: 0;
        font-family: var(--serif);
        font-size: 14px;
        line-height: 1.5;
        color: var(--ink-soft);
      }

      /* ─── Rooms by building ─── */
      .rooms-by-bld { margin-bottom: 16px; }
      .rooms-by-bld:last-child { margin-bottom: 0; }
      .rooms-bld-h {
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 600;
        color: var(--ink-soft);
        margin: 0 0 8px;
      }
      .rooms-bld-row {
        width: 100%;
        background: var(--bone-soft);
        border: 1px solid var(--line);
        padding: 10px 14px;
        display: flex;
        align-items: baseline;
        gap: 12px;
        cursor: pointer;
        font: inherit;
        color: var(--ink);
        text-align: left;
        border-radius: 3px;
        min-height: 44px;
      }
      .rooms-bld-row:hover { background: var(--bone-deep); }
      .rooms-bld-row:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }
      .rooms-bld-code {
        font-family: var(--mono);
        font-size: 11px;
        color: var(--ink-soft);
        flex-shrink: 0;
      }
      .rooms-bld-name {
        font-family: var(--serif);
        font-size: 15px;
      }

      /* ─── Related entries ─── */
      .rel-row {
        width: 100%;
        background: var(--bone-soft);
        border: 1px solid var(--line);
        padding: 12px 14px;
        text-align: left;
        cursor: pointer;
        font: inherit;
        color: var(--ink);
        border-radius: 3px;
      }
      .rel-row:hover { background: var(--bone-deep); }
      .rel-row:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }
      .rel-row-h {
        margin: 0 0 4px;
        display: flex;
        gap: 10px;
        align-items: baseline;
        flex-wrap: wrap;
      }
      .rel-row-cd {
        font-family: var(--mono);
        font-size: 11px;
        font-weight: 600;
      }
      .rel-row-t {
        font-family: var(--serif);
        font-size: 14px;
      }
      .rel-row-why {
        margin: 0;
        font-family: var(--serif);
        font-size: 13px;
        font-style: italic;
        color: var(--ink-soft);
      }

      /* ─── Evidence ─── */
      .evid-list { padding: 4px 0 0; }
      .evid-row {
        display: grid;
        grid-template-columns: 70px 1fr;
        gap: 12px;
        padding: 8px 0;
        border-top: 1px solid var(--line-soft);
      }
      .evid-row:first-child { border-top: none; padding-top: 0; }
      .evid-tier {
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.06em;
        color: var(--ink-soft);
      }
      .evid-source {
        font-family: var(--serif);
        font-size: 13px;
        line-height: 1.4;
      }

      /* ─── Populations ─── */
      .pop-list, .idx-results { list-style: none; padding: 0; margin: 0; }
      .pop-acc-code {
        font-family: var(--mono);
        font-size: 10px;
        color: var(--ink-soft);
        margin-right: 6px;
      }
      .pop-desc {
        font-family: var(--serif);
        font-size: 15px;
        line-height: 1.5;
        margin: 0 0 16px;
      }
      .pop-rel-h {
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--ink-soft);
        margin: 0 0 8px;
      }
      .pop-rel-row {
        width: 100%;
        background: var(--bone-soft);
        border: 1px solid var(--line);
        padding: 10px 12px;
        display: flex;
        gap: 10px;
        align-items: baseline;
        cursor: pointer;
        font: inherit;
        color: var(--ink);
        text-align: left;
        border-radius: 3px;
        min-height: 44px;
      }
      .pop-rel-row:hover { background: var(--bone-deep); }
      .pop-rel-row:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }
      .pop-rel-cd {
        font-family: var(--mono);
        font-size: 10px;
        color: var(--ink-soft);
        flex-shrink: 0;
        min-width: 40px;
      }
      .pop-rel-t {
        flex: 1;
        font-family: var(--serif);
        font-size: 14px;
      }

      /* ─── Index ─── */
      .idx-search {
        padding: 12px 20px;
        border-bottom: 1px solid var(--line-soft);
      }
      .idx-search-input {
        width: 100%;
        padding: 12px 14px;
        background: var(--bone-soft);
        border: 1px solid var(--line);
        color: var(--ink);
        font-family: var(--serif);
        font-size: 15px;
        border-radius: 3px;
        min-height: 44px;
      }
      .idx-search-input:focus {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
        background: var(--bone-light);
      }
      .idx-filters {
        padding: 12px 20px;
        display: grid;
        gap: 10px;
        border-bottom: 1px solid var(--line-soft);
      }
      .idx-fg {
        display: grid;
        grid-template-columns: 100px 1fr;
        gap: 10px;
        align-items: center;
      }
      .idx-fg-l {
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--ink-soft);
      }
      .idx-fg-s {
        padding: 8px 10px;
        background: var(--bone-soft);
        border: 1px solid var(--line);
        color: var(--ink);
        font-family: var(--sans);
        font-size: 13px;
        border-radius: 3px;
        min-height: 36px;
      }
      .idx-fg-s:focus {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }
      .idx-summary {
        padding: 12px 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        border-bottom: 1px solid var(--line-soft);
      }
      .idx-count {
        flex: 1;
        margin: 0;
        font-family: var(--mono);
        font-size: 11px;
        letter-spacing: 0.06em;
        color: var(--ink-soft);
      }
      .idx-reset {
        background: transparent;
        border: 1px solid var(--ink);
        color: var(--ink);
        padding: 6px 12px;
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        cursor: pointer;
        border-radius: 2px;
        min-height: 32px;
      }
      .idx-reset:hover { background: var(--ink); color: var(--bone); }
      .idx-reset:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }
      .idx-results { padding: 8px 20px; display: grid; gap: 6px; }
      .idx-empty {
        padding: 32px 20px;
        text-align: center;
        font-family: var(--serif);
        color: var(--ink-soft);
        font-style: italic;
      }

      /* ─── Room stats + critical ─── */
      .room-stats {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
      }
      .rs-box {
        background: var(--bone-light);
        border: 1px solid var(--line);
        padding: 10px 8px;
        text-align: center;
        border-radius: 3px;
      }
      .rs-num {
        font-family: var(--serif);
        font-size: 22px;
        font-weight: 500;
        margin: 0 0 2px;
        line-height: 1;
      }
      .rs-l {
        font-family: var(--mono);
        font-size: 9px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--ink-soft);
        margin: 0;
      }
      .critical-row {
        width: 100%;
        background: var(--ink);
        color: var(--bone);
        border: none;
        padding: 12px 14px;
        display: flex;
        gap: 12px;
        align-items: baseline;
        cursor: pointer;
        font: inherit;
        text-align: left;
        border-radius: 3px;
        min-height: 44px;
      }
      .critical-row:hover { background: var(--ink-soft); }
      .critical-row:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }
      .critical-cd {
        font-family: var(--mono);
        font-size: 11px;
        font-weight: 600;
        flex-shrink: 0;
        min-width: 40px;
      }
      .critical-t {
        font-family: var(--serif);
        font-size: 14px;
        line-height: 1.35;
      }

      /* ─── Room spec inline expand ─── */
      .cat-group-room {
        padding: 0;
        border-bottom: none;
        margin-bottom: 16px;
      }
      .cat-group-room:last-child { margin-bottom: 0; }
      .room-spec-row {
        background: var(--bone-soft);
        border: 1px solid var(--line);
        border-radius: 3px;
        margin-bottom: 4px;
      }
      .room-spec-row.is-expanded {
        border-color: var(--ink);
      }
      .room-spec-head {
        width: 100%;
        background: transparent;
        border: none;
        padding: 12px 14px;
        text-align: left;
        cursor: pointer;
        font: inherit;
        color: var(--ink);
        display: flex;
        gap: 12px;
        align-items: flex-start;
        min-height: 60px;
      }
      .room-spec-head:hover { background: var(--bone-deep); }
      .room-spec-head:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: -2px;
      }
      .room-spec-l {
        display: flex;
        flex-direction: column;
        gap: 4px;
        flex-shrink: 0;
        min-width: 60px;
      }
      .room-spec-t {
        flex: 1;
        font-family: var(--serif);
        font-size: 14px;
        margin: 0;
        line-height: 1.4;
      }
      .room-spec-tog {
        font-family: var(--mono);
        font-size: 16px;
        line-height: 1;
        flex-shrink: 0;
        padding-top: 2px;
      }
      .room-spec-body {
        padding: 0 14px 14px 86px;
        border-top: 1px solid var(--line-soft);
      }
      .room-spec-s {
        font-family: var(--serif);
        font-size: 13px;
        line-height: 1.5;
        margin: 12px 0 8px;
        color: var(--ink-soft);
      }
      .room-spec-go {
        background: transparent;
        border: 1px solid var(--ink);
        color: var(--ink);
        padding: 6px 10px;
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        cursor: pointer;
        border-radius: 2px;
        min-height: 32px;
      }
      .room-spec-go:hover { background: var(--ink); color: var(--bone); }
      .room-spec-go:focus-visible {
        outline: 2px solid var(--ink);
        outline-offset: 2px;
      }

      .back-btn {
        background: transparent;
        border: 1px solid var(--ink);
        color: var(--ink);
        padding: 8px 14px;
        font-family: var(--mono);
        font-size: 11px;
        cursor: pointer;
        margin: 20px;
      }

      /* ─── Reduced motion ─── */
      @media (prefers-reduced-motion: reduce) {
        * {
          animation-duration: 0.01ms !important;
          animation-iteration-count: 1 !important;
          transition-duration: 0.01ms !important;
          scroll-behavior: auto !important;
        }
      }
    `}</style>
  );
}
