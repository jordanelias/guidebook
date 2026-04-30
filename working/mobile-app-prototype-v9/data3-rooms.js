// ROOMS_SYNTHESIS — design synthesis data for all 14 rooms
// Merged at access time with the static room records in BUILDINGS

export const ROOMS_SYNTHESIS = {

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
