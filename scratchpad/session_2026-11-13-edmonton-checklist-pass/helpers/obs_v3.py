"""Steps 2 and 3, third run: every numbered item (derived from items.json), every figure, and the
statements and group phrases the second critic found missing (F3, F7), observed in ONE pass, then
adjudicated once each.

Adjudication rule of this run (REPLAY-V3-BRIEF F2):
  * NAMES-EXISTING wherever the phrase names the concept a held term defines, whether or not that
    term is a parameter or declined. Where it is neither, R16 goes red for it; that red is the
    owner conflict OD-53 and is reported, not worked around (no decline, no promotion).
  * DEFERRED only with a rationale that says why it is held: colour contrast against LRV contrast
    (unsettled on this source); the two "path of travel" phrases (OD-52, OT-1, OT-2); a quantity
    with no term or parameter (OD-50, and this batch mints no term); an element with no held term
    (this batch mints no term: a withheld act, said so plainly); a group phrase (no term exists for
    the group; the identity registry holds it, which an adjudication cannot name).
  * NOT-OURS for a real phrase that is not one of the project's concepts (strollers).
Surface forms exactly as printed; context quotes verbatim from the derived text."""
import json, sys, sqlite3
from common import run, loc, STEM, REF, DB, SESS

EX, DF, NO = 'NAMES-EXISTING', 'DEFERRED', 'NOT-OURS'

QTY = ("A quantity the source states a figure for; the catalogue holds no term or parameter for it. "
       "Whether a source that is not a code may add a parameter is the owner's open question OD-50. "
       "This batch mints no term, so the phrase is held DEFERRED; the concept itself is settled on this "
       "source (ADJUDICATION Q2 item 2 names add-term --from-observation as the act), so DEFERRED here "
       "records a withheld act, not an unsettled reading. The figure is kept verbatim in the context quote.")
ELEM = ("An element or provision the source requires, with no figure; the catalogue holds no term for it. "
        "This batch mints no term, so the phrase is held DEFERRED; the concept is settled on this source "
        "(ADJUDICATION Q2 item 2 names add-term --from-observation as the act), so DEFERRED here records a "
        "withheld act, not an unsettled reading.")
CONTRAST = ("The source asks for colour contrast and states no figure and no measure. Whether this colour "
            "contrast names TERM-011 LRV contrast (a light reflectance value difference) cannot be settled on "
            "this source alone: it does not say whether the contrast meant is of reflectance, of hue or of pattern.")
PATH = ("OT-1 and OT-2 place the owner's term 'Barrier-free path of travel' as a circulation route through a "
        "building, specific to wheelchair and mobility-device users. This source uses the phrase for the "
        "exterior route from parking or drop-off to the entrance. Whether this use names that term is the "
        "owner's open question OD-52. Not adjudicated to TERM-048; the term is not minted.")


def near(t, n, why):
    return f' The nearest held term, {t} ({n}), is not what the phrase names: {why}.'


def names(t, n, why):
    return (f'{why} {t} ({n}) is held and is neither a parameter nor declined, so R16 reads it as undisposed. '
            f'This batch neither promotes nor declines it: whether a single-source batch may decline a held term '
            f'is the owner\'s open question OD-53. R16\'s red for this term is reported, not worked around.')


def group(code, disp, extra=''):
    return (f"A group of disabled people, not an element or a quantity. The identity registry holds the group as "
            f"{code} ('{disp}'); a term adjudication can point only at a term, the catalogue holds no term for "
            f"this group, and so no outcome but DEFERRED fits. The group reaches a row only as a lens on a figure "
            f"(extraction_lens_links), and this clause has no figure the catalogue holds.{extra}")


P1_TURN = 'For example, a wider turning radius and wider doors are required by many wheelchairs and scooters today.'
P1_DEV = 'For example, people with low vision, people who use different mobility devices (scooters/ walkers/wheelchairs) etc.'
P1_CATS = 'Physical Access Deaf or Hard of Hearing Access Blind or Low Vision Access Cognitive Limitations Access'
CATS_WHY = (" The four access category names stand in the PDF text layer of page 1 in white (colour ffffff, read "
            "with PyMuPDF in this run) beside the LEGEND, and are not visible in render p0000 (read in this run); "
            "no checklist item carries them. [NOT VERIFIED] whether they label the four logo figures at the top of the page.")
I45 = ('Ensure any open area beneath the stairs is enclosed with planters, railings, benches, fencing etc to ensure no '
       'access. Tactile strips under the stairs on the ground and a contrasting colour on the back of the stairwell '
       'above the tactile strips to alert a potential safety hazard')
I85 = ('Accessible sink (minimum knee space of 735mm/29”) with soap and towel dispenser close to sink at preferred '
       'height of 1200mm/47”. Include a low mounted or tilt mirror 1000mm/39” above floor and insulate any exposed pipes. '
       'Automatic or sensor operated faucets preferred')

# (surface form as printed, item, context quote verbatim, outcome, term, rationale)
OBS = [
 # ---- page 1
 ('Universal Design', 'p1', 'The City of Edmonton Accessibility Advisory Committee (AAC) has created this checklist to promote the concepts of Universal Design.', EX, 'TERM-017',
  names('TERM-017', 'universal design', 'The source promotes the concepts of Universal Design; TERM-017 universal design is "Design usable by all people without adaptation".')),
 ('wider turning radius', 'p1', P1_TURN, EX, 'TERM-003', 'The space a wheelchair or scooter needs to turn; TERM-003 turning circle (parameter 5) is the space for wheelchair rotation.'),
 ('wider doors', 'p1', P1_TURN, EX, 'TERM-021', 'The width of doors as the source contrasts it with the minimum standards; TERM-021 door width (parameter 9).'),
 ('Strollers for children', 'p1', 'Strollers for children are larger and require more room for maneuverability.', NO, None,
  'A real phrase, not one of the project\'s concepts: strollers are not a disability group or an access need. The source cites them as a further reason to exceed minimum standards; no figure is attached.'),
 ('people with low vision', 'p1', P1_DEV, DF, None, group('BLIND', 'blind and low-vision people')),
 ('mobility devices', 'p1', P1_DEV, EX, 'TERM-079',
  names('TERM-079', 'mobility aid', 'The source names "different mobility devices (scooters/ walkers/wheelchairs)"; TERM-079 mobility aid is a "Device supporting locomotion or transfer".')),
 ('Physical Access', 'p1', P1_CATS, DF, None, 'An access category label, naming no single identity group or access need held in the registries.' + CATS_WHY),
 ('Deaf or Hard of Hearing Access', 'p1', P1_CATS, DF, None, group('DEAF', 'Deaf and hard-of-hearing people', CATS_WHY)),
 ('Blind or Low Vision Access', 'p1', P1_CATS, DF, None, group('BLIND', 'blind and low-vision people', CATS_WHY)),
 ('Cognitive Limitations Access', 'p1', P1_CATS, DF, None, 'An access category label naming cognitive access; no single identity code holds "cognitive limitations" (ID, BRAIN, DEM and NDV each hold part).' + CATS_WHY),
 # ---- 1. parking
 ('barrier-free parking spaces', '1.1', 'Designated barrier-free parking spaces located closest to barrier-free entrance', EX, 'TERM-027',
  names('TERM-027', 'accessible parking', 'Designated barrier-free parking spaces; TERM-027 accessible parking is "Designated parking for disabled drivers/passengers".')),
 ('Barrier-free unobstructed path of travel', '1.2', 'Barrier-free unobstructed path of travel (minimum width of 1500mm/59”) from parking area to building entrance (clear of snow, garbage cans, sign posts and other obstacles; pathway well lit; not behind vehicles).', DF, None, PATH),
 ('minimum width', '1.2', 'Barrier-free unobstructed path of travel (minimum width of 1500mm/59”) from parking area to building entrance (clear of snow, garbage cans, sign posts and other obstacles; pathway well lit; not behind vehicles).', DF, None,
  'The width of the item 1.2 path. Not adjudicated to TERM-002 corridor width while the owner has not said which route term this path is (OD-52): whether its width is the clear width of the circulation route TERM-002 defines waits on that answer. The 1500 mm figure is parked (OD-47), not written.'),
 ('colour contrast', '1.2', 'Pathway shall have colour contrast and distinctive patterns where there are changes in level and surface material', DF, None, CONTRAST),
 ('Curb ramp', '1.3', 'Curb ramp to sidewalk located between parking spaces', EX, 'TERM-089', 'A curb ramp is an inclined surface built as a discrete element to bridge a level difference on a route; TERM-089 ramp, declined as a parameter (an element).'),
 ('Access aisle painted on pavement', '1.4', 'Access aisle painted on pavement between barrier-free parking spaces', DF, None, ELEM),
 ('Accessible parking symbols', '1.5', 'Accessible parking symbols painted on pavement at the entrance of each stall. The symbol and any associated background paint should not occupy the entire area. The more painted surface, the more likely pavement will become slippery', DF, None, ELEM + ' The item also states a slip hazard (R7), recorded on the search and in a gap.'),
 ('Vertically mounted sign', '1.6', 'Vertically mounted sign showing accessibility symbol located near the centre line of each designated stall (minimum 1500mm/60” from ground to mid sign, max 2500mm/98” high)', DF, None, QTY),
 ('Number of designated accessible parking spaces per number of parking stalls', '1.7', 'Number of designated accessible parking spaces per number of parking stalls: 1 accessible stall per 2-10 spaces, 2 per 11-25 spaces, 2 per 26-50 and 4 per 51-100. One additional accessible stall for each additional increment of 100 or part thereof', DF, None, QTY + ' A count, a kind no held parameter has.'),
 ('access aisle', '1.8', 'Passenger loading zones need: an access aisle not less than 1500mm/59” to 6000mm/236” long adjacent and parallel to the vehicle pull-up space, a curb ramp where there are curbs between the access aisle and the vehicle pull-up space and a clear height of not less than 2750mm/108” at the pull-up space and along the vertical access and egress routes', DF, None, QTY),
 ('clear height', '1.8', 'Passenger loading zones need: an access aisle not less than 1500mm/59” to 6000mm/236” long adjacent and parallel to the vehicle pull-up space, a curb ramp where there are curbs between the access aisle and the vehicle pull-up space and a clear height of not less than 2750mm/108” at the pull-up space and along the vertical access and egress routes', EX, 'TERM-061', 'An unobstructed vertical dimension above a route; TERM-061 headroom clearance (parameter 11).'),
 ('directional signs', '1.9', 'If the location of designated parking stalls is not easily visible from the approach viewpoint, appropriate directional signs showing location of designated stalls shall be provided', DF, None,
  ELEM + near('TERM-028', 'wayfinding', 'it is the system that enables navigation, of which directional signs are one part')),
 ('clear accessible path', '1.10', 'Ensure there is a clear accessible path between accessible stalls and the payment machine', DF, None,
  'A route between the stalls and the payment machine. Which route term this document\'s paths name is before the owner as OD-52 (the item 1.2 and 2.1 phrases); this phrase waits on the same answer.'),
 ('Information for parking payment', '1.11', 'Information for parking payment is easy to understand and clearly visible for accessible stalls', DF, None, ELEM),
 # ---- 2. entrances
 ('Barrier-free path of travel', '2.1', 'Barrier-free path of travel from parking and/or drop off zone to entrance', DF, None, PATH),
 ('Signage at all non-accessible entrances', '2.2', 'Signage at all non-accessible entrances should clearly indicate location of barrier-free entrance', DF, None, ELEM),
 ('Doorway clearance', '2.3', 'Doorway clearance is 850mm when the door is in the open 90 degree position (920mm/36” preferred)', EX, 'TERM-021', 'The clear opening of a doorway with the door open to 90 degrees; TERM-021 door width (parameter 9).'),
 ('Door operating device', '2.4', 'Door operating device should not require tight grasping or twisting of the wrist (doors should have lever handles)', DF, None, ELEM),
 ('tight grasping or twisting of the wrist', '2.4', 'Door operating device should not require tight grasping or twisting of the wrist (doors should have lever handles)', EX, 'TERM-088',
  names('TERM-088', 'upper limb function and grip', 'The clause names a grip and a wrist movement the door hardware must not demand; TERM-088 upper limb function and grip is "Hand, wrist and arm capability governing operable force, grip type and one-handed use".')),
 ('lever handles', '2.4', 'Door operating device should not require tight grasping or twisting of the wrist (doors should have lever handles)', EX, 'TERM-004',
  names('TERM-004', 'lever handle', 'TERM-004 lever handle is "Door handle operable without grip/twist motion", which is what the clause asks for.')),
 ('automatic sliding doors', '2.5', 'The primary entrance is barrier-free (automatic sliding doors are optimal; power doors with large paddle/push plate is the next best alternative, wave to open preferred where feasible)', DF, None, ELEM),
 ('pedestrian entrances', '2.6', 'In addition to the barrier-free entrances required, not less than 50% of the pedestrian entrances, including the primary entrance of a building, including walkways leading to the entrances from a public thoroughfare and from on-site parking areas, shall be barrier-free', DF, None, QTY + ' A proportion of entrances, a kind no held parameter has.'),
 ('vestibule', '2.7', 'If entrance is through doors in a series, leave enough room (1200mm/47” plus the width of the door) for a wheelchair to occupy the vestibule while opening the 2nd door', DF, None, QTY),
 ('Automatic door operator button', '2.8', 'Automatic door operator button is 800mm/31.5”-1500mm/59” from the ground and is located 1500mm/59” back from the door.', DF, None, QTY),
 ('doorway threshold', '2.9', 'Level, or beveled doorway threshold (maximum of 13mm/0.5” rise)', DF, None,
  QTY + near('TERM-022', 'level threshold', 'its definition is "Zero-step entry at doorway", and this item allows a bevelled 13 mm rise')),
 ('Colour contrast', '2.10', 'Colour contrast to identify doorway threshold, frame or entrance.', DF, None, CONTRAST),
 ('Corridors should be 1100mm/43”', '2.10', 'Corridors should be 1100mm/43” (recommend 1800mm/71”)', EX, 'TERM-002', 'The width of corridors; TERM-002 corridor width (parameter 4).'),
 # ---- 3. signage
 ('assistive listening devices', '3.1', 'Facilities and services for persons with disabilities identified with appropriate symbols (e.g. availability of assistive listening devices)', DF, None,
  ELEM + near('TERM-006', 'hearing loop', 'a hearing loop is one kind of assistive listening device; the phrase names the class')),
 ('Signage available in symbol form', '3.2', 'Signage available in symbol form for those with visual processing difficulties or who are unable to read', EX, 'TERM-019',
  names('TERM-019', 'pictogram signage', 'Signage in symbol form; TERM-019 pictogram signage is "Simplified graphic symbols for wayfinding".')),
 ('those with visual processing difficulties or who are unable to read', '3.2', 'Signage available in symbol form for those with visual processing difficulties or who are unable to read', DF, None,
  'A group named by two functions (visual processing; reading), not an element or a quantity. No identity code holds it as one group (it spans BLIND, ID, BRAIN, NDV and people who do not read the language), and a term adjudication can point only at a term, of which the catalogue holds none for it. The clause has no figure, so no lens link can carry it.'),
 ('braille', '3.3', 'Signage includes braille as well as large print, high colour contrast tactile lettering that is a mix of caps and lower case letters and is designed to prevent glare', DF, None, ELEM),
 ('high colour contrast tactile lettering', '3.3', 'Signage includes braille as well as large print, high colour contrast tactile lettering that is a mix of caps and lower case letters and is designed to prevent glare', DF, None, CONTRAST),
 ('way-finding signage', '3.4', 'General and way-finding signage consistent in design and easily identifiable', DF, None,
  ELEM + near('TERM-028', 'wayfinding', 'it is the system that enables navigation; the phrase names the signage, one part of it')),
 ('Braille signage', '3.5', 'Braille signage mounted at appropriate height (chest level) and location', DF, None, ELEM),
 ('Signage font in Sans Serif', '3.6', 'Signage font in Sans Serif (e.g., Verdana, Arial) for reading ease.', DF, None, ELEM),
 ('Signage should be 1350mm/51” high from floor level', '3.6', 'Signage should be 1350mm/51” high from floor level and not located on a door (should be 150mm/6” from the door frame).', DF, None, QTY),
 ('tactile signage', '3.6', 'If tactile signage is installed it should be 1200mm/47” from floor level (building directories should be tactile)', DF, None, QTY),
 # ---- 4. stairs
 ('Slip-resistant', '4.1', 'Slip-resistant, tactile finish or strips contrasting in colour and texture on all landings, tread edges/stair nosings, and the beginning and end of a ramp.', DF, None, QTY + ' Slip resistance, stated with no figure.'),
 ('tactile finish or strips', '4.1', 'Slip-resistant, tactile finish or strips contrasting in colour and texture on all landings, tread edges/stair nosings, and the beginning and end of a ramp.', EX, 'TERM-010',
  names('TERM-010', 'tactile walking surface indicator', 'A tactile finish or strips on landings, nosings and at the ends of a ramp; TERM-010 is a "Ground surface detectable by foot or cane for guidance/warning".')),
 ('tactile strips', '4.1', 'Changes in elevation at stairwells shall be indicated by tactile strips, which are as wide as the stair and have colour contrast', EX, 'TERM-010',
  names('TERM-010', 'tactile walking surface indicator', 'Strips indicating a change in elevation at a stairwell; TERM-010 is a "Ground surface detectable by foot or cane for guidance/warning".')),
 ('Step demarcation in yellow', '4.2', 'Step demarcation in yellow on sides and back of escalator steps', DF, None, ELEM),
 ('rise between 125mm/5” and 180mm/7”', '4.3', 'Steps for stairs have a rise between 125mm/5” and 180mm/7” and a run of not less than 280mm/11” (should not be open between steps).', DF, None, QTY),
 ('run of not less than 280mm/11”', '4.3', 'Steps for stairs have a rise between 125mm/5” and 180mm/7” and a run of not less than 280mm/11” (should not be open between steps).', DF, None, QTY),
 ('Avoid single isolated steps', '4.3', 'Avoid single isolated steps', DF, None, ELEM + ' The statement warns against a hazard (R7), recorded on the search and in a gap.'),
 ('Illumination', '4.4', 'Illumination shall be positioned to minimize glare and shadow', DF, None, ELEM),
 ('open area beneath the stairs', '4.5', I45, DF, None, ELEM + ' The item states a hazard (R7), recorded on the search and in a gap in the source\'s words.'),
 ('Tactile strips under the stairs on the ground', '4.5', I45, EX, 'TERM-010',
  names('TERM-010', 'tactile walking surface indicator', 'Tactile strips on the ground under the stairs, to alert a hazard; TERM-010 is a "Ground surface detectable by foot or cane for guidance/warning".')),
 ('contrasting colour on the back of the stairwell', '4.5', I45, DF, None, CONTRAST),
 ('Carpet', '4.6', 'Carpet is securely attached', DF, None, ELEM),
 ('handrails on both sides', '4.7', 'A stairway shall have a handrail on at least one side, but if it is 1100mm/43” or more wide, it shall have handrails on both sides.', DF, None, QTY + ' A count of handrails conditioned on a stair width; neither a count kind nor a stair-width parameter is held (ADJUDICATION A5).'),
 ('colour contrast from wall and surrounding environment', '4.7', 'Handrails should be splinter and rust proof, located on both sides of the stairs and ramps, and have a colour contrast from wall and surrounding environment.', DF, None, CONTRAST),
 ('tactile cues', '4.8', 'Handrails should have a system of tactile cues (texture changes) within 300mm/12” from each end', DF, None, QTY),
 # ---- 5. elevators
 ('clear colour contrast', '5.1', 'Doors have clear colour contrast from door surroundings', DF, None, CONTRAST),
 ('Location of elevators', '5.2', 'Location of elevators clearly identified at main entrance', DF, None,
  ELEM + near('TERM-014', 'accessible lift', 'the phrase names how the elevators are found, not the elevator')),
 ('turning radius', '5.3', 'Preferred dimension of elevator car to allow for optimal turning radius of 1500x1500mm/60x60” with elevator door at least 910 – 915mm/36” wide', EX, 'TERM-003', 'The source calls a 1500 x 1500 mm car the space for a turning radius; TERM-003 turning circle (parameter 5) is the space for wheelchair rotation.'),
 ('elevator door at least 910 – 915mm/36” wide', '5.3', 'Preferred dimension of elevator car to allow for optimal turning radius of 1500x1500mm/60x60” with elevator door at least 910 – 915mm/36” wide', EX, 'TERM-021', 'The clear width of an elevator door; TERM-021 door width (parameter 9).'),
 ('stretcher', '5.3', '(one elevator has inside dimensions that will accommodate a stretcher at 2010mm/79” long and 610mm/24” wide) 1828mm/72” by 2032mm/80”', DF, None, QTY + ' Elevator car inside dimensions.'),
 ('Elevator buttons and emergency controls mounted at an accessible height', '5.4', 'Elevator buttons and emergency controls mounted at an accessible height (1045mm/41”-1095mm/43” from ground)', DF, None, QTY),
 ('large print tactile numbers and Braille', '5.5', 'Elevator buttons and emergency controls incorporate large print tactile numbers and Braille mounted in a raised fashion (not flush or recessed).', DF, None, ELEM),
 ('Colour contrast', '5.5', 'Colour contrast shall be used to identify the floor registration button panel from background, call buttons should protrude from adjacent surface', DF, None, CONTRAST),
 ('Braille and tactile numbers', '5.6', 'Braille and tactile numbers placed on both sides of door jambs at appropriate height to identify floor level', DF, None, ELEM),
 ('Visual indicator in elevators', '5.7', 'Visual indicator in elevators to indicate “help on the way” for use in an emergency', DF, None, ELEM),
 ('Audible communication system', '5.8', 'Audible communication system shall be available for accessing elevators, inside the car and have an announcement identifying the direction of travel and floors', DF, None, ELEM),
 ('Elevator waiting areas should have seating', '5.9', 'Elevator waiting areas should have seating in close proximity', DF, None,
  ELEM + near('TERM-052', 'rest point seating', 'it is seating at intervals along a route; this is seating at a waiting area')),
 ('Elevator doors shall begin to close', '5.10', 'Elevator doors shall begin to close after a minimum of 8 seconds from the fully open position', DF, None, QTY + ' A door dwell time.'),
 # ---- 6. ramps
 ('Ramps', '6.1', 'Ramps are used for any slope steeper than 1 in 20 in a path of travel.', EX, 'TERM-089', 'TERM-089 ramp, declined as a parameter (an element).'),
 ('Preferred maximum slope', '6.1', 'Preferred maximum slope is 1 in 16 (1 in 12 in AB building code)', EX, 'TERM-001', 'The slope of a ramp; TERM-001 ramp gradient (parameter 3).'),
 ('With the ramp at any point', '6.2', 'With the ramp at any point shall not be less than 1500mm/60”; 870mm/34” min clearspace between handrails.', DF, None,
  'The sentence as printed has no subject noun, so what its 1500 mm measures (a ramp width is the likeliest reading) cannot be settled on this source alone. Decided once for this run: the 1500 mm is held here as an observation only and is neither written nor parked as an extraction.'),
 ('clearspace between handrails', '6.2', 'With the ramp at any point shall not be less than 1500mm/60”; 870mm/34” min clearspace between handrails.', EX, 'TERM-002', 'The clear width of a ramp between its handrails; TERM-002 corridor width (parameter 4), which already holds a ramp width between handrails (canonical extraction 192, REF-00987, setting "ramp run; between handrails").'),
 ('Level landings/ resting areas provided at 9m/10yd intervals along ramp', '6.2', 'Level landings/ resting areas provided at 9m/10yd intervals along ramp', EX, 'TERM-091', 'The interval between landings along a ramp is the length of a flight between landings; TERM-091 ramp run length (parameter 12).'),
 ('tight turns or switch-backs', '6.3', 'Minimize or avoid tight turns or switch-backs', DF, None, ELEM),
 ('15mm/0.6” wide strip', '6.4', 'Strong colour contrast and tactile surfacing on all ramp landings and a 15mm/0.6” wide strip in contrasting colour and texture at the top of ramp to warn users of a change in elevation', DF, None, QTY),
 ('Strong colour contrast', '6.4', 'Strong colour contrast and tactile surfacing on all ramp landings and a 15mm/0.6” wide strip in contrasting colour and texture at the top of ramp to warn users of a change in elevation', DF, None, CONTRAST),
 ('able to open doors without backing onto ramp', '6.5', 'Landings designed to accommodate larger chairs and scooters (able to open doors without backing onto ramp).', DF, None, ELEM + ' The statement names a hazard (backing onto the ramp) the landing is sized to prevent (R7), recorded on the search and in a gap.'),
 ('Landings must be min 1200mm/47”long', '6.5', 'Landings must be min 1200mm/47”long and same width as the ramp', DF, None,
  QTY + near('TERM-092', 'intermediate landing', 'it is a platform between successive ramp runs; these landings are those at doors, at the ends of the ramp')),
 # ---- 7. handrails
 ('diameter', '7.1', 'Handrails should have a diameter not less than 30mm/1.18” or more than 43mm/1.69”', DF, None, QTY),
 ('handrails on both sides', '7.1', 'A stairway should have a handrail on at least one side but if it is 1100mm or more wide it shall have handrails on both sides and are continuously graspable.', DF, None, QTY + ' A count of handrails conditioned on a stair width (ADJUDICATION A5).'),
 ('contrasting colour', '7.2', 'Handrails in contrasting colour to wall or surrounding area', DF, None, CONTRAST),
 ('Handrails provided at two heights', '7.3', 'Handrails provided at two heights with an unobscured view between.', DF, None, ELEM),
 ('Handrail height', '7.3', 'Handrail height should be 865mm/34” and no more than 965mm/38”', DF, None, QTY),
 ('Handrails extend horizontally', '7.4', 'Handrails extend horizontally beyond last stair and terminate to wall or ground', DF, None, ELEM),
 # ---- 8. washrooms
 ('wave to open or push button', '8.1', 'Have a wave to open or push button available', DF, None, ELEM),
 ('only one turn with clear corner', '8.2', 'For washrooms without entrance door, there is only one turn with clear corner so persons who are blind do not become disoriented', DF, None, ELEM + ' The clause states a harm it prevents (R7), recorded on the search and in a gap.'),
 ('persons who are blind', '8.2', 'For washrooms without entrance door, there is only one turn with clear corner so persons who are blind do not become disoriented', DF, None, group('BLIND', 'blind and low-vision people')),
 ('Proper signage', '8.3', 'Proper signage located outside the entrance and stall door', DF, None, ELEM),
 ('located around perimeter', '8.4', 'Sinks, garbage cans, etc. located around perimeter rather than in the centre of the room', DF, None, ELEM),
 ('knee space', '8.5', I85, DF, None, QTY),
 ('soap and towel dispenser', '8.5', I85, DF, None, QTY),
 ('low mounted or tilt mirror', '8.5', I85, DF, None, QTY),
 ('insulate any exposed pipes', '8.5', I85, DF, None, ELEM + ' The provision guards against a hazard the source does not name (R7 statement of its kind), recorded on the search and in a gap in the source\'s words.'),
 ('Automatic or sensor operated faucets', '8.5', I85, DF, None, ELEM),
 ('ACCESSIBLE WASHROOM STALL', '8.6', 'ACCESSIBLE WASHROOM STALL:', DF, None, ELEM + near('TERM-009', 'accessible bathroom', 'it is a room; the phrase names a stall within one (ADJUDICATION A4, F12)')),
 ('minimum 1700mm x 1500mm/70 x 60”', '8.6', 'minimum 1700mm x 1500mm/70 x 60”', DF, None, QTY + ' The size of the accessible washroom stall.'),
 ('person with limited mobility', '8.6', 'door that swings outward so person with limited mobility can close it independently', DF, None, group('MOB', 'disabled people with mobility needs; wheelchair users')),
 ('grab bars', '8.6', 'equipped with door pull handle, coat hook, grab bars at various appropriate heights and placement', EX, 'TERM-008',
  names('TERM-008', 'grab bar', 'TERM-008 grab bar is a "Support rail for transfer and balance in bathrooms".')),
 ('large, sliding latch (not thumb-turning)', '8.6', 'can be locked from the inside with a large, sliding latch (not thumb-turning)', DF, None, ELEM),
 ('toilet paper reachable without leaning too far off toilet', '8.6', 'toilet paper reachable without leaning too far off toilet', DF, None, ELEM + ' The bullet also states the hazard it avoids (leaning too far off the toilet; R7), recorded on the search and in a gap.'),
 ('accessible toilet height', '8.6', 'accessible toilet height between 400mm-460mm/16”-18”', DF, None, QTY),
 ('various toilet size and heights', '8.6', 'various toilet size and heights. Or adding a step stool option if unavailable.', DF, None, ELEM),
 ('vertically mounted grab bar', '8.6', 'at least one urinal should have a vertically mounted grab bar installed on each side', EX, 'TERM-008',
  names('TERM-008', 'grab bar', 'A grab bar at a urinal; TERM-008 grab bar is a "Support rail for transfer and balance in bathrooms".')),
 ('Call buttons', '8.6', 'Call buttons shall be installed in all barrier-free washroom stalls for facilities (which are staffed with security) during open hours', DF, None, ELEM),
 ('gender inclusive/family washroom', '8.7', 'Self-contained, gender inclusive/family washroom available, with proper signage provided in an accessible location', DF, None, ELEM),
 # ---- 9. interior
 ('Public and emergency phones', '9.1', 'Public and emergency phones mounted at an accessible height with a minimum of 865mm/34” and a maximum of 1370mm/54 above the floor', DF, None, QTY),
 ('TTY', '9.2', 'TTY (built in typewriter) phone for users who are Deaf or hard of hearing.', DF, None, ELEM),
 ('users who are Deaf or hard of hearing', '9.2', 'TTY (built in typewriter) phone for users who are Deaf or hard of hearing.', DF, None, group('DEAF', 'Deaf and hard-of-hearing people')),
 ('live captioning', '9.2', 'Video Relay Service (VRS), Video Relay Interpreting (VRI) or other live captioning app are other available options', EX, 'TERM-025',
  names('TERM-025', 'captioning', 'A live captioning app; TERM-025 captioning is "Real-time text display of speech".')),
 ('drinking fountain', '9.3', 'At least one drinking fountain at accessible height (610mm/24” from ground preferred) spout located near front, controls either automatic or easily operated, cane detectable.', DF, None, QTY),
 ('One accessible section of counter', '9.4', 'One accessible section of counter in all areas that serve the public.', DF, None, ELEM),
 ('barrier-free counter surface', '9.4', 'A barrier-free counter surface shall not be more than 865mm/34” above the floor', DF, None, QTY),
 ('Shelving, coat hooks and light switches', '9.5', 'Shelving, coat hooks and light switches at an accessible height', DF, None, ELEM),
 ('variety of seating options', '9.6', 'Have a variety of seating options available, including space for persons using wheelchairs to sit/park in all public seating areas, including companion seating (without blocking walk through areas).', DF, None, ELEM),
 ('seats with a variety of widths, adjustable armrests and backrests', '9.6', '(i.e. seats with a variety of widths, adjustable armrests and backrests).', DF, None, ELEM + ' Seat width is a body-size provision (access need A-SIZE names seat width); the clause states no figure.'),
 ('Level wheelchair seating area', '9.7', 'Level wheelchair seating area (in theatres, lecture halls, sports arenas, etc), to also include companion seating and unobstructed views', DF, None, ELEM),
 ('contrasting strip of colour', '9.8', 'Glass doors or partitions include a contrasting strip of colour across at eye-level', DF, None, CONTRAST),
 ('Hearing loops', '9.9', 'Hearing loops provided (counter loop or portable hearing loop)', EX, 'TERM-006',
  names('TERM-006', 'hearing loop', 'TERM-006 hearing loop is an "Audio frequency induction loop system for hearing aid users".')),
 # ---- 10. alarms
 ('audible and visual signal', '10.1', 'All alarm systems to include an audible and visual signal', DF, None,
  'The source requires an audible and a visual signal on all alarm systems. Whether this names TERM-013 visual fire alarm ("Strobe/flashing light fire alarm for deaf/HoH users") cannot be settled on this source alone: it does not say that the alarm systems meant are fire alarms, or what the visual signal is.'),
 # ---- 11. furniture
 ('detectable by someone who uses a cane', '11.1', 'Well anchored furniture should only be placed outside the main path of travel (inside or outside) and is detectable by someone who uses a cane', DF, None, ELEM),
 ('someone who uses a cane', '11.1', 'Well anchored furniture should only be placed outside the main path of travel (inside or outside) and is detectable by someone who uses a cane', DF, None,
  'A group named by its device, not an element or a quantity. Which group cannot be settled on this source alone: a cane used to detect furniture reads as a long (white) cane, which would be BLIND (\'blind and low-vision people\'), but the source does not say so, and a support cane would be MOB. A term adjudication can point only at a term, and the catalogue holds none for this group.'),
 ('good colour contrast', '11.2', 'There should be good colour contrast between street furniture and background surfaces (generally, grey colours should be avoided as they blend into the general background)', DF, None, CONTRAST),
 ('grey colours should be avoided', '11.2', 'There should be good colour contrast between street furniture and background surfaces (generally, grey colours should be avoided as they blend into the general background)', DF, None, CONTRAST + ' The clause also states the harm it avoids (furniture that blends into the background; R7), recorded on the search and in a gap.'),
 ('Variety of benches', '11.3', 'Variety of benches should be provided (some including a back and an arm rest)', DF, None, ELEM),
 ('quiet space', '11.4', 'Have a quiet space available', DF, None,
  ELEM + near('TERM-074', 'withdrawal space and exit legibility', 'it joins somewhere to withdraw to with a legible route out; the source says only "quiet space"')),
]

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    items = json.load(open(SESS + '/items.json'))
    seen = {o[1] for o in OBS}
    missing = [k for k in items if k not in seen]
    assert not missing, missing
    con = sqlite3.connect('file:' + DB + '?mode=ro', uri=True)
    held = {r[0] for r in con.execute('select term_id from terms')}
    for s, item, q, outc, term, why in OBS:
        assert (term is None) == (outc in (DF, NO)), s
        assert term is None or term in held, (s, term)
    before = con.execute("select count(*) from observed_terms where ref_id=?", (REF,)).fetchone()[0]
    assert dry or before == 0, f'observations already exist for {REF}: {before}; refusing to run twice'
    bad = 0
    for s, item, q, outc, term, why in OBS:
        rc, o = run('observe-term', '--ref-id', REF, '--surface-form', s, '--language', 'EN',
                    '--locator', loc(item), '--context-quote', q, '--session', STEM, dry=dry)
        oid = None
        try:
            oid = json.loads(o[o.index('{'):])['observation_id']
        except Exception:
            pass
        if rc or (oid is None and not dry):
            bad += 1
            print('REFUSED', item, s, '|', o[-300:].replace('\n', ' '))
            continue
        if dry:
            continue
        a = ['adjudicate-term', '--observation-id', str(oid), '--outcome', outc, '--rationale', why, '--session', STEM]
        if term:
            a += ['--term-id', term]
        rc2, o2 = run(*a)
        print(item, s[:40], 'obs', oid, '|', outc, term or '', '|', 'ok' if rc2 == 0 else o2[-200:])
    print('refused:', bad, 'of', len(OBS))
