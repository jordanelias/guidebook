import subprocess,sys,os
SESS='session_2026-11-06-pipeline-batch'
DB=os.path.abspath('scratchpad/session_2026-11-06-pipeline-batch/walk.db')
DRY='--dry-run' in sys.argv
ADMLOC='PDF page %s of 74; 2015 edition incorporating 2020 and 2024 amendments'
rows=[]
def r(ref,p,lens,val,unit,cmp_,quote,sec,jur,setting,loc,note,locnote):
    rows.append((ref,p,lens,val,unit,cmp_,quote,sec,jur,setting,loc,note,locnote))
A='REF-00992'
LENS_NOTE=' Lens %s is the reader\'s reading, not the source\'s statement [ASSUMPTION: %s].'
# --- parameter 4, ADM
r(A,4,'MOB','1200','mm','>=','they have an unobstructed width (excluding any projections into the space) along their length of at least 1200mm;','Approved Document M Volume 2, para 3.14(b)','UK','corridors and passageways, buildings other than dwellings',('3','3.14','b'),
  'Quantity: minimum unobstructed width of a corridor or passageway, excluding projections. Para 3.14(c) adds passing places 1800 mm long and 1800 mm wide where the width is under 1800 mm; that threshold is not filed as a row. Note to 3.14(b): for school buildings the preferred width is 2700 mm where lockers stand in the corridor.'+LENS_NOTE%('MOB','para 3.11 names wheelchair users passing and turning as the reason for the width'),ADMLOC%33)
# --- parameter 9, ADM Table 2
T=[('Straight-on (without a turn or 800 750 oblique approach)','straight-on approach','800','750'),
   ('At right angles to an access route 800 750 at least 1500mm wide','right angles to an access route at least 1500 mm wide','800','750'),
   ('At right angles to an access route 825 775 at least 1200mm wide','right angles to an access route at least 1200 mm wide','825','775'),
   ('External doors to buildings used 1000 775 by the general public','external doors to buildings used by the general public','1000','775')]
for q,lab,new,old in T:
    for col,val in (('new buildings',new),('existing buildings',old)):
        r(A,9,'ALL',val,'mm','>=',q,'Approved Document M Volume 2, para 2.13(b) and Table 2','UK',f'{col}; {lab}',('2','2.13','b'),
          f'Quantity: minimum effective clear width through a single leaf door, or one leaf of a double leaf door, measured as Diagram 9 shows (diagram not read). Row "{lab}", column "{col}" of Table 2, which carries both columns in one row of text. Para 3.10(b) applies the same table to internal doors.'+LENS_NOTE%('ALL','Table 2 names no population; para 2.11 lists wheelchair users among several users'),ADMLOC%27)
# --- parameter 6, ADM
F='the opening force at the leading edge of the door is not more than 30N from 0° (the door in the closed position) to 30° open, and not more than 22.5N from 30° to 60° of the opening cycle;'
r(A,6,'MOB','30','N','<=',F,'Approved Document M Volume 2, para 3.10(a)','UK','internal doors opened manually, 0 to 30 degrees',('3','3.10','a'),
  'Quantity: maximum opening force at the leading edge of an internal door, 0 to 30 degrees open. The same two figures are stated for entrance doors at para 2.13(a), in a conditional form (a powered system is required where the door cannot otherwise be opened within them); not filed twice (rule 5).'+LENS_NOTE%('MOB','para 2.9 names wheelchair users and people with limited strength as those a heavy door excludes'),ADMLOC%32)
r(A,6,'MOB','22.5','N','<=',F,'Approved Document M Volume 2, para 3.10(a)','UK','internal doors opened manually, 30 to 60 degrees',('3','3.10','a'),
  'Quantity: maximum opening force at the leading edge of an internal door, 30 to 60 degrees of the opening cycle. See the 0 to 30 degree row for the entrance-door repeat at para 2.13(a).'+LENS_NOTE%('MOB','para 2.9'),ADMLOC%32)
# --- parameter 8, ADM
L='in light reflectance value between the two surfaces is greater than 30 points.'
r(A,8,'BLIND','30','points','>',L,'Approved Document M Volume 2, para 0.26, definition of contrast visually','UK','two adjoining surfaces; default case',('0','0.26',None),
  'Quantity: difference in light reflectance value (LRV, 0 to 100 scale) between two surfaces for them to count as contrasting visually. The sentence begins on the previous page (PDF page 16 ends "the difference"); the quote starts at the page break. Strictly greater than 30 points.'+LENS_NOTE%('BLIND','paras 3.8 and 3.12 give people with impaired sight as the reason for visual contrast of doors and walls'),ADMLOC%17)
r(A,8,'BLIND','20','points','>=','Where illuminance on surfaces is greater than 200 lux, a difference in light reflectance value should be a minimum of 20 points.','Approved Document M Volume 2, para 0.26, definition of contrast visually','UK','two adjoining surfaces; illuminance above 200 lux',('0','0.26',None),
  'Quantity: reduced LRV difference permitted where illuminance on the surfaces exceeds 200 lux. A relaxation of the 30 point figure, stated as an alternative, not as a condition on a row of another parameter (illuminance is not a parameter here).'+LENS_NOTE%('BLIND','as the 30 point row'),ADMLOC%17)
r(A,8,'BLIND','15','points','>=','Where door opening furniture projects beyond the face of the door or otherwise creates enhanced differentiation and shade, a minimum difference in light reflectance value of 15 points is considered adequate.','Approved Document M Volume 2, para 0.26, definition of contrast visually','UK','door opening furniture projecting beyond the face of the door',('0','0.26',None),
  'Quantity: reduced LRV difference considered adequate where door opening furniture projects or otherwise creates differentiation and shade. A relaxation of the 30 point figure.'+LENS_NOTE%('BLIND','as the 30 point row'),ADMLOC%17)
# --- ADA
B='REF-00987'
def ada(p,lens,val,unit,cmp_,quote,sec,loc,setting,note,why):
    r(B,p,lens,val,unit,cmp_,quote,'2010 ADA Standards for Accessible Design, '+sec,'US',setting,loc,note+LENS_NOTE%(lens,why),'ada.gov 2010 Standards page, HTML as retrieved 2026-10-30')
ada(4,'MOB','915','mm','>=','the clear width of walking surfaces shall be 36 inches (915 mm) minimum.','403.5.1',('4','403.5.1',None),'accessible routes','Quantity: minimum clear width of a walking surface on an accessible route. The source states inches with the millimetre figure beside it; the millimetre figure is the one filed. The exception permits 815 mm for a length of 610 mm maximum, with 1220 mm long, 915 mm wide segments between; not filed as a row.','chapter 4 is titled accessible routes and the surrounding clauses (403.5.2) set widths for turning around wheelchair-sized elements')
ada(5,'MOB','1525','mm','>=','The turning space shall be a space of 60 inches (1525 mm) diameter minimum.','304.3.1',('3','304.3.1',None),'turning space, circular','Quantity: minimum diameter of the circular turning space. 304.3.2 allows a T-shaped space within a 1525 mm square as the alternative; not filed as a row. Millimetre figure filed as stated beside the inch figure.','section 304 is titled turning space and is a wheelchair provision')
ada(6,'ALL','22.2','N','<=','Interior hinged doors and gates: 5 pounds (22.2 N) maximum.','404.2.9',('4','404.2.9',None),'interior hinged doors and gates','Quantity: maximum force to push or pull open an interior hinged door. The same figure is stated for sliding or folding doors in the next line, and for operable parts at 309.4; not filed twice. Fire doors are left to the administrative authority.','404.2.9 names no population')
ada(9,'MOB','815','mm','>=','Door openings shall provide a clear width of 32 inches (815 mm) minimum.','404.2.3',('4','404.2.3',None),'door openings; clear width','Quantity: minimum clear width of a door opening, measured between the face of the door and the stop with the door open 90 degrees; 915 mm where the opening is more than 610 mm deep.','the measurement basis is a swung-open door, the wheelchair-passage case')
ada(11,'ALL','2030','mm','>=','Vertical clearance shall be 80 inches (2030 mm) high minimum.','307.4',('3','307.4',None),'protruding objects; walkway vertical clearance','Quantity: minimum vertical clearance. Door closers and door stops may be 1980 mm minimum (exception, not filed). Guardrails are required where clearance is less.','307.4 names no population')
for ref,p,lens,val,unit,cmp_,quote,sec,jur,setting,loc,note,locnote in rows:
    cmd=['python3','scripts/db.py','add-extraction','--ref-id',ref,'--parameter-id',str(p),'--identity',lens,'--claim-type','numerical','--claimed-value',val,'--claimed-unit',unit,'--claim-text',quote,'--source-section',sec,'--jurisdiction',jur,'--setting',setting,'--extraction-method','skim','--extraction-status','preliminary','--figure-role','claim','--comparator',cmp_,'--relation','none','--locator-scheme','section','--loc-section',loc[0],'--loc-note',locnote,'--notes',note,'--session',SESS]
    if loc[1]: cmd+=['--loc-paragraph' if ref==A else '--loc-subsection',loc[1]]
    if loc[2]: cmd+=['--loc-clause',loc[2]]
    if DRY: cmd.append('--dry-run')
    out=subprocess.run(cmd,env={**os.environ,'GUIDEBOOK_DB_PATH':DB},capture_output=True,text=True)
    tail=(out.stdout+out.stderr).strip().splitlines()
    ok='"extraction_id"' in out.stdout
    print(ref,p,val,unit,'OK' if ok else 'FAIL: '+' | '.join(tail[-3:]))
