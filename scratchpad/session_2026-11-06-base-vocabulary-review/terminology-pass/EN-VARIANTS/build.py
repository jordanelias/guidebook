"""Build observations / coverage / reverse-harvest TSVs for the EN-VARIANTS terminology pass (English register
tested against other English-language jurisdictions), verifying every quote (after whitespace collapse) in the saved
extracted text. Adapted from FR-FR/build.py. Run from the repository root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/EN-VARIANTS/build.py
Exits 1 if any quote or phrase fails to verify. Read-only apart from the TSVs in this folder."""
import re, sys, csv, os, importlib.util
D = 'scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/EN-VARIANTS'
INST = {  # jurisdiction -> (instrument title as written, text file)
 'US': ("2010 ADA Standards for Accessible Design", D + '/text/a2f0dc7adef4.txt'),
 'UK': ("The Building Regulations 2010 Approved Document M Volume 2 – Buildings other than dwellings (2015 edition incorporating 2020 and 2024 amendments)", D + '/text/0e5d4dee25b3.txt'),
 'AU': ("Disability (Access to Premises — Buildings) Standards 2010, Compilation No. 3", D + '/text/7aab78bfba5f.txt'),
 'NZ': ("Acceptable Solutions and Verification Methods For New Zealand Building Code Clause D1 Access Routes (D1/AS1 second edition, amendment 6)", D + '/text/02132b6af9ba.txt'),
 'SG': ("Code on Accessibility in the Built Environment 2025 (Version 1.1)", D + '/text/846c3044c174.txt'),
 'IE': ("Building Regulations Technical Guidance Document M 2022 Access and Use", D + '/text/e6042db0542a.txt'),
}
JUR = list(INST)
READ = {'US': 'partly', 'UK': 'full', 'AU': 'full', 'NZ': 'full', 'SG': 'full', 'IE': 'partly'}
def norm(s): return re.sub(r'\s+', ' ', s).strip()
TXT = {k: norm(open(v[1], encoding='utf-8').read()) for k, v in INST.items()}

OBS, REV = [], []
for m in ['obs_uk', 'obs_nz', 'obs_au', 'obs_sg', 'obs_us', 'obs_ie', 'obs_misc']:
    spec = importlib.util.spec_from_file_location(m, f'{D}/tools/{m}.py'); mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod); OBS += mod.OBS; REV += mod.REV

REGISTER = [  # catalogue 2.1 (32), 2.2 (18), base parameters (10), B651 headings RHFAC does not name (15), EN variant concepts (7)
 "Well-illuminated (if site expected to be lit)", "Surface is firm, stable and slip resistant", "Seating", "Handrails", "Clear width",
 "Accessible path of travel", "Drainage", "Clear signage", "Audio accessibility and communication enhancement technologies",
 "Level landings with clear space", "Floor surface is stable, firm, and non-slip", "Clear space for approach",
 "Well illuminated (if required for expected usage)", "Surface is stable, firm, and slip resistant", "Shelter",
 "Riser height and tread depth", "Nosing design", "No open riser", "Level threshold", "Height clearance (if sheltered or parkade)",
 "Edge protection", "Colour-contrasted and slip-resistant strip on nosing", "Tactile attention indicators (truncated domes)", "Slope",
 "Sink faucet is easy to use or automatic", "Outlets and switches are at accessible heights", "Microwave mounting height accessible and safe",
 "Level landings with clear space and at regular intervals", "Colour-contrasted and slip-resistant strip", "Accessible lockers",
 "Accessible door hardware", "Accessible controls",
 "height", "level", "width", "clearance", "number", "slope", "depth", "riser", "tread", "force", "time", "gradient", "size", "volume",
 "capacity", "distance", "lighting levels", "ratio",
 "Ramp gradient (parameter 3)", "Corridor width (parameter 4)", "Turning circle (parameter 5)", "Operating force (parameter 6)",
 "Reverberation time (parameter 7)", "LRV contrast (parameter 8)", "Door width (parameter 9)", "Colour temperature (parameter 10)",
 "Headroom clearance (parameter 11)", "Ramp run length (parameter 12)",
 "Gratings (B651 4.4.4)", "Headroom and protruding objects (B651 4.5)", "Headroom (B651 4.5.1)", "Protruding objects (B651 4.5.2)",
 "Spouts (B651 6.1.2)", "Lavatories (B651 6.2.3)", "Enclosures (B651 6.5.3)", "Speed bumps (B651 8.3.8)", "Bollards (B651 8.3.9)",
 "Landscaping elements (B651 8.7)", "Flower or shrub planters (B651 8.7.1)", "Vegetation (B651 8.7.3)", "Guy wires (B651 8.7.4)",
 "Scaffolding (B651 8.8.2)", "Gradation limits (B651 D.6.1)",
 "curb", "elevator", "washroom", "ramp", "maneuvering", "accessible route", "Well-lit (any)",
]
SRC = [('catalogue 2.1', 32), ('catalogue 2.2', 18), ('base_parameters', 10), ('b651-headings RHFAC-does-not-name', 15), ('EN variant concept (this pass)', 7)]
ALIAS = {"slope": {"Slope"}, "Headroom and protruding objects (B651 4.5)": {"Headroom", "Protruding objects (B651 4.5.2)"},
         "Headroom (B651 4.5.1)": {"Headroom"}, "Lavatories (B651 6.2.3)": {"lavatory (B651 6.2.3 Lavatories)"},
         "Well-lit (any)": {"Well-illuminated (if site expected to be lit)", "Well illuminated (if required for expected usage)"}}
PARTIAL = {  # concept -> why the match is not the register concept (ours)
 "Microwave mounting height accessible and safe": None,
 "Accessible lockers": "PARTIAL: locker rooms (US) and approach space (UK) only; no locker unit rule",
 "Colour temperature (parameter 10)": "DIFFERENT QUANTITY: UK 'colour rendering' only; no colour temperature anywhere",
 "Reverberation time (parameter 7)": "BROADER: reverberation named qualitatively (UK, SG); no reverberation time quantity",
 "volume": "PARTIAL: telephone / ALS volume control, not paging volume",
 "ratio": "MIXED: signal-to-noise ratio (UK, US) is another sense; SG 'proportional basis' is the room-ratio sense",
 "distance": "DIFFERENT SENSE: bollard spacing; no distance markers",
 "Shelter": "PARTIAL: UK weather protection at doors, SG sheltered routes, AU shelter as a building class, US bus shelter",
 "Drainage": "MIXED: AU defines 'drainage' as a plumbing system (different sense); SG/US/IE surface water is the register sense",
 "Colour-contrasted and slip-resistant strip on nosing": "US advisory only; UK contrast without slip; SG and NZ carry both",
 "Seating": "MIXED: rest seating (SG resting areas, US benches) vs audience wheelchair spaces (UK, AU, NZ)",
 "capacity": "PARTIAL: lift capacity (AU pool lift, US via ASME); no paging or room capacity",
}
del PARTIAL["Microwave mounting height accessible and safe"]
ABSENT = {
 "Microwave mounting height accessible and safe": "'microwave' 0 hits in all six texts (US grep across all chapters incl. unread ch8 kitchens)",
 "Speed bumps (B651 8.3.8)": "'speed bump' / 'speed hump' 0 hits in all six texts",
 "Landscaping elements (B651 8.7)": "'landscap' 0 hits in the read parts; exterior realm is out of scope of these building instruments",
 "Flower or shrub planters (B651 8.7.1)": "'planter' 0 hits",
 "Vegetation (B651 8.7.3)": "'vegetation' 0 hits",
 "Guy wires (B651 8.7.4)": "'guy wire' 0 hits",
 "Scaffolding (B651 8.8.2)": "'scaffold' 0 hits; SG 2.3/2.4 temporary obstructions and construction-site footpaths are the nearest (reverse harvest)",
 "Gradation limits (B651 D.6.1)": "trail surface gradation not treated; US ch10 recreation (trails) NOT READ, so absence is scoped to read parts",
}

def check(ins, q, ph):
    return norm(q) in TXT[ins], norm(ph).lower() in norm(q).lower()

def main():
    bad = 0; rows = []
    for c, ph, ins, loc, q, note in OBS:
        okq, okp = check(ins, q, ph)
        if not (okq and okp): bad += 1; print('FAIL', ins, loc, ph, okq, okp, file=sys.stderr)
        rows.append([c, ph, 'en', ins, INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if okq and okp else 'NO', note])
    with open(D + '/observations.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept (register label; | = counts for each)', 'phrase_verbatim', 'language', 'jurisdiction', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'note (ours)'])
        w.writerows(rows)
    rbad = 0
    with open(D + '/reverse-harvest.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['phrase_verbatim (instrument own phrase)', 'kind (ours)', 'language', 'jurisdiction', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'gloss_OURS_not_an_equivalence'])
        for ph, kind, ins, loc, q, g in REV:
            okq, okp = check(ins, q, ph)
            if not (okq and okp): rbad += 1; print('REV FAIL', ins, loc, ph, okq, okp, file=sys.stderr)
            w.writerow([ph, kind, 'en', ins, INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if okq and okp else 'NO', g])
    labels = set()
    for r in rows: labels |= set(r[0].split('|'))
    unknown = labels - set(REGISTER) - set().union(*ALIAS.values())
    if unknown: print('UNMAPPED concept labels:', sorted(unknown), file=sys.stderr); bad += len(unknown)
    srcs = [s for s, n in SRC for _ in range(n)]
    assert len(srcs) == len(REGISTER), (len(srcs), len(REGISTER))
    with open(D + '/coverage.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['register_concept', 'register_source', 'status', 'n_observations'] + [f'{j} (read:{READ[j]})' for j in JUR] + ['phrases_found (distinct, jurisdiction-tagged)', 'note'])
        for c, src in zip(REGISTER, srcs):
            keys = {c} | ALIAS.get(c, set())
            hit = [r for r in rows if keys & set(r[0].split('|'))]
            per = []
            for j in JUR:
                hj = [r for r in hit if r[3] == j]
                per.append(str(len(hj)) if hj else ('ABSENT' if READ[j] == 'full' else 'absent-in-read-parts'))
            if hit:
                st = 'FOUND-PARTIAL' if c in PARTIAL else 'FOUND'
                ph = ' / '.join(sorted({f'{r[1]} [{r[3]}]' for r in hit}))
                w.writerow([c, src, st, len(hit)] + per + [ph, PARTIAL.get(c, '')])
            else:
                w.writerow([c, src, 'SEARCHED-ABSENT', 0] + per + ['', ABSENT.get(c, 'NO NOTE: check')])
    print('observations', len(rows), 'reverse-harvest', len(REV), 'failures', bad + rbad)
    sys.exit(1 if bad + rbad else 0)

if __name__ == '__main__':
    main()
