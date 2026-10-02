import os, subprocess, sys, json
sys.path.insert(0,'scripts/research')
import retrieval_log as rl
SCR='/tmp/claude-0/-home-user-guidebook/5b214a57-ade4-5889-9a78-ce2de4360478/scratchpad'
S='session_2026-10-01-research-batch-23'
SLUG='accessible-circulation-geometry'
def run(args,show=True):
    r=subprocess.run(['python3','scripts/db.py']+args,env=dict(os.environ,GUIDEBOOK_DB_PATH=SCR+'/batch23.db'),capture_output=True,text=True)
    o=(r.stdout+r.stderr).strip().splitlines()
    if show: print('  ',args[0],'->',r.returncode,' | '.join(o[-3:])[:230],flush=True)
    return r
# ---------------- REF-01022 as T3 grey
run(['add-source','--ref-id','REF-01022','--author','corp|Ieder(in)','--year','2023',
 '--title','Internetconsultatie verzamelbesluit Bbl 2024 (reactie van Ieder(in), 9 november 2023, ref. 23-0915/AvdV/SvK)',
 '--tier','3','--evidence-type','grey','--jurisdiction','NL','--source-type','letter','--grey-flag','1',
 '--grey-reason',"consultation reply (internetconsultatie reactie) by a national umbrella organisation, dated 9 November 2023 and signed by its director; not peer-reviewed; no DOI. CO-1-ADJACENT AND NOT CLAIMED AS CO-1 (D-0178): the letter calls its author 'het netwerk van mensen met een beperking of chronische ziekte', but its governance (who controls the network) was not retrieved -- iederin.nl pages answered with a bot-challenge stub (HTTP 202) -- and no individual disabled author or consulted member is named.",
 '--url','https://internetconsultatie.nl/verzamelbesluit_bouwwerken_leefomgeving_2024/reactie/237535/bestand','--url-accessed','2026-10-01',
 '--pages','p. 1 (bullet 3, hellingbanen / NEN 9120)','--metadata-quality','GREY','--verification-status','VERIFIED','--verification-method','direct-render',
 '--lang-detected','nl','--lang-detection-method','native_title_verified','--slug',SLUG,'--local-ref-id','NL-03','--session',S])
run(['add-extraction','--ref-id','REF-01022','--slug',SLUG,'--parameter-id','3','--identity','MOB','--claim-type','qualitative',
 '--claimed-value','supports adjusting the ramp (hellingbaan) requirements to align with draft NEN 9120; hopes other parts of the regulation follow once the standard is finished',
 '--claim-text','De eisen voor hellingbanen worden aangepast zodat ze in lijn zijn met de NEN- norm 9120 die in ontwikkeling is. Ieder(in) ondersteunt de implementatie van deze NEN-norm',
 '--source-section','Letter p. 1, third bullet','--jurisdiction','NL','--extraction-method','full-read','--extraction-status','preliminary','--root-type','committee_assertion','--root-ref-id','REF-01022',
 '--measurement-paradigm','stated_unmeasured','--device-class','not_device_scoped','--figure-role','finding','--relation','none',
 '--root-population-note',"Ieder(in) describes itself in the retrieved letter as 'het netwerk van mensen met een beperking of chronische ziekte' -- people with any disability or chronic illness, not wheelchair users in particular. No individual authors or consulted members are named; the letter is signed by the director.",
 '--notes',"A NATIONAL DISABILITY NETWORK'S ENDORSEMENT WITHOUT A FIGURE, FILED AS A FINDING (it asserts no value): the letter states no gradient and voices no criticism of the Bbl tiers. It is evidence that the network was consulted on, and supported, the ramp tiers Stb. 2024/368 (REF-01020) took from NEN 9120; it is NOT evidence that those tiers are acceptable to wheelchair users in use (contrast REF-01025, FUB 2007, which calls 1:12 a safety risk). RE-FILED after the adversarial pass (F1) as T3 grey with the same wording: Co-1 is not claimed because co-production is not evidenced in the retrieved bytes. Dated 9 November 2023, before the amendment was made (25 November 2024).",
 '--locator-scheme','section','--loc-section','Letter p. 1','--loc-paragraph','bullet 3','--session',S])
run(['observe-term','--ref-id','REF-01022','--surface-form','hellingbanen','--language','NL','--locator','Letter p. 1, third bullet','--context-quote','De eisen voor hellingbanen worden aangepast zodat ze in lijn zijn met de NEN- norm 9120 die in ontwikkeling is.','--session',S])
run(['add-population-match','--ref-id','REF-01022','--target-population','MOB','--study-population','no participants; the position of Ieder(in), a national network of people with any disability or chronic illness, stated in a consultation letter','--match-grade','PARTIAL','--mismatch-note',"The author body speaks for people with any disability or chronic illness, which includes mobility-device users but is not specific to them; no sample, no members named, a position and not a measurement. PARTIAL for MOB, not EXACT.",'--session',S])
run(['log-mining','--slug',SLUG,'--ref','REF-01022','--direction','backward','--notes',"Pass RAN by reading the letter in full (2 pp.). It cites no source, bibliography or figure. Its only external referents are the Verzamelbesluit Bbl 2024 (retrieved this batch as Stb. 2024, 368 = REF-01020) and NEN 9120 (a draft Dutch standard, the national elaboration of EN 17210; paywalled and filed as a research_code_leads row). Nothing further to chase.",'--session',S])
# ---------------- REF-01024 as T5 national_fw
run(['add-source','--ref-id','REF-01024','--author','corp|Boverket','--year','2011',
 '--title','Boverkets föreskrifter och allmänna råd om tillgänglighet och användbarhet för personer med nedsatt rörelse- eller orienteringsförmåga på allmänna platser och inom områden för andra anläggningar än byggnader',
 '--series','Boverkets författningssamling','--series-number','BFS 2011:5 (ALM 2)',
 '--tier','5','--evidence-type','national_fw','--jurisdiction','SE','--source-type','guideline',
 '--url','https://www.varberg.se/download/18.2b514d9b18a92e6fafc230fb/1387272663974/BFS2011-5-ALM2.pdf','--url-accessed','2026-10-01',
 '--pages','8 § och 9 § Allmänt råd (PDF p. 4 of 8)','--metadata-quality','COMPLETE-STATUTORY','--verification-status','VERIFIED','--verification-method','direct-render',
 '--lang-detected','sv','--lang-detection-method','native_title_verified','--slug',SLUG,'--local-ref-id','SE-02','--session',S])
common=" Currency: Boverket's own PBL-kunskapsbanken page on accessibility on public places, retrieved this session (artefact 54cbad3421ee4f37.html), names BFS 2011:5 - ALM 2 as the applicable regulation. Year: title page 'Utkom från trycket den 26 april 2011'. FILED T5 national_fw, NOT T6 code (adversarial finding F2): the instrument mixes binding föreskrifter and non-binding allmänna råd, and BOTH figures extracted from it are allmänna råd; governance/tier-system.md line 21 names 'Boverket BBR advisories' as the T5 worked example. The binding föreskrift beside the 1:20 advice (9 §, first paragraph) states no gradient."
for (text,cv,unit,sect,notes,scheme) in [
 ('En ramp bör a) luta högst 1:20 mellan minst 2 meter långa vilplan, b) ha en höjdskillnad på högst 0,5 meter mellan vilplanen','1:20','rise:run ratio (advised maximum between landings at least 2 m long; at most 0.5 m rise between landings)','BFS 2011:5 ALM 2, 9 §, Allmänt råd (PDF p. 4)',"GENERAL ADVICE (allmänt råd), NOT A BINDING FÖRESKRIFT: 'bör' (should). Scope: public places and areas for facilities other than buildings (ALM 2, 1 §)."+common,dict(section='9 §',subsection='Allmänt råd',paragraph='a')),
 ('En utjämning till 0-nivå bör inte ha större lutning än 1:12. Bredden bör vara 90–100 cm.','1:12','rise:run ratio (advised maximum for an utjämning till 0-nivå, a kerb-type levelling ramp at crossings and similar places)','BFS 2011:5 ALM 2, 8 §, Allmänt råd (PDF p. 4)',"GENERAL ADVICE ('bör'); the element is a dropped-kerb type ramp (utjämning till 0-nivå) between walking surfaces, not a ramp of travel, hence setting 'kerb ramp'."+common,dict(section='8 §',subsection='Allmänt råd'))]:
    cmd=['add-extraction','--ref-id','REF-01024','--slug',SLUG,'--parameter-id','3','--identity','MOB','--claim-type','numerical','--claimed-value',cv,'--claimed-unit',unit,'--claim-text',text,'--source-section',sect,'--jurisdiction','SE','--extraction-method','full-read','--extraction-status','preliminary','--root-type','committee_assertion','--root-ref-id','REF-01024','--measurement-paradigm','stated_unmeasured','--device-class','not_device_scoped','--figure-role','claim','--comparator','<=','--relation','none','--notes',notes,'--locator-scheme','section','--loc-section',scheme['section'],'--loc-subsection',scheme['subsection'],'--session',S]
    if 'paragraph' in scheme: cmd+=['--loc-paragraph',scheme['paragraph']]
    if '0-nivå' in text: cmd+=['--setting','kerb ramp (utjämning till 0-nivå)']
    run(cmd)
run(['observe-term','--ref-id','REF-01024','--surface-form','utjämning till 0-nivå','--language','SV','--locator','8 §, Allmänt råd','--context-quote','En utjämning till 0-nivå bör inte ha större lutning än 1:12.','--session',S])
run(['add-population-match','--ref-id','REF-01024','--target-population','MOB','--study-population','no participants; regulation with general advice (Boverket BFS 2011:5 ALM 2)','--match-grade','PROXY','--mismatch-note',"PROXY by construction: a regulatory or advisory text asserts a figure; it does not study a population, so there is no population-of-study to compare against mobility-device users. Same grading as REF-00987 (ADA), REF-00994 (IPC) and REF-00995 (Flemish decree). The 2026-09-25 owner ruling on PARTIAL applies to a facility AUDIT's measured sample and does not transfer (batch 22 finding 0e).",'--session',S])
# ---------------- new execs carrying the re-filed admission edges
man=[json.loads(l) for l in open(f'retrieval-log/{S}/manifest.jsonl')]
def art(u):
    ok=[m for m in man if m['url']==u and m.get('status') and 200<=m['status']<300 and m['bytes']>0 and not m.get('derived')]
    return ok[-1]['artefact']
for url,lang,juris,tt,ref,tier,prior,note in [
 ('https://internetconsultatie.nl/verzamelbesluit_bouwwerken_leefomgeving_2024/reactie/237535/bestand','NL','NL','co1','REF-01022',None,
  'Re-recording of the admission edge for REF-01022 after the adversarial pass (F1); the retrieval itself is the one logged on the earlier exec for this URL. Prior: as on that exec -- expect the Ieder(in) reply to endorse or criticise the revised ramp requirements (a follow-up prior composed at logging time, after the first retrieval).',
  "RE-FILING EXEC (adversarial-pass repair F1). Same retrieval as the earlier exec for this URL (200, 75 kB, 2 pp.; Ieder(in) letter of 9 November 2023): supports aligning the Bbl ramp requirements with NEN 9120 in development; states no figure. The first admission (T1 co1, REF-01022) was WITHDRAWN before capture and the source re-filed under the same ref_id as T3 grey: the Co-1 warrant is not evidenced in the retrieved bytes (D-0178), and the governance pages on iederin.nl returned bot-challenge stubs (HTTP 202, artefacts a836bdbc7ef3655e.html and f09f27d41341ea64.html). Admitted as REF-01022."),
 ('https://www.varberg.se/download/18.2b514d9b18a92e6fafc230fb/1387272663974/BFS2011-5-ALM2.pdf','SV','SE','code','REF-01024',None,
  'Re-recording of the admission edge for REF-01024 after the adversarial pass (F2); the retrieval is the one logged on the earlier exec for this URL. Prior: as on that exec (a follow-up prior composed at logging time, after the first retrieval).',
  "RE-FILING EXEC (adversarial-pass repair F2). Same retrieval as the earlier exec for this URL (200, 48 kB, 8 pp., 'Utkom från trycket den 26 april 2011'). 9 § Allmänt råd: 'En ramp bör luta högst 1:20 mellan minst 2 meter långa vilplan'; 8 § Allmänt råd: kerb-type levelling 1:12. The first admission (T6 code) was WITHDRAWN before capture and re-filed under the same ref_id as T5 national_fw because both figures are non-binding advice. Admitted as REF-01024.")]:
    cmd=['log-search','--slug',SLUG,'--language',lang,'--query-text',url,'--engine','web','--depth-method','scoping','--jurisdiction',juris,'--target-evidence-type','co1' if ref=='REF-01022' else 'national_fw','--prior-expectation',prior,'--results-found','1','--results-screened','1','--results-admitted','1','--admitted-ref-id',ref,'--saturation-signal','saturated','--harm-finding','0','--findings-note',note,'--origin','planned','--result-artefact','retrieval-log/%s/%s'%(S,art(url)),'--session',S]
    if ref=='REF-01022': cmd+=['--target-tier','1']
    run(cmd)
