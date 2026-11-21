"""Build the proposed identity x access-need x ICF triples (T-145 research batch).

Reads data/guidebook.db read-only and governance/functional-taxonomy.md; writes triples.json (one object per triple,
with the assembled warrant) and prints a preview. Writes NOTHING to the database.

What is judged (this file's PAIRS) and what is derived (everything else):
  judged   -- which identity a need serves, why, and which ICF codes carry it
  derived  -- every quotation (must be a substring of the live record), every support fact (identity_icf_map link
              ids, access_need_icf rows), and every taxonomy anchor (parsed from governance/functional-taxonomy.md 2.1)
A code that neither map supports must name an axis whose anchors list it, and must carry its own reason; the script
refuses otherwise. A quotation that is not found in the live record is refused. Re-run after any change to the maps.
"""
import json, re, sqlite3, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SESSION = "session_2026-11-21-identity-need-icf-triples"
OUT = pathlib.Path(__file__).with_name("triples.json")

# kind: E1 = the identity's own description names the need; E2 = the need's registry text names the identity's
# condition; M = the two maps already meet on a code (the identity's map and the need's absorbs/maps);
# E3 = a judgment with a link the project's records do not state (named as such in the reason).
# codes: (code, axis_or_None, reason_or_None). axis/reason only where neither map holds the code.
PAIRS = [
 # ---- perceiving
 dict(i="BLIND", n="A-NOSIGHT", kind="E2", qn="blindness, low vision", qi="blind and low-vision people",
      why="the need's registry text names blindness and low vision and the identity is blind and low-vision people",
      codes=[("b210", "AX-VIS-N", "the seeing-function anchor of the two vision axes, the function the need substitutes for"),
             ("d460", None, None), ("d310–d329", None, None), ("e240", None, None), ("e125", None, None),
             ("e150", None, None), ("e155", None, None)]),
 dict(i="DEAF", n="A-NOSOUND", kind="E2", qn="Deaf, hard of hearing, late-deafened", qi="Deaf, or late-deafened",
      why="the need's registry text names Deaf, hard-of-hearing and late-deafened people",
      codes=[("b230", "AX-AUD", "the hearing-function anchor of the auditory axis, the function the need substitutes for"),
             ("d310–d329", None, None), ("d330–d349", None, None), ("e250", None, None), ("e1251", None, None),
             ("e125", None, None)]),
 dict(i="DEAFBLIND", n="A-TACTILE", kind="E1", qn="DeafBlind (Protactile)", qi="centring touch",
      why="the need's registry text names DeafBlind (Protactile) access and the identity's description centres touch; both records say DeafBlind access is distinct from blind plus Deaf, so no vision or hearing code is proposed",
      codes=[("e340", None, None), ("e150", None, None), ("e155", None, None)]),
 dict(i="VES", n="A-STABLE", kind="E1", qn="vestibular disorders", qi="Served primarily by A-STABLE",
      why="the identity's description says it is served primarily by this need and the need's registry text names vestibular disorders",
      codes=[("b235", "AX-BAL", "the vestibular-function anchor of the balance axis, which the axis table says includes environments that precipitate dizziness"),
             ("d415", "AX-BAL", "an anchor of the balance axis (posture under visual and motion destabilisation)"),
             ("e150", None, None), ("e240", None, None)]),
 dict(i="BRAIN", n="A-STABLE", kind="E2", qn="post-concussion", qi="post-concussion",
      why="the need's registry text names post-concussion and the identity's description includes post-concussion",
      codes=[("e150", None, None), ("e240", None, None)]),
 # ---- communicating
 dict(i="BRAIN", n="A-NOSPEECH", kind="E3", qn="aphasia", qi="stroke",
      why="the need's registry text names aphasia and the identity's description includes stroke; that aphasia follows stroke is general medical knowledge that no project record states, so this pair is an inference for the owner to confirm",
      codes=[("d330", "AX-COM-E", "an anchor of the expressive-communication axis (producing speech)"),
             ("d350", "AX-COM-E", "an anchor of the expressive-communication axis (conversation)"),
             ("e125", None, None), ("e340", None, None)]),
 dict(i="ID", n="A-PLAIN", kind="E2", qn="intellectual disability", qi="First-class",
      why="the need's registry text names intellectual disability and the identity is people with intellectual disability",
      codes=[("b117", "AX-COG-L", "an anchor of the information-access axis (comprehension load)"),
             ("d166", "AX-COG-L", "an anchor of the information-access axis (reading signage and instructions)"),
             ("e150", None, None), ("e155", None, None)]),
 dict(i="DEM", n="A-PLAIN", kind="E2", qn="dementia", qi="Alzheimer disease and related dementias",
      why="the need's registry text names dementia and the identity is people living with dementia",
      codes=[("b117", "AX-COG-L", "an anchor of the information-access axis (comprehension load)"),
             ("d460", None, None), ("e150", None, None), ("e155", None, None)]),
 dict(i="BRAIN", n="A-PLAIN", kind="E2", qn="brain injury", qi="acquired brain injury",
      why="the need's registry text names brain injury and the identity is people with acquired brain injury",
      codes=[("b117", "AX-COG-L", "an anchor of the information-access axis (comprehension load)"),
             ("d460", None, None), ("e150", None, None), ("e155", None, None)]),
 # ---- operating
 dict(i="MOB", n="A-REACH", kind="E2", qn="wheelchair users", qi="wheelchair users",
      why="the need's registry text names wheelchair users, ambulatory wheelchair users and cane/crutch users, and the identity is people with mobility needs including wheelchair users",
      codes=[("d465", None, None), ("d420", None, None), ("d450", None, None), ("e120", None, None),
             ("e150", None, None), ("e155", None, None)]),
 dict(i="LMB", n="A-REACH", kind="E2", qn="limb difference", qi="limb differences",
      why="the need's registry text names limb difference and the identity is people with limb differences",
      codes=[("d440", None, None), ("d445", None, None), ("e120", None, None), ("e150", None, None), ("e155", None, None)]),
 dict(i="MOVE", n="A-PRECISION", kind="E1", qn="tremor, dystonia, Parkinson's", qi="Pairs with A-PRECISION",
      why="the identity's description says it pairs with this need and the need's registry text names tremor, dystonia and Parkinson's",
      codes=[("b765", None, None), ("e115", None, None),
             ("d440", "AX-REA", "an anchor of the reach-and-manipulation axis; the need's obligation is no fine-motor or drag-only interaction")]),
 dict(i="MOB", n="A-SELFCARE", kind="M", qn="bathing, dressing, toileting, eating", qi="wheelchair users",
      why="the identity's map holds washing and toileting activity codes and the need's registry text names bathing and toileting",
      codes=[("d510", None, None), ("d530", None, None), ("e115", None, None), ("e150", None, None), ("e340", None, None)]),
 dict(i="SCI", n="A-SELFCARE", kind="M", qn="bathing, dressing, toileting, eating", qi="Spinal cord injury",
      why="the identity's map holds washing and toileting activity codes and the need's registry text names bathing and toileting",
      codes=[("d510", None, None), ("d530", None, None), ("e115", None, None), ("e150", None, None), ("e340", None, None)]),
 dict(i="LMB", n="A-SELFCARE", kind="M", qn="bathing, dressing, toileting, eating", qi="upper-limb disabilities",
      why="the identity's map holds washing and dressing activity codes that the need's own rows also hold",
      codes=[("d510", None, None), ("d540", None, None), ("e115", None, None), ("e150", None, None), ("e340", None, None)]),
 # ---- pacing
 dict(i="ADHD", n="A-LOWLOAD", kind="E2", qn="ADHD", qi="ADHD",
      why="the need's registry text names ADHD and the identity is people with ADHD",
      codes=[("b140", "AX-SPR", "the attention-function anchor of the sensory-load axis; the need's obligation keeps attention demand low"),
             ("e150", None, None)]),
 dict(i="DEM", n="A-LOWLOAD", kind="E2", qn="dementia", qi="Alzheimer disease and related dementias",
      why="the need's registry text names dementia and the identity is people living with dementia",
      codes=[("b144", "AX-COG-O", "the memory-function anchor of the orientation axis; the need's obligation keeps memory demand low"),
             ("d460", None, None), ("d230", None, None), ("e150", None, None)]),
 dict(i="BRAIN", n="A-LOWLOAD", kind="E2", qn="brain injury", qi="acquired brain injury",
      why="the need's registry text names brain injury and the identity is people with acquired brain injury",
      codes=[("b144", "AX-COG-O", "the memory-function anchor of the orientation axis; the need's obligation keeps memory demand low"),
             ("d230", None, None), ("e150", None, None)]),
 dict(i="ID", n="A-LOWLOAD", kind="E2", qn="intellectual disability", qi="First-class",
      why="the need's registry text names intellectual disability and the identity is people with intellectual disability",
      codes=[("b117", "AX-COG-L", "an anchor of the information-access axis (comprehension load)"), ("e150", None, None)]),
 dict(i="COM", n="A-TIME", kind="E3", qn="brain fog impairs organizing time", qi="long COVID",
      why="the need's own ICF row records the owner's rationale that brain fog impairs organizing time; that the identity (complex, energy-limiting conditions including long COVID and ME/CFS) carries brain fog is not stated in a project record, so this pair is an inference for the owner to confirm",
      codes=[("b164", None, None)]),
 dict(i="COM", n="A-EFFORT", kind="E1", qn="ME/CFS, Long COVID, POTS", qi="long COVID, MCAS, ME/CFS",
      why="the need's registry text names ME/CFS, Long COVID and POTS and the identity's description lists the same conditions",
      codes=[("d450", None, None), ("d455", None, None),
             ("b455", "AX-STA", "the exercise-tolerance anchor of the sustained-exertion axis, the demand this need lowers"),
             ("b130", "AX-STA", "the energy-and-drive anchor of the sustained-exertion axis, the demand this need lowers"),
             ("e120", None, None), ("e150", None, None)]),
 dict(i="MS", n="A-EFFORT", kind="E2", qn="MS fatigue", qi="fatigue",
      why="the need's registry text names MS fatigue and the identity's description names fatigue",
      codes=[("b455", "AX-STA", "the exercise-tolerance anchor of the sustained-exertion axis, the demand this need lowers"),
             ("b130", "AX-STA", "the energy-and-drive anchor of the sustained-exertion axis, the demand this need lowers"),
             ("e120", None, None), ("e150", None, None)]),
 dict(i="PAIN", n="A-EFFORT", kind="E2", qn="pain", qi="sustained discomfort affecting endurance",
      why="the need's registry text names pain and the identity's description says pain affects endurance",
      codes=[("d450", None, None), ("d455", None, None),
             ("b280", "AX-PAI", "the pain-sensation anchor of the pain-load axis"), ("e120", None, None), ("e150", None, None)]),
 # ---- environment and safety
 dict(i="AUT", n="A-STIMULUS", kind="E2", qn="autistic people", qi="Autism spectrum",
      why="the need's registry text names autistic people and the identity is autistic people",
      codes=[("d230", None, None),
             ("b156", "AX-SPR", "the perceptual-function anchor of the sensory-load axis"),
             ("e150", None, None), ("e240", None, None), ("e250", None, None)]),
 dict(i="NDV", n="A-STIMULUS", kind="E2", qn="sensory processing differences", qi="neurodivergent",
      why="the need's registry text names sensory processing differences and the identity's map mechanism is sensory processing",
      codes=[("d230", None, None),
             ("b156", "AX-SPR", "the perceptual-function anchor of the sensory-load axis"),
             ("e150", None, None), ("e240", None, None), ("e250", None, None)]),
 dict(i="BRAIN", n="A-STIMULUS", kind="E2", qn="post-concussion", qi="post-concussion",
      why="the need's registry text names post-concussion and the identity's description includes post-concussion",
      codes=[("b156", "AX-SPR", "the perceptual-function anchor of the sensory-load axis"),
             ("e150", None, None), ("e240", None, None), ("e250", None, None)]),
 dict(i="MH", n="A-STIMULUS", kind="E2", qn="PTSD", qi="trauma",
      why="the need's registry text names PTSD and the identity's description includes trauma",
      codes=[("d230", None, None), ("e150", None, None), ("e240", None, None), ("e250", None, None)]),
 dict(i="EPI", n="A-TRIGGER", kind="E1", qn="photosensitive epilepsy", qi="photosensitivity",
      why="the need's registry text names photosensitive epilepsy and the identity's description names photosensitivity as a subtype; the need's e240 row is annotated flash/strobe",
      codes=[("e240", None, None)]),
 dict(i="COM", n="A-TRIGGER", kind="E1", qn="MCAS", qi="MCAS",
      why="the need's registry text names MCAS and the identity's description lists MCAS; the need's e260 row concerns airborne exposure",
      codes=[("e260", None, None),
             ("b435", "AX-CHM", "an anchor of the airborne-exposure axis"), ("b440", "AX-CHM", "an anchor of the airborne-exposure axis")]),
 dict(i="MH", n="A-CALM", kind="E2", qn="anxiety, PTSD, psychiatric distress", qi="Mood, anxiety, trauma",
      why="the need's registry text names anxiety, PTSD and psychiatric distress and the identity's description names mood, anxiety and trauma",
      codes=[("b152", "AX-ARO", "the emotional-function anchor of the arousal-safety axis"),
             ("d240", "AX-ARO", "the stress-handling anchor of the arousal-safety axis"),
             ("d230", None, None), ("e150", None, None)]),
 dict(i="AUT", n="A-CALM", kind="E2", qn="autistic people", qi="Autism spectrum",
      why="the need's registry text names autistic people and the identity is autistic people",
      codes=[("d230", None, None), ("d240", "AX-ARO", "the stress-handling anchor of the arousal-safety axis"), ("e150", None, None)]),
 dict(i="LPA", n="A-SIZE", kind="E1", qn="little people", qi="Served by A-SIZE",
      why="the identity's description says it is served by this need and the need's registry text names little people; no ICF code is recorded for body size, so only the need's own environmental codes are proposed",
      codes=[("e115", None, None), ("e120", None, None), ("e150", None, None), ("e155", None, None)]),
 dict(i="TALL", n="A-SIZE", kind="E1", qn="tall people", qi="Served by A-SIZE",
      why="the identity's description says it is served by this need and the need's registry text names tall people; no ICF code is recorded for body size, so only the need's own environmental codes are proposed",
      codes=[("e115", None, None), ("e120", None, None), ("e150", None, None), ("e155", None, None)]),
 dict(i="BAR", n="A-SIZE", kind="E1", qn="fat people", qi="Served by A-SIZE",
      why="the identity's description says it is served by this need and the need's registry text names fat people; no ICF code is recorded for body size, so only the need's own environmental codes are proposed",
      codes=[("e115", None, None), ("e120", None, None), ("e150", None, None), ("e155", None, None)]),
]

def anchors():
    """axis -> set of ICF codes, parsed from the 2.1 axis register of governance/functional-taxonomy.md."""
    out = {}
    for ln in (ROOT / "governance/functional-taxonomy.md").read_text().splitlines():
        m = re.match(r"\|\s*`(AX-[A-Z-]+)`\s*\|[^|]*\|([^|]*)\|", ln)
        if m:
            out[m.group(1)] = set(re.findall(r"\b[bde]\d{3,4}\b", m.group(2)))
    return out

def main():
    c = sqlite3.connect(f"file:{ROOT}/data/guidebook.db?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    ax = anchors()
    idn = {r["identity_code"]: r for r in c.execute("select * from base_taxonomy_identity where status='active'")}
    need = {r["need_code"]: r for r in c.execute("select * from access_needs")}
    icf = {r["icf_code"]: r for r in c.execute("select * from base_icf")}
    imap, nmap = {}, {}
    for r in c.execute("select * from identity_icf_map where retired_at is null order by link_id"):
        imap.setdefault((r["identity_code"], r["icf_code"]), []).append(r)
    for r in c.execute("select * from access_need_icf"):
        nmap[(r["need_code"], r["icf_code"])] = r
    nrows = {}
    for r in c.execute("select need_code, notes from access_need_icf"):
        nrows.setdefault(r["need_code"], []).append(r["notes"] or "")
    errors, triples, seen = [], [], set()
    for p in PAIRS:
        I, N = p["i"], p["n"]
        if I not in idn: errors.append(f"{I}: not an active identity"); continue
        if N not in need: errors.append(f"{N}: not a need"); continue
        ntext = " | ".join(filter(None, [need[N]["absorbs"], need[N]["design_obligation"], need[N]["notes"]] + nrows.get(N, [])))
        itext = " | ".join(filter(None, [idn[I]["display_name"], idn[I]["description"]] +
                                      [r["mechanism"] for (ii, _), rs in imap.items() if ii == I for r in rs]))
        if p["qn"] not in ntext: errors.append(f"{I}x{N}: need quote not found in the need's records: {p['qn']!r}")
        if p["qi"] not in itext: errors.append(f"{I}x{N}: identity quote not found in the identity's records: {p['qi']!r}")
        for code, axis, reason in p["codes"]:
            if code not in icf: errors.append(f"{I}x{N}x{code}: code not in base_icf"); continue
            if (I, N, code) in seen: errors.append(f"{I}x{N}x{code}: listed twice"); continue
            seen.add((I, N, code))
            facts = []
            if (I, code) in imap:
                rs = imap[(I, code)]
                facts.append(f"identity_icf_map link {'/'.join(str(r['link_id']) for r in rs)} ties {I} to {code} "
                             f"({rs[0]['mapping_confidence']}; mechanism: {rs[0]['mechanism']})")
            if (N, code) in nmap:
                r = nmap[(N, code)]
                facts.append(f"access_need_icf holds {N} -> {code} ({r['confidence']}"
                             + (f"; note: {r['notes']}" if r["notes"] else "") + ")")
            if not facts:
                if not axis or not reason:
                    errors.append(f"{I}x{N}x{code}: neither map holds it, so it needs an axis and a reason"); continue
                if code not in ax.get(axis, set()):
                    errors.append(f"{I}x{N}x{code}: {axis} does not list {code} among its ICF anchors"); continue
                facts.append(f"neither map holds this pair; governance/functional-taxonomy.md 2.1 lists {code} among the "
                             f"ICF anchors of {axis}, {reason}")
            warrant = (f"Judged {p['kind']} by {SESSION}: {p['why']}. Need {N} absorbs: \"{p['qn']}\"; identity {I}: "
                       f"\"{p['qi']}\". Code {code}: " + "; ".join(facts) + ". A proposal for the owner's review, not a determination.")
            triples.append(dict(identity=I, need=N, icf=code, kind=p["kind"], warrant=warrant,
                                support=("both maps" if (I, code) in imap and (N, code) in nmap else
                                         "identity map" if (I, code) in imap else
                                         "need map" if (N, code) in nmap else "taxonomy anchor")))
    if errors:
        print("REFUSED:"); [print(" ", e) for e in errors]; sys.exit(1)
    OUT.write_text(json.dumps(triples, ensure_ascii=False, indent=1))
    from collections import Counter
    print(f"triples: {len(triples)}  pairs: {len(PAIRS)}")
    print("by support:", dict(Counter(t["support"] for t in triples)))
    print("by kind:   ", dict(Counter(t["kind"] for t in triples)))
    print("identities:", len({t['identity'] for t in triples}), " needs:", len({t['need'] for t in triples}))
    print("max warrant length:", max(len(t["warrant"]) for t in triples))

main()
