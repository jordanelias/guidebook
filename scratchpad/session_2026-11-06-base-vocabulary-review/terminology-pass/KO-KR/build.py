"""Build observations / coverage / reverse-harvest / seeds TSVs for the KO/KR terminology pass and verify
every quote in the saved extracted text. Run from the repository root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/KO-KR/build.py
Verification: a quote passes only if it occurs in the saved text with ALL whitespace removed from both
(Korean PDF extraction breaks lines inside words, so a space-preserving match is impossible), and the
phrase occurs in its quote the same way. The PDF page is COMPUTED from the form feeds in the saved text,
never typed. Exits 1 on any failure. Reads the catalogue, b651-headings.tsv and the DB read-only; writes
only the TSVs in this folder."""
import re, sys, csv, sqlite3, hashlib
S = 'scratchpad/session_2026-11-06-base-vocabulary-review'
D = S + '/terminology-pass/KO-KR'
INST = {  # code: (title as written, issuing body, edition in force (from the bytes), URL, artefact, text file)
 'R1': ('장애인ㆍ노인ㆍ임산부 등의 편의증진 보장에 관한 법률 시행규칙 [별표 1] 편의시설의 구조·재질등에 관한 세부기준(제2조제1항관련)',
        '보건복지부 (보건복지부령); served by 법제처 국가법령정보센터',
        'annex stamp <개정 2023. 12. 11.>; linked unchanged from the Rule in force [시행 2026. 7. 2.] [보건복지부령 제1166호, 2026. 4. 1., 일부개정]',
        'https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162950009&bylClsCd=110201 (byte-identical to flSeq=162983711, REF-01031)',
        'b71c64f1a9b3125f.pdf', 'b71c64f1a9b3125f.txt'),
 'D2': ('장애인ㆍ노인ㆍ임산부 등의 편의증진 보장에 관한 법률 시행령 [별표 2] 대상시설별 편의시설의 종류 및 설치기준(제4조관련)',
        '대통령령; served by 법제처 국가법령정보센터',
        'annex stamp <개정 2024. 9. 19.>; linked from the Decree in force [시행 2026. 1. 2.] [대통령령 제35947호, 2025. 12. 30., 타법개정]',
        'https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=159615061&bylClsCd=110201', '7f0d40fff30743f5.pdf', '7f0d40fff30743f5.txt'),
 'D1': ('장애인·노인·임산부 등의 편의증진 보장에 관한 법률 시행령 [별표 1] 편의시설 설치 대상시설(제3조 관련)',
        '대통령령; served by 법제처 국가법령정보센터', 'annex stamp <개정 2024. 9. 19.>; Decree in force 2026-01-02',
        'https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=159615049&bylClsCd=110201', '418c8dbed012ef70.pdf', '418c8dbed012ef70.txt'),
 'R2': ('장애인ㆍ노인ㆍ임산부 등의 편의증진 보장에 관한 법률 시행규칙 [별표 2] 편의시설의 안내표시기준(제3조관련)',
        '보건복지부 (보건복지부령); served by 법제처 국가법령정보센터', 'annex stamp <개정 2023. 12. 11.>; Rule in force 2026-07-02',
        'https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162950097&bylClsCd=110201', '788c3fe703cb3d54.pdf', '788c3fe703cb3d54.txt'),
 'ACT': ('장애인ㆍ노인ㆍ임산부 등의 편의증진 보장에 관한 법률 ( 약칭: 장애인등편의법 )', '국회 (법률); served by 법제처 국가법령정보센터',
        '[시행 2025. 12. 21.] [법률 제20594호, 2024. 12. 20., 일부개정]',
        'https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=267429&chrClsCd=010202&urlMode=lsInfoP&efYd=20251221&ancYnChk=0', '8883966f2cba408a.html', '8883966f2cba408a.txt'),
 'DEC': ('장애인ㆍ노인ㆍ임산부 등의 편의증진 보장에 관한 법률 시행령 ( 약칭: 장애인등편의법 시행령 )', '대통령령; served by 법제처 국가법령정보센터',
        '[시행 2026. 1. 2.] [대통령령 제35947호, 2025. 12. 30., 타법개정]',
        'https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=281167&chrClsCd=010202&urlMode=lsInfoP&efYd=20260102&ancYnChk=0', '436707211a092d9d.html', '436707211a092d9d.txt'),
 'RUL': ('장애인ㆍ노인ㆍ임산부 등의 편의증진 보장에 관한 법률 시행규칙 ( 약칭: 장애인등편의법 시행규칙 )', '보건복지부 (보건복지부령); served by 법제처 국가법령정보센터',
        '[시행 2026. 7. 2.] [보건복지부령 제1166호, 2026. 4. 1., 일부개정]',
        'https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=285263&chrClsCd=010202&urlMode=lsInfoP&efYd=20260702&ancYnChk=0', '5c7c9db943614f9f.html', '5c7c9db943614f9f.txt'),
}
def strip(s): return re.sub(r'\s+', '', s)
RAW = {k: open(D + '/text/' + v[5], encoding='utf-8').read() for k, v in INST.items()}
TXT = {k: strip(v) for k, v in RAW.items()}
PAGES = {}
for k, v in RAW.items():  # cumulative stripped length at the end of each form-feed page (PDFs only)
    pp, acc = [], 0
    for pg in v.split('\f'):
        acc += len(strip(pg)); pp.append(acc)
    PAGES[k] = pp
def page(ins, q):
    i = TXT[ins].find(strip(q))
    if i < 0 or len(PAGES[ins]) < 2: return ''
    n = next(j for j, e in enumerate(PAGES[ins]) if i < e) + 1
    return f'; PDF p. {n} of {len([p for p in RAW[ins].split(chr(12)) if strip(p)])}'

# ---------------------------------------------------------------- register, derived (never retyped)
cat = open(S + '/rhfac-b651-catalogue.md', encoding='utf-8').read()
s21 = cat.split('### 2.1')[1].split('### 2.2')[0]; s22 = cat.split('### 2.2')[1].split('### 2.4')[0]
C21 = [r.split('|')[2].strip() for r in s21.splitlines() if re.match(r'\|\s*\d+\s*\|', r)]
C22 = [r.split('|')[1].strip() for r in s22.split('| Word | Sections |')[1].splitlines() if re.match(r'\|\s*[a-z]', r)]
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
PAR = [f'{n} (parameter {i})' for i, n in con.execute("select p.parameter_id, t.canonical_en from base_parameters p join terms t using(term_id) order by 1")]
B651 = [f'B651 {r[0]} {r[1]}' for r in csv.reader(open(S + '/b651-headings.tsv', encoding='utf-8'), delimiter='\t') if r and r[-1] == 'RHFAC-does-not-name']
REGISTER = [(c, 'catalogue 2.1') for c in C21] + [(c, 'catalogue 2.2') for c in C22] + [(c, 'base_parameters') for c in PAR] + [(c, 'b651-headings (RHFAC-does-not-name)') for c in B651]
LAB = {c for c, _ in REGISTER}

# ---------------------------------------------------------------- observations
# (concepts '|'-separated, phrase verbatim, instrument, locator (item numbering as printed), quote verbatim, note ours)
OBS = [
 ("Well-illuminated (if site expected to be lit)|Well illuminated (if required for expected usage)|lighting levels", "조도", "R1", "제9호 라목 (10)",
  "출입구, 승강대, 조작기의 조도는 저시력인 등 장애인의 안전을 위하여 최소 150LX 이상으로 하여야 한다.", "the only lighting rule in the annex: illuminance at a lift's entrance, car and controls, warranted by 저시력인 (people with low vision); no route or site lighting"),
 ("Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant", "잘 미끄러지지 아니하는 재질", "R1", "제1호 라목 (1)",
  "접근로의 바닥표면은 장애인등이 넘어지지 아니하도록 잘 미끄러지지 아니하는 재질로 평탄하게 마감하여야 한다.", "carve: slip resistance + 평탄 (level/even finish), with the aim 넘어지지 아니하도록 (so people do not fall); 'firm' and 'stable' have no counterpart"),
 ("Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant", "평탄하게 마감", "R1", "제12호 라목 (1)",
  "경사로의 바닥표면은 잘 미끄러지지 아니하는 재질로 평탄하게 마감하여야 한다.", "same formula on ramps"),
 ("Floor surface is stable, firm, and non-slip", "미끄러지지 아니하는 재질", "R1", "제7호 나목 (2)",
  "바닥표면은 미끄러지지 아니하는 재질로 평탄하게 마감하여야 하며, 넘어졌을 경우 가급적 충격이 적은 재료를 사용하여야 한다.", "corridor floor; adds an impact-absorbing material clause (see reverse harvest)"),
 ("Seating", "좌석", "R1", "제20호 나목 (1)",
  "휠체어사용자를 위한 관람석은 이동식 좌석 또는 접이식 좌석을 사용하여 마련하여야 한다.", "DIFFERENT SENSE: auditorium seats removable to make a wheelchair place, not rest seating"),
 ("Seating", "샤워용 접이식의자", "R1", "제15호 마목 (3)",
  "샤워실에는 아래의 그림과 같이 샤워용 접이식의자를 바닥면으로부터 0.4미터 이상 0.45미터 이하의 높이로 설치하여야 한다.", "NARROWER: shower seat"),
 ("Handrails", "손잡이", "R1", "제7호 다목 (2)",
  "손잡이의 높이는 아래의 그림과 같이 바닥면으로부터 0.8미터 이상 0.9미터 이하로 하여야 하며", "손잡이 is one word for handrail, grab bar and door handle; the sense is fixed only by its host element"),
 ("Handrails", "손잡이를 연속하여 설치", "R1", "제8호 라목 (1)",
  "계단의 양측면에는 손잡이를 연속하여 설치하여야 한다.", "stair handrails, both sides, continuous"),
 ("Clear width", "유효폭", "R1", "제1호 가목 (1)",
  "휠체어사용자가 통행할 수 있도록 접근로의 유효폭은 1.2미터 이상으로 하여야 한다.", "유효폭 (effective width) is the general clear-width term; doors use 통과유효폭"),
 ("Accessible path of travel", "장애인등의 통행이 가능한 접근로", "R1", "제1호 (heading)",
  "1. 장애인등의 통행이 가능한 접근로", "carve: 접근로 is the exterior route from the site edge to the main entrance; inside it becomes 복도 및 통로"),
 ("Accessible path of travel", "접근로", "D2", "제3호 가목 (1) (가)",
  "대상시설 외부에서 건축물의 주출입구에 이르는 접근로는", "the decree defines the route by its end points"),
 ("Clear signage", "안내표지", "R2", "제2호 가목",
  "안내표지의 색상은 청색과 백색을 사용하여야 한다.", "signage standard fixes colour (blue/white), not legibility"),
 ("Clear signage", "점자표지판", "R1", "제6호 다목 (2)",
  "건축물안의 공중의 이용을 주목적으로 하는 사무실 등의 출입문옆 벽면의 1.5미터 높이에는 방이름을 표기한 점자표지판을 부착하여야 한다.", "room-name braille plate"),
 ("Audio accessibility and communication enhancement technologies", "집단보청장치", "R1", "제20호 나목 (7)",
  "난청자를 위하여 자기(磁氣)루프, FM송수신장치 등 집단보청장치를 설치할 수 있다.", "assistive listening named as a class (집단보청장치) with 자기(磁氣)루프 and FM as members; recommended (할 수 있다)"),
 ("Audio accessibility and communication enhancement technologies|volume", "음량증폭전화기", "D2", "제6호 가목 (2)",
  "큰문자버튼전화기, 음량증폭전화기", "telephones for deaf and hard-of-hearing users; 'volume' only as telephone amplification"),
 ("Level landings with clear space|Level landings with clear space and at regular intervals", "수평면으로된 참", "R1", "제12호 가목 (2)",
  "바닥면으로부터 높이 0.75미터 이내마다 휴식을 할 수 있도록 수평면으로된 참을 설치하여야 한다.", "ramp landing interval set by RISE (높이), aim stated as rest (휴식)"),
 ("Level landings with clear space", "활동공간", "R1", "제12호 가목 (3)",
  "경사로의 시작과 끝, 굴절부분 및 참에는 1.5미터×1.5미터 이상의 활동공간을 확보하여야 한다.", "clear space at landings"),
 ("Level landings with clear space and at regular intervals", "수평면으로 된 참", "R1", "제1호 가목 (3)",
  "30미터마다 1.5미터×1.5미터 이상의 수평면으로 된 참을 설치할 수 있다.", "access-route rest landing by run (30 m); spelling differs from 제12호 (수평면으로 된 / 수평면으로된) inside one annex"),
 ("Clear space for approach", "휠체어를 탄 채 접근이 가능한 활동공간", "R1", "제21호 가목",
  "접수대 또는 작업대의 전면에는 휠체어를 탄 채 접근이 가능한 활동공간을 확보하여야 한다.", "unquantified approach space; 활동공간 is also the word for turning and side-transfer space"),
 ("Shelter", "지붕과 차양", "R1", "제12호 마목",
  "건물과 연결된 경사로를 외부에 설치하는 경우 햇볕, 눈, 비 등을 가릴 수 있도록 지붕과 차양을 설치할 수 있다.", "NARROWER: exterior ramps only, recommended"),
 ("Riser height and tread depth|riser|tread", "디딤판의 너비", "R1", "제8호 다목 (2)",
  "디딤판의 너비는 0.28미터 이상, 챌면의 높이는 0.18미터 이하로 하되", "tread is a WIDTH (너비), riser a HEIGHT; uniformity within a flight is required in the same clause"),
 ("Nosing design", "계단코", "R1", "제8호 다목 (3)",
  "계단코는 3센티미터 이상 돌출하여서는 아니된다.", "nosing projection limit"),
 ("Nosing design", "챌면의 기울기", "R1", "제8호 다목 (3)",
  "발끝이나 목발의 끝이 걸리지 아니하도록 챌면의 기울기는 디딤판의 수평면으로부터 60도 이상으로 하여야 하며", "riser angle, aim stated for toes and crutch tips"),
 ("No open riser|riser", "챌면을 반드시 설치", "R1", "제8호 다목 (1)",
  "계단에는 챌면을 반드시 설치하여야 한다.", "stated positively: risers must be installed"),
 ("Level threshold", "문턱", "R1", "제6호 가목 (4)",
  "출입구의 바닥면에는 문턱이나 높이차이를 두어서는 안 된다.", "no threshold or level difference; fire-door exception to 2 cm in the same clause"),
 ("Level threshold", "턱낮추기", "R1", "제5호 가목",
  "건축물의 주출입구와 통로의 높이차이는 2센티미터 이하가 되도록 설치하여야 한다.", "heading 턱낮추기 (lowering the step) carries the entrance rule"),
 ("Height clearance (if sheltered or parkade)|clearance|Headroom clearance (parameter 11)|B651 4.5.1 Headroom", "유효높이", "R1", "제7호 라목 (3)",
  "통로상부는 바닥면으로부터 2.1미터 이상의 유효높이를 확보해야 한다.", "headroom over routes; no parking-garage headroom rule in the texts read"),
 ("Edge protection", "추락방지턱", "R1", "제12호 라목 (2)",
  "휠체어의 바퀴가 경사로 밖으로 미끄러져 나가지 아니하도록 5센티미터 이상의 추락방지턱 또는 측벽을 설치할 수 있다.", "ramp edge upstand, recommended; also at stairs (제8호 바목)"),
 ("Edge protection", "추락방지설비", "D2", "제3호 가목 (12) (나)",
  "장애인등이 추락할 우려가 있는 경우에는 난간 등 추락방", "decree level: fall-prevention equipment; the quote stops where the table cell breaks (지설비를 갖추어야 한다 follows after the column label)"),
 ("Colour-contrasted and slip-resistant strip on nosing|Colour-contrasted and slip-resistant strip", "미끄럼방지재", "R1", "제8호 마목 (2)",
  "계단코에는 줄눈넣기를 하거나 경질고무류 등의 미끄럼방지재로 마감하여야 한다.", "slip half: grooving or hard rubber at the nosing"),
 ("Colour-contrasted and slip-resistant strip on nosing|Colour-contrasted and slip-resistant strip|LRV contrast (parameter 8)", "계단코의 색상", "R1", "제8호 바목 (2)",
  "계단코의 색상은 계단의 바닥재색상과 달리 할 수 있다.", "colour half: 'different colour', recommended; no luminance quantity"),
 ("Tactile attention indicators (truncated domes)", "감지용점형블록", "R1", "제16호 가목 (1)",
  "점자블록은 아래의 그림과 같은 감지용점형블록과 유도용 선형블록을 사용하여야 한다.", "defined pair: warning (점형) and guidance (선형); umbrella 점자블록"),
 ("Tactile attention indicators (truncated domes)", "원뿔절단형", "R1", "제16호 가목 (4)",
  "점형블록의 돌출점은 반구형·원뿔절단형 또는 이 두가지의 혼합배열형으로 하며", "truncated cone is one of three permitted dot shapes"),
 ("Slope|slope|gradient", "기울기", "R1", "제1호 나목 (1)",
  "접근로의 기울기는 18분의 1이하로 하여야 한다.", "gradient written as a fraction 'N분의 1'; 기울기 serves slope and gradient alike"),
 ("Sink faucet is easy to use or automatic", "수도꼭지", "R1", "제13호 가목 (3) (다)",
  "세정장치·수도꼭지 등은 광감지식·누름버튼식·레버식 등 사용하기 쉬운 형태로 설치하여야 한다.", "operation types named: sensor, push button, lever"),
 ("Outlets and switches are at accessible heights", "콘센트·스위치", "R1", "제19호 라목 (3)",
  "콘센트·스위치·수납선반·옷걸이 등의 높이는 바닥면으로부터 0.8미터 이상 1.2미터 이하로 설치하여야 한다.", "guest rooms and bedrooms (객실등) only"),
 ("Accessible lockers", "수납공간", "R1", "제15호 마목 (4)",
  "탈의실의 수납공간의 높이는 휠체어사용자가 이용할 수 있도록 바닥면으로부터 0.4미터 이상 1.2미터 이하로 설치하여야 하며", "NARROWER: changing-room storage, no locker noun"),
 ("Accessible door hardware", "레버형", "R1", "제6호 다목 (1)",
  "출입문의 손잡이는 중앙지점이 바닥면으로부터 0.8미터와 0.9미터사이에 위치하도록 설치하여야 하며, 그 형태는 레버형이나 수평 또는 수직막대형으로 할 수 있다.", "handle height mandatory; lever or bar form recommended"),
 ("Accessible controls", "이용자 조작설비", "R1", "제9호 다목 (heading)",
  "다. 이용자 조작설비", "heading also used for telephones (제28호 다목)"),
 ("Accessible controls|height", "조작반", "R1", "제9호 다목 (1)",
  "호출버튼·조작반·통화장치 등 승강기의 안팎에 설치되는 모든 스위치의 높이는 바닥면으로부터 0.8미터 이상 1.2미터 이하로 설치하여야 한다.", "lift controls"),
 # quantity-bearing words (catalogue 2.2)
 ("height", "높이", "R1", "제7호 다목 (2)", "손잡이의 높이는 아래의 그림과 같이 바닥면으로부터 0.8미터 이상 0.9미터 이하로 하여야 하며", "높이 measured 바닥면으로부터 (from the floor surface) throughout"),
 ("level", "높이차이", "R1", "제5호 가목", "건축물의 주출입구와 통로의 높이차이는 2센티미터 이하가 되도록 설치하여야 한다.", "'level' is split: 높이차이 (level difference), 단차 (step), 수평면 (horizontal), 층 (storey)"),
 ("level", "단차", "R1", "제1호 나목 (2)", "대지 내를 연결하는 주접근로에 단차가 있을 경우 그 높이 차이는 2센티미터 이하로 하여야 한다.", "단차 and 높이 차이 in one sentence; spacing 높이 차이 / 높이차이 varies"),
 ("level", "층수", "R1", "제8호 라목 (3)", "손잡이의 양끝부분 및 굴절부분에는 층수·위치 등을 나타내는 점자표지판을 부착하여야 한다.", "storey sense"),
 ("width|depth", "깊이", "R1", "제9호 나목 (1)", "승강기내부의 유효바닥면적은 폭 1.1미터 이상, 깊이 1.35미터 이상으로 하여야 한다.", "lift car as 유효바닥면적 (effective floor area) by 폭 × 깊이"),
 ("clearance", "틈", "R1", "제9호 가목 (3)", "승강장바닥과 승강기바닥의 틈은 3센티미터 이하로 하여야 한다.", "gap sense"),
 ("clearance", "무릎 및 휠체어의 발판이 들어갈 수 있도록", "R1", "제20호 다목 (2)", "열람석의 하부에는 무릎 및 휠체어의 발판이 들어갈 수 있도록 바닥면으로부터 높이 0.65미터 이상, 깊이 0.45미터 이상의 공간을 확보하여야 한다.", "knee clearance described by what enters (knees and footplates), no 'clearance' noun"),
 ("number|ratio", "1퍼센트 이상", "D2", "제3호 가목 (13)", "기숙사 및 숙박시설등의 전체 침실수 또는 객실의 1퍼센트 이", "proportional count of accessible rooms; quote ends at the cell break"),
 ("number", "36개의 돌출점", "R1", "제16호 가목 (3)", "점형블록은 블록당 36개의 돌출점을 가진 것을 표준형으로 한다.", "count of dots"),
 ("time", "닫히는 시간", "R1", "제6호 나목 (3)", "여닫이문에 도어체크를 설치하는 경우에는 문이 닫히는 시간이 3초 이상 충분하게 확보되도록 하여야 한다.", "closing time of a door closer"),
 ("time", "개방시간", "R1", "제6호 나목 (4)", "자동문은 휠체어사용자의 통행을 고려하여 문의 개방시간이 충분하게 확보되도록 설치하여야 하며", "automatic door open time, unquantified"),
 ("size", "크기", "R1", "제16호 가목 (2)", "점자블록의 크기는 0.3미터×0.3미터인 것을 표준형으로 하며", "tile size; also parking-space size (제4호 나목)"),
 ("distance", "앞 좌석과의 거리", "R1", "제20호 나목 (4)", "앞 좌석과의 거리는 일반 좌석의 1.5배 이상으로 하여", "DIFFERENT SENSE: seat spacing, not distance markers"),
 ("ratio", "설치비율", "D2", "제3호 가목 (2) (가)", "는 설치비율에 따라 장애인의 이용이 편리한 위치에 구분·", "parking ratio deferred to 주차장법령"),
 # base parameters
 ("ramp gradient (parameter 3)", "경사로의 기울기", "R1", "제12호 나목 (1)", "경사로의 기울기는 12분의 1 이하로 하여야 한다.", "relaxation to 8분의 1 under three cumulative conditions in 나목 (2)"),
 ("corridor width (parameter 4)", "복도의 유효폭", "R1", "제7호 가목", "복도의 유효폭은 1.2미터 이상으로 하되, 복도의 양옆에 거실이 있는 경우에는 1.5미터 이상으로 할 수 있다.", "corridor and passage are one object: 복도 및 통로"),
 ("turning circle (parameter 5)", "휠체어가 회전할 수 있도록", "R1", "제13호 나목 (1) (가)", "이 경우 대변기의 전면에는 휠체어가 회전할 수 있도록 1.4미터×1.4미터 이상의 활동공간을 확보하여야 한다.", "turning space is a SQUARE 활동공간, never a circle or diameter"),
 ("turning circle (parameter 5)", "휠체어가 회전할 수 있는 공간", "R1", "제19호 나목 (2)", "객실등의 내부에는 휠체어가 회전할 수 있는 공간을 확보하여야 한다.", "unquantified in guest rooms"),
 ("turning circle (parameter 5)", "180도 회전", "R1", "제9호 라목 (2)", "승강기 내부의 후면에는 내부에서 휠체어가 180도 회전이 불가능할 경우", "turn named by angle; a mirror substitutes when it is impossible"),
 ("door width (parameter 9)", "통과유효폭", "R1", "제6호 가목 (1)", "출입구(문)은 아래의 그림과 같이 그 통과유효폭을 0.9미터 이상으로", "passage clear width; the clause pairs it with 전면 유효거리 (approach depth)"),
 ("LRV contrast (parameter 8)", "바닥재의 색상", "R1", "제16호 가목 (7)", "점자블록의 색상은 원칙적으로 황색으로 사용하되, 바닥재의 색상과 비슷하여 구별하기 어려운 경우에는 다른 색상으로 할 수 있다.", "BROADER: contrast is 'colour different from the floor'; yellow by default"),
 ("ramp run length (parameter 12)", "경사로의 길이", "R1", "제12호 다목 (1)", "경사로의 길이가 1.8미터 이상이거나 높이가 0.15미터 이상인 경우에는 양측면에 손잡이를 연속하여 설치하여야 한다.", "length appears only as a handrail trigger; landings are set by rise (제12호 가목 (2))"),
 # B651 headings RHFAC does not name
 ("B651 4.4.4 Gratings", "격자구멍", "R1", "제1호 라목 (3)", "덮개에 격자구멍 또는 틈새가 있는 경우에는 그 간격이 2센티미터 이하가 되도록 하여야 한다.", "covers over hazards with grid holes or slots"),
 ("B651 4.5 Headroom and protruding objects", "보행장애물", "R1", "제7호 라목 (heading)", "라. 보행장애물", "one heading 보행장애물 (walking obstacles) holds protrusion and headroom; also 제1호 마목"),
 ("B651 4.5.2 Protruding objects", "돌출폭", "R1", "제7호 라목 (1)", "통로의 바닥면으로부터 높이 0.6미터에서 2.1미터 이내의 벽면으로부터 돌출된 물체의 돌출폭은 0.1미터 이하로 할 수 있다.", "recommended (할 수 있다)"),
 ("B651 6.1.2 Spouts", "분출구", "R1", "제22호 나목 (3)", "음료대의 분출구의 높이는 0.7미터 이상 0.8미터 이하로 하여야 한다.", "drinking fountain spout"),
 ("B651 6.2.3 Lavatories", "휠체어사용자용 세면대", "R1", "제13호 라목 (1) (가)", "휠체어사용자용 세면대의 상단높이는 바닥면으로부터 0.85미터 이하, 하단 높이는 0.65미터 이상으로 하여야 한다.", ""),
 ("B651 6.5.3 Enclosures", "샤워부스", "R1", "제15호 나목 (2)", "샤워실(샤워부스를 포함한다)의 유효바닥면적은 0.9미터×0.9미터 또는", "PARTIAL: shower room includes the booth; no enclosure rule as such"),
 ("B651 8.7.3 Vegetation", "가로수", "R1", "제1호 마목 (2)", "가로수는 지면에서 2.1미터까지 가지치기를 하여야 한다.", "NARROWER: street-tree pruning height"),
]

PARTIAL = {
 "Well-illuminated (if site expected to be lit)": "NARROWER: lift illuminance only; no site or route lighting",
 "Well illuminated (if required for expected usage)": "NARROWER: lift illuminance only",
 "Seating": "DIFFERENT SENSE / NARROWER: auditorium seats and shower seat; no rest seating",
 "Shelter": "NARROWER: roof and canopy over exterior ramps, recommended",
 "Height clearance (if sheltered or parkade)": "NARROWER: route headroom only; no parking headroom",
 "Accessible lockers": "NARROWER: changing-room storage space",
 "Outlets and switches are at accessible heights": "NARROWER: guest rooms only",
 "volume": "PARTIAL: telephone amplification only",
 "distance": "DIFFERENT SENSE: seat spacing",
 "ratio": "PARTIAL: parking ratio by reference, room percentage",
 "LRV contrast (parameter 8)": "BROADER: colour difference, never quantified",
 "turning circle (parameter 5)": "CARVE: square space or unquantified, never a circle",
 "ramp run length (parameter 12)": "PARTIAL: length only as handrail trigger; landings by rise",
 "B651 6.5.3 Enclosures": "PARTIAL: shower booth as part of the shower room",
 "B651 8.7.3 Vegetation": "NARROWER: street trees only",
 "B651 4.5 Headroom and protruding objects": "MERGED under 보행장애물",
}
ABSENT = {
 "Drainage": "배수 0 in all seven texts; shower floor 기울기 30분의 1 implies fall but names no drainage; 덮개 covers hazards, not drains",
 "Microwave mounting height accessible and safe": "전자레인지 0; no kitchen-appliance rule",
 "force": "힘 occurs only inside 닫힘 (a UI label); 조작력, 뉴턴 0; nearest is '미닫이문은 가벼운 재질로' (light material), no force",
 "capacity": "용량, 정원 0; the lift car is set by 유효바닥면적, not rated load or persons",
 "operating force (parameter 6)": "no force quantity anywhere; door closer by closing time (3초) instead",
 "reverberation time (parameter 7)": "잔향, 반향, 흡음 0; the only acoustic quantity is ambient noise 주변소음도 75데시벨 for telephones",
 "colour temperature (parameter 10)": "색온도, 켈빈 0; lighting only as 조도 at lifts",
 "B651 8.3.8 Speed bumps": "과속방지턱 0",
 "B651 8.3.9 Bollards": "볼라드 0; nearest is 연석·울타리 separating route from roadway (제1호 다목)",
 "B651 8.7 Landscaping elements": "no landscaping heading; 가로수 pruning only (counted under 8.7.3)",
 "B651 8.7.1 Flower or shrub planters": "화분, 식재 0",
 "B651 8.7.4 Guy wires": "지선 0; nearest is 가로등·전주·간판 as obstacles (제1호 마목 (1))",
 "B651 8.8.2 Scaffolding": "비계 occurs only inside 정비계획 (Act); no temporary-works rule",
 "B651 D.6.1 Gradation limits": "no trail or aggregate rule",
}

# ---------------------------------------------------------------- reverse harvest
# (phrase verbatim, kind (ours), instrument, locator, quote verbatim, gloss OURS)
REV = [
 ("장애인등", "defined user class", "ACT", "제2조 제1호", "“장애인등”이란 장애인ㆍ노인ㆍ임산부 등 일상생활에서 이동, 시설 이용 및 정보 접근 등에 불편을 느끼는 사람을 말한다.", "one statutory class: disabled people, older people, pregnant women and others who experience inconvenience"),
 ("편의시설", "defined object", "ACT", "제2조 제2호", "“편의시설”이란 장애인등이 일상생활에서 이동하거나 시설을 이용할 때 편리하게 하고, 정보에 쉽게 접근할 수 있도록 하기 위한 시설과 설비를 말한다.", "'convenience facility': the unit the law regulates"),
 ("대상시설", "defined scope", "ACT", "제7조", "편의시설을 설치하여야 하는 대상(이하 “대상시설”이라 한다)", "target facilities"),
 ("시설주", "defined duty-holder", "ACT", "제2조 제3호", "“시설주”(施設主)란 제7조 에 따른 대상시설의 소유자 또는 관리자", "facility owner or manager"),
 ("공공건물 및 공중이용시설", "defined building class", "ACT", "제2조 제6호", "“공공건물 및 공중이용시설”이란 불특정다수가 이용하는 건축물, 시설 및 그 부대시설로서", "public buildings and facilities used by the public"),
 ("최단거리", "design principle", "ACT", "제3조", "가능하면 최대한 편리한 방법으로 최단거리로 이동할 수 있도록 편의시설을 설치하여야 한다.", "shortest-route principle"),
 ("접근권", "right", "ACT", "제4조", "제4조(접근권)", "right of access"),
 ("적용의 완화", "compliance route (relaxation)", "ACT", "제15조", "세부기준을 완화한 별도의 기준을 정하고 시설주관기관의 승인을 받아", "approved relaxed standard"),
 ("세부기준보다 안전하고 편리한 대안", "compliance route (equivalent or better)", "DEC", "제7조 제1항 제2호", "과학기술의 발전 등에 따라 세부기준보다 안전하고 편리한 대안을 제시하는 경우", "an alternative safer and more convenient than the detailed standard"),
 ("장애물 없는 생활환경 인증", "certification scheme", "ACT", "제10조의2", "장애물 없는 생활환경 인증(이하 “인증”이라 한다)", "barrier-free living environment certification"),
 ("편의시설 상세표준도", "standard detail drawings", "ACT", "제14조 제2항", "편의시설 상세표준도(詳細標準圖)를 작성하여 보급하여야 한다.", "ministry standard detail drawings"),
 ("전동보장구충전시설", "provided equipment", "ACT", "제16조 제1항", "전동보장구충전시설(전동휠체어 등 전기를 동력원으로 사용하는 보장구를 충전할 수 있는 시설을 의미한다. 이하 같다)", "power-wheelchair charging facility"),
 ("장애인용 쇼핑카트", "provided equipment", "ACT", "제16조 제1항", "휠체어, 점자(點字) 안내책자, 보청기기, 장애인용 쇼핑카트", "equipment the owner must keep"),
 ("한국수어 통역", "service", "ACT", "제16조의2", "안내 서비스, 한국수어 통역 등의 편의 제공을 요청할 수 있다.", "Korean Sign Language interpretation on request"),
 ("시험적용", "compliance route (trial)", "RUL", "제2조 제2항", "일정기간 동안 시험적용을 할 필요가 있거나", "trial application of new products"),
 ("규제의 재검토", "review cycle", "RUL", "제8조", "매 2년이 되는 시점", "two-yearly review of the detailed standards"),
 ("권장사항", "drafting convention", "R1", "비고", "있다\"로 규정된 사항은 장애인 등의 이용편의를 위한 권장사항임", "every 'may' (할 수 있다) item is a recommendation"),
 ("의무", "drafting convention (matrix cell)", "D2", "제3호 나목 (table)", "의 권 의 의 권 권 권 권 권", "matrix cells 의무 / 권장 split vertically into 의/무 and 권/장 by the table layout"),
 ("매개시설", "facility category", "D2", "제3호 나목 (table header)", "매개시설 내부시설", "categories: connecting, interior, sanitary, information, other facilities"),
 ("위생시설", "facility category", "D2", "제3호 나목 (table header)", "위생시설", "sanitary facilities"),
 ("안내시설", "facility category", "D2", "제3호 나목 (table header)", "안내시설", "information facilities"),
 ("바닥면적의 합계", "applicability threshold", "D1", "제2호 가목 (1)", "용도에 쓰이는 바닥면적의 합계가 50제곱미터 이상 1천제곱미터 미만인 시설", "duty triggered by building use and floor area"),
 ("교행구역", "element", "R1", "제1호 가목 (2)", "50미터마다 1.5미터×1.5미터 이상의 교행구역을 설치할 수 있다.", "passing zone"),
 ("주접근로", "element", "R1", "제1호 나목 (2)", "대지 내를 연결하는 주접근로에 단차가 있을 경우", "main access route"),
 ("연석", "element", "R1", "제1호 다목 (2)", "연석의 높이는 6센티미터 이상 15센티미터 이하로 할 수 있으며", "kerb"),
 ("바닥재의 질감을 달리", "technique (tactile substitute)", "R1", "제1호 다목 (1)", "시각장애인이 감지할 수 있도록 바닥재의 질감을 달리하여야 한다.", "texture change as an alternative to a physical separator or tactile tile"),
 ("덮개", "element", "R1", "제1호 라목 (3)", "장애인등이 빠질 위험이 있는 곳에는 덮개를 설치하되", "cover over openings"),
 ("장애인전용주차구역", "element", "R1", "제4호 (heading)", "4. 장애인전용주차구역", "parking reserved for disabled people"),
 ("평행주차형식", "element variant", "R1", "제4호 나목 (1)", "평행주차형식인 경우에는 주차대수 1대에 대하여 폭 2미터 이상, 길이 6미터 이상으로", "parallel parking layout"),
 ("승하차", "activity", "R1", "제4호 나목 (2)", "장애인등의 승하차에 지장을 주는 높이차이가 없어야 하며", "getting in and out of a vehicle"),
 ("장애인전용표시", "marking", "R1", "제4호 다목 (1)", "운전자가 식별하기 쉬운 색상으로 아래의 그림과 같이 장애인전용표시를 하여야 한다.", "reserved-space marking"),
 ("높이차이가 제거된 건축물 출입구", "element (heading)", "R1", "제5호 (heading)", "5. 높이차이가 제거된 건축물 출입구", "entrance with the level difference removed"),
 ("전면 유효거리", "quantity", "R1", "제6호 가목 (1)", "출입구(문)의 전면 유효거리는 1.2미터 이상으로 하며", "effective clear distance in front of a door"),
 ("문의 개폐에 소요되는 공간", "quantity rule", "R1", "제6호 가목 (1)", "연속된 출입문의 경우 문의 개폐에 소요되는 공간은 유효거리에 포함하지 아니한다.", "door swing excluded from the clear distance between doors in series"),
 ("경기용 휠체어 사용자", "user group", "R1", "제6호 가목 (2)", "경기용 휠체어 사용자를 위한 출입구(문)의 통과유효폭은 1.2미터 이상으로 해야 한다.", "sports-wheelchair users in sports facilities"),
 ("회전문", "excluded element", "R1", "제6호 나목 (1)", "출입문은 회전문을 제외한 다른 형태의 문을 설치하여야 한다.", "revolving doors excluded"),
 ("도어체크", "element", "R1", "제6호 나목 (3)", "여닫이문에 도어체크를 설치하는 경우에는", "door closer (loan word)"),
 ("감지범위", "quantity (unquantified)", "R1", "제6호 나목 (4)", "개폐기의 작동장치는 가급적 감지범위를 넓게 하여야 한다.", "automatic door sensing range"),
 ("턱이 있는 문지방", "excluded element", "R1", "제6호 나목 (2)", "턱이 있는 문지방이나 홈을 설치하여서는 아니된다.", "raised sill or groove on sliding doors"),
 ("호출할 수 있는 벨", "element", "R1", "제6호 라목 (2)", "시설관리자 등을 호출할 수 있는 벨을 자동문옆에 설치할 수 있다.", "call bell for staff"),
 ("점형블록", "element", "R1", "제6호 라목 (1)", "건축물 주출입구의 0.3미터 전면에는 문의 폭만큼 점형블록을 설치하거나", "warning tiles 0.3 m before an entrance"),
 ("킥플레이트", "element", "R1", "제7호 마목 (1)", "복도의 벽면에는 바닥면으로부터 0.15미터에서 0.35미터까지 킥플레이트를 설치할 수 있다.", "kick plate on corridor walls"),
 ("모서리 부분은 둥글게 마감", "technique", "R1", "제7호 마목 (2)", "복도의 모서리 부분은 둥글게 마감할 수 있다.", "rounded corners"),
 ("충격이 적은 재료", "material property", "R1", "제7호 나목 (2)", "넘어졌을 경우 가급적 충격이 적은 재료를 사용하여야 한다.", "low-impact flooring for falls"),
 ("접근방지용난간", "element", "R1", "제7호 라목 (3)", "높이 0.6미터 이하에 접근방지용난간 또는 보호벽을 설치해야 한다.", "cane-detectable barrier under low obstacles"),
 ("손잡이의 지름", "quantity", "R1", "제7호 다목 (3)", "손잡이의 지름은 아래의 그림과 같이 3.2센티미터 이상 3.8센티미터 이하로 해야 한다.", "handrail diameter, with an oval variant by perimeter"),
 ("벽과 손잡이의 간격", "quantity", "R1", "제7호 다목 (4)", "벽과 손잡이의 간격은 5센티미터 내외로", "handrail-to-wall gap"),
 ("거실", "context term", "R1", "제7호 가목", "복도의 양옆에 거실이 있는 경우에는 1.5미터 이상으로 할 수 있다.", "habitable rooms on both sides"),
 ("직선 또는 꺾임형태", "stair form", "R1", "제8호 가목 (1)", "계단은 직선 또는 꺾임형태로 설치할 수 있다.", "straight or dog-leg stairs"),
 ("옥외 피난계단", "element variant", "R1", "제8호 나목", "건축물의 옥외 피난계단은 0.9미터 이상으로 할 수 있다.", "external escape stair"),
 ("수평손잡이", "element", "R1", "제8호 라목 (2)", "경사면에 설치된 손잡이의 끝부분에는 0.3미터 이상의 수평손잡이를 설치하여야 한다.", "horizontal handrail extension; same word is a horizontal grab bar in toilets"),
 ("줄눈넣기", "technique", "R1", "제8호 마목 (2)", "계단코에는 줄눈넣기를 하거나", "grooving the nosing"),
 ("유효바닥면적", "quantity", "R1", "제9호 나목 (1)", "승강기내부의 유효바닥면적은 폭 1.1미터 이상", "effective floor area (lift, toilet, shower, seat space)"),
 ("신축하는 건물", "applicability split", "R1", "제9호 나목 (1)", "다만, 신축하는 건물의 경우에는 폭을 1.6미터 이상으로", "new-build versus existing (기존시설) values"),
 ("거울", "element", "R1", "제9호 라목 (2)", "승강기 후면의 0.6미터 이상의 높이에 견고한 재질의 거울을 설치하여야 한다.", "mirror for reversing out of a lift"),
 ("음향신호장치", "element", "R1", "제9호 라목 (3)", "승강기의 도착여부를 표시하는 점멸등 및 음향신호장치를 설치하여야 하며", "flashing light and audible signal on arrival"),
 ("광감지식개폐장치", "element", "R1", "제9호 라목 (4)", "광감지식개폐장치를 설치하는 경우에는 바닥면으로부터 0.3미터에서", "light-sensing door reopening device"),
 ("되열림장치", "element", "R1", "제9호 라목 (5)", "다시 열리는 되열림장치를 설치하여야 한다.", "door reopening device"),
 ("토글방식", "technique", "R1", "제9호 라목 (8)", "층수선택버튼이 토글방식인 경우에는", "toggle call buttons with voice confirmation and cancel"),
 ("저시력인", "user group", "R1", "제9호 라목 (10)", "저시력인 등 장애인의 안전을 위하여", "people with low vision"),
 ("장애인용 에스컬레이터", "element", "R1", "제10호 (heading)", "10. 장애인용 에스컬레이터", "escalator for disabled people"),
 ("분당 30미터", "quantity", "R1", "제10호 가목 (2)", "속도는 분당 30미터 이내로 하여야 한다.", "escalator speed"),
 ("수평이동손잡이", "element", "R1", "제10호 다목 (2)", "에스컬레이터의 양끝부분에는 수평이동손잡이를 1.2미터 이상 설치하여야 한다.", "horizontal moving handrail"),
 ("수평고정손잡이", "element", "R1", "제10호 다목 (3)", "1미터 이상의 수평고정손잡이를 설치할 수", "fixed horizontal handrail beyond the escalator"),
 ("경사형 휠체어리프트", "element", "R1", "제11호 나목", "경사형 휠체어리프트는 휠체어받침판의 유효면적을 폭 0.76미터 이상", "inclined platform lift"),
 ("수직형 휠체어리프트", "element", "R1", "제11호 다목", "수직형 휠체어리프트는 내부의 유효바닥면적을 폭 0.9미터 이상", "vertical platform lift; mandatory for new builds (D2 제3호 가목 (6))"),
 ("비상정지", "element", "R1", "제11호 가목 (3)", "운행중 돌발상태가 발생하는 경우 비상정지시킬 수 있고", "emergency stop"),
 ("상시보조서비스", "compliance condition (staffing)", "R1", "제12호 나목 (2) (다)", "시설관리자 등으로부터 상시보조서비스가 제공될 것", "standing assistance service as one condition for a steeper ramp"),
 ("매트", "element", "R1", "제12호 라목 (3)", "휠체어의 벽면충돌에 따른 충격을 완화하기 위하여 벽에 매트를 부착할 수 있다.", "wall padding"),
 ("측면접근", "technique", "R1", "제13호 나목 (1) (가)", "휠체어의 측면접근을 위하여 유효폭 0.75미터 이상의 활동공간을 확보하여야 한다.", "side transfer space"),
 ("등받이가 있는 양변기형태", "element form", "R1", "제13호 나목 (2) (가)", "대변기는 등받이가 있는 양변기형태로 하되", "Western-style WC with backrest (excludes squat pan)"),
 ("회전식", "element form", "R1", "제13호 나목 (3) (나)", "다른쪽 손잡이는 0.6미터 내외의 길이로 회전식으로 설치하여야 한다.", "swing-away grab bar"),
 ("사다리형태의 손잡이", "element", "R1", "제13호 나목 (3) (마)", "천장에 부착된 사다리형태의 손잡이를 설치할 수 있다.", "ceiling-mounted ladder grab"),
 ("화장실사용여부를 시각적으로 알 수 있는 설비", "element", "R1", "제13호 나목 (4) (나)", "출입문에는 화장실사용여부를 시각적으로 알 수 있는 설비 및 잠금장치를 갖추어야 한다.", "visual occupied indicator"),
 ("비상용 벨", "element", "R1", "제13호 나목 (4) (라)", "바닥면으로부터 0.2미터 내외의 높이에서도 이용이 가능하도록 하여야 한다.", "emergency bell reachable from the floor"),
 ("음성유도장치", "element", "R1", "제13호 가목 (3) (라)", "안내표시와 함께 음성유도장치를 설치하여야 한다.", "audio guidance to toilets in welfare facilities"),
 ("보행곤란자", "user group", "R1", "제13호 라목 (2) (가)", "목발사용자 등 보행곤란자를 위하여", "people with walking difficulty, crutch users"),
 ("냉·온수의 구분", "information", "R1", "제13호 라목 (2) (나)", "수도꼭지는 냉·온수의 구분을 점자로 표시하여야 한다.", "hot/cold in braille"),
 ("물에 젖어도 미끄러지지 아니하는 재질", "material property", "R1", "제13호 가목 (2) (가)", "바닥표면은 물에 젖어도 미끄러지지 아니하는 재질로 마감하여야 한다.", "wet slip resistance"),
 ("온돌방보다 침대방", "room type", "R1", "제19호 나목 (1)", "휠체어사용자를 위한 객실등은 온돌방보다 침대방으로 할 수 있다.", "bed room rather than floor-heated (ondol) sleeping room"),
 ("청각장애인용 초인등", "element", "R1", "제19호 라목 (4)", "초인종과 함께 청각장애인용 초인등을 설치하여야 한다.", "doorbell light"),
 ("청각장애인용 경보설비", "element", "R1", "제19호 라목 (5)", "건축물전체의 비상경보시스템과 연결된 청각장애인용 경보설비를 설치하여야 한다.", "visual alarm linked to the building system"),
 ("동행인", "user group", "R1", "제20호 나목 (1)", "휠체어사용자가 아닌 동행인이 함께 앉을 수 있도록 하여야 한다.", "companion seating"),
 ("시야", "quantity (sightline)", "R1", "제20호 나목 (3)", "시야가 확보될 수 있도록 관람석 앞에 기둥이나 시야를 가리는 장애물 등을 두어서는 아니 되며", "sightlines"),
 ("열람석", "element", "R1", "제20호 다목 (1)", "열람석상단까지의 높이는 바닥면으로부터 0.7미터 이상 0.9미터 이하로", "reading desk"),
 ("접수대 또는 작업대", "element", "R1", "제21호 (heading)", "21. 장애인등의 이용이 가능한 접수대 또는 작업대", "reception or work counter"),
 ("동전투입구", "element", "R1", "제22호 나목 (2)", "자동판매기 또는 자동발매기의 동전투입구·조작버튼·상품출구의 높이는", "vending machine coin slot"),
 ("임산부 등을 위한 휴게시설", "element", "R1", "제27호 (heading)", "27. 임산부 등을 위한 휴게시설", "rest facility for pregnant women and others"),
 ("수유실", "room", "R1", "제27호 나목 (1)", "수유실로 사용할 수 있는 장소를 별도로 마련하되, 기저귀교환대, 세면대 등의 설비를 갖추어야 한다.", "nursing room with changing table"),
 ("지팡이 및 목발을 세울 곳", "element", "R1", "제28호 라목", "지팡이 및 목발을 세울 곳을 마련할 수 있다.", "cane and crutch rest at telephones"),
 ("우체통투입구", "element", "R1", "제29호 나목", "우체통투입구의 높이는 0.9미터 이상 1.2미터 이하로 하여야 한다.", "post-box slot"),
 ("매립식", "installation method", "R1", "제16호 나목 (3)", "점자블록은 매립식으로 설치하여야 한다.", "embedded tiles; 부착식 (surface-applied) as exception"),
 ("촉지도식 안내판", "element", "R1", "제17호 가목 (1)", "점자안내판 또는 촉지도식 안내판에는 주요시설 또는 방의 배치를 점자, 양각면 또는 선으로 간략하게 표시하여야 한다.", "tactile map board"),
 ("전자식 신호장치", "element", "R1", "제17호 다목", "특수신호장치를 소지한 시각장애인이 접근할 경우 대상시설의 이름을 안내하는 전자식 신호장치를 설치할 수 있다.", "beacon announcing the facility name"),
 ("점멸형태의 비상경보등", "element", "R1", "제18호", "비상벨설비 주변에는 점멸형태의 비상경보등을 함께 설치하고", "flashing emergency light"),
 ("음향신호기", "element", "D2", "제3호 가목 (11) (다)", "횡단보도에 시각장애인을 위한 음향신", "audible pedestrian signal (quote stops at the cell break)"),
 ("전자문자안내판", "element", "D2", "제3호 가목 (11) (라)", "전자문자안내판 또는 기타 전자문자안내", "electronic text display for deaf users"),
 ("통로유도등", "element", "D2", "제3호 가목 (12) (가)", "청각장애인용 피난구유도등·통로유도등 및 시각장애인용", "exit and route guidance lights"),
 ("영유아용 거치대", "element", "D2", "제3호 가목 (7)", "영유아용 거치대 등 임산부 및 영유아가 안전하고 편리하게 이용할 수 있는", "infant seat in toilets"),
 ("높이 차이가 있는 무대", "element", "D2", "제3호 가목 (14) (나)", "공연장, 집회장 및 강당 등에 설치된 무대에 높이 차이가", "stage access"),
 ("장애인전용주택", "building class", "D2", "제4호 가목 (4) (나)", "장애인전용주택의 세대내 출입문은", "housing dedicated to disabled residents"),
 ("골도전화기", "element (defined)", "D2", "제6호 가목 (2)", "골도전화기(청각장애인을 위하여 머리뼈", "bone-conduction telephone (definition continues past the line)"),
 ("주변소음도", "quantity", "D2", "제6호 가목 (1)", "주변소음도가 75데시벨이상인 경우에는", "ambient noise level as an exemption trigger"),
 ("부출입구", "compliance route (alternative entrance)", "D2", "제3호 가목 (3) (나)", "주출입구 대신 부출입구의 높이차이", "secondary entrance in place of the main one"),
 ("청색과 백색", "colour rule", "R2", "제2호 가목", "청색과 백색", "blue and white"),
 ("기본형", "sign type", "R2", "제2호 다목", "시각장애인용 안내표지와 청각장애인용 안내표지는 기본형과 함께 설치하여야 한다.", "base pictogram plus disability-specific signs"),
]

# ---------------------------------------------------------------- seeds (model-generated, flagged)
SEEDS = [
 ("Drainage", "배수구 / 배수 기울기", "KR", "MODEL-GENERATED; not in the texts read; probably in 건축물의 설비기준 등에 관한 규칙 or BF certification guidance (not read)"),
 ("Microwave mounting height accessible and safe", "전자레인지 설치높이", "KR", "MODEL-GENERATED; kitchens are not regulated by the Act's annexes; possibly 장애인 주거 개조 guides"),
 ("force", "조작력 / 개폐력", "KR", "MODEL-GENERATED; held aliases 조작력, 개폐력 occur in no text read; possibly KS or BF certification evaluation items"),
 ("operating force (parameter 6)", "문 개폐력 (N)", "KR", "MODEL-GENERATED"),
 ("reverberation time (parameter 7)", "잔향시간", "KR", "MODEL-GENERATED; held alias 잔향 시간 occurs in no text read; school or acoustic standards (not read)"),
 ("colour temperature (parameter 10)", "색온도 (K)", "KR", "MODEL-GENERATED; held alias 색온도 occurs in no text read; KS C lighting standards (not read)"),
 ("capacity", "적재하중 / 정원(인승)", "KR", "MODEL-GENERATED; lift capacity is in lift safety rules, not here"),
 ("B651 8.3.8 Speed bumps", "과속방지턱", "KR", "MODEL-GENERATED; road-side rules (교통약자의 이동편의 증진법, not read)"),
 ("B651 8.3.9 Bollards", "볼라드 / 차량진입억제용 말뚝", "KR", "MODEL-GENERATED; 교통약자의 이동편의 증진법 시행규칙 (not read)"),
 ("B651 8.7.1 Flower or shrub planters", "화단 / 식재", "KR", "MODEL-GENERATED"),
]

def ok(ins, q, ph):
    return strip(q) in TXT[ins] and strip(ph) in strip(q)

def main():
    bad = 0
    for c, *_ in OBS:
        for x in c.split('|'):
            if x not in LAB: print('UNKNOWN CONCEPT', x, file=sys.stderr); bad += 1
    for x in list(PARTIAL) + list(ABSENT):
        if x not in LAB: print('UNKNOWN CONCEPT (status maps)', x, file=sys.stderr); bad += 1
    rows = []
    for c, ph, ins, loc, q, note in OBS:
        v = ok(ins, q, ph)
        if not v: bad += 1; print('OBS FAIL', ins, loc, ph, strip(q) in TXT[ins], file=sys.stderr)
        rows.append([c, ph, 'ko', ins + ' ' + INST[ins][0], loc + page(ins, q), q, 'text/' + INST[ins][5], 'yes' if v else 'NO', note])
    W = lambda name: csv.writer(open(D + '/' + name, 'w', newline='', encoding='utf-8'), delimiter='\t', lineterminator='\n')
    w = W('observations.tsv')
    w.writerow(['concept (register label; | = counts for each)', 'phrase_verbatim', 'language', 'instrument', 'locator (item as printed; PDF page computed)', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text (whitespace-stripped)', 'note (ours)'])
    w.writerows(rows)
    w = W('reverse-harvest.tsv')
    w.writerow(['phrase_verbatim (instrument own phrase)', 'kind (ours)', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text (whitespace-stripped)', 'gloss_OURS_not_an_equivalence'])
    for ph, kind, ins, loc, q, g in REV:
        v = ok(ins, q, ph)
        if not v: bad += 1; print('REV FAIL', ins, loc, ph, strip(q) in TXT[ins], file=sys.stderr)
        w.writerow([ph, kind, 'ko', ins + ' ' + INST[ins][0], loc + page(ins, q), q, 'text/' + INST[ins][5], 'yes' if v else 'NO', g])
    w = W('coverage.tsv')
    w.writerow(['register_concept', 'register_source', 'status', 'n_observations', 'phrases_found (distinct)', 'note'])
    st_count = {}
    for c, src in REGISTER:
        hit = [r for r in rows if c in r[0].split('|')]
        if hit:
            st = 'FOUND-PARTIAL' if c in PARTIAL else 'FOUND'
            w.writerow([c, src, st, len(hit), ' / '.join(sorted({r[1] for r in hit})), PARTIAL.get(c, '')])
        else:
            st = 'SEARCHED-ABSENT'
            if c not in ABSENT: print('NO ABSENCE NOTE', c, file=sys.stderr); bad += 1
            w.writerow([c, src, st, 0, '', ABSENT.get(c, 'NO NOTE')])
        st_count[st] = st_count.get(st, 0) + 1
    w = W('seeds.tsv')
    w.writerow(['register_concept', 'seed (MODEL-GENERATED, not a finding)', 'jurisdiction meant', 'flag and note'])
    for s in SEEDS:
        if s[0] not in ABSENT: print('SEED FOR NON-ABSENT CONCEPT', s[0], file=sys.stderr); bad += 1
        w.writerow(s)
    w = W('instruments.tsv')
    w.writerow(['code', 'title_as_written', 'issuing_body', 'edition_in_force (from the bytes)', 'url', 'artefact', 'sha256_retrieved_bytes', 'text_file', 'sha256_text_file', 'retrieval_status', 'read_in_full', 'parts_read_and_skipped'])
    READ = {
     'R1': ('yes (text); figures unread', 'READ: items 1, 4-22, 27-29 and 비고 (items 2, 3, 23-26 are 삭제). SKIPPED: every "아래의 그림" figure (images; the extracted text has blank space where they sit).'),
     'D2': ('yes', 'READ: items 2, 3 가목 (1)-(17), 3 나목 matrix, 4, 6. The 의무/권장 matrix was read cell by cell for layout only: its column alignment in extracted text is unreliable, so no observation depends on which facility a cell belongs to.'),
     'D1': ('yes', 'READ: items 1-4 and 비고.'),
     'R2': ('yes (text); drawing unread', 'READ: items 1-3 text. SKIPPED: the 작도법 drawing (image).'),
     'ACT': ('partly', 'READ: arts 1-9, 14-17. SKIPPED: arts 9의2-13 (conformity check, certification administration, surveys, plans, council, support), 22-27 (inspection, orders, penalties), 부칙.'),
     'DEC': ('partly', 'READ: arts 1-5의2, 7, 7의2. SKIPPED: arts 6-6의7 (council), 7의3-15 (parking permits, enforcement, fines), 부칙, and 별표 2의2-3 (certification-duty facilities, not fetched).'),
     'RUL': ('partly', 'READ: arts 1-8. SKIPPED: 부칙; 별표 3 (equipment to keep) and forms not fetched.'),
    }
    man = {}
    import json
    for l in open('retrieval-log/session_2026-11-06-base-vocabulary-review/manifest.jsonl', encoding='utf-8'):
        d = json.loads(l)
        if d.get('status') == 200: man[d['artefact']] = d['sha256']
    for k, (t, iss, ed, url, art, tf) in INST.items():
        sha = man.get(art, 'NOT IN MANIFEST')
        if sha == 'NOT IN MANIFEST' or hashlib.sha256(open('retrieval-log/session_2026-11-06-base-vocabulary-review/' + art, 'rb').read()).hexdigest() != sha:
            print('ARTEFACT HASH MISMATCH', k, file=sys.stderr); bad += 1
        tsha = hashlib.sha256(open(D + '/text/' + tf, 'rb').read()).hexdigest()
        w.writerow([k, t, iss, ed, url, art, sha, 'text/' + tf, tsha, 'RETRIEVED 200', READ[k][0], READ[k][1]])
    w.writerow(['BF', '장애물 없는 생활환경 인증에 관한 규칙 (certification criteria)', '보건복지부·국토교통부 공동부령', 'not determined', '', '', '', '', '', 'NOT ATTEMPTED (budget)', 'no', 'named in Act art 10의2; its evaluation items were not fetched'])
    w.writerow(['KS', 'KS standards cited by guidance (none cited in the texts read)', '', '', '', '', '', '', '', 'NOT ATTEMPTED', 'no', 'no KS number occurs in the seven texts'])
    print('register', len(REGISTER), 'status', st_count)
    print('observations', len(rows), 'distinct phrases', len({r[1] for r in rows}), 'reverse-harvest', len(REV), 'seeds', len(SEEDS), 'failures', bad)
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
