#!/usr/bin/env python3
"""Batch 20 — GAP-033: adjudicate the observed_terms backlog, one judgement per observation.

Run from the worktree root. Writes to the SCRATCH db only (GUIDEBOOK_DB_PATH).
NAMES-NEW goes through `db.py add-term --from-observation` (mint + adjudicate in one act);
everything else through `db.py adjudicate-term`. New term ids are read from add-term's own
output, never computed here.
"""
import json, os, subprocess, sys

SCRATCH = "/tmp/claude-0/-home-user-guidebook/34e8c762-53ff-5f39-b746-3f5298058fcb/scratchpad/b20.db"
S = "session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa"
ENV = dict(os.environ, GUIDEBOOK_DB_PATH=SCRATCH)


def db(*args):
    r = subprocess.run(["python3", "scripts/db.py", *args, "--session", S],
                       capture_output=True, text=True, env=ENV)
    out = r.stdout.strip()
    if r.returncode != 0:
        print("FAILED:", args[:4], "\n", r.stderr[-1500:], out[-800:])
        sys.exit(1)
    return json.loads(out[out.index("{"):])


# ---- 1. NAMES-NEW: mint first, so NAMES-EXISTING rows can point at them --------------------
MINT = [
    (58, "ramp",
     "An inclined walking or wheeling surface that bridges a level difference on a route, considered as an element.",
     "circulation",
     "Element-level concept: TERM-001 (ramp gradient) is its slope, as TERM-002 (corridor width) is to TERM-048 (circulation route). Subtypes observed in the corpus -- access ramp, curb ramp, step ramp, long ramp, short ramp, hellend vlak, 傾斜路 -- are NARROWER phrases adjudicated to this term, not terms of their own.",
     "NAMES-NEW. The vocabulary holds the ramp's SLOPE (TERM-001) but not the RAMP: eight observations across six sources name the element itself -- a feature that is present or absent (REF-01007's audit item 'Does the health facility have access ramp?'), a class with its own gradient band (step ramp / long ramp, REF-00997), a length class (short ramps, REF-01008), a statutory object (傾斜路, REF-00990). Precedent: TERM-048 circulation route is held beside TERM-002 corridor width. Without an element term every one of those phrases has to be forced onto the gradient or left unlinked. Minted from this observation because its source uses the bare element in English as an audit item."),
    (18, "level difference",
     "The vertical height to be bridged between two floor or ground levels -- the rise a ramp, step or lift must overcome.",
     "circulation",
     "Several sources condition a ramp's permitted gradient on it: Flemish decree Art. 19 bands by niveauverschil (REF-00995), the Australian step-ramp/long-ramp split at a 190 mm rise (REF-00997), REF-01004's ramp height as an independent variable, REF-01008's curb heights of 3, 6 and 9 in. Distinct from TERM-022 (level threshold), which is the zero-step doorway entry that removes a level difference.",
     "NAMES-NEW. 'niveauverschillen' is the variable the Flemish decree conditions its gradient bands on ('tien procent bij niveauverschillen tot 10 cm'), and the same variable carries the permitted gradient in at least three other sources in this corpus under other names (rise, height, curb height). No term holds it, so a gradient stated 'for a rise of X' has nothing to point at for X. The English canonical is a literal gloss of niveauverschil, not a back-translated alias: the alias belongs to this Dutch observation, in its own language."),
    (13, "ramp run length",
     "The horizontal length of a single ramp flight between landings (the UK 'going of a flight').",
     "circulation",
     "Sources condition the permitted gradient on it: Approved Document M Table 1 (REF-00992) by going, REF-01002's 20 ft transit distance, REF-01005 Table 13's maximum horizontal projection of each run, Walter 1971's 10 ft and 20 ft ramps as REF-01008 reports them. The mechanism is stated by REF-00996: effort is sustained longer on a longer run. Distinct from level difference, which is the vertical dimension.",
     "NAMES-NEW. 'going of a flight' is the variable Approved Document M sets its gradient limits against ('Limits for ramp gradients / Going of a flight / Maximum gradient / Maximum rise'), and run length is the single most repeated conditioning variable in this parameter's evidence -- which is why three 1:12s in three jurisdictions are not one figure (the observation's own note). No term holds it. Canonical in plain English rather than the UK term, with 'going' kept as the observed phrase."),
    (19, "intermediate landing",
     "A level platform between successive ramp runs, sized to allow rest, turning or retreat.",
     "circulation",
     "The Flemish memorandum warrants it in user terms: it lets a wheelchair user turn back without completing the whole ramp (REF-00995). It bounds TERM ramp run length from above.",
     "NAMES-NEW. 'tussenbordes' names a design element the vocabulary lacks: the decree requires one of 120 x 150 cm above a 50 cm level difference or a 10 m ramp over 4 percent, and its warrant is the most user-centred rationale any code in this corpus states. It is not TERM-048 (a route) nor the ramp itself. The English canonical is a literal gloss (tussen = between, bordes = landing)."),
    (43, "ramp usability",
     "Whether, and with what effort, difficulty, discomfort or risk, a person can traverse the full length of a ramp -- the outcome a ramp gradient is judged against.",
     "circulation",
     "Outcome-side concept, as TERM-050 (speech intelligibility) is to TERM-007 (reverberation time). Operationalised in this corpus as completion (REF-01005), perceived effort on the Borg scale (REF-01002), perceived discomfort (REF-01004), difficulty ratings (REF-01008) and physiological load; the Flemish handbook names it fysieke haalbaarheid and makes it the starting point of its rule (REF-00996). Measures are adjudicated to this term as operationalisations, not given terms of their own.",
     "NAMES-NEW. REF-00980 asks about 'the usability of the range of ramp slopes allowed under the current ADA accessibility guidelines' -- the property every study on this parameter measures and no term names. Without it the vocabulary has an input (TERM-001) and no outcome, so an effort scale, a completion rate and a feasibility criterion cannot be recognised as measuring the same thing. English canonical from an English T1 title word, not coined."),
    (59, "accessibility audit",
     "A structured on-site assessment of a building or facility against an accessibility checklist or standard.",
     "methodology",
     "A participatory variant (REF-01006) is run by or with disabled people and carries a Co-1 warrant; the method alone does not. An audit measures COMPLIANCE with a yardstick, never what the yardstick should be (REF-01006, REF-01007). Distinct from TERM-060 (post-occupancy evaluation), which assesses a building in use against its intended performance and occupant experience.",
     "NAMES-NEW. This batch's entire cluster is accessibility audits (REF-01006, REF-01007, candidates 123, 126-130), and the corpus has no term for the method -- so the one thing every one of them shares cannot be retrieved as a concept. REF-01007 uses the phrase for exactly this: 'Accessibility audits can be used for monitoring purposes to understand whether facilities are adhering to certain standards'. It is not POE (TERM-060)."),
]

new_ids = {}
for obs, canon, definition, domain, scope, rationale in MINT:
    out = db("add-term", "--from-observation", str(obs), "--canonical-en", canon,
             "--definition", definition, "--domain", domain, "--scope-note", scope,
             "--rationale", rationale)
    new_ids[canon] = out["term_id"]
    print(f"obs {obs:>2} NAMES-NEW  {out['term_id']} {canon!r}")

RAMP, LEVEL, RUN, LANDING, USAB, AUDIT = (new_ids[k] for k in (
    "ramp", "level difference", "ramp run length", "intermediate landing",
    "ramp usability", "accessibility audit"))

# ---- 2. Everything else --------------------------------------------------------------------
E, D, N = "NAMES-EXISTING", "DEFERRED", "NOT-OURS"
ROUTE = ("the ramp-versus-route boundary is unresolved in this corpus: TERM-001 is defined as the slope of a RAMP, "
         "this source measures the running slope of outdoor PATHS or trails, and no term holds route gradient. "
         "Extraction 49 already files REF-01003's path slopes on parameter 3 (ramp gradient), so the same "
         "conflation is live in the evidence. Adjudicating this phrase onto TERM-001 would ratify it; minting "
         "a route-gradient term would imply extraction 49 is mis-filed. That is a judgment about the parameter's "
         "scope, not about this phrase, and it is left for the batch that re-determines parameter 3.")
ACT = ("it names an ACTIVITY (a wheelchair task on a slope), not a design parameter or element. CLAUDE.md "
       "section 6 sends activities to the ICF lens (base_icf d4 mobility codes), and the vocabulary's only "
       "activity-shaped terms are the functional-axis rows TERM-031..047, a coinage the owner ruled bad on "
       "2026-08-18. Whether task phrases get term rows or ICF links is undecided; forcing either here would "
       "decide it by accident.")
RULE5 = ("the concept IS held, but as a column vocabulary rather than a term (rule 5: one home). Minting a term "
         "for it would create a second home; adjudicating NOT-OURS would say it is not a concept of ours, which "
         "is false. Deferred until the term-versus-column placement is decided for held vocabularies.")

ROWS = [
    (1, E, "TERM-001", "'ramp slope' in 'greater power and pushrim force on steeper ramp slopes' is the slope of a ramp, which is TERM-001's definition word for word. The setting is a transit bus boarding ramp, recorded on the source's extractions; the concept is the same."),
    (2, D, None, "'ascending slopes' is a skill item in a wheelchair skills test ('negotiating kerbs, ascending slopes, traversing tracks'): " + ACT),
    (3, D, None, "'slope propulsions' names propelling a wheelchair on slopes as the unit of exposure for musculoskeletal risk: " + ACT),
    (4, E, "TERM-001", "'inclines' in 'propulsion at different speeds and inclines, ascending and descending ramps' is the inclination of the ramps being ascended -- the ramp's slope. TERM-001."),
    (5, E, "TERM-001", "'running slope' in 'Ramp runs shall have a running slope not steeper than 1:12' (ADA 405.2) is the slope of a ramp run in the direction of travel. TERM-001; 'running' distinguishes it from cross slope, which is not this parameter."),
    (6, D, None, "自走 ('self-propelling', in 'depending on the gradient you may not be able to go by self-propulsion') names the propulsion mode, which the schema holds as source_value_extractions.device_class = 'manual_self_propelled': " + RULE5),
    (7, E, "TERM-001", "勾配 is defined by the source itself -- 勾配とは、斜面の程度のことをいいます, 'gradient means the degree of a slope' -- under the heading on the legal スロープの勾配基準 (ramp gradient standard, 1/12). It names the slope of a ramp. TERM-001."),
    (8, E, "TERM-001", "'Neigung' in 'Rampenläufe dürfen maximal eine Neigung von 6 % aufweisen' is the inclination of a ramp run. TERM-001, stated as a percentage."),
    (9, E, RAMP, "傾斜路 is the Japanese statutory term for a ramp as an element ('傾斜路 ... used by unspecified and many persons or mainly by the elderly and disabled'). It names the ramp, not its slope, so it points at the element term minted this batch rather than TERM-001."),
    (10, D, None, "移動等円滑化経路 names a legally DESIGNATED accessible route, the route the 1:12 ceiling attaches to (the observation's own note). TERM-048 (circulation route) is the nearest and is broader and defined as horizontal movement through a building, which this route is not. An 'accessible route' term is probably warranted, but minting its English name from a Japanese statute would be back-translation (R11); it should be minted from an English-language source that uses the phrase itself."),
    (11, D, None, "敷地内の通路 ('path within the site') names an external site path that carries its own ramp provisions. TERM-048 is scoped to routes THROUGH A BUILDING, so it does not fit, and the vocabulary has no site-route term. Whether site and building routes are one concept or two is a scoping decision for the circulation vocabulary, not one this phrase can settle."),
    (12, N, None, "誘導すべき建築物特定施設 names Japan's GUIDED (誘導) standard, which buildings are steered toward rather than held to. The distinction it draws -- guidance versus mandatory -- is carried in this project by the tier ladder (T5 national_fw versus T6 code), not by the concept vocabulary; TERM-075 is defined as BINDING requirements, so it would be wrong here. Not a term concept; the observation's substance is already represented by how the source is tiered."),
    (13, "minted", None, None),
    (14, E, "TERM-075", "義務基準 ('mandatory standard') is binding accessibility requirements, TERM-075's definition. The DPO uses it pejoratively -- the mandatory standard alone does not make smooth use possible -- which is exactly TERM-075's scope note: the regulatory floor is not evidence of adequacy."),
    (15, N, None, "'min. grade best practice' is a SPEECH ACT the IPC performs on its 1:20 figure (best practice rather than maximum). 'Best practice' is a determination-level category in this project (tier-system section 8, 'best practice as currently known'), carried by extraction figure_role and comparator, not a concept the vocabulary names. Recording it as a term would put a determination label in the vocabulary."),
    (16, N, None, "'secondary or ancillary facilities' is the IPC's facility-importance scope for its relaxed 1:14 figure. It is a condition on one guide's figure, held in that extraction's setting, not a concept the vocabulary needs; minting a facility-importance classification on a single guide's wording would be thin warrant."),
    (17, E, "TERM-001", "'hellingspercentage' is the gradient of a helling (ramp) expressed as a percentage ('Het hellingspercentage bedraagt hoogstens ...'). TERM-001; the observation's point about ratio-versus-percentage notation is a unit fact the extractions carry in claimed_unit, not a second concept."),
    (18, "minted", None, None),
    (19, "minted", None, None),
    (20, E, USAB, "'fysieke haalbaarheid' ('physical feasibility' of the independent wheelchair user) is the Flemish handbook's name for whether a user can manage the whole ramp -- the outcome the gradient is judged against, which the handbook makes the starting point of its rule. That is the ramp usability term minted this batch, whose scope note names this phrase."),
    (21, E, "TERM-016", "'zelfstandige rolstoelgebruiker' is a wheelchair user, TERM-016, narrowed by the source's own parenthesis to the INDEPENDENT (self-propelling) user as the design case. The narrowing is real and is carried on extractions as device_class manual_self_propelled; the concept named is TERM-016."),
    (22, N, None, "'uitgangspunt' ('starting point') is a discourse word marking the speech act -- feasibility is what the rule is derived FROM. The substance is carried by observation 20's adjudication to ramp usability; the word itself names no concept."),
    (23, E, RAMP, "'hellend vlak' is, in the source's own words, what a SHORT helling is often called ('Een korte helling wordt vaak hellend vlak genoemd') -- a short ramp permitted a steeper percentage. A narrower phrase for the ramp element, adjudicated to it; its length condition is what ramp run length holds."),
    (24, E, RAMP, "'step ramp' is a ramp class defined by rise (<190 mm) and given its own gradient band (1:8). It names the element, narrowed by level difference; adjudicated to the ramp element term rather than minted separately, per that term's scope note."),
    (25, E, RAMP, "'long ramp' is the complement of 'step ramp' (rise >190 mm, 1:14). Same element, same adjudication; the rise that divides the two classes is level difference."),
    (26, N, None, "'prescriber' names a clinical ROLE -- the actor the document assigns the gradient decision to, with authority to depart from AS 1428.1 on documented reasoning. Not a built-environment concept. What it raises for Co-2 (clinical authority over a design parameter) is recorded in the observation's notes and belongs in a Co-2 reading, not the vocabulary."),
    (27, N, None, "'Class 1 and 2 buildings' is the Australian National Construction Code's building classification. It decides whether AS 1428.1 applies, which is load-bearing for the question, but it is a jurisdiction's legal category, not a concept of ours; its effect is recorded where the source's applicability claim is extracted."),
    (28, D, None, "'Livable Housing Design Standard' is a named instrument. Named instruments are narrower aliases of a concept (TERM-064's scope note), but which concept depends on the level applied: a minimum dwelling-access level is TERM-059 (visitability), a full-use level is TERM-068 (accessible housing). The observed context ('Livable Housing Guidelines are advisory') does not say which level, so it cannot be adjudicated on this source."),
    (29, D, None, "'private dwellings' names a SETTING. The vocabulary holds housing only as standards of a dwelling (TERM-059 visitability, TERM-068 accessible housing), not the dwelling as a setting; TERM-070 (school learning environment) shows setting terms exist, so a dwelling setting term is a reasonable mint -- but one FAQ answer is thin warrant, and the housing slug is where it should be decided."),
    (30, N, None, "'disabled-by-design' is a title-level framing claim about causation (design disables users of mobility devices). It is a thesis the review argues, not a design concept the vocabulary names; its substance is the review's findings, which are extracted."),
    (31, N, None, "'factor of disablement' is the same causal framing as observation 30, stated in the conclusions. Not a vocabulary concept, for the same reason."),
    (32, E, "TERM-079", "'mobility assistive devices' (the review's MobAD) are devices supporting locomotion, TERM-079 (mobility aid). TERM-079's scope note keeps the device distinct from the person (TERM-016), and the phrase names the device."),
    (33, N, None, "'least accessible elements' is a ranking phrase ('were deemed to be the least accessible elements'), not a concept. The elements it ranks (pathways, boarding ramps, entrances) are named separately."),
    (34, D, None, "'ramp incident' names an ADVERSE EVENT on a ramp (78 percent of wheelchair users had one in three years). The corpus records harm as harm_finding flags and case studies and has no adverse-event vocabulary; whether event types (ramp incident, fall, tip-over) warrant terms is a vocabulary question the stair slug will raise too (candidate 117, rehomed this batch, is a stair-accident study). Deferred rather than decided on one source."),
    (35, E, "TERM-001", "'steep ramp slope' is TERM-001 with an evaluative qualifier: over 60 percent of those with an incident named steep ramp slope as the contributing factor. The concept is the slope; 'steep' is the source's judgment of it."),
    (36, D, None, "'exterior ramp thresholds' names the transition where a (bus) ramp meets the ground or kerb -- a lip or level change at the ramp's end. TERM-022 (level threshold) is a zero-step DOORWAY entry, a different place and function. REF-01008's lip findings (a 1 in lip made an acceptable ramp unacceptable) bear on the same concept. It likely warrants a term, but this abstract fragment ('Steep ramp slope, exterior ramp thresholds and') does not define it; mint from a source that does."),
    (37, N, None, "'coping mechanisms' names users' STRATEGIES for propelling up a ramp -- a behavioural finding about people, not a design concept. Its content belongs in the source's qualitative findings."),
    (38, N, None, "'solutions' is a generic word the source puts in scare quotes ('proposed solutions to accessibility, such as ramps, often generate problems of their own'). It names nothing; the claim it carries is a finding, and ramps as an element are the ramp term."),
    (39, N, None, "'tipping point' names a THRESHOLD VALUE on the gradient scale (5.50 percent, after which all respondents felt uncertainty). A threshold is the output of a determination, not a vocabulary concept, and a term that named one would be the value-bearing container add-term refuses. The underlying outcome (uncertainty) is ramp usability; the phrase itself is a value."),
    (40, D, None, "'critical longitudinal slopes' are threshold slopes on forest and park TRAILS: " + ROUTE),
    (41, D, None, "'complex independent movement with certain risk' is a graded usability category, which would otherwise go to ramp usability -- but it grades movement on TRAILS: " + ROUTE),
    (42, E, "TERM-001", "'ramp slope' in 'the usability of the range of ramp slopes allowed under the current ADA accessibility guidelines' is TERM-001 exactly."),
    (43, "minted", None, None),
    (44, E, "TERM-001", "'ramps of different slopes' names the independent variable of a kinematic study -- the ramp's slope. TERM-001."),
    (45, E, "TERM-001", "'running slope' in 'requirements for ramp design, including their maximum running slope and cross slope' is the slope of a RAMP along the direction of travel. TERM-001; cross slope is a different parameter."),
    (46, E, USAB, "'perceived effort' (Borg scale) is the measure REF-01002 uses for how hard wheelchair users find it to negotiate ramps. It operationalises ramp usability, and the term's scope note records Borg-scale perceived effort as one of its measures; measures are adjudicated to the outcome they measure rather than given terms of their own."),
    (47, D, None, "'running slope' here is the running slope of OUTDOOR PATHWAYS ('proposed accessibility guidelines for running slope and cross slope'), not of a ramp: " + ROUTE),
    (48, D, None, "'perceived difficulty' would be a ramp-usability measure, but these are ratings of OUTDOOR PATHWAYS: " + ROUTE),
    (49, E, "TERM-001", "'ramp slope and height' names two independent variables. The slope half is TERM-001 and is what this source's extractions on parameter 3 concern; the height half is the rise, now level difference. One observation takes one outcome, so this row records TERM-001 and names the second concept here rather than writing a second row that would read as a contest."),
    (50, E, USAB, "'perceived discomfort while ascending and descending' ramps is a measure of ramp usability, named in that term's scope note. Adjudicated to it as an operationalisation."),
    (51, E, "TERM-001", "'running slope', located at REF-01005's ramp objectives ('the maximum slopes that can be managed'), is the slope of a ramp -- the 1979 study's whole ramp experiment varies it. TERM-001."),
    (52, D, None, "'marginal population' names the SUBGROUP at the edge of capability whose needs set the design case ('steeper slopes present problems to subgroups within the total wheelchair population'). This project's equivalent is the most-accommodating rule (owner directive 2026-07-21) -- a DOCTRINE, not a term -- and minting a term for it would put a doctrinal commitment into the vocabulary by the back door. Deferred to the owner, whose rule it is."),
    (53, E, "TERM-053", "'limitations of stamina' is reduced capacity for sustained activity, TERM-053's definition. The source uses it as a GROUP label ('People with limitations of stamina ... may have difficulty with ramps steeper than 1:20'); TERM-053's scope note forbids it as a population umbrella, so this adjudication names the mechanism, not a population."),
    (54, D, None, "'walking and reaching limitations' names TWO functional limitations. The only terms for them are the functional-axis rows TERM-031 (Ambulant movement) and TERM-041 (Reach & manipulation), and the owner ruled 'axes' a bad coined term on 2026-08-18; adjudicating onto them would harden a vocabulary the owner has criticised. The ICF lens is the ruled frame for functional limitation (CLAUDE.md section 6)."),
    (55, E, AUDIT, "'participatory accessibility audit' is the accessibility audit method, run in partnership and -- in this source -- by field investigators who were all persons with disabilities. The accessibility audit term minted this batch names the method and its scope note records the participatory variant as the one that carries a Co-1 warrant."),
    (56, D, None, "'Community Based Participatory Research' names the co-production methodology behind REF-01006's Co-1 warrant, which the schema holds as evidence_sources.co1_source_type = 'participatory_research': " + RULE5),
    (57, D, None, "'universal accessibility' appears only as part of a standard's title ('Harmonised Guidelines and Standards for Universal Accessibility in India (2021)'). Whether it means TERM-017 (universal design, usable by all without adaptation) or accessibility for persons with disabilities -- this project's own reading of 'universal' (CLAUDE.md section 9) -- cannot be settled from a title."),
    (58, "minted", None, None),
    (59, "minted", None, None),
    (60, N, None, "'external accessibility' is the label of one sub-scale of a 22-item questionnaire (eight items: sidewalk, floors, ramp, handrail, door). An instrument's grouping of its items, not a concept; the items it groups are named separately."),
    (61, E, RAMP, "'curb ramp' is the object REF-01008 tested -- a short ramp through a curb. A narrower phrase for the ramp element (its level difference is the curb height, its run length 2-10 ft); adjudicated to the element rather than minted, per that term's scope note."),
    (62, N, None, "'handicapped pedestrians' is the period's UMBRELLA population label (1974-1980). It names no concept of ours: the doctrine forbids population umbrellas, and the groups the report actually sampled -- manual and electric wheelchair users, cane and crutch users, people with prosthetic limbs, elderly people -- are what the identity lens holds. The context sentence the observation carries uses 'handicapped people'; the source's own 'handicapped pedestrians' occurs in its acceptability discussion ('hazardous, for handicapped pedestrians, when they must use the ramp to enter or leave a street')."),
    (63, E, RAMP, "'short ramps' is the ramp element qualified by length -- the class REF-01008's recommendations are scoped to. Adjudicated to the ramp element; the length condition is ramp run length."),
]

counts = {}
for obs, outcome, term, rationale in ROWS:
    if outcome == "minted":
        counts["NAMES-NEW"] = counts.get("NAMES-NEW", 0) + 1
        continue
    args = ["adjudicate-term", "--observation-id", str(obs), "--outcome", outcome,
            "--rationale", rationale]
    if term:
        args += ["--term-id", term]
    out = db(*args)
    counts[outcome] = counts.get(outcome, 0) + 1
    print(f"obs {obs:>2} {outcome:<15} {term or ''}")
print("COUNTS (this run, derive the live totals from term_adjudications):", counts)
