import sys, re, hashlib, sqlite3, collections
tools, root = sys.argv[1], sys.argv[2]
sys.path.insert(0, tools); import obs_data as d
S = root + '/scratchpad/session_2026-11-06-base-vocabulary-review'
OUT = S + '/terminology-pass/JA-JP'; T = OUT + '/text'
def norm(s): return re.sub(r'[ 　\t]+',' ',s)
def check(f,q):
    raw=open(f'{T}/{d.F[f]}',encoding='utf-8').read()
    if q in raw: return 'exact'
    if norm(q) in norm(raw): return 'ws-normalised'
    if q in re.sub(r'\n[ 　]*','',raw): return 'line-joined'
    return 'MISSING'
# register concepts derived from the catalogue tables, never retyped
cat = open(S+'/rhfac-b651-catalogue.md',encoding='utf-8').read()
s21 = cat.split('### 2.1')[1].split('### 2.2')[0]; s22 = cat.split('### 2.2')[1].split('## 3.')[0]
C = [r.split('|')[2].strip() for r in s21.splitlines() if re.match(r'\|\s*\d+\s*\|', r)]
tbl = s22.split('| Word | Sections |')[1].split('\n\n')[0]
Q = [r.split('|')[1].strip() for r in tbl.splitlines() if re.match(r'\|\s*[a-z]', r)]
con = sqlite3.connect(f'file:{root}/data/guidebook.db?mode=ro', uri=True)
P = con.execute("select p.parameter_id, t.canonical_en from base_parameters p join terms t using(term_id) order by 1").fetchall()
concepts = [(f'C{i+1:02d}', c, 'RHFAC recurring statement (catalogue 2.1)') for i,c in enumerate(C)]
concepts += [(f'Q-{w}', w, 'quantity-bearing word (catalogue 2.2)') for w in Q]
concepts += [(f'P{pid:02d}', n, 'active base parameter') for pid,n in P]
ids = {c[0] for c in concepts}
assert all(o[0] in ids for o in d.OBS), [o[0] for o in d.OBS if o[0] not in ids]
# observations
with open(OUT+'/observations.tsv','w',encoding='utf-8') as f:
    f.write('obs_id\tconcept_id\tconcept_label\tphrase_verbatim\tlanguage\tinstrument\tlocator\tcontext_quote_verbatim\tquote_check\tphrase_in_quote\ttext_file\n')
    lab = {c[0]:c[1] for c in concepts}
    for i,o in enumerate(d.OBS,1):
        f.write('\t'.join([f'JA-{i:03d}',o[0],lab[o[0]],o[1],'ja',d.I[o[2]],o[3],o[4],check(o[2],o[4]),str(o[1] in o[4]),'text/'+d.F[o[2]]])+'\n')
with open(OUT+'/reverse-harvest.tsv','w',encoding='utf-8') as f:
    f.write('rh_id\tphrase_verbatim\tlanguage\tinstrument\tlocator\tcontext_quote_verbatim\tquote_check\tgloss_OURS_not_an_equivalent\twhy_no_register_row\ttext_file\n')
    for i,o in enumerate(d.RH,1):
        f.write('\t'.join([f'JA-RH-{i:03d}',o[0],'ja',d.I[o[1]],o[2],o[3],check(o[1],o[3]),o[4],o[5],'text/'+d.F[o[1]]])+'\n')
n = collections.Counter(o[0] for o in d.OBS)
SHARED = {'C11':'C02','C13':'C01','C14':'C02','C25x':None,'C28':'C10','C29':'C22','Q-riser':'C16','Q-tread':'C16','Q-gradient':'C24','Q-slope':'C24','P06':'Q-force'}
NOTE = {
'C01':'law (Order 379, Ord. 114) sets no lighting duty; design standard treats it as 照明設備 / 明るさ / 足元灯',
'C02':'JA carve is 粗面 or 滑りにくい材料 (rough or slip-resistant); "firm" and "stable" have no counterpart in the law text read',
'C03':'law: 休憩の用に供する設備 (guidance tier only, corridors); 優先席 is the transport/priority-seat sense',
'C05':'law writes bare 幅; design standard writes 有効幅員 and defines its measurement for doors',
'C06':'statutory route types: 移動等円滑化経路, 視覚障害者移動等円滑化経路, 車椅子使用者用経路',
'C07':'design standard only (排水溝, 溝蓋, 水はけ); not in the law text',
'C08':'law: 標識 (signs at facilities) and 案内板/案内設備 (layout boards); JIS Z 8210 pictograms by reference (not obtained)',
'C09':'law: lift voice announcements only; design standard: 集団補聴装置（ヒアリングループシステム）, 光警報装置, 情報伝達設備',
'C10':'landing defined by rise interval and 踏幅, not by clear space',
'C12':'located by grep only; approach space expressed as 接近 / 前面のスペース',
'C15':'design standard: 上屋, 屋根、庇 (snow/rain); not in law',
'C16':'Ord. 114 sets both; design standard spells けあげ in kana and gives the T+2R relation',
'C18':'design standard: 蹴込み板 / 蹴込み寸法',
'C19':'no threshold noun: the clause is 戸の前後に高低差がない; design standard adds 下枠の立ち上がり',
'C20':'only in a design-example caption (parking under pilotis); no clearance rule found in the parts read',
'C21':'立ち上がり / 脱輪防止 / 車椅子当たり (design standard)',
'C22':'contrast carved as 色の明度、色相又は彩度の差 (law) and 輝度比 (design standard); strip = 滑り止め',
'C23':'点状ブロック等 defined in Order Art.11; JIS T 9251 not obtained',
'C24':'勾配 (gradient) and 傾斜 (incline) both used; source text carries ruby on 勾 in two clauses',
'C25':'located by grep only (水栓金具 レバー式/センサー式)',
'C26':'design standard 18.5 sets centre heights',
'C27':'電子レンジ: 0 hits in design-standard text; not treated by the law texts read in full',
'C30':'located by grep only (changing rooms)',
'C31':'door operation carved as a structure (自動的に開閉する構造…) not as hardware; hardware = 取っ手 / ドアクローザー in design standard',
'C32':'law: 制御装置 for lifts only',
'C04':'手すり; JA distinguishes one side vs 両側 by tier',
'C17':'段鼻の突き出し',
'Q-height':'高さ throughout; example 受け口の高さ (urinal rim)',
'Q-level':'高低差 / 水平',
'Q-width':'幅',
'Q-clearance':'only クリアランス (hinge gap) found — a different sense; no general clearance word',
'Q-number':'数, mostly as count rules by proportion',
'Q-depth':'奥行き (lift car, lobby)',
'Q-force':'only qualitative 軽い力; no force quantity in law or in parts read',
'Q-time':'閉鎖作動時間 (door closer)',
'Q-size':'寸法',
'Q-volume':'located by grep only (音量, in an auditorium context)',
'Q-capacity':'定員 / 積載荷重 (lifts, platform lifts), grep only',
'Q-distance':'経路の長さ; also 五十メートル以内ごと interval',
'Q-lighting levels':'照度, grep only; no lux value found in parts read',
'Q-ratio':'proportional count rules (百分の一を乗じて得た数); 輝度比 is under C22',
'P03':'勾配 of 傾斜路, with separate indoor/outdoor and tier values',
'P04':'廊下等 (defined) / 屋内の通路; width with a passing-place alternative (すれ違い)',
'P05':'carved by function: 車椅子の転回に支障がない場所, 140㎝角, 直径150㎝以上の円; 回転 vs 転回（方向転換）',
'P07':'no 残響 in any text; carved as 響きの抑制 (suppressing reverberance) without a time quantity',
'P08':'no LRV; 明度差, 輝度比, 輝度コントラスト',
'P09':'出入口 幅 (law) / 出入口の有効幅員 (design standard)',
'P10':'色温度: 0 hits in design standard; not in law texts read in full',
'P11':'no headroom minimum found; treated as collision hazard (十分な高さのない空間, 突出物)',
'P12':'law carves landings by rise (高さ七十五センチメートル以内ごと), not run length; design standard mentions 傾斜路の距離 only for signage',
}
with open(OUT+'/coverage.tsv','w',encoding='utf-8') as f:
    f.write('concept_id\tconcept_label\tsource_of_concept\tstatus\tn_observations\tnote\n')
    for cid,lab_,src in concepts:
        k = n.get(cid,0); sh = SHARED.get(cid)
        weak = k and all('page not read in full' in o[3] for o in d.OBS if o[0]==cid)
        if k: st='FOUND (grep-located; page not read in full)' if weak else 'FOUND'
        elif sh: st=f'FOUND (shared with {sh})'; k=n.get(sh,0)
        elif cid in ('C27','P10'): st='SEARCHED-ABSENT'
        else: st='NOT-READ'
        f.write('\t'.join([cid,lab_,src,st,str(k),NOTE.get(cid, NOTE.get(sh or '', ''))])+'\n')
print(len(concepts), 'concepts;', len(d.OBS), 'obs;', len(d.RH), 'rh')
