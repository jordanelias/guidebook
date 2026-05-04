# FDR Findings — reach-range-and-accessible-controls
**Slug:** `reach-range-and-accessible-controls`
**Topic directory:** `controls-and-hardware`
**FDR run date:** 2026-04-08
**Scenarios run:** 3
**Status:** PARTIAL — grip/controls and laterality/UPL complete; tremor and fine-motor scenarios not yet run

---

## FDR-RRC-01 — d440 + reduced grip force → controls (switches / outlets / door hardware)

**Sources:** ADA §309.4; ICC A117.1-2017 §404.2.7; US Access Board ADA Guide (advisory); BS 8300 (UK)

| Parameter | Value | Condition | Source | Tier | Delta |
|---|---|---|---|---|---|
| Rotational hardware torque limit | ≤28 inch-pounds (≤3.16 N·m) | Lever handles, rotational controls — grip-deficit users cannot overcome higher torque | ICC A117.1-2017 §404.2.7 | Tier 5 | **NOVEL** — torque-specific limit absent from slug BPC; force-only previously recorded |
| Forward push/pull hardware force | ≤66.7 N (15 lbf) | Panic hardware, push bars, forward-actuated controls — distinct force category from rotational | ICC A117.1-2017 §404.2.7 | Tier 5 | **NOVEL** — this force category absent from BPC |
| Knuckle clearance behind hardware | ≥38mm (1½ inch) min | Bars, pulls, all door hardware — enables grip without finger scraping; essential for reduced ROM | US Access Board ADA Guide (advisory) | Tier 5 | **NOVEL** — clearance dimension absent from BPC |
| Lever handle grip diameter | ≥19mm | Reduced grip span; permits wrap-grip without fine-motor engagement | BS 8300 (UK advisory) | Tier 5 | **NOVEL** — grip diameter spec absent from BPC |
| Hardware shape | Closed-fist or loose-grip operable; no tight pinch, wrist twist, or simultaneous multi-action | All grip-deficit functional profiles | ADA §309.4; ICC A117.1 | Tier 5 | CONFIRMS existing BPC prose — no new spatial parameter |

**Universal Mode candidates:** Rotational torque ≤28 in-lb; knuckle clearance ≥38mm. Both apply across grip-deficit functional profiles with no known counter-indication. Route to connection-scout.

---

## FDR-RRC-02 — d440 + dominant hand loss of function → controls (laterality-specific placement)

**GAP — Inherently individualized**

No built environment literature identified specifying laterality-sensitive switch or socket placement (i.e., mounting position relative to the user's functional side). OT literature covers adaptive equipment prescription and rehabilitation protocols, not architectural mounting position by affected side.

The design problem cannot be resolved at a population level: the functional side varies per individual and is not predictable at design stage. This is a Tier 2 individual-assessment problem, not a Tier 5/6 architectural specification problem.

[GAP: laterality-specific control positioning — inherently individualized; architectural standardisation not possible without individual assessment; Mode S OT prescription only]

---

## FDR-RRC-03 — d445 + unilateral UPL + prosthesis → controls (reach envelope)

**GAP — Device-variable; not standardisable**

UPL prosthesis OT literature covers rehabilitation protocols, AT training, and prosthesis prescription. No spatial reach-envelope modifications to built environment controls were identified. Functional reach envelope varies substantially by device type (body-powered vs. myoelectric), amputation level, and individual training. No single architectural specification is extractable.

Existing BPC reach range dimensions (380–1220mm AFH) remain applicable as the baseline; individual prosthesis users may need custom assessment.

[GAP: UPL prosthesis reach envelope — too device-variable for architectural specification; existing reach-range BPC dimensions are the appropriate baseline; Tier 2 individual assessment required for deviations]

---

## FDR-RRC-04 — d440 + tremor / fine motor deficit → controls (switches, outlets)

**Sources:** IETF OT perspective (essentialtremor.org); OccupationalTherapy.com Essential Tremor course (Article 4913); Steadiwear OT guide (2025)

**Clinical reasoning extracted:** OT intervention for tremor targets reducing precision demand on controls and stabilising the proximal before the distal. Two environmental design implications follow directly.

| Parameter | Value | Condition | Source | Tier | Delta |
|---|---|---|---|---|---|
| Switch face area — preferred type | Large rocker / paddle switch; minimum face dimension ≥50mm | Tremor: larger target reduces miss-activation; less precision required per activation | IETF OT Perspective; OT clinical reasoning (essentialtremor.org) | Co-2 | **NOVEL** — switch face size as tremor-mitigation parameter absent from BPC |
| Adjacent stabilising surface near control | Shelf, sill, or counter at elbow height (≈900–1000mm AFH) within reach of control | OT clinical reasoning: stabilise core/arm before operating control; surface within reach enables forearm support prior to activation | IETF OT Perspective; OccupationalTherapy.com ET course | Co-2 | **NOVEL** — proximal stabilisation surface as design enabler absent from BPC |
| Voice-activated / motion-sensor controls | Eliminates fine motor contact requirement entirely | Severe tremor where contact-based control is unreliable; also applicable to high-spasticity | OT clinical reasoning (multiple sources) | Co-2 | REFINES — existing BPC notes automation; adds clinical reasoning basis specific to tremor |

**Clinical reasoning note:** OT consistently applies proximal-to-distal stabilisation strategy for tremor — core stable, then shoulder, then elbow, then hand. The architectural corollary is that the environment should provide a stable surface for the proximal limb segment adjacent to any fine-motor control. This is not currently specified anywhere in standards literature.

---

## FDR-RRC-05 — d445 + bilateral upper limb weakness → counter / shelf reach

**Sources:** France+Associates case study (Alice — limb amputation, OT-architect co-production, 2022) [single case]; PVA SCI Upper Limb Preservation CPG (Physiopedia / PVA 2021) [Tier 4 CPG]; Rehab Management OT case (Petito, OTR/L) [single case]; Koontz et al. transfer height consensus [Tier 2 SR]

| Parameter | Value | Condition | Source | Tier | Delta |
|---|---|---|---|---|---|
| Standard worktop height — inaccessible threshold | 900mm AFH is too tall for most wheelchair users with bilateral UPL weakness | Bilateral UPL weakness + seated position; reach and force both compromised | France+Associates case study (2022) | Case | **NOVEL** — population-agnostic mechanism; 900mm as exclusionary threshold documented via case clinical reasoning |
| Preferred worktop height — seated user | Lower counters or height-adjustable worktops; individual assessment required | Bilateral UPL weakness; WC seat height varies individually | France+Associates case; Rehab Management OT case (Petito) | Case/Co-2 | REFINES — adjustable worktop already in kitchen BPC; adds clinical reasoning from UPL-specific bilateral weakness |
| Overhead storage ceiling — bilateral UPL | ≤shoulder height of seated user; avoid any overhead reach for bilateral UPL users | Upper limb preservation: avoid arm above shoulder height; overhead reach increases shoulder injury risk | PVA SCI Upper Limb Preservation CPG (Physiopedia) | Tier 4 CPG | **NOVEL** — overhead reach prohibition for bilateral UPL absent from reach-range BPC as a clinical rationale |
| Transfer surface height — level transfer principle | Transfer surface height should match wheelchair seat height (approx. 430–500mm) | Bilateral UPL: transferring to higher surface significantly increases upper limb exertion; level transfer minimises load | Koontz et al. cited in PMC4562294 (SR consensus) | Tier 2 | REFINES — transfer height in bathroom BPC; adds bilateral UPL mechanism and broader spatial application |
| Knee clearance — individualized to WC geometry | Counter/table knee clearance individualized: floor-to-seat height + thigh height + cushion depth = required knee clearance | Power WC users: footplate ground clearance ≥75mm; thigh height varies; standard 680mm may be insufficient for tall users | Rehab Management OT case (Petito, OTR/L) | Case/Co-2 | **NOVEL** — individualized knee clearance calculation method absent from BPC; standard 680mm shown insufficient in case |

**Clinical reasoning note (Petito case):** Community OT/wheelchair specialist documents that WC assessment must include home environment measurement — counter height is determined by wheelchair geometry, not by population average. This is the clinical reasoning basis for why adjustable worktops are best practice, not optional.
