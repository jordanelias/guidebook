import json, sys
sys.path.insert(0,'/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/edm')
from obs import run, pdfp, LOG, STEM
EX='NAMES-EXISTING'; DF='DEFERRED'
W='A requirement or feature the source states with no figure, for an element the catalogue holds no term for. Not minted in this from-evidence run (OR-17 leaves minting to the data pull request the owner reads); recorded so the phrase is not lost.'
CW='The source requires colour contrast here and states no figure; whether its colour contrast is the catalogue LRV contrast is not stated and is left for the owner (see the observation at item 1.2).'
O=[
('Curb ramp','1.3','Curb ramp to sidewalk located between parking spaces',EX,'TERM-089','A curb ramp is a ramp.'),
('Access aisle painted on pavement','1.4','Access aisle painted on pavement between barrier-free parking spaces',DF,None,W),
('Accessible parking symbols','1.5','Accessible parking symbols painted on pavement at the entrance of each stall.',EX,'TERM-027','Accessible parking marking.'),
('directional signs','1.9','appropriate directional signs showing location of designated stalls shall be provided',EX,'TERM-028','Wayfinding signage.'),
('payment machine','1.10','Ensure there is a clear accessible path between accessible stalls and the payment machine',EX,'TERM-048','A route between stalls and the payment machine.'),
('Information for parking payment','1.11','Information for parking payment is easy to understand and clearly visible for accessible stalls',DF,None,W),
('Barrier-free path of travel','2.1','Barrier-free path of travel from parking and/or drop off zone to entrance',EX,'TERM-048','A route from parking to entrance.'),
('Signage at all non-accessible entrances','2.2','Signage at all non-accessible entrances should clearly indicate location of barrier-free entrance',EX,'TERM-028','Wayfinding signage.'),
('automatic sliding doors','2.5','automatic sliding doors are optimal; power doors with large paddle/push plate is the next best alternative, wave to open preferred where feasible',DF,None,W),
('assistive listening devices','3.1','Facilities and services for persons with disabilities identified with appropriate symbols (e.g. availability of assistive listening devices)',DF,None,W),
('Braille signage mounted at appropriate height','3.5','Braille signage mounted at appropriate height (chest level) and location',DF,None,W),
('Step demarcation in yellow','4.2','Step demarcation in yellow on sides and back of escalator steps',DF,None,W),
('Illumination shall be positioned to minimize glare and shadow','4.4','Illumination shall be positioned to minimize glare and shadow',DF,None,W),
('open area beneath the stairs','4.5','Ensure any open area beneath the stairs is enclosed with planters, railings, benches, fencing etc to ensure no access.',DF,None,W),
('Carpet is securely attached','4.6','Carpet is securely attached',DF,None,W),
('clear colour contrast','5.1','Doors have clear colour contrast from door surroundings',DF,None,CW),
('large print tactile numbers and Braille','5.5','Elevator buttons and emergency controls incorporate large print tactile numbers and Braille mounted in a raised fashion (not flush or recessed).',DF,None,W),
('Braille and tactile numbers','5.6','Braille and tactile numbers placed on both sides of door jambs at appropriate height to identify floor level',DF,None,W),
('Elevator waiting areas','5.9','Elevator waiting areas should have seating in close proximity',DF,None,W),
('tight turns or switch-backs','6.3','Minimize or avoid tight turns or switch-backs',DF,None,W),
('Handrails extend horizontally','7.4','Handrails extend horizontally beyond last stair and terminate to wall or ground',DF,None,W),
('wave to open or push button','8.1','Single door entrance is optimal. Have a wave to open or push button available',DF,None,W),
('persons who are blind do not become disoriented','8.2','For washrooms without entrance door, there is only one turn with clear corner so persons who are blind do not become disoriented',DF,None,W),
('Proper signage located outside the entrance and stall door','8.3','Proper signage located outside the entrance and stall door',DF,None,W),
('located around perimeter','8.4','Sinks, garbage cans, etc. located around perimeter rather than in the centre of the room',DF,None,W),
('Shelving, coat hooks and light switches','9.5','Shelving, coat hooks and light switches at an accessible height',DF,None,W),
('variety of seating options','9.6','Have a variety of seating options available, including space for persons using wheelchairs to sit/park in all public seating areas',DF,None,W),
('contrasting strip of colour','9.8','Glass doors or partitions include a contrasting strip of colour across at eye-level',DF,None,CW),
('detectable by someone who uses a cane','11.1','Well anchored furniture should only be placed outside the main path of travel (inside or outside) and is detectable by someone who uses a cane',DF,None,W),
('good colour contrast','11.2','There should be good colour contrast between street furniture and background surfaces',DF,None,CW),
('Variety of benches','11.3','Variety of benches should be provided (some including a back and an arm rest)',DF,None,W),
]
out=[]
for surf,item,quote,outc,term,why in O:
    loc=f'PDF p. {pdfp(item)}, item {item}'
    o=run('observe-term','--ref-id','REF-01037','--surface-form',surf,'--language','EN','--locator',loc,'--context-quote',quote,'--session',STEM)
    try: oid=json.loads(o)['observation_id']
    except Exception: oid=None
    rec={'step':'observe-term','surface':surf,'item':item,'result':o[-250:] if oid is None else {'observation_id':oid}}
    if oid is not None:
        aa=['adjudicate-term','--observation-id',str(oid),'--outcome',outc,'--rationale',why,'--session',STEM]+(['--term-id',term] if term else [])
        rec['adjudicate']=run(*aa)[-120:]
    out.append(rec); print(item,surf[:36],'|',('obs %s'%oid) if oid else rec['result'][:200].replace('\n',' '))
open(LOG,'a').write('\n'.join(json.dumps(r,ensure_ascii=False) for r in out)+'\n')
