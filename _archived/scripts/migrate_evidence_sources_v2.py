#!/usr/bin/env python3
"""
Full migration: evidence_sources → evidence_sources_v2 + evidence_source_authors
Includes: field decomposition, language detection, translation, author normalization
"""

import sqlite3, re, json, csv, shutil, os, sys, datetime
from collections import defaultdict

try:
    import langdetect
    langdetect.DetectorFactory.seed = 42
    HAS_LANGDETECT = True
except ImportError:
    HAS_LANGDETECT = False

DB_IN  = "/home/claude/guidebook-final.db"
DB_OUT = "/home/claude/guidebook-migrated.db"
REVIEW_CSV = "/home/claude/migration-review.csv"
TS = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")

# ──────────────────────────────────────────────────────────────
# TRANSLATIONS: non-Latin titles/names translated by Claude directly
# ──────────────────────────────────────────────────────────────
TRANSLATIONS = {
    # Japanese
    "盲道 specifications":
        "Tactile guiding block (blister/corduroy paving) specifications",
    "点字ブロック":
        "Tactile paving blocks (braille blocks)",
    "盲ろう者のコミュニケーション":
        "Communication for deafblind persons",
    "建築設計標準 (updated)":
        "Architectural Design Standards (updated)",
    "障害者の居住にも対応した住宅の設計ハンドブック":
        "Design handbook for housing that accommodates persons with disabilities",
    "カームダウンスペース — calming space research (JP/US/FR comparison)":
        "Calm-down space — calming space research (Japan / US / France comparison)",
    "感覚過敏及び発達障害傾向を有する人の簡易構造物を用いたカームダウンスペース使用時における生体情報とアンケート回答の傾向分析及び日本・アメリカ・フランスでの実証実験の総合比較":
        "Analysis of biological information and questionnaire response tendencies when using calm-down spaces with simple structures among persons with sensory hypersensitivity and neurodevelopmental tendencies, with comprehensive comparison of practical experiments conducted in Japan, the United States, and France",
    "バリアフリー法 建築物移動等円滑化誘導基準":
        "Barrier-Free Law: Guidance standards for facilitating mobility in buildings",
    "バリアフリー法 — 段差なし principle":
        "Barrier-Free Law: Zero-step (level-access) principle",
    "バリアフリー法 — 出入口規定":
        "Barrier-Free Law: Entrance and exit regulations",
    "光警報装置 guideline — recommended not mandatory":
        "Visual alarm device guideline — recommended, not mandatory",
    # Korean
    "편의증진법 시행규칙 별표1 §3 — 시각장애인 유도 블록":
        "Enforcement rules of the Act on Convenience Promotion, Annex 1 §3 — tactile guidance blocks for visually impaired persons",
    "Tactile route advocacy publications":
        "Tactile route advocacy publications",  # already English
    "서울형 치매전담실 가이드북":
        "Seoul-type dementia care room guidebook",
    "장애인·노인·임산부 등의 편의증진 보장에 관한 법률 (Act on Convenience Promotion for":
        "Act on Convenience Promotion for Persons with Disabilities, the Elderly, Pregnant Women, etc.",
    "편의증진법 — 점자블록 statutory provisions":
        "Act on Convenience Promotion — tactile paving block statutory provisions",
    # Chinese (Simplified)
    "城市普通中小学校校舍建设标准 — National school building standards (China),":
        "National standards for construction of urban primary and secondary school buildings (China)",
    "北京市特殊教育学校设计规范":
        "Beijing special education school design standards",
    "老年住宅 (3rd ed.). China Architecture & Building Press":
        "Elderly housing (3rd ed.). China Architecture & Building Press",
    "无障碍设计规范 (Code for Accessibility Design)":
        "Code for accessibility design — GB 50763-2012",
    "GB 50763-2012 §3.2 — 盲道 specifications":
        "Code for Accessibility Design §3.2 — tactile guiding surface specifications",
    "GB 50763-2012 §3.12.4 无障碍设计规范 (Code for Accessibility Design":
        "Code for Accessibility Design §3.12.4 — accessible design regulations",
    "GB 50763-2012 盲道 (tactile wayfinding)":
        "Code for Accessibility Design — tactile guiding surfaces (wayfinding)",
    "GB 50763-2012 §8 — visual alarm provisions":
        "Code for Accessibility Design §8 — visual alarm provisions",
    "GB 50118-2010 §5.3.4 — Room acoustic performance":
        "Code for sound insulation design of civil buildings §5.3.4 — room acoustic performance",
    # Japanese corporate names
    "MLIT Japan": "Ministry of Land, Infrastructure, Transport and Tourism (Japan)",
    "MLIT / JIS": "Ministry of Land, Infrastructure, Transport and Tourism / Japan Industrial Standards (Japan)",
    "MEXT (文部科学省)": "Ministry of Education, Culture, Sports, Science and Technology (Japan) — MEXT",
    "FDMA Japan": "Fire and Disaster Management Agency (Japan)",
    "筑波大学 (Tsukuba University researchers)": "University of Tsukuba researchers",
    "全難聴 (Zennancho)": "Zennancho — Japan Federation of the Hard of Hearing and Late-Deafened",
    # Korean corporate names
    "한국시각장애인연합회": "Korea Blind Union (KBU) / Visually Impaired Persons Association of Korea",
    "Korean Government": "Korean Government",
    "Seoul Metropolitan Government": "Seoul Metropolitan Government",
    "Korea Ministry": "Korean Ministry (accessibility)",
    "Korean OT researchers (KCI/Korea Science": "Korean OT researchers (KCI/Korea Science Index)",
    # Chinese corporate names
    "MOHURD": "Ministry of Housing and Urban-Rural Development (China) — MOHURD",
    "GB/T 16252 + 建标156-2011": "GB/T 16252 + 建标156-2011 (National school building standards, China)",
    "Beijing Municipal Government": "Beijing Municipal Government",
    "Zhejiang Standard": "Zhejiang Provincial Standard",
    "周燕珉 et al.": "Zhou Yanmin et al.",
    # Finnish
    "Invalidiliitto": "Invalidiliitto (Finnish Association of People with Physical Disabilities)",
    "ESKEH-kartoitusmenetelmä — accessibility audit framework":
        "ESKEH survey method — accessibility audit framework",
}

def translate(text, lang):
    """Return English translation if available, else None."""
    if not text: return None
    if lang == 'en': return None  # already English
    # Direct lookup
    for key, val in TRANSLATIONS.items():
        if text.strip().startswith(key) or key in text:
            return val
    return None

def detect_lang(text):
    """Detect language. Returns (iso_code, method)."""
    if not text or len(text.strip()) < 3:
        return 'en', 'default'
    # Unicode block detection for non-Latin scripts (fast, high confidence)
    has_jp = any(0x3040 <= ord(c) <= 0x30FF or 0x4E00 <= ord(c) <= 0x9FFF for c in text)
    has_ko = any(0xAC00 <= ord(c) <= 0xD7AF or 0x1100 <= ord(c) <= 0x11FF for c in text)
    has_zh = any(0x4E00 <= ord(c) <= 0x9FFF for c in text) and not has_jp
    has_ar = any(0x0600 <= ord(c) <= 0x06FF for c in text)
    has_hi = any(0x0900 <= ord(c) <= 0x097F for c in text)
    has_ru = any(0x0400 <= ord(c) <= 0x04FF for c in text)

    if has_ko: return 'ko', 'unicode_block'
    if has_jp: return 'ja', 'unicode_block'
    if has_zh: return 'zh', 'unicode_block'
    if has_ar: return 'ar', 'unicode_block'
    if has_hi: return 'hi', 'unicode_block'
    if has_ru: return 'ru', 'unicode_block'

    # For Latin-script texts, use langdetect
    if HAS_LANGDETECT:
        try:
            lang = langdetect.detect(text)
            return lang, 'langdetect'
        except:
            pass
    return 'en', 'default'

# ──────────────────────────────────────────────────────────────
# TITLE PARSER
# ──────────────────────────────────────────────────────────────
JOURNAL_PATTERN = re.compile(
    r'\.?\s+'
    r'([A-Z][A-Za-z &\-]{1,50})'   # journal abbreviation
    r'\s+(\d+)\(([^)]+)\)[:\s]+'   # vol(issue):
    r'([\d]+(?:e\d+)?)'            # pages start
    r'(?:[–\-]([\d]+))?'           # pages end (optional)
)
PAGES_PATTERN = re.compile(r'\bpp?\.?\s*([\d]+)\s*[–\-]\s*([\d]+)')

def parse_title(raw):
    """Decompose the title field into structured parts. Returns a dict."""
    if not raw:
        return {}
    t = raw
    out = {
        'pub_title': None, 'pub_subtitle': None, 'chapter_title': None,
        'journal_abbrev': None, 'volume': None, 'issue': None,
        'pages_start': None, 'pages_end': None, 'article_number': None,
        'doi': None, 'pmid': None, 'url': None,
        'bpc_shorthand': None, 'bpc_note': None,
        'grey_flag': 0, 'grey_reason': None,
        'verification_note': None,
        'standard_number': None,
        'book_title': None,
        'publisher': None,
        'source_type_hint': None,
    }

    # 1. Verification notes
    m = re.search(r'\[((?:UNVERIFIED|POSSIBLE.ERROR|GAP:|Unverified)[^\]]*)\]', t, re.I)
    if m:
        out['verification_note'] = m.group(1).strip()
        t = t[:m.start()] + t[m.end():]

    # 2. GREY flag
    m = re.search(r'\[GREY\s*(?:—\s*([^\]]+))?\]', t, re.I)
    if m:
        out['grey_flag'] = 1
        out['grey_reason'] = (m.group(1) or '').strip() or None
        t = t[:m.start()] + t[m.end():]

    # 3. DOI inline
    for pattern in [
        r'DOI[:\s]+(10\.\S+?)(?:\s|$|\]|\)|\.(?:\s|$))',
        r'https?://doi\.org/(10\.\S+?)(?:\s|$|\]|\))',
    ]:
        m = re.search(pattern, t, re.I)
        if m:
            doi_cand = m.group(1).rstrip('.,;)')
            if re.match(r'^10\.\d{4,}/', doi_cand):
                out['doi'] = doi_cand
            t = t[:m.start()] + t[m.end():]

    # 4. PMID inline
    m = re.search(r'PMID[:\s]+(\d{5,})', t, re.I)
    if m:
        out['pmid'] = m.group(1)
        t = t[:m.start()] + t[m.end():]

    # 5. URL inline
    m = re.search(r'https?://\S+', t)
    if m:
        out['url'] = m.group(0).rstrip('.,;)')
        t = t[:m.start()] + t[m.end():]

    # 6. Journal citation block: "Journal Abbrev Vol(Issue):pages"
    m = JOURNAL_PATTERN.search(t)
    if m:
        journal_cand = m.group(1).strip()
        # Filter out false matches (plain English words)
        noise = {'In', 'The', 'DOI', 'PMID', 'URL', 'See', 'From', 'Per'}
        if journal_cand not in noise and len(journal_cand) > 2:
            out['journal_abbrev'] = journal_cand
            out['volume'] = m.group(2)
            out['issue'] = m.group(3)
            out['pages_start'] = m.group(4)
            out['pages_end'] = m.group(5)
            t = t[:m.start()] + t[m.end():]

    # 6b. "pp. X–Y" pattern (for book chapters)
    if not out['pages_start']:
        m = PAGES_PATTERN.search(t)
        if m:
            out['pages_start'] = m.group(1)
            out['pages_end'] = m.group(2)
            t = t[:m.start()] + t[m.end():]

    # 7. Book chapter: "In [Editor/Book]"
    m = re.search(r'\.\s+In\s+(.{5,80}?)(?:\.|$)', t, re.I)
    if m:
        out['book_title'] = m.group(1).strip()
        out['source_type_hint'] = 'book_chapter'
        t = t[:m.start()] + t[m.end():]

    # 8. Standard number detection
    m = re.search(
        r'\b((?:ISO|DIN|BS|EN|NEN|AS|NZS|JIS|GB|UNI|CEN|IEC|ANSI|ASHRAE|NFPA|CSA|NBR|TEK|BFS|BBR|BR18|NCC)'
        r'[\s/]?[\w\-\.:+]+(?::\d{4})?)',
        t)
    if m:
        out['standard_number'] = m.group(1)
        out['source_type_hint'] = 'standard'

    # 9. Internal file path
    if re.match(r'^references/', t.strip()):
        out['source_type_hint'] = 'internal'

    # 10. BPC shorthand: leading annotation before em-dash (not a subtitle em-dash)
    # Pattern: short BPC note — actual title
    m = re.match(r'^([A-Z][A-Z0-9\s\-\.]{3,40})\s+—\s+(.+)$', t.strip())
    if m and len(m.group(1).split()) <= 5:
        out['bpc_shorthand'] = m.group(1).strip()
        t = m.group(2).strip()

    # 11. Trailing BPC note after period
    m = re.search(r'\.\s+(\[.+?\])\s*$', t)
    if m:
        out['bpc_note'] = m.group(1)
        t = t[:m.start()+1]

    # 12. Publisher (for books/reports)
    m = re.search(r'\.\s+([A-Z][A-Za-z &]+(?:Press|Publishers?|Publications?|Books?|University Press))\s*\.?\s*$', t)
    if m:
        out['publisher'] = m.group(1).strip()
        t = t[:m.start()]

    # Clean up pub_title
    pub_title = t.strip().strip('.,;')
    # Split subtitle at ': '
    if ': ' in pub_title and not re.search(r'https?://', pub_title):
        parts = pub_title.split(': ', 1)
        pub_title = parts[0].strip()
        out['pub_subtitle'] = parts[1].strip()

    out['pub_title'] = pub_title if pub_title else None
    return out

# ──────────────────────────────────────────────────────────────
# YEAR PARSER
# ──────────────────────────────────────────────────────────────
def parse_year(raw):
    y = str(raw or '').strip()
    if re.match(r'^\d{4}$', y):
        return int(y), None
    if y in ('n.d.', 'n.d', ''):
        return None, 'n.d.'
    if y == 'ongoing':
        return None, 'ongoing'
    if y == 'annual':
        return None, 'annual'
    # "2020/pub.2022" → 2022
    m = re.search(r'pub\.?(\d{4})', y)
    if m: return int(m.group(1)), y
    # "April 2017" → 2017
    m = re.search(r'(\d{4})', y)
    if m: return int(m.group(1)), y
    return None, y or None

# ──────────────────────────────────────────────────────────────
# AUTHOR PARSER
# ──────────────────────────────────────────────────────────────
PLACEHOLDER_RE = re.compile(
    r'^\(?(internal|author TBC|E\d+\s*—|source TBC|authors TBC|scoping review author TBC'
    r'|C0\d+|Crompton co-author|2024 scoping|India Autism|UAE \(case)', re.I)

INDIVIDUAL_RE = re.compile(r'^[A-ZÀ-Öa-zà-ö][a-zà-öA-Z\'\-]+,\s*[A-Z]')

CORPORATE_SIGNALS = re.compile(
    r'\b(ISO|DIN|WHO|CDC|MLIT|MOHURD|RNIB|RCOT|CAOT|COTEC|APF|DPI|SCIE|NDTi|PVA|DSDC|DbI'
    r'|ABNT|AENOR|BSI|CEN|IEC|ANSI|ASHRAE|ASA|NFPA|CSA|NEN|AIJ|UNI|IES|CIE|IEEE'
    r'|HLAA|AOTA|ESCAP|BCA|ABCB|WELL|LEED|IWBI|RHF|KfW|HDB|ANAH|NDIS|NHS|NICE'
    r'|VA|DOJ|HUD|UN|EU|ICC|OECD|UNESCO|FDMA|MEXT|JIS|SBi|Rijksoverheid|Légifrance'
    r'|Riksdagen|Boverket|Husbanken|Direktoratet|Invalidiliitto|Zennancho|全難聴|全日本'
    r'|한국|서울|Korean Government|Swedish|Finnish|Norwegian|Ministry|Department'
    r'|Government|Commission|Committee|Federation|Alliance|Council|Authority'
    r'|Foundation|Institute|Association|Society|Network|Center|Centre)\b', re.I)

def parse_authors(raw):
    """Returns list of author dicts: [{last, first, suffix, corporate_name, is_corporate, role, position}]"""
    if not raw: return []
    raw = raw.strip()

    if PLACEHOLDER_RE.match(raw):
        return []  # no rows; author_count_is_complete=0

    authors = []
    role = 'author'

    # Detect "Eds." editors
    if re.search(r'\(Ed[s]?\.\)', raw, re.I):
        role = 'editor'
        raw = re.sub(r'\s*\(Ed[s]?\.\)', '', raw, flags=re.I)

    # Truncated? Flag
    is_complete = 1
    if ' et al' in raw.lower():
        is_complete = 0
        raw = re.sub(r'\s*et al\.?', '', raw, flags=re.I)

    # Split on ' & ', ' and ', '; ', or '/'
    if '/' in raw and not re.search(r'https?://', raw):
        parts = [p.strip() for p in raw.split('/')]
    elif re.search(r';\s', raw):
        parts = [p.strip() for p in raw.split(';')]
    elif ' & ' in raw:
        parts = [p.strip() for p in raw.split(' & ')]
    elif ',' in raw:
        # Could be "Last, F., Last, F., ..." or "Last, First"
        # If more than one "Last, F." pattern, it's a list
        matches = re.findall(r'[A-ZÀ-Ö][a-zà-ö\'\-]+,\s*[A-Z][a-z\.]*', raw)
        if len(matches) > 1:
            parts = []
            remaining = raw
            for m in matches:
                idx = remaining.find(m)
                parts.append(m.strip())
                remaining = remaining[idx + len(m):]
        else:
            parts = [raw]
    else:
        parts = [raw]

    for i, part in enumerate(parts):
        part = part.strip().strip(',')
        if not part: continue

        is_corp = (
            bool(CORPORATE_SIGNALS.search(part)) or
            not bool(re.search(r'[a-zà-ö]{3,}.*,', part)) and
            not bool(INDIVIDUAL_RE.match(part))
        )

        # Non-Latin → always corporate
        if any(ord(c) > 0x0500 for c in part):
            is_corp = True

        if is_corp:
            authors.append({
                'position': i + 1,
                'is_corporate': 1,
                'corporate_name': part,
                'corporate_name_en': None,
                'last_name': None,
                'first_name': None,
                'suffix': None,
                'orcid': None,
                'role': role,
            })
        else:
            # Parse "Last, F.M." or "Last, FirstName" or "LastF" (no comma)
            if ',' in part:
                last, _, rest = part.partition(',')
                first = rest.strip()
                # Suffix detection
                suffix = None
                for suf in ('Jr.', 'Sr.', 'III', 'II', 'IV'):
                    if first.endswith(suf):
                        suffix = suf
                        first = first[:-len(suf)].strip()
            else:
                # No comma: "Hamre C" or "Levine D" — last token is initial
                tokens = part.split()
                if len(tokens) >= 2:
                    last = tokens[0]
                    first = ' '.join(tokens[1:])
                else:
                    last = part
                    first = None
                suffix = None

            authors.append({
                'position': i + 1,
                'is_corporate': 0,
                'corporate_name': None,
                'corporate_name_en': None,
                'last_name': last.strip() if last else None,
                'first_name': first.strip() if first else None,
                'suffix': suffix,
                'orcid': None,
                'role': role,
            })

    return authors, is_complete

# ──────────────────────────────────────────────────────────────
# SOURCE TYPE INFERENCE
# ──────────────────────────────────────────────────────────────
def infer_source_type(parsed_title, tier, authors_raw, evidence_type):
    hint = parsed_title.get('source_type_hint')
    if hint: return hint
    if parsed_title.get('standard_number'):
        return 'standard'
    if tier and int(tier) >= 4:
        return 'standard'
    if parsed_title.get('journal_abbrev') or parsed_title.get('volume'):
        return 'journal_article'
    if parsed_title.get('book_title'):
        return 'book_chapter'
    grey_flag = parsed_title.get('grey_flag', 0)
    if grey_flag:
        return 'grey'
    if evidence_type and 'book' in str(evidence_type).lower():
        return 'book'
    et = str(evidence_type or '').lower()
    if 'review' in et or 'rct' in et or 'cohort' in et or 'study' in et:
        return 'journal_article'
    if re.search(r'RCOT|AOTA|CAOT|WHO|NHS|NICE|NDIS|HUD|VA\b', authors_raw or ''):
        return 'guideline'
    return None  # flag for review

# ──────────────────────────────────────────────────────────────
# EVIDENCE TYPE NORMALIZER
# ──────────────────────────────────────────────────────────────
ET_MAP = {
    'SYSTEMATIC_REVIEW': 'systematic_review',
    'systematic_review_meta_analysis': 'meta_analysis',
    'systematic_review': 'systematic_review',
    'scoping_review': 'scoping_review',
    'narrative_review': 'narrative_review',
    'review': 'narrative_review',
    'REVIEW': 'narrative_review',
    'meta_analysis': 'meta_analysis',
    'CLINICAL_STUDY': 'primary_research',
    'primary-research': 'primary_research',
    'primary_study': 'primary_research',
    'BIOMECHANICS_STUDY': 'biomechanics_study',
    'EXERCISE_PHYSIOLOGY_STUDY': 'exercise_physiology',
    'GOVERNMENT_REPORT': 'government_report',
    'INDUSTRY_GUIDANCE': 'industry_guidance',
    'INTERNATIONAL_STANDARD': 'international_standard',
    'book': 'book',
}

VALID_ET = {
    'rct','systematic_review','meta_analysis','scoping_review','narrative_review',
    'cohort_study','cross_sectional','case_series','primary_research',
    'biomechanics_study','exercise_physiology','clinical_guideline',
    'international_standard','national_standard','government_report',
    'industry_guidance','book','thesis','expert_opinion','grey'
}

def normalize_et(val):
    if not val: return None
    mapped = ET_MAP.get(val, val)
    return mapped if mapped in VALID_ET else None

# ──────────────────────────────────────────────────────────────
# MAIN MIGRATION
# ──────────────────────────────────────────────────────────────
def main():
    shutil.copy(DB_IN, DB_OUT)
    conn = sqlite3.connect(DB_OUT)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")

    # Create new tables
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS evidence_source_authors (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_id              TEXT NOT NULL,
        position            INTEGER NOT NULL,
        last_name           TEXT,
        first_name          TEXT,
        suffix              TEXT,
        orcid               TEXT,
        is_corporate        INTEGER NOT NULL DEFAULT 0,
        corporate_name      TEXT,
        corporate_name_en   TEXT,
        role                TEXT NOT NULL DEFAULT 'author',
        created_at          TEXT,
        created_by_session  TEXT,
        UNIQUE(ref_id, position, role)
    );
    CREATE INDEX IF NOT EXISTS idx_esa_ref_id ON evidence_source_authors(ref_id);
    CREATE INDEX IF NOT EXISTS idx_esa_last   ON evidence_source_authors(last_name);
    CREATE INDEX IF NOT EXISTS idx_esa_corp   ON evidence_source_authors(corporate_name);

    CREATE TABLE IF NOT EXISTS evidence_sources_v2 (
        ref_id                      TEXT PRIMARY KEY,
        source_type                 TEXT,
        -- Author summary (denorm)
        author_count                INTEGER,
        author_count_is_complete    INTEGER DEFAULT 0,
        first_author_last           TEXT,
        first_author_first          TEXT,
        is_corporate_primary        INTEGER DEFAULT 0,
        author_display              TEXT,
        -- Date
        pub_year                    INTEGER,
        pub_year_note               TEXT,
        -- Title
        pub_title                   TEXT,
        pub_subtitle                TEXT,
        chapter_title               TEXT,
        original_title              TEXT,
        -- Language
        lang_detected               TEXT,
        lang_detection_method       TEXT,
        pub_title_en                TEXT,
        pub_subtitle_en             TEXT,
        chapter_title_en            TEXT,
        journal_name_en             TEXT,
        translation_method          TEXT,
        translation_reviewed        INTEGER DEFAULT 0,
        -- Journal
        journal_name                TEXT,
        journal_abbrev              TEXT,
        volume                      TEXT,
        issue                       TEXT,
        pages_start                 TEXT,
        pages_end                   TEXT,
        article_number              TEXT,
        -- Book/Report
        publisher                   TEXT,
        publisher_location          TEXT,
        edition                     TEXT,
        book_title                  TEXT,
        series                      TEXT,
        series_number               TEXT,
        report_number               TEXT,
        institution                 TEXT,
        -- Standard
        standard_number             TEXT,
        -- Identifiers
        doi                         TEXT,
        pmid                        TEXT,
        pmcid                       TEXT,
        isbn                        TEXT,
        issn                        TEXT,
        url                         TEXT,
        url_accessed                TEXT,
        handle                      TEXT,
        local_id                    TEXT,
        -- Evidence classification
        tier                        INTEGER,
        evidence_type               TEXT,
        jurisdiction                TEXT,
        co1_provenance              TEXT,
        co1_source_type             TEXT,
        synthesis_attribution_required INTEGER,
        -- Quality
        metadata_quality            TEXT,
        verification_status         TEXT,
        doi_resolution_outcome      TEXT,
        doi_less_key                TEXT,
        -- Annotations
        bpc_shorthand               TEXT,
        bpc_note                    TEXT,
        grey_flag                   INTEGER DEFAULT 0,
        grey_reason                 TEXT,
        verification_note           TEXT,
        prior_expectation           TEXT,
        search_queries_used         TEXT,
        derivation_chain            TEXT,
        -- Notes / Audit
        notes                       TEXT,
        created_at                  TEXT,
        created_by_session          TEXT,
        updated_at                  TEXT,
        updated_by_session          TEXT
    );
    """)

    rows = conn.execute("""
        SELECT ref_id, authors, year, title, doi, doi_less_key, pmid, tier, evidence_type,
               jurisdiction, metadata_quality, verification_status,
               co1_provenance, co1_source_type, synthesis_attribution_required,
               notes, created_at, created_by_session, updated_at, updated_by_session,
               derivation_chain, prior_expectation, search_queries_used, doi_resolution_outcome
        FROM evidence_sources
    """).fetchall()

    review_rows = []
    migrated = 0
    author_rows_total = 0

    for row in rows:
        ref_id = row['ref_id']
        raw_authors = row['authors'] or ''
        raw_year    = row['year'] or ''
        raw_title   = row['title'] or ''

        # --- Parse title ---
        pt = parse_title(raw_title)

        # --- DOI: prefer existing column if clean ---
        existing_doi = row['doi']
        final_doi = existing_doi if existing_doi and existing_doi.startswith('10.') else pt.get('doi') or existing_doi

        # --- PMID: prefer existing column ---
        final_pmid = row['pmid'] or pt.get('pmid')

        # --- Year ---
        pub_year, pub_year_note = parse_year(raw_year)

        # --- Language detection ---
        text_for_lang = (pt.get('pub_title') or '') + ' ' + raw_authors
        lang, lang_method = detect_lang(text_for_lang.strip())

        # --- Translation ---
        translation_method = 'native_english'
        pub_title_en = None
        if lang != 'en':
            trans = translate(raw_title, lang) or translate(pt.get('pub_title') or '', lang)
            if trans:
                pub_title_en = trans
                translation_method = 'machine_claude'
            else:
                translation_method = None  # needs manual

        # --- Authors ---
        result = parse_authors(raw_authors)
        if result and isinstance(result, tuple):
            author_list, is_complete = result
        else:
            author_list, is_complete = [], 0

        # Denorm fields
        author_count = len(author_list) if author_list else None
        first = author_list[0] if author_list else None
        first_author_last  = first['last_name'] if first and not first['is_corporate'] else None
        first_author_first = first['first_name'] if first and not first['is_corporate'] else None
        is_corporate_primary = first['is_corporate'] if first else 0

        # Author display (APA)
        def apa_name(a):
            if a['is_corporate']:
                return a['corporate_name_en'] or a['corporate_name'] or ''
            ln = a.get('last_name') or ''
            fn = a.get('first_name') or ''
            suf = (', ' + a['suffix']) if a.get('suffix') else ''
            return f"{ln}, {fn}{suf}".strip(', ')

        if not author_list:
            author_display = raw_authors  # preserve original if unparsed
        elif len(author_list) == 1:
            author_display = apa_name(author_list[0])
        elif len(author_list) == 2:
            author_display = f"{apa_name(author_list[0])}, & {apa_name(author_list[1])}"
        else:
            names = [apa_name(a) for a in author_list]
            if not is_complete:
                author_display = ', '.join(names) + ', et al.'
            elif len(names) <= 20:
                author_display = ', '.join(names[:-1]) + ', & ' + names[-1]
            else:
                author_display = ', '.join(names[:19]) + ', ... ' + names[-1]

        # --- Source type ---
        source_type = infer_source_type(pt, row['tier'], raw_authors, row['evidence_type'])

        # --- Evidence type ---
        evidence_type_norm = normalize_et(row['evidence_type'])

        # --- Metadata quality revised ---
        mq = row['metadata_quality']

        # --- Flags for review ---
        flags = []
        if not pt.get('pub_title') or len((pt.get('pub_title') or '').split()) < 2:
            flags.append('SHORT_TITLE')
        if not source_type:
            flags.append('SOURCE_TYPE_UNKNOWN')
        if lang != 'en' and not pub_title_en:
            flags.append('NEEDS_TRANSLATION')
        if not is_complete and author_count and author_count > 0:
            flags.append('ET_AL_INCOMPLETE')
        if not author_list and raw_authors and not PLACEHOLDER_RE.match(raw_authors):
            flags.append('AUTHOR_PARSE_FAILED')

        review_rows.append({
            'ref_id': ref_id,
            'original_authors': raw_authors,
            'original_year': raw_year,
            'original_title': raw_title[:100],
            'pub_title': (pt.get('pub_title') or '')[:80],
            'journal_abbrev': pt.get('journal_abbrev', ''),
            'volume': pt.get('volume', ''),
            'doi_extracted': pt.get('doi', ''),
            'doi_final': final_doi or '',
            'lang': lang,
            'pub_title_en': pub_title_en or '',
            'source_type': source_type or '',
            'author_count': author_count,
            'is_complete': is_complete,
            'flags': '|'.join(flags),
        })

        # --- Insert into evidence_sources_v2 ---
        conn.execute("""
            INSERT OR REPLACE INTO evidence_sources_v2 (
                ref_id, source_type,
                author_count, author_count_is_complete,
                first_author_last, first_author_first,
                is_corporate_primary, author_display,
                pub_year, pub_year_note,
                pub_title, pub_subtitle, chapter_title,
                lang_detected, lang_detection_method,
                pub_title_en, translation_method, translation_reviewed,
                journal_abbrev, volume, issue, pages_start, pages_end,
                book_title, publisher,
                standard_number,
                doi, pmid,
                url, grey_flag, grey_reason, verification_note,
                bpc_shorthand, bpc_note,
                tier, evidence_type, jurisdiction,
                co1_provenance, co1_source_type, synthesis_attribution_required,
                metadata_quality, verification_status,
                doi_resolution_outcome, doi_less_key,
                prior_expectation, search_queries_used, derivation_chain,
                notes, created_at, created_by_session, updated_at, updated_by_session
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            )
        """, (
            ref_id, source_type,
            author_count, is_complete,
            first_author_last, first_author_first,
            is_corporate_primary, author_display,
            pub_year, pub_year_note,
            pt.get('pub_title'), pt.get('pub_subtitle'), pt.get('chapter_title'),
            lang, lang_method,
            pub_title_en, translation_method, 0,
            pt.get('journal_abbrev'), pt.get('volume'), pt.get('issue'),
            pt.get('pages_start'), pt.get('pages_end'),
            pt.get('book_title'), pt.get('publisher'),
            pt.get('standard_number'),
            final_doi, final_pmid,
            pt.get('url'), pt.get('grey_flag', 0), pt.get('grey_reason'),
            pt.get('verification_note'),
            pt.get('bpc_shorthand'), pt.get('bpc_note'),
            row['tier'], evidence_type_norm, row['jurisdiction'],
            row['co1_provenance'], row['co1_source_type'],
            row['synthesis_attribution_required'],
            mq, row['verification_status'],
            row['doi_resolution_outcome'], row['doi_less_key'],
            row['prior_expectation'], row['search_queries_used'],
            row['derivation_chain'],
            row['notes'], row['created_at'], row['created_by_session'],
            TS, 'migration_v2',
        ))
        migrated += 1

        # --- Insert author rows ---
        for a in author_list:
            # Corporate name translation
            corp_name = a.get('corporate_name')
            corp_en = None
            if corp_name:
                corp_en = translate(corp_name, lang) or translate(corp_name, 'ja') or \
                          translate(corp_name, 'ko') or translate(corp_name, 'zh')
                if not corp_en and lang == 'en':
                    corp_en = None  # already English

            try:
                conn.execute("""
                    INSERT OR IGNORE INTO evidence_source_authors
                    (ref_id, position, last_name, first_name, suffix, orcid,
                     is_corporate, corporate_name, corporate_name_en, role,
                     created_at, created_by_session)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    ref_id, a['position'],
                    a.get('last_name'), a.get('first_name'), a.get('suffix'), a.get('orcid'),
                    a['is_corporate'],
                    corp_name, corp_en, a['role'],
                    TS, 'migration_v2',
                ))
                author_rows_total += 1
            except Exception as e:
                pass  # UNIQUE constraint — skip duplicate

    conn.commit()

    # Write review CSV
    with open(REVIEW_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(review_rows[0].keys()))
        writer.writeheader()
        writer.writerows(review_rows)

    # Summary stats
    print(f"\n{'='*60}")
    print(f"MIGRATION COMPLETE")
    print(f"{'='*60}")
    print(f"Rows migrated:          {migrated}")
    print(f"Author rows created:    {author_rows_total}")
    print(f"Review CSV:             {REVIEW_CSV}")

    # Quick validation
    v2_count = conn.execute("SELECT COUNT(*) FROM evidence_sources_v2").fetchone()[0]
    auth_count = conn.execute("SELECT COUNT(*) FROM evidence_source_authors").fetchone()[0]
    print(f"\nevidence_sources_v2:    {v2_count} rows")
    print(f"evidence_source_authors:{auth_count} rows")

    # Field population rates
    print(f"\n{'FIELD':<30} {'POPULATED':>10} {'%':>6}")
    print("─" * 50)
    for field in ['pub_title', 'pub_year', 'source_type', 'lang_detected',
                  'pub_title_en', 'doi', 'pmid', 'journal_abbrev',
                  'standard_number', 'verification_status', 'grey_flag']:
        if field == 'grey_flag':
            n = conn.execute(f"SELECT COUNT(*) FROM evidence_sources_v2 WHERE grey_flag = 1").fetchone()[0]
        else:
            n = conn.execute(f"SELECT COUNT(*) FROM evidence_sources_v2 WHERE [{field}] IS NOT NULL AND [{field}] != ''").fetchone()[0]
        print(f"{field:<30} {n:>10} {100*n//v2_count:>5}%")

    # Flag summary
    flagged = [r for r in review_rows if r['flags']]
    print(f"\nRows with review flags: {len(flagged)}")
    flag_counts = defaultdict(int)
    for r in flagged:
        for f in r['flags'].split('|'):
            if f: flag_counts[f] += 1
    for flag, cnt in sorted(flag_counts.items(), key=lambda x: -x[1]):
        print(f"  {flag:<30} {cnt}")

    # Language distribution
    print(f"\nLanguage distribution (evidence_sources_v2):")
    for row in conn.execute("SELECT lang_detected, COUNT(*) FROM evidence_sources_v2 GROUP BY lang_detected ORDER BY COUNT(*) DESC").fetchall():
        print(f"  {row[0] or 'NULL':<10} {row[1]}")

    conn.close()

if __name__ == '__main__':
    main()
