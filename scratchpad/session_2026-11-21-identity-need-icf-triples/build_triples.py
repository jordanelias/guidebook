"""Build the proposed identity x access-need x ICF triples (T-145 research batch), second version.

Reads data/guidebook.db read-only and governance/functional-taxonomy.md; writes triples.json (rows to propose) and
withheld.json (rows held back for an owner question); prints a preview. Writes NOTHING to the database.

Judged (PAIRS): which identity a need serves, why, and which ICF codes carry it. Derived: every quotation (must be a
substring of a live record), every pointer (identity_icf_map link ids, access_need_icf membership), every taxonomy
anchor and the axis's status (parsed from governance/functional-taxonomy.md 2.1), every recorded ICF title.

Rules the script enforces (each answers a finding of the adversarial pass of this session):
  * A code held in neither map must name an axis whose anchors list it. A code held only in the identity map, or only
    by an axis anchor, must carry a stated tie to the need, in words, with no ICF title from memory.
  * A need-side activity or function code (d, b) is proposed for an identity only where that identity's own map holds
    the same code; need-side environmental codes (e) are proposed for every judged pair.
  * A code held by more than half of the needs (derived) is dropped: it distinguishes no pair.
  * Body-function (b) codes are WITHHELD, not proposed: identity_icf_map holds activity (d) codes only, and
    functional-taxonomy.md 0.5 says axes describe specifications, never a portrait of a person. The owner decides.
  * A-AT is not paired: its registry note flags it as possibly outside the built environment, for the owner.
    ALL is a scope marker, not an identity. NDV is not paired where its codes would copy a member's (AUT).
"""
import json, re, sqlite3, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent
OUT, OUTW = HERE / "triples.json", HERE / "withheld.json"

# codes: (code, axis_or_None, tie_or_None). tie required unless the need's own map holds the code.
# rec: extra (path, substring) records the why leans on, each verified present.
MEMBER = " The named condition is one member of this identity; the row is keyed on the whole identity, and whether the link holds for each member is for the owner to confirm."
PAIRS = [
 dict(i="BLIND", n="A-NOSIGHT", qn="blindness, low vision", qi="blind and low-vision people",
      why="The need's registry text names blindness and low vision, and the identity is blind and low-vision people.",
      codes=[("b210", "AX-VIS-N", "the function the need replaces for a person without sight"),
             ("d460", "AX-VIS-N", "the identity's map holds it for spatial orientation and AX-VIS-N lists it; the need makes information perceivable without sight"),
             ("d310–d329", None, "the identity's map holds it for information access, and the need's obligation is text alternatives, braille and a logical reading order"),
             ("e240", None, None), ("e125", None, None), ("e155", None, None)]),
 dict(i="DEAF", n="A-NOSOUND", qn="Deaf, hard of hearing, late-deafened", qi="Deaf, or late-deafened",
      why="The need's registry text names Deaf, hard-of-hearing and late-deafened people.",
      codes=[("b230", "AX-AUD", "the function the need replaces for a person who does not hear"),
             ("d310–d329", None, "the identity's map holds it for communication and alert receipt, and the need's obligation is captions, transcripts and visual alerts"),
             ("e250", None, None), ("e1251", None, None), ("e125", None, None)]),
 dict(i="DEAFBLIND", n="A-TACTILE", qn="DeafBlind (Protactile)", qi="Not VIS+DEAF",
      why="The need's registry text names DeafBlind (Protactile) access and the identity's description says it is not blindness plus deafness. The need's own note records that DeafBlind access is distinct, and functional-taxonomy.md 4 maps DBL to VIS-N x AUD at compound weight, so only the need's environmental codes are proposed.",
      codes=[("e340", None, None), ("e155", None, None)]),
 dict(i="VES", n="A-STABLE", qn="vestibular disorders", qi="Served primarily by A-STABLE",
      why="The identity's description says it is served primarily by this need, and the need's registry text names vestibular disorders.",
      codes=[("b235", "AX-BAL", "the balance axis lists it and the need holds the visual reference still"),
             ("d415", "AX-BAL", "the balance axis lists it, and the need's obligation includes handrails and signalled level changes"),
             ("e240", None, None)]),
 dict(i="BRAIN", n="A-STABLE", qn="post-concussion", qi="post-concussion",
      why="The need's registry text names post-concussion and the identity's description includes post-concussion; functional-taxonomy.md 4 maps PCS-TBI to BAL." + MEMBER,
      rec=[("governance/functional-taxonomy.md", "`PCS-TBI` (post-concussion) | BAL")],
      codes=[("b235", "AX-BAL", "the balance axis lists it"),
             ("d415", "AX-BAL", "the balance axis lists it, and the need's obligation includes handrails and signalled level changes"),
             ("e240", None, None)]),
 dict(i="BRAIN", n="A-NOSPEECH", qn="aphasia", qi="stroke",
      why="The need's registry text names aphasia and the identity's description includes stroke. populations.json (neurological and acquired brain injury profile) lists \"stroke sequelae (unilateral neglect, navigation impairment, aphasia, hemiplegia)\", and functional-taxonomy.md 4 maps NEU to COM-E but also lists aphasia/dysarthria (COM-E) as a deferred candidate profile, so aphasia is not yet filed under any identity." + MEMBER,
      rec=[("references/website/data/populations.json", "stroke sequelae (unilateral neglect, navigation impairment, aphasia, hemiplegia)"),
           ("governance/functional-taxonomy.md", "aphasia/dysarthria (COM-E)")],
      codes=[("d330", "AX-COM-E", "the axis for producing speech lists it, and the need's obligation is never to require speech"),
             ("d350", "AX-COM-E", "the axis for producing speech lists it, and the need's obligation is never to require speech"),
             ("e125", None, None), ("e340", None, None)]),
 dict(i="ID", n="A-PLAIN", qn="intellectual disability", qi="people with intellectual disability",
      why="The need's registry text names intellectual disability and the identity is people with intellectual disability.",
      codes=[("b117", "AX-COG-L", "the information-access axis lists it"), ("e155", None, None)]),
 dict(i="DEM", n="A-PLAIN", qn="dementia", qi="Cognitive — memory, attention, wayfinding, sequencing",
      why="The need's registry text names dementia and the identity is people living with dementia; the identity's map and the need's signage row both mention wayfinding.",
      codes=[("b117", "AX-COG-L", "the information-access axis lists it"),
             ("d460", None, "the identity's map holds it for wayfinding, and the need's signage row is annotated wayfinding"),
             ("e155", None, None)]),
 dict(i="BRAIN", n="A-PLAIN", qn="brain injury", qi="acquired brain injury",
      why="The need's registry text names brain injury and the identity is people with acquired brain injury.",
      codes=[("b117", "AX-COG-L", "the information-access axis lists it"), ("e155", None, None)]),
 dict(i="MOB", n="A-REACH", qn="wheelchair users, ambulatory wheelchair users, cane/crutch users", qi="wheelchair users",
      why="The need's registry text names wheelchair users, ambulatory wheelchair users and cane/crutch users, and the identity is people with mobility needs including wheelchair users.",
      codes=[("d465", None, "the identity's map holds it for wheelchair use, which the need's registry text names"),
             ("d420", None, "the identity's map holds it for transfer, and the need asks for seated-height controls and clearance"),
             ("d450", None, "the identity's map holds it for ambulation, and the need names ambulatory wheelchair and cane/crutch users"),
             ("e120", None, None), ("e155", None, None)]),
 dict(i="SCI", n="A-REACH", qn="wheelchair users", qi="paraplegia or tetraplegia",
      why="The need's registry text names wheelchair users; the identity is people with spinal cord injuries (paraplegia or tetraplegia), and functional-taxonomy.md 4 maps SCI to WHM and REA.",
      rec=[("governance/functional-taxonomy.md", "WHM, REA, THR, CNT, PAI")],
      codes=[("d465", None, "the identity's map holds it for wheelchair use, which the need's registry text names"),
             ("d420", None, "the identity's map holds it for transfer, and the need asks for seated-height controls and clearance"),
             ("d450", None, "the identity's map holds it for ambulation, and the need names ambulatory wheelchair and cane/crutch users"),
             ("e120", None, None), ("e155", None, None)]),
 dict(i="LMB", n="A-REACH", qn="limb difference", qi="limb differences",
      why="The need's registry text names limb difference and the identity is people with limb differences.",
      codes=[("d440", None, "the identity's map holds it for grip, force and bilateral function, and the need asks for one-handed operation"),
             ("d445", None, "the identity's map holds it for grip, force and bilateral function, and the need asks for one-handed operation"),
             ("e120", None, None), ("e155", None, None)]),
 dict(i="MOVE", n="A-PRECISION", qn="tremor, dystonia, Parkinson's", qi="Pairs with A-PRECISION",
      why="The identity's description says it pairs with this need, and the need's registry text names tremor, dystonia and Parkinson's.",
      codes=[("b765", None, None),
             ("d440", "AX-REA", "the reach-and-manipulation axis lists it, and the need's obligation is no fine-motor or drag-only interaction"),
             ("e115", None, None)]),
 dict(i="MOB", n="A-SELFCARE", qn="bathing, dressing, toileting, eating", qi="wheelchair users",
      why="The need's registry text names bathing and toileting, the identity's map holds washing and toileting activity codes, and the identity includes wheelchair users.",
      codes=[("d510", None, None), ("d530", None, "the identity's map holds it and the need's registry text names toileting"),
             ("e115", None, None), ("e340", None, None)]),
 dict(i="SCI", n="A-SELFCARE", qn="bathing, dressing, toileting, eating", qi="paraplegia or tetraplegia",
      why="The need's registry text names bathing and toileting, and the identity's map holds washing and toileting activity codes.",
      codes=[("d510", None, None), ("d530", None, "the identity's map holds it and the need's registry text names toileting"),
             ("e115", None, None), ("e340", None, None)]),
 dict(i="LMB", n="A-SELFCARE", qn="bathing, dressing, toileting, eating", qi="upper-limb disabilities",
      why="The need's registry text names bathing and dressing, and the identity's map holds washing and dressing activity codes.",
      codes=[("d510", None, None), ("d540", None, None), ("e115", None, None), ("e340", None, None)]),
 dict(i="DEM", n="A-LOWLOAD", qn="dementia", qi="Cognitive — memory, attention, wayfinding, sequencing",
      why="The need's registry text names dementia and the identity is people living with dementia; the identity's map and the need's wayfinding row both mention wayfinding.",
      codes=[("b144", "AX-COG-O", "the orientation axis lists it, and the need's obligation keeps memory demand low"),
             ("d460", None, "the identity's map holds it for wayfinding, and the need's wayfinding row is annotated wayfinding")]),
 dict(i="ADHD", n="A-LOWLOAD", qn="ADHD", qi="ADHD",
      why="The need's registry text names ADHD and the identity is people with ADHD.",
      codes=[("b140", "AX-SPR", "the sensory-load axis lists it, and the need's obligation keeps attention demand low")]),
 dict(i="BRAIN", n="A-LOWLOAD", qn="brain injury", qi="acquired brain injury",
      why="The need's registry text names brain injury and the identity is people with acquired brain injury.",
      codes=[("b144", "AX-COG-O", "the orientation axis lists it, and the need's obligation keeps memory demand low")]),
 dict(i="ID", n="A-LOWLOAD", qn="intellectual disability", qi="people with intellectual disability",
      why="The need's registry text names intellectual disability and the identity is people with intellectual disability.",
      codes=[("b117", "AX-COG-L", "the information-access axis lists it")]),
 dict(i="COM", n="A-TIME", qn="brain fog impairs organizing time", qi="long COVID",
      why="The need's own ICF row (access_need_icf, A-TIME to b164) records the owner's rationale that brain fog impairs organizing time; the identity's description lists long COVID and ME/CFS. That the identity carries brain fog is not stated in a project record, so this pair is an inference for the owner to confirm." + MEMBER,
      codes=[("b164", None, None)]),
 dict(i="COM", n="A-EFFORT", qn="ME/CFS, Long COVID, POTS", qi="long COVID, MCAS, ME/CFS",
      why="The need's registry text names ME/CFS, Long COVID and POTS, and the identity's description lists the same conditions.",
      codes=[("d450", None, "the identity's map holds it for exertion limits, and the need asks for short paths and rest points"),
             ("d455", None, "the identity's map holds it for exertion limits, and the need asks for short paths and rest points"),
             ("b455", "AX-STA", "the sustained-exertion axis lists it"), ("b130", "AX-STA", "the sustained-exertion axis lists it"),
             ("e120", None, None)]),
 dict(i="MS", n="A-EFFORT", qn="MS fatigue", qi="fatigue",
      why="The need's registry text names MS fatigue and the identity's description names fatigue.",
      codes=[("b455", "AX-STA", "the sustained-exertion axis lists it"), ("b130", "AX-STA", "the sustained-exertion axis lists it"),
             ("e120", None, None)]),
 dict(i="PAIN", n="A-EFFORT", qn="pain", qi="sustained discomfort affecting endurance",
      why="The need's registry text names pain and the identity's description says pain affects endurance.",
      codes=[("d450", None, "the identity's map holds it for pain-limited endurance, and the need asks for short paths and rest points"),
             ("d455", None, "the identity's map holds it for pain-limited endurance, and the need asks for short paths and rest points"),
             ("b280", "AX-PAI", "the pain-load axis lists it"), ("e120", None, None)]),
 dict(i="AUT", n="A-STIMULUS", qn="autistic people", qi="Autism spectrum",
      why="The need's registry text names autistic people and the identity is autistic people.",
      codes=[("d230", "AX-SPR", "the identity's map holds it for environment consistency and the sensory-load axis lists it"),
             ("b156", "AX-SPR", "the sensory-load axis lists it"), ("e240", None, None), ("e250", None, None)]),
 dict(i="BRAIN", n="A-STIMULUS", qn="post-concussion", qi="post-concussion",
      why="The need's registry text names post-concussion and the identity's description includes post-concussion." + MEMBER,
      codes=[("b156", "AX-SPR", "the sensory-load axis lists it"), ("e240", None, None), ("e250", None, None)]),
 dict(i="MH", n="A-STIMULUS", qn="PTSD", qi="trauma",
      why="The need's registry text names PTSD and the identity's description names trauma." + MEMBER,
      codes=[("d230", "AX-SPR", "the identity's map holds it for sensory safety and the sensory-load axis lists it"),
             ("e240", None, None), ("e250", None, None)]),
 dict(i="EPI", n="A-TRIGGER", qn="photosensitive epilepsy", qi="photosensitivity",
      why="The need's registry text names photosensitive epilepsy and the identity's description names photosensitivity as a subtype; the need's e240 row is annotated flash/strobe.",
      codes=[("e240", None, None)]),
 dict(i="COM", n="A-TRIGGER", qn="MCAS", qi="MCAS",
      why="The need's registry text names MCAS, the identity's description lists MCAS, and functional-taxonomy.md 4 maps MCAS to CHM." + MEMBER,
      rec=[("governance/functional-taxonomy.md", "MCAS | OFS/MCAS | PROFILE (diagnostic) | **CHM primary**")],
      codes=[("e260", None, None), ("b435", "AX-CHM", "the airborne-exposure axis lists it"), ("b440", "AX-CHM", "the airborne-exposure axis lists it")]),
 dict(i="MH", n="A-CALM", qn="anxiety, PTSD, psychiatric distress", qi="Mood, anxiety, trauma",
      why="The need's registry text names anxiety, PTSD and psychiatric distress, and the identity's description names mood, anxiety and trauma.",
      codes=[("b152", "AX-ARO", "the arousal-safety axis lists it"),
             ("d240", "AX-ARO", "the arousal-safety axis lists it, and the need's obligation is not to manufacture pressure")]),
 dict(i="AUT", n="A-CALM", qn="autistic people", qi="Autism spectrum",
      why="The need's registry text names autistic people and the identity is autistic people; functional-taxonomy.md 4 maps AUT to ARO.",
      codes=[("b152", "AX-ARO", "the arousal-safety axis lists it"),
             ("d240", "AX-ARO", "the arousal-safety axis lists it, and the need's obligation is not to manufacture pressure")]),
] + [
 dict(i=i, n="A-SIZE", qn=q, qi="Served by A-SIZE",
      why=f"The identity's description says it is served by this need and the need's registry text names {q}. No ICF code is recorded for body size, so only the need's own environmental codes are proposed.",
      codes=[("e115", None, None), ("e120", None, None), ("e155", None, None)])
 for i, q in (("LPA", "little people"), ("TALL", "tall people"), ("BAR", "fat people"))
] + [
 dict(i="MOB", n="A-SIZE", qn="wheelchair seating height", qi="wheelchair users",
      why="The need's registry text names wheelchair seating height and the identity includes wheelchair users.",
      codes=[("d465", None, "the identity's map holds it for wheelchair use, and the need's registry text names wheelchair seating height"),
             ("e120", None, None)]),
]


def anchors():
    out, status = {}, {}
    for ln in (ROOT / "governance/functional-taxonomy.md").read_text().splitlines():
        m = re.match(r"\|\s*`(AX-[A-Z-]+)`\s*\|[^|]*\|([^|]*)\|([^|]*)\|\s*([A-Z]+)\s*\|", ln)
        if m:
            out[m.group(1)] = set(re.findall(r"\b[bde]\d{3,4}\b", m.group(2)))
            status[m.group(1)] = m.group(4)
    return out, status


def main():
    c = sqlite3.connect(f"file:{ROOT}/data/guidebook.db?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    ax, axstat = anchors()
    idn = {r["identity_code"]: r for r in c.execute("select * from base_taxonomy_identity where status='active'")}
    need = {r["need_code"]: r for r in c.execute("select * from access_needs")}
    icf = {r["icf_code"]: r for r in c.execute("select * from base_icf")}
    imap, nmap = {}, {}
    for r in c.execute("select * from identity_icf_map where retired_at is null order by link_id"):
        imap.setdefault((r["identity_code"], r["icf_code"]), []).append(r)
    for r in c.execute("select * from access_need_icf"):
        nmap[(r["need_code"], r["icf_code"])] = r
    nneeds = c.execute("select count(*) from access_needs").fetchone()[0]
    held = {}
    for (n, code) in nmap: held.setdefault(code, set()).add(n)
    common = {code for code, ns in held.items() if len(ns) * 2 > nneeds}
    errors, triples, withheld, dropped, seen = [], [], [], [], set()
    for p in PAIRS:
        I, N = p["i"], p["n"]
        if I not in idn: errors.append(f"{I}: not an active identity"); continue
        if N not in need: errors.append(f"{N}: not a need"); continue
        ntext = " | ".join(filter(None, [need[N]["absorbs"], need[N]["design_obligation"], need[N]["notes"]] +
                                  [r["notes"] for (nn, _), r in nmap.items() if nn == N]))
        itext = " | ".join(filter(None, [idn[I]["display_name"], idn[I]["description"]] +
                                  [r["mechanism"] for (ii, _), rs in imap.items() if ii == I for r in rs]))
        if p["qn"] not in ntext: errors.append(f"{I}x{N}: need quote not found in the need's records: {p['qn']!r}")
        if p["qi"] not in itext: errors.append(f"{I}x{N}: identity quote not found in the identity's records: {p['qi']!r}")
        for path, sub in p.get("rec", []):
            if sub not in (ROOT / path).read_text(): errors.append(f"{I}x{N}: record {path} lacks {sub!r}")
        for code, axis, tie in p["codes"]:
            if code not in icf: errors.append(f"{I}x{N}x{code}: code not in base_icf"); continue
            if (I, N, code) in seen: errors.append(f"{I}x{N}x{code}: listed twice"); continue
            seen.add((I, N, code))
            in_i, in_n = (I, code) in imap, (N, code) in nmap
            if code in common:
                dropped.append(f"{I}|{N}|{code} (held by {len(held[code])} of {nneeds} needs)"); continue
            if code[0] in "db" and in_n and not in_i and (I, N, code) and not tie and code[0] == "d":
                pass
            parts = []
            if in_n and code[0] in "db" and not in_i and code[0] == "d":
                dropped.append(f"{I}|{N}|{code} (need-map activity code; the identity's map does not hold it)"); continue
            if in_n:
                r = nmap[(N, code)]
                parts.append(f"access_need_icf holds {N} -> {code}" + (f" (annotated: {r['notes']})" if r["notes"] else ""))
            if in_i:
                parts.append("identity_icf_map link " + "/".join(str(r["link_id"]) for r in imap[(I, code)]) + f" holds it for {I}")
            if axis:
                if code not in ax.get(axis, set()):
                    errors.append(f"{I}x{N}x{code}: {axis} does not list {code} among its ICF anchors"); continue
                parts.append(f"{axis} (status {axstat[axis]}) lists it among its ICF anchors in governance/functional-taxonomy.md 2.1")
            if not in_n:
                if not tie: errors.append(f"{I}x{N}x{code}: not held by the need's map, so it needs a stated tie"); continue
                if not (in_i or axis): errors.append(f"{I}x{N}x{code}: neither map nor anchor holds it"); continue
                parts.append("tie: " + tie)
            title = icf[code]["title"] if icf[code]["title_source"] and "skills/" in (icf[code]["title_source"] or "") else None
            head = f"Code {code}" + (f" (title recorded in base_icf: \"{title}\")" if title else "")
            warrant = f"{p['why']} Need {N} registry text: \"{p['qn']}\". Identity {I}: \"{p['qi']}\". {head}: " + "; ".join(parts) + "."
            row = dict(identity=I, need=N, icf=code, warrant=warrant,
                       support=("both maps" if in_i and in_n else "identity map" if in_i else "need map" if in_n else "taxonomy anchor"))
            (withheld if code[0] == "b" else triples).append(row)
    if errors:
        print("REFUSED:"); [print(" ", e) for e in errors]; sys.exit(1)
    OUT.write_text(json.dumps(triples, ensure_ascii=False, indent=1))
    OUTW.write_text(json.dumps(withheld, ensure_ascii=False, indent=1))
    from collections import Counter
    print(f"proposed: {len(triples)}  withheld (b-codes): {len(withheld)}  pairs: {len(PAIRS)}")
    print("dropped:", len(dropped)); [print("  ", d) for d in dropped]
    print("by support:", dict(Counter(t["support"] for t in triples)))
    print("identities proposed:", sorted({t['identity'] for t in triples}))
    print("needs proposed:", sorted({t['need'] for t in triples}))
    print("max warrant length:", max(len(t["warrant"]) for t in triples))

main()
