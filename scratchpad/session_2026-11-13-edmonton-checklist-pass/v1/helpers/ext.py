import subprocess, json, sys
sys.path.insert(0,'/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/edm')
from obs import run, pdfp, LOG, STEM
ALL=('ALL','named_in_text','meet the needs of all users')
MOB=('MOB','named_in_text','wider turning radius and wider doors are required by many wheelchairs and scooters today')
CODE='the Code (required) colour (blue)'; BEST='the Best Practice colour (magenta)'
def note(item,col,extra=''):
    return f'PDF p. {pdfp(item)}, item {item}. Rendered in {col}; the source legend on PDF p. 1 names blue Code (required) and magenta Best Practice. The classification is read from the text-layer colour of the run and checked against the page render. {extra}'.strip()
# (param, item, claim_type, value, unit, comparator, claim_text, setting, lens, colour, extra)
X=[
(3,'6.1','numerical','1:20','rise:run ratio','>','Ramps are used for any slope steeper than 1 in 20 in a path of travel.','ramp in a path of travel',ALL,BEST,'A threshold above which the source says ramps are used; the source does not state it as a maximum.'),
(3,'6.1','numerical','1:16','rise:run ratio','<=','Preferred maximum slope is 1 in 16','ramp in a path of travel',ALL,BEST,''),
(3,'6.1','numerical','1:12','rise:run ratio','<=','(1 in 12 in AB building code)','ramp; the source attributes it to the AB (Alberta) building code',ALL,CODE,'The figure is the source\'s own attribution to the Alberta building code; that code is not held here.'),
(4,'1.2','numerical','1500','mm','>=','Barrier-free unobstructed path of travel (minimum width of 1500mm/59”)','path of travel from parking area to building entrance',ALL,BEST,'The words in parentheses are the Best Practice run; the rest of the item is Code (required).'),
(4,'2.10','numerical','1100','mm','=','Corridors should be 1100mm/43”','corridor',ALL,CODE,'Printed in item 2.10 under the entrances heading; the item also carries a colour-contrast clause.'),
(4,'2.10','numerical','1800','mm','=','(recommend 1800mm/71”)','corridor',ALL,BEST,'Recommended value beside the 1100 mm figure.'),
(9,'2.3','numerical','850','mm','=','Doorway clearance is 850mm when the door is in the open 90 degree position','doorway; door open to 90 degrees',MOB,CODE,'The source writes "is 850mm"; it does not say minimum.'),
(9,'2.3','numerical','920','mm','=','(920mm/36” preferred)','doorway; door open to 90 degrees',MOB,BEST,''),
(9,'5.3','range','910 to 915','mm','between','with elevator door at least 910 – 915mm/36” wide','elevator door',MOB,BEST,'Printed as "at least 910 – 915mm"; the source gives two figures and no reason for them.'),
(5,'5.3','numerical','1500','mm','=','Preferred dimension of elevator car to allow for optimal turning radius of 1500x1500mm/60x60”','elevator car',MOB,BEST,'The source writes 1500x1500 mm: a square, not a radius; only the side is entered as the value.'),
(11,'1.8','numerical','2750','mm','>=','a clear height of not less than 2750mm/108” at the pull-up space and along the vertical access and egress routes','passenger loading zone: pull-up space and access and egress routes',ALL,CODE,''),
(12,'6.2','numerical','9','m','=','Level landings/ resting areas provided at 9m/10yd intervals along ramp','ramp',ALL,CODE,'The source writes "at 9m intervals"; the sense of maximum is the reader\'s, not stated.'),
]
ABSENT=[
(8,'7.2','absent',None,None,None,'Handrails in contrasting colour to wall or surrounding area','handrail',ALL,BEST,'The source requires contrasting colour here and elsewhere and states no luminance or reflectance figure.'),
(6,'2.4','absent',None,None,None,'Door operating device should not require tight grasping or twisting of the wrist (doors should have lever handles)','door operating device',ALL,CODE,'The source states no force figure for operating a door.'),
]
if __name__=='__main__':
    dry = '--dry' in sys.argv
    out=[]
    for rec in X+ABSENT:
        p,item,ct,val,unit,cmp_,txt,setting,lens,col,extra=rec
        a=['add-extraction','--ref-id','REF-01037','--parameter-id',str(p),'--identity',lens[0],'--lens-basis',lens[1],'--lens-basis-text',lens[2],'--claim-type',ct,'--claim-text',txt,'--source-section',f'Item {item}','--loc-note',f'PDF p. {pdfp(item)}','--jurisdiction','CA','--setting',setting,'--extraction-method','full-read','--root-type','committee_assertion','--measurement-paradigm','stated_unmeasured','--figure-role',('finding' if ct=='absent' else 'claim'),'--relation','none','--notes',note(item,col,extra),'--session',STEM]
        if ct=='absent': a+=['--extraction-status','absent-confirmed']
        else: a+=['--claimed-value',val,'--claimed-unit',unit,'--comparator',cmp_]
        o=run(*a,dry=dry)
        r={'step':'add-extraction'+('(dry)' if dry else ''),'param':p,'item':item,'result':o[-420:]}
        out.append(r); print(p,item,ct,val or '', '|',o.replace('\n',' ')[:230])
    if not dry: open(LOG,'a').write('\n'.join(json.dumps(r,ensure_ascii=False) for r in out)+'\n')
