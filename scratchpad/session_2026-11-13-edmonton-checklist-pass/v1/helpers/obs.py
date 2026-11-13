import subprocess, json, sys
SC='/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/edm'
STEM='session_2026-11-13-edmonton-checklist-pass'
LOG='/home/user/guidebook/scratchpad/'+STEM+'/digest-log.jsonl'
PG={'1':2,'2':3,'3':4,'4':5,'5':6,'6':7,'7':8,'8':9}
def pdfp(item):
    if item=='p1': return 1
    maj,mnr=item.split('.'); mnr=int(mnr); maj=int(maj)
    if maj==1: return 2 if mnr<=9 else 3
    if maj==2: return 3
    if maj==3: return 4
    if maj==4: return 4 if mnr<=5 else 5
    if maj==5: return 5
    if maj in (6,7): return 6
    if maj==8: return 7
    if maj in (9,10): return 8
    return 9
def run(*a, dry=False):
    r=subprocess.run([SC+'/db.sh',*a]+(['--dry-run'] if dry else []),capture_output=True,text=True)
    return r.stdout.strip()
EX='NAMES-EXISTING'; DF='DEFERRED'
DEFER_WHY='A quantity or element the source states a figure or requirement for, and the catalogue holds no term for it. Not minted in this from-evidence run: add-term mints a name and OR-17 leaves minting to the data pull request the owner reads. Recorded as an observation so the phrase is not lost.'
OBS=[
('path of travel','1.2','Barrier-free unobstructed path of travel (minimum width of 1500mm/59”) from parking area to building entrance',EX,'TERM-048','The source names the route from parking to entrance; TERM-048 is the circulation route.'),
('Corridors','2.10','Corridors should be 1100mm/43” (recommend 1800mm/71”)',EX,'TERM-002','Source states a corridor width.'),
('Doorway clearance','2.3','Doorway clearance is 850mm when the door is in the open 90 degree position (920mm/36” preferred)',EX,'TERM-021','Source states a doorway clear opening; TERM-021 door width is the clear opening width of an accessible door.'),
('elevator door at least 910 – 915mm/36” wide','5.3','Preferred dimension of elevator car to allow for optimal turning radius of 1500x1500mm/60x60” with elevator door at least 910 – 915mm/36” wide',EX,'TERM-021','The source states the width of an elevator door; read as a door width in the elevator setting.'),
('turning radius','5.3','Preferred dimension of elevator car to allow for optimal turning radius of 1500x1500mm/60x60” with elevator door at least 910 – 915mm/36” wide',EX,'TERM-003','The source calls a 1500 x 1500 mm space a turning radius; TERM-003 is the space for wheelchair rotation.'),
('Preferred maximum slope','6.1','Ramps are used for any slope steeper than 1 in 20 in a path of travel. Preferred maximum slope is 1 in 16 (1 in 12 in AB building code)',EX,'TERM-001','Source states ramp slopes.'),
('Level landings/ resting areas provided at 9m/10yd intervals along ramp','6.2','Level landings/ resting areas provided at 9m/10yd intervals along ramp',EX,'TERM-091','Source states the interval between landings, which is the run of a ramp flight between landings.'),
('Landings must be min 1200mm/47”long','6.5','Landings must be min 1200mm/47”long and same width as the ramp',EX,'TERM-092','Source states a landing dimension.'),
('clear height','1.8','a clear height of not less than 2750mm/108” at the pull-up space and along the vertical access and egress routes',EX,'TERM-061','Unobstructed vertical dimension above a route.'),
('lever handles','2.4','Door operating device should not require tight grasping or twisting of the wrist (doors should have lever handles)',EX,'TERM-004','Source names lever handles.'),
('Hearing loops','9.9','Hearing loops provided (counter loop or portable hearing loop)',EX,'TERM-006','Source names hearing loops.'),
('ACCESSIBLE WASHROOM STALL','8.6','ACCESSIBLE WASHROOM STALL:',EX,'TERM-009','The accessible washroom stall is the accessible bathroom (the source writes washroom).'),
('tactile strips','4.1','Changes in elevation at stairwells shall be indicated by tactile strips, which are as wide as the stair and have colour contrast',EX,'TERM-010','Source names tactile strips.'),
('symbol form','3.2','Signage available in symbol form for those with visual processing difficulties or who are unable to read',EX,'TERM-019','Symbol-form signage is pictogram signage.'),
('live captioning app','9.2','Video Relay Service (VRS), Video Relay Interpreting (VRI) or other live captioning app are other available options',EX,'TERM-025','Live captioning.'),
('barrier-free parking spaces','1.1','Designated barrier-free parking spaces located closest to barrier-free entrance',EX,'TERM-027','Accessible parking.'),
('way-finding signage','3.4','General and way-finding signage consistent in design and easily identifiable',EX,'TERM-028','Wayfinding.'),
('grab bars','8.6','equipped with door pull handle, coat hook, grab bars at various appropriate heights and placement',EX,'TERM-008','Grab bars.'),
('doorway threshold','2.9','Level, or beveled doorway threshold (maximum of 13mm/0.5” rise)',EX,'TERM-022','Level threshold.'),
('audible and visual signal','10.1','All alarm systems to include an audible and visual signal',EX,'TERM-013','Alarm with a visual signal is the visual fire alarm concept (the source says alarm systems, not fire alarms).'),
('Location of elevators','5.2','Location of elevators clearly identified at main entrance',EX,'TERM-014','Elevators; TERM-014 accessible lift.'),
('Universal Design','p1','this checklist to promote the concepts of Universal Design',EX,'TERM-017','Universal design.'),
('mobility devices (scooters/ walkers/ wheelchairs)','p1','people who use different mobility devices (scooters/ walkers/ wheelchairs) etc.',EX,'TERM-079','Mobility aids.'),
('colour contrast','1.2','Pathway shall have colour contrast and distinctive patterns where there are changes in level and surface material',DF,None,'The source requires colour contrast in many places and states no figure. Whether its colour contrast is the catalogue\'s LRV contrast (a luminance reflectance difference) is not stated by the source; left for the owner rather than assumed.'),
('access aisle','1.8','an access aisle not less than 1500mm/59” to 6000mm/236” long adjacent and parallel to the vehicle pull-up space',DF,None,DEFER_WHY),
('Vertically mounted sign','1.6','Vertically mounted sign showing accessibility symbol located near the centre line of each designated stall (minimum 1500mm/60” from ground to mid sign, max 2500mm/98” high)',DF,None,DEFER_WHY),
('Number of designated accessible parking spaces per number of parking stalls','1.7','Number of designated accessible parking spaces per number of parking stalls: 1 accessible stall per 2-10 spaces, 2 per 11-25 spaces, 2 per 26-50 and 4 per 51-100.',DF,None,DEFER_WHY),
('vestibule','2.7','If entrance is through doors in a series, leave enough room (1200mm/47” plus the width of the door) for a wheelchair to occupy the vestibule while opening the 2nd door',DF,None,DEFER_WHY),
('Automatic door operator button','2.8','Automatic door operator button is 800mm/31.5”-1500mm/59” from the ground and is located 1500mm/59” back from the door.',DF,None,DEFER_WHY),
('pedestrian entrances','2.6','not less than 50% of the pedestrian entrances, including the primary entrance of a building',DF,None,DEFER_WHY),
('Signage should be 1350mm/51” high from floor level','3.6','Signage should be 1350mm/51” high from floor level and not located on a door (should be 150mm/6” from the door frame).',DF,None,DEFER_WHY),
('rise between 125mm/5” and 180mm/7”','4.3','Steps for stairs have a rise between 125mm/5” and 180mm/7” and a run of not less than 280mm/11”',DF,None,DEFER_WHY),
('handrails on both sides','4.7','A stairway shall have a handrail on at least one side, but if it is 1100mm/43” or more wide, it shall have handrails on both sides.',DF,None,DEFER_WHY),
('tactile cues','4.8','Handrails should have a system of tactile cues (texture changes) within 300mm/12” from each end',DF,None,DEFER_WHY),
('Elevator buttons and emergency controls mounted at an accessible height','5.4','Elevator buttons and emergency controls mounted at an accessible height (1045mm/41”-1095mm/43” from ground)',DF,None,DEFER_WHY),
('Elevator doors shall begin to close','5.10','Elevator doors shall begin to close after a minimum of 8 seconds from the fully open position',DF,None,DEFER_WHY),
('clearspace between handrails','6.2','870mm/34” min clearspace between handrails.',DF,None,DEFER_WHY),
('With the ramp at any point','6.2','With the ramp at any point shall not be less than 1500mm/60”',DF,None,DEFER_WHY+' The sentence as printed has no subject noun (it reads like a ramp width); recorded as printed.'),
('15mm/0.6” wide strip','6.4','a 15mm/0.6” wide strip in contrasting colour and texture at the top of ramp to warn users of a change in elevation',DF,None,DEFER_WHY),
('diameter','7.1','Handrails should have a diameter not less than 30mm/1.18” or more than 43mm/1.69”',DF,None,DEFER_WHY),
('Handrail height','7.3','Handrail height should be 865mm/34” and no more than 965mm/38”',DF,None,DEFER_WHY),
('knee space','8.5','Accessible sink (minimum knee space of 735mm/29”)',DF,None,DEFER_WHY),
('soap and towel dispenser','8.5','soap and towel dispenser close to sink at preferred height of 1200mm/47”',DF,None,DEFER_WHY),
('low mounted or tilt mirror','8.5','Include a low mounted or tilt mirror 1000mm/39” above floor',DF,None,DEFER_WHY),
('accessible toilet height','8.6','accessible toilet height between 400mm-460mm/16”-18”',DF,None,DEFER_WHY),
('Public and emergency phones','9.1','Public and emergency phones mounted at an accessible height with a minimum of 865mm/34” and a maximum of 1370mm/54 above the floor',DF,None,DEFER_WHY),
('drinking fountain','9.3','At least one drinking fountain at accessible height (610mm/24” from ground preferred)',DF,None,DEFER_WHY),
('barrier-free counter surface','9.4','A barrier-free counter surface shall not be more than 865mm/34” above the floor',DF,None,DEFER_WHY),
('TTY','9.2','TTY (built in typewriter) phone for users who are Deaf or hard of hearing.',DF,None,'An element with no catalogue term; the source states no figure. Recorded so the phrase is not lost.'),
('Braille','3.3','Signage includes braille as well as large print, high colour contrast tactile lettering that is a mix of caps and lower case letters and is designed to prevent glare',DF,None,'An element with no catalogue term; the source states no figure.'),
('quiet space','11.4','Have a quiet space available',DF,None,'Possibly TERM-012 sensory room or TERM-074 withdrawal space; the source says only quiet space and states no figure. Left for the owner.'),
('companion seating','9.7','Level wheelchair seating area (in theatres, lecture halls, sports arenas, etc), to also include companion seating and unobstructed views',DF,None,'An element with no catalogue term; the source states no figure.'),
('gender inclusive/family washroom','8.7','Self-contained, gender inclusive/family washroom available, with proper signage provided in an accessible location',DF,None,'An element with no catalogue term (TERM-058 is the Changing Places toilet, which the source does not name); no figure.'),
('Visual indicator in elevators','5.7','Visual indicator in elevators to indicate “help on the way” for use in an emergency',DF,None,'An element with no catalogue term; no figure.'),
('Audible communication system','5.8','Audible communication system shall be available for accessing elevators, inside the car and have an announcement identifying the direction of travel and floors',DF,None,'An element with no catalogue term; no figure.'),
]
if __name__=='__main__':
    out=[]
    for surf,item,quote,outc,term,why in OBS:
        loc=f'PDF p. {pdfp(item)}'+('' if item=='p1' else f', item {item}')
        a=['observe-term','--ref-id','REF-01037','--surface-form',surf,'--language','EN','--locator',loc,'--context-quote',quote,'--session',STEM]
        o=run(*a)
        try: oid=json.loads(o)['observation_id']
        except Exception: oid=None
        rec={'step':'observe-term','surface':surf,'item':item,'result':o[-300:] if oid is None else {'observation_id':oid}}
        if oid is not None:
            aa=['adjudicate-term','--observation-id',str(oid),'--outcome',outc,'--rationale',why,'--session',STEM]
            if term: aa+=['--term-id',term]
            ao=run(*aa); rec['adjudicate']=ao[-200:]
        out.append(rec); print(rec['surface'][:40],'|',rec['result'] if oid is None else 'obs %s'%oid,'|',rec.get('adjudicate','')[:90].replace('\n',' '))
    open(LOG,'a').write('\n'.join(json.dumps(r,ensure_ascii=False) for r in out)+'\n')
