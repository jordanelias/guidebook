import re, json, collections, sqlite3, sys
sys.path.insert(0,'/tmp/claude-0/-home-user-guidebook/85c53b12-0695-5c1e-b998-83da3eff20b4/scratchpad/build')
from parse import parse, SCR
OUT='/home/user/guidebook/scratchpad/session_2026-11-06-base-vocabulary-review'
rows=parse(f'{SCR}/rhfac_clean.txt')

# ---- section titles from the survey's own table of contents ----
toc=[l.strip() for l in open(f'{SCR}/rhfac_clean.txt',encoding='utf-8')][:200]
titles={}; chap={}
i=0
pend=None
for s in toc:
    m=re.match(r'^(\d{1,2})\.\s+([A-Z].*)$',s)
    if m and not re.match(r'^\d+\.\d',s): chap[m.group(1)]=m.group(2).strip(); continue
    m=re.match(r'^(\d{1,2}\.\d{1,2})\s+(.*?)(?:\s+(\d{1,2}))?$',s)
    if m and not re.match(r'^\d+\.\d+\.\d',s):
        titles[m.group(1)]=m.group(2).strip(); pend=m.group(1); continue
    if pend and not m and not re.match(r'^\d',s) and titles.get(pend) is not None and not re.search(r'\d$',titles[pend]) and len(s)<70:
        mm=re.match(r'^(.*?)(?:\s+(\d{1,2}))?$',s)
        if '(' in s or s[0].islower() or s.startswith('and') or s.startswith('Meeting') or s.startswith('Service') or s.startswith('Accommodation') or s.startswith('to '):
            titles[pend]+=' '+mm.group(1)
# repair known wraps by their TOC lines
fix={'3.1':'Interior Doors and Doorways (not including Washrooms)','4.2':'Reception Desks, Service Counters, and Self-Service Transaction Kiosks',
 '4.3':'Waiting Areas, General Seating, Meeting Rooms, and Lounges','6.3':'Directory Boards and Information Kiosks','7.1':'Emergency Exits and Areas of Refuge',
 '8.4':'Lodging and Temporary Accommodation','9.2':'Unit Entrance and Entrance to Outdoor Spaces','10.4':'Trail and Pathway Wayfinding and Signage',
 '8.19':'Family and Nursing Rooms','8.20':'Specialized Learning Spaces','8.23':'Respite and Sensory Rooms','12.1':'Technology Use','12.2':'Website Information','12.3':'Innovation'}
titles.update(fix)
chap={'1':'Vehicular Access','2':'Exterior Approach and Entrance','3':'Interior Circulation','4':'Interior Services and Environment','5':'Sanitary Facilities',
 '6':'Wayfinding and Signage','7':'Emergency Systems','8':'Additional Use of Spaces','9':'Residential Units','10':'Trails and Pathways','11':'Mind-Friendly Environments','12':'Technology & Innovation'}
KIND={'1':'site element','2':'site element','3':'building element','4':'room / space','5':'room / space','6':'system','7':'system','8':'building typology / room','9':'dwelling room / element','10':'outdoor typology','11':'cross-cutting','12':'cross-cutting'}

# ---- technique tags: transparent rules on the criterion's own words; multi-tag ----
TAGS=[
('circulation_geometry', r'clear (width|space|opening)|path of travel|pathway|manoeuvr|maneuv|passing|rest area|line-up|queuing|layout|logical|direct|corridor|route|approach|turning'),
('vertical_transitions', r'\bramp|stair|riser|tread|nosing|landing|elevator|lift\b|escalator|moving walkway|level (change|threshold)|slope|gradient|curb|threshold|step'),
('surfaces_and_slip', r'slip|firm|stable|surface|floor(ing)? (finish|surface)|flooring|carpet|drainage|deck|upholster|pattern'),
('doors_and_entries', r'\bdoor|entrance|entry|gate|turnstile|hardware|handle|threshold|opening time|hold-open|power-operated|vision panel|kick plate|force'),
('reach_and_heights', r'height|reach|knee clearance|within (easy )?reach|accessible (height|location)|mounting|mounted|outlet|switch|counter|desk|table|sink|shelf|shelves|rod|locker|mailbox|control'),
('lighting_and_glare', r'illuminat|lighting|glare|daylight|light\b|reflect|window'),
('colour_and_contrast', r'contrast|colour|color|busy pattern|high contrast|palette'),
('tactile_and_detectable', r'tactile|truncated|cane detect|detectable|braille|raised|attention indicator|edge protection|obstacle|overhead|protruding|height clearance'),
('wayfinding_and_signage', r'signage|\bsign\b|signs|wayfinding|directory|pictogram|symbol|lettering|landmark|numbering|identif|interpretive|distance marker|trailhead|map'),
('acoustic_and_audio', r'acoustic|noise|sound|audio|hearing|speaker|paging|volume|ambient|voice|audible'),
('communication_and_information', r'communication|information|alternative (media|formats|languages)|visual and audible|notification|website|intercom|interactive|kiosk|menu|prices|printed'),
('sanitary_and_fixtures', r'washroom|toilet|urinal|grab bar|shower|bathtub|faucet|flush|plumbing|ablution|change table|toilet paper|fixture|sink|drinking fountain|fume hood|eyewash'),
('seating_and_furniture', r'seating|seat\b|chair|table|bench|furniture|bed\b|upholster|workstation|desk|picnic'),
('emergency_and_life_safety', r'emergency|fire|alarm|evacuation|refuge|exit|first aid|fail-safe|safety|guard|barrier'),
('sensory_and_cognitive', r'sensory|strobing|flicker|scent|restoration|biophilic|respite|calming|stimulation|predictab|orientation|memory|mind-friendly|temperature|toys'),
('thermal_and_air', r'temperature|thermal|scent|ventilation|air'),
('provision_and_quantity', r'number of|adequate number|ratio|variety of|options|mix of|additional rooms|designated|dedicated|expected (use|usage)'),
('operation_and_technology', r'technology|training|maintenance|wifi|policy|innovation|staff|payment|security and entry|self-service|vending|automated|controls? for power'),
('outdoor_and_site', r'parking|drop-off|transit|pedestrian crossing|shelter|curb|trail|viewpoint|playground|patio|balcony|outdoor|picnic|service dog relief|ev charging|electric vehicle'),
]
def tags(text):
    t=text.lower(); return [n for n,rx in TAGS if re.search(rx,t)]

# ---- normalised concept phrase, for recurrence across sections ----
def concept(text):
    t=text.lower()
    t=re.sub(r'\([^)]*\)','',t); t=re.sub(r'\bif [a-z ,/-]*$','',t)
    t=re.sub(r'\b(is|are|has|have|include|includes|with|and|or|at|the|a|an|of|to|for|on|in)\b',' ',t)
    t=re.sub(r'[^a-z -]',' ',t); t=re.sub(r'\s+',' ',t).strip()
    return t
data=[]
for r in rows:
    sec=r['code'].rsplit('.',1)[0]; ch=sec.split('.')[0]
    data.append({'code':r['code'],'chapter':ch,'chapter_title':chap[ch],'kind':KIND[ch],'section':sec,'section_title':titles.get(sec,'?'),
                 'text':re.sub(r'\s+',' ',r['text']).strip(),'points':r['points'],'techniques':tags(r['text'])})
json.dump(data,open(f'{SCR}/build/criteria.json','w'),ensure_ascii=False)
with open(f'{OUT}/rhfac-criteria.tsv','w',encoding='utf-8') as f:
    f.write('code\tchapter\tkind\tsection\tsection_title\tcriterion_text (Canadian English, as the survey words it)\tmax_points\ttechnique_tags (rule-assigned lead; see catalogue section 3)\n')
    for d in data:
        f.write('\t'.join([d['code'],d['chapter_title'],d['kind'],d['section'],d['section_title'],d['text'],str(d['points']),';'.join(d['techniques'])])+'\n')
print(len(data), 'untitled sections:', sorted({d['section'] for d in data if d['section_title']=='?'}))
print('untagged:', sum(1 for d in data if not d['techniques']))
