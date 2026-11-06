import subprocess,os,sys
SESS='session_2026-11-06-pipeline-batch'
DB=os.path.abspath('scratchpad/session_2026-11-06-pipeline-batch/walk.db')
ED='PDF page %s of 74; 2015 edition incorporating 2020 and 2024 amendments'
LN=" Lens ALL: the clause names no population [ASSUMPTION: ALL is the scope marker for a provision whose own text names no one]."
UNIT=" Unit filed as the source states it (metres); a row in millimetres from another source will not compose with it until the engine owns a length family (GAP-072)."
Q113='it has a surface width of at least 1.5m, with passing places, free of obstructions to a height of 2.1m;'
rows=[
 ('REF-00992',4,'1.5','m','>=',Q113,'Approved Document M Volume 2, para 1.13(a)','UK','level approach to a building entrance',('1','1.13','a'),ED%19,'Quantity: minimum surface width of a level approach, with passing places. Para 1.13(b) sets the passing places (1.8 m wide, 2 m long, not more than 50 m apart); not filed as rows.'+LN+UNIT),
 ('REF-00992',11,'2.1','m','>=',Q113,'Approved Document M Volume 2, para 1.13(a)','UK','level approach to a building entrance',('1','1.13','a'),ED%19,'Quantity: height to which the level approach is to be free of obstructions, which is the headroom clearance over the route. Read from the same sentence as the width row (parameter 4); the sentence states two quantities.'+LN+UNIT),
 ('REF-00992',4,'1800','mm',None,'A surface width of 1800mm can accommodate any amount of non-vehicular traffic without the need for passing places.','Approved Document M Volume 2, para 1.11','UK','approach routes outside buildings',('1','1.11',None),ED%18,'Quantity: surface width that accommodates any amount of non-vehicular traffic without passing places. A design consideration ("can accommodate"), not a provision; no comparator is stated.'+LN),
 ('REF-00992',4,'1200','mm',None,'A surface width of 1200mm may be acceptable on restricted sites, subject to agreement with the building control body.','Approved Document M Volume 2, para 1.11','UK','approach routes outside buildings, restricted sites',('1','1.11',None),ED%18,'Quantity: surface width that may be acceptable on restricted sites with the building control body\'s agreement. A design consideration ("may be acceptable"), not a provision; no comparator is stated.'+LN),
 ('REF-00992',4,'1.5','m','>=','it has a surface width between walls, upstands or kerbs of at least 1.5m;','Approved Document M Volume 2, para 1.26(e)','UK','ramp between walls, upstands or kerbs',('1','1.26','e'),ED%21,'Quantity: minimum surface width of a ramp between walls, upstands or kerbs.'+LN+UNIT),
 ('REF-00987',4,'915','mm','>=','The clear width of a ramp run and, where handrails are provided, the clear width between handrails shall be 36 inches (915 mm) minimum.','2010 ADA Standards for Accessible Design, 405.5','US','ramp run; between handrails',('4','405.5',None),'ada.gov 2010 Standards page, HTML as retrieved 2026-10-30','Quantity: minimum clear width of a ramp run, and between handrails where provided. Millimetre figure filed as stated beside the inch figure. The exception for employee work areas is not filed.'+LN),
]
for ref,p,val,unit,cmp_,quote,sec,jur,setting,loc,locnote,note in rows:
    c=['python3','scripts/db.py','add-extraction','--ref-id',ref,'--parameter-id',str(p),'--identity','ALL','--claim-type','numerical','--claimed-value',val,'--claimed-unit',unit,'--claim-text',quote,'--source-section',sec,'--jurisdiction',jur,'--setting',setting,'--extraction-method','skim','--extraction-status','preliminary','--figure-role','claim','--relation','none','--locator-scheme','section','--loc-section',loc[0],'--loc-note',locnote,'--notes',note,'--session',SESS]
    if cmp_: c+=['--comparator',cmp_]
    if loc[1]: c+=['--loc-paragraph' if ref=='REF-00992' else '--loc-subsection',loc[1]]
    if loc[2]: c+=['--loc-clause',loc[2]]
    o=subprocess.run(c,env={**os.environ,'GUIDEBOOK_DB_PATH':DB},capture_output=True,text=True)
    print(ref,p,val,unit,'OK' if '"extraction_id"' in o.stdout else 'FAIL '+(o.stdout+o.stderr)[-300:])
