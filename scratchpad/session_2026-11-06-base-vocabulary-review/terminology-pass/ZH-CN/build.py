"""Build observations / coverage / reverse-harvest TSVs for the ZH-CN terminology pass and verify every quote
against the saved text (whitespace removed on both sides, since Chinese has no word spacing). Run from the repo root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/ZH-CN/build.py
Exits 1 if any quote is not in the saved text or any phrase is not in its quote. Register concepts are DERIVED
(catalogue 2.1 and 2.2 tables, b651-headings.tsv last column, base_parameters read-only), never retyped.
Adapted from FR-FR/build.py and JA-JP/tools/build.py. Writes only the TSVs in this folder.
CAVEAT: text/ee78b16e1dec13b8.txt is a corrected OCR TRANSCRIPTION of an image-only PDF, not the artefact's bytes."""
import re, sys, csv, sqlite3
S = 'scratchpad/session_2026-11-06-base-vocabulary-review'
D = S + '/terminology-pass/ZH-CN'
INST = {
 'G': ('GB 55019-2021《建筑与市政工程无障碍通用规范》', D + '/text/ee78b16e1dec13b8.txt'),
 'L': ('《中华人民共和国无障碍环境建设法》(2023)', D + '/text/575638778aada9c1.txt'),
}
def norm(s): return re.sub(r'\s+', '', s)
TXT = {k: norm(open(v[1], encoding='utf-8').read()) for k, v in INST.items()}

# ---- register, derived ----
cat = open(S + '/rhfac-b651-catalogue.md', encoding='utf-8').read()
s21 = cat.split('### 2.1')[1].split('### 2.2')[0]; s22 = cat.split('### 2.2')[1].split('### 2.4')[0]
C = [r.split('|')[2].strip() for r in s21.splitlines() if re.match(r'\|\s*\d+\s*\|', r)]
Q = [r.split('|')[1].strip() for r in s22.split('| Word | Sections |')[1].splitlines() if re.match(r'\|\s*[a-z]', r)]
B = [(r[0], r[1]) for r in csv.reader(open(S + '/b651-headings.tsv', encoding='utf-8'), delimiter='\t') if r and r[-1] == 'RHFAC-does-not-name']
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
P = con.execute("select p.parameter_id, t.canonical_en from base_parameters p join terms t using(term_id) where p.status='active' order by 1").fetchall()
REG = [(f'C{i+1:02d}', c, 'catalogue 2.1') for i, c in enumerate(C)] + [(f'Q-{w}', w, 'catalogue 2.2') for w in Q] \
    + [(f'P{p:02d}', n, 'base_parameters') for p, n in P] + [(f'B-{k}', h, 'B651 heading RHFAC does not name') for k, h in B]
IDS = {r[0] for r in REG}

# ---- observations: (concept ids '|'-separated, phrase verbatim, inst, locator, quote verbatim, note ours) ----
OBS = [
 ("C02|C14", "坚固、平整、防滑、不积水", "G", "2.1.4 (p.2)", "无障碍通行设施的地面应坚固、平整、防滑、不积水。", "one four-quality phrase for every accessible route surface; 'stable' has no separate word"),
 ("C11", "坚固、平整、防滑、不积水", "G", "3.1.5 (p.9)", "无障碍服务设施的地面应坚固、平整、防滑、不积水。", "same phrase repeated for service-facility floors"),
 ("C02|C11", "防滑性能", "G", "5.0.2 (p.17)", "应对无障碍设施的地面防滑性能、扶手和安全抓杆的受力性能进行验收", "slip resistance is checked at handover (验收), not specified as a value"),
 ("C03", "座椅", "G", "3.3.2(2) (p.12)", "乘轮椅者使用的座椅的高度应为400mm～450mm", "NARROWER: seat in an accessible changing room only; 座椅 in 2.1.2 is listed as an obstacle"),
 ("C03", "坐台", "G", "3.1.11(3) (p.10)", "淋浴间坐台应安装牢固", "shower seat"),
 ("C03", "优先坐席", "L", "art. 42", "设置无障碍服务窗口、专用等候区域、绿色通道和优先坐席", "priority seats in transport; a service duty, not a design rule"),
 ("C04", "扶手", "G", "2.8.1 (p.6)", "满足无障碍要求的单层扶手的高度应为850mm～900mm", ""),
 ("C04", "双层扶手", "G", "2.8.1 (p.6)", "设置双层扶手时，上层扶手高度应为850mm～900mm", "two-tier handrail is a named configuration"),
 ("C05|Q-width|Q-clearance", "通行净宽", "G", "2.2.2 (p.2)", "无障碍通道的通行净宽不应小于1.20m", "the code's one width word: clear passage width, used for routes, ramps, doors, gates, lifts"),
 ("C06", "无障碍通行流线", "G", "2.1.1 (p.2)", "城市开敞空间、建筑场地、建筑内部及其之间应提供连贯的无障碍通行流线。", "the route is a continuous 'flow line' across open space, site and building"),
 ("C06", "无障碍通道", "G", "2.2.2 (p.2)", "无障碍通道的通行净宽不应小于1.20m", "the route element; interior and exterior alike"),
 ("C07", "不积水", "G", "2.1.4 (p.2)", "无障碍通行设施的地面应坚固、平整、防滑、不积水。", "drainage expressed as an outcome (no ponding)"),
 ("C07|B-4.4.4", "雨水箅子", "G", "2.10.7 (p.7)", "缘石坡道上下坡处不应设置雨水箅子。", "drain grating; glyph 箅 read visually"),
 ("C08", "无障碍标识", "G", "4.0.1 (p.15)", "无障碍标识应纳入室内外环境的标识系统，应连续并清楚地指明无障碍设施的位置和方向。", ""),
 ("C08", "引导标识", "G", "2.9.4 (p.7)", "并应设置引导标识。", "guidance signage at accessible parking"),
 ("C08", "无障碍标志", "G", "4.0.2 (p.15)", "无障碍标志的安装位置和高度应保证从站立和座位的视觉角度都能够看见", "标志 (symbol) and 标识 (sign/signage) are both used"),
 ("C08", "引导标识系统", "L", "art. 12", "并纳入周边环境或者建筑物内部的引导标识系统", ""),
 ("C09|Q-volume", "音量放大和助听耦合", "G", "4.0.7(2) (p.15)", "应至少设1部电话具备免提对话、音量放大和助听耦合的功能", "PARTIAL: telephone volume amplification and hearing-aid coupling only; no room assistive-listening system"),
 ("C09", "文字信息的辅助服务", "G", "4.0.5 (p.15)", "以声音为主要传播手段的公共服务应提供文字信息的辅助服务", "text support where information is spoken"),
 ("C10", "休息平台", "G", "2.3.3 (p.3)", "轮椅坡道的起点、终点和休息平台的通行净宽不应小于坡道的通行净宽", "ramp landings: start, end and rest platform"),
 ("C10", "平台的净深度", "G", "2.4.2 (p.3)", "平台的净深度不应小于1.50m", "landing before an entrance door, measured with the door fully open"),
 ("C28", "每段坡道的提升高度", "G", "2.3.1(2) (p.3)", "每段坡道的提升高度不应大于750mm", "the interval between rest landings is fixed by rise per ramp run, not by run length"),
 ("C12", "净空间", "G", "3.1.11(2) (p.10)", "淋浴间前应设便于乘轮椅者通行和转动的净空间", "clear floor space in front of a fixture"),
 ("C12", "净空间", "G", "3.1.12(1) (p.11)", "浴盆侧面应设不小于1500mm×800mm的净空间", ""),
 ("C12|Q-clearance", "容膝容脚空间", "G", "3.1.10(1) (p.10)", "250mm的容膝容脚空间", "knee and toe space under a basin, counter or service desk"),
 ("C15", "雨篷", "G", "2.4.2 (p.3)", "无障碍出入口的上方应设置雨篷。", "NARROWER: canopy over an accessible entrance only"),
 ("C16|Q-riser", "踢面", "G", "2.7.1(3) (p.6)", "不应采用无踢面和直角形突缘的踏步", "PARTIAL: riser named as an element; no riser height or tread depth set"),
 ("C16|Q-tread", "踏面", "G", "2.7.1(4) (p.6)", "踏步防滑条、警示条等附着物均不应突出踏面。", "tread surface named; no tread depth set"),
 ("C17", "直角形突缘", "G", "2.7.1(3) (p.6)", "不应采用无踢面和直角形突缘的踏步", "nosing is 突缘; the rule bans the square (right-angle) nosing"),
 ("C18", "无踢面", "G", "2.7.1(3) (p.6)", "不应采用无踢面和直角形突缘的踏步", "open riser = 'step without a riser face', for steps used mainly by 视觉障碍者"),
 ("C19", "门槛", "G", "2.5.3 (p.4)", "满足无障碍要求的门不应设挡块和门槛，门口有高差时，高度不应大于15mm，并应以斜面过渡", "no noun for a level threshold: thresholds (门槛) and stops (挡块) are banned and any 高差 is bevelled (斜面过渡)"),
 ("C20|P11|B-4.5|B-4.5.1", "净高", "G", "2.2.5 (p.2)", "自动扶梯、楼梯的下部和其他室内外低矮空间可以进入时，应在净高不大于2.00m处采取安全阻挡措施。", "headroom appears as the height below which an enterable low space must be barred"),
 ("C21", "临空侧", "G", "2.3.5 (p.3)", "设置扶手的轮椅坡道的临空侧应采取安全阻挡措施。", "edge protection is a 'safety stopping measure' on the open (drop) side"),
 ("C21", "安全防护设施", "G", "2.1.3 (p.2)", "无障碍通行流线在临近地形险要地段处应设置安全防护设施，必要时应同时设置安全警示线。", "near dangerous terrain"),
 ("C22|C29", "踏步防滑条、警示条", "G", "2.7.1(4) (p.6)", "踏步防滑条、警示条等附着物均不应突出踏面。", "PARTIAL: slip-resistant and warning strips are named but no contrast is required of them; contrast is required of the first step (2.7.1(2))"),
 ("C22|C29", "颜色或材质", "G", "2.7.1(2) (p.6)", "上行和下行的第一阶踏步应在颜色或材质上与平台有明显区别", "contrast by colour OR material of the first step, not a nosing strip"),
 ("C23", "提示盲道", "G", "2.11.3 (p.8)", "需要安全警示和提示处应设置提示盲道", "warning tactile paving; paired with 行进盲道 (guidance)"),
 ("C24|Q-slope|Q-gradient|P03", "纵向坡度", "G", "2.3.1(1) (p.3)", "横向坡度不应大于1：50，纵向坡度不应大于1：12", "running slope; cross slope is 横向坡度"),
 ("C24|Q-slope", "横向坡度", "G", "2.3.1(1) (p.3)", "横向坡度不应大于1：50", ""),
 ("P03", "轮椅坡道", "G", "2.3.1 (p.3)", "轮椅坡道的坡度和坡段提升高度应符合下列规定", "the ramp is a 'wheelchair ramp'; the kerb ramp is a separate object (缘石坡道)"),
 ("C25", "杠杆式水龙头或感应式自动出水方式", "G", "3.1.10(3) (p.10)", "出水龙头应采用杠杆式水龙头或感应式自动出水方式。", "lever tap or sensor-operated automatic flow"),
 ("C26|C32", "开关和调控面板", "G", "3.1.6 (p.9)", "无障碍服务设施内供使用者操控的照明、设备、设施的开关和调控面板应易于识别，距地面高度应为0.85m～1.10m。", "PARTIAL for C26: switches and control panels; outlets (sockets) are not named"),
 ("C27", "电器", "G", "3.1.13(1) (p.11)", "厨房设施和电器应方便乘轮椅者靠近和使用", "BROADER: kitchen appliances in general; no microwave and no mounting height"),
 ("C30", "储物柜", "G", "3.3.2(1) (p.12)", "乘轮椅者使用的储物柜前应设直径不小于1.50m的轮椅回转空间", "locker, in an accessible changing room"),
 ("C31", "单手握拳操作", "G", "2.5.4(2) (p.4)", "平开门的门扇外侧和里侧均应设置扶手，扶手应保证单手握拳操作", "door hardware: the door handle is also called 扶手 here, operable with one closed fist"),
 ("C31", "闭门器", "G", "2.5.8 (p.4)", "满足无障碍要求的安装有闭门器的门，从闭门器最大受控角度到完全关闭前10°的闭门时间不应小于3s。", "door closer"),
 ("C31", "执手", "G", "3.4.7 (p.13)", "窗户可开启扇的执手或启闭开关距地面高度应为0.85m～1.00m", "window handle (执手) is distinct from the door 扶手"),
 ("C32", "呼叫按钮", "G", "2.6.1(2) (p.5)", "呼叫按钮的中心距地面高度应为0.85m～1.10m", "lift call button"),
 ("C32", "手动启闭装置", "G", "2.5.5(2) (p.4)", "当设置手动启闭装置时，可操作部件的中心距地面高度应为0.85m～1.00m。", "manual activation device of an automatic door"),
 ("Q-height", "距地面高度", "G", "3.1.6 (p.9)", "距地面高度应为0.85m～1.10m", "every mounting height is 'height above floor/ground'"),
 ("Q-height", "提升高度", "G", "2.3.1(2) (p.3)", "每段坡道的提升高度不应大于750mm", "rise of a ramp run"),
 ("Q-level", "地面高差", "G", "2.2.1 (p.2)", "无障碍通道上有地面高差时，应设置轮椅坡道或缘石坡道。", "level change = 高差 (height difference)"),
 ("Q-level", "平坡出入口", "G", "2.4.1(1) (p.3)", "地面坡度不大于1：20的平坡出入口", "level (gently sloped) entrance, defined by a slope bound"),
 ("Q-number", "总停车数", "G", "2.9.5 (p.7)", "总停车数在100辆以下时应至少设置1个无障碍机动车停车位", "counts set against a total"),
 ("Q-depth", "深度", "G", "2.6.2 (p.5)", "满足乘轮椅者使用的最小轿厢规格，深度不应小于1.40m", "lift-car depth"),
 ("Q-depth", "进深", "G", "3.1.10(1) (p.10)", "范围内进深不小于450mm", "depth of the knee space"),
 ("Q-force|P06", "门开启所需的力度", "G", "2.5.4(3) (p.4)", "除防火门外，门开启所需的力度不应大于25N。", "force word is 力度"),
 ("Q-force|P06", "操作所需的力度", "G", "3.4.7 (p.13)", "手动开关窗户操作所需的力度不应大于25N。", "window operating force"),
 ("Q-force", "受力性能", "G", "5.0.2 (p.17)", "扶手和安全抓杆的受力性能进行验收", "load-bearing performance of rails, checked at handover"),
 ("Q-time", "闭门时间", "G", "2.5.8 (p.4)", "从闭门器最大受控角度到完全关闭前10°的闭门时间不应小于3s", ""),
 ("Q-time", "完全开启时间", "G", "2.6.3(3) (p.5)", "完全开启时间应保持不小于3s。", "lift-door dwell time"),
 ("Q-size", "尺寸", "G", "3.2.2(1) (p.11)", "应方便乘轮椅者到达和进出，尺寸不应小于1.80m×1.50m", "size of an accessible toilet cubicle"),
 ("Q-size", "轿厢的规格", "G", "2.6.2 (p.5)", "无障碍电梯的轿厢的规格应依据建筑类型和使用要求选用。", "lift-car 'specification' (size class)"),
 ("Q-capacity", "容纳担架", "G", "2.6.2 (p.5)", "同时满足乘轮椅者使用和容纳担架的轿厢", "PARTIAL: lift capacity expressed as accommodating a stretcher, not a load or person count"),
 ("Q-distance", "距离", "G", "2.6.1(2) (p.5)", "且距内转角处侧墙距离不应小于400mm", "DIFFERENT SENSE: a setback distance, not RHFAC's distance markers"),
 ("Q-ratio", "1：1的陪护席位", "G", "3.5.4(3) (p.13)", "在轮椅席位旁或邻近的座席处应设置1：1的陪护席位", "PARTIAL: companion-seat ratio; RHFAC's ratio is a room-type mix"),
 ("Q-ratio", "不少于总停车数1%", "G", "2.9.5 (p.7)", "100辆以上时应设置不少于总停车数1%的无障碍机动车停车位", "proportional parking count"),
 ("P04", "无障碍通道的通行净宽", "G", "2.2.2 (p.2)", "无障碍通道的通行净宽不应小于1.20m，人员密集的公共场所的通行净宽不应小于1.80m。", "no 走廊 (corridor) in the code: interior and exterior routes are one object, with a crowd-density variant"),
 ("P05", "轮椅回转空间", "G", "2.6.1(1) (p.5)", "电梯门前应设直径不小于1.50m的轮椅回转空间", "turning space defined by a circle diameter"),
 ("P08", "颜色或亮度对比", "G", "2.8.5 (p.6)", "扶手应与背景有明显的颜色或亮度对比。", "BROADER: colour or brightness contrast, never quantified; no LRV"),
 ("P09", "门开启后的通行净宽", "G", "2.5.4(1) (p.4)", "新建和扩建建筑的门开启后的通行净宽不应小于900mm，既有建筑改造或改建的门开启后的通行净宽不应小于800mm", "door width is the clear width when open, split by new vs existing building"),
 ("P12", "坡段提升高度", "G", "2.3.1 (p.3)", "轮椅坡道的坡度和坡段提升高度应符合下列规定", "DIFFERENT AXIS: a ramp run is bounded by its rise, not by a run length"),
 ("B-4.5|B-4.5.2", "突出部分", "G", "2.1.2 (p.2)", "固定在无障碍通道、轮椅坡道、楼梯的墙或柱面上的物体，突出部分大于100mm且底面距地面高度小于2.00m时", "protruding objects on walls or columns"),
 ("B-4.4.4", "箅子", "G", "2.2.4 (p.2)", "无障碍通道上有井盖、箅子时，井盖、箅子孔洞的宽度或直径不应大于13mm，条状孔洞应垂直于通行方向。", "gratings and manhole covers; glyph 箅 read visually"),
 ("B-6.1.2", "饮水机", "G", "3.6.2 (p.14)", "当设置饮水机、自动取款机、自动售票机、自动贩卖机等时，每个区域的不同类型设施应至少有1台为低位服务设施。", "PARTIAL: drinking-water machine must have a low-level unit; no spout rule"),
 ("B-6.2.3", "无障碍洗手盆", "G", "3.1.10 (p.10)", "无障碍洗手盆应符合下列规定", "lavatory (wash basin)"),
 ("B-6.5.3", "活动门帘", "G", "3.3.1(3) (p.12)", "淋浴间入口应采用活动门帘。", "PARTIAL: shower enclosure entrance uses a movable curtain"),
 ("B-8.3.9", "阻车桩", "G", "2.10.7 (p.7)", "设置阻车桩时，阻车桩的净间距不应小于900mm。", "bollards at kerb ramps"),
 ("B-8.8.2", "临时占用", "L", "art. 28", "因特殊情况临时占用无障碍设施的，应当公告并设置护栏、警示标志或者信号设施，同时采取必要的替代性措施。", "PARTIAL: temporary occupation of facilities, with barriers and warnings; scaffolding not named"),
]
PARTIAL = {
 "C03": "NARROWER: changing-room seat, shower seat, transport priority seat; no rest seating on routes",
 "C09": "NARROWER: telephone amplification and hearing-aid coupling, text support; no room systems",
 "C15": "NARROWER: entrance canopy only",
 "C16": "PARTIAL: riser and tread named as elements; no riser height or tread depth",
 "C22": "PARTIAL: strips named; contrast attaches to the first step, not the strip",
 "C29": "PARTIAL: as C22",
 "C26": "PARTIAL: switches and control panels; outlets not named",
 "C27": "BROADER: kitchen appliances in general; no microwave, no mounting height",
 "Q-volume": "PARTIAL: telephone volume amplification, not PA volume",
 "Q-capacity": "PARTIAL: lift car accommodating a stretcher",
 "Q-distance": "DIFFERENT SENSE: setback distances; no distance markers",
 "Q-ratio": "PARTIAL: companion-seat and parking proportions; no room-type mix",
 "P08": "BROADER: colour or brightness contrast, never quantified",
 "P12": "DIFFERENT AXIS: run bounded by rise",
 "B-6.1.2": "PARTIAL: low-level drinking-water machine; no spout",
 "B-6.5.3": "PARTIAL: shower entrance curtain",
 "B-8.8.2": "PARTIAL: temporary occupation (law); scaffolding not named",
}
ABSENT = {
 "C01": "no illuminance or lighting requirement; 照明 occurs only as a thing whose switch is placed (3.1.6), 地灯 only as an obstacle (2.1.2)",
 "C13": "as C01",
 "Q-lighting levels": "as C01; 照度 0 in both texts",
 "P07": "混响 0, 吸声 0 in both texts; the only acoustic word is 噪声污染 for crossing signals (4.0.8(4))",
 "P10": "色温 0 in both texts",
 "B-8.3.8": "减速带 0; speed bumps not treated",
 "B-8.7": "no landscaping clause; the obstacle list of 2.1.2 names signs, bins, seats, lamp posts, bollard-like 隔离墩, ground lights and cable trays, not planting",
 "B-8.7.1": "花坛/种植 0",
 "B-8.7.3": "植物/绿化 0 (公共绿地 occurs only as a parking location, 2.9.5)",
 "B-8.7.4": "拉线 0",
 "B-D.6.1": "no trail or beach clauses; 级配 0",
}

# ---- reverse harvest: (phrase verbatim, kind ours, inst, locator, quote verbatim, gloss OURS) ----
REV = [
 ("无障碍通行设施", "defined category", "G", "1.0.3(4); ch. 2", "保障无障碍通行设施、无障碍服务设施和无障碍信息交流设施的安全、功能和性能", "ours: passage facilities; the code divides all provision into three facility classes"),
 ("无障碍服务设施", "defined category", "G", "1.0.3(4); ch. 3", "保障无障碍通行设施、无障碍服务设施和无障碍信息交流设施的安全、功能和性能", "ours: service facilities (toilets, baths, rooms, seating, counters)"),
 ("无障碍信息交流设施", "defined category", "G", "1.0.3(4); ch. 4", "保障无障碍通行设施、无障碍服务设施和无障碍信息交流设施的安全、功能和性能", "ours: information and communication facilities, a chapter of their own"),
 ("残疾人、老年人等有需求的人", "user category", "G", "1.0.3(1)", "满足残疾人、老年人等有需求的人使用", "ours: disabled people, older people and others with a need"),
 ("行动障碍者", "user category", "G", "2.1.2", "均不应妨碍行动障碍者的独立通行", "ours: people with mobility impairment"),
 ("视觉障碍者", "user category", "G", "2.7.1", "视觉障碍者主要使用的楼梯和台阶应符合下列规定", "ours: people with visual impairment; rules scoped to stairs 'mainly used' by them"),
 ("听觉障碍者、视觉障碍者和言语障碍者", "user category", "G", "3.4.8", "应同时满足听觉障碍者、视觉障碍者和言语障碍者使用", "ours: hearing, visual and speech impairment"),
 ("乘轮椅者", "user category", "G", "3.1.2", "应方便乘轮椅者进入和使用", "ours: wheelchair rider"),
 ("独立通行", "performance aim", "G", "2.1.2", "均不应妨碍行动障碍者的独立通行", "ours: independent passage"),
 ("系统性", "performance aim", "G", "1.0.3(3)", "保证系统性及无障碍设施之间有效衔接", "ours: systemic continuity between facilities; also checked at handover (5.0.1)"),
 ("安全警示线", "element", "G", "2.1.3", "必要时应同时设置安全警示线", "ours: safety warning line near hazardous terrain"),
 ("地形险要地段", "site condition", "G", "2.1.3", "无障碍通行流线在临近地形险要地段处应设置安全防护设施", "ours: dangerous terrain"),
 ("检票口、结算口", "element", "G", "2.2.3", "各类检票口、结算口等应设轮椅通道", "ours: ticket gates and checkouts"),
 ("轮椅通道", "element", "G", "2.2.3", "各类检票口、结算口等应设轮椅通道", "ours: wheelchair lane (also beside parking, 2.9.2)"),
 ("人员密集的公共场所", "context class", "G", "2.2.2", "人员密集的公共场所的通行净宽不应小于1.80m", "ours: crowded public places, which raise the route width"),
 ("安全阻挡措施", "technique", "G", "2.2.5", "应在净高不大于2.00m处采取安全阻挡措施", "ours: safety stopping measure; one phrase for barring low spaces and ramp drop edges"),
 ("坡段起止点的高差", "quantity", "G", "2.3.1(1)", "当条件受限且坡段起止点的高差不大于150mm时", "ours: rise between start and end of a ramp run, which unlocks a steeper slope"),
 ("条件受限", "compliance route", "G", "2.3.1(1)", "当条件受限且坡段起止点的高差不大于150mm时", "ours: 'where conditions are constrained', a relaxation trigger"),
 ("升降平台", "element", "G", "2.4.1(3); 2.6.5", "同时设置台阶和升降平台的出入口", "ours: platform lift as one of three accessible-entrance types"),
 ("出入口闸机", "element", "G", "2.4.3", "设置出入口闸机时", "ours: entrance turnstile or gate"),
 ("旋转门", "element", "G", "2.5.2", "在无障碍通道上不应使用旋转门。", "ours: revolving door, banned on accessible routes"),
 ("挡块", "element", "G", "2.5.3", "满足无障碍要求的门不应设挡块和门槛", "ours: door stop or sill block"),
 ("斜面过渡", "technique", "G", "2.5.3", "并应以斜面过渡", "ours: bevelled transition of a small level change"),
 ("全玻璃门", "element", "G", "2.5.6", "全玻璃门应符合下列规定", "ours: all-glass door"),
 ("防撞提示", "technique", "G", "2.5.6(3)", "防撞提示应横跨玻璃门或隔断", "ours: anti-collision marking on glazing"),
 ("净间距", "quantity", "G", "2.5.7", "两道门之间的距离除去门扇摆动的空间后的净间距不应小于1.50m", "ours: clear distance between doors in series"),
 ("观察窗", "element", "G", "2.5.9", "满足无障碍要求的双向开启的门应在可视高度部分安装观察窗", "ours: vision panel in a double-acting door"),
 ("候梯厅", "space", "G", "2.6.1", "无障碍电梯的候梯厅应符合下列规定", "ours: lift lobby"),
 ("盲文标志", "element", "G", "2.6.1(2)", "按钮应设置盲文标志", "ours: braille marking"),
 ("抵达音响", "element", "G", "2.6.1(4)", "应设置电梯运行显示装置和抵达音响", "ours: arrival chime"),
 ("宽轿厢", "element", "G", "2.6.2", "如采用宽轿厢", "ours: wide car; paired with 深轿厢 (deep car)"),
 ("深轿厢", "element", "G", "2.6.2", "如采用深轿厢", "ours: deep car"),
 ("水平滑动式门", "element", "G", "2.6.3(1)", "应为水平滑动式门", "ours: horizontal sliding door"),
 ("安全挡板", "element", "G", "2.6.5(1)", "应设扶手、安全挡板和呼叫控制按钮", "ours: safety guard plate of a platform lift"),
 ("防止误入", "technique", "G", "2.6.5(2)", "应采用防止误入的安全防护措施", "ours: preventing mistaken entry"),
 ("水平延伸", "technique", "G", "2.8.3", "扶手起点和终点处应水平延伸", "ours: horizontal extension of a handrail"),
 ("截面的内侧边缘与墙面的净距离", "quantity", "G", "2.8.4", "截面的内侧边缘与墙面的净距离不应小于40mm", "ours: handrail clearance from wall"),
 ("上/落客区", "space", "G", "2.9 heading", "无障碍机动车停车位和上/落客区", "ours: passenger loading zone"),
 ("轮椅通道线", "element", "G", "2.9.4", "应设置停车线、轮椅通道线和无障碍标志", "ours: wheelchair-aisle marking"),
 ("缘石坡道", "element", "G", "2.10.1", "有高差时应设置缘石坡道", "ours: kerb ramp, a separate object from the wheelchair ramp"),
 ("全宽式单面坡缘石坡道", "element", "G", "2.10.4(1)", "全宽式单面坡缘石坡道的坡度不应大于1：20", "ours: full-width single-slope kerb ramp"),
 ("三面坡缘石坡道", "element", "G", "2.10.5(2)", "三面坡缘石坡道的正面坡道宽度不应小于1.20m", "ours: three-sided kerb ramp"),
 ("坡口", "element", "G", "2.10.2", "缘石坡道的坡口与车行道之间应无高差。", "ours: the mouth of a kerb ramp at the carriageway"),
 ("过渡空间", "space", "G", "2.10.6", "缘石坡道顶端处应留有过渡空间", "ours: transition space at the top of a kerb ramp"),
 ("行进盲道", "element", "G", "2.11.3", "行进盲道的起点、终点、转弯处，应设置提示盲道", "ours: guidance tactile paving; 盲道 is the parent term"),
 ("救助呼叫装置", "element", "G", "3.1.4", "应设置易于识别和使用的救助呼叫装置", "ours: emergency assistance call device; must be usable by a person fallen to the floor (3.1.8(6))"),
 ("跌倒在地面的人", "user situation", "G", "3.1.8(6)", "并应满足坐在坐便器上和跌倒在地面的人均能够使用", "ours: a person who has fallen to the floor"),
 ("安全抓杆", "element", "G", "3.1.7(2)", "安全抓杆直径应为30mm～40mm", "ours: grab bar; distinct from 扶手"),
 ("L形安全抓杆", "element", "G", "3.1.8(3)", "无障碍坐便器另一侧设置的L形安全抓杆", "ours: L-shaped grab bar"),
 ("低位挂衣钩、低位毛巾架、低位搁物架", "element", "G", "3.1.7(3)", "低位挂衣钩、低位毛巾架、低位搁物架距地面高度不应大于1.20m", "ours: low-level hook, towel rail, shelf; 低位 'low-position' is a productive prefix"),
 ("坐便器水箱控制装置", "element", "G", "3.1.8(4)", "坐便器水箱控制装置应位于易于触及的位置，应可自动操作或单手操作", "ours: flush control"),
 ("取纸器", "element", "G", "3.1.8(5)", "取纸器应设在坐便器的侧前方", "ours: toilet-paper dispenser"),
 ("支撑安全抓杆", "element", "G", "3.1.9(2)", "应在小便器上部设置支撑安全抓杆", "ours: supporting grab bar above a urinal"),
 ("镜子反光面", "element", "G", "3.1.10(2)", "镜子反光面的底端距地面的高度不应大于1.00m", "ours: mirror reflecting surface"),
 ("手持的喷头", "element", "G", "3.1.11(5)", "应设置一个手持的喷头", "ours: hand-held shower head"),
 ("无障碍盆浴间", "space", "G", "3.1.12", "无障碍盆浴间应符合下列规定", "ours: accessible bath room"),
 ("无障碍厨房", "space", "G", "3.1.13", "无障碍厨房应符合下列规定", "ours: accessible kitchen"),
 ("无障碍厕位", "space", "G", "3.2.2", "无障碍厕位应符合下列规定", "ours: accessible cubicle inside a public toilet; distinct from 无障碍厕所 (a separate room)"),
 ("无障碍厕所", "space", "G", "3.2.3", "无障碍厕所应符合下列规定", "ours: stand-alone accessible toilet room"),
 ("多功能台", "element", "G", "3.2.3(2)", "内部应设置无障碍坐便器、无障碍洗手盆、多功能台", "ours: multi-purpose table (e.g. changing shelf)"),
 ("门外可紧急开启的门闩", "element", "G", "3.2.2(2)", "并应采用门外可紧急开启的门闩", "ours: latch openable from outside in an emergency"),
 ("无障碍客房", "space", "G", "3.4", "无障碍客房和无障碍住房、居室", "ours: accessible guest room"),
 ("无障碍住房、居室", "space", "G", "3.4", "无障碍客房和无障碍住房、居室", "ours: accessible dwelling and living room (residential)"),
 ("床侧通道", "space", "G", "3.4.6", "乘轮椅者上下床用的床侧通道宽度不应小于1.20m。", "ours: bedside transfer aisle"),
 ("门禁", "element", "G", "3.4.8", "无障碍住房的门禁和无障碍客房的门铃应同时满足听觉障碍者、视觉障碍者和言语障碍者使用。", "ours: door-entry system, usable by hearing, visual and speech impairment"),
 ("轮椅席位", "space", "G", "3.5", "轮椅席位的观看视线不应受到遮挡", "ours: wheelchair space in seating"),
 ("陪护席位", "space", "G", "3.5.4(3)", "应设置1：1的陪护席位", "ours: companion seat"),
 ("观看视线", "quantity", "G", "3.5.1", "轮椅席位的观看视线不应受到遮挡，并不应遮挡他人视线。", "ours: sightline"),
 ("低位服务设施", "defined category", "G", "3.6.1", "为公众提供服务的各类服务台均应设置低位服务设施", "ours: low-level service facility"),
 ("低位电话", "element", "G", "4.0.7(2)", "应至少设1部低位电话", "ours: low-level telephone"),
 ("听筒线", "element", "G", "4.0.7(2)", "听筒线长度不应小于600mm", "ours: handset cord"),
 ("个人自助终端", "element", "G", "4.0.7(3)", "应至少设1部低位个人自助终端", "ours: self-service kiosk"),
 ("读屏软件", "element", "G", "4.0.7(4)", "应至少提供1台具备读屏软件和支持屏幕放大功能的计算机", "ours: screen reader"),
 ("可替换键盘", "element", "G", "4.0.7(4)", "支持可替换键盘的计算机不应少于20%", "ours: replaceable keyboard"),
 ("过街音响提示装置", "element", "G", "4.0.8", "过街音响提示装置应符合下列规定", "ours: audible pedestrian signal"),
 ("视觉标识和听觉标识", "technique", "G", "4.0.4", "应同时提供包括视觉标识和听觉标识的警示标识", "ours: two-sense warning"),
 ("维护责任人", "role", "G", "5.0.3", "对竣工验收交付使用的无障碍设施应明确维护责任人。", "ours: person responsible for maintenance; maintenance is part of the code"),
 ("应急维护措施", "technique", "G", "5.0.6", "维护责任人应采取应急维护措施", "ours: emergency maintenance, e.g. slip resistance lost to rain or snow"),
 ("既有建筑改造或改建", "compliance route", "G", "2.5.4(1)", "既有建筑改造或改建的门开启后的通行净宽不应小于800mm", "ours: existing-building alteration carries its own lower value"),
 ("创新性的技术方法和措施", "compliance route", "G", "1.0.4", "创新性的技术方法和措施，应进行论证并符合本规范中有关性能的要求。", "ours: innovative methods allowed if demonstrated against performance requirements"),
 ("各级文物保护单位", "context class", "G", "1.0.3(6)", "各级文物保护单位根据需要在不破坏文物的前提下进行无障碍设施建设。", "ours: protected heritage sites"),
 ("全文强制性工程建设规范", "drafting form", "G", "前言 (p.4)", "逐步用全文强制性工程建设规范取代现行标准中分散的强制性条文", "ours: fully mandatory construction code replacing scattered mandatory clauses"),
 ("适老化改造", "technique", "L", "art. 4", "无障碍环境建设应当与适老化改造相结合", "ours: age-friendly retrofit, joined to barrier-free construction by statute"),
 ("同步规划、同步设计、同步施工、同步验收、同步交付使用", "process rule", "L", "art. 12", "无障碍设施应当与主体工程同步规划、同步设计、同步施工、同步验收、同步交付使用", "ours: the 'five synchronies' with the main works"),
 ("替代性措施", "compliance route", "L", "art. 18", "不具备无障碍设施改造条件的，责任人应当采取必要的替代性措施。", "ours: alternative measure where retrofit is not feasible"),
 ("家庭无障碍设施改造", "technique", "L", "art. 19", "县级以上人民政府应当支持、指导家庭无障碍设施改造。", "ours: home adaptation, subsidised"),
 ("加装电梯", "technique", "L", "art. 22", "国家支持城镇老旧小区既有多层住宅加装电梯或者其他无障碍设施", "ours: adding lifts to existing multi-storey housing"),
 ("人行天桥和人行地下通道", "element", "L", "art. 23", "大型居住区的人行天桥和人行地下通道", "ours: footbridges and pedestrian underpasses"),
 ("体验试用", "process rule", "L", "art. 17", "参加意见征询和体验试用等活动", "ours: trial use by disabled and older people's representatives during design and handover"),
 ("临时无障碍设施", "element", "L", "art. 27", "因特殊情况设置的临时无障碍设施，应当符合无障碍设施工程建设标准。", "ours: temporary accessible facility"),
 ("服务犬", "user situation", "L", "art. 46", "应当为残疾人携带导盲犬、导听犬、辅助犬等服务犬提供便利", "ours: service dogs, named by three kinds"),
 ("无障碍服务窗口", "element", "L", "art. 40", "应当设置低位服务台或者无障碍服务窗口", "ours: accessible service window"),
 ("语音、大字、闪光等提示装置", "element", "L", "art. 47", "视情况设置语音、大字、闪光等提示装置", "ours: voice, large-print and flashing alerts in emergency shelters"),
 ("通用设计理念", "doctrine", "L", "art. 51", "国家推广通用设计理念", "ours: the universal-design idea, promoted by statute"),
 ("认证", "compliance route", "L", "art. 53", "国家建立健全无障碍设计、设施、产品、服务的认证和无障碍信息的评测制度", "ours: certification of design, facilities, products, services"),
]

def main():
    bad = 0; rows = []
    for c, ph, ins, loc, q, note in OBS:
        for cid in c.split('|'):
            assert cid in IDS, cid
        ok = norm(q) in TXT[ins] and norm(ph) in norm(q)
        if not ok: bad += 1; print('FAIL', ins, loc, ph, file=sys.stderr)
        rows.append([c, ph, 'zh (Simplified, zh-Hans)', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok else 'NO', note])
    with open(D + '/observations.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept_ids (| = counts for each; labels in coverage.tsv)', 'phrase_verbatim', 'language (written form)', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'note (ours)'])
        w.writerows(rows)
    rb = 0
    with open(D + '/reverse-harvest.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['phrase_verbatim (instrument own phrase)', 'kind (ours)', 'language (written form)', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'gloss_OURS_not_an_equivalence'])
        for ph, kind, ins, loc, q, g in REV:
            ok = norm(q) in TXT[ins] and norm(ph) in norm(q)
            if not ok: rb += 1; print('REV FAIL', ins, loc, ph, file=sys.stderr)
            w.writerow([ph, kind, 'zh (Simplified, zh-Hans)', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok else 'NO', g])
    with open(D + '/coverage.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept_id', 'register_concept', 'register_source', 'status', 'n_observations', 'phrases_found (distinct)', 'note'])
        for cid, lab, src in REG:
            hit = [r for r in rows if cid in r[0].split('|')]
            if hit:
                st = 'FOUND-PARTIAL' if cid in PARTIAL else 'FOUND'
                notes = '; '.join(sorted({r[8] for r in hit if r[8]}))
                w.writerow([cid, lab, src, st, len(hit), ' / '.join(sorted({r[1] for r in hit})), (PARTIAL[cid] + '; ' if cid in PARTIAL else '') + notes])
            else:
                w.writerow([cid, lab, src, 'SEARCHED-ABSENT', 0, '', ABSENT.get(cid, 'NO NOTE: check')])
    stray = [k for k in list(PARTIAL) + list(ABSENT) if k not in IDS]
    if stray: bad += 1; print('STRAY KEYS', stray, file=sys.stderr)
    print('register', len(REG), 'observations', len(rows), 'reverse-harvest', len(REV), 'failures', bad + rb)
    sys.exit(1 if bad + rb else 0)

if __name__ == '__main__':
    main()
