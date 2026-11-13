"""Step 2 and 3: every numbered item (derived from items.json) and every figure, observed in
ONE pass, then adjudicated. NAMES-EXISTING only to a term that is already a parameter or
already declined (R16 holds without declaring anything); everything else DEFERRED with the
open question it waits on. Surface forms as printed (F14); a surface form names the concept
it is adjudicated to (F12)."""
import json, sys, sqlite3
from common import run, loc, STEM, REF, DB, SESS

EX, DF = 'NAMES-EXISTING', 'DEFERRED'
AQ4 = ("A quantity the source states a figure for; the catalogue holds no parameter for it. Deferred, "
       "not minted and not promoted: whether a source that is not a code may add a parameter is the "
       "owner's open question AQ-4 (ADJUDICATION 5.3), and a term minted here would be a NAMES-NEW "
       "term neither promoted nor declined, which R16 refuses. The figure is kept verbatim in the "
       "context quote.")
AQ7 = ("An element or feature the source requires, with no figure. The catalogue holds no parameter "
       "for it; adjudicating it to a held term that is neither a parameter nor declined would fail R16, "
       "and declining such a term in a single-source batch is the owner's open question AQ-7 "
       "(ADJUDICATION 5.3). Deferred; the phrase is kept as printed.")
OR17 = ("The source requires colour contrast and states no figure. Whether its colour contrast names "
        "the catalogue's TERM-011 LRV contrast (a light reflectance value difference) is a vocabulary "
        "judgment under OR-17 that this source alone does not settle (ADJUDICATION F8): the genuinely "
        "unsettled kind of DEFERRED.")
AQ6 = ("OT-1 and OT-2 (references/project-standards.md, 'OT-1: \"Barrier-free path of travel. It is a "
       "circulation route that is specific to people in wheelchairs/mobility devices.\"') place the "
       "owner's term as a circulation route through a building, specific to wheelchair and "
       "mobility-device users, to be minted from observation 68. This source uses the phrase for the "
       "exterior route from parking or drop-off to the entrance, with a colour-contrast provision "
       "attached. Whether this sighting names that term is the owner's open question AQ-6. Not "
       "adjudicated to TERM-048 and the term is not minted here.")


def near(t, n):
    return f' The catalogue holds {t} ({n}), which is neither a parameter nor declined; not adjudicated to it here.'


# (surface form as printed, item, context quote verbatim, outcome, term, rationale)
OBS = [
 ('Universal Design', 'p1', 'The City of Edmonton Accessibility Advisory Committee (AAC) has created this checklist to promote the concepts of Universal Design.', DF, None, 'A design concept, not a quantity or an element.' + near('TERM-017', 'universal design') + ' Declining it is AQ-7.'),
 ('wider turning radius', 'p1', 'For example, a wider turning radius and wider doors are required by many wheelchairs and scooters today.', EX, 'TERM-003', 'The space a wheelchair or scooter needs to turn; TERM-003 turning circle (parameter 5) is the space for wheelchair rotation.'),
 ('wider doors', 'p1', 'For example, a wider turning radius and wider doors are required by many wheelchairs and scooters today.', EX, 'TERM-021', 'The width of doors as the source contrasts it with the minimum standards; TERM-021 door width (parameter 9).'),
 ('mobility devices', 'p1', 'For example, people with low vision, people who use different mobility devices (scooters/ walkers/wheelchairs) etc.', DF, None, 'A class of assistive devices, an element.' + near('TERM-079', 'mobility aids') + ' AQ-7.'),
 ('barrier-free parking spaces', '1.1', 'Designated barrier-free parking spaces located closest to barrier-free entrance', DF, None, AQ7 + near('TERM-027', 'accessible parking')),
 ('Barrier-free unobstructed path of travel', '1.2', 'Barrier-free unobstructed path of travel (minimum width of 1500mm/59”) from parking area to building entrance (clear of snow, garbage cans, sign posts and other obstacles; pathway well lit; not behind vehicles).', DF, None, AQ6),
 ('minimum width', '1.2', 'Barrier-free unobstructed path of travel (minimum width of 1500mm/59”) from parking area to building entrance (clear of snow, garbage cans, sign posts and other obstacles; pathway well lit; not behind vehicles).', EX, 'TERM-002', 'The minimum clear width of an accessible route; TERM-002 corridor width is the clear width of an accessible circulation route (parameter 4, which already holds route widths outside buildings). Which route term the path is (AQ-6) does not change that this is its width.'),
 ('colour contrast', '1.2', 'Pathway shall have colour contrast and distinctive patterns where there are changes in level and surface material', DF, None, OR17),
 ('Curb ramp', '1.3', 'Curb ramp to sidewalk located between parking spaces', EX, 'TERM-089', 'A curb ramp is an inclined surface built as a discrete element to bridge a level difference on a route; TERM-089 ramp, declined as a parameter (an element).'),
 ('Access aisle painted on pavement', '1.4', 'Access aisle painted on pavement between barrier-free parking spaces', DF, None, AQ7),
 ('Accessible parking symbols', '1.5', 'Accessible parking symbols painted on pavement at the entrance of each stall. The symbol and any associated background paint should not occupy the entire area. The more painted surface, the more likely pavement will become slippery', DF, None, AQ7),
 ('Vertically mounted sign', '1.6', 'Vertically mounted sign showing accessibility symbol located near the centre line of each designated stall (minimum 1500mm/60” from ground to mid sign, max 2500mm/98” high)', DF, None, AQ4),
 ('Number of designated accessible parking spaces per number of parking stalls', '1.7', 'Number of designated accessible parking spaces per number of parking stalls: 1 accessible stall per 2-10 spaces, 2 per 11-25 spaces, 2 per 26-50 and 4 per 51-100. One additional accessible stall for each additional increment of 100 or part thereof', DF, None, AQ4 + ' A count, a kind the catalogue does not hold.'),
 ('access aisle', '1.8', 'Passenger loading zones need: an access aisle not less than 1500mm/59” to 6000mm/236” long adjacent and parallel to the vehicle pull-up space, a curb ramp where there are curbs between the access aisle and the vehicle pull-up space and a clear height of not less than 2750mm/108” at the pull-up space and along the vertical access and egress routes', DF, None, AQ4),
 ('clear height', '1.8', 'Passenger loading zones need: an access aisle not less than 1500mm/59” to 6000mm/236” long adjacent and parallel to the vehicle pull-up space, a curb ramp where there are curbs between the access aisle and the vehicle pull-up space and a clear height of not less than 2750mm/108” at the pull-up space and along the vertical access and egress routes', EX, 'TERM-061', 'An unobstructed vertical dimension above a route; TERM-061 headroom clearance (parameter 11).'),
 ('directional signs', '1.9', 'If the location of designated parking stalls is not easily visible from the approach viewpoint, appropriate directional signs showing location of designated stalls shall be provided', DF, None, AQ7 + near('TERM-028', 'wayfinding')),
 ('clear accessible path', '1.10', 'Ensure there is a clear accessible path between accessible stalls and the payment machine', DF, None, AQ7 + ' A route between the stalls and the payment machine (not the payment machine); the route vocabulary for this document is also before the owner as AQ-6.'),
 ('Information for parking payment', '1.11', 'Information for parking payment is easy to understand and clearly visible for accessible stalls', DF, None, AQ7),
 ('Barrier-free path of travel', '2.1', 'Barrier-free path of travel from parking and/or drop off zone to entrance', DF, None, AQ6),
 ('Signage at all non-accessible entrances', '2.2', 'Signage at all non-accessible entrances should clearly indicate location of barrier-free entrance', DF, None, AQ7),
 ('Doorway clearance', '2.3', 'Doorway clearance is 850mm when the door is in the open 90 degree position (920mm/36” preferred)', EX, 'TERM-021', 'The clear opening of a doorway with the door open to 90 degrees; TERM-021 door width (parameter 9).'),
 ('Door operating device', '2.4', 'Door operating device should not require tight grasping or twisting of the wrist (doors should have lever handles)', DF, None, AQ7),
 ('lever handles', '2.4', 'Door operating device should not require tight grasping or twisting of the wrist (doors should have lever handles)', DF, None, AQ7 + near('TERM-004', 'lever handles')),
 ('automatic sliding doors', '2.5', 'The primary entrance is barrier-free (automatic sliding doors are optimal; power doors with large paddle/push plate is the next best alternative, wave to open preferred where feasible)', DF, None, AQ7),
 ('pedestrian entrances', '2.6', 'In addition to the barrier-free entrances required, not less than 50% of the pedestrian entrances, including the primary entrance of a building, including walkways leading to the entrances from a public thoroughfare and from on-site parking areas, shall be barrier-free', DF, None, AQ4 + ' A proportion of entrances, a kind the catalogue does not hold.'),
 ('vestibule', '2.7', 'If entrance is through doors in a series, leave enough room (1200mm/47” plus the width of the door) for a wheelchair to occupy the vestibule while opening the 2nd door', DF, None, AQ4),
 ('Automatic door operator button', '2.8', 'Automatic door operator button is 800mm/31.5”-1500mm/59” from the ground and is located 1500mm/59” back from the door.', DF, None, AQ4),
 ('doorway threshold', '2.9', 'Level, or beveled doorway threshold (maximum of 13mm/0.5” rise)', DF, None, AQ4 + ' The catalogue holds TERM-022 level threshold, whose definition ("zero-step entry at doorway") states its own answer, which this 13 mm rise contradicts; that term is T-072 item 6\'s to judge. Not adjudicated to it.'),
 ('Colour contrast', '2.10', 'Colour contrast to identify doorway threshold, frame or entrance.', DF, None, OR17),
 ('Corridors should be 1100mm/43”', '2.10', 'Corridors should be 1100mm/43” (recommend 1800mm/71”)', EX, 'TERM-002', 'The width of corridors; TERM-002 corridor width (parameter 4).'),
 ('assistive listening devices', '3.1', 'Facilities and services for persons with disabilities identified with appropriate symbols (e.g. availability of assistive listening devices)', DF, None, AQ7),
 ('symbol form', '3.2', 'Signage available in symbol form for those with visual processing difficulties or who are unable to read', DF, None, AQ7 + near('TERM-019', 'pictogram signage')),
 ('braille', '3.3', 'Signage includes braille as well as large print, high colour contrast tactile lettering that is a mix of caps and lower case letters and is designed to prevent glare', DF, None, AQ7),
 ('high colour contrast tactile lettering', '3.3', 'Signage includes braille as well as large print, high colour contrast tactile lettering that is a mix of caps and lower case letters and is designed to prevent glare', DF, None, OR17),
 ('way-finding signage', '3.4', 'General and way-finding signage consistent in design and easily identifiable', DF, None, AQ7 + near('TERM-028', 'wayfinding')),
 ('Braille signage', '3.5', 'Braille signage mounted at appropriate height (chest level) and location', DF, None, AQ7),
 ('Signage should be 1350mm/51” high from floor level', '3.6', 'Signage should be 1350mm/51” high from floor level and not located on a door (should be 150mm/6” from the door frame).', DF, None, AQ4),
 ('tactile signage', '3.6', 'If tactile signage is installed it should be 1200mm/47” from floor level (building directories should be tactile)', DF, None, AQ4),
 ('tactile strips', '4.1', 'Changes in elevation at stairwells shall be indicated by tactile strips, which are as wide as the stair and have colour contrast', DF, None, AQ7 + near('TERM-010', 'tactile surfaces')),
 ('Step demarcation in yellow', '4.2', 'Step demarcation in yellow on sides and back of escalator steps', DF, None, AQ7),
 ('rise between 125mm/5” and 180mm/7”', '4.3', 'Steps for stairs have a rise between 125mm/5” and 180mm/7” and a run of not less than 280mm/11” (should not be open between steps).', DF, None, AQ4),
 ('run of not less than 280mm/11”', '4.3', 'Steps for stairs have a rise between 125mm/5” and 180mm/7” and a run of not less than 280mm/11” (should not be open between steps).', DF, None, AQ4),
 ('Illumination', '4.4', 'Illumination shall be positioned to minimize glare and shadow', DF, None, AQ7),
 ('open area beneath the stairs', '4.5', 'Ensure any open area beneath the stairs is enclosed with planters, railings, benches, fencing etc to ensure no access.', DF, None, AQ7),
 ('Carpet', '4.6', 'Carpet is securely attached', DF, None, AQ7),
 ('handrails on both sides', '4.7', 'A stairway shall have a handrail on at least one side, but if it is 1100mm/43” or more wide, it shall have handrails on both sides.', DF, None, AQ4 + ' A count of handrails conditioned on a stair width; neither a count kind nor a stair-width parameter is held (ADJUDICATION A5).'),
 ('tactile cues', '4.8', 'Handrails should have a system of tactile cues (texture changes) within 300mm/12” from each end', DF, None, AQ4),
 ('clear colour contrast', '5.1', 'Doors have clear colour contrast from door surroundings', DF, None, OR17),
 ('Location of elevators', '5.2', 'Location of elevators clearly identified at main entrance', DF, None, AQ7 + near('TERM-014', 'accessible lift')),
 ('turning radius', '5.3', 'Preferred dimension of elevator car to allow for optimal turning radius of 1500x1500mm/60x60” with elevator door at least 910 – 915mm/36” wide', EX, 'TERM-003', 'The source calls a 1500 x 1500 mm car the space for a turning radius; TERM-003 turning circle (parameter 5) is the space for wheelchair rotation.'),
 ('elevator door at least 910 – 915mm/36” wide', '5.3', 'Preferred dimension of elevator car to allow for optimal turning radius of 1500x1500mm/60x60” with elevator door at least 910 – 915mm/36” wide', EX, 'TERM-021', 'The clear width of an elevator door; TERM-021 door width (parameter 9).'),
 ('stretcher', '5.3', '(one elevator has inside dimensions that will accommodate a stretcher at 2010mm/79” long and 610mm/24” wide) 1828mm/72” by 2032mm/80”', DF, None, AQ4 + ' Elevator car inside dimensions; no parameter.'),
 ('Elevator buttons and emergency controls mounted at an accessible height', '5.4', 'Elevator buttons and emergency controls mounted at an accessible height (1045mm/41”-1095mm/43” from ground)', DF, None, AQ4),
 ('large print tactile numbers and Braille', '5.5', 'Elevator buttons and emergency controls incorporate large print tactile numbers and Braille mounted in a raised fashion (not flush or recessed).', DF, None, AQ7),
 ('Colour contrast', '5.5', 'Colour contrast shall be used to identify the floor registration button panel from background, call buttons should protrude from adjacent surface', DF, None, OR17),
 ('Braille and tactile numbers', '5.6', 'Braille and tactile numbers placed on both sides of door jambs at appropriate height to identify floor level', DF, None, AQ7),
 ('Visual indicator in elevators', '5.7', 'Visual indicator in elevators to indicate “help on the way” for use in an emergency', DF, None, AQ7),
 ('Audible communication system', '5.8', 'Audible communication system shall be available for accessing elevators, inside the car and have an announcement identifying the direction of travel and floors', DF, None, AQ7),
 ('Elevator waiting areas should have seating', '5.9', 'Elevator waiting areas should have seating in close proximity', DF, None, AQ7),
 ('Elevator doors shall begin to close', '5.10', 'Elevator doors shall begin to close after a minimum of 8 seconds from the fully open position', DF, None, AQ4 + ' A time, a door dwell time; no parameter.'),
 ('Ramps', '6.1', 'Ramps are used for any slope steeper than 1 in 20 in a path of travel.', EX, 'TERM-089', 'TERM-089 ramp, declined as a parameter (an element).'),
 ('Preferred maximum slope', '6.1', 'Preferred maximum slope is 1 in 16 (1 in 12 in AB building code)', EX, 'TERM-001', 'The slope of a ramp; TERM-001 ramp gradient (parameter 3).'),
 ('With the ramp at any point', '6.2', 'With the ramp at any point shall not be less than 1500mm/60”; 870mm/34” min clearspace between handrails.', DF, None, 'The sentence as printed has no subject noun: it reads like a ramp width (TERM-002 corridor width, parameter 4), but this source alone cannot settle what the 1500 mm measures (ADJUDICATION F2). Deferred as genuinely unsettled; the figure is parked, not written (AQ-1).'),
 ('clearspace between handrails', '6.2', 'With the ramp at any point shall not be less than 1500mm/60”; 870mm/34” min clearspace between handrails.', EX, 'TERM-002', 'The clear width of a ramp between its handrails; TERM-002 corridor width (parameter 4), which already holds a ramp width between handrails (canonical extraction 192).'),
 ('Level landings/ resting areas provided at 9m/10yd intervals along ramp', '6.2', 'Level landings/ resting areas provided at 9m/10yd intervals along ramp', EX, 'TERM-091', 'The interval between landings along a ramp is the length of a flight between landings; TERM-091 ramp run length (parameter 12).'),
 ('tight turns or switch-backs', '6.3', 'Minimize or avoid tight turns or switch-backs', DF, None, AQ7),
 ('15mm/0.6” wide strip', '6.4', 'Strong colour contrast and tactile surfacing on all ramp landings and a 15mm/0.6” wide strip in contrasting colour and texture at the top of ramp to warn users of a change in elevation', DF, None, AQ4),
 ('Strong colour contrast', '6.4', 'Strong colour contrast and tactile surfacing on all ramp landings and a 15mm/0.6” wide strip in contrasting colour and texture at the top of ramp to warn users of a change in elevation', DF, None, OR17),
 ('Landings must be min 1200mm/47”long', '6.5', 'Landings designed to accommodate larger chairs and scooters (able to open doors without backing onto ramp). Landings must be min 1200mm/47”long and same width as the ramp', DF, None, AQ4 + ' The catalogue holds TERM-092 intermediate landing, which E2 names as a term to be renamed in a research pull request and T-072 item 6 owns; not adjudicated to it here.'),
 ('diameter', '7.1', 'Handrails should have a diameter not less than 30mm/1.18” or more than 43mm/1.69”', DF, None, AQ4),
 ('handrails on both sides', '7.1', 'A stairway should have a handrail on at least one side but if it is 1100mm or more wide it shall have handrails on both sides and are continuously graspable.', DF, None, AQ4 + ' A count of handrails conditioned on a stair width (ADJUDICATION A5).'),
 ('contrasting colour', '7.2', 'Handrails in contrasting colour to wall or surrounding area', DF, None, OR17),
 ('Handrail height', '7.3', 'Handrail height should be 865mm/34” and no more than 965mm/38”', DF, None, AQ4),
 ('Handrails extend horizontally', '7.4', 'Handrails extend horizontally beyond last stair and terminate to wall or ground', DF, None, AQ7),
 ('wave to open or push button', '8.1', 'Have a wave to open or push button available', DF, None, AQ7),
 ('only one turn with clear corner', '8.2', 'For washrooms without entrance door, there is only one turn with clear corner so persons who are blind do not become disoriented', DF, None, AQ7),
 ('Proper signage', '8.3', 'Proper signage located outside the entrance and stall door', DF, None, AQ7),
 ('located around perimeter', '8.4', 'Sinks, garbage cans, etc. located around perimeter rather than in the centre of the room', DF, None, AQ7),
 ('knee space', '8.5', 'Accessible sink (minimum knee space of 735mm/29”) with soap and towel dispenser close to sink at preferred height of 1200mm/47”.', DF, None, AQ4),
 ('soap and towel dispenser', '8.5', 'Accessible sink (minimum knee space of 735mm/29”) with soap and towel dispenser close to sink at preferred height of 1200mm/47”.', DF, None, AQ4),
 ('low mounted or tilt mirror', '8.5', 'Include a low mounted or tilt mirror 1000mm/39” above floor and insulate any exposed pipes.', DF, None, AQ4),
 ('ACCESSIBLE WASHROOM STALL', '8.6', 'ACCESSIBLE WASHROOM STALL:', DF, None, AQ7 + ' A stall, not a room: not TERM-009 accessible bathroom (ADJUDICATION A4, F12).'),
 ('minimum 1700mm x 1500mm/70 x 60”', '8.6', 'minimum 1700mm x 1500mm/70 x 60”', DF, None, AQ4 + ' The size of the accessible washroom stall; no parameter.'),
 ('person with limited mobility', '8.6', 'door that swings outward so person with limited mobility can close it independently', DF, None, AQ7 + ' The phrase names a group (a lens matter), and the provision is a door swing, an element.'),
 ('grab bars', '8.6', 'equipped with door pull handle, coat hook, grab bars at various appropriate heights and placement', DF, None, AQ7 + near('TERM-008', 'grab bars')),
 ('accessible toilet height', '8.6', 'accessible toilet height between 400mm-460mm/16”-18”', DF, None, AQ4),
 ('various toilet size and heights', '8.6', 'various toilet size and heights. Or adding a step stool option if unavailable.', DF, None, AQ7),
 ('gender inclusive/family washroom', '8.7', 'Self-contained, gender inclusive/family washroom available, with proper signage provided in an accessible location', DF, None, AQ7),
 ('Public and emergency phones', '9.1', 'Public and emergency phones mounted at an accessible height with a minimum of 865mm/34” and a maximum of 1370mm/54 above the floor', DF, None, AQ4),
 ('TTY', '9.2', 'TTY (built in typewriter) phone for users who are Deaf or hard of hearing.', DF, None, AQ7),
 ('live captioning app', '9.2', 'Video Relay Service (VRS), Video Relay Interpreting (VRI) or other live captioning app are other available options', DF, None, AQ7 + near('TERM-025', 'live captioning')),
 ('drinking fountain', '9.3', 'At least one drinking fountain at accessible height (610mm/24” from ground preferred) spout located near front, controls either automatic or easily operated, cane detectable.', DF, None, AQ4),
 ('barrier-free counter surface', '9.4', 'A barrier-free counter surface shall not be more than 865mm/34” above the floor', DF, None, AQ4),
 ('Shelving, coat hooks and light switches', '9.5', 'Shelving, coat hooks and light switches at an accessible height', DF, None, AQ7),
 ('variety of seating options', '9.6', 'Have a variety of seating options available, including space for persons using wheelchairs to sit/park in all public seating areas, including companion seating (without blocking walk through areas).', DF, None, AQ7),
 ('Level wheelchair seating area', '9.7', 'Level wheelchair seating area (in theatres, lecture halls, sports arenas, etc), to also include companion seating and unobstructed views', DF, None, AQ7),
 ('contrasting strip of colour', '9.8', 'Glass doors or partitions include a contrasting strip of colour across at eye-level', DF, None, OR17),
 ('Hearing loops', '9.9', 'Hearing loops provided (counter loop or portable hearing loop)', DF, None, AQ7 + near('TERM-006', 'hearing loop')),
 ('audible and visual signal', '10.1', 'All alarm systems to include an audible and visual signal', DF, None, AQ7 + ' The source says alarm systems with an audible and visual signal, not a visual fire alarm; not TERM-013 (ADJUDICATION F12).'),
 ('detectable by someone who uses a cane', '11.1', 'Well anchored furniture should only be placed outside the main path of travel (inside or outside) and is detectable by someone who uses a cane', DF, None, AQ7),
 ('good colour contrast', '11.2', 'There should be good colour contrast between street furniture and background surfaces (generally, grey colours should be avoided as they blend into the general background)', DF, None, OR17),
 ('Variety of benches', '11.3', 'Variety of benches should be provided (some including a back and an arm rest)', DF, None, AQ7),
 ('quiet space', '11.4', 'Have a quiet space available', DF, None, AQ7 + ' The nearest held terms are TERM-012 sensory room and TERM-074 withdrawal space; the source says only quiet space.'),
]

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    items = json.load(open(SESS + '/items.json'))
    seen = {o[1] for o in OBS}
    missing = [k for k in items if k not in seen]
    assert not missing, missing
    con = sqlite3.connect('file:' + DB + '?mode=ro', uri=True)
    allowed = {r[0] for r in con.execute('select term_id from base_parameters')} | \
              {r[0] for r in con.execute('select term_id from parameter_declinations where revoked_at is null')}
    for s, item, q, outc, term, why in OBS:
        assert outc != EX or term in allowed, (s, term)
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
