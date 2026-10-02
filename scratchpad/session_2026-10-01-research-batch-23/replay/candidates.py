import os, subprocess
SCR='/tmp/claude-0/-home-user-guidebook/5b214a57-ade4-5889-9a78-ce2de4360478/scratchpad'
S='session_2026-10-01-research-batch-23'
def run(args):
    r=subprocess.run(['python3','scripts/db.py']+args,env=dict(os.environ,GUIDEBOOK_DB_PATH=SCR+'/batch23.db'),capture_output=True,text=True)
    out=(r.stdout+r.stderr).strip().splitlines()
    print(r.returncode,' | '.join(out[-3:])[:400],flush=True)
C=[
 dict(exec='160',disp='PENDING-VERIFICATION',title='Boverkets föreskrifter om krav på tomter m.m. (BFS 2024:13) — 2 kap. 3 § gångvägar luta högst 1:12',
  loc='https://rinfo.boverket.se/BFS2024-13/pdf/BFS2024-13.pdf',tier='6',harm='0',art='24b5e81b0f4a0928-text.txt',quote='luta högst 1:12',
  why='NOT ADMITTED: a WALKWAY-on-plot rule (gångvägar mellan entréer och målpunkter), not a ramp rule; whether route slope belongs under parameter 3 is GAP-033\'s open scope question. The Boverket page on walkways says the 1:12 applies "oavsett om lutningen är en del av exempelvis en hårdgjord markyta eller om den är utförd som en ramp" -- i.e. Sweden does not distinguish ramp from sloped walkway at this point.',
  notes='HYPOTHESIS (R15): admit as a SE T6 code source with one extraction if GAP-033 resolves route gradient into parameter 3. Retrieved 200, 5 pp., printed 20 Nov 2024, in force 1 July 2025 (2 kap. 3 §: "Gångvägar som avses i 2 § ska ... 3. luta högst 1:12"). Same 1:12 as the building rule admitted as REF-01023.'),
 dict(exec='173',disp='OUT-OF-SCOPE',title='Orden VIV/561/2010, de 1 de febrero — documento técnico de condiciones básicas de accesibilidad en espacios públicos urbanizados (art. 14 Rampas)',
  loc='https://www.boe.es/diario_boe/txt.php?id=BOE-A-2010-4057',tier='6',harm='0',art='ce7c5fdc63f3bb2c-text.txt',
  quote='La pendiente longitudinal máxima será del 10% para tramos de hasta 3 m de longitud y del 8% para tramos de hasta 10 m de longitud.',
  why='NOT ADMITTED: DEROGATED on 2 January 2022 by Orden TMA/851/2021 (BOE analysis block: "Fecha de derogación: 02/01/2022", "SE DEROGA, por Orden TMA/851/2021"). The in-force successor is admitted as REF-01028. Recorded so the repealed order is not re-admitted from a council or vendor page that still cites it.',
  notes='Art. 14.1 b) read 10% to 3 m and 8% to 10 m (the successor keeps the percentages and caps the run at 9 m). It is the root of the figures REF-01029 (CERMI Madrid, Dec 2018) restates.'),
 dict(exec='174',disp='PENDING-VERIFICATION',title='ABCB Standard for Livable Housing Design (2022), Clause 1.1 — step-free access path: gradient and length limits',
  loc='https://abcb.gov.au/editions/ncc-2022/adopted/volume-two/h-class-1-and-10-buildings/part-h8-livable-housing-design',tier='6',harm='0',art='f9b1b4f92ea0ebc2-text.txt',
  quote='Even if Clause 1.1 is not complied with, all other relevant provisions of the ABCB Standard for Livable Housing Design must still be complied with.',
  why='NOT ADMITTED: the NCC 2022 Vol. 2 H8 page retrieved defers the gradient and length limits to Clause 1.1(4) of the separate ABCB Standard, which was not located or retrieved this batch; the page itself uses 1:14 only as an exemption trigger (average ground slope). A web-search summary said the Standard sets 1:14 (1:20 over runs up to 15 m) -- unverified, not used.',
  notes='HYPOTHESIS (R15): the Standard (Livable Housing Design, ABCB 2022) is the AU primary for private dwellings that AS 1428.1 does not cover (lead 88). NCC 2025 currency unchecked. Next: locate the Standard PDF on abcb.gov.au and read Clause 1.1.'),
 dict(exec='155',disp='PENDING-VERIFICATION',title='Gatu- och fastighetskontoret (Stockholm), tjänsteutlåtande 2001-08-02: Förbättrad tillgänglighet till offentliga platser med hjälp av ramper',
  loc='https://insynsverige.se/documentHandler.ashx?did=52240',tier='3',harm='0',art='6ce224bbadd7b205-text.txt',
  quote='våra krav på ramplutningar är 1:20, för att personer på egen hand ska kunna ta sig upp',
  why='NOT ADMITTED: a 2001 municipal officer memo, found by a mismatched search hit (the query sought a 2007-era DPO consultation reply). It states the Stockholm office\'s own requirement as 1:20 "för att personer på egen hand ska kunna ta sig upp" while noting that a 1:20 ramp for a single step is 3 m long and unwieldy in old streets -- a stated trade-off between independence and space.',
  notes='HYPOTHESIS (R15): a Swedish municipal source (sub-national, Bucket-1 country) with the same 1:20 independence warrant as FUB 2007 and the ALM 2 advice. Date, authorship and whether the 1:20 is a binding municipal rule are not established from the 4-page memo; read the attached letter from the handikapprådet chair before any admission.'),
 dict(exec='143',disp='OUT-OF-SCOPE',title='CEN/CLC JTC 11 — Towards common European criteria on accessibility of the built environment: Outcomes of Mandate M/420 (workshop deck, 22 March 2021)',
  loc='https://www.une.org/normalizacion_documentos/PT%20EN%2017210.pdf',tier='4',harm='0',art='a426a8c5ff9b197e-text.txt',
  quote='Vertical circulation (ramps, stairs, handrails, lifts, escalators)',
  why='NOT ADMITTED: 18 slides listing the structure of EN 17210:2021 (chapter 10 "Vertical circulation (ramps, stairs, handrails, lifts, escalators)"); it states no ramp gradient. Its only use is to contradict a web-search summary that placed a ramp clause in chapter 7.',
  notes='EN 17210:2021 itself is paywalled (research_code_leads). The Dutch Bbl nota (REF-01020) says the small-rise ramp tiers come from NEN 9120, the Dutch elaboration of EN 17210.'),
]
for c in C:
    a=['add-candidate','--exec-id',c['exec'],'--found-under-slug','accessible-circulation-geometry','--disposition',c['disp'],'--title',c['title'],'--locator',c['loc'],'--locator-status','RESOLVED','--tier-guess',c['tier'],'--harm-finding',c['harm'],'--why-not-admitted',c['why'],'--notes',c['notes'],'--surfaced-in','retrieval-log/%s/%s'%(S,c['art']),'--session',S]
    if c.get('quote'): a+=['--surfaced-quote',c['quote']]
    print(c['exec'],c['disp'],end=' -> ')
    run(a)
