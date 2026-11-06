"""Write ../equivalents.tsv and check every quote against the saved text; exit 1 on any miss.
Run from the repo root: python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/ZH-CN/tools/equiv_build.py
Match is on whitespace-stripped text (pdftotext -layout inserts spaces and line breaks inside CJK runs).
Texts under ../text/ are local and not committed; each is named by the artefact sha256 prefix in the retrieval log."""
import csv, os, re, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
S = {  # key: (title as written, issuer, URL, text file, text kind, tier)
 'GB': ('建筑与市政工程无障碍通用规范 GB 55019-2021', '住房和城乡建设部', 'https://www.gov.cn/zhengce/zhengceku/2022-03/30/5682480/files/136d6deb037942068a290c9d2c28789f.pdf', 'ee78b16e1dec13b8', 'TRANSCRIPTION (OCR, hand-corrected; image-only PDF)', '1'),
 'LAW': ('中华人民共和国无障碍环境建设法', '全国人民代表大会常务委员会 (republished by 12371.cn, source 新华社)', 'https://www.12371.cn/2023/06/29/ARTI1687994873832995.shtml', '575638778aada9c1', 'extracted (HTML tags stripped)', '1'),
 'REG12': ('无障碍环境建设条例 (国务院令第622号, 2012)', '国务院', 'https://www.gov.cn/flfg/2012-07/10/content_2179947.htm', '74b8d2c5429630c9', 'extracted (HTML tags stripped)', '2'),
 'BJREG': ('北京市无障碍环境建设条例 (2021)', '北京市人民代表大会常务委员会', 'https://www.beijing.gov.cn/zhengce/dfxfg/202110/W020230904572688598051.pdf', '23135cb9ffb84656', 'extracted (pdftotext)', '2'),
 'MZ': ('养老服务常用图形符号及标志 MZ/T 131—2019', '中华人民共和国民政部', 'https://www.gov.cn/xinwen/2019-12/24/5463665/files/4bb69f1b9c8743c7aedd9f1b44858f1a.pdf', '600c6137712d20e2', 'extracted (pdftotext)', '3'),
 'BJG': ('北京无障碍城市设计导则 (Urban Design Guidelines for Accessibility of Beijing)', 'hosted by 北京市规划和自然资源委员会', 'https://ghzrzyw.beijing.gov.cn/biaozhunguanli/bz/qt/202106/P020210624562130214835.pdf', 'a3650e08fd144a75', 'extracted (pdftotext; columns interleave)', '4'),
}
L = {'R2-050': 'designated accessible spaces', 'R2-051': 'parking spaces for limited mobility users', 'R2-281': 'Parking',
     'R2-333': 'Accessible', 'R2-163': 'Elevators', 'R2-164': 'Elevating devices', 'R2-166': 'elevator lobbies',
     'R2-168': 'Platform lifts', 'R2-169': 'stair lift', 'R2-174': 'Escalators', 'R2-083': 'Ramp', 'R2-059': 'Curb ramps',
     'R2-072': 'Accessible route', 'R2-176': 'Washroom facilities', 'R2-177': 'Universal washrooms', 'R2-178': 'Toilet stalls',
     'R2-201': 'Signage', 'R2-111': 'accessible seating spaces', 'R2-093': 'Tactile walking surface indicator'}
CODE, COLL, REG, OLD, QUAL, SEED = 'code term', 'colloquial', 'regional variant', 'outdated or disfavoured', 'qualifier', 'unattested seed'
# concept, form, jur, usage, scope_note, src, locator, quote, conflation_note, check ('text' | 'image' | 'none')
R = [
 # parking
 ('R2-050', '无障碍机动车停车位', 'CN', CODE, 'the code term; 机动车 (motor vehicle) is explicit', 'GB', '2.9 heading; 2.9.1', '应将通行方便、路线短的停车位设为无障碍机动车停车位。', '', 'text'),
 ('R2-050', '停车位', 'CN', CODE, 'BROADER: any parking space; the accessible bay is designated from among them (2.9.1)', 'GB', '2.9.1', '应将通行方便、路线短的停车位设为无障碍机动车停车位。', '', 'text'),
 ('R2-050', '无障碍停车位', 'CN', CODE, 'statute form, without 机动车; priority (优先) use by vehicles driven by or carrying 肢体残疾人, others when spaces suffice', 'LAW', 'art. 24', '停车场应当按照无障碍设施工程建设标准，设置无障碍停车位，并设置显著标志标识。', 'art. 24 para. 3 opens the same bay to 其他行动不便的残疾人、老年人、孕妇、婴幼儿 when spaces suffice: CN keeps one bay with a user order, where B651 has a second class (R2-051). Not settled.', 'text'),
 ('R2-050', '无障碍停车位', 'CN', OLD, 'same form; the 2012 regulation made the bay exclusive (专用) to 肢体残疾人 vehicles, where the 2023 law gives priority (优先); status of the 2012 regulation after the 2023 law UNVERIFIED', 'REG12', 'art. 14', '无障碍停车位为肢体残疾人驾驶或者乘坐的机动车专用。', 'one form, two scopes over time (exclusive 2012, priority 2023)', 'text'),
 ('R2-050', '无障碍停车位', 'CN-BJ', REG, 'Beijing statute; exclusive use and a permit (肢体残疾人证) to be shown', 'BJREG', 'art. 17 (PDF p.7)', '使用无障碍停车位的，驾驶人或者乘坐人应当出示肢体残疾人证。', '', 'text'),
 ('R2-050', '泊位', 'CN-BJ', CODE, 'BROADER: generic word for a bay, used to count accessible bays in the penalty clause', 'BJREG', 'art. 39 (PDF p.12)', '每个泊位处一万元罚款', '', 'text'),
 ('R2-050', '无障碍停车位', 'CN', CODE, 'signage name of a public-information symbol, reproduced from GB/T 10001.9-2008 (06); its gloss narrows users to 残疾人', 'MZ', 'table A.1 no. 40 (PDF p.18, printed p.14)', '表示供残疾人使用的停车位', '', 'text'),
 ('R2-050', '无障碍车位', 'CN-BJ', COLL, 'shortened form in municipal guidance, same object as the code term on the same page', 'BJG', 'PDF p.58', '无障碍车位应靠近站场垂直电梯处，并应设置无障碍标识。', '', 'text'),
 ('R2-050', '无障碍机动车停车位', 'CN-BJ', CODE, 'guidance repeats the code term; the diagram on the same page is captioned 无障碍停车位示意图', 'BJG', 'PDF p.54', '无障碍机动车停车位应靠近出入口', 'two forms for one object on one page; read as equivalent, not a conflation', 'text'),
 ('R2-050', '残疾人专用停车位', 'CN', SEED, 'MODEL-GENERATED seed, flagged. Seen only in search-engine summaries of a Sichuan report (news, excluded) and a Shenzhen draft notice (sf.sz.gov.cn, TLS failure, not retrieved); not attested by any text read', '', '', '', '', 'none'),
 ('R2-281', '停车场', 'CN', CODE, 'the car park as a setting', 'LAW', 'art. 24', '停车场应当按照无障碍设施工程建设标准，设置无障碍停车位', '', 'text'),
 # qualifier class
 ('R2-333', '无障碍', 'CN', QUAL, 'the code and statute umbrella word (literally barrier-free); scope WIDER than disabled people: 残疾人、老年人等有需求的人', 'GB', '1.0.3(1)', '满足残疾人、老年人等有需求的人使用，消除他们在社会生活上的障碍；', '', 'text'),
 ('R2-333', '无障碍', 'CN', QUAL, 'statute: beneficiaries 残疾人、老年人, extended to anyone with a 无障碍需求', 'LAW', 'art. 2', '残疾人、老年人之外的其他人有无障碍需求的，可以享受无障碍环境便利。', '', 'text'),
 ('R2-333', '通用设计理念', 'CN', QUAL, 'universal design as a promoted idea, beside 无障碍; WIDER (general population)', 'LAW', 'art. 51', '国家推广通用设计理念', '', 'text'),
 ('R2-333', '无障碍通用设计', 'CN', QUAL, 'compound joining both umbrella words as one modifier', 'REG12', 'art. 6', '国家鼓励、支持采用无障碍通用设计的技术和产品', 'treats 无障碍 and 通用设计 as one; and the same article contrasts it with 残疾人专用 (next row)', 'text'),
 ('R2-333', '残疾人专用', 'CN', QUAL, 'NARROWER: for disabled people only, set against 无障碍通用设计 in one sentence', 'REG12', 'art. 6', '推进残疾人专用的无障碍技术和产品的开发、应用和推广。', '', 'text'),
 ('R2-333', '无障碍通用设计', 'CN-BJ', REG, 'Beijing statute repeats the compound', 'BJREG', 'art. 7 (PDF p.3)', '鼓励采用无障碍通用设计的技术和产品', '', 'text'),
 ('R2-333', '通用设计', 'CN-BJ', QUAL, 'a principle of the Beijing statute, listed with 合理便利 (reasonable accommodation)', 'BJREG', 'art. 3 (PDF p.2)', '遵循通用设计、合理便利、广泛受益的原则', '', 'text'),
 ('R2-333', '通用', 'CN', CODE, 'NOT the qualifier: in the code title, 通用规范 means a general (cross-cutting) technical code, per the 前言', 'GB', '前言 (printed p.4)', '分为工程项目类规范（简称项目规范）和通用技术类规范（简称通用规范）两种类型', 'CONFLATION RISK: the title 建筑与市政工程无障碍通用规范 reads as "barrier-free universal code" to a reader who takes 通用 as universal design; the instrument defines 通用 as general. Recorded, not resolved.', 'text'),
 ('R2-333', '国际通用', 'CN-BJ', QUAL, 'NOT universal design: 通用 = commonly used internationally (signage standards)', 'BJG', 'PDF p.61 (3.6.2)', '无障碍标识尺寸与颜色应符合国际通用标准要求', 'the same guide uses 通用 for universal design (PDF p.21) and for "common" here', 'text'),
 ('R2-333', '通用包容', 'CN-BJ', QUAL, 'municipal guidance pairs universal and inclusive as one quality of 无障碍城市设计', 'BJG', 'PDF p.4', '通用包容是无障碍城市设计的核心品质', '', 'text'),
 ('R2-333', '包容性', 'CN-BJ', QUAL, 'defined by the guide in terms of 能力障碍者 (persons with impaired ability): the project scope', 'BJG', 'PDF p.21 (1.4.2)', '“包容性”即：全部的能力障碍者均可平等参与各类社会活动', '', 'text'),
 ('R2-333', '通用性', 'CN-BJ', QUAL, 'WIDER: defined over everyone walking or using any non-motorised mobility device (wheelchair, pram, skateboard, bicycle)', 'BJG', 'PDF p.21 (1.4.2)', '所有人步行或使用任何非机动代步器具', '', 'text'),
 ('R2-333', '全龄友好', 'CN-BJ', COLL, 'all-ages-friendly; the nearest form to "... friendly"; WIDER, keyed to age and to all people', 'BJG', 'PDF p.20', '体现全龄友好的城市和建筑的设计理念', '', 'text'),
 ('R2-333', '适老化', 'CN', QUAL, 'age-adapted; a different population (older people), joined to 无障碍环境建设 by statute', 'LAW', 'art. 4', '无障碍环境建设应当与适老化改造相结合', 'the statute couples two scopes (disability, ageing) under one programme', 'text'),
 ('R2-333', '无障碍设施', 'CN', QUAL, 'symbol name; gloss uses 残障人 where the next symbol in the same table uses 残疾人', 'MZ', 'table A.1 no. 39 (PDF p.18, printed p.14)', '表示供残障人使用的设施，如轮椅', '', 'text'),
 # vertical transport
 ('R2-163', '无障碍电梯', 'CN', CODE, 'NARROWER: the accessible subset of 电梯 that a public building must have one of', 'GB', '2.6.4', '公共建筑内设有电梯时，至少应设置1部无障碍电梯。', '', 'text'),
 ('R2-163', '电梯', 'CN', CODE, 'the general word; in this code a car-type lift (escalators are 自动扶梯)', 'GB', '2.6.4', '公共建筑内设有电梯时，至少应设置1部无障碍电梯。', '', 'text'),
 ('R2-163', '电梯', 'CN', CODE, 'statute: retrofit of lifts in older multi-storey housing (加装电梯)', 'LAW', 'art. 22', '国家支持城镇老旧小区既有多层住宅加装电梯或者其他无障碍设施', '', 'text'),
 ('R2-163', '无障碍电梯', 'CN-BJ', REG, 'Beijing statute, metro stations', 'BJREG', 'art. 16 (PDF p.7)', '确实不具备加装无障碍电梯条件的', '', 'text'),
 ('R2-163', '电梯', 'CN', CODE, 'symbol name, from GB/T 10001.1-2012 (013)', 'MZ', 'table A.1 no. 4 (PDF p.9, printed p.5)', '表示公用电梯或其位置', '', 'text'),
 ('R2-163', '垂直电梯', 'CN-BJ', COLL, '"vertical" 电梯, written beside 扶梯 to exclude the escalator', 'BJG', 'PDF p.19', '设有垂直电梯或扶', 'implies 电梯 alone can cover escalators; the national 电梯 definition (special-equipment rules) was not retrieved', 'text'),
 ('R2-163', '无障碍垂直电梯', 'CN-BJ', COLL, 'list item, metro stations', 'BJG', 'PDF p.37', '无障碍垂直电梯', '', 'text'),
 ('R2-163', '直梯', 'CN-BJ', COLL, 'short colloquial form in a speech bubble (a traveller with luggage), set against 扶梯', 'BJG', 'PDF p.11 (printed p.18), read from the page image', '带着大件行李，还是坐直梯吧。', '', 'image'),
 ('R2-163', '天桥升降梯', 'CN-BJ', COLL, 'footbridge lift, in a list of crossing elements', 'BJG', 'PDF p.37', '天桥升降梯', 'the figure caption on PDF p.42 says 人行天桥电梯 for what may be the same object; whether it is an elevator or a platform lift is not stated; not judged', 'text'),
 ('R2-163', '人行天桥电梯', 'CN-BJ', COLL, 'figure caption', 'BJG', 'PDF p.42', '人行天桥电梯实例图', 'see 天桥升降梯 (PDF p.37)', 'text'),
 ('R2-164', '无障碍电梯和升降平台', 'CN', CODE, 'no umbrella noun: the code heads one section with both objects', 'GB', '2.6 heading', '2.6 无障碍电梯和升降平台', '', 'text'),
 ('R2-166', '候梯厅', 'CN', CODE, 'lift lobby of an accessible lift', 'GB', '2.6.1', '无障碍电梯的候梯厅应符合下列规定：', '', 'text'),
 ('R2-168', '升降平台', 'CN', CODE, 'platform lift; one of three permitted accessible-entrance types', 'GB', '2.4.1(3); 2.6.5', '3 同时设置台阶和升降平台的出入口。', '', 'text'),
 ('R2-168', '轮椅升降机', 'CN-BJ', COLL, 'listed under temporary accessible equipment (临时无障碍设备), so possibly a portable device', 'BJG', 'PDF p.37', '临时无障碍设备●临时坡道●轮椅升降机', '升降机 is also used for lifts in other Chinese-language jurisdictions (not read here); equivalence to 升降平台 not judged', 'text'),
 ('R2-168', '垂直升降平台', 'CN', SEED, 'MODEL-GENERATED seed, flagged: the title of GB/T 24805 seen only in search summaries and sales listings; not retrieved', '', '', '', '', 'none'),
 ('R2-169', '楼道升降机', 'CN', SEED, 'MODEL-GENERATED seed, flagged: GB/T 24806 title, seen only in a sales-site link title; not retrieved', '', '', '', '', 'none'),
 ('R2-174', '自动扶梯', 'CN', CODE, 'escalator', 'GB', '2.2.5', '自动扶梯、楼梯的下部和其他室内外低矮空间可以进入时', '', 'text'),
 ('R2-174', '扶梯', 'CN-BJ', COLL, 'short form of 自动扶梯', 'BJG', 'PDF p.53', '扶梯和每层楼梯梯段起止和休息平台处应设置提示', '', 'text'),
 # other elements, second reading
 ('R2-083', '轮椅坡道', 'CN', CODE, 'the ramp in the code is named for the wheelchair', 'GB', '2.2.1', '无障碍通道上有地面高差时，应设置轮椅坡道或缘石坡道。', '', 'text'),
 ('R2-083', '无障碍坡道', 'CN', CODE, 'symbol name from GB/T 10001.9-2008 (07); users glossed as 残疾人、老年人、伤病人等', 'MZ', 'table A.1 no. 41 (PDF p.19, printed p.15)', '行动不便者使用的坡道', '', 'text'),
 ('R2-083', '无障碍坡道', 'CN-BJ', COLL, 'guidance uses both 无障碍坡道 and 轮椅坡道', 'BJG', 'PDF p.53', '出入口应设置无障碍坡道或以坡地形过渡', 'whether the guide uses the two forms for one object or for two is not stated; not judged', 'text'),
 ('R2-059', '缘石坡道', 'CN', CODE, 'kerb ramp, a separate object from 轮椅坡道', 'GB', '2.2.1', '应设置轮椅坡道或缘石坡道', '', 'text'),
 ('R2-059', '三面缘石坡道', 'CN-BJ', CODE, 'NARROWER: the three-sided type', 'BJG', 'PDF p.27', '设置三面缘石坡道', '', 'text'),
 ('R2-059', '下降式路缘石', 'CN-BJ', OLD, 'a rendering of the English "dropped curb" in a history paragraph; not used as a design term', 'BJG', 'PDF p.21', '下降式路缘石（dropped curb）', '', 'text'),
 ('R2-072', '无障碍通道', 'CN', CODE, 'the route element', 'GB', '2.2.1', '无障碍通道上有地面高差时', '', 'text'),
 ('R2-072', '无障碍通行流线', 'CN', CODE, 'the continuous route across open space, site and building', 'GB', '2.1.1', '应提供连贯的无障碍通行流线', '', 'text'),
 ('R2-072', '无障碍路线', 'CN-BJ', COLL, 'route as planned in guidance', 'BJG', 'PDF p.30', '室外场地无障碍路线', '', 'text'),
 ('R2-176', '公共卫生间（厕所）', 'CN', CODE, 'the code gives 卫生间 and 厕所 as one, in parentheses', 'GB', '3.2 heading', '3.2 公共卫生间（厕所）和无障碍厕所', '', 'text'),
 ('R2-177', '无障碍厕所', 'CN', CODE, 'stand-alone single-user room', 'GB', '3.2.3', '无障碍厕所应符合下列规定：', '', 'text'),
 ('R2-177', '无障碍卫生间', 'CN', CODE, 'in the code: the bathroom inside an accessible guest room or dwelling', 'GB', '3.4.4', '无障碍客房和无障碍住房、居室内应设置无障碍卫生间', 'CONFLATION across sources: the code keeps 无障碍卫生间 for the room inside a guest room or dwelling and 无障碍厕所 for the public stand-alone room; the Beijing guide uses 无障碍卫生间 for the public room (next row). Not settled.', 'text'),
 ('R2-177', '无障碍卫生间', 'CN-BJ', COLL, 'guidance: the public stand-alone room, with 无障碍厕位 as the fallback', 'BJG', 'PDF p.63 (3.6.3)', '公共卫生间内应设置无障碍卫生间', 'see the row above', 'text'),
 ('R2-178', '无障碍厕位', 'CN', CODE, 'cubicle inside a public toilet', 'GB', '3.2.2', '无障碍厕位应符合下列规定：', '', 'text'),
 ('R2-178', '无障碍厕位', 'CN-BJ', CODE, 'guidance repeats the code term as the fallback when no stand-alone room fits', 'BJG', 'PDF p.63', '应在公共厕所内设置无障碍厕位', '', 'text'),
 ('R2-201', '无障碍标识', 'CN', CODE, 'signage', 'GB', '4.0.1', '无障碍标识应纳入室内外环境的标识系统', 'the code uses 标识 (signage) and 标志 (symbol) in adjacent clauses 4.0.1 and 4.0.2', 'text'),
 ('R2-201', '无障碍标志', 'CN', CODE, 'the symbol or sign as an object with a mounting position', 'GB', '4.0.2', '无障碍标志的安装位置和高度', 'see the row above', 'text'),
 ('R2-111', '轮椅席位', 'CN', CODE, 'wheelchair space in seating', 'GB', '3.5.1', '轮椅席位的观看视线不应受到遮挡', '', 'text'),
 ('R2-111', '轮椅专席', 'CN-BJ', REG, 'NARROWER setting: wheelchair place in a bus or metro car', 'BJREG', 'art. 16 (PDF p.7)', '应当设置扶手、轮椅专席或者专区', '', 'text'),
 ('R2-093', '盲道', 'CN', CODE, 'tactile paving, parent of 提示盲道 and 行进盲道 (code 2.11)', 'LAW', 'art. 23', '应当按照标准设置盲道', '', 'text'),
]
COLS = ['concept_id', 'concept_label', 'form', 'language', 'jurisdiction', 'usage_type', 'scope_note', 'attestation_tier', 'source', 'locator', 'quote', 'conflation_note', 'quote_check']
def norm(s): return re.sub(r'\s+', '', s)
cache, fails, out = {}, 0, []
for c, form, jur, use, scope, src, loc, quote, conf, chk in R:
    if src:
        title, iss, url, f, kind, tier = S[src]
        if f not in cache: cache[f] = norm(open(os.path.join(D, 'text', f + '.txt'), encoding='utf-8').read())
        if chk == 'text':
            ok = norm(quote) in cache[f] and norm(form.replace('（厕所）', '')) in cache[f]
            if not ok: fails += 1; print('MISS', c, form, quote)
            qc = ('verified in ' + kind) if ok else 'MISS'
        else: qc = 'read from page image (not in extracted text)'
        source = f'{title}; {iss}; {url}'
        if len(quote) > 60: fails += 1; print('LONG', quote)
    else: tier, source, qc = 'seed', '', 'no quote (seed)'
    out.append([c, L[c], form, 'zh-Hans', jur, use, scope, tier, source, loc, quote, conf, qc])
with open(os.path.join(D, 'equivalents.tsv'), 'w', encoding='utf-8', newline='') as fh:
    w = csv.writer(fh, delimiter='\t', lineterminator='\n'); w.writerow(COLS); w.writerows(out)
print('rows', len(out), 'concepts', len({r[0] for r in out}), 'failures', fails)
sys.exit(1 if fails else 0)
